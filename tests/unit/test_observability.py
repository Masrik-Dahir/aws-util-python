"""Tests for aws_util.observability module."""
from __future__ import annotations

import json
import time
from typing import Any
from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError

from aws_util.observability import (
    AlarmFactoryResult,
    CanaryResult,
    DMSMonitorResult,
    DashboardResult,
    EMFMetricResult,
    ErrorAggregatorResult,
    ErrorDigest,
    HealthEventResult,
    KinesisAlarmResult,
    LogInsightsQueryResult,
    QuotaMonitorResult,
    ServiceMapNode,
    ServiceMapResult,
    StructuredLogEntry,
    StructuredLogger,
    TraceResult,
    _hash_error,
    _is_error_line,
    aggregate_errors,
    batch_put_trace_segments,
    build_service_map,
    create_canary,
    create_dlq_depth_alarm,
    create_lambda_alarms,
    create_xray_trace,
    delete_canary,
    dms_task_monitor,
    emit_emf_metric,
    emit_emf_metrics_batch,
    generate_lambda_dashboard,
    get_trace_summaries,
    health_event_to_teams,
    kinesis_analytics_alarm_manager,
    run_log_insights_query,
    service_quota_monitor,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str, message: str = "error") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}}, "Op"
    )


class _FakeLambdaContext:
    """Minimal Lambda context stub."""

    def __init__(
        self,
        request_id: str = "req-123",
        function_name: str = "my-func",
    ) -> None:
        self.aws_request_id = request_id
        self.function_name = function_name


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_structured_log_entry(self) -> None:
        e = StructuredLogEntry(
            level="INFO", message="hello", timestamp="2024-01-01T00:00:00Z"
        )
        assert e.level == "INFO"
        assert e.extra == {}

    def test_trace_result(self) -> None:
        r = TraceResult(segment_id="abc", trace_id="1-2-3")
        assert r.sampled is True

    def test_emf_metric_result(self) -> None:
        r = EMFMetricResult(
            namespace="NS", metric_name="M", value=1.0
        )
        assert r.emitted is True
        assert r.unit == "None"
        assert r.dimensions == {}

    def test_alarm_factory_result(self) -> None:
        r = AlarmFactoryResult(
            alarm_name="a", topic_arn="t", metric_name="m"
        )
        assert r.created is True

    def test_log_insights_query_result(self) -> None:
        r = LogInsightsQueryResult(
            query_id="q1", status="Complete"
        )
        assert r.results == []
        assert r.statistics == {}

    def test_dashboard_result(self) -> None:
        r = DashboardResult(dashboard_name="d")
        assert r.dashboard_arn == ""
        assert r.function_names == []

    def test_error_digest(self) -> None:
        d = ErrorDigest(
            error_hash="abc", message="fail", count=3
        )
        assert d.first_seen == ""
        assert d.last_seen == ""

    def test_error_aggregator_result(self) -> None:
        r = ErrorAggregatorResult(
            log_group="/test", total_errors=0, unique_errors=0
        )
        assert r.digests == []
        assert r.notification_sent is False

    def test_canary_result(self) -> None:
        r = CanaryResult(
            canary_name="c", endpoint="http://x", status="READY"
        )
        assert r.created is True

    def test_service_map_node(self) -> None:
        n = ServiceMapNode(name="svc")
        assert n.service_type == ""
        assert n.edges == []

    def test_service_map_result(self) -> None:
        r = ServiceMapResult()
        assert r.nodes == []
        assert r.start_time == ""
        assert r.end_time == ""


# ---------------------------------------------------------------------------
# 1. Structured Logger
# ---------------------------------------------------------------------------


