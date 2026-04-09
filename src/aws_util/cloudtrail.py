"""aws_util.cloudtrail — AWS CloudTrail utilities.

Provides high-level helpers for managing CloudTrail trails, event data
stores, event selectors, insight selectors, and event lookup.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CancelQueryResult",
    "CreateChannelResult",
    "CreateDashboardResult",
    "DescribeQueryResult",
    "DisableFederationResult",
    "EnableFederationResult",
    "EventDataStoreResult",
    "EventSelectorResult",
    "GenerateQueryResult",
    "GetChannelResult",
    "GetDashboardResult",
    "GetEventConfigurationResult",
    "GetEventDataStoreResult",
    "GetImportResult",
    "GetResourcePolicyResult",
    "InsightSelectorResult",
    "ListChannelsResult",
    "ListDashboardsResult",
    "ListImportFailuresResult",
    "ListImportsResult",
    "ListInsightsMetricDataResult",
    "ListPublicKeysResult",
    "ListTagsResult",
    "LookupEvent",
    "PutEventConfigurationResult",
    "PutResourcePolicyResult",
    "QueryResult",
    "RestoreEventDataStoreResult",
    "SearchSampleQueriesResult",
    "StartDashboardRefreshResult",
    "StartImportResult",
    "StopImportResult",
    "TrailResult",
    "TrailStatus",
    "TrailSummary",
    "UpdateChannelResult",
    "UpdateDashboardResult",
    "UpdateEventDataStoreResult",
    "add_tags",
    "cancel_query",
    "create_channel",
    "create_dashboard",
    "create_event_data_store",
    "create_trail",
    "delete_channel",
    "delete_dashboard",
    "delete_event_data_store",
    "delete_resource_policy",
    "delete_trail",
    "deregister_organization_delegated_admin",
    "describe_event_data_store",
    "describe_query",
    "describe_trails",
    "disable_federation",
    "enable_federation",
    "generate_query",
    "get_channel",
    "get_dashboard",
    "get_event_configuration",
    "get_event_data_store",
    "get_event_selectors",
    "get_import",
    "get_insight_selectors",
    "get_query_results",
    "get_resource_policy",
    "get_trail",
    "get_trail_status",
    "list_channels",
    "list_dashboards",
    "list_event_data_stores",
    "list_import_failures",
    "list_imports",
    "list_insights_metric_data",
    "list_public_keys",
    "list_queries",
    "list_tags",
    "list_trails",
    "lookup_events",
    "put_event_configuration",
    "put_event_selectors",
    "put_insight_selectors",
    "put_resource_policy",
    "register_organization_delegated_admin",
    "remove_tags",
    "restore_event_data_store",
    "search_sample_queries",
    "start_dashboard_refresh",
    "start_event_data_store_ingestion",
    "start_import",
    "start_logging",
    "start_query",
    "stop_event_data_store_ingestion",
    "stop_import",
    "stop_logging",
    "update_channel",
    "update_dashboard",
    "update_event_data_store",
    "update_trail",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TrailResult(BaseModel):
    """Metadata for a CloudTrail trail."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str
    arn: str
    s3_bucket_name: str | None = None
    s3_key_prefix: str | None = None
    sns_topic_arn: str | None = None
    include_global_service_events: bool = True
    is_multi_region_trail: bool = False
    home_region: str | None = None
    log_file_validation_enabled: bool = False
    cloud_watch_logs_log_group_arn: str | None = None
    cloud_watch_logs_role_arn: str | None = None
    kms_key_id: str | None = None
    is_organization_trail: bool = False
    extra: dict[str, Any] = {}


class TrailStatus(BaseModel):
    """Status information for a CloudTrail trail."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    is_logging: bool = False
    latest_delivery_time: Any = None
    latest_notification_time: Any = None
    latest_cloud_watch_logs_delivery_time: Any = None
    start_logging_time: Any = None
    stop_logging_time: Any = None
    latest_delivery_error: str | None = None
    latest_notification_error: str | None = None
    latest_digest_delivery_time: Any = None
    extra: dict[str, Any] = {}


class TrailSummary(BaseModel):
    """Summary information for a CloudTrail trail (from ListTrails)."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    trail_arn: str
    name: str
    home_region: str | None = None


class LookupEvent(BaseModel):
    """An event returned by LookupEvents."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    event_id: str
    event_name: str | None = None
    event_source: str | None = None
    event_time: Any = None
    username: str | None = None
    cloud_trail_event: str | None = None
    resources: list[dict[str, Any]] = []
    extra: dict[str, Any] = {}


class EventDataStoreResult(BaseModel):
    """Metadata for a CloudTrail Lake event data store."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    event_data_store_arn: str
    name: str | None = None
    status: str | None = None
    retention_period: int | None = None
    multi_region_enabled: bool = False
    organization_enabled: bool = False
    created_timestamp: Any = None
    updated_timestamp: Any = None
    advanced_event_selectors: list[dict[str, Any]] = []
    extra: dict[str, Any] = {}


class QueryResult(BaseModel):
    """Result of a CloudTrail Lake query."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    query_id: str
    query_status: str | None = None
    query_statistics: dict[str, Any] = {}
    query_result_rows: list[list[dict[str, str]]] = []
    extra: dict[str, Any] = {}


class EventSelectorResult(BaseModel):
    """Event selectors for a trail."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    trail_arn: str
    event_selectors: list[dict[str, Any]] = []
    advanced_event_selectors: list[dict[str, Any]] = []


