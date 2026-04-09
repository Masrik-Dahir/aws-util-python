from __future__ import annotations

import datetime
import logging
import time
from collections.abc import Generator
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, field_validator

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "VALID_CLOUDWATCH_UNITS",
    "DeleteInsightRulesResult",
    "DescribeAlarmContributorsResult",
    "DescribeAlarmHistoryResult",
    "DescribeAlarmsForMetricResult",
    "DescribeAlarmsResult",
    "DescribeAnomalyDetectorsResult",
    "DescribeInsightRulesResult",
    "DisableInsightRulesResult",
    "EnableInsightRulesResult",
    "GetDashboardResult",
    "GetInsightRuleReportResult",
    "GetMetricDataResult",
    "GetMetricStreamResult",
    "GetMetricWidgetImageResult",
    "ListDashboardsResult",
    "ListManagedInsightRulesResult",
    "ListMetricStreamsResult",
    "ListMetricsResult",
    "ListTagsForResourceResult",
    "LogEvent",
    "MetricDatum",
    "MetricDimension",
    "PutDashboardResult",
    "PutManagedInsightRulesResult",
    "PutMetricStreamResult",
    "create_alarm",
    "create_log_group",
    "create_log_stream",
    "delete_alarms",
    "delete_anomaly_detector",
    "delete_dashboards",
    "delete_insight_rules",
    "delete_metric_stream",
    "describe_alarm_contributors",
    "describe_alarm_history",
    "describe_alarms",
    "describe_alarms_for_metric",
    "describe_anomaly_detectors",
    "describe_insight_rules",
    "disable_alarm_actions",
    "disable_insight_rules",
    "enable_alarm_actions",
    "enable_insight_rules",
    "get_dashboard",
    "get_insight_rule_report",
    "get_log_events",
    "get_metric_data",
    "get_metric_statistics",
    "get_metric_stream",
    "get_metric_widget_image",
    "list_dashboards",
    "list_managed_insight_rules",
    "list_metric_streams",
    "list_metrics",
    "list_tags_for_resource",
    "put_anomaly_detector",
    "put_composite_alarm",
    "put_dashboard",
    "put_insight_rule",
    "put_log_events",
    "put_managed_insight_rules",
    "put_metric",
    "put_metric_alarm",
    "put_metric_data",
    "put_metric_stream",
    "put_metrics",
    "set_alarm_state",
    "start_metric_streams",
    "stop_metric_streams",
    "tag_resource",
    "tail_log_stream",
    "untag_resource",
]

# Valid CloudWatch unit strings (from CloudWatch API docs).
VALID_CLOUDWATCH_UNITS: frozenset[str] = frozenset(
    {
        "Seconds",
        "Microseconds",
        "Milliseconds",
        "Bytes",
        "Kilobytes",
        "Megabytes",
        "Gigabytes",
        "Terabytes",
        "Bits",
        "Kilobits",
        "Megabits",
        "Gigabits",
        "Terabits",
        "Percent",
        "Count",
        "Bytes/Second",
        "Kilobytes/Second",
        "Megabytes/Second",
        "Gigabytes/Second",
        "Terabytes/Second",
        "Bits/Second",
        "Kilobits/Second",
        "Megabits/Second",
        "Gigabits/Second",
        "Terabits/Second",
        "Count/Second",
        "None",
    }
)

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class MetricDimension(BaseModel):
    """A single CloudWatch metric dimension (name/value pair)."""

    model_config = ConfigDict(frozen=True)

    name: str
    value: str


class MetricDatum(BaseModel):
    """A single data point to publish to CloudWatch Metrics."""

    model_config = ConfigDict(frozen=True)

    metric_name: str
    value: float
    unit: str = "None"
    dimensions: list[MetricDimension] = []

    @field_validator("unit")
    @classmethod
    def _validate_unit(cls, v: str) -> str:
        if v not in VALID_CLOUDWATCH_UNITS:
            raise ValueError(f"Invalid CloudWatch unit {v!r}")
        return v


class LogEvent(BaseModel):
    """A single CloudWatch Logs log event."""

    model_config = ConfigDict(frozen=True)

    timestamp: int
    """Unix epoch in milliseconds."""
    message: str

    @classmethod
    def now(cls, message: str) -> LogEvent:
        """Create a :class:`LogEvent` timestamped to the current millisecond."""
        return cls(timestamp=int(time.time() * 1000), message=message)


# ---------------------------------------------------------------------------
# CloudWatch Metrics utilities
# ---------------------------------------------------------------------------


def put_metric(
    namespace: str,
    metric_name: str,
    value: float,
    unit: str = "None",
    dimensions: list[MetricDimension] | None = None,
    region_name: str | None = None,
) -> None:
    """Publish a single custom metric data point to CloudWatch.

    Args:
        namespace: Metric namespace, e.g. ``"MyApp/Performance"``.
        metric_name: Metric name, e.g. ``"Latency"``.
        value: Numeric data point value.
        unit: CloudWatch unit string.  Defaults to ``"None"``.
        dimensions: Optional list of :class:`MetricDimension` objects.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the put operation fails.
    """
    datum = MetricDatum(
        metric_name=metric_name,
        value=value,
        unit=unit,
        dimensions=dimensions or [],
    )
    put_metrics(namespace, [datum], region_name=region_name)


def put_metrics(
    namespace: str,
    metrics: list[MetricDatum],
    region_name: str | None = None,
) -> None:
    """Publish metric data points to CloudWatch.

    Args:
        namespace: Metric namespace.
        metrics: List of :class:`MetricDatum` objects.  Larger lists are
            chunked automatically into batches of up to 1000 (the
            ``PutMetricData`` API maximum).
        region_name: AWS region override.

    Raises:
        RuntimeError: If any put operation fails.
    """
    client = get_client("cloudwatch", region_name)
    # AWS PutMetricData supports up to 1000 metric data items per call.
    chunk_size = 1000
    for i in range(0, len(metrics), chunk_size):
        chunk = metrics[i : i + chunk_size]
        metric_data = [
            {
                "MetricName": m.metric_name,
                "Value": m.value,
                "Unit": m.unit,
                "Dimensions": [{"Name": d.name, "Value": d.value} for d in m.dimensions],
            }
            for m in chunk
        ]
        try:
            client.put_metric_data(Namespace=namespace, MetricData=metric_data)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to put metrics to namespace {namespace!r}") from exc


