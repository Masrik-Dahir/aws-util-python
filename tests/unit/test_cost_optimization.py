"""Tests for aws_util.cost_optimization module."""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError

from aws_util.cost_optimization import (
    CURAnalysisResult,
    ConcurrencyOptimizerResult,
    ConcurrencyRecommendation,
    CostAttributionTaggerResult,
    DeadCodeResult,
    DynamoDBCapacityAdvice,
    DynamoDBCapacityAdvisorResult,
    ECRPolicyResult,
    IdleInstanceResult,
    IdleRDSResult,
    LambdaRightSizerResult,
    LogRetentionChange,
    LogRetentionEnforcerResult,
    MemoryConfig,
    SPCoverageResult,
    TagComplianceResource,
    TieringResult,
    TrustedAdvisorResult,
    UnusedResource,
    UnusedResourceFinderResult,
    concurrency_optimizer,
    cost_and_usage_report_analyzer,
    cost_attribution_tagger,
    dynamodb_capacity_advisor,
    ec2_idle_instance_stopper,
    ecr_lifecycle_policy_applier,
    lambda_dead_code_detector,
    lambda_right_sizer,
    log_retention_enforcer,
    rds_idle_snapshot_and_delete,
    s3_intelligent_tiering_enrollor,
    savings_plan_coverage_reporter,
    trusted_advisor_report_to_s3,
    unused_resource_finder,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str, message: str = "error") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}}, "Op"
    )


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_memory_config(self) -> None:
        m = MemoryConfig(
            memory_mb=256,
            avg_duration_ms=50.0,
            estimated_cost_per_invocation=0.001,
        )
        assert m.memory_mb == 256
        assert m.avg_duration_ms == 50.0

    def test_lambda_right_sizer_result(self) -> None:
        r = LambdaRightSizerResult(
            function_name="fn",
            recommended_memory_mb=512,
            estimated_savings_pct=15.0,
        )
        assert r.function_name == "fn"
        assert r.configurations == []

    def test_unused_resource(self) -> None:
        u = UnusedResource(
            resource_type="Lambda",
            resource_id="fn1",
            reason="idle",
        )
        assert u.resource_type == "Lambda"

    def test_unused_resource_finder_result(self) -> None:
        r = UnusedResourceFinderResult(total_found=3)
        assert r.idle_lambdas == []
        assert r.empty_queues == []
        assert r.orphaned_log_groups == []

    def test_concurrency_recommendation(self) -> None:
        c = ConcurrencyRecommendation(
            function_name="fn",
            max_concurrent=10,
            avg_concurrent=5.5,
            recommended_reserved=20,
            recommendation="moderate",
        )
        assert c.function_name == "fn"

    def test_concurrency_optimizer_result(self) -> None:
        r = ConcurrencyOptimizerResult(total_analyzed=2)
        assert r.functions == []

    def test_tag_compliance_resource(self) -> None:
        t = TagComplianceResource(
            resource_arn="arn:aws:lambda:us-east-1:123:function:fn",
            resource_type="lambda",
            missing_tags=["env"],
            compliant=False,
        )
        assert t.compliant is False

    def test_cost_attribution_tagger_result(self) -> None:
        r = CostAttributionTaggerResult(
            resources_checked=5,
            resources_tagged=2,
            already_compliant=3,
        )
        assert r.failures == []

    def test_dynamodb_capacity_advice(self) -> None:
        d = DynamoDBCapacityAdvice(
            table_name="tbl",
            billing_mode="PROVISIONED",
            provisioned_rcu=100,
            provisioned_wcu=50,
            consumed_rcu=20.0,
            consumed_wcu=10.0,
            recommendation="reduce",
        )
        assert d.table_name == "tbl"

    def test_dynamodb_capacity_advisor_result(self) -> None:
        r = DynamoDBCapacityAdvisorResult(total_analyzed=1)
        assert r.tables == []

    def test_log_retention_change(self) -> None:
        c = LogRetentionChange(
            log_group="/aws/lambda/fn",
            previous_retention_days=None,
            new_retention_days=30,
        )
        assert c.new_retention_days == 30

    def test_log_retention_enforcer_result(self) -> None:
        r = LogRetentionEnforcerResult(
            groups_updated=2,
            groups_already_compliant=1,
        )
        assert r.changes == []
        assert r.failures == []


# ---------------------------------------------------------------------------
# 1. Lambda Right-Sizer tests
# ---------------------------------------------------------------------------


