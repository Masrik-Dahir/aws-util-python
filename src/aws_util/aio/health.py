"""Native async AWS Health utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.health import (
    AffectedAccountResult,
    AffectedEntityResult,
    DescribeAffectedEntitiesForOrganizationResult,
    DescribeEntityAggregatesForOrganizationResult,
    DescribeEntityAggregatesResult,
    DescribeHealthServiceStatusForOrganizationResult,
    EventAggregateResult,
    EventDetailResult,
    EventResult,
    EventTypeResult,
    OrgEventDetailResult,
    OrgEventResult,
    _parse_entity,
    _parse_event,
    _parse_event_aggregate,
    _parse_event_type,
    _parse_org_event,
)

__all__ = [
    "AffectedAccountResult",
    "AffectedEntityResult",
    "DescribeAffectedEntitiesForOrganizationResult",
    "DescribeEntityAggregatesForOrganizationResult",
    "DescribeEntityAggregatesResult",
    "DescribeHealthServiceStatusForOrganizationResult",
    "EventAggregateResult",
    "EventDetailResult",
    "EventResult",
    "EventTypeResult",
    "OrgEventDetailResult",
    "OrgEventResult",
    "describe_affected_accounts_for_organization",
    "describe_affected_entities",
    "describe_affected_entities_for_organization",
    "describe_entity_aggregates",
    "describe_entity_aggregates_for_organization",
    "describe_event_aggregates",
    "describe_event_details",
    "describe_event_details_for_organization",
    "describe_event_types",
    "describe_events",
    "describe_events_for_organization",
    "describe_health_service_status_for_organization",
    "disable_health_service_access_for_organization",
    "enable_health_service_access_for_organization",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


async def describe_events(
    *,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> list[EventResult]:
    """Describe AWS Health events.

    Args:
        filter: Optional filter criteria dict.
        region_name: AWS region override.

    Returns:
        A list of :class:`EventResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = await client.call("DescribeEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_events failed") from exc
    return [_parse_event(e) for e in resp.get("events", [])]


async def describe_event_details(
    event_arns: list[str],
    *,
    region_name: str | None = None,
) -> list[EventDetailResult]:
    """Describe details for specific Health events.

    Args:
        event_arns: List of event ARNs.
        region_name: AWS region override.

    Returns:
        A list of :class:`EventDetailResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    try:
        resp = await client.call("DescribeEventDetails", eventArns=event_arns)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_event_details failed") from exc
    results: list[EventDetailResult] = []
    for item in resp.get("successfulSet", []):
        ev = _parse_event(item["event"])
        desc = item.get("eventDescription", {}).get("latestDescription")
        results.append(
            EventDetailResult(
                event=ev,
                event_description=desc,
                extra={k: v for k, v in item.items() if k not in {"event", "eventDescription"}},
            )
        )
    return results


async def describe_affected_entities(
    *,
    filter: dict[str, Any],
    region_name: str | None = None,
) -> list[AffectedEntityResult]:
    """Describe entities affected by Health events.

    Args:
        filter: Filter criteria dict (must include eventArns).
        region_name: AWS region override.

    Returns:
        A list of :class:`AffectedEntityResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    try:
        resp = await client.call("DescribeAffectedEntities", filter=filter)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_affected_entities failed") from exc
    return [_parse_entity(e) for e in resp.get("entities", [])]


async def describe_event_types(
    *,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> list[EventTypeResult]:
    """Describe available AWS Health event types.

    Args:
        filter: Optional filter criteria dict.
        region_name: AWS region override.

    Returns:
        A list of :class:`EventTypeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = await client.call("DescribeEventTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_event_types failed") from exc
    return [_parse_event_type(t) for t in resp.get("eventTypes", [])]


async def describe_event_aggregates(
    aggregate_field: str,
    *,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> list[EventAggregateResult]:
    """Describe aggregated counts of Health events.

    Args:
        aggregate_field: The field to aggregate by.
        filter: Optional filter criteria dict.
        region_name: AWS region override.

    Returns:
        A list of :class:`EventAggregateResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {"aggregateField": aggregate_field}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = await client.call("DescribeEventAggregates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_event_aggregates failed") from exc
    return [_parse_event_aggregate(a) for a in resp.get("eventAggregates", [])]