# ---------------------------------------------------------------------------
# CloudWatch Logs utilities
# ---------------------------------------------------------------------------


def create_log_group(
    log_group_name: str,
    region_name: str | None = None,
) -> None:
    """Create a CloudWatch Logs log group if it does not already exist.

    Args:
        log_group_name: Name of the log group, e.g. ``"/myapp/api"``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If creation fails for a reason other than the group
            already existing.
    """
    client = get_client("logs", region_name)
    try:
        client.create_log_group(logGroupName=log_group_name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceAlreadyExistsException":
            return
        raise wrap_aws_error(exc, f"Failed to create log group {log_group_name!r}") from exc


def create_log_stream(
    log_group_name: str,
    log_stream_name: str,
    region_name: str | None = None,
) -> None:
    """Create a CloudWatch Logs log stream if it does not already exist.

    Args:
        log_group_name: Parent log group name.
        log_stream_name: Name of the log stream.
        region_name: AWS region override.

    Raises:
        RuntimeError: If creation fails for a reason other than the stream
            already existing.
    """
    client = get_client("logs", region_name)
    try:
        client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
        )
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ResourceAlreadyExistsException":
            return
        raise wrap_aws_error(
            exc, f"Failed to create log stream {log_stream_name!r} in {log_group_name!r}"
        ) from exc


def put_log_events(
    log_group_name: str,
    log_stream_name: str,
    events: list[LogEvent],
    region_name: str | None = None,
) -> None:
    """Write log events to a CloudWatch Logs stream.

    Events must be sorted in ascending timestamp order (CloudWatch
    requirement).

    .. note::

        The log group and log stream must already exist.  This function does
        **not** auto-create them.  Use :func:`create_log_group` and
        :func:`create_log_stream` beforehand if needed.

    Args:
        log_group_name: Log group name.
        log_stream_name: Log stream name.
        events: List of :class:`LogEvent` objects sorted by timestamp.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the put operation fails.
    """
    client = get_client("logs", region_name)
    log_events = [{"timestamp": e.timestamp, "message": e.message} for e in events]
    try:
        client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to put log events to {log_group_name!r}/{log_stream_name!r}"
        ) from exc


