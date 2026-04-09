"""aws_util.detective --- Amazon Detective utilities.

Provides functions for managing Amazon Detective: creating/deleting graphs,
managing member accounts, handling invitations, and running investigations.
Uses the ``detective`` boto3 service name.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchGetGraphMemberDatasourcesResult",
    "BatchGetMembershipDatasourcesResult",
    "DescribeOrganizationConfigurationResult",
    "GraphResult",
    "IndicatorResult",
    "InvestigationResult",
    "InvitationResult",
    "ListDatasourcePackagesResult",
    "ListOrganizationAdminAccountsResult",
    "ListTagsForResourceResult",
    "MemberResult",
    "accept_invitation",
    "batch_get_graph_member_datasources",
    "batch_get_membership_datasources",
    "create_graph",
    "create_members",
    "delete_graph",
    "delete_members",
    "describe_organization_configuration",
    "disable_organization_admin_account",
    "disassociate_membership",
    "enable_organization_admin_account",
    "get_investigation",
    "get_members",
    "list_datasource_packages",
    "list_graphs",
    "list_indicators",
    "list_investigations",
    "list_invitations",
    "list_members",
    "list_organization_admin_accounts",
    "list_tags_for_resource",
    "reject_invitation",
    "start_investigation",
    "start_monitoring_member",
    "tag_resource",
    "untag_resource",
    "update_datasource_packages",
    "update_investigation_state",
    "update_organization_configuration",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class GraphResult(BaseModel):
    """An Amazon Detective behavior graph."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    graph_arn: str = ""
    created_at: str | None = None
    extra: dict[str, Any] = {}


class MemberResult(BaseModel):
    """An Amazon Detective member account."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    account_id: str = ""
    email_address: str = ""
    status: str = ""
    invited_time: str | None = None
    updated_time: str | None = None
    graph_arn: str = ""
    extra: dict[str, Any] = {}


class InvitationResult(BaseModel):
    """An Amazon Detective invitation."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    graph_arn: str = ""
    account_id: str = ""
    email_address: str = ""
    status: str = ""
    extra: dict[str, Any] = {}


class InvestigationResult(BaseModel):
    """An Amazon Detective investigation."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    investigation_id: str = ""
    graph_arn: str = ""
    entity_arn: str = ""
    entity_type: str = ""
    status: str = ""
    severity: str = ""
    created_time: str | None = None
    extra: dict[str, Any] = {}


class IndicatorResult(BaseModel):
    """An Amazon Detective investigation indicator."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    indicator_type: str = ""
    indicator_detail: dict[str, Any] = {}
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Graph management
# ---------------------------------------------------------------------------


