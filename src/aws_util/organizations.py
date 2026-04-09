"""aws_util.organizations — AWS Organizations utilities.

Provides high-level helpers for managing AWS Organizations including
organization lifecycle, organizational units (OUs), accounts, policies,
handshakes, tagging, and hierarchy traversal.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AccountResult",
    "CancelHandshakeResult",
    "CreateGovCloudAccountResult",
    "DeclineHandshakeResult",
    "DescribeCreateAccountStatusResult",
    "DescribeEffectivePolicyResult",
    "DescribeHandshakeResult",
    "DescribeResourcePolicyResult",
    "EnableAllFeaturesResult",
    "HandshakeResult",
    "ListAccountsWithInvalidEffectivePolicyResult",
    "ListAwsServiceAccessForOrganizationResult",
    "ListCreateAccountStatusResult",
    "ListDelegatedAdministratorsResult",
    "ListDelegatedServicesForAccountResult",
    "ListEffectivePolicyValidationErrorsResult",
    "ListHandshakesForAccountResult",
    "ListHandshakesForOrganizationResult",
    "ListPoliciesForTargetResult",
    "ListTargetsForPolicyResult",
    "OUResult",
    "OrgResult",
    "PolicyResult",
    "PolicySummaryResult",
    "PutResourcePolicyResult",
    "RootResult",
    "UpdateOrganizationalUnitResult",
    "accept_handshake",
    "attach_policy",
    "cancel_handshake",
    "close_account",
    "create_account",
    "create_gov_cloud_account",
    "create_organization",
    "create_organizational_unit",
    "create_policy",
    "decline_handshake",
    "delete_organization",
    "delete_organizational_unit",
    "delete_policy",
    "delete_resource_policy",
    "deregister_delegated_administrator",
    "describe_account",
    "describe_create_account_status",
    "describe_effective_policy",
    "describe_handshake",
    "describe_organization",
    "describe_organizational_unit",
    "describe_policy",
    "describe_resource_policy",
    "detach_policy",
    "disable_aws_service_access",
    "disable_policy_type",
    "enable_all_features",
    "enable_aws_service_access",
    "enable_policy_type",
    "invite_account_to_organization",
    "leave_organization",
    "list_accounts",
    "list_accounts_for_parent",
    "list_accounts_with_invalid_effective_policy",
    "list_aws_service_access_for_organization",
    "list_children",
    "list_create_account_status",
    "list_delegated_administrators",
    "list_delegated_services_for_account",
    "list_effective_policy_validation_errors",
    "list_handshakes_for_account",
    "list_handshakes_for_organization",
    "list_organizational_units_for_parent",
    "list_parents",
    "list_policies",
    "list_policies_for_target",
    "list_roots",
    "list_tags_for_resource",
    "list_targets_for_policy",
    "move_account",
    "put_resource_policy",
    "register_delegated_administrator",
    "remove_account_from_organization",
    "tag_resource",
    "untag_resource",
    "update_organizational_unit",
    "update_policy",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class OrgResult(BaseModel):
    """Metadata for an AWS Organization."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    master_account_arn: str = ""
    master_account_id: str = ""
    master_account_email: str = ""
    feature_set: str = ""
    available_policy_types: list[dict[str, Any]] = []
    extra: dict[str, Any] = {}


class OUResult(BaseModel):
    """Metadata for an organizational unit."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str = ""
    extra: dict[str, Any] = {}


class AccountResult(BaseModel):
    """Metadata for an AWS account in the organization."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str = ""
    email: str = ""
    status: str = ""
    joined_method: str = ""
    joined_timestamp: Any = None
    extra: dict[str, Any] = {}


class PolicyResult(BaseModel):
    """Full policy including summary and content."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str = ""
    description: str = ""
    type: str = ""
    aws_managed: bool = False
    content: str = ""
    extra: dict[str, Any] = {}


class PolicySummaryResult(BaseModel):
    """Summary metadata for an Organizations policy."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str = ""
    description: str = ""
    type: str = ""
    aws_managed: bool = False
    extra: dict[str, Any] = {}


