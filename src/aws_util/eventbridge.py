from __future__ import annotations

import json
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error

__all__ = [
    "CancelReplayResult",
    "CreateApiDestinationResult",
    "CreateArchiveResult",
    "CreateConnectionResult",
    "CreateEndpointResult",
    "CreateEventBusResult",
    "CreatePartnerEventSourceResult",
    "DeauthorizeConnectionResult",
    "DeleteConnectionResult",
    "DescribeApiDestinationResult",
    "DescribeArchiveResult",
    "DescribeConnectionResult",
    "DescribeEndpointResult",
    "DescribeEventBusResult",
    "DescribeEventSourceResult",
    "DescribePartnerEventSourceResult",
    "DescribeReplayResult",
    "DescribeRuleResult",
    "EventEntry",
    "ListApiDestinationsResult",
    "ListArchivesResult",
    "ListConnectionsResult",
    "ListEndpointsResult",
    "ListEventBusesResult",
    "ListEventSourcesResult",
    "ListPartnerEventSourceAccountsResult",
    "ListPartnerEventSourcesResult",
    "ListReplaysResult",
    "ListRuleNamesByTargetResult",
    "ListTagsForResourceResult",
    "ListTargetsByRuleResult",
    "PutEventsResult",
    "PutPartnerEventsResult",
    "PutRuleResult",
    "PutTargetsResult",
    "RemoveTargetsResult",
    "RunEventPatternResult",
    "StartReplayResult",
    "UpdateApiDestinationResult",
    "UpdateArchiveResult",
    "UpdateConnectionResult",
    "UpdateEndpointResult",
    "UpdateEventBusResult",
    "activate_event_source",
    "cancel_replay",
    "create_api_destination",
    "create_archive",
    "create_connection",
    "create_endpoint",
    "create_event_bus",
    "create_partner_event_source",
    "deactivate_event_source",
    "deauthorize_connection",
    "delete_api_destination",
    "delete_archive",
    "delete_connection",
    "delete_endpoint",
    "delete_event_bus",
    "delete_partner_event_source",
    "delete_rule",
    "describe_api_destination",
    "describe_archive",
    "describe_connection",
    "describe_endpoint",
    "describe_event_bus",
    "describe_event_source",
    "describe_partner_event_source",
    "describe_replay",
    "describe_rule",
    "disable_rule",
    "enable_rule",
    "list_api_destinations",
    "list_archives",
    "list_connections",
    "list_endpoints",
    "list_event_buses",
    "list_event_sources",
    "list_partner_event_source_accounts",
    "list_partner_event_sources",
    "list_replays",
    "list_rule_names_by_target",
    "list_rules",
    "list_tags_for_resource",
    "list_targets_by_rule",
    "put_event",
    "put_events",
    "put_events_chunked",
    "put_partner_events",
    "put_permission",
    "put_rule",
    "put_targets",
    "remove_permission",
    "remove_targets",
    "run_event_pattern",
    "start_replay",
    "tag_resource",
    "untag_resource",
    "update_api_destination",
    "update_archive",
    "update_connection",
    "update_endpoint",
    "update_event_bus",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class EventEntry(BaseModel):
    """A single event to publish to Amazon EventBridge."""

    model_config = ConfigDict(frozen=True)

    source: str
    """Identifies the service or application that generated the event,
    e.g. ``"com.myapp.orders"``."""

    detail_type: str
    """A human-readable phrase describing the event, e.g.
    ``"Order Placed"``."""

    detail: dict[str, Any]
    """Free-form JSON object containing event data."""

    event_bus_name: str = "default"
    """Target event bus.  Defaults to the account's default bus."""

    resources: list[str] = Field(default_factory=list)
    """Optional list of ARNs identifying resources involved in the event."""


class PutEventsResult(BaseModel):
    """Result of a ``PutEvents`` call."""

    model_config = ConfigDict(frozen=True)

    failed_count: int
    successful_count: int
    entries: list[dict[str, Any]]


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def put_event(
    source: str,
    detail_type: str,
    detail: dict[str, Any],
    event_bus_name: str = "default",
    resources: list[str] | None = None,
    region_name: str | None = None,
) -> PutEventsResult:
    """Publish a single event to Amazon EventBridge.

    Args:
        source: Event source identifier, e.g. ``"com.myapp.orders"``.
        detail_type: Short description of the event type.
        detail: Event payload as a dict (JSON-serialisable).
        event_bus_name: Target event bus name or ARN.  Defaults to
            ``"default"``.
        resources: Optional list of resource ARNs associated with the event.
        region_name: AWS region override.

    Returns:
        A :class:`PutEventsResult` describing success/failure counts.

    Raises:
        RuntimeError: If the API call fails or the event is rejected.
    """
    entry = EventEntry(
        source=source,
        detail_type=detail_type,
        detail=detail,
        event_bus_name=event_bus_name,
        resources=resources or [],
    )
    return put_events([entry], region_name=region_name)


def put_events(
    events: list[EventEntry],
    region_name: str | None = None,
) -> PutEventsResult:
    """Publish up to 10 events to EventBridge in a single API call.

    On **partial** failures (some events succeed, some fail), a
    :class:`PutEventsResult` is returned containing both success and failure
    details.  Only when **all** events fail is an :class:`AwsServiceError`
    raised.

    Args:
        events: List of :class:`EventEntry` objects (up to 10 per call).
        region_name: AWS region override.

    Returns:
        A :class:`PutEventsResult` describing success/failure counts and
        any failed entries.

    Raises:
        AwsServiceError: If **all** events fail to publish.
        RuntimeError: If the underlying API call itself fails.
        ValueError: If more than 10 events are supplied.
    """
    if len(events) > 10:
        raise ValueError("put_events supports at most 10 events per call")

    client = get_client("events", region_name)
    entries = [
        {
            "Source": e.source,
            "DetailType": e.detail_type,
            "Detail": json.dumps(e.detail),
            "EventBusName": e.event_bus_name,
            "Resources": e.resources,
        }
        for e in events
    ]
    try:
        resp = client.put_events(Entries=entries)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put events to EventBridge") from exc

    failed = resp.get("FailedEntryCount", 0)
    failed_entries = [e for e in resp.get("Entries", []) if e.get("ErrorCode")]
    successful = len(events) - failed

    result = PutEventsResult(
        failed_count=failed,
        successful_count=successful,
        entries=resp.get("Entries", []),
    )

    if failed and successful == 0:
        raise AwsServiceError(f"All {failed} event(s) failed to publish: {failed_entries}")

    return result


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def put_events_chunked(
    events: list[EventEntry],
    region_name: str | None = None,
) -> list[PutEventsResult]:
    """Publish any number of events to EventBridge, chunking into batches of 10.

    EventBridge's ``PutEvents`` API accepts a maximum of 10 events per call.
    This helper splits *events* into chunks and calls :func:`put_events` for
    each, accumulating results.

    Args:
        events: Arbitrarily long list of :class:`EventEntry` objects.
        region_name: AWS region override.

    Returns:
        A list of :class:`PutEventsResult` — one per batch of 10.

    Raises:
        RuntimeError: If any batch fails.
    """
    results: list[PutEventsResult] = []
    for i in range(0, len(events), 10):
        batch = events[i : i + 10]
        results.append(put_events(batch, region_name=region_name))
    return results


def list_rules(
    event_bus_name: str = "default",
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List EventBridge rules on a given event bus.

    Args:
        event_bus_name: Event bus name or ARN (default ``"default"``).
        region_name: AWS region override.

    Returns:
        A list of rule detail dicts (``Name``, ``Arn``, ``State``,
        ``ScheduleExpression``, ``EventPattern``, etc.).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    rules: list[dict[str, Any]] = []
    kwargs: dict[str, Any] = {"EventBusName": event_bus_name}
    try:
        paginator = client.get_paginator("list_rules")
        for page in paginator.paginate(**kwargs):
            rules.extend(page.get("Rules", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_rules failed") from exc
    return rules


class CancelReplayResult(BaseModel):
    """Result of cancel_replay."""

    model_config = ConfigDict(frozen=True)

    replay_arn: str | None = None
    state: str | None = None
    state_reason: str | None = None


class CreateApiDestinationResult(BaseModel):
    """Result of create_api_destination."""

    model_config = ConfigDict(frozen=True)

    api_destination_arn: str | None = None
    api_destination_state: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None


class CreateArchiveResult(BaseModel):
    """Result of create_archive."""

    model_config = ConfigDict(frozen=True)

    archive_arn: str | None = None
    state: str | None = None
    state_reason: str | None = None
    creation_time: str | None = None


class CreateConnectionResult(BaseModel):
    """Result of create_connection."""

    model_config = ConfigDict(frozen=True)

    connection_arn: str | None = None
    connection_state: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None


class CreateEndpointResult(BaseModel):
    """Result of create_endpoint."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    arn: str | None = None
    routing_config: dict[str, Any] | None = None
    replication_config: dict[str, Any] | None = None
    event_buses: list[dict[str, Any]] | None = None
    role_arn: str | None = None
    state: str | None = None


class CreateEventBusResult(BaseModel):
    """Result of create_event_bus."""

    model_config = ConfigDict(frozen=True)

    event_bus_arn: str | None = None
    description: str | None = None
    kms_key_identifier: str | None = None
    dead_letter_config: dict[str, Any] | None = None
    log_config: dict[str, Any] | None = None


class CreatePartnerEventSourceResult(BaseModel):
    """Result of create_partner_event_source."""

    model_config = ConfigDict(frozen=True)

    event_source_arn: str | None = None


class DeauthorizeConnectionResult(BaseModel):
    """Result of deauthorize_connection."""

    model_config = ConfigDict(frozen=True)

    connection_arn: str | None = None
    connection_state: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    last_authorized_time: str | None = None


class DeleteConnectionResult(BaseModel):
    """Result of delete_connection."""

    model_config = ConfigDict(frozen=True)

    connection_arn: str | None = None
    connection_state: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    last_authorized_time: str | None = None


class DescribeApiDestinationResult(BaseModel):
    """Result of describe_api_destination."""

    model_config = ConfigDict(frozen=True)

    api_destination_arn: str | None = None
    name: str | None = None
    description: str | None = None
    api_destination_state: str | None = None
    connection_arn: str | None = None
    invocation_endpoint: str | None = None
    http_method: str | None = None
    invocation_rate_limit_per_second: int | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None


class DescribeArchiveResult(BaseModel):
    """Result of describe_archive."""

    model_config = ConfigDict(frozen=True)

    archive_arn: str | None = None
    archive_name: str | None = None
    event_source_arn: str | None = None
    description: str | None = None
    event_pattern: str | None = None
    state: str | None = None
    state_reason: str | None = None
    kms_key_identifier: str | None = None
    retention_days: int | None = None
    size_bytes: int | None = None
    event_count: int | None = None
    creation_time: str | None = None


class DescribeConnectionResult(BaseModel):
    """Result of describe_connection."""

    model_config = ConfigDict(frozen=True)

    connection_arn: str | None = None
    name: str | None = None
    description: str | None = None
    invocation_connectivity_parameters: dict[str, Any] | None = None
    connection_state: str | None = None
    state_reason: str | None = None
    authorization_type: str | None = None
    secret_arn: str | None = None
    kms_key_identifier: str | None = None
    auth_parameters: dict[str, Any] | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    last_authorized_time: str | None = None


class DescribeEndpointResult(BaseModel):
    """Result of describe_endpoint."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    description: str | None = None
    arn: str | None = None
    routing_config: dict[str, Any] | None = None
    replication_config: dict[str, Any] | None = None
    event_buses: list[dict[str, Any]] | None = None
    role_arn: str | None = None
    endpoint_id: str | None = None
    endpoint_url: str | None = None
    state: str | None = None
    state_reason: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None


class DescribeEventBusResult(BaseModel):
    """Result of describe_event_bus."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    arn: str | None = None
    description: str | None = None
    kms_key_identifier: str | None = None
    dead_letter_config: dict[str, Any] | None = None
    policy: str | None = None
    log_config: dict[str, Any] | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None


class DescribeEventSourceResult(BaseModel):
    """Result of describe_event_source."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    created_by: str | None = None
    creation_time: str | None = None
    expiration_time: str | None = None
    name: str | None = None
    state: str | None = None


class DescribePartnerEventSourceResult(BaseModel):
    """Result of describe_partner_event_source."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    name: str | None = None


class DescribeReplayResult(BaseModel):
    """Result of describe_replay."""

    model_config = ConfigDict(frozen=True)

    replay_name: str | None = None
    replay_arn: str | None = None
    description: str | None = None
    state: str | None = None
    state_reason: str | None = None
    event_source_arn: str | None = None
    destination: dict[str, Any] | None = None
    event_start_time: str | None = None
    event_end_time: str | None = None
    event_last_replayed_time: str | None = None
    replay_start_time: str | None = None
    replay_end_time: str | None = None


class DescribeRuleResult(BaseModel):
    """Result of describe_rule."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    arn: str | None = None
    event_pattern: str | None = None
    schedule_expression: str | None = None
    state: str | None = None
    description: str | None = None
    role_arn: str | None = None
    managed_by: str | None = None
    event_bus_name: str | None = None
    created_by: str | None = None


class ListApiDestinationsResult(BaseModel):
    """Result of list_api_destinations."""

    model_config = ConfigDict(frozen=True)

    api_destinations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListArchivesResult(BaseModel):
    """Result of list_archives."""

    model_config = ConfigDict(frozen=True)

    archives: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListConnectionsResult(BaseModel):
    """Result of list_connections."""

    model_config = ConfigDict(frozen=True)

    connections: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEndpointsResult(BaseModel):
    """Result of list_endpoints."""

    model_config = ConfigDict(frozen=True)

    endpoints: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEventBusesResult(BaseModel):
    """Result of list_event_buses."""

    model_config = ConfigDict(frozen=True)

    event_buses: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEventSourcesResult(BaseModel):
    """Result of list_event_sources."""

    model_config = ConfigDict(frozen=True)

    event_sources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPartnerEventSourceAccountsResult(BaseModel):
    """Result of list_partner_event_source_accounts."""

    model_config = ConfigDict(frozen=True)

    partner_event_source_accounts: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPartnerEventSourcesResult(BaseModel):
    """Result of list_partner_event_sources."""

    model_config = ConfigDict(frozen=True)

    partner_event_sources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListReplaysResult(BaseModel):
    """Result of list_replays."""

    model_config = ConfigDict(frozen=True)

    replays: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRuleNamesByTargetResult(BaseModel):
    """Result of list_rule_names_by_target."""

    model_config = ConfigDict(frozen=True)

    rule_names: list[str] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class ListTargetsByRuleResult(BaseModel):
    """Result of list_targets_by_rule."""

    model_config = ConfigDict(frozen=True)

    targets: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutPartnerEventsResult(BaseModel):
    """Result of put_partner_events."""

    model_config = ConfigDict(frozen=True)

    failed_entry_count: int | None = None
    entries: list[dict[str, Any]] | None = None


class PutRuleResult(BaseModel):
    """Result of put_rule."""

    model_config = ConfigDict(frozen=True)

    rule_arn: str | None = None


class PutTargetsResult(BaseModel):
    """Result of put_targets."""

    model_config = ConfigDict(frozen=True)

    failed_entry_count: int | None = None
    failed_entries: list[dict[str, Any]] | None = None


class RemoveTargetsResult(BaseModel):
    """Result of remove_targets."""

    model_config = ConfigDict(frozen=True)

    failed_entry_count: int | None = None
    failed_entries: list[dict[str, Any]] | None = None


class RunEventPatternResult(BaseModel):
    """Result of run_event_pattern."""

    model_config = ConfigDict(frozen=True)

    result: bool | None = None


class StartReplayResult(BaseModel):
    """Result of start_replay."""

    model_config = ConfigDict(frozen=True)

    replay_arn: str | None = None
    state: str | None = None
    state_reason: str | None = None
    replay_start_time: str | None = None


class UpdateApiDestinationResult(BaseModel):
    """Result of update_api_destination."""

    model_config = ConfigDict(frozen=True)

    api_destination_arn: str | None = None
    api_destination_state: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None


class UpdateArchiveResult(BaseModel):
    """Result of update_archive."""

    model_config = ConfigDict(frozen=True)

    archive_arn: str | None = None
    state: str | None = None
    state_reason: str | None = None
    creation_time: str | None = None


class UpdateConnectionResult(BaseModel):
    """Result of update_connection."""

    model_config = ConfigDict(frozen=True)

    connection_arn: str | None = None
    connection_state: str | None = None
    creation_time: str | None = None
    last_modified_time: str | None = None
    last_authorized_time: str | None = None


class UpdateEndpointResult(BaseModel):
    """Result of update_endpoint."""

    model_config = ConfigDict(frozen=True)

    name: str | None = None
    arn: str | None = None
    routing_config: dict[str, Any] | None = None
    replication_config: dict[str, Any] | None = None
    event_buses: list[dict[str, Any]] | None = None
    role_arn: str | None = None
    endpoint_id: str | None = None
    endpoint_url: str | None = None
    state: str | None = None


class UpdateEventBusResult(BaseModel):
    """Result of update_event_bus."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    name: str | None = None
    kms_key_identifier: str | None = None
    description: str | None = None
    dead_letter_config: dict[str, Any] | None = None
    log_config: dict[str, Any] | None = None


def activate_event_source(
    name: str,
    region_name: str | None = None,
) -> None:
    """Activate event source.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.activate_event_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to activate event source") from exc
    return None


def cancel_replay(
    replay_name: str,
    region_name: str | None = None,
) -> CancelReplayResult:
    """Cancel replay.

    Args:
        replay_name: Replay name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplayName"] = replay_name
    try:
        resp = client.cancel_replay(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel replay") from exc
    return CancelReplayResult(
        replay_arn=resp.get("ReplayArn"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
    )


def create_api_destination(
    name: str,
    connection_arn: str,
    invocation_endpoint: str,
    http_method: str,
    *,
    description: str | None = None,
    invocation_rate_limit_per_second: int | None = None,
    region_name: str | None = None,
) -> CreateApiDestinationResult:
    """Create api destination.

    Args:
        name: Name.
        connection_arn: Connection arn.
        invocation_endpoint: Invocation endpoint.
        http_method: Http method.
        description: Description.
        invocation_rate_limit_per_second: Invocation rate limit per second.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ConnectionArn"] = connection_arn
    kwargs["InvocationEndpoint"] = invocation_endpoint
    kwargs["HttpMethod"] = http_method
    if description is not None:
        kwargs["Description"] = description
    if invocation_rate_limit_per_second is not None:
        kwargs["InvocationRateLimitPerSecond"] = invocation_rate_limit_per_second
    try:
        resp = client.create_api_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create api destination") from exc
    return CreateApiDestinationResult(
        api_destination_arn=resp.get("ApiDestinationArn"),
        api_destination_state=resp.get("ApiDestinationState"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def create_archive(
    archive_name: str,
    event_source_arn: str,
    *,
    description: str | None = None,
    event_pattern: str | None = None,
    retention_days: int | None = None,
    kms_key_identifier: str | None = None,
    region_name: str | None = None,
) -> CreateArchiveResult:
    """Create archive.

    Args:
        archive_name: Archive name.
        event_source_arn: Event source arn.
        description: Description.
        event_pattern: Event pattern.
        retention_days: Retention days.
        kms_key_identifier: Kms key identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ArchiveName"] = archive_name
    kwargs["EventSourceArn"] = event_source_arn
    if description is not None:
        kwargs["Description"] = description
    if event_pattern is not None:
        kwargs["EventPattern"] = event_pattern
    if retention_days is not None:
        kwargs["RetentionDays"] = retention_days
    if kms_key_identifier is not None:
        kwargs["KmsKeyIdentifier"] = kms_key_identifier
    try:
        resp = client.create_archive(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create archive") from exc
    return CreateArchiveResult(
        archive_arn=resp.get("ArchiveArn"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        creation_time=resp.get("CreationTime"),
    )


def create_connection(
    name: str,
    authorization_type: str,
    auth_parameters: dict[str, Any],
    *,
    description: str | None = None,
    invocation_connectivity_parameters: dict[str, Any] | None = None,
    kms_key_identifier: str | None = None,
    region_name: str | None = None,
) -> CreateConnectionResult:
    """Create connection.

    Args:
        name: Name.
        authorization_type: Authorization type.
        auth_parameters: Auth parameters.
        description: Description.
        invocation_connectivity_parameters: Invocation connectivity parameters.
        kms_key_identifier: Kms key identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["AuthorizationType"] = authorization_type
    kwargs["AuthParameters"] = auth_parameters
    if description is not None:
        kwargs["Description"] = description
    if invocation_connectivity_parameters is not None:
        kwargs["InvocationConnectivityParameters"] = invocation_connectivity_parameters
    if kms_key_identifier is not None:
        kwargs["KmsKeyIdentifier"] = kms_key_identifier
    try:
        resp = client.create_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create connection") from exc
    return CreateConnectionResult(
        connection_arn=resp.get("ConnectionArn"),
        connection_state=resp.get("ConnectionState"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def create_endpoint(
    name: str,
    routing_config: dict[str, Any],
    event_buses: list[dict[str, Any]],
    *,
    description: str | None = None,
    replication_config: dict[str, Any] | None = None,
    role_arn: str | None = None,
    region_name: str | None = None,
) -> CreateEndpointResult:
    """Create endpoint.

    Args:
        name: Name.
        routing_config: Routing config.
        event_buses: Event buses.
        description: Description.
        replication_config: Replication config.
        role_arn: Role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["RoutingConfig"] = routing_config
    kwargs["EventBuses"] = event_buses
    if description is not None:
        kwargs["Description"] = description
    if replication_config is not None:
        kwargs["ReplicationConfig"] = replication_config
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    try:
        resp = client.create_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create endpoint") from exc
    return CreateEndpointResult(
        name=resp.get("Name"),
        arn=resp.get("Arn"),
        routing_config=resp.get("RoutingConfig"),
        replication_config=resp.get("ReplicationConfig"),
        event_buses=resp.get("EventBuses"),
        role_arn=resp.get("RoleArn"),
        state=resp.get("State"),
    )


def create_event_bus(
    name: str,
    *,
    event_source_name: str | None = None,
    description: str | None = None,
    kms_key_identifier: str | None = None,
    dead_letter_config: dict[str, Any] | None = None,
    log_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateEventBusResult:
    """Create event bus.

    Args:
        name: Name.
        event_source_name: Event source name.
        description: Description.
        kms_key_identifier: Kms key identifier.
        dead_letter_config: Dead letter config.
        log_config: Log config.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if event_source_name is not None:
        kwargs["EventSourceName"] = event_source_name
    if description is not None:
        kwargs["Description"] = description
    if kms_key_identifier is not None:
        kwargs["KmsKeyIdentifier"] = kms_key_identifier
    if dead_letter_config is not None:
        kwargs["DeadLetterConfig"] = dead_letter_config
    if log_config is not None:
        kwargs["LogConfig"] = log_config
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_event_bus(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create event bus") from exc
    return CreateEventBusResult(
        event_bus_arn=resp.get("EventBusArn"),
        description=resp.get("Description"),
        kms_key_identifier=resp.get("KmsKeyIdentifier"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        log_config=resp.get("LogConfig"),
    )


def create_partner_event_source(
    name: str,
    account: str,
    region_name: str | None = None,
) -> CreatePartnerEventSourceResult:
    """Create partner event source.

    Args:
        name: Name.
        account: Account.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Account"] = account
    try:
        resp = client.create_partner_event_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create partner event source") from exc
    return CreatePartnerEventSourceResult(
        event_source_arn=resp.get("EventSourceArn"),
    )


def deactivate_event_source(
    name: str,
    region_name: str | None = None,
) -> None:
    """Deactivate event source.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.deactivate_event_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deactivate event source") from exc
    return None


def deauthorize_connection(
    name: str,
    region_name: str | None = None,
) -> DeauthorizeConnectionResult:
    """Deauthorize connection.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.deauthorize_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deauthorize connection") from exc
    return DeauthorizeConnectionResult(
        connection_arn=resp.get("ConnectionArn"),
        connection_state=resp.get("ConnectionState"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_authorized_time=resp.get("LastAuthorizedTime"),
    )


def delete_api_destination(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete api destination.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_api_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete api destination") from exc
    return None


def delete_archive(
    archive_name: str,
    region_name: str | None = None,
) -> None:
    """Delete archive.

    Args:
        archive_name: Archive name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ArchiveName"] = archive_name
    try:
        client.delete_archive(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete archive") from exc
    return None


def delete_connection(
    name: str,
    region_name: str | None = None,
) -> DeleteConnectionResult:
    """Delete connection.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.delete_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete connection") from exc
    return DeleteConnectionResult(
        connection_arn=resp.get("ConnectionArn"),
        connection_state=resp.get("ConnectionState"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_authorized_time=resp.get("LastAuthorizedTime"),
    )


def delete_endpoint(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete endpoint.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete endpoint") from exc
    return None


def delete_event_bus(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete event bus.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_event_bus(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete event bus") from exc
    return None


def delete_partner_event_source(
    name: str,
    account: str,
    region_name: str | None = None,
) -> None:
    """Delete partner event source.

    Args:
        name: Name.
        account: Account.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Account"] = account
    try:
        client.delete_partner_event_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete partner event source") from exc
    return None


def delete_rule(
    name: str,
    *,
    event_bus_name: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete rule.

    Args:
        name: Name.
        event_bus_name: Event bus name.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    if force is not None:
        kwargs["Force"] = force
    try:
        client.delete_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete rule") from exc
    return None


def describe_api_destination(
    name: str,
    region_name: str | None = None,
) -> DescribeApiDestinationResult:
    """Describe api destination.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_api_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe api destination") from exc
    return DescribeApiDestinationResult(
        api_destination_arn=resp.get("ApiDestinationArn"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        api_destination_state=resp.get("ApiDestinationState"),
        connection_arn=resp.get("ConnectionArn"),
        invocation_endpoint=resp.get("InvocationEndpoint"),
        http_method=resp.get("HttpMethod"),
        invocation_rate_limit_per_second=resp.get("InvocationRateLimitPerSecond"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def describe_archive(
    archive_name: str,
    region_name: str | None = None,
) -> DescribeArchiveResult:
    """Describe archive.

    Args:
        archive_name: Archive name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ArchiveName"] = archive_name
    try:
        resp = client.describe_archive(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe archive") from exc
    return DescribeArchiveResult(
        archive_arn=resp.get("ArchiveArn"),
        archive_name=resp.get("ArchiveName"),
        event_source_arn=resp.get("EventSourceArn"),
        description=resp.get("Description"),
        event_pattern=resp.get("EventPattern"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        kms_key_identifier=resp.get("KmsKeyIdentifier"),
        retention_days=resp.get("RetentionDays"),
        size_bytes=resp.get("SizeBytes"),
        event_count=resp.get("EventCount"),
        creation_time=resp.get("CreationTime"),
    )


def describe_connection(
    name: str,
    region_name: str | None = None,
) -> DescribeConnectionResult:
    """Describe connection.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe connection") from exc
    return DescribeConnectionResult(
        connection_arn=resp.get("ConnectionArn"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        invocation_connectivity_parameters=resp.get("InvocationConnectivityParameters"),
        connection_state=resp.get("ConnectionState"),
        state_reason=resp.get("StateReason"),
        authorization_type=resp.get("AuthorizationType"),
        secret_arn=resp.get("SecretArn"),
        kms_key_identifier=resp.get("KmsKeyIdentifier"),
        auth_parameters=resp.get("AuthParameters"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_authorized_time=resp.get("LastAuthorizedTime"),
    )


def describe_endpoint(
    name: str,
    *,
    home_region: str | None = None,
    region_name: str | None = None,
) -> DescribeEndpointResult:
    """Describe endpoint.

    Args:
        name: Name.
        home_region: Home region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if home_region is not None:
        kwargs["HomeRegion"] = home_region
    try:
        resp = client.describe_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint") from exc
    return DescribeEndpointResult(
        name=resp.get("Name"),
        description=resp.get("Description"),
        arn=resp.get("Arn"),
        routing_config=resp.get("RoutingConfig"),
        replication_config=resp.get("ReplicationConfig"),
        event_buses=resp.get("EventBuses"),
        role_arn=resp.get("RoleArn"),
        endpoint_id=resp.get("EndpointId"),
        endpoint_url=resp.get("EndpointUrl"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def describe_event_bus(
    *,
    name: str | None = None,
    region_name: str | None = None,
) -> DescribeEventBusResult:
    """Describe event bus.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = client.describe_event_bus(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe event bus") from exc
    return DescribeEventBusResult(
        name=resp.get("Name"),
        arn=resp.get("Arn"),
        description=resp.get("Description"),
        kms_key_identifier=resp.get("KmsKeyIdentifier"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        policy=resp.get("Policy"),
        log_config=resp.get("LogConfig"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def describe_event_source(
    name: str,
    region_name: str | None = None,
) -> DescribeEventSourceResult:
    """Describe event source.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_event_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe event source") from exc
    return DescribeEventSourceResult(
        arn=resp.get("Arn"),
        created_by=resp.get("CreatedBy"),
        creation_time=resp.get("CreationTime"),
        expiration_time=resp.get("ExpirationTime"),
        name=resp.get("Name"),
        state=resp.get("State"),
    )


def describe_partner_event_source(
    name: str,
    region_name: str | None = None,
) -> DescribePartnerEventSourceResult:
    """Describe partner event source.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.describe_partner_event_source(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe partner event source") from exc
    return DescribePartnerEventSourceResult(
        arn=resp.get("Arn"),
        name=resp.get("Name"),
    )


def describe_replay(
    replay_name: str,
    region_name: str | None = None,
) -> DescribeReplayResult:
    """Describe replay.

    Args:
        replay_name: Replay name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplayName"] = replay_name
    try:
        resp = client.describe_replay(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe replay") from exc
    return DescribeReplayResult(
        replay_name=resp.get("ReplayName"),
        replay_arn=resp.get("ReplayArn"),
        description=resp.get("Description"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        event_source_arn=resp.get("EventSourceArn"),
        destination=resp.get("Destination"),
        event_start_time=resp.get("EventStartTime"),
        event_end_time=resp.get("EventEndTime"),
        event_last_replayed_time=resp.get("EventLastReplayedTime"),
        replay_start_time=resp.get("ReplayStartTime"),
        replay_end_time=resp.get("ReplayEndTime"),
    )


def describe_rule(
    name: str,
    *,
    event_bus_name: str | None = None,
    region_name: str | None = None,
) -> DescribeRuleResult:
    """Describe rule.

    Args:
        name: Name.
        event_bus_name: Event bus name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    try:
        resp = client.describe_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe rule") from exc
    return DescribeRuleResult(
        name=resp.get("Name"),
        arn=resp.get("Arn"),
        event_pattern=resp.get("EventPattern"),
        schedule_expression=resp.get("ScheduleExpression"),
        state=resp.get("State"),
        description=resp.get("Description"),
        role_arn=resp.get("RoleArn"),
        managed_by=resp.get("ManagedBy"),
        event_bus_name=resp.get("EventBusName"),
        created_by=resp.get("CreatedBy"),
    )


def disable_rule(
    name: str,
    *,
    event_bus_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disable rule.

    Args:
        name: Name.
        event_bus_name: Event bus name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    try:
        client.disable_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable rule") from exc
    return None


def enable_rule(
    name: str,
    *,
    event_bus_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Enable rule.

    Args:
        name: Name.
        event_bus_name: Event bus name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    try:
        client.enable_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable rule") from exc
    return None


def list_api_destinations(
    *,
    name_prefix: str | None = None,
    connection_arn: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListApiDestinationsResult:
    """List api destinations.

    Args:
        name_prefix: Name prefix.
        connection_arn: Connection arn.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if connection_arn is not None:
        kwargs["ConnectionArn"] = connection_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_api_destinations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list api destinations") from exc
    return ListApiDestinationsResult(
        api_destinations=resp.get("ApiDestinations"),
        next_token=resp.get("NextToken"),
    )


def list_archives(
    *,
    name_prefix: str | None = None,
    event_source_arn: str | None = None,
    state: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListArchivesResult:
    """List archives.

    Args:
        name_prefix: Name prefix.
        event_source_arn: Event source arn.
        state: State.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if event_source_arn is not None:
        kwargs["EventSourceArn"] = event_source_arn
    if state is not None:
        kwargs["State"] = state
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_archives(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list archives") from exc
    return ListArchivesResult(
        archives=resp.get("Archives"),
        next_token=resp.get("NextToken"),
    )


def list_connections(
    *,
    name_prefix: str | None = None,
    connection_state: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListConnectionsResult:
    """List connections.

    Args:
        name_prefix: Name prefix.
        connection_state: Connection state.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if connection_state is not None:
        kwargs["ConnectionState"] = connection_state
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_connections(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list connections") from exc
    return ListConnectionsResult(
        connections=resp.get("Connections"),
        next_token=resp.get("NextToken"),
    )


def list_endpoints(
    *,
    name_prefix: str | None = None,
    home_region: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEndpointsResult:
    """List endpoints.

    Args:
        name_prefix: Name prefix.
        home_region: Home region.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if home_region is not None:
        kwargs["HomeRegion"] = home_region
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list endpoints") from exc
    return ListEndpointsResult(
        endpoints=resp.get("Endpoints"),
        next_token=resp.get("NextToken"),
    )


def list_event_buses(
    *,
    name_prefix: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListEventBusesResult:
    """List event buses.

    Args:
        name_prefix: Name prefix.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_event_buses(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list event buses") from exc
    return ListEventBusesResult(
        event_buses=resp.get("EventBuses"),
        next_token=resp.get("NextToken"),
    )


def list_event_sources(
    *,
    name_prefix: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListEventSourcesResult:
    """List event sources.

    Args:
        name_prefix: Name prefix.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_event_sources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list event sources") from exc
    return ListEventSourcesResult(
        event_sources=resp.get("EventSources"),
        next_token=resp.get("NextToken"),
    )


def list_partner_event_source_accounts(
    event_source_name: str,
    *,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListPartnerEventSourceAccountsResult:
    """List partner event source accounts.

    Args:
        event_source_name: Event source name.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventSourceName"] = event_source_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_partner_event_source_accounts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list partner event source accounts") from exc
    return ListPartnerEventSourceAccountsResult(
        partner_event_source_accounts=resp.get("PartnerEventSourceAccounts"),
        next_token=resp.get("NextToken"),
    )


def list_partner_event_sources(
    name_prefix: str,
    *,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListPartnerEventSourcesResult:
    """List partner event sources.

    Args:
        name_prefix: Name prefix.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamePrefix"] = name_prefix
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_partner_event_sources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list partner event sources") from exc
    return ListPartnerEventSourcesResult(
        partner_event_sources=resp.get("PartnerEventSources"),
        next_token=resp.get("NextToken"),
    )


def list_replays(
    *,
    name_prefix: str | None = None,
    state: str | None = None,
    event_source_arn: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListReplaysResult:
    """List replays.

    Args:
        name_prefix: Name prefix.
        state: State.
        event_source_arn: Event source arn.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if state is not None:
        kwargs["State"] = state
    if event_source_arn is not None:
        kwargs["EventSourceArn"] = event_source_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_replays(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list replays") from exc
    return ListReplaysResult(
        replays=resp.get("Replays"),
        next_token=resp.get("NextToken"),
    )


def list_rule_names_by_target(
    target_arn: str,
    *,
    event_bus_name: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListRuleNamesByTargetResult:
    """List rule names by target.

    Args:
        target_arn: Target arn.
        event_bus_name: Event bus name.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetArn"] = target_arn
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_rule_names_by_target(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list rule names by target") from exc
    return ListRuleNamesByTargetResult(
        rule_names=resp.get("RuleNames"),
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
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def list_targets_by_rule(
    rule: str,
    *,
    event_bus_name: str | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListTargetsByRuleResult:
    """List targets by rule.

    Args:
        rule: Rule.
        event_bus_name: Event bus name.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Rule"] = rule
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_targets_by_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list targets by rule") from exc
    return ListTargetsByRuleResult(
        targets=resp.get("Targets"),
        next_token=resp.get("NextToken"),
    )


def put_partner_events(
    entries: list[dict[str, Any]],
    region_name: str | None = None,
) -> PutPartnerEventsResult:
    """Put partner events.

    Args:
        entries: Entries.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Entries"] = entries
    try:
        resp = client.put_partner_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put partner events") from exc
    return PutPartnerEventsResult(
        failed_entry_count=resp.get("FailedEntryCount"),
        entries=resp.get("Entries"),
    )


def put_permission(
    *,
    event_bus_name: str | None = None,
    action: str | None = None,
    principal: str | None = None,
    statement_id: str | None = None,
    condition: dict[str, Any] | None = None,
    policy: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put permission.

    Args:
        event_bus_name: Event bus name.
        action: Action.
        principal: Principal.
        statement_id: Statement id.
        condition: Condition.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    if action is not None:
        kwargs["Action"] = action
    if principal is not None:
        kwargs["Principal"] = principal
    if statement_id is not None:
        kwargs["StatementId"] = statement_id
    if condition is not None:
        kwargs["Condition"] = condition
    if policy is not None:
        kwargs["Policy"] = policy
    try:
        client.put_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put permission") from exc
    return None


def put_rule(
    name: str,
    *,
    schedule_expression: str | None = None,
    event_pattern: str | None = None,
    state: str | None = None,
    description: str | None = None,
    role_arn: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    event_bus_name: str | None = None,
    region_name: str | None = None,
) -> PutRuleResult:
    """Put rule.

    Args:
        name: Name.
        schedule_expression: Schedule expression.
        event_pattern: Event pattern.
        state: State.
        description: Description.
        role_arn: Role arn.
        tags: Tags.
        event_bus_name: Event bus name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if schedule_expression is not None:
        kwargs["ScheduleExpression"] = schedule_expression
    if event_pattern is not None:
        kwargs["EventPattern"] = event_pattern
    if state is not None:
        kwargs["State"] = state
    if description is not None:
        kwargs["Description"] = description
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    if tags is not None:
        kwargs["Tags"] = tags
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    try:
        resp = client.put_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put rule") from exc
    return PutRuleResult(
        rule_arn=resp.get("RuleArn"),
    )


def put_targets(
    rule: str,
    targets: list[dict[str, Any]],
    *,
    event_bus_name: str | None = None,
    region_name: str | None = None,
) -> PutTargetsResult:
    """Put targets.

    Args:
        rule: Rule.
        targets: Targets.
        event_bus_name: Event bus name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Rule"] = rule
    kwargs["Targets"] = targets
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    try:
        resp = client.put_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put targets") from exc
    return PutTargetsResult(
        failed_entry_count=resp.get("FailedEntryCount"),
        failed_entries=resp.get("FailedEntries"),
    )


def remove_permission(
    *,
    statement_id: str | None = None,
    remove_all_permissions: bool | None = None,
    event_bus_name: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove permission.

    Args:
        statement_id: Statement id.
        remove_all_permissions: Remove all permissions.
        event_bus_name: Event bus name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if statement_id is not None:
        kwargs["StatementId"] = statement_id
    if remove_all_permissions is not None:
        kwargs["RemoveAllPermissions"] = remove_all_permissions
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    try:
        client.remove_permission(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove permission") from exc
    return None


def remove_targets(
    rule: str,
    ids: list[str],
    *,
    event_bus_name: str | None = None,
    force: bool | None = None,
    region_name: str | None = None,
) -> RemoveTargetsResult:
    """Remove targets.

    Args:
        rule: Rule.
        ids: Ids.
        event_bus_name: Event bus name.
        force: Force.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Rule"] = rule
    kwargs["Ids"] = ids
    if event_bus_name is not None:
        kwargs["EventBusName"] = event_bus_name
    if force is not None:
        kwargs["Force"] = force
    try:
        resp = client.remove_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove targets") from exc
    return RemoveTargetsResult(
        failed_entry_count=resp.get("FailedEntryCount"),
        failed_entries=resp.get("FailedEntries"),
    )


def run_event_pattern(
    event_pattern: str,
    event: str,
    region_name: str | None = None,
) -> RunEventPatternResult:
    """Run event pattern.

    Args:
        event_pattern: Event pattern.
        event: Event.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventPattern"] = event_pattern
    kwargs["Event"] = event
    try:
        resp = client.test_event_pattern(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to run event pattern") from exc
    return RunEventPatternResult(
        result=resp.get("Result"),
    )


def start_replay(
    replay_name: str,
    event_source_arn: str,
    event_start_time: str,
    event_end_time: str,
    destination: dict[str, Any],
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> StartReplayResult:
    """Start replay.

    Args:
        replay_name: Replay name.
        event_source_arn: Event source arn.
        event_start_time: Event start time.
        event_end_time: Event end time.
        destination: Destination.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplayName"] = replay_name
    kwargs["EventSourceArn"] = event_source_arn
    kwargs["EventStartTime"] = event_start_time
    kwargs["EventEndTime"] = event_end_time
    kwargs["Destination"] = destination
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.start_replay(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start replay") from exc
    return StartReplayResult(
        replay_arn=resp.get("ReplayArn"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        replay_start_time=resp.get("ReplayStartTime"),
    )


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
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
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
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
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_api_destination(
    name: str,
    *,
    description: str | None = None,
    connection_arn: str | None = None,
    invocation_endpoint: str | None = None,
    http_method: str | None = None,
    invocation_rate_limit_per_second: int | None = None,
    region_name: str | None = None,
) -> UpdateApiDestinationResult:
    """Update api destination.

    Args:
        name: Name.
        description: Description.
        connection_arn: Connection arn.
        invocation_endpoint: Invocation endpoint.
        http_method: Http method.
        invocation_rate_limit_per_second: Invocation rate limit per second.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if connection_arn is not None:
        kwargs["ConnectionArn"] = connection_arn
    if invocation_endpoint is not None:
        kwargs["InvocationEndpoint"] = invocation_endpoint
    if http_method is not None:
        kwargs["HttpMethod"] = http_method
    if invocation_rate_limit_per_second is not None:
        kwargs["InvocationRateLimitPerSecond"] = invocation_rate_limit_per_second
    try:
        resp = client.update_api_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update api destination") from exc
    return UpdateApiDestinationResult(
        api_destination_arn=resp.get("ApiDestinationArn"),
        api_destination_state=resp.get("ApiDestinationState"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def update_archive(
    archive_name: str,
    *,
    description: str | None = None,
    event_pattern: str | None = None,
    retention_days: int | None = None,
    kms_key_identifier: str | None = None,
    region_name: str | None = None,
) -> UpdateArchiveResult:
    """Update archive.

    Args:
        archive_name: Archive name.
        description: Description.
        event_pattern: Event pattern.
        retention_days: Retention days.
        kms_key_identifier: Kms key identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ArchiveName"] = archive_name
    if description is not None:
        kwargs["Description"] = description
    if event_pattern is not None:
        kwargs["EventPattern"] = event_pattern
    if retention_days is not None:
        kwargs["RetentionDays"] = retention_days
    if kms_key_identifier is not None:
        kwargs["KmsKeyIdentifier"] = kms_key_identifier
    try:
        resp = client.update_archive(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update archive") from exc
    return UpdateArchiveResult(
        archive_arn=resp.get("ArchiveArn"),
        state=resp.get("State"),
        state_reason=resp.get("StateReason"),
        creation_time=resp.get("CreationTime"),
    )


def update_connection(
    name: str,
    *,
    description: str | None = None,
    authorization_type: str | None = None,
    auth_parameters: dict[str, Any] | None = None,
    invocation_connectivity_parameters: dict[str, Any] | None = None,
    kms_key_identifier: str | None = None,
    region_name: str | None = None,
) -> UpdateConnectionResult:
    """Update connection.

    Args:
        name: Name.
        description: Description.
        authorization_type: Authorization type.
        auth_parameters: Auth parameters.
        invocation_connectivity_parameters: Invocation connectivity parameters.
        kms_key_identifier: Kms key identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if authorization_type is not None:
        kwargs["AuthorizationType"] = authorization_type
    if auth_parameters is not None:
        kwargs["AuthParameters"] = auth_parameters
    if invocation_connectivity_parameters is not None:
        kwargs["InvocationConnectivityParameters"] = invocation_connectivity_parameters
    if kms_key_identifier is not None:
        kwargs["KmsKeyIdentifier"] = kms_key_identifier
    try:
        resp = client.update_connection(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update connection") from exc
    return UpdateConnectionResult(
        connection_arn=resp.get("ConnectionArn"),
        connection_state=resp.get("ConnectionState"),
        creation_time=resp.get("CreationTime"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_authorized_time=resp.get("LastAuthorizedTime"),
    )


def update_endpoint(
    name: str,
    *,
    description: str | None = None,
    routing_config: dict[str, Any] | None = None,
    replication_config: dict[str, Any] | None = None,
    event_buses: list[dict[str, Any]] | None = None,
    role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateEndpointResult:
    """Update endpoint.

    Args:
        name: Name.
        description: Description.
        routing_config: Routing config.
        replication_config: Replication config.
        event_buses: Event buses.
        role_arn: Role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if routing_config is not None:
        kwargs["RoutingConfig"] = routing_config
    if replication_config is not None:
        kwargs["ReplicationConfig"] = replication_config
    if event_buses is not None:
        kwargs["EventBuses"] = event_buses
    if role_arn is not None:
        kwargs["RoleArn"] = role_arn
    try:
        resp = client.update_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update endpoint") from exc
    return UpdateEndpointResult(
        name=resp.get("Name"),
        arn=resp.get("Arn"),
        routing_config=resp.get("RoutingConfig"),
        replication_config=resp.get("ReplicationConfig"),
        event_buses=resp.get("EventBuses"),
        role_arn=resp.get("RoleArn"),
        endpoint_id=resp.get("EndpointId"),
        endpoint_url=resp.get("EndpointUrl"),
        state=resp.get("State"),
    )


def update_event_bus(
    *,
    name: str | None = None,
    kms_key_identifier: str | None = None,
    description: str | None = None,
    dead_letter_config: dict[str, Any] | None = None,
    log_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateEventBusResult:
    """Update event bus.

    Args:
        name: Name.
        kms_key_identifier: Kms key identifier.
        description: Description.
        dead_letter_config: Dead letter config.
        log_config: Log config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("events", region_name)
    kwargs: dict[str, Any] = {}
    if name is not None:
        kwargs["Name"] = name
    if kms_key_identifier is not None:
        kwargs["KmsKeyIdentifier"] = kms_key_identifier
    if description is not None:
        kwargs["Description"] = description
    if dead_letter_config is not None:
        kwargs["DeadLetterConfig"] = dead_letter_config
    if log_config is not None:
        kwargs["LogConfig"] = log_config
    try:
        resp = client.update_event_bus(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update event bus") from exc
    return UpdateEventBusResult(
        arn=resp.get("Arn"),
        name=resp.get("Name"),
        kms_key_identifier=resp.get("KmsKeyIdentifier"),
        description=resp.get("Description"),
        dead_letter_config=resp.get("DeadLetterConfig"),
        log_config=resp.get("LogConfig"),
    )
