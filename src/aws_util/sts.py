from __future__ import annotations

from datetime import datetime
from typing import Any

import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AssumeRoleWithSamlResult",
    "AssumeRoleWithWebIdentityResult",
    "AssumeRootResult",
    "AssumedRoleCredentials",
    "CallerIdentity",
    "DecodeAuthorizationMessageResult",
    "GetAccessKeyInfoResult",
    "GetDelegatedAccessTokenResult",
    "GetFederationTokenResult",
    "GetSessionTokenResult",
    "assume_role",
    "assume_role_session",
    "assume_role_with_saml",
    "assume_role_with_web_identity",
    "assume_root",
    "decode_authorization_message",
    "get_access_key_info",
    "get_account_id",
    "get_caller_identity",
    "get_delegated_access_token",
    "get_federation_token",
    "get_session_token",
    "is_valid_account_id",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CallerIdentity(BaseModel):
    """The identity of the caller making the AWS request."""

    model_config = ConfigDict(frozen=True)

    account_id: str
    arn: str
    user_id: str


class AssumedRoleCredentials(BaseModel):
    """Temporary credentials obtained by assuming an IAM role."""

    model_config = ConfigDict(frozen=True)

    access_key_id: str
    secret_access_key: str
    session_token: str
    expiration: datetime


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_caller_identity(
    region_name: str | None = None,
) -> CallerIdentity:
    """Return the identity of the AWS principal making this call.

    Equivalent to ``aws sts get-caller-identity``.  Useful for verifying
    which account/role is active at runtime.

    Args:
        region_name: AWS region override.

    Returns:
        A :class:`CallerIdentity` with account ID, ARN, and user ID.

    Raises:
        RuntimeError: If the STS call fails.
    """
    client = get_client("sts", region_name)
    try:
        resp = client.get_caller_identity()
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_caller_identity failed") from exc
    return CallerIdentity(
        account_id=resp["Account"],
        arn=resp["Arn"],
        user_id=resp["UserId"],
    )


def get_account_id(region_name: str | None = None) -> str:
    """Return the AWS account ID of the current caller.

    Args:
        region_name: AWS region override.

    Returns:
        12-digit AWS account ID as a string.
    """
    return get_caller_identity(region_name).account_id


def assume_role(
    role_arn: str,
    session_name: str,
    duration_seconds: int = 3600,
    external_id: str | None = None,
    region_name: str | None = None,
) -> AssumedRoleCredentials:
    """Assume an IAM role and return temporary credentials.

    Args:
        role_arn: ARN of the role to assume.
        session_name: Identifier for the assumed-role session (appears in
            CloudTrail logs).
        duration_seconds: Credential validity in seconds (900–43200).
            Defaults to ``3600`` (one hour).
        external_id: Optional external ID required by the role's trust policy.
        region_name: AWS region override.

    Returns:
        An :class:`AssumedRoleCredentials` with temporary access keys.

    Raises:
        RuntimeError: If the assume-role call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict = {
        "RoleArn": role_arn,
        "RoleSessionName": session_name,
        "DurationSeconds": duration_seconds,
    }
    if external_id is not None:
        kwargs["ExternalId"] = external_id

    try:
        resp = client.assume_role(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to assume role {role_arn!r}") from exc

    creds = resp["Credentials"]
    return AssumedRoleCredentials(
        access_key_id=creds["AccessKeyId"],
        secret_access_key=creds["SecretAccessKey"],
        session_token=creds["SessionToken"],
        expiration=creds["Expiration"],
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def assume_role_session(
    role_arn: str,
    session_name: str,
    duration_seconds: int = 3600,
    external_id: str | None = None,
    region_name: str | None = None,
) -> boto3.Session:
    """Assume an IAM role and return a ready-to-use boto3 Session.

    Combines :func:`assume_role` with ``boto3.Session`` construction so
    callers can immediately create service clients under the assumed role
    without manually threading credentials.

    Args:
        role_arn: ARN of the role to assume.
        session_name: Identifier for the session (appears in CloudTrail logs).
        duration_seconds: Credential validity in seconds (default ``3600``).
        external_id: Optional external ID required by the role's trust policy.
        region_name: AWS region for the returned session.

    Returns:
        A ``boto3.Session`` authenticated with the assumed role's temporary
        credentials.

    Raises:
        RuntimeError: If the assume-role call fails.
    """
    creds = assume_role(
        role_arn,
        session_name,
        duration_seconds=duration_seconds,
        external_id=external_id,
        region_name=region_name,
    )
    kwargs: dict = {
        "aws_access_key_id": creds.access_key_id,
        "aws_secret_access_key": creds.secret_access_key,
        "aws_session_token": creds.session_token,
    }
    if region_name is not None:
        kwargs["region_name"] = region_name
    return boto3.Session(**kwargs)


def is_valid_account_id(value: str) -> bool:
    """Return ``True`` if *value* is a 12-digit AWS account ID.

    Args:
        value: String to validate.

    Returns:
        ``True`` if *value* is exactly 12 ASCII digits, ``False`` otherwise.
    """
    return value.isdigit() and len(value) == 12


class AssumeRoleWithSamlResult(BaseModel):
    """Result of assume_role_with_saml."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    assumed_role_user: dict[str, Any] | None = None
    packed_policy_size: int | None = None
    subject: str | None = None
    subject_type: str | None = None
    issuer: str | None = None
    audience: str | None = None
    name_qualifier: str | None = None
    source_identity: str | None = None