class HandshakeResult(BaseModel):
    """Metadata for an Organizations handshake."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    state: str = ""
    action: str = ""
    resources: list[dict[str, Any]] = []
    parties: list[dict[str, Any]] = []
    requested_timestamp: Any = None
    expiration_timestamp: Any = None
    extra: dict[str, Any] = {}


class RootResult(BaseModel):
    """Metadata for an Organizations root."""

    model_config = ConfigDict(frozen=True)

    id: str
    arn: str
    name: str = ""
    policy_types: list[dict[str, Any]] = []
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

_ORG_KEYS = {
    "Id",
    "Arn",
    "MasterAccountArn",
    "MasterAccountId",
    "MasterAccountEmail",
    "FeatureSet",
    "AvailablePolicyTypes",
}


def _parse_org(data: dict[str, Any]) -> OrgResult:
    """Parse a raw Organization dict into a model."""
    return OrgResult(
        id=data["Id"],
        arn=data["Arn"],
        master_account_arn=data.get("MasterAccountArn", ""),
        master_account_id=data.get("MasterAccountId", ""),
        master_account_email=data.get("MasterAccountEmail", ""),
        feature_set=data.get("FeatureSet", ""),
        available_policy_types=data.get("AvailablePolicyTypes", []),
        extra={k: v for k, v in data.items() if k not in _ORG_KEYS},
    )


_OU_KEYS = {"Id", "Arn", "Name"}


def _parse_ou(data: dict[str, Any]) -> OUResult:
    """Parse a raw OrganizationalUnit dict into a model."""
    return OUResult(
        id=data["Id"],
        arn=data["Arn"],
        name=data.get("Name", ""),
        extra={k: v for k, v in data.items() if k not in _OU_KEYS},
    )


_ACCOUNT_KEYS = {
    "Id",
    "Arn",
    "Name",
    "Email",
    "Status",
    "JoinedMethod",
    "JoinedTimestamp",
}


def _parse_account(data: dict[str, Any]) -> AccountResult:
    """Parse a raw Account dict into a model."""
    return AccountResult(
        id=data["Id"],
        arn=data["Arn"],
        name=data.get("Name", ""),
        email=data.get("Email", ""),
        status=data.get("Status", ""),
        joined_method=data.get("JoinedMethod", ""),
        joined_timestamp=data.get("JoinedTimestamp"),
        extra={k: v for k, v in data.items() if k not in _ACCOUNT_KEYS},
    )


_POLICY_SUMMARY_KEYS = {
    "Id",
    "Arn",
    "Name",
    "Description",
    "Type",
    "AwsManaged",
}


def _parse_policy_summary(
    data: dict[str, Any],
) -> PolicySummaryResult:
    """Parse a raw PolicySummary dict into a model."""
    return PolicySummaryResult(
        id=data["Id"],
        arn=data["Arn"],
        name=data.get("Name", ""),
        description=data.get("Description", ""),
        type=data.get("Type", ""),
        aws_managed=data.get("AwsManaged", False),
        extra={k: v for k, v in data.items() if k not in _POLICY_SUMMARY_KEYS},
    )


def _parse_policy(data: dict[str, Any]) -> PolicyResult:
    """Parse a raw Policy dict (with PolicySummary + Content)."""
    summary = data.get("PolicySummary", {})
    return PolicyResult(
        id=summary.get("Id", ""),
        arn=summary.get("Arn", ""),
        name=summary.get("Name", ""),
        description=summary.get("Description", ""),
        type=summary.get("Type", ""),
        aws_managed=summary.get("AwsManaged", False),
        content=data.get("Content", ""),
        extra={k: v for k, v in summary.items() if k not in _POLICY_SUMMARY_KEYS},
    )


_HANDSHAKE_KEYS = {
    "Id",
    "Arn",
    "State",
    "Action",
    "Resources",
    "Parties",
    "RequestedTimestamp",
    "ExpirationTimestamp",
}


def _parse_handshake(data: dict[str, Any]) -> HandshakeResult:
    """Parse a raw Handshake dict into a model."""
    return HandshakeResult(
        id=data["Id"],
        arn=data["Arn"],
        state=data.get("State", ""),
        action=data.get("Action", ""),
        resources=data.get("Resources", []),
        parties=data.get("Parties", []),
        requested_timestamp=data.get("RequestedTimestamp"),
        expiration_timestamp=data.get("ExpirationTimestamp"),
        extra={k: v for k, v in data.items() if k not in _HANDSHAKE_KEYS},
    )


_ROOT_KEYS = {"Id", "Arn", "Name", "PolicyTypes"}


def _parse_root(data: dict[str, Any]) -> RootResult:
    """Parse a raw Root dict into a model."""
    return RootResult(
        id=data["Id"],
        arn=data["Arn"],
        name=data.get("Name", ""),
        policy_types=data.get("PolicyTypes", []),
        extra={k: v for k, v in data.items() if k not in _ROOT_KEYS},
    )


# ---------------------------------------------------------------------------
# Organization lifecycle
# ---------------------------------------------------------------------------


def create_organization(
    *,
    feature_set: str = "ALL",
    region_name: str | None = None,
) -> OrgResult:
    """Create an AWS Organization.

    Args:
        feature_set: ``"ALL"`` or ``"CONSOLIDATED_BILLING"``.
        region_name: AWS region override.

    Returns:
        An :class:`OrgResult` for the new organization.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.create_organization(FeatureSet=feature_set)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_organization failed") from exc
    return _parse_org(resp["Organization"])


