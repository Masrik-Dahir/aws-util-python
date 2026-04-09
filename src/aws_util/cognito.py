from __future__ import annotations

from datetime import datetime
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AdminGetDeviceResult",
    "AdminListDevicesResult",
    "AdminListGroupsForUserResult",
    "AdminListUserAuthEventsResult",
    "AdminRespondToAuthChallengeResult",
    "AssociateSoftwareTokenResult",
    "AuthResult",
    "CognitoUser",
    "CognitoUserPool",
    "ConfirmDeviceResult",
    "ConfirmSignUpResult",
    "CreateGroupResult",
    "CreateIdentityProviderResult",
    "CreateManagedLoginBrandingResult",
    "CreateResourceServerResult",
    "CreateTermsResult",
    "CreateUserImportJobResult",
    "CreateUserPoolClientResult",
    "CreateUserPoolDomainResult",
    "CreateUserPoolResult",
    "DescribeIdentityProviderResult",
    "DescribeManagedLoginBrandingByClientResult",
    "DescribeManagedLoginBrandingResult",
    "DescribeResourceServerResult",
    "DescribeRiskConfigurationResult",
    "DescribeTermsResult",
    "DescribeUserImportJobResult",
    "DescribeUserPoolClientResult",
    "DescribeUserPoolDomainResult",
    "DescribeUserPoolResult",
    "ForgotPasswordResult",
    "GetCsvHeaderResult",
    "GetDeviceResult",
    "GetGroupResult",
    "GetIdentityProviderByIdentifierResult",
    "GetLogDeliveryConfigurationResult",
    "GetSigningCertificateResult",
    "GetTokensFromRefreshTokenResult",
    "GetUiCustomizationResult",
    "GetUserAttributeVerificationCodeResult",
    "GetUserAuthFactorsResult",
    "GetUserPoolMfaConfigResult",
    "GetUserResult",
    "InitiateAuthResult",
    "ListDevicesResult",
    "ListGroupsResult",
    "ListIdentityProvidersResult",
    "ListResourceServersResult",
    "ListTagsForResourceResult",
    "ListTermsResult",
    "ListUserImportJobsResult",
    "ListUserPoolClientsResult",
    "ListUsersInGroupResult",
    "ListWebAuthnCredentialsResult",
    "ResendConfirmationCodeResult",
    "RespondToAuthChallengeResult",
    "SetLogDeliveryConfigurationResult",
    "SetRiskConfigurationResult",
    "SetUiCustomizationResult",
    "SetUserPoolMfaConfigResult",
    "SignUpResult",
    "StartUserImportJobResult",
    "StartWebAuthnRegistrationResult",
    "StopUserImportJobResult",
    "UpdateGroupResult",
    "UpdateIdentityProviderResult",
    "UpdateManagedLoginBrandingResult",
    "UpdateResourceServerResult",
    "UpdateTermsResult",
    "UpdateUserAttributesResult",
    "UpdateUserPoolClientResult",
    "UpdateUserPoolDomainResult",
    "VerifySoftwareTokenResult",
    "add_custom_attributes",
    "admin_add_user_to_group",
    "admin_confirm_sign_up",
    "admin_create_user",
    "admin_delete_user",
    "admin_delete_user_attributes",
    "admin_disable_provider_for_user",
    "admin_disable_user",
    "admin_enable_user",
    "admin_forget_device",
    "admin_get_device",
    "admin_get_user",
    "admin_initiate_auth",
    "admin_link_provider_for_user",
    "admin_list_devices",
    "admin_list_groups_for_user",
    "admin_list_user_auth_events",
    "admin_remove_user_from_group",
    "admin_reset_user_password",
    "admin_respond_to_auth_challenge",
    "admin_set_user_mfa_preference",
    "admin_set_user_password",
    "admin_set_user_settings",
    "admin_update_auth_event_feedback",
    "admin_update_device_status",
    "admin_update_user_attributes",
    "admin_user_global_sign_out",
    "associate_software_token",
    "bulk_create_users",
    "change_password",
    "complete_web_authn_registration",
    "confirm_device",
    "confirm_forgot_password",
    "confirm_sign_up",
    "create_group",
    "create_identity_provider",
    "create_managed_login_branding",
    "create_resource_server",
    "create_terms",
    "create_user_import_job",
    "create_user_pool",
    "create_user_pool_client",
    "create_user_pool_domain",
    "delete_group",
    "delete_identity_provider",
    "delete_managed_login_branding",
    "delete_resource_server",
    "delete_terms",
    "delete_user",
    "delete_user_attributes",
    "delete_user_pool",
    "delete_user_pool_client",
    "delete_user_pool_domain",
    "delete_web_authn_credential",
    "describe_identity_provider",
    "describe_managed_login_branding",
    "describe_managed_login_branding_by_client",
    "describe_resource_server",
    "describe_risk_configuration",
    "describe_terms",
    "describe_user_import_job",
    "describe_user_pool",
    "describe_user_pool_client",
    "describe_user_pool_domain",
    "forget_device",
    "forgot_password",
    "get_csv_header",
    "get_device",
    "get_group",
    "get_identity_provider_by_identifier",
    "get_log_delivery_configuration",
    "get_or_create_user",
    "get_signing_certificate",
    "get_tokens_from_refresh_token",
    "get_ui_customization",
    "get_user",
    "get_user_attribute_verification_code",
    "get_user_auth_factors",
    "get_user_pool_mfa_config",
    "global_sign_out",
    "initiate_auth",
    "list_devices",
    "list_groups",
    "list_identity_providers",
    "list_resource_servers",
    "list_tags_for_resource",
    "list_terms",
    "list_user_import_jobs",
    "list_user_pool_clients",
    "list_user_pools",
    "list_users",
    "list_users_in_group",
    "list_web_authn_credentials",
    "resend_confirmation_code",
    "reset_user_password",
    "respond_to_auth_challenge",
    "revoke_token",
    "set_log_delivery_configuration",
    "set_risk_configuration",
    "set_ui_customization",
    "set_user_mfa_preference",
    "set_user_pool_mfa_config",
    "set_user_settings",
    "sign_up",
    "start_user_import_job",
    "start_web_authn_registration",
    "stop_user_import_job",
    "tag_resource",
    "untag_resource",
    "update_auth_event_feedback",
    "update_device_status",
    "update_group",
    "update_identity_provider",
    "update_managed_login_branding",
    "update_resource_server",
    "update_terms",
    "update_user_attributes",
    "update_user_pool",
    "update_user_pool_client",
    "update_user_pool_domain",
    "verify_software_token",
    "verify_user_attribute",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CognitoUser(BaseModel):
    """A Cognito user pool user."""

    model_config = ConfigDict(frozen=True)

    username: str
    user_status: str
    enabled: bool = True
    create_date: datetime | None = None
    last_modified_date: datetime | None = None
    attributes: dict[str, str] = {}


class CognitoUserPool(BaseModel):
    """Metadata for a Cognito user pool."""

    model_config = ConfigDict(frozen=True)

    pool_id: str
    pool_name: str
    status: str | None = None
    last_modified_date: datetime | None = None
    creation_date: datetime | None = None


class AuthResult(BaseModel):
    """Authentication tokens returned from Cognito."""

    model_config = ConfigDict(frozen=True)

    access_token: str | None = None
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def admin_create_user(
    user_pool_id: str,
    username: str,
    temp_password: str | None = None,
    attributes: dict[str, str] | None = None,
    suppress_welcome_email: bool = False,
    region_name: str | None = None,
) -> CognitoUser:
    """Create a new user in a Cognito user pool (admin API).

    Args:
        user_pool_id: The user pool ID.
        username: Desired username.
        temp_password: Temporary password.  If ``None``, Cognito auto-generates
            one and sends it via the pool's email/SMS config.
        attributes: User attributes, e.g. ``{"email": "user@example.com"}``.
        suppress_welcome_email: Suppress the welcome message.
        region_name: AWS region override.

    Returns:
        The newly created :class:`CognitoUser`.

    Raises:
        RuntimeError: If user creation fails.
    """
    client = get_client("cognito-idp", region_name)
    user_attrs = [{"Name": k, "Value": v} for k, v in (attributes or {}).items()]
    kwargs: dict[str, Any] = {
        "UserPoolId": user_pool_id,
        "Username": username,
        "UserAttributes": user_attrs,
    }
    if temp_password:
        kwargs["TemporaryPassword"] = temp_password
    if suppress_welcome_email:
        kwargs["MessageAction"] = "SUPPRESS"

    try:
        resp = client.admin_create_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create Cognito user {username!r}") from exc
    return _parse_user(resp["User"])