class TestLambdaRightSizer:
    def test_basic_right_sizing(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }

        # Return different durations for different memory sizes
        call_count = {"n": 0}

        def cw_metrics(**kwargs: Any) -> dict[str, Any]:
            call_count["n"] += 1
            if call_count["n"] == 1:
                return {
                    "Datapoints": [{"Average": 200.0}],
                }
            if call_count["n"] == 2:
                return {
                    "Datapoints": [{"Average": 100.0}],
                }
            return {"Datapoints": [{"Average": 80.0}]}

        mock_cw.get_metric_statistics.side_effect = cw_metrics

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = lambda_right_sizer(
                function_name="my-func",
                memory_configs=[128, 256, 512],
                invocations_per_config=1,
                region_name=REGION,
            )

        assert isinstance(result, LambdaRightSizerResult)
        assert result.function_name == "my-func"
        assert len(result.configurations) == 3
        # Restore was called with original memory
        restore_calls = [
            c
            for c in mock_lam.update_function_configuration.call_args_list
            if c.kwargs.get("MemorySize") == 128
        ]
        assert len(restore_calls) >= 1

    def test_default_memory_configs(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = lambda_right_sizer(
                function_name="fn",
                invocations_per_config=1,
            )

        # Default configs: [128, 256, 512, 1024]
        assert len(result.configurations) == 4

    def test_no_datapoints_uses_fallback(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 256,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = lambda_right_sizer(
                function_name="fn",
                memory_configs=[256],
                invocations_per_config=2,
            )

        assert len(result.configurations) == 1
        # Fallback uses 100.0ms default when no CW datapoints
        assert result.configurations[0].avg_duration_ms == 100.0

    def test_savings_when_original_in_configs(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 512,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }

        call_idx = {"n": 0}

        def cw_metrics(**kwargs: Any) -> dict[str, Any]:
            call_idx["n"] += 1
            if call_idx["n"] == 1:
                return {"Datapoints": [{"Average": 50.0}]}
            return {"Datapoints": [{"Average": 200.0}]}

        mock_cw.get_metric_statistics.side_effect = cw_metrics

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = lambda_right_sizer(
                function_name="fn",
                memory_configs=[128, 512],
                invocations_per_config=1,
            )

        assert result.recommended_memory_mb == 128
        assert result.estimated_savings_pct > 0

    def test_get_config_error(self) -> None:
        mock_lam = MagicMock()
        mock_lam.get_function_configuration.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_lam,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to get config"
            ):
                lambda_right_sizer(
                    function_name="bad-fn",
                    memory_configs=[128],
                )

    def test_update_config_error(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }
        mock_lam.update_function_configuration.side_effect = (
            _client_error("InvalidParameterValueException")
        )

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to update"
            ):
                lambda_right_sizer(
                    function_name="fn",
                    memory_configs=[256],
                    invocations_per_config=1,
                )

    def test_invoke_error(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.side_effect = _client_error(
            "ServiceException"
        )

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to invoke"
            ):
                lambda_right_sizer(
                    function_name="fn",
                    memory_configs=[128],
                    invocations_per_config=1,
                )

    def test_get_metrics_error(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }
        mock_cw.get_metric_statistics.side_effect = _client_error(
            "InternalServiceFault"
        )

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to get metrics"
            ):
                lambda_right_sizer(
                    function_name="fn",
                    memory_configs=[128],
                    invocations_per_config=1,
                )

    def test_restore_error(self) -> None:
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }

        update_count = {"n": 0}

        def update_side_effect(**kwargs: Any) -> dict[str, Any]:
            update_count["n"] += 1
            # First call succeeds (setting to test memory),
            # second call fails (restoring)
            if update_count["n"] > 1:
                raise _client_error("ServiceException")
            return {}

        mock_lam.update_function_configuration.side_effect = (
            update_side_effect
        )
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Average": 100.0}],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to restore"
            ):
                lambda_right_sizer(
                    function_name="fn",
                    memory_configs=[256],
                    invocations_per_config=1,
                )

    def test_original_not_in_configs_zero_savings(self) -> None:
        """When original memory is not in configs, savings is 0."""
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 1024,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {"HTTPHeaders": {}},
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Average": 50.0}],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = lambda_right_sizer(
                function_name="fn",
                memory_configs=[128, 256],
                invocations_per_config=1,
            )

        # original_memory (1024) not in tested configs
        assert result.estimated_savings_pct == 0.0

    def test_invoke_with_log_result_header(self) -> None:
        """When x-amz-log-result header has a numeric value."""
        mock_lam = MagicMock()
        mock_cw = MagicMock()

        mock_lam.get_function_configuration.return_value = {
            "MemorySize": 128,
        }
        mock_lam.update_function_configuration.return_value = {}
        mock_lam.invoke.return_value = {
            "ResponseMetadata": {
                "HTTPHeaders": {"x-amz-log-result": "42.5"},
            },
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = lambda_right_sizer(
                function_name="fn",
                memory_configs=[128],
                invocations_per_config=1,
            )

        # When no CW datapoints, uses average of durations
        assert result.configurations[0].avg_duration_ms == 42.5


# ---------------------------------------------------------------------------
# 2. Unused Resource Finder tests
# ---------------------------------------------------------------------------


class TestUnusedResourceFinder:
    def test_finds_idle_lambdas(self) -> None:
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {
            "Functions": [
                {
                    "FunctionName": "old-fn",
                    "LastModified": "2020-01-01T00:00:00+00:00",
                },
                {
                    "FunctionName": "new-fn",
                    "LastModified": "2099-01-01T00:00:00+00:00",
                },
            ]
        }
        mock_sqs.list_queues.return_value = {}
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder(
                days_inactive=30, region_name=REGION
            )

        assert len(result.idle_lambdas) == 1
        assert result.idle_lambdas[0].resource_id == "old-fn"

    def test_finds_empty_queues(self) -> None:
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {"Functions": []}
        mock_sqs.list_queues.return_value = {
            "QueueUrls": [
                "https://sqs.us-east-1.amazonaws.com/123/q1",
                "https://sqs.us-east-1.amazonaws.com/123/q2",
            ],
        }
        mock_sqs.get_queue_attributes.side_effect = [
            {
                "Attributes": {
                    "ApproximateNumberOfMessages": "0",
                },
            },
            {
                "Attributes": {
                    "ApproximateNumberOfMessages": "5",
                },
            },
        ]
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder(region_name=REGION)

        assert len(result.empty_queues) == 1

    def test_finds_orphaned_log_groups(self) -> None:
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {
            "Functions": [
                {"FunctionName": "active-fn"},
            ]
        }
        mock_sqs.list_queues.return_value = {}
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {"logGroupName": "/aws/lambda/active-fn"},
                {"logGroupName": "/aws/lambda/deleted-fn"},
                {"logGroupName": "/custom/group"},
            ],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder(region_name=REGION)

        assert len(result.orphaned_log_groups) == 1
        assert (
            result.orphaned_log_groups[0].resource_id
            == "/aws/lambda/deleted-fn"
        )

    def test_list_functions_error(self) -> None:
        mock_lam = MagicMock()
        mock_lam.list_functions.side_effect = _client_error(
            "ServiceException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_lam,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to list Lambda functions"
            ):
                unused_resource_finder()

    def test_list_queues_error(self) -> None:
        mock_lam = MagicMock()
        mock_sqs = MagicMock()

        mock_lam.list_functions.return_value = {"Functions": []}
        mock_sqs.list_queues.side_effect = _client_error(
            "ServiceException"
        )

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            return mock_sqs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to list SQS queues"
            ):
                unused_resource_finder()

    def test_describe_log_groups_error(self) -> None:
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {"Functions": []}
        mock_sqs.list_queues.return_value = {}
        mock_logs.describe_log_groups.side_effect = _client_error(
            "ServiceException"
        )

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to list log groups"
            ):
                unused_resource_finder()

    def test_queue_attributes_error_skipped(self) -> None:
        """Inaccessible queues are silently skipped."""
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {"Functions": []}
        mock_sqs.list_queues.return_value = {
            "QueueUrls": ["https://sqs/bad-q"],
        }
        mock_sqs.get_queue_attributes.side_effect = _client_error(
            "AccessDenied"
        )
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder()

        assert result.empty_queues == []
        assert result.total_found == 0

    def test_unparseable_date_skipped(self) -> None:
        """Lambda with unparseable LastModified is skipped."""
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {
            "Functions": [
                {
                    "FunctionName": "bad-date-fn",
                    "LastModified": "not-a-date",
                },
            ]
        }
        mock_sqs.list_queues.return_value = {}
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder()

        assert result.idle_lambdas == []

    def test_no_last_modified_skipped(self) -> None:
        """Lambda without LastModified field is skipped."""
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {
            "Functions": [
                {"FunctionName": "no-date-fn"},
            ]
        }
        mock_sqs.list_queues.return_value = {}
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder()

        assert result.idle_lambdas == []

    def test_total_found_sums_all_types(self) -> None:
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {
            "Functions": [
                {
                    "FunctionName": "old-fn",
                    "LastModified": "2020-01-01T00:00:00+00:00",
                },
            ]
        }
        mock_sqs.list_queues.return_value = {
            "QueueUrls": ["https://sqs/q1"],
        }
        mock_sqs.get_queue_attributes.return_value = {
            "Attributes": {"ApproximateNumberOfMessages": "0"},
        }
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {"logGroupName": "/aws/lambda/deleted-fn"},
            ],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder(days_inactive=30)

        assert result.total_found == 3

    def test_lambda_with_0000_timezone(self) -> None:
        """Lambda LastModified with +0000 timezone format."""
        mock_lam = MagicMock()
        mock_sqs = MagicMock()
        mock_logs = MagicMock()

        mock_lam.list_functions.return_value = {
            "Functions": [
                {
                    "FunctionName": "tz-fn",
                    "LastModified": "2020-01-01T00:00:00+0000",
                },
            ]
        }
        mock_sqs.list_queues.return_value = {}
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "lambda":
                return mock_lam
            if service == "sqs":
                return mock_sqs
            return mock_logs

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = unused_resource_finder(days_inactive=30)

        assert len(result.idle_lambdas) == 1


