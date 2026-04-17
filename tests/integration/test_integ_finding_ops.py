"""Integration tests for aws_util.finding_ops against LocalStack."""
from __future__ import annotations

import json

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. security_hub_finding_router
# ---------------------------------------------------------------------------


class TestSecurityHubFindingRouter:
    @pytest.mark.skip(
        reason="Not supported in LocalStack community"
    )
    def test_routes_findings(self, sqs_queue):
        from aws_util.finding_ops import security_hub_finding_router

        sqs = ls_client("sqs")
        critical_queue = sqs.create_queue(QueueName="critical-queue")["QueueUrl"]
        high_queue = sqs.create_queue(QueueName="high-queue")["QueueUrl"]

        result = security_hub_finding_router(
            critical_queue_url=critical_queue,
            high_queue_url=high_queue,
            default_queue_url=sqs_queue,
            region_name=REGION,
        )
        assert isinstance(result.total_findings, int)
        assert isinstance(result.critical_count, int)
        assert isinstance(result.high_count, int)
        assert isinstance(result.default_count, int)


# ---------------------------------------------------------------------------
# 2. cloudtrail_anomaly_detector
# ---------------------------------------------------------------------------


class TestCloudtrailAnomalyDetector:
    @pytest.mark.skip(
        reason="Not supported in LocalStack community"
    )
    def test_detects_anomalies(self, sns_topic):
        from aws_util.finding_ops import cloudtrail_anomaly_detector

        result = cloudtrail_anomaly_detector(
            trail_name="test-trail",
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.events_analyzed, int)
        assert isinstance(result.anomalies_found, int)


# ---------------------------------------------------------------------------
# 3. inspector_finding_to_jira (Inspector not available)
# ---------------------------------------------------------------------------


class TestInspectorFindingToJira:
    @pytest.mark.skip(
        reason="Inspector not available in LocalStack community"
    )
    def test_processes_inspector_findings(self, dynamodb_pk_table):
        from aws_util.finding_ops import inspector_finding_to_jira

        result = inspector_finding_to_jira(
            table_name=dynamodb_pk_table,
            from_email="sender@example.com",
            to_emails=["recipient@example.com"],
            max_findings=10,
            region_name=REGION,
        )
        assert isinstance(result.findings_count, int)
        assert isinstance(result.new_findings, int)
        assert isinstance(result.emails_sent, int)


# ---------------------------------------------------------------------------
# 4. macie_finding_remediation (Macie not available)
# ---------------------------------------------------------------------------


class TestMacieFindingRemediation:
    @pytest.mark.skip(
        reason="Macie not available in LocalStack community"
    )
    def test_remediates_macie_findings(self, dynamodb_pk_table):
        from aws_util.finding_ops import macie_finding_remediation

        result = macie_finding_remediation(
            table_name=dynamodb_pk_table,
            max_findings=10,
            region_name=REGION,
        )
        assert isinstance(result.findings_count, int)
        assert isinstance(result.remediated_count, int)
        assert isinstance(result.buckets_affected, list)


# ---------------------------------------------------------------------------
# 5. detective_graph_exporter (Detective not available)
# ---------------------------------------------------------------------------


class TestDetectiveGraphExporter:
    @pytest.mark.skip(
        reason="Detective not available in LocalStack community"
    )
    def test_exports_graph(self, s3_bucket):
        from aws_util.finding_ops import detective_graph_exporter

        result = detective_graph_exporter(
            graph_arn="arn:aws:detective:us-east-1:123456789012:graph:abc123",
            bucket=s3_bucket,
            key_prefix="detective-export",
            database_name="detective_db",
            table_name_prefix="detective",
            region_name=REGION,
        )
        assert isinstance(result.members_count, int)
        assert isinstance(result.s3_key, str)
        assert isinstance(result.glue_table_name, str)


# ---------------------------------------------------------------------------
# 6. access_analyzer_finding_suppressor (Access Analyzer not available)
# ---------------------------------------------------------------------------


class TestAccessAnalyzerFindingSuppressor:
    @pytest.mark.skip(
        reason="Access Analyzer not available in LocalStack community"
    )
    def test_suppresses_findings(self, dynamodb_pk_table, logs_group):
        from aws_util.finding_ops import access_analyzer_finding_suppressor

        result = access_analyzer_finding_suppressor(
            analyzer_arn="arn:aws:access-analyzer:us-east-1:123456789012:analyzer/test",
            table_name=dynamodb_pk_table,
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert isinstance(result.findings_count, int)
        assert isinstance(result.suppressed_count, int)
        assert isinstance(result.unresolved_count, int)
