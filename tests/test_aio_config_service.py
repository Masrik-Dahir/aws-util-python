

"""Tests for aws_util.aio.config_service — native async AWS Config utilities."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.config_service as mod
from aws_util.config_service import (
    ComplianceResult,
    ConfigRuleResult,
    ConfigurationRecorderResult,
    RemediationConfigResult,
)
from aws_util.aio.config_service import (

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
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_client(monkeypatch):
    """Replace ``async_client`` so every function gets a mock client."""
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.config_service.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# put_config_rule
# ---------------------------------------------------------------------------


async def test_put_config_rule_success(mock_client):
    mock_client.call.return_value = {}
    await put_config_rule(
        "rule-1",
        source={"Owner": "AWS", "SourceIdentifier": "S3_BUCKET_VERSIONING_ENABLED"},
    )
    mock_client.call.assert_called_once()
    kw = mock_client.call.call_args
    assert kw[1]["ConfigRule"]["ConfigRuleName"] == "rule-1"


async def test_put_config_rule_with_scope_and_params(mock_client):
    mock_client.call.return_value = {}
    await put_config_rule(
        "rule-1",
        source={"Owner": "AWS", "SourceIdentifier": "X"},
        scope={"ComplianceResourceTypes": ["AWS::S3::Bucket"]},
        input_parameters='{"key":"value"}',
    )
    kw = mock_client.call.call_args[1]
    assert kw["ConfigRule"]["Scope"]["ComplianceResourceTypes"] == ["AWS::S3::Bucket"]
    assert kw["ConfigRule"]["InputParameters"] == '{"key":"value"}'


async def test_put_config_rule_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to put config rule"):
        await put_config_rule("rule-1", source={"Owner": "AWS", "SourceIdentifier": "X"})


async def test_put_config_rule_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_config_rule("rule-1", source={"Owner": "AWS", "SourceIdentifier": "X"})


# ---------------------------------------------------------------------------
# describe_config_rules
# ---------------------------------------------------------------------------


async def test_describe_config_rules_empty(mock_client):
    mock_client.call.return_value = {"ConfigRules": []}
    result = await describe_config_rules()
    assert result == []


async def test_describe_config_rules_single_page(mock_client):
    mock_client.call.return_value = {
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
    result = await describe_config_rules()
    assert len(result) == 1
    assert result[0].config_rule_name == "rule-1"
    assert result[0].config_rule_arn == "arn:rule-1"
    assert result[0].state == "ACTIVE"
    assert "Description" in result[0].extra


async def test_describe_config_rules_with_filter(mock_client):
    mock_client.call.return_value = {"ConfigRules": []}
    await describe_config_rules(config_rule_names=["rule-1"])
    kw = mock_client.call.call_args[1]
    assert kw["ConfigRuleNames"] == ["rule-1"]


async def test_describe_config_rules_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "ConfigRules": [
                {"ConfigRuleName": "rule-1", "Source": {}, "ConfigRuleState": "ACTIVE"}
            ],
            "NextToken": "tok1",
        },
        {
            "ConfigRules": [
                {"ConfigRuleName": "rule-2", "Source": {}, "ConfigRuleState": "ACTIVE"}
            ],
        },
    ]
    result = await describe_config_rules()
    assert len(result) == 2


async def test_describe_config_rules_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="describe_config_rules failed"):
        await describe_config_rules()


# ---------------------------------------------------------------------------
# delete_config_rule
# ---------------------------------------------------------------------------


async def test_delete_config_rule_success(mock_client):
    mock_client.call.return_value = {}
    await delete_config_rule("rule-1")
    mock_client.call.assert_called_once()


async def test_delete_config_rule_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to delete config rule"):
        await delete_config_rule("rule-1")


async def test_delete_config_rule_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_config_rule("rule-1")


# ---------------------------------------------------------------------------
# start_config_rules_evaluation
# ---------------------------------------------------------------------------


async def test_start_config_rules_evaluation_success(mock_client):
    mock_client.call.return_value = {}
    await start_config_rules_evaluation(["rule-1", "rule-2"])
    kw = mock_client.call.call_args[1]
    assert kw["ConfigRuleNames"] == ["rule-1", "rule-2"]


async def test_start_config_rules_evaluation_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to start config rules evaluation"):
        await start_config_rules_evaluation(["rule-1"])


# ---------------------------------------------------------------------------
# describe_compliance_by_config_rule
# ---------------------------------------------------------------------------


async def test_describe_compliance_empty(mock_client):
    mock_client.call.return_value = {"ComplianceByConfigRules": []}
    result = await describe_compliance_by_config_rule()
    assert result == []


async def test_describe_compliance_returns_results(mock_client):
    mock_client.call.return_value = {
        "ComplianceByConfigRules": [
            {
                "ConfigRuleName": "rule-1",
                "Compliance": {"ComplianceType": "COMPLIANT"},
            }
        ]
    }
    result = await describe_compliance_by_config_rule()
    assert len(result) == 1
    assert result[0].compliance_type == "COMPLIANT"


async def test_describe_compliance_with_filters(mock_client):
    mock_client.call.return_value = {"ComplianceByConfigRules": []}
    await describe_compliance_by_config_rule(
        config_rule_names=["rule-1"],
        compliance_types=["NON_COMPLIANT"],
    )
    kw = mock_client.call.call_args[1]
    assert kw["ConfigRuleNames"] == ["rule-1"]
    assert kw["ComplianceTypes"] == ["NON_COMPLIANT"]


async def test_describe_compliance_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "ComplianceByConfigRules": [
                {"ConfigRuleName": "r1", "Compliance": {"ComplianceType": "COMPLIANT"}}
            ],
            "NextToken": "tok",
        },
        {
            "ComplianceByConfigRules": [
                {"ConfigRuleName": "r2", "Compliance": {"ComplianceType": "NON_COMPLIANT"}}
            ],
        },
    ]
    result = await describe_compliance_by_config_rule()
    assert len(result) == 2


async def test_describe_compliance_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="describe_compliance_by_config_rule failed"):
        await describe_compliance_by_config_rule()


# ---------------------------------------------------------------------------
# get_compliance_details_by_config_rule
# ---------------------------------------------------------------------------


async def test_get_compliance_details_empty(mock_client):
    mock_client.call.return_value = {"EvaluationResults": []}
    result = await get_compliance_details_by_config_rule("rule-1")
    assert result == []


async def test_get_compliance_details_returns_results(mock_client):
    mock_client.call.return_value = {
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
    result = await get_compliance_details_by_config_rule("rule-1")
    assert len(result) == 1
    assert result[0].resource_type == "AWS::S3::Bucket"
    assert result[0].annotation == "Not versioned"
    assert "ResultToken" in result[0].extra


async def test_get_compliance_details_with_filters(mock_client):
    mock_client.call.return_value = {"EvaluationResults": []}
    await get_compliance_details_by_config_rule(
        "rule-1", compliance_types=["COMPLIANT"], limit=10
    )
    kw = mock_client.call.call_args[1]
    assert kw["ComplianceTypes"] == ["COMPLIANT"]
    assert kw["Limit"] == 10


async def test_get_compliance_details_missing_timestamp(mock_client):
    mock_client.call.return_value = {
        "EvaluationResults": [
            {
                "EvaluationResultIdentifier": {
                    "EvaluationResultQualifier": {"ConfigRuleName": "rule-1"}
                },
                "ComplianceType": "COMPLIANT",
            }
        ]
    }
    result = await get_compliance_details_by_config_rule("rule-1")
    assert result[0].ordering_timestamp is None


async def test_get_compliance_details_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "EvaluationResults": [
                {
                    "EvaluationResultIdentifier": {
                        "EvaluationResultQualifier": {"ConfigRuleName": "rule-1"}
                    },
                    "ComplianceType": "COMPLIANT",
                }
            ],
            "NextToken": "tok",
        },
        {
            "EvaluationResults": [
                {
                    "EvaluationResultIdentifier": {
                        "EvaluationResultQualifier": {"ConfigRuleName": "rule-1"}
                    },
                    "ComplianceType": "NON_COMPLIANT",
                }
            ],
        },
    ]
    result = await get_compliance_details_by_config_rule("rule-1")
    assert len(result) == 2


async def test_get_compliance_details_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="get_compliance_details_by_config_rule failed"):
        await get_compliance_details_by_config_rule("rule-1")


# ---------------------------------------------------------------------------
# describe_configuration_recorders
# ---------------------------------------------------------------------------


async def test_describe_recorders_empty(mock_client):
    mock_client.call.return_value = {"ConfigurationRecorders": []}
    result = await describe_configuration_recorders()
    assert result == []


async def test_describe_recorders_with_status(mock_client):
    mock_client.call.side_effect = [
        {
            "ConfigurationRecorders": [
                {
                    "name": "default",
                    "roleARN": "arn:role",
                    "recordingGroup": {"allSupported": True},
                }
            ]
        },
        {
            "ConfigurationRecordersStatus": [{"recording": True}]
        },
    ]
    result = await describe_configuration_recorders()
    assert len(result) == 1
    assert result[0].name == "default"
    assert result[0].status == "recording"


async def test_describe_recorders_stopped(mock_client):
    mock_client.call.side_effect = [
        {"ConfigurationRecorders": [{"name": "default", "roleARN": "arn:role"}]},
        {"ConfigurationRecordersStatus": [{"recording": False}]},
    ]
    result = await describe_configuration_recorders()
    assert result[0].status == "stopped"


async def test_describe_recorders_status_error_ignored(mock_client):
    first_call = True

    async def side_effect(*args, **kwargs):
        nonlocal first_call
        if first_call:
            first_call = False
            return {"ConfigurationRecorders": [{"name": "default", "roleARN": "arn:role"}]}
        raise ValueError("status error")

    mock_client.call.side_effect = side_effect
    result = await describe_configuration_recorders()
    assert result[0].status is None


async def test_describe_recorders_with_names(mock_client):
    mock_client.call.return_value = {"ConfigurationRecorders": []}
    await describe_configuration_recorders(names=["rec-1"])
    kw = mock_client.call.call_args[1]
    assert kw["ConfigurationRecorderNames"] == ["rec-1"]


async def test_describe_recorders_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="describe_configuration_recorders failed"):
        await describe_configuration_recorders()


async def test_describe_recorders_pascal_case(mock_client):
    mock_client.call.side_effect = [
        {
            "ConfigurationRecorders": [
                {"Name": "default", "RoleARN": "arn:role", "RecordingGroup": {"allSupported": True}}
            ]
        },
        {"ConfigurationRecordersStatus": []},
    ]
    result = await describe_configuration_recorders()
    assert result[0].name == "default"
    assert result[0].role_arn == "arn:role"


# ---------------------------------------------------------------------------
# put_configuration_recorder
# ---------------------------------------------------------------------------


async def test_put_recorder_success(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_recorder("default", role_arn="arn:role")
    kw = mock_client.call.call_args[1]
    assert kw["ConfigurationRecorder"]["name"] == "default"


async def test_put_recorder_with_recording_group(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_recorder(
        "default", role_arn="arn:role", recording_group={"allSupported": True}
    )
    kw = mock_client.call.call_args[1]
    assert kw["ConfigurationRecorder"]["recordingGroup"] == {"allSupported": True}


async def test_put_recorder_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to put configuration recorder"):
        await put_configuration_recorder("default", role_arn="arn:role")


# ---------------------------------------------------------------------------
# start_configuration_recorder / stop_configuration_recorder
# ---------------------------------------------------------------------------


async def test_start_recorder_success(mock_client):
    mock_client.call.return_value = {}
    await start_configuration_recorder("default")
    mock_client.call.assert_called_once()


async def test_start_recorder_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to start configuration recorder"):
        await start_configuration_recorder("default")


async def test_stop_recorder_success(mock_client):
    mock_client.call.return_value = {}
    await stop_configuration_recorder("default")
    mock_client.call.assert_called_once()


async def test_stop_recorder_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to stop configuration recorder"):
        await stop_configuration_recorder("default")


# ---------------------------------------------------------------------------
# deliver_config_snapshot
# ---------------------------------------------------------------------------


async def test_deliver_snapshot_success(mock_client):
    mock_client.call.return_value = {"configSnapshotId": "snap-123"}
    result = await deliver_config_snapshot("channel-1")
    assert result == "snap-123"


async def test_deliver_snapshot_missing_id(mock_client):
    mock_client.call.return_value = {}
    result = await deliver_config_snapshot("channel-1")
    assert result == ""


async def test_deliver_snapshot_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to deliver config snapshot"):
        await deliver_config_snapshot("channel-1")


# ---------------------------------------------------------------------------
# put_remediation_configurations
# ---------------------------------------------------------------------------


async def test_put_remediation_success(mock_client):
    mock_client.call.return_value = {"FailedBatches": []}
    result = await put_remediation_configurations(
        remediation_configs=[
            {"ConfigRuleName": "rule-1", "TargetType": "SSM_DOCUMENT", "TargetId": "doc-1"}
        ]
    )
    assert result == []


async def test_put_remediation_with_failures(mock_client):
    mock_client.call.return_value = {
        "FailedBatches": [{"FailureMessage": "oops"}]
    }
    result = await put_remediation_configurations(
        remediation_configs=[{"ConfigRuleName": "rule-1"}]
    )
    assert len(result) == 1


async def test_put_remediation_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to put remediation configurations"):
        await put_remediation_configurations(
            remediation_configs=[{"ConfigRuleName": "rule-1"}]
        )


# ---------------------------------------------------------------------------
# describe_remediation_configurations
# ---------------------------------------------------------------------------


async def test_describe_remediation_empty(mock_client):
    mock_client.call.return_value = {"RemediationConfigurations": []}
    result = await describe_remediation_configurations(["rule-1"])
    assert result == []


async def test_describe_remediation_returns_results(mock_client):
    mock_client.call.return_value = {
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
    result = await describe_remediation_configurations(["rule-1"])
    assert len(result) == 1
    assert result[0].target_type == "SSM_DOCUMENT"
    assert result[0].automatic is True
    assert "Arn" in result[0].extra


async def test_describe_remediation_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="describe_remediation_configurations failed"):
        await describe_remediation_configurations(["rule-1"])


# ---------------------------------------------------------------------------
# start_remediation_execution
# ---------------------------------------------------------------------------


async def test_start_remediation_success(mock_client):
    mock_client.call.return_value = {
        "FailureMessage": "",
        "FailedItems": [],
    }
    result = await start_remediation_execution(
        "rule-1",
        resource_keys=[{"resourceType": "AWS::S3::Bucket", "resourceId": "my-bucket"}],
    )
    assert result["FailureMessage"] == ""
    assert result["FailedItems"] == []


async def test_start_remediation_with_failures(mock_client):
    mock_client.call.return_value = {
        "FailureMessage": "partial",
        "FailedItems": [{"resourceType": "X", "resourceId": "1"}],
    }
    result = await start_remediation_execution(
        "rule-1",
        resource_keys=[{"resourceType": "X", "resourceId": "1"}],
    )
    assert len(result["FailedItems"]) == 1


async def test_start_remediation_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to start remediation execution"):
        await start_remediation_execution(
            "rule-1", resource_keys=[{"resourceType": "X", "resourceId": "1"}]
        )


# ---------------------------------------------------------------------------
# list_discovered_resources
# ---------------------------------------------------------------------------


async def test_list_discovered_empty(mock_client):
    mock_client.call.return_value = {"resourceIdentifiers": []}
    result = await list_discovered_resources("AWS::S3::Bucket")
    assert result == []


async def test_list_discovered_returns_results(mock_client):
    mock_client.call.return_value = {
        "resourceIdentifiers": [
            {"resourceType": "AWS::S3::Bucket", "resourceId": "bucket-1"}
        ]
    }
    result = await list_discovered_resources("AWS::S3::Bucket")
    assert len(result) == 1


async def test_list_discovered_with_filters(mock_client):
    mock_client.call.return_value = {"resourceIdentifiers": []}
    await list_discovered_resources(
        "AWS::EC2::Instance",
        resource_ids=["i-123"],
        resource_name="my-instance",
        limit=5,
    )
    kw = mock_client.call.call_args[1]
    assert kw["resourceIds"] == ["i-123"]
    assert kw["resourceName"] == "my-instance"
    assert kw["limit"] == 5


async def test_list_discovered_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "resourceIdentifiers": [{"resourceId": "1"}],
            "nextToken": "tok",
        },
        {
            "resourceIdentifiers": [{"resourceId": "2"}],
        },
    ]
    result = await list_discovered_resources("AWS::S3::Bucket")
    assert len(result) == 2


async def test_list_discovered_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="list_discovered_resources failed"):
        await list_discovered_resources("AWS::S3::Bucket")


# ---------------------------------------------------------------------------
# get_resource_config_history
# ---------------------------------------------------------------------------


async def test_get_history_empty(mock_client):
    mock_client.call.return_value = {"configurationItems": []}
    result = await get_resource_config_history("AWS::S3::Bucket", "bucket-1")
    assert result == []


async def test_get_history_returns_results(mock_client):
    mock_client.call.return_value = {
        "configurationItems": [
            {"resourceType": "AWS::S3::Bucket", "resourceId": "bucket-1"}
        ]
    }
    result = await get_resource_config_history("AWS::S3::Bucket", "bucket-1")
    assert len(result) == 1


async def test_get_history_with_limit(mock_client):
    mock_client.call.return_value = {"configurationItems": []}
    await get_resource_config_history("AWS::S3::Bucket", "bucket-1", limit=10)
    kw = mock_client.call.call_args[1]
    assert kw["limit"] == 10


async def test_get_history_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "configurationItems": [{"resourceId": "1"}],
            "nextToken": "tok",
        },
        {
            "configurationItems": [{"resourceId": "2"}],
        },
    ]
    result = await get_resource_config_history("AWS::S3::Bucket", "bucket-1")
    assert len(result) == 2


async def test_get_history_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="get_resource_config_history failed"):
        await get_resource_config_history("AWS::S3::Bucket", "bucket-1")


# ---------------------------------------------------------------------------
# describe_configuration_aggregators
# ---------------------------------------------------------------------------


async def test_describe_aggregators_empty(mock_client):
    mock_client.call.return_value = {"ConfigurationAggregators": []}
    result = await describe_configuration_aggregators()
    assert result == []


async def test_describe_aggregators_returns_results(mock_client):
    mock_client.call.return_value = {
        "ConfigurationAggregators": [
            {"ConfigurationAggregatorName": "agg-1"}
        ]
    }
    result = await describe_configuration_aggregators()
    assert len(result) == 1


async def test_describe_aggregators_with_names(mock_client):
    mock_client.call.return_value = {"ConfigurationAggregators": []}
    await describe_configuration_aggregators(names=["agg-1"])
    kw = mock_client.call.call_args[1]
    assert kw["ConfigurationAggregatorNames"] == ["agg-1"]


async def test_describe_aggregators_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "ConfigurationAggregators": [{"ConfigurationAggregatorName": "a1"}],
            "NextToken": "tok",
        },
        {
            "ConfigurationAggregators": [{"ConfigurationAggregatorName": "a2"}],
        },
    ]
    result = await describe_configuration_aggregators()
    assert len(result) == 2


async def test_describe_aggregators_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="describe_configuration_aggregators failed"):
        await describe_configuration_aggregators()


# ---------------------------------------------------------------------------
# put_aggregation_authorization
# ---------------------------------------------------------------------------


async def test_put_auth_success(mock_client):
    mock_client.call.return_value = {
        "AggregationAuthorization": {
            "AuthorizedAccountId": "123456789012",
            "AuthorizedAwsRegion": "us-east-1",
        }
    }
    result = await put_aggregation_authorization("123456789012", "us-east-1")
    assert result["AuthorizedAccountId"] == "123456789012"


async def test_put_auth_missing(mock_client):
    mock_client.call.return_value = {}
    result = await put_aggregation_authorization("123456789012", "us-east-1")
    assert result == {}


async def test_put_auth_error(mock_client):
    mock_client.call.side_effect = ValueError("oops")
    with pytest.raises(RuntimeError, match="Failed to put aggregation authorization"):
        await put_aggregation_authorization("123456789012", "us-east-1")


# ---------------------------------------------------------------------------
# __all__ completeness
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
            assert hasattr(mod, name), f"Missing export: {name}"


async def test_associate_resource_types(mock_client):
    mock_client.call.return_value = {}
    await associate_resource_types("test-configuration_recorder_arn", [], )
    mock_client.call.assert_called_once()


async def test_associate_resource_types_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await associate_resource_types("test-configuration_recorder_arn", [], )


async def test_associate_resource_types_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to associate resource types"):
        await associate_resource_types("test-configuration_recorder_arn", [], )


async def test_batch_get_aggregate_resource_config(mock_client):
    mock_client.call.return_value = {}
    await batch_get_aggregate_resource_config("test-configuration_aggregator_name", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_aggregate_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_aggregate_resource_config("test-configuration_aggregator_name", [], )


async def test_batch_get_aggregate_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get aggregate resource config"):
        await batch_get_aggregate_resource_config("test-configuration_aggregator_name", [], )


async def test_batch_get_resource_config(mock_client):
    mock_client.call.return_value = {}
    await batch_get_resource_config([], )
    mock_client.call.assert_called_once()


async def test_batch_get_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_resource_config([], )


async def test_batch_get_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get resource config"):
        await batch_get_resource_config([], )


async def test_delete_aggregation_authorization(mock_client):
    mock_client.call.return_value = {}
    await delete_aggregation_authorization("test-authorized_account_id", "test-authorized_aws_region", )
    mock_client.call.assert_called_once()


async def test_delete_aggregation_authorization_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_aggregation_authorization("test-authorized_account_id", "test-authorized_aws_region", )


async def test_delete_aggregation_authorization_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete aggregation authorization"):
        await delete_aggregation_authorization("test-authorized_account_id", "test-authorized_aws_region", )


async def test_delete_configuration_aggregator(mock_client):
    mock_client.call.return_value = {}
    await delete_configuration_aggregator("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_aggregator_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_aggregator("test-configuration_aggregator_name", )


async def test_delete_configuration_aggregator_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete configuration aggregator"):
        await delete_configuration_aggregator("test-configuration_aggregator_name", )


async def test_delete_configuration_recorder(mock_client):
    mock_client.call.return_value = {}
    await delete_configuration_recorder("test-configuration_recorder_name", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_recorder_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_recorder("test-configuration_recorder_name", )


async def test_delete_configuration_recorder_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete configuration recorder"):
        await delete_configuration_recorder("test-configuration_recorder_name", )


async def test_delete_conformance_pack(mock_client):
    mock_client.call.return_value = {}
    await delete_conformance_pack("test-conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_delete_conformance_pack_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_conformance_pack("test-conformance_pack_name", )


async def test_delete_conformance_pack_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete conformance pack"):
        await delete_conformance_pack("test-conformance_pack_name", )


async def test_delete_delivery_channel(mock_client):
    mock_client.call.return_value = {}
    await delete_delivery_channel("test-delivery_channel_name", )
    mock_client.call.assert_called_once()


async def test_delete_delivery_channel_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_delivery_channel("test-delivery_channel_name", )


async def test_delete_delivery_channel_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete delivery channel"):
        await delete_delivery_channel("test-delivery_channel_name", )


async def test_delete_evaluation_results(mock_client):
    mock_client.call.return_value = {}
    await delete_evaluation_results("test-config_rule_name", )
    mock_client.call.assert_called_once()


async def test_delete_evaluation_results_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_evaluation_results("test-config_rule_name", )


async def test_delete_evaluation_results_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete evaluation results"):
        await delete_evaluation_results("test-config_rule_name", )


async def test_delete_organization_config_rule(mock_client):
    mock_client.call.return_value = {}
    await delete_organization_config_rule("test-organization_config_rule_name", )
    mock_client.call.assert_called_once()


async def test_delete_organization_config_rule_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_organization_config_rule("test-organization_config_rule_name", )


async def test_delete_organization_config_rule_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete organization config rule"):
        await delete_organization_config_rule("test-organization_config_rule_name", )


async def test_delete_organization_conformance_pack(mock_client):
    mock_client.call.return_value = {}
    await delete_organization_conformance_pack("test-organization_conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_delete_organization_conformance_pack_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_organization_conformance_pack("test-organization_conformance_pack_name", )


async def test_delete_organization_conformance_pack_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete organization conformance pack"):
        await delete_organization_conformance_pack("test-organization_conformance_pack_name", )


async def test_delete_pending_aggregation_request(mock_client):
    mock_client.call.return_value = {}
    await delete_pending_aggregation_request("test-requester_account_id", "test-requester_aws_region", )
    mock_client.call.assert_called_once()


async def test_delete_pending_aggregation_request_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_pending_aggregation_request("test-requester_account_id", "test-requester_aws_region", )


async def test_delete_pending_aggregation_request_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete pending aggregation request"):
        await delete_pending_aggregation_request("test-requester_account_id", "test-requester_aws_region", )


async def test_delete_remediation_configuration(mock_client):
    mock_client.call.return_value = {}
    await delete_remediation_configuration("test-config_rule_name", )
    mock_client.call.assert_called_once()


async def test_delete_remediation_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_remediation_configuration("test-config_rule_name", )


async def test_delete_remediation_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete remediation configuration"):
        await delete_remediation_configuration("test-config_rule_name", )


async def test_delete_remediation_exceptions(mock_client):
    mock_client.call.return_value = {}
    await delete_remediation_exceptions("test-config_rule_name", [], )
    mock_client.call.assert_called_once()


async def test_delete_remediation_exceptions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_remediation_exceptions("test-config_rule_name", [], )


async def test_delete_remediation_exceptions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete remediation exceptions"):
        await delete_remediation_exceptions("test-config_rule_name", [], )


async def test_delete_resource_config(mock_client):
    mock_client.call.return_value = {}
    await delete_resource_config("test-resource_type", "test-resource_id", )
    mock_client.call.assert_called_once()


async def test_delete_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_config("test-resource_type", "test-resource_id", )


async def test_delete_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete resource config"):
        await delete_resource_config("test-resource_type", "test-resource_id", )


async def test_delete_retention_configuration(mock_client):
    mock_client.call.return_value = {}
    await delete_retention_configuration("test-retention_configuration_name", )
    mock_client.call.assert_called_once()


async def test_delete_retention_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_retention_configuration("test-retention_configuration_name", )


async def test_delete_retention_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete retention configuration"):
        await delete_retention_configuration("test-retention_configuration_name", )


async def test_delete_service_linked_configuration_recorder(mock_client):
    mock_client.call.return_value = {}
    await delete_service_linked_configuration_recorder("test-service_principal", )
    mock_client.call.assert_called_once()


async def test_delete_service_linked_configuration_recorder_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_linked_configuration_recorder("test-service_principal", )


async def test_delete_service_linked_configuration_recorder_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete service linked configuration recorder"):
        await delete_service_linked_configuration_recorder("test-service_principal", )


async def test_delete_stored_query(mock_client):
    mock_client.call.return_value = {}
    await delete_stored_query("test-query_name", )
    mock_client.call.assert_called_once()


async def test_delete_stored_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_stored_query("test-query_name", )


async def test_delete_stored_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete stored query"):
        await delete_stored_query("test-query_name", )


async def test_describe_aggregate_compliance_by_config_rules(mock_client):
    mock_client.call.return_value = {}
    await describe_aggregate_compliance_by_config_rules("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_describe_aggregate_compliance_by_config_rules_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_aggregate_compliance_by_config_rules("test-configuration_aggregator_name", )


async def test_describe_aggregate_compliance_by_config_rules_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe aggregate compliance by config rules"):
        await describe_aggregate_compliance_by_config_rules("test-configuration_aggregator_name", )


async def test_describe_aggregate_compliance_by_conformance_packs(mock_client):
    mock_client.call.return_value = {}
    await describe_aggregate_compliance_by_conformance_packs("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_describe_aggregate_compliance_by_conformance_packs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_aggregate_compliance_by_conformance_packs("test-configuration_aggregator_name", )


async def test_describe_aggregate_compliance_by_conformance_packs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe aggregate compliance by conformance packs"):
        await describe_aggregate_compliance_by_conformance_packs("test-configuration_aggregator_name", )


async def test_describe_aggregation_authorizations(mock_client):
    mock_client.call.return_value = {}
    await describe_aggregation_authorizations()
    mock_client.call.assert_called_once()


async def test_describe_aggregation_authorizations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_aggregation_authorizations()


async def test_describe_aggregation_authorizations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe aggregation authorizations"):
        await describe_aggregation_authorizations()


async def test_describe_compliance_by_resource(mock_client):
    mock_client.call.return_value = {}
    await describe_compliance_by_resource()
    mock_client.call.assert_called_once()


async def test_describe_compliance_by_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_compliance_by_resource()


async def test_describe_compliance_by_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe compliance by resource"):
        await describe_compliance_by_resource()


async def test_describe_config_rule_evaluation_status(mock_client):
    mock_client.call.return_value = {}
    await describe_config_rule_evaluation_status()
    mock_client.call.assert_called_once()


async def test_describe_config_rule_evaluation_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_config_rule_evaluation_status()


async def test_describe_config_rule_evaluation_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe config rule evaluation status"):
        await describe_config_rule_evaluation_status()


async def test_describe_configuration_aggregator_sources_status(mock_client):
    mock_client.call.return_value = {}
    await describe_configuration_aggregator_sources_status("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_describe_configuration_aggregator_sources_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration_aggregator_sources_status("test-configuration_aggregator_name", )


async def test_describe_configuration_aggregator_sources_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe configuration aggregator sources status"):
        await describe_configuration_aggregator_sources_status("test-configuration_aggregator_name", )


async def test_describe_configuration_recorder_status(mock_client):
    mock_client.call.return_value = {}
    await describe_configuration_recorder_status()
    mock_client.call.assert_called_once()


async def test_describe_configuration_recorder_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration_recorder_status()


async def test_describe_configuration_recorder_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe configuration recorder status"):
        await describe_configuration_recorder_status()


async def test_describe_conformance_pack_compliance(mock_client):
    mock_client.call.return_value = {}
    await describe_conformance_pack_compliance("test-conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_describe_conformance_pack_compliance_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_conformance_pack_compliance("test-conformance_pack_name", )


async def test_describe_conformance_pack_compliance_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe conformance pack compliance"):
        await describe_conformance_pack_compliance("test-conformance_pack_name", )


async def test_describe_conformance_pack_status(mock_client):
    mock_client.call.return_value = {}
    await describe_conformance_pack_status()
    mock_client.call.assert_called_once()


async def test_describe_conformance_pack_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_conformance_pack_status()


async def test_describe_conformance_pack_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe conformance pack status"):
        await describe_conformance_pack_status()


async def test_describe_conformance_packs(mock_client):
    mock_client.call.return_value = {}
    await describe_conformance_packs()
    mock_client.call.assert_called_once()


async def test_describe_conformance_packs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_conformance_packs()


async def test_describe_conformance_packs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe conformance packs"):
        await describe_conformance_packs()


async def test_describe_delivery_channel_status(mock_client):
    mock_client.call.return_value = {}
    await describe_delivery_channel_status()
    mock_client.call.assert_called_once()


async def test_describe_delivery_channel_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_delivery_channel_status()


async def test_describe_delivery_channel_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe delivery channel status"):
        await describe_delivery_channel_status()


async def test_describe_delivery_channels(mock_client):
    mock_client.call.return_value = {}
    await describe_delivery_channels()
    mock_client.call.assert_called_once()


async def test_describe_delivery_channels_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_delivery_channels()


async def test_describe_delivery_channels_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe delivery channels"):
        await describe_delivery_channels()


async def test_describe_organization_config_rule_statuses(mock_client):
    mock_client.call.return_value = {}
    await describe_organization_config_rule_statuses()
    mock_client.call.assert_called_once()


async def test_describe_organization_config_rule_statuses_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_config_rule_statuses()


async def test_describe_organization_config_rule_statuses_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe organization config rule statuses"):
        await describe_organization_config_rule_statuses()


async def test_describe_organization_config_rules(mock_client):
    mock_client.call.return_value = {}
    await describe_organization_config_rules()
    mock_client.call.assert_called_once()


async def test_describe_organization_config_rules_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_config_rules()


async def test_describe_organization_config_rules_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe organization config rules"):
        await describe_organization_config_rules()


async def test_describe_organization_conformance_pack_statuses(mock_client):
    mock_client.call.return_value = {}
    await describe_organization_conformance_pack_statuses()
    mock_client.call.assert_called_once()


async def test_describe_organization_conformance_pack_statuses_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_conformance_pack_statuses()


async def test_describe_organization_conformance_pack_statuses_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe organization conformance pack statuses"):
        await describe_organization_conformance_pack_statuses()


async def test_describe_organization_conformance_packs(mock_client):
    mock_client.call.return_value = {}
    await describe_organization_conformance_packs()
    mock_client.call.assert_called_once()


async def test_describe_organization_conformance_packs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_conformance_packs()


async def test_describe_organization_conformance_packs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe organization conformance packs"):
        await describe_organization_conformance_packs()


async def test_describe_pending_aggregation_requests(mock_client):
    mock_client.call.return_value = {}
    await describe_pending_aggregation_requests()
    mock_client.call.assert_called_once()


async def test_describe_pending_aggregation_requests_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pending_aggregation_requests()


async def test_describe_pending_aggregation_requests_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe pending aggregation requests"):
        await describe_pending_aggregation_requests()


async def test_describe_remediation_exceptions(mock_client):
    mock_client.call.return_value = {}
    await describe_remediation_exceptions("test-config_rule_name", )
    mock_client.call.assert_called_once()


async def test_describe_remediation_exceptions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_remediation_exceptions("test-config_rule_name", )


async def test_describe_remediation_exceptions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe remediation exceptions"):
        await describe_remediation_exceptions("test-config_rule_name", )


async def test_describe_remediation_execution_status(mock_client):
    mock_client.call.return_value = {}
    await describe_remediation_execution_status("test-config_rule_name", )
    mock_client.call.assert_called_once()


async def test_describe_remediation_execution_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_remediation_execution_status("test-config_rule_name", )


async def test_describe_remediation_execution_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe remediation execution status"):
        await describe_remediation_execution_status("test-config_rule_name", )


async def test_describe_retention_configurations(mock_client):
    mock_client.call.return_value = {}
    await describe_retention_configurations()
    mock_client.call.assert_called_once()


async def test_describe_retention_configurations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_retention_configurations()


async def test_describe_retention_configurations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe retention configurations"):
        await describe_retention_configurations()


async def test_disassociate_resource_types(mock_client):
    mock_client.call.return_value = {}
    await disassociate_resource_types("test-configuration_recorder_arn", [], )
    mock_client.call.assert_called_once()


async def test_disassociate_resource_types_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_resource_types("test-configuration_recorder_arn", [], )


async def test_disassociate_resource_types_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disassociate resource types"):
        await disassociate_resource_types("test-configuration_recorder_arn", [], )


async def test_get_aggregate_compliance_details_by_config_rule(mock_client):
    mock_client.call.return_value = {}
    await get_aggregate_compliance_details_by_config_rule("test-configuration_aggregator_name", "test-config_rule_name", "test-account_id", "test-aws_region", )
    mock_client.call.assert_called_once()


async def test_get_aggregate_compliance_details_by_config_rule_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_aggregate_compliance_details_by_config_rule("test-configuration_aggregator_name", "test-config_rule_name", "test-account_id", "test-aws_region", )


async def test_get_aggregate_compliance_details_by_config_rule_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get aggregate compliance details by config rule"):
        await get_aggregate_compliance_details_by_config_rule("test-configuration_aggregator_name", "test-config_rule_name", "test-account_id", "test-aws_region", )


async def test_get_aggregate_config_rule_compliance_summary(mock_client):
    mock_client.call.return_value = {}
    await get_aggregate_config_rule_compliance_summary("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_get_aggregate_config_rule_compliance_summary_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_aggregate_config_rule_compliance_summary("test-configuration_aggregator_name", )


async def test_get_aggregate_config_rule_compliance_summary_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get aggregate config rule compliance summary"):
        await get_aggregate_config_rule_compliance_summary("test-configuration_aggregator_name", )


async def test_get_aggregate_conformance_pack_compliance_summary(mock_client):
    mock_client.call.return_value = {}
    await get_aggregate_conformance_pack_compliance_summary("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_get_aggregate_conformance_pack_compliance_summary_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_aggregate_conformance_pack_compliance_summary("test-configuration_aggregator_name", )


async def test_get_aggregate_conformance_pack_compliance_summary_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get aggregate conformance pack compliance summary"):
        await get_aggregate_conformance_pack_compliance_summary("test-configuration_aggregator_name", )


async def test_get_aggregate_discovered_resource_counts(mock_client):
    mock_client.call.return_value = {}
    await get_aggregate_discovered_resource_counts("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_get_aggregate_discovered_resource_counts_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_aggregate_discovered_resource_counts("test-configuration_aggregator_name", )


async def test_get_aggregate_discovered_resource_counts_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get aggregate discovered resource counts"):
        await get_aggregate_discovered_resource_counts("test-configuration_aggregator_name", )


async def test_get_aggregate_resource_config(mock_client):
    mock_client.call.return_value = {}
    await get_aggregate_resource_config("test-configuration_aggregator_name", {}, )
    mock_client.call.assert_called_once()


async def test_get_aggregate_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_aggregate_resource_config("test-configuration_aggregator_name", {}, )


async def test_get_aggregate_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get aggregate resource config"):
        await get_aggregate_resource_config("test-configuration_aggregator_name", {}, )


async def test_get_compliance_details_by_resource(mock_client):
    mock_client.call.return_value = {}
    await get_compliance_details_by_resource()
    mock_client.call.assert_called_once()


async def test_get_compliance_details_by_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_compliance_details_by_resource()


async def test_get_compliance_details_by_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get compliance details by resource"):
        await get_compliance_details_by_resource()


async def test_get_compliance_summary_by_config_rule(mock_client):
    mock_client.call.return_value = {}
    await get_compliance_summary_by_config_rule()
    mock_client.call.assert_called_once()


async def test_get_compliance_summary_by_config_rule_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_compliance_summary_by_config_rule()


async def test_get_compliance_summary_by_config_rule_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get compliance summary by config rule"):
        await get_compliance_summary_by_config_rule()


async def test_get_compliance_summary_by_resource_type(mock_client):
    mock_client.call.return_value = {}
    await get_compliance_summary_by_resource_type()
    mock_client.call.assert_called_once()


async def test_get_compliance_summary_by_resource_type_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_compliance_summary_by_resource_type()


async def test_get_compliance_summary_by_resource_type_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get compliance summary by resource type"):
        await get_compliance_summary_by_resource_type()


async def test_get_conformance_pack_compliance_details(mock_client):
    mock_client.call.return_value = {}
    await get_conformance_pack_compliance_details("test-conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_get_conformance_pack_compliance_details_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_conformance_pack_compliance_details("test-conformance_pack_name", )


async def test_get_conformance_pack_compliance_details_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get conformance pack compliance details"):
        await get_conformance_pack_compliance_details("test-conformance_pack_name", )


async def test_get_conformance_pack_compliance_summary(mock_client):
    mock_client.call.return_value = {}
    await get_conformance_pack_compliance_summary([], )
    mock_client.call.assert_called_once()


async def test_get_conformance_pack_compliance_summary_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_conformance_pack_compliance_summary([], )


async def test_get_conformance_pack_compliance_summary_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get conformance pack compliance summary"):
        await get_conformance_pack_compliance_summary([], )


async def test_get_custom_rule_policy(mock_client):
    mock_client.call.return_value = {}
    await get_custom_rule_policy()
    mock_client.call.assert_called_once()


async def test_get_custom_rule_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_custom_rule_policy()


async def test_get_custom_rule_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get custom rule policy"):
        await get_custom_rule_policy()


async def test_get_discovered_resource_counts(mock_client):
    mock_client.call.return_value = {}
    await get_discovered_resource_counts()
    mock_client.call.assert_called_once()


async def test_get_discovered_resource_counts_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_discovered_resource_counts()


async def test_get_discovered_resource_counts_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get discovered resource counts"):
        await get_discovered_resource_counts()


async def test_get_organization_config_rule_detailed_status(mock_client):
    mock_client.call.return_value = {}
    await get_organization_config_rule_detailed_status("test-organization_config_rule_name", )
    mock_client.call.assert_called_once()


async def test_get_organization_config_rule_detailed_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_organization_config_rule_detailed_status("test-organization_config_rule_name", )


async def test_get_organization_config_rule_detailed_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get organization config rule detailed status"):
        await get_organization_config_rule_detailed_status("test-organization_config_rule_name", )


async def test_get_organization_conformance_pack_detailed_status(mock_client):
    mock_client.call.return_value = {}
    await get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_get_organization_conformance_pack_detailed_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", )


async def test_get_organization_conformance_pack_detailed_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get organization conformance pack detailed status"):
        await get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", )


async def test_get_organization_custom_rule_policy(mock_client):
    mock_client.call.return_value = {}
    await get_organization_custom_rule_policy("test-organization_config_rule_name", )
    mock_client.call.assert_called_once()


async def test_get_organization_custom_rule_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_organization_custom_rule_policy("test-organization_config_rule_name", )


async def test_get_organization_custom_rule_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get organization custom rule policy"):
        await get_organization_custom_rule_policy("test-organization_config_rule_name", )


async def test_get_resource_evaluation_summary(mock_client):
    mock_client.call.return_value = {}
    await get_resource_evaluation_summary("test-resource_evaluation_id", )
    mock_client.call.assert_called_once()


async def test_get_resource_evaluation_summary_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_evaluation_summary("test-resource_evaluation_id", )


async def test_get_resource_evaluation_summary_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get resource evaluation summary"):
        await get_resource_evaluation_summary("test-resource_evaluation_id", )


async def test_get_stored_query(mock_client):
    mock_client.call.return_value = {}
    await get_stored_query("test-query_name", )
    mock_client.call.assert_called_once()


async def test_get_stored_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_stored_query("test-query_name", )


async def test_get_stored_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get stored query"):
        await get_stored_query("test-query_name", )


async def test_list_aggregate_discovered_resources(mock_client):
    mock_client.call.return_value = {}
    await list_aggregate_discovered_resources("test-configuration_aggregator_name", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_list_aggregate_discovered_resources_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_aggregate_discovered_resources("test-configuration_aggregator_name", "test-resource_type", )


async def test_list_aggregate_discovered_resources_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list aggregate discovered resources"):
        await list_aggregate_discovered_resources("test-configuration_aggregator_name", "test-resource_type", )


async def test_list_configuration_recorders(mock_client):
    mock_client.call.return_value = {}
    await list_configuration_recorders()
    mock_client.call.assert_called_once()


async def test_list_configuration_recorders_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_configuration_recorders()


async def test_list_configuration_recorders_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list configuration recorders"):
        await list_configuration_recorders()


async def test_list_conformance_pack_compliance_scores(mock_client):
    mock_client.call.return_value = {}
    await list_conformance_pack_compliance_scores()
    mock_client.call.assert_called_once()


async def test_list_conformance_pack_compliance_scores_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_conformance_pack_compliance_scores()


async def test_list_conformance_pack_compliance_scores_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list conformance pack compliance scores"):
        await list_conformance_pack_compliance_scores()


async def test_list_resource_evaluations(mock_client):
    mock_client.call.return_value = {}
    await list_resource_evaluations()
    mock_client.call.assert_called_once()


async def test_list_resource_evaluations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_evaluations()


async def test_list_resource_evaluations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list resource evaluations"):
        await list_resource_evaluations()


async def test_list_stored_queries(mock_client):
    mock_client.call.return_value = {}
    await list_stored_queries()
    mock_client.call.assert_called_once()


async def test_list_stored_queries_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_stored_queries()


async def test_list_stored_queries_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list stored queries"):
        await list_stored_queries()


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource_arn", )


async def test_put_configuration_aggregator(mock_client):
    mock_client.call.return_value = {}
    await put_configuration_aggregator("test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_put_configuration_aggregator_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_configuration_aggregator("test-configuration_aggregator_name", )


async def test_put_configuration_aggregator_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put configuration aggregator"):
        await put_configuration_aggregator("test-configuration_aggregator_name", )


async def test_put_conformance_pack(mock_client):
    mock_client.call.return_value = {}
    await put_conformance_pack("test-conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_put_conformance_pack_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_conformance_pack("test-conformance_pack_name", )


async def test_put_conformance_pack_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put conformance pack"):
        await put_conformance_pack("test-conformance_pack_name", )


async def test_put_delivery_channel(mock_client):
    mock_client.call.return_value = {}
    await put_delivery_channel({}, )
    mock_client.call.assert_called_once()


async def test_put_delivery_channel_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_delivery_channel({}, )


async def test_put_delivery_channel_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put delivery channel"):
        await put_delivery_channel({}, )


async def test_put_evaluations(mock_client):
    mock_client.call.return_value = {}
    await put_evaluations("test-result_token", )
    mock_client.call.assert_called_once()


async def test_put_evaluations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_evaluations("test-result_token", )


async def test_put_evaluations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put evaluations"):
        await put_evaluations("test-result_token", )


async def test_put_external_evaluation(mock_client):
    mock_client.call.return_value = {}
    await put_external_evaluation("test-config_rule_name", {}, )
    mock_client.call.assert_called_once()


async def test_put_external_evaluation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_external_evaluation("test-config_rule_name", {}, )


async def test_put_external_evaluation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put external evaluation"):
        await put_external_evaluation("test-config_rule_name", {}, )


async def test_put_organization_config_rule(mock_client):
    mock_client.call.return_value = {}
    await put_organization_config_rule("test-organization_config_rule_name", )
    mock_client.call.assert_called_once()


async def test_put_organization_config_rule_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_organization_config_rule("test-organization_config_rule_name", )


async def test_put_organization_config_rule_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put organization config rule"):
        await put_organization_config_rule("test-organization_config_rule_name", )


async def test_put_organization_conformance_pack(mock_client):
    mock_client.call.return_value = {}
    await put_organization_conformance_pack("test-organization_conformance_pack_name", )
    mock_client.call.assert_called_once()


async def test_put_organization_conformance_pack_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_organization_conformance_pack("test-organization_conformance_pack_name", )


async def test_put_organization_conformance_pack_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put organization conformance pack"):
        await put_organization_conformance_pack("test-organization_conformance_pack_name", )


async def test_put_remediation_exceptions(mock_client):
    mock_client.call.return_value = {}
    await put_remediation_exceptions("test-config_rule_name", [], )
    mock_client.call.assert_called_once()


async def test_put_remediation_exceptions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_remediation_exceptions("test-config_rule_name", [], )


async def test_put_remediation_exceptions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put remediation exceptions"):
        await put_remediation_exceptions("test-config_rule_name", [], )


async def test_put_resource_config(mock_client):
    mock_client.call.return_value = {}
    await put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", "test-configuration", )
    mock_client.call.assert_called_once()


async def test_put_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", "test-configuration", )


async def test_put_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put resource config"):
        await put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", "test-configuration", )


async def test_put_retention_configuration(mock_client):
    mock_client.call.return_value = {}
    await put_retention_configuration(1, )
    mock_client.call.assert_called_once()


async def test_put_retention_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_retention_configuration(1, )


async def test_put_retention_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put retention configuration"):
        await put_retention_configuration(1, )


async def test_put_service_linked_configuration_recorder(mock_client):
    mock_client.call.return_value = {}
    await put_service_linked_configuration_recorder("test-service_principal", )
    mock_client.call.assert_called_once()


async def test_put_service_linked_configuration_recorder_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_service_linked_configuration_recorder("test-service_principal", )


async def test_put_service_linked_configuration_recorder_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put service linked configuration recorder"):
        await put_service_linked_configuration_recorder("test-service_principal", )


async def test_put_stored_query(mock_client):
    mock_client.call.return_value = {}
    await put_stored_query({}, )
    mock_client.call.assert_called_once()


async def test_put_stored_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_stored_query({}, )


async def test_put_stored_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put stored query"):
        await put_stored_query({}, )


async def test_select_aggregate_resource_config(mock_client):
    mock_client.call.return_value = {}
    await select_aggregate_resource_config("test-expression", "test-configuration_aggregator_name", )
    mock_client.call.assert_called_once()


async def test_select_aggregate_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await select_aggregate_resource_config("test-expression", "test-configuration_aggregator_name", )


async def test_select_aggregate_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to select aggregate resource config"):
        await select_aggregate_resource_config("test-expression", "test-configuration_aggregator_name", )


async def test_select_resource_config(mock_client):
    mock_client.call.return_value = {}
    await select_resource_config("test-expression", )
    mock_client.call.assert_called_once()


async def test_select_resource_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await select_resource_config("test-expression", )


async def test_select_resource_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to select resource config"):
        await select_resource_config("test-expression", )


async def test_start_resource_evaluation(mock_client):
    mock_client.call.return_value = {}
    await start_resource_evaluation({}, "test-evaluation_mode", )
    mock_client.call.assert_called_once()


async def test_start_resource_evaluation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_resource_evaluation({}, "test-evaluation_mode", )


async def test_start_resource_evaluation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start resource evaluation"):
        await start_resource_evaluation({}, "test-evaluation_mode", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_get_compliance_details_by_config_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_compliance_details_by_config_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_compliance_details_by_config_rule({}, limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_discovered_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_discovered_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_discovered_resources("test-resource_type", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_resource_config_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_resource_config_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_resource_config_history("test-resource_type", "test-resource_id", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_remediation_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import delete_remediation_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await delete_remediation_configuration({}, resource_type="test-resource_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_aggregate_compliance_by_config_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_aggregate_compliance_by_config_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_aggregate_compliance_by_config_rules({}, filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_aggregate_compliance_by_conformance_packs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_aggregate_compliance_by_conformance_packs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_aggregate_compliance_by_conformance_packs({}, filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_aggregation_authorizations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_aggregation_authorizations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_aggregation_authorizations(limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_compliance_by_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_compliance_by_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_compliance_by_resource(resource_type="test-resource_type", resource_id="test-resource_id", compliance_types="test-compliance_types", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_config_rule_evaluation_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_config_rule_evaluation_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_config_rule_evaluation_status(config_rule_names={}, next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_configuration_aggregator_sources_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_configuration_aggregator_sources_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_configuration_aggregator_sources_status({}, update_status="test-update_status", next_token="test-next_token", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_configuration_recorder_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_configuration_recorder_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_configuration_recorder_status(configuration_recorder_names={}, service_principal="test-service_principal", arn="test-arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_conformance_pack_compliance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_conformance_pack_compliance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_conformance_pack_compliance("test-conformance_pack_name", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_conformance_pack_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_conformance_pack_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_conformance_pack_status(conformance_pack_names="test-conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_conformance_packs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_conformance_packs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_conformance_packs(conformance_pack_names="test-conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_delivery_channel_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_delivery_channel_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_delivery_channel_status(delivery_channel_names="test-delivery_channel_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_delivery_channels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_delivery_channels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_delivery_channels(delivery_channel_names="test-delivery_channel_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_organization_config_rule_statuses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_organization_config_rule_statuses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_organization_config_rule_statuses(organization_config_rule_names={}, limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_organization_config_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_organization_config_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_organization_config_rules(organization_config_rule_names={}, limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_organization_conformance_pack_statuses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_organization_conformance_pack_statuses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_organization_conformance_pack_statuses(organization_conformance_pack_names="test-organization_conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_organization_conformance_packs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_organization_conformance_packs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_organization_conformance_packs(organization_conformance_pack_names="test-organization_conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pending_aggregation_requests_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_pending_aggregation_requests
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_pending_aggregation_requests(limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_remediation_exceptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_remediation_exceptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_remediation_exceptions({}, resource_keys="test-resource_keys", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_remediation_execution_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_remediation_execution_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_remediation_execution_status({}, resource_keys="test-resource_keys", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_retention_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import describe_retention_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await describe_retention_configurations(retention_configuration_names={}, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_aggregate_compliance_details_by_config_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_aggregate_compliance_details_by_config_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_aggregate_compliance_details_by_config_rule({}, {}, 1, "test-aws_region", compliance_type="test-compliance_type", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_aggregate_config_rule_compliance_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_aggregate_config_rule_compliance_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_aggregate_config_rule_compliance_summary({}, filters=[{}], group_by_key="test-group_by_key", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_aggregate_conformance_pack_compliance_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_aggregate_conformance_pack_compliance_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_aggregate_conformance_pack_compliance_summary({}, filters=[{}], group_by_key="test-group_by_key", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_aggregate_discovered_resource_counts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_aggregate_discovered_resource_counts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_aggregate_discovered_resource_counts({}, filters=[{}], group_by_key="test-group_by_key", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_compliance_details_by_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_compliance_details_by_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_compliance_details_by_resource(resource_type="test-resource_type", resource_id="test-resource_id", compliance_types="test-compliance_types", next_token="test-next_token", resource_evaluation_id="test-resource_evaluation_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_compliance_summary_by_resource_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_compliance_summary_by_resource_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_compliance_summary_by_resource_type(resource_types="test-resource_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_conformance_pack_compliance_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_conformance_pack_compliance_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_conformance_pack_compliance_details("test-conformance_pack_name", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_conformance_pack_compliance_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_conformance_pack_compliance_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_conformance_pack_compliance_summary("test-conformance_pack_names", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_custom_rule_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_custom_rule_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_custom_rule_policy(config_rule_name={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_discovered_resource_counts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_discovered_resource_counts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_discovered_resource_counts(resource_types="test-resource_types", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_organization_config_rule_detailed_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_organization_config_rule_detailed_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_organization_config_rule_detailed_status({}, filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_organization_conformance_pack_detailed_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import get_organization_conformance_pack_detailed_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await get_organization_conformance_pack_detailed_status("test-organization_conformance_pack_name", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aggregate_discovered_resources_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_aggregate_discovered_resources
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_aggregate_discovered_resources({}, "test-resource_type", filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_configuration_recorders_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_configuration_recorders
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_configuration_recorders(filters=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_conformance_pack_compliance_scores_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_conformance_pack_compliance_scores
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_conformance_pack_compliance_scores(filters=[{}], sort_order="test-sort_order", sort_by="test-sort_by", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_evaluations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_resource_evaluations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_resource_evaluations(filters=[{}], limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_stored_queries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_stored_queries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_stored_queries(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_configuration_aggregator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_configuration_aggregator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_configuration_aggregator({}, account_aggregation_sources=1, organization_aggregation_source="test-organization_aggregation_source", tags=[{"Key": "k", "Value": "v"}], aggregator_filters="test-aggregator_filters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_conformance_pack_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_conformance_pack
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_conformance_pack("test-conformance_pack_name", template_s3_uri="test-template_s3_uri", template_body="test-template_body", delivery_s3_bucket="test-delivery_s3_bucket", delivery_s3_key_prefix="test-delivery_s3_key_prefix", conformance_pack_input_parameters="test-conformance_pack_input_parameters", template_ssm_document_details="test-template_ssm_document_details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_evaluations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_evaluations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_evaluations("test-result_token", evaluations="test-evaluations", run_mode="test-run_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_organization_config_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_organization_config_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_organization_config_rule({}, organization_managed_rule_metadata="test-organization_managed_rule_metadata", organization_custom_rule_metadata="test-organization_custom_rule_metadata", excluded_accounts=1, organization_custom_policy_rule_metadata="test-organization_custom_policy_rule_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_organization_conformance_pack_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_organization_conformance_pack
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_organization_conformance_pack("test-organization_conformance_pack_name", template_s3_uri="test-template_s3_uri", template_body="test-template_body", delivery_s3_bucket="test-delivery_s3_bucket", delivery_s3_key_prefix="test-delivery_s3_key_prefix", conformance_pack_input_parameters="test-conformance_pack_input_parameters", excluded_accounts=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_remediation_exceptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_remediation_exceptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_remediation_exceptions({}, "test-resource_keys", message="test-message", expiration_time="test-expiration_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_resource_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_resource_config("test-resource_type", "test-schema_version_id", "test-resource_id", {}, resource_name="test-resource_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_service_linked_configuration_recorder_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_service_linked_configuration_recorder
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_service_linked_configuration_recorder("test-service_principal", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_stored_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import put_stored_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await put_stored_query("test-stored_query", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_select_aggregate_resource_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import select_aggregate_resource_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await select_aggregate_resource_config("test-expression", {}, limit=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_select_resource_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import select_resource_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await select_resource_config("test-expression", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_resource_evaluation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.config_service import start_resource_evaluation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.config_service.async_client", lambda *a, **kw: mock_client)
    await start_resource_evaluation("test-resource_details", "test-evaluation_mode", evaluation_context={}, evaluation_timeout=1, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()