# ---------------------------------------------------------------------------
# 3. Concurrency Optimizer tests
# ---------------------------------------------------------------------------


class TestConcurrencyOptimizer:
    def test_no_datapoints(self) -> None:
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_cw,
        ):
            result = concurrency_optimizer(
                function_names=["fn1"],
                region_name=REGION,
            )

        assert result.total_analyzed == 1
        assert result.functions[0].max_concurrent == 0
        assert "No concurrency data" in result.functions[0].recommendation

    def test_low_concurrency(self) -> None:
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [
                {"Maximum": 3, "Average": 1.5},
            ],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_cw,
        ):
            result = concurrency_optimizer(
                function_names=["fn1"],
            )

        assert result.functions[0].max_concurrent == 3
        assert "Low concurrency" in result.functions[0].recommendation
        assert result.functions[0].recommended_reserved == 0

    def test_moderate_concurrency(self) -> None:
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [
                {"Maximum": 20, "Average": 10.0},
                {"Maximum": 15, "Average": 8.0},
            ],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_cw,
        ):
            result = concurrency_optimizer(
                function_names=["fn1"],
            )

        assert result.functions[0].max_concurrent == 20
        assert (
            "Moderate concurrency" in result.functions[0].recommendation
        )
        assert result.functions[0].recommended_reserved == 30

    def test_high_concurrency(self) -> None:
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [
                {"Maximum": 100, "Average": 60.0},
                {"Maximum": 80, "Average": 50.0},
            ],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_cw,
        ):
            result = concurrency_optimizer(
                function_names=["fn1"],
            )

        assert result.functions[0].max_concurrent == 100
        assert "High concurrency" in result.functions[0].recommendation
        assert result.functions[0].recommended_reserved == 65

    def test_multiple_functions(self) -> None:
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_cw,
        ):
            result = concurrency_optimizer(
                function_names=["fn1", "fn2", "fn3"],
            )

        assert result.total_analyzed == 3
        assert len(result.functions) == 3

    def test_metrics_error(self) -> None:
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.side_effect = _client_error(
            "InternalServiceFault"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_cw,
        ):
            with pytest.raises(
                RuntimeError,
                match="Failed to get concurrency metrics",
            ):
                concurrency_optimizer(function_names=["fn1"])


# ---------------------------------------------------------------------------
# 4. Cost Attribution Tagger tests
# ---------------------------------------------------------------------------


