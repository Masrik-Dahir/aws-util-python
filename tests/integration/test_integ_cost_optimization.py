"""Integration tests for aws_util.cost_optimization against LocalStack."""
from __future__ import annotations

import json

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. lambda_right_sizer
# ---------------------------------------------------------------------------


class TestLambdaRightSizer:
    @pytest.mark.skip(reason="CloudWatch GetMetricStatistics returns 500 on LocalStack community")
    def test_analyzes_function(self, iam_role):
        from aws_util.cost_optimization import lambda_right_sizer
        import io, zipfile

        lam = ls_client("lambda")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(e, c): return e")
        try:
            lam.create_function(
                FunctionName="right-sizer-fn",
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
                MemorySize=512,
            )
        except lam.exceptions.ResourceConflictException:
            pass  # function already exists

        result = lambda_right_sizer(
            function_name="right-sizer-fn",
            region_name=REGION,
        )
        assert isinstance(result.configurations, list)


# ---------------------------------------------------------------------------
# 2. unused_resource_finder
# ---------------------------------------------------------------------------


class TestUnusedResourceFinder:
    def test_finds_resources(self):
        from aws_util.cost_optimization import unused_resource_finder

        result = unused_resource_finder(region_name=REGION)
        assert isinstance(result.idle_lambdas, list)
        assert isinstance(result.empty_queues, list)
        assert isinstance(result.orphaned_log_groups, list)
        assert isinstance(result.total_found, int)


# ---------------------------------------------------------------------------
# 3. log_retention_enforcer
# ---------------------------------------------------------------------------


class TestLogRetentionEnforcer:
    def test_enforces_retention(self, logs_group):
        from aws_util.cost_optimization import log_retention_enforcer

        result = log_retention_enforcer(
            retention_days=14,
            region_name=REGION,
        )
        assert result.groups_updated >= 0


# ---------------------------------------------------------------------------
# 4. cost_attribution_tagger
# ---------------------------------------------------------------------------


class TestCostAttributionTagger:
    @pytest.mark.skip(reason="ResourceGroupsTaggingAPI not fully supported on LocalStack community")
    def test_tags_resources(self, s3_bucket):
        from aws_util.cost_optimization import cost_attribution_tagger

        result = cost_attribution_tagger(
            resource_arns=[f"arn:aws:s3:::{s3_bucket}"],
            required_tags={"CostCenter": "Engineering", "Environment": "test"},
            region_name=REGION,
        )
        assert result.resources_tagged >= 0


# ---------------------------------------------------------------------------
# 5. dynamodb_capacity_advisor
# ---------------------------------------------------------------------------


class TestDynamodbCapacityAdvisor:
    @pytest.mark.skip(
        reason="CloudWatch GetMetricStatistics returns 500 on LocalStack community"
    )
    def test_advises(self, dynamodb_pk_table):
        from aws_util.cost_optimization import dynamodb_capacity_advisor

        result = dynamodb_capacity_advisor(
            table_names=[dynamodb_pk_table],
            region_name=REGION,
        )
        assert isinstance(result.tables, list)
        assert result.total_analyzed >= 0


# ---------------------------------------------------------------------------
# 6. concurrency_optimizer
# ---------------------------------------------------------------------------


class TestConcurrencyOptimizer:
    @pytest.mark.skip(reason="CloudWatch GetMetricStatistics returns 500 on LocalStack community")
    def test_optimizes(self, iam_role):
        from aws_util.cost_optimization import concurrency_optimizer
        import io, zipfile

        lam = ls_client("lambda")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(e, c): return e")
        try:
            lam.create_function(
                FunctionName="concurrency-fn",
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
            )
        except lam.exceptions.ResourceConflictException:
            pass  # function already exists

        result = concurrency_optimizer(
            function_names=["concurrency-fn"],
            region_name=REGION,
        )
        assert isinstance(result.functions, list)


# ---------------------------------------------------------------------------
# 7. trusted_advisor_report_to_s3
# ---------------------------------------------------------------------------


class TestTrustedAdvisorReportToS3:
    @pytest.mark.skip(reason="Support API (Trusted Advisor) not available in LocalStack community")
    def test_generates_report(self, s3_bucket):
        from aws_util.cost_optimization import trusted_advisor_report_to_s3

        result = trusted_advisor_report_to_s3(
            bucket=s3_bucket,
            report_key="reports/trusted-advisor.json",
            region_name=REGION,
        )
        assert isinstance(result.checks_count, int)
        assert isinstance(result.flagged_resources, int)
        assert result.s3_key == "reports/trusted-advisor.json"


# ---------------------------------------------------------------------------
# 8. cost_and_usage_report_analyzer
# ---------------------------------------------------------------------------


class TestCostAndUsageReportAnalyzer:
    @pytest.mark.skip(reason="Athena / Cost Explorer (CUR) not available in LocalStack community")
    def test_analyzes_report(self, sns_topic):
        from aws_util.cost_optimization import cost_and_usage_report_analyzer

        result = cost_and_usage_report_analyzer(
            database="cur_db",
            table="cur_table",
            output_location="s3://test-bucket/athena-results/",
            threshold_percent=50.0,
            sns_topic_arn=sns_topic,
            region_name=REGION,
        )
        assert isinstance(result.query_execution_id, str)
        assert isinstance(result.services_analyzed, int)
        assert isinstance(result.anomalies_found, int)