class InsightSelectorResult(BaseModel):
    """Insight selectors for a trail."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    trail_arn: str
    insight_selectors: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_TRAIL_KNOWN_KEYS = {
    "Name",
    "TrailARN",
    "S3BucketName",
    "S3KeyPrefix",
    "SnsTopicARN",
    "IncludeGlobalServiceEvents",
    "IsMultiRegionTrail",
    "HomeRegion",
    "LogFileValidationEnabled",
    "CloudWatchLogsLogGroupArn",
    "CloudWatchLogsRoleArn",
    "KmsKeyId",
    "IsOrganizationTrail",
}

_STATUS_KNOWN_KEYS = {
    "IsLogging",
    "LatestDeliveryTime",
    "LatestNotificationTime",
    "LatestCloudWatchLogsDeliveryTime",
    "StartLoggingTime",
    "StopLoggingTime",
    "LatestDeliveryError",
    "LatestNotificationError",
    "LatestDigestDeliveryTime",
}

_LOOKUP_KNOWN_KEYS = {
    "EventId",
    "EventName",
    "EventSource",
    "EventTime",
    "Username",
    "CloudTrailEvent",
    "Resources",
}

_EDS_KNOWN_KEYS = {
    "EventDataStoreArn",
    "Name",
    "Status",
    "RetentionPeriod",
    "MultiRegionEnabled",
    "OrganizationEnabled",
    "CreatedTimestamp",
    "UpdatedTimestamp",
    "AdvancedEventSelectors",
}


def _parse_trail(raw: dict[str, Any]) -> TrailResult:
    """Parse a raw trail dict into a TrailResult model."""
    return TrailResult(
        name=raw.get("Name", ""),
        arn=raw.get("TrailARN", ""),
        s3_bucket_name=raw.get("S3BucketName"),
        s3_key_prefix=raw.get("S3KeyPrefix"),
        sns_topic_arn=raw.get("SnsTopicARN"),
        include_global_service_events=raw.get("IncludeGlobalServiceEvents", True),
        is_multi_region_trail=raw.get("IsMultiRegionTrail", False),
        home_region=raw.get("HomeRegion"),
        log_file_validation_enabled=raw.get("LogFileValidationEnabled", False),
        cloud_watch_logs_log_group_arn=raw.get("CloudWatchLogsLogGroupArn"),
        cloud_watch_logs_role_arn=raw.get("CloudWatchLogsRoleArn"),
        kms_key_id=raw.get("KmsKeyId"),
        is_organization_trail=raw.get("IsOrganizationTrail", False),
        extra={k: v for k, v in raw.items() if k not in _TRAIL_KNOWN_KEYS},
    )


def _parse_status(raw: dict[str, Any]) -> TrailStatus:
    """Parse a raw trail status dict into a TrailStatus model."""
    return TrailStatus(
        is_logging=raw.get("IsLogging", False),
        latest_delivery_time=raw.get("LatestDeliveryTime"),
        latest_notification_time=raw.get("LatestNotificationTime"),
        latest_cloud_watch_logs_delivery_time=raw.get("LatestCloudWatchLogsDeliveryTime"),
        start_logging_time=raw.get("StartLoggingTime"),
        stop_logging_time=raw.get("StopLoggingTime"),
        latest_delivery_error=raw.get("LatestDeliveryError"),
        latest_notification_error=raw.get("LatestNotificationError"),
        latest_digest_delivery_time=raw.get("LatestDigestDeliveryTime"),
        extra={k: v for k, v in raw.items() if k not in _STATUS_KNOWN_KEYS},
    )


def _parse_lookup_event(raw: dict[str, Any]) -> LookupEvent:
    """Parse a raw lookup event dict into a LookupEvent model."""
    return LookupEvent(
        event_id=raw.get("EventId", ""),
        event_name=raw.get("EventName"),
        event_source=raw.get("EventSource"),
        event_time=raw.get("EventTime"),
        username=raw.get("Username"),
        cloud_trail_event=raw.get("CloudTrailEvent"),
        resources=raw.get("Resources", []),
        extra={k: v for k, v in raw.items() if k not in _LOOKUP_KNOWN_KEYS},
    )


def _parse_event_data_store(
    raw: dict[str, Any],
) -> EventDataStoreResult:
    """Parse a raw event data store dict into an EventDataStoreResult."""
    return EventDataStoreResult(
        event_data_store_arn=raw.get("EventDataStoreArn", ""),
        name=raw.get("Name"),
        status=raw.get("Status"),
        retention_period=raw.get("RetentionPeriod"),
        multi_region_enabled=raw.get("MultiRegionEnabled", False),
        organization_enabled=raw.get("OrganizationEnabled", False),
        created_timestamp=raw.get("CreatedTimestamp"),
        updated_timestamp=raw.get("UpdatedTimestamp"),
        advanced_event_selectors=raw.get("AdvancedEventSelectors", []),
        extra={k: v for k, v in raw.items() if k not in _EDS_KNOWN_KEYS},
    )


# ---------------------------------------------------------------------------
# Trail CRUD
# ---------------------------------------------------------------------------


def create_trail(
    name: str,
    *,
    s3_bucket_name: str,
    s3_key_prefix: str | None = None,
    sns_topic_name: str | None = None,
    include_global_service_events: bool = True,
    is_multi_region_trail: bool = False,
    enable_log_file_validation: bool = False,
    cloud_watch_logs_log_group_arn: str | None = None,
    cloud_watch_logs_role_arn: str | None = None,
    kms_key_id: str | None = None,
    is_organization_trail: bool = False,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> TrailResult:
    """Create a new CloudTrail trail.

    Args:
        name: Trail name.
        s3_bucket_name: S3 bucket for log delivery.
        s3_key_prefix: Optional S3 key prefix.
        sns_topic_name: Optional SNS topic name for notifications.
        include_global_service_events: Include global events.
        is_multi_region_trail: Enable multi-region logging.
        enable_log_file_validation: Enable log file integrity
            validation.
        cloud_watch_logs_log_group_arn: CloudWatch Logs group ARN.
        cloud_watch_logs_role_arn: CloudWatch Logs role ARN.
        kms_key_id: KMS key ID for encryption.
        is_organization_trail: Enable organization trail.
        tags: Optional list of tag dicts with ``Key`` and ``Value``.
        region_name: AWS region override.

    Returns:
        A :class:`TrailResult` for the new trail.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "S3BucketName": s3_bucket_name,
        "IncludeGlobalServiceEvents": include_global_service_events,
        "IsMultiRegionTrail": is_multi_region_trail,
        "EnableLogFileValidation": enable_log_file_validation,
        "IsOrganizationTrail": is_organization_trail,
    }
    if s3_key_prefix is not None:
        kwargs["S3KeyPrefix"] = s3_key_prefix
    if sns_topic_name is not None:
        kwargs["SnsTopicName"] = sns_topic_name
    if cloud_watch_logs_log_group_arn is not None:
        kwargs["CloudWatchLogsLogGroupArn"] = cloud_watch_logs_log_group_arn
    if cloud_watch_logs_role_arn is not None:
        kwargs["CloudWatchLogsRoleArn"] = cloud_watch_logs_role_arn
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["TagsList"] = tags
    try:
        resp = client.create_trail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_trail failed for {name!r}") from exc
    return _parse_trail(resp)


