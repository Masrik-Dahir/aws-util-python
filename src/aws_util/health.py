"""aws_util.health — AWS Health (Personal Health Dashboard) utilities.

Provides helpers for querying AWS Health events, affected entities,
event types, aggregates, and organization-level event information.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

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
# Models
# ---------------------------------------------------------------------------


class EventResult(BaseModel):
    """Metadata for an AWS Health event."""

    model_config = ConfigDict(frozen=True)

    arn: str
    service: str | None = None
    event_type_code: str | None = None
    event_type_category: str | None = None
    region: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    last_updated_time: str | None = None
    status_code: str | None = None
    extra: dict[str, Any] = {}


class EventDetailResult(BaseModel):
    """Detailed information for a Health event."""

    model_config = ConfigDict(frozen=True)

    event: EventResult
    event_description: str | None = None
    extra: dict[str, Any] = {}


class AffectedEntityResult(BaseModel):
    """An entity affected by an AWS Health event."""

    model_config = ConfigDict(frozen=True)

    entity_value: str
    event_arn: str
    aws_account_id: str | None = None
    entity_url: str | None = None
    status_code: str | None = None
    last_updated_time: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class EventTypeResult(BaseModel):
    """Metadata for an AWS Health event type."""

    model_config = ConfigDict(frozen=True)

    service: str | None = None
    code: str | None = None
    category: str | None = None
    extra: dict[str, Any] = {}


class EventAggregateResult(BaseModel):
    """Aggregate count for a Health event grouping."""

    model_config = ConfigDict(frozen=True)

    aggregate_value: str | None = None
    count: int = 0
    extra: dict[str, Any] = {}


class AffectedAccountResult(BaseModel):
    """An AWS account affected by an organization event."""

    model_config = ConfigDict(frozen=True)

    account_id: str
    extra: dict[str, Any] = {}


class OrgEventResult(BaseModel):
    """An AWS Health event at the organization level."""

    model_config = ConfigDict(frozen=True)

    arn: str
    service: str | None = None
    event_type_code: str | None = None
    event_type_category: str | None = None
    region: str | None = None
    start_time: str | None = None
    end_time: str | None = None
    last_updated_time: str | None = None
    status_code: str | None = None
    extra: dict[str, Any] = {}


class OrgEventDetailResult(BaseModel):
    """Detailed information for an organization-level Health event."""

    model_config = ConfigDict(frozen=True)

    event: OrgEventResult
    event_description: str | None = None
    aws_account_id: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


def _parse_event(raw: dict[str, Any]) -> EventResult:
    """Parse a raw Health event dict into an :class:`EventResult`."""
    _keys = {
        "arn",
        "service",
        "eventTypeCode",
        "eventTypeCategory",
        "region",
        "startTime",
        "endTime",
        "lastUpdatedTime",
        "statusCode",
    }
    return EventResult(
        arn=raw["arn"],
        service=raw.get("service"),
        event_type_code=raw.get("eventTypeCode"),
        event_type_category=raw.get("eventTypeCategory"),
        region=raw.get("region"),
        start_time=str(raw["startTime"]) if raw.get("startTime") else None,
        end_time=str(raw["endTime"]) if raw.get("endTime") else None,
        last_updated_time=(str(raw["lastUpdatedTime"]) if raw.get("lastUpdatedTime") else None),
        status_code=raw.get("statusCode"),
        extra={k: v for k, v in raw.items() if k not in _keys},
    )


def _parse_entity(raw: dict[str, Any]) -> AffectedEntityResult:
    """Parse a raw affected entity dict."""
    _keys = {
        "entityValue",
        "eventArn",
        "awsAccountId",
        "entityUrl",
        "statusCode",
        "lastUpdatedTime",
        "tags",
    }
    return AffectedEntityResult(
        entity_value=raw["entityValue"],
        event_arn=raw["eventArn"],
        aws_account_id=raw.get("awsAccountId"),
        entity_url=raw.get("entityUrl"),
        status_code=raw.get("statusCode"),
        last_updated_time=(str(raw["lastUpdatedTime"]) if raw.get("lastUpdatedTime") else None),
        tags=raw.get("tags", {}),
        extra={k: v for k, v in raw.items() if k not in _keys},
    )


def _parse_event_type(raw: dict[str, Any]) -> EventTypeResult:
    """Parse a raw event type dict."""
    _keys = {"service", "code", "category"}
    return EventTypeResult(
        service=raw.get("service"),
        code=raw.get("code"),
        category=raw.get("category"),
        extra={k: v for k, v in raw.items() if k not in _keys},
    )


def _parse_event_aggregate(raw: dict[str, Any]) -> EventAggregateResult:
    """Parse a raw event aggregate dict."""
    _keys = {"aggregateValue", "count"}
    return EventAggregateResult(
        aggregate_value=raw.get("aggregateValue"),
        count=raw.get("count", 0),
        extra={k: v for k, v in raw.items() if k not in _keys},
    )


def _parse_org_event(raw: dict[str, Any]) -> OrgEventResult:
    """Parse a raw organization event dict."""
    _keys = {
        "arn",
        "service",
        "eventTypeCode",
        "eventTypeCategory",
        "region",
        "startTime",
        "endTime",
        "lastUpdatedTime",
        "statusCode",
    }
    return OrgEventResult(
        arn=raw["arn"],
        service=raw.get("service"),
        event_type_code=raw.get("eventTypeCode"),
        event_type_category=raw.get("eventTypeCategory"),
        region=raw.get("region"),
        start_time=str(raw["startTime"]) if raw.get("startTime") else None,
        end_time=str(raw["endTime"]) if raw.get("endTime") else None,
        last_updated_time=(str(raw["lastUpdatedTime"]) if raw.get("lastUpdatedTime") else None),
        status_code=raw.get("statusCode"),
        extra={k: v for k, v in raw.items() if k not in _keys},
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def describe_events(
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
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.describe_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_events failed") from exc
    return [_parse_event(e) for e in resp.get("events", [])]


def describe_event_details(
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
    client = get_client("health", region_name)
    try:
        resp = client.describe_event_details(eventArns=event_arns)
    except ClientError as exc:
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


def describe_affected_entities(
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
    client = get_client("health", region_name)
    try:
        resp = client.describe_affected_entities(filter=filter)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_affected_entities failed") from exc
    return [_parse_entity(e) for e in resp.get("entities", [])]


def describe_event_types(
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
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.describe_event_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_event_types failed") from exc
    return [_parse_event_type(t) for t in resp.get("eventTypes", [])]


def describe_event_aggregates(
    aggregate_field: str,
    *,
    filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> list[EventAggregateResult]:
    """Describe aggregated counts of Health events.

    Args:
        aggregate_field: The field to aggregate by (e.g. ``"eventTypeCategory"``).
        filter: Optional filter criteria dict.
        region_name: AWS region override.

    Returns:
        A list of :class:`EventAggregateResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {"aggregateField": aggregate_field}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.describe_event_aggregates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_event_aggregates failed") from exc
    return [_parse_event_aggregate(a) for a in resp.get("eventAggregates", [])]


def describe_affected_accounts_for_organization(
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
    client = get_client("health", region_name)
    try:
        resp = client.describe_affected_accounts_for_organization(
            eventArn=event_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            "describe_affected_accounts_for_organization failed",
        ) from exc
    return [AffectedAccountResult(account_id=acct) for acct in resp.get("affectedAccounts", [])]


def describe_events_for_organization(
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
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if filter is not None:
        kwargs["filter"] = filter
    try:
        resp = client.describe_events_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_events_for_organization failed") from exc
    return [_parse_org_event(e) for e in resp.get("events", [])]


def describe_event_details_for_organization(
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
    client = get_client("health", region_name)
    try:
        resp = client.describe_event_details_for_organization(
            organizationEventDetailFilters=organization_event_detail_filters,
        )
    except ClientError as exc:
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


class DescribeAffectedEntitiesForOrganizationResult(BaseModel):
    """Result of describe_affected_entities_for_organization."""

    model_config = ConfigDict(frozen=True)

    entities: list[dict[str, Any]] | None = None
    failed_set: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeEntityAggregatesResult(BaseModel):
    """Result of describe_entity_aggregates."""

    model_config = ConfigDict(frozen=True)

    entity_aggregates: list[dict[str, Any]] | None = None


class DescribeEntityAggregatesForOrganizationResult(BaseModel):
    """Result of describe_entity_aggregates_for_organization."""

    model_config = ConfigDict(frozen=True)

    organization_entity_aggregates: list[dict[str, Any]] | None = None


class DescribeHealthServiceStatusForOrganizationResult(BaseModel):
    """Result of describe_health_service_status_for_organization."""

    model_config = ConfigDict(frozen=True)

    health_service_access_status_for_organization: str | None = None


def describe_affected_entities_for_organization(
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
    client = get_client("health", region_name)
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
        resp = client.describe_affected_entities_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe affected entities for organization") from exc
    return DescribeAffectedEntitiesForOrganizationResult(
        entities=resp.get("entities"),
        failed_set=resp.get("failedSet"),
        next_token=resp.get("nextToken"),
    )


def describe_entity_aggregates(
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
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}
    if event_arns is not None:
        kwargs["eventArns"] = event_arns
    try:
        resp = client.describe_entity_aggregates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe entity aggregates") from exc
    return DescribeEntityAggregatesResult(
        entity_aggregates=resp.get("entityAggregates"),
    )


def describe_entity_aggregates_for_organization(
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
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["eventArns"] = event_arns
    if aws_account_ids is not None:
        kwargs["awsAccountIds"] = aws_account_ids
    try:
        resp = client.describe_entity_aggregates_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe entity aggregates for organization") from exc
    return DescribeEntityAggregatesForOrganizationResult(
        organization_entity_aggregates=resp.get("organizationEntityAggregates"),
    )


def describe_health_service_status_for_organization(
    region_name: str | None = None,
) -> DescribeHealthServiceStatusForOrganizationResult:
    """Describe health service status for organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_health_service_status_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to describe health service status for organization"
        ) from exc
    return DescribeHealthServiceStatusForOrganizationResult(
        health_service_access_status_for_organization=resp.get(
            "healthServiceAccessStatusForOrganization"
        ),
    )


def disable_health_service_access_for_organization(
    region_name: str | None = None,
) -> None:
    """Disable health service access for organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.disable_health_service_access_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to disable health service access for organization"
        ) from exc
    return None


def enable_health_service_access_for_organization(
    region_name: str | None = None,
) -> None:
    """Enable health service access for organization.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("health", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.enable_health_service_access_for_organization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to enable health service access for organization"
        ) from exc
    return None
