"""Tests for aws_util.config_service module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.config_service as mod
from aws_util.config_service import (
    ComplianceResult,
    ConfigRuleResult,
    ConfigurationRecorderResult,
    RemediationConfigResult,
    delete_config_rule,
    deliver_config_snapshot,
    describe_compliance_by_config_rule,
    describe_config_rules,
    describe_configuration_aggregators,
    describe_configuration_recorders,
    describe_remediation_configurations,
    get_compliance_details_by_config_rule,
    get_resource_config_history,
    list_discovered_resources,
    put_aggregation_authorization,
    put_config_rule,
    put_configuration_recorder,
    put_remediation_configurations,
    start_config_rules_evaluation,
    start_configuration_recorder,
    start_remediation_execution,
    stop_configuration_recorder,
    associate_resource_types,
    batch_get_aggregate_resource_config,
    batch_get_resource_config,
    delete_aggregation_authorization,
    delete_configuration_aggregator,
    delete_configuration_recorder,
    delete_conformance_pack,
    delete_delivery_channel,
    delete_evaluation_results,
    delete_organization_config_rule,
    delete_organization_conformance_pack,
    delete_pending_aggregation_request,
    delete_remediation_configuration,
    delete_remediation_exceptions,
    delete_resource_config,
    delete_retention_configuration,
    delete_service_linked_configuration_recorder,
    delete_stored_query,
    describe_aggregate_compliance_by_config_rules,
    describe_aggregate_compliance_by_conformance_packs,
    describe_aggregation_authorizations,
    describe_compliance_by_resource,
    describe_config_rule_evaluation_status,
    describe_configuration_aggregator_sources_status,
    describe_configuration_recorder_status,
    describe_conformance_pack_compliance,
    describe_conformance_pack_status,
    describe_conformance_packs,
    describe_delivery_channel_status,
    describe_delivery_channels,
    describe_organization_config_rule_statuses,
    describe_organization_config_rules,
    describe_organization_conformance_pack_statuses,
    describe_organization_conformance_packs,
    describe_pending_aggregation_requests,
    describe_remediation_exceptions,
    describe_remediation_execution_status,
    describe_retention_configurations,
    disassociate_resource_types,
    get_aggregate_compliance_details_by_config_rule,
    get_aggregate_config_rule_compliance_summary,
    get_aggregate_conformance_pack_compliance_summary,
    get_aggregate_discovered_resource_counts,
    get_aggregate_resource_config,
    get_compliance_details_by_resource,
    get_compliance_summary_by_config_rule,
    get_compliance_summary_by_resource_type,
    get_conformance_pack_compliance_details,
    get_conformance_pack_compliance_summary,
    get_custom_rule_policy,
    get_discovered_resource_counts,
    get_organization_config_rule_detailed_status,
    get_organization_conformance_pack_detailed_status,
    get_organization_custom_rule_policy,
    get_resource_evaluation_summary,
    get_stored_query,
    list_aggregate_discovered_resources,
    list_configuration_recorders,
    list_conformance_pack_compliance_scores,
    list_resource_evaluations,
    list_stored_queries,
    list_tags_for_resource,
    put_configuration_aggregator,
    put_conformance_pack,
    put_delivery_channel,
    put_evaluations,
    put_external_evaluation,
    put_organization_config_rule,
    put_organization_conformance_pack,
    put_remediation_exceptions,
    put_resource_config,
    put_retention_configuration,
    put_service_linked_configuration_recorder,
    put_stored_query,
    select_aggregate_resource_config,
    select_resource_config,
    start_resource_evaluation,
    tag_resource,
    untag_resource,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str = "InternalError", message: str = "boom") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}},
        "TestOp",
    )


def _mock_client_with_paginator(pages: list[dict]) -> MagicMock:
    """Return a mock client whose paginator yields the given pages."""
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = iter(pages)
    mock.get_paginator.return_value = paginator
    return mock


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_config_rule_result_defaults(self):
        r = ConfigRuleResult(config_rule_name="rule-1")
        assert r.config_rule_name == "rule-1"
        assert r.config_rule_arn is None
        assert r.config_rule_id is None
        assert r.source == {}
        assert r.scope is None
        assert r.compliance_type is None
        assert r.state is None
        assert r.extra == {}

    def test_config_rule_result_frozen(self):
        r = ConfigRuleResult(config_rule_name="rule-1")
        with pytest.raises(Exception):
            r.config_rule_name = "other"  # type: ignore[misc]

    def test_configuration_recorder_result_defaults(self):
        r = ConfigurationRecorderResult(name="default")
        assert r.name == "default"
        assert r.role_arn == ""
        assert r.recording_group is None
        assert r.status is None
        assert r.extra == {}

    def test_compliance_result_defaults(self):
        r = ComplianceResult(config_rule_name="rule-1")
        assert r.config_rule_name == "rule-1"
        assert r.resource_type is None
        assert r.resource_id is None
        assert r.compliance_type == ""
        assert r.annotation is None
        assert r.ordering_timestamp is None
        assert r.extra == {}

    def test_remediation_config_result_defaults(self):
        r = RemediationConfigResult(config_rule_name="rule-1")
        assert r.config_rule_name == "rule-1"
        assert r.target_type == ""
        assert r.target_id == ""
        assert r.parameters is None
        assert r.automatic is False
        assert r.retry_attempt_seconds is None
        assert r.maximum_automatic_attempts is None
        assert r.extra == {}

    def test_remediation_config_result_full(self):
        r = RemediationConfigResult(
            config_rule_name="rule-1",
            target_type="SSM_DOCUMENT",
            target_id="doc-1",
            parameters={"key": {"StaticValue": {"Values": ["v"]}}},
            automatic=True,
            retry_attempt_seconds=60,
            maximum_automatic_attempts=5,
            extra={"Arn": "arn:..."},
        )
        assert r.automatic is True
        assert r.retry_attempt_seconds == 60


# ---------------------------------------------------------------------------
# put_config_rule
# ---------------------------------------------------------------------------


class TestPutConfigRule:
    def test_success_minimal(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        put_config_rule(
            "rule-1",
            source={"Owner": "AWS", "SourceIdentifier": "S3_BUCKET_VERSIONING_ENABLED"},
            region_name=REGION,
        )
        mock.put_config_rule.assert_called_once()
        call_kwargs = mock.put_config_rule.call_args[1]
        assert call_kwargs["ConfigRule"]["ConfigRuleName"] == "rule-1"
        assert "Scope" not in call_kwargs["ConfigRule"]
        assert "InputParameters" not in call_kwargs["ConfigRule"]

    def test_success_with_scope_and_params(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        put_config_rule(
            "rule-1",
            source={"Owner": "AWS", "SourceIdentifier": "S3_BUCKET_VERSIONING_ENABLED"},
            scope={"ComplianceResourceTypes": ["AWS::S3::Bucket"]},
            input_parameters='{"key":"value"}',
            region_name=REGION,
        )
        call_kwargs = mock.put_config_rule.call_args[1]
        assert call_kwargs["ConfigRule"]["Scope"]["ComplianceResourceTypes"] == ["AWS::S3::Bucket"]
        assert call_kwargs["ConfigRule"]["InputParameters"] == '{"key":"value"}'

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.put_config_rule.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to put config rule"):
            put_config_rule(
                "rule-1",
                source={"Owner": "AWS", "SourceIdentifier": "X"},
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# describe_config_rules
# ---------------------------------------------------------------------------


class TestDescribeConfigRules:
    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator([{"ConfigRules": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_config_rules(region_name=REGION)
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "ConfigRules": [
                        {
                            "ConfigRuleName": "rule-1",
                            "ConfigRuleArn": "arn:rule-1",
                            "ConfigRuleId": "id-1",
                            "Source": {"Owner": "AWS", "SourceIdentifier": "S3_BUCKET_VERSIONING_ENABLED"},
                            "Scope": {"ComplianceResourceTypes": ["AWS::S3::Bucket"]},
                            "ConfigRuleState": "ACTIVE",
                            "Description": "Test rule",
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_config_rules(region_name=REGION)
        assert len(result) == 1
        assert result[0].config_rule_name == "rule-1"
        assert result[0].config_rule_arn == "arn:rule-1"
        assert result[0].config_rule_id == "id-1"
        assert result[0].state == "ACTIVE"
        assert "Description" in result[0].extra

    def test_with_filter(self, monkeypatch):
        mock = _mock_client_with_paginator([{"ConfigRules": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        describe_config_rules(config_rule_names=["rule-1"], region_name=REGION)
        call_kwargs = mock.get_paginator.return_value.paginate.call_args[1]
        assert call_kwargs["ConfigRuleNames"] == ["rule-1"]

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="describe_config_rules failed"):
            describe_config_rules(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_config_rule
# ---------------------------------------------------------------------------


class TestDeleteConfigRule:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        delete_config_rule("rule-1", region_name=REGION)
        mock.delete_config_rule.assert_called_once_with(ConfigRuleName="rule-1")

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.delete_config_rule.side_effect = _client_error("NoSuchConfigRuleException")
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to delete config rule"):
            delete_config_rule("rule-1", region_name=REGION)


# ---------------------------------------------------------------------------
# start_config_rules_evaluation
# ---------------------------------------------------------------------------


class TestStartConfigRulesEvaluation:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        start_config_rules_evaluation(["rule-1", "rule-2"], region_name=REGION)
        mock.start_config_rules_evaluation.assert_called_once_with(
            ConfigRuleNames=["rule-1", "rule-2"],
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.start_config_rules_evaluation.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to start config rules evaluation"):
            start_config_rules_evaluation(["rule-1"], region_name=REGION)


# ---------------------------------------------------------------------------
# describe_compliance_by_config_rule
# ---------------------------------------------------------------------------


class TestDescribeComplianceByConfigRule:
    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator([{"ComplianceByConfigRules": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_compliance_by_config_rule(region_name=REGION)
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "ComplianceByConfigRules": [
                        {
                            "ConfigRuleName": "rule-1",
                            "Compliance": {"ComplianceType": "COMPLIANT"},
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_compliance_by_config_rule(region_name=REGION)
        assert len(result) == 1
        assert result[0].config_rule_name == "rule-1"
        assert result[0].compliance_type == "COMPLIANT"

    def test_with_filters(self, monkeypatch):
        mock = _mock_client_with_paginator([{"ComplianceByConfigRules": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        describe_compliance_by_config_rule(
            config_rule_names=["rule-1"],
            compliance_types=["NON_COMPLIANT"],
            region_name=REGION,
        )
        call_kwargs = mock.get_paginator.return_value.paginate.call_args[1]
        assert call_kwargs["ConfigRuleNames"] == ["rule-1"]
        assert call_kwargs["ComplianceTypes"] == ["NON_COMPLIANT"]

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="describe_compliance_by_config_rule failed"):
            describe_compliance_by_config_rule(region_name=REGION)


# ---------------------------------------------------------------------------
# get_compliance_details_by_config_rule
# ---------------------------------------------------------------------------


class TestGetComplianceDetailsByConfigRule:
    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator([{"EvaluationResults": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = get_compliance_details_by_config_rule("rule-1", region_name=REGION)
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "EvaluationResults": [
                        {
                            "EvaluationResultIdentifier": {
                                "EvaluationResultQualifier": {
                                    "ConfigRuleName": "rule-1",
                                    "ResourceType": "AWS::S3::Bucket",
                                    "ResourceId": "my-bucket",
                                }
                            },
                            "ComplianceType": "NON_COMPLIANT",
                            "Annotation": "Not versioned",
                            "OrderingTimestamp": "2025-01-01T00:00:00Z",
                            "ResultToken": "tok-1",
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = get_compliance_details_by_config_rule("rule-1", region_name=REGION)
        assert len(result) == 1
        assert result[0].config_rule_name == "rule-1"
        assert result[0].resource_type == "AWS::S3::Bucket"
        assert result[0].resource_id == "my-bucket"
        assert result[0].compliance_type == "NON_COMPLIANT"
        assert result[0].annotation == "Not versioned"
        assert result[0].ordering_timestamp == "2025-01-01T00:00:00Z"
        assert "ResultToken" in result[0].extra

    def test_with_filters(self, monkeypatch):
        mock = _mock_client_with_paginator([{"EvaluationResults": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        get_compliance_details_by_config_rule(
            "rule-1",
            compliance_types=["COMPLIANT"],
            limit=10,
            region_name=REGION,
        )
        call_kwargs = mock.get_paginator.return_value.paginate.call_args[1]
        assert call_kwargs["ComplianceTypes"] == ["COMPLIANT"]
        assert call_kwargs["Limit"] == 10

    def test_missing_ordering_timestamp(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "EvaluationResults": [
                        {
                            "EvaluationResultIdentifier": {
                                "EvaluationResultQualifier": {
                                    "ConfigRuleName": "rule-1",
                                }
                            },
                            "ComplianceType": "COMPLIANT",
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = get_compliance_details_by_config_rule("rule-1", region_name=REGION)
        assert result[0].ordering_timestamp is None

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="get_compliance_details_by_config_rule failed"):
            get_compliance_details_by_config_rule("rule-1", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_configuration_recorders
# ---------------------------------------------------------------------------


class TestDescribeConfigurationRecorders:
    def test_empty(self, monkeypatch):
        mock = MagicMock()
        mock.describe_configuration_recorders.return_value = {
            "ConfigurationRecorders": []
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_recorders(region_name=REGION)
        assert result == []

    def test_returns_results_with_status(self, monkeypatch):
        mock = MagicMock()
        mock.describe_configuration_recorders.return_value = {
            "ConfigurationRecorders": [
                {
                    "name": "default",
                    "roleARN": "arn:iam::123:role/config-role",
                    "recordingGroup": {"allSupported": True},
                }
            ]
        }
        mock.describe_configuration_recorder_status.return_value = {
            "ConfigurationRecordersStatus": [
                {"recording": True}
            ]
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_recorders(region_name=REGION)
        assert len(result) == 1
        assert result[0].name == "default"
        assert result[0].role_arn == "arn:iam::123:role/config-role"
        assert result[0].status == "recording"

    def test_status_stopped(self, monkeypatch):
        mock = MagicMock()
        mock.describe_configuration_recorders.return_value = {
            "ConfigurationRecorders": [{"name": "default", "roleARN": "arn:role"}]
        }
        mock.describe_configuration_recorder_status.return_value = {
            "ConfigurationRecordersStatus": [{"recording": False}]
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_recorders(region_name=REGION)
        assert result[0].status == "stopped"

    def test_status_error_ignored(self, monkeypatch):
        mock = MagicMock()
        mock.describe_configuration_recorders.return_value = {
            "ConfigurationRecorders": [{"name": "default", "roleARN": "arn:role"}]
        }
        mock.describe_configuration_recorder_status.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_recorders(region_name=REGION)
        assert result[0].status is None

    def test_with_names_filter(self, monkeypatch):
        mock = MagicMock()
        mock.describe_configuration_recorders.return_value = {
            "ConfigurationRecorders": []
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        describe_configuration_recorders(names=["rec-1"], region_name=REGION)
        call_kwargs = mock.describe_configuration_recorders.call_args[1]
        assert call_kwargs["ConfigurationRecorderNames"] == ["rec-1"]

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_configuration_recorders.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="describe_configuration_recorders failed"):
            describe_configuration_recorders(region_name=REGION)

    def test_pascal_case_keys(self, monkeypatch):
        """Handle PascalCase keys from some API responses."""
        mock = MagicMock()
        mock.describe_configuration_recorders.return_value = {
            "ConfigurationRecorders": [
                {
                    "Name": "default",
                    "RoleARN": "arn:role",
                    "RecordingGroup": {"allSupported": True},
                }
            ]
        }
        mock.describe_configuration_recorder_status.return_value = {
            "ConfigurationRecordersStatus": []
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_recorders(region_name=REGION)
        assert result[0].name == "default"
        assert result[0].role_arn == "arn:role"
        assert result[0].recording_group == {"allSupported": True}


# ---------------------------------------------------------------------------
# put_configuration_recorder
# ---------------------------------------------------------------------------


class TestPutConfigurationRecorder:
    def test_success_minimal(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        put_configuration_recorder("default", role_arn="arn:role", region_name=REGION)
        call_kwargs = mock.put_configuration_recorder.call_args[1]
        rec = call_kwargs["ConfigurationRecorder"]
        assert rec["name"] == "default"
        assert rec["roleARN"] == "arn:role"
        assert "recordingGroup" not in rec

    def test_success_with_recording_group(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        put_configuration_recorder(
            "default",
            role_arn="arn:role",
            recording_group={"allSupported": True},
            region_name=REGION,
        )
        call_kwargs = mock.put_configuration_recorder.call_args[1]
        assert call_kwargs["ConfigurationRecorder"]["recordingGroup"] == {"allSupported": True}

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.put_configuration_recorder.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to put configuration recorder"):
            put_configuration_recorder("default", role_arn="arn:role", region_name=REGION)


# ---------------------------------------------------------------------------
# start_configuration_recorder / stop_configuration_recorder
# ---------------------------------------------------------------------------


class TestStartStopConfigurationRecorder:
    def test_start_success(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        start_configuration_recorder("default", region_name=REGION)
        mock.start_configuration_recorder.assert_called_once_with(
            ConfigurationRecorderName="default",
        )

    def test_start_error(self, monkeypatch):
        mock = MagicMock()
        mock.start_configuration_recorder.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to start configuration recorder"):
            start_configuration_recorder("default", region_name=REGION)

    def test_stop_success(self, monkeypatch):
        mock = MagicMock()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        stop_configuration_recorder("default", region_name=REGION)
        mock.stop_configuration_recorder.assert_called_once_with(
            ConfigurationRecorderName="default",
        )

    def test_stop_error(self, monkeypatch):
        mock = MagicMock()
        mock.stop_configuration_recorder.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to stop configuration recorder"):
            stop_configuration_recorder("default", region_name=REGION)


# ---------------------------------------------------------------------------
# deliver_config_snapshot
# ---------------------------------------------------------------------------


class TestDeliverConfigSnapshot:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.deliver_config_snapshot.return_value = {
            "configSnapshotId": "snap-123"
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = deliver_config_snapshot("channel-1", region_name=REGION)
        assert result == "snap-123"

    def test_missing_snapshot_id(self, monkeypatch):
        mock = MagicMock()
        mock.deliver_config_snapshot.return_value = {}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = deliver_config_snapshot("channel-1", region_name=REGION)
        assert result == ""

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.deliver_config_snapshot.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to deliver config snapshot"):
            deliver_config_snapshot("channel-1", region_name=REGION)


# ---------------------------------------------------------------------------
# put_remediation_configurations
# ---------------------------------------------------------------------------


class TestPutRemediationConfigurations:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.put_remediation_configurations.return_value = {"FailedBatches": []}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = put_remediation_configurations(
            remediation_configs=[
                {
                    "ConfigRuleName": "rule-1",
                    "TargetType": "SSM_DOCUMENT",
                    "TargetId": "doc-1",
                }
            ],
            region_name=REGION,
        )
        assert result == []

    def test_with_failures(self, monkeypatch):
        mock = MagicMock()
        mock.put_remediation_configurations.return_value = {
            "FailedBatches": [{"FailureMessage": "oops"}]
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = put_remediation_configurations(
            remediation_configs=[{"ConfigRuleName": "rule-1"}],
            region_name=REGION,
        )
        assert len(result) == 1

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.put_remediation_configurations.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to put remediation configurations"):
            put_remediation_configurations(
                remediation_configs=[{"ConfigRuleName": "rule-1"}],
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# describe_remediation_configurations
# ---------------------------------------------------------------------------


class TestDescribeRemediationConfigurations:
    def test_empty(self, monkeypatch):
        mock = MagicMock()
        mock.describe_remediation_configurations.return_value = {
            "RemediationConfigurations": []
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_remediation_configurations(["rule-1"], region_name=REGION)
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = MagicMock()
        mock.describe_remediation_configurations.return_value = {
            "RemediationConfigurations": [
                {
                    "ConfigRuleName": "rule-1",
                    "TargetType": "SSM_DOCUMENT",
                    "TargetId": "doc-1",
                    "Parameters": {"key": {"StaticValue": {"Values": ["v"]}}},
                    "Automatic": True,
                    "RetryAttemptSeconds": 60,
                    "MaximumAutomaticAttempts": 5,
                    "Arn": "arn:remediation",
                }
            ]
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_remediation_configurations(["rule-1"], region_name=REGION)
        assert len(result) == 1
        assert result[0].config_rule_name == "rule-1"
        assert result[0].target_type == "SSM_DOCUMENT"
        assert result[0].target_id == "doc-1"
        assert result[0].automatic is True
        assert result[0].retry_attempt_seconds == 60
        assert result[0].maximum_automatic_attempts == 5
        assert "Arn" in result[0].extra

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_remediation_configurations.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="describe_remediation_configurations failed"):
            describe_remediation_configurations(["rule-1"], region_name=REGION)


# ---------------------------------------------------------------------------
# start_remediation_execution
# ---------------------------------------------------------------------------


class TestStartRemediationExecution:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.start_remediation_execution.return_value = {
            "FailureMessage": "",
            "FailedItems": [],
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = start_remediation_execution(
            "rule-1",
            resource_keys=[
                {"resourceType": "AWS::S3::Bucket", "resourceId": "my-bucket"}
            ],
            region_name=REGION,
        )
        assert result["FailureMessage"] == ""
        assert result["FailedItems"] == []

    def test_with_failures(self, monkeypatch):
        mock = MagicMock()
        mock.start_remediation_execution.return_value = {
            "FailureMessage": "partial failure",
            "FailedItems": [{"resourceType": "AWS::S3::Bucket", "resourceId": "bad-bucket"}],
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = start_remediation_execution(
            "rule-1",
            resource_keys=[
                {"resourceType": "AWS::S3::Bucket", "resourceId": "bad-bucket"}
            ],
            region_name=REGION,
        )
        assert result["FailureMessage"] == "partial failure"
        assert len(result["FailedItems"]) == 1

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.start_remediation_execution.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to start remediation execution"):
            start_remediation_execution(
                "rule-1",
                resource_keys=[{"resourceType": "X", "resourceId": "1"}],
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# list_discovered_resources
# ---------------------------------------------------------------------------


class TestListDiscoveredResources:
    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator([{"resourceIdentifiers": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = list_discovered_resources("AWS::S3::Bucket", region_name=REGION)
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "resourceIdentifiers": [
                        {
                            "resourceType": "AWS::S3::Bucket",
                            "resourceId": "bucket-1",
                            "resourceName": "my-bucket",
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = list_discovered_resources("AWS::S3::Bucket", region_name=REGION)
        assert len(result) == 1
        assert result[0]["resourceId"] == "bucket-1"

    def test_with_filters(self, monkeypatch):
        mock = _mock_client_with_paginator([{"resourceIdentifiers": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        list_discovered_resources(
            "AWS::EC2::Instance",
            resource_ids=["i-123"],
            resource_name="my-instance",
            limit=5,
            region_name=REGION,
        )
        call_kwargs = mock.get_paginator.return_value.paginate.call_args[1]
        assert call_kwargs["resourceIds"] == ["i-123"]
        assert call_kwargs["resourceName"] == "my-instance"
        assert call_kwargs["limit"] == 5

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="list_discovered_resources failed"):
            list_discovered_resources("AWS::S3::Bucket", region_name=REGION)


# ---------------------------------------------------------------------------
# get_resource_config_history
# ---------------------------------------------------------------------------


class TestGetResourceConfigHistory:
    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator([{"configurationItems": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = get_resource_config_history(
            "AWS::S3::Bucket", "bucket-1", region_name=REGION
        )
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "configurationItems": [
                        {
                            "resourceType": "AWS::S3::Bucket",
                            "resourceId": "bucket-1",
                            "configuration": "{}",
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = get_resource_config_history(
            "AWS::S3::Bucket", "bucket-1", region_name=REGION
        )
        assert len(result) == 1

    def test_with_limit(self, monkeypatch):
        mock = _mock_client_with_paginator([{"configurationItems": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        get_resource_config_history(
            "AWS::S3::Bucket", "bucket-1", limit=10, region_name=REGION
        )
        call_kwargs = mock.get_paginator.return_value.paginate.call_args[1]
        assert call_kwargs["limit"] == 10

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="get_resource_config_history failed"):
            get_resource_config_history("AWS::S3::Bucket", "bucket-1", region_name=REGION)


# ---------------------------------------------------------------------------
# describe_configuration_aggregators
# ---------------------------------------------------------------------------


class TestDescribeConfigurationAggregators:
    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator([{"ConfigurationAggregators": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_aggregators(region_name=REGION)
        assert result == []

    def test_returns_results(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "ConfigurationAggregators": [
                        {
                            "ConfigurationAggregatorName": "agg-1",
                            "AccountAggregationSources": [
                                {"AccountIds": ["123456789012"]}
                            ],
                        }
                    ]
                }
            ]
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = describe_configuration_aggregators(region_name=REGION)
        assert len(result) == 1
        assert result[0]["ConfigurationAggregatorName"] == "agg-1"

    def test_with_names(self, monkeypatch):
        mock = _mock_client_with_paginator([{"ConfigurationAggregators": []}])
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        describe_configuration_aggregators(names=["agg-1"], region_name=REGION)
        call_kwargs = mock.get_paginator.return_value.paginate.call_args[1]
        assert call_kwargs["ConfigurationAggregatorNames"] == ["agg-1"]

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="describe_configuration_aggregators failed"):
            describe_configuration_aggregators(region_name=REGION)


# ---------------------------------------------------------------------------
# put_aggregation_authorization
# ---------------------------------------------------------------------------


class TestPutAggregationAuthorization:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.put_aggregation_authorization.return_value = {
            "AggregationAuthorization": {
                "AuthorizedAccountId": "123456789012",
                "AuthorizedAwsRegion": "us-east-1",
            }
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = put_aggregation_authorization(
            "123456789012", "us-east-1", region_name=REGION
        )
        assert result["AuthorizedAccountId"] == "123456789012"
        assert result["AuthorizedAwsRegion"] == "us-east-1"

    def test_missing_auth(self, monkeypatch):
        mock = MagicMock()
        mock.put_aggregation_authorization.return_value = {}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        result = put_aggregation_authorization(
            "123456789012", "us-east-1", region_name=REGION
        )
        assert result == {}

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.put_aggregation_authorization.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        with pytest.raises(RuntimeError, match="Failed to put aggregation authorization"):
            put_aggregation_authorization("123456789012", "us-east-1", region_name=REGION)


# ---------------------------------------------------------------------------
# __all__ completeness
# ---------------------------------------------------------------------------


class TestAll:
    def test_all_exports(self):
        for name in mod.__all__:
            assert hasattr(mod, name), f"Missing export: {name}"


def test_associate_resource_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_resource_types.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    associate_resource_types("test-configuration_recorder_arn", [], region_name=REGION)
    mock_client.associate_resource_types.assert_called_once()


def test_associate_resource_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_resource_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_resource_types",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate resource types"):
        associate_resource_types("test-configuration_recorder_arn", [], region_name=REGION)


def test_batch_get_aggregate_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_aggregate_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    batch_get_aggregate_resource_config("test-configuration_aggregator_name", [], region_name=REGION)
    mock_client.batch_get_aggregate_resource_config.assert_called_once()


def test_batch_get_aggregate_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_aggregate_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_aggregate_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get aggregate resource config"):
        batch_get_aggregate_resource_config("test-configuration_aggregator_name", [], region_name=REGION)


def test_batch_get_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    batch_get_resource_config([], region_name=REGION)
    mock_client.batch_get_resource_config.assert_called_once()


def test_batch_get_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get resource config"):
        batch_get_resource_config([], region_name=REGION)


def test_delete_aggregation_authorization(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_aggregation_authorization.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_aggregation_authorization("test-authorized_account_id", "test-authorized_aws_region", region_name=REGION)
    mock_client.delete_aggregation_authorization.assert_called_once()


def test_delete_aggregation_authorization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_aggregation_authorization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_aggregation_authorization",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete aggregation authorization"):
        delete_aggregation_authorization("test-authorized_account_id", "test-authorized_aws_region", region_name=REGION)


def test_delete_configuration_aggregator(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_configuration_aggregator("test-configuration_aggregator_name", region_name=REGION)
    mock_client.delete_configuration_aggregator.assert_called_once()


def test_delete_configuration_aggregator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_aggregator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_aggregator",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration aggregator"):
        delete_configuration_aggregator("test-configuration_aggregator_name", region_name=REGION)


def test_delete_configuration_recorder(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_recorder.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_configuration_recorder("test-configuration_recorder_name", region_name=REGION)
    mock_client.delete_configuration_recorder.assert_called_once()


def test_delete_configuration_recorder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_recorder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_recorder",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration recorder"):
        delete_configuration_recorder("test-configuration_recorder_name", region_name=REGION)


def test_delete_conformance_pack(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_conformance_pack.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_conformance_pack("test-conformance_pack_name", region_name=REGION)
    mock_client.delete_conformance_pack.assert_called_once()


def test_delete_conformance_pack_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_conformance_pack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_conformance_pack",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete conformance pack"):
        delete_conformance_pack("test-conformance_pack_name", region_name=REGION)


def test_delete_delivery_channel(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_delivery_channel.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_delivery_channel("test-delivery_channel_name", region_name=REGION)
    mock_client.delete_delivery_channel.assert_called_once()


def test_delete_delivery_channel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_delivery_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_delivery_channel",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete delivery channel"):
        delete_delivery_channel("test-delivery_channel_name", region_name=REGION)


def test_delete_evaluation_results(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_evaluation_results.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_evaluation_results("test-config_rule_name", region_name=REGION)
    mock_client.delete_evaluation_results.assert_called_once()


def test_delete_evaluation_results_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_evaluation_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_evaluation_results",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete evaluation results"):
        delete_evaluation_results("test-config_rule_name", region_name=REGION)


def test_delete_organization_config_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organization_config_rule.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_organization_config_rule("test-organization_config_rule_name", region_name=REGION)
    mock_client.delete_organization_config_rule.assert_called_once()


def test_delete_organization_config_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organization_config_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_organization_config_rule",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete organization config rule"):
        delete_organization_config_rule("test-organization_config_rule_name", region_name=REGION)


def test_delete_organization_conformance_pack(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organization_conformance_pack.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_organization_conformance_pack("test-organization_conformance_pack_name", region_name=REGION)
    mock_client.delete_organization_conformance_pack.assert_called_once()


def test_delete_organization_conformance_pack_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organization_conformance_pack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_organization_conformance_pack",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete organization conformance pack"):
        delete_organization_conformance_pack("test-organization_conformance_pack_name", region_name=REGION)


def test_delete_pending_aggregation_request(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_pending_aggregation_request.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_pending_aggregation_request("test-requester_account_id", "test-requester_aws_region", region_name=REGION)
    mock_client.delete_pending_aggregation_request.assert_called_once()


def test_delete_pending_aggregation_request_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_pending_aggregation_request.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_pending_aggregation_request",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete pending aggregation request"):
        delete_pending_aggregation_request("test-requester_account_id", "test-requester_aws_region", region_name=REGION)


def test_delete_remediation_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_remediation_configuration.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_remediation_configuration("test-config_rule_name", region_name=REGION)
    mock_client.delete_remediation_configuration.assert_called_once()


def test_delete_remediation_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_remediation_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_remediation_configuration",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete remediation configuration"):
        delete_remediation_configuration("test-config_rule_name", region_name=REGION)


def test_delete_remediation_exceptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_remediation_exceptions.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_remediation_exceptions("test-config_rule_name", [], region_name=REGION)
    mock_client.delete_remediation_exceptions.assert_called_once()


def test_delete_remediation_exceptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_remediation_exceptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_remediation_exceptions",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete remediation exceptions"):
        delete_remediation_exceptions("test-config_rule_name", [], region_name=REGION)


def test_delete_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_resource_config("test-resource_type", "test-resource_id", region_name=REGION)
    mock_client.delete_resource_config.assert_called_once()


def test_delete_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource config"):
        delete_resource_config("test-resource_type", "test-resource_id", region_name=REGION)


def test_delete_retention_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_retention_configuration.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_retention_configuration("test-retention_configuration_name", region_name=REGION)
    mock_client.delete_retention_configuration.assert_called_once()


def test_delete_retention_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_retention_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_retention_configuration",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete retention configuration"):
        delete_retention_configuration("test-retention_configuration_name", region_name=REGION)


def test_delete_service_linked_configuration_recorder(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_linked_configuration_recorder.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_service_linked_configuration_recorder("test-service_principal", region_name=REGION)
    mock_client.delete_service_linked_configuration_recorder.assert_called_once()


def test_delete_service_linked_configuration_recorder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_linked_configuration_recorder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_linked_configuration_recorder",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service linked configuration recorder"):
        delete_service_linked_configuration_recorder("test-service_principal", region_name=REGION)


def test_delete_stored_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stored_query.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_stored_query("test-query_name", region_name=REGION)
    mock_client.delete_stored_query.assert_called_once()


def test_delete_stored_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_stored_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stored_query",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete stored query"):
        delete_stored_query("test-query_name", region_name=REGION)


def test_describe_aggregate_compliance_by_config_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregate_compliance_by_config_rules.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_aggregate_compliance_by_config_rules("test-configuration_aggregator_name", region_name=REGION)
    mock_client.describe_aggregate_compliance_by_config_rules.assert_called_once()


def test_describe_aggregate_compliance_by_config_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregate_compliance_by_config_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_aggregate_compliance_by_config_rules",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe aggregate compliance by config rules"):
        describe_aggregate_compliance_by_config_rules("test-configuration_aggregator_name", region_name=REGION)


def test_describe_aggregate_compliance_by_conformance_packs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregate_compliance_by_conformance_packs.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_aggregate_compliance_by_conformance_packs("test-configuration_aggregator_name", region_name=REGION)
    mock_client.describe_aggregate_compliance_by_conformance_packs.assert_called_once()


def test_describe_aggregate_compliance_by_conformance_packs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregate_compliance_by_conformance_packs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_aggregate_compliance_by_conformance_packs",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe aggregate compliance by conformance packs"):
        describe_aggregate_compliance_by_conformance_packs("test-configuration_aggregator_name", region_name=REGION)


def test_describe_aggregation_authorizations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregation_authorizations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_aggregation_authorizations(region_name=REGION)
    mock_client.describe_aggregation_authorizations.assert_called_once()


def test_describe_aggregation_authorizations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_aggregation_authorizations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_aggregation_authorizations",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe aggregation authorizations"):
        describe_aggregation_authorizations(region_name=REGION)


def test_describe_compliance_by_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_compliance_by_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_compliance_by_resource(region_name=REGION)
    mock_client.describe_compliance_by_resource.assert_called_once()


def test_describe_compliance_by_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_compliance_by_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_compliance_by_resource",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe compliance by resource"):
        describe_compliance_by_resource(region_name=REGION)


def test_describe_config_rule_evaluation_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_config_rule_evaluation_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_config_rule_evaluation_status(region_name=REGION)
    mock_client.describe_config_rule_evaluation_status.assert_called_once()


def test_describe_config_rule_evaluation_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_config_rule_evaluation_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_config_rule_evaluation_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe config rule evaluation status"):
        describe_config_rule_evaluation_status(region_name=REGION)


def test_describe_configuration_aggregator_sources_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_aggregator_sources_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_configuration_aggregator_sources_status("test-configuration_aggregator_name", region_name=REGION)
    mock_client.describe_configuration_aggregator_sources_status.assert_called_once()


def test_describe_configuration_aggregator_sources_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_aggregator_sources_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration_aggregator_sources_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe configuration aggregator sources status"):
        describe_configuration_aggregator_sources_status("test-configuration_aggregator_name", region_name=REGION)


def test_describe_configuration_recorder_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_recorder_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_configuration_recorder_status(region_name=REGION)
    mock_client.describe_configuration_recorder_status.assert_called_once()


def test_describe_configuration_recorder_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_recorder_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration_recorder_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe configuration recorder status"):
        describe_configuration_recorder_status(region_name=REGION)


def test_describe_conformance_pack_compliance(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conformance_pack_compliance.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_conformance_pack_compliance("test-conformance_pack_name", region_name=REGION)
    mock_client.describe_conformance_pack_compliance.assert_called_once()


def test_describe_conformance_pack_compliance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conformance_pack_compliance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_conformance_pack_compliance",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe conformance pack compliance"):
        describe_conformance_pack_compliance("test-conformance_pack_name", region_name=REGION)


def test_describe_conformance_pack_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conformance_pack_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_conformance_pack_status(region_name=REGION)
    mock_client.describe_conformance_pack_status.assert_called_once()


def test_describe_conformance_pack_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conformance_pack_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_conformance_pack_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe conformance pack status"):
        describe_conformance_pack_status(region_name=REGION)


def test_describe_conformance_packs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conformance_packs.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_conformance_packs(region_name=REGION)
    mock_client.describe_conformance_packs.assert_called_once()


def test_describe_conformance_packs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_conformance_packs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_conformance_packs",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe conformance packs"):
        describe_conformance_packs(region_name=REGION)


def test_describe_delivery_channel_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_delivery_channel_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_delivery_channel_status(region_name=REGION)
    mock_client.describe_delivery_channel_status.assert_called_once()


def test_describe_delivery_channel_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_delivery_channel_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_delivery_channel_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe delivery channel status"):
        describe_delivery_channel_status(region_name=REGION)


def test_describe_delivery_channels(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_delivery_channels.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_delivery_channels(region_name=REGION)
    mock_client.describe_delivery_channels.assert_called_once()


def test_describe_delivery_channels_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_delivery_channels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_delivery_channels",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe delivery channels"):
        describe_delivery_channels(region_name=REGION)


def test_describe_organization_config_rule_statuses(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_config_rule_statuses.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_config_rule_statuses(region_name=REGION)
    mock_client.describe_organization_config_rule_statuses.assert_called_once()


def test_describe_organization_config_rule_statuses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_config_rule_statuses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_config_rule_statuses",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe organization config rule statuses"):
        describe_organization_config_rule_statuses(region_name=REGION)


def test_describe_organization_config_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_config_rules.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_config_rules(region_name=REGION)
    mock_client.describe_organization_config_rules.assert_called_once()


def test_describe_organization_config_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_config_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_config_rules",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe organization config rules"):
        describe_organization_config_rules(region_name=REGION)


def test_describe_organization_conformance_pack_statuses(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_conformance_pack_statuses.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_conformance_pack_statuses(region_name=REGION)
    mock_client.describe_organization_conformance_pack_statuses.assert_called_once()


def test_describe_organization_conformance_pack_statuses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_conformance_pack_statuses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_conformance_pack_statuses",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe organization conformance pack statuses"):
        describe_organization_conformance_pack_statuses(region_name=REGION)


def test_describe_organization_conformance_packs(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_conformance_packs.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_conformance_packs(region_name=REGION)
    mock_client.describe_organization_conformance_packs.assert_called_once()


def test_describe_organization_conformance_packs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_conformance_packs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_conformance_packs",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe organization conformance packs"):
        describe_organization_conformance_packs(region_name=REGION)


def test_describe_pending_aggregation_requests(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pending_aggregation_requests.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_pending_aggregation_requests(region_name=REGION)
    mock_client.describe_pending_aggregation_requests.assert_called_once()


def test_describe_pending_aggregation_requests_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pending_aggregation_requests.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pending_aggregation_requests",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe pending aggregation requests"):
        describe_pending_aggregation_requests(region_name=REGION)


def test_describe_remediation_exceptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_remediation_exceptions.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_remediation_exceptions("test-config_rule_name", region_name=REGION)
    mock_client.describe_remediation_exceptions.assert_called_once()


def test_describe_remediation_exceptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_remediation_exceptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_remediation_exceptions",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe remediation exceptions"):
        describe_remediation_exceptions("test-config_rule_name", region_name=REGION)


def test_describe_remediation_execution_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_remediation_execution_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_remediation_execution_status("test-config_rule_name", region_name=REGION)
    mock_client.describe_remediation_execution_status.assert_called_once()


def test_describe_remediation_execution_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_remediation_execution_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_remediation_execution_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe remediation execution status"):
        describe_remediation_execution_status("test-config_rule_name", region_name=REGION)


def test_describe_retention_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_retention_configurations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_retention_configurations(region_name=REGION)
    mock_client.describe_retention_configurations.assert_called_once()


def test_describe_retention_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_retention_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_retention_configurations",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe retention configurations"):
        describe_retention_configurations(region_name=REGION)


def test_disassociate_resource_types(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_resource_types.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    disassociate_resource_types("test-configuration_recorder_arn", [], region_name=REGION)
    mock_client.disassociate_resource_types.assert_called_once()


def test_disassociate_resource_types_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_resource_types.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_resource_types",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate resource types"):
        disassociate_resource_types("test-configuration_recorder_arn", [], region_name=REGION)


def test_get_aggregate_compliance_details_by_config_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_compliance_details_by_config_rule.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_compliance_details_by_config_rule("test-configuration_aggregator_name", "test-config_rule_name", "test-account_id", "test-aws_region", region_name=REGION)
    mock_client.get_aggregate_compliance_details_by_config_rule.assert_called_once()


def test_get_aggregate_compliance_details_by_config_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_compliance_details_by_config_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aggregate_compliance_details_by_config_rule",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aggregate compliance details by config rule"):
        get_aggregate_compliance_details_by_config_rule("test-configuration_aggregator_name", "test-config_rule_name", "test-account_id", "test-aws_region", region_name=REGION)


def test_get_aggregate_config_rule_compliance_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_config_rule_compliance_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_config_rule_compliance_summary("test-configuration_aggregator_name", region_name=REGION)
    mock_client.get_aggregate_config_rule_compliance_summary.assert_called_once()


def test_get_aggregate_config_rule_compliance_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_config_rule_compliance_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aggregate_config_rule_compliance_summary",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aggregate config rule compliance summary"):
        get_aggregate_config_rule_compliance_summary("test-configuration_aggregator_name", region_name=REGION)


def test_get_aggregate_conformance_pack_compliance_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_conformance_pack_compliance_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_conformance_pack_compliance_summary("test-configuration_aggregator_name", region_name=REGION)
    mock_client.get_aggregate_conformance_pack_compliance_summary.assert_called_once()


def test_get_aggregate_conformance_pack_compliance_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_conformance_pack_compliance_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aggregate_conformance_pack_compliance_summary",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aggregate conformance pack compliance summary"):
        get_aggregate_conformance_pack_compliance_summary("test-configuration_aggregator_name", region_name=REGION)


def test_get_aggregate_discovered_resource_counts(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_discovered_resource_counts.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_discovered_resource_counts("test-configuration_aggregator_name", region_name=REGION)
    mock_client.get_aggregate_discovered_resource_counts.assert_called_once()


def test_get_aggregate_discovered_resource_counts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_discovered_resource_counts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aggregate_discovered_resource_counts",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aggregate discovered resource counts"):
        get_aggregate_discovered_resource_counts("test-configuration_aggregator_name", region_name=REGION)


def test_get_aggregate_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_resource_config("test-configuration_aggregator_name", {}, region_name=REGION)
    mock_client.get_aggregate_resource_config.assert_called_once()


def test_get_aggregate_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregate_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aggregate_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aggregate resource config"):
        get_aggregate_resource_config("test-configuration_aggregator_name", {}, region_name=REGION)


def test_get_compliance_details_by_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compliance_details_by_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_compliance_details_by_resource(region_name=REGION)
    mock_client.get_compliance_details_by_resource.assert_called_once()


def test_get_compliance_details_by_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compliance_details_by_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_compliance_details_by_resource",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get compliance details by resource"):
        get_compliance_details_by_resource(region_name=REGION)


def test_get_compliance_summary_by_config_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compliance_summary_by_config_rule.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_compliance_summary_by_config_rule(region_name=REGION)
    mock_client.get_compliance_summary_by_config_rule.assert_called_once()


def test_get_compliance_summary_by_config_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compliance_summary_by_config_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_compliance_summary_by_config_rule",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get compliance summary by config rule"):
        get_compliance_summary_by_config_rule(region_name=REGION)


def test_get_compliance_summary_by_resource_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compliance_summary_by_resource_type.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_compliance_summary_by_resource_type(region_name=REGION)
    mock_client.get_compliance_summary_by_resource_type.assert_called_once()


def test_get_compliance_summary_by_resource_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compliance_summary_by_resource_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_compliance_summary_by_resource_type",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get compliance summary by resource type"):
        get_compliance_summary_by_resource_type(region_name=REGION)


def test_get_conformance_pack_compliance_details(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_conformance_pack_compliance_details.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_conformance_pack_compliance_details("test-conformance_pack_name", region_name=REGION)
    mock_client.get_conformance_pack_compliance_details.assert_called_once()


def test_get_conformance_pack_compliance_details_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_conformance_pack_compliance_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_conformance_pack_compliance_details",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get conformance pack compliance details"):
        get_conformance_pack_compliance_details("test-conformance_pack_name", region_name=REGION)


def test_get_conformance_pack_compliance_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_conformance_pack_compliance_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_conformance_pack_compliance_summary([], region_name=REGION)
    mock_client.get_conformance_pack_compliance_summary.assert_called_once()


def test_get_conformance_pack_compliance_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_conformance_pack_compliance_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_conformance_pack_compliance_summary",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get conformance pack compliance summary"):
        get_conformance_pack_compliance_summary([], region_name=REGION)


def test_get_custom_rule_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_rule_policy.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_custom_rule_policy(region_name=REGION)
    mock_client.get_custom_rule_policy.assert_called_once()


def test_get_custom_rule_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_custom_rule_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_custom_rule_policy",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get custom rule policy"):
        get_custom_rule_policy(region_name=REGION)


def test_get_discovered_resource_counts(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_discovered_resource_counts.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_discovered_resource_counts(region_name=REGION)
    mock_client.get_discovered_resource_counts.assert_called_once()


def test_get_discovered_resource_counts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_discovered_resource_counts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_discovered_resource_counts",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get discovered resource counts"):
        get_discovered_resource_counts(region_name=REGION)


def test_get_organization_config_rule_detailed_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organization_config_rule_detailed_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_organization_config_rule_detailed_status("test-organization_config_rule_name", region_name=REGION)
    mock_client.get_organization_config_rule_detailed_status.assert_called_once()


def test_get_organization_config_rule_detailed_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organization_config_rule_detailed_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_organization_config_rule_detailed_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get organization config rule detailed status"):
        get_organization_config_rule_detailed_status("test-organization_config_rule_name", region_name=REGION)


def test_get_organization_conformance_pack_detailed_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organization_conformance_pack_detailed_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", region_name=REGION)
    mock_client.get_organization_conformance_pack_detailed_status.assert_called_once()


def test_get_organization_conformance_pack_detailed_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organization_conformance_pack_detailed_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_organization_conformance_pack_detailed_status",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get organization conformance pack detailed status"):
        get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", region_name=REGION)


def test_get_organization_custom_rule_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organization_custom_rule_policy.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_organization_custom_rule_policy("test-organization_config_rule_name", region_name=REGION)
    mock_client.get_organization_custom_rule_policy.assert_called_once()


def test_get_organization_custom_rule_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organization_custom_rule_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_organization_custom_rule_policy",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get organization custom rule policy"):
        get_organization_custom_rule_policy("test-organization_config_rule_name", region_name=REGION)


def test_get_resource_evaluation_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_evaluation_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_resource_evaluation_summary("test-resource_evaluation_id", region_name=REGION)
    mock_client.get_resource_evaluation_summary.assert_called_once()


def test_get_resource_evaluation_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_evaluation_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_evaluation_summary",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource evaluation summary"):
        get_resource_evaluation_summary("test-resource_evaluation_id", region_name=REGION)


def test_get_stored_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stored_query.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_stored_query("test-query_name", region_name=REGION)
    mock_client.get_stored_query.assert_called_once()


def test_get_stored_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_stored_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_stored_query",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get stored query"):
        get_stored_query("test-query_name", region_name=REGION)


def test_list_aggregate_discovered_resources(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aggregate_discovered_resources.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_aggregate_discovered_resources("test-configuration_aggregator_name", "test-resource_type", region_name=REGION)
    mock_client.list_aggregate_discovered_resources.assert_called_once()


def test_list_aggregate_discovered_resources_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aggregate_discovered_resources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aggregate_discovered_resources",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list aggregate discovered resources"):
        list_aggregate_discovered_resources("test-configuration_aggregator_name", "test-resource_type", region_name=REGION)


def test_list_configuration_recorders(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_recorders.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_configuration_recorders(region_name=REGION)
    mock_client.list_configuration_recorders.assert_called_once()


def test_list_configuration_recorders_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_recorders.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_configuration_recorders",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list configuration recorders"):
        list_configuration_recorders(region_name=REGION)


def test_list_conformance_pack_compliance_scores(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_conformance_pack_compliance_scores.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_conformance_pack_compliance_scores(region_name=REGION)
    mock_client.list_conformance_pack_compliance_scores.assert_called_once()


def test_list_conformance_pack_compliance_scores_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_conformance_pack_compliance_scores.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_conformance_pack_compliance_scores",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list conformance pack compliance scores"):
        list_conformance_pack_compliance_scores(region_name=REGION)


def test_list_resource_evaluations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_resource_evaluations(region_name=REGION)
    mock_client.list_resource_evaluations.assert_called_once()


def test_list_resource_evaluations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_evaluations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_evaluations",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource evaluations"):
        list_resource_evaluations(region_name=REGION)


def test_list_stored_queries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stored_queries.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_stored_queries(region_name=REGION)
    mock_client.list_stored_queries.assert_called_once()


def test_list_stored_queries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_stored_queries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_stored_queries",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list stored queries"):
        list_stored_queries(region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_put_configuration_aggregator(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_configuration_aggregator("test-configuration_aggregator_name", region_name=REGION)
    mock_client.put_configuration_aggregator.assert_called_once()


def test_put_configuration_aggregator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_configuration_aggregator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_configuration_aggregator",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put configuration aggregator"):
        put_configuration_aggregator("test-configuration_aggregator_name", region_name=REGION)


def test_put_conformance_pack(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_conformance_pack.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_conformance_pack("test-conformance_pack_name", region_name=REGION)
    mock_client.put_conformance_pack.assert_called_once()


def test_put_conformance_pack_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_conformance_pack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_conformance_pack",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put conformance pack"):
        put_conformance_pack("test-conformance_pack_name", region_name=REGION)


def test_put_delivery_channel(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_delivery_channel.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_delivery_channel({}, region_name=REGION)
    mock_client.put_delivery_channel.assert_called_once()


def test_put_delivery_channel_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_delivery_channel.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_delivery_channel",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put delivery channel"):
        put_delivery_channel({}, region_name=REGION)


def test_put_evaluations(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_evaluations("test-result_token", region_name=REGION)
    mock_client.put_evaluations.assert_called_once()


def test_put_evaluations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_evaluations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_evaluations",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put evaluations"):
        put_evaluations("test-result_token", region_name=REGION)


def test_put_external_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_external_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_external_evaluation("test-config_rule_name", {}, region_name=REGION)
    mock_client.put_external_evaluation.assert_called_once()


def test_put_external_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_external_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_external_evaluation",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put external evaluation"):
        put_external_evaluation("test-config_rule_name", {}, region_name=REGION)


def test_put_organization_config_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_organization_config_rule.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_organization_config_rule("test-organization_config_rule_name", region_name=REGION)
    mock_client.put_organization_config_rule.assert_called_once()


def test_put_organization_config_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_organization_config_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_organization_config_rule",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put organization config rule"):
        put_organization_config_rule("test-organization_config_rule_name", region_name=REGION)


def test_put_organization_conformance_pack(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_organization_conformance_pack.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_organization_conformance_pack("test-organization_conformance_pack_name", region_name=REGION)
    mock_client.put_organization_conformance_pack.assert_called_once()


def test_put_organization_conformance_pack_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_organization_conformance_pack.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_organization_conformance_pack",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put organization conformance pack"):
        put_organization_conformance_pack("test-organization_conformance_pack_name", region_name=REGION)


def test_put_remediation_exceptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_remediation_exceptions.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_remediation_exceptions("test-config_rule_name", [], region_name=REGION)
    mock_client.put_remediation_exceptions.assert_called_once()


def test_put_remediation_exceptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_remediation_exceptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_remediation_exceptions",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put remediation exceptions"):
        put_remediation_exceptions("test-config_rule_name", [], region_name=REGION)


def test_put_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", "test-configuration", region_name=REGION)
    mock_client.put_resource_config.assert_called_once()


def test_put_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource config"):
        put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", "test-configuration", region_name=REGION)


def test_put_retention_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_retention_configuration.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_retention_configuration(1, region_name=REGION)
    mock_client.put_retention_configuration.assert_called_once()


def test_put_retention_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_retention_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_retention_configuration",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put retention configuration"):
        put_retention_configuration(1, region_name=REGION)


def test_put_service_linked_configuration_recorder(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_service_linked_configuration_recorder.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_service_linked_configuration_recorder("test-service_principal", region_name=REGION)
    mock_client.put_service_linked_configuration_recorder.assert_called_once()


def test_put_service_linked_configuration_recorder_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_service_linked_configuration_recorder.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_service_linked_configuration_recorder",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put service linked configuration recorder"):
        put_service_linked_configuration_recorder("test-service_principal", region_name=REGION)


def test_put_stored_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_stored_query.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_stored_query({}, region_name=REGION)
    mock_client.put_stored_query.assert_called_once()


def test_put_stored_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_stored_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_stored_query",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put stored query"):
        put_stored_query({}, region_name=REGION)


def test_select_aggregate_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.select_aggregate_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    select_aggregate_resource_config("test-expression", "test-configuration_aggregator_name", region_name=REGION)
    mock_client.select_aggregate_resource_config.assert_called_once()


def test_select_aggregate_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.select_aggregate_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "select_aggregate_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to select aggregate resource config"):
        select_aggregate_resource_config("test-expression", "test-configuration_aggregator_name", region_name=REGION)


def test_select_resource_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.select_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    select_resource_config("test-expression", region_name=REGION)
    mock_client.select_resource_config.assert_called_once()


def test_select_resource_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.select_resource_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "select_resource_config",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to select resource config"):
        select_resource_config("test-expression", region_name=REGION)


def test_start_resource_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_resource_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    start_resource_evaluation({}, "test-evaluation_mode", region_name=REGION)
    mock_client.start_resource_evaluation.assert_called_once()


def test_start_resource_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_resource_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_resource_evaluation",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start resource evaluation"):
        start_resource_evaluation({}, "test-evaluation_mode", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_delete_remediation_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import delete_remediation_configuration
    mock_client = MagicMock()
    mock_client.delete_remediation_configuration.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    delete_remediation_configuration({}, resource_type="test-resource_type", region_name="us-east-1")
    mock_client.delete_remediation_configuration.assert_called_once()

def test_describe_aggregate_compliance_by_config_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_aggregate_compliance_by_config_rules
    mock_client = MagicMock()
    mock_client.describe_aggregate_compliance_by_config_rules.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_aggregate_compliance_by_config_rules({}, filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_aggregate_compliance_by_config_rules.assert_called_once()

def test_describe_aggregate_compliance_by_conformance_packs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_aggregate_compliance_by_conformance_packs
    mock_client = MagicMock()
    mock_client.describe_aggregate_compliance_by_conformance_packs.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_aggregate_compliance_by_conformance_packs({}, filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_aggregate_compliance_by_conformance_packs.assert_called_once()

def test_describe_aggregation_authorizations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_aggregation_authorizations
    mock_client = MagicMock()
    mock_client.describe_aggregation_authorizations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_aggregation_authorizations(limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_aggregation_authorizations.assert_called_once()

def test_describe_compliance_by_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_compliance_by_resource
    mock_client = MagicMock()
    mock_client.describe_compliance_by_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_compliance_by_resource(resource_type="test-resource_type", resource_id="test-resource_id", compliance_types="test-compliance_types", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_compliance_by_resource.assert_called_once()

def test_describe_config_rule_evaluation_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_config_rule_evaluation_status
    mock_client = MagicMock()
    mock_client.describe_config_rule_evaluation_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_config_rule_evaluation_status(config_rule_names={}, next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.describe_config_rule_evaluation_status.assert_called_once()

def test_describe_configuration_aggregator_sources_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_configuration_aggregator_sources_status
    mock_client = MagicMock()
    mock_client.describe_configuration_aggregator_sources_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_configuration_aggregator_sources_status({}, update_status="test-update_status", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.describe_configuration_aggregator_sources_status.assert_called_once()

def test_describe_configuration_recorder_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_configuration_recorder_status
    mock_client = MagicMock()
    mock_client.describe_configuration_recorder_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_configuration_recorder_status(configuration_recorder_names={}, service_principal="test-service_principal", arn="test-arn", region_name="us-east-1")
    mock_client.describe_configuration_recorder_status.assert_called_once()

def test_describe_conformance_pack_compliance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_conformance_pack_compliance
    mock_client = MagicMock()
    mock_client.describe_conformance_pack_compliance.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_conformance_pack_compliance("test-conformance_pack_name", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_conformance_pack_compliance.assert_called_once()

def test_describe_conformance_pack_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_conformance_pack_status
    mock_client = MagicMock()
    mock_client.describe_conformance_pack_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_conformance_pack_status(conformance_pack_names="test-conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_conformance_pack_status.assert_called_once()

def test_describe_conformance_packs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_conformance_packs
    mock_client = MagicMock()
    mock_client.describe_conformance_packs.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_conformance_packs(conformance_pack_names="test-conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_conformance_packs.assert_called_once()

def test_describe_delivery_channel_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_delivery_channel_status
    mock_client = MagicMock()
    mock_client.describe_delivery_channel_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_delivery_channel_status(delivery_channel_names="test-delivery_channel_names", region_name="us-east-1")
    mock_client.describe_delivery_channel_status.assert_called_once()

def test_describe_delivery_channels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_delivery_channels
    mock_client = MagicMock()
    mock_client.describe_delivery_channels.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_delivery_channels(delivery_channel_names="test-delivery_channel_names", region_name="us-east-1")
    mock_client.describe_delivery_channels.assert_called_once()

def test_describe_organization_config_rule_statuses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_organization_config_rule_statuses
    mock_client = MagicMock()
    mock_client.describe_organization_config_rule_statuses.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_config_rule_statuses(organization_config_rule_names={}, limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_organization_config_rule_statuses.assert_called_once()

def test_describe_organization_config_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_organization_config_rules
    mock_client = MagicMock()
    mock_client.describe_organization_config_rules.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_config_rules(organization_config_rule_names={}, limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_organization_config_rules.assert_called_once()

def test_describe_organization_conformance_pack_statuses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_organization_conformance_pack_statuses
    mock_client = MagicMock()
    mock_client.describe_organization_conformance_pack_statuses.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_conformance_pack_statuses(organization_conformance_pack_names="test-organization_conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_organization_conformance_pack_statuses.assert_called_once()

def test_describe_organization_conformance_packs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_organization_conformance_packs
    mock_client = MagicMock()
    mock_client.describe_organization_conformance_packs.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_organization_conformance_packs(organization_conformance_pack_names="test-organization_conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_organization_conformance_packs.assert_called_once()

def test_describe_pending_aggregation_requests_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_pending_aggregation_requests
    mock_client = MagicMock()
    mock_client.describe_pending_aggregation_requests.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_pending_aggregation_requests(limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_pending_aggregation_requests.assert_called_once()

def test_describe_remediation_exceptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_remediation_exceptions
    mock_client = MagicMock()
    mock_client.describe_remediation_exceptions.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_remediation_exceptions({}, resource_keys="test-resource_keys", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_remediation_exceptions.assert_called_once()

def test_describe_remediation_execution_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_remediation_execution_status
    mock_client = MagicMock()
    mock_client.describe_remediation_execution_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_remediation_execution_status({}, resource_keys="test-resource_keys", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_remediation_execution_status.assert_called_once()

def test_describe_retention_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import describe_retention_configurations
    mock_client = MagicMock()
    mock_client.describe_retention_configurations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    describe_retention_configurations(retention_configuration_names={}, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_retention_configurations.assert_called_once()

def test_get_aggregate_compliance_details_by_config_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_aggregate_compliance_details_by_config_rule
    mock_client = MagicMock()
    mock_client.get_aggregate_compliance_details_by_config_rule.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_compliance_details_by_config_rule({}, {}, 1, "test-aws_region", compliance_type="test-compliance_type", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_aggregate_compliance_details_by_config_rule.assert_called_once()

def test_get_aggregate_config_rule_compliance_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_aggregate_config_rule_compliance_summary
    mock_client = MagicMock()
    mock_client.get_aggregate_config_rule_compliance_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_config_rule_compliance_summary({}, filters=[{}], group_by_key="test-group_by_key", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_aggregate_config_rule_compliance_summary.assert_called_once()

def test_get_aggregate_conformance_pack_compliance_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_aggregate_conformance_pack_compliance_summary
    mock_client = MagicMock()
    mock_client.get_aggregate_conformance_pack_compliance_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_conformance_pack_compliance_summary({}, filters=[{}], group_by_key="test-group_by_key", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_aggregate_conformance_pack_compliance_summary.assert_called_once()

def test_get_aggregate_discovered_resource_counts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_aggregate_discovered_resource_counts
    mock_client = MagicMock()
    mock_client.get_aggregate_discovered_resource_counts.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_aggregate_discovered_resource_counts({}, filters=[{}], group_by_key="test-group_by_key", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_aggregate_discovered_resource_counts.assert_called_once()

def test_get_compliance_details_by_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_compliance_details_by_resource
    mock_client = MagicMock()
    mock_client.get_compliance_details_by_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_compliance_details_by_resource(resource_type="test-resource_type", resource_id="test-resource_id", compliance_types="test-compliance_types", next_token="test-next_token", resource_evaluation_id="test-resource_evaluation_id", region_name="us-east-1")
    mock_client.get_compliance_details_by_resource.assert_called_once()

def test_get_compliance_summary_by_resource_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_compliance_summary_by_resource_type
    mock_client = MagicMock()
    mock_client.get_compliance_summary_by_resource_type.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_compliance_summary_by_resource_type(resource_types="test-resource_types", region_name="us-east-1")
    mock_client.get_compliance_summary_by_resource_type.assert_called_once()

def test_get_conformance_pack_compliance_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_conformance_pack_compliance_details
    mock_client = MagicMock()
    mock_client.get_conformance_pack_compliance_details.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_conformance_pack_compliance_details("test-conformance_pack_name", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_conformance_pack_compliance_details.assert_called_once()

def test_get_conformance_pack_compliance_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_conformance_pack_compliance_summary
    mock_client = MagicMock()
    mock_client.get_conformance_pack_compliance_summary.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_conformance_pack_compliance_summary("test-conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_conformance_pack_compliance_summary.assert_called_once()

def test_get_custom_rule_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_custom_rule_policy
    mock_client = MagicMock()
    mock_client.get_custom_rule_policy.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_custom_rule_policy(config_rule_name={}, region_name="us-east-1")
    mock_client.get_custom_rule_policy.assert_called_once()

def test_get_discovered_resource_counts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_discovered_resource_counts
    mock_client = MagicMock()
    mock_client.get_discovered_resource_counts.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_discovered_resource_counts(resource_types="test-resource_types", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_discovered_resource_counts.assert_called_once()

def test_get_organization_config_rule_detailed_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_organization_config_rule_detailed_status
    mock_client = MagicMock()
    mock_client.get_organization_config_rule_detailed_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_organization_config_rule_detailed_status({}, filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_organization_config_rule_detailed_status.assert_called_once()

def test_get_organization_conformance_pack_detailed_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import get_organization_conformance_pack_detailed_status
    mock_client = MagicMock()
    mock_client.get_organization_conformance_pack_detailed_status.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_organization_conformance_pack_detailed_status.assert_called_once()

def test_list_aggregate_discovered_resources_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import list_aggregate_discovered_resources
    mock_client = MagicMock()
    mock_client.list_aggregate_discovered_resources.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_aggregate_discovered_resources({}, "test-resource_type", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_aggregate_discovered_resources.assert_called_once()

def test_list_configuration_recorders_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import list_configuration_recorders
    mock_client = MagicMock()
    mock_client.list_configuration_recorders.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_configuration_recorders(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_configuration_recorders.assert_called_once()

def test_list_conformance_pack_compliance_scores_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import list_conformance_pack_compliance_scores
    mock_client = MagicMock()
    mock_client.list_conformance_pack_compliance_scores.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_conformance_pack_compliance_scores(filters=[{}], sort_order="test-sort_order", sort_by="test-sort_by", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_conformance_pack_compliance_scores.assert_called_once()

def test_list_resource_evaluations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import list_resource_evaluations
    mock_client = MagicMock()
    mock_client.list_resource_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_resource_evaluations(filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_evaluations.assert_called_once()

def test_list_stored_queries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import list_stored_queries
    mock_client = MagicMock()
    mock_client.list_stored_queries.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_stored_queries(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_stored_queries.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_put_configuration_aggregator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_configuration_aggregator
    mock_client = MagicMock()
    mock_client.put_configuration_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_configuration_aggregator({}, account_aggregation_sources=1, organization_aggregation_source="test-organization_aggregation_source", tags=[{"Key": "k", "Value": "v"}], aggregator_filters="test-aggregator_filters", region_name="us-east-1")
    mock_client.put_configuration_aggregator.assert_called_once()

def test_put_conformance_pack_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_conformance_pack
    mock_client = MagicMock()
    mock_client.put_conformance_pack.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_conformance_pack("test-conformance_pack_name", template_s3_uri="test-template_s3_uri", template_body="test-template_body", delivery_s3_bucket="test-delivery_s3_bucket", delivery_s3_key_prefix="test-delivery_s3_key_prefix", conformance_pack_input_parameters="test-conformance_pack_input_parameters", template_ssm_document_details="test-template_ssm_document_details", region_name="us-east-1")
    mock_client.put_conformance_pack.assert_called_once()

def test_put_evaluations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_evaluations
    mock_client = MagicMock()
    mock_client.put_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_evaluations("test-result_token", evaluations="test-evaluations", run_mode="test-run_mode", region_name="us-east-1")
    mock_client.put_evaluations.assert_called_once()

def test_put_organization_config_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_organization_config_rule
    mock_client = MagicMock()
    mock_client.put_organization_config_rule.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_organization_config_rule({}, organization_managed_rule_metadata="test-organization_managed_rule_metadata", organization_custom_rule_metadata="test-organization_custom_rule_metadata", excluded_accounts=1, organization_custom_policy_rule_metadata="test-organization_custom_policy_rule_metadata", region_name="us-east-1")
    mock_client.put_organization_config_rule.assert_called_once()

def test_put_organization_conformance_pack_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_organization_conformance_pack
    mock_client = MagicMock()
    mock_client.put_organization_conformance_pack.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_organization_conformance_pack("test-organization_conformance_pack_name", template_s3_uri="test-template_s3_uri", template_body="test-template_body", delivery_s3_bucket="test-delivery_s3_bucket", delivery_s3_key_prefix="test-delivery_s3_key_prefix", conformance_pack_input_parameters="test-conformance_pack_input_parameters", excluded_accounts=1, region_name="us-east-1")
    mock_client.put_organization_conformance_pack.assert_called_once()

def test_put_remediation_exceptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_remediation_exceptions
    mock_client = MagicMock()
    mock_client.put_remediation_exceptions.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_remediation_exceptions({}, "test-resource_keys", message="test-message", expiration_time="test-expiration_time", region_name="us-east-1")
    mock_client.put_remediation_exceptions.assert_called_once()

def test_put_resource_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_resource_config
    mock_client = MagicMock()
    mock_client.put_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", {}, resource_name="test-resource_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.put_resource_config.assert_called_once()

def test_put_service_linked_configuration_recorder_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_service_linked_configuration_recorder
    mock_client = MagicMock()
    mock_client.put_service_linked_configuration_recorder.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_service_linked_configuration_recorder("test-service_principal", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.put_service_linked_configuration_recorder.assert_called_once()

def test_put_stored_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import put_stored_query
    mock_client = MagicMock()
    mock_client.put_stored_query.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    put_stored_query("test-stored_query", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.put_stored_query.assert_called_once()

def test_select_aggregate_resource_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import select_aggregate_resource_config
    mock_client = MagicMock()
    mock_client.select_aggregate_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    select_aggregate_resource_config("test-expression", {}, limit=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.select_aggregate_resource_config.assert_called_once()

def test_select_resource_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import select_resource_config
    mock_client = MagicMock()
    mock_client.select_resource_config.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    select_resource_config("test-expression", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.select_resource_config.assert_called_once()

def test_start_resource_evaluation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.config_service import start_resource_evaluation
    mock_client = MagicMock()
    mock_client.start_resource_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.config_service.get_client", lambda *a, **kw: mock_client)
    start_resource_evaluation("test-resource_details", "test-evaluation_mode", evaluation_context={}, evaluation_timeout=1, client_token="test-client_token", region_name="us-east-1")
    mock_client.start_resource_evaluation.assert_called_once()
