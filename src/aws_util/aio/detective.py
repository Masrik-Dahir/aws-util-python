"""Native async Amazon Detective utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.detective import (
    BatchGetGraphMemberDatasourcesResult,
    BatchGetMembershipDatasourcesResult,
    DescribeOrganizationConfigurationResult,
    GraphResult,
    IndicatorResult,
    InvestigationResult,
    InvitationResult,
    ListDatasourcePackagesResult,
    ListOrganizationAdminAccountsResult,
    ListTagsForResourceResult,
    MemberResult,
    _parse_graph,
    _parse_indicator,
    _parse_investigation,
    _parse_invitation,
    _parse_member,
)
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
# Graph management
# ---------------------------------------------------------------------------


async def create_graph(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateGraph", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_graph failed") from exc
    return resp.get("GraphArn", "")


async def delete_graph(
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
    client = async_client("detective", region_name)
    try:
        await client.call("DeleteGraph", GraphArn=graph_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_graph failed for {graph_arn!r}") from exc


async def list_graphs(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[GraphResult] = []
    try:
        while True:
            resp = await client.call("ListGraphs", **kwargs)
            for g in resp.get("GraphList", []):
                results.append(_parse_graph(g))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_graphs failed") from exc
    return results


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------


async def create_members(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {
        "GraphArn": graph_arn,
        "Accounts": accounts,
        "DisableEmailNotification": disable_email_notification,
    }
    if message:
        kwargs["Message"] = message
    try:
        resp = await client.call("CreateMembers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_members failed") from exc
    return {
        "Members": [_parse_member(m) for m in resp.get("Members", [])],
        "UnprocessedAccounts": resp.get("UnprocessedAccounts", []),
    }


async def list_members(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {"GraphArn": graph_arn}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[MemberResult] = []
    try:
        while True:
            resp = await client.call("ListMembers", **kwargs)
            for m in resp.get("MemberDetails", []):
                results.append(_parse_member(m))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_members failed") from exc
    return results


async def get_members(
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
    client = async_client("detective", region_name)
    try:
        resp = await client.call(
            "GetMembers",
            GraphArn=graph_arn,
            AccountIds=account_ids,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "get_members failed") from exc
    return [_parse_member(m) for m in resp.get("MemberDetails", [])]


async def delete_members(
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
    client = async_client("detective", region_name)
    try:
        resp = await client.call(
            "DeleteMembers",
            GraphArn=graph_arn,
            AccountIds=account_ids,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


# ---------------------------------------------------------------------------
# Invitations
# ---------------------------------------------------------------------------


async def accept_invitation(
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
    client = async_client("detective", region_name)
    try:
        await client.call("AcceptInvitation", GraphArn=graph_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"accept_invitation failed for {graph_arn!r}") from exc


async def reject_invitation(
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
    client = async_client("detective", region_name)
    try:
        await client.call("RejectInvitation", GraphArn=graph_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"reject_invitation failed for {graph_arn!r}") from exc


async def list_invitations(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[InvitationResult] = []
    try:
        while True:
            resp = await client.call("ListInvitations", **kwargs)
            for inv in resp.get("Invitations", []):
                results.append(_parse_invitation(inv))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_invitations failed") from exc
    return results


# ---------------------------------------------------------------------------
# Investigations
# ---------------------------------------------------------------------------


async def start_investigation(
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
    client = async_client("detective", region_name)
    try:
        resp = await client.call(
            "StartInvestigation",
            GraphArn=graph_arn,
            EntityArn=entity_arn,
            ScopeStartTime=scope_start_time,
            ScopeEndTime=scope_end_time,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "start_investigation failed") from exc
    return resp.get("InvestigationId", "")


async def get_investigation(
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
    client = async_client("detective", region_name)
    try:
        resp = await client.call(
            "GetInvestigation",
            GraphArn=graph_arn,
            InvestigationId=investigation_id,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_investigation failed for {investigation_id!r}",
        ) from exc
    return _parse_investigation(resp)


async def list_investigations(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {"GraphArn": graph_arn}
    if filter_criteria:
        kwargs["FilterCriteria"] = filter_criteria
    if sort_criteria:
        kwargs["SortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[InvestigationResult] = []
    try:
        while True:
            resp = await client.call("ListInvestigations", **kwargs)
            for inv in resp.get("InvestigationDetails", []):
                results.append(_parse_investigation(inv))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_investigations failed") from exc
    return results


async def list_indicators(
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
    client = async_client("detective", region_name)
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
        while True:
            resp = await client.call("ListIndicators", **kwargs)
            for ind in resp.get("Indicators", []):
                results.append(_parse_indicator(ind))
            token = resp.get("NextToken")
            if not token:
                break
            kwargs["NextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_indicators failed") from exc
    return results


async def batch_get_graph_member_datasources(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["AccountIds"] = account_ids
    try:
        resp = await client.call("BatchGetGraphMemberDatasources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get graph member datasources") from exc
    return BatchGetGraphMemberDatasourcesResult(
        member_datasources=resp.get("MemberDatasources"),
        unprocessed_accounts=resp.get("UnprocessedAccounts"),
    )


async def batch_get_membership_datasources(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArns"] = graph_arns
    try:
        resp = await client.call("BatchGetMembershipDatasources", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get membership datasources") from exc
    return BatchGetMembershipDatasourcesResult(
        membership_datasources=resp.get("MembershipDatasources"),
        unprocessed_graphs=resp.get("UnprocessedGraphs"),
    )


async def describe_organization_configuration(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    try:
        resp = await client.call("DescribeOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe organization configuration") from exc
    return DescribeOrganizationConfigurationResult(
        auto_enable=resp.get("AutoEnable"),
    )


async def disable_organization_admin_account(
    region_name: str | None = None,
) -> None:
    """Disable organization admin account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisableOrganizationAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable organization admin account") from exc
    return None


async def disassociate_membership(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    try:
        await client.call("DisassociateMembership", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate membership") from exc
    return None


async def enable_organization_admin_account(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountId"] = account_id
    try:
        await client.call("EnableOrganizationAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable organization admin account") from exc
    return None


async def list_datasource_packages(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListDatasourcePackages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list datasource packages") from exc
    return ListDatasourcePackagesResult(
        datasource_packages=resp.get("DatasourcePackages"),
        next_token=resp.get("NextToken"),
    )


async def list_organization_admin_accounts(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListOrganizationAdminAccounts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list organization admin accounts") from exc
    return ListOrganizationAdminAccountsResult(
        administrators=resp.get("Administrators"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def start_monitoring_member(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["AccountId"] = account_id
    try:
        await client.call("StartMonitoringMember", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start monitoring member") from exc
    return None


async def tag_resource(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_datasource_packages(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["DatasourcePackages"] = datasource_packages
    try:
        await client.call("UpdateDatasourcePackages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update datasource packages") from exc
    return None


async def update_investigation_state(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    kwargs["InvestigationId"] = investigation_id
    kwargs["State"] = state
    try:
        await client.call("UpdateInvestigationState", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update investigation state") from exc
    return None


async def update_organization_configuration(
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
    client = async_client("detective", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GraphArn"] = graph_arn
    if auto_enable is not None:
        kwargs["AutoEnable"] = auto_enable
    try:
        await client.call("UpdateOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update organization configuration") from exc
    return None
