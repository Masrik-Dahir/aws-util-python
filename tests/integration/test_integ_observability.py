"""Integration tests for aws_util.observability against LocalStack."""
from __future__ import annotations

import json
import time

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. create_lambda_alarms
# ---------------------------------------------------------------------------


class TestCreateLambdaAlarms:
    @pytest.mark.skip(reason="CloudWatch PutMetricAlarm returns 500 on LocalStack community")
    def test_creates_alarms(self, sns_topic):
        from aws_util.observability import create_lambda_alarms

        import io
        import zipfile

        iam = ls_client("iam")
        role_name = f"alarm-test-role-{int(time.time())}"
        try:
            role = iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}],
                }),
            )
            role_arn = role["Role"]["Arn"]
        except iam.exceptions.EntityAlreadyExistsException:
            role_arn = iam.get_role(RoleName=role_name)["Role"]["Arn"]

        lam = ls_client("lambda")
        fn_name = f"alarm-test-fn-{int(time.time())}"
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(e, c): return e")
        lam.create_function(
            FunctionName=fn_name,
            Runtime="python3.12",
            Role=role_arn,
            Handler="handler.handler",
            Code={"ZipFile": buf.getvalue()},
        )

        results = create_lambda_alarms(
            function_name=fn_name,
            sns_topic_arn=sns_topic,
            error_threshold=1,
            region_name=REGION,
        )
        # Returns a list of AlarmFactoryResult
        assert len(results) >= 1
        assert results[0].alarm_name
        assert results[0].created is True


# ---------------------------------------------------------------------------
# 2. create_dlq_depth_alarm
# ---------------------------------------------------------------------------


class TestCreateDlqDepthAlarm:
    @pytest.mark.skip(reason="CloudWatch PutMetricAlarm returns 500 on LocalStack community")
    def test_creates_depth_alarm(self, sqs_queue, sns_topic):
        from aws_util.observability import create_dlq_depth_alarm

        # create_dlq_depth_alarm expects queue_name (not queue_url)
        # Extract queue name from URL
        queue_name = sqs_queue.split("/")[-1]

        result = create_dlq_depth_alarm(
            queue_name=queue_name,
            sns_topic_arn=sns_topic,
            threshold=10,
            region_name=REGION,
        )
        assert result.alarm_name
        assert result.created is True


# ---------------------------------------------------------------------------
# 3. run_log_insights_query
# ---------------------------------------------------------------------------


class TestRunLogInsightsQuery:
    def test_runs_query(self, logs_group):
        from aws_util.observability import run_log_insights_query

        # Put a log event
        logs = ls_client("logs")
        logs.create_log_stream(logGroupName=logs_group, logStreamName="test-stream")
        now_ms = int(time.time() * 1000)
        logs.put_log_events(
            logGroupName=logs_group,
            logStreamName="test-stream",
            logEvents=[
                {"timestamp": now_ms, "message": "ERROR something went wrong"},
            ],
        )

        now = int(time.time())
        result = run_log_insights_query(
            log_group_names=[logs_group],
            query_string="fields @timestamp, @message | limit 10",
            start_time=now - 3600,
            end_time=now,
            region_name=REGION,
        )
        assert isinstance(result.results, list)


# ---------------------------------------------------------------------------
# 4. emit_emf_metric
# ---------------------------------------------------------------------------


class TestEmitEmfMetric:
    def test_emits_metric(self):
        from aws_util.observability import emit_emf_metric

        # emit_emf_metric writes structured JSON to stdout (EMF format)
        # It does not take log_group_name or region_name
        result = emit_emf_metric(
            namespace="TestApp",
            metric_name="Latency",
            value=42.5,
            unit="Milliseconds",
            dimensions={"Service": "API", "Environment": "test"},
        )
        assert result.emitted is True
        assert result.namespace == "TestApp"
        assert result.metric_name == "Latency"
        assert result.value == 42.5


# ---------------------------------------------------------------------------
# 5. aggregate_errors
# ---------------------------------------------------------------------------