def create_graph(
    *,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Create a Detective behavior graph.

    Args:
        tags: Optional tags for the graph.
        region_name: AWS region override.

    Returns:
        The graph ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = client.create_graph(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_graph failed") from exc
    return resp.get("GraphArn", "")


def delete_graph(
    graph_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Detective behavior graph.

    Args:
        graph_arn: ARN of the graph to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        client.delete_graph(GraphArn=graph_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_graph failed for {graph_arn!r}") from exc


def list_graphs(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[GraphResult]:
    """List Detective behavior graphs.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`GraphResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[GraphResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_graphs(**kwargs)
            for g in resp.get("GraphList", []):
                results.append(_parse_graph(g))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_graphs failed") from exc
    return results


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------


def create_members(
    graph_arn: str,
    accounts: list[dict[str, str]],
    *,
    message: str | None = None,
    disable_email_notification: bool = False,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Create member associations in a Detective graph.

    Args:
        graph_arn: ARN of the behavior graph.
        accounts: List of dicts with ``AccountId`` and ``EmailAddress``.
        message: Optional invitation message.
        disable_email_notification: Whether to skip email notification.
        region_name: AWS region override.

    Returns:
        A dict with ``Members`` and ``UnprocessedAccounts``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {
        "GraphArn": graph_arn,
        "Accounts": accounts,
        "DisableEmailNotification": disable_email_notification,
    }
    if message:
        kwargs["Message"] = message
    try:
        resp = client.create_members(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_members failed") from exc
    return {
        "Members": [_parse_member(m) for m in resp.get("Members", [])],
        "UnprocessedAccounts": resp.get("UnprocessedAccounts", []),
    }


def list_members(
    graph_arn: str,
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[MemberResult]:
    """List members of a Detective behavior graph.

    Args:
        graph_arn: ARN of the behavior graph.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`MemberResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {"GraphArn": graph_arn}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[MemberResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_members(**kwargs)
            for m in resp.get("MemberDetails", []):
                results.append(_parse_member(m))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_members failed") from exc
    return results


def get_members(
    graph_arn: str,
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[MemberResult]:
    """Get details for specific members of a Detective graph.

    Args:
        graph_arn: ARN of the behavior graph.
        account_ids: List of AWS account IDs.
        region_name: AWS region override.

    Returns:
        A list of :class:`MemberResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        resp = client.get_members(
            GraphArn=graph_arn,
            AccountIds=account_ids,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_members failed") from exc
    return [_parse_member(m) for m in resp.get("MemberDetails", [])]


def delete_members(
    graph_arn: str,
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Delete members from a Detective behavior graph.

    Args:
        graph_arn: ARN of the behavior graph.
        account_ids: List of AWS account IDs to remove.
        region_name: AWS region override.

    Returns:
        A list of unprocessed account dicts (empty on full success).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        resp = client.delete_members(
            GraphArn=graph_arn,
            AccountIds=account_ids,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------


def accept_invitation(
    graph_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Accept a Detective graph invitation.

    Args:
        graph_arn: ARN of the behavior graph.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        client.accept_invitation(GraphArn=graph_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"accept_invitation failed for {graph_arn!r}") from exc


def reject_invitation(
    graph_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Reject a Detective graph invitation.

    Args:
        graph_arn: ARN of the behavior graph.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        client.reject_invitation(GraphArn=graph_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"reject_invitation failed for {graph_arn!r}") from exc


def list_invitations(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[InvitationResult]:
    """List Detective invitations for the current account.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`InvitationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[InvitationResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_invitations(**kwargs)
            for inv in resp.get("Invitations", []):
                results.append(_parse_invitation(inv))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_invitations failed") from exc
    return results


# ---------------------------------------------------------------------------
# Investigations
# ---------------------------------------------------------------------------


def start_investigation(
    graph_arn: str,
    entity_arn: str,
    scope_start_time: str,
    scope_end_time: str,
    *,
    region_name: str | None = None,
) -> str:
    """Start a Detective investigation.

    Args:
        graph_arn: ARN of the behavior graph.
        entity_arn: ARN of the entity to investigate.
        scope_start_time: ISO-8601 start time.
        scope_end_time: ISO-8601 end time.
        region_name: AWS region override.

    Returns:
        The investigation ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        resp = client.start_investigation(
            GraphArn=graph_arn,
            EntityArn=entity_arn,
            ScopeStartTime=scope_start_time,
            ScopeEndTime=scope_end_time,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_investigation failed") from exc
    return resp.get("InvestigationId", "")


def get_investigation(
    graph_arn: str,
    investigation_id: str,
    *,
    region_name: str | None = None,
) -> InvestigationResult:
    """Get details of a Detective investigation.

    Args:
        graph_arn: ARN of the behavior graph.
        investigation_id: The investigation identifier.
        region_name: AWS region override.

    Returns:
        An :class:`InvestigationResult` with investigation details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    try:
        resp = client.get_investigation(
            GraphArn=graph_arn,
            InvestigationId=investigation_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_investigation failed for {investigation_id!r}",
        ) from exc
    return _parse_investigation(resp)


def list_investigations(
    graph_arn: str,
    *,
    filter_criteria: dict[str, Any] | None = None,
    sort_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[InvestigationResult]:
    """List Detective investigations.

    Args:
        graph_arn: ARN of the behavior graph.
        filter_criteria: Filter criteria dict.
        sort_criteria: Sort criteria dict.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`InvestigationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {"GraphArn": graph_arn}
    if filter_criteria:
        kwargs["FilterCriteria"] = filter_criteria
    if sort_criteria:
        kwargs["SortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[InvestigationResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_investigations(**kwargs)
            for inv in resp.get("InvestigationDetails", []):
                results.append(_parse_investigation(inv))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_investigations failed") from exc
    return results


def list_indicators(
    graph_arn: str,
    investigation_id: str,
    *,
    indicator_type: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[IndicatorResult]:
    """List indicators for a Detective investigation.

    Args:
        graph_arn: ARN of the behavior graph.
        investigation_id: The investigation identifier.
        indicator_type: Optional indicator type filter.
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`IndicatorResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {
        "GraphArn": graph_arn,
        "InvestigationId": investigation_id,
    }
    if indicator_type:
        kwargs["IndicatorType"] = indicator_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[IndicatorResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = client.list_indicators(**kwargs)
            for ind in resp.get("Indicators", []):
                results.append(_parse_indicator(ind))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_indicators failed") from exc
    return results


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_graph(g: dict[str, Any]) -> GraphResult:
    """Parse a raw graph dict into a :class:`GraphResult`."""
    return GraphResult(
        graph_arn=g.get("Arn", ""),
        created_at=(str(g["CreatedTime"]) if "CreatedTime" in g else None),
        extra={k: v for k, v in g.items() if k not in {"Arn", "CreatedTime"}},
    )


def _parse_member(m: dict[str, Any]) -> MemberResult:
    """Parse a raw member dict into a :class:`MemberResult`."""
    return MemberResult(
        account_id=m.get("AccountId", ""),
        email_address=m.get("EmailAddress", ""),
        status=m.get("Status", ""),
        invited_time=(str(m["InvitedTime"]) if "InvitedTime" in m else None),
        updated_time=(str(m["UpdatedTime"]) if "UpdatedTime" in m else None),
        graph_arn=m.get("GraphArn", ""),
        extra={
            k: v
            for k, v in m.items()
            if k
            not in {
                "AccountId",
                "EmailAddress",
                "Status",
                "InvitedTime",
                "UpdatedTime",
                "GraphArn",
            }
        },
    )


def _parse_invitation(inv: dict[str, Any]) -> InvitationResult:
    """Parse a raw invitation dict into an :class:`InvitationResult`."""
    return InvitationResult(
        graph_arn=inv.get("GraphArn", ""),
        account_id=inv.get("AccountId", ""),
        email_address=inv.get("EmailAddress", ""),
        status=inv.get("Status", ""),
        extra={
            k: v
            for k, v in inv.items()
            if k
            not in {
                "GraphArn",
                "AccountId",
                "EmailAddress",
                "Status",
            }
        },
    )


def _parse_investigation(
    inv: dict[str, Any],
) -> InvestigationResult:
    """Parse a raw investigation dict."""
    return InvestigationResult(
        investigation_id=inv.get("InvestigationId", ""),
        graph_arn=inv.get("GraphArn", ""),
        entity_arn=inv.get("EntityArn", ""),
        entity_type=inv.get("EntityType", ""),
        status=inv.get("Status", ""),
        severity=inv.get("Severity", ""),
        created_time=(str(inv["CreatedTime"]) if "CreatedTime" in inv else None),
        extra={
            k: v
            for k, v in inv.items()
            if k
            not in {
                "InvestigationId",
                "GraphArn",
                "EntityArn",
                "EntityType",
                "Status",
                "Severity",
                "CreatedTime",
            }
        },
    )


def _parse_indicator(ind: dict[str, Any]) -> IndicatorResult:
    """Parse a raw indicator dict."""
    return IndicatorResult(
        indicator_type=ind.get("IndicatorType", ""),
        indicator_detail=ind.get("IndicatorDetail", {}),
        extra={k: v for k, v in ind.items() if k not in {"IndicatorType", "IndicatorDetail"}},
    )


class BatchGetGraphMemberDatasourcesResult(BaseModel):
    """Result of batch_get_graph_member_datasources."""

    model_config = ConfigDict(frozen=True)

    member_datasources: list[dict[str, Any]] | None = None
    unprocessed_accounts: list[dict[str, Any]] | None = None


class BatchGetMembershipDatasourcesResult(BaseModel):
    """Result of batch_get_membership_datasources."""

    model_config = ConfigDict(frozen=True)

    membership_datasources: list[dict[str, Any]] | None = None
    unprocessed_graphs: list[dict[str, Any]] | None = None


class DescribeOrganizationConfigurationResult(BaseModel):
    """Result of describe_organization_configuration."""

    model_config = ConfigDict(frozen=True)

    auto_enable: bool | None = None


class ListDatasourcePackagesResult(BaseModel):
    """Result of list_datasource_packages."""

    model_config = ConfigDict(frozen=True)

    datasource_packages: dict[str, Any] | None = None
    next_token: str | None = None


class ListOrganizationAdminAccountsResult(BaseModel):
    """Result of list_organization_admin_accounts."""

    model_config = ConfigDict(frozen=True)

    administrators: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


def batch_get_graph_member_datasources(
    graph_arn: str,
    account_ids: list[str],
    region_name: str | None = None,
) -> BatchGetGraphMemberDatasourcesResult:
    """Batch get graph member datasources.

    Args:
        graph_arn: Graph arn.
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["AccountIds"] = account_ids
    try:
        resp = client.batch_get_graph_member_datasources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get graph member datasources") from exc
    return BatchGetGraphMemberDatasourcesResult(
        member_datasources=resp.get("MemberDatasources"),
        unprocessed_accounts=resp.get("UnprocessedAccounts"),
    )


def batch_get_membership_datasources(
    graph_arns: list[str],
    region_name: str | None = None,
) -> BatchGetMembershipDatasourcesResult:
    """Batch get membership datasources.

    Args:
        graph_arns: Graph arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArns"] = graph_arns
    try:
        resp = client.batch_get_membership_datasources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get membership datasources") from exc
    return BatchGetMembershipDatasourcesResult(
        membership_datasources=resp.get("MembershipDatasources"),
        unprocessed_graphs=resp.get("UnprocessedGraphs"),
    )


def describe_organization_configuration(
    graph_arn: str,
    region_name: str | None = None,
) -> DescribeOrganizationConfigurationResult:
    """Describe organization configuration.

    Args:
        graph_arn: Graph arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    try:
        resp = client.describe_organization_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe organization configuration") from exc
    return DescribeOrganizationConfigurationResult(
        auto_enable=resp.get("AutoEnable"),
    )


def disable_organization_admin_account(
    region_name: str | None = None,
) -> None:
    """Disable organization admin account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.disable_organization_admin_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable organization admin account") from exc
    return None


def disassociate_membership(
    graph_arn: str,
    region_name: str | None = None,
) -> None:
    """Disassociate membership.

    Args:
        graph_arn: Graph arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    try:
        client.disassociate_membership(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate membership") from exc
    return None


def enable_organization_admin_account(
    account_id: str,
    region_name: str | None = None,
) -> None:
    """Enable organization admin account.

    Args:
        account_id: Account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    try:
        client.enable_organization_admin_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable organization admin account") from exc
    return None


def list_datasource_packages(
    graph_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDatasourcePackagesResult:
    """List datasource packages.

    Args:
        graph_arn: Graph arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_datasource_packages(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list datasource packages") from exc
    return ListDatasourcePackagesResult(
        datasource_packages=resp.get("DatasourcePackages"),
        next_token=resp.get("NextToken"),
    )


def list_organization_admin_accounts(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListOrganizationAdminAccountsResult:
    """List organization admin accounts.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_organization_admin_accounts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list organization admin accounts") from exc
    return ListOrganizationAdminAccountsResult(
        administrators=resp.get("Administrators"),
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
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def start_monitoring_member(
    graph_arn: str,
    account_id: str,
    region_name: str | None = None,
) -> None:
    """Start monitoring member.

    Args:
        graph_arn: Graph arn.
        account_id: Account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["AccountId"] = account_id
    try:
        client.start_monitoring_member(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start monitoring member") from exc
    return None


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
    client = get_client("detective", region_name)
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
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_datasource_packages(
    graph_arn: str,
    datasource_packages: list[str],
    region_name: str | None = None,
) -> None:
    """Update datasource packages.

    Args:
        graph_arn: Graph arn.
        datasource_packages: Datasource packages.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["DatasourcePackages"] = datasource_packages
    try:
        client.update_datasource_packages(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update datasource packages") from exc
    return None


def update_investigation_state(
    graph_arn: str,
    investigation_id: str,
    state: str,
    region_name: str | None = None,
) -> None:
    """Update investigation state.

    Args:
        graph_arn: Graph arn.
        investigation_id: Investigation id.
        state: State.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["InvestigationId"] = investigation_id
    kwargs["State"] = state
    try:
        client.update_investigation_state(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update investigation state") from exc
    return None


def update_organization_configuration(
    graph_arn: str,
    *,
    auto_enable: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update organization configuration.

    Args:
        graph_arn: Graph arn.
        auto_enable: Auto enable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    if auto_enable is not None:
        kwargs["AutoEnable"] = auto_enable
    try:
        client.update_organization_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update organization configuration") from exc
    return None
