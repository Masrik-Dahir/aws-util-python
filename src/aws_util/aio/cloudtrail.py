"""Native async CloudTrail utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.cloudtrail import (
    CancelQueryResult,
    CreateChannelResult,
    CreateDashboardResult,
    DescribeQueryResult,
    DisableFederationResult,
    EnableFederationResult,
    EventDataStoreResult,
    EventSelectorResult,
    GenerateQueryResult,
    GetChannelResult,
    GetDashboardResult,
    GetEventConfigurationResult,
    GetEventDataStoreResult,
    GetImportResult,
    GetResourcePolicyResult,
    InsightSelectorResult,
    ListChannelsResult,
    ListDashboardsResult,
    ListImportFailuresResult,
    ListImportsResult,
    ListInsightsMetricDataResult,
    ListPublicKeysResult,
    ListTagsResult,
    LookupEvent,
    PutEventConfigurationResult,
    PutResourcePolicyResult,
    QueryResult,
    RestoreEventDataStoreResult,
    SearchSampleQueriesResult,
    StartDashboardRefreshResult,
    StartImportResult,
    StopImportResult,
    TrailResult,
    TrailStatus,
    TrailSummary,
    UpdateChannelResult,
    UpdateDashboardResult,
    UpdateEventDataStoreResult,
    _parse_event_data_store,
    _parse_lookup_event,
    _parse_status,
    _parse_trail,
)
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
# Trail CRUD
# ---------------------------------------------------------------------------


async def create_trail(
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
        sns_topic_name: Optional SNS topic name.
        include_global_service_events: Include global events.
        is_multi_region_trail: Enable multi-region logging.
        enable_log_file_validation: Enable log file validation.
        cloud_watch_logs_log_group_arn: CloudWatch Logs group ARN.
        cloud_watch_logs_role_arn: CloudWatch Logs role ARN.
        kms_key_id: KMS key ID for encryption.
        is_organization_trail: Enable organization trail.
        tags: Optional list of tag dicts.
        region_name: AWS region override.

    Returns:
        A :class:`TrailResult` for the new trail.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("CreateTrail", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_trail failed for {name!r}") from exc
    return _parse_trail(resp)


async def describe_trails(
    *,
    trail_name_list: list[str] | None = None,
    include_shadow_trails: bool = True,
    region_name: str | None = None,
) -> list[TrailResult]:
    """Describe one or more CloudTrail trails.

    Args:
        trail_name_list: Optional list of trail names or ARNs.
        include_shadow_trails: Include shadow trails.
        region_name: AWS region override.

    Returns:
        A list of :class:`TrailResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {
        "includeShadowTrails": include_shadow_trails,
    }
    if trail_name_list is not None:
        kwargs["trailNameList"] = trail_name_list
    try:
        resp = await client.call("DescribeTrails", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_trails failed") from exc
    return [_parse_trail(t) for t in resp.get("trailList", [])]


async def get_trail(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call("GetTrail", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_trail failed for {name!r}") from exc
    return _parse_trail(resp.get("Trail", {}))


async def update_trail(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("UpdateTrail", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_trail failed for {name!r}") from exc
    return _parse_trail(resp)


async def delete_trail(
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
    client = async_client("cloudtrail", region_name)
    try:
        await client.call("DeleteTrail", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_trail failed for {name!r}") from exc


# ---------------------------------------------------------------------------
# Logging control
# ---------------------------------------------------------------------------


async def start_logging(
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
    client = async_client("cloudtrail", region_name)
    try:
        await client.call("StartLogging", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"start_logging failed for {name!r}") from exc


async def stop_logging(
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
    client = async_client("cloudtrail", region_name)
    try:
        await client.call("StopLogging", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"stop_logging failed for {name!r}") from exc


async def get_trail_status(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call("GetTrailStatus", Name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_trail_status failed for {name!r}") from exc
    return _parse_status(resp)


# ---------------------------------------------------------------------------
# Event lookup
# ---------------------------------------------------------------------------


async def lookup_events(
    *,
    lookup_attributes: list[dict[str, str]] | None = None,
    start_time: Any = None,
    end_time: Any = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[LookupEvent]:
    """Look up management and data events captured by CloudTrail.

    Args:
        lookup_attributes: Lookup attribute dicts.
        start_time: Start of time range.
        end_time: End of time range.
        max_results: Maximum number of events per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`LookupEvent` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudtrail", region_name)
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
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("LookupEvents", **kwargs)
            for event in resp.get("Events", []):
                results.append(_parse_lookup_event(event))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "lookup_events failed") from exc
    return results


# ---------------------------------------------------------------------------
# List trails
# ---------------------------------------------------------------------------


async def list_trails(
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
    client = async_client("cloudtrail", region_name)
    results: list[TrailSummary] = []
    try:
        token: str | None = None
        while True:
            kw: dict[str, Any] = {}
            if token:
                kw["NextToken"] = token
            resp = await client.call("ListTrails", **kw)
            for trail in resp.get("Trails", []):
                results.append(
                    TrailSummary(
                        trail_arn=trail.get("TrailARN", ""),
                        name=trail.get("Name", ""),
                        home_region=trail.get("HomeRegion"),
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_trails failed") from exc
    return results


# ---------------------------------------------------------------------------
# Event Data Store operations
# ---------------------------------------------------------------------------


async def create_event_data_store(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("CreateEventDataStore", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"create_event_data_store failed for {name!r}",
        ) from exc
    return _parse_event_data_store(resp)


async def describe_event_data_store(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call(
            "DescribeEventDataStore",
            EventDataStore=event_data_store,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_event_data_store failed for {event_data_store!r}",
        ) from exc
    return _parse_event_data_store(resp)


async def list_event_data_stores(
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
    client = async_client("cloudtrail", region_name)
    results: list[EventDataStoreResult] = []
    try:
        token: str | None = None
        while True:
            kw: dict[str, Any] = {}
            if token:
                kw["NextToken"] = token
            resp = await client.call("ListEventDataStores", **kw)
            for eds in resp.get("EventDataStores", []):
                results.append(_parse_event_data_store(eds))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_event_data_stores failed") from exc
    return results


async def delete_event_data_store(
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
    client = async_client("cloudtrail", region_name)
    try:
        await client.call(
            "DeleteEventDataStore",
            EventDataStore=event_data_store,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"delete_event_data_store failed for {event_data_store!r}",
        ) from exc


# ---------------------------------------------------------------------------
# CloudTrail Lake queries
# ---------------------------------------------------------------------------


async def start_query(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call("StartQuery", QueryStatement=query_statement)
    except Exception as exc:
        raise wrap_aws_error(exc, "start_query failed") from exc
    return resp.get("QueryId", "")


async def get_query_results(
    query_id: str,
    *,
    event_data_store: str | None = None,
    max_query_results: int | None = None,
    region_name: str | None = None,
) -> QueryResult:
    """Get the results of a CloudTrail Lake query.

    Args:
        query_id: The query ID from :func:`start_query`.
        event_data_store: Event data store ARN (optional).
        max_query_results: Max number of result rows.
        region_name: AWS region override.

    Returns:
        A :class:`QueryResult` with the query results.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {"QueryId": query_id}
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    if max_query_results is not None:
        kwargs["MaxQueryResults"] = max_query_results
    try:
        resp = await client.call("GetQueryResults", **kwargs)
    except Exception as exc:
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


async def list_queries(
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
    client = async_client("cloudtrail", region_name)
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
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("ListQueries", **kwargs)
            results.extend(resp.get("Queries", []))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_queries failed") from exc
    return results


# ---------------------------------------------------------------------------
# Event selectors
# ---------------------------------------------------------------------------


async def put_event_selectors(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {"TrailName": trail_name}
    if event_selectors is not None:
        kwargs["EventSelectors"] = event_selectors
    if advanced_event_selectors is not None:
        kwargs["AdvancedEventSelectors"] = advanced_event_selectors
    try:
        resp = await client.call("PutEventSelectors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"put_event_selectors failed for {trail_name!r}",
        ) from exc
    return EventSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        event_selectors=resp.get("EventSelectors", []),
        advanced_event_selectors=resp.get("AdvancedEventSelectors", []),
    )


async def get_event_selectors(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call("GetEventSelectors", TrailName=trail_name)
    except Exception as exc:
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


async def put_insight_selectors(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call(
            "PutInsightSelectors",
            TrailName=trail_name,
            InsightSelectors=insight_selectors,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"put_insight_selectors failed for {trail_name!r}",
        ) from exc
    return InsightSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        insight_selectors=resp.get("InsightSelectors", []),
    )


async def get_insight_selectors(
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
    client = async_client("cloudtrail", region_name)
    try:
        resp = await client.call("GetInsightSelectors", TrailName=trail_name)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_insight_selectors failed for {trail_name!r}",
        ) from exc
    return InsightSelectorResult(
        trail_arn=resp.get("TrailARN", ""),
        insight_selectors=resp.get("InsightSelectors", []),
    )


async def add_tags(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagsList"] = tags_list
    try:
        await client.call("AddTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add tags") from exc
    return None


async def cancel_query(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryId"] = query_id
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    if event_data_store_owner_account_id is not None:
        kwargs["EventDataStoreOwnerAccountId"] = event_data_store_owner_account_id
    try:
        resp = await client.call("CancelQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel query") from exc
    return CancelQueryResult(
        query_id=resp.get("QueryId"),
        query_status=resp.get("QueryStatus"),
        event_data_store_owner_account_id=resp.get("EventDataStoreOwnerAccountId"),
    )


async def create_channel(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Source"] = source
    kwargs["Destinations"] = destinations
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create channel") from exc
    return CreateChannelResult(
        channel_arn=resp.get("ChannelArn"),
        name=resp.get("Name"),
        source=resp.get("Source"),
        destinations=resp.get("Destinations"),
        tags=resp.get("Tags"),
    )


async def create_dashboard(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("CreateDashboard", **kwargs)
    except Exception as exc:
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


async def delete_channel(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Channel"] = channel
    try:
        await client.call("DeleteChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete channel") from exc
    return None


async def delete_dashboard(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    try:
        await client.call("DeleteDashboard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dashboard") from exc
    return None


async def delete_resource_policy(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


async def deregister_organization_delegated_admin(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DelegatedAdminAccountId"] = delegated_admin_account_id
    try:
        await client.call("DeregisterOrganizationDelegatedAdmin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister organization delegated admin") from exc
    return None


async def describe_query(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("DescribeQuery", **kwargs)
    except Exception as exc:
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


async def disable_federation(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        resp = await client.call("DisableFederation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable federation") from exc
    return DisableFederationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        federation_status=resp.get("FederationStatus"),
    )


async def enable_federation(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    kwargs["FederationRoleArn"] = federation_role_arn
    try:
        resp = await client.call("EnableFederation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable federation") from exc
    return EnableFederationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        federation_status=resp.get("FederationStatus"),
        federation_role_arn=resp.get("FederationRoleArn"),
    )


async def generate_query(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStores"] = event_data_stores
    kwargs["Prompt"] = prompt
    try:
        resp = await client.call("GenerateQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to generate query") from exc
    return GenerateQueryResult(
        query_statement=resp.get("QueryStatement"),
        query_alias=resp.get("QueryAlias"),
        event_data_store_owner_account_id=resp.get("EventDataStoreOwnerAccountId"),
    )


async def get_channel(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Channel"] = channel
    try:
        resp = await client.call("GetChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get channel") from exc
    return GetChannelResult(
        channel_arn=resp.get("ChannelArn"),
        name=resp.get("Name"),
        source=resp.get("Source"),
        source_config=resp.get("SourceConfig"),
        destinations=resp.get("Destinations"),
        ingestion_status=resp.get("IngestionStatus"),
    )


async def get_dashboard(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    try:
        resp = await client.call("GetDashboard", **kwargs)
    except Exception as exc:
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


async def get_event_configuration(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    try:
        resp = await client.call("GetEventConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get event configuration") from exc
    return GetEventConfigurationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        max_event_size=resp.get("MaxEventSize"),
        context_key_selectors=resp.get("ContextKeySelectors"),
    )


async def get_event_data_store(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        resp = await client.call("GetEventDataStore", **kwargs)
    except Exception as exc:
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


async def get_import(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportId"] = import_id
    try:
        resp = await client.call("GetImport", **kwargs)
    except Exception as exc:
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


async def get_resource_policy(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
        resource_policy=resp.get("ResourcePolicy"),
        delegated_admin_resource_policy=resp.get("DelegatedAdminResourcePolicy"),
    )


async def list_channels(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListChannels", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list channels") from exc
    return ListChannelsResult(
        channels=resp.get("Channels"),
        next_token=resp.get("NextToken"),
    )


async def list_dashboards(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("ListDashboards", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dashboards") from exc
    return ListDashboardsResult(
        dashboards=resp.get("Dashboards"),
        next_token=resp.get("NextToken"),
    )


async def list_import_failures(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportId"] = import_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListImportFailures", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list import failures") from exc
    return ListImportFailuresResult(
        failures=resp.get("Failures"),
        next_token=resp.get("NextToken"),
    )


async def list_imports(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("ListImports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list imports") from exc
    return ListImportsResult(
        imports=resp.get("Imports"),
        next_token=resp.get("NextToken"),
    )


async def list_insights_metric_data(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("ListInsightsMetricData", **kwargs)
    except Exception as exc:
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


async def list_public_keys(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListPublicKeys", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list public keys") from exc
    return ListPublicKeysResult(
        public_key_list=resp.get("PublicKeyList"),
        next_token=resp.get("NextToken"),
    )


async def list_tags(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceIdList"] = resource_id_list
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags") from exc
    return ListTagsResult(
        resource_tag_list=resp.get("ResourceTagList"),
        next_token=resp.get("NextToken"),
    )


async def put_event_configuration(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MaxEventSize"] = max_event_size
    kwargs["ContextKeySelectors"] = context_key_selectors
    if event_data_store is not None:
        kwargs["EventDataStore"] = event_data_store
    try:
        resp = await client.call("PutEventConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put event configuration") from exc
    return PutEventConfigurationResult(
        event_data_store_arn=resp.get("EventDataStoreArn"),
        max_event_size=resp.get("MaxEventSize"),
        context_key_selectors=resp.get("ContextKeySelectors"),
    )


async def put_resource_policy(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["ResourcePolicy"] = resource_policy
    try:
        resp = await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        resource_arn=resp.get("ResourceArn"),
        resource_policy=resp.get("ResourcePolicy"),
        delegated_admin_resource_policy=resp.get("DelegatedAdminResourcePolicy"),
    )


async def register_organization_delegated_admin(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MemberAccountId"] = member_account_id
    try:
        await client.call("RegisterOrganizationDelegatedAdmin", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register organization delegated admin") from exc
    return None


async def remove_tags(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceId"] = resource_id
    kwargs["TagsList"] = tags_list
    try:
        await client.call("RemoveTags", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove tags") from exc
    return None


async def restore_event_data_store(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        resp = await client.call("RestoreEventDataStore", **kwargs)
    except Exception as exc:
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


async def search_sample_queries(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SearchPhrase"] = search_phrase
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("SearchSampleQueries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search sample queries") from exc
    return SearchSampleQueriesResult(
        search_results=resp.get("SearchResults"),
        next_token=resp.get("NextToken"),
    )


async def start_dashboard_refresh(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    if query_parameter_values is not None:
        kwargs["QueryParameterValues"] = query_parameter_values
    try:
        resp = await client.call("StartDashboardRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start dashboard refresh") from exc
    return StartDashboardRefreshResult(
        refresh_id=resp.get("RefreshId"),
    )


async def start_event_data_store_ingestion(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        await client.call("StartEventDataStoreIngestion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start event data store ingestion") from exc
    return None


async def start_import(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("StartImport", **kwargs)
    except Exception as exc:
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


async def stop_event_data_store_ingestion(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EventDataStore"] = event_data_store
    try:
        await client.call("StopEventDataStoreIngestion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop event data store ingestion") from exc
    return None


async def stop_import(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportId"] = import_id
    try:
        resp = await client.call("StopImport", **kwargs)
    except Exception as exc:
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


async def update_channel(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Channel"] = channel
    if destinations is not None:
        kwargs["Destinations"] = destinations
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = await client.call("UpdateChannel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update channel") from exc
    return UpdateChannelResult(
        channel_arn=resp.get("ChannelArn"),
        name=resp.get("Name"),
        source=resp.get("Source"),
        destinations=resp.get("Destinations"),
    )


async def update_dashboard(
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
    client = async_client("cloudtrail", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardId"] = dashboard_id
    if widgets is not None:
        kwargs["Widgets"] = widgets
    if refresh_schedule is not None:
        kwargs["RefreshSchedule"] = refresh_schedule
    if termination_protection_enabled is not None:
        kwargs["TerminationProtectionEnabled"] = termination_protection_enabled
    try:
        resp = await client.call("UpdateDashboard", **kwargs)
    except Exception as exc:
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


async def update_event_data_store(
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
    client = async_client("cloudtrail", region_name)
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
        resp = await client.call("UpdateEventDataStore", **kwargs)
    except Exception as exc:
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