class TestCostAttributionTagger:
    def test_all_compliant(self) -> None:
        mock_tagging = MagicMock()
        mock_tagging.get_resources.return_value = {
            "ResourceTagMappingList": [
                {
                    "ResourceARN": "arn:aws:lambda:us-east-1:123:fn",
                    "Tags": [
                        {"Key": "env", "Value": "prod"},
                        {"Key": "team", "Value": "platform"},
                    ],
                },
            ],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            result = cost_attribution_tagger(
                resource_arns=[
                    "arn:aws:lambda:us-east-1:123:fn",
                ],
                required_tags={"env": "prod", "team": "platform"},
            )

        assert result.resources_checked == 1
        assert result.already_compliant == 1
        assert result.resources_tagged == 0
        assert result.failures == []

    def test_missing_tags_applied(self) -> None:
        mock_tagging = MagicMock()
        mock_tagging.get_resources.return_value = {
            "ResourceTagMappingList": [
                {
                    "ResourceARN": "arn:aws:lambda:us-east-1:123:fn",
                    "Tags": [{"Key": "env", "Value": "prod"}],
                },
            ],
        }
        mock_tagging.tag_resources.return_value = {
            "FailedResourcesMap": {},
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            result = cost_attribution_tagger(
                resource_arns=[
                    "arn:aws:lambda:us-east-1:123:fn",
                ],
                required_tags={
                    "env": "prod",
                    "team": "platform",
                },
            )

        assert result.resources_tagged == 1
        assert result.already_compliant == 0

    def test_no_existing_tags(self) -> None:
        mock_tagging = MagicMock()
        mock_tagging.get_resources.return_value = {
            "ResourceTagMappingList": [],
        }
        mock_tagging.tag_resources.return_value = {
            "FailedResourcesMap": {},
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            result = cost_attribution_tagger(
                resource_arns=["arn:aws:sqs:us-east-1:123:q1"],
                required_tags={"env": "dev"},
            )

        assert result.resources_tagged == 1

    def test_get_resources_error(self) -> None:
        mock_tagging = MagicMock()
        mock_tagging.get_resources.side_effect = _client_error(
            "InternalServiceException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to get tags"
            ):
                cost_attribution_tagger(
                    resource_arns=["arn:bad"],
                    required_tags={"env": "dev"},
                )

    def test_tag_resources_error(self) -> None:
        mock_tagging = MagicMock()
        mock_tagging.get_resources.return_value = {
            "ResourceTagMappingList": [],
        }
        mock_tagging.tag_resources.side_effect = _client_error(
            "InternalServiceException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            result = cost_attribution_tagger(
                resource_arns=["arn:aws:lambda:us-east-1:123:fn"],
                required_tags={"env": "dev"},
            )

        assert len(result.failures) == 1
        assert result.resources_tagged == 0

    def test_partial_tagging_failure(self) -> None:
        mock_tagging = MagicMock()
        mock_tagging.get_resources.return_value = {
            "ResourceTagMappingList": [],
        }
        mock_tagging.tag_resources.return_value = {
            "FailedResourcesMap": {
                "arn:bad": {"StatusCode": 400},
            },
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            result = cost_attribution_tagger(
                resource_arns=["arn:bad"],
                required_tags={"env": "dev"},
            )

        assert len(result.failures) == 1
        assert "partially failed" in result.failures[0]

    def test_multiple_resources_mixed(self) -> None:
        mock_tagging = MagicMock()

        call_idx = {"n": 0}

        def get_resources_side_effect(**kwargs: Any) -> dict[str, Any]:
            call_idx["n"] += 1
            if call_idx["n"] == 1:
                return {
                    "ResourceTagMappingList": [
                        {
                            "ResourceARN": "arn1",
                            "Tags": [
                                {"Key": "env", "Value": "prod"},
                            ],
                        },
                    ],
                }
            return {"ResourceTagMappingList": []}

        mock_tagging.get_resources.side_effect = (
            get_resources_side_effect
        )
        mock_tagging.tag_resources.return_value = {
            "FailedResourcesMap": {},
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_tagging,
        ):
            result = cost_attribution_tagger(
                resource_arns=["arn1", "arn2"],
                required_tags={"env": "prod"},
            )

        assert result.resources_checked == 2
        assert result.already_compliant == 1
        assert result.resources_tagged == 1


# ---------------------------------------------------------------------------
# 5. DynamoDB Capacity Advisor tests
# ---------------------------------------------------------------------------


class TestDynamoDBCapacityAdvisor:
    def test_pay_per_request_table(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "BillingModeSummary": {
                    "BillingMode": "PAY_PER_REQUEST",
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0,
                },
            },
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = dynamodb_capacity_advisor(
                table_names=["tbl"],
                region_name=REGION,
            )

        assert result.total_analyzed == 1
        assert "on-demand" in result.tables[0].recommendation

    def test_low_utilization_provisioned(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 100,
                    "WriteCapacityUnits": 100,
                },
            },
        }

        cw_call = {"n": 0}

        def cw_metrics(**kwargs: Any) -> dict[str, Any]:
            cw_call["n"] += 1
            if cw_call["n"] == 1:
                # RCU: low usage
                return {"Datapoints": [{"Sum": 5.0}]}
            # WCU: low usage
            return {"Datapoints": [{"Sum": 3.0}]}

        mock_cw.get_metric_statistics.side_effect = cw_metrics

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = dynamodb_capacity_advisor(
                table_names=["tbl"],
            )

        assert "low utilization" in result.tables[0].recommendation.lower()

    def test_high_utilization_provisioned(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 100,
                    "WriteCapacityUnits": 100,
                },
            },
        }

        cw_call = {"n": 0}

        def cw_metrics(**kwargs: Any) -> dict[str, Any]:
            cw_call["n"] += 1
            if cw_call["n"] == 1:
                return {"Datapoints": [{"Sum": 90.0}]}
            return {"Datapoints": [{"Sum": 85.0}]}

        mock_cw.get_metric_statistics.side_effect = cw_metrics

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = dynamodb_capacity_advisor(
                table_names=["tbl"],
            )

        assert "high utilization" in result.tables[0].recommendation.lower()

    def test_moderate_utilization(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 100,
                    "WriteCapacityUnits": 100,
                },
            },
        }

        cw_call = {"n": 0}

        def cw_metrics(**kwargs: Any) -> dict[str, Any]:
            cw_call["n"] += 1
            if cw_call["n"] == 1:
                return {"Datapoints": [{"Sum": 50.0}]}
            return {"Datapoints": [{"Sum": 50.0}]}

        mock_cw.get_metric_statistics.side_effect = cw_metrics

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = dynamodb_capacity_advisor(
                table_names=["tbl"],
            )

        assert "moderate" in result.tables[0].recommendation.lower()

    def test_zero_provisioned_capacity(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0,
                },
            },
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = dynamodb_capacity_advisor(
                table_names=["tbl"],
            )

        assert "zero" in result.tables[0].recommendation.lower()

    def test_describe_table_error(self) -> None:
        mock_ddb = MagicMock()
        mock_ddb.describe_table.side_effect = _client_error(
            "ResourceNotFoundException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_ddb,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to describe table"
            ):
                dynamodb_capacity_advisor(
                    table_names=["bad-tbl"],
                )

    def test_rcu_metrics_error(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 100,
                    "WriteCapacityUnits": 100,
                },
            },
        }
        mock_cw.get_metric_statistics.side_effect = _client_error(
            "InternalServiceFault"
        )

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to get RCU metrics"
            ):
                dynamodb_capacity_advisor(
                    table_names=["tbl"],
                )

    def test_wcu_metrics_error(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 100,
                    "WriteCapacityUnits": 100,
                },
            },
        }

        cw_call = {"n": 0}

        def cw_metrics(**kwargs: Any) -> dict[str, Any]:
            cw_call["n"] += 1
            if cw_call["n"] == 1:
                return {"Datapoints": []}
            raise _client_error("InternalServiceFault")

        mock_cw.get_metric_statistics.side_effect = cw_metrics

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to get WCU metrics"
            ):
                dynamodb_capacity_advisor(
                    table_names=["tbl"],
                )

    def test_multiple_tables(self) -> None:
        mock_ddb = MagicMock()
        mock_cw = MagicMock()

        mock_ddb.describe_table.return_value = {
            "Table": {
                "TableName": "tbl",
                "BillingModeSummary": {
                    "BillingMode": "PAY_PER_REQUEST",
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 0,
                    "WriteCapacityUnits": 0,
                },
            },
        }
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [],
        }

        def client_factory(
            service: str, region_name: str | None = None
        ) -> MagicMock:
            if service == "dynamodb":
                return mock_ddb
            return mock_cw

        with patch(
            "aws_util.cost_optimization.get_client",
            side_effect=client_factory,
        ):
            result = dynamodb_capacity_advisor(
                table_names=["tbl1", "tbl2"],
            )

        assert result.total_analyzed == 2
        assert len(result.tables) == 2