def get_log_events(
    log_group_name: str,
    log_stream_name: str,
    start_time: int | None = None,
    end_time: int | None = None,
    limit: int = 100,
    region_name: str | None = None,
) -> list[LogEvent]:
    """Retrieve log events from a CloudWatch Logs stream.

    Args:
        log_group_name: Log group name.
        log_stream_name: Log stream name.
        start_time: Start of the time range (Unix ms, inclusive).
        end_time: End of the time range (Unix ms, inclusive).
        limit: Maximum number of events to return (default 100).
        region_name: AWS region override.

    Returns:
        A list of :class:`LogEvent` objects in ascending timestamp order.

    Raises:
        RuntimeError: If the retrieval fails.
    """
    client = get_client("logs", region_name)
    kwargs: dict = {
        "logGroupName": log_group_name,
        "logStreamName": log_stream_name,
        "limit": limit,
        "startFromHead": True,
    }
    if start_time is not None:
        kwargs["startTime"] = start_time
    if end_time is not None:
        kwargs["endTime"] = end_time

    try:
        resp = client.get_log_events(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to get log events from {log_group_name!r}/{log_stream_name!r}"
        ) from exc

    return [
        LogEvent(timestamp=e["timestamp"], message=e["message"]) for e in resp.get("events", [])
    ]


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def get_metric_statistics(
    namespace: str,
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    period: int = 300,
    statistics: list[str] | None = None,
    dimensions: list[MetricDimension] | None = None,
    region_name: str | None = None,
) -> list[dict]:
    """Fetch historical CloudWatch metric data points.

    Args:
        namespace: Metric namespace, e.g. ``"AWS/Lambda"``.
        metric_name: Metric name, e.g. ``"Errors"``.
        start_time: Start of the time range (UTC).
        end_time: End of the time range (UTC).
        period: Granularity in seconds (must be a multiple of 60, default
            ``300`` / 5 min).
        statistics: Which statistics to return.  Defaults to
            ``["Average", "Sum", "Maximum", "Minimum", "SampleCount"]``.
        dimensions: Optional dimension filters.
        region_name: AWS region override.

    Returns:
        A list of data-point dicts sorted by ``Timestamp``, each containing
        the requested statistics.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict = {
        "Namespace": namespace,
        "MetricName": metric_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": period,
        "Statistics": statistics or ["Average", "Sum", "Maximum", "Minimum", "SampleCount"],
    }
    if dimensions:
        kwargs["Dimensions"] = [{"Name": d.name, "Value": d.value} for d in dimensions]

    try:
        resp = client.get_metric_statistics(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"get_metric_statistics failed for {namespace}/{metric_name}"
        ) from exc

    return sorted(resp.get("Datapoints", []), key=lambda dp: dp["Timestamp"])


def create_alarm(
    alarm_name: str,
    namespace: str,
    metric_name: str,
    threshold: float,
    comparison_operator: str = "GreaterThanOrEqualToThreshold",
    evaluation_periods: int = 1,
    period: int = 300,
    statistic: str = "Sum",
    alarm_actions: list[str] | None = None,
    ok_actions: list[str] | None = None,
    dimensions: list[MetricDimension] | None = None,
    treat_missing_data: str = "notBreaching",
    region_name: str | None = None,
) -> None:
    """Create or update a CloudWatch metric alarm.

    Args:
        alarm_name: Unique alarm name.
        namespace: Metric namespace.
        metric_name: Metric name.
        threshold: Value the metric is compared against.
        comparison_operator: One of ``"GreaterThanOrEqualToThreshold"``,
            ``"GreaterThanThreshold"``, ``"LessThanThreshold"``,
            ``"LessThanOrEqualToThreshold"``.
        evaluation_periods: Number of consecutive periods before the alarm
            state changes (default ``1``).
        period: Evaluation period in seconds (default ``300``).
        statistic: Metric statistic — ``"Sum"``, ``"Average"``, ``"Maximum"``,
            ``"Minimum"``, ``"SampleCount"``.
        alarm_actions: SNS topic ARNs or auto-scaling ARNs to trigger when the
            alarm enters ALARM state.
        ok_actions: ARNs to trigger when the alarm returns to OK state.
        dimensions: Metric dimensions to filter by.
        treat_missing_data: How to handle missing data — ``"notBreaching"``
            (default), ``"breaching"``, ``"ignore"``, or ``"missing"``.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the alarm creation fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict = {
        "AlarmName": alarm_name,
        "Namespace": namespace,
        "MetricName": metric_name,
        "Threshold": threshold,
        "ComparisonOperator": comparison_operator,
        "EvaluationPeriods": evaluation_periods,
        "Period": period,
        "Statistic": statistic,
        "TreatMissingData": treat_missing_data,
        "AlarmActions": alarm_actions or [],
        "OKActions": ok_actions or [],
    }
    if dimensions:
        kwargs["Dimensions"] = [{"Name": d.name, "Value": d.value} for d in dimensions]

    try:
        client.put_metric_alarm(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_alarm failed for {alarm_name!r}") from exc


def tail_log_stream(
    log_group_name: str,
    log_stream_name: str,
    poll_interval: float = 2.0,
    duration_seconds: float = 60.0,
    region_name: str | None = None,
) -> Generator[LogEvent, None, None]:
    """Tail a CloudWatch Logs stream and yield new log events as they arrive.

    Args:
        log_group_name: Log group name.
        log_stream_name: Log stream name.
        poll_interval: Seconds between polls (default ``2``).
        duration_seconds: Total seconds to tail (default ``60``).  Set to
            ``float('inf')`` for indefinite tailing.
        region_name: AWS region override.

    Yields:
        :class:`LogEvent` objects in arrival order.
    """
    client = get_client("logs", region_name)
    kwargs: dict = {
        "logGroupName": log_group_name,
        "logStreamName": log_stream_name,
        "startFromHead": False,
    }
    deadline = time.monotonic() + duration_seconds

    while time.monotonic() < deadline:
        try:
            resp = client.get_log_events(**kwargs)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code", "")
            logger.error(
                "tail_log_stream error on %s/%s: %s",
                log_group_name,
                log_stream_name,
                exc,
            )
            # Re-raise non-transient errors (e.g. permission issues).
            if error_code in {"AccessDeniedException", "AccessDenied"}:
                raise wrap_aws_error(
                    exc,
                    f"tail_log_stream denied for {log_group_name!r}/{log_stream_name!r}",
                ) from exc
            break

        events = resp.get("events", [])
        for event in events:
            yield LogEvent(timestamp=event["timestamp"], message=event["message"])

        next_token = resp.get("nextForwardToken")
        if next_token:
            kwargs["nextToken"] = next_token
        time.sleep(poll_interval)


class DeleteInsightRulesResult(BaseModel):
    """Result of delete_insight_rules."""

    model_config = ConfigDict(frozen=True)

    failures: list[dict[str, Any]] | None = None


class DescribeAlarmContributorsResult(BaseModel):
    """Result of describe_alarm_contributors."""

    model_config = ConfigDict(frozen=True)

    alarm_contributors: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeAlarmHistoryResult(BaseModel):
    """Result of describe_alarm_history."""

    model_config = ConfigDict(frozen=True)

    alarm_history_items: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeAlarmsResult(BaseModel):
    """Result of describe_alarms."""

    model_config = ConfigDict(frozen=True)

    composite_alarms: list[dict[str, Any]] | None = None
    metric_alarms: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeAlarmsForMetricResult(BaseModel):
    """Result of describe_alarms_for_metric."""

    model_config = ConfigDict(frozen=True)

    metric_alarms: list[dict[str, Any]] | None = None


class DescribeAnomalyDetectorsResult(BaseModel):
    """Result of describe_anomaly_detectors."""

    model_config = ConfigDict(frozen=True)

    anomaly_detectors: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeInsightRulesResult(BaseModel):
    """Result of describe_insight_rules."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    insight_rules: list[dict[str, Any]] | None = None


class DisableInsightRulesResult(BaseModel):
    """Result of disable_insight_rules."""

    model_config = ConfigDict(frozen=True)

    failures: list[dict[str, Any]] | None = None


class EnableInsightRulesResult(BaseModel):
    """Result of enable_insight_rules."""

    model_config = ConfigDict(frozen=True)

    failures: list[dict[str, Any]] | None = None


class GetDashboardResult(BaseModel):
    """Result of get_dashboard."""

    model_config = ConfigDict(frozen=True)

    dashboard_arn: str | None = None
    dashboard_body: str | None = None
    dashboard_name: str | None = None


class GetInsightRuleReportResult(BaseModel):
    """Result of get_insight_rule_report."""

    model_config = ConfigDict(frozen=True)

    key_labels: list[str] | None = None
    aggregation_statistic: str | None = None
    aggregate_value: float | None = None
    approximate_unique_count: int | None = None
    contributors: list[dict[str, Any]] | None = None
    metric_datapoints: list[dict[str, Any]] | None = None


class GetMetricDataResult(BaseModel):
    """Result of get_metric_data."""

    model_config = ConfigDict(frozen=True)

    metric_data_results: list[dict[str, Any]] | None = None
    next_token: str | None = None
    messages: list[dict[str, Any]] | None = None


class GetMetricStreamResult(BaseModel):
    """Result of get_metric_stream."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    name: str | None = None
    include_filters: list[dict[str, Any]] | None = None
    exclude_filters: list[dict[str, Any]] | None = None
    firehose_arn: str | None = None
    role_arn: str | None = None
    state: str | None = None
    creation_date: str | None = None
    last_update_date: str | None = None
    output_format: str | None = None
    statistics_configurations: list[dict[str, Any]] | None = None
    include_linked_accounts_metrics: bool | None = None


class GetMetricWidgetImageResult(BaseModel):
    """Result of get_metric_widget_image."""

    model_config = ConfigDict(frozen=True)

    metric_widget_image: bytes | None = None


class ListDashboardsResult(BaseModel):
    """Result of list_dashboards."""

    model_config = ConfigDict(frozen=True)

    dashboard_entries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListManagedInsightRulesResult(BaseModel):
    """Result of list_managed_insight_rules."""

    model_config = ConfigDict(frozen=True)

    managed_rules: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListMetricStreamsResult(BaseModel):
    """Result of list_metric_streams."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    entries: list[dict[str, Any]] | None = None


class ListMetricsResult(BaseModel):
    """Result of list_metrics."""

    model_config = ConfigDict(frozen=True)

    metrics: list[dict[str, Any]] | None = None
    next_token: str | None = None
    owning_accounts: list[str] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


class PutDashboardResult(BaseModel):
    """Result of put_dashboard."""

    model_config = ConfigDict(frozen=True)

    dashboard_validation_messages: list[dict[str, Any]] | None = None


class PutManagedInsightRulesResult(BaseModel):
    """Result of put_managed_insight_rules."""

    model_config = ConfigDict(frozen=True)

    failures: list[dict[str, Any]] | None = None


class PutMetricStreamResult(BaseModel):
    """Result of put_metric_stream."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None


def delete_alarms(
    alarm_names: list[str],
    region_name: str | None = None,
) -> None:
    """Delete alarms.

    Args:
        alarm_names: Alarm names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmNames"] = alarm_names
    try:
        client.delete_alarms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete alarms") from exc
    return None


def delete_anomaly_detector(
    *,
    namespace: str | None = None,
    metric_name: str | None = None,
    dimensions: list[dict[str, Any]] | None = None,
    stat: str | None = None,
    single_metric_anomaly_detector: dict[str, Any] | None = None,
    metric_math_anomaly_detector: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Delete anomaly detector.

    Args:
        namespace: Namespace.
        metric_name: Metric name.
        dimensions: Dimensions.
        stat: Stat.
        single_metric_anomaly_detector: Single metric anomaly detector.
        metric_math_anomaly_detector: Metric math anomaly detector.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if metric_name is not None:
        kwargs["MetricName"] = metric_name
    if dimensions is not None:
        kwargs["Dimensions"] = dimensions
    if stat is not None:
        kwargs["Stat"] = stat
    if single_metric_anomaly_detector is not None:
        kwargs["SingleMetricAnomalyDetector"] = single_metric_anomaly_detector
    if metric_math_anomaly_detector is not None:
        kwargs["MetricMathAnomalyDetector"] = metric_math_anomaly_detector
    try:
        client.delete_anomaly_detector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete anomaly detector") from exc
    return None


def delete_dashboards(
    dashboard_names: list[str],
    region_name: str | None = None,
) -> None:
    """Delete dashboards.

    Args:
        dashboard_names: Dashboard names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardNames"] = dashboard_names
    try:
        client.delete_dashboards(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete dashboards") from exc
    return None


def delete_insight_rules(
    rule_names: list[str],
    region_name: str | None = None,
) -> DeleteInsightRulesResult:
    """Delete insight rules.

    Args:
        rule_names: Rule names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleNames"] = rule_names
    try:
        resp = client.delete_insight_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete insight rules") from exc
    return DeleteInsightRulesResult(
        failures=resp.get("Failures"),
    )


def delete_metric_stream(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete metric stream.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        client.delete_metric_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete metric stream") from exc
    return None


def describe_alarm_contributors(
    alarm_name: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAlarmContributorsResult:
    """Describe alarm contributors.

    Args:
        alarm_name: Alarm name.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmName"] = alarm_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_alarm_contributors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe alarm contributors") from exc
    return DescribeAlarmContributorsResult(
        alarm_contributors=resp.get("AlarmContributors"),
        next_token=resp.get("NextToken"),
    )


def describe_alarm_history(
    *,
    alarm_name: str | None = None,
    alarm_contributor_id: str | None = None,
    alarm_types: list[str] | None = None,
    history_item_type: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    scan_by: str | None = None,
    region_name: str | None = None,
) -> DescribeAlarmHistoryResult:
    """Describe alarm history.

    Args:
        alarm_name: Alarm name.
        alarm_contributor_id: Alarm contributor id.
        alarm_types: Alarm types.
        history_item_type: History item type.
        start_date: Start date.
        end_date: End date.
        max_records: Max records.
        next_token: Next token.
        scan_by: Scan by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if alarm_name is not None:
        kwargs["AlarmName"] = alarm_name
    if alarm_contributor_id is not None:
        kwargs["AlarmContributorId"] = alarm_contributor_id
    if alarm_types is not None:
        kwargs["AlarmTypes"] = alarm_types
    if history_item_type is not None:
        kwargs["HistoryItemType"] = history_item_type
    if start_date is not None:
        kwargs["StartDate"] = start_date
    if end_date is not None:
        kwargs["EndDate"] = end_date
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if scan_by is not None:
        kwargs["ScanBy"] = scan_by
    try:
        resp = client.describe_alarm_history(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe alarm history") from exc
    return DescribeAlarmHistoryResult(
        alarm_history_items=resp.get("AlarmHistoryItems"),
        next_token=resp.get("NextToken"),
    )


def describe_alarms(
    *,
    alarm_names: list[str] | None = None,
    alarm_name_prefix: str | None = None,
    alarm_types: list[str] | None = None,
    children_of_alarm_name: str | None = None,
    parents_of_alarm_name: str | None = None,
    state_value: str | None = None,
    action_prefix: str | None = None,
    max_records: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAlarmsResult:
    """Describe alarms.

    Args:
        alarm_names: Alarm names.
        alarm_name_prefix: Alarm name prefix.
        alarm_types: Alarm types.
        children_of_alarm_name: Children of alarm name.
        parents_of_alarm_name: Parents of alarm name.
        state_value: State value.
        action_prefix: Action prefix.
        max_records: Max records.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if alarm_names is not None:
        kwargs["AlarmNames"] = alarm_names
    if alarm_name_prefix is not None:
        kwargs["AlarmNamePrefix"] = alarm_name_prefix
    if alarm_types is not None:
        kwargs["AlarmTypes"] = alarm_types
    if children_of_alarm_name is not None:
        kwargs["ChildrenOfAlarmName"] = children_of_alarm_name
    if parents_of_alarm_name is not None:
        kwargs["ParentsOfAlarmName"] = parents_of_alarm_name
    if state_value is not None:
        kwargs["StateValue"] = state_value
    if action_prefix is not None:
        kwargs["ActionPrefix"] = action_prefix
    if max_records is not None:
        kwargs["MaxRecords"] = max_records
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_alarms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe alarms") from exc
    return DescribeAlarmsResult(
        composite_alarms=resp.get("CompositeAlarms"),
        metric_alarms=resp.get("MetricAlarms"),
        next_token=resp.get("NextToken"),
    )


def describe_alarms_for_metric(
    metric_name: str,
    namespace: str,
    *,
    statistic: str | None = None,
    extended_statistic: str | None = None,
    dimensions: list[dict[str, Any]] | None = None,
    period: int | None = None,
    unit: str | None = None,
    region_name: str | None = None,
) -> DescribeAlarmsForMetricResult:
    """Describe alarms for metric.

    Args:
        metric_name: Metric name.
        namespace: Namespace.
        statistic: Statistic.
        extended_statistic: Extended statistic.
        dimensions: Dimensions.
        period: Period.
        unit: Unit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MetricName"] = metric_name
    kwargs["Namespace"] = namespace
    if statistic is not None:
        kwargs["Statistic"] = statistic
    if extended_statistic is not None:
        kwargs["ExtendedStatistic"] = extended_statistic
    if dimensions is not None:
        kwargs["Dimensions"] = dimensions
    if period is not None:
        kwargs["Period"] = period
    if unit is not None:
        kwargs["Unit"] = unit
    try:
        resp = client.describe_alarms_for_metric(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe alarms for metric") from exc
    return DescribeAlarmsForMetricResult(
        metric_alarms=resp.get("MetricAlarms"),
    )


def describe_anomaly_detectors(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    namespace: str | None = None,
    metric_name: str | None = None,
    dimensions: list[dict[str, Any]] | None = None,
    anomaly_detector_types: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeAnomalyDetectorsResult:
    """Describe anomaly detectors.

    Args:
        next_token: Next token.
        max_results: Max results.
        namespace: Namespace.
        metric_name: Metric name.
        dimensions: Dimensions.
        anomaly_detector_types: Anomaly detector types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if metric_name is not None:
        kwargs["MetricName"] = metric_name
    if dimensions is not None:
        kwargs["Dimensions"] = dimensions
    if anomaly_detector_types is not None:
        kwargs["AnomalyDetectorTypes"] = anomaly_detector_types
    try:
        resp = client.describe_anomaly_detectors(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe anomaly detectors") from exc
    return DescribeAnomalyDetectorsResult(
        anomaly_detectors=resp.get("AnomalyDetectors"),
        next_token=resp.get("NextToken"),
    )


def describe_insight_rules(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeInsightRulesResult:
    """Describe insight rules.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_insight_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe insight rules") from exc
    return DescribeInsightRulesResult(
        next_token=resp.get("NextToken"),
        insight_rules=resp.get("InsightRules"),
    )


def disable_alarm_actions(
    alarm_names: list[str],
    region_name: str | None = None,
) -> None:
    """Disable alarm actions.

    Args:
        alarm_names: Alarm names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmNames"] = alarm_names
    try:
        client.disable_alarm_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable alarm actions") from exc
    return None


def disable_insight_rules(
    rule_names: list[str],
    region_name: str | None = None,
) -> DisableInsightRulesResult:
    """Disable insight rules.

    Args:
        rule_names: Rule names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleNames"] = rule_names
    try:
        resp = client.disable_insight_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable insight rules") from exc
    return DisableInsightRulesResult(
        failures=resp.get("Failures"),
    )


def enable_alarm_actions(
    alarm_names: list[str],
    region_name: str | None = None,
) -> None:
    """Enable alarm actions.

    Args:
        alarm_names: Alarm names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmNames"] = alarm_names
    try:
        client.enable_alarm_actions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable alarm actions") from exc
    return None


def enable_insight_rules(
    rule_names: list[str],
    region_name: str | None = None,
) -> EnableInsightRulesResult:
    """Enable insight rules.

    Args:
        rule_names: Rule names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleNames"] = rule_names
    try:
        resp = client.enable_insight_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable insight rules") from exc
    return EnableInsightRulesResult(
        failures=resp.get("Failures"),
    )


def get_dashboard(
    dashboard_name: str,
    region_name: str | None = None,
) -> GetDashboardResult:
    """Get dashboard.

    Args:
        dashboard_name: Dashboard name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardName"] = dashboard_name
    try:
        resp = client.get_dashboard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get dashboard") from exc
    return GetDashboardResult(
        dashboard_arn=resp.get("DashboardArn"),
        dashboard_body=resp.get("DashboardBody"),
        dashboard_name=resp.get("DashboardName"),
    )


def get_insight_rule_report(
    rule_name: str,
    start_time: str,
    end_time: str,
    period: int,
    *,
    max_contributor_count: int | None = None,
    metrics: list[str] | None = None,
    order_by: str | None = None,
    region_name: str | None = None,
) -> GetInsightRuleReportResult:
    """Get insight rule report.

    Args:
        rule_name: Rule name.
        start_time: Start time.
        end_time: End time.
        period: Period.
        max_contributor_count: Max contributor count.
        metrics: Metrics.
        order_by: Order by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleName"] = rule_name
    kwargs["StartTime"] = start_time
    kwargs["EndTime"] = end_time
    kwargs["Period"] = period
    if max_contributor_count is not None:
        kwargs["MaxContributorCount"] = max_contributor_count
    if metrics is not None:
        kwargs["Metrics"] = metrics
    if order_by is not None:
        kwargs["OrderBy"] = order_by
    try:
        resp = client.get_insight_rule_report(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get insight rule report") from exc
    return GetInsightRuleReportResult(
        key_labels=resp.get("KeyLabels"),
        aggregation_statistic=resp.get("AggregationStatistic"),
        aggregate_value=resp.get("AggregateValue"),
        approximate_unique_count=resp.get("ApproximateUniqueCount"),
        contributors=resp.get("Contributors"),
        metric_datapoints=resp.get("MetricDatapoints"),
    )


def get_metric_data(
    metric_data_queries: list[dict[str, Any]],
    start_time: str,
    end_time: str,
    *,
    next_token: str | None = None,
    scan_by: str | None = None,
    max_datapoints: int | None = None,
    label_options: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> GetMetricDataResult:
    """Get metric data.

    Args:
        metric_data_queries: Metric data queries.
        start_time: Start time.
        end_time: End time.
        next_token: Next token.
        scan_by: Scan by.
        max_datapoints: Max datapoints.
        label_options: Label options.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MetricDataQueries"] = metric_data_queries
    kwargs["StartTime"] = start_time
    kwargs["EndTime"] = end_time
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if scan_by is not None:
        kwargs["ScanBy"] = scan_by
    if max_datapoints is not None:
        kwargs["MaxDatapoints"] = max_datapoints
    if label_options is not None:
        kwargs["LabelOptions"] = label_options
    try:
        resp = client.get_metric_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get metric data") from exc
    return GetMetricDataResult(
        metric_data_results=resp.get("MetricDataResults"),
        next_token=resp.get("NextToken"),
        messages=resp.get("Messages"),
    )


def get_metric_stream(
    name: str,
    region_name: str | None = None,
) -> GetMetricStreamResult:
    """Get metric stream.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = client.get_metric_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get metric stream") from exc
    return GetMetricStreamResult(
        arn=resp.get("Arn"),
        name=resp.get("Name"),
        include_filters=resp.get("IncludeFilters"),
        exclude_filters=resp.get("ExcludeFilters"),
        firehose_arn=resp.get("FirehoseArn"),
        role_arn=resp.get("RoleArn"),
        state=resp.get("State"),
        creation_date=resp.get("CreationDate"),
        last_update_date=resp.get("LastUpdateDate"),
        output_format=resp.get("OutputFormat"),
        statistics_configurations=resp.get("StatisticsConfigurations"),
        include_linked_accounts_metrics=resp.get("IncludeLinkedAccountsMetrics"),
    )


def get_metric_widget_image(
    metric_widget: str,
    *,
    output_format: str | None = None,
    region_name: str | None = None,
) -> GetMetricWidgetImageResult:
    """Get metric widget image.

    Args:
        metric_widget: Metric widget.
        output_format: Output format.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MetricWidget"] = metric_widget
    if output_format is not None:
        kwargs["OutputFormat"] = output_format
    try:
        resp = client.get_metric_widget_image(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get metric widget image") from exc
    return GetMetricWidgetImageResult(
        metric_widget_image=resp.get("MetricWidgetImage"),
    )


def list_dashboards(
    *,
    dashboard_name_prefix: str | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDashboardsResult:
    """List dashboards.

    Args:
        dashboard_name_prefix: Dashboard name prefix.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if dashboard_name_prefix is not None:
        kwargs["DashboardNamePrefix"] = dashboard_name_prefix
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_dashboards(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list dashboards") from exc
    return ListDashboardsResult(
        dashboard_entries=resp.get("DashboardEntries"),
        next_token=resp.get("NextToken"),
    )


def list_managed_insight_rules(
    resource_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListManagedInsightRulesResult:
    """List managed insight rules.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_managed_insight_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list managed insight rules") from exc
    return ListManagedInsightRulesResult(
        managed_rules=resp.get("ManagedRules"),
        next_token=resp.get("NextToken"),
    )


def list_metric_streams(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListMetricStreamsResult:
    """List metric streams.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_metric_streams(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list metric streams") from exc
    return ListMetricStreamsResult(
        next_token=resp.get("NextToken"),
        entries=resp.get("Entries"),
    )


def list_metrics(
    *,
    namespace: str | None = None,
    metric_name: str | None = None,
    dimensions: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    recently_active: str | None = None,
    include_linked_accounts: bool | None = None,
    owning_account: str | None = None,
    region_name: str | None = None,
) -> ListMetricsResult:
    """List metrics.

    Args:
        namespace: Namespace.
        metric_name: Metric name.
        dimensions: Dimensions.
        next_token: Next token.
        recently_active: Recently active.
        include_linked_accounts: Include linked accounts.
        owning_account: Owning account.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if metric_name is not None:
        kwargs["MetricName"] = metric_name
    if dimensions is not None:
        kwargs["Dimensions"] = dimensions
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if recently_active is not None:
        kwargs["RecentlyActive"] = recently_active
    if include_linked_accounts is not None:
        kwargs["IncludeLinkedAccounts"] = include_linked_accounts
    if owning_account is not None:
        kwargs["OwningAccount"] = owning_account
    try:
        resp = client.list_metrics(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list metrics") from exc
    return ListMetricsResult(
        metrics=resp.get("Metrics"),
        next_token=resp.get("NextToken"),
        owning_accounts=resp.get("OwningAccounts"),
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
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def put_anomaly_detector(
    *,
    namespace: str | None = None,
    metric_name: str | None = None,
    dimensions: list[dict[str, Any]] | None = None,
    stat: str | None = None,
    configuration: dict[str, Any] | None = None,
    metric_characteristics: dict[str, Any] | None = None,
    single_metric_anomaly_detector: dict[str, Any] | None = None,
    metric_math_anomaly_detector: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put anomaly detector.

    Args:
        namespace: Namespace.
        metric_name: Metric name.
        dimensions: Dimensions.
        stat: Stat.
        configuration: Configuration.
        metric_characteristics: Metric characteristics.
        single_metric_anomaly_detector: Single metric anomaly detector.
        metric_math_anomaly_detector: Metric math anomaly detector.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if metric_name is not None:
        kwargs["MetricName"] = metric_name
    if dimensions is not None:
        kwargs["Dimensions"] = dimensions
    if stat is not None:
        kwargs["Stat"] = stat
    if configuration is not None:
        kwargs["Configuration"] = configuration
    if metric_characteristics is not None:
        kwargs["MetricCharacteristics"] = metric_characteristics
    if single_metric_anomaly_detector is not None:
        kwargs["SingleMetricAnomalyDetector"] = single_metric_anomaly_detector
    if metric_math_anomaly_detector is not None:
        kwargs["MetricMathAnomalyDetector"] = metric_math_anomaly_detector
    try:
        client.put_anomaly_detector(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put anomaly detector") from exc
    return None


def put_composite_alarm(
    alarm_name: str,
    alarm_rule: str,
    *,
    actions_enabled: bool | None = None,
    alarm_actions: list[str] | None = None,
    alarm_description: str | None = None,
    insufficient_data_actions: list[str] | None = None,
    ok_actions: list[str] | None = None,
    tags: list[dict[str, Any]] | None = None,
    actions_suppressor: str | None = None,
    actions_suppressor_wait_period: int | None = None,
    actions_suppressor_extension_period: int | None = None,
    region_name: str | None = None,
) -> None:
    """Put composite alarm.

    Args:
        alarm_name: Alarm name.
        alarm_rule: Alarm rule.
        actions_enabled: Actions enabled.
        alarm_actions: Alarm actions.
        alarm_description: Alarm description.
        insufficient_data_actions: Insufficient data actions.
        ok_actions: Ok actions.
        tags: Tags.
        actions_suppressor: Actions suppressor.
        actions_suppressor_wait_period: Actions suppressor wait period.
        actions_suppressor_extension_period: Actions suppressor extension period.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmName"] = alarm_name
    kwargs["AlarmRule"] = alarm_rule
    if actions_enabled is not None:
        kwargs["ActionsEnabled"] = actions_enabled
    if alarm_actions is not None:
        kwargs["AlarmActions"] = alarm_actions
    if alarm_description is not None:
        kwargs["AlarmDescription"] = alarm_description
    if insufficient_data_actions is not None:
        kwargs["InsufficientDataActions"] = insufficient_data_actions
    if ok_actions is not None:
        kwargs["OKActions"] = ok_actions
    if tags is not None:
        kwargs["Tags"] = tags
    if actions_suppressor is not None:
        kwargs["ActionsSuppressor"] = actions_suppressor
    if actions_suppressor_wait_period is not None:
        kwargs["ActionsSuppressorWaitPeriod"] = actions_suppressor_wait_period
    if actions_suppressor_extension_period is not None:
        kwargs["ActionsSuppressorExtensionPeriod"] = actions_suppressor_extension_period
    try:
        client.put_composite_alarm(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put composite alarm") from exc
    return None


def put_dashboard(
    dashboard_name: str,
    dashboard_body: str,
    region_name: str | None = None,
) -> PutDashboardResult:
    """Put dashboard.

    Args:
        dashboard_name: Dashboard name.
        dashboard_body: Dashboard body.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DashboardName"] = dashboard_name
    kwargs["DashboardBody"] = dashboard_body
    try:
        resp = client.put_dashboard(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put dashboard") from exc
    return PutDashboardResult(
        dashboard_validation_messages=resp.get("DashboardValidationMessages"),
    )


def put_insight_rule(
    rule_name: str,
    rule_definition: str,
    *,
    rule_state: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    apply_on_transformed_logs: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put insight rule.

    Args:
        rule_name: Rule name.
        rule_definition: Rule definition.
        rule_state: Rule state.
        tags: Tags.
        apply_on_transformed_logs: Apply on transformed logs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleName"] = rule_name
    kwargs["RuleDefinition"] = rule_definition
    if rule_state is not None:
        kwargs["RuleState"] = rule_state
    if tags is not None:
        kwargs["Tags"] = tags
    if apply_on_transformed_logs is not None:
        kwargs["ApplyOnTransformedLogs"] = apply_on_transformed_logs
    try:
        client.put_insight_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put insight rule") from exc
    return None


def put_managed_insight_rules(
    managed_rules: list[dict[str, Any]],
    region_name: str | None = None,
) -> PutManagedInsightRulesResult:
    """Put managed insight rules.

    Args:
        managed_rules: Managed rules.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ManagedRules"] = managed_rules
    try:
        resp = client.put_managed_insight_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put managed insight rules") from exc
    return PutManagedInsightRulesResult(
        failures=resp.get("Failures"),
    )


def put_metric_alarm(
    alarm_name: str,
    evaluation_periods: int,
    comparison_operator: str,
    *,
    alarm_description: str | None = None,
    actions_enabled: bool | None = None,
    ok_actions: list[str] | None = None,
    alarm_actions: list[str] | None = None,
    insufficient_data_actions: list[str] | None = None,
    metric_name: str | None = None,
    namespace: str | None = None,
    statistic: str | None = None,
    extended_statistic: str | None = None,
    dimensions: list[dict[str, Any]] | None = None,
    period: int | None = None,
    unit: str | None = None,
    datapoints_to_alarm: int | None = None,
    threshold: float | None = None,
    treat_missing_data: str | None = None,
    evaluate_low_sample_count_percentile: str | None = None,
    metrics: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    threshold_metric_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put metric alarm.

    Args:
        alarm_name: Alarm name.
        evaluation_periods: Evaluation periods.
        comparison_operator: Comparison operator.
        alarm_description: Alarm description.
        actions_enabled: Actions enabled.
        ok_actions: Ok actions.
        alarm_actions: Alarm actions.
        insufficient_data_actions: Insufficient data actions.
        metric_name: Metric name.
        namespace: Namespace.
        statistic: Statistic.
        extended_statistic: Extended statistic.
        dimensions: Dimensions.
        period: Period.
        unit: Unit.
        datapoints_to_alarm: Datapoints to alarm.
        threshold: Threshold.
        treat_missing_data: Treat missing data.
        evaluate_low_sample_count_percentile: Evaluate low sample count percentile.
        metrics: Metrics.
        tags: Tags.
        threshold_metric_id: Threshold metric id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmName"] = alarm_name
    kwargs["EvaluationPeriods"] = evaluation_periods
    kwargs["ComparisonOperator"] = comparison_operator
    if alarm_description is not None:
        kwargs["AlarmDescription"] = alarm_description
    if actions_enabled is not None:
        kwargs["ActionsEnabled"] = actions_enabled
    if ok_actions is not None:
        kwargs["OKActions"] = ok_actions
    if alarm_actions is not None:
        kwargs["AlarmActions"] = alarm_actions
    if insufficient_data_actions is not None:
        kwargs["InsufficientDataActions"] = insufficient_data_actions
    if metric_name is not None:
        kwargs["MetricName"] = metric_name
    if namespace is not None:
        kwargs["Namespace"] = namespace
    if statistic is not None:
        kwargs["Statistic"] = statistic
    if extended_statistic is not None:
        kwargs["ExtendedStatistic"] = extended_statistic
    if dimensions is not None:
        kwargs["Dimensions"] = dimensions
    if period is not None:
        kwargs["Period"] = period
    if unit is not None:
        kwargs["Unit"] = unit
    if datapoints_to_alarm is not None:
        kwargs["DatapointsToAlarm"] = datapoints_to_alarm
    if threshold is not None:
        kwargs["Threshold"] = threshold
    if treat_missing_data is not None:
        kwargs["TreatMissingData"] = treat_missing_data
    if evaluate_low_sample_count_percentile is not None:
        kwargs["EvaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile
    if metrics is not None:
        kwargs["Metrics"] = metrics
    if tags is not None:
        kwargs["Tags"] = tags
    if threshold_metric_id is not None:
        kwargs["ThresholdMetricId"] = threshold_metric_id
    try:
        client.put_metric_alarm(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put metric alarm") from exc
    return None


def put_metric_data(
    namespace: str,
    *,
    metric_data: list[dict[str, Any]] | None = None,
    entity_metric_data: list[dict[str, Any]] | None = None,
    strict_entity_validation: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Put metric data.

    Args:
        namespace: Namespace.
        metric_data: Metric data.
        entity_metric_data: Entity metric data.
        strict_entity_validation: Strict entity validation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Namespace"] = namespace
    if metric_data is not None:
        kwargs["MetricData"] = metric_data
    if entity_metric_data is not None:
        kwargs["EntityMetricData"] = entity_metric_data
    if strict_entity_validation is not None:
        kwargs["StrictEntityValidation"] = strict_entity_validation
    try:
        client.put_metric_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put metric data") from exc
    return None


def put_metric_stream(
    name: str,
    firehose_arn: str,
    role_arn: str,
    output_format: str,
    *,
    include_filters: list[dict[str, Any]] | None = None,
    exclude_filters: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    statistics_configurations: list[dict[str, Any]] | None = None,
    include_linked_accounts_metrics: bool | None = None,
    region_name: str | None = None,
) -> PutMetricStreamResult:
    """Put metric stream.

    Args:
        name: Name.
        firehose_arn: Firehose arn.
        role_arn: Role arn.
        output_format: Output format.
        include_filters: Include filters.
        exclude_filters: Exclude filters.
        tags: Tags.
        statistics_configurations: Statistics configurations.
        include_linked_accounts_metrics: Include linked accounts metrics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["FirehoseArn"] = firehose_arn
    kwargs["RoleArn"] = role_arn
    kwargs["OutputFormat"] = output_format
    if include_filters is not None:
        kwargs["IncludeFilters"] = include_filters
    if exclude_filters is not None:
        kwargs["ExcludeFilters"] = exclude_filters
    if tags is not None:
        kwargs["Tags"] = tags
    if statistics_configurations is not None:
        kwargs["StatisticsConfigurations"] = statistics_configurations
    if include_linked_accounts_metrics is not None:
        kwargs["IncludeLinkedAccountsMetrics"] = include_linked_accounts_metrics
    try:
        resp = client.put_metric_stream(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put metric stream") from exc
    return PutMetricStreamResult(
        arn=resp.get("Arn"),
    )


def set_alarm_state(
    alarm_name: str,
    state_value: str,
    state_reason: str,
    *,
    state_reason_data: str | None = None,
    region_name: str | None = None,
) -> None:
    """Set alarm state.

    Args:
        alarm_name: Alarm name.
        state_value: State value.
        state_reason: State reason.
        state_reason_data: State reason data.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AlarmName"] = alarm_name
    kwargs["StateValue"] = state_value
    kwargs["StateReason"] = state_reason
    if state_reason_data is not None:
        kwargs["StateReasonData"] = state_reason_data
    try:
        client.set_alarm_state(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to set alarm state") from exc
    return None


def start_metric_streams(
    names: list[str],
    region_name: str | None = None,
) -> None:
    """Start metric streams.

    Args:
        names: Names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Names"] = names
    try:
        client.start_metric_streams(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start metric streams") from exc
    return None


def stop_metric_streams(
    names: list[str],
    region_name: str | None = None,
) -> None:
    """Stop metric streams.

    Args:
        names: Names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Names"] = names
    try:
        client.stop_metric_streams(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop metric streams") from exc
    return None


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
    client = get_client("cloudwatch", region_name)
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
    client = get_client("cloudwatch", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