def admin_get_user(
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> CognitoUser | None:
    """Fetch a Cognito user by username (admin API).

    Returns:
        A :class:`CognitoUser`, or ``None`` if not found.
    """
    client = get_client("cognito-idp", region_name)
    try:
        resp = client.admin_get_user(UserPoolId=user_pool_id, Username=username)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "UserNotFoundException":
            return None
        raise wrap_aws_error(exc, f"admin_get_user failed for {username!r}") from exc
    attrs = {a["Name"]: a["Value"] for a in resp.get("UserAttributes", [])}
    return CognitoUser(
        username=resp["Username"],
        user_status=resp["UserStatus"],
        enabled=resp.get("Enabled", True),
        create_date=resp.get("UserCreateDate"),
        last_modified_date=resp.get("UserLastModifiedDate"),
        attributes=attrs,
    )


def admin_delete_user(
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> None:
    """Delete a Cognito user (admin API).

    Args:
        user_pool_id: The user pool ID.
        username: Username to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = get_client("cognito-idp", region_name)
    try:
        client.admin_delete_user(UserPoolId=user_pool_id, Username=username)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete Cognito user {username!r}") from exc


def admin_set_user_password(
    user_pool_id: str,
    username: str,
    password: str,
    permanent: bool = True,
    region_name: str | None = None,
) -> None:
    """Set or reset a Cognito user's password (admin API).

    Args:
        user_pool_id: The user pool ID.
        username: Target username.
        password: New password.
        permanent: ``True`` (default) sets a permanent password.  ``False``
            sets a temporary password that requires a change on next sign-in.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the operation fails.
    """
    client = get_client("cognito-idp", region_name)
    try:
        client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=permanent,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to set password for Cognito user {username!r}") from exc


def admin_add_user_to_group(
    user_pool_id: str,
    username: str,
    group_name: str,
    region_name: str | None = None,
) -> None:
    """Add a Cognito user to a group (admin API).

    Args:
        user_pool_id: The user pool ID.
        username: Target username.
        group_name: Group to add the user to.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the operation fails.
    """
    client = get_client("cognito-idp", region_name)
    try:
        client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=username,
            GroupName=group_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to add {username!r} to group {group_name!r}") from exc


def admin_remove_user_from_group(
    user_pool_id: str,
    username: str,
    group_name: str,
    region_name: str | None = None,
) -> None:
    """Remove a Cognito user from a group (admin API).

    Args:
        user_pool_id: The user pool ID.
        username: Target username.
        group_name: Group to remove the user from.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the operation fails.
    """
    client = get_client("cognito-idp", region_name)
    try:
        client.admin_remove_user_from_group(
            UserPoolId=user_pool_id,
            Username=username,
            GroupName=group_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to remove {username!r} from group {group_name!r}"
        ) from exc


def list_users(
    user_pool_id: str,
    filter_str: str | None = None,
    attributes_to_get: list[str] | None = None,
    region_name: str | None = None,
) -> list[CognitoUser]:
    """List users in a Cognito user pool.

    Args:
        user_pool_id: The user pool ID.
        filter_str: Cognito filter expression, e.g.
            ``'email = "alice@example.com"'``.
        attributes_to_get: Subset of attributes to include in the response.
        region_name: AWS region override.

    Returns:
        A list of :class:`CognitoUser` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {"UserPoolId": user_pool_id}
    if filter_str:
        kwargs["Filter"] = filter_str
    if attributes_to_get:
        kwargs["AttributesToGet"] = attributes_to_get

    users: list[CognitoUser] = []
    try:
        paginator = client.get_paginator("list_users")
        for page in paginator.paginate(**kwargs):
            for user in page.get("Users", []):
                users.append(_parse_user(user))
    except ClientError as exc:
        raise wrap_aws_error(exc, f"list_users failed for pool {user_pool_id!r}") from exc
    return users


def admin_initiate_auth(
    user_pool_id: str,
    client_id: str,
    username: str,
    password: str,
    region_name: str | None = None,
) -> AuthResult:
    """Authenticate a user with username/password (admin API, no SRP).

    Args:
        user_pool_id: The user pool ID.
        client_id: The app client ID.
        username: Username.
        password: Password.
        region_name: AWS region override.

    Returns:
        An :class:`AuthResult` containing JWT tokens.

    Raises:
        RuntimeError: If authentication fails.
    """
    client = get_client("cognito-idp", region_name)
    try:
        resp = client.admin_initiate_auth(
            UserPoolId=user_pool_id,
            ClientId=client_id,
            AuthFlow="ADMIN_NO_SRP_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "admin_initiate_auth failed") from exc
    result = resp.get("AuthenticationResult", {})
    return AuthResult(
        access_token=result.get("AccessToken"),
        id_token=result.get("IdToken"),
        refresh_token=result.get("RefreshToken"),
        token_type=result.get("TokenType"),
        expires_in=result.get("ExpiresIn"),
    )


def list_user_pools(
    region_name: str | None = None,
) -> list[CognitoUserPool]:
    """List Cognito user pools in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`CognitoUserPool` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    pools: list[CognitoUserPool] = []
    try:
        paginator = client.get_paginator("list_user_pools")
        for page in paginator.paginate(MaxResults=60):
            for pool in page.get("UserPools", []):
                pools.append(
                    CognitoUserPool(
                        pool_id=pool["Id"],
                        pool_name=pool["Name"],
                        last_modified_date=pool.get("LastModifiedDate"),
                        creation_date=pool.get("CreationDate"),
                        status=pool.get("Status"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_user_pools failed") from exc
    return pools


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_user(user: dict) -> CognitoUser:
    attrs = {a["Name"]: a["Value"] for a in user.get("Attributes", [])}
    return CognitoUser(
        username=user["Username"],
        user_status=user.get("UserStatus", "UNKNOWN"),
        enabled=user.get("Enabled", True),
        create_date=user.get("UserCreateDate"),
        last_modified_date=user.get("UserLastModifiedDate"),
        attributes=attrs,
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def get_or_create_user(
    user_pool_id: str,
    username: str,
    attributes: dict[str, str] | None = None,
    temp_password: str | None = None,
    region_name: str | None = None,
) -> tuple[CognitoUser, bool]:
    """Get an existing Cognito user or create one if they do not exist.

    Args:
        user_pool_id: The user pool ID.
        username: Username to get or create.
        attributes: User attributes applied only when creating a new user.
        temp_password: Temporary password applied only when creating.
        region_name: AWS region override.

    Returns:
        A ``(user, created)`` tuple where *created* is ``True`` if the user
        was just created.

    Raises:
        RuntimeError: If the create or get call fails.
    """
    existing = admin_get_user(user_pool_id, username, region_name=region_name)
    if existing is not None:
        return existing, False

    user = admin_create_user(
        user_pool_id,
        username,
        temp_password=temp_password,
        attributes=attributes,
        region_name=region_name,
    )
    return user, True


def bulk_create_users(
    user_pool_id: str,
    users: list[dict[str, Any]],
    region_name: str | None = None,
) -> list[CognitoUser]:
    """Create multiple Cognito users from a list of user dicts.

    Each dict must have a ``"username"`` key and optionally ``"attributes"``
    and ``"temp_password"`` keys.

    Args:
        user_pool_id: The user pool ID.
        users: List of user definition dicts.
        region_name: AWS region override.

    Returns:
        A list of created :class:`CognitoUser` objects.

    Raises:
        RuntimeError: If any user creation fails.
    """
    created: list[CognitoUser] = []
    for user_def in users:
        user = admin_create_user(
            user_pool_id,
            username=user_def["username"],
            temp_password=user_def.get("temp_password"),
            attributes=user_def.get("attributes"),
            suppress_welcome_email=user_def.get("suppress_welcome_email", False),
            region_name=region_name,
        )
        created.append(user)
    return created


def reset_user_password(
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> None:
    """Trigger a password reset email/SMS for a Cognito user.

    Marks the user as requiring a password reset on next sign-in.

    Args:
        user_pool_id: The user pool ID.
        username: Target username.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the operation fails.
    """
    client = get_client("cognito-idp", region_name)
    try:
        client.admin_reset_user_password(UserPoolId=user_pool_id, Username=username)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"reset_user_password failed for {username!r}") from exc


class AdminGetDeviceResult(BaseModel):
    """Result of admin_get_device."""

    model_config = ConfigDict(frozen=True)

    device: dict[str, Any] | None = None


class AdminListDevicesResult(BaseModel):
    """Result of admin_list_devices."""

    model_config = ConfigDict(frozen=True)

    devices: list[dict[str, Any]] | None = None
    pagination_token: str | None = None


class AdminListGroupsForUserResult(BaseModel):
    """Result of admin_list_groups_for_user."""

    model_config = ConfigDict(frozen=True)

    groups: list[dict[str, Any]] | None = None
    next_token: str | None = None


class AdminListUserAuthEventsResult(BaseModel):
    """Result of admin_list_user_auth_events."""

    model_config = ConfigDict(frozen=True)

    auth_events: list[dict[str, Any]] | None = None
    next_token: str | None = None


class AdminRespondToAuthChallengeResult(BaseModel):
    """Result of admin_respond_to_auth_challenge."""

    model_config = ConfigDict(frozen=True)

    challenge_name: str | None = None
    session: str | None = None
    challenge_parameters: dict[str, Any] | None = None
    authentication_result: dict[str, Any] | None = None


class AssociateSoftwareTokenResult(BaseModel):
    """Result of associate_software_token."""

    model_config = ConfigDict(frozen=True)

    secret_code: str | None = None
    session: str | None = None


class ConfirmDeviceResult(BaseModel):
    """Result of confirm_device."""

    model_config = ConfigDict(frozen=True)

    user_confirmation_necessary: bool | None = None


class ConfirmSignUpResult(BaseModel):
    """Result of confirm_sign_up."""

    model_config = ConfigDict(frozen=True)

    session: str | None = None


class CreateGroupResult(BaseModel):
    """Result of create_group."""

    model_config = ConfigDict(frozen=True)

    group: dict[str, Any] | None = None


class CreateIdentityProviderResult(BaseModel):
    """Result of create_identity_provider."""

    model_config = ConfigDict(frozen=True)

    identity_provider: dict[str, Any] | None = None


class CreateManagedLoginBrandingResult(BaseModel):
    """Result of create_managed_login_branding."""

    model_config = ConfigDict(frozen=True)

    managed_login_branding: dict[str, Any] | None = None


class CreateResourceServerResult(BaseModel):
    """Result of create_resource_server."""

    model_config = ConfigDict(frozen=True)

    resource_server: dict[str, Any] | None = None


class CreateTermsResult(BaseModel):
    """Result of create_terms."""

    model_config = ConfigDict(frozen=True)

    terms: dict[str, Any] | None = None


class CreateUserImportJobResult(BaseModel):
    """Result of create_user_import_job."""

    model_config = ConfigDict(frozen=True)

    user_import_job: dict[str, Any] | None = None


class CreateUserPoolResult(BaseModel):
    """Result of create_user_pool."""

    model_config = ConfigDict(frozen=True)

    user_pool: dict[str, Any] | None = None


class CreateUserPoolClientResult(BaseModel):
    """Result of create_user_pool_client."""

    model_config = ConfigDict(frozen=True)

    user_pool_client: dict[str, Any] | None = None


class CreateUserPoolDomainResult(BaseModel):
    """Result of create_user_pool_domain."""

    model_config = ConfigDict(frozen=True)

    managed_login_version: int | None = None
    cloud_front_domain: str | None = None


class DescribeIdentityProviderResult(BaseModel):
    """Result of describe_identity_provider."""

    model_config = ConfigDict(frozen=True)

    identity_provider: dict[str, Any] | None = None


class DescribeManagedLoginBrandingResult(BaseModel):
    """Result of describe_managed_login_branding."""

    model_config = ConfigDict(frozen=True)

    managed_login_branding: dict[str, Any] | None = None


class DescribeManagedLoginBrandingByClientResult(BaseModel):
    """Result of describe_managed_login_branding_by_client."""

    model_config = ConfigDict(frozen=True)

    managed_login_branding: dict[str, Any] | None = None


class DescribeResourceServerResult(BaseModel):
    """Result of describe_resource_server."""

    model_config = ConfigDict(frozen=True)

    resource_server: dict[str, Any] | None = None


class DescribeRiskConfigurationResult(BaseModel):
    """Result of describe_risk_configuration."""

    model_config = ConfigDict(frozen=True)

    risk_configuration: dict[str, Any] | None = None


class DescribeTermsResult(BaseModel):
    """Result of describe_terms."""

    model_config = ConfigDict(frozen=True)

    terms: dict[str, Any] | None = None


class DescribeUserImportJobResult(BaseModel):
    """Result of describe_user_import_job."""

    model_config = ConfigDict(frozen=True)

    user_import_job: dict[str, Any] | None = None


class DescribeUserPoolResult(BaseModel):
    """Result of describe_user_pool."""

    model_config = ConfigDict(frozen=True)

    user_pool: dict[str, Any] | None = None


class DescribeUserPoolClientResult(BaseModel):
    """Result of describe_user_pool_client."""

    model_config = ConfigDict(frozen=True)

    user_pool_client: dict[str, Any] | None = None


class DescribeUserPoolDomainResult(BaseModel):
    """Result of describe_user_pool_domain."""

    model_config = ConfigDict(frozen=True)

    domain_description: dict[str, Any] | None = None


class ForgotPasswordResult(BaseModel):
    """Result of forgot_password."""

    model_config = ConfigDict(frozen=True)

    code_delivery_details: dict[str, Any] | None = None


class GetCsvHeaderResult(BaseModel):
    """Result of get_csv_header."""

    model_config = ConfigDict(frozen=True)

    user_pool_id: str | None = None
    csv_header: list[str] | None = None


class GetDeviceResult(BaseModel):
    """Result of get_device."""

    model_config = ConfigDict(frozen=True)

    device: dict[str, Any] | None = None


class GetGroupResult(BaseModel):
    """Result of get_group."""

    model_config = ConfigDict(frozen=True)

    group: dict[str, Any] | None = None


class GetIdentityProviderByIdentifierResult(BaseModel):
    """Result of get_identity_provider_by_identifier."""

    model_config = ConfigDict(frozen=True)

    identity_provider: dict[str, Any] | None = None


class GetLogDeliveryConfigurationResult(BaseModel):
    """Result of get_log_delivery_configuration."""

    model_config = ConfigDict(frozen=True)

    log_delivery_configuration: dict[str, Any] | None = None


class GetSigningCertificateResult(BaseModel):
    """Result of get_signing_certificate."""

    model_config = ConfigDict(frozen=True)

    certificate: str | None = None


class GetTokensFromRefreshTokenResult(BaseModel):
    """Result of get_tokens_from_refresh_token."""

    model_config = ConfigDict(frozen=True)

    authentication_result: dict[str, Any] | None = None


class GetUiCustomizationResult(BaseModel):
    """Result of get_ui_customization."""

    model_config = ConfigDict(frozen=True)

    ui_customization: dict[str, Any] | None = None


class GetUserResult(BaseModel):
    """Result of get_user."""

    model_config = ConfigDict(frozen=True)

    username: str | None = None
    user_attributes: list[dict[str, Any]] | None = None
    mfa_options: list[dict[str, Any]] | None = None
    preferred_mfa_setting: str | None = None
    user_mfa_setting_list: list[str] | None = None


class GetUserAttributeVerificationCodeResult(BaseModel):
    """Result of get_user_attribute_verification_code."""

    model_config = ConfigDict(frozen=True)

    code_delivery_details: dict[str, Any] | None = None


class GetUserAuthFactorsResult(BaseModel):
    """Result of get_user_auth_factors."""

    model_config = ConfigDict(frozen=True)

    username: str | None = None
    preferred_mfa_setting: str | None = None
    user_mfa_setting_list: list[str] | None = None
    configured_user_auth_factors: list[str] | None = None


class GetUserPoolMfaConfigResult(BaseModel):
    """Result of get_user_pool_mfa_config."""

    model_config = ConfigDict(frozen=True)

    sms_mfa_configuration: dict[str, Any] | None = None
    software_token_mfa_configuration: dict[str, Any] | None = None
    email_mfa_configuration: dict[str, Any] | None = None
    mfa_configuration: str | None = None
    web_authn_configuration: dict[str, Any] | None = None


class InitiateAuthResult(BaseModel):
    """Result of initiate_auth."""

    model_config = ConfigDict(frozen=True)

    challenge_name: str | None = None
    session: str | None = None
    challenge_parameters: dict[str, Any] | None = None
    authentication_result: dict[str, Any] | None = None
    available_challenges: list[str] | None = None


class ListDevicesResult(BaseModel):
    """Result of list_devices."""

    model_config = ConfigDict(frozen=True)

    devices: list[dict[str, Any]] | None = None
    pagination_token: str | None = None


class ListGroupsResult(BaseModel):
    """Result of list_groups."""

    model_config = ConfigDict(frozen=True)

    groups: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListIdentityProvidersResult(BaseModel):
    """Result of list_identity_providers."""

    model_config = ConfigDict(frozen=True)

    providers: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListResourceServersResult(BaseModel):
    """Result of list_resource_servers."""

    model_config = ConfigDict(frozen=True)

    resource_servers: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListTermsResult(BaseModel):
    """Result of list_terms."""

    model_config = ConfigDict(frozen=True)

    terms: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListUserImportJobsResult(BaseModel):
    """Result of list_user_import_jobs."""

    model_config = ConfigDict(frozen=True)

    user_import_jobs: list[dict[str, Any]] | None = None
    pagination_token: str | None = None


class ListUserPoolClientsResult(BaseModel):
    """Result of list_user_pool_clients."""

    model_config = ConfigDict(frozen=True)

    user_pool_clients: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListUsersInGroupResult(BaseModel):
    """Result of list_users_in_group."""

    model_config = ConfigDict(frozen=True)

    users: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListWebAuthnCredentialsResult(BaseModel):
    """Result of list_web_authn_credentials."""

    model_config = ConfigDict(frozen=True)

    credentials: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ResendConfirmationCodeResult(BaseModel):
    """Result of resend_confirmation_code."""

    model_config = ConfigDict(frozen=True)

    code_delivery_details: dict[str, Any] | None = None


class RespondToAuthChallengeResult(BaseModel):
    """Result of respond_to_auth_challenge."""

    model_config = ConfigDict(frozen=True)

    challenge_name: str | None = None
    session: str | None = None
    challenge_parameters: dict[str, Any] | None = None
    authentication_result: dict[str, Any] | None = None


class SetLogDeliveryConfigurationResult(BaseModel):
    """Result of set_log_delivery_configuration."""

    model_config = ConfigDict(frozen=True)

    log_delivery_configuration: dict[str, Any] | None = None


class SetRiskConfigurationResult(BaseModel):
    """Result of set_risk_configuration."""

    model_config = ConfigDict(frozen=True)

    risk_configuration: dict[str, Any] | None = None


class SetUiCustomizationResult(BaseModel):
    """Result of set_ui_customization."""

    model_config = ConfigDict(frozen=True)

    ui_customization: dict[str, Any] | None = None


class SetUserPoolMfaConfigResult(BaseModel):
    """Result of set_user_pool_mfa_config."""

    model_config = ConfigDict(frozen=True)

    sms_mfa_configuration: dict[str, Any] | None = None
    software_token_mfa_configuration: dict[str, Any] | None = None
    email_mfa_configuration: dict[str, Any] | None = None
    mfa_configuration: str | None = None
    web_authn_configuration: dict[str, Any] | None = None


class SignUpResult(BaseModel):
    """Result of sign_up."""

    model_config = ConfigDict(frozen=True)

    user_confirmed: bool | None = None
    code_delivery_details: dict[str, Any] | None = None
    user_sub: str | None = None
    session: str | None = None


class StartUserImportJobResult(BaseModel):
    """Result of start_user_import_job."""

    model_config = ConfigDict(frozen=True)

    user_import_job: dict[str, Any] | None = None


class StartWebAuthnRegistrationResult(BaseModel):
    """Result of start_web_authn_registration."""

    model_config = ConfigDict(frozen=True)

    credential_creation_options: dict[str, Any] | None = None


class StopUserImportJobResult(BaseModel):
    """Result of stop_user_import_job."""

    model_config = ConfigDict(frozen=True)

    user_import_job: dict[str, Any] | None = None


class UpdateGroupResult(BaseModel):
    """Result of update_group."""

    model_config = ConfigDict(frozen=True)

    group: dict[str, Any] | None = None


class UpdateIdentityProviderResult(BaseModel):
    """Result of update_identity_provider."""

    model_config = ConfigDict(frozen=True)

    identity_provider: dict[str, Any] | None = None


class UpdateManagedLoginBrandingResult(BaseModel):
    """Result of update_managed_login_branding."""

    model_config = ConfigDict(frozen=True)

    managed_login_branding: dict[str, Any] | None = None


class UpdateResourceServerResult(BaseModel):
    """Result of update_resource_server."""

    model_config = ConfigDict(frozen=True)

    resource_server: dict[str, Any] | None = None


class UpdateTermsResult(BaseModel):
    """Result of update_terms."""

    model_config = ConfigDict(frozen=True)

    terms: dict[str, Any] | None = None


class UpdateUserAttributesResult(BaseModel):
    """Result of update_user_attributes."""

    model_config = ConfigDict(frozen=True)

    code_delivery_details_list: list[dict[str, Any]] | None = None


class UpdateUserPoolClientResult(BaseModel):
    """Result of update_user_pool_client."""

    model_config = ConfigDict(frozen=True)

    user_pool_client: dict[str, Any] | None = None


class UpdateUserPoolDomainResult(BaseModel):
    """Result of update_user_pool_domain."""

    model_config = ConfigDict(frozen=True)

    managed_login_version: int | None = None
    cloud_front_domain: str | None = None


class VerifySoftwareTokenResult(BaseModel):
    """Result of verify_software_token."""

    model_config = ConfigDict(frozen=True)

    status: str | None = None
    session: str | None = None


def add_custom_attributes(
    user_pool_id: str,
    custom_attributes: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add custom attributes.

    Args:
        user_pool_id: User pool id.
        custom_attributes: Custom attributes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["CustomAttributes"] = custom_attributes
    try:
        client.add_custom_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add custom attributes") from exc
    return None


def admin_confirm_sign_up(
    user_pool_id: str,
    username: str,
    *,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Admin confirm sign up.

    Args:
        user_pool_id: User pool id.
        username: Username.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        client.admin_confirm_sign_up(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin confirm sign up") from exc
    return None


def admin_delete_user_attributes(
    user_pool_id: str,
    username: str,
    user_attribute_names: list[str],
    region_name: str | None = None,
) -> None:
    """Admin delete user attributes.

    Args:
        user_pool_id: User pool id.
        username: Username.
        user_attribute_names: User attribute names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["UserAttributeNames"] = user_attribute_names
    try:
        client.admin_delete_user_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin delete user attributes") from exc
    return None


def admin_disable_provider_for_user(
    user_pool_id: str,
    user: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Admin disable provider for user.

    Args:
        user_pool_id: User pool id.
        user: User.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["User"] = user
    try:
        client.admin_disable_provider_for_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin disable provider for user") from exc
    return None


def admin_disable_user(
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> None:
    """Admin disable user.

    Args:
        user_pool_id: User pool id.
        username: Username.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    try:
        client.admin_disable_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin disable user") from exc
    return None


def admin_enable_user(
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> None:
    """Admin enable user.

    Args:
        user_pool_id: User pool id.
        username: Username.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    try:
        client.admin_enable_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin enable user") from exc
    return None


def admin_forget_device(
    user_pool_id: str,
    username: str,
    device_key: str,
    region_name: str | None = None,
) -> None:
    """Admin forget device.

    Args:
        user_pool_id: User pool id.
        username: Username.
        device_key: Device key.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["DeviceKey"] = device_key
    try:
        client.admin_forget_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin forget device") from exc
    return None


def admin_get_device(
    device_key: str,
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> AdminGetDeviceResult:
    """Admin get device.

    Args:
        device_key: Device key.
        user_pool_id: User pool id.
        username: Username.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeviceKey"] = device_key
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    try:
        resp = client.admin_get_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin get device") from exc
    return AdminGetDeviceResult(
        device=resp.get("Device"),
    )


def admin_link_provider_for_user(
    user_pool_id: str,
    destination_user: dict[str, Any],
    source_user: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Admin link provider for user.

    Args:
        user_pool_id: User pool id.
        destination_user: Destination user.
        source_user: Source user.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["DestinationUser"] = destination_user
    kwargs["SourceUser"] = source_user
    try:
        client.admin_link_provider_for_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin link provider for user") from exc
    return None


def admin_list_devices(
    user_pool_id: str,
    username: str,
    *,
    limit: int | None = None,
    pagination_token: str | None = None,
    region_name: str | None = None,
) -> AdminListDevicesResult:
    """Admin list devices.

    Args:
        user_pool_id: User pool id.
        username: Username.
        limit: Limit.
        pagination_token: Pagination token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    if limit is not None:
        kwargs["Limit"] = limit
    if pagination_token is not None:
        kwargs["PaginationToken"] = pagination_token
    try:
        resp = client.admin_list_devices(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin list devices") from exc
    return AdminListDevicesResult(
        devices=resp.get("Devices"),
        pagination_token=resp.get("PaginationToken"),
    )


def admin_list_groups_for_user(
    username: str,
    user_pool_id: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> AdminListGroupsForUserResult:
    """Admin list groups for user.

    Args:
        username: Username.
        user_pool_id: User pool id.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Username"] = username
    kwargs["UserPoolId"] = user_pool_id
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.admin_list_groups_for_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin list groups for user") from exc
    return AdminListGroupsForUserResult(
        groups=resp.get("Groups"),
        next_token=resp.get("NextToken"),
    )


def admin_list_user_auth_events(
    user_pool_id: str,
    username: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> AdminListUserAuthEventsResult:
    """Admin list user auth events.

    Args:
        user_pool_id: User pool id.
        username: Username.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.admin_list_user_auth_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin list user auth events") from exc
    return AdminListUserAuthEventsResult(
        auth_events=resp.get("AuthEvents"),
        next_token=resp.get("NextToken"),
    )


def admin_reset_user_password(
    user_pool_id: str,
    username: str,
    *,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Admin reset user password.

    Args:
        user_pool_id: User pool id.
        username: Username.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        client.admin_reset_user_password(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin reset user password") from exc
    return None


def admin_respond_to_auth_challenge(
    user_pool_id: str,
    client_id: str,
    challenge_name: str,
    *,
    challenge_responses: dict[str, Any] | None = None,
    session: str | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    context_data: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> AdminRespondToAuthChallengeResult:
    """Admin respond to auth challenge.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        challenge_name: Challenge name.
        challenge_responses: Challenge responses.
        session: Session.
        analytics_metadata: Analytics metadata.
        context_data: Context data.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    kwargs["ChallengeName"] = challenge_name
    if challenge_responses is not None:
        kwargs["ChallengeResponses"] = challenge_responses
    if session is not None:
        kwargs["Session"] = session
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if context_data is not None:
        kwargs["ContextData"] = context_data
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.admin_respond_to_auth_challenge(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin respond to auth challenge") from exc
    return AdminRespondToAuthChallengeResult(
        challenge_name=resp.get("ChallengeName"),
        session=resp.get("Session"),
        challenge_parameters=resp.get("ChallengeParameters"),
        authentication_result=resp.get("AuthenticationResult"),
    )


def admin_set_user_mfa_preference(
    username: str,
    user_pool_id: str,
    *,
    sms_mfa_settings: dict[str, Any] | None = None,
    software_token_mfa_settings: dict[str, Any] | None = None,
    email_mfa_settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Admin set user mfa preference.

    Args:
        username: Username.
        user_pool_id: User pool id.
        sms_mfa_settings: Sms mfa settings.
        software_token_mfa_settings: Software token mfa settings.
        email_mfa_settings: Email mfa settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Username"] = username
    kwargs["UserPoolId"] = user_pool_id
    if sms_mfa_settings is not None:
        kwargs["SMSMfaSettings"] = sms_mfa_settings
    if software_token_mfa_settings is not None:
        kwargs["SoftwareTokenMfaSettings"] = software_token_mfa_settings
    if email_mfa_settings is not None:
        kwargs["EmailMfaSettings"] = email_mfa_settings
    try:
        client.admin_set_user_mfa_preference(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin set user mfa preference") from exc
    return None


def admin_set_user_settings(
    user_pool_id: str,
    username: str,
    mfa_options: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Admin set user settings.

    Args:
        user_pool_id: User pool id.
        username: Username.
        mfa_options: Mfa options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["MFAOptions"] = mfa_options
    try:
        client.admin_set_user_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin set user settings") from exc
    return None


def admin_update_auth_event_feedback(
    user_pool_id: str,
    username: str,
    event_id: str,
    feedback_value: str,
    region_name: str | None = None,
) -> None:
    """Admin update auth event feedback.

    Args:
        user_pool_id: User pool id.
        username: Username.
        event_id: Event id.
        feedback_value: Feedback value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["EventId"] = event_id
    kwargs["FeedbackValue"] = feedback_value
    try:
        client.admin_update_auth_event_feedback(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin update auth event feedback") from exc
    return None


def admin_update_device_status(
    user_pool_id: str,
    username: str,
    device_key: str,
    *,
    device_remembered_status: str | None = None,
    region_name: str | None = None,
) -> None:
    """Admin update device status.

    Args:
        user_pool_id: User pool id.
        username: Username.
        device_key: Device key.
        device_remembered_status: Device remembered status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["DeviceKey"] = device_key
    if device_remembered_status is not None:
        kwargs["DeviceRememberedStatus"] = device_remembered_status
    try:
        client.admin_update_device_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin update device status") from exc
    return None


def admin_update_user_attributes(
    user_pool_id: str,
    username: str,
    user_attributes: list[dict[str, Any]],
    *,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Admin update user attributes.

    Args:
        user_pool_id: User pool id.
        username: Username.
        user_attributes: User attributes.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["UserAttributes"] = user_attributes
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        client.admin_update_user_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin update user attributes") from exc
    return None


def admin_user_global_sign_out(
    user_pool_id: str,
    username: str,
    region_name: str | None = None,
) -> None:
    """Admin user global sign out.

    Args:
        user_pool_id: User pool id.
        username: Username.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    try:
        client.admin_user_global_sign_out(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to admin user global sign out") from exc
    return None


def associate_software_token(
    *,
    access_token: str | None = None,
    session: str | None = None,
    region_name: str | None = None,
) -> AssociateSoftwareTokenResult:
    """Associate software token.

    Args:
        access_token: Access token.
        session: Session.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    if access_token is not None:
        kwargs["AccessToken"] = access_token
    if session is not None:
        kwargs["Session"] = session
    try:
        resp = client.associate_software_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate software token") from exc
    return AssociateSoftwareTokenResult(
        secret_code=resp.get("SecretCode"),
        session=resp.get("Session"),
    )


def change_password(
    proposed_password: str,
    access_token: str,
    *,
    previous_password: str | None = None,
    region_name: str | None = None,
) -> None:
    """Change password.

    Args:
        proposed_password: Proposed password.
        access_token: Access token.
        previous_password: Previous password.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ProposedPassword"] = proposed_password
    kwargs["AccessToken"] = access_token
    if previous_password is not None:
        kwargs["PreviousPassword"] = previous_password
    try:
        client.change_password(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to change password") from exc
    return None


def complete_web_authn_registration(
    access_token: str,
    credential: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Complete web authn registration.

    Args:
        access_token: Access token.
        credential: Credential.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["Credential"] = credential
    try:
        client.complete_web_authn_registration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to complete web authn registration") from exc
    return None


def confirm_device(
    access_token: str,
    device_key: str,
    *,
    device_secret_verifier_config: dict[str, Any] | None = None,
    device_name: str | None = None,
    region_name: str | None = None,
) -> ConfirmDeviceResult:
    """Confirm device.

    Args:
        access_token: Access token.
        device_key: Device key.
        device_secret_verifier_config: Device secret verifier config.
        device_name: Device name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["DeviceKey"] = device_key
    if device_secret_verifier_config is not None:
        kwargs["DeviceSecretVerifierConfig"] = device_secret_verifier_config
    if device_name is not None:
        kwargs["DeviceName"] = device_name
    try:
        resp = client.confirm_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to confirm device") from exc
    return ConfirmDeviceResult(
        user_confirmation_necessary=resp.get("UserConfirmationNecessary"),
    )


def confirm_forgot_password(
    client_id: str,
    username: str,
    confirmation_code: str,
    password: str,
    *,
    secret_hash: str | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    user_context_data: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Confirm forgot password.

    Args:
        client_id: Client id.
        username: Username.
        confirmation_code: Confirmation code.
        password: Password.
        secret_hash: Secret hash.
        analytics_metadata: Analytics metadata.
        user_context_data: User context data.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientId"] = client_id
    kwargs["Username"] = username
    kwargs["ConfirmationCode"] = confirmation_code
    kwargs["Password"] = password
    if secret_hash is not None:
        kwargs["SecretHash"] = secret_hash
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        client.confirm_forgot_password(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to confirm forgot password") from exc
    return None


def confirm_sign_up(
    client_id: str,
    username: str,
    confirmation_code: str,
    *,
    secret_hash: str | None = None,
    force_alias_creation: bool | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    user_context_data: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    session: str | None = None,
    region_name: str | None = None,
) -> ConfirmSignUpResult:
    """Confirm sign up.

    Args:
        client_id: Client id.
        username: Username.
        confirmation_code: Confirmation code.
        secret_hash: Secret hash.
        force_alias_creation: Force alias creation.
        analytics_metadata: Analytics metadata.
        user_context_data: User context data.
        client_metadata: Client metadata.
        session: Session.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientId"] = client_id
    kwargs["Username"] = username
    kwargs["ConfirmationCode"] = confirmation_code
    if secret_hash is not None:
        kwargs["SecretHash"] = secret_hash
    if force_alias_creation is not None:
        kwargs["ForceAliasCreation"] = force_alias_creation
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    if session is not None:
        kwargs["Session"] = session
    try:
        resp = client.confirm_sign_up(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to confirm sign up") from exc
    return ConfirmSignUpResult(
        session=resp.get("Session"),
    )


def create_group(
    group_name: str,
    user_pool_id: str,
    *,
    description: str | None = None,
    role_arn: str | None = None,
    precedence: int | None = None,
    region_name: str | None = None,
) -> CreateGroupResult:
    """Create group.

    Args:
        group_name: Group name.
        user_pool_id: User pool id.
        description: Description.
        role_arn: Role arn.
        precedence: Precedence.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["UserPoolId"] = user_pool_id
    if description is not None:
        kwargs["Description"] = description
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    if precedence is not None:
        kwargs["Precedence"] = precedence
    try:
        resp = client.create_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create group") from exc
    return CreateGroupResult(
        group=resp.get("Group"),
    )


def create_identity_provider(
    user_pool_id: str,
    provider_name: str,
    provider_type: str,
    provider_details: dict[str, Any],
    *,
    attribute_mapping: dict[str, Any] | None = None,
    idp_identifiers: list[str] | None = None,
    region_name: str | None = None,
) -> CreateIdentityProviderResult:
    """Create identity provider.

    Args:
        user_pool_id: User pool id.
        provider_name: Provider name.
        provider_type: Provider type.
        provider_details: Provider details.
        attribute_mapping: Attribute mapping.
        idp_identifiers: Idp identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ProviderName"] = provider_name
    kwargs["ProviderType"] = provider_type
    kwargs["ProviderDetails"] = provider_details
    if attribute_mapping is not None:
        kwargs["AttributeMapping"] = attribute_mapping
    if idp_identifiers is not None:
        kwargs["IdpIdentifiers"] = idp_identifiers
    try:
        resp = client.create_identity_provider(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create identity provider") from exc
    return CreateIdentityProviderResult(
        identity_provider=resp.get("IdentityProvider"),
    )


def create_managed_login_branding(
    user_pool_id: str,
    client_id: str,
    *,
    use_cognito_provided_values: bool | None = None,
    settings: dict[str, Any] | None = None,
    assets: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateManagedLoginBrandingResult:
    """Create managed login branding.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        use_cognito_provided_values: Use cognito provided values.
        settings: Settings.
        assets: Assets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    if use_cognito_provided_values is not None:
        kwargs["UseCognitoProvidedValues"] = use_cognito_provided_values
    if settings is not None:
        kwargs["Settings"] = settings
    if assets is not None:
        kwargs["Assets"] = assets
    try:
        resp = client.create_managed_login_branding(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create managed login branding") from exc
    return CreateManagedLoginBrandingResult(
        managed_login_branding=resp.get("ManagedLoginBranding"),
    )


def create_resource_server(
    user_pool_id: str,
    identifier: str,
    name: str,
    *,
    scopes: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateResourceServerResult:
    """Create resource server.

    Args:
        user_pool_id: User pool id.
        identifier: Identifier.
        name: Name.
        scopes: Scopes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Identifier"] = identifier
    kwargs["Name"] = name
    if scopes is not None:
        kwargs["Scopes"] = scopes
    try:
        resp = client.create_resource_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create resource server") from exc
    return CreateResourceServerResult(
        resource_server=resp.get("ResourceServer"),
    )


def create_terms(
    user_pool_id: str,
    client_id: str,
    terms_name: str,
    terms_source: str,
    enforcement: str,
    *,
    links: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateTermsResult:
    """Create terms.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        terms_name: Terms name.
        terms_source: Terms source.
        enforcement: Enforcement.
        links: Links.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    kwargs["TermsName"] = terms_name
    kwargs["TermsSource"] = terms_source
    kwargs["Enforcement"] = enforcement
    if links is not None:
        kwargs["Links"] = links
    try:
        resp = client.create_terms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create terms") from exc
    return CreateTermsResult(
        terms=resp.get("Terms"),
    )


def create_user_import_job(
    job_name: str,
    user_pool_id: str,
    cloud_watch_logs_role_arn: str,
    region_name: str | None = None,
) -> CreateUserImportJobResult:
    """Create user import job.

    Args:
        job_name: Job name.
        user_pool_id: User pool id.
        cloud_watch_logs_role_arn: Cloud watch logs role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["JobName"] = job_name
    kwargs["UserPoolId"] = user_pool_id
    kwargs["CloudWatchLogsRoleArn"] = cloud_watch_logs_role_arn
    try:
        resp = client.create_user_import_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user import job") from exc
    return CreateUserImportJobResult(
        user_import_job=resp.get("UserImportJob"),
    )


def create_user_pool(
    pool_name: str,
    *,
    policies: dict[str, Any] | None = None,
    deletion_protection: str | None = None,
    lambda_config: dict[str, Any] | None = None,
    auto_verified_attributes: list[str] | None = None,
    alias_attributes: list[str] | None = None,
    username_attributes: list[str] | None = None,
    sms_verification_message: str | None = None,
    email_verification_message: str | None = None,
    email_verification_subject: str | None = None,
    verification_message_template: dict[str, Any] | None = None,
    sms_authentication_message: str | None = None,
    mfa_configuration: str | None = None,
    user_attribute_update_settings: dict[str, Any] | None = None,
    device_configuration: dict[str, Any] | None = None,
    email_configuration: dict[str, Any] | None = None,
    sms_configuration: dict[str, Any] | None = None,
    user_pool_tags: dict[str, Any] | None = None,
    admin_create_user_config: dict[str, Any] | None = None,
    schema: list[dict[str, Any]] | None = None,
    user_pool_add_ons: dict[str, Any] | None = None,
    username_configuration: dict[str, Any] | None = None,
    account_recovery_setting: dict[str, Any] | None = None,
    user_pool_tier: str | None = None,
    region_name: str | None = None,
) -> CreateUserPoolResult:
    """Create user pool.

    Args:
        pool_name: Pool name.
        policies: Policies.
        deletion_protection: Deletion protection.
        lambda_config: Lambda config.
        auto_verified_attributes: Auto verified attributes.
        alias_attributes: Alias attributes.
        username_attributes: Username attributes.
        sms_verification_message: Sms verification message.
        email_verification_message: Email verification message.
        email_verification_subject: Email verification subject.
        verification_message_template: Verification message template.
        sms_authentication_message: Sms authentication message.
        mfa_configuration: Mfa configuration.
        user_attribute_update_settings: User attribute update settings.
        device_configuration: Device configuration.
        email_configuration: Email configuration.
        sms_configuration: Sms configuration.
        user_pool_tags: User pool tags.
        admin_create_user_config: Admin create user config.
        schema: Schema.
        user_pool_add_ons: User pool add ons.
        username_configuration: Username configuration.
        account_recovery_setting: Account recovery setting.
        user_pool_tier: User pool tier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PoolName"] = pool_name
    if policies is not None:
        kwargs["Policies"] = policies
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if lambda_config is not None:
        kwargs["LambdaConfig"] = lambda_config
    if auto_verified_attributes is not None:
        kwargs["AutoVerifiedAttributes"] = auto_verified_attributes
    if alias_attributes is not None:
        kwargs["AliasAttributes"] = alias_attributes
    if username_attributes is not None:
        kwargs["UsernameAttributes"] = username_attributes
    if sms_verification_message is not None:
        kwargs["SmsVerificationMessage"] = sms_verification_message
    if email_verification_message is not None:
        kwargs["EmailVerificationMessage"] = email_verification_message
    if email_verification_subject is not None:
        kwargs["EmailVerificationSubject"] = email_verification_subject
    if verification_message_template is not None:
        kwargs["VerificationMessageTemplate"] = verification_message_template
    if sms_authentication_message is not None:
        kwargs["SmsAuthenticationMessage"] = sms_authentication_message
    if mfa_configuration is not None:
        kwargs["MfaConfiguration"] = mfa_configuration
    if user_attribute_update_settings is not None:
        kwargs["UserAttributeUpdateSettings"] = user_attribute_update_settings
    if device_configuration is not None:
        kwargs["DeviceConfiguration"] = device_configuration
    if email_configuration is not None:
        kwargs["EmailConfiguration"] = email_configuration
    if sms_configuration is not None:
        kwargs["SmsConfiguration"] = sms_configuration
    if user_pool_tags is not None:
        kwargs["UserPoolTags"] = user_pool_tags
    if admin_create_user_config is not None:
        kwargs["AdminCreateUserConfig"] = admin_create_user_config
    if schema is not None:
        kwargs["Schema"] = schema
    if user_pool_add_ons is not None:
        kwargs["UserPoolAddOns"] = user_pool_add_ons
    if username_configuration is not None:
        kwargs["UsernameConfiguration"] = username_configuration
    if account_recovery_setting is not None:
        kwargs["AccountRecoverySetting"] = account_recovery_setting
    if user_pool_tier is not None:
        kwargs["UserPoolTier"] = user_pool_tier
    try:
        resp = client.create_user_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user pool") from exc
    return CreateUserPoolResult(
        user_pool=resp.get("UserPool"),
    )


def create_user_pool_client(
    user_pool_id: str,
    client_name: str,
    *,
    generate_secret: bool | None = None,
    refresh_token_validity: int | None = None,
    access_token_validity: int | None = None,
    id_token_validity: int | None = None,
    token_validity_units: dict[str, Any] | None = None,
    read_attributes: list[str] | None = None,
    write_attributes: list[str] | None = None,
    explicit_auth_flows: list[str] | None = None,
    supported_identity_providers: list[str] | None = None,
    callback_ur_ls: list[str] | None = None,
    logout_ur_ls: list[str] | None = None,
    default_redirect_uri: str | None = None,
    allowed_o_auth_flows: list[str] | None = None,
    allowed_o_auth_scopes: list[str] | None = None,
    allowed_o_auth_flows_user_pool_client: bool | None = None,
    analytics_configuration: dict[str, Any] | None = None,
    prevent_user_existence_errors: str | None = None,
    enable_token_revocation: bool | None = None,
    enable_propagate_additional_user_context_data: bool | None = None,
    auth_session_validity: int | None = None,
    refresh_token_rotation: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUserPoolClientResult:
    """Create user pool client.

    Args:
        user_pool_id: User pool id.
        client_name: Client name.
        generate_secret: Generate secret.
        refresh_token_validity: Refresh token validity.
        access_token_validity: Access token validity.
        id_token_validity: Id token validity.
        token_validity_units: Token validity units.
        read_attributes: Read attributes.
        write_attributes: Write attributes.
        explicit_auth_flows: Explicit auth flows.
        supported_identity_providers: Supported identity providers.
        callback_ur_ls: Callback ur ls.
        logout_ur_ls: Logout ur ls.
        default_redirect_uri: Default redirect uri.
        allowed_o_auth_flows: Allowed o auth flows.
        allowed_o_auth_scopes: Allowed o auth scopes.
        allowed_o_auth_flows_user_pool_client: Allowed o auth flows user pool client.
        analytics_configuration: Analytics configuration.
        prevent_user_existence_errors: Prevent user existence errors.
        enable_token_revocation: Enable token revocation.
        enable_propagate_additional_user_context_data: Enable propagate additional user context data.
        auth_session_validity: Auth session validity.
        refresh_token_rotation: Refresh token rotation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientName"] = client_name
    if generate_secret is not None:
        kwargs["GenerateSecret"] = generate_secret
    if refresh_token_validity is not None:
        kwargs["RefreshTokenValidity"] = refresh_token_validity
    if access_token_validity is not None:
        kwargs["AccessTokenValidity"] = access_token_validity
    if id_token_validity is not None:
        kwargs["IdTokenValidity"] = id_token_validity
    if token_validity_units is not None:
        kwargs["TokenValidityUnits"] = token_validity_units
    if read_attributes is not None:
        kwargs["ReadAttributes"] = read_attributes
    if write_attributes is not None:
        kwargs["WriteAttributes"] = write_attributes
    if explicit_auth_flows is not None:
        kwargs["ExplicitAuthFlows"] = explicit_auth_flows
    if supported_identity_providers is not None:
        kwargs["SupportedIdentityProviders"] = supported_identity_providers
    if callback_ur_ls is not None:
        kwargs["CallbackURLs"] = callback_ur_ls
    if logout_ur_ls is not None:
        kwargs["LogoutURLs"] = logout_ur_ls
    if default_redirect_uri is not None:
        kwargs["DefaultRedirectURI"] = default_redirect_uri
    if allowed_o_auth_flows is not None:
        kwargs["AllowedOAuthFlows"] = allowed_o_auth_flows
    if allowed_o_auth_scopes is not None:
        kwargs["AllowedOAuthScopes"] = allowed_o_auth_scopes
    if allowed_o_auth_flows_user_pool_client is not None:
        kwargs["AllowedOAuthFlowsUserPoolClient"] = allowed_o_auth_flows_user_pool_client
    if analytics_configuration is not None:
        kwargs["AnalyticsConfiguration"] = analytics_configuration
    if prevent_user_existence_errors is not None:
        kwargs["PreventUserExistenceErrors"] = prevent_user_existence_errors
    if enable_token_revocation is not None:
        kwargs["EnableTokenRevocation"] = enable_token_revocation
    if enable_propagate_additional_user_context_data is not None:
        kwargs["EnablePropagateAdditionalUserContextData"] = (
            enable_propagate_additional_user_context_data
        )
    if auth_session_validity is not None:
        kwargs["AuthSessionValidity"] = auth_session_validity
    if refresh_token_rotation is not None:
        kwargs["RefreshTokenRotation"] = refresh_token_rotation
    try:
        resp = client.create_user_pool_client(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user pool client") from exc
    return CreateUserPoolClientResult(
        user_pool_client=resp.get("UserPoolClient"),
    )


def create_user_pool_domain(
    domain: str,
    user_pool_id: str,
    *,
    managed_login_version: int | None = None,
    custom_domain_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUserPoolDomainResult:
    """Create user pool domain.

    Args:
        domain: Domain.
        user_pool_id: User pool id.
        managed_login_version: Managed login version.
        custom_domain_config: Custom domain config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["UserPoolId"] = user_pool_id
    if managed_login_version is not None:
        kwargs["ManagedLoginVersion"] = managed_login_version
    if custom_domain_config is not None:
        kwargs["CustomDomainConfig"] = custom_domain_config
    try:
        resp = client.create_user_pool_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user pool domain") from exc
    return CreateUserPoolDomainResult(
        managed_login_version=resp.get("ManagedLoginVersion"),
        cloud_front_domain=resp.get("CloudFrontDomain"),
    )


def delete_group(
    group_name: str,
    user_pool_id: str,
    region_name: str | None = None,
) -> None:
    """Delete group.

    Args:
        group_name: Group name.
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["UserPoolId"] = user_pool_id
    try:
        client.delete_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete group") from exc
    return None


def delete_identity_provider(
    user_pool_id: str,
    provider_name: str,
    region_name: str | None = None,
) -> None:
    """Delete identity provider.

    Args:
        user_pool_id: User pool id.
        provider_name: Provider name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ProviderName"] = provider_name
    try:
        client.delete_identity_provider(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete identity provider") from exc
    return None


def delete_managed_login_branding(
    managed_login_branding_id: str,
    user_pool_id: str,
    region_name: str | None = None,
) -> None:
    """Delete managed login branding.

    Args:
        managed_login_branding_id: Managed login branding id.
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ManagedLoginBrandingId"] = managed_login_branding_id
    kwargs["UserPoolId"] = user_pool_id
    try:
        client.delete_managed_login_branding(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete managed login branding") from exc
    return None


def delete_resource_server(
    user_pool_id: str,
    identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete resource server.

    Args:
        user_pool_id: User pool id.
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Identifier"] = identifier
    try:
        client.delete_resource_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource server") from exc
    return None


def delete_terms(
    terms_id: str,
    user_pool_id: str,
    region_name: str | None = None,
) -> None:
    """Delete terms.

    Args:
        terms_id: Terms id.
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TermsId"] = terms_id
    kwargs["UserPoolId"] = user_pool_id
    try:
        client.delete_terms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete terms") from exc
    return None


def delete_user(
    access_token: str,
    region_name: str | None = None,
) -> None:
    """Delete user.

    Args:
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    try:
        client.delete_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user") from exc
    return None


def delete_user_attributes(
    user_attribute_names: list[str],
    access_token: str,
    region_name: str | None = None,
) -> None:
    """Delete user attributes.

    Args:
        user_attribute_names: User attribute names.
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserAttributeNames"] = user_attribute_names
    kwargs["AccessToken"] = access_token
    try:
        client.delete_user_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user attributes") from exc
    return None


def delete_user_pool(
    user_pool_id: str,
    region_name: str | None = None,
) -> None:
    """Delete user pool.

    Args:
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    try:
        client.delete_user_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user pool") from exc
    return None


def delete_user_pool_client(
    user_pool_id: str,
    client_id: str,
    region_name: str | None = None,
) -> None:
    """Delete user pool client.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    try:
        client.delete_user_pool_client(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user pool client") from exc
    return None


def delete_user_pool_domain(
    domain: str,
    user_pool_id: str,
    region_name: str | None = None,
) -> None:
    """Delete user pool domain.

    Args:
        domain: Domain.
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["UserPoolId"] = user_pool_id
    try:
        client.delete_user_pool_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user pool domain") from exc
    return None


def delete_web_authn_credential(
    access_token: str,
    credential_id: str,
    region_name: str | None = None,
) -> None:
    """Delete web authn credential.

    Args:
        access_token: Access token.
        credential_id: Credential id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["CredentialId"] = credential_id
    try:
        client.delete_web_authn_credential(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete web authn credential") from exc
    return None


def describe_identity_provider(
    user_pool_id: str,
    provider_name: str,
    region_name: str | None = None,
) -> DescribeIdentityProviderResult:
    """Describe identity provider.

    Args:
        user_pool_id: User pool id.
        provider_name: Provider name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ProviderName"] = provider_name
    try:
        resp = client.describe_identity_provider(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe identity provider") from exc
    return DescribeIdentityProviderResult(
        identity_provider=resp.get("IdentityProvider"),
    )


def describe_managed_login_branding(
    user_pool_id: str,
    managed_login_branding_id: str,
    *,
    return_merged_resources: bool | None = None,
    region_name: str | None = None,
) -> DescribeManagedLoginBrandingResult:
    """Describe managed login branding.

    Args:
        user_pool_id: User pool id.
        managed_login_branding_id: Managed login branding id.
        return_merged_resources: Return merged resources.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ManagedLoginBrandingId"] = managed_login_branding_id
    if return_merged_resources is not None:
        kwargs["ReturnMergedResources"] = return_merged_resources
    try:
        resp = client.describe_managed_login_branding(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe managed login branding") from exc
    return DescribeManagedLoginBrandingResult(
        managed_login_branding=resp.get("ManagedLoginBranding"),
    )


def describe_managed_login_branding_by_client(
    user_pool_id: str,
    client_id: str,
    *,
    return_merged_resources: bool | None = None,
    region_name: str | None = None,
) -> DescribeManagedLoginBrandingByClientResult:
    """Describe managed login branding by client.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        return_merged_resources: Return merged resources.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    if return_merged_resources is not None:
        kwargs["ReturnMergedResources"] = return_merged_resources
    try:
        resp = client.describe_managed_login_branding_by_client(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe managed login branding by client") from exc
    return DescribeManagedLoginBrandingByClientResult(
        managed_login_branding=resp.get("ManagedLoginBranding"),
    )


def describe_resource_server(
    user_pool_id: str,
    identifier: str,
    region_name: str | None = None,
) -> DescribeResourceServerResult:
    """Describe resource server.

    Args:
        user_pool_id: User pool id.
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Identifier"] = identifier
    try:
        resp = client.describe_resource_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe resource server") from exc
    return DescribeResourceServerResult(
        resource_server=resp.get("ResourceServer"),
    )


def describe_risk_configuration(
    user_pool_id: str,
    *,
    client_id: str | None = None,
    region_name: str | None = None,
) -> DescribeRiskConfigurationResult:
    """Describe risk configuration.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if client_id is not None:
        kwargs["ClientId"] = client_id
    try:
        resp = client.describe_risk_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe risk configuration") from exc
    return DescribeRiskConfigurationResult(
        risk_configuration=resp.get("RiskConfiguration"),
    )


def describe_terms(
    terms_id: str,
    user_pool_id: str,
    region_name: str | None = None,
) -> DescribeTermsResult:
    """Describe terms.

    Args:
        terms_id: Terms id.
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TermsId"] = terms_id
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.describe_terms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe terms") from exc
    return DescribeTermsResult(
        terms=resp.get("Terms"),
    )


def describe_user_import_job(
    user_pool_id: str,
    job_id: str,
    region_name: str | None = None,
) -> DescribeUserImportJobResult:
    """Describe user import job.

    Args:
        user_pool_id: User pool id.
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["JobId"] = job_id
    try:
        resp = client.describe_user_import_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user import job") from exc
    return DescribeUserImportJobResult(
        user_import_job=resp.get("UserImportJob"),
    )


def describe_user_pool(
    user_pool_id: str,
    region_name: str | None = None,
) -> DescribeUserPoolResult:
    """Describe user pool.

    Args:
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.describe_user_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user pool") from exc
    return DescribeUserPoolResult(
        user_pool=resp.get("UserPool"),
    )


def describe_user_pool_client(
    user_pool_id: str,
    client_id: str,
    region_name: str | None = None,
) -> DescribeUserPoolClientResult:
    """Describe user pool client.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    try:
        resp = client.describe_user_pool_client(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user pool client") from exc
    return DescribeUserPoolClientResult(
        user_pool_client=resp.get("UserPoolClient"),
    )


def describe_user_pool_domain(
    domain: str,
    region_name: str | None = None,
) -> DescribeUserPoolDomainResult:
    """Describe user pool domain.

    Args:
        domain: Domain.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    try:
        resp = client.describe_user_pool_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user pool domain") from exc
    return DescribeUserPoolDomainResult(
        domain_description=resp.get("DomainDescription"),
    )


def forget_device(
    device_key: str,
    *,
    access_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Forget device.

    Args:
        device_key: Device key.
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeviceKey"] = device_key
    if access_token is not None:
        kwargs["AccessToken"] = access_token
    try:
        client.forget_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to forget device") from exc
    return None


def forgot_password(
    client_id: str,
    username: str,
    *,
    secret_hash: str | None = None,
    user_context_data: dict[str, Any] | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ForgotPasswordResult:
    """Forgot password.

    Args:
        client_id: Client id.
        username: Username.
        secret_hash: Secret hash.
        user_context_data: User context data.
        analytics_metadata: Analytics metadata.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientId"] = client_id
    kwargs["Username"] = username
    if secret_hash is not None:
        kwargs["SecretHash"] = secret_hash
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.forgot_password(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to forgot password") from exc
    return ForgotPasswordResult(
        code_delivery_details=resp.get("CodeDeliveryDetails"),
    )


def get_csv_header(
    user_pool_id: str,
    region_name: str | None = None,
) -> GetCsvHeaderResult:
    """Get csv header.

    Args:
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.get_csv_header(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get csv header") from exc
    return GetCsvHeaderResult(
        user_pool_id=resp.get("UserPoolId"),
        csv_header=resp.get("CSVHeader"),
    )


def get_device(
    device_key: str,
    *,
    access_token: str | None = None,
    region_name: str | None = None,
) -> GetDeviceResult:
    """Get device.

    Args:
        device_key: Device key.
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeviceKey"] = device_key
    if access_token is not None:
        kwargs["AccessToken"] = access_token
    try:
        resp = client.get_device(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get device") from exc
    return GetDeviceResult(
        device=resp.get("Device"),
    )


def get_group(
    group_name: str,
    user_pool_id: str,
    region_name: str | None = None,
) -> GetGroupResult:
    """Get group.

    Args:
        group_name: Group name.
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.get_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get group") from exc
    return GetGroupResult(
        group=resp.get("Group"),
    )


def get_identity_provider_by_identifier(
    user_pool_id: str,
    idp_identifier: str,
    region_name: str | None = None,
) -> GetIdentityProviderByIdentifierResult:
    """Get identity provider by identifier.

    Args:
        user_pool_id: User pool id.
        idp_identifier: Idp identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["IdpIdentifier"] = idp_identifier
    try:
        resp = client.get_identity_provider_by_identifier(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get identity provider by identifier") from exc
    return GetIdentityProviderByIdentifierResult(
        identity_provider=resp.get("IdentityProvider"),
    )


def get_log_delivery_configuration(
    user_pool_id: str,
    region_name: str | None = None,
) -> GetLogDeliveryConfigurationResult:
    """Get log delivery configuration.

    Args:
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.get_log_delivery_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get log delivery configuration") from exc
    return GetLogDeliveryConfigurationResult(
        log_delivery_configuration=resp.get("LogDeliveryConfiguration"),
    )


def get_signing_certificate(
    user_pool_id: str,
    region_name: str | None = None,
) -> GetSigningCertificateResult:
    """Get signing certificate.

    Args:
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.get_signing_certificate(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get signing certificate") from exc
    return GetSigningCertificateResult(
        certificate=resp.get("Certificate"),
    )


def get_tokens_from_refresh_token(
    refresh_token: str,
    client_id: str,
    *,
    client_secret: str | None = None,
    device_key: str | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetTokensFromRefreshTokenResult:
    """Get tokens from refresh token.

    Args:
        refresh_token: Refresh token.
        client_id: Client id.
        client_secret: Client secret.
        device_key: Device key.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RefreshToken"] = refresh_token
    kwargs["ClientId"] = client_id
    if client_secret is not None:
        kwargs["ClientSecret"] = client_secret
    if device_key is not None:
        kwargs["DeviceKey"] = device_key
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.get_tokens_from_refresh_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get tokens from refresh token") from exc
    return GetTokensFromRefreshTokenResult(
        authentication_result=resp.get("AuthenticationResult"),
    )


def get_ui_customization(
    user_pool_id: str,
    *,
    client_id: str | None = None,
    region_name: str | None = None,
) -> GetUiCustomizationResult:
    """Get ui customization.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if client_id is not None:
        kwargs["ClientId"] = client_id
    try:
        resp = client.get_ui_customization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get ui customization") from exc
    return GetUiCustomizationResult(
        ui_customization=resp.get("UICustomization"),
    )


def get_user(
    access_token: str,
    region_name: str | None = None,
) -> GetUserResult:
    """Get user.

    Args:
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    try:
        resp = client.get_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get user") from exc
    return GetUserResult(
        username=resp.get("Username"),
        user_attributes=resp.get("UserAttributes"),
        mfa_options=resp.get("MFAOptions"),
        preferred_mfa_setting=resp.get("PreferredMfaSetting"),
        user_mfa_setting_list=resp.get("UserMFASettingList"),
    )


def get_user_attribute_verification_code(
    access_token: str,
    attribute_name: str,
    *,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetUserAttributeVerificationCodeResult:
    """Get user attribute verification code.

    Args:
        access_token: Access token.
        attribute_name: Attribute name.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["AttributeName"] = attribute_name
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.get_user_attribute_verification_code(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get user attribute verification code") from exc
    return GetUserAttributeVerificationCodeResult(
        code_delivery_details=resp.get("CodeDeliveryDetails"),
    )


def get_user_auth_factors(
    access_token: str,
    region_name: str | None = None,
) -> GetUserAuthFactorsResult:
    """Get user auth factors.

    Args:
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    try:
        resp = client.get_user_auth_factors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get user auth factors") from exc
    return GetUserAuthFactorsResult(
        username=resp.get("Username"),
        preferred_mfa_setting=resp.get("PreferredMfaSetting"),
        user_mfa_setting_list=resp.get("UserMFASettingList"),
        configured_user_auth_factors=resp.get("ConfiguredUserAuthFactors"),
    )


def get_user_pool_mfa_config(
    user_pool_id: str,
    region_name: str | None = None,
) -> GetUserPoolMfaConfigResult:
    """Get user pool mfa config.

    Args:
        user_pool_id: User pool id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    try:
        resp = client.get_user_pool_mfa_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get user pool mfa config") from exc
    return GetUserPoolMfaConfigResult(
        sms_mfa_configuration=resp.get("SmsMfaConfiguration"),
        software_token_mfa_configuration=resp.get("SoftwareTokenMfaConfiguration"),
        email_mfa_configuration=resp.get("EmailMfaConfiguration"),
        mfa_configuration=resp.get("MfaConfiguration"),
        web_authn_configuration=resp.get("WebAuthnConfiguration"),
    )


def global_sign_out(
    access_token: str,
    region_name: str | None = None,
) -> None:
    """Global sign out.

    Args:
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    try:
        client.global_sign_out(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to global sign out") from exc
    return None


def initiate_auth(
    auth_flow: str,
    client_id: str,
    *,
    auth_parameters: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    user_context_data: dict[str, Any] | None = None,
    session: str | None = None,
    region_name: str | None = None,
) -> InitiateAuthResult:
    """Initiate auth.

    Args:
        auth_flow: Auth flow.
        client_id: Client id.
        auth_parameters: Auth parameters.
        client_metadata: Client metadata.
        analytics_metadata: Analytics metadata.
        user_context_data: User context data.
        session: Session.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthFlow"] = auth_flow
    kwargs["ClientId"] = client_id
    if auth_parameters is not None:
        kwargs["AuthParameters"] = auth_parameters
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if session is not None:
        kwargs["Session"] = session
    try:
        resp = client.initiate_auth(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to initiate auth") from exc
    return InitiateAuthResult(
        challenge_name=resp.get("ChallengeName"),
        session=resp.get("Session"),
        challenge_parameters=resp.get("ChallengeParameters"),
        authentication_result=resp.get("AuthenticationResult"),
        available_challenges=resp.get("AvailableChallenges"),
    )


def list_devices(
    access_token: str,
    *,
    limit: int | None = None,
    pagination_token: str | None = None,
    region_name: str | None = None,
) -> ListDevicesResult:
    """List devices.

    Args:
        access_token: Access token.
        limit: Limit.
        pagination_token: Pagination token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    if limit is not None:
        kwargs["Limit"] = limit
    if pagination_token is not None:
        kwargs["PaginationToken"] = pagination_token
    try:
        resp = client.list_devices(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list devices") from exc
    return ListDevicesResult(
        devices=resp.get("Devices"),
        pagination_token=resp.get("PaginationToken"),
    )


def list_groups(
    user_pool_id: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListGroupsResult:
    """List groups.

    Args:
        user_pool_id: User pool id.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list groups") from exc
    return ListGroupsResult(
        groups=resp.get("Groups"),
        next_token=resp.get("NextToken"),
    )


def list_identity_providers(
    user_pool_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListIdentityProvidersResult:
    """List identity providers.

    Args:
        user_pool_id: User pool id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_identity_providers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list identity providers") from exc
    return ListIdentityProvidersResult(
        providers=resp.get("Providers"),
        next_token=resp.get("NextToken"),
    )


def list_resource_servers(
    user_pool_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceServersResult:
    """List resource servers.

    Args:
        user_pool_id: User pool id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_resource_servers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource servers") from exc
    return ListResourceServersResult(
        resource_servers=resp.get("ResourceServers"),
        next_token=resp.get("NextToken"),
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
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def list_terms(
    user_pool_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTermsResult:
    """List terms.

    Args:
        user_pool_id: User pool id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_terms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list terms") from exc
    return ListTermsResult(
        terms=resp.get("Terms"),
        next_token=resp.get("NextToken"),
    )


def list_user_import_jobs(
    user_pool_id: str,
    max_results: int,
    *,
    pagination_token: str | None = None,
    region_name: str | None = None,
) -> ListUserImportJobsResult:
    """List user import jobs.

    Args:
        user_pool_id: User pool id.
        max_results: Max results.
        pagination_token: Pagination token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["MaxResults"] = max_results
    if pagination_token is not None:
        kwargs["PaginationToken"] = pagination_token
    try:
        resp = client.list_user_import_jobs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list user import jobs") from exc
    return ListUserImportJobsResult(
        user_import_jobs=resp.get("UserImportJobs"),
        pagination_token=resp.get("PaginationToken"),
    )


def list_user_pool_clients(
    user_pool_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListUserPoolClientsResult:
    """List user pool clients.

    Args:
        user_pool_id: User pool id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_user_pool_clients(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list user pool clients") from exc
    return ListUserPoolClientsResult(
        user_pool_clients=resp.get("UserPoolClients"),
        next_token=resp.get("NextToken"),
    )


def list_users_in_group(
    user_pool_id: str,
    group_name: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListUsersInGroupResult:
    """List users in group.

    Args:
        user_pool_id: User pool id.
        group_name: Group name.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["GroupName"] = group_name
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_users_in_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list users in group") from exc
    return ListUsersInGroupResult(
        users=resp.get("Users"),
        next_token=resp.get("NextToken"),
    )


def list_web_authn_credentials(
    access_token: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListWebAuthnCredentialsResult:
    """List web authn credentials.

    Args:
        access_token: Access token.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_web_authn_credentials(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list web authn credentials") from exc
    return ListWebAuthnCredentialsResult(
        credentials=resp.get("Credentials"),
        next_token=resp.get("NextToken"),
    )


def resend_confirmation_code(
    client_id: str,
    username: str,
    *,
    secret_hash: str | None = None,
    user_context_data: dict[str, Any] | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ResendConfirmationCodeResult:
    """Resend confirmation code.

    Args:
        client_id: Client id.
        username: Username.
        secret_hash: Secret hash.
        user_context_data: User context data.
        analytics_metadata: Analytics metadata.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientId"] = client_id
    kwargs["Username"] = username
    if secret_hash is not None:
        kwargs["SecretHash"] = secret_hash
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.resend_confirmation_code(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to resend confirmation code") from exc
    return ResendConfirmationCodeResult(
        code_delivery_details=resp.get("CodeDeliveryDetails"),
    )


def respond_to_auth_challenge(
    client_id: str,
    challenge_name: str,
    *,
    session: str | None = None,
    challenge_responses: dict[str, Any] | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    user_context_data: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RespondToAuthChallengeResult:
    """Respond to auth challenge.

    Args:
        client_id: Client id.
        challenge_name: Challenge name.
        session: Session.
        challenge_responses: Challenge responses.
        analytics_metadata: Analytics metadata.
        user_context_data: User context data.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientId"] = client_id
    kwargs["ChallengeName"] = challenge_name
    if session is not None:
        kwargs["Session"] = session
    if challenge_responses is not None:
        kwargs["ChallengeResponses"] = challenge_responses
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.respond_to_auth_challenge(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to respond to auth challenge") from exc
    return RespondToAuthChallengeResult(
        challenge_name=resp.get("ChallengeName"),
        session=resp.get("Session"),
        challenge_parameters=resp.get("ChallengeParameters"),
        authentication_result=resp.get("AuthenticationResult"),
    )


def revoke_token(
    token: str,
    client_id: str,
    *,
    client_secret: str | None = None,
    region_name: str | None = None,
) -> None:
    """Revoke token.

    Args:
        token: Token.
        client_id: Client id.
        client_secret: Client secret.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Token"] = token
    kwargs["ClientId"] = client_id
    if client_secret is not None:
        kwargs["ClientSecret"] = client_secret
    try:
        client.revoke_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to revoke token") from exc
    return None


def set_log_delivery_configuration(
    user_pool_id: str,
    log_configurations: list[dict[str, Any]],
    region_name: str | None = None,
) -> SetLogDeliveryConfigurationResult:
    """Set log delivery configuration.

    Args:
        user_pool_id: User pool id.
        log_configurations: Log configurations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["LogConfigurations"] = log_configurations
    try:
        resp = client.set_log_delivery_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set log delivery configuration") from exc
    return SetLogDeliveryConfigurationResult(
        log_delivery_configuration=resp.get("LogDeliveryConfiguration"),
    )


def set_risk_configuration(
    user_pool_id: str,
    *,
    client_id: str | None = None,
    compromised_credentials_risk_configuration: dict[str, Any] | None = None,
    account_takeover_risk_configuration: dict[str, Any] | None = None,
    risk_exception_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SetRiskConfigurationResult:
    """Set risk configuration.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        compromised_credentials_risk_configuration: Compromised credentials risk configuration.
        account_takeover_risk_configuration: Account takeover risk configuration.
        risk_exception_configuration: Risk exception configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if client_id is not None:
        kwargs["ClientId"] = client_id
    if compromised_credentials_risk_configuration is not None:
        kwargs["CompromisedCredentialsRiskConfiguration"] = (
            compromised_credentials_risk_configuration
        )
    if account_takeover_risk_configuration is not None:
        kwargs["AccountTakeoverRiskConfiguration"] = account_takeover_risk_configuration
    if risk_exception_configuration is not None:
        kwargs["RiskExceptionConfiguration"] = risk_exception_configuration
    try:
        resp = client.set_risk_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set risk configuration") from exc
    return SetRiskConfigurationResult(
        risk_configuration=resp.get("RiskConfiguration"),
    )


def set_ui_customization(
    user_pool_id: str,
    *,
    client_id: str | None = None,
    css: str | None = None,
    image_file: bytes | None = None,
    region_name: str | None = None,
) -> SetUiCustomizationResult:
    """Set ui customization.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        css: Css.
        image_file: Image file.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if client_id is not None:
        kwargs["ClientId"] = client_id
    if css is not None:
        kwargs["CSS"] = css
    if image_file is not None:
        kwargs["ImageFile"] = image_file
    try:
        resp = client.set_ui_customization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set ui customization") from exc
    return SetUiCustomizationResult(
        ui_customization=resp.get("UICustomization"),
    )


def set_user_mfa_preference(
    access_token: str,
    *,
    sms_mfa_settings: dict[str, Any] | None = None,
    software_token_mfa_settings: dict[str, Any] | None = None,
    email_mfa_settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Set user mfa preference.

    Args:
        access_token: Access token.
        sms_mfa_settings: Sms mfa settings.
        software_token_mfa_settings: Software token mfa settings.
        email_mfa_settings: Email mfa settings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    if sms_mfa_settings is not None:
        kwargs["SMSMfaSettings"] = sms_mfa_settings
    if software_token_mfa_settings is not None:
        kwargs["SoftwareTokenMfaSettings"] = software_token_mfa_settings
    if email_mfa_settings is not None:
        kwargs["EmailMfaSettings"] = email_mfa_settings
    try:
        client.set_user_mfa_preference(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set user mfa preference") from exc
    return None


def set_user_pool_mfa_config(
    user_pool_id: str,
    *,
    sms_mfa_configuration: dict[str, Any] | None = None,
    software_token_mfa_configuration: dict[str, Any] | None = None,
    email_mfa_configuration: dict[str, Any] | None = None,
    mfa_configuration: str | None = None,
    web_authn_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SetUserPoolMfaConfigResult:
    """Set user pool mfa config.

    Args:
        user_pool_id: User pool id.
        sms_mfa_configuration: Sms mfa configuration.
        software_token_mfa_configuration: Software token mfa configuration.
        email_mfa_configuration: Email mfa configuration.
        mfa_configuration: Mfa configuration.
        web_authn_configuration: Web authn configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if sms_mfa_configuration is not None:
        kwargs["SmsMfaConfiguration"] = sms_mfa_configuration
    if software_token_mfa_configuration is not None:
        kwargs["SoftwareTokenMfaConfiguration"] = software_token_mfa_configuration
    if email_mfa_configuration is not None:
        kwargs["EmailMfaConfiguration"] = email_mfa_configuration
    if mfa_configuration is not None:
        kwargs["MfaConfiguration"] = mfa_configuration
    if web_authn_configuration is not None:
        kwargs["WebAuthnConfiguration"] = web_authn_configuration
    try:
        resp = client.set_user_pool_mfa_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set user pool mfa config") from exc
    return SetUserPoolMfaConfigResult(
        sms_mfa_configuration=resp.get("SmsMfaConfiguration"),
        software_token_mfa_configuration=resp.get("SoftwareTokenMfaConfiguration"),
        email_mfa_configuration=resp.get("EmailMfaConfiguration"),
        mfa_configuration=resp.get("MfaConfiguration"),
        web_authn_configuration=resp.get("WebAuthnConfiguration"),
    )


def set_user_settings(
    access_token: str,
    mfa_options: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Set user settings.

    Args:
        access_token: Access token.
        mfa_options: Mfa options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["MFAOptions"] = mfa_options
    try:
        client.set_user_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set user settings") from exc
    return None


def sign_up(
    client_id: str,
    username: str,
    *,
    secret_hash: str | None = None,
    password: str | None = None,
    user_attributes: list[dict[str, Any]] | None = None,
    validation_data: list[dict[str, Any]] | None = None,
    analytics_metadata: dict[str, Any] | None = None,
    user_context_data: dict[str, Any] | None = None,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SignUpResult:
    """Sign up.

    Args:
        client_id: Client id.
        username: Username.
        secret_hash: Secret hash.
        password: Password.
        user_attributes: User attributes.
        validation_data: Validation data.
        analytics_metadata: Analytics metadata.
        user_context_data: User context data.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClientId"] = client_id
    kwargs["Username"] = username
    if secret_hash is not None:
        kwargs["SecretHash"] = secret_hash
    if password is not None:
        kwargs["Password"] = password
    if user_attributes is not None:
        kwargs["UserAttributes"] = user_attributes
    if validation_data is not None:
        kwargs["ValidationData"] = validation_data
    if analytics_metadata is not None:
        kwargs["AnalyticsMetadata"] = analytics_metadata
    if user_context_data is not None:
        kwargs["UserContextData"] = user_context_data
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.sign_up(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to sign up") from exc
    return SignUpResult(
        user_confirmed=resp.get("UserConfirmed"),
        code_delivery_details=resp.get("CodeDeliveryDetails"),
        user_sub=resp.get("UserSub"),
        session=resp.get("Session"),
    )


def start_user_import_job(
    user_pool_id: str,
    job_id: str,
    region_name: str | None = None,
) -> StartUserImportJobResult:
    """Start user import job.

    Args:
        user_pool_id: User pool id.
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["JobId"] = job_id
    try:
        resp = client.start_user_import_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start user import job") from exc
    return StartUserImportJobResult(
        user_import_job=resp.get("UserImportJob"),
    )


def start_web_authn_registration(
    access_token: str,
    region_name: str | None = None,
) -> StartWebAuthnRegistrationResult:
    """Start web authn registration.

    Args:
        access_token: Access token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    try:
        resp = client.start_web_authn_registration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start web authn registration") from exc
    return StartWebAuthnRegistrationResult(
        credential_creation_options=resp.get("CredentialCreationOptions"),
    )


def stop_user_import_job(
    user_pool_id: str,
    job_id: str,
    region_name: str | None = None,
) -> StopUserImportJobResult:
    """Stop user import job.

    Args:
        user_pool_id: User pool id.
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["JobId"] = job_id
    try:
        resp = client.stop_user_import_job(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop user import job") from exc
    return StopUserImportJobResult(
        user_import_job=resp.get("UserImportJob"),
    )


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
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
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
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
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_auth_event_feedback(
    user_pool_id: str,
    username: str,
    event_id: str,
    feedback_token: str,
    feedback_value: str,
    region_name: str | None = None,
) -> None:
    """Update auth event feedback.

    Args:
        user_pool_id: User pool id.
        username: Username.
        event_id: Event id.
        feedback_token: Feedback token.
        feedback_value: Feedback value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Username"] = username
    kwargs["EventId"] = event_id
    kwargs["FeedbackToken"] = feedback_token
    kwargs["FeedbackValue"] = feedback_value
    try:
        client.update_auth_event_feedback(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update auth event feedback") from exc
    return None


def update_device_status(
    access_token: str,
    device_key: str,
    *,
    device_remembered_status: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update device status.

    Args:
        access_token: Access token.
        device_key: Device key.
        device_remembered_status: Device remembered status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["DeviceKey"] = device_key
    if device_remembered_status is not None:
        kwargs["DeviceRememberedStatus"] = device_remembered_status
    try:
        client.update_device_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update device status") from exc
    return None


def update_group(
    group_name: str,
    user_pool_id: str,
    *,
    description: str | None = None,
    role_arn: str | None = None,
    precedence: int | None = None,
    region_name: str | None = None,
) -> UpdateGroupResult:
    """Update group.

    Args:
        group_name: Group name.
        user_pool_id: User pool id.
        description: Description.
        role_arn: Role arn.
        precedence: Precedence.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupName"] = group_name
    kwargs["UserPoolId"] = user_pool_id
    if description is not None:
        kwargs["Description"] = description
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    if precedence is not None:
        kwargs["Precedence"] = precedence
    try:
        resp = client.update_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update group") from exc
    return UpdateGroupResult(
        group=resp.get("Group"),
    )


def update_identity_provider(
    user_pool_id: str,
    provider_name: str,
    *,
    provider_details: dict[str, Any] | None = None,
    attribute_mapping: dict[str, Any] | None = None,
    idp_identifiers: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateIdentityProviderResult:
    """Update identity provider.

    Args:
        user_pool_id: User pool id.
        provider_name: Provider name.
        provider_details: Provider details.
        attribute_mapping: Attribute mapping.
        idp_identifiers: Idp identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ProviderName"] = provider_name
    if provider_details is not None:
        kwargs["ProviderDetails"] = provider_details
    if attribute_mapping is not None:
        kwargs["AttributeMapping"] = attribute_mapping
    if idp_identifiers is not None:
        kwargs["IdpIdentifiers"] = idp_identifiers
    try:
        resp = client.update_identity_provider(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update identity provider") from exc
    return UpdateIdentityProviderResult(
        identity_provider=resp.get("IdentityProvider"),
    )


def update_managed_login_branding(
    *,
    user_pool_id: str | None = None,
    managed_login_branding_id: str | None = None,
    use_cognito_provided_values: bool | None = None,
    settings: dict[str, Any] | None = None,
    assets: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateManagedLoginBrandingResult:
    """Update managed login branding.

    Args:
        user_pool_id: User pool id.
        managed_login_branding_id: Managed login branding id.
        use_cognito_provided_values: Use cognito provided values.
        settings: Settings.
        assets: Assets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    if user_pool_id is not None:
        kwargs["UserPoolId"] = user_pool_id
    if managed_login_branding_id is not None:
        kwargs["ManagedLoginBrandingId"] = managed_login_branding_id
    if use_cognito_provided_values is not None:
        kwargs["UseCognitoProvidedValues"] = use_cognito_provided_values
    if settings is not None:
        kwargs["Settings"] = settings
    if assets is not None:
        kwargs["Assets"] = assets
    try:
        resp = client.update_managed_login_branding(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update managed login branding") from exc
    return UpdateManagedLoginBrandingResult(
        managed_login_branding=resp.get("ManagedLoginBranding"),
    )


def update_resource_server(
    user_pool_id: str,
    identifier: str,
    name: str,
    *,
    scopes: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateResourceServerResult:
    """Update resource server.

    Args:
        user_pool_id: User pool id.
        identifier: Identifier.
        name: Name.
        scopes: Scopes.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["Identifier"] = identifier
    kwargs["Name"] = name
    if scopes is not None:
        kwargs["Scopes"] = scopes
    try:
        resp = client.update_resource_server(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update resource server") from exc
    return UpdateResourceServerResult(
        resource_server=resp.get("ResourceServer"),
    )


def update_terms(
    terms_id: str,
    user_pool_id: str,
    *,
    terms_name: str | None = None,
    terms_source: str | None = None,
    enforcement: str | None = None,
    links: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateTermsResult:
    """Update terms.

    Args:
        terms_id: Terms id.
        user_pool_id: User pool id.
        terms_name: Terms name.
        terms_source: Terms source.
        enforcement: Enforcement.
        links: Links.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TermsId"] = terms_id
    kwargs["UserPoolId"] = user_pool_id
    if terms_name is not None:
        kwargs["TermsName"] = terms_name
    if terms_source is not None:
        kwargs["TermsSource"] = terms_source
    if enforcement is not None:
        kwargs["Enforcement"] = enforcement
    if links is not None:
        kwargs["Links"] = links
    try:
        resp = client.update_terms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update terms") from exc
    return UpdateTermsResult(
        terms=resp.get("Terms"),
    )


def update_user_attributes(
    user_attributes: list[dict[str, Any]],
    access_token: str,
    *,
    client_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateUserAttributesResult:
    """Update user attributes.

    Args:
        user_attributes: User attributes.
        access_token: Access token.
        client_metadata: Client metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserAttributes"] = user_attributes
    kwargs["AccessToken"] = access_token
    if client_metadata is not None:
        kwargs["ClientMetadata"] = client_metadata
    try:
        resp = client.update_user_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user attributes") from exc
    return UpdateUserAttributesResult(
        code_delivery_details_list=resp.get("CodeDeliveryDetailsList"),
    )


def update_user_pool(
    user_pool_id: str,
    *,
    policies: dict[str, Any] | None = None,
    deletion_protection: str | None = None,
    lambda_config: dict[str, Any] | None = None,
    auto_verified_attributes: list[str] | None = None,
    sms_verification_message: str | None = None,
    email_verification_message: str | None = None,
    email_verification_subject: str | None = None,
    verification_message_template: dict[str, Any] | None = None,
    sms_authentication_message: str | None = None,
    user_attribute_update_settings: dict[str, Any] | None = None,
    mfa_configuration: str | None = None,
    device_configuration: dict[str, Any] | None = None,
    email_configuration: dict[str, Any] | None = None,
    sms_configuration: dict[str, Any] | None = None,
    user_pool_tags: dict[str, Any] | None = None,
    admin_create_user_config: dict[str, Any] | None = None,
    user_pool_add_ons: dict[str, Any] | None = None,
    account_recovery_setting: dict[str, Any] | None = None,
    pool_name: str | None = None,
    user_pool_tier: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update user pool.

    Args:
        user_pool_id: User pool id.
        policies: Policies.
        deletion_protection: Deletion protection.
        lambda_config: Lambda config.
        auto_verified_attributes: Auto verified attributes.
        sms_verification_message: Sms verification message.
        email_verification_message: Email verification message.
        email_verification_subject: Email verification subject.
        verification_message_template: Verification message template.
        sms_authentication_message: Sms authentication message.
        user_attribute_update_settings: User attribute update settings.
        mfa_configuration: Mfa configuration.
        device_configuration: Device configuration.
        email_configuration: Email configuration.
        sms_configuration: Sms configuration.
        user_pool_tags: User pool tags.
        admin_create_user_config: Admin create user config.
        user_pool_add_ons: User pool add ons.
        account_recovery_setting: Account recovery setting.
        pool_name: Pool name.
        user_pool_tier: User pool tier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    if policies is not None:
        kwargs["Policies"] = policies
    if deletion_protection is not None:
        kwargs["DeletionProtection"] = deletion_protection
    if lambda_config is not None:
        kwargs["LambdaConfig"] = lambda_config
    if auto_verified_attributes is not None:
        kwargs["AutoVerifiedAttributes"] = auto_verified_attributes
    if sms_verification_message is not None:
        kwargs["SmsVerificationMessage"] = sms_verification_message
    if email_verification_message is not None:
        kwargs["EmailVerificationMessage"] = email_verification_message
    if email_verification_subject is not None:
        kwargs["EmailVerificationSubject"] = email_verification_subject
    if verification_message_template is not None:
        kwargs["VerificationMessageTemplate"] = verification_message_template
    if sms_authentication_message is not None:
        kwargs["SmsAuthenticationMessage"] = sms_authentication_message
    if user_attribute_update_settings is not None:
        kwargs["UserAttributeUpdateSettings"] = user_attribute_update_settings
    if mfa_configuration is not None:
        kwargs["MfaConfiguration"] = mfa_configuration
    if device_configuration is not None:
        kwargs["DeviceConfiguration"] = device_configuration
    if email_configuration is not None:
        kwargs["EmailConfiguration"] = email_configuration
    if sms_configuration is not None:
        kwargs["SmsConfiguration"] = sms_configuration
    if user_pool_tags is not None:
        kwargs["UserPoolTags"] = user_pool_tags
    if admin_create_user_config is not None:
        kwargs["AdminCreateUserConfig"] = admin_create_user_config
    if user_pool_add_ons is not None:
        kwargs["UserPoolAddOns"] = user_pool_add_ons
    if account_recovery_setting is not None:
        kwargs["AccountRecoverySetting"] = account_recovery_setting
    if pool_name is not None:
        kwargs["PoolName"] = pool_name
    if user_pool_tier is not None:
        kwargs["UserPoolTier"] = user_pool_tier
    try:
        client.update_user_pool(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user pool") from exc
    return None


def update_user_pool_client(
    user_pool_id: str,
    client_id: str,
    *,
    client_name: str | None = None,
    refresh_token_validity: int | None = None,
    access_token_validity: int | None = None,
    id_token_validity: int | None = None,
    token_validity_units: dict[str, Any] | None = None,
    read_attributes: list[str] | None = None,
    write_attributes: list[str] | None = None,
    explicit_auth_flows: list[str] | None = None,
    supported_identity_providers: list[str] | None = None,
    callback_ur_ls: list[str] | None = None,
    logout_ur_ls: list[str] | None = None,
    default_redirect_uri: str | None = None,
    allowed_o_auth_flows: list[str] | None = None,
    allowed_o_auth_scopes: list[str] | None = None,
    allowed_o_auth_flows_user_pool_client: bool | None = None,
    analytics_configuration: dict[str, Any] | None = None,
    prevent_user_existence_errors: str | None = None,
    enable_token_revocation: bool | None = None,
    enable_propagate_additional_user_context_data: bool | None = None,
    auth_session_validity: int | None = None,
    refresh_token_rotation: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateUserPoolClientResult:
    """Update user pool client.

    Args:
        user_pool_id: User pool id.
        client_id: Client id.
        client_name: Client name.
        refresh_token_validity: Refresh token validity.
        access_token_validity: Access token validity.
        id_token_validity: Id token validity.
        token_validity_units: Token validity units.
        read_attributes: Read attributes.
        write_attributes: Write attributes.
        explicit_auth_flows: Explicit auth flows.
        supported_identity_providers: Supported identity providers.
        callback_ur_ls: Callback ur ls.
        logout_ur_ls: Logout ur ls.
        default_redirect_uri: Default redirect uri.
        allowed_o_auth_flows: Allowed o auth flows.
        allowed_o_auth_scopes: Allowed o auth scopes.
        allowed_o_auth_flows_user_pool_client: Allowed o auth flows user pool client.
        analytics_configuration: Analytics configuration.
        prevent_user_existence_errors: Prevent user existence errors.
        enable_token_revocation: Enable token revocation.
        enable_propagate_additional_user_context_data: Enable propagate additional user context data.
        auth_session_validity: Auth session validity.
        refresh_token_rotation: Refresh token rotation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserPoolId"] = user_pool_id
    kwargs["ClientId"] = client_id
    if client_name is not None:
        kwargs["ClientName"] = client_name
    if refresh_token_validity is not None:
        kwargs["RefreshTokenValidity"] = refresh_token_validity
    if access_token_validity is not None:
        kwargs["AccessTokenValidity"] = access_token_validity
    if id_token_validity is not None:
        kwargs["IdTokenValidity"] = id_token_validity
    if token_validity_units is not None:
        kwargs["TokenValidityUnits"] = token_validity_units
    if read_attributes is not None:
        kwargs["ReadAttributes"] = read_attributes
    if write_attributes is not None:
        kwargs["WriteAttributes"] = write_attributes
    if explicit_auth_flows is not None:
        kwargs["ExplicitAuthFlows"] = explicit_auth_flows
    if supported_identity_providers is not None:
        kwargs["SupportedIdentityProviders"] = supported_identity_providers
    if callback_ur_ls is not None:
        kwargs["CallbackURLs"] = callback_ur_ls
    if logout_ur_ls is not None:
        kwargs["LogoutURLs"] = logout_ur_ls
    if default_redirect_uri is not None:
        kwargs["DefaultRedirectURI"] = default_redirect_uri
    if allowed_o_auth_flows is not None:
        kwargs["AllowedOAuthFlows"] = allowed_o_auth_flows
    if allowed_o_auth_scopes is not None:
        kwargs["AllowedOAuthScopes"] = allowed_o_auth_scopes
    if allowed_o_auth_flows_user_pool_client is not None:
        kwargs["AllowedOAuthFlowsUserPoolClient"] = allowed_o_auth_flows_user_pool_client
    if analytics_configuration is not None:
        kwargs["AnalyticsConfiguration"] = analytics_configuration
    if prevent_user_existence_errors is not None:
        kwargs["PreventUserExistenceErrors"] = prevent_user_existence_errors
    if enable_token_revocation is not None:
        kwargs["EnableTokenRevocation"] = enable_token_revocation
    if enable_propagate_additional_user_context_data is not None:
        kwargs["EnablePropagateAdditionalUserContextData"] = (
            enable_propagate_additional_user_context_data
        )
    if auth_session_validity is not None:
        kwargs["AuthSessionValidity"] = auth_session_validity
    if refresh_token_rotation is not None:
        kwargs["RefreshTokenRotation"] = refresh_token_rotation
    try:
        resp = client.update_user_pool_client(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user pool client") from exc
    return UpdateUserPoolClientResult(
        user_pool_client=resp.get("UserPoolClient"),
    )


def update_user_pool_domain(
    domain: str,
    user_pool_id: str,
    *,
    managed_login_version: int | None = None,
    custom_domain_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateUserPoolDomainResult:
    """Update user pool domain.

    Args:
        domain: Domain.
        user_pool_id: User pool id.
        managed_login_version: Managed login version.
        custom_domain_config: Custom domain config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Domain"] = domain
    kwargs["UserPoolId"] = user_pool_id
    if managed_login_version is not None:
        kwargs["ManagedLoginVersion"] = managed_login_version
    if custom_domain_config is not None:
        kwargs["CustomDomainConfig"] = custom_domain_config
    try:
        resp = client.update_user_pool_domain(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user pool domain") from exc
    return UpdateUserPoolDomainResult(
        managed_login_version=resp.get("ManagedLoginVersion"),
        cloud_front_domain=resp.get("CloudFrontDomain"),
    )


def verify_software_token(
    user_code: str,
    *,
    access_token: str | None = None,
    session: str | None = None,
    friendly_device_name: str | None = None,
    region_name: str | None = None,
) -> VerifySoftwareTokenResult:
    """Verify software token.

    Args:
        user_code: User code.
        access_token: Access token.
        session: Session.
        friendly_device_name: Friendly device name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserCode"] = user_code
    if access_token is not None:
        kwargs["AccessToken"] = access_token
    if session is not None:
        kwargs["Session"] = session
    if friendly_device_name is not None:
        kwargs["FriendlyDeviceName"] = friendly_device_name
    try:
        resp = client.verify_software_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to verify software token") from exc
    return VerifySoftwareTokenResult(
        status=resp.get("Status"),
        session=resp.get("Session"),
    )


def verify_user_attribute(
    access_token: str,
    attribute_name: str,
    code: str,
    region_name: str | None = None,
) -> None:
    """Verify user attribute.

    Args:
        access_token: Access token.
        attribute_name: Attribute name.
        code: Code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cognito-idp", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessToken"] = access_token
    kwargs["AttributeName"] = attribute_name
    kwargs["Code"] = code
    try:
        client.verify_user_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to verify user attribute") from exc
    return None