# ---------------------------------------------------------------------------
# 6. Log Retention Enforcer tests
# ---------------------------------------------------------------------------


class TestLogRetentionEnforcer:
    def test_sets_retention_on_groups_without_policy(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {"logGroupName": "/aws/lambda/fn1"},
                {"logGroupName": "/aws/lambda/fn2"},
            ],
        }
        mock_logs.put_retention_policy.return_value = {}

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer(
                retention_days=30,
                region_name=REGION,
            )

        assert result.groups_updated == 2
        assert len(result.changes) == 2
        assert result.changes[0].new_retention_days == 30
        assert result.changes[0].previous_retention_days is None

    def test_already_compliant_groups(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {
                    "logGroupName": "/aws/lambda/fn1",
                    "retentionInDays": 14,
                },
                {
                    "logGroupName": "/aws/lambda/fn2",
                    "retentionInDays": 30,
                },
            ],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer(retention_days=30)

        assert result.groups_already_compliant == 2
        assert result.groups_updated == 0

    def test_reduces_longer_retention(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {
                    "logGroupName": "/aws/lambda/fn1",
                    "retentionInDays": 90,
                },
            ],
        }
        mock_logs.put_retention_policy.return_value = {}

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer(retention_days=30)

        assert result.groups_updated == 1
        assert result.changes[0].previous_retention_days == 90
        assert result.changes[0].new_retention_days == 30

    def test_mixed_groups(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {
                    "logGroupName": "/aws/lambda/fn1",
                    "retentionInDays": 7,
                },
                {"logGroupName": "/aws/lambda/fn2"},
                {
                    "logGroupName": "/aws/lambda/fn3",
                    "retentionInDays": 365,
                },
            ],
        }
        mock_logs.put_retention_policy.return_value = {}

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer(retention_days=30)

        assert result.groups_already_compliant == 1
        assert result.groups_updated == 2

    def test_describe_log_groups_error(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.side_effect = _client_error(
            "ServiceUnavailableException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            with pytest.raises(
                RuntimeError, match="Failed to list log groups"
            ):
                log_retention_enforcer()

    def test_put_retention_policy_error(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {"logGroupName": "/aws/lambda/fn1"},
            ],
        }
        mock_logs.put_retention_policy.side_effect = _client_error(
            "InvalidParameterException"
        )

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer(retention_days=30)

        assert result.groups_updated == 0
        assert len(result.failures) == 1

    def test_custom_prefix(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [
                {"logGroupName": "/custom/fn1"},
            ],
        }
        mock_logs.put_retention_policy.return_value = {}

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer(
                retention_days=14,
                log_group_prefix="/custom/",
            )

        assert result.groups_updated == 1
        mock_logs.describe_log_groups.assert_called_once_with(
            logGroupNamePrefix="/custom/",
        )

    def test_empty_log_groups(self) -> None:
        mock_logs = MagicMock()
        mock_logs.describe_log_groups.return_value = {
            "logGroups": [],
        }

        with patch(
            "aws_util.cost_optimization.get_client",
            return_value=mock_logs,
        ):
            result = log_retention_enforcer()

        assert result.groups_updated == 0
        assert result.groups_already_compliant == 0
        assert result.changes == []


# ==================================================================
# 7. trusted_advisor_report_to_s3
# ==================================================================


class TestTrustedAdvisorReportToS3:
    def test_success(self) -> None:
        mock_support = MagicMock()
        mock_support.describe_trusted_advisor_checks.return_value = {
            "checks": [
                {"id": "c1", "name": "Check1", "category": "cost_optimizing"},
            ],
        }
        mock_support.describe_trusted_advisor_check_result.return_value = {
            "result": {"status": "ok", "flaggedResources": []},
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}

        def factory(svc, region_name=None):
            return {"support": mock_support, "s3": mock_s3}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = trusted_advisor_report_to_s3(
                bucket="reports", report_key="ta_report.json",
            )

        assert result.checks_count == 1
        assert result.flagged_resources == 0
        assert result.s3_key == "ta_report.json"
        assert result.alerts_sent == 0

    def test_with_sns_alert(self) -> None:
        mock_support = MagicMock()
        mock_support.describe_trusted_advisor_checks.return_value = {
            "checks": [{"id": "c1", "name": "Check1", "category": "security"}],
        }
        mock_support.describe_trusted_advisor_check_result.return_value = {
            "result": {"status": "error", "flaggedResources": [{"resource": "r1"}]},
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}
        mock_sns = MagicMock()
        mock_sns.publish.return_value = {}

        def factory(svc, region_name=None):
            return {"support": mock_support, "s3": mock_s3, "sns": mock_sns}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = trusted_advisor_report_to_s3(
                bucket="reports", report_key="ta.json",
                sns_topic_arn="arn:aws:sns:us-east-1:123:alerts",
            )

        assert result.alerts_sent == 1
        assert result.flagged_resources == 1

    def test_describe_checks_error(self) -> None:
        mock_support = MagicMock()
        mock_support.describe_trusted_advisor_checks.side_effect = _client_error("SubscriptionRequiredException")
        mock_s3 = MagicMock()

        def factory(svc, region_name=None):
            return {"support": mock_support, "s3": mock_s3}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_checks failed"):
                trusted_advisor_report_to_s3(bucket="b", report_key="k")

    def test_s3_upload_error(self) -> None:
        mock_support = MagicMock()
        mock_support.describe_trusted_advisor_checks.return_value = {"checks": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = _client_error("AccessDenied")

        def factory(svc, region_name=None):
            return {"support": mock_support, "s3": mock_s3}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="s3 upload failed"):
                trusted_advisor_report_to_s3(bucket="b", report_key="k")

    def test_category_filter(self) -> None:
        mock_support = MagicMock()
        mock_support.describe_trusted_advisor_checks.return_value = {
            "checks": [
                {"id": "c1", "name": "CostCheck", "category": "cost_optimizing"},
                {"id": "c2", "name": "SecCheck", "category": "security"},
            ],
        }
        mock_support.describe_trusted_advisor_check_result.return_value = {
            "result": {"status": "ok", "flaggedResources": []},
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}

        def factory(svc, region_name=None):
            return {"support": mock_support, "s3": mock_s3}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = trusted_advisor_report_to_s3(
                bucket="b", report_key="k",
                check_categories=["security"],
            )

        assert result.checks_count == 1