class TestStructuredLogger:
    def test_info(self, capsys: pytest.CaptureFixture[str]) -> None:
        logger = StructuredLogger(service_name="my-svc")
        entry = logger.info("hello world")
        assert entry.level == "INFO"
        assert entry.message == "hello world"
        assert entry.cold_start is True
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert parsed["message"] == "hello world"
        assert parsed["service"] == "my-svc"

    def test_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        logger = StructuredLogger()
        entry = logger.error("something broke", extra={"code": 500})
        assert entry.level == "ERROR"
        assert entry.extra == {"code": 500}
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert parsed["extra"]["code"] == 500

    def test_warning(self, capsys: pytest.CaptureFixture[str]) -> None:
        logger = StructuredLogger()
        entry = logger.warning("caution")
        assert entry.level == "WARNING"
        capsys.readouterr()

    def test_debug(self, capsys: pytest.CaptureFixture[str]) -> None:
        logger = StructuredLogger()
        entry = logger.debug("trace detail")
        assert entry.level == "DEBUG"
        capsys.readouterr()

    def test_inject_lambda_context(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        logger = StructuredLogger()
        ctx = _FakeLambdaContext()
        logger.inject_lambda_context(ctx)
        entry = logger.info("with context")
        assert entry.request_id == "req-123"
        assert entry.function_name == "my-func"
        capsys.readouterr()

    def test_cold_start_tracked(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        logger = StructuredLogger()
        first = logger.info("first")
        assert first.cold_start is True
        second = logger.info("second")
        assert second.cold_start is False
        capsys.readouterr()

    def test_set_correlation_id(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        logger = StructuredLogger()
        logger.set_correlation_id("corr-abc")
        entry = logger.info("correlated")
        assert entry.correlation_id == "corr-abc"
        capsys.readouterr()

    def test_inject_lambda_context_missing_attrs(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        logger = StructuredLogger()
        bare_ctx = object()  # no aws_request_id or function_name
        logger.inject_lambda_context(bare_ctx)
        entry = logger.info("bare context")
        assert entry.request_id == ""
        assert entry.function_name == ""
        capsys.readouterr()

    def test_no_service_name_omits_key(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        logger = StructuredLogger()
        logger.info("no service")
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert "service" not in parsed


# ---------------------------------------------------------------------------
# 2. Distributed Tracer
# ---------------------------------------------------------------------------


class TestDistributedTracer:
    @patch("aws_util.observability.get_client")
    def test_create_xray_trace(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        result = create_xray_trace(
            "test-segment",
            annotations={"key": "val"},
            metadata={"data": 123},
        )
        assert isinstance(result, TraceResult)
        assert result.sampled is True
        assert result.segment_id != ""
        assert result.trace_id.startswith("1-")
        mock_client.put_trace_segments.assert_called_once()

    @patch("aws_util.observability.get_client")
    def test_create_xray_trace_no_extras(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        result = create_xray_trace("simple-segment")
        assert isinstance(result, TraceResult)
        mock_client.put_trace_segments.assert_called_once()

    @patch("aws_util.observability.get_client")
    def test_create_xray_trace_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.put_trace_segments.side_effect = _client_error(
            "ThrottledException"
        )
        mock_gc.return_value = mock_client
        with pytest.raises(RuntimeError, match="Failed to create X-Ray trace"):
            create_xray_trace("fail-segment")

    @patch("aws_util.observability.get_client")
    def test_batch_put_trace_segments(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        segs = [
            {
                "name": "seg1",
                "id": "aaa",
                "trace_id": "1-abc",
                "start_time": 1.0,
                "end_time": 2.0,
            },
            {
                "name": "seg2",
                "id": "bbb",
                "trace_id": "1-def",
                "start_time": 1.0,
                "end_time": 2.0,
            },
        ]
        results = batch_put_trace_segments(segs)
        assert len(results) == 2
        assert results[0].segment_id == "aaa"
        assert results[1].trace_id == "1-def"

    @patch("aws_util.observability.get_client")
    def test_batch_put_trace_segments_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.put_trace_segments.side_effect = _client_error(
            "ThrottledException"
        )
        mock_gc.return_value = mock_client
        with pytest.raises(RuntimeError, match="Failed to batch put"):
            batch_put_trace_segments([{"id": "a", "trace_id": "t"}])


# ---------------------------------------------------------------------------
# 3. Custom Metric Emitter (EMF)
# ---------------------------------------------------------------------------


class TestEMFMetricEmitter:
    def test_emit_emf_metric(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = emit_emf_metric(
            "MyApp",
            "Latency",
            42.5,
            unit="Milliseconds",
            dimensions={"env": "prod"},
        )
        assert isinstance(result, EMFMetricResult)
        assert result.namespace == "MyApp"
        assert result.value == 42.5
        assert result.dimensions == {"env": "prod"}
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert parsed["_aws"]["CloudWatchMetrics"][0]["Namespace"] == "MyApp"
        assert parsed["Latency"] == 42.5
        assert parsed["env"] == "prod"

    def test_emit_emf_metric_no_dimensions(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        result = emit_emf_metric("NS", "Count", 1.0)
        assert result.dimensions == {}
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert parsed["_aws"]["CloudWatchMetrics"][0]["Dimensions"] == []

    def test_emit_emf_metrics_batch(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        metrics = [
            {"name": "Latency", "value": 10.0, "unit": "Milliseconds"},
            {"name": "ErrorCount", "value": 2.0},
        ]
        results = emit_emf_metrics_batch(
            "MyApp", metrics, dimensions={"env": "prod"}
        )
        assert len(results) == 2
        assert results[0].metric_name == "Latency"
        assert results[1].unit == "None"
        out = capsys.readouterr().out
        parsed = json.loads(out)
        assert parsed["Latency"] == 10.0
        assert parsed["ErrorCount"] == 2.0

    def test_emit_emf_metrics_batch_no_dimensions(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        metrics = [{"name": "M1", "value": 5.0}]
        results = emit_emf_metrics_batch("NS", metrics)
        assert len(results) == 1
        assert results[0].dimensions == {}
        capsys.readouterr()


# ---------------------------------------------------------------------------
# 4. Alarm Factory
# ---------------------------------------------------------------------------


class TestAlarmFactory:
    def test_create_lambda_alarms(self) -> None:
        sns = boto3.client("sns", region_name=REGION)
        topic_arn = sns.create_topic(Name="alarm-topic")["TopicArn"]

        results = create_lambda_alarms(
            "my-func", topic_arn, region_name=REGION
        )
        assert len(results) == 3
        names = [r.alarm_name for r in results]
        assert "my-func-Errors" in names
        assert "my-func-Duration-P99" in names
        assert "my-func-Throttles" in names
        for r in results:
            assert r.topic_arn == topic_arn
            assert r.created is True

    def test_create_lambda_alarms_custom_thresholds(self) -> None:
        sns = boto3.client("sns", region_name=REGION)
        topic_arn = sns.create_topic(Name="t")["TopicArn"]

        results = create_lambda_alarms(
            "func2",
            topic_arn,
            error_threshold=5,
            duration_p99_threshold=5000.0,
            throttle_threshold=10,
            evaluation_periods=3,
            period=60,
            region_name=REGION,
        )
        assert len(results) == 3

    @patch("aws_util.observability.get_client")
    def test_create_lambda_alarms_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.put_metric_alarm.side_effect = _client_error(
            "LimitExceededException"
        )
        mock_gc.return_value = mock_client
        with pytest.raises(RuntimeError, match="Failed to create alarm"):
            create_lambda_alarms("fn", "arn:aws:sns:us-east-1:123:t")

    def test_create_dlq_depth_alarm(self) -> None:
        sns = boto3.client("sns", region_name=REGION)
        topic_arn = sns.create_topic(Name="dlq-topic")["TopicArn"]

        result = create_dlq_depth_alarm(
            "my-dlq", topic_arn, threshold=5, region_name=REGION
        )
        assert isinstance(result, AlarmFactoryResult)
        assert result.alarm_name == "my-dlq-DLQ-Depth"
        assert result.created is True

    @patch("aws_util.observability.get_client")
    def test_create_dlq_depth_alarm_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.put_metric_alarm.side_effect = _client_error(
            "LimitExceededException"
        )
        mock_gc.return_value = mock_client
        with pytest.raises(RuntimeError, match="Failed to create DLQ"):
            create_dlq_depth_alarm("q", "arn:aws:sns:us-east-1:123:t")


# ---------------------------------------------------------------------------
# 5. Log Insights Query Runner
# ---------------------------------------------------------------------------


class TestLogInsightsQueryRunner:
    @patch("aws_util.observability.get_client")
    def test_run_query_complete(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.return_value = {"queryId": "q-123"}
        mock_client.get_query_results.return_value = {
            "status": "Complete",
            "results": [
                [
                    {"field": "@message", "value": "hello"},
                    {"field": "@timestamp", "value": "2024-01-01"},
                ]
            ],
            "statistics": {
                "recordsMatched": 10.0,
                "recordsScanned": 100.0,
            },
        }

        result = run_log_insights_query(
            ["/aws/lambda/fn"],
            "fields @message",
            start_time=1000,
            end_time=2000,
        )
        assert result.query_id == "q-123"
        assert result.status == "Complete"
        assert len(result.results) == 1
        assert result.results[0]["@message"] == "hello"
        assert result.statistics["recordsMatched"] == 10.0

    @patch("aws_util.observability.get_client")
    def test_run_query_polls_until_complete(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.return_value = {"queryId": "q-456"}
        mock_client.get_query_results.side_effect = [
            {"status": "Running", "results": []},
            {"status": "Complete", "results": [], "statistics": {}},
        ]

        result = run_log_insights_query(
            ["/test"],
            "fields @message",
            start_time=1,
            end_time=2,
            poll_interval=0.01,
        )
        assert result.status == "Complete"
        assert mock_client.get_query_results.call_count == 2

    @patch("aws_util.observability.get_client")
    def test_run_query_failed(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.return_value = {"queryId": "q-fail"}
        mock_client.get_query_results.return_value = {
            "status": "Failed",
            "results": [],
        }

        with pytest.raises(RuntimeError, match="query .* failed"):
            run_log_insights_query(
                ["/test"], "bad query", start_time=1, end_time=2
            )

    @patch("aws_util.observability.time.monotonic")
    @patch("aws_util.observability.time.sleep")
    @patch("aws_util.observability.get_client")
    def test_run_query_timeout(
        self,
        mock_gc: MagicMock,
        mock_sleep: MagicMock,
        mock_monotonic: MagicMock,
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.return_value = {"queryId": "q-slow"}
        mock_client.get_query_results.return_value = {
            "status": "Running",
            "results": [],
        }
        # First call sets deadline (0 + 60 = 60), subsequent calls exceed it
        mock_monotonic.side_effect = [0.0, 0.1, 999.0]

        with pytest.raises(TimeoutError, match="did not complete"):
            run_log_insights_query(
                ["/test"],
                "fields @message",
                start_time=1,
                end_time=2,
                poll_interval=0.01,
                max_wait=60.0,
            )

    @patch("aws_util.observability.get_client")
    def test_run_query_start_error(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.side_effect = _client_error(
            "InvalidParameterException"
        )

        with pytest.raises(RuntimeError, match="Failed to start"):
            run_log_insights_query(
                ["/test"], "bad", start_time=1, end_time=2
            )

    @patch("aws_util.observability.get_client")
    def test_run_query_get_results_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.return_value = {"queryId": "q-err"}
        mock_client.get_query_results.side_effect = _client_error(
            "ServiceUnavailableException"
        )

        with pytest.raises(RuntimeError, match="Failed to get query results"):
            run_log_insights_query(
                ["/test"], "fields @message", start_time=1, end_time=2
            )

    @patch("aws_util.observability.get_client")
    def test_run_query_cancelled(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.start_query.return_value = {"queryId": "q-cancel"}
        mock_client.get_query_results.return_value = {
            "status": "Cancelled",
            "results": [],
            "statistics": {},
        }

        result = run_log_insights_query(
            ["/test"], "fields @message", start_time=1, end_time=2
        )
        assert result.status == "Cancelled"


# ---------------------------------------------------------------------------
# 6. Dashboard Generator
# ---------------------------------------------------------------------------


class TestDashboardGenerator:
    def test_generate_dashboard(self) -> None:
        result = generate_lambda_dashboard(
            "test-dash",
            ["func-a", "func-b"],
            region_name=REGION,
        )
        assert isinstance(result, DashboardResult)
        assert result.dashboard_name == "test-dash"
        assert result.function_names == ["func-a", "func-b"]

    def test_generate_dashboard_single_function(self) -> None:
        result = generate_lambda_dashboard(
            "single-dash",
            ["my-func"],
            region_name=REGION,
        )
        assert len(result.function_names) == 1

    @patch("aws_util.observability.get_client")
    def test_generate_dashboard_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.put_dashboard.side_effect = _client_error(
            "InternalServiceFault"
        )
        mock_gc.return_value = mock_client
        with pytest.raises(RuntimeError, match="Failed to create dashboard"):
            generate_lambda_dashboard("d", ["fn"])


# ---------------------------------------------------------------------------
# 7. Error Aggregator
# ---------------------------------------------------------------------------


class TestErrorAggregator:
    def test_aggregate_no_errors(self) -> None:
        logs = boto3.client("logs", region_name=REGION)
        logs.create_log_group(logGroupName="/test/app")
        logs.create_log_stream(
            logGroupName="/test/app", logStreamName="stream-1"
        )
        logs.put_log_events(
            logGroupName="/test/app",
            logStreamName="stream-1",
            logEvents=[
                {"timestamp": 1000, "message": "all good"},
            ],
        )

        result = aggregate_errors(
            "/test/app",
            start_time=0,
            end_time=9999999,
            region_name=REGION,
        )
        assert result.total_errors == 0
        assert result.unique_errors == 0
        assert result.notification_sent is False

    @patch("aws_util.observability.get_client")
    def test_aggregate_with_errors(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.describe_log_streams.return_value = {
            "logStreams": [{"logStreamName": "s1"}]
        }
        mock_client.get_log_events.return_value = {
            "events": [
                {"timestamp": 1000, "message": "ERROR: something failed"},
                {"timestamp": 1001, "message": "ok line"},
                {"timestamp": 1002, "message": "Exception in handler"},
                {"timestamp": 1003, "message": "Traceback (most recent)"},
            ]
        }
        mock_gc.return_value = mock_client

        result = aggregate_errors(
            "/test/errs",
            start_time=0,
            end_time=9999999,
        )
        assert result.total_errors == 3
        assert result.unique_errors >= 1
        assert len(result.digests) >= 1

    @patch("aws_util.observability.get_client")
    def test_aggregate_with_sns_notification(
        self, mock_gc: MagicMock
    ) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_streams.return_value = {
            "logStreams": [{"logStreamName": "s1"}]
        }
        mock_logs.get_log_events.return_value = {
            "events": [
                {"timestamp": 1000, "message": "ERROR: crash"},
            ]
        }
        mock_sns = MagicMock()
        mock_sns.publish.return_value = {}

        mock_gc.side_effect = [mock_logs, mock_sns]

        result = aggregate_errors(
            "/test/notify",
            start_time=0,
            end_time=9999999,
            sns_topic_arn="arn:aws:sns:us-east-1:123:err-digest",
        )
        assert result.notification_sent is True

    def test_aggregate_no_sns_when_no_errors(self) -> None:
        logs = boto3.client("logs", region_name=REGION)
        logs.create_log_group(logGroupName="/test/clean")
        logs.create_log_stream(
            logGroupName="/test/clean", logStreamName="s1"
        )
        logs.put_log_events(
            logGroupName="/test/clean",
            logStreamName="s1",
            logEvents=[
                {"timestamp": 1000, "message": "info: all ok"},
            ],
        )
        sns = boto3.client("sns", region_name=REGION)
        topic_arn = sns.create_topic(Name="no-notify")["TopicArn"]

        result = aggregate_errors(
            "/test/clean",
            start_time=0,
            end_time=9999999,
            sns_topic_arn=topic_arn,
            region_name=REGION,
        )
        assert result.notification_sent is False

    def test_aggregate_no_streams(self) -> None:
        logs = boto3.client("logs", region_name=REGION)
        logs.create_log_group(logGroupName="/test/empty")

        result = aggregate_errors(
            "/test/empty",
            start_time=0,
            end_time=9999999,
            region_name=REGION,
        )
        assert result.total_errors == 0

    @patch("aws_util.observability.get_client")
    def test_aggregate_describe_streams_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.describe_log_streams.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        mock_gc.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to describe"):
            aggregate_errors("/bad", start_time=0, end_time=1)

    @patch("aws_util.observability.get_client")
    def test_aggregate_get_events_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.describe_log_streams.return_value = {
            "logStreams": [{"logStreamName": "s1"}]
        }
        mock_client.get_log_events.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        mock_gc.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to get log events"):
            aggregate_errors("/bad", start_time=0, end_time=1)

    @patch("aws_util.observability.get_client")
    def test_aggregate_sns_publish_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_streams.return_value = {
            "logStreams": [{"logStreamName": "s1"}]
        }
        mock_logs.get_log_events.return_value = {
            "events": [
                {"timestamp": 1000, "message": "ERROR: boom"}
            ]
        }
        mock_sns = MagicMock()
        mock_sns.publish.side_effect = _client_error(
            "AuthorizationErrorException"
        )

        # Return logs client first, sns client second
        mock_gc.side_effect = [mock_logs, mock_sns]

        with pytest.raises(RuntimeError, match="Failed to publish error"):
            aggregate_errors(
                "/test",
                start_time=0,
                end_time=1,
                sns_topic_arn="arn:aws:sns:us-east-1:123:t",
            )

    @patch("aws_util.observability.get_client")
    def test_aggregate_duplicate_errors(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.describe_log_streams.return_value = {
            "logStreams": [{"logStreamName": "s1"}]
        }
        mock_client.get_log_events.return_value = {
            "events": [
                {"timestamp": 1000, "message": "ERROR: same error msg"},
                {"timestamp": 1001, "message": "ERROR: same error msg"},
                {"timestamp": 1002, "message": "ERROR: same error msg"},
            ]
        }
        mock_gc.return_value = mock_client

        result = aggregate_errors(
            "/test/dup",
            start_time=0,
            end_time=9999999,
        )
        assert result.total_errors == 3
        # Duplicates should be collapsed
        assert result.unique_errors == 1


# ---------------------------------------------------------------------------
# Error helper tests
# ---------------------------------------------------------------------------


class TestErrorHelpers:
    def test_is_error_line_error(self) -> None:
        assert _is_error_line("ERROR: something broke") is True

    def test_is_error_line_exception(self) -> None:
        assert _is_error_line("ValueError: bad value") is False
        assert _is_error_line("Exception in thread") is True

    def test_is_error_line_traceback(self) -> None:
        assert _is_error_line("Traceback (most recent call last):") is True

    def test_is_error_line_failed(self) -> None:
        assert _is_error_line("Task Failed successfully") is True

    def test_is_error_line_normal(self) -> None:
        assert _is_error_line("INFO: all good") is False

    def test_hash_error_deterministic(self) -> None:
        msg1 = "ERROR: something broke"
        msg2 = "ERROR: something broke"
        assert _hash_error(msg1) == _hash_error(msg2)

    def test_hash_error_strips_timestamps(self) -> None:
        msg1 = "2024-01-01T00:00:00 ERROR: broke"
        msg2 = "2024-06-15T12:30:00 ERROR: broke"
        assert _hash_error(msg1) == _hash_error(msg2)

    def test_hash_error_strips_uuids(self) -> None:
        msg1 = "req 12345678-1234-1234-1234-123456789abc ERROR"
        msg2 = "req abcdefab-abcd-abcd-abcd-abcdefabcdef ERROR"
        assert _hash_error(msg1) == _hash_error(msg2)


# ---------------------------------------------------------------------------
# 8. Canary Health Checker
# ---------------------------------------------------------------------------


class TestCanaryHealthChecker:
    @patch("aws_util.observability.get_client")
    def test_create_canary(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client

        result = create_canary(
            "my-canary",
            "https://api.example.com/health",
            "artifacts-bucket",
            execution_role_arn="arn:aws:iam::123:role/canary",
        )
        assert isinstance(result, CanaryResult)
        assert result.canary_name == "my-canary"
        assert result.status == "CREATING"
        assert result.created is True
        mock_client.create_canary.assert_called_once()

    @patch("aws_util.observability.get_client")
    def test_create_canary_custom_params(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client

        result = create_canary(
            "custom-canary",
            "https://example.com",
            "bucket",
            schedule_expression="rate(1 minute)",
            runtime_version="syn-python-selenium-2.0",
        )
        assert result.endpoint == "https://example.com"
        call_kwargs = mock_client.create_canary.call_args[1]
        assert call_kwargs["Schedule"]["Expression"] == "rate(1 minute)"

    @patch("aws_util.observability.get_client")
    def test_create_canary_error(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.create_canary.side_effect = _client_error(
            "ValidationException"
        )
        mock_gc.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to create canary"):
            create_canary("bad", "http://x", "bucket")

    @patch("aws_util.observability.get_client")
    def test_delete_canary(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client

        result = delete_canary("my-canary")
        assert result.status == "DELETED"
        assert result.created is False
        mock_client.delete_canary.assert_called_once_with(
            Name="my-canary"
        )

    @patch("aws_util.observability.get_client")
    def test_delete_canary_error(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_client.delete_canary.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        mock_gc.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to delete canary"):
            delete_canary("missing")


# ---------------------------------------------------------------------------
# 9. Service Map Builder
# ---------------------------------------------------------------------------


class TestServiceMapBuilder:
    @patch("aws_util.observability.get_client")
    def test_build_service_map(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.get_service_graph.return_value = {
            "Services": [
                {
                    "ReferenceId": 1,
                    "Name": "my-lambda",
                    "Type": "AWS::Lambda",
                    "Edges": [{"ReferenceId": 2}],
                },
                {
                    "ReferenceId": 2,
                    "Name": "my-dynamodb",
                    "Type": "AWS::DynamoDB",
                    "Edges": [],
                },
            ]
        }

        result = build_service_map(1000.0, 2000.0)
        assert isinstance(result, ServiceMapResult)
        assert len(result.nodes) == 2
        assert result.nodes[0].name == "my-lambda"
        assert "my-dynamodb" in result.nodes[0].edges
        assert result.nodes[1].edges == []

    @patch("aws_util.observability.get_client")
    def test_build_service_map_empty(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.get_service_graph.return_value = {"Services": []}

        result = build_service_map(1.0, 2.0)
        assert result.nodes == []

    @patch("aws_util.observability.get_client")
    def test_build_service_map_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.get_service_graph.side_effect = _client_error(
            "ThrottledException"
        )
        mock_gc.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to get X-Ray"):
            build_service_map(1.0, 2.0)

    @patch("aws_util.observability.get_client")
    def test_build_service_map_unresolved_edge(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.get_service_graph.return_value = {
            "Services": [
                {
                    "ReferenceId": 1,
                    "Name": "svc-a",
                    "Type": "AWS::Lambda",
                    "Edges": [{"ReferenceId": 99}],
                },
            ]
        }

        result = build_service_map(1.0, 2.0)
        # Edge with unresolved ReferenceId should not appear
        assert result.nodes[0].edges == []

    @patch("aws_util.observability.get_client")
    def test_get_trace_summaries(self, mock_gc: MagicMock) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.get_trace_summaries.return_value = {
            "TraceSummaries": [
                {"Id": "1-abc", "Duration": 0.5},
                {"Id": "1-def", "Duration": 1.2},
            ]
        }

        results = get_trace_summaries(1.0, 2.0)
        assert len(results) == 2
        assert results[0]["Id"] == "1-abc"

    @patch("aws_util.observability.get_client")
    def test_get_trace_summaries_with_filter(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.get_trace_summaries.return_value = {
            "TraceSummaries": [{"Id": "1-xyz"}]
        }

        results = get_trace_summaries(
            1.0, 2.0, filter_expression='service("my-svc")'
        )
        assert len(results) == 1
        call_kwargs = mock_client.get_trace_summaries.call_args[1]
        assert "FilterExpression" in call_kwargs

    @patch("aws_util.observability.get_client")
    def test_get_trace_summaries_no_filter(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_gc.return_value = mock_client
        mock_client.get_trace_summaries.return_value = {
            "TraceSummaries": []
        }

        results = get_trace_summaries(1.0, 2.0)
        assert results == []
        call_kwargs = mock_client.get_trace_summaries.call_args[1]
        assert "FilterExpression" not in call_kwargs

    @patch("aws_util.observability.get_client")
    def test_get_trace_summaries_error(
        self, mock_gc: MagicMock
    ) -> None:
        mock_client = MagicMock()
        mock_client.get_trace_summaries.side_effect = _client_error(
            "ThrottledException"
        )
        mock_gc.return_value = mock_client

        with pytest.raises(RuntimeError, match="Failed to get trace"):
            get_trace_summaries(1.0, 2.0)


# ---------------------------------------------------------------------------
# New model tests
# ---------------------------------------------------------------------------


import aws_util.observability as _obs_mod


class TestNewObservabilityModels:
    def test_kinesis_alarm_result(self) -> None:
        r = KinesisAlarmResult(
            application_status="RUNNING",
            alarms_created=2,
            alarm_names=["a1", "a2"],
        )
        assert r.alarms_created == 2

    def test_dms_monitor_result(self) -> None:
        r = DMSMonitorResult(
            task_status="running",
            tables_monitored=3,
            metrics_published=9,
            total_rows=100,
        )
        assert r.total_rows == 100

    def test_health_event_result(self) -> None:
        r = HealthEventResult(
            events_found=5,
            messages_sent=5,
            affected_accounts=["111", "222"],
        )
        assert len(r.affected_accounts) == 2

    def test_quota_monitor_result(self) -> None:
        r = QuotaMonitorResult(
            services_checked=2,
            quotas_near_limit=1,
            alarms_created=1,
        )
        assert r.services_checked == 2


# ---------------------------------------------------------------------------
# 10. kinesis_analytics_alarm_manager
# ---------------------------------------------------------------------------


class TestKinesisAnalyticsAlarmManager:
    def test_happy_path(self) -> None:
        kda_mock = MagicMock()
        cw_mock = MagicMock()
        kda_mock.describe_application.return_value = {
            "ApplicationDetail": {"ApplicationStatus": "RUNNING"},
        }
        cw_mock.put_metric_alarm.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return kda_mock if service == "kinesisanalyticsv2" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = kinesis_analytics_alarm_manager(
                application_name="my-kda-app",
                sns_topic_arn="arn:aws:sns:us-east-1:123:alerts",
                alarm_prefix="kda",
            )
        assert isinstance(result, KinesisAlarmResult)
        assert result.application_status == "RUNNING"
        assert result.alarms_created == 2
        assert len(result.alarm_names) == 2
        assert "kda-my-kda-app-MillisBehindLatest" in result.alarm_names
        assert "kda-my-kda-app-Records" in result.alarm_names

    def test_describe_application_error(self) -> None:
        kda_mock = MagicMock()
        kda_mock.describe_application.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return kda_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_application failed"):
                kinesis_analytics_alarm_manager("bad-app", "arn:sns", "pfx")

    def test_put_metric_alarm_error(self) -> None:
        kda_mock = MagicMock()
        cw_mock = MagicMock()
        kda_mock.describe_application.return_value = {
            "ApplicationDetail": {"ApplicationStatus": "RUNNING"},
        }
        cw_mock.put_metric_alarm.side_effect = _client_error(
            "LimitExceededException"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return kda_mock if service == "kinesisanalyticsv2" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="put_metric_alarm failed"):
                kinesis_analytics_alarm_manager("app", "arn:sns", "pfx")

    def test_unknown_status(self) -> None:
        kda_mock = MagicMock()
        cw_mock = MagicMock()
        kda_mock.describe_application.return_value = {
            "ApplicationDetail": {},
        }
        cw_mock.put_metric_alarm.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return kda_mock if service == "kinesisanalyticsv2" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = kinesis_analytics_alarm_manager("app", "arn:sns", "pfx")
        assert result.application_status == "UNKNOWN"


# ---------------------------------------------------------------------------
# 11. dms_task_monitor
# ---------------------------------------------------------------------------


class TestDMSTaskMonitor:
    def test_happy_path(self) -> None:
        dms_mock = MagicMock()
        cw_mock = MagicMock()
        dms_mock.describe_replication_tasks.return_value = {
            "ReplicationTasks": [{"Status": "running"}],
        }
        dms_mock.describe_table_statistics.return_value = {
            "TableStatistics": [
                {
                    "SchemaName": "public",
                    "TableName": "users",
                    "Inserts": 100,
                    "Deletes": 10,
                    "Updates": 50,
                },
                {
                    "SchemaName": "public",
                    "TableName": "orders",
                    "Inserts": 200,
                    "Deletes": 5,
                    "Updates": 30,
                },
            ],
        }
        cw_mock.put_metric_data.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return dms_mock if service == "dms" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = dms_task_monitor(
                replication_task_arn="arn:aws:dms:us-east-1:123:task:abc",
                metric_namespace="DMS/Monitor",
            )
        assert isinstance(result, DMSMonitorResult)
        assert result.task_status == "running"
        assert result.tables_monitored == 2
        assert result.metrics_published == 6  # 3 metrics per table * 2 tables
        assert result.total_rows == 395  # 100+10+50 + 200+5+30

    def test_no_tasks_found(self) -> None:
        dms_mock = MagicMock()
        cw_mock = MagicMock()
        dms_mock.describe_replication_tasks.return_value = {
            "ReplicationTasks": [],
        }
        dms_mock.describe_table_statistics.return_value = {
            "TableStatistics": [],
        }

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return dms_mock if service == "dms" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = dms_task_monitor("arn:task", "NS")
        assert result.task_status == "unknown"
        assert result.tables_monitored == 0

    def test_describe_tasks_error(self) -> None:
        dms_mock = MagicMock()
        dms_mock.describe_replication_tasks.side_effect = _client_error(
            "ResourceNotFoundFault"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return dms_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_replication_tasks failed"):
                dms_task_monitor("arn:bad", "NS")

    def test_describe_table_statistics_error(self) -> None:
        dms_mock = MagicMock()
        cw_mock = MagicMock()
        dms_mock.describe_replication_tasks.return_value = {
            "ReplicationTasks": [{"Status": "running"}],
        }
        dms_mock.describe_table_statistics.side_effect = _client_error(
            "ResourceNotFoundFault"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return dms_mock if service == "dms" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_table_statistics failed"):
                dms_task_monitor("arn:task", "NS")

    def test_put_metric_data_error(self) -> None:
        dms_mock = MagicMock()
        cw_mock = MagicMock()
        dms_mock.describe_replication_tasks.return_value = {
            "ReplicationTasks": [{"Status": "running"}],
        }
        dms_mock.describe_table_statistics.return_value = {
            "TableStatistics": [
                {"SchemaName": "s", "TableName": "t", "Inserts": 1, "Deletes": 0, "Updates": 0},
            ],
        }
        cw_mock.put_metric_data.side_effect = _client_error("InternalFailure")

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return dms_mock if service == "dms" else cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="put_metric_data failed"):
                dms_task_monitor("arn:task", "NS")


# ---------------------------------------------------------------------------
# 12. health_event_to_teams
# ---------------------------------------------------------------------------


class TestHealthEventToTeams:
    def test_happy_path(self) -> None:
        health_mock = MagicMock()
        orgs_mock = MagicMock()
        sqs_mock = MagicMock()

        health_mock.describe_events.return_value = {
            "events": [
                {
                    "arn": "arn:aws:health:us-east-1::event/EC2/issue/abc",
                    "service": "EC2",
                    "region": "us-east-1",
                    "statusCode": "open",
                    "startTime": "2026-04-15T00:00:00Z",
                },
            ],
        }
        health_mock.describe_affected_accounts.return_value = {
            "affectedAccounts": ["111222333444"],
        }
        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {"Accounts": [{"Id": "111222333444", "Name": "Production"}]},
        ]
        orgs_mock.get_paginator.return_value = paginator_mock
        sqs_mock.send_message.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "health":
                return health_mock
            if service == "organizations":
                return orgs_mock
            return sqs_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = health_event_to_teams(
                queue_url="https://sqs.us-east-1.amazonaws.com/123/health-queue",
                lookback_hours=24,
            )
        assert isinstance(result, HealthEventResult)
        assert result.events_found == 1
        assert result.messages_sent == 1
        assert "111222333444" in result.affected_accounts

    def test_no_events(self) -> None:
        health_mock = MagicMock()
        orgs_mock = MagicMock()
        sqs_mock = MagicMock()
        health_mock.describe_events.return_value = {"events": []}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "health":
                return health_mock
            if service == "organizations":
                return orgs_mock
            return sqs_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = health_event_to_teams("https://sqs/q")
        assert result.events_found == 0
        assert result.messages_sent == 0
        assert result.affected_accounts == []

    def test_describe_events_error(self) -> None:
        health_mock = MagicMock()
        orgs_mock = MagicMock()
        sqs_mock = MagicMock()
        health_mock.describe_events.side_effect = _client_error(
            "InvalidParameter"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "health":
                return health_mock
            if service == "organizations":
                return orgs_mock
            return sqs_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_events failed"):
                health_event_to_teams("https://sqs/q")

    def test_sqs_send_error(self) -> None:
        health_mock = MagicMock()
        orgs_mock = MagicMock()
        sqs_mock = MagicMock()
        health_mock.describe_events.return_value = {
            "events": [{"arn": "arn:event", "service": "EC2"}],
        }
        health_mock.describe_affected_accounts.return_value = {
            "affectedAccounts": [],
        }
        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [{"Accounts": []}]
        orgs_mock.get_paginator.return_value = paginator_mock
        sqs_mock.send_message.side_effect = _client_error(
            "AWS.SimpleQueueService.NonExistentQueue"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "health":
                return health_mock
            if service == "organizations":
                return orgs_mock
            return sqs_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="send_message failed"):
                health_event_to_teams("https://sqs/bad-q")

    def test_affected_accounts_error_continues(self) -> None:
        health_mock = MagicMock()
        orgs_mock = MagicMock()
        sqs_mock = MagicMock()
        health_mock.describe_events.return_value = {
            "events": [{"arn": "arn:event", "service": "EC2"}],
        }
        health_mock.describe_affected_accounts.side_effect = _client_error(
            "AccessDenied"
        )
        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [{"Accounts": []}]
        orgs_mock.get_paginator.return_value = paginator_mock
        sqs_mock.send_message.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "health":
                return health_mock
            if service == "organizations":
                return orgs_mock
            return sqs_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = health_event_to_teams("https://sqs/q")
        # Should succeed — affected_accounts error is silently caught
        assert result.events_found == 1
        assert result.messages_sent == 1

    def test_orgs_error_continues(self) -> None:
        health_mock = MagicMock()
        orgs_mock = MagicMock()
        sqs_mock = MagicMock()
        health_mock.describe_events.return_value = {
            "events": [{"arn": "arn:event"}],
        }
        health_mock.describe_affected_accounts.return_value = {
            "affectedAccounts": ["111"],
        }
        orgs_mock.get_paginator.side_effect = _client_error("AccessDenied")
        sqs_mock.send_message.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "health":
                return health_mock
            if service == "organizations":
                return orgs_mock
            return sqs_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = health_event_to_teams("https://sqs/q")
        # Organizations error silently caught
        assert result.events_found == 1


# ---------------------------------------------------------------------------
# 13. service_quota_monitor
# ---------------------------------------------------------------------------


class TestServiceQuotaMonitor:
    def test_happy_path(self) -> None:
        sq_mock = MagicMock()
        ddb_mock = MagicMock()
        cw_mock = MagicMock()

        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {
                "Quotas": [
                    {"QuotaCode": "L-1234", "Value": 100},
                    {"QuotaCode": "L-5678", "Value": 50},
                ],
            },
        ]
        sq_mock.get_paginator.return_value = paginator_mock
        ddb_mock.get_item.return_value = {"Item": {}}
        cw_mock.put_metric_alarm.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "service-quotas":
                return sq_mock
            if service == "dynamodb":
                return ddb_mock
            return cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = service_quota_monitor(
                service_codes=["lambda"],
                table_name="quota-thresholds",
                alarm_prefix="quota",
            )
        assert isinstance(result, QuotaMonitorResult)
        assert result.services_checked == 1
        assert result.alarms_created == 2
        assert result.quotas_near_limit == 2

    def test_custom_threshold_from_dynamodb(self) -> None:
        sq_mock = MagicMock()
        ddb_mock = MagicMock()
        cw_mock = MagicMock()

        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {"Quotas": [{"QuotaCode": "L-1234", "Value": 200}]},
        ]
        sq_mock.get_paginator.return_value = paginator_mock
        ddb_mock.get_item.return_value = {
            "Item": {"threshold_pct": {"N": "90"}},
        }
        cw_mock.put_metric_alarm.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "service-quotas":
                return sq_mock
            if service == "dynamodb":
                return ddb_mock
            return cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = service_quota_monitor(["ec2"], "tbl", "pfx")
        assert result.alarms_created == 1

    def test_zero_quota_value_skipped(self) -> None:
        sq_mock = MagicMock()
        ddb_mock = MagicMock()
        cw_mock = MagicMock()

        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {"Quotas": [{"QuotaCode": "L-0000", "Value": 0}]},
        ]
        sq_mock.get_paginator.return_value = paginator_mock

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "service-quotas":
                return sq_mock
            if service == "dynamodb":
                return ddb_mock
            return cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = service_quota_monitor(["ec2"], "tbl", "pfx")
        assert result.alarms_created == 0
        cw_mock.put_metric_alarm.assert_not_called()

    def test_list_service_quotas_error(self) -> None:
        sq_mock = MagicMock()
        paginator_mock = MagicMock()
        paginator_mock.paginate.side_effect = _client_error(
            "NoSuchResourceException"
        )
        sq_mock.get_paginator.return_value = paginator_mock

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            return sq_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="list_service_quotas failed"):
                service_quota_monitor(["bad-svc"], "tbl", "pfx")

    def test_put_metric_alarm_error(self) -> None:
        sq_mock = MagicMock()
        ddb_mock = MagicMock()
        cw_mock = MagicMock()

        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {"Quotas": [{"QuotaCode": "L-1234", "Value": 100}]},
        ]
        sq_mock.get_paginator.return_value = paginator_mock
        ddb_mock.get_item.return_value = {"Item": {}}
        cw_mock.put_metric_alarm.side_effect = _client_error(
            "LimitExceededException"
        )

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "service-quotas":
                return sq_mock
            if service == "dynamodb":
                return ddb_mock
            return cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="put_metric_alarm failed"):
                service_quota_monitor(["lambda"], "tbl", "pfx")

    def test_multiple_service_codes(self) -> None:
        sq_mock = MagicMock()
        ddb_mock = MagicMock()
        cw_mock = MagicMock()

        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {"Quotas": [{"QuotaCode": "L-1", "Value": 10}]},
        ]
        sq_mock.get_paginator.return_value = paginator_mock
        ddb_mock.get_item.return_value = {"Item": {}}
        cw_mock.put_metric_alarm.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "service-quotas":
                return sq_mock
            if service == "dynamodb":
                return ddb_mock
            return cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = service_quota_monitor(["ec2", "lambda", "s3"], "tbl", "pfx")
        assert result.services_checked == 3

    def test_ddb_get_item_error_continues(self) -> None:
        """DynamoDB get_item for custom threshold silently falls back to default."""
        sq_mock = MagicMock()
        ddb_mock = MagicMock()
        cw_mock = MagicMock()

        paginator_mock = MagicMock()
        paginator_mock.paginate.return_value = [
            {"Quotas": [{"QuotaCode": "L-1", "Value": 100}]},
        ]
        sq_mock.get_paginator.return_value = paginator_mock
        ddb_mock.get_item.side_effect = _client_error("ResourceNotFoundException")
        cw_mock.put_metric_alarm.return_value = {}

        def factory(service: str, *a: Any, **kw: Any) -> Any:
            if service == "service-quotas":
                return sq_mock
            if service == "dynamodb":
                return ddb_mock
            return cw_mock

        with patch.object(_obs_mod, "get_client", side_effect=factory):
            result = service_quota_monitor(["ec2"], "tbl", "pfx")
        # Should use default threshold and succeed
        assert result.alarms_created == 1