class TestAggregateErrors:
    def test_aggregates_from_log(self, logs_group):
        from aws_util.observability import aggregate_errors

        logs = ls_client("logs")
        logs.create_log_stream(logGroupName=logs_group, logStreamName="err-stream")
        now = int(time.time() * 1000)
        logs.put_log_events(
            logGroupName=logs_group,
            logStreamName="err-stream",
            logEvents=[
                {"timestamp": now, "message": "ERROR NullPointerException"},
                {"timestamp": now + 1, "message": "ERROR TimeoutException"},
                {"timestamp": now + 2, "message": "INFO all good"},
            ],
        )

        now_epoch = int(time.time())
        result = aggregate_errors(
            log_group_name=logs_group,
            start_time=(now_epoch - 3600) * 1000,
            end_time=(now_epoch + 60) * 1000,
            region_name=REGION,
        )
        # ErrorAggregatorResult has total_errors, unique_errors, digests
        assert isinstance(result.total_errors, int)
        assert isinstance(result.unique_errors, int)
        assert isinstance(result.digests, list)


# ---------------------------------------------------------------------------
# 6. create_xray_trace
# ---------------------------------------------------------------------------


class TestCreateXrayTrace:
    @pytest.mark.skip(reason="X-Ray not available in LocalStack community")
    def test_creates_trace(self):
        from aws_util.observability import create_xray_trace

        result = create_xray_trace(
            segment_name="test-segment",
            annotations={"env": "test"},
            metadata={"detail": "integration-test"},
            region_name=REGION,
        )
        assert result.segment_id
        assert result.trace_id
        assert result.sampled is True


# ---------------------------------------------------------------------------
# 7. batch_put_trace_segments
# ---------------------------------------------------------------------------


class TestBatchPutTraceSegments:
    @pytest.mark.skip(reason="X-Ray not available in LocalStack community")
    def test_batch_puts_segments(self):
        import hashlib

        from aws_util.observability import batch_put_trace_segments

        now = time.time()
        trace_id = f"1-{int(now):08x}-{'0' * 24}"
        segments = [
            {
                "name": f"seg-{i}",
                "id": hashlib.md5(f"seg-{i}-{now}".encode()).hexdigest()[:16],
                "trace_id": trace_id,
                "start_time": now,
                "end_time": now + 0.001,
                "in_progress": False,
            }
            for i in range(3)
        ]

        results = batch_put_trace_segments(
            segments=segments,
            region_name=REGION,
        )
        assert len(results) == 3
        for r in results:
            assert r.segment_id
            assert r.trace_id == trace_id


# ---------------------------------------------------------------------------
# 8. emit_emf_metrics_batch
# ---------------------------------------------------------------------------


class TestEmitEmfMetricsBatch:
    def test_emits_batch(self):
        from aws_util.observability import emit_emf_metrics_batch

        metrics = [
            {"name": "Latency", "value": 42.5, "unit": "Milliseconds"},
            {"name": "ErrorCount", "value": 3.0, "unit": "Count"},
            {"name": "RequestSize", "value": 1024.0, "unit": "Bytes"},
        ]

        results = emit_emf_metrics_batch(
            namespace="TestBatchApp",
            metrics=metrics,
            dimensions={"Service": "API", "Stage": "test"},
        )
        assert len(results) == 3
        for r in results:
            assert r.emitted is True
            assert r.namespace == "TestBatchApp"
        assert results[0].metric_name == "Latency"
        assert results[0].value == 42.5
        assert results[1].metric_name == "ErrorCount"
        assert results[2].metric_name == "RequestSize"


# ---------------------------------------------------------------------------
# 9. generate_lambda_dashboard
# ---------------------------------------------------------------------------


class TestGenerateLambdaDashboard:
    @pytest.mark.skip(reason="CloudWatch PutDashboard may return 500 on LocalStack community")
    def test_generates_dashboard(self):
        from aws_util.observability import generate_lambda_dashboard

        result = generate_lambda_dashboard(
            dashboard_name="test-dashboard",
            function_names=["fn-alpha", "fn-beta"],
            region_name=REGION,
        )
        assert result.dashboard_name == "test-dashboard"
        assert result.function_names == ["fn-alpha", "fn-beta"]


# ---------------------------------------------------------------------------
# 10. create_canary / delete_canary
# ---------------------------------------------------------------------------