def describe_organization(
    *,
    region_name: str | None = None,
) -> OrgResult:
    """Describe the current AWS Organization.

    Args:
        region_name: AWS region override.

    Returns:
        An :class:`OrgResult` describing the organization.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.describe_organization()
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_organization failed") from exc
    return _parse_org(resp["Organization"])


# ---------------------------------------------------------------------------
# Organizational Unit operations
# ---------------------------------------------------------------------------


def create_organizational_unit(
    parent_id: str,
    name: str,
    *,
    region_name: str | None = None,
) -> OUResult:
    """Create an organizational unit under a parent.

    Args:
        parent_id: The parent root or OU ID.
        name: Name for the new OU.
        region_name: AWS region override.

    Returns:
        An :class:`OUResult` for the new OU.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.create_organizational_unit(ParentId=parent_id, Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_organizational_unit failed for {name!r}") from exc
    return _parse_ou(resp["OrganizationalUnit"])


def describe_organizational_unit(
    ou_id: str,
    *,
    region_name: str | None = None,
) -> OUResult:
    """Describe an organizational unit.

    Args:
        ou_id: The OU ID.
        region_name: AWS region override.

    Returns:
        An :class:`OUResult` describing the OU.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.describe_organizational_unit(OrganizationalUnitId=ou_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_organizational_unit failed for {ou_id!r}",
        ) from exc
    return _parse_ou(resp["OrganizationalUnit"])


def list_organizational_units_for_parent(
    parent_id: str,
    *,
    region_name: str | None = None,
) -> list[OUResult]:
    """List organizational units under a parent.

    Args:
        parent_id: The parent root or OU ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`OUResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[OUResult] = []
    try:
        paginator = client.get_paginator("list_organizational_units_for_parent")
        for page in paginator.paginate(ParentId=parent_id):
            for ou in page.get("OrganizationalUnits", []):
                results.append(_parse_ou(ou))
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "list_organizational_units_for_parent failed",
        ) from exc
    return results


# ---------------------------------------------------------------------------
# Account operations
# ---------------------------------------------------------------------------


def list_accounts(
    *,
    region_name: str | None = None,
) -> list[AccountResult]:
    """List all accounts in the organization.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`AccountResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[AccountResult] = []
    try:
        paginator = client.get_paginator("list_accounts")
        for page in paginator.paginate():
            for acct in page.get("Accounts", []):
                results.append(_parse_account(acct))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_accounts failed") from exc
    return results


def list_accounts_for_parent(
    parent_id: str,
    *,
    region_name: str | None = None,
) -> list[AccountResult]:
    """List accounts under a specific parent.

    Args:
        parent_id: The parent root or OU ID.
        region_name: AWS region override.

    Returns:
        A list of :class:`AccountResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[AccountResult] = []
    try:
        paginator = client.get_paginator("list_accounts_for_parent")
        for page in paginator.paginate(ParentId=parent_id):
            for acct in page.get("Accounts", []):
                results.append(_parse_account(acct))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_accounts_for_parent failed") from exc
    return results


def describe_account(
    account_id: str,
    *,
    region_name: str | None = None,
) -> AccountResult:
    """Describe a single account.

    Args:
        account_id: The AWS account ID.
        region_name: AWS region override.

    Returns:
        An :class:`AccountResult` describing the account.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.describe_account(AccountId=account_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_account failed for {account_id!r}") from exc
    return _parse_account(resp["Account"])


def create_account(
    email: str,
    account_name: str,
    *,
    iam_user_access_to_billing: str = "ALLOW",
    role_name: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Request creation of a new member account.

    Args:
        email: Email address for the new account.
        account_name: Friendly name for the new account.
        iam_user_access_to_billing: ``"ALLOW"`` or ``"DENY"``.
        role_name: Name of the IAM role for cross-account access.
        region_name: AWS region override.

    Returns:
        The ``CreateAccountStatus`` dict from the API response.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {
        "Email": email,
        "AccountName": account_name,
        "IamUserAccessToBilling": iam_user_access_to_billing,
    }
    if role_name is not None:
        kwargs["RoleName"] = role_name
    try:
        resp = client.create_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_account failed for {account_name!r}",
        ) from exc
    return resp.get("CreateAccountStatus", {})


def invite_account_to_organization(
    target_id: str,
    *,
    notes: str | None = None,
    region_name: str | None = None,
) -> HandshakeResult:
    """Invite an existing AWS account to join the organization.

    Args:
        target_id: Account ID or email to invite.
        notes: Optional notes for the invitation.
        region_name: AWS region override.

    Returns:
        A :class:`HandshakeResult` for the invitation handshake.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {
        "Target": {"Id": target_id, "Type": "ACCOUNT"},
    }
    if notes is not None:
        kwargs["Notes"] = notes
    try:
        resp = client.invite_account_to_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"invite_account_to_organization failed for {target_id!r}",
        ) from exc
    return _parse_handshake(resp["Handshake"])


def accept_handshake(
    handshake_id: str,
    *,
    region_name: str | None = None,
) -> HandshakeResult:
    """Accept a handshake invitation.

    Args:
        handshake_id: The handshake ID to accept.
        region_name: AWS region override.

    Returns:
        A :class:`HandshakeResult` for the accepted handshake.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.accept_handshake(HandshakeId=handshake_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"accept_handshake failed for {handshake_id!r}",
        ) from exc
    return _parse_handshake(resp["Handshake"])


def move_account(
    account_id: str,
    source_parent_id: str,
    destination_parent_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Move an account between OUs or roots.

    Args:
        account_id: The account ID to move.
        source_parent_id: Current parent (root or OU ID).
        destination_parent_id: Destination parent (root or OU ID).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        client.move_account(
            AccountId=account_id,
            SourceParentId=source_parent_id,
            DestinationParentId=destination_parent_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"move_account failed for {account_id!r}",
        ) from exc


def remove_account_from_organization(
    account_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Remove a member account from the organization.

    Args:
        account_id: The account ID to remove.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        client.remove_account_from_organization(AccountId=account_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"remove_account_from_organization failed for {account_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Hierarchy traversal
# ---------------------------------------------------------------------------


def list_roots(
    *,
    region_name: str | None = None,
) -> list[RootResult]:
    """List the roots of the organization.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`RootResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[RootResult] = []
    try:
        paginator = client.get_paginator("list_roots")
        for page in paginator.paginate():
            for root in page.get("Roots", []):
                results.append(_parse_root(root))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_roots failed") from exc
    return results


def list_children(
    parent_id: str,
    child_type: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """List children of a parent (accounts or OUs).

    Args:
        parent_id: The parent root or OU ID.
        child_type: ``"ACCOUNT"`` or ``"ORGANIZATIONAL_UNIT"``.
        region_name: AWS region override.

    Returns:
        A list of child dicts with ``Id`` and ``Type`` keys.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[dict[str, str]] = []
    try:
        paginator = client.get_paginator("list_children")
        for page in paginator.paginate(ParentId=parent_id, ChildType=child_type):
            results.extend(page.get("Children", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_children failed") from exc
    return results


def list_parents(
    child_id: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """List the parents of a child (account or OU).

    Args:
        child_id: The child account or OU ID.
        region_name: AWS region override.

    Returns:
        A list of parent dicts with ``Id`` and ``Type`` keys.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[dict[str, str]] = []
    try:
        paginator = client.get_paginator("list_parents")
        for page in paginator.paginate(ChildId=child_id):
            results.extend(page.get("Parents", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_parents failed") from exc
    return results


# ---------------------------------------------------------------------------
# Policy operations
# ---------------------------------------------------------------------------


def list_policies(
    policy_filter: str = "SERVICE_CONTROL_POLICY",
    *,
    region_name: str | None = None,
) -> list[PolicySummaryResult]:
    """List policies in the organization.

    Args:
        policy_filter: Policy type filter (e.g.
            ``"SERVICE_CONTROL_POLICY"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`PolicySummaryResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[PolicySummaryResult] = []
    try:
        paginator = client.get_paginator("list_policies")
        for page in paginator.paginate(Filter=policy_filter):
            for pol in page.get("Policies", []):
                results.append(_parse_policy_summary(pol))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_policies failed") from exc
    return results


def describe_policy(
    policy_id: str,
    *,
    region_name: str | None = None,
) -> PolicyResult:
    """Describe a policy including its content.

    Args:
        policy_id: The policy ID.
        region_name: AWS region override.

    Returns:
        A :class:`PolicyResult` with the full policy details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.describe_policy(PolicyId=policy_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_policy failed for {policy_id!r}") from exc
    return _parse_policy(resp["Policy"])


def create_policy(
    name: str,
    content: str,
    description: str,
    policy_type: str = "SERVICE_CONTROL_POLICY",
    *,
    region_name: str | None = None,
) -> PolicyResult:
    """Create an Organizations policy.

    Args:
        name: Policy name.
        content: JSON policy document.
        description: Human-readable description.
        policy_type: Policy type (default SCP).
        region_name: AWS region override.

    Returns:
        A :class:`PolicyResult` for the new policy.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.create_policy(
            Name=name,
            Content=content,
            Description=description,
            Type=policy_type,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_policy failed for {name!r}") from exc
    return _parse_policy(resp["Policy"])


def update_policy(
    policy_id: str,
    *,
    name: str | None = None,
    content: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> PolicyResult:
    """Update an existing Organizations policy.

    Args:
        policy_id: The policy ID.
        name: New name (optional).
        content: New policy document (optional).
        description: New description (optional).
        region_name: AWS region override.

    Returns:
        A :class:`PolicyResult` for the updated policy.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {"PolicyId": policy_id}
    if name is not None:
        kwargs["Name"] = name
    if content is not None:
        kwargs["Content"] = content
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.update_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_policy failed for {policy_id!r}") from exc
    return _parse_policy(resp["Policy"])


def delete_policy(
    policy_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an Organizations policy.

    Args:
        policy_id: The policy ID to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        client.delete_policy(PolicyId=policy_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_policy failed for {policy_id!r}") from exc


def attach_policy(
    policy_id: str,
    target_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Attach a policy to a target (root, OU, or account).

    Args:
        policy_id: The policy ID.
        target_id: The target root, OU, or account ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        client.attach_policy(PolicyId=policy_id, TargetId=target_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"attach_policy failed for {policy_id!r} -> {target_id!r}",
        ) from exc


def detach_policy(
    policy_id: str,
    target_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Detach a policy from a target.

    Args:
        policy_id: The policy ID.
        target_id: The target root, OU, or account ID.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        client.detach_policy(PolicyId=policy_id, TargetId=target_id)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"detach_policy failed for {policy_id!r} from {target_id!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Policy type management
# ---------------------------------------------------------------------------


def enable_policy_type(
    root_id: str,
    policy_type: str = "SERVICE_CONTROL_POLICY",
    *,
    region_name: str | None = None,
) -> RootResult:
    """Enable a policy type on a root.

    Args:
        root_id: The root ID.
        policy_type: Policy type to enable.
        region_name: AWS region override.

    Returns:
        A :class:`RootResult` with the updated root info.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.enable_policy_type(RootId=root_id, PolicyType=policy_type)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"enable_policy_type failed for {root_id!r}") from exc
    return _parse_root(resp["Root"])


def disable_policy_type(
    root_id: str,
    policy_type: str = "SERVICE_CONTROL_POLICY",
    *,
    region_name: str | None = None,
) -> RootResult:
    """Disable a policy type on a root.

    Args:
        root_id: The root ID.
        policy_type: Policy type to disable.
        region_name: AWS region override.

    Returns:
        A :class:`RootResult` with the updated root info.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        resp = client.disable_policy_type(RootId=root_id, PolicyType=policy_type)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"disable_policy_type failed for {root_id!r}") from exc
    return _parse_root(resp["Root"])


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


def list_tags_for_resource(
    resource_id: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """List tags for an Organizations resource.

    Args:
        resource_id: The resource ID (account, OU, root, or policy).
        region_name: AWS region override.

    Returns:
        A list of ``{"Key": ..., "Value": ...}`` tag dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    results: list[dict[str, str]] = []
    try:
        paginator = client.get_paginator("list_tags_for_resource")
        for page in paginator.paginate(ResourceId=resource_id):
            results.extend(page.get("Tags", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_tags_for_resource failed") from exc
    return results


def tag_resource(
    resource_id: str,
    tags: list[dict[str, str]],
    *,
    region_name: str | None = None,
) -> None:
    """Tag an Organizations resource.

    Args:
        resource_id: The resource ID.
        tags: List of ``{"Key": ..., "Value": ...}`` tag dicts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    try:
        client.tag_resource(ResourceId=resource_id, Tags=tags)
    except ClientError as exc:
        raise wrap_aws_error(exc, "tag_resource failed") from exc


class CancelHandshakeResult(BaseModel):
    """Result of cancel_handshake."""

    model_config = ConfigDict(frozen=True)

    handshake: dict[str, Any] | None = None


class CreateGovCloudAccountResult(BaseModel):
    """Result of create_gov_cloud_account."""

    model_config = ConfigDict(frozen=True)

    create_account_status: dict[str, Any] | None = None


class DeclineHandshakeResult(BaseModel):
    """Result of decline_handshake."""

    model_config = ConfigDict(frozen=True)

    handshake: dict[str, Any] | None = None


class DescribeCreateAccountStatusResult(BaseModel):
    """Result of describe_create_account_status."""

    model_config = ConfigDict(frozen=True)

    create_account_status: dict[str, Any] | None = None


class DescribeEffectivePolicyResult(BaseModel):
    """Result of describe_effective_policy."""

    model_config = ConfigDict(frozen=True)

    effective_policy: dict[str, Any] | None = None


class DescribeHandshakeResult(BaseModel):
    """Result of describe_handshake."""

    model_config = ConfigDict(frozen=True)

    handshake: dict[str, Any] | None = None


class DescribeResourcePolicyResult(BaseModel):
    """Result of describe_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_policy: dict[str, Any] | None = None


class EnableAllFeaturesResult(BaseModel):
    """Result of enable_all_features."""

    model_config = ConfigDict(frozen=True)

    handshake: dict[str, Any] | None = None


class ListAccountsWithInvalidEffectivePolicyResult(BaseModel):
    """Result of list_accounts_with_invalid_effective_policy."""

    model_config = ConfigDict(frozen=True)

    accounts: list[dict[str, Any]] | None = None
    policy_type: str | None = None
    next_token: str | None = None


class ListAwsServiceAccessForOrganizationResult(BaseModel):
    """Result of list_aws_service_access_for_organization."""

    model_config = ConfigDict(frozen=True)

    enabled_service_principals: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListCreateAccountStatusResult(BaseModel):
    """Result of list_create_account_status."""

    model_config = ConfigDict(frozen=True)

    create_account_statuses: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDelegatedAdministratorsResult(BaseModel):
    """Result of list_delegated_administrators."""

    model_config = ConfigDict(frozen=True)

    delegated_administrators: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDelegatedServicesForAccountResult(BaseModel):
    """Result of list_delegated_services_for_account."""

    model_config = ConfigDict(frozen=True)

    delegated_services: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEffectivePolicyValidationErrorsResult(BaseModel):
    """Result of list_effective_policy_validation_errors."""

    model_config = ConfigDict(frozen=True)

    account_id: str | None = None
    policy_type: str | None = None
    path: str | None = None
    evaluation_timestamp: str | None = None
    next_token: str | None = None
    effective_policy_validation_errors: list[dict[str, Any]] | None = None


class ListHandshakesForAccountResult(BaseModel):
    """Result of list_handshakes_for_account."""

    model_config = ConfigDict(frozen=True)

    handshakes: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListHandshakesForOrganizationResult(BaseModel):
    """Result of list_handshakes_for_organization."""

    model_config = ConfigDict(frozen=True)

    handshakes: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPoliciesForTargetResult(BaseModel):
    """Result of list_policies_for_target."""

    model_config = ConfigDict(frozen=True)

    policies: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTargetsForPolicyResult(BaseModel):
    """Result of list_targets_for_policy."""

    model_config = ConfigDict(frozen=True)

    targets: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_policy: dict[str, Any] | None = None


class UpdateOrganizationalUnitResult(BaseModel):
    """Result of update_organizational_unit."""

    model_config = ConfigDict(frozen=True)

    organizational_unit: dict[str, Any] | None = None


def cancel_handshake(
    handshake_id: str,
    region_name: str | None = None,
) -> CancelHandshakeResult:
    """Cancel handshake.

    Args:
        handshake_id: Handshake id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HandshakeId"] = handshake_id
    try:
        resp = client.cancel_handshake(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel handshake") from exc
    return CancelHandshakeResult(
        handshake=resp.get("Handshake"),
    )


def close_account(
    account_id: str,
    region_name: str | None = None,
) -> None:
    """Close account.

    Args:
        account_id: Account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    try:
        client.close_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to close account") from exc
    return None


def create_gov_cloud_account(
    email: str,
    account_name: str,
    *,
    role_name: str | None = None,
    iam_user_access_to_billing: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateGovCloudAccountResult:
    """Create gov cloud account.

    Args:
        email: Email.
        account_name: Account name.
        role_name: Role name.
        iam_user_access_to_billing: Iam user access to billing.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Email"] = email
    kwargs["AccountName"] = account_name
    if role_name is not None:
        kwargs["RoleName"] = role_name
    if iam_user_access_to_billing is not None:
        kwargs["IamUserAccessToBilling"] = iam_user_access_to_billing
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_gov_cloud_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create gov cloud account") from exc
    return CreateGovCloudAccountResult(
        create_account_status=resp.get("CreateAccountStatus"),
    )


def decline_handshake(
    handshake_id: str,
    region_name: str | None = None,
) -> DeclineHandshakeResult:
    """Decline handshake.

    Args:
        handshake_id: Handshake id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HandshakeId"] = handshake_id
    try:
        resp = client.decline_handshake(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to decline handshake") from exc
    return DeclineHandshakeResult(
        handshake=resp.get("Handshake"),
    )


def delete_organization(
    region_name: str | None = None,
) -> None:
    """Delete organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.delete_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete organization") from exc
    return None


def delete_organizational_unit(
    organizational_unit_id: str,
    region_name: str | None = None,
) -> None:
    """Delete organizational unit.

    Args:
        organizational_unit_id: Organizational unit id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationalUnitId"] = organizational_unit_id
    try:
        client.delete_organizational_unit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete organizational unit") from exc
    return None


def delete_resource_policy(
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


def deregister_delegated_administrator(
    account_id: str,
    service_principal: str,
    region_name: str | None = None,
) -> None:
    """Deregister delegated administrator.

    Args:
        account_id: Account id.
        service_principal: Service principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["ServicePrincipal"] = service_principal
    try:
        client.deregister_delegated_administrator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister delegated administrator") from exc
    return None


def describe_create_account_status(
    create_account_request_id: str,
    region_name: str | None = None,
) -> DescribeCreateAccountStatusResult:
    """Describe create account status.

    Args:
        create_account_request_id: Create account request id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CreateAccountRequestId"] = create_account_request_id
    try:
        resp = client.describe_create_account_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe create account status") from exc
    return DescribeCreateAccountStatusResult(
        create_account_status=resp.get("CreateAccountStatus"),
    )


def describe_effective_policy(
    policy_type: str,
    *,
    target_id: str | None = None,
    region_name: str | None = None,
) -> DescribeEffectivePolicyResult:
    """Describe effective policy.

    Args:
        policy_type: Policy type.
        target_id: Target id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyType"] = policy_type
    if target_id is not None:
        kwargs["TargetId"] = target_id
    try:
        resp = client.describe_effective_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe effective policy") from exc
    return DescribeEffectivePolicyResult(
        effective_policy=resp.get("EffectivePolicy"),
    )


def describe_handshake(
    handshake_id: str,
    region_name: str | None = None,
) -> DescribeHandshakeResult:
    """Describe handshake.

    Args:
        handshake_id: Handshake id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HandshakeId"] = handshake_id
    try:
        resp = client.describe_handshake(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe handshake") from exc
    return DescribeHandshakeResult(
        handshake=resp.get("Handshake"),
    )


def describe_resource_policy(
    region_name: str | None = None,
) -> DescribeResourcePolicyResult:
    """Describe resource policy.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe resource policy") from exc
    return DescribeResourcePolicyResult(
        resource_policy=resp.get("ResourcePolicy"),
    )


def disable_aws_service_access(
    service_principal: str,
    region_name: str | None = None,
) -> None:
    """Disable aws service access.

    Args:
        service_principal: Service principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServicePrincipal"] = service_principal
    try:
        client.disable_aws_service_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable aws service access") from exc
    return None


def enable_all_features(
    region_name: str | None = None,
) -> EnableAllFeaturesResult:
    """Enable all features.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.enable_all_features(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable all features") from exc
    return EnableAllFeaturesResult(
        handshake=resp.get("Handshake"),
    )


def enable_aws_service_access(
    service_principal: str,
    region_name: str | None = None,
) -> None:
    """Enable aws service access.

    Args:
        service_principal: Service principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServicePrincipal"] = service_principal
    try:
        client.enable_aws_service_access(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable aws service access") from exc
    return None


def leave_organization(
    region_name: str | None = None,
) -> None:
    """Leave organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.leave_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to leave organization") from exc
    return None


def list_accounts_with_invalid_effective_policy(
    policy_type: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAccountsWithInvalidEffectivePolicyResult:
    """List accounts with invalid effective policy.

    Args:
        policy_type: Policy type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyType"] = policy_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_accounts_with_invalid_effective_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list accounts with invalid effective policy") from exc
    return ListAccountsWithInvalidEffectivePolicyResult(
        accounts=resp.get("Accounts"),
        policy_type=resp.get("PolicyType"),
        next_token=resp.get("NextToken"),
    )


def list_aws_service_access_for_organization(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAwsServiceAccessForOrganizationResult:
    """List aws service access for organization.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_aws_service_access_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list aws service access for organization") from exc
    return ListAwsServiceAccessForOrganizationResult(
        enabled_service_principals=resp.get("EnabledServicePrincipals"),
        next_token=resp.get("NextToken"),
    )


def list_create_account_status(
    *,
    states: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCreateAccountStatusResult:
    """List create account status.

    Args:
        states: States.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    if states is not None:
        kwargs["States"] = states
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_create_account_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list create account status") from exc
    return ListCreateAccountStatusResult(
        create_account_statuses=resp.get("CreateAccountStatuses"),
        next_token=resp.get("NextToken"),
    )


def list_delegated_administrators(
    *,
    service_principal: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDelegatedAdministratorsResult:
    """List delegated administrators.

    Args:
        service_principal: Service principal.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    if service_principal is not None:
        kwargs["ServicePrincipal"] = service_principal
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_delegated_administrators(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list delegated administrators") from exc
    return ListDelegatedAdministratorsResult(
        delegated_administrators=resp.get("DelegatedAdministrators"),
        next_token=resp.get("NextToken"),
    )


def list_delegated_services_for_account(
    account_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDelegatedServicesForAccountResult:
    """List delegated services for account.

    Args:
        account_id: Account id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_delegated_services_for_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list delegated services for account") from exc
    return ListDelegatedServicesForAccountResult(
        delegated_services=resp.get("DelegatedServices"),
        next_token=resp.get("NextToken"),
    )


def list_effective_policy_validation_errors(
    account_id: str,
    policy_type: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEffectivePolicyValidationErrorsResult:
    """List effective policy validation errors.

    Args:
        account_id: Account id.
        policy_type: Policy type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["PolicyType"] = policy_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_effective_policy_validation_errors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list effective policy validation errors") from exc
    return ListEffectivePolicyValidationErrorsResult(
        account_id=resp.get("AccountId"),
        policy_type=resp.get("PolicyType"),
        path=resp.get("Path"),
        evaluation_timestamp=resp.get("EvaluationTimestamp"),
        next_token=resp.get("NextToken"),
        effective_policy_validation_errors=resp.get("EffectivePolicyValidationErrors"),
    )


def list_handshakes_for_account(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListHandshakesForAccountResult:
    """List handshakes for account.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_handshakes_for_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list handshakes for account") from exc
    return ListHandshakesForAccountResult(
        handshakes=resp.get("Handshakes"),
        next_token=resp.get("NextToken"),
    )


def list_handshakes_for_organization(
    *,
    filter: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListHandshakesForOrganizationResult:
    """List handshakes for organization.

    Args:
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_handshakes_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list handshakes for organization") from exc
    return ListHandshakesForOrganizationResult(
        handshakes=resp.get("Handshakes"),
        next_token=resp.get("NextToken"),
    )


def list_policies_for_target(
    target_id: str,
    filter: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPoliciesForTargetResult:
    """List policies for target.

    Args:
        target_id: Target id.
        filter: Filter.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetId"] = target_id
    kwargs["Filter"] = filter
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_policies_for_target(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list policies for target") from exc
    return ListPoliciesForTargetResult(
        policies=resp.get("Policies"),
        next_token=resp.get("NextToken"),
    )


def list_targets_for_policy(
    policy_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTargetsForPolicyResult:
    """List targets for policy.

    Args:
        policy_id: Policy id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PolicyId"] = policy_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_targets_for_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list targets for policy") from exc
    return ListTargetsForPolicyResult(
        targets=resp.get("Targets"),
        next_token=resp.get("NextToken"),
    )


def put_resource_policy(
    content: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        content: Content.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Content"] = content
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_policy=resp.get("ResourcePolicy"),
    )


def register_delegated_administrator(
    account_id: str,
    service_principal: str,
    region_name: str | None = None,
) -> None:
    """Register delegated administrator.

    Args:
        account_id: Account id.
        service_principal: Service principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    kwargs["ServicePrincipal"] = service_principal
    try:
        client.register_delegated_administrator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register delegated administrator") from exc
    return None


def untag_resource(
    resource_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_id: Resource id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_organizational_unit(
    organizational_unit_id: str,
    *,
    name: str | None = None,
    region_name: str | None = None,
) -> UpdateOrganizationalUnitResult:
    """Update organizational unit.

    Args:
        organizational_unit_id: Organizational unit id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("organizations", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationalUnitId"] = organizational_unit_id
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = client.update_organizational_unit(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update organizational unit") from exc
    return UpdateOrganizationalUnitResult(
        organizational_unit=resp.get("OrganizationalUnit"),
    )