# ==================================================================
# 8. cost_and_usage_report_analyzer
# ==================================================================


class TestCostAndUsageReportAnalyzer:
    def test_success_with_anomalies(self) -> None:
        mock_athena = MagicMock()
        mock_athena.start_query_execution.return_value = {"QueryExecutionId": "qe-1"}
        mock_athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}},
        }
        mock_athena.get_query_results.return_value = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "service"}, {"VarCharValue": "cost"}]},
                    {"Data": [{"VarCharValue": "EC2"}, {"VarCharValue": "800"}]},
                    {"Data": [{"VarCharValue": "S3"}, {"VarCharValue": "200"}]},
                ],
            },
        }
        mock_sns = MagicMock()
        mock_sns.publish.return_value = {}

        def factory(svc, region_name=None):
            return {"athena": mock_athena, "sns": mock_sns}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with patch("time.sleep", lambda _: None):
                result = cost_and_usage_report_analyzer(
                    database="cur_db", table="cur_table",
                    output_location="s3://results/",
                    threshold_percent=50.0,
                    sns_topic_arn="arn:sns",
                )

        assert result.query_execution_id == "qe-1"
        assert result.services_analyzed == 2
        assert result.anomalies_found == 1  # EC2 is 80% > 50%
        assert result.alert_sent is True

    def test_no_anomalies(self) -> None:
        mock_athena = MagicMock()
        mock_athena.start_query_execution.return_value = {"QueryExecutionId": "qe-1"}
        mock_athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}},
        }
        mock_athena.get_query_results.return_value = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "service"}, {"VarCharValue": "cost"}]},
                    {"Data": [{"VarCharValue": "EC2"}, {"VarCharValue": "50"}]},
                    {"Data": [{"VarCharValue": "S3"}, {"VarCharValue": "50"}]},
                ],
            },
        }
        mock_sns = MagicMock()

        def factory(svc, region_name=None):
            return {"athena": mock_athena, "sns": mock_sns}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with patch("time.sleep", lambda _: None):
                result = cost_and_usage_report_analyzer(
                    database="db", table="t",
                    output_location="s3://r/",
                    threshold_percent=60.0,
                    sns_topic_arn="arn:sns",
                )

        assert result.anomalies_found == 0
        assert result.alert_sent is False

    def test_start_query_error(self) -> None:
        mock_athena = MagicMock()
        mock_athena.start_query_execution.side_effect = _client_error("InvalidRequestException")
        mock_sns = MagicMock()

        def factory(svc, region_name=None):
            return {"athena": mock_athena, "sns": mock_sns}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="start_query failed"):
                cost_and_usage_report_analyzer(
                    database="db", table="t",
                    output_location="s3://r/",
                    threshold_percent=50.0,
                    sns_topic_arn="arn:sns",
                )

    def test_query_failed(self) -> None:
        mock_athena = MagicMock()
        mock_athena.start_query_execution.return_value = {"QueryExecutionId": "qe-1"}
        mock_athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "FAILED"}},
        }
        mock_sns = MagicMock()

        def factory(svc, region_name=None):
            return {"athena": mock_athena, "sns": mock_sns}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with patch("time.sleep", lambda _: None):
                with pytest.raises(RuntimeError, match="query ended with state"):
                    cost_and_usage_report_analyzer(
                        database="db", table="t",
                        output_location="s3://r/",
                        threshold_percent=50.0,
                        sns_topic_arn="arn:sns",
                    )


# ==================================================================
# 9. savings_plan_coverage_reporter
# ==================================================================


