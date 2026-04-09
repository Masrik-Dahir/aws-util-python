"""Native async Amazon Timestream Query utilities.

Uses :mod:`aws_util.aio._engine` for true non-blocking I/O.  Pydantic
models and pure-compute helpers are re-exported from the sync module.
"""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.timestream_query import (
    ColumnInfo,
    DescribeAccountSettingsResult,
    DescribeScheduledQueryResult,
    EndpointInfo,
    ListTagsForResourceResult,
    PrepareQueryResult,
    QueryResult,
    Row,
    ScheduledQueryDescription,
    UpdateAccountSettingsResult,
    _parse_query_result,
    _parse_scheduled_query,
)

__all__ = [
    "ColumnInfo",
    "DescribeAccountSettingsResult",
    "DescribeScheduledQueryResult",
    "EndpointInfo",
    "ListTagsForResourceResult",
    "PrepareQueryResult",
    "QueryResult",
    "Row",
    "ScheduledQueryDescription",
    "UpdateAccountSettingsResult",
    "cancel_query",
    "create_scheduled_query",
    "delete_scheduled_query",
    "describe_account_settings",
    "describe_endpoints",
    "describe_scheduled_query",
    "execute_scheduled_query",
    "list_scheduled_queries",
    "list_tags_for_resource",
    "prepare_query",
    "query",
    "run_query",
    "tag_resource",
    "untag_resource",
    "update_account_settings",
    "update_scheduled_query",
]


# ---------------------------------------------------------------------------
# Query operations
# ---------------------------------------------------------------------------


async def query(
    query_string: str,
    *,
    max_rows: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> QueryResult:
    """Execute a single-page Timestream query.

    Args:
        query_string: SQL-like query string.
        max_rows: Maximum rows per page.
        next_token: Pagination token for the next page.
        region_name: AWS region override.

    Returns:
        A :class:`QueryResult` for this page.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {"QueryString": query_string}
    if max_rows is not None:
        kwargs["MaxRows"] = max_rows
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("Query", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "query failed") from exc
    return _parse_query_result(resp)


async def describe_endpoints(
    *,
    region_name: str | None = None,
) -> list[EndpointInfo]:
    """Describe Timestream query endpoints.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`EndpointInfo`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    try:
        resp = await client.call("DescribeEndpoints")
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_endpoints failed") from exc
    return [
        EndpointInfo(
            address=ep.get("Address", ""),
            cache_period_in_minutes=ep.get("CachePeriodInMinutes", 0),
        )
        for ep in resp.get("Endpoints", [])
    ]


async def cancel_query(
    query_id: str,
    *,
    region_name: str | None = None,
) -> bool:
    """Cancel a running Timestream query.

    Args:
        query_id: Identifier of the query to cancel.
        region_name: AWS region override.

    Returns:
        ``True`` if the cancellation message was sent.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    try:
        await client.call("CancelQuery", QueryId=query_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"cancel_query failed for {query_id!r}") from exc
    return True


async def run_query(
    query_string: str,
    *,
    max_rows: int | None = None,
    region_name: str | None = None,
) -> QueryResult:
    """Execute a query and auto-paginate all result pages.

    Collects rows across all pages into a single :class:`QueryResult`.

    Args:
        query_string: SQL-like query string.
        max_rows: Maximum rows per page.
        region_name: AWS region override.

    Returns:
        A :class:`QueryResult` with all rows and column info.

    Raises:
        RuntimeError: If any API call fails.
    """
    all_rows: list[Row] = []
    column_info: list[ColumnInfo] = []
    query_id: str | None = None
    token: str | None = None

    while True:
        page = await query(
            query_string,
            max_rows=max_rows,
            next_token=token,
            region_name=region_name,
        )
        if query_id is None:
            query_id = page.query_id
        if not column_info and page.column_info:
            column_info = page.column_info
        all_rows.extend(page.rows)
        token = page.next_token
        if not token:
            break

    return QueryResult(
        query_id=query_id,
        rows=all_rows,
        column_info=column_info,
    )


# ---------------------------------------------------------------------------
# Scheduled query operations
# ---------------------------------------------------------------------------


async def create_scheduled_query(
    name: str,
    query_string: str,
    schedule_expression: str,
    *,
    target_database: str | None = None,
    target_table: str | None = None,
    notification_sns_topic_arn: str | None = None,
    scheduled_query_execution_role_arn: str | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> ScheduledQueryDescription:
    """Create a Timestream scheduled query.

    Args:
        name: Name for the scheduled query.
        query_string: SQL query to schedule.
        schedule_expression: Cron or rate expression.
        target_database: Target database for results.
        target_table: Target table for results.
        notification_sns_topic_arn: SNS topic for notifications.
        scheduled_query_execution_role_arn: IAM role ARN.
        tags: Optional list of ``{"Key": ..., "Value": ...}`` tags.
        region_name: AWS region override.

    Returns:
        A :class:`ScheduledQueryDescription`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "QueryString": query_string,
        "ScheduleConfiguration": {
            "ScheduleExpression": schedule_expression,
        },
        "NotificationConfiguration": {},
    }
    if notification_sns_topic_arn is not None:
        kwargs["NotificationConfiguration"]["SnsConfiguration"] = {
            "TopicArn": notification_sns_topic_arn,
        }
    if scheduled_query_execution_role_arn is not None:
        kwargs["ScheduledQueryExecutionRoleArn"] = scheduled_query_execution_role_arn
    if target_database is not None and target_table is not None:
        kwargs["TargetConfiguration"] = {
            "TimestreamConfiguration": {
                "DatabaseName": target_database,
                "TableName": target_table,
                "TimeColumn": "time",
                "DimensionMappings": [],
            },
        }
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateScheduledQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_scheduled_query failed") from exc
    return _parse_scheduled_query(resp.get("ScheduledQuery", resp))


