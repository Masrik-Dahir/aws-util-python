"""Tests for aws_util.iot module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.iot import (
    IoTJob,
    IoTPolicy,
    IoTThing,
    IoTThingGroup,
    IoTThingType,
    IoTTopicRule,
    add_thing_to_thing_group,
    attach_policy,
    cancel_job,
    create_job,
    create_policy,
    create_thing,
    create_thing_group,
    create_thing_type,
    create_topic_rule,
    delete_policy,
    delete_thing,
    delete_topic_rule,
    describe_job,
    describe_thing,
    detach_policy,
    get_policy,
    get_topic_rule,
    list_jobs,
    list_policies,
    list_thing_groups,
    list_thing_types,
    list_things,
    list_topic_rules,
    update_thing,
    accept_certificate_transfer,
    add_thing_to_billing_group,
    associate_sbom_with_package_version,
    associate_targets_with_job,
    attach_principal_policy,
    attach_security_profile,
    attach_thing_principal,
    cancel_audit_mitigation_actions_task,
    cancel_audit_task,
    cancel_certificate_transfer,
    cancel_detect_mitigation_actions_task,
    cancel_job_execution,
    clear_default_authorizer,
    confirm_topic_rule_destination,
    create_audit_suppression,
    create_authorizer,
    create_billing_group,
    create_certificate_from_csr,
    create_certificate_provider,
    create_command,
    create_custom_metric,
    create_dimension,
    create_domain_configuration,
    create_dynamic_thing_group,
    create_fleet_metric,
    create_job_template,
    create_keys_and_certificate,
    create_mitigation_action,
    create_ota_update,
    create_package,
    create_package_version,
    create_policy_version,
    create_provisioning_claim,
    create_provisioning_template,
    create_provisioning_template_version,
    create_role_alias,
    create_scheduled_audit,
    create_security_profile,
    create_stream,
    create_topic_rule_destination,
    delete_account_audit_configuration,
    delete_audit_suppression,
    delete_authorizer,
    delete_billing_group,
    delete_ca_certificate,
    delete_certificate,
    delete_certificate_provider,
    delete_command,
    delete_command_execution,
    delete_custom_metric,
    delete_dimension,
    delete_domain_configuration,
    delete_dynamic_thing_group,
    delete_fleet_metric,
    delete_job,
    delete_job_execution,
    delete_job_template,
    delete_mitigation_action,
    delete_ota_update,
    delete_package,
    delete_package_version,
    delete_policy_version,
    delete_provisioning_template,
    delete_provisioning_template_version,
    delete_registration_code,
    delete_role_alias,
    delete_scheduled_audit,
    delete_security_profile,
    delete_stream,
    delete_thing_group,
    delete_thing_type,
    delete_topic_rule_destination,
    delete_v2_logging_level,
    deprecate_thing_type,
    describe_account_audit_configuration,
    describe_audit_finding,
    describe_audit_mitigation_actions_task,
    describe_audit_suppression,
    describe_audit_task,
    describe_authorizer,
    describe_billing_group,
    describe_ca_certificate,
    describe_certificate,
    describe_certificate_provider,
    describe_custom_metric,
    describe_default_authorizer,
    describe_detect_mitigation_actions_task,
    describe_dimension,
    describe_domain_configuration,
    describe_encryption_configuration,
    describe_endpoint,
    describe_event_configurations,
    describe_fleet_metric,
    describe_index,
    describe_job_execution,
    describe_job_template,
    describe_managed_job_template,
    describe_mitigation_action,
    describe_provisioning_template,
    describe_provisioning_template_version,
    describe_role_alias,
    describe_scheduled_audit,
    describe_security_profile,
    describe_stream,
    describe_thing_group,
    describe_thing_registration_task,
    describe_thing_type,
    detach_principal_policy,
    detach_security_profile,
    detach_thing_principal,
    disable_topic_rule,
    disassociate_sbom_from_package_version,
    enable_topic_rule,
    get_behavior_model_training_summaries,
    get_buckets_aggregation,
    get_cardinality,
    get_command,
    get_command_execution,
    get_effective_policies,
    get_indexing_configuration,
    get_job_document,
    get_logging_options,
    get_ota_update,
    get_package,
    get_package_configuration,
    get_package_version,
    get_percentiles,
    get_policy_version,
    get_registration_code,
    get_statistics,
    get_thing_connectivity_data,
    get_topic_rule_destination,
    get_v2_logging_options,
    list_active_violations,
    list_attached_policies,
    list_audit_findings,
    list_audit_mitigation_actions_executions,
    list_audit_mitigation_actions_tasks,
    list_audit_suppressions,
    list_audit_tasks,
    list_authorizers,
    list_billing_groups,
    list_ca_certificates,
    list_certificate_providers,
    list_certificates,
    list_certificates_by_ca,
    list_command_executions,
    list_commands,
    list_custom_metrics,
    list_detect_mitigation_actions_executions,
    list_detect_mitigation_actions_tasks,
    list_dimensions,
    list_domain_configurations,
    list_fleet_metrics,
    list_indices,
    list_job_executions_for_job,
    list_job_executions_for_thing,
    list_job_templates,
    list_managed_job_templates,
    list_metric_values,
    list_mitigation_actions,
    list_ota_updates,
    list_outgoing_certificates,
    list_package_versions,
    list_packages,
    list_policy_principals,
    list_policy_versions,
    list_principal_policies,
    list_principal_things,
    list_principal_things_v2,
    list_provisioning_template_versions,
    list_provisioning_templates,
    list_related_resources_for_audit_finding,
    list_role_aliases,
    list_sbom_validation_results,
    list_scheduled_audits,
    list_security_profiles,
    list_security_profiles_for_target,
    list_streams,
    list_tags_for_resource,
    list_targets_for_policy,
    list_targets_for_security_profile,
    list_thing_groups_for_thing,
    list_thing_principals,
    list_thing_principals_v2,
    list_thing_registration_task_reports,
    list_thing_registration_tasks,
    list_things_in_billing_group,
    list_things_in_thing_group,
    list_topic_rule_destinations,
    list_v2_logging_levels,
    list_violation_events,
    put_verification_state_on_violation,
    register_ca_certificate,
    register_certificate,
    register_certificate_without_ca,
    register_thing,
    reject_certificate_transfer,
    remove_thing_from_billing_group,
    remove_thing_from_thing_group,
    replace_topic_rule,
    run_authorization,
    run_invoke_authorizer,
    search_index,
    set_default_authorizer,
    set_default_policy_version,
    set_logging_options,
    set_v2_logging_level,
    set_v2_logging_options,
    start_audit_mitigation_actions_task,
    start_detect_mitigation_actions_task,
    start_on_demand_audit_task,
    start_thing_registration_task,
    stop_thing_registration_task,
    tag_resource,
    transfer_certificate,
    untag_resource,
    update_account_audit_configuration,
    update_audit_suppression,
    update_authorizer,
    update_billing_group,
    update_ca_certificate,
    update_certificate,
    update_certificate_provider,
    update_command,
    update_custom_metric,
    update_dimension,
    update_domain_configuration,
    update_dynamic_thing_group,
    update_encryption_configuration,
    update_event_configurations,
    update_fleet_metric,
    update_indexing_configuration,
    update_job,
    update_mitigation_action,
    update_package,
    update_package_configuration,
    update_package_version,
    update_provisioning_template,
    update_role_alias,
    update_scheduled_audit,
    update_security_profile,
    update_stream,
    update_thing_group,
    update_thing_groups_for_thing,
    update_thing_type,
    update_topic_rule_destination,
    validate_security_profile_behaviors,
)

REGION = "us-east-1"


def _client_error(code: str = "ServiceException", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Thing operations
# ---------------------------------------------------------------------------


@patch("aws_util.iot.get_client")
def test_create_thing_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_thing.return_value = {
        "thingName": "t1", "thingArn": "arn:...",
    }
    result = create_thing("t1", "sensor", {"key": "val"}, region_name=REGION)
    assert result.thing_name == "t1"
    assert result.thing_type_name == "sensor"


@patch("aws_util.iot.get_client")
def test_create_thing_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_thing.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_thing("t1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_thing_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_thing.return_value = {
        "thingName": "t1", "thingArn": "arn:...",
        "thingTypeName": "sensor", "attributes": {"k": "v"}, "version": 1,
    }
    result = describe_thing("t1", region_name=REGION)
    assert result.thing_name == "t1"
    assert result.version == 1


@patch("aws_util.iot.get_client")
def test_describe_thing_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_thing.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_thing("t1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_things_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"things": [{"thingName": "t1", "thingArn": "arn:..."}]},
    ]
    result = list_things(region_name=REGION)
    assert len(result) == 1
    assert result[0].thing_name == "t1"


@patch("aws_util.iot.get_client")
def test_list_things_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_things(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_thing_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_thing("t1", region_name=REGION)
    client.delete_thing.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_thing_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_thing.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_thing("t1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_thing_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    update_thing(
        "t1", thing_type_name="new_type",
        attributes={"k": "v"}, remove_thing_type=True,
        region_name=REGION,
    )
    client.update_thing.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_thing_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.update_thing.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        update_thing("t1", region_name=REGION)


# ---------------------------------------------------------------------------
# Thing type operations
# ---------------------------------------------------------------------------


@patch("aws_util.iot.get_client")
def test_create_thing_type_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_thing_type.return_value = {
        "thingTypeName": "sensor", "thingTypeArn": "arn:...",
    }
    result = create_thing_type(
        "sensor",
        searchable_attributes=["location"],
        description="Sensor type",
        region_name=REGION,
    )
    assert result.thing_type_name == "sensor"


@patch("aws_util.iot.get_client")
def test_create_thing_type_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_thing_type.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_thing_type("sensor", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_types_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"thingTypes": [{"thingTypeName": "sensor", "thingTypeArn": "arn:..."}]},
    ]
    result = list_thing_types(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.iot.get_client")
def test_list_thing_types_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_thing_types(region_name=REGION)


# ---------------------------------------------------------------------------
# Thing group operations
# ---------------------------------------------------------------------------


@patch("aws_util.iot.get_client")
def test_create_thing_group_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_thing_group.return_value = {
        "thingGroupName": "grp1", "thingGroupArn": "arn:...",
    }
    result = create_thing_group("grp1", parent_group_name="parent", region_name=REGION)
    assert result.thing_group_name == "grp1"


@patch("aws_util.iot.get_client")
def test_create_thing_group_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_thing_group.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_thing_group("grp1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_groups_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"thingGroups": [{"groupName": "grp1", "groupArn": "arn:..."}]},
    ]
    result = list_thing_groups(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.iot.get_client")
def test_list_thing_groups_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_thing_groups(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_add_thing_to_thing_group_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    add_thing_to_thing_group("t1", "grp1", region_name=REGION)
    client.add_thing_to_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_add_thing_to_thing_group_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.add_thing_to_thing_group.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        add_thing_to_thing_group("t1", "grp1", region_name=REGION)


# ---------------------------------------------------------------------------
# Policy operations
# ---------------------------------------------------------------------------


@patch("aws_util.iot.get_client")
def test_create_policy_with_dict(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_policy.return_value = {
        "policyName": "pol1", "policyArn": "arn:...",
        "policyDocument": "{}", "policyVersionId": "1",
    }
    result = create_policy("pol1", {"Version": "2012-10-17"}, region_name=REGION)
    assert result.policy_name == "pol1"


@patch("aws_util.iot.get_client")
def test_create_policy_with_string(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_policy.return_value = {
        "policyName": "pol1", "policyArn": "arn:...",
    }
    result = create_policy("pol1", '{"Version":"2012-10-17"}', region_name=REGION)
    assert result.policy_name == "pol1"


@patch("aws_util.iot.get_client")
def test_create_policy_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_policy.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_policy("pol1", "{}", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_policy_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_policy.return_value = {
        "policyName": "pol1", "policyArn": "arn:...",
        "policyDocument": "{}", "defaultVersionId": "1",
    }
    result = get_policy("pol1", region_name=REGION)
    assert result.policy_name == "pol1"


@patch("aws_util.iot.get_client")
def test_get_policy_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_policy.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        get_policy("pol1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_policies_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"policies": [{"policyName": "pol1", "policyArn": "arn:..."}]},
    ]
    result = list_policies(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.iot.get_client")
def test_list_policies_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_policies(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_policy_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_policy("pol1", region_name=REGION)
    client.delete_policy.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_policy_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_policy.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_policy("pol1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_attach_policy_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    attach_policy("pol1", "arn:target", region_name=REGION)
    client.attach_policy.assert_called_once()


@patch("aws_util.iot.get_client")
def test_attach_policy_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.attach_policy.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        attach_policy("pol1", "arn:target", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_detach_policy_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    detach_policy("pol1", "arn:target", region_name=REGION)
    client.detach_policy.assert_called_once()


@patch("aws_util.iot.get_client")
def test_detach_policy_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.detach_policy.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        detach_policy("pol1", "arn:target", region_name=REGION)


# ---------------------------------------------------------------------------
# Topic rule operations
# ---------------------------------------------------------------------------


@patch("aws_util.iot.get_client")
def test_create_topic_rule_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    create_topic_rule(
        "rule1", "SELECT * FROM 'topic'", [{"lambda": {}}],
        description="test", rule_disabled=False, region_name=REGION,
    )
    client.create_topic_rule.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_topic_rule_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_topic_rule.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_topic_rule("rule1", "SELECT *", [], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_topic_rule_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_topic_rule.return_value = {
        "ruleArn": "arn:...",
        "rule": {
            "ruleName": "rule1", "sql": "SELECT *",
            "description": "test", "ruleDisabled": False,
        },
    }
    result = get_topic_rule("rule1", region_name=REGION)
    assert result.rule_name == "rule1"
    assert result.sql == "SELECT *"


@patch("aws_util.iot.get_client")
def test_get_topic_rule_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.get_topic_rule.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        get_topic_rule("rule1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_topic_rules_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"rules": [{"ruleName": "rule1", "ruleArn": "arn:..."}]},
    ]
    result = list_topic_rules(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.iot.get_client")
def test_list_topic_rules_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_topic_rules(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_topic_rule_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_topic_rule("rule1", region_name=REGION)
    client.delete_topic_rule.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_topic_rule_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_topic_rule.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        delete_topic_rule("rule1", region_name=REGION)


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


@patch("aws_util.iot.get_client")
def test_create_job_with_document_dict(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.return_value = {"jobId": "job1", "jobArn": "arn:..."}
    result = create_job(
        "job1", ["arn:thing/t1"],
        document={"key": "val"},
        description="test job",
        target_selection="SNAPSHOT",
        region_name=REGION,
    )
    assert result.job_id == "job1"


@patch("aws_util.iot.get_client")
def test_create_job_with_document_source(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.return_value = {"jobId": "job1", "jobArn": "arn:..."}
    result = create_job(
        "job1", ["arn:thing/t1"],
        document_source="s3://bucket/doc.json",
        region_name=REGION,
    )
    assert result.job_id == "job1"


@patch("aws_util.iot.get_client")
def test_create_job_with_string_doc(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.return_value = {"jobId": "job1", "jobArn": "arn:..."}
    result = create_job(
        "job1", ["arn:thing/t1"],
        document='{"key":"val"}',
        region_name=REGION,
    )
    assert result.job_id == "job1"


@patch("aws_util.iot.get_client")
def test_create_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        create_job("job1", ["arn:thing/t1"], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_job_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_job.return_value = {
        "job": {
            "jobId": "job1", "jobArn": "arn:...",
            "status": "IN_PROGRESS", "description": "test",
            "targetSelection": "SNAPSHOT", "targets": ["arn:..."],
        },
    }
    result = describe_job("job1", region_name=REGION)
    assert result.job_id == "job1"
    assert result.status == "IN_PROGRESS"


@patch("aws_util.iot.get_client")
def test_describe_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.describe_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        describe_job("job1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_jobs_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"jobs": [{"jobId": "job1", "jobArn": "arn:..."}]},
    ]
    result = list_jobs(status="IN_PROGRESS", region_name=REGION)
    assert len(result) == 1


@patch("aws_util.iot.get_client")
def test_list_jobs_no_filter(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"jobs": [{"jobId": "job1"}]},
    ]
    result = list_jobs(region_name=REGION)
    assert len(result) == 1


@patch("aws_util.iot.get_client")
def test_list_jobs_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        list_jobs(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_cancel_job_success(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    cancel_job("job1", reason_code="CANCELLED", comment="done", region_name=REGION)
    client.cancel_job.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_job_no_reason(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    cancel_job("job1", region_name=REGION)
    client.cancel_job.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_job_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.cancel_job.side_effect = _client_error()
    with pytest.raises(RuntimeError):
        cancel_job("job1", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_accept_certificate_transfer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.accept_certificate_transfer.return_value = {}
    accept_certificate_transfer("test-certificate_id", region_name=REGION)
    mock_client.accept_certificate_transfer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_accept_certificate_transfer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.accept_certificate_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_certificate_transfer",
    )
    with pytest.raises(RuntimeError, match="Failed to accept certificate transfer"):
        accept_certificate_transfer("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_add_thing_to_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_thing_to_billing_group.return_value = {}
    add_thing_to_billing_group(region_name=REGION)
    mock_client.add_thing_to_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_add_thing_to_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_thing_to_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_thing_to_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to add thing to billing group"):
        add_thing_to_billing_group(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_associate_sbom_with_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_sbom_with_package_version.return_value = {}
    associate_sbom_with_package_version("test-package_name", "test-version_name", {}, region_name=REGION)
    mock_client.associate_sbom_with_package_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_associate_sbom_with_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_sbom_with_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_sbom_with_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to associate sbom with package version"):
        associate_sbom_with_package_version("test-package_name", "test-version_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_associate_targets_with_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_targets_with_job.return_value = {}
    associate_targets_with_job([], "test-job_id", region_name=REGION)
    mock_client.associate_targets_with_job.assert_called_once()


@patch("aws_util.iot.get_client")
def test_associate_targets_with_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.associate_targets_with_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_targets_with_job",
    )
    with pytest.raises(RuntimeError, match="Failed to associate targets with job"):
        associate_targets_with_job([], "test-job_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_attach_principal_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_principal_policy.return_value = {}
    attach_principal_policy("test-policy_name", "test-principal", region_name=REGION)
    mock_client.attach_principal_policy.assert_called_once()


@patch("aws_util.iot.get_client")
def test_attach_principal_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_principal_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_principal_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to attach principal policy"):
        attach_principal_policy("test-policy_name", "test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_attach_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_security_profile.return_value = {}
    attach_security_profile("test-security_profile_name", "test-security_profile_target_arn", region_name=REGION)
    mock_client.attach_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_attach_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to attach security profile"):
        attach_security_profile("test-security_profile_name", "test-security_profile_target_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_attach_thing_principal(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_thing_principal.return_value = {}
    attach_thing_principal("test-thing_name", "test-principal", region_name=REGION)
    mock_client.attach_thing_principal.assert_called_once()


@patch("aws_util.iot.get_client")
def test_attach_thing_principal_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.attach_thing_principal.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_thing_principal",
    )
    with pytest.raises(RuntimeError, match="Failed to attach thing principal"):
        attach_thing_principal("test-thing_name", "test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_cancel_audit_mitigation_actions_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_audit_mitigation_actions_task.return_value = {}
    cancel_audit_mitigation_actions_task("test-task_id", region_name=REGION)
    mock_client.cancel_audit_mitigation_actions_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_audit_mitigation_actions_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_audit_mitigation_actions_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_audit_mitigation_actions_task",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel audit mitigation actions task"):
        cancel_audit_mitigation_actions_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_cancel_audit_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_audit_task.return_value = {}
    cancel_audit_task("test-task_id", region_name=REGION)
    mock_client.cancel_audit_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_audit_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_audit_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_audit_task",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel audit task"):
        cancel_audit_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_cancel_certificate_transfer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_certificate_transfer.return_value = {}
    cancel_certificate_transfer("test-certificate_id", region_name=REGION)
    mock_client.cancel_certificate_transfer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_certificate_transfer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_certificate_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_certificate_transfer",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel certificate transfer"):
        cancel_certificate_transfer("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_cancel_detect_mitigation_actions_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_detect_mitigation_actions_task.return_value = {}
    cancel_detect_mitigation_actions_task("test-task_id", region_name=REGION)
    mock_client.cancel_detect_mitigation_actions_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_detect_mitigation_actions_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_detect_mitigation_actions_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_detect_mitigation_actions_task",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel detect mitigation actions task"):
        cancel_detect_mitigation_actions_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_cancel_job_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_job_execution.return_value = {}
    cancel_job_execution("test-job_id", "test-thing_name", region_name=REGION)
    mock_client.cancel_job_execution.assert_called_once()


@patch("aws_util.iot.get_client")
def test_cancel_job_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.cancel_job_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_job_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to cancel job execution"):
        cancel_job_execution("test-job_id", "test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_clear_default_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.clear_default_authorizer.return_value = {}
    clear_default_authorizer(region_name=REGION)
    mock_client.clear_default_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_clear_default_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.clear_default_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "clear_default_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to clear default authorizer"):
        clear_default_authorizer(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_confirm_topic_rule_destination(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.confirm_topic_rule_destination.return_value = {}
    confirm_topic_rule_destination("test-confirmation_token", region_name=REGION)
    mock_client.confirm_topic_rule_destination.assert_called_once()


@patch("aws_util.iot.get_client")
def test_confirm_topic_rule_destination_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.confirm_topic_rule_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "confirm_topic_rule_destination",
    )
    with pytest.raises(RuntimeError, match="Failed to confirm topic rule destination"):
        confirm_topic_rule_destination("test-confirmation_token", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_audit_suppression(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_audit_suppression.return_value = {}
    create_audit_suppression("test-check_name", {}, "test-client_request_token", region_name=REGION)
    mock_client.create_audit_suppression.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_audit_suppression_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_audit_suppression.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_audit_suppression",
    )
    with pytest.raises(RuntimeError, match="Failed to create audit suppression"):
        create_audit_suppression("test-check_name", {}, "test-client_request_token", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_authorizer.return_value = {}
    create_authorizer("test-authorizer_name", "test-authorizer_function_arn", region_name=REGION)
    mock_client.create_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to create authorizer"):
        create_authorizer("test-authorizer_name", "test-authorizer_function_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_billing_group.return_value = {}
    create_billing_group("test-billing_group_name", region_name=REGION)
    mock_client.create_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create billing group"):
        create_billing_group("test-billing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_certificate_from_csr(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_certificate_from_csr.return_value = {}
    create_certificate_from_csr("test-certificate_signing_request", region_name=REGION)
    mock_client.create_certificate_from_csr.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_certificate_from_csr_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_certificate_from_csr.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_certificate_from_csr",
    )
    with pytest.raises(RuntimeError, match="Failed to create certificate from csr"):
        create_certificate_from_csr("test-certificate_signing_request", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_certificate_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_certificate_provider.return_value = {}
    create_certificate_provider("test-certificate_provider_name", "test-lambda_function_arn", [], region_name=REGION)
    mock_client.create_certificate_provider.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_certificate_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_certificate_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_certificate_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to create certificate provider"):
        create_certificate_provider("test-certificate_provider_name", "test-lambda_function_arn", [], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_command(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_command.return_value = {}
    create_command("test-command_id", region_name=REGION)
    mock_client.create_command.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_command_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_command",
    )
    with pytest.raises(RuntimeError, match="Failed to create command"):
        create_command("test-command_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_custom_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_custom_metric.return_value = {}
    create_custom_metric("test-metric_name", "test-metric_type", "test-client_request_token", region_name=REGION)
    mock_client.create_custom_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_custom_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_custom_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to create custom metric"):
        create_custom_metric("test-metric_name", "test-metric_type", "test-client_request_token", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_dimension(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_dimension.return_value = {}
    create_dimension("test-name", "test-type_value", [], "test-client_request_token", region_name=REGION)
    mock_client.create_dimension.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_dimension_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_dimension.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dimension",
    )
    with pytest.raises(RuntimeError, match="Failed to create dimension"):
        create_dimension("test-name", "test-type_value", [], "test-client_request_token", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_domain_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_domain_configuration.return_value = {}
    create_domain_configuration("test-domain_configuration_name", region_name=REGION)
    mock_client.create_domain_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_domain_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_domain_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_domain_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to create domain configuration"):
        create_domain_configuration("test-domain_configuration_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_dynamic_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_dynamic_thing_group.return_value = {}
    create_dynamic_thing_group("test-thing_group_name", "test-query_string", region_name=REGION)
    mock_client.create_dynamic_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_dynamic_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_dynamic_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_dynamic_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create dynamic thing group"):
        create_dynamic_thing_group("test-thing_group_name", "test-query_string", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_fleet_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_fleet_metric.return_value = {}
    create_fleet_metric("test-metric_name", "test-query_string", {}, 1, "test-aggregation_field", region_name=REGION)
    mock_client.create_fleet_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_fleet_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_fleet_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_fleet_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to create fleet metric"):
        create_fleet_metric("test-metric_name", "test-query_string", {}, 1, "test-aggregation_field", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_job_template.return_value = {}
    create_job_template("test-job_template_id", "test-description", region_name=REGION)
    mock_client.create_job_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to create job template"):
        create_job_template("test-job_template_id", "test-description", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_keys_and_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_keys_and_certificate.return_value = {}
    create_keys_and_certificate(region_name=REGION)
    mock_client.create_keys_and_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_keys_and_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_keys_and_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_keys_and_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to create keys and certificate"):
        create_keys_and_certificate(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_mitigation_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_mitigation_action.return_value = {}
    create_mitigation_action("test-action_name", "test-role_arn", {}, region_name=REGION)
    mock_client.create_mitigation_action.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_mitigation_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_mitigation_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_mitigation_action",
    )
    with pytest.raises(RuntimeError, match="Failed to create mitigation action"):
        create_mitigation_action("test-action_name", "test-role_arn", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_ota_update(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_ota_update.return_value = {}
    create_ota_update("test-ota_update_id", [], [], "test-role_arn", region_name=REGION)
    mock_client.create_ota_update.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_ota_update_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_ota_update.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ota_update",
    )
    with pytest.raises(RuntimeError, match="Failed to create ota update"):
        create_ota_update("test-ota_update_id", [], [], "test-role_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_package(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_package.return_value = {}
    create_package("test-package_name", region_name=REGION)
    mock_client.create_package.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_package_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_package.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_package",
    )
    with pytest.raises(RuntimeError, match="Failed to create package"):
        create_package("test-package_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_package_version.return_value = {}
    create_package_version("test-package_name", "test-version_name", region_name=REGION)
    mock_client.create_package_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to create package version"):
        create_package_version("test-package_name", "test-version_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_policy_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_policy_version.return_value = {}
    create_policy_version("test-policy_name", "test-policy_document", region_name=REGION)
    mock_client.create_policy_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_policy_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_policy_version",
    )
    with pytest.raises(RuntimeError, match="Failed to create policy version"):
        create_policy_version("test-policy_name", "test-policy_document", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_provisioning_claim(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_provisioning_claim.return_value = {}
    create_provisioning_claim("test-template_name", region_name=REGION)
    mock_client.create_provisioning_claim.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_provisioning_claim_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_provisioning_claim.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_provisioning_claim",
    )
    with pytest.raises(RuntimeError, match="Failed to create provisioning claim"):
        create_provisioning_claim("test-template_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_provisioning_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_provisioning_template.return_value = {}
    create_provisioning_template("test-template_name", "test-template_body", "test-provisioning_role_arn", region_name=REGION)
    mock_client.create_provisioning_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_provisioning_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_provisioning_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_provisioning_template",
    )
    with pytest.raises(RuntimeError, match="Failed to create provisioning template"):
        create_provisioning_template("test-template_name", "test-template_body", "test-provisioning_role_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_provisioning_template_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_provisioning_template_version.return_value = {}
    create_provisioning_template_version("test-template_name", "test-template_body", region_name=REGION)
    mock_client.create_provisioning_template_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_provisioning_template_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_provisioning_template_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_provisioning_template_version",
    )
    with pytest.raises(RuntimeError, match="Failed to create provisioning template version"):
        create_provisioning_template_version("test-template_name", "test-template_body", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_role_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_role_alias.return_value = {}
    create_role_alias("test-role_alias", "test-role_arn", region_name=REGION)
    mock_client.create_role_alias.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_role_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_role_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_role_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to create role alias"):
        create_role_alias("test-role_alias", "test-role_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_scheduled_audit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_scheduled_audit.return_value = {}
    create_scheduled_audit("test-frequency", [], "test-scheduled_audit_name", region_name=REGION)
    mock_client.create_scheduled_audit.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_scheduled_audit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_scheduled_audit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_scheduled_audit",
    )
    with pytest.raises(RuntimeError, match="Failed to create scheduled audit"):
        create_scheduled_audit("test-frequency", [], "test-scheduled_audit_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_security_profile.return_value = {}
    create_security_profile("test-security_profile_name", region_name=REGION)
    mock_client.create_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to create security profile"):
        create_security_profile("test-security_profile_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_stream(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_stream.return_value = {}
    create_stream("test-stream_id", [], "test-role_arn", region_name=REGION)
    mock_client.create_stream.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_stream_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_stream",
    )
    with pytest.raises(RuntimeError, match="Failed to create stream"):
        create_stream("test-stream_id", [], "test-role_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_create_topic_rule_destination(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_topic_rule_destination.return_value = {}
    create_topic_rule_destination({}, region_name=REGION)
    mock_client.create_topic_rule_destination.assert_called_once()


@patch("aws_util.iot.get_client")
def test_create_topic_rule_destination_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_topic_rule_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_topic_rule_destination",
    )
    with pytest.raises(RuntimeError, match="Failed to create topic rule destination"):
        create_topic_rule_destination({}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_account_audit_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_account_audit_configuration.return_value = {}
    delete_account_audit_configuration(region_name=REGION)
    mock_client.delete_account_audit_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_account_audit_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_account_audit_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_audit_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete account audit configuration"):
        delete_account_audit_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_audit_suppression(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_audit_suppression.return_value = {}
    delete_audit_suppression("test-check_name", {}, region_name=REGION)
    mock_client.delete_audit_suppression.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_audit_suppression_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_audit_suppression.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_audit_suppression",
    )
    with pytest.raises(RuntimeError, match="Failed to delete audit suppression"):
        delete_audit_suppression("test-check_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_authorizer.return_value = {}
    delete_authorizer("test-authorizer_name", region_name=REGION)
    mock_client.delete_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to delete authorizer"):
        delete_authorizer("test-authorizer_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_billing_group.return_value = {}
    delete_billing_group("test-billing_group_name", region_name=REGION)
    mock_client.delete_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete billing group"):
        delete_billing_group("test-billing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_ca_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_ca_certificate.return_value = {}
    delete_ca_certificate("test-certificate_id", region_name=REGION)
    mock_client.delete_ca_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_ca_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_ca_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ca_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to delete ca certificate"):
        delete_ca_certificate("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate.return_value = {}
    delete_certificate("test-certificate_id", region_name=REGION)
    mock_client.delete_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to delete certificate"):
        delete_certificate("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_certificate_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate_provider.return_value = {}
    delete_certificate_provider("test-certificate_provider_name", region_name=REGION)
    mock_client.delete_certificate_provider.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_certificate_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_certificate_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_certificate_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to delete certificate provider"):
        delete_certificate_provider("test-certificate_provider_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_command(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_command.return_value = {}
    delete_command("test-command_id", region_name=REGION)
    mock_client.delete_command.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_command_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_command",
    )
    with pytest.raises(RuntimeError, match="Failed to delete command"):
        delete_command("test-command_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_command_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_command_execution.return_value = {}
    delete_command_execution("test-execution_id", "test-target_arn", region_name=REGION)
    mock_client.delete_command_execution.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_command_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_command_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_command_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to delete command execution"):
        delete_command_execution("test-execution_id", "test-target_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_custom_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_metric.return_value = {}
    delete_custom_metric("test-metric_name", region_name=REGION)
    mock_client.delete_custom_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_custom_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_custom_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to delete custom metric"):
        delete_custom_metric("test-metric_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_dimension(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dimension.return_value = {}
    delete_dimension("test-name", region_name=REGION)
    mock_client.delete_dimension.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_dimension_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dimension.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dimension",
    )
    with pytest.raises(RuntimeError, match="Failed to delete dimension"):
        delete_dimension("test-name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_domain_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain_configuration.return_value = {}
    delete_domain_configuration("test-domain_configuration_name", region_name=REGION)
    mock_client.delete_domain_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_domain_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_domain_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_domain_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete domain configuration"):
        delete_domain_configuration("test-domain_configuration_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_dynamic_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dynamic_thing_group.return_value = {}
    delete_dynamic_thing_group("test-thing_group_name", region_name=REGION)
    mock_client.delete_dynamic_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_dynamic_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_dynamic_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_dynamic_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete dynamic thing group"):
        delete_dynamic_thing_group("test-thing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_fleet_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet_metric.return_value = {}
    delete_fleet_metric("test-metric_name", region_name=REGION)
    mock_client.delete_fleet_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_fleet_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_fleet_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_fleet_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to delete fleet metric"):
        delete_fleet_metric("test-metric_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job.return_value = {}
    delete_job("test-job_id", region_name=REGION)
    mock_client.delete_job.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_job",
    )
    with pytest.raises(RuntimeError, match="Failed to delete job"):
        delete_job("test-job_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_job_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job_execution.return_value = {}
    delete_job_execution("test-job_id", "test-thing_name", 1, region_name=REGION)
    mock_client.delete_job_execution.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_job_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_job_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to delete job execution"):
        delete_job_execution("test-job_id", "test-thing_name", 1, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job_template.return_value = {}
    delete_job_template("test-job_template_id", region_name=REGION)
    mock_client.delete_job_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to delete job template"):
        delete_job_template("test-job_template_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_mitigation_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_mitigation_action.return_value = {}
    delete_mitigation_action("test-action_name", region_name=REGION)
    mock_client.delete_mitigation_action.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_mitigation_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_mitigation_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_mitigation_action",
    )
    with pytest.raises(RuntimeError, match="Failed to delete mitigation action"):
        delete_mitigation_action("test-action_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_ota_update(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_ota_update.return_value = {}
    delete_ota_update("test-ota_update_id", region_name=REGION)
    mock_client.delete_ota_update.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_ota_update_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_ota_update.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ota_update",
    )
    with pytest.raises(RuntimeError, match="Failed to delete ota update"):
        delete_ota_update("test-ota_update_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_package(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package.return_value = {}
    delete_package("test-package_name", region_name=REGION)
    mock_client.delete_package.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_package_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_package",
    )
    with pytest.raises(RuntimeError, match="Failed to delete package"):
        delete_package("test-package_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package_version.return_value = {}
    delete_package_version("test-package_name", "test-version_name", region_name=REGION)
    mock_client.delete_package_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to delete package version"):
        delete_package_version("test-package_name", "test-version_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_policy_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_policy_version.return_value = {}
    delete_policy_version("test-policy_name", "test-policy_version_id", region_name=REGION)
    mock_client.delete_policy_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_policy_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_policy_version",
    )
    with pytest.raises(RuntimeError, match="Failed to delete policy version"):
        delete_policy_version("test-policy_name", "test-policy_version_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_provisioning_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_provisioning_template.return_value = {}
    delete_provisioning_template("test-template_name", region_name=REGION)
    mock_client.delete_provisioning_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_provisioning_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_provisioning_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_provisioning_template",
    )
    with pytest.raises(RuntimeError, match="Failed to delete provisioning template"):
        delete_provisioning_template("test-template_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_provisioning_template_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_provisioning_template_version.return_value = {}
    delete_provisioning_template_version("test-template_name", 1, region_name=REGION)
    mock_client.delete_provisioning_template_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_provisioning_template_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_provisioning_template_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_provisioning_template_version",
    )
    with pytest.raises(RuntimeError, match="Failed to delete provisioning template version"):
        delete_provisioning_template_version("test-template_name", 1, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_registration_code(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_registration_code.return_value = {}
    delete_registration_code(region_name=REGION)
    mock_client.delete_registration_code.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_registration_code_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_registration_code.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_registration_code",
    )
    with pytest.raises(RuntimeError, match="Failed to delete registration code"):
        delete_registration_code(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_role_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_role_alias.return_value = {}
    delete_role_alias("test-role_alias", region_name=REGION)
    mock_client.delete_role_alias.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_role_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_role_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_role_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to delete role alias"):
        delete_role_alias("test-role_alias", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_scheduled_audit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_scheduled_audit.return_value = {}
    delete_scheduled_audit("test-scheduled_audit_name", region_name=REGION)
    mock_client.delete_scheduled_audit.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_scheduled_audit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_scheduled_audit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_scheduled_audit",
    )
    with pytest.raises(RuntimeError, match="Failed to delete scheduled audit"):
        delete_scheduled_audit("test-scheduled_audit_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_security_profile.return_value = {}
    delete_security_profile("test-security_profile_name", region_name=REGION)
    mock_client.delete_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to delete security profile"):
        delete_security_profile("test-security_profile_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_stream(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_stream.return_value = {}
    delete_stream("test-stream_id", region_name=REGION)
    mock_client.delete_stream.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_stream_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_stream",
    )
    with pytest.raises(RuntimeError, match="Failed to delete stream"):
        delete_stream("test-stream_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_thing_group.return_value = {}
    delete_thing_group("test-thing_group_name", region_name=REGION)
    mock_client.delete_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete thing group"):
        delete_thing_group("test-thing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_thing_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_thing_type.return_value = {}
    delete_thing_type("test-thing_type_name", region_name=REGION)
    mock_client.delete_thing_type.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_thing_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_thing_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_thing_type",
    )
    with pytest.raises(RuntimeError, match="Failed to delete thing type"):
        delete_thing_type("test-thing_type_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_topic_rule_destination(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_topic_rule_destination.return_value = {}
    delete_topic_rule_destination("test-arn", region_name=REGION)
    mock_client.delete_topic_rule_destination.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_topic_rule_destination_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_topic_rule_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_topic_rule_destination",
    )
    with pytest.raises(RuntimeError, match="Failed to delete topic rule destination"):
        delete_topic_rule_destination("test-arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_delete_v2_logging_level(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_v2_logging_level.return_value = {}
    delete_v2_logging_level("test-target_type", "test-target_name", region_name=REGION)
    mock_client.delete_v2_logging_level.assert_called_once()


@patch("aws_util.iot.get_client")
def test_delete_v2_logging_level_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_v2_logging_level.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_v2_logging_level",
    )
    with pytest.raises(RuntimeError, match="Failed to delete v2 logging level"):
        delete_v2_logging_level("test-target_type", "test-target_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_deprecate_thing_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.deprecate_thing_type.return_value = {}
    deprecate_thing_type("test-thing_type_name", region_name=REGION)
    mock_client.deprecate_thing_type.assert_called_once()


@patch("aws_util.iot.get_client")
def test_deprecate_thing_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.deprecate_thing_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deprecate_thing_type",
    )
    with pytest.raises(RuntimeError, match="Failed to deprecate thing type"):
        deprecate_thing_type("test-thing_type_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_account_audit_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_audit_configuration.return_value = {}
    describe_account_audit_configuration(region_name=REGION)
    mock_client.describe_account_audit_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_account_audit_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_account_audit_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_audit_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe account audit configuration"):
        describe_account_audit_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_audit_finding(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_finding.return_value = {}
    describe_audit_finding("test-finding_id", region_name=REGION)
    mock_client.describe_audit_finding.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_audit_finding_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_finding.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_audit_finding",
    )
    with pytest.raises(RuntimeError, match="Failed to describe audit finding"):
        describe_audit_finding("test-finding_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_audit_mitigation_actions_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_mitigation_actions_task.return_value = {}
    describe_audit_mitigation_actions_task("test-task_id", region_name=REGION)
    mock_client.describe_audit_mitigation_actions_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_audit_mitigation_actions_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_mitigation_actions_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_audit_mitigation_actions_task",
    )
    with pytest.raises(RuntimeError, match="Failed to describe audit mitigation actions task"):
        describe_audit_mitigation_actions_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_audit_suppression(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_suppression.return_value = {}
    describe_audit_suppression("test-check_name", {}, region_name=REGION)
    mock_client.describe_audit_suppression.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_audit_suppression_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_suppression.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_audit_suppression",
    )
    with pytest.raises(RuntimeError, match="Failed to describe audit suppression"):
        describe_audit_suppression("test-check_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_audit_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_task.return_value = {}
    describe_audit_task("test-task_id", region_name=REGION)
    mock_client.describe_audit_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_audit_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_audit_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_audit_task",
    )
    with pytest.raises(RuntimeError, match="Failed to describe audit task"):
        describe_audit_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_authorizer.return_value = {}
    describe_authorizer("test-authorizer_name", region_name=REGION)
    mock_client.describe_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to describe authorizer"):
        describe_authorizer("test-authorizer_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_billing_group.return_value = {}
    describe_billing_group("test-billing_group_name", region_name=REGION)
    mock_client.describe_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to describe billing group"):
        describe_billing_group("test-billing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_ca_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_ca_certificate.return_value = {}
    describe_ca_certificate("test-certificate_id", region_name=REGION)
    mock_client.describe_ca_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_ca_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_ca_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_ca_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to describe ca certificate"):
        describe_ca_certificate("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificate.return_value = {}
    describe_certificate("test-certificate_id", region_name=REGION)
    mock_client.describe_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to describe certificate"):
        describe_certificate("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_certificate_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificate_provider.return_value = {}
    describe_certificate_provider("test-certificate_provider_name", region_name=REGION)
    mock_client.describe_certificate_provider.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_certificate_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificate_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_certificate_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to describe certificate provider"):
        describe_certificate_provider("test-certificate_provider_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_custom_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_custom_metric.return_value = {}
    describe_custom_metric("test-metric_name", region_name=REGION)
    mock_client.describe_custom_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_custom_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_custom_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_custom_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to describe custom metric"):
        describe_custom_metric("test-metric_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_default_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_default_authorizer.return_value = {}
    describe_default_authorizer(region_name=REGION)
    mock_client.describe_default_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_default_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_default_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_default_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to describe default authorizer"):
        describe_default_authorizer(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_detect_mitigation_actions_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_detect_mitigation_actions_task.return_value = {}
    describe_detect_mitigation_actions_task("test-task_id", region_name=REGION)
    mock_client.describe_detect_mitigation_actions_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_detect_mitigation_actions_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_detect_mitigation_actions_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_detect_mitigation_actions_task",
    )
    with pytest.raises(RuntimeError, match="Failed to describe detect mitigation actions task"):
        describe_detect_mitigation_actions_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_dimension(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_dimension.return_value = {}
    describe_dimension("test-name", region_name=REGION)
    mock_client.describe_dimension.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_dimension_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_dimension.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_dimension",
    )
    with pytest.raises(RuntimeError, match="Failed to describe dimension"):
        describe_dimension("test-name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_domain_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_domain_configuration.return_value = {}
    describe_domain_configuration("test-domain_configuration_name", region_name=REGION)
    mock_client.describe_domain_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_domain_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_domain_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_domain_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe domain configuration"):
        describe_domain_configuration("test-domain_configuration_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_encryption_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_encryption_configuration.return_value = {}
    describe_encryption_configuration(region_name=REGION)
    mock_client.describe_encryption_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_encryption_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_encryption_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_encryption_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe encryption configuration"):
        describe_encryption_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_endpoint.return_value = {}
    describe_endpoint(region_name=REGION)
    mock_client.describe_endpoint.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to describe endpoint"):
        describe_endpoint(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_event_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_configurations.return_value = {}
    describe_event_configurations(region_name=REGION)
    mock_client.describe_event_configurations.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_event_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event configurations"):
        describe_event_configurations(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_fleet_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_metric.return_value = {}
    describe_fleet_metric("test-metric_name", region_name=REGION)
    mock_client.describe_fleet_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_fleet_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_fleet_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_fleet_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to describe fleet metric"):
        describe_fleet_metric("test-metric_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_index(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_index.return_value = {}
    describe_index("test-index_name", region_name=REGION)
    mock_client.describe_index.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_index_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_index.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_index",
    )
    with pytest.raises(RuntimeError, match="Failed to describe index"):
        describe_index("test-index_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_job_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_execution.return_value = {}
    describe_job_execution("test-job_id", "test-thing_name", region_name=REGION)
    mock_client.describe_job_execution.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_job_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_job_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to describe job execution"):
        describe_job_execution("test-job_id", "test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_template.return_value = {}
    describe_job_template("test-job_template_id", region_name=REGION)
    mock_client.describe_job_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to describe job template"):
        describe_job_template("test-job_template_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_managed_job_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_managed_job_template.return_value = {}
    describe_managed_job_template("test-template_name", region_name=REGION)
    mock_client.describe_managed_job_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_managed_job_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_managed_job_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_managed_job_template",
    )
    with pytest.raises(RuntimeError, match="Failed to describe managed job template"):
        describe_managed_job_template("test-template_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_mitigation_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_mitigation_action.return_value = {}
    describe_mitigation_action("test-action_name", region_name=REGION)
    mock_client.describe_mitigation_action.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_mitigation_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_mitigation_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_mitigation_action",
    )
    with pytest.raises(RuntimeError, match="Failed to describe mitigation action"):
        describe_mitigation_action("test-action_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_provisioning_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_provisioning_template.return_value = {}
    describe_provisioning_template("test-template_name", region_name=REGION)
    mock_client.describe_provisioning_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_provisioning_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_provisioning_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_provisioning_template",
    )
    with pytest.raises(RuntimeError, match="Failed to describe provisioning template"):
        describe_provisioning_template("test-template_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_provisioning_template_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_provisioning_template_version.return_value = {}
    describe_provisioning_template_version("test-template_name", 1, region_name=REGION)
    mock_client.describe_provisioning_template_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_provisioning_template_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_provisioning_template_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_provisioning_template_version",
    )
    with pytest.raises(RuntimeError, match="Failed to describe provisioning template version"):
        describe_provisioning_template_version("test-template_name", 1, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_role_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_role_alias.return_value = {}
    describe_role_alias("test-role_alias", region_name=REGION)
    mock_client.describe_role_alias.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_role_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_role_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_role_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to describe role alias"):
        describe_role_alias("test-role_alias", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_scheduled_audit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_scheduled_audit.return_value = {}
    describe_scheduled_audit("test-scheduled_audit_name", region_name=REGION)
    mock_client.describe_scheduled_audit.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_scheduled_audit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_scheduled_audit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduled_audit",
    )
    with pytest.raises(RuntimeError, match="Failed to describe scheduled audit"):
        describe_scheduled_audit("test-scheduled_audit_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_security_profile.return_value = {}
    describe_security_profile("test-security_profile_name", region_name=REGION)
    mock_client.describe_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to describe security profile"):
        describe_security_profile("test-security_profile_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_stream(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_stream.return_value = {}
    describe_stream("test-stream_id", region_name=REGION)
    mock_client.describe_stream.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_stream_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_stream",
    )
    with pytest.raises(RuntimeError, match="Failed to describe stream"):
        describe_stream("test-stream_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_thing_group.return_value = {}
    describe_thing_group("test-thing_group_name", region_name=REGION)
    mock_client.describe_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to describe thing group"):
        describe_thing_group("test-thing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_thing_registration_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_thing_registration_task.return_value = {}
    describe_thing_registration_task("test-task_id", region_name=REGION)
    mock_client.describe_thing_registration_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_thing_registration_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_thing_registration_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_thing_registration_task",
    )
    with pytest.raises(RuntimeError, match="Failed to describe thing registration task"):
        describe_thing_registration_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_describe_thing_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_thing_type.return_value = {}
    describe_thing_type("test-thing_type_name", region_name=REGION)
    mock_client.describe_thing_type.assert_called_once()


@patch("aws_util.iot.get_client")
def test_describe_thing_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_thing_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_thing_type",
    )
    with pytest.raises(RuntimeError, match="Failed to describe thing type"):
        describe_thing_type("test-thing_type_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_detach_principal_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_principal_policy.return_value = {}
    detach_principal_policy("test-policy_name", "test-principal", region_name=REGION)
    mock_client.detach_principal_policy.assert_called_once()


@patch("aws_util.iot.get_client")
def test_detach_principal_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_principal_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_principal_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to detach principal policy"):
        detach_principal_policy("test-policy_name", "test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_detach_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_security_profile.return_value = {}
    detach_security_profile("test-security_profile_name", "test-security_profile_target_arn", region_name=REGION)
    mock_client.detach_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_detach_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to detach security profile"):
        detach_security_profile("test-security_profile_name", "test-security_profile_target_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_detach_thing_principal(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_thing_principal.return_value = {}
    detach_thing_principal("test-thing_name", "test-principal", region_name=REGION)
    mock_client.detach_thing_principal.assert_called_once()


@patch("aws_util.iot.get_client")
def test_detach_thing_principal_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.detach_thing_principal.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_thing_principal",
    )
    with pytest.raises(RuntimeError, match="Failed to detach thing principal"):
        detach_thing_principal("test-thing_name", "test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_disable_topic_rule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_topic_rule.return_value = {}
    disable_topic_rule("test-rule_name", region_name=REGION)
    mock_client.disable_topic_rule.assert_called_once()


@patch("aws_util.iot.get_client")
def test_disable_topic_rule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_topic_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_topic_rule",
    )
    with pytest.raises(RuntimeError, match="Failed to disable topic rule"):
        disable_topic_rule("test-rule_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_disassociate_sbom_from_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_sbom_from_package_version.return_value = {}
    disassociate_sbom_from_package_version("test-package_name", "test-version_name", region_name=REGION)
    mock_client.disassociate_sbom_from_package_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_disassociate_sbom_from_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_sbom_from_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_sbom_from_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate sbom from package version"):
        disassociate_sbom_from_package_version("test-package_name", "test-version_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_enable_topic_rule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_topic_rule.return_value = {}
    enable_topic_rule("test-rule_name", region_name=REGION)
    mock_client.enable_topic_rule.assert_called_once()


@patch("aws_util.iot.get_client")
def test_enable_topic_rule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_topic_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_topic_rule",
    )
    with pytest.raises(RuntimeError, match="Failed to enable topic rule"):
        enable_topic_rule("test-rule_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_behavior_model_training_summaries(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_behavior_model_training_summaries.return_value = {}
    get_behavior_model_training_summaries(region_name=REGION)
    mock_client.get_behavior_model_training_summaries.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_behavior_model_training_summaries_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_behavior_model_training_summaries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_behavior_model_training_summaries",
    )
    with pytest.raises(RuntimeError, match="Failed to get behavior model training summaries"):
        get_behavior_model_training_summaries(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_buckets_aggregation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_buckets_aggregation.return_value = {}
    get_buckets_aggregation("test-query_string", "test-aggregation_field", {}, region_name=REGION)
    mock_client.get_buckets_aggregation.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_buckets_aggregation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_buckets_aggregation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_buckets_aggregation",
    )
    with pytest.raises(RuntimeError, match="Failed to get buckets aggregation"):
        get_buckets_aggregation("test-query_string", "test-aggregation_field", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_cardinality(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cardinality.return_value = {}
    get_cardinality("test-query_string", region_name=REGION)
    mock_client.get_cardinality.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_cardinality_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_cardinality.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cardinality",
    )
    with pytest.raises(RuntimeError, match="Failed to get cardinality"):
        get_cardinality("test-query_string", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_command(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_command.return_value = {}
    get_command("test-command_id", region_name=REGION)
    mock_client.get_command.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_command_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_command",
    )
    with pytest.raises(RuntimeError, match="Failed to get command"):
        get_command("test-command_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_command_execution(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_command_execution.return_value = {}
    get_command_execution("test-execution_id", "test-target_arn", region_name=REGION)
    mock_client.get_command_execution.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_command_execution_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_command_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_command_execution",
    )
    with pytest.raises(RuntimeError, match="Failed to get command execution"):
        get_command_execution("test-execution_id", "test-target_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_effective_policies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_effective_policies.return_value = {}
    get_effective_policies(region_name=REGION)
    mock_client.get_effective_policies.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_effective_policies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_effective_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_effective_policies",
    )
    with pytest.raises(RuntimeError, match="Failed to get effective policies"):
        get_effective_policies(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_indexing_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_indexing_configuration.return_value = {}
    get_indexing_configuration(region_name=REGION)
    mock_client.get_indexing_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_indexing_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_indexing_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_indexing_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get indexing configuration"):
        get_indexing_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_job_document(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_job_document.return_value = {}
    get_job_document("test-job_id", region_name=REGION)
    mock_client.get_job_document.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_job_document_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_job_document.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_job_document",
    )
    with pytest.raises(RuntimeError, match="Failed to get job document"):
        get_job_document("test-job_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_logging_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_logging_options.return_value = {}
    get_logging_options(region_name=REGION)
    mock_client.get_logging_options.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_logging_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_logging_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_logging_options",
    )
    with pytest.raises(RuntimeError, match="Failed to get logging options"):
        get_logging_options(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_ota_update(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_ota_update.return_value = {}
    get_ota_update("test-ota_update_id", region_name=REGION)
    mock_client.get_ota_update.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_ota_update_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_ota_update.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ota_update",
    )
    with pytest.raises(RuntimeError, match="Failed to get ota update"):
        get_ota_update("test-ota_update_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_package(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package.return_value = {}
    get_package("test-package_name", region_name=REGION)
    mock_client.get_package.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_package_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_package",
    )
    with pytest.raises(RuntimeError, match="Failed to get package"):
        get_package("test-package_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_package_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_configuration.return_value = {}
    get_package_configuration(region_name=REGION)
    mock_client.get_package_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_package_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_package_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get package configuration"):
        get_package_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_version.return_value = {}
    get_package_version("test-package_name", "test-version_name", region_name=REGION)
    mock_client.get_package_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to get package version"):
        get_package_version("test-package_name", "test-version_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_percentiles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_percentiles.return_value = {}
    get_percentiles("test-query_string", region_name=REGION)
    mock_client.get_percentiles.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_percentiles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_percentiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_percentiles",
    )
    with pytest.raises(RuntimeError, match="Failed to get percentiles"):
        get_percentiles("test-query_string", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_policy_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_policy_version.return_value = {}
    get_policy_version("test-policy_name", "test-policy_version_id", region_name=REGION)
    mock_client.get_policy_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_policy_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_policy_version",
    )
    with pytest.raises(RuntimeError, match="Failed to get policy version"):
        get_policy_version("test-policy_name", "test-policy_version_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_registration_code(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_registration_code.return_value = {}
    get_registration_code(region_name=REGION)
    mock_client.get_registration_code.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_registration_code_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_registration_code.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_registration_code",
    )
    with pytest.raises(RuntimeError, match="Failed to get registration code"):
        get_registration_code(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_statistics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_statistics.return_value = {}
    get_statistics("test-query_string", region_name=REGION)
    mock_client.get_statistics.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_statistics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_statistics",
    )
    with pytest.raises(RuntimeError, match="Failed to get statistics"):
        get_statistics("test-query_string", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_thing_connectivity_data(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_thing_connectivity_data.return_value = {}
    get_thing_connectivity_data("test-thing_name", region_name=REGION)
    mock_client.get_thing_connectivity_data.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_thing_connectivity_data_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_thing_connectivity_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_thing_connectivity_data",
    )
    with pytest.raises(RuntimeError, match="Failed to get thing connectivity data"):
        get_thing_connectivity_data("test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_topic_rule_destination(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_topic_rule_destination.return_value = {}
    get_topic_rule_destination("test-arn", region_name=REGION)
    mock_client.get_topic_rule_destination.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_topic_rule_destination_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_topic_rule_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_topic_rule_destination",
    )
    with pytest.raises(RuntimeError, match="Failed to get topic rule destination"):
        get_topic_rule_destination("test-arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_get_v2_logging_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_v2_logging_options.return_value = {}
    get_v2_logging_options(region_name=REGION)
    mock_client.get_v2_logging_options.assert_called_once()


@patch("aws_util.iot.get_client")
def test_get_v2_logging_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_v2_logging_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_v2_logging_options",
    )
    with pytest.raises(RuntimeError, match="Failed to get v2 logging options"):
        get_v2_logging_options(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_active_violations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_active_violations.return_value = {}
    list_active_violations(region_name=REGION)
    mock_client.list_active_violations.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_active_violations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_active_violations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_active_violations",
    )
    with pytest.raises(RuntimeError, match="Failed to list active violations"):
        list_active_violations(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_attached_policies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_attached_policies.return_value = {}
    list_attached_policies("test-target", region_name=REGION)
    mock_client.list_attached_policies.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_attached_policies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_attached_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_attached_policies",
    )
    with pytest.raises(RuntimeError, match="Failed to list attached policies"):
        list_attached_policies("test-target", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_audit_findings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_findings.return_value = {}
    list_audit_findings(region_name=REGION)
    mock_client.list_audit_findings.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_audit_findings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_audit_findings",
    )
    with pytest.raises(RuntimeError, match="Failed to list audit findings"):
        list_audit_findings(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_audit_mitigation_actions_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_mitigation_actions_executions.return_value = {}
    list_audit_mitigation_actions_executions("test-task_id", "test-finding_id", region_name=REGION)
    mock_client.list_audit_mitigation_actions_executions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_audit_mitigation_actions_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_mitigation_actions_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_audit_mitigation_actions_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list audit mitigation actions executions"):
        list_audit_mitigation_actions_executions("test-task_id", "test-finding_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_audit_mitigation_actions_tasks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_mitigation_actions_tasks.return_value = {}
    list_audit_mitigation_actions_tasks("test-start_time", "test-end_time", region_name=REGION)
    mock_client.list_audit_mitigation_actions_tasks.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_audit_mitigation_actions_tasks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_mitigation_actions_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_audit_mitigation_actions_tasks",
    )
    with pytest.raises(RuntimeError, match="Failed to list audit mitigation actions tasks"):
        list_audit_mitigation_actions_tasks("test-start_time", "test-end_time", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_audit_suppressions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_suppressions.return_value = {}
    list_audit_suppressions(region_name=REGION)
    mock_client.list_audit_suppressions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_audit_suppressions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_suppressions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_audit_suppressions",
    )
    with pytest.raises(RuntimeError, match="Failed to list audit suppressions"):
        list_audit_suppressions(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_audit_tasks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_tasks.return_value = {}
    list_audit_tasks("test-start_time", "test-end_time", region_name=REGION)
    mock_client.list_audit_tasks.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_audit_tasks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_audit_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_audit_tasks",
    )
    with pytest.raises(RuntimeError, match="Failed to list audit tasks"):
        list_audit_tasks("test-start_time", "test-end_time", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_authorizers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_authorizers.return_value = {}
    list_authorizers(region_name=REGION)
    mock_client.list_authorizers.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_authorizers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_authorizers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_authorizers",
    )
    with pytest.raises(RuntimeError, match="Failed to list authorizers"):
        list_authorizers(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_billing_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_billing_groups.return_value = {}
    list_billing_groups(region_name=REGION)
    mock_client.list_billing_groups.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_billing_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_billing_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_billing_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to list billing groups"):
        list_billing_groups(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_ca_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_ca_certificates.return_value = {}
    list_ca_certificates(region_name=REGION)
    mock_client.list_ca_certificates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_ca_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_ca_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ca_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to list ca certificates"):
        list_ca_certificates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_certificate_providers(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_certificate_providers.return_value = {}
    list_certificate_providers(region_name=REGION)
    mock_client.list_certificate_providers.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_certificate_providers_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_certificate_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_certificate_providers",
    )
    with pytest.raises(RuntimeError, match="Failed to list certificate providers"):
        list_certificate_providers(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_certificates.return_value = {}
    list_certificates(region_name=REGION)
    mock_client.list_certificates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to list certificates"):
        list_certificates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_certificates_by_ca(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_certificates_by_ca.return_value = {}
    list_certificates_by_ca("test-ca_certificate_id", region_name=REGION)
    mock_client.list_certificates_by_ca.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_certificates_by_ca_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_certificates_by_ca.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_certificates_by_ca",
    )
    with pytest.raises(RuntimeError, match="Failed to list certificates by ca"):
        list_certificates_by_ca("test-ca_certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_command_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_command_executions.return_value = {}
    list_command_executions(region_name=REGION)
    mock_client.list_command_executions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_command_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_command_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_command_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list command executions"):
        list_command_executions(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_commands(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_commands.return_value = {}
    list_commands(region_name=REGION)
    mock_client.list_commands.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_commands_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_commands.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_commands",
    )
    with pytest.raises(RuntimeError, match="Failed to list commands"):
        list_commands(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_custom_metrics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_custom_metrics.return_value = {}
    list_custom_metrics(region_name=REGION)
    mock_client.list_custom_metrics.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_custom_metrics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_custom_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_custom_metrics",
    )
    with pytest.raises(RuntimeError, match="Failed to list custom metrics"):
        list_custom_metrics(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_detect_mitigation_actions_executions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_detect_mitigation_actions_executions.return_value = {}
    list_detect_mitigation_actions_executions(region_name=REGION)
    mock_client.list_detect_mitigation_actions_executions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_detect_mitigation_actions_executions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_detect_mitigation_actions_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_detect_mitigation_actions_executions",
    )
    with pytest.raises(RuntimeError, match="Failed to list detect mitigation actions executions"):
        list_detect_mitigation_actions_executions(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_detect_mitigation_actions_tasks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_detect_mitigation_actions_tasks.return_value = {}
    list_detect_mitigation_actions_tasks("test-start_time", "test-end_time", region_name=REGION)
    mock_client.list_detect_mitigation_actions_tasks.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_detect_mitigation_actions_tasks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_detect_mitigation_actions_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_detect_mitigation_actions_tasks",
    )
    with pytest.raises(RuntimeError, match="Failed to list detect mitigation actions tasks"):
        list_detect_mitigation_actions_tasks("test-start_time", "test-end_time", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_dimensions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_dimensions.return_value = {}
    list_dimensions(region_name=REGION)
    mock_client.list_dimensions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_dimensions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_dimensions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_dimensions",
    )
    with pytest.raises(RuntimeError, match="Failed to list dimensions"):
        list_dimensions(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_domain_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_domain_configurations.return_value = {}
    list_domain_configurations(region_name=REGION)
    mock_client.list_domain_configurations.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_domain_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_domain_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_domain_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to list domain configurations"):
        list_domain_configurations(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_fleet_metrics(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_fleet_metrics.return_value = {}
    list_fleet_metrics(region_name=REGION)
    mock_client.list_fleet_metrics.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_fleet_metrics_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_fleet_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_fleet_metrics",
    )
    with pytest.raises(RuntimeError, match="Failed to list fleet metrics"):
        list_fleet_metrics(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_indices(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_indices.return_value = {}
    list_indices(region_name=REGION)
    mock_client.list_indices.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_indices_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_indices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_indices",
    )
    with pytest.raises(RuntimeError, match="Failed to list indices"):
        list_indices(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_job_executions_for_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_executions_for_job.return_value = {}
    list_job_executions_for_job("test-job_id", region_name=REGION)
    mock_client.list_job_executions_for_job.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_job_executions_for_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_executions_for_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_job_executions_for_job",
    )
    with pytest.raises(RuntimeError, match="Failed to list job executions for job"):
        list_job_executions_for_job("test-job_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_job_executions_for_thing(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_executions_for_thing.return_value = {}
    list_job_executions_for_thing("test-thing_name", region_name=REGION)
    mock_client.list_job_executions_for_thing.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_job_executions_for_thing_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_executions_for_thing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_job_executions_for_thing",
    )
    with pytest.raises(RuntimeError, match="Failed to list job executions for thing"):
        list_job_executions_for_thing("test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_job_templates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_templates.return_value = {}
    list_job_templates(region_name=REGION)
    mock_client.list_job_templates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_job_templates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_job_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_job_templates",
    )
    with pytest.raises(RuntimeError, match="Failed to list job templates"):
        list_job_templates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_managed_job_templates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_managed_job_templates.return_value = {}
    list_managed_job_templates(region_name=REGION)
    mock_client.list_managed_job_templates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_managed_job_templates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_managed_job_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_managed_job_templates",
    )
    with pytest.raises(RuntimeError, match="Failed to list managed job templates"):
        list_managed_job_templates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_metric_values(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_metric_values.return_value = {}
    list_metric_values("test-thing_name", "test-metric_name", "test-start_time", "test-end_time", region_name=REGION)
    mock_client.list_metric_values.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_metric_values_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_metric_values.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_metric_values",
    )
    with pytest.raises(RuntimeError, match="Failed to list metric values"):
        list_metric_values("test-thing_name", "test-metric_name", "test-start_time", "test-end_time", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_mitigation_actions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_mitigation_actions.return_value = {}
    list_mitigation_actions(region_name=REGION)
    mock_client.list_mitigation_actions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_mitigation_actions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_mitigation_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_mitigation_actions",
    )
    with pytest.raises(RuntimeError, match="Failed to list mitigation actions"):
        list_mitigation_actions(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_ota_updates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_ota_updates.return_value = {}
    list_ota_updates(region_name=REGION)
    mock_client.list_ota_updates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_ota_updates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_ota_updates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ota_updates",
    )
    with pytest.raises(RuntimeError, match="Failed to list ota updates"):
        list_ota_updates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_outgoing_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_outgoing_certificates.return_value = {}
    list_outgoing_certificates(region_name=REGION)
    mock_client.list_outgoing_certificates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_outgoing_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_outgoing_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_outgoing_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to list outgoing certificates"):
        list_outgoing_certificates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_package_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_versions.return_value = {}
    list_package_versions("test-package_name", region_name=REGION)
    mock_client.list_package_versions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_package_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_package_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_package_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list package versions"):
        list_package_versions("test-package_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_packages(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_packages.return_value = {}
    list_packages(region_name=REGION)
    mock_client.list_packages.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_packages_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_packages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_packages",
    )
    with pytest.raises(RuntimeError, match="Failed to list packages"):
        list_packages(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_policy_principals(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_policy_principals.return_value = {}
    list_policy_principals("test-policy_name", region_name=REGION)
    mock_client.list_policy_principals.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_policy_principals_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_policy_principals.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policy_principals",
    )
    with pytest.raises(RuntimeError, match="Failed to list policy principals"):
        list_policy_principals("test-policy_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_policy_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_policy_versions.return_value = {}
    list_policy_versions("test-policy_name", region_name=REGION)
    mock_client.list_policy_versions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_policy_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_policy_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policy_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list policy versions"):
        list_policy_versions("test-policy_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_principal_policies(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_principal_policies.return_value = {}
    list_principal_policies("test-principal", region_name=REGION)
    mock_client.list_principal_policies.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_principal_policies_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_principal_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_principal_policies",
    )
    with pytest.raises(RuntimeError, match="Failed to list principal policies"):
        list_principal_policies("test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_principal_things(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_principal_things.return_value = {}
    list_principal_things("test-principal", region_name=REGION)
    mock_client.list_principal_things.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_principal_things_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_principal_things.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_principal_things",
    )
    with pytest.raises(RuntimeError, match="Failed to list principal things"):
        list_principal_things("test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_principal_things_v2(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_principal_things_v2.return_value = {}
    list_principal_things_v2("test-principal", region_name=REGION)
    mock_client.list_principal_things_v2.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_principal_things_v2_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_principal_things_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_principal_things_v2",
    )
    with pytest.raises(RuntimeError, match="Failed to list principal things v2"):
        list_principal_things_v2("test-principal", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_provisioning_template_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_provisioning_template_versions.return_value = {}
    list_provisioning_template_versions("test-template_name", region_name=REGION)
    mock_client.list_provisioning_template_versions.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_provisioning_template_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_provisioning_template_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_provisioning_template_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to list provisioning template versions"):
        list_provisioning_template_versions("test-template_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_provisioning_templates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_provisioning_templates.return_value = {}
    list_provisioning_templates(region_name=REGION)
    mock_client.list_provisioning_templates.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_provisioning_templates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_provisioning_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_provisioning_templates",
    )
    with pytest.raises(RuntimeError, match="Failed to list provisioning templates"):
        list_provisioning_templates(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_related_resources_for_audit_finding(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_related_resources_for_audit_finding.return_value = {}
    list_related_resources_for_audit_finding("test-finding_id", region_name=REGION)
    mock_client.list_related_resources_for_audit_finding.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_related_resources_for_audit_finding_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_related_resources_for_audit_finding.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_related_resources_for_audit_finding",
    )
    with pytest.raises(RuntimeError, match="Failed to list related resources for audit finding"):
        list_related_resources_for_audit_finding("test-finding_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_role_aliases(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_role_aliases.return_value = {}
    list_role_aliases(region_name=REGION)
    mock_client.list_role_aliases.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_role_aliases_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_role_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_role_aliases",
    )
    with pytest.raises(RuntimeError, match="Failed to list role aliases"):
        list_role_aliases(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_sbom_validation_results(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sbom_validation_results.return_value = {}
    list_sbom_validation_results("test-package_name", "test-version_name", region_name=REGION)
    mock_client.list_sbom_validation_results.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_sbom_validation_results_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sbom_validation_results.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sbom_validation_results",
    )
    with pytest.raises(RuntimeError, match="Failed to list sbom validation results"):
        list_sbom_validation_results("test-package_name", "test-version_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_scheduled_audits(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_scheduled_audits.return_value = {}
    list_scheduled_audits(region_name=REGION)
    mock_client.list_scheduled_audits.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_scheduled_audits_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_scheduled_audits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_scheduled_audits",
    )
    with pytest.raises(RuntimeError, match="Failed to list scheduled audits"):
        list_scheduled_audits(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_security_profiles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_security_profiles.return_value = {}
    list_security_profiles(region_name=REGION)
    mock_client.list_security_profiles.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_security_profiles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_security_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_profiles",
    )
    with pytest.raises(RuntimeError, match="Failed to list security profiles"):
        list_security_profiles(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_security_profiles_for_target(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_security_profiles_for_target.return_value = {}
    list_security_profiles_for_target("test-security_profile_target_arn", region_name=REGION)
    mock_client.list_security_profiles_for_target.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_security_profiles_for_target_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_security_profiles_for_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_profiles_for_target",
    )
    with pytest.raises(RuntimeError, match="Failed to list security profiles for target"):
        list_security_profiles_for_target("test-security_profile_target_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_streams(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_streams.return_value = {}
    list_streams(region_name=REGION)
    mock_client.list_streams.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_streams_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_streams.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_streams",
    )
    with pytest.raises(RuntimeError, match="Failed to list streams"):
        list_streams(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_targets_for_policy(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_targets_for_policy.return_value = {}
    list_targets_for_policy("test-policy_name", region_name=REGION)
    mock_client.list_targets_for_policy.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_targets_for_policy_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_targets_for_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_targets_for_policy",
    )
    with pytest.raises(RuntimeError, match="Failed to list targets for policy"):
        list_targets_for_policy("test-policy_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_targets_for_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_targets_for_security_profile.return_value = {}
    list_targets_for_security_profile("test-security_profile_name", region_name=REGION)
    mock_client.list_targets_for_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_targets_for_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_targets_for_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_targets_for_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to list targets for security profile"):
        list_targets_for_security_profile("test-security_profile_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_groups_for_thing(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_groups_for_thing.return_value = {}
    list_thing_groups_for_thing("test-thing_name", region_name=REGION)
    mock_client.list_thing_groups_for_thing.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_thing_groups_for_thing_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_groups_for_thing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_thing_groups_for_thing",
    )
    with pytest.raises(RuntimeError, match="Failed to list thing groups for thing"):
        list_thing_groups_for_thing("test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_principals(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_principals.return_value = {}
    list_thing_principals("test-thing_name", region_name=REGION)
    mock_client.list_thing_principals.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_thing_principals_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_principals.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_thing_principals",
    )
    with pytest.raises(RuntimeError, match="Failed to list thing principals"):
        list_thing_principals("test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_principals_v2(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_principals_v2.return_value = {}
    list_thing_principals_v2("test-thing_name", region_name=REGION)
    mock_client.list_thing_principals_v2.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_thing_principals_v2_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_principals_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_thing_principals_v2",
    )
    with pytest.raises(RuntimeError, match="Failed to list thing principals v2"):
        list_thing_principals_v2("test-thing_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_registration_task_reports(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_registration_task_reports.return_value = {}
    list_thing_registration_task_reports("test-task_id", "test-report_type", region_name=REGION)
    mock_client.list_thing_registration_task_reports.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_thing_registration_task_reports_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_registration_task_reports.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_thing_registration_task_reports",
    )
    with pytest.raises(RuntimeError, match="Failed to list thing registration task reports"):
        list_thing_registration_task_reports("test-task_id", "test-report_type", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_thing_registration_tasks(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_registration_tasks.return_value = {}
    list_thing_registration_tasks(region_name=REGION)
    mock_client.list_thing_registration_tasks.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_thing_registration_tasks_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_thing_registration_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_thing_registration_tasks",
    )
    with pytest.raises(RuntimeError, match="Failed to list thing registration tasks"):
        list_thing_registration_tasks(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_things_in_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_things_in_billing_group.return_value = {}
    list_things_in_billing_group("test-billing_group_name", region_name=REGION)
    mock_client.list_things_in_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_things_in_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_things_in_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_things_in_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to list things in billing group"):
        list_things_in_billing_group("test-billing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_things_in_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_things_in_thing_group.return_value = {}
    list_things_in_thing_group("test-thing_group_name", region_name=REGION)
    mock_client.list_things_in_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_things_in_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_things_in_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_things_in_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to list things in thing group"):
        list_things_in_thing_group("test-thing_group_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_topic_rule_destinations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_topic_rule_destinations.return_value = {}
    list_topic_rule_destinations(region_name=REGION)
    mock_client.list_topic_rule_destinations.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_topic_rule_destinations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_topic_rule_destinations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_topic_rule_destinations",
    )
    with pytest.raises(RuntimeError, match="Failed to list topic rule destinations"):
        list_topic_rule_destinations(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_v2_logging_levels(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_v2_logging_levels.return_value = {}
    list_v2_logging_levels(region_name=REGION)
    mock_client.list_v2_logging_levels.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_v2_logging_levels_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_v2_logging_levels.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_v2_logging_levels",
    )
    with pytest.raises(RuntimeError, match="Failed to list v2 logging levels"):
        list_v2_logging_levels(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_list_violation_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_violation_events.return_value = {}
    list_violation_events("test-start_time", "test-end_time", region_name=REGION)
    mock_client.list_violation_events.assert_called_once()


@patch("aws_util.iot.get_client")
def test_list_violation_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_violation_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_violation_events",
    )
    with pytest.raises(RuntimeError, match="Failed to list violation events"):
        list_violation_events("test-start_time", "test-end_time", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_put_verification_state_on_violation(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_verification_state_on_violation.return_value = {}
    put_verification_state_on_violation("test-violation_id", "test-verification_state", region_name=REGION)
    mock_client.put_verification_state_on_violation.assert_called_once()


@patch("aws_util.iot.get_client")
def test_put_verification_state_on_violation_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.put_verification_state_on_violation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_verification_state_on_violation",
    )
    with pytest.raises(RuntimeError, match="Failed to put verification state on violation"):
        put_verification_state_on_violation("test-violation_id", "test-verification_state", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_register_ca_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_ca_certificate.return_value = {}
    register_ca_certificate("test-ca_certificate", region_name=REGION)
    mock_client.register_ca_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_register_ca_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_ca_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_ca_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to register ca certificate"):
        register_ca_certificate("test-ca_certificate", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_register_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_certificate.return_value = {}
    register_certificate("test-certificate_pem", region_name=REGION)
    mock_client.register_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_register_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to register certificate"):
        register_certificate("test-certificate_pem", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_register_certificate_without_ca(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_certificate_without_ca.return_value = {}
    register_certificate_without_ca("test-certificate_pem", region_name=REGION)
    mock_client.register_certificate_without_ca.assert_called_once()


@patch("aws_util.iot.get_client")
def test_register_certificate_without_ca_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_certificate_without_ca.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_certificate_without_ca",
    )
    with pytest.raises(RuntimeError, match="Failed to register certificate without ca"):
        register_certificate_without_ca("test-certificate_pem", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_register_thing(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_thing.return_value = {}
    register_thing("test-template_body", region_name=REGION)
    mock_client.register_thing.assert_called_once()


@patch("aws_util.iot.get_client")
def test_register_thing_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.register_thing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_thing",
    )
    with pytest.raises(RuntimeError, match="Failed to register thing"):
        register_thing("test-template_body", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_reject_certificate_transfer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reject_certificate_transfer.return_value = {}
    reject_certificate_transfer("test-certificate_id", region_name=REGION)
    mock_client.reject_certificate_transfer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_reject_certificate_transfer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reject_certificate_transfer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_certificate_transfer",
    )
    with pytest.raises(RuntimeError, match="Failed to reject certificate transfer"):
        reject_certificate_transfer("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_remove_thing_from_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_thing_from_billing_group.return_value = {}
    remove_thing_from_billing_group(region_name=REGION)
    mock_client.remove_thing_from_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_remove_thing_from_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_thing_from_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_thing_from_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to remove thing from billing group"):
        remove_thing_from_billing_group(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_remove_thing_from_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_thing_from_thing_group.return_value = {}
    remove_thing_from_thing_group(region_name=REGION)
    mock_client.remove_thing_from_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_remove_thing_from_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_thing_from_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_thing_from_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to remove thing from thing group"):
        remove_thing_from_thing_group(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_replace_topic_rule(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.replace_topic_rule.return_value = {}
    replace_topic_rule("test-rule_name", {}, region_name=REGION)
    mock_client.replace_topic_rule.assert_called_once()


@patch("aws_util.iot.get_client")
def test_replace_topic_rule_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.replace_topic_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replace_topic_rule",
    )
    with pytest.raises(RuntimeError, match="Failed to replace topic rule"):
        replace_topic_rule("test-rule_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_run_authorization(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_authorization.return_value = {}
    run_authorization([], region_name=REGION)
    mock_client.test_authorization.assert_called_once()


@patch("aws_util.iot.get_client")
def test_run_authorization_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_authorization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_authorization",
    )
    with pytest.raises(RuntimeError, match="Failed to run authorization"):
        run_authorization([], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_run_invoke_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_invoke_authorizer.return_value = {}
    run_invoke_authorizer("test-authorizer_name", region_name=REGION)
    mock_client.test_invoke_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_run_invoke_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.test_invoke_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_invoke_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to run invoke authorizer"):
        run_invoke_authorizer("test-authorizer_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_search_index(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_index.return_value = {}
    search_index("test-query_string", region_name=REGION)
    mock_client.search_index.assert_called_once()


@patch("aws_util.iot.get_client")
def test_search_index_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.search_index.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_index",
    )
    with pytest.raises(RuntimeError, match="Failed to search index"):
        search_index("test-query_string", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_set_default_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_default_authorizer.return_value = {}
    set_default_authorizer("test-authorizer_name", region_name=REGION)
    mock_client.set_default_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_set_default_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_default_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_default_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to set default authorizer"):
        set_default_authorizer("test-authorizer_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_set_default_policy_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_default_policy_version.return_value = {}
    set_default_policy_version("test-policy_name", "test-policy_version_id", region_name=REGION)
    mock_client.set_default_policy_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_set_default_policy_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_default_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_default_policy_version",
    )
    with pytest.raises(RuntimeError, match="Failed to set default policy version"):
        set_default_policy_version("test-policy_name", "test-policy_version_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_set_logging_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_logging_options.return_value = {}
    set_logging_options({}, region_name=REGION)
    mock_client.set_logging_options.assert_called_once()


@patch("aws_util.iot.get_client")
def test_set_logging_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_logging_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_logging_options",
    )
    with pytest.raises(RuntimeError, match="Failed to set logging options"):
        set_logging_options({}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_set_v2_logging_level(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_v2_logging_level.return_value = {}
    set_v2_logging_level({}, "test-log_level", region_name=REGION)
    mock_client.set_v2_logging_level.assert_called_once()


@patch("aws_util.iot.get_client")
def test_set_v2_logging_level_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_v2_logging_level.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_v2_logging_level",
    )
    with pytest.raises(RuntimeError, match="Failed to set v2 logging level"):
        set_v2_logging_level({}, "test-log_level", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_set_v2_logging_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_v2_logging_options.return_value = {}
    set_v2_logging_options(region_name=REGION)
    mock_client.set_v2_logging_options.assert_called_once()


@patch("aws_util.iot.get_client")
def test_set_v2_logging_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_v2_logging_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_v2_logging_options",
    )
    with pytest.raises(RuntimeError, match="Failed to set v2 logging options"):
        set_v2_logging_options(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_start_audit_mitigation_actions_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_audit_mitigation_actions_task.return_value = {}
    start_audit_mitigation_actions_task("test-task_id", {}, {}, "test-client_request_token", region_name=REGION)
    mock_client.start_audit_mitigation_actions_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_start_audit_mitigation_actions_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_audit_mitigation_actions_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_audit_mitigation_actions_task",
    )
    with pytest.raises(RuntimeError, match="Failed to start audit mitigation actions task"):
        start_audit_mitigation_actions_task("test-task_id", {}, {}, "test-client_request_token", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_start_detect_mitigation_actions_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_detect_mitigation_actions_task.return_value = {}
    start_detect_mitigation_actions_task("test-task_id", {}, [], "test-client_request_token", region_name=REGION)
    mock_client.start_detect_mitigation_actions_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_start_detect_mitigation_actions_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_detect_mitigation_actions_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_detect_mitigation_actions_task",
    )
    with pytest.raises(RuntimeError, match="Failed to start detect mitigation actions task"):
        start_detect_mitigation_actions_task("test-task_id", {}, [], "test-client_request_token", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_start_on_demand_audit_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_on_demand_audit_task.return_value = {}
    start_on_demand_audit_task([], region_name=REGION)
    mock_client.start_on_demand_audit_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_start_on_demand_audit_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_on_demand_audit_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_on_demand_audit_task",
    )
    with pytest.raises(RuntimeError, match="Failed to start on demand audit task"):
        start_on_demand_audit_task([], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_start_thing_registration_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_thing_registration_task.return_value = {}
    start_thing_registration_task("test-template_body", "test-input_file_bucket", "test-input_file_key", "test-role_arn", region_name=REGION)
    mock_client.start_thing_registration_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_start_thing_registration_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_thing_registration_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_thing_registration_task",
    )
    with pytest.raises(RuntimeError, match="Failed to start thing registration task"):
        start_thing_registration_task("test-template_body", "test-input_file_bucket", "test-input_file_key", "test-role_arn", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_stop_thing_registration_task(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_thing_registration_task.return_value = {}
    stop_thing_registration_task("test-task_id", region_name=REGION)
    mock_client.stop_thing_registration_task.assert_called_once()


@patch("aws_util.iot.get_client")
def test_stop_thing_registration_task_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_thing_registration_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_thing_registration_task",
    )
    with pytest.raises(RuntimeError, match="Failed to stop thing registration task"):
        stop_thing_registration_task("test-task_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.iot.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_transfer_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.transfer_certificate.return_value = {}
    transfer_certificate("test-certificate_id", "test-target_aws_account", region_name=REGION)
    mock_client.transfer_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_transfer_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.transfer_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "transfer_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to transfer certificate"):
        transfer_certificate("test-certificate_id", "test-target_aws_account", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.iot.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_account_audit_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_account_audit_configuration.return_value = {}
    update_account_audit_configuration(region_name=REGION)
    mock_client.update_account_audit_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_account_audit_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_account_audit_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_audit_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update account audit configuration"):
        update_account_audit_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_audit_suppression(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_audit_suppression.return_value = {}
    update_audit_suppression("test-check_name", {}, region_name=REGION)
    mock_client.update_audit_suppression.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_audit_suppression_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_audit_suppression.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_audit_suppression",
    )
    with pytest.raises(RuntimeError, match="Failed to update audit suppression"):
        update_audit_suppression("test-check_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_authorizer(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_authorizer.return_value = {}
    update_authorizer("test-authorizer_name", region_name=REGION)
    mock_client.update_authorizer.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_authorizer_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_authorizer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_authorizer",
    )
    with pytest.raises(RuntimeError, match="Failed to update authorizer"):
        update_authorizer("test-authorizer_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_billing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_billing_group.return_value = {}
    update_billing_group("test-billing_group_name", {}, region_name=REGION)
    mock_client.update_billing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_billing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_billing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_billing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update billing group"):
        update_billing_group("test-billing_group_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_ca_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_ca_certificate.return_value = {}
    update_ca_certificate("test-certificate_id", region_name=REGION)
    mock_client.update_ca_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_ca_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_ca_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ca_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to update ca certificate"):
        update_ca_certificate("test-certificate_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_certificate(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_certificate.return_value = {}
    update_certificate("test-certificate_id", "test-new_status", region_name=REGION)
    mock_client.update_certificate.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_certificate_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_certificate",
    )
    with pytest.raises(RuntimeError, match="Failed to update certificate"):
        update_certificate("test-certificate_id", "test-new_status", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_certificate_provider(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_certificate_provider.return_value = {}
    update_certificate_provider("test-certificate_provider_name", region_name=REGION)
    mock_client.update_certificate_provider.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_certificate_provider_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_certificate_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_certificate_provider",
    )
    with pytest.raises(RuntimeError, match="Failed to update certificate provider"):
        update_certificate_provider("test-certificate_provider_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_command(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_command.return_value = {}
    update_command("test-command_id", region_name=REGION)
    mock_client.update_command.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_command_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_command.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_command",
    )
    with pytest.raises(RuntimeError, match="Failed to update command"):
        update_command("test-command_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_custom_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_custom_metric.return_value = {}
    update_custom_metric("test-metric_name", "test-display_name", region_name=REGION)
    mock_client.update_custom_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_custom_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_custom_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_custom_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to update custom metric"):
        update_custom_metric("test-metric_name", "test-display_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_dimension(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dimension.return_value = {}
    update_dimension("test-name", [], region_name=REGION)
    mock_client.update_dimension.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_dimension_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dimension.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dimension",
    )
    with pytest.raises(RuntimeError, match="Failed to update dimension"):
        update_dimension("test-name", [], region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_domain_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_domain_configuration.return_value = {}
    update_domain_configuration("test-domain_configuration_name", region_name=REGION)
    mock_client.update_domain_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_domain_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_domain_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_domain_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update domain configuration"):
        update_domain_configuration("test-domain_configuration_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_dynamic_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dynamic_thing_group.return_value = {}
    update_dynamic_thing_group("test-thing_group_name", {}, region_name=REGION)
    mock_client.update_dynamic_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_dynamic_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_dynamic_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_dynamic_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update dynamic thing group"):
        update_dynamic_thing_group("test-thing_group_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_encryption_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_encryption_configuration.return_value = {}
    update_encryption_configuration("test-encryption_type", region_name=REGION)
    mock_client.update_encryption_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_encryption_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_encryption_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_encryption_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update encryption configuration"):
        update_encryption_configuration("test-encryption_type", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_event_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_event_configurations.return_value = {}
    update_event_configurations(region_name=REGION)
    mock_client.update_event_configurations.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_event_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_event_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_event_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to update event configurations"):
        update_event_configurations(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_fleet_metric(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_fleet_metric.return_value = {}
    update_fleet_metric("test-metric_name", "test-index_name", region_name=REGION)
    mock_client.update_fleet_metric.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_fleet_metric_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_fleet_metric.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_fleet_metric",
    )
    with pytest.raises(RuntimeError, match="Failed to update fleet metric"):
        update_fleet_metric("test-metric_name", "test-index_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_indexing_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_indexing_configuration.return_value = {}
    update_indexing_configuration(region_name=REGION)
    mock_client.update_indexing_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_indexing_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_indexing_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_indexing_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update indexing configuration"):
        update_indexing_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_job(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_job.return_value = {}
    update_job("test-job_id", region_name=REGION)
    mock_client.update_job.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_job_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_job",
    )
    with pytest.raises(RuntimeError, match="Failed to update job"):
        update_job("test-job_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_mitigation_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_mitigation_action.return_value = {}
    update_mitigation_action("test-action_name", region_name=REGION)
    mock_client.update_mitigation_action.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_mitigation_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_mitigation_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_mitigation_action",
    )
    with pytest.raises(RuntimeError, match="Failed to update mitigation action"):
        update_mitigation_action("test-action_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_package(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package.return_value = {}
    update_package("test-package_name", region_name=REGION)
    mock_client.update_package.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_package_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_package",
    )
    with pytest.raises(RuntimeError, match="Failed to update package"):
        update_package("test-package_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_package_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_configuration.return_value = {}
    update_package_configuration(region_name=REGION)
    mock_client.update_package_configuration.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_package_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_package_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update package configuration"):
        update_package_configuration(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_package_version(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_version.return_value = {}
    update_package_version("test-package_name", "test-version_name", region_name=REGION)
    mock_client.update_package_version.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_package_version_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_package_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_package_version",
    )
    with pytest.raises(RuntimeError, match="Failed to update package version"):
        update_package_version("test-package_name", "test-version_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_provisioning_template(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_provisioning_template.return_value = {}
    update_provisioning_template("test-template_name", region_name=REGION)
    mock_client.update_provisioning_template.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_provisioning_template_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_provisioning_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_provisioning_template",
    )
    with pytest.raises(RuntimeError, match="Failed to update provisioning template"):
        update_provisioning_template("test-template_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_role_alias(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_role_alias.return_value = {}
    update_role_alias("test-role_alias", region_name=REGION)
    mock_client.update_role_alias.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_role_alias_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_role_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_role_alias",
    )
    with pytest.raises(RuntimeError, match="Failed to update role alias"):
        update_role_alias("test-role_alias", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_scheduled_audit(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_scheduled_audit.return_value = {}
    update_scheduled_audit("test-scheduled_audit_name", region_name=REGION)
    mock_client.update_scheduled_audit.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_scheduled_audit_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_scheduled_audit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_scheduled_audit",
    )
    with pytest.raises(RuntimeError, match="Failed to update scheduled audit"):
        update_scheduled_audit("test-scheduled_audit_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_security_profile(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_security_profile.return_value = {}
    update_security_profile("test-security_profile_name", region_name=REGION)
    mock_client.update_security_profile.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_security_profile_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security_profile",
    )
    with pytest.raises(RuntimeError, match="Failed to update security profile"):
        update_security_profile("test-security_profile_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_stream(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_stream.return_value = {}
    update_stream("test-stream_id", region_name=REGION)
    mock_client.update_stream.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_stream_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_stream",
    )
    with pytest.raises(RuntimeError, match="Failed to update stream"):
        update_stream("test-stream_id", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_thing_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_thing_group.return_value = {}
    update_thing_group("test-thing_group_name", {}, region_name=REGION)
    mock_client.update_thing_group.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_thing_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_thing_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_thing_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update thing group"):
        update_thing_group("test-thing_group_name", {}, region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_thing_groups_for_thing(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_thing_groups_for_thing.return_value = {}
    update_thing_groups_for_thing(region_name=REGION)
    mock_client.update_thing_groups_for_thing.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_thing_groups_for_thing_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_thing_groups_for_thing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_thing_groups_for_thing",
    )
    with pytest.raises(RuntimeError, match="Failed to update thing groups for thing"):
        update_thing_groups_for_thing(region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_thing_type(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_thing_type.return_value = {}
    update_thing_type("test-thing_type_name", region_name=REGION)
    mock_client.update_thing_type.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_thing_type_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_thing_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_thing_type",
    )
    with pytest.raises(RuntimeError, match="Failed to update thing type"):
        update_thing_type("test-thing_type_name", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_update_topic_rule_destination(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_topic_rule_destination.return_value = {}
    update_topic_rule_destination("test-arn", "test-status", region_name=REGION)
    mock_client.update_topic_rule_destination.assert_called_once()


@patch("aws_util.iot.get_client")
def test_update_topic_rule_destination_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_topic_rule_destination.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_topic_rule_destination",
    )
    with pytest.raises(RuntimeError, match="Failed to update topic rule destination"):
        update_topic_rule_destination("test-arn", "test-status", region_name=REGION)


@patch("aws_util.iot.get_client")
def test_validate_security_profile_behaviors(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.validate_security_profile_behaviors.return_value = {}
    validate_security_profile_behaviors([], region_name=REGION)
    mock_client.validate_security_profile_behaviors.assert_called_once()


@patch("aws_util.iot.get_client")
def test_validate_security_profile_behaviors_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.validate_security_profile_behaviors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "validate_security_profile_behaviors",
    )
    with pytest.raises(RuntimeError, match="Failed to validate security profile behaviors"):
        validate_security_profile_behaviors([], region_name=REGION)


def test_update_thing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_thing
    mock_client = MagicMock()
    mock_client.update_thing.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_thing("test-thing_name", thing_type_name="test-thing_type_name", attributes="test-attributes", region_name="us-east-1")
    mock_client.update_thing.assert_called_once()

def test_create_thing_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_thing_type
    mock_client = MagicMock()
    mock_client.create_thing_type.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_thing_type("test-thing_type_name", searchable_attributes="test-searchable_attributes", description="test-description", region_name="us-east-1")
    mock_client.create_thing_type.assert_called_once()

def test_create_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_thing_group
    mock_client = MagicMock()
    mock_client.create_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_thing_group("test-thing_group_name", parent_group_name="test-parent_group_name", region_name="us-east-1")
    mock_client.create_thing_group.assert_called_once()

def test_accept_certificate_transfer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import accept_certificate_transfer
    mock_client = MagicMock()
    mock_client.accept_certificate_transfer.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    accept_certificate_transfer("test-certificate_id", set_as_active="test-set_as_active", region_name="us-east-1")
    mock_client.accept_certificate_transfer.assert_called_once()

def test_add_thing_to_billing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import add_thing_to_billing_group
    mock_client = MagicMock()
    mock_client.add_thing_to_billing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    add_thing_to_billing_group(billing_group_name="test-billing_group_name", billing_group_arn="test-billing_group_arn", thing_name="test-thing_name", thing_arn="test-thing_arn", region_name="us-east-1")
    mock_client.add_thing_to_billing_group.assert_called_once()

def test_associate_sbom_with_package_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import associate_sbom_with_package_version
    mock_client = MagicMock()
    mock_client.associate_sbom_with_package_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    associate_sbom_with_package_version("test-package_name", "test-version_name", "test-sbom", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_sbom_with_package_version.assert_called_once()

def test_associate_targets_with_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import associate_targets_with_job
    mock_client = MagicMock()
    mock_client.associate_targets_with_job.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    associate_targets_with_job("test-targets", "test-job_id", comment="test-comment", namespace_id="test-namespace_id", region_name="us-east-1")
    mock_client.associate_targets_with_job.assert_called_once()

def test_attach_thing_principal_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import attach_thing_principal
    mock_client = MagicMock()
    mock_client.attach_thing_principal.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    attach_thing_principal("test-thing_name", "test-principal", thing_principal_type="test-thing_principal_type", region_name="us-east-1")
    mock_client.attach_thing_principal.assert_called_once()

def test_cancel_job_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import cancel_job_execution
    mock_client = MagicMock()
    mock_client.cancel_job_execution.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    cancel_job_execution("test-job_id", "test-thing_name", force=True, expected_version="test-expected_version", status_details="test-status_details", region_name="us-east-1")
    mock_client.cancel_job_execution.assert_called_once()

def test_create_audit_suppression_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_audit_suppression
    mock_client = MagicMock()
    mock_client.create_audit_suppression.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_audit_suppression("test-check_name", "test-resource_identifier", "test-client_request_token", expiration_date="test-expiration_date", suppress_indefinitely="test-suppress_indefinitely", description="test-description", region_name="us-east-1")
    mock_client.create_audit_suppression.assert_called_once()

def test_create_authorizer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_authorizer
    mock_client = MagicMock()
    mock_client.create_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_authorizer("test-authorizer_name", "test-authorizer_function_arn", token_key_name="test-token_key_name", token_signing_public_keys="test-token_signing_public_keys", status="test-status", tags=[{"Key": "k", "Value": "v"}], signing_disabled="test-signing_disabled", enable_caching_for_http=True, region_name="us-east-1")
    mock_client.create_authorizer.assert_called_once()

def test_create_billing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_billing_group
    mock_client = MagicMock()
    mock_client.create_billing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_billing_group("test-billing_group_name", billing_group_properties={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_billing_group.assert_called_once()

def test_create_certificate_from_csr_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_certificate_from_csr
    mock_client = MagicMock()
    mock_client.create_certificate_from_csr.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_certificate_from_csr("test-certificate_signing_request", set_as_active="test-set_as_active", region_name="us-east-1")
    mock_client.create_certificate_from_csr.assert_called_once()

def test_create_certificate_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_certificate_provider
    mock_client = MagicMock()
    mock_client.create_certificate_provider.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_certificate_provider("test-certificate_provider_name", "test-lambda_function_arn", 1, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_certificate_provider.assert_called_once()

def test_create_command_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_command
    mock_client = MagicMock()
    mock_client.create_command.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_command("test-command_id", namespace="test-namespace", display_name="test-display_name", description="test-description", payload="test-payload", mandatory_parameters="test-mandatory_parameters", role_arn="test-role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_command.assert_called_once()

def test_create_custom_metric_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_custom_metric
    mock_client = MagicMock()
    mock_client.create_custom_metric.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_custom_metric("test-metric_name", "test-metric_type", "test-client_request_token", display_name="test-display_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_custom_metric.assert_called_once()

def test_create_dimension_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_dimension
    mock_client = MagicMock()
    mock_client.create_dimension.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_dimension("test-name", "test-type_value", "test-string_values", "test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dimension.assert_called_once()

def test_create_domain_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_domain_configuration
    mock_client = MagicMock()
    mock_client.create_domain_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_domain_configuration({}, domain_name="test-domain_name", server_certificate_arns="test-server_certificate_arns", validation_certificate_arn="test-validation_certificate_arn", authorizer_config={}, service_type="test-service_type", tags=[{"Key": "k", "Value": "v"}], tls_config={}, server_certificate_config={}, authentication_type="test-authentication_type", application_protocol="test-application_protocol", client_certificate_config={}, region_name="us-east-1")
    mock_client.create_domain_configuration.assert_called_once()

def test_create_dynamic_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_dynamic_thing_group
    mock_client = MagicMock()
    mock_client.create_dynamic_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_dynamic_thing_group("test-thing_group_name", "test-query_string", thing_group_properties={}, index_name="test-index_name", query_version="test-query_version", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_dynamic_thing_group.assert_called_once()

def test_create_fleet_metric_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_fleet_metric
    mock_client = MagicMock()
    mock_client.create_fleet_metric.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_fleet_metric("test-metric_name", "test-query_string", "test-aggregation_type", "test-period", "test-aggregation_field", description="test-description", query_version="test-query_version", index_name="test-index_name", unit="test-unit", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_fleet_metric.assert_called_once()

def test_create_job_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_job_template
    mock_client = MagicMock()
    mock_client.create_job_template.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_job_template("test-job_template_id", "test-description", job_arn="test-job_arn", document_source="test-document_source", document="test-document", presigned_url_config={}, job_executions_rollout_config={}, abort_config={}, timeout_config=1, tags=[{"Key": "k", "Value": "v"}], job_executions_retry_config={}, maintenance_windows="test-maintenance_windows", destination_package_versions="test-destination_package_versions", region_name="us-east-1")
    mock_client.create_job_template.assert_called_once()

def test_create_keys_and_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_keys_and_certificate
    mock_client = MagicMock()
    mock_client.create_keys_and_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_keys_and_certificate(set_as_active="test-set_as_active", region_name="us-east-1")
    mock_client.create_keys_and_certificate.assert_called_once()

def test_create_mitigation_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_mitigation_action
    mock_client = MagicMock()
    mock_client.create_mitigation_action.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_mitigation_action("test-action_name", "test-role_arn", "test-action_params", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_mitigation_action.assert_called_once()

def test_create_ota_update_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_ota_update
    mock_client = MagicMock()
    mock_client.create_ota_update.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_ota_update("test-ota_update_id", "test-targets", "test-files", "test-role_arn", description="test-description", protocols="test-protocols", target_selection="test-target_selection", aws_job_executions_rollout_config={}, aws_job_presigned_url_config={}, aws_job_abort_config={}, aws_job_timeout_config=1, additional_parameters="test-additional_parameters", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_ota_update.assert_called_once()

def test_create_package_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_package
    mock_client = MagicMock()
    mock_client.create_package.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_package("test-package_name", description="test-description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_package.assert_called_once()

def test_create_package_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_package_version
    mock_client = MagicMock()
    mock_client.create_package_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_package_version("test-package_name", "test-version_name", description="test-description", attributes="test-attributes", artifact="test-artifact", recipe="test-recipe", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_package_version.assert_called_once()

def test_create_policy_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_policy_version
    mock_client = MagicMock()
    mock_client.create_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_policy_version("test-policy_name", "test-policy_document", set_as_default="test-set_as_default", region_name="us-east-1")
    mock_client.create_policy_version.assert_called_once()

def test_create_provisioning_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_provisioning_template
    mock_client = MagicMock()
    mock_client.create_provisioning_template.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_provisioning_template("test-template_name", "test-template_body", "test-provisioning_role_arn", description="test-description", enabled=True, pre_provisioning_hook="test-pre_provisioning_hook", tags=[{"Key": "k", "Value": "v"}], type_value="test-type_value", region_name="us-east-1")
    mock_client.create_provisioning_template.assert_called_once()

def test_create_provisioning_template_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_provisioning_template_version
    mock_client = MagicMock()
    mock_client.create_provisioning_template_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_provisioning_template_version("test-template_name", "test-template_body", set_as_default="test-set_as_default", region_name="us-east-1")
    mock_client.create_provisioning_template_version.assert_called_once()

def test_create_role_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_role_alias
    mock_client = MagicMock()
    mock_client.create_role_alias.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_role_alias("test-role_alias", "test-role_arn", credential_duration_seconds=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_role_alias.assert_called_once()

def test_create_scheduled_audit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_scheduled_audit
    mock_client = MagicMock()
    mock_client.create_scheduled_audit.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_scheduled_audit("test-frequency", "test-target_check_names", "test-scheduled_audit_name", day_of_month="test-day_of_month", day_of_week="test-day_of_week", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_scheduled_audit.assert_called_once()

def test_create_security_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_security_profile
    mock_client = MagicMock()
    mock_client.create_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_security_profile("test-security_profile_name", security_profile_description="test-security_profile_description", behaviors="test-behaviors", alert_targets="test-alert_targets", additional_metrics_to_retain="test-additional_metrics_to_retain", additional_metrics_to_retain_v2="test-additional_metrics_to_retain_v2", tags=[{"Key": "k", "Value": "v"}], metrics_export_config=1, region_name="us-east-1")
    mock_client.create_security_profile.assert_called_once()

def test_create_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import create_stream
    mock_client = MagicMock()
    mock_client.create_stream.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    create_stream("test-stream_id", "test-files", "test-role_arn", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_stream.assert_called_once()

def test_delete_account_audit_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_account_audit_configuration
    mock_client = MagicMock()
    mock_client.delete_account_audit_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_account_audit_configuration(delete_scheduled_audits=True, region_name="us-east-1")
    mock_client.delete_account_audit_configuration.assert_called_once()

def test_delete_billing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_billing_group
    mock_client = MagicMock()
    mock_client.delete_billing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_billing_group("test-billing_group_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.delete_billing_group.assert_called_once()

def test_delete_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_certificate
    mock_client = MagicMock()
    mock_client.delete_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_certificate("test-certificate_id", force_delete=True, region_name="us-east-1")
    mock_client.delete_certificate.assert_called_once()

def test_delete_dynamic_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_dynamic_thing_group
    mock_client = MagicMock()
    mock_client.delete_dynamic_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_dynamic_thing_group("test-thing_group_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.delete_dynamic_thing_group.assert_called_once()

def test_delete_fleet_metric_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_fleet_metric
    mock_client = MagicMock()
    mock_client.delete_fleet_metric.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_fleet_metric("test-metric_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.delete_fleet_metric.assert_called_once()

def test_delete_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_job
    mock_client = MagicMock()
    mock_client.delete_job.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_job("test-job_id", force=True, namespace_id="test-namespace_id", region_name="us-east-1")
    mock_client.delete_job.assert_called_once()

def test_delete_job_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_job_execution
    mock_client = MagicMock()
    mock_client.delete_job_execution.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_job_execution("test-job_id", "test-thing_name", "test-execution_number", force=True, namespace_id="test-namespace_id", region_name="us-east-1")
    mock_client.delete_job_execution.assert_called_once()

def test_delete_ota_update_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_ota_update
    mock_client = MagicMock()
    mock_client.delete_ota_update.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_ota_update("test-ota_update_id", delete_stream=True, force_delete_aws_job=True, region_name="us-east-1")
    mock_client.delete_ota_update.assert_called_once()

def test_delete_package_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_package
    mock_client = MagicMock()
    mock_client.delete_package.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_package("test-package_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_package.assert_called_once()

def test_delete_package_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_package_version
    mock_client = MagicMock()
    mock_client.delete_package_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_package_version("test-package_name", "test-version_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.delete_package_version.assert_called_once()

def test_delete_security_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_security_profile
    mock_client = MagicMock()
    mock_client.delete_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_security_profile("test-security_profile_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.delete_security_profile.assert_called_once()

def test_delete_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import delete_thing_group
    mock_client = MagicMock()
    mock_client.delete_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    delete_thing_group("test-thing_group_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.delete_thing_group.assert_called_once()

def test_deprecate_thing_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import deprecate_thing_type
    mock_client = MagicMock()
    mock_client.deprecate_thing_type.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    deprecate_thing_type("test-thing_type_name", undo_deprecate="test-undo_deprecate", region_name="us-east-1")
    mock_client.deprecate_thing_type.assert_called_once()

def test_describe_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import describe_endpoint
    mock_client = MagicMock()
    mock_client.describe_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    describe_endpoint(endpoint_type="test-endpoint_type", region_name="us-east-1")
    mock_client.describe_endpoint.assert_called_once()

def test_describe_job_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import describe_job_execution
    mock_client = MagicMock()
    mock_client.describe_job_execution.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    describe_job_execution("test-job_id", "test-thing_name", execution_number="test-execution_number", region_name="us-east-1")
    mock_client.describe_job_execution.assert_called_once()

def test_describe_managed_job_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import describe_managed_job_template
    mock_client = MagicMock()
    mock_client.describe_managed_job_template.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    describe_managed_job_template("test-template_name", template_version="test-template_version", region_name="us-east-1")
    mock_client.describe_managed_job_template.assert_called_once()

def test_disassociate_sbom_from_package_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import disassociate_sbom_from_package_version
    mock_client = MagicMock()
    mock_client.disassociate_sbom_from_package_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    disassociate_sbom_from_package_version("test-package_name", "test-version_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_sbom_from_package_version.assert_called_once()

def test_get_behavior_model_training_summaries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_behavior_model_training_summaries
    mock_client = MagicMock()
    mock_client.get_behavior_model_training_summaries.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_behavior_model_training_summaries(security_profile_name="test-security_profile_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.get_behavior_model_training_summaries.assert_called_once()

def test_get_buckets_aggregation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_buckets_aggregation
    mock_client = MagicMock()
    mock_client.get_buckets_aggregation.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_buckets_aggregation("test-query_string", "test-aggregation_field", "test-buckets_aggregation_type", index_name="test-index_name", query_version="test-query_version", region_name="us-east-1")
    mock_client.get_buckets_aggregation.assert_called_once()

def test_get_cardinality_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_cardinality
    mock_client = MagicMock()
    mock_client.get_cardinality.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_cardinality("test-query_string", index_name="test-index_name", aggregation_field="test-aggregation_field", query_version="test-query_version", region_name="us-east-1")
    mock_client.get_cardinality.assert_called_once()

def test_get_command_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_command_execution
    mock_client = MagicMock()
    mock_client.get_command_execution.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_command_execution("test-execution_id", "test-target_arn", include_result=True, region_name="us-east-1")
    mock_client.get_command_execution.assert_called_once()

def test_get_effective_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_effective_policies
    mock_client = MagicMock()
    mock_client.get_effective_policies.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_effective_policies(principal="test-principal", cognito_identity_pool_id="test-cognito_identity_pool_id", thing_name="test-thing_name", region_name="us-east-1")
    mock_client.get_effective_policies.assert_called_once()

def test_get_job_document_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_job_document
    mock_client = MagicMock()
    mock_client.get_job_document.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_job_document("test-job_id", before_substitution="test-before_substitution", region_name="us-east-1")
    mock_client.get_job_document.assert_called_once()

def test_get_percentiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_percentiles
    mock_client = MagicMock()
    mock_client.get_percentiles.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_percentiles("test-query_string", index_name="test-index_name", aggregation_field="test-aggregation_field", query_version="test-query_version", percents="test-percents", region_name="us-east-1")
    mock_client.get_percentiles.assert_called_once()

def test_get_statistics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import get_statistics
    mock_client = MagicMock()
    mock_client.get_statistics.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    get_statistics("test-query_string", index_name="test-index_name", aggregation_field="test-aggregation_field", query_version="test-query_version", region_name="us-east-1")
    mock_client.get_statistics.assert_called_once()

def test_list_active_violations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_active_violations
    mock_client = MagicMock()
    mock_client.list_active_violations.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_active_violations(thing_name="test-thing_name", security_profile_name="test-security_profile_name", behavior_criteria_type="test-behavior_criteria_type", list_suppressed_alerts="test-list_suppressed_alerts", verification_state="test-verification_state", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_active_violations.assert_called_once()

def test_list_attached_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_attached_policies
    mock_client = MagicMock()
    mock_client.list_attached_policies.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_attached_policies("test-target", recursive=True, marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.list_attached_policies.assert_called_once()

def test_list_audit_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_audit_findings
    mock_client = MagicMock()
    mock_client.list_audit_findings.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_audit_findings(task_id="test-task_id", check_name="test-check_name", resource_identifier="test-resource_identifier", max_results=1, next_token="test-next_token", start_time="test-start_time", end_time="test-end_time", list_suppressed_findings="test-list_suppressed_findings", region_name="us-east-1")
    mock_client.list_audit_findings.assert_called_once()

def test_list_audit_mitigation_actions_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_audit_mitigation_actions_executions
    mock_client = MagicMock()
    mock_client.list_audit_mitigation_actions_executions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_audit_mitigation_actions_executions("test-task_id", "test-finding_id", action_status="test-action_status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_audit_mitigation_actions_executions.assert_called_once()

def test_list_audit_mitigation_actions_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_audit_mitigation_actions_tasks
    mock_client = MagicMock()
    mock_client.list_audit_mitigation_actions_tasks.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_audit_mitigation_actions_tasks("test-start_time", "test-end_time", audit_task_id="test-audit_task_id", finding_id="test-finding_id", task_status="test-task_status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_audit_mitigation_actions_tasks.assert_called_once()

def test_list_audit_suppressions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_audit_suppressions
    mock_client = MagicMock()
    mock_client.list_audit_suppressions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_audit_suppressions(check_name="test-check_name", resource_identifier="test-resource_identifier", ascending_order="test-ascending_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_audit_suppressions.assert_called_once()

def test_list_audit_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_audit_tasks
    mock_client = MagicMock()
    mock_client.list_audit_tasks.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_audit_tasks("test-start_time", "test-end_time", task_type="test-task_type", task_status="test-task_status", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_audit_tasks.assert_called_once()

def test_list_authorizers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_authorizers
    mock_client = MagicMock()
    mock_client.list_authorizers.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_authorizers(page_size=1, marker="test-marker", ascending_order="test-ascending_order", status="test-status", region_name="us-east-1")
    mock_client.list_authorizers.assert_called_once()

def test_list_billing_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_billing_groups
    mock_client = MagicMock()
    mock_client.list_billing_groups.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_billing_groups(next_token="test-next_token", max_results=1, name_prefix_filter=[{}], region_name="us-east-1")
    mock_client.list_billing_groups.assert_called_once()

def test_list_ca_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_ca_certificates
    mock_client = MagicMock()
    mock_client.list_ca_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_ca_certificates(page_size=1, marker="test-marker", ascending_order="test-ascending_order", template_name="test-template_name", region_name="us-east-1")
    mock_client.list_ca_certificates.assert_called_once()

def test_list_certificate_providers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_certificate_providers
    mock_client = MagicMock()
    mock_client.list_certificate_providers.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_certificate_providers(next_token="test-next_token", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_certificate_providers.assert_called_once()

def test_list_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_certificates
    mock_client = MagicMock()
    mock_client.list_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_certificates(page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_certificates.assert_called_once()

def test_list_certificates_by_ca_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_certificates_by_ca
    mock_client = MagicMock()
    mock_client.list_certificates_by_ca.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_certificates_by_ca("test-ca_certificate_id", page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_certificates_by_ca.assert_called_once()

def test_list_command_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_command_executions
    mock_client = MagicMock()
    mock_client.list_command_executions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_command_executions(max_results=1, next_token="test-next_token", namespace="test-namespace", status="test-status", sort_order="test-sort_order", started_time_filter=[{}], completed_time_filter=[{}], target_arn="test-target_arn", command_arn="test-command_arn", region_name="us-east-1")
    mock_client.list_command_executions.assert_called_once()

def test_list_commands_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_commands
    mock_client = MagicMock()
    mock_client.list_commands.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_commands(max_results=1, next_token="test-next_token", namespace="test-namespace", command_parameter_name="test-command_parameter_name", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.list_commands.assert_called_once()

def test_list_custom_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_custom_metrics
    mock_client = MagicMock()
    mock_client.list_custom_metrics.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_custom_metrics(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_custom_metrics.assert_called_once()

def test_list_detect_mitigation_actions_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_detect_mitigation_actions_executions
    mock_client = MagicMock()
    mock_client.list_detect_mitigation_actions_executions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_detect_mitigation_actions_executions(task_id="test-task_id", violation_id="test-violation_id", thing_name="test-thing_name", start_time="test-start_time", end_time="test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_detect_mitigation_actions_executions.assert_called_once()

def test_list_detect_mitigation_actions_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_detect_mitigation_actions_tasks
    mock_client = MagicMock()
    mock_client.list_detect_mitigation_actions_tasks.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_detect_mitigation_actions_tasks("test-start_time", "test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_detect_mitigation_actions_tasks.assert_called_once()

def test_list_dimensions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_dimensions
    mock_client = MagicMock()
    mock_client.list_dimensions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_dimensions(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_dimensions.assert_called_once()

def test_list_domain_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_domain_configurations
    mock_client = MagicMock()
    mock_client.list_domain_configurations.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_domain_configurations(marker="test-marker", page_size=1, service_type="test-service_type", region_name="us-east-1")
    mock_client.list_domain_configurations.assert_called_once()

def test_list_fleet_metrics_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_fleet_metrics
    mock_client = MagicMock()
    mock_client.list_fleet_metrics.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_fleet_metrics(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_fleet_metrics.assert_called_once()

def test_list_indices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_indices
    mock_client = MagicMock()
    mock_client.list_indices.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_indices(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_indices.assert_called_once()

def test_list_job_executions_for_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_job_executions_for_job
    mock_client = MagicMock()
    mock_client.list_job_executions_for_job.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_job_executions_for_job("test-job_id", status="test-status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_job_executions_for_job.assert_called_once()

def test_list_job_executions_for_thing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_job_executions_for_thing
    mock_client = MagicMock()
    mock_client.list_job_executions_for_thing.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_job_executions_for_thing("test-thing_name", status="test-status", namespace_id="test-namespace_id", max_results=1, next_token="test-next_token", job_id="test-job_id", region_name="us-east-1")
    mock_client.list_job_executions_for_thing.assert_called_once()

def test_list_job_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_job_templates
    mock_client = MagicMock()
    mock_client.list_job_templates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_job_templates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_job_templates.assert_called_once()

def test_list_managed_job_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_managed_job_templates
    mock_client = MagicMock()
    mock_client.list_managed_job_templates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_managed_job_templates(template_name="test-template_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_managed_job_templates.assert_called_once()

def test_list_metric_values_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_metric_values
    mock_client = MagicMock()
    mock_client.list_metric_values.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_metric_values("test-thing_name", "test-metric_name", "test-start_time", "test-end_time", dimension_name="test-dimension_name", dimension_value_operator="test-dimension_value_operator", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_metric_values.assert_called_once()

def test_list_mitigation_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_mitigation_actions
    mock_client = MagicMock()
    mock_client.list_mitigation_actions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_mitigation_actions(action_type="test-action_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_mitigation_actions.assert_called_once()

def test_list_ota_updates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_ota_updates
    mock_client = MagicMock()
    mock_client.list_ota_updates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_ota_updates(max_results=1, next_token="test-next_token", ota_update_status="test-ota_update_status", region_name="us-east-1")
    mock_client.list_ota_updates.assert_called_once()

def test_list_outgoing_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_outgoing_certificates
    mock_client = MagicMock()
    mock_client.list_outgoing_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_outgoing_certificates(page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_outgoing_certificates.assert_called_once()

def test_list_package_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_package_versions
    mock_client = MagicMock()
    mock_client.list_package_versions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_package_versions("test-package_name", status="test-status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_package_versions.assert_called_once()

def test_list_packages_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_packages
    mock_client = MagicMock()
    mock_client.list_packages.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_packages(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_packages.assert_called_once()

def test_list_policy_principals_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_policy_principals
    mock_client = MagicMock()
    mock_client.list_policy_principals.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_policy_principals("test-policy_name", marker="test-marker", page_size=1, ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_policy_principals.assert_called_once()

def test_list_principal_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_principal_policies
    mock_client = MagicMock()
    mock_client.list_principal_policies.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_principal_policies("test-principal", marker="test-marker", page_size=1, ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_principal_policies.assert_called_once()

def test_list_principal_things_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_principal_things
    mock_client = MagicMock()
    mock_client.list_principal_things.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_principal_things("test-principal", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_principal_things.assert_called_once()

def test_list_principal_things_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_principal_things_v2
    mock_client = MagicMock()
    mock_client.list_principal_things_v2.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_principal_things_v2("test-principal", next_token="test-next_token", max_results=1, thing_principal_type="test-thing_principal_type", region_name="us-east-1")
    mock_client.list_principal_things_v2.assert_called_once()

def test_list_provisioning_template_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_provisioning_template_versions
    mock_client = MagicMock()
    mock_client.list_provisioning_template_versions.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_provisioning_template_versions("test-template_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_provisioning_template_versions.assert_called_once()

def test_list_provisioning_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_provisioning_templates
    mock_client = MagicMock()
    mock_client.list_provisioning_templates.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_provisioning_templates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_provisioning_templates.assert_called_once()

def test_list_related_resources_for_audit_finding_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_related_resources_for_audit_finding
    mock_client = MagicMock()
    mock_client.list_related_resources_for_audit_finding.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_related_resources_for_audit_finding("test-finding_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_related_resources_for_audit_finding.assert_called_once()

def test_list_role_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_role_aliases
    mock_client = MagicMock()
    mock_client.list_role_aliases.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_role_aliases(page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_role_aliases.assert_called_once()

def test_list_sbom_validation_results_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_sbom_validation_results
    mock_client = MagicMock()
    mock_client.list_sbom_validation_results.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_sbom_validation_results("test-package_name", "test-version_name", validation_result="test-validation_result", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sbom_validation_results.assert_called_once()

def test_list_scheduled_audits_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_scheduled_audits
    mock_client = MagicMock()
    mock_client.list_scheduled_audits.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_scheduled_audits(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_scheduled_audits.assert_called_once()

def test_list_security_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_security_profiles
    mock_client = MagicMock()
    mock_client.list_security_profiles.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_security_profiles(next_token="test-next_token", max_results=1, dimension_name="test-dimension_name", metric_name="test-metric_name", region_name="us-east-1")
    mock_client.list_security_profiles.assert_called_once()

def test_list_security_profiles_for_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_security_profiles_for_target
    mock_client = MagicMock()
    mock_client.list_security_profiles_for_target.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_security_profiles_for_target("test-security_profile_target_arn", next_token="test-next_token", max_results=1, recursive=True, region_name="us-east-1")
    mock_client.list_security_profiles_for_target.assert_called_once()

def test_list_streams_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_streams
    mock_client = MagicMock()
    mock_client.list_streams.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_streams(max_results=1, next_token="test-next_token", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.list_streams.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_list_targets_for_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_targets_for_policy
    mock_client = MagicMock()
    mock_client.list_targets_for_policy.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_targets_for_policy("test-policy_name", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.list_targets_for_policy.assert_called_once()

def test_list_targets_for_security_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_targets_for_security_profile
    mock_client = MagicMock()
    mock_client.list_targets_for_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_targets_for_security_profile("test-security_profile_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_targets_for_security_profile.assert_called_once()

def test_list_thing_groups_for_thing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_thing_groups_for_thing
    mock_client = MagicMock()
    mock_client.list_thing_groups_for_thing.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_thing_groups_for_thing("test-thing_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_thing_groups_for_thing.assert_called_once()

def test_list_thing_principals_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_thing_principals
    mock_client = MagicMock()
    mock_client.list_thing_principals.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_thing_principals("test-thing_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_thing_principals.assert_called_once()

def test_list_thing_principals_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_thing_principals_v2
    mock_client = MagicMock()
    mock_client.list_thing_principals_v2.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_thing_principals_v2("test-thing_name", next_token="test-next_token", max_results=1, thing_principal_type="test-thing_principal_type", region_name="us-east-1")
    mock_client.list_thing_principals_v2.assert_called_once()

def test_list_thing_registration_task_reports_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_thing_registration_task_reports
    mock_client = MagicMock()
    mock_client.list_thing_registration_task_reports.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_thing_registration_task_reports("test-task_id", 1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_thing_registration_task_reports.assert_called_once()

def test_list_thing_registration_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_thing_registration_tasks
    mock_client = MagicMock()
    mock_client.list_thing_registration_tasks.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_thing_registration_tasks(next_token="test-next_token", max_results=1, status="test-status", region_name="us-east-1")
    mock_client.list_thing_registration_tasks.assert_called_once()

def test_list_things_in_billing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_things_in_billing_group
    mock_client = MagicMock()
    mock_client.list_things_in_billing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_things_in_billing_group("test-billing_group_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_things_in_billing_group.assert_called_once()

def test_list_things_in_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_things_in_thing_group
    mock_client = MagicMock()
    mock_client.list_things_in_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_things_in_thing_group("test-thing_group_name", recursive=True, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_things_in_thing_group.assert_called_once()

def test_list_topic_rule_destinations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_topic_rule_destinations
    mock_client = MagicMock()
    mock_client.list_topic_rule_destinations.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_topic_rule_destinations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_topic_rule_destinations.assert_called_once()

def test_list_v2_logging_levels_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_v2_logging_levels
    mock_client = MagicMock()
    mock_client.list_v2_logging_levels.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_v2_logging_levels(target_type="test-target_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_v2_logging_levels.assert_called_once()

def test_list_violation_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import list_violation_events
    mock_client = MagicMock()
    mock_client.list_violation_events.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    list_violation_events("test-start_time", "test-end_time", thing_name="test-thing_name", security_profile_name="test-security_profile_name", behavior_criteria_type="test-behavior_criteria_type", list_suppressed_alerts="test-list_suppressed_alerts", verification_state="test-verification_state", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_violation_events.assert_called_once()

def test_put_verification_state_on_violation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import put_verification_state_on_violation
    mock_client = MagicMock()
    mock_client.put_verification_state_on_violation.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    put_verification_state_on_violation("test-violation_id", "test-verification_state", verification_state_description="test-verification_state_description", region_name="us-east-1")
    mock_client.put_verification_state_on_violation.assert_called_once()

def test_register_ca_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import register_ca_certificate
    mock_client = MagicMock()
    mock_client.register_ca_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    register_ca_certificate("test-ca_certificate", verification_certificate="test-verification_certificate", set_as_active="test-set_as_active", allow_auto_registration=True, registration_config={}, tags=[{"Key": "k", "Value": "v"}], certificate_mode="test-certificate_mode", region_name="us-east-1")
    mock_client.register_ca_certificate.assert_called_once()

def test_register_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import register_certificate
    mock_client = MagicMock()
    mock_client.register_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    register_certificate("test-certificate_pem", ca_certificate_pem="test-ca_certificate_pem", set_as_active="test-set_as_active", status="test-status", region_name="us-east-1")
    mock_client.register_certificate.assert_called_once()

def test_register_certificate_without_ca_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import register_certificate_without_ca
    mock_client = MagicMock()
    mock_client.register_certificate_without_ca.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    register_certificate_without_ca("test-certificate_pem", status="test-status", region_name="us-east-1")
    mock_client.register_certificate_without_ca.assert_called_once()

def test_register_thing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import register_thing
    mock_client = MagicMock()
    mock_client.register_thing.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    register_thing("test-template_body", parameters="test-parameters", region_name="us-east-1")
    mock_client.register_thing.assert_called_once()

def test_reject_certificate_transfer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import reject_certificate_transfer
    mock_client = MagicMock()
    mock_client.reject_certificate_transfer.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    reject_certificate_transfer("test-certificate_id", reject_reason="test-reject_reason", region_name="us-east-1")
    mock_client.reject_certificate_transfer.assert_called_once()

def test_remove_thing_from_billing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import remove_thing_from_billing_group
    mock_client = MagicMock()
    mock_client.remove_thing_from_billing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    remove_thing_from_billing_group(billing_group_name="test-billing_group_name", billing_group_arn="test-billing_group_arn", thing_name="test-thing_name", thing_arn="test-thing_arn", region_name="us-east-1")
    mock_client.remove_thing_from_billing_group.assert_called_once()

def test_remove_thing_from_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import remove_thing_from_thing_group
    mock_client = MagicMock()
    mock_client.remove_thing_from_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    remove_thing_from_thing_group(thing_group_name="test-thing_group_name", thing_group_arn="test-thing_group_arn", thing_name="test-thing_name", thing_arn="test-thing_arn", region_name="us-east-1")
    mock_client.remove_thing_from_thing_group.assert_called_once()

def test_run_authorization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import run_authorization
    mock_client = MagicMock()
    mock_client.test_authorization.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    run_authorization("test-auth_infos", principal="test-principal", cognito_identity_pool_id="test-cognito_identity_pool_id", client_id="test-client_id", policy_names_to_add="test-policy_names_to_add", policy_names_to_skip="test-policy_names_to_skip", region_name="us-east-1")
    mock_client.test_authorization.assert_called_once()

def test_run_invoke_authorizer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import run_invoke_authorizer
    mock_client = MagicMock()
    mock_client.test_invoke_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    run_invoke_authorizer("test-authorizer_name", token="test-token", token_signature="test-token_signature", http_context={}, mqtt_context={}, tls_context={}, region_name="us-east-1")
    mock_client.test_invoke_authorizer.assert_called_once()

def test_search_index_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import search_index
    mock_client = MagicMock()
    mock_client.search_index.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    search_index("test-query_string", index_name="test-index_name", next_token="test-next_token", max_results=1, query_version="test-query_version", region_name="us-east-1")
    mock_client.search_index.assert_called_once()

def test_set_v2_logging_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import set_v2_logging_options
    mock_client = MagicMock()
    mock_client.set_v2_logging_options.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    set_v2_logging_options(role_arn="test-role_arn", default_log_level="test-default_log_level", disable_all_logs=True, region_name="us-east-1")
    mock_client.set_v2_logging_options.assert_called_once()

def test_start_detect_mitigation_actions_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import start_detect_mitigation_actions_task
    mock_client = MagicMock()
    mock_client.start_detect_mitigation_actions_task.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    start_detect_mitigation_actions_task("test-task_id", "test-target", "test-actions", "test-client_request_token", violation_event_occurrence_range="test-violation_event_occurrence_range", include_only_active_violations=True, include_suppressed_alerts=True, region_name="us-east-1")
    mock_client.start_detect_mitigation_actions_task.assert_called_once()

def test_transfer_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import transfer_certificate
    mock_client = MagicMock()
    mock_client.transfer_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    transfer_certificate("test-certificate_id", 1, transfer_message="test-transfer_message", region_name="us-east-1")
    mock_client.transfer_certificate.assert_called_once()

def test_update_account_audit_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_account_audit_configuration
    mock_client = MagicMock()
    mock_client.update_account_audit_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_account_audit_configuration(role_arn="test-role_arn", audit_notification_target_configurations={}, audit_check_configurations={}, region_name="us-east-1")
    mock_client.update_account_audit_configuration.assert_called_once()

def test_update_audit_suppression_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_audit_suppression
    mock_client = MagicMock()
    mock_client.update_audit_suppression.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_audit_suppression("test-check_name", "test-resource_identifier", expiration_date="test-expiration_date", suppress_indefinitely="test-suppress_indefinitely", description="test-description", region_name="us-east-1")
    mock_client.update_audit_suppression.assert_called_once()

def test_update_authorizer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_authorizer
    mock_client = MagicMock()
    mock_client.update_authorizer.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_authorizer("test-authorizer_name", authorizer_function_arn="test-authorizer_function_arn", token_key_name="test-token_key_name", token_signing_public_keys="test-token_signing_public_keys", status="test-status", enable_caching_for_http=True, region_name="us-east-1")
    mock_client.update_authorizer.assert_called_once()

def test_update_billing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_billing_group
    mock_client = MagicMock()
    mock_client.update_billing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_billing_group("test-billing_group_name", {}, expected_version="test-expected_version", region_name="us-east-1")
    mock_client.update_billing_group.assert_called_once()

def test_update_ca_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_ca_certificate
    mock_client = MagicMock()
    mock_client.update_ca_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_ca_certificate("test-certificate_id", new_status="test-new_status", new_auto_registration_status="test-new_auto_registration_status", registration_config={}, remove_auto_registration="test-remove_auto_registration", region_name="us-east-1")
    mock_client.update_ca_certificate.assert_called_once()

def test_update_certificate_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_certificate_provider
    mock_client = MagicMock()
    mock_client.update_certificate_provider.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_certificate_provider("test-certificate_provider_name", lambda_function_arn="test-lambda_function_arn", account_default_for_operations=1, region_name="us-east-1")
    mock_client.update_certificate_provider.assert_called_once()

def test_update_command_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_command
    mock_client = MagicMock()
    mock_client.update_command.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_command("test-command_id", display_name="test-display_name", description="test-description", deprecated="test-deprecated", region_name="us-east-1")
    mock_client.update_command.assert_called_once()

def test_update_domain_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_domain_configuration
    mock_client = MagicMock()
    mock_client.update_domain_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_domain_configuration({}, authorizer_config={}, domain_configuration_status={}, remove_authorizer_config={}, tls_config={}, server_certificate_config={}, authentication_type="test-authentication_type", application_protocol="test-application_protocol", client_certificate_config={}, region_name="us-east-1")
    mock_client.update_domain_configuration.assert_called_once()

def test_update_dynamic_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_dynamic_thing_group
    mock_client = MagicMock()
    mock_client.update_dynamic_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_dynamic_thing_group("test-thing_group_name", {}, expected_version="test-expected_version", index_name="test-index_name", query_string="test-query_string", query_version="test-query_version", region_name="us-east-1")
    mock_client.update_dynamic_thing_group.assert_called_once()

def test_update_encryption_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_encryption_configuration
    mock_client = MagicMock()
    mock_client.update_encryption_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_encryption_configuration("test-encryption_type", kms_key_arn="test-kms_key_arn", kms_access_role_arn="test-kms_access_role_arn", region_name="us-east-1")
    mock_client.update_encryption_configuration.assert_called_once()

def test_update_event_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_event_configurations
    mock_client = MagicMock()
    mock_client.update_event_configurations.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_event_configurations(event_configurations={}, region_name="us-east-1")
    mock_client.update_event_configurations.assert_called_once()

def test_update_fleet_metric_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_fleet_metric
    mock_client = MagicMock()
    mock_client.update_fleet_metric.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_fleet_metric("test-metric_name", "test-index_name", query_string="test-query_string", aggregation_type="test-aggregation_type", period="test-period", aggregation_field="test-aggregation_field", description="test-description", query_version="test-query_version", unit="test-unit", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.update_fleet_metric.assert_called_once()

def test_update_indexing_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_indexing_configuration
    mock_client = MagicMock()
    mock_client.update_indexing_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_indexing_configuration(thing_indexing_configuration={}, thing_group_indexing_configuration={}, region_name="us-east-1")
    mock_client.update_indexing_configuration.assert_called_once()

def test_update_job_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_job
    mock_client = MagicMock()
    mock_client.update_job.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_job("test-job_id", description="test-description", presigned_url_config={}, job_executions_rollout_config={}, abort_config={}, timeout_config=1, namespace_id="test-namespace_id", job_executions_retry_config={}, region_name="us-east-1")
    mock_client.update_job.assert_called_once()

def test_update_mitigation_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_mitigation_action
    mock_client = MagicMock()
    mock_client.update_mitigation_action.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_mitigation_action("test-action_name", role_arn="test-role_arn", action_params="test-action_params", region_name="us-east-1")
    mock_client.update_mitigation_action.assert_called_once()

def test_update_package_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_package
    mock_client = MagicMock()
    mock_client.update_package.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_package("test-package_name", description="test-description", default_version_name="test-default_version_name", unset_default_version="test-unset_default_version", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_package.assert_called_once()

def test_update_package_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_package_configuration
    mock_client = MagicMock()
    mock_client.update_package_configuration.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_package_configuration(version_update_by_jobs_config={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.update_package_configuration.assert_called_once()

def test_update_package_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_package_version
    mock_client = MagicMock()
    mock_client.update_package_version.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_package_version("test-package_name", "test-version_name", description="test-description", attributes="test-attributes", artifact="test-artifact", action="test-action", recipe="test-recipe", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_package_version.assert_called_once()

def test_update_provisioning_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_provisioning_template
    mock_client = MagicMock()
    mock_client.update_provisioning_template.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_provisioning_template("test-template_name", description="test-description", enabled=True, default_version_id="test-default_version_id", provisioning_role_arn="test-provisioning_role_arn", pre_provisioning_hook="test-pre_provisioning_hook", remove_pre_provisioning_hook="test-remove_pre_provisioning_hook", region_name="us-east-1")
    mock_client.update_provisioning_template.assert_called_once()

def test_update_role_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_role_alias
    mock_client = MagicMock()
    mock_client.update_role_alias.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_role_alias("test-role_alias", role_arn="test-role_arn", credential_duration_seconds=1, region_name="us-east-1")
    mock_client.update_role_alias.assert_called_once()

def test_update_scheduled_audit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_scheduled_audit
    mock_client = MagicMock()
    mock_client.update_scheduled_audit.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_scheduled_audit("test-scheduled_audit_name", frequency="test-frequency", day_of_month="test-day_of_month", day_of_week="test-day_of_week", target_check_names="test-target_check_names", region_name="us-east-1")
    mock_client.update_scheduled_audit.assert_called_once()

def test_update_security_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_security_profile
    mock_client = MagicMock()
    mock_client.update_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_security_profile("test-security_profile_name", security_profile_description="test-security_profile_description", behaviors="test-behaviors", alert_targets="test-alert_targets", additional_metrics_to_retain="test-additional_metrics_to_retain", additional_metrics_to_retain_v2="test-additional_metrics_to_retain_v2", delete_behaviors=True, delete_alert_targets=True, delete_additional_metrics_to_retain=True, expected_version="test-expected_version", metrics_export_config=1, delete_metrics_export_config=True, region_name="us-east-1")
    mock_client.update_security_profile.assert_called_once()

def test_update_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_stream
    mock_client = MagicMock()
    mock_client.update_stream.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_stream("test-stream_id", description="test-description", files="test-files", role_arn="test-role_arn", region_name="us-east-1")
    mock_client.update_stream.assert_called_once()

def test_update_thing_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_thing_group
    mock_client = MagicMock()
    mock_client.update_thing_group.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_thing_group("test-thing_group_name", {}, expected_version="test-expected_version", region_name="us-east-1")
    mock_client.update_thing_group.assert_called_once()

def test_update_thing_groups_for_thing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_thing_groups_for_thing
    mock_client = MagicMock()
    mock_client.update_thing_groups_for_thing.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_thing_groups_for_thing(thing_name="test-thing_name", thing_groups_to_add="test-thing_groups_to_add", thing_groups_to_remove="test-thing_groups_to_remove", override_dynamic_groups="test-override_dynamic_groups", region_name="us-east-1")
    mock_client.update_thing_groups_for_thing.assert_called_once()

def test_update_thing_type_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iot import update_thing_type
    mock_client = MagicMock()
    mock_client.update_thing_type.return_value = {}
    monkeypatch.setattr("aws_util.iot.get_client", lambda *a, **kw: mock_client)
    update_thing_type("test-thing_type_name", thing_type_properties={}, region_name="us-east-1")
    mock_client.update_thing_type.assert_called_once()