class TestSavingsPlanCoverageReporter:
    def test_success(self) -> None:
        mock_ce = MagicMock()
        mock_ce.get_savings_plans_coverage.return_value = {
            "SavingsPlansCoverages": [
                {
                    "Coverage": {
                        "TotalCost": {"Amount": "1000"},
                        "CoveredCost": {"Amount": "800"},
                    },
                }
            ],
        }
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}
        mock_cw = MagicMock()
        mock_cw.put_metric_data.return_value = {}

        def factory(svc, region_name=None):
            return {"ce": mock_ce, "s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = savings_plan_coverage_reporter(
                bucket="reports", report_key="sp.json",
                start_date="2024-01-01", end_date="2024-02-01",
                metric_namespace="Custom/SP",
            )

        assert result.coverage_percent == 80.0
        assert result.total_spend == 1000.0
        assert result.covered_spend == 800.0
        assert result.s3_key == "sp.json"

    def test_ce_error(self) -> None:
        mock_ce = MagicMock()
        mock_ce.get_savings_plans_coverage.side_effect = _client_error("DataUnavailableException")
        mock_s3 = MagicMock()
        mock_cw = MagicMock()

        def factory(svc, region_name=None):
            return {"ce": mock_ce, "s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="get_coverage failed"):
                savings_plan_coverage_reporter(
                    bucket="b", report_key="k",
                    start_date="2024-01-01", end_date="2024-02-01",
                    metric_namespace="ns",
                )

    def test_s3_upload_error(self) -> None:
        mock_ce = MagicMock()
        mock_ce.get_savings_plans_coverage.return_value = {"SavingsPlansCoverages": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.side_effect = _client_error("AccessDenied")
        mock_cw = MagicMock()

        def factory(svc, region_name=None):
            return {"ce": mock_ce, "s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="s3 upload failed"):
                savings_plan_coverage_reporter(
                    bucket="b", report_key="k",
                    start_date="2024-01-01", end_date="2024-02-01",
                    metric_namespace="ns",
                )

    def test_cw_metric_error(self) -> None:
        mock_ce = MagicMock()
        mock_ce.get_savings_plans_coverage.return_value = {"SavingsPlansCoverages": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}
        mock_cw = MagicMock()
        mock_cw.put_metric_data.side_effect = _client_error("InternalError")

        def factory(svc, region_name=None):
            return {"ce": mock_ce, "s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="put_metric_data failed"):
                savings_plan_coverage_reporter(
                    bucket="b", report_key="k",
                    start_date="2024-01-01", end_date="2024-02-01",
                    metric_namespace="ns",
                )

    def test_zero_spend(self) -> None:
        mock_ce = MagicMock()
        mock_ce.get_savings_plans_coverage.return_value = {"SavingsPlansCoverages": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}
        mock_cw = MagicMock()
        mock_cw.put_metric_data.return_value = {}

        def factory(svc, region_name=None):
            return {"ce": mock_ce, "s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = savings_plan_coverage_reporter(
                bucket="b", report_key="k",
                start_date="2024-01-01", end_date="2024-02-01",
                metric_namespace="ns",
            )

        assert result.coverage_percent == 0.0


# ==================================================================
# 10. ec2_idle_instance_stopper
# ==================================================================


class TestEC2IdleInstanceStopper:
    def test_success_stop_past_grace(self) -> None:
        import time

        mock_ec2 = MagicMock()
        mock_ec2.describe_instances.return_value = {
            "Reservations": [
                {"Instances": [{"InstanceId": "i-123"}]},
            ],
        }
        mock_ec2.stop_instances.return_value = {}
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Average": 1.0}],
        }
        # Already on watch list with first_seen far in the past
        mock_ddb = MagicMock()
        mock_ddb.get_item.return_value = {
            "Item": {"pk": {"S": "i-123"}, "first_seen": {"N": "0"}},
        }

        def factory(svc, region_name=None):
            return {"ec2": mock_ec2, "cloudwatch": mock_cw, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = ec2_idle_instance_stopper(
                table_name="idle_watch", cpu_threshold=5.0, grace_period_hours=24,
            )

        assert result.instances_checked == 1
        assert result.idle_found == 1
        assert result.stopped_count == 1
        mock_ec2.stop_instances.assert_called_once()

    def test_new_idle_added_to_watch(self) -> None:
        mock_ec2 = MagicMock()
        mock_ec2.describe_instances.return_value = {
            "Reservations": [
                {"Instances": [{"InstanceId": "i-456"}]},
            ],
        }
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Average": 2.0}],
        }
        mock_ddb = MagicMock()
        mock_ddb.get_item.return_value = {}  # Not on watch list
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"ec2": mock_ec2, "cloudwatch": mock_cw, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = ec2_idle_instance_stopper(
                table_name="t", cpu_threshold=5.0,
            )

        assert result.idle_found == 1
        assert result.watched_count == 1
        assert result.stopped_count == 0

    def test_not_idle(self) -> None:
        mock_ec2 = MagicMock()
        mock_ec2.describe_instances.return_value = {
            "Reservations": [
                {"Instances": [{"InstanceId": "i-busy"}]},
            ],
        }
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Average": 80.0}],
        }
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"ec2": mock_ec2, "cloudwatch": mock_cw, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = ec2_idle_instance_stopper(table_name="t")

        assert result.idle_found == 0
        assert result.stopped_count == 0

    def test_describe_instances_error(self) -> None:
        mock_ec2 = MagicMock()
        mock_ec2.describe_instances.side_effect = _client_error("UnauthorizedOperation")
        mock_cw = MagicMock()
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"ec2": mock_ec2, "cloudwatch": mock_cw, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_instances failed"):
                ec2_idle_instance_stopper(table_name="t")


# ==================================================================
# 11. rds_idle_snapshot_and_delete
# ==================================================================


class TestRDSIdleSnapshotAndDelete:
    def test_dry_run(self) -> None:
        mock_rds = MagicMock()
        mock_rds.describe_db_instances.return_value = {
            "DBInstances": [{"DBInstanceIdentifier": "db-1"}],
        }
        mock_rds.create_db_snapshot.return_value = {}
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Sum": 0}],
        }

        def factory(svc, region_name=None):
            return {"rds": mock_rds, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = rds_idle_snapshot_and_delete(dry_run=True)

        assert result.idle_found == 1
        assert result.snapshots_created == 1
        assert result.deleted_count == 0
        assert result.dry_run is True
        mock_rds.delete_db_instance.assert_not_called()

    def test_delete_when_not_dry_run(self) -> None:
        mock_rds = MagicMock()
        mock_rds.describe_db_instances.return_value = {
            "DBInstances": [{"DBInstanceIdentifier": "db-1"}],
        }
        mock_rds.create_db_snapshot.return_value = {}
        mock_rds.delete_db_instance.return_value = {}
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Sum": 0}],
        }

        def factory(svc, region_name=None):
            return {"rds": mock_rds, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = rds_idle_snapshot_and_delete(dry_run=False)

        assert result.deleted_count == 1
        assert result.dry_run is False

    def test_not_idle(self) -> None:
        mock_rds = MagicMock()
        mock_rds.describe_db_instances.return_value = {
            "DBInstances": [{"DBInstanceIdentifier": "db-busy"}],
        }
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Sum": 100}],
        }

        def factory(svc, region_name=None):
            return {"rds": mock_rds, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = rds_idle_snapshot_and_delete()

        assert result.idle_found == 0
        assert result.snapshots_created == 0

    def test_describe_db_error(self) -> None:
        mock_rds = MagicMock()
        mock_rds.describe_db_instances.side_effect = _client_error("AccessDenied")
        mock_cw = MagicMock()

        def factory(svc, region_name=None):
            return {"rds": mock_rds, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_db_instances failed"):
                rds_idle_snapshot_and_delete()

    def test_with_sns_notification(self) -> None:
        mock_rds = MagicMock()
        mock_rds.describe_db_instances.return_value = {
            "DBInstances": [{"DBInstanceIdentifier": "db-1"}],
        }
        mock_rds.create_db_snapshot.return_value = {}
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Sum": 0}],
        }
        mock_sns = MagicMock()
        mock_sns.publish.return_value = {}

        def factory(svc, region_name=None):
            return {"rds": mock_rds, "cloudwatch": mock_cw, "sns": mock_sns}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = rds_idle_snapshot_and_delete(
                sns_topic_arn="arn:aws:sns:us-east-1:123:topic",
            )

        assert result.snapshots_created == 1
        mock_sns.publish.assert_called_once()


# ==================================================================
# 12. ecr_lifecycle_policy_applier
# ==================================================================


class TestECRLifecyclePolicyApplier:
    def test_success(self) -> None:
        mock_ecr = MagicMock()
        mock_ecr.describe_repositories.return_value = {
            "repositories": [
                {"repositoryName": "repo1"},
                {"repositoryName": "repo2"},
            ],
        }
        mock_ecr.put_lifecycle_policy.return_value = {}
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"ecr": mock_ecr, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = ecr_lifecycle_policy_applier(table_name="ecr_audit")

        assert result.repositories_updated == 2
        assert result.already_configured == 0
        assert result.errors == 0

    def test_already_exists(self) -> None:
        mock_ecr = MagicMock()
        mock_ecr.describe_repositories.return_value = {
            "repositories": [{"repositoryName": "repo1"}],
        }
        mock_ecr.put_lifecycle_policy.side_effect = _client_error("LifecyclePolicyAlreadyExistsException")
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"ecr": mock_ecr, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = ecr_lifecycle_policy_applier(table_name="t")

        assert result.already_configured == 1
        assert result.repositories_updated == 0

    def test_other_ecr_error(self) -> None:
        mock_ecr = MagicMock()
        mock_ecr.describe_repositories.return_value = {
            "repositories": [{"repositoryName": "repo1"}],
        }
        mock_ecr.put_lifecycle_policy.side_effect = _client_error("ServerException")
        mock_ddb = MagicMock()
        mock_ddb.put_item.return_value = {}

        def factory(svc, region_name=None):
            return {"ecr": mock_ecr, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = ecr_lifecycle_policy_applier(table_name="t")

        assert result.errors == 1

    def test_describe_repos_error(self) -> None:
        mock_ecr = MagicMock()
        mock_ecr.describe_repositories.side_effect = _client_error("AccessDeniedException")
        mock_ddb = MagicMock()

        def factory(svc, region_name=None):
            return {"ecr": mock_ecr, "dynamodb": mock_ddb}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="describe_repositories failed"):
                ecr_lifecycle_policy_applier(table_name="t")


# ==================================================================
# 13. s3_intelligent_tiering_enrollor
# ==================================================================


class TestS3IntelligentTieringEnrollor:
    def test_success(self) -> None:
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {
            "Buckets": [{"Name": "bucket1"}, {"Name": "bucket2"}],
        }
        mock_s3.put_bucket_intelligent_tiering_configuration.return_value = {}
        mock_cw = MagicMock()
        mock_cw.put_metric_data.return_value = {}

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = s3_intelligent_tiering_enrollor(metric_namespace="Custom/S3")

        assert result.buckets_checked == 2
        assert result.buckets_enrolled == 2
        assert result.already_enrolled == 0

    def test_no_such_bucket_skipped(self) -> None:
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {
            "Buckets": [{"Name": "gone-bucket"}],
        }
        mock_s3.put_bucket_intelligent_tiering_configuration.side_effect = _client_error("NoSuchBucket")
        mock_cw = MagicMock()
        mock_cw.put_metric_data.return_value = {}

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = s3_intelligent_tiering_enrollor(metric_namespace="ns")

        assert result.buckets_enrolled == 0
        assert result.already_enrolled == 0

    def test_list_buckets_error(self) -> None:
        mock_s3 = MagicMock()
        mock_s3.list_buckets.side_effect = _client_error("AccessDenied")
        mock_cw = MagicMock()

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="list_buckets failed"):
                s3_intelligent_tiering_enrollor(metric_namespace="ns")

    def test_cw_error(self) -> None:
        mock_s3 = MagicMock()
        mock_s3.list_buckets.return_value = {"Buckets": []}
        mock_cw = MagicMock()
        mock_cw.put_metric_data.side_effect = _client_error("InternalError")

        def factory(svc, region_name=None):
            return {"s3": mock_s3, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="put_metric_data failed"):
                s3_intelligent_tiering_enrollor(metric_namespace="ns")


# ==================================================================
# 14. lambda_dead_code_detector
# ==================================================================


class TestLambdaDeadCodeDetector:
    def test_success_no_archive(self) -> None:
        mock_lam = MagicMock()
        mock_lam.list_functions.return_value = {
            "Functions": [
                {"FunctionName": "fn1"},
                {"FunctionName": "fn2"},
            ],
        }
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.side_effect = [
            {"Datapoints": []},  # fn1: no datapoints => 0 invocations
            {"Datapoints": [{"Sum": 100}]},  # fn2: active
        ]

        def factory(svc, region_name=None):
            return {"lambda": mock_lam, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = lambda_dead_code_detector()

        assert result.functions_checked == 2
        assert result.dead_functions == 1
        assert result.dead_function_names == ["fn1"]
        assert result.archived_count == 0

    def test_with_archive(self) -> None:
        import urllib.request

        mock_lam = MagicMock()
        mock_lam.list_functions.return_value = {
            "Functions": [{"FunctionName": "dead-fn"}],
        }
        mock_lam.get_function.return_value = {
            "Code": {"Location": "https://example.com/code.zip"},
        }
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {"Datapoints": []}
        mock_s3 = MagicMock()
        mock_s3.put_object.return_value = {}

        def factory(svc, region_name=None):
            return {"lambda": mock_lam, "cloudwatch": mock_cw, "s3": mock_s3}[svc]

        import io
        fake_response = io.BytesIO(b"zip-content")

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with patch("urllib.request.urlopen", return_value=fake_response):
                result = lambda_dead_code_detector(bucket="archive-bucket")

        assert result.dead_functions == 1
        assert result.archived_count == 1

    def test_list_functions_error(self) -> None:
        mock_lam = MagicMock()
        mock_lam.list_functions.side_effect = _client_error("AccessDeniedException")
        mock_cw = MagicMock()

        def factory(svc, region_name=None):
            return {"lambda": mock_lam, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            with pytest.raises(RuntimeError, match="list_functions failed"):
                lambda_dead_code_detector()

    def test_all_active(self) -> None:
        mock_lam = MagicMock()
        mock_lam.list_functions.return_value = {
            "Functions": [{"FunctionName": "active-fn"}],
        }
        mock_cw = MagicMock()
        mock_cw.get_metric_statistics.return_value = {
            "Datapoints": [{"Sum": 50}],
        }

        def factory(svc, region_name=None):
            return {"lambda": mock_lam, "cloudwatch": mock_cw}[svc]

        with patch("aws_util.cost_optimization.get_client", side_effect=factory):
            result = lambda_dead_code_detector()

        assert result.dead_functions == 0
        assert result.dead_function_names == []