async def list_scheduled_queries(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> tuple[list[ScheduledQueryDescription], str | None]:
    """List Timestream scheduled queries.

    Args:
        max_results: Maximum number of results.
        next_token: Pagination token.
        region_name: AWS region override.

    Returns:
        A tuple of (list of :class:`ScheduledQueryDescription`, next_token).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListScheduledQueries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_scheduled_queries failed") from exc
    queries = [_parse_scheduled_query(q) for q in resp.get("ScheduledQueries", [])]
    return queries, resp.get("NextToken")


async def execute_scheduled_query(
    scheduled_query_arn: str,
    invocation_time: str,
    *,
    region_name: str | None = None,
) -> bool:
    """Manually trigger a scheduled query execution.

    Args:
        scheduled_query_arn: ARN of the scheduled query.
        invocation_time: ISO-8601 timestamp for the invocation.
        region_name: AWS region override.

    Returns:
        ``True`` if the execution was triggered.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    try:
        await client.call(
            "ExecuteScheduledQuery",
            ScheduledQueryArn=scheduled_query_arn,
            InvocationTime=invocation_time,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "execute_scheduled_query failed") from exc
    return True


async def delete_scheduled_query(
    scheduled_query_arn: str,
    *,
    region_name: str | None = None,
) -> bool:
    """Delete a scheduled query.

    Args:
        scheduled_query_arn: ARN of the scheduled query to delete.
        region_name: AWS region override.

    Returns:
        ``True`` if the deletion succeeded.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    try:
        await client.call(
            "DeleteScheduledQuery",
            ScheduledQueryArn=scheduled_query_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_scheduled_query failed") from exc
    return True


async def describe_account_settings(
    region_name: str | None = None,
) -> DescribeAccountSettingsResult:
    """Describe account settings.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account settings") from exc
    return DescribeAccountSettingsResult(
        max_query_tcu=resp.get("MaxQueryTCU"),
        query_pricing_model=resp.get("QueryPricingModel"),
        query_compute=resp.get("QueryCompute"),
    )


async def describe_scheduled_query(
    scheduled_query_arn: str,
    region_name: str | None = None,
) -> DescribeScheduledQueryResult:
    """Describe scheduled query.

    Args:
        scheduled_query_arn: Scheduled query arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduledQueryArn"] = scheduled_query_arn
    try:
        resp = await client.call("DescribeScheduledQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe scheduled query") from exc
    return DescribeScheduledQueryResult(
        scheduled_query=resp.get("ScheduledQuery"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


async def prepare_query(
    query_string: str,
    *,
    validate_only: bool | None = None,
    region_name: str | None = None,
) -> PrepareQueryResult:
    """Prepare query.

    Args:
        query_string: Query string.
        validate_only: Validate only.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryString"] = query_string
    if validate_only is not None:
        kwargs["ValidateOnly"] = validate_only
    try:
        resp = await client.call("PrepareQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to prepare query") from exc
    return PrepareQueryResult(
        query_string=resp.get("QueryString"),
        columns=resp.get("Columns"),
        parameters=resp.get("Parameters"),
    )


async def tag_resource(
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
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
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
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_account_settings(
    *,
    max_query_tcu: int | None = None,
    query_pricing_model: str | None = None,
    query_compute: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateAccountSettingsResult:
    """Update account settings.

    Args:
        max_query_tcu: Max query tcu.
        query_pricing_model: Query pricing model.
        query_compute: Query compute.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    if max_query_tcu is not None:
        kwargs["MaxQueryTCU"] = max_query_tcu
    if query_pricing_model is not None:
        kwargs["QueryPricingModel"] = query_pricing_model
    if query_compute is not None:
        kwargs["QueryCompute"] = query_compute
    try:
        resp = await client.call("UpdateAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account settings") from exc
    return UpdateAccountSettingsResult(
        max_query_tcu=resp.get("MaxQueryTCU"),
        query_pricing_model=resp.get("QueryPricingModel"),
        query_compute=resp.get("QueryCompute"),
    )


async def update_scheduled_query(
    scheduled_query_arn: str,
    state: str,
    region_name: str | None = None,
) -> None:
    """Update scheduled query.

    Args:
        scheduled_query_arn: Scheduled query arn.
        state: State.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-query", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ScheduledQueryArn"] = scheduled_query_arn
    kwargs["State"] = state
    try:
        await client.call("UpdateScheduledQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update scheduled query") from exc
    return None