class TestCanaryLifecycle:
    @pytest.mark.skip(reason="CloudWatch Synthetics not available in LocalStack community")
    def test_creates_and_deletes_canary(self, s3_bucket, iam_role):
        from aws_util.observability import create_canary, delete_canary

        create_result = create_canary(
            canary_name="test-canary",
            endpoint="https://example.com/health",
            s3_bucket=s3_bucket,
            schedule_expression="rate(5 minutes)",
            execution_role_arn=iam_role,
            region_name=REGION,
        )
        assert create_result.canary_name == "test-canary"
        assert create_result.endpoint == "https://example.com/health"
        assert create_result.created is True

        delete_result = delete_canary(
            canary_name="test-canary",
            region_name=REGION,
        )
        assert delete_result.canary_name == "test-canary"
        assert delete_result.status == "DELETED"
        assert delete_result.created is False


# ---------------------------------------------------------------------------
# 11. build_service_map
# ---------------------------------------------------------------------------


class TestBuildServiceMap:
    @pytest.mark.skip(reason="X-Ray not available in LocalStack community")
    def test_builds_map(self):
        from aws_util.observability import build_service_map

        now = time.time()
        result = build_service_map(
            start_time=now - 3600,
            end_time=now,
            region_name=REGION,
        )
        assert isinstance(result.nodes, list)
        assert result.start_time
        assert result.end_time


# ---------------------------------------------------------------------------
# 12. get_trace_summaries
# ---------------------------------------------------------------------------


class TestGetTraceSummaries:
    @pytest.mark.skip(reason="X-Ray not available in LocalStack community")
    def test_gets_summaries(self):
        from aws_util.observability import get_trace_summaries

        now = time.time()
        result = get_trace_summaries(
            start_time=now - 3600,
            end_time=now,
            region_name=REGION,
        )
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# 13. kinesis_analytics_alarm_manager
# ---------------------------------------------------------------------------


class TestKinesisAnalyticsAlarmManager:
    @pytest.mark.skip(reason="Kinesis Analytics V2 not available in LocalStack community")
    def test_creates_alarms(self, sns_topic):
        from aws_util.observability import kinesis_analytics_alarm_manager

        result = kinesis_analytics_alarm_manager(
            application_name="test-kda-app",
            sns_topic_arn=sns_topic,
            alarm_prefix="integ-test",
            milliseconds_behind_threshold=60000,
            region_name=REGION,
        )
        assert result.application_status
        assert isinstance(result.alarm_names, list)


# ---------------------------------------------------------------------------
# 14. dms_task_monitor
# ---------------------------------------------------------------------------


class TestDmsTaskMonitor:
    @pytest.mark.skip(reason="DMS not available in LocalStack community")
    def test_monitors_task(self):
        from aws_util.observability import dms_task_monitor

        result = dms_task_monitor(
            replication_task_arn="arn:aws:dms:us-east-1:000000000000:task:test-task",
            metric_namespace="TestDMS",
            region_name=REGION,
        )
        assert result.task_status
        assert isinstance(result.tables_monitored, int)


# ---------------------------------------------------------------------------
# 15. health_event_to_teams
# ---------------------------------------------------------------------------


class TestHealthEventToTeams:
    @pytest.mark.skip(reason="AWS Health API not available in LocalStack community")
    def test_forwards_events(self, sqs_queue):
        from aws_util.observability import health_event_to_teams

        result = health_event_to_teams(
            queue_url=sqs_queue,
            lookback_hours=24,
            region_name=REGION,
        )
        assert isinstance(result.events_found, int)
        assert isinstance(result.messages_sent, int)
        assert isinstance(result.affected_accounts, list)


# ---------------------------------------------------------------------------
# 16. service_quota_monitor
# ---------------------------------------------------------------------------


class TestServiceQuotaMonitor:
    @pytest.mark.skip(reason="Service Quotas not available in LocalStack community")
    def test_monitors_quotas(self, dynamodb_pk_table):
        from aws_util.observability import service_quota_monitor

        result = service_quota_monitor(
            service_codes=["ec2", "lambda"],
            table_name=dynamodb_pk_table,
            alarm_prefix="integ-quota",
            region_name=REGION,
        )
        assert isinstance(result.services_checked, int)
        assert isinstance(result.quotas_near_limit, int)
        assert isinstance(result.alarms_created, int)
