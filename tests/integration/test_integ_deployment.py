"""Integration tests for aws_util.deployment against LocalStack."""
from __future__ import annotations

import io
import json
import time
import zipfile

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _make_lambda_zip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("handler.py", "def handler(event, context): return event")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# 1. lambda_layer_publisher
# ---------------------------------------------------------------------------


class TestLambdaLayerPublisher:
    def test_publishes_layer(self, tmp_path):
        from aws_util.deployment import lambda_layer_publisher

        # lambda_layer_publisher takes a local directory, not S3 bucket/key
        # Create a temp directory with a sample file
        layer_dir = tmp_path / "layer"
        layer_dir.mkdir()
        (layer_dir / "utils.py").write_text("def helper(): return True")

        result = lambda_layer_publisher(
            layer_name="test-layer",
            directory=str(layer_dir),
            compatible_runtimes=["python3.12"],
            description="Test layer",
            region_name=REGION,
        )
        assert result.layer_name == "test-layer"
        assert result.version_number >= 1
        assert result.layer_arn


# ---------------------------------------------------------------------------
# 2. stack_deployer
# ---------------------------------------------------------------------------


class TestStackDeployer:
    def test_deploys_stack(self):
        from aws_util.deployment import stack_deployer

        stack_name = f"test-stack-deploy-{int(time.time())}"
        template = json.dumps({
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {
                "TestBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {},
                }
            },
        })

        result = stack_deployer(
            stack_name=stack_name,
            template_body=template,
            region_name=REGION,
        )
        assert result.stack_name == stack_name
        # stack_deployer returns StackDeployResult; status can be
        # CREATE_COMPLETE, UPDATE_COMPLETE, or NO_CHANGES
        assert result.status in ("CREATE_COMPLETE", "UPDATE_COMPLETE", "NO_CHANGES")


# ---------------------------------------------------------------------------
# 3. lambda_warmer
# ---------------------------------------------------------------------------


class TestLambdaWarmer:
    def test_warms_function(self, iam_role):
        from aws_util.deployment import lambda_warmer

        lam = ls_client("lambda")
        fn_name = f"test-warmer-fn-{int(time.time())}"
        try:
            lam.create_function(
                FunctionName=fn_name,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": _make_lambda_zip()},
            )
        except lam.exceptions.ResourceConflictException:
            pass  # Function already exists

        # lambda_warmer takes function_name (singular), not function_names/concurrency
        result = lambda_warmer(
            function_name=fn_name,
            schedule_expression="rate(5 minutes)",
            region_name=REGION,
        )
        # LambdaWarmerResult has function_name, rule_name, rule_arn, schedule_expression
        assert result.function_name == fn_name
        assert result.rule_name
        assert result.rule_arn


# ---------------------------------------------------------------------------
# 4. config_drift_detector
# ---------------------------------------------------------------------------


class TestConfigDriftDetector:
    def test_detects_no_drift(self, iam_role):
        from aws_util.deployment import config_drift_detector

        lam = ls_client("lambda")
        fn_name = f"test-drift-fn-{int(time.time())}"
        lam.create_function(
            FunctionName=fn_name,
            Runtime="python3.12",
            Role=iam_role,
            Handler="handler.handler",
            Code={"ZipFile": _make_lambda_zip()},
        )

        # config_drift_detector checks Lambda/API GW configs against desired state
        result = config_drift_detector(
            function_names=[fn_name],
            region_name=REGION,
        )
        # DriftDetectionResult has drifted, drift_items, resources_checked
        assert isinstance(result.drifted, bool)
        assert isinstance(result.drift_items, list)
        assert result.resources_checked >= 1


# ---------------------------------------------------------------------------
# 5. lambda_canary_deploy
# ---------------------------------------------------------------------------


class TestLambdaCanaryDeploy:
    def test_creates_alias_on_first_deploy(self, iam_role):
        from aws_util.deployment import lambda_canary_deploy

        lam = ls_client("lambda")
        fn_name = f"test-canary-fn-{int(time.time())}"
        try:
            lam.create_function(
                FunctionName=fn_name,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": _make_lambda_zip()},
            )
        except lam.exceptions.ResourceConflictException:
            pass

        result = lambda_canary_deploy(
            function_name=fn_name,
            alias_name="live",
            steps=[1.0],
            interval_seconds=0,
            region_name=REGION,
        )
        assert result.function_name == fn_name
        assert result.alias_name == "live"
        assert result.new_version
        assert result.final_weight == 1.0
        assert result.rolled_back is False


# ---------------------------------------------------------------------------
# 6. environment_promoter
# ---------------------------------------------------------------------------