# ---------------------------------------------------------------------------
# 9. savings_plan_coverage_reporter
# ---------------------------------------------------------------------------


class TestSavingsPlanCoverageReporter:
    @pytest.mark.skip(reason="Cost Explorer (Savings Plans) not available in LocalStack community")
    def test_reports_coverage(self, s3_bucket):
        from aws_util.cost_optimization import savings_plan_coverage_reporter

        result = savings_plan_coverage_reporter(
            bucket=s3_bucket,
            report_key="reports/savings-plans.json",
            start_date="2024-01-01",
            end_date="2024-02-01",
            metric_namespace="Test/SP",
            region_name=REGION,
        )
        assert isinstance(result.coverage_percent, float)
        assert isinstance(result.total_spend, float)
        assert result.s3_key == "reports/savings-plans.json"


# ---------------------------------------------------------------------------
# 10. ec2_idle_instance_stopper
# ---------------------------------------------------------------------------


class TestEc2IdleInstanceStopper:
    @pytest.mark.skip(
        reason="CloudWatch GetMetricStatistics returns 500 on LocalStack community"
    )
    def test_detects_idle_instances(self, dynamodb_pk_table):
        from aws_util.cost_optimization import ec2_idle_instance_stopper

        result = ec2_idle_instance_stopper(
            table_name=dynamodb_pk_table,
            cpu_threshold=5.0,
            grace_period_hours=24,
            region_name=REGION,
        )
        assert isinstance(result.instances_checked, int)
        assert isinstance(result.idle_found, int)
        assert isinstance(result.stopped_count, int)
        assert isinstance(result.watched_count, int)


# ---------------------------------------------------------------------------
# 11. rds_idle_snapshot_and_delete
# ---------------------------------------------------------------------------


class TestRdsIdleSnapshotAndDelete:
    @pytest.mark.skip(
        reason="RDS + CloudWatch GetMetricStatistics not reliably available in LocalStack community"
    )
    def test_finds_idle_rds(self):
        from aws_util.cost_optimization import rds_idle_snapshot_and_delete

        result = rds_idle_snapshot_and_delete(
            lookback_days=7,
            dry_run=True,
            region_name=REGION,
        )
        assert isinstance(result.instances_checked, int)
        assert isinstance(result.idle_found, int)
        assert isinstance(result.snapshots_created, int)
        assert result.dry_run is True


# ---------------------------------------------------------------------------
# 12. ecr_lifecycle_policy_applier
# ---------------------------------------------------------------------------


class TestEcrLifecyclePolicyApplier:
    @pytest.mark.skip(reason="ECR not available in LocalStack community")
    def test_applies_lifecycle(self, dynamodb_table):
        from aws_util.cost_optimization import ecr_lifecycle_policy_applier

        result = ecr_lifecycle_policy_applier(
            table_name=dynamodb_table,
            max_image_count=50,
            region_name=REGION,
        )
        assert isinstance(result.repositories_updated, int)
        assert isinstance(result.already_configured, int)
        assert isinstance(result.errors, int)


# ---------------------------------------------------------------------------
# 13. s3_intelligent_tiering_enrollor
# ---------------------------------------------------------------------------


class TestS3IntelligentTieringEnrollor:
    @pytest.mark.skip(
        reason="S3 Intelligent-Tiering configuration API not reliably supported in LocalStack community"
    )
    def test_enrolls_buckets(self, s3_bucket):
        from aws_util.cost_optimization import s3_intelligent_tiering_enrollor

        result = s3_intelligent_tiering_enrollor(
            metric_namespace="Test/Tiering",
            archive_access_days=90,
            deep_archive_days=180,
            region_name=REGION,
        )
        assert isinstance(result.buckets_checked, int)
        assert isinstance(result.buckets_enrolled, int)
        assert isinstance(result.already_enrolled, int)


# ---------------------------------------------------------------------------
# 14. lambda_dead_code_detector
# ---------------------------------------------------------------------------


class TestLambdaDeadCodeDetector:
    @pytest.mark.skip(
        reason="CloudWatch GetMetricStatistics returns 500 on LocalStack community"
    )
    def test_detects_dead_code(self, iam_role):
        import io
        import zipfile

        from aws_util.cost_optimization import lambda_dead_code_detector

        lam = ls_client("lambda")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("handler.py", "def handler(e, c): return e")
        try:
            lam.create_function(
                FunctionName="dead-code-fn",
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": buf.getvalue()},
            )
        except lam.exceptions.ResourceConflictException:
            pass

        result = lambda_dead_code_detector(
            lookback_days=30,
            region_name=REGION,
        )
        assert isinstance(result.functions_checked, int)
        assert isinstance(result.dead_functions, int)
        assert isinstance(result.dead_function_names, list)