class AssumeRoleWithWebIdentityResult(BaseModel):
    """Result of assume_role_with_web_identity."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    subject_from_web_identity_token: str | None = None
    assumed_role_user: dict[str, Any] | None = None
    packed_policy_size: int | None = None
    provider: str | None = None
    audience: str | None = None
    source_identity: str | None = None


class AssumeRootResult(BaseModel):
    """Result of assume_root."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    source_identity: str | None = None


class DecodeAuthorizationMessageResult(BaseModel):
    """Result of decode_authorization_message."""

    model_config = ConfigDict(frozen=True)

    decoded_message: str | None = None


class GetAccessKeyInfoResult(BaseModel):
    """Result of get_access_key_info."""

    model_config = ConfigDict(frozen=True)

    account: str | None = None


class GetDelegatedAccessTokenResult(BaseModel):
    """Result of get_delegated_access_token."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    packed_policy_size: int | None = None
    assumed_principal: str | None = None


class GetFederationTokenResult(BaseModel):
    """Result of get_federation_token."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    federated_user: dict[str, Any] | None = None
    packed_policy_size: int | None = None


class GetSessionTokenResult(BaseModel):
    """Result of get_session_token."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None


def assume_role_with_saml(
    role_arn: str,
    principal_arn: str,
    saml_assertion: str,
    *,
    policy_arns: list[dict[str, Any]] | None = None,
    policy: str | None = None,
    duration_seconds: int | None = None,
    region_name: str | None = None,
) -> AssumeRoleWithSamlResult:
    """Assume role with saml.

    Args:
        role_arn: Role arn.
        principal_arn: Principal arn.
        saml_assertion: Saml assertion.
        policy_arns: Policy arns.
        policy: Policy.
        duration_seconds: Duration seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleArn"] = role_arn
    kwargs["PrincipalArn"] = principal_arn
    kwargs["SAMLAssertion"] = saml_assertion
    if policy_arns is not None:
        kwargs["PolicyArns"] = policy_arns
    if policy is not None:
        kwargs["Policy"] = policy
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    try:
        resp = client.assume_role_with_saml(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to assume role with saml") from exc
    return AssumeRoleWithSamlResult(
        credentials=resp.get("Credentials"),
        assumed_role_user=resp.get("AssumedRoleUser"),
        packed_policy_size=resp.get("PackedPolicySize"),
        subject=resp.get("Subject"),
        subject_type=resp.get("SubjectType"),
        issuer=resp.get("Issuer"),
        audience=resp.get("Audience"),
        name_qualifier=resp.get("NameQualifier"),
        source_identity=resp.get("SourceIdentity"),
    )


def assume_role_with_web_identity(
    role_arn: str,
    role_session_name: str,
    web_identity_token: str,
    *,
    provider_id: str | None = None,
    policy_arns: list[dict[str, Any]] | None = None,
    policy: str | None = None,
    duration_seconds: int | None = None,
    region_name: str | None = None,
) -> AssumeRoleWithWebIdentityResult:
    """Assume role with web identity.

    Args:
        role_arn: Role arn.
        role_session_name: Role session name.
        web_identity_token: Web identity token.
        provider_id: Provider id.
        policy_arns: Policy arns.
        policy: Policy.
        duration_seconds: Duration seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RoleArn"] = role_arn
    kwargs["RoleSessionName"] = role_session_name
    kwargs["WebIdentityToken"] = web_identity_token
    if provider_id is not None:
        kwargs["ProviderId"] = provider_id
    if policy_arns is not None:
        kwargs["PolicyArns"] = policy_arns
    if policy is not None:
        kwargs["Policy"] = policy
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    try:
        resp = client.assume_role_with_web_identity(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to assume role with web identity") from exc
    return AssumeRoleWithWebIdentityResult(
        credentials=resp.get("Credentials"),
        subject_from_web_identity_token=resp.get("SubjectFromWebIdentityToken"),
        assumed_role_user=resp.get("AssumedRoleUser"),
        packed_policy_size=resp.get("PackedPolicySize"),
        provider=resp.get("Provider"),
        audience=resp.get("Audience"),
        source_identity=resp.get("SourceIdentity"),
    )


def assume_root(
    target_principal: str,
    task_policy_arn: dict[str, Any],
    *,
    duration_seconds: int | None = None,
    region_name: str | None = None,
) -> AssumeRootResult:
    """Assume root.

    Args:
        target_principal: Target principal.
        task_policy_arn: Task policy arn.
        duration_seconds: Duration seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetPrincipal"] = target_principal
    kwargs["TaskPolicyArn"] = task_policy_arn
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    try:
        resp = client.assume_root(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to assume root") from exc
    return AssumeRootResult(
        credentials=resp.get("Credentials"),
        source_identity=resp.get("SourceIdentity"),
    )


def decode_authorization_message(
    encoded_message: str,
    region_name: str | None = None,
) -> DecodeAuthorizationMessageResult:
    """Decode authorization message.

    Args:
        encoded_message: Encoded message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EncodedMessage"] = encoded_message
    try:
        resp = client.decode_authorization_message(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to decode authorization message") from exc
    return DecodeAuthorizationMessageResult(
        decoded_message=resp.get("DecodedMessage"),
    )


def get_access_key_info(
    access_key_id: str,
    region_name: str | None = None,
) -> GetAccessKeyInfoResult:
    """Get access key info.

    Args:
        access_key_id: Access key id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccessKeyId"] = access_key_id
    try:
        resp = client.get_access_key_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get access key info") from exc
    return GetAccessKeyInfoResult(
        account=resp.get("Account"),
    )


def get_delegated_access_token(
    trade_in_token: str,
    region_name: str | None = None,
) -> GetDelegatedAccessTokenResult:
    """Get delegated access token.

    Args:
        trade_in_token: Trade in token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TradeInToken"] = trade_in_token
    try:
        resp = client.get_delegated_access_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get delegated access token") from exc
    return GetDelegatedAccessTokenResult(
        credentials=resp.get("Credentials"),
        packed_policy_size=resp.get("PackedPolicySize"),
        assumed_principal=resp.get("AssumedPrincipal"),
    )


def get_federation_token(
    name: str,
    *,
    policy: str | None = None,
    policy_arns: list[dict[str, Any]] | None = None,
    duration_seconds: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> GetFederationTokenResult:
    """Get federation token.

    Args:
        name: Name.
        policy: Policy.
        policy_arns: Policy arns.
        duration_seconds: Duration seconds.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if policy is not None:
        kwargs["Policy"] = policy
    if policy_arns is not None:
        kwargs["PolicyArns"] = policy_arns
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.get_federation_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get federation token") from exc
    return GetFederationTokenResult(
        credentials=resp.get("Credentials"),
        federated_user=resp.get("FederatedUser"),
        packed_policy_size=resp.get("PackedPolicySize"),
    )


def get_session_token(
    *,
    duration_seconds: int | None = None,
    serial_number: str | None = None,
    token_code: str | None = None,
    region_name: str | None = None,
) -> GetSessionTokenResult:
    """Get session token.

    Args:
        duration_seconds: Duration seconds.
        serial_number: Serial number.
        token_code: Token code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("sts", region_name)
    kwargs: dict[str, Any] = {}
    if duration_seconds is not None:
        kwargs["DurationSeconds"] = duration_seconds
    if serial_number is not None:
        kwargs["SerialNumber"] = serial_number
    if token_code is not None:
        kwargs["TokenCode"] = token_code
    try:
        resp = client.get_session_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get session token") from exc
    return GetSessionTokenResult(
        credentials=resp.get("Credentials"),
    )