class TestEnvironmentPromoter:
    def test_promotes_env_vars(self, iam_role):
        from aws_util.deployment import environment_promoter

        lam = ls_client("lambda")
        base_name = f"test-promote-{int(time.time())}"
        src_fn = f"{base_name}-dev"
        tgt_fn = f"{base_name}-prod"

        # Create source function with env vars
        try:
            lam.create_function(
                FunctionName=src_fn,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": _make_lambda_zip()},
                Environment={"Variables": {"APP_ENV": "dev", "DB_HOST": "localhost"}},
            )
        except lam.exceptions.ResourceConflictException:
            pass

        # Create target function
        try:
            lam.create_function(
                FunctionName=tgt_fn,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": _make_lambda_zip()},
            )
        except lam.exceptions.ResourceConflictException:
            pass

        result = environment_promoter(
            function_name=base_name,
            source_stage="dev",
            target_stage="prod",
            region_name=REGION,
        )
        assert result.function_name == base_name
        assert result.source_stage == "dev"
        assert result.target_stage == "prod"
        assert result.env_vars_copied >= 2


# ---------------------------------------------------------------------------
# 7. rollback_manager
# ---------------------------------------------------------------------------


class TestRollbackManager:
    @pytest.mark.skip(reason="CloudWatch GetMetricStatistics returns 500 on LocalStack community")
    def test_no_rollback_when_healthy(self, iam_role):
        from aws_util.deployment import rollback_manager

        lam = ls_client("lambda")
        fn_name = f"test-rollback-fn-{int(time.time())}"
        try:
            lam.create_function(
                FunctionName=fn_name,
                Runtime="python3.12",
                Role=iam_role,
                Handler="handler.handler",
                Code={"ZipFile": _make_lambda_zip()},
            )
        except lam.exceptions.ResourceConflictException:
            pass

        # Publish a version and create an alias
        pub = lam.publish_version(FunctionName=fn_name)
        version = pub["Version"]
        try:
            lam.create_alias(
                FunctionName=fn_name,
                Name="live",
                FunctionVersion=version,
            )
        except lam.exceptions.ResourceConflictException:
            pass

        result = rollback_manager(
            function_name=fn_name,
            alias_name="live",
            error_threshold=5.0,
            evaluation_minutes=1,
            region_name=REGION,
        )
        assert result.function_name == fn_name
        assert result.alias_name == "live"
        assert isinstance(result.rolled_back, bool)
        assert isinstance(result.error_rate, float)


# ---------------------------------------------------------------------------
# 8. lambda_package_builder
# ---------------------------------------------------------------------------


class TestLambdaPackageBuilder:
    def test_builds_and_uploads_package(self, tmp_path, s3_bucket):
        from aws_util.deployment import lambda_package_builder

        src_dir = tmp_path / "lambda_src"
        src_dir.mkdir()
        (src_dir / "handler.py").write_text(
            "def handler(event, context): return event"
        )
        (src_dir / "utils.py").write_text("HELPER = True")

        result = lambda_package_builder(
            source_dir=str(src_dir),
            s3_bucket=s3_bucket,
            s3_key="packages/test-lambda.zip",
            region_name=REGION,
        )
        assert result.s3_bucket == s3_bucket
        assert result.s3_key == "packages/test-lambda.zip"
        assert result.zip_size_bytes > 0
        assert result.files_included >= 2

        # Verify the object actually exists in S3
        s3 = ls_client("s3")
        head = s3.head_object(Bucket=s3_bucket, Key="packages/test-lambda.zip")
        assert head["ContentLength"] > 0


# ---------------------------------------------------------------------------
# 9. cloudfront_invalidation_with_logging (CloudFront not available)
# ---------------------------------------------------------------------------


class TestCloudfrontInvalidationWithLogging:
    @pytest.mark.skip(
        reason="CloudFront not available in LocalStack community"
    )
    def test_invalidation_with_logging(self, logs_group):
        from aws_util.deployment import cloudfront_invalidation_with_logging

        result = cloudfront_invalidation_with_logging(
            distribution_id="EDFDVBD6EXAMPLE",
            paths=["/index.html", "/*"],
            log_group_name=logs_group,
            region_name=REGION,
        )
        assert isinstance(result.invalidation_id, str)
        assert isinstance(result.status, str)
        assert result.paths_invalidated == 2
        assert isinstance(result.logged, bool)


# ---------------------------------------------------------------------------
# 10. elastic_beanstalk_env_refresher (ElasticBeanstalk not available)
# ---------------------------------------------------------------------------


class TestElasticBeanstalkEnvRefresher:
    @pytest.mark.skip(
        reason="ElasticBeanstalk not available in LocalStack community"
    )
    def test_refreshes_environment(self):
        from aws_util.deployment import elastic_beanstalk_env_refresher

        result = elastic_beanstalk_env_refresher(
            application_name="test-app",
            environment_name="test-env",
            version_label="v1",
            ssm_prefix="/test/beanstalk/",
            region_name=REGION,
        )
        assert isinstance(result.environment_id, str)
        assert isinstance(result.status, str)
        assert isinstance(result.params_injected, int)


# ---------------------------------------------------------------------------
# 11. app_runner_auto_deployer (App Runner not available)
# ---------------------------------------------------------------------------