def describe_trails(
    *,
    trail_name_list: list[str] | None = None,
    include_shadow_trails: bool = True,
    region_name: str | None = None,
) -> list[TrailResult]:
    """Describe one or more CloudTrail trails.

    Args:
        trail_name_list: Optional list of trail names or ARNs.
        include_shadow_trails: Include shadow trails (default True).
        region_name: AWS region override.

    Returns:
        A list of :class:`TrailResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {
        "includeShadowTrails": include_shadow_trails,
    }
    if trail_name_list is not None:
        kwargs["trailNameList"] = trail_name_list
    try:
        resp = client.describe_trails(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_trails failed") from exc
    return [_parse_trail(t) for t in resp.get("trailList", [])]


def get_trail(
    name: str,
    *,
    region_name: str | None = None,
) -> TrailResult:
    """Get details for a single CloudTrail trail.

    Args:
        name: Trail name or ARN.
        region_name: AWS region override.

    Returns:
        A :class:`TrailResult` for the trail.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.get_trail(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_trail failed for {name!r}") from exc
    return _parse_trail(resp.get("Trail", {}))


def update_trail(
    name: str,
    *,
    s3_bucket_name: str | None = None,
    s3_key_prefix: str | None = None,
    sns_topic_name: str | None = None,
    include_global_service_events: bool | None = None,
    is_multi_region_trail: bool | None = None,
    enable_log_file_validation: bool | None = None,
    cloud_watch_logs_log_group_arn: str | None = None,
    cloud_watch_logs_role_arn: str | None = None,
    kms_key_id: str | None = None,
    is_organization_trail: bool | None = None,
    region_name: str | None = None,
) -> TrailResult:
    """Update an existing CloudTrail trail.

    Args:
        name: Trail name or ARN.
        s3_bucket_name: New S3 bucket name.
        s3_key_prefix: New S3 key prefix.
        sns_topic_name: New SNS topic name.
        include_global_service_events: Include global events.
        is_multi_region_trail: Enable multi-region logging.
        enable_log_file_validation: Enable log file validation.
        cloud_watch_logs_log_group_arn: CloudWatch Logs group ARN.
        cloud_watch_logs_role_arn: CloudWatch Logs role ARN.
        kms_key_id: KMS key ID.
        is_organization_trail: Enable organization trail.
        region_name: AWS region override.

    Returns:
        A :class:`TrailResult` for the updated trail.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {"Name": name}
    if s3_bucket_name is not None:
        kwargs["S3BucketName"] = s3_bucket_name
    if s3_key_prefix is not None:
        kwargs["S3KeyPrefix"] = s3_key_prefix
    if sns_topic_name is not None:
        kwargs["SnsTopicName"] = sns_topic_name
    if include_global_service_events is not None:
        kwargs["IncludeGlobalServiceEvents"] = include_global_service_events
    if is_multi_region_trail is not None:
        kwargs["IsMultiRegionTrail"] = is_multi_region_trail
    if enable_log_file_validation is not None:
        kwargs["EnableLogFileValidation"] = enable_log_file_validation
    if cloud_watch_logs_log_group_arn is not None:
        kwargs["CloudWatchLogsLogGroupArn"] = cloud_watch_logs_log_group_arn
    if cloud_watch_logs_role_arn is not None:
        kwargs["CloudWatchLogsRoleArn"] = cloud_watch_logs_role_arn
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if is_organization_trail is not None:
        kwargs["IsOrganizationTrail"] = is_organization_trail
    try:
        resp = client.update_trail(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_trail failed for {name!r}") from exc
    return _parse_trail(resp)


def delete_trail(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CloudTrail trail.

    Args:
        name: Trail name or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        client.delete_trail(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_trail failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Logging control
# ---------------------------------------------------------------------------


def start_logging(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Start logging for a CloudTrail trail.

    Args:
        name: Trail name or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        client.start_logging(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"start_logging failed for {name!r}") from exc


def stop_logging(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Stop logging for a CloudTrail trail.

    Args:
        name: Trail name or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        client.stop_logging(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"stop_logging failed for {name!r}") from exc


def get_trail_status(
    name: str,
    *,
    region_name: str | None = None,
) -> TrailStatus:
    """Get the status of a CloudTrail trail.

    Args:
        name: Trail name or ARN.
        region_name: AWS region override.

    Returns:
        A :class:`TrailStatus` for the trail.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.get_trail_status(Name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_trail_status failed for {name!r}") from exc
    return _parse_status(resp)


# ---------------------------------------------------------------------------
# Event lookup
# ---------------------------------------------------------------------------


def lookup_events(
    *,
    lookup_attributes: list[dict[str, str]] | None = None,
    start_time: Any = None,
    end_time: Any = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[LookupEvent]:
    """Look up management and data events captured by CloudTrail.

    Args:
        lookup_attributes: List of lookup attribute dicts with
            ``AttributeKey`` and ``AttributeValue``.
        start_time: Start of the time range.
        end_time: End of the time range.
        max_results: Maximum number of events to return per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`LookupEvent` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if lookup_attributes is not None:
        kwargs["LookupAttributes"] = lookup_attributes
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[LookupEvent] = []
    try:
        paginator = client.get_paginator("lookup_events")
        for page in paginator.paginate(**kwargs):
            for event in page.get("Events", []):
                results.append(_parse_lookup_event(event))
    except ClientError as exc:
        raise wrap_aws_error(exc, "lookup_events failed") from exc
    return results


# ---------------------------------------------------------------------------
# List trails
# ---------------------------------------------------------------------------


def list_trails(
    *,
    region_name: str | None = None,
) -> list[TrailSummary]:
    """List all trails in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`TrailSummary` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    results: list[TrailSummary] = []
    try:
        paginator = client.get_paginator("list_trails")
        for page in paginator.paginate():
            for trail in page.get("Trails", []):
                results.append(
                    TrailSummary(
                        trail_arn=trail.get("TrailARN", ""),
                        name=trail.get("Name", ""),
                        home_region=trail.get("HomeRegion"),
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_trails failed") from exc
    return results


# ---------------------------------------------------------------------------
# Event Data Store operations
# ---------------------------------------------------------------------------


def create_event_data_store(
    name: str,
    *,
    retention_period: int | None = None,
    multi_region_enabled: bool = True,
    organization_enabled: bool = False,
    advanced_event_selectors: list[dict[str, Any]] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> EventDataStoreResult:
    """Create a CloudTrail Lake event data store.

    Args:
        name: Event data store name.
        retention_period: Retention period in days.
        multi_region_enabled: Enable multi-region collection.
        organization_enabled: Enable organization-wide collection.
        advanced_event_selectors: Advanced event selectors.
        tags: Optional list of tag dicts.
        region_name: AWS region override.

    Returns:
        An :class:`EventDataStoreResult` for the new store.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "MultiRegionEnabled": multi_region_enabled,
        "OrganizationEnabled": organization_enabled,
    }
    if retention_period is not None:
        kwargs["RetentionPeriod"] = retention_period
    if advanced_event_selectors is not None:
        kwargs["AdvancedEventSelectors"] = advanced_event_selectors
    if tags is not None:
        kwargs["TagsList"] = tags
    try:
        resp = client.create_event_data_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"create_event_data_store failed for {name!r}",
        ) from exc
    return _parse_event_data_store(resp)


def describe_event_data_store(
    event_data_store: str,
    *,
    region_name: str | None = None,
) -> EventDataStoreResult:
    """Describe a CloudTrail Lake event data store.

    Args:
        event_data_store: Event data store ARN or name.
        region_name: AWS region override.

    Returns:
        An :class:`EventDataStoreResult` for the store.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.describe_event_data_store(EventDataStore=event_data_store)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_event_data_store failed for {event_data_store!r}",
        ) from exc
    return _parse_event_data_store(resp)


def list_event_data_stores(
    *,
    region_name: str | None = None,
) -> list[EventDataStoreResult]:
    """List CloudTrail Lake event data stores.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`EventDataStoreResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    results: list[EventDataStoreResult] = []
    try:
        paginator = client.get_paginator("list_event_data_stores")
        for page in paginator.paginate():
            for eds in page.get("EventDataStores", []):
                results.append(_parse_event_data_store(eds))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_event_data_stores failed") from exc
    return results


def delete_event_data_store(
    event_data_store: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a CloudTrail Lake event data store.

    Args:
        event_data_store: Event data store ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        client.delete_event_data_store(EventDataStore=event_data_store)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"delete_event_data_store failed for {event_data_store!r}",
        ) from exc


# ---------------------------------------------------------------------------
# CloudTrail Lake queries
# ---------------------------------------------------------------------------


def start_query(
    query_statement: str,
    *,
    region_name: str | None = None,
) -> str:
    """Start a CloudTrail Lake query.

    Args:
        query_statement: SQL query statement.
        region_name: AWS region override.

    Returns:
        The query ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.start_query(QueryStatement=query_statement)
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_query failed") from exc
    return resp.get("QueryId", "")


def get_query_results(
    query_id: str,
    *,
    event_data_store: str | None = None,
    max_query_results: int | None = None,
    region_name: str | None = None,
) -> QueryResult:
    """Get the results of a CloudTrail Lake query.

    Args:
        query_id: The query ID returned by :func:`start_query`.
        event_data_store: Event data store ARN (optional).
        max_query_results: Max number of result rows.
        region_name: AWS region override.

    Returns:
        A :class:`QueryResult` with the query results.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {"QueryId": query_id}
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    if max_query_results is not None:
        kwargs["MaxQueryResults"] = max_query_results
    try:
        resp = client.get_query_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_query_results failed for {query_id!r}",
        ) from exc
    return QueryResult(
        query_id=query_id,
        query_status=resp.get("QueryStatus"),
        query_statistics=resp.get("QueryStatistics", {}),
        query_result_rows=resp.get("QueryResultRows", []),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "QueryStatus",
                "QueryStatistics",
                "QueryResultRows",
                "ResponseMetadata",
            }
        },
    )


def list_queries(
    event_data_store: str,
    *,
    start_time: Any = None,
    end_time: Any = None,
    query_status: str | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List queries for an event data store.

    Args:
        event_data_store: Event data store ARN.
        start_time: Start of the time range.
        end_time: End of the time range.
        query_status: Filter by query status.
        region_name: AWS region override.

    Returns:
        A list of query summary dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {
        "EventDataStore": event_data_store,
    }
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if query_status is not None:
        kwargs["QueryStatus"] = query_status
    results: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("list_queries")
        for page in paginator.paginate(**kwargs):
            results.extend(page.get("Queries", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_queries failed") from exc
    return results


# ---------------------------------------------------------------------------
# Event selectors
# ---------------------------------------------------------------------------


def put_event_selectors(
    trail_name: str,
    *,
    event_selectors: list[dict[str, Any]] | None = None,
    advanced_event_selectors: (list[dict[str, Any]] | None) = None,
    region_name: str | None = None,
) -> EventSelectorResult:
    """Put event selectors on a trail.

    Args:
        trail_name: Trail name or ARN.
        event_selectors: Classic event selectors.
        advanced_event_selectors: Advanced event selectors.
        region_name: AWS region override.

    Returns:
        An :class:`EventSelectorResult` with the applied selectors.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {"TrailName": trail_name}
    if event_selectors is not None:
        kwargs["EventSelectors"] = event_selectors
    if advanced_event_selectors is not None:
        kwargs["AdvancedEventSelectors"] = advanced_event_selectors
    try:
        resp = client.put_event_selectors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"put_event_selectors failed for {trail_name!r}",
        ) from exc
    return EventSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        event_selectors=resp.get("EventSelectors", []),
        advanced_event_selectors=resp.get("AdvancedEventSelectors", []),
    )


def get_event_selectors(
    trail_name: str,
    *,
    region_name: str | None = None,
) -> EventSelectorResult:
    """Get event selectors for a trail.

    Args:
        trail_name: Trail name or ARN.
        region_name: AWS region override.

    Returns:
        An :class:`EventSelectorResult` with the current selectors.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.get_event_selectors(TrailName=trail_name)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_event_selectors failed for {trail_name!r}",
        ) from exc
    return EventSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        event_selectors=resp.get("EventSelectors", []),
        advanced_event_selectors=resp.get("AdvancedEventSelectors", []),
    )


# ---------------------------------------------------------------------------
# Insight selectors
# ---------------------------------------------------------------------------


def put_insight_selectors(
    trail_name: str,
    *,
    insight_selectors: list[dict[str, Any]],
    region_name: str | None = None,
) -> InsightSelectorResult:
    """Put insight selectors on a trail.

    Args:
        trail_name: Trail name or ARN.
        insight_selectors: Insight selector list.
        region_name: AWS region override.

    Returns:
        An :class:`InsightSelectorResult` with the applied selectors.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.put_insight_selectors(
            TrailName=trail_name,
            InsightSelectors=insight_selectors,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"put_insight_selectors failed for {trail_name!r}",
        ) from exc
    return InsightSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        insight_selectors=resp.get("InsightSelectors", []),
    )


def get_insight_selectors(
    trail_name: str,
    *,
    region_name: str | None = None,
) -> InsightSelectorResult:
    """Get insight selectors for a trail.

    Args:
        trail_name: Trail name or ARN.
        region_name: AWS region override.

    Returns:
        An :class:`InsightSelectorResult` with the current selectors.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    try:
        resp = client.get_insight_selectors(TrailName=trail_name)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_insight_selectors failed for {trail_name!r}",
        ) from exc
    return InsightSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        insight_selectors=resp.get("InsightSelectors", []),
    )


class CancelQueryResult(BaseModel):
    """Result of cancel_query."""

    model_config = ConfigDict(frozen=True)

    query_id: str | None = None
    query_status: str | None = None
    event_data_store_owner_account_id: str | None = None


class CreateChannelResult(BaseModel):
    """Result of create_channel."""

    model_config = ConfigDict(frozen=True)

    channel_arn: str | None = None
    name: str | None = None
    source: str | None = None
    destinations: list[dict[str, Any]] | None = None
    tags: list[dict[str, Any]] | None = None


class CreateDashboardResult(BaseModel):
    """Result of create_dashboard."""

    model_config = ConfigDict(frozen=True)

    dashboard_arn: str | None = None
    name: str | None = None
    type_value: str | None = None
    widgets: list[dict[str, Any]] | None = None
    tags_list: list[dict[str, Any]] | None = None
    refresh_schedule: dict[str, Any] | None = None
    termination_protection_enabled: bool | None = None


class DescribeQueryResult(BaseModel):
    """Result of describe_query."""

    model_config = ConfigDict(frozen=True)

    query_id: str | None = None
    query_string: str | None = None
    query_status: str | None = None
    query_statistics: dict[str, Any] | None = None
    error_message: str | None = None
    delivery_s3_uri: str | None = None
    delivery_status: str | None = None
    prompt: str | None = None
    event_data_store_owner_account_id: str | None = None


class DisableFederationResult(BaseModel):
    """Result of disable_federation."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    federation_status: str | None = None


class EnableFederationResult(BaseModel):
    """Result of enable_federation."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    federation_status: str | None = None
    federation_role_arn: str | None = None


class GenerateQueryResult(BaseModel):
    """Result of generate_query."""

    model_config = ConfigDict(frozen=True)

    query_statement: str | None = None
    query_alias: str | None = None
    event_data_store_owner_account_id: str | None = None


class GetChannelResult(BaseModel):
    """Result of get_channel."""

    model_config = ConfigDict(frozen=True)

    channel_arn: str | None = None
    name: str | None = None
    source: str | None = None
    source_config: dict[str, Any] | None = None
    destinations: list[dict[str, Any]] | None = None
    ingestion_status: dict[str, Any] | None = None


class GetDashboardResult(BaseModel):
    """Result of get_dashboard."""

    model_config = ConfigDict(frozen=True)

    dashboard_arn: str | None = None
    type_value: str | None = None
    status: str | None = None
    widgets: list[dict[str, Any]] | None = None
    refresh_schedule: dict[str, Any] | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None
    last_refresh_id: str | None = None
    last_refresh_failure_reason: str | None = None
    termination_protection_enabled: bool | None = None


class GetEventConfigurationResult(BaseModel):
    """Result of get_event_configuration."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    max_event_size: str | None = None
    context_key_selectors: list[dict[str, Any]] | None = None


class GetEventDataStoreResult(BaseModel):
    """Result of get_event_data_store."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    name: str | None = None
    status: str | None = None
    advanced_event_selectors: list[dict[str, Any]] | None = None
    multi_region_enabled: bool | None = None
    organization_enabled: bool | None = None
    retention_period: int | None = None
    termination_protection_enabled: bool | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None
    kms_key_id: str | None = None
    billing_mode: str | None = None
    federation_status: str | None = None
    federation_role_arn: str | None = None
    partition_keys: list[dict[str, Any]] | None = None


class GetImportResult(BaseModel):
    """Result of get_import."""

    model_config = ConfigDict(frozen=True)

    import_id: str | None = None
    destinations: list[str] | None = None
    import_source: dict[str, Any] | None = None
    start_event_time: str | None = None
    end_event_time: str | None = None
    import_status: str | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None
    import_statistics: dict[str, Any] | None = None


class GetResourcePolicyResult(BaseModel):
    """Result of get_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    resource_policy: str | None = None
    delegated_admin_resource_policy: str | None = None


class ListChannelsResult(BaseModel):
    """Result of list_channels."""

    model_config = ConfigDict(frozen=True)

    channels: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDashboardsResult(BaseModel):
    """Result of list_dashboards."""

    model_config = ConfigDict(frozen=True)

    dashboards: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListImportFailuresResult(BaseModel):
    """Result of list_import_failures."""

    model_config = ConfigDict(frozen=True)

    failures: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListImportsResult(BaseModel):
    """Result of list_imports."""

    model_config = ConfigDict(frozen=True)

    imports: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInsightsMetricDataResult(BaseModel):
    """Result of list_insights_metric_data."""

    model_config = ConfigDict(frozen=True)

    event_source: str | None = None
    event_name: str | None = None
    insight_type: str | None = None
    error_code: str | None = None
    timestamps: list[str] | None = None
    values: list[float] | None = None
    next_token: str | None = None


class ListPublicKeysResult(BaseModel):
    """Result of list_public_keys."""

    model_config = ConfigDict(frozen=True)

    public_key_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsResult(BaseModel):
    """Result of list_tags."""

    model_config = ConfigDict(frozen=True)

    resource_tag_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutEventConfigurationResult(BaseModel):
    """Result of put_event_configuration."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    max_event_size: str | None = None
    context_key_selectors: list[dict[str, Any]] | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None
    resource_policy: str | None = None
    delegated_admin_resource_policy: str | None = None


class RestoreEventDataStoreResult(BaseModel):
    """Result of restore_event_data_store."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    name: str | None = None
    status: str | None = None
    advanced_event_selectors: list[dict[str, Any]] | None = None
    multi_region_enabled: bool | None = None
    organization_enabled: bool | None = None
    retention_period: int | None = None
    termination_protection_enabled: bool | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None
    kms_key_id: str | None = None
    billing_mode: str | None = None


class SearchSampleQueriesResult(BaseModel):
    """Result of search_sample_queries."""

    model_config = ConfigDict(frozen=True)

    search_results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class StartDashboardRefreshResult(BaseModel):
    """Result of start_dashboard_refresh."""

    model_config = ConfigDict(frozen=True)

    refresh_id: str | None = None


class StartImportResult(BaseModel):
    """Result of start_import."""

    model_config = ConfigDict(frozen=True)

    import_id: str | None = None
    destinations: list[str] | None = None
    import_source: dict[str, Any] | None = None
    start_event_time: str | None = None
    end_event_time: str | None = None
    import_status: str | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None


class StopImportResult(BaseModel):
    """Result of stop_import."""

    model_config = ConfigDict(frozen=True)

    import_id: str | None = None
    import_source: dict[str, Any] | None = None
    destinations: list[str] | None = None
    import_status: str | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None
    start_event_time: str | None = None
    end_event_time: str | None = None
    import_statistics: dict[str, Any] | None = None


class UpdateChannelResult(BaseModel):
    """Result of update_channel."""

    model_config = ConfigDict(frozen=True)

    channel_arn: str | None = None
    name: str | None = None
    source: str | None = None
    destinations: list[dict[str, Any]] | None = None


class UpdateDashboardResult(BaseModel):
    """Result of update_dashboard."""

    model_config = ConfigDict(frozen=True)

    dashboard_arn: str | None = None
    name: str | None = None
    type_value: str | None = None
    widgets: list[dict[str, Any]] | None = None
    refresh_schedule: dict[str, Any] | None = None
    termination_protection_enabled: bool | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None


class UpdateEventDataStoreResult(BaseModel):
    """Result of update_event_data_store."""

    model_config = ConfigDict(frozen=True)

    event_data_store_arn: str | None = None
    name: str | None = None
    status: str | None = None
    advanced_event_selectors: list[dict[str, Any]] | None = None
    multi_region_enabled: bool | None = None
    organization_enabled: bool | None = None
    retention_period: int | None = None
    termination_protection_enabled: bool | None = None
    created_timestamp: str | None = None
    updated_timestamp: str | None = None
    kms_key_id: str | None = None
    billing_mode: str | None = None
    federation_status: str | None = None
    federation_role_arn: str | None = None


def add_tags(
    resource_id: str,
    tags_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Add tags.

    Args:
        resource_id: Resource id.
        tags_list: Tags list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagsList"] = tags_list
    try:
        client.add_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to add tags") from exc
    return None


def cancel_query(
    query_id: str,
    *,
    event_data_store: str | None = None,
    event_data_store_owner_account_id: str | None = None,
    region_name: str | None = None,
) -> CancelQueryResult:
    """Cancel query.

    Args:
        query_id: Query id.
        event_data_store: Event data store.
        event_data_store_owner_account_id: Event data store owner account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryId"] = query_id
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    if event_data_store_owner_account_id is not None:
        kwargs["EventDataStoreOwnerAccountId"] = event_data_store_owner_account_id
    try:
        resp = client.cancel_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel query") from exc
    return CancelQueryResult(
        query_id=resp.get("QueryId"),
        query_status=resp.get("QueryStatus"),
        event_data_store_owner_account_id=resp.get("EventDataStoreOwnerAccountId"),
    )


def create_channel(
    name: str,
    source: str,
    destinations: list[dict[str, Any]],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateChannelResult:
    """Create channel.

    Args:
        name: Name.
        source: Source.
        destinations: Destinations.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Source"] = source
    kwargs["Destinations"] = destinations
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create channel") from exc
    return CreateChannelResult(
        channel_arn=resp.get("ChannelArn"),
        name=resp.get("Name"),
        source=resp.get("Source"),
        destinations=resp.get("Destinations"),
        tags=resp.get("Tags"),
    )


def create_dashboard(
    name: str,
    *,
    refresh_schedule: dict[str, Any] | None = None,
    tags_list: list[dict[str, Any]] | None = None,
    termination_protection_enabled: bool | None = None,
    widgets: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDashboardResult:
    """Create dashboard.

    Args:
        name: Name.
        refresh_schedule: Refresh schedule.
        tags_list: Tags list.
        termination_protection_enabled: Termination protection enabled.
        widgets: Widgets.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if refresh_schedule is not None:
        kwargs["RefreshSchedule"] = refresh_schedule
    if tags_list is not None:
        kwargs["TagsList"] = tags_list
    if termination_protection_enabled is not None:
        kwargs["TerminationProtectionEnabled"] = termination_protection_enabled
    if widgets is not None:
        kwargs["Widgets"] = widgets
    try:
        resp = client.create_dashboard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create dashboard") from exc
    return CreateDashboardResult(
        dashboard_arn=resp.get("DashboardArn"),
        name=resp.get("Name"),
        type_value=resp.get("Type"),
        widgets=resp.get("Widgets"),
        tags_list=resp.get("TagsList"),
        refresh_schedule=resp.get("RefreshSchedule"),
        termination_protection_enabled=resp.get("TerminationProtectionEnabled"),
    )


def delete_channel(
    channel: str,
    region_name: str | None = None,
) -> None:
    """Delete channel.

    Args:
        channel: Channel.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Channel"] = channel
    try:
        client.delete_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete channel") from exc
    return None


def delete_dashboard(
    dashboard_id: str,
    region_name: str | None = None,
) -> None:
    """Delete dashboard.

    Args:
        dashboard_id: Dashboard id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    try:
        client.delete_dashboard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete dashboard") from exc
    return None


def delete_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


def deregister_organization_delegated_admin(
    delegated_admin_account_id: str,
    region_name: str | None = None,
) -> None:
    """Deregister organization delegated admin.

    Args:
        delegated_admin_account_id: Delegated admin account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DelegatedAdminAccountId"] = delegated_admin_account_id
    try:
        client.deregister_organization_delegated_admin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister organization delegated admin") from exc
    return None


def describe_query(
    *,
    event_data_store: str | None = None,
    query_id: str | None = None,
    query_alias: str | None = None,
    refresh_id: str | None = None,
    event_data_store_owner_account_id: str | None = None,
    region_name: str | None = None,
) -> DescribeQueryResult:
    """Describe query.

    Args:
        event_data_store: Event data store.
        query_id: Query id.
        query_alias: Query alias.
        refresh_id: Refresh id.
        event_data_store_owner_account_id: Event data store owner account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    if query_id is not None:
        kwargs["QueryId"] = query_id
    if query_alias is not None:
        kwargs["QueryAlias"] = query_alias
    if refresh_id is not None:
        kwargs["RefreshId"] = refresh_id
    if event_data_store_owner_account_id is not None:
        kwargs["EventDataStoreOwnerAccountId"] = event_data_store_owner_account_id
    try:
        resp = client.describe_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe query") from exc
    return DescribeQueryResult(
        query_id=resp.get("QueryId"),
        query_string=resp.get("QueryString"),
        query_status=resp.get("QueryStatus"),
        query_statistics=resp.get("QueryStatistics"),
        error_message=resp.get("ErrorMessage"),
        delivery_s3_uri=resp.get("DeliveryS3Uri"),
        delivery_status=resp.get("DeliveryStatus"),
        prompt=resp.get("Prompt"),
        event_data_store_owner_account_id=resp.get("EventDataStoreOwnerAccountId"),
    )


def disable_federation(
    event_data_store: str,
    region_name: str | None = None,
) -> DisableFederationResult:
    """Disable federation.

    Args:
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        resp = client.disable_federation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable federation") from exc
    return DisableFederationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        federation_status=resp.get("FederationStatus"),
    )


def enable_federation(
    event_data_store: str,
    federation_role_arn: str,
    region_name: str | None = None,
) -> EnableFederationResult:
    """Enable federation.

    Args:
        event_data_store: Event data store.
        federation_role_arn: Federation role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    kwargs["FederationRoleArn"] = federation_role_arn
    try:
        resp = client.enable_federation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable federation") from exc
    return EnableFederationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        federation_status=resp.get("FederationStatus"),
        federation_role_arn=resp.get("FederationRoleArn"),
    )


def generate_query(
    event_data_stores: list[str],
    prompt: str,
    region_name: str | None = None,
) -> GenerateQueryResult:
    """Generate query.

    Args:
        event_data_stores: Event data stores.
        prompt: Prompt.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStores"] = event_data_stores
    kwargs["Prompt"] = prompt
    try:
        resp = client.generate_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to generate query") from exc
    return GenerateQueryResult(
        query_statement=resp.get("QueryStatement"),
        query_alias=resp.get("QueryAlias"),
        event_data_store_owner_account_id=resp.get("EventDataStoreOwnerAccountId"),
    )


def get_channel(
    channel: str,
    region_name: str | None = None,
) -> GetChannelResult:
    """Get channel.

    Args:
        channel: Channel.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Channel"] = channel
    try:
        resp = client.get_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get channel") from exc
    return GetChannelResult(
        channel_arn=resp.get("ChannelArn"),
        name=resp.get("Name"),
        source=resp.get("Source"),
        source_config=resp.get("SourceConfig"),
        destinations=resp.get("Destinations"),
        ingestion_status=resp.get("IngestionStatus"),
    )


def get_dashboard(
    dashboard_id: str,
    region_name: str | None = None,
) -> GetDashboardResult:
    """Get dashboard.

    Args:
        dashboard_id: Dashboard id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    try:
        resp = client.get_dashboard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get dashboard") from exc
    return GetDashboardResult(
        dashboard_arn=resp.get("DashboardArn"),
        type_value=resp.get("Type"),
        status=resp.get("Status"),
        widgets=resp.get("Widgets"),
        refresh_schedule=resp.get("RefreshSchedule"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
        last_refresh_id=resp.get("LastRefreshId"),
        last_refresh_failure_reason=resp.get("LastRefreshFailureReason"),
        termination_protection_enabled=resp.get("TerminationProtectionEnabled"),
    )


def get_event_configuration(
    *,
    event_data_store: str | None = None,
    region_name: str | None = None,
) -> GetEventConfigurationResult:
    """Get event configuration.

    Args:
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    try:
        resp = client.get_event_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get event configuration") from exc
    return GetEventConfigurationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        max_event_size=resp.get("MaxEventSize"),
        context_key_selectors=resp.get("ContextKeySelectors"),
    )


def get_event_data_store(
    event_data_store: str,
    region_name: str | None = None,
) -> GetEventDataStoreResult:
    """Get event data store.

    Args:
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        resp = client.get_event_data_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get event data store") from exc
    return GetEventDataStoreResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        name=resp.get("Name"),
        status=resp.get("Status"),
        advanced_event_selectors=resp.get("AdvancedEventSelectors"),
        multi_region_enabled=resp.get("MultiRegionEnabled"),
        organization_enabled=resp.get("OrganizationEnabled"),
        retention_period=resp.get("RetentionPeriod"),
        termination_protection_enabled=resp.get("TerminationProtectionEnabled"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
        kms_key_id=resp.get("KmsKeyId"),
        billing_mode=resp.get("BillingMode"),
        federation_status=resp.get("FederationStatus"),
        federation_role_arn=resp.get("FederationRoleArn"),
        partition_keys=resp.get("PartitionKeys"),
    )


def get_import(
    import_id: str,
    region_name: str | None = None,
) -> GetImportResult:
    """Get import.

    Args:
        import_id: Import id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportId"] = import_id
    try:
        resp = client.get_import(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get import") from exc
    return GetImportResult(
        import_id=resp.get("ImportId"),
        destinations=resp.get("Destinations"),
        import_source=resp.get("ImportSource"),
        start_event_time=resp.get("StartEventTime"),
        end_event_time=resp.get("EndEventTime"),
        import_status=resp.get("ImportStatus"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
        import_statistics=resp.get("ImportStatistics"),
    )


def get_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.get_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
        resource_policy=resp.get("ResourcePolicy"),
        delegated_admin_resource_policy=resp.get("DelegatedAdminResourcePolicy"),
    )


def list_channels(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListChannelsResult:
    """List channels.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_channels(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list channels") from exc
    return ListChannelsResult(
        channels=resp.get("Channels"),
        next_token=resp.get("NextToken"),
    )


def list_dashboards(
    *,
    name_prefix: str | None = None,
    type_value: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDashboardsResult:
    """List dashboards.

    Args:
        name_prefix: Name prefix.
        type_value: Type value.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if name_prefix is not None:
        kwargs["NamePrefix"] = name_prefix
    if type_value is not None:
        kwargs["Type"] = type_value
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_dashboards(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list dashboards") from exc
    return ListDashboardsResult(
        dashboards=resp.get("Dashboards"),
        next_token=resp.get("NextToken"),
    )


def list_import_failures(
    import_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListImportFailuresResult:
    """List import failures.

    Args:
        import_id: Import id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportId"] = import_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_import_failures(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list import failures") from exc
    return ListImportFailuresResult(
        failures=resp.get("Failures"),
        next_token=resp.get("NextToken"),
    )


def list_imports(
    *,
    max_results: int | None = None,
    destination: str | None = None,
    import_status: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListImportsResult:
    """List imports.

    Args:
        max_results: Max results.
        destination: Destination.
        import_status: Import status.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if destination is not None:
        kwargs["Destination"] = destination
    if import_status is not None:
        kwargs["ImportStatus"] = import_status
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_imports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list imports") from exc
    return ListImportsResult(
        imports=resp.get("Imports"),
        next_token=resp.get("NextToken"),
    )


def list_insights_metric_data(
    event_source: str,
    event_name: str,
    insight_type: str,
    *,
    error_code: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    period: int | None = None,
    data_type: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListInsightsMetricDataResult:
    """List insights metric data.

    Args:
        event_source: Event source.
        event_name: Event name.
        insight_type: Insight type.
        error_code: Error code.
        start_time: Start time.
        end_time: End time.
        period: Period.
        data_type: Data type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventSource"] = event_source
    kwargs["EventName"] = event_name
    kwargs["InsightType"] = insight_type
    if error_code is not None:
        kwargs["ErrorCode"] = error_code
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if period is not None:
        kwargs["Period"] = period
    if data_type is not None:
        kwargs["DataType"] = data_type
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_insights_metric_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list insights metric data") from exc
    return ListInsightsMetricDataResult(
        event_source=resp.get("EventSource"),
        event_name=resp.get("EventName"),
        insight_type=resp.get("InsightType"),
        error_code=resp.get("ErrorCode"),
        timestamps=resp.get("Timestamps"),
        values=resp.get("Values"),
        next_token=resp.get("NextToken"),
    )


def list_public_keys(
    *,
    start_time: str | None = None,
    end_time: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPublicKeysResult:
    """List public keys.

    Args:
        start_time: Start time.
        end_time: End time.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_public_keys(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list public keys") from exc
    return ListPublicKeysResult(
        public_key_list=resp.get("PublicKeyList"),
        next_token=resp.get("NextToken"),
    )


def list_tags(
    resource_id_list: list[str],
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsResult:
    """List tags.

    Args:
        resource_id_list: Resource id list.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceIdList"] = resource_id_list
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags") from exc
    return ListTagsResult(
        resource_tag_list=resp.get("ResourceTagList"),
        next_token=resp.get("NextToken"),
    )


def put_event_configuration(
    max_event_size: str,
    context_key_selectors: list[dict[str, Any]],
    *,
    event_data_store: str | None = None,
    region_name: str | None = None,
) -> PutEventConfigurationResult:
    """Put event configuration.

    Args:
        max_event_size: Max event size.
        context_key_selectors: Context key selectors.
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MaxEventSize"] = max_event_size
    kwargs["ContextKeySelectors"] = context_key_selectors
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    try:
        resp = client.put_event_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put event configuration") from exc
    return PutEventConfigurationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        max_event_size=resp.get("MaxEventSize"),
        context_key_selectors=resp.get("ContextKeySelectors"),
    )


def put_resource_policy(
    resource_arn: str,
    resource_policy: str,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        resource_policy: Resource policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["ResourcePolicy"] = resource_policy
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
        resource_policy=resp.get("ResourcePolicy"),
        delegated_admin_resource_policy=resp.get("DelegatedAdminResourcePolicy"),
    )


def register_organization_delegated_admin(
    member_account_id: str,
    region_name: str | None = None,
) -> None:
    """Register organization delegated admin.

    Args:
        member_account_id: Member account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberAccountId"] = member_account_id
    try:
        client.register_organization_delegated_admin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register organization delegated admin") from exc
    return None


def remove_tags(
    resource_id: str,
    tags_list: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Remove tags.

    Args:
        resource_id: Resource id.
        tags_list: Tags list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagsList"] = tags_list
    try:
        client.remove_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to remove tags") from exc
    return None


def restore_event_data_store(
    event_data_store: str,
    region_name: str | None = None,
) -> RestoreEventDataStoreResult:
    """Restore event data store.

    Args:
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        resp = client.restore_event_data_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore event data store") from exc
    return RestoreEventDataStoreResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        name=resp.get("Name"),
        status=resp.get("Status"),
        advanced_event_selectors=resp.get("AdvancedEventSelectors"),
        multi_region_enabled=resp.get("MultiRegionEnabled"),
        organization_enabled=resp.get("OrganizationEnabled"),
        retention_period=resp.get("RetentionPeriod"),
        termination_protection_enabled=resp.get("TerminationProtectionEnabled"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
        kms_key_id=resp.get("KmsKeyId"),
        billing_mode=resp.get("BillingMode"),
    )


def search_sample_queries(
    search_phrase: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> SearchSampleQueriesResult:
    """Search sample queries.

    Args:
        search_phrase: Search phrase.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SearchPhrase"] = search_phrase
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.search_sample_queries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search sample queries") from exc
    return SearchSampleQueriesResult(
        search_results=resp.get("SearchResults"),
        next_token=resp.get("NextToken"),
    )


def start_dashboard_refresh(
    dashboard_id: str,
    *,
    query_parameter_values: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartDashboardRefreshResult:
    """Start dashboard refresh.

    Args:
        dashboard_id: Dashboard id.
        query_parameter_values: Query parameter values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    if query_parameter_values is not None:
        kwargs["QueryParameterValues"] = query_parameter_values
    try:
        resp = client.start_dashboard_refresh(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start dashboard refresh") from exc
    return StartDashboardRefreshResult(
        refresh_id=resp.get("RefreshId"),
    )


def start_event_data_store_ingestion(
    event_data_store: str,
    region_name: str | None = None,
) -> None:
    """Start event data store ingestion.

    Args:
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        client.start_event_data_store_ingestion(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start event data store ingestion") from exc
    return None


def start_import(
    *,
    destinations: list[str] | None = None,
    import_source: dict[str, Any] | None = None,
    start_event_time: str | None = None,
    end_event_time: str | None = None,
    import_id: str | None = None,
    region_name: str | None = None,
) -> StartImportResult:
    """Start import.

    Args:
        destinations: Destinations.
        import_source: Import source.
        start_event_time: Start event time.
        end_event_time: End event time.
        import_id: Import id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if destinations is not None:
        kwargs["Destinations"] = destinations
    if import_source is not None:
        kwargs["ImportSource"] = import_source
    if start_event_time is not None:
        kwargs["StartEventTime"] = start_event_time
    if end_event_time is not None:
        kwargs["EndEventTime"] = end_event_time
    if import_id is not None:
        kwargs["ImportId"] = import_id
    try:
        resp = client.start_import(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start import") from exc
    return StartImportResult(
        import_id=resp.get("ImportId"),
        destinations=resp.get("Destinations"),
        import_source=resp.get("ImportSource"),
        start_event_time=resp.get("StartEventTime"),
        end_event_time=resp.get("EndEventTime"),
        import_status=resp.get("ImportStatus"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
    )


def stop_event_data_store_ingestion(
    event_data_store: str,
    region_name: str | None = None,
) -> None:
    """Stop event data store ingestion.

    Args:
        event_data_store: Event data store.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        client.stop_event_data_store_ingestion(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop event data store ingestion") from exc
    return None


def stop_import(
    import_id: str,
    region_name: str | None = None,
) -> StopImportResult:
    """Stop import.

    Args:
        import_id: Import id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportId"] = import_id
    try:
        resp = client.stop_import(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop import") from exc
    return StopImportResult(
        import_id=resp.get("ImportId"),
        import_source=resp.get("ImportSource"),
        destinations=resp.get("Destinations"),
        import_status=resp.get("ImportStatus"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
        start_event_time=resp.get("StartEventTime"),
        end_event_time=resp.get("EndEventTime"),
        import_statistics=resp.get("ImportStatistics"),
    )


def update_channel(
    channel: str,
    *,
    destinations: list[dict[str, Any]] | None = None,
    name: str | None = None,
    region_name: str | None = None,
) -> UpdateChannelResult:
    """Update channel.

    Args:
        channel: Channel.
        destinations: Destinations.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Channel"] = channel
    if destinations is not None:
        kwargs["Destinations"] = destinations
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = client.update_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update channel") from exc
    return UpdateChannelResult(
        channel_arn=resp.get("ChannelArn"),
        name=resp.get("Name"),
        source=resp.get("Source"),
        destinations=resp.get("Destinations"),
    )


def update_dashboard(
    dashboard_id: str,
    *,
    widgets: list[dict[str, Any]] | None = None,
    refresh_schedule: dict[str, Any] | None = None,
    termination_protection_enabled: bool | None = None,
    region_name: str | None = None,
) -> UpdateDashboardResult:
    """Update dashboard.

    Args:
        dashboard_id: Dashboard id.
        widgets: Widgets.
        refresh_schedule: Refresh schedule.
        termination_protection_enabled: Termination protection enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    if widgets is not None:
        kwargs["Widgets"] = widgets
    if refresh_schedule is not None:
        kwargs["RefreshSchedule"] = refresh_schedule
    if termination_protection_enabled is not None:
        kwargs["TerminationProtectionEnabled"] = termination_protection_enabled
    try:
        resp = client.update_dashboard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update dashboard") from exc
    return UpdateDashboardResult(
        dashboard_arn=resp.get("DashboardArn"),
        name=resp.get("Name"),
        type_value=resp.get("Type"),
        widgets=resp.get("Widgets"),
        refresh_schedule=resp.get("RefreshSchedule"),
        termination_protection_enabled=resp.get("TerminationProtectionEnabled"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
    )


def update_event_data_store(
    event_data_store: str,
    *,
    name: str | None = None,
    advanced_event_selectors: list[dict[str, Any]] | None = None,
    multi_region_enabled: bool | None = None,
    organization_enabled: bool | None = None,
    retention_period: int | None = None,
    termination_protection_enabled: bool | None = None,
    kms_key_id: str | None = None,
    billing_mode: str | None = None,
    region_name: str | None = None,
) -> UpdateEventDataStoreResult:
    """Update event data store.

    Args:
        event_data_store: Event data store.
        name: Name.
        advanced_event_selectors: Advanced event selectors.
        multi_region_enabled: Multi region enabled.
        organization_enabled: Organization enabled.
        retention_period: Retention period.
        termination_protection_enabled: Termination protection enabled.
        kms_key_id: Kms key id.
        billing_mode: Billing mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    if name is not None:
        kwargs["Name"] = name
    if advanced_event_selectors is not None:
        kwargs["AdvancedEventSelectors"] = advanced_event_selectors
    if multi_region_enabled is not None:
        kwargs["MultiRegionEnabled"] = multi_region_enabled
    if organization_enabled is not None:
        kwargs["OrganizationEnabled"] = organization_enabled
    if retention_period is not None:
        kwargs["RetentionPeriod"] = retention_period
    if termination_protection_enabled is not None:
        kwargs["TerminationProtectionEnabled"] = termination_protection_enabled
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if billing_mode is not None:
        kwargs["BillingMode"] = billing_mode
    try:
        resp = client.update_event_data_store(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update event data store") from exc
    return UpdateEventDataStoreResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        name=resp.get("Name"),
        status=resp.get("Status"),
        advanced_event_selectors=resp.get("AdvancedEventSelectors"),
        multi_region_enabled=resp.get("MultiRegionEnabled"),
        organization_enabled=resp.get("OrganizationEnabled"),
        retention_period=resp.get("RetentionPeriod"),
        termination_protection_enabled=resp.get("TerminationProtectionEnabled"),
        created_timestamp=resp.get("CreatedTimestamp"),
        updated_timestamp=resp.get("UpdatedTimestamp"),
        kms_key_id=resp.get("KmsKeyId"),
        billing_mode=resp.get("BillingMode"),
        federation_status=resp.get("FederationStatus"),
        federation_role_arn=resp.get("FederationRoleArn"),
    )
