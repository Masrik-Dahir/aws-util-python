"""Native async IAM utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.iam import (
    CreateAccessKeyResult,
    CreateDelegationRequestResult,
    CreateGroupResult,
    CreateInstanceProfileResult,
    CreateLoginProfileResult,
    CreateOpenIdConnectProviderResult,
    CreatePolicyVersionResult,
    CreateSamlProviderResult,
    CreateServiceLinkedRoleResult,
    CreateServiceSpecificCredentialResult,
    CreateUserResult,
    CreateVirtualMfaDeviceResult,
    DeleteServiceLinkedRoleResult,
    DisableOrganizationsRootCredentialsManagementResult,
    DisableOrganizationsRootSessionsResult,
    EnableOrganizationsRootCredentialsManagementResult,
    EnableOrganizationsRootSessionsResult,
    GenerateCredentialReportResult,
    GenerateOrganizationsAccessReportResult,
    GenerateServiceLastAccessedDetailsResult,
    GetAccessKeyLastUsedResult,
    GetAccountAuthorizationDetailsResult,
    GetAccountPasswordPolicyResult,
    GetAccountSummaryResult,
    GetContextKeysForCustomPolicyResult,
    GetContextKeysForPrincipalPolicyResult,
    GetCredentialReportResult,
    GetGroupPolicyResult,
    GetGroupResult,
    GetInstanceProfileResult,
    GetLoginProfileResult,
    GetMfaDeviceResult,
    GetOpenIdConnectProviderResult,
    GetOrganizationsAccessReportResult,
    GetPolicyResult,
    GetPolicyVersionResult,
    GetRolePolicyResult,
    GetSamlProviderResult,
    GetServerCertificateResult,
    GetServiceLastAccessedDetailsResult,
    GetServiceLastAccessedDetailsWithEntitiesResult,
    GetServiceLinkedRoleDeletionStatusResult,
    GetSshPublicKeyResult,
    GetUserPolicyResult,
    GetUserResult,
    IAMPolicy,
    IAMRole,
    IAMUser,
    ListAccessKeysResult,
    ListAccountAliasesResult,
    ListAttachedGroupPoliciesResult,
    ListAttachedRolePoliciesResult,
    ListAttachedUserPoliciesResult,
    ListEntitiesForPolicyResult,
    ListGroupPoliciesResult,
    ListGroupsForUserResult,
    ListGroupsResult,
    ListInstanceProfilesForRoleResult,
    ListInstanceProfilesResult,
    ListInstanceProfileTagsResult,
    ListMfaDevicesResult,
    ListMfaDeviceTagsResult,
    ListOpenIdConnectProvidersResult,
    ListOpenIdConnectProviderTagsResult,
    ListOrganizationsFeaturesResult,
    ListPoliciesGrantingServiceAccessResult,
    ListPolicyTagsResult,
    ListPolicyVersionsResult,
    ListRolePoliciesResult,
    ListRoleTagsResult,
    ListSamlProvidersResult,
    ListSamlProviderTagsResult,
    ListServerCertificatesResult,
    ListServerCertificateTagsResult,
    ListServiceSpecificCredentialsResult,
    ListSigningCertificatesResult,
    ListSshPublicKeysResult,
    ListUserPoliciesResult,
    ListUserTagsResult,
    ListVirtualMfaDevicesResult,
    ResetServiceSpecificCredentialResult,
    SimulateCustomPolicyResult,
    SimulatePrincipalPolicyResult,
    UpdateRoleDescriptionResult,
    UpdateSamlProviderResult,
    UploadServerCertificateResult,
    UploadSigningCertificateResult,
    UploadSshPublicKeyResult,
    _parse_policy,
    _parse_role,
)

__all__ = [
    "CreateAccessKeyResult",
    "CreateDelegationRequestResult",
    "CreateGroupResult",
    "CreateInstanceProfileResult",
    "CreateLoginProfileResult",
    "CreateOpenIdConnectProviderResult",
    "CreatePolicyVersionResult",
    "CreateSamlProviderResult",
    "CreateServiceLinkedRoleResult",
    "CreateServiceSpecificCredentialResult",
    "CreateUserResult",
    "CreateVirtualMfaDeviceResult",
    "DeleteServiceLinkedRoleResult",
    "DisableOrganizationsRootCredentialsManagementResult",
    "DisableOrganizationsRootSessionsResult",
    "EnableOrganizationsRootCredentialsManagementResult",
    "EnableOrganizationsRootSessionsResult",
    "GenerateCredentialReportResult",
    "GenerateOrganizationsAccessReportResult",
    "GenerateServiceLastAccessedDetailsResult",
    "GetAccessKeyLastUsedResult",
    "GetAccountAuthorizationDetailsResult",
    "GetAccountPasswordPolicyResult",
    "GetAccountSummaryResult",
    "GetContextKeysForCustomPolicyResult",
    "GetContextKeysForPrincipalPolicyResult",
    "GetCredentialReportResult",
    "GetGroupPolicyResult",
    "GetGroupResult",
    "GetInstanceProfileResult",
    "GetLoginProfileResult",
    "GetMfaDeviceResult",
    "GetOpenIdConnectProviderResult",
    "GetOrganizationsAccessReportResult",
    "GetPolicyResult",
    "GetPolicyVersionResult",
    "GetRolePolicyResult",
    "GetSamlProviderResult",
    "GetServerCertificateResult",
    "GetServiceLastAccessedDetailsResult",
    "GetServiceLastAccessedDetailsWithEntitiesResult",
    "GetServiceLinkedRoleDeletionStatusResult",
    "GetSshPublicKeyResult",
    "GetUserPolicyResult",
    "GetUserResult",
    "IAMPolicy",
    "IAMRole",
    "IAMUser",
    "ListAccessKeysResult",
    "ListAccountAliasesResult",
    "ListAttachedGroupPoliciesResult",
    "ListAttachedRolePoliciesResult",
    "ListAttachedUserPoliciesResult",
    "ListEntitiesForPolicyResult",
    "ListGroupPoliciesResult",
    "ListGroupsForUserResult",
    "ListGroupsResult",
    "ListInstanceProfileTagsResult",
    "ListInstanceProfilesForRoleResult",
    "ListInstanceProfilesResult",
    "ListMfaDeviceTagsResult",
    "ListMfaDevicesResult",
    "ListOpenIdConnectProviderTagsResult",
    "ListOpenIdConnectProvidersResult",
    "ListOrganizationsFeaturesResult",
    "ListPoliciesGrantingServiceAccessResult",
    "ListPolicyTagsResult",
    "ListPolicyVersionsResult",
    "ListRolePoliciesResult",
    "ListRoleTagsResult",
    "ListSamlProviderTagsResult",
    "ListSamlProvidersResult",
    "ListServerCertificateTagsResult",
    "ListServerCertificatesResult",
    "ListServiceSpecificCredentialsResult",
    "ListSigningCertificatesResult",
    "ListSshPublicKeysResult",
    "ListUserPoliciesResult",
    "ListUserTagsResult",
    "ListVirtualMfaDevicesResult",
    "ResetServiceSpecificCredentialResult",
    "SimulateCustomPolicyResult",
    "SimulatePrincipalPolicyResult",
    "UpdateRoleDescriptionResult",
    "UpdateSamlProviderResult",
    "UploadServerCertificateResult",
    "UploadSigningCertificateResult",
    "UploadSshPublicKeyResult",
    "add_client_id_to_open_id_connect_provider",
    "add_role_to_instance_profile",
    "add_user_to_group",
    "attach_group_policy",
    "attach_role_policy",
    "attach_user_policy",
    "change_password",
    "create_access_key",
    "create_account_alias",
    "create_delegation_request",
    "create_group",
    "create_instance_profile",
    "create_login_profile",
    "create_open_id_connect_provider",
    "create_policy",
    "create_policy_version",
    "create_role",
    "create_role_with_policies",
    "create_saml_provider",
    "create_service_linked_role",
    "create_service_specific_credential",
    "create_user",
    "create_virtual_mfa_device",
    "deactivate_mfa_device",
    "delete_access_key",
    "delete_account_alias",
    "delete_account_password_policy",
    "delete_group",
    "delete_group_policy",
    "delete_instance_profile",
    "delete_login_profile",
    "delete_open_id_connect_provider",
    "delete_policy",
    "delete_policy_version",
    "delete_role",
    "delete_role_permissions_boundary",
    "delete_role_policy",
    "delete_saml_provider",
    "delete_server_certificate",
    "delete_service_linked_role",
    "delete_service_specific_credential",
    "delete_signing_certificate",
    "delete_ssh_public_key",
    "delete_user",
    "delete_user_permissions_boundary",
    "delete_user_policy",
    "delete_virtual_mfa_device",
    "detach_group_policy",
    "detach_role_policy",
    "detach_user_policy",
    "disable_organizations_root_credentials_management",
    "disable_organizations_root_sessions",
    "enable_mfa_device",
    "enable_organizations_root_credentials_management",
    "enable_organizations_root_sessions",
    "ensure_role",
    "generate_credential_report",
    "generate_organizations_access_report",
    "generate_service_last_accessed_details",
    "get_access_key_last_used",
    "get_account_authorization_details",
    "get_account_password_policy",
    "get_account_summary",
    "get_context_keys_for_custom_policy",
    "get_context_keys_for_principal_policy",
    "get_credential_report",
    "get_group",
    "get_group_policy",
    "get_instance_profile",
    "get_login_profile",
    "get_mfa_device",
    "get_open_id_connect_provider",
    "get_organizations_access_report",
    "get_policy",
    "get_policy_version",
    "get_role",
    "get_role_policy",
    "get_saml_provider",
    "get_server_certificate",
    "get_service_last_accessed_details",
    "get_service_last_accessed_details_with_entities",
    "get_service_linked_role_deletion_status",
    "get_ssh_public_key",
    "get_user",
    "get_user_policy",
    "list_access_keys",
    "list_account_aliases",
    "list_attached_group_policies",
    "list_attached_role_policies",
    "list_attached_user_policies",
    "list_entities_for_policy",
    "list_group_policies",
    "list_groups",
    "list_groups_for_user",
    "list_instance_profile_tags",
    "list_instance_profiles",
    "list_instance_profiles_for_role",
    "list_mfa_device_tags",
    "list_mfa_devices",
    "list_open_id_connect_provider_tags",
    "list_open_id_connect_providers",
    "list_organizations_features",
    "list_policies",
    "list_policies_granting_service_access",
    "list_policy_tags",
    "list_policy_versions",
    "list_role_policies",
    "list_role_tags",
    "list_roles",
    "list_saml_provider_tags",
    "list_saml_providers",
    "list_server_certificate_tags",
    "list_server_certificates",
    "list_service_specific_credentials",
    "list_signing_certificates",
    "list_ssh_public_keys",
    "list_user_policies",
    "list_user_tags",
    "list_users",
    "list_virtual_mfa_devices",
    "put_group_policy",
    "put_role_permissions_boundary",
    "put_role_policy",
    "put_user_permissions_boundary",
    "put_user_policy",
    "remove_client_id_from_open_id_connect_provider",
    "remove_role_from_instance_profile",
    "remove_user_from_group",
    "reset_service_specific_credential",
    "resync_mfa_device",
    "set_default_policy_version",
    "set_security_token_service_preferences",
    "simulate_custom_policy",
    "simulate_principal_policy",
    "tag_instance_profile",
    "tag_mfa_device",
    "tag_open_id_connect_provider",
    "tag_policy",
    "tag_role",
    "tag_saml_provider",
    "tag_server_certificate",
    "tag_user",
    "untag_instance_profile",
    "untag_mfa_device",
    "untag_open_id_connect_provider",
    "untag_policy",
    "untag_role",
    "untag_saml_provider",
    "untag_server_certificate",
    "untag_user",
    "update_access_key",
    "update_account_password_policy",
    "update_assume_role_policy",
    "update_group",
    "update_login_profile",
    "update_open_id_connect_provider_thumbprint",
    "update_role",
    "update_role_description",
    "update_saml_provider",
    "update_server_certificate",
    "update_service_specific_credential",
    "update_signing_certificate",
    "update_ssh_public_key",
    "update_user",
    "upload_server_certificate",
    "upload_signing_certificate",
    "upload_ssh_public_key",
]


# ---------------------------------------------------------------------------
# Role utilities
# ---------------------------------------------------------------------------


async def create_role(
    role_name: str,
    assume_role_policy: dict[str, Any],
    description: str = "",
    path: str = "/",
    region_name: str | None = None,
) -> IAMRole:
    """Create an IAM role.

    Args:
        role_name: Unique name for the role.
        assume_role_policy: Trust policy document as a dict.
        description: Human-readable description of the role.
        path: IAM path for the role (default ``"/"``).
        region_name: AWS region override.

    Returns:
        The newly created :class:`IAMRole`.

    Raises:
        RuntimeError: If role creation fails.
    """
    client = async_client("iam", region_name)
    try:
        resp = await client.call(
            "CreateRole",
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description=description,
            Path=path,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create IAM role {role_name!r}") from exc
    return _parse_role(resp["Role"])


async def get_role(
    role_name: str,
    region_name: str | None = None,
) -> IAMRole | None:
    """Fetch an IAM role by name.

    Returns:
        An :class:`IAMRole`, or ``None`` if not found.
    """
    client = async_client("iam", region_name)
    try:
        resp = await client.call("GetRole", RoleName=role_name)
        return _parse_role(resp["Role"])
    except RuntimeError as exc:
        if "NoSuchEntity" in str(exc):
            return None
        raise


async def delete_role(
    role_name: str,
    region_name: str | None = None,
) -> None:
    """Delete an IAM role.

    All inline policies and managed policy attachments must be detached before
    deletion.

    Args:
        role_name: Name of the role to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("iam", region_name)
    try:
        await client.call("DeleteRole", RoleName=role_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete IAM role {role_name!r}") from exc


async def list_roles(
    path_prefix: str = "/",
    region_name: str | None = None,
) -> list[IAMRole]:
    """List IAM roles, optionally filtered by path prefix.

    Args:
        path_prefix: IAM path prefix filter (default ``"/"`` returns all).
        region_name: AWS region override.

    Returns:
        A list of :class:`IAMRole` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    roles: list[IAMRole] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {"PathPrefix": path_prefix}
            if token:
                kwargs["Marker"] = token
            resp = await client.call("ListRoles", **kwargs)
            for role in resp.get("Roles", []):
                roles.append(_parse_role(role))
            if not resp.get("IsTruncated", False):
                break
            token = resp.get("Marker")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_roles failed") from exc
    return roles


async def attach_role_policy(
    role_name: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Attach a managed policy to an IAM role.

    Args:
        role_name: Target role name.
        policy_arn: ARN of the managed policy to attach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the attachment fails.
    """
    client = async_client("iam", region_name)
    try:
        await client.call(
            "AttachRolePolicy",
            RoleName=role_name,
            PolicyArn=policy_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to attach policy {policy_arn!r} to role {role_name!r}"
        ) from exc


async def detach_role_policy(
    role_name: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Detach a managed policy from an IAM role.

    Args:
        role_name: Target role name.
        policy_arn: ARN of the policy to detach.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the detachment fails.
    """
    client = async_client("iam", region_name)
    try:
        await client.call(
            "DetachRolePolicy",
            RoleName=role_name,
            PolicyArn=policy_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"Failed to detach policy {policy_arn!r} from role {role_name!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Policy utilities
# ---------------------------------------------------------------------------


async def create_policy(
    policy_name: str,
    policy_document: dict[str, Any],
    description: str = "",
    path: str = "/",
    region_name: str | None = None,
) -> IAMPolicy:
    """Create a customer-managed IAM policy.

    Args:
        policy_name: Unique policy name.
        policy_document: Policy document as a dict.
        description: Human-readable description.
        path: IAM path for the policy.
        region_name: AWS region override.

    Returns:
        The newly created :class:`IAMPolicy`.

    Raises:
        RuntimeError: If policy creation fails.
    """
    client = async_client("iam", region_name)
    try:
        resp = await client.call(
            "CreatePolicy",
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_document),
            Description=description,
            Path=path,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to create IAM policy {policy_name!r}") from exc
    return _parse_policy(resp["Policy"])


async def delete_policy(
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete a customer-managed IAM policy.

    The policy must be detached from all roles, users, and groups first.

    Args:
        policy_arn: ARN of the policy to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = async_client("iam", region_name)
    try:
        await client.call("DeletePolicy", PolicyArn=policy_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"Failed to delete IAM policy {policy_arn!r}") from exc


async def list_policies(
    scope: str = "Local",
    path_prefix: str = "/",
    region_name: str | None = None,
) -> list[IAMPolicy]:
    """List IAM policies.

    Args:
        scope: ``"Local"`` (default, customer-managed only), ``"AWS"``
            (AWS-managed only), or ``"All"``.
        path_prefix: IAM path prefix filter.
        region_name: AWS region override.

    Returns:
        A list of :class:`IAMPolicy` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    policies: list[IAMPolicy] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "Scope": scope,
                "PathPrefix": path_prefix,
            }
            if token:
                kwargs["Marker"] = token
            resp = await client.call("ListPolicies", **kwargs)
            for policy in resp.get("Policies", []):
                policies.append(_parse_policy(policy))
            if not resp.get("IsTruncated", False):
                break
            token = resp.get("Marker")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_policies failed") from exc
    return policies


async def list_users(
    path_prefix: str = "/",
    region_name: str | None = None,
) -> list[IAMUser]:
    """List IAM users, optionally filtered by path prefix.

    Args:
        path_prefix: IAM path prefix filter (default ``"/"`` returns all).
        region_name: AWS region override.

    Returns:
        A list of :class:`IAMUser` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    users: list[IAMUser] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {"PathPrefix": path_prefix}
            if token:
                kwargs["Marker"] = token
            resp = await client.call("ListUsers", **kwargs)
            for user in resp.get("Users", []):
                users.append(
                    IAMUser(
                        user_id=user["UserId"],
                        user_name=user["UserName"],
                        arn=user["Arn"],
                        path=user["Path"],
                        create_date=user.get("CreateDate"),
                    )
                )
            if not resp.get("IsTruncated", False):
                break
            token = resp.get("Marker")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_users failed") from exc
    return users


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def create_role_with_policies(
    role_name: str,
    trust_policy: dict[str, Any],
    managed_policy_arns: list[str] | None = None,
    inline_policies: dict[str, dict[str, Any]] | None = None,
    description: str = "",
    region_name: str | None = None,
) -> IAMRole:
    """Create an IAM role and attach managed and inline policies in one call.

    Args:
        role_name: Unique name for the role.
        trust_policy: Trust relationship policy document as a dict.
        managed_policy_arns: List of managed policy ARNs to attach.
        inline_policies: Dict of ``{policy_name: policy_document}`` inline
            policies to embed directly in the role.
        description: Human-readable description.
        region_name: AWS region override.

    Returns:
        The newly created :class:`IAMRole`.

    Raises:
        RuntimeError: If any step fails.
    """
    role = await create_role(
        role_name,
        trust_policy,
        description=description,
        region_name=region_name,
    )

    # Attach managed policies in parallel
    if managed_policy_arns:
        await asyncio.gather(
            *(
                attach_role_policy(role_name, arn, region_name=region_name)
                for arn in managed_policy_arns
            )
        )

    # Put inline policies in parallel
    if inline_policies:
        client = async_client("iam", region_name)

        async def _put_inline(pol_name: str, pol_doc: dict[str, Any]) -> None:
            try:
                await client.call(
                    "PutRolePolicy",
                    RoleName=role_name,
                    PolicyName=pol_name,
                    PolicyDocument=json.dumps(pol_doc),
                )
            except Exception as exc:
                raise wrap_aws_error(
                    exc, f"Failed to put inline policy {pol_name!r} on role {role_name!r}"
                ) from exc

        await asyncio.gather(
            *(_put_inline(pol_name, pol_doc) for pol_name, pol_doc in inline_policies.items())
        )

    return role


async def ensure_role(
    role_name: str,
    trust_policy: dict[str, Any],
    managed_policy_arns: list[str] | None = None,
    description: str = "",
    region_name: str | None = None,
) -> tuple[IAMRole, bool]:
    """Get or create an IAM role (idempotent).

    If the role already exists it is returned unchanged.  If it does not
    exist it is created with the supplied trust policy and managed policies.

    Args:
        role_name: Role name.
        trust_policy: Trust policy used only when creating a new role.
        managed_policy_arns: Managed policies to attach on creation only.
        description: Description used only when creating a new role.
        region_name: AWS region override.

    Returns:
        A ``(role, created)`` tuple where *created* is ``True`` if the role
        was just created.
    """
    existing = await get_role(role_name, region_name=region_name)
    if existing is not None:
        return existing, False

    role = await create_role_with_policies(
        role_name,
        trust_policy,
        managed_policy_arns=managed_policy_arns,
        description=description,
        region_name=region_name,
    )
    return role, True


async def add_client_id_to_open_id_connect_provider(
    open_id_connect_provider_arn: str,
    client_id: str,
    region_name: str | None = None,
) -> None:
    """Add client id to open id connect provider.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        client_id: Client id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    kwargs["ClientID"] = client_id
    try:
        await client.call("AddClientIDToOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add client id to open id connect provider") from exc
    return None


async def add_role_to_instance_profile(
    instance_profile_name: str,
    role_name: str,
    region_name: str | None = None,
) -> None:
    """Add role to instance profile.

    Args:
        instance_profile_name: Instance profile name.
        role_name: Role name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    kwargs["RoleName"] = role_name
    try:
        await client.call("AddRoleToInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add role to instance profile") from exc
    return None


async def add_user_to_group(
    group_name: str,
    user_name: str,
    region_name: str | None = None,
) -> None:
    """Add user to group.

    Args:
        group_name: Group name.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["UserName"] = user_name
    try:
        await client.call("AddUserToGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add user to group") from exc
    return None


async def attach_group_policy(
    group_name: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Attach group policy.

    Args:
        group_name: Group name.
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["PolicyArn"] = policy_arn
    try:
        await client.call("AttachGroupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach group policy") from exc
    return None


async def attach_user_policy(
    user_name: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Attach user policy.

    Args:
        user_name: User name.
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["PolicyArn"] = policy_arn
    try:
        await client.call("AttachUserPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach user policy") from exc
    return None


async def change_password(
    old_password: str,
    new_password: str,
    region_name: str | None = None,
) -> None:
    """Change password.

    Args:
        old_password: Old password.
        new_password: New password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OldPassword"] = old_password
    kwargs["NewPassword"] = new_password
    try:
        await client.call("ChangePassword", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to change password") from exc
    return None


async def create_access_key(
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> CreateAccessKeyResult:
    """Create access key.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        resp = await client.call("CreateAccessKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create access key") from exc
    return CreateAccessKeyResult(
        access_key=resp.get("AccessKey"),
    )


async def create_account_alias(
    account_alias: str,
    region_name: str | None = None,
) -> None:
    """Create account alias.

    Args:
        account_alias: Account alias.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountAlias"] = account_alias
    try:
        await client.call("CreateAccountAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create account alias") from exc
    return None


async def create_delegation_request(
    description: str,
    permissions: dict[str, Any],
    requestor_workflow_id: str,
    notification_channel: str,
    session_duration: int,
    *,
    owner_account_id: str | None = None,
    request_message: str | None = None,
    redirect_url: str | None = None,
    only_send_by_owner: bool | None = None,
    region_name: str | None = None,
) -> CreateDelegationRequestResult:
    """Create delegation request.

    Args:
        description: Description.
        permissions: Permissions.
        requestor_workflow_id: Requestor workflow id.
        notification_channel: Notification channel.
        session_duration: Session duration.
        owner_account_id: Owner account id.
        request_message: Request message.
        redirect_url: Redirect url.
        only_send_by_owner: Only send by owner.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Description"] = description
    kwargs["Permissions"] = permissions
    kwargs["RequestorWorkflowId"] = requestor_workflow_id
    kwargs["NotificationChannel"] = notification_channel
    kwargs["SessionDuration"] = session_duration
    if owner_account_id is not None:
        kwargs["OwnerAccountId"] = owner_account_id
    if request_message is not None:
        kwargs["RequestMessage"] = request_message
    if redirect_url is not None:
        kwargs["RedirectUrl"] = redirect_url
    if only_send_by_owner is not None:
        kwargs["OnlySendByOwner"] = only_send_by_owner
    try:
        resp = await client.call("CreateDelegationRequest", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create delegation request") from exc
    return CreateDelegationRequestResult(
        console_deep_link=resp.get("ConsoleDeepLink"),
        delegation_request_id=resp.get("DelegationRequestId"),
    )


async def create_group(
    group_name: str,
    *,
    path: str | None = None,
    region_name: str | None = None,
) -> CreateGroupResult:
    """Create group.

    Args:
        group_name: Group name.
        path: Path.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    if path is not None:
        kwargs["Path"] = path
    try:
        resp = await client.call("CreateGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create group") from exc
    return CreateGroupResult(
        group=resp.get("Group"),
    )


async def create_instance_profile(
    instance_profile_name: str,
    *,
    path: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateInstanceProfileResult:
    """Create instance profile.

    Args:
        instance_profile_name: Instance profile name.
        path: Path.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    if path is not None:
        kwargs["Path"] = path
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create instance profile") from exc
    return CreateInstanceProfileResult(
        instance_profile=resp.get("InstanceProfile"),
    )


async def create_login_profile(
    *,
    user_name: str | None = None,
    password: str | None = None,
    password_reset_required: bool | None = None,
    region_name: str | None = None,
) -> CreateLoginProfileResult:
    """Create login profile.

    Args:
        user_name: User name.
        password: Password.
        password_reset_required: Password reset required.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    if password is not None:
        kwargs["Password"] = password
    if password_reset_required is not None:
        kwargs["PasswordResetRequired"] = password_reset_required
    try:
        resp = await client.call("CreateLoginProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create login profile") from exc
    return CreateLoginProfileResult(
        login_profile=resp.get("LoginProfile"),
    )


async def create_open_id_connect_provider(
    url: str,
    *,
    client_id_list: list[str] | None = None,
    thumbprint_list: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateOpenIdConnectProviderResult:
    """Create open id connect provider.

    Args:
        url: Url.
        client_id_list: Client id list.
        thumbprint_list: Thumbprint list.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Url"] = url
    if client_id_list is not None:
        kwargs["ClientIDList"] = client_id_list
    if thumbprint_list is not None:
        kwargs["ThumbprintList"] = thumbprint_list
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create open id connect provider") from exc
    return CreateOpenIdConnectProviderResult(
        open_id_connect_provider_arn=resp.get("OpenIDConnectProviderArn"),
        tags=resp.get("Tags"),
    )


async def create_policy_version(
    policy_arn: str,
    policy_document: str,
    *,
    set_as_default: bool | None = None,
    region_name: str | None = None,
) -> CreatePolicyVersionResult:
    """Create policy version.

    Args:
        policy_arn: Policy arn.
        policy_document: Policy document.
        set_as_default: Set as default.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    kwargs["PolicyDocument"] = policy_document
    if set_as_default is not None:
        kwargs["SetAsDefault"] = set_as_default
    try:
        resp = await client.call("CreatePolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create policy version") from exc
    return CreatePolicyVersionResult(
        policy_version=resp.get("PolicyVersion"),
    )


async def create_saml_provider(
    saml_metadata_document: str,
    name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    assertion_encryption_mode: str | None = None,
    add_private_key: str | None = None,
    region_name: str | None = None,
) -> CreateSamlProviderResult:
    """Create saml provider.

    Args:
        saml_metadata_document: Saml metadata document.
        name: Name.
        tags: Tags.
        assertion_encryption_mode: Assertion encryption mode.
        add_private_key: Add private key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLMetadataDocument"] = saml_metadata_document
    kwargs["Name"] = name
    if tags is not None:
        kwargs["Tags"] = tags
    if assertion_encryption_mode is not None:
        kwargs["AssertionEncryptionMode"] = assertion_encryption_mode
    if add_private_key is not None:
        kwargs["AddPrivateKey"] = add_private_key
    try:
        resp = await client.call("CreateSAMLProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create saml provider") from exc
    return CreateSamlProviderResult(
        saml_provider_arn=resp.get("SAMLProviderArn"),
        tags=resp.get("Tags"),
    )


async def create_service_linked_role(
    aws_service_name: str,
    *,
    description: str | None = None,
    custom_suffix: str | None = None,
    region_name: str | None = None,
) -> CreateServiceLinkedRoleResult:
    """Create service linked role.

    Args:
        aws_service_name: Aws service name.
        description: Description.
        custom_suffix: Custom suffix.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AWSServiceName"] = aws_service_name
    if description is not None:
        kwargs["Description"] = description
    if custom_suffix is not None:
        kwargs["CustomSuffix"] = custom_suffix
    try:
        resp = await client.call("CreateServiceLinkedRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create service linked role") from exc
    return CreateServiceLinkedRoleResult(
        role=resp.get("Role"),
    )


async def create_service_specific_credential(
    user_name: str,
    service_name: str,
    *,
    credential_age_days: int | None = None,
    region_name: str | None = None,
) -> CreateServiceSpecificCredentialResult:
    """Create service specific credential.

    Args:
        user_name: User name.
        service_name: Service name.
        credential_age_days: Credential age days.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["ServiceName"] = service_name
    if credential_age_days is not None:
        kwargs["CredentialAgeDays"] = credential_age_days
    try:
        resp = await client.call("CreateServiceSpecificCredential", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create service specific credential") from exc
    return CreateServiceSpecificCredentialResult(
        service_specific_credential=resp.get("ServiceSpecificCredential"),
    )


async def create_user(
    user_name: str,
    *,
    path: str | None = None,
    permissions_boundary: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateUserResult:
    """Create user.

    Args:
        user_name: User name.
        path: Path.
        permissions_boundary: Permissions boundary.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if path is not None:
        kwargs["Path"] = path
    if permissions_boundary is not None:
        kwargs["PermissionsBoundary"] = permissions_boundary
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create user") from exc
    return CreateUserResult(
        user=resp.get("User"),
    )


async def create_virtual_mfa_device(
    virtual_mfa_device_name: str,
    *,
    path: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateVirtualMfaDeviceResult:
    """Create virtual mfa device.

    Args:
        virtual_mfa_device_name: Virtual mfa device name.
        path: Path.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["VirtualMFADeviceName"] = virtual_mfa_device_name
    if path is not None:
        kwargs["Path"] = path
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateVirtualMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create virtual mfa device") from exc
    return CreateVirtualMfaDeviceResult(
        virtual_mfa_device=resp.get("VirtualMFADevice"),
    )


async def deactivate_mfa_device(
    serial_number: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Deactivate mfa device.

    Args:
        serial_number: Serial number.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SerialNumber"] = serial_number
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("DeactivateMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deactivate mfa device") from exc
    return None


async def delete_access_key(
    access_key_id: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete access key.

    Args:
        access_key_id: Access key id.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessKeyId"] = access_key_id
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("DeleteAccessKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete access key") from exc
    return None


async def delete_account_alias(
    account_alias: str,
    region_name: str | None = None,
) -> None:
    """Delete account alias.

    Args:
        account_alias: Account alias.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountAlias"] = account_alias
    try:
        await client.call("DeleteAccountAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account alias") from exc
    return None


async def delete_account_password_policy(
    region_name: str | None = None,
) -> None:
    """Delete account password policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DeleteAccountPasswordPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account password policy") from exc
    return None


async def delete_group(
    group_name: str,
    region_name: str | None = None,
) -> None:
    """Delete group.

    Args:
        group_name: Group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    try:
        await client.call("DeleteGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete group") from exc
    return None


async def delete_group_policy(
    group_name: str,
    policy_name: str,
    region_name: str | None = None,
) -> None:
    """Delete group policy.

    Args:
        group_name: Group name.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["PolicyName"] = policy_name
    try:
        await client.call("DeleteGroupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete group policy") from exc
    return None


async def delete_instance_profile(
    instance_profile_name: str,
    region_name: str | None = None,
) -> None:
    """Delete instance profile.

    Args:
        instance_profile_name: Instance profile name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    try:
        await client.call("DeleteInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete instance profile") from exc
    return None


async def delete_login_profile(
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete login profile.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("DeleteLoginProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete login profile") from exc
    return None


async def delete_open_id_connect_provider(
    open_id_connect_provider_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete open id connect provider.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    try:
        await client.call("DeleteOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete open id connect provider") from exc
    return None


async def delete_policy_version(
    policy_arn: str,
    version_id: str,
    region_name: str | None = None,
) -> None:
    """Delete policy version.

    Args:
        policy_arn: Policy arn.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    kwargs["VersionId"] = version_id
    try:
        await client.call("DeletePolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete policy version") from exc
    return None


async def delete_role_permissions_boundary(
    role_name: str,
    region_name: str | None = None,
) -> None:
    """Delete role permissions boundary.

    Args:
        role_name: Role name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    try:
        await client.call("DeleteRolePermissionsBoundary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete role permissions boundary") from exc
    return None


async def delete_role_policy(
    role_name: str,
    policy_name: str,
    region_name: str | None = None,
) -> None:
    """Delete role policy.

    Args:
        role_name: Role name.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["PolicyName"] = policy_name
    try:
        await client.call("DeleteRolePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete role policy") from exc
    return None


async def delete_saml_provider(
    saml_provider_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete saml provider.

    Args:
        saml_provider_arn: Saml provider arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLProviderArn"] = saml_provider_arn
    try:
        await client.call("DeleteSAMLProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete saml provider") from exc
    return None


async def delete_server_certificate(
    server_certificate_name: str,
    region_name: str | None = None,
) -> None:
    """Delete server certificate.

    Args:
        server_certificate_name: Server certificate name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    try:
        await client.call("DeleteServerCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete server certificate") from exc
    return None


async def delete_service_linked_role(
    role_name: str,
    region_name: str | None = None,
) -> DeleteServiceLinkedRoleResult:
    """Delete service linked role.

    Args:
        role_name: Role name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    try:
        resp = await client.call("DeleteServiceLinkedRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete service linked role") from exc
    return DeleteServiceLinkedRoleResult(
        deletion_task_id=resp.get("DeletionTaskId"),
    )


async def delete_service_specific_credential(
    service_specific_credential_id: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete service specific credential.

    Args:
        service_specific_credential_id: Service specific credential id.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceSpecificCredentialId"] = service_specific_credential_id
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("DeleteServiceSpecificCredential", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete service specific credential") from exc
    return None


async def delete_signing_certificate(
    certificate_id: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete signing certificate.

    Args:
        certificate_id: Certificate id.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateId"] = certificate_id
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("DeleteSigningCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete signing certificate") from exc
    return None


async def delete_ssh_public_key(
    user_name: str,
    ssh_public_key_id: str,
    region_name: str | None = None,
) -> None:
    """Delete ssh public key.

    Args:
        user_name: User name.
        ssh_public_key_id: Ssh public key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["SSHPublicKeyId"] = ssh_public_key_id
    try:
        await client.call("DeleteSSHPublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ssh public key") from exc
    return None


async def delete_user(
    user_name: str,
    region_name: str | None = None,
) -> None:
    """Delete user.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    try:
        await client.call("DeleteUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete user") from exc
    return None


async def delete_user_permissions_boundary(
    user_name: str,
    region_name: str | None = None,
) -> None:
    """Delete user permissions boundary.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    try:
        await client.call("DeleteUserPermissionsBoundary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete user permissions boundary") from exc
    return None


async def delete_user_policy(
    user_name: str,
    policy_name: str,
    region_name: str | None = None,
) -> None:
    """Delete user policy.

    Args:
        user_name: User name.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["PolicyName"] = policy_name
    try:
        await client.call("DeleteUserPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete user policy") from exc
    return None


async def delete_virtual_mfa_device(
    serial_number: str,
    region_name: str | None = None,
) -> None:
    """Delete virtual mfa device.

    Args:
        serial_number: Serial number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SerialNumber"] = serial_number
    try:
        await client.call("DeleteVirtualMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete virtual mfa device") from exc
    return None


async def detach_group_policy(
    group_name: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Detach group policy.

    Args:
        group_name: Group name.
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["PolicyArn"] = policy_arn
    try:
        await client.call("DetachGroupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach group policy") from exc
    return None


async def detach_user_policy(
    user_name: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Detach user policy.

    Args:
        user_name: User name.
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["PolicyArn"] = policy_arn
    try:
        await client.call("DetachUserPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach user policy") from exc
    return None


async def disable_organizations_root_credentials_management(
    region_name: str | None = None,
) -> DisableOrganizationsRootCredentialsManagementResult:
    """Disable organizations root credentials management.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DisableOrganizationsRootCredentialsManagement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to disable organizations root credentials management"
        ) from exc
    return DisableOrganizationsRootCredentialsManagementResult(
        organization_id=resp.get("OrganizationId"),
        enabled_features=resp.get("EnabledFeatures"),
    )


async def disable_organizations_root_sessions(
    region_name: str | None = None,
) -> DisableOrganizationsRootSessionsResult:
    """Disable organizations root sessions.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DisableOrganizationsRootSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable organizations root sessions") from exc
    return DisableOrganizationsRootSessionsResult(
        organization_id=resp.get("OrganizationId"),
        enabled_features=resp.get("EnabledFeatures"),
    )


async def enable_mfa_device(
    user_name: str,
    serial_number: str,
    authentication_code1: str,
    authentication_code2: str,
    region_name: str | None = None,
) -> None:
    """Enable mfa device.

    Args:
        user_name: User name.
        serial_number: Serial number.
        authentication_code1: Authentication code1.
        authentication_code2: Authentication code2.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["SerialNumber"] = serial_number
    kwargs["AuthenticationCode1"] = authentication_code1
    kwargs["AuthenticationCode2"] = authentication_code2
    try:
        await client.call("EnableMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable mfa device") from exc
    return None


async def enable_organizations_root_credentials_management(
    region_name: str | None = None,
) -> EnableOrganizationsRootCredentialsManagementResult:
    """Enable organizations root credentials management.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("EnableOrganizationsRootCredentialsManagement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to enable organizations root credentials management"
        ) from exc
    return EnableOrganizationsRootCredentialsManagementResult(
        organization_id=resp.get("OrganizationId"),
        enabled_features=resp.get("EnabledFeatures"),
    )


async def enable_organizations_root_sessions(
    region_name: str | None = None,
) -> EnableOrganizationsRootSessionsResult:
    """Enable organizations root sessions.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("EnableOrganizationsRootSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable organizations root sessions") from exc
    return EnableOrganizationsRootSessionsResult(
        organization_id=resp.get("OrganizationId"),
        enabled_features=resp.get("EnabledFeatures"),
    )


async def generate_credential_report(
    region_name: str | None = None,
) -> GenerateCredentialReportResult:
    """Generate credential report.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GenerateCredentialReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate credential report") from exc
    return GenerateCredentialReportResult(
        state=resp.get("State"),
        description=resp.get("Description"),
    )


async def generate_organizations_access_report(
    entity_path: str,
    *,
    organizations_policy_id: str | None = None,
    region_name: str | None = None,
) -> GenerateOrganizationsAccessReportResult:
    """Generate organizations access report.

    Args:
        entity_path: Entity path.
        organizations_policy_id: Organizations policy id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EntityPath"] = entity_path
    if organizations_policy_id is not None:
        kwargs["OrganizationsPolicyId"] = organizations_policy_id
    try:
        resp = await client.call("GenerateOrganizationsAccessReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate organizations access report") from exc
    return GenerateOrganizationsAccessReportResult(
        job_id=resp.get("JobId"),
    )


async def generate_service_last_accessed_details(
    arn: str,
    *,
    granularity: str | None = None,
    region_name: str | None = None,
) -> GenerateServiceLastAccessedDetailsResult:
    """Generate service last accessed details.

    Args:
        arn: Arn.
        granularity: Granularity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    if granularity is not None:
        kwargs["Granularity"] = granularity
    try:
        resp = await client.call("GenerateServiceLastAccessedDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate service last accessed details") from exc
    return GenerateServiceLastAccessedDetailsResult(
        job_id=resp.get("JobId"),
    )


async def get_access_key_last_used(
    access_key_id: str,
    region_name: str | None = None,
) -> GetAccessKeyLastUsedResult:
    """Get access key last used.

    Args:
        access_key_id: Access key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessKeyId"] = access_key_id
    try:
        resp = await client.call("GetAccessKeyLastUsed", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get access key last used") from exc
    return GetAccessKeyLastUsedResult(
        user_name=resp.get("UserName"),
        access_key_last_used=resp.get("AccessKeyLastUsed"),
    )


async def get_account_authorization_details(
    *,
    filter: list[str] | None = None,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> GetAccountAuthorizationDetailsResult:
    """Get account authorization details.

    Args:
        filter: Filter.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("GetAccountAuthorizationDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account authorization details") from exc
    return GetAccountAuthorizationDetailsResult(
        user_detail_list=resp.get("UserDetailList"),
        group_detail_list=resp.get("GroupDetailList"),
        role_detail_list=resp.get("RoleDetailList"),
        policies=resp.get("Policies"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def get_account_password_policy(
    region_name: str | None = None,
) -> GetAccountPasswordPolicyResult:
    """Get account password policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAccountPasswordPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account password policy") from exc
    return GetAccountPasswordPolicyResult(
        password_policy=resp.get("PasswordPolicy"),
    )


async def get_account_summary(
    region_name: str | None = None,
) -> GetAccountSummaryResult:
    """Get account summary.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetAccountSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get account summary") from exc
    return GetAccountSummaryResult(
        summary_map=resp.get("SummaryMap"),
    )


async def get_context_keys_for_custom_policy(
    policy_input_list: list[str],
    region_name: str | None = None,
) -> GetContextKeysForCustomPolicyResult:
    """Get context keys for custom policy.

    Args:
        policy_input_list: Policy input list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyInputList"] = policy_input_list
    try:
        resp = await client.call("GetContextKeysForCustomPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get context keys for custom policy") from exc
    return GetContextKeysForCustomPolicyResult(
        context_key_names=resp.get("ContextKeyNames"),
    )


async def get_context_keys_for_principal_policy(
    policy_source_arn: str,
    *,
    policy_input_list: list[str] | None = None,
    region_name: str | None = None,
) -> GetContextKeysForPrincipalPolicyResult:
    """Get context keys for principal policy.

    Args:
        policy_source_arn: Policy source arn.
        policy_input_list: Policy input list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicySourceArn"] = policy_source_arn
    if policy_input_list is not None:
        kwargs["PolicyInputList"] = policy_input_list
    try:
        resp = await client.call("GetContextKeysForPrincipalPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get context keys for principal policy") from exc
    return GetContextKeysForPrincipalPolicyResult(
        context_key_names=resp.get("ContextKeyNames"),
    )


async def get_credential_report(
    region_name: str | None = None,
) -> GetCredentialReportResult:
    """Get credential report.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetCredentialReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get credential report") from exc
    return GetCredentialReportResult(
        content=resp.get("Content"),
        report_format=resp.get("ReportFormat"),
        generated_time=resp.get("GeneratedTime"),
    )


async def get_group(
    group_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> GetGroupResult:
    """Get group.

    Args:
        group_name: Group name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("GetGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get group") from exc
    return GetGroupResult(
        group=resp.get("Group"),
        users=resp.get("Users"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def get_group_policy(
    group_name: str,
    policy_name: str,
    region_name: str | None = None,
) -> GetGroupPolicyResult:
    """Get group policy.

    Args:
        group_name: Group name.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["PolicyName"] = policy_name
    try:
        resp = await client.call("GetGroupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get group policy") from exc
    return GetGroupPolicyResult(
        group_name=resp.get("GroupName"),
        policy_name=resp.get("PolicyName"),
        policy_document=resp.get("PolicyDocument"),
    )


async def get_instance_profile(
    instance_profile_name: str,
    region_name: str | None = None,
) -> GetInstanceProfileResult:
    """Get instance profile.

    Args:
        instance_profile_name: Instance profile name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    try:
        resp = await client.call("GetInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get instance profile") from exc
    return GetInstanceProfileResult(
        instance_profile=resp.get("InstanceProfile"),
    )


async def get_login_profile(
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> GetLoginProfileResult:
    """Get login profile.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        resp = await client.call("GetLoginProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get login profile") from exc
    return GetLoginProfileResult(
        login_profile=resp.get("LoginProfile"),
    )


async def get_mfa_device(
    serial_number: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> GetMfaDeviceResult:
    """Get mfa device.

    Args:
        serial_number: Serial number.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SerialNumber"] = serial_number
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        resp = await client.call("GetMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get mfa device") from exc
    return GetMfaDeviceResult(
        user_name=resp.get("UserName"),
        serial_number=resp.get("SerialNumber"),
        enable_date=resp.get("EnableDate"),
        certifications=resp.get("Certifications"),
    )


async def get_open_id_connect_provider(
    open_id_connect_provider_arn: str,
    region_name: str | None = None,
) -> GetOpenIdConnectProviderResult:
    """Get open id connect provider.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    try:
        resp = await client.call("GetOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get open id connect provider") from exc
    return GetOpenIdConnectProviderResult(
        url=resp.get("Url"),
        client_id_list=resp.get("ClientIDList"),
        thumbprint_list=resp.get("ThumbprintList"),
        create_date=resp.get("CreateDate"),
        tags=resp.get("Tags"),
    )


async def get_organizations_access_report(
    job_id: str,
    *,
    max_items: int | None = None,
    marker: str | None = None,
    sort_key: str | None = None,
    region_name: str | None = None,
) -> GetOrganizationsAccessReportResult:
    """Get organizations access report.

    Args:
        job_id: Job id.
        max_items: Max items.
        marker: Marker.
        sort_key: Sort key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    if sort_key is not None:
        kwargs["SortKey"] = sort_key
    try:
        resp = await client.call("GetOrganizationsAccessReport", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get organizations access report") from exc
    return GetOrganizationsAccessReportResult(
        job_status=resp.get("JobStatus"),
        job_creation_date=resp.get("JobCreationDate"),
        job_completion_date=resp.get("JobCompletionDate"),
        number_of_services_accessible=resp.get("NumberOfServicesAccessible"),
        number_of_services_not_accessed=resp.get("NumberOfServicesNotAccessed"),
        access_details=resp.get("AccessDetails"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
        error_details=resp.get("ErrorDetails"),
    )


async def get_policy(
    policy_arn: str,
    region_name: str | None = None,
) -> GetPolicyResult:
    """Get policy.

    Args:
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    try:
        resp = await client.call("GetPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get policy") from exc
    return GetPolicyResult(
        policy=resp.get("Policy"),
    )


async def get_policy_version(
    policy_arn: str,
    version_id: str,
    region_name: str | None = None,
) -> GetPolicyVersionResult:
    """Get policy version.

    Args:
        policy_arn: Policy arn.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    kwargs["VersionId"] = version_id
    try:
        resp = await client.call("GetPolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get policy version") from exc
    return GetPolicyVersionResult(
        policy_version=resp.get("PolicyVersion"),
    )


async def get_role_policy(
    role_name: str,
    policy_name: str,
    region_name: str | None = None,
) -> GetRolePolicyResult:
    """Get role policy.

    Args:
        role_name: Role name.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["PolicyName"] = policy_name
    try:
        resp = await client.call("GetRolePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get role policy") from exc
    return GetRolePolicyResult(
        role_name=resp.get("RoleName"),
        policy_name=resp.get("PolicyName"),
        policy_document=resp.get("PolicyDocument"),
    )


async def get_saml_provider(
    saml_provider_arn: str,
    region_name: str | None = None,
) -> GetSamlProviderResult:
    """Get saml provider.

    Args:
        saml_provider_arn: Saml provider arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLProviderArn"] = saml_provider_arn
    try:
        resp = await client.call("GetSAMLProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get saml provider") from exc
    return GetSamlProviderResult(
        saml_provider_uuid=resp.get("SAMLProviderUUID"),
        saml_metadata_document=resp.get("SAMLMetadataDocument"),
        create_date=resp.get("CreateDate"),
        valid_until=resp.get("ValidUntil"),
        tags=resp.get("Tags"),
        assertion_encryption_mode=resp.get("AssertionEncryptionMode"),
        private_key_list=resp.get("PrivateKeyList"),
    )


async def get_server_certificate(
    server_certificate_name: str,
    region_name: str | None = None,
) -> GetServerCertificateResult:
    """Get server certificate.

    Args:
        server_certificate_name: Server certificate name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    try:
        resp = await client.call("GetServerCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get server certificate") from exc
    return GetServerCertificateResult(
        server_certificate=resp.get("ServerCertificate"),
    )


async def get_service_last_accessed_details(
    job_id: str,
    *,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> GetServiceLastAccessedDetailsResult:
    """Get service last accessed details.

    Args:
        job_id: Job id.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("GetServiceLastAccessedDetails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get service last accessed details") from exc
    return GetServiceLastAccessedDetailsResult(
        job_status=resp.get("JobStatus"),
        job_type=resp.get("JobType"),
        job_creation_date=resp.get("JobCreationDate"),
        services_last_accessed=resp.get("ServicesLastAccessed"),
        job_completion_date=resp.get("JobCompletionDate"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
        error=resp.get("Error"),
    )


async def get_service_last_accessed_details_with_entities(
    job_id: str,
    service_namespace: str,
    *,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> GetServiceLastAccessedDetailsWithEntitiesResult:
    """Get service last accessed details with entities.

    Args:
        job_id: Job id.
        service_namespace: Service namespace.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobId"] = job_id
    kwargs["ServiceNamespace"] = service_namespace
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("GetServiceLastAccessedDetailsWithEntities", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to get service last accessed details with entities"
        ) from exc
    return GetServiceLastAccessedDetailsWithEntitiesResult(
        job_status=resp.get("JobStatus"),
        job_creation_date=resp.get("JobCreationDate"),
        job_completion_date=resp.get("JobCompletionDate"),
        entity_details_list=resp.get("EntityDetailsList"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
        error=resp.get("Error"),
    )


async def get_service_linked_role_deletion_status(
    deletion_task_id: str,
    region_name: str | None = None,
) -> GetServiceLinkedRoleDeletionStatusResult:
    """Get service linked role deletion status.

    Args:
        deletion_task_id: Deletion task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeletionTaskId"] = deletion_task_id
    try:
        resp = await client.call("GetServiceLinkedRoleDeletionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get service linked role deletion status") from exc
    return GetServiceLinkedRoleDeletionStatusResult(
        status=resp.get("Status"),
        reason=resp.get("Reason"),
    )


async def get_ssh_public_key(
    user_name: str,
    ssh_public_key_id: str,
    encoding: str,
    region_name: str | None = None,
) -> GetSshPublicKeyResult:
    """Get ssh public key.

    Args:
        user_name: User name.
        ssh_public_key_id: Ssh public key id.
        encoding: Encoding.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["SSHPublicKeyId"] = ssh_public_key_id
    kwargs["Encoding"] = encoding
    try:
        resp = await client.call("GetSSHPublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ssh public key") from exc
    return GetSshPublicKeyResult(
        ssh_public_key=resp.get("SSHPublicKey"),
    )


async def get_user(
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> GetUserResult:
    """Get user.

    Args:
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        resp = await client.call("GetUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get user") from exc
    return GetUserResult(
        user=resp.get("User"),
    )


async def get_user_policy(
    user_name: str,
    policy_name: str,
    region_name: str | None = None,
) -> GetUserPolicyResult:
    """Get user policy.

    Args:
        user_name: User name.
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["PolicyName"] = policy_name
    try:
        resp = await client.call("GetUserPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get user policy") from exc
    return GetUserPolicyResult(
        user_name=resp.get("UserName"),
        policy_name=resp.get("PolicyName"),
        policy_document=resp.get("PolicyDocument"),
    )


async def list_access_keys(
    *,
    user_name: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAccessKeysResult:
    """List access keys.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListAccessKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list access keys") from exc
    return ListAccessKeysResult(
        access_key_metadata=resp.get("AccessKeyMetadata"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_account_aliases(
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAccountAliasesResult:
    """List account aliases.

    Args:
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListAccountAliases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list account aliases") from exc
    return ListAccountAliasesResult(
        account_aliases=resp.get("AccountAliases"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_attached_group_policies(
    group_name: str,
    *,
    path_prefix: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAttachedGroupPoliciesResult:
    """List attached group policies.

    Args:
        group_name: Group name.
        path_prefix: Path prefix.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListAttachedGroupPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list attached group policies") from exc
    return ListAttachedGroupPoliciesResult(
        attached_policies=resp.get("AttachedPolicies"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_attached_role_policies(
    role_name: str,
    *,
    path_prefix: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAttachedRolePoliciesResult:
    """List attached role policies.

    Args:
        role_name: Role name.
        path_prefix: Path prefix.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListAttachedRolePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list attached role policies") from exc
    return ListAttachedRolePoliciesResult(
        attached_policies=resp.get("AttachedPolicies"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_attached_user_policies(
    user_name: str,
    *,
    path_prefix: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListAttachedUserPoliciesResult:
    """List attached user policies.

    Args:
        user_name: User name.
        path_prefix: Path prefix.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListAttachedUserPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list attached user policies") from exc
    return ListAttachedUserPoliciesResult(
        attached_policies=resp.get("AttachedPolicies"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_entities_for_policy(
    policy_arn: str,
    *,
    entity_filter: str | None = None,
    path_prefix: str | None = None,
    policy_usage_filter: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListEntitiesForPolicyResult:
    """List entities for policy.

    Args:
        policy_arn: Policy arn.
        entity_filter: Entity filter.
        path_prefix: Path prefix.
        policy_usage_filter: Policy usage filter.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    if entity_filter is not None:
        kwargs["EntityFilter"] = entity_filter
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if policy_usage_filter is not None:
        kwargs["PolicyUsageFilter"] = policy_usage_filter
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListEntitiesForPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list entities for policy") from exc
    return ListEntitiesForPolicyResult(
        policy_groups=resp.get("PolicyGroups"),
        policy_users=resp.get("PolicyUsers"),
        policy_roles=resp.get("PolicyRoles"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_group_policies(
    group_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListGroupPoliciesResult:
    """List group policies.

    Args:
        group_name: Group name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListGroupPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list group policies") from exc
    return ListGroupPoliciesResult(
        policy_names=resp.get("PolicyNames"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_groups(
    *,
    path_prefix: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListGroupsResult:
    """List groups.

    Args:
        path_prefix: Path prefix.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list groups") from exc
    return ListGroupsResult(
        groups=resp.get("Groups"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_groups_for_user(
    user_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListGroupsForUserResult:
    """List groups for user.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListGroupsForUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list groups for user") from exc
    return ListGroupsForUserResult(
        groups=resp.get("Groups"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_instance_profile_tags(
    instance_profile_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListInstanceProfileTagsResult:
    """List instance profile tags.

    Args:
        instance_profile_name: Instance profile name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListInstanceProfileTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list instance profile tags") from exc
    return ListInstanceProfileTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_instance_profiles(
    *,
    path_prefix: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListInstanceProfilesResult:
    """List instance profiles.

    Args:
        path_prefix: Path prefix.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListInstanceProfiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list instance profiles") from exc
    return ListInstanceProfilesResult(
        instance_profiles=resp.get("InstanceProfiles"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_instance_profiles_for_role(
    role_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListInstanceProfilesForRoleResult:
    """List instance profiles for role.

    Args:
        role_name: Role name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListInstanceProfilesForRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list instance profiles for role") from exc
    return ListInstanceProfilesForRoleResult(
        instance_profiles=resp.get("InstanceProfiles"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_mfa_device_tags(
    serial_number: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListMfaDeviceTagsResult:
    """List mfa device tags.

    Args:
        serial_number: Serial number.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SerialNumber"] = serial_number
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListMFADeviceTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list mfa device tags") from exc
    return ListMfaDeviceTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_mfa_devices(
    *,
    user_name: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListMfaDevicesResult:
    """List mfa devices.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListMFADevices", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list mfa devices") from exc
    return ListMfaDevicesResult(
        mfa_devices=resp.get("MFADevices"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_open_id_connect_provider_tags(
    open_id_connect_provider_arn: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListOpenIdConnectProviderTagsResult:
    """List open id connect provider tags.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListOpenIDConnectProviderTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list open id connect provider tags") from exc
    return ListOpenIdConnectProviderTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_open_id_connect_providers(
    region_name: str | None = None,
) -> ListOpenIdConnectProvidersResult:
    """List open id connect providers.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("ListOpenIDConnectProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list open id connect providers") from exc
    return ListOpenIdConnectProvidersResult(
        open_id_connect_provider_list=resp.get("OpenIDConnectProviderList"),
    )


async def list_organizations_features(
    region_name: str | None = None,
) -> ListOrganizationsFeaturesResult:
    """List organizations features.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("ListOrganizationsFeatures", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list organizations features") from exc
    return ListOrganizationsFeaturesResult(
        organization_id=resp.get("OrganizationId"),
        enabled_features=resp.get("EnabledFeatures"),
    )


async def list_policies_granting_service_access(
    arn: str,
    service_namespaces: list[str],
    *,
    marker: str | None = None,
    region_name: str | None = None,
) -> ListPoliciesGrantingServiceAccessResult:
    """List policies granting service access.

    Args:
        arn: Arn.
        service_namespaces: Service namespaces.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["ServiceNamespaces"] = service_namespaces
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("ListPoliciesGrantingServiceAccess", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list policies granting service access") from exc
    return ListPoliciesGrantingServiceAccessResult(
        policies_granting_service_access=resp.get("PoliciesGrantingServiceAccess"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_policy_tags(
    policy_arn: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListPolicyTagsResult:
    """List policy tags.

    Args:
        policy_arn: Policy arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListPolicyTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list policy tags") from exc
    return ListPolicyTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_policy_versions(
    policy_arn: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListPolicyVersionsResult:
    """List policy versions.

    Args:
        policy_arn: Policy arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListPolicyVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list policy versions") from exc
    return ListPolicyVersionsResult(
        versions=resp.get("Versions"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_role_policies(
    role_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListRolePoliciesResult:
    """List role policies.

    Args:
        role_name: Role name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListRolePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list role policies") from exc
    return ListRolePoliciesResult(
        policy_names=resp.get("PolicyNames"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_role_tags(
    role_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListRoleTagsResult:
    """List role tags.

    Args:
        role_name: Role name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListRoleTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list role tags") from exc
    return ListRoleTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_saml_provider_tags(
    saml_provider_arn: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListSamlProviderTagsResult:
    """List saml provider tags.

    Args:
        saml_provider_arn: Saml provider arn.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLProviderArn"] = saml_provider_arn
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListSAMLProviderTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list saml provider tags") from exc
    return ListSamlProviderTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_saml_providers(
    region_name: str | None = None,
) -> ListSamlProvidersResult:
    """List saml providers.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("ListSAMLProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list saml providers") from exc
    return ListSamlProvidersResult(
        saml_provider_list=resp.get("SAMLProviderList"),
    )


async def list_server_certificate_tags(
    server_certificate_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListServerCertificateTagsResult:
    """List server certificate tags.

    Args:
        server_certificate_name: Server certificate name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListServerCertificateTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list server certificate tags") from exc
    return ListServerCertificateTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_server_certificates(
    *,
    path_prefix: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListServerCertificatesResult:
    """List server certificates.

    Args:
        path_prefix: Path prefix.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if path_prefix is not None:
        kwargs["PathPrefix"] = path_prefix
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListServerCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list server certificates") from exc
    return ListServerCertificatesResult(
        server_certificate_metadata_list=resp.get("ServerCertificateMetadataList"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_service_specific_credentials(
    *,
    user_name: str | None = None,
    service_name: str | None = None,
    all_users: bool | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListServiceSpecificCredentialsResult:
    """List service specific credentials.

    Args:
        user_name: User name.
        service_name: Service name.
        all_users: All users.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    if service_name is not None:
        kwargs["ServiceName"] = service_name
    if all_users is not None:
        kwargs["AllUsers"] = all_users
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListServiceSpecificCredentials", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list service specific credentials") from exc
    return ListServiceSpecificCredentialsResult(
        service_specific_credentials=resp.get("ServiceSpecificCredentials"),
        marker=resp.get("Marker"),
        is_truncated=resp.get("IsTruncated"),
    )


async def list_signing_certificates(
    *,
    user_name: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListSigningCertificatesResult:
    """List signing certificates.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListSigningCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list signing certificates") from exc
    return ListSigningCertificatesResult(
        certificates=resp.get("Certificates"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_ssh_public_keys(
    *,
    user_name: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListSshPublicKeysResult:
    """List ssh public keys.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if user_name is not None:
        kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListSSHPublicKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ssh public keys") from exc
    return ListSshPublicKeysResult(
        ssh_public_keys=resp.get("SSHPublicKeys"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_user_policies(
    user_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListUserPoliciesResult:
    """List user policies.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListUserPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list user policies") from exc
    return ListUserPoliciesResult(
        policy_names=resp.get("PolicyNames"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_user_tags(
    user_name: str,
    *,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListUserTagsResult:
    """List user tags.

    Args:
        user_name: User name.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListUserTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list user tags") from exc
    return ListUserTagsResult(
        tags=resp.get("Tags"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def list_virtual_mfa_devices(
    *,
    assignment_status: str | None = None,
    marker: str | None = None,
    max_items: int | None = None,
    region_name: str | None = None,
) -> ListVirtualMfaDevicesResult:
    """List virtual mfa devices.

    Args:
        assignment_status: Assignment status.
        marker: Marker.
        max_items: Max items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if assignment_status is not None:
        kwargs["AssignmentStatus"] = assignment_status
    if marker is not None:
        kwargs["Marker"] = marker
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    try:
        resp = await client.call("ListVirtualMFADevices", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list virtual mfa devices") from exc
    return ListVirtualMfaDevicesResult(
        virtual_mfa_devices=resp.get("VirtualMFADevices"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def put_group_policy(
    group_name: str,
    policy_name: str,
    policy_document: str,
    region_name: str | None = None,
) -> None:
    """Put group policy.

    Args:
        group_name: Group name.
        policy_name: Policy name.
        policy_document: Policy document.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["PolicyName"] = policy_name
    kwargs["PolicyDocument"] = policy_document
    try:
        await client.call("PutGroupPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put group policy") from exc
    return None


async def put_role_permissions_boundary(
    role_name: str,
    permissions_boundary: str,
    region_name: str | None = None,
) -> None:
    """Put role permissions boundary.

    Args:
        role_name: Role name.
        permissions_boundary: Permissions boundary.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["PermissionsBoundary"] = permissions_boundary
    try:
        await client.call("PutRolePermissionsBoundary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put role permissions boundary") from exc
    return None


async def put_role_policy(
    role_name: str,
    policy_name: str,
    policy_document: str,
    region_name: str | None = None,
) -> None:
    """Put role policy.

    Args:
        role_name: Role name.
        policy_name: Policy name.
        policy_document: Policy document.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["PolicyName"] = policy_name
    kwargs["PolicyDocument"] = policy_document
    try:
        await client.call("PutRolePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put role policy") from exc
    return None


async def put_user_permissions_boundary(
    user_name: str,
    permissions_boundary: str,
    region_name: str | None = None,
) -> None:
    """Put user permissions boundary.

    Args:
        user_name: User name.
        permissions_boundary: Permissions boundary.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["PermissionsBoundary"] = permissions_boundary
    try:
        await client.call("PutUserPermissionsBoundary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put user permissions boundary") from exc
    return None


async def put_user_policy(
    user_name: str,
    policy_name: str,
    policy_document: str,
    region_name: str | None = None,
) -> None:
    """Put user policy.

    Args:
        user_name: User name.
        policy_name: Policy name.
        policy_document: Policy document.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["PolicyName"] = policy_name
    kwargs["PolicyDocument"] = policy_document
    try:
        await client.call("PutUserPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put user policy") from exc
    return None


async def remove_client_id_from_open_id_connect_provider(
    open_id_connect_provider_arn: str,
    client_id: str,
    region_name: str | None = None,
) -> None:
    """Remove client id from open id connect provider.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        client_id: Client id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    kwargs["ClientID"] = client_id
    try:
        await client.call("RemoveClientIDFromOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to remove client id from open id connect provider"
        ) from exc
    return None


async def remove_role_from_instance_profile(
    instance_profile_name: str,
    role_name: str,
    region_name: str | None = None,
) -> None:
    """Remove role from instance profile.

    Args:
        instance_profile_name: Instance profile name.
        role_name: Role name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    kwargs["RoleName"] = role_name
    try:
        await client.call("RemoveRoleFromInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove role from instance profile") from exc
    return None


async def remove_user_from_group(
    group_name: str,
    user_name: str,
    region_name: str | None = None,
) -> None:
    """Remove user from group.

    Args:
        group_name: Group name.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["UserName"] = user_name
    try:
        await client.call("RemoveUserFromGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove user from group") from exc
    return None


async def reset_service_specific_credential(
    service_specific_credential_id: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> ResetServiceSpecificCredentialResult:
    """Reset service specific credential.

    Args:
        service_specific_credential_id: Service specific credential id.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceSpecificCredentialId"] = service_specific_credential_id
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        resp = await client.call("ResetServiceSpecificCredential", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reset service specific credential") from exc
    return ResetServiceSpecificCredentialResult(
        service_specific_credential=resp.get("ServiceSpecificCredential"),
    )


async def resync_mfa_device(
    user_name: str,
    serial_number: str,
    authentication_code1: str,
    authentication_code2: str,
    region_name: str | None = None,
) -> None:
    """Resync mfa device.

    Args:
        user_name: User name.
        serial_number: Serial number.
        authentication_code1: Authentication code1.
        authentication_code2: Authentication code2.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["SerialNumber"] = serial_number
    kwargs["AuthenticationCode1"] = authentication_code1
    kwargs["AuthenticationCode2"] = authentication_code2
    try:
        await client.call("ResyncMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resync mfa device") from exc
    return None


async def set_default_policy_version(
    policy_arn: str,
    version_id: str,
    region_name: str | None = None,
) -> None:
    """Set default policy version.

    Args:
        policy_arn: Policy arn.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    kwargs["VersionId"] = version_id
    try:
        await client.call("SetDefaultPolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set default policy version") from exc
    return None


async def set_security_token_service_preferences(
    global_endpoint_token_version: str,
    region_name: str | None = None,
) -> None:
    """Set security token service preferences.

    Args:
        global_endpoint_token_version: Global endpoint token version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalEndpointTokenVersion"] = global_endpoint_token_version
    try:
        await client.call("SetSecurityTokenServicePreferences", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set security token service preferences") from exc
    return None


async def simulate_custom_policy(
    policy_input_list: list[str],
    action_names: list[str],
    *,
    permissions_boundary_policy_input_list: list[str] | None = None,
    resource_arns: list[str] | None = None,
    resource_policy: str | None = None,
    resource_owner: str | None = None,
    caller_arn: str | None = None,
    context_entries: list[dict[str, Any]] | None = None,
    resource_handling_option: str | None = None,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> SimulateCustomPolicyResult:
    """Simulate custom policy.

    Args:
        policy_input_list: Policy input list.
        action_names: Action names.
        permissions_boundary_policy_input_list: Permissions boundary policy input list.
        resource_arns: Resource arns.
        resource_policy: Resource policy.
        resource_owner: Resource owner.
        caller_arn: Caller arn.
        context_entries: Context entries.
        resource_handling_option: Resource handling option.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyInputList"] = policy_input_list
    kwargs["ActionNames"] = action_names
    if permissions_boundary_policy_input_list is not None:
        kwargs["PermissionsBoundaryPolicyInputList"] = permissions_boundary_policy_input_list
    if resource_arns is not None:
        kwargs["ResourceArns"] = resource_arns
    if resource_policy is not None:
        kwargs["ResourcePolicy"] = resource_policy
    if resource_owner is not None:
        kwargs["ResourceOwner"] = resource_owner
    if caller_arn is not None:
        kwargs["CallerArn"] = caller_arn
    if context_entries is not None:
        kwargs["ContextEntries"] = context_entries
    if resource_handling_option is not None:
        kwargs["ResourceHandlingOption"] = resource_handling_option
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("SimulateCustomPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to simulate custom policy") from exc
    return SimulateCustomPolicyResult(
        evaluation_results=resp.get("EvaluationResults"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def simulate_principal_policy(
    policy_source_arn: str,
    action_names: list[str],
    *,
    policy_input_list: list[str] | None = None,
    permissions_boundary_policy_input_list: list[str] | None = None,
    resource_arns: list[str] | None = None,
    resource_policy: str | None = None,
    resource_owner: str | None = None,
    caller_arn: str | None = None,
    context_entries: list[dict[str, Any]] | None = None,
    resource_handling_option: str | None = None,
    max_items: int | None = None,
    marker: str | None = None,
    region_name: str | None = None,
) -> SimulatePrincipalPolicyResult:
    """Simulate principal policy.

    Args:
        policy_source_arn: Policy source arn.
        action_names: Action names.
        policy_input_list: Policy input list.
        permissions_boundary_policy_input_list: Permissions boundary policy input list.
        resource_arns: Resource arns.
        resource_policy: Resource policy.
        resource_owner: Resource owner.
        caller_arn: Caller arn.
        context_entries: Context entries.
        resource_handling_option: Resource handling option.
        max_items: Max items.
        marker: Marker.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicySourceArn"] = policy_source_arn
    kwargs["ActionNames"] = action_names
    if policy_input_list is not None:
        kwargs["PolicyInputList"] = policy_input_list
    if permissions_boundary_policy_input_list is not None:
        kwargs["PermissionsBoundaryPolicyInputList"] = permissions_boundary_policy_input_list
    if resource_arns is not None:
        kwargs["ResourceArns"] = resource_arns
    if resource_policy is not None:
        kwargs["ResourcePolicy"] = resource_policy
    if resource_owner is not None:
        kwargs["ResourceOwner"] = resource_owner
    if caller_arn is not None:
        kwargs["CallerArn"] = caller_arn
    if context_entries is not None:
        kwargs["ContextEntries"] = context_entries
    if resource_handling_option is not None:
        kwargs["ResourceHandlingOption"] = resource_handling_option
    if max_items is not None:
        kwargs["MaxItems"] = max_items
    if marker is not None:
        kwargs["Marker"] = marker
    try:
        resp = await client.call("SimulatePrincipalPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to simulate principal policy") from exc
    return SimulatePrincipalPolicyResult(
        evaluation_results=resp.get("EvaluationResults"),
        is_truncated=resp.get("IsTruncated"),
        marker=resp.get("Marker"),
    )


async def tag_instance_profile(
    instance_profile_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag instance profile.

    Args:
        instance_profile_name: Instance profile name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    kwargs["Tags"] = tags
    try:
        await client.call("TagInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag instance profile") from exc
    return None


async def tag_mfa_device(
    serial_number: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag mfa device.

    Args:
        serial_number: Serial number.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SerialNumber"] = serial_number
    kwargs["Tags"] = tags
    try:
        await client.call("TagMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag mfa device") from exc
    return None


async def tag_open_id_connect_provider(
    open_id_connect_provider_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag open id connect provider.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag open id connect provider") from exc
    return None


async def tag_policy(
    policy_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag policy.

    Args:
        policy_arn: Policy arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag policy") from exc
    return None


async def tag_role(
    role_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag role.

    Args:
        role_name: Role name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["Tags"] = tags
    try:
        await client.call("TagRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag role") from exc
    return None


async def tag_saml_provider(
    saml_provider_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag saml provider.

    Args:
        saml_provider_arn: Saml provider arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLProviderArn"] = saml_provider_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagSAMLProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag saml provider") from exc
    return None


async def tag_server_certificate(
    server_certificate_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag server certificate.

    Args:
        server_certificate_name: Server certificate name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    kwargs["Tags"] = tags
    try:
        await client.call("TagServerCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag server certificate") from exc
    return None


async def tag_user(
    user_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag user.

    Args:
        user_name: User name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["Tags"] = tags
    try:
        await client.call("TagUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag user") from exc
    return None


async def untag_instance_profile(
    instance_profile_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag instance profile.

    Args:
        instance_profile_name: Instance profile name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceProfileName"] = instance_profile_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagInstanceProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag instance profile") from exc
    return None


async def untag_mfa_device(
    serial_number: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag mfa device.

    Args:
        serial_number: Serial number.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SerialNumber"] = serial_number
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagMFADevice", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag mfa device") from exc
    return None


async def untag_open_id_connect_provider(
    open_id_connect_provider_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag open id connect provider.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagOpenIDConnectProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag open id connect provider") from exc
    return None


async def untag_policy(
    policy_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag policy.

    Args:
        policy_arn: Policy arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyArn"] = policy_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag policy") from exc
    return None


async def untag_role(
    role_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag role.

    Args:
        role_name: Role name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag role") from exc
    return None


async def untag_saml_provider(
    saml_provider_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag saml provider.

    Args:
        saml_provider_arn: Saml provider arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLProviderArn"] = saml_provider_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagSAMLProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag saml provider") from exc
    return None


async def untag_server_certificate(
    server_certificate_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag server certificate.

    Args:
        server_certificate_name: Server certificate name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagServerCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag server certificate") from exc
    return None


async def untag_user(
    user_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag user.

    Args:
        user_name: User name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag user") from exc
    return None


async def update_access_key(
    access_key_id: str,
    status: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update access key.

    Args:
        access_key_id: Access key id.
        status: Status.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessKeyId"] = access_key_id
    kwargs["Status"] = status
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("UpdateAccessKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update access key") from exc
    return None


async def update_account_password_policy(
    *,
    minimum_password_length: int | None = None,
    require_symbols: bool | None = None,
    require_numbers: bool | None = None,
    require_uppercase_characters: bool | None = None,
    require_lowercase_characters: bool | None = None,
    allow_users_to_change_password: bool | None = None,
    max_password_age: int | None = None,
    password_reuse_prevention: int | None = None,
    hard_expiry: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update account password policy.

    Args:
        minimum_password_length: Minimum password length.
        require_symbols: Require symbols.
        require_numbers: Require numbers.
        require_uppercase_characters: Require uppercase characters.
        require_lowercase_characters: Require lowercase characters.
        allow_users_to_change_password: Allow users to change password.
        max_password_age: Max password age.
        password_reuse_prevention: Password reuse prevention.
        hard_expiry: Hard expiry.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    if minimum_password_length is not None:
        kwargs["MinimumPasswordLength"] = minimum_password_length
    if require_symbols is not None:
        kwargs["RequireSymbols"] = require_symbols
    if require_numbers is not None:
        kwargs["RequireNumbers"] = require_numbers
    if require_uppercase_characters is not None:
        kwargs["RequireUppercaseCharacters"] = require_uppercase_characters
    if require_lowercase_characters is not None:
        kwargs["RequireLowercaseCharacters"] = require_lowercase_characters
    if allow_users_to_change_password is not None:
        kwargs["AllowUsersToChangePassword"] = allow_users_to_change_password
    if max_password_age is not None:
        kwargs["MaxPasswordAge"] = max_password_age
    if password_reuse_prevention is not None:
        kwargs["PasswordReusePrevention"] = password_reuse_prevention
    if hard_expiry is not None:
        kwargs["HardExpiry"] = hard_expiry
    try:
        await client.call("UpdateAccountPasswordPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account password policy") from exc
    return None


async def update_assume_role_policy(
    role_name: str,
    policy_document: str,
    region_name: str | None = None,
) -> None:
    """Update assume role policy.

    Args:
        role_name: Role name.
        policy_document: Policy document.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["PolicyDocument"] = policy_document
    try:
        await client.call("UpdateAssumeRolePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update assume role policy") from exc
    return None


async def update_group(
    group_name: str,
    *,
    new_path: str | None = None,
    new_group_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update group.

    Args:
        group_name: Group name.
        new_path: New path.
        new_group_name: New group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    if new_path is not None:
        kwargs["NewPath"] = new_path
    if new_group_name is not None:
        kwargs["NewGroupName"] = new_group_name
    try:
        await client.call("UpdateGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update group") from exc
    return None


async def update_login_profile(
    user_name: str,
    *,
    password: str | None = None,
    password_reset_required: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update login profile.

    Args:
        user_name: User name.
        password: Password.
        password_reset_required: Password reset required.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if password is not None:
        kwargs["Password"] = password
    if password_reset_required is not None:
        kwargs["PasswordResetRequired"] = password_reset_required
    try:
        await client.call("UpdateLoginProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update login profile") from exc
    return None


async def update_open_id_connect_provider_thumbprint(
    open_id_connect_provider_arn: str,
    thumbprint_list: list[str],
    region_name: str | None = None,
) -> None:
    """Update open id connect provider thumbprint.

    Args:
        open_id_connect_provider_arn: Open id connect provider arn.
        thumbprint_list: Thumbprint list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OpenIDConnectProviderArn"] = open_id_connect_provider_arn
    kwargs["ThumbprintList"] = thumbprint_list
    try:
        await client.call("UpdateOpenIDConnectProviderThumbprint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update open id connect provider thumbprint") from exc
    return None


async def update_role(
    role_name: str,
    *,
    description: str | None = None,
    max_session_duration: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update role.

    Args:
        role_name: Role name.
        description: Description.
        max_session_duration: Max session duration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    if description is not None:
        kwargs["Description"] = description
    if max_session_duration is not None:
        kwargs["MaxSessionDuration"] = max_session_duration
    try:
        await client.call("UpdateRole", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update role") from exc
    return None


async def update_role_description(
    role_name: str,
    description: str,
    region_name: str | None = None,
) -> UpdateRoleDescriptionResult:
    """Update role description.

    Args:
        role_name: Role name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleName"] = role_name
    kwargs["Description"] = description
    try:
        resp = await client.call("UpdateRoleDescription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update role description") from exc
    return UpdateRoleDescriptionResult(
        role=resp.get("Role"),
    )


async def update_saml_provider(
    saml_provider_arn: str,
    *,
    saml_metadata_document: str | None = None,
    assertion_encryption_mode: str | None = None,
    add_private_key: str | None = None,
    remove_private_key: str | None = None,
    region_name: str | None = None,
) -> UpdateSamlProviderResult:
    """Update saml provider.

    Args:
        saml_provider_arn: Saml provider arn.
        saml_metadata_document: Saml metadata document.
        assertion_encryption_mode: Assertion encryption mode.
        add_private_key: Add private key.
        remove_private_key: Remove private key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SAMLProviderArn"] = saml_provider_arn
    if saml_metadata_document is not None:
        kwargs["SAMLMetadataDocument"] = saml_metadata_document
    if assertion_encryption_mode is not None:
        kwargs["AssertionEncryptionMode"] = assertion_encryption_mode
    if add_private_key is not None:
        kwargs["AddPrivateKey"] = add_private_key
    if remove_private_key is not None:
        kwargs["RemovePrivateKey"] = remove_private_key
    try:
        resp = await client.call("UpdateSAMLProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update saml provider") from exc
    return UpdateSamlProviderResult(
        saml_provider_arn=resp.get("SAMLProviderArn"),
    )


async def update_server_certificate(
    server_certificate_name: str,
    *,
    new_path: str | None = None,
    new_server_certificate_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update server certificate.

    Args:
        server_certificate_name: Server certificate name.
        new_path: New path.
        new_server_certificate_name: New server certificate name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    if new_path is not None:
        kwargs["NewPath"] = new_path
    if new_server_certificate_name is not None:
        kwargs["NewServerCertificateName"] = new_server_certificate_name
    try:
        await client.call("UpdateServerCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update server certificate") from exc
    return None


async def update_service_specific_credential(
    service_specific_credential_id: str,
    status: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update service specific credential.

    Args:
        service_specific_credential_id: Service specific credential id.
        status: Status.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServiceSpecificCredentialId"] = service_specific_credential_id
    kwargs["Status"] = status
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("UpdateServiceSpecificCredential", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update service specific credential") from exc
    return None


async def update_signing_certificate(
    certificate_id: str,
    status: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update signing certificate.

    Args:
        certificate_id: Certificate id.
        status: Status.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateId"] = certificate_id
    kwargs["Status"] = status
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        await client.call("UpdateSigningCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update signing certificate") from exc
    return None


async def update_ssh_public_key(
    user_name: str,
    ssh_public_key_id: str,
    status: str,
    region_name: str | None = None,
) -> None:
    """Update ssh public key.

    Args:
        user_name: User name.
        ssh_public_key_id: Ssh public key id.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["SSHPublicKeyId"] = ssh_public_key_id
    kwargs["Status"] = status
    try:
        await client.call("UpdateSSHPublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ssh public key") from exc
    return None


async def update_user(
    user_name: str,
    *,
    new_path: str | None = None,
    new_user_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update user.

    Args:
        user_name: User name.
        new_path: New path.
        new_user_name: New user name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    if new_path is not None:
        kwargs["NewPath"] = new_path
    if new_user_name is not None:
        kwargs["NewUserName"] = new_user_name
    try:
        await client.call("UpdateUser", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update user") from exc
    return None


async def upload_server_certificate(
    server_certificate_name: str,
    certificate_body: str,
    private_key: str,
    *,
    path: str | None = None,
    certificate_chain: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UploadServerCertificateResult:
    """Upload server certificate.

    Args:
        server_certificate_name: Server certificate name.
        certificate_body: Certificate body.
        private_key: Private key.
        path: Path.
        certificate_chain: Certificate chain.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServerCertificateName"] = server_certificate_name
    kwargs["CertificateBody"] = certificate_body
    kwargs["PrivateKey"] = private_key
    if path is not None:
        kwargs["Path"] = path
    if certificate_chain is not None:
        kwargs["CertificateChain"] = certificate_chain
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("UploadServerCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to upload server certificate") from exc
    return UploadServerCertificateResult(
        server_certificate_metadata=resp.get("ServerCertificateMetadata"),
        tags=resp.get("Tags"),
    )


async def upload_signing_certificate(
    certificate_body: str,
    *,
    user_name: str | None = None,
    region_name: str | None = None,
) -> UploadSigningCertificateResult:
    """Upload signing certificate.

    Args:
        certificate_body: Certificate body.
        user_name: User name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CertificateBody"] = certificate_body
    if user_name is not None:
        kwargs["UserName"] = user_name
    try:
        resp = await client.call("UploadSigningCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to upload signing certificate") from exc
    return UploadSigningCertificateResult(
        certificate=resp.get("Certificate"),
    )


async def upload_ssh_public_key(
    user_name: str,
    ssh_public_key_body: str,
    region_name: str | None = None,
) -> UploadSshPublicKeyResult:
    """Upload ssh public key.

    Args:
        user_name: User name.
        ssh_public_key_body: Ssh public key body.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iam", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserName"] = user_name
    kwargs["SSHPublicKeyBody"] = ssh_public_key_body
    try:
        resp = await client.call("UploadSSHPublicKey", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to upload ssh public key") from exc
    return UploadSshPublicKeyResult(
        ssh_public_key=resp.get("SSHPublicKey"),
    )