class TestAppRunnerAutoDeployer:
    @pytest.mark.skip(
        reason="App Runner not available in LocalStack community"
    )
    def test_auto_deploys(self):
        from aws_util.deployment import app_runner_auto_deployer

        result = app_runner_auto_deployer(
            service_arn="arn:aws:apprunner:us-east-1:123456789012:service/test-svc/abc123",
            repository_name="test-repo",
            region_name=REGION,
        )
        assert isinstance(result.service_id, str)
        assert isinstance(result.image_updated, bool)
        assert isinstance(result.new_image_tag, str)


# ---------------------------------------------------------------------------
# 12. eks_node_group_scaler (EKS not available)
# ---------------------------------------------------------------------------


class TestEksNodeGroupScaler:
    @pytest.mark.skip(
        reason="EKS not available in LocalStack community"
    )
    def test_scales_node_group(self):
        from aws_util.deployment import eks_node_group_scaler

        result = eks_node_group_scaler(
            cluster_name="test-cluster",
            nodegroup_name="test-nodegroup",
            metric_name="CPUUtilization",
            metric_namespace="AWS/EKS",
            threshold=80.0,
            scale_up_size=4,
            scale_down_size=2,
            region_name=REGION,
        )
        assert isinstance(result.cluster_name, str)
        assert isinstance(result.current_size, int)
        assert isinstance(result.desired_size, int)
        assert isinstance(result.scaled, bool)


# ---------------------------------------------------------------------------
# 13. eks_config_map_sync (EKS not available — but uses SSM+DynamoDB only)
# ---------------------------------------------------------------------------


class TestEksConfigMapSync:
    @pytest.mark.skip(
        reason="EKS not available in LocalStack community"
    )
    def test_syncs_config_map(self):
        from aws_util.deployment import eks_config_map_sync

        result = eks_config_map_sync(
            cluster_name="test-cluster",
            ssm_prefix="/test/eks/configmap/",
            table_name="test-configmap-table",
            config_map_name="app-config",
            region_name=REGION,
        )
        assert isinstance(result.parameters_synced, int)
        assert isinstance(result.config_map_name, str)
        assert isinstance(result.table_updated, bool)


# ---------------------------------------------------------------------------
# 14. batch_job_monitor (Batch not available)
# ---------------------------------------------------------------------------


class TestBatchJobMonitor:
    @pytest.mark.skip(
        reason="AWS Batch not available in LocalStack community"
    )
    def test_monitors_batch_job(self):
        from aws_util.deployment import batch_job_monitor

        result = batch_job_monitor(
            job_name="test-batch-job",
            job_queue="test-queue",
            job_definition="test-job-def",
            region_name=REGION,
        )
        assert isinstance(result.job_id, str)
        assert isinstance(result.status, str)
        assert isinstance(result.duration_seconds, float)
        assert isinstance(result.metrics_published, int)


# ---------------------------------------------------------------------------
# 15. autoscaling_scheduled_action_manager (AutoScaling not available)
# ---------------------------------------------------------------------------


class TestAutoscalingScheduledActionManager:
    @pytest.mark.skip(
        reason="AutoScaling not available in LocalStack community"
    )
    def test_manages_scheduled_actions(self, dynamodb_pk_table):
        from aws_util.deployment import autoscaling_scheduled_action_manager

        result = autoscaling_scheduled_action_manager(
            asg_name="test-asg",
            table_name=dynamodb_pk_table,
            region_name=REGION,
        )
        assert isinstance(result.actions_synced, int)
        assert isinstance(result.actions_created, int)
        assert isinstance(result.actions_updated, int)


# ---------------------------------------------------------------------------
# 16. stepfunctions_execution_tracker
# ---------------------------------------------------------------------------


class TestStepfunctionsExecutionTracker:
    def test_tracks_execution(self, iam_role):
        from aws_util.deployment import stepfunctions_execution_tracker

        sfn = ls_client("stepfunctions")

        # Create a simple Pass-state machine
        definition = json.dumps({
            "Comment": "Test state machine",
            "StartAt": "PassState",
            "States": {
                "PassState": {
                    "Type": "Pass",
                    "Result": {"message": "done"},
                    "End": True,
                }
            },
        })

        sm_name = f"test-sm-{int(time.time())}"
        try:
            sm_resp = sfn.create_state_machine(
                name=sm_name,
                definition=definition,
                roleArn=iam_role,
            )
            sm_arn = sm_resp["stateMachineArn"]
        except sfn.exceptions.StateMachineAlreadyExists:
            # Retrieve the existing ARN
            machines = sfn.list_state_machines()["stateMachines"]
            sm_arn = next(m["stateMachineArn"] for m in machines if m["name"] == sm_name)

        result = stepfunctions_execution_tracker(
            state_machine_arn=sm_arn,
            input_data={"key": "value"},
            region_name=REGION,
        )
        assert result.execution_arn
        assert result.status in ("RUNNING", "SUCCEEDED", "FAILED", "TIMED_OUT", "ABORTED")
        assert isinstance(result.duration_seconds, float)