async def describe_affected_accounts_for_organization(
    event_arn: str,
    *,
    region_name: str | None = None,
) -> list[AffectedAccountResult]:
    """Describe accounts affected by an organization Health event.

    Args:
        event_arn: The event ARN.
        region_name: AWS region override.

    Returns:
        A list of :class:`AffectedAccountResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    try:
        resp = await client.call(
            "DescribeAffectedAccountsForOrganization",
            eventArn=event_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "describe_affected_accounts_for_organization failed",
        ) from exc
    return [AffectedAccountResult(account_id=acct) for acct in resp.get("affectedAccounts", [])]


async def describe_events_for_organization(
    *,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> list[OrgEventResult]:
    """Describe Health events for an AWS organization.

    Args:
        filter: Optional filter criteria dict.
        region_name: AWS region override.

    Returns:
        A list of :class:`OrgEventResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = await client.call("DescribeEventsForOrganization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_events_for_organization failed") from exc
    return [_parse_org_event(e) for e in resp.get("events", [])]


async def describe_event_details_for_organization(
    organization_event_detail_filters: list[dict[str, Any]],
    *,
    region_name: str | None = None,
) -> list[OrgEventDetailResult]:
    """Describe event details for organization-level Health events.

    Args:
        organization_event_detail_filters: List of filter dicts, each
            containing ``eventArn`` and optionally ``awsAccountId``.
        region_name: AWS region override.

    Returns:
        A list of :class:`OrgEventDetailResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    try:
        resp = await client.call(
            "DescribeEventDetailsForOrganization",
            organizationEventDetailFilters=(organization_event_detail_filters),
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            "describe_event_details_for_organization failed",
        ) from exc
    results: list[OrgEventDetailResult] = []
    for item in resp.get("successfulSet", []):
        ev = _parse_org_event(item["event"])
        desc = item.get("eventDescription", {}).get("latestDescription")
        results.append(
            OrgEventDetailResult(
                event=ev,
                event_description=desc,
                aws_account_id=item.get("awsAccountId"),
                extra={
                    k: v
                    for k, v in item.items()
                    if k not in {"event", "eventDescription", "awsAccountId"}
                },
            )
        )
    return results


async def describe_affected_entities_for_organization(
    *,
    organization_entity_filters: list[dict[str, Any]] | None = None,
    locale: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    organization_entity_account_filters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> DescribeAffectedEntitiesForOrganizationResult:
    """Describe affected entities for organization.

    Args:
        organization_entity_filters: Organization entity filters.
        locale: Locale.
        next_token: Next token.
        max_results: Max results.
        organization_entity_account_filters: Organization entity account filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if organization_entity_filters is not None:
        kwargs["organizationEntityFilters"] = organization_entity_filters
    if locale is not None:
        kwargs["locale"] = locale
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if organization_entity_account_filters is not None:
        kwargs["organizationEntityAccountFilters"] = organization_entity_account_filters
    try:
        resp = await client.call("DescribeAffectedEntitiesForOrganization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe affected entities for organization") from exc
    return DescribeAffectedEntitiesForOrganizationResult(
        entities=resp.get("entities"),
        failed_set=resp.get("failedSet"),
        next_token=resp.get("nextToken"),
    )


async def describe_entity_aggregates(
    *,
    event_arns: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeEntityAggregatesResult:
    """Describe entity aggregates.

    Args:
        event_arns: Event arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if event_arns is not None:
        kwargs["eventArns"] = event_arns
    try:
        resp = await client.call("DescribeEntityAggregates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe entity aggregates") from exc
    return DescribeEntityAggregatesResult(
        entity_aggregates=resp.get("entityAggregates"),
    )


async def describe_entity_aggregates_for_organization(
    event_arns: list[str],
    *,
    aws_account_ids: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeEntityAggregatesForOrganizationResult:
    """Describe entity aggregates for organization.

    Args:
        event_arns: Event arns.
        aws_account_ids: Aws account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["eventArns"] = event_arns
    if aws_account_ids is not None:
        kwargs["awsAccountIds"] = aws_account_ids
    try:
        resp = await client.call("DescribeEntityAggregatesForOrganization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe entity aggregates for organization") from exc
    return DescribeEntityAggregatesForOrganizationResult(
        organization_entity_aggregates=resp.get("organizationEntityAggregates"),
    )


async def describe_health_service_status_for_organization(
    region_name: str | None = None,
) -> DescribeHealthServiceStatusForOrganizationResult:
    """Describe health service status for organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeHealthServiceStatusForOrganization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to describe health service status for organization"
        ) from exc
    return DescribeHealthServiceStatusForOrganizationResult(
        health_service_access_status_for_organization=resp.get(
            "healthServiceAccessStatusForOrganization"
        ),
    )


async def disable_health_service_access_for_organization(
    region_name: str | None = None,
) -> None:
    """Disable health service access for organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisableHealthServiceAccessForOrganization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to disable health service access for organization"
        ) from exc
    return None


async def enable_health_service_access_for_organization(
    region_name: str | None = None,
) -> None:
    """Enable health service access for organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("health", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("EnableHealthServiceAccessForOrganization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, "Failed to enable health service access for organization"
        ) from exc
    return None
