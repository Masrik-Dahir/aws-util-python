"""Tests for aws_util.aio.iot -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.iot import (
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
from aws_util.exceptions import AwsServiceError

R = "us-east-1"


def _mf(mc):
    return lambda *a, **kw: mc


# -- Thing --

async def test_create_thing(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingName": "t1", "thingArn": "arn"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await create_thing("t1", region_name=R); assert isinstance(r, IoTThing)

async def test_create_thing_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingName": "t1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await create_thing("t1", thing_type_name="tt", attributes={"k": "v"}, region_name=R)
    assert r.thing_type_name == "tt"

async def test_create_thing_runtime_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_thing("t1", region_name=R)

async def test_create_thing_generic_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_thing("t1", region_name=R)

async def test_describe_thing(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingName": "t1", "thingArn": "arn", "thingTypeName": "tt", "attributes": {}, "version": 2}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await describe_thing("t1", region_name=R); assert r.version == 2

async def test_describe_thing_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await describe_thing("t1", region_name=R)

async def test_list_things(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = [{"thingName": "t1"}]
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await list_things(region_name=R); assert len(r) == 1

async def test_list_things_err(monkeypatch):
    mc = AsyncMock(); mc.paginate.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_things(region_name=R)

async def test_delete_thing(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await delete_thing("t1", region_name=R)

async def test_delete_thing_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await delete_thing("t1", region_name=R)

async def test_update_thing(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await update_thing("t1", region_name=R)

async def test_update_thing_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await update_thing("t1", thing_type_name="tt", attributes={"k": "v"}, remove_thing_type=True, region_name=R)

async def test_update_thing_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await update_thing("t1", region_name=R)

# -- Thing type --

async def test_create_thing_type(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingTypeName": "tt1", "thingTypeArn": "arn"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await create_thing_type("tt1", region_name=R); assert isinstance(r, IoTThingType)

async def test_create_thing_type_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingTypeName": "tt1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_thing_type("tt1", searchable_attributes=["a"], description="d", region_name=R)

async def test_create_thing_type_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_thing_type("tt1", region_name=R)

async def test_list_thing_types(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = [{"thingTypeName": "tt1"}]
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await list_thing_types(region_name=R); assert len(r) == 1

async def test_list_thing_types_err(monkeypatch):
    mc = AsyncMock(); mc.paginate.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_thing_types(region_name=R)

# -- Thing group --

async def test_create_thing_group(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingGroupName": "g1", "thingGroupArn": "arn"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await create_thing_group("g1", region_name=R); assert isinstance(r, IoTThingGroup)

async def test_create_thing_group_parent(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"thingGroupName": "g1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_thing_group("g1", parent_group_name="parent", region_name=R)

async def test_create_thing_group_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_thing_group("g1", region_name=R)

async def test_list_thing_groups(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = [{"groupName": "g1", "groupArn": "arn"}]
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await list_thing_groups(region_name=R); assert len(r) == 1

async def test_list_thing_groups_err(monkeypatch):
    mc = AsyncMock(); mc.paginate.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_thing_groups(region_name=R)

async def test_add_thing_to_group(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await add_thing_to_thing_group("t1", "g1", region_name=R)

async def test_add_thing_to_group_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await add_thing_to_thing_group("t1", "g1", region_name=R)

# -- Policy --

async def test_create_policy_str(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"policyName": "p1", "policyArn": "arn", "policyDocument": "{}", "policyVersionId": "1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await create_policy("p1", "{}", region_name=R); assert isinstance(r, IoTPolicy)

async def test_create_policy_dict(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"policyName": "p1", "policyArn": "arn", "policyDocument": "{}", "policyVersionId": "1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_policy("p1", {"Version": "2012-10-17"}, region_name=R)

async def test_create_policy_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_policy("p1", "{}", region_name=R)

async def test_get_policy(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"policyName": "p1", "policyArn": "arn", "policyDocument": "{}", "defaultVersionId": "1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    assert (await get_policy("p1", region_name=R)).policy_name == "p1"

async def test_get_policy_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await get_policy("p1", region_name=R)

async def test_list_policies(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = [{"policyName": "p1", "policyArn": "arn"}]
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    assert len(await list_policies(region_name=R)) == 1

async def test_list_policies_err(monkeypatch):
    mc = AsyncMock(); mc.paginate.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_policies(region_name=R)

async def test_delete_policy(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await delete_policy("p1", region_name=R)

async def test_delete_policy_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await delete_policy("p1", region_name=R)

async def test_attach_policy(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await attach_policy("p1", "arn:target", region_name=R)

async def test_attach_policy_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await attach_policy("p1", "arn:target", region_name=R)

async def test_detach_policy(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await detach_policy("p1", "arn:target", region_name=R)

async def test_detach_policy_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await detach_policy("p1", "arn:target", region_name=R)

# -- Topic rule --

async def test_create_topic_rule(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_topic_rule("r1", "SELECT *", [{}], region_name=R)

async def test_create_topic_rule_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_topic_rule("r1", "SELECT *", [], region_name=R)

async def test_get_topic_rule(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ruleArn": "arn", "rule": {"ruleName": "r1", "sql": "SELECT *", "description": "d", "ruleDisabled": False}}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await get_topic_rule("r1", region_name=R); assert isinstance(r, IoTTopicRule)

async def test_get_topic_rule_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await get_topic_rule("r1", region_name=R)

async def test_list_topic_rules(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = [{"ruleName": "r1", "ruleArn": "arn"}]
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    assert len(await list_topic_rules(region_name=R)) == 1

async def test_list_topic_rules_err(monkeypatch):
    mc = AsyncMock(); mc.paginate.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_topic_rules(region_name=R)

async def test_delete_topic_rule(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await delete_topic_rule("r1", region_name=R)

async def test_delete_topic_rule_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await delete_topic_rule("r1", region_name=R)

# -- Job --

async def test_create_job(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"jobId": "j1", "jobArn": "arn"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await create_job("j1", ["arn:t"], region_name=R); assert isinstance(r, IoTJob)

async def test_create_job_doc_source(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"jobId": "j1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_job("j1", ["arn:t"], document_source="s3://b/d", region_name=R)

async def test_create_job_doc_str(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"jobId": "j1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_job("j1", ["arn:t"], document='{"k":"v"}', region_name=R)

async def test_create_job_doc_dict(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"jobId": "j1"}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await create_job("j1", ["arn:t"], document={"k": "v"}, region_name=R)

async def test_create_job_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await create_job("j1", ["arn:t"], region_name=R)

async def test_describe_job(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"job": {"jobId": "j1", "status": "IN_PROGRESS"}}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    r = await describe_job("j1", region_name=R); assert r.status == "IN_PROGRESS"

async def test_describe_job_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await describe_job("j1", region_name=R)

async def test_list_jobs(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = [{"jobId": "j1"}]
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    assert len(await list_jobs(region_name=R)) == 1

async def test_list_jobs_status(monkeypatch):
    mc = AsyncMock(); mc.paginate.return_value = []
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await list_jobs(status="IN_PROGRESS", region_name=R)

async def test_list_jobs_err(monkeypatch):
    mc = AsyncMock(); mc.paginate.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await list_jobs(region_name=R)

async def test_cancel_job(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await cancel_job("j1", region_name=R)

async def test_cancel_job_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    await cancel_job("j1", reason_code="TIMEOUT", comment="timed out", region_name=R)

async def test_cancel_job_err(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = Exception("boom")
    monkeypatch.setattr("aws_util.aio.iot.async_client", _mf(mc))
    with pytest.raises(AwsServiceError): await cancel_job("j1", region_name=R)


async def test_accept_certificate_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await accept_certificate_transfer("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_accept_certificate_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await accept_certificate_transfer("test-certificate_id", )


async def test_add_thing_to_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_thing_to_billing_group()
    mock_client.call.assert_called_once()


async def test_add_thing_to_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_thing_to_billing_group()


async def test_associate_sbom_with_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_sbom_with_package_version("test-package_name", "test-version_name", {}, )
    mock_client.call.assert_called_once()


async def test_associate_sbom_with_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_sbom_with_package_version("test-package_name", "test-version_name", {}, )


async def test_associate_targets_with_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_targets_with_job([], "test-job_id", )
    mock_client.call.assert_called_once()


async def test_associate_targets_with_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_targets_with_job([], "test-job_id", )


async def test_attach_principal_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_principal_policy("test-policy_name", "test-principal", )
    mock_client.call.assert_called_once()


async def test_attach_principal_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_principal_policy("test-policy_name", "test-principal", )


async def test_attach_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_security_profile("test-security_profile_name", "test-security_profile_target_arn", )
    mock_client.call.assert_called_once()


async def test_attach_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_security_profile("test-security_profile_name", "test-security_profile_target_arn", )


async def test_attach_thing_principal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_thing_principal("test-thing_name", "test-principal", )
    mock_client.call.assert_called_once()


async def test_attach_thing_principal_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_thing_principal("test-thing_name", "test-principal", )


async def test_cancel_audit_mitigation_actions_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_audit_mitigation_actions_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_cancel_audit_mitigation_actions_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_audit_mitigation_actions_task("test-task_id", )


async def test_cancel_audit_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_audit_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_cancel_audit_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_audit_task("test-task_id", )


async def test_cancel_certificate_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_certificate_transfer("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_cancel_certificate_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_certificate_transfer("test-certificate_id", )


async def test_cancel_detect_mitigation_actions_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_detect_mitigation_actions_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_cancel_detect_mitigation_actions_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_detect_mitigation_actions_task("test-task_id", )


async def test_cancel_job_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_job_execution("test-job_id", "test-thing_name", )
    mock_client.call.assert_called_once()


async def test_cancel_job_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_job_execution("test-job_id", "test-thing_name", )


async def test_clear_default_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await clear_default_authorizer()
    mock_client.call.assert_called_once()


async def test_clear_default_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await clear_default_authorizer()


async def test_confirm_topic_rule_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await confirm_topic_rule_destination("test-confirmation_token", )
    mock_client.call.assert_called_once()


async def test_confirm_topic_rule_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await confirm_topic_rule_destination("test-confirmation_token", )


async def test_create_audit_suppression(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_audit_suppression("test-check_name", {}, "test-client_request_token", )
    mock_client.call.assert_called_once()


async def test_create_audit_suppression_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_audit_suppression("test-check_name", {}, "test-client_request_token", )


async def test_create_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_authorizer("test-authorizer_name", "test-authorizer_function_arn", )
    mock_client.call.assert_called_once()


async def test_create_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_authorizer("test-authorizer_name", "test-authorizer_function_arn", )


async def test_create_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_billing_group("test-billing_group_name", )
    mock_client.call.assert_called_once()


async def test_create_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_billing_group("test-billing_group_name", )


async def test_create_certificate_from_csr(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_certificate_from_csr("test-certificate_signing_request", )
    mock_client.call.assert_called_once()


async def test_create_certificate_from_csr_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_certificate_from_csr("test-certificate_signing_request", )


async def test_create_certificate_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_certificate_provider("test-certificate_provider_name", "test-lambda_function_arn", [], )
    mock_client.call.assert_called_once()


async def test_create_certificate_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_certificate_provider("test-certificate_provider_name", "test-lambda_function_arn", [], )


async def test_create_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_command("test-command_id", )
    mock_client.call.assert_called_once()


async def test_create_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_command("test-command_id", )


async def test_create_custom_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_metric("test-metric_name", "test-metric_type", "test-client_request_token", )
    mock_client.call.assert_called_once()


async def test_create_custom_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_metric("test-metric_name", "test-metric_type", "test-client_request_token", )


async def test_create_dimension(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dimension("test-name", "test-type_value", [], "test-client_request_token", )
    mock_client.call.assert_called_once()


async def test_create_dimension_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dimension("test-name", "test-type_value", [], "test-client_request_token", )


async def test_create_domain_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_domain_configuration("test-domain_configuration_name", )
    mock_client.call.assert_called_once()


async def test_create_domain_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_domain_configuration("test-domain_configuration_name", )


async def test_create_dynamic_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_dynamic_thing_group("test-thing_group_name", "test-query_string", )
    mock_client.call.assert_called_once()


async def test_create_dynamic_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_dynamic_thing_group("test-thing_group_name", "test-query_string", )


async def test_create_fleet_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_fleet_metric("test-metric_name", "test-query_string", {}, 1, "test-aggregation_field", )
    mock_client.call.assert_called_once()


async def test_create_fleet_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_fleet_metric("test-metric_name", "test-query_string", {}, 1, "test-aggregation_field", )


async def test_create_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_job_template("test-job_template_id", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_job_template("test-job_template_id", "test-description", )


async def test_create_keys_and_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_keys_and_certificate()
    mock_client.call.assert_called_once()


async def test_create_keys_and_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_keys_and_certificate()


async def test_create_mitigation_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_mitigation_action("test-action_name", "test-role_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_mitigation_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_mitigation_action("test-action_name", "test-role_arn", {}, )


async def test_create_ota_update(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_ota_update("test-ota_update_id", [], [], "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_ota_update_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_ota_update("test-ota_update_id", [], [], "test-role_arn", )


async def test_create_package(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_package("test-package_name", )
    mock_client.call.assert_called_once()


async def test_create_package_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_package("test-package_name", )


async def test_create_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_package_version("test-package_name", "test-version_name", )
    mock_client.call.assert_called_once()


async def test_create_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_package_version("test-package_name", "test-version_name", )


async def test_create_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_policy_version("test-policy_name", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_create_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_policy_version("test-policy_name", "test-policy_document", )


async def test_create_provisioning_claim(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_provisioning_claim("test-template_name", )
    mock_client.call.assert_called_once()


async def test_create_provisioning_claim_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_provisioning_claim("test-template_name", )


async def test_create_provisioning_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_provisioning_template("test-template_name", "test-template_body", "test-provisioning_role_arn", )
    mock_client.call.assert_called_once()


async def test_create_provisioning_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_provisioning_template("test-template_name", "test-template_body", "test-provisioning_role_arn", )


async def test_create_provisioning_template_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_provisioning_template_version("test-template_name", "test-template_body", )
    mock_client.call.assert_called_once()


async def test_create_provisioning_template_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_provisioning_template_version("test-template_name", "test-template_body", )


async def test_create_role_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_role_alias("test-role_alias", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_role_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_role_alias("test-role_alias", "test-role_arn", )


async def test_create_scheduled_audit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_scheduled_audit("test-frequency", [], "test-scheduled_audit_name", )
    mock_client.call.assert_called_once()


async def test_create_scheduled_audit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_scheduled_audit("test-frequency", [], "test-scheduled_audit_name", )


async def test_create_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_security_profile("test-security_profile_name", )
    mock_client.call.assert_called_once()


async def test_create_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_security_profile("test-security_profile_name", )


async def test_create_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_stream("test-stream_id", [], "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_stream("test-stream_id", [], "test-role_arn", )


async def test_create_topic_rule_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_topic_rule_destination({}, )
    mock_client.call.assert_called_once()


async def test_create_topic_rule_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_topic_rule_destination({}, )


async def test_delete_account_audit_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_audit_configuration()
    mock_client.call.assert_called_once()


async def test_delete_account_audit_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_audit_configuration()


async def test_delete_audit_suppression(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_audit_suppression("test-check_name", {}, )
    mock_client.call.assert_called_once()


async def test_delete_audit_suppression_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_audit_suppression("test-check_name", {}, )


async def test_delete_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_authorizer("test-authorizer_name", )
    mock_client.call.assert_called_once()


async def test_delete_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_authorizer("test-authorizer_name", )


async def test_delete_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_billing_group("test-billing_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_billing_group("test-billing_group_name", )


async def test_delete_ca_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ca_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_delete_ca_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ca_certificate("test-certificate_id", )


async def test_delete_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_delete_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_certificate("test-certificate_id", )


async def test_delete_certificate_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_certificate_provider("test-certificate_provider_name", )
    mock_client.call.assert_called_once()


async def test_delete_certificate_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_certificate_provider("test-certificate_provider_name", )


async def test_delete_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_command("test-command_id", )
    mock_client.call.assert_called_once()


async def test_delete_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_command("test-command_id", )


async def test_delete_command_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_command_execution("test-execution_id", "test-target_arn", )
    mock_client.call.assert_called_once()


async def test_delete_command_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_command_execution("test-execution_id", "test-target_arn", )


async def test_delete_custom_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_metric("test-metric_name", )
    mock_client.call.assert_called_once()


async def test_delete_custom_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_metric("test-metric_name", )


async def test_delete_dimension(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dimension("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_dimension_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dimension("test-name", )


async def test_delete_domain_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_domain_configuration("test-domain_configuration_name", )
    mock_client.call.assert_called_once()


async def test_delete_domain_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_domain_configuration("test-domain_configuration_name", )


async def test_delete_dynamic_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_dynamic_thing_group("test-thing_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_dynamic_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_dynamic_thing_group("test-thing_group_name", )


async def test_delete_fleet_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_fleet_metric("test-metric_name", )
    mock_client.call.assert_called_once()


async def test_delete_fleet_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_fleet_metric("test-metric_name", )


async def test_delete_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_delete_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_job("test-job_id", )


async def test_delete_job_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_job_execution("test-job_id", "test-thing_name", 1, )
    mock_client.call.assert_called_once()


async def test_delete_job_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_job_execution("test-job_id", "test-thing_name", 1, )


async def test_delete_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_job_template("test-job_template_id", )
    mock_client.call.assert_called_once()


async def test_delete_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_job_template("test-job_template_id", )


async def test_delete_mitigation_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_mitigation_action("test-action_name", )
    mock_client.call.assert_called_once()


async def test_delete_mitigation_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_mitigation_action("test-action_name", )


async def test_delete_ota_update(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ota_update("test-ota_update_id", )
    mock_client.call.assert_called_once()


async def test_delete_ota_update_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ota_update("test-ota_update_id", )


async def test_delete_package(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_package("test-package_name", )
    mock_client.call.assert_called_once()


async def test_delete_package_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_package("test-package_name", )


async def test_delete_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_package_version("test-package_name", "test-version_name", )
    mock_client.call.assert_called_once()


async def test_delete_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_package_version("test-package_name", "test-version_name", )


async def test_delete_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_policy_version("test-policy_name", "test-policy_version_id", )
    mock_client.call.assert_called_once()


async def test_delete_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_policy_version("test-policy_name", "test-policy_version_id", )


async def test_delete_provisioning_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_provisioning_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_delete_provisioning_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_provisioning_template("test-template_name", )


async def test_delete_provisioning_template_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_provisioning_template_version("test-template_name", 1, )
    mock_client.call.assert_called_once()


async def test_delete_provisioning_template_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_provisioning_template_version("test-template_name", 1, )


async def test_delete_registration_code(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_registration_code()
    mock_client.call.assert_called_once()


async def test_delete_registration_code_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_registration_code()


async def test_delete_role_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_role_alias("test-role_alias", )
    mock_client.call.assert_called_once()


async def test_delete_role_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_role_alias("test-role_alias", )


async def test_delete_scheduled_audit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_scheduled_audit("test-scheduled_audit_name", )
    mock_client.call.assert_called_once()


async def test_delete_scheduled_audit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_scheduled_audit("test-scheduled_audit_name", )


async def test_delete_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_security_profile("test-security_profile_name", )
    mock_client.call.assert_called_once()


async def test_delete_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_security_profile("test-security_profile_name", )


async def test_delete_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_stream("test-stream_id", )
    mock_client.call.assert_called_once()


async def test_delete_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_stream("test-stream_id", )


async def test_delete_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_thing_group("test-thing_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_thing_group("test-thing_group_name", )


async def test_delete_thing_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_thing_type("test-thing_type_name", )
    mock_client.call.assert_called_once()


async def test_delete_thing_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_thing_type("test-thing_type_name", )


async def test_delete_topic_rule_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_topic_rule_destination("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_topic_rule_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_topic_rule_destination("test-arn", )


async def test_delete_v2_logging_level(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_v2_logging_level("test-target_type", "test-target_name", )
    mock_client.call.assert_called_once()


async def test_delete_v2_logging_level_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_v2_logging_level("test-target_type", "test-target_name", )


async def test_deprecate_thing_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await deprecate_thing_type("test-thing_type_name", )
    mock_client.call.assert_called_once()


async def test_deprecate_thing_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deprecate_thing_type("test-thing_type_name", )


async def test_describe_account_audit_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_audit_configuration()
    mock_client.call.assert_called_once()


async def test_describe_account_audit_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_audit_configuration()


async def test_describe_audit_finding(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_audit_finding("test-finding_id", )
    mock_client.call.assert_called_once()


async def test_describe_audit_finding_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_audit_finding("test-finding_id", )


async def test_describe_audit_mitigation_actions_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_audit_mitigation_actions_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_describe_audit_mitigation_actions_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_audit_mitigation_actions_task("test-task_id", )


async def test_describe_audit_suppression(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_audit_suppression("test-check_name", {}, )
    mock_client.call.assert_called_once()


async def test_describe_audit_suppression_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_audit_suppression("test-check_name", {}, )


async def test_describe_audit_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_audit_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_describe_audit_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_audit_task("test-task_id", )


async def test_describe_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_authorizer("test-authorizer_name", )
    mock_client.call.assert_called_once()


async def test_describe_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_authorizer("test-authorizer_name", )


async def test_describe_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_billing_group("test-billing_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_billing_group("test-billing_group_name", )


async def test_describe_ca_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_ca_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_describe_ca_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_ca_certificate("test-certificate_id", )


async def test_describe_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_describe_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_certificate("test-certificate_id", )


async def test_describe_certificate_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_certificate_provider("test-certificate_provider_name", )
    mock_client.call.assert_called_once()


async def test_describe_certificate_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_certificate_provider("test-certificate_provider_name", )


async def test_describe_custom_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_custom_metric("test-metric_name", )
    mock_client.call.assert_called_once()


async def test_describe_custom_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_custom_metric("test-metric_name", )


async def test_describe_default_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_default_authorizer()
    mock_client.call.assert_called_once()


async def test_describe_default_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_default_authorizer()


async def test_describe_detect_mitigation_actions_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_detect_mitigation_actions_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_describe_detect_mitigation_actions_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_detect_mitigation_actions_task("test-task_id", )


async def test_describe_dimension(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_dimension("test-name", )
    mock_client.call.assert_called_once()


async def test_describe_dimension_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_dimension("test-name", )


async def test_describe_domain_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_domain_configuration("test-domain_configuration_name", )
    mock_client.call.assert_called_once()


async def test_describe_domain_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_domain_configuration("test-domain_configuration_name", )


async def test_describe_encryption_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_encryption_configuration()
    mock_client.call.assert_called_once()


async def test_describe_encryption_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_encryption_configuration()


async def test_describe_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoint()
    mock_client.call.assert_called_once()


async def test_describe_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoint()


async def test_describe_event_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_configurations()
    mock_client.call.assert_called_once()


async def test_describe_event_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_configurations()


async def test_describe_fleet_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_fleet_metric("test-metric_name", )
    mock_client.call.assert_called_once()


async def test_describe_fleet_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_fleet_metric("test-metric_name", )


async def test_describe_index(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_index("test-index_name", )
    mock_client.call.assert_called_once()


async def test_describe_index_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_index("test-index_name", )


async def test_describe_job_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_job_execution("test-job_id", "test-thing_name", )
    mock_client.call.assert_called_once()


async def test_describe_job_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_job_execution("test-job_id", "test-thing_name", )


async def test_describe_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_job_template("test-job_template_id", )
    mock_client.call.assert_called_once()


async def test_describe_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_job_template("test-job_template_id", )


async def test_describe_managed_job_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_managed_job_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_describe_managed_job_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_managed_job_template("test-template_name", )


async def test_describe_mitigation_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_mitigation_action("test-action_name", )
    mock_client.call.assert_called_once()


async def test_describe_mitigation_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_mitigation_action("test-action_name", )


async def test_describe_provisioning_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_provisioning_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_describe_provisioning_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_provisioning_template("test-template_name", )


async def test_describe_provisioning_template_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_provisioning_template_version("test-template_name", 1, )
    mock_client.call.assert_called_once()


async def test_describe_provisioning_template_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_provisioning_template_version("test-template_name", 1, )


async def test_describe_role_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_role_alias("test-role_alias", )
    mock_client.call.assert_called_once()


async def test_describe_role_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_role_alias("test-role_alias", )


async def test_describe_scheduled_audit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_scheduled_audit("test-scheduled_audit_name", )
    mock_client.call.assert_called_once()


async def test_describe_scheduled_audit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_scheduled_audit("test-scheduled_audit_name", )


async def test_describe_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_profile("test-security_profile_name", )
    mock_client.call.assert_called_once()


async def test_describe_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_profile("test-security_profile_name", )


async def test_describe_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_stream("test-stream_id", )
    mock_client.call.assert_called_once()


async def test_describe_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_stream("test-stream_id", )


async def test_describe_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_thing_group("test-thing_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_thing_group("test-thing_group_name", )


async def test_describe_thing_registration_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_thing_registration_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_describe_thing_registration_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_thing_registration_task("test-task_id", )


async def test_describe_thing_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_thing_type("test-thing_type_name", )
    mock_client.call.assert_called_once()


async def test_describe_thing_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_thing_type("test-thing_type_name", )


async def test_detach_principal_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_principal_policy("test-policy_name", "test-principal", )
    mock_client.call.assert_called_once()


async def test_detach_principal_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_principal_policy("test-policy_name", "test-principal", )


async def test_detach_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_security_profile("test-security_profile_name", "test-security_profile_target_arn", )
    mock_client.call.assert_called_once()


async def test_detach_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_security_profile("test-security_profile_name", "test-security_profile_target_arn", )


async def test_detach_thing_principal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_thing_principal("test-thing_name", "test-principal", )
    mock_client.call.assert_called_once()


async def test_detach_thing_principal_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_thing_principal("test-thing_name", "test-principal", )


async def test_disable_topic_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_topic_rule("test-rule_name", )
    mock_client.call.assert_called_once()


async def test_disable_topic_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_topic_rule("test-rule_name", )


async def test_disassociate_sbom_from_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_sbom_from_package_version("test-package_name", "test-version_name", )
    mock_client.call.assert_called_once()


async def test_disassociate_sbom_from_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_sbom_from_package_version("test-package_name", "test-version_name", )


async def test_enable_topic_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_topic_rule("test-rule_name", )
    mock_client.call.assert_called_once()


async def test_enable_topic_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_topic_rule("test-rule_name", )


async def test_get_behavior_model_training_summaries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_behavior_model_training_summaries()
    mock_client.call.assert_called_once()


async def test_get_behavior_model_training_summaries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_behavior_model_training_summaries()


async def test_get_buckets_aggregation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_buckets_aggregation("test-query_string", "test-aggregation_field", {}, )
    mock_client.call.assert_called_once()


async def test_get_buckets_aggregation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_buckets_aggregation("test-query_string", "test-aggregation_field", {}, )


async def test_get_cardinality(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cardinality("test-query_string", )
    mock_client.call.assert_called_once()


async def test_get_cardinality_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cardinality("test-query_string", )


async def test_get_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_command("test-command_id", )
    mock_client.call.assert_called_once()


async def test_get_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_command("test-command_id", )


async def test_get_command_execution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_command_execution("test-execution_id", "test-target_arn", )
    mock_client.call.assert_called_once()


async def test_get_command_execution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_command_execution("test-execution_id", "test-target_arn", )


async def test_get_effective_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_effective_policies()
    mock_client.call.assert_called_once()


async def test_get_effective_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_effective_policies()


async def test_get_indexing_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_indexing_configuration()
    mock_client.call.assert_called_once()


async def test_get_indexing_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_indexing_configuration()


async def test_get_job_document(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_job_document("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_job_document_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_job_document("test-job_id", )


async def test_get_logging_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_logging_options()
    mock_client.call.assert_called_once()


async def test_get_logging_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_logging_options()


async def test_get_ota_update(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ota_update("test-ota_update_id", )
    mock_client.call.assert_called_once()


async def test_get_ota_update_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ota_update("test-ota_update_id", )


async def test_get_package(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_package("test-package_name", )
    mock_client.call.assert_called_once()


async def test_get_package_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_package("test-package_name", )


async def test_get_package_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_package_configuration()
    mock_client.call.assert_called_once()


async def test_get_package_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_package_configuration()


async def test_get_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_package_version("test-package_name", "test-version_name", )
    mock_client.call.assert_called_once()


async def test_get_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_package_version("test-package_name", "test-version_name", )


async def test_get_percentiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_percentiles("test-query_string", )
    mock_client.call.assert_called_once()


async def test_get_percentiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_percentiles("test-query_string", )


async def test_get_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_policy_version("test-policy_name", "test-policy_version_id", )
    mock_client.call.assert_called_once()


async def test_get_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_policy_version("test-policy_name", "test-policy_version_id", )


async def test_get_registration_code(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_registration_code()
    mock_client.call.assert_called_once()


async def test_get_registration_code_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_registration_code()


async def test_get_statistics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_statistics("test-query_string", )
    mock_client.call.assert_called_once()


async def test_get_statistics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_statistics("test-query_string", )


async def test_get_thing_connectivity_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_thing_connectivity_data("test-thing_name", )
    mock_client.call.assert_called_once()


async def test_get_thing_connectivity_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_thing_connectivity_data("test-thing_name", )


async def test_get_topic_rule_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_topic_rule_destination("test-arn", )
    mock_client.call.assert_called_once()


async def test_get_topic_rule_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_topic_rule_destination("test-arn", )


async def test_get_v2_logging_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_v2_logging_options()
    mock_client.call.assert_called_once()


async def test_get_v2_logging_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_v2_logging_options()


async def test_list_active_violations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_active_violations()
    mock_client.call.assert_called_once()


async def test_list_active_violations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_active_violations()


async def test_list_attached_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_attached_policies("test-target", )
    mock_client.call.assert_called_once()


async def test_list_attached_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_attached_policies("test-target", )


async def test_list_audit_findings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_audit_findings()
    mock_client.call.assert_called_once()


async def test_list_audit_findings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_audit_findings()


async def test_list_audit_mitigation_actions_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_audit_mitigation_actions_executions("test-task_id", "test-finding_id", )
    mock_client.call.assert_called_once()


async def test_list_audit_mitigation_actions_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_audit_mitigation_actions_executions("test-task_id", "test-finding_id", )


async def test_list_audit_mitigation_actions_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_audit_mitigation_actions_tasks("test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_list_audit_mitigation_actions_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_audit_mitigation_actions_tasks("test-start_time", "test-end_time", )


async def test_list_audit_suppressions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_audit_suppressions()
    mock_client.call.assert_called_once()


async def test_list_audit_suppressions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_audit_suppressions()


async def test_list_audit_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_audit_tasks("test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_list_audit_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_audit_tasks("test-start_time", "test-end_time", )


async def test_list_authorizers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_authorizers()
    mock_client.call.assert_called_once()


async def test_list_authorizers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_authorizers()


async def test_list_billing_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_billing_groups()
    mock_client.call.assert_called_once()


async def test_list_billing_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_billing_groups()


async def test_list_ca_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ca_certificates()
    mock_client.call.assert_called_once()


async def test_list_ca_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ca_certificates()


async def test_list_certificate_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_certificate_providers()
    mock_client.call.assert_called_once()


async def test_list_certificate_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_certificate_providers()


async def test_list_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_certificates()
    mock_client.call.assert_called_once()


async def test_list_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_certificates()


async def test_list_certificates_by_ca(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_certificates_by_ca("test-ca_certificate_id", )
    mock_client.call.assert_called_once()


async def test_list_certificates_by_ca_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_certificates_by_ca("test-ca_certificate_id", )


async def test_list_command_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_command_executions()
    mock_client.call.assert_called_once()


async def test_list_command_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_command_executions()


async def test_list_commands(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_commands()
    mock_client.call.assert_called_once()


async def test_list_commands_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_commands()


async def test_list_custom_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_custom_metrics()
    mock_client.call.assert_called_once()


async def test_list_custom_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_custom_metrics()


async def test_list_detect_mitigation_actions_executions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_detect_mitigation_actions_executions()
    mock_client.call.assert_called_once()


async def test_list_detect_mitigation_actions_executions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_detect_mitigation_actions_executions()


async def test_list_detect_mitigation_actions_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_detect_mitigation_actions_tasks("test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_list_detect_mitigation_actions_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_detect_mitigation_actions_tasks("test-start_time", "test-end_time", )


async def test_list_dimensions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_dimensions()
    mock_client.call.assert_called_once()


async def test_list_dimensions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_dimensions()


async def test_list_domain_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_domain_configurations()
    mock_client.call.assert_called_once()


async def test_list_domain_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_domain_configurations()


async def test_list_fleet_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_fleet_metrics()
    mock_client.call.assert_called_once()


async def test_list_fleet_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_fleet_metrics()


async def test_list_indices(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_indices()
    mock_client.call.assert_called_once()


async def test_list_indices_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_indices()


async def test_list_job_executions_for_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_job_executions_for_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_list_job_executions_for_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_job_executions_for_job("test-job_id", )


async def test_list_job_executions_for_thing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_job_executions_for_thing("test-thing_name", )
    mock_client.call.assert_called_once()


async def test_list_job_executions_for_thing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_job_executions_for_thing("test-thing_name", )


async def test_list_job_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_job_templates()
    mock_client.call.assert_called_once()


async def test_list_job_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_job_templates()


async def test_list_managed_job_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_managed_job_templates()
    mock_client.call.assert_called_once()


async def test_list_managed_job_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_managed_job_templates()


async def test_list_metric_values(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_metric_values("test-thing_name", "test-metric_name", "test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_list_metric_values_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_metric_values("test-thing_name", "test-metric_name", "test-start_time", "test-end_time", )


async def test_list_mitigation_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_mitigation_actions()
    mock_client.call.assert_called_once()


async def test_list_mitigation_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_mitigation_actions()


async def test_list_ota_updates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ota_updates()
    mock_client.call.assert_called_once()


async def test_list_ota_updates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ota_updates()


async def test_list_outgoing_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_outgoing_certificates()
    mock_client.call.assert_called_once()


async def test_list_outgoing_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_outgoing_certificates()


async def test_list_package_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_package_versions("test-package_name", )
    mock_client.call.assert_called_once()


async def test_list_package_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_package_versions("test-package_name", )


async def test_list_packages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_packages()
    mock_client.call.assert_called_once()


async def test_list_packages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_packages()


async def test_list_policy_principals(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policy_principals("test-policy_name", )
    mock_client.call.assert_called_once()


async def test_list_policy_principals_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policy_principals("test-policy_name", )


async def test_list_policy_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policy_versions("test-policy_name", )
    mock_client.call.assert_called_once()


async def test_list_policy_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policy_versions("test-policy_name", )


async def test_list_principal_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_principal_policies("test-principal", )
    mock_client.call.assert_called_once()


async def test_list_principal_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_principal_policies("test-principal", )


async def test_list_principal_things(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_principal_things("test-principal", )
    mock_client.call.assert_called_once()


async def test_list_principal_things_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_principal_things("test-principal", )


async def test_list_principal_things_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_principal_things_v2("test-principal", )
    mock_client.call.assert_called_once()


async def test_list_principal_things_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_principal_things_v2("test-principal", )


async def test_list_provisioning_template_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_provisioning_template_versions("test-template_name", )
    mock_client.call.assert_called_once()


async def test_list_provisioning_template_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_provisioning_template_versions("test-template_name", )


async def test_list_provisioning_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_provisioning_templates()
    mock_client.call.assert_called_once()


async def test_list_provisioning_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_provisioning_templates()


async def test_list_related_resources_for_audit_finding(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_related_resources_for_audit_finding("test-finding_id", )
    mock_client.call.assert_called_once()


async def test_list_related_resources_for_audit_finding_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_related_resources_for_audit_finding("test-finding_id", )


async def test_list_role_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_role_aliases()
    mock_client.call.assert_called_once()


async def test_list_role_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_role_aliases()


async def test_list_sbom_validation_results(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sbom_validation_results("test-package_name", "test-version_name", )
    mock_client.call.assert_called_once()


async def test_list_sbom_validation_results_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sbom_validation_results("test-package_name", "test-version_name", )


async def test_list_scheduled_audits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_scheduled_audits()
    mock_client.call.assert_called_once()


async def test_list_scheduled_audits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_scheduled_audits()


async def test_list_security_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_profiles()
    mock_client.call.assert_called_once()


async def test_list_security_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_profiles()


async def test_list_security_profiles_for_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_profiles_for_target("test-security_profile_target_arn", )
    mock_client.call.assert_called_once()


async def test_list_security_profiles_for_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_profiles_for_target("test-security_profile_target_arn", )


async def test_list_streams(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_streams()
    mock_client.call.assert_called_once()


async def test_list_streams_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_streams()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_targets_for_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_targets_for_policy("test-policy_name", )
    mock_client.call.assert_called_once()


async def test_list_targets_for_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_targets_for_policy("test-policy_name", )


async def test_list_targets_for_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_targets_for_security_profile("test-security_profile_name", )
    mock_client.call.assert_called_once()


async def test_list_targets_for_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_targets_for_security_profile("test-security_profile_name", )


async def test_list_thing_groups_for_thing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_thing_groups_for_thing("test-thing_name", )
    mock_client.call.assert_called_once()


async def test_list_thing_groups_for_thing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_thing_groups_for_thing("test-thing_name", )


async def test_list_thing_principals(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_thing_principals("test-thing_name", )
    mock_client.call.assert_called_once()


async def test_list_thing_principals_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_thing_principals("test-thing_name", )


async def test_list_thing_principals_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_thing_principals_v2("test-thing_name", )
    mock_client.call.assert_called_once()


async def test_list_thing_principals_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_thing_principals_v2("test-thing_name", )


async def test_list_thing_registration_task_reports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_thing_registration_task_reports("test-task_id", "test-report_type", )
    mock_client.call.assert_called_once()


async def test_list_thing_registration_task_reports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_thing_registration_task_reports("test-task_id", "test-report_type", )


async def test_list_thing_registration_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_thing_registration_tasks()
    mock_client.call.assert_called_once()


async def test_list_thing_registration_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_thing_registration_tasks()


async def test_list_things_in_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_things_in_billing_group("test-billing_group_name", )
    mock_client.call.assert_called_once()


async def test_list_things_in_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_things_in_billing_group("test-billing_group_name", )


async def test_list_things_in_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_things_in_thing_group("test-thing_group_name", )
    mock_client.call.assert_called_once()


async def test_list_things_in_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_things_in_thing_group("test-thing_group_name", )


async def test_list_topic_rule_destinations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_topic_rule_destinations()
    mock_client.call.assert_called_once()


async def test_list_topic_rule_destinations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_topic_rule_destinations()


async def test_list_v2_logging_levels(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_v2_logging_levels()
    mock_client.call.assert_called_once()


async def test_list_v2_logging_levels_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_v2_logging_levels()


async def test_list_violation_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_violation_events("test-start_time", "test-end_time", )
    mock_client.call.assert_called_once()


async def test_list_violation_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_violation_events("test-start_time", "test-end_time", )


async def test_put_verification_state_on_violation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_verification_state_on_violation("test-violation_id", "test-verification_state", )
    mock_client.call.assert_called_once()


async def test_put_verification_state_on_violation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_verification_state_on_violation("test-violation_id", "test-verification_state", )


async def test_register_ca_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_ca_certificate("test-ca_certificate", )
    mock_client.call.assert_called_once()


async def test_register_ca_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_ca_certificate("test-ca_certificate", )


async def test_register_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_certificate("test-certificate_pem", )
    mock_client.call.assert_called_once()


async def test_register_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_certificate("test-certificate_pem", )


async def test_register_certificate_without_ca(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_certificate_without_ca("test-certificate_pem", )
    mock_client.call.assert_called_once()


async def test_register_certificate_without_ca_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_certificate_without_ca("test-certificate_pem", )


async def test_register_thing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_thing("test-template_body", )
    mock_client.call.assert_called_once()


async def test_register_thing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_thing("test-template_body", )


async def test_reject_certificate_transfer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_certificate_transfer("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_reject_certificate_transfer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_certificate_transfer("test-certificate_id", )


async def test_remove_thing_from_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_thing_from_billing_group()
    mock_client.call.assert_called_once()


async def test_remove_thing_from_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_thing_from_billing_group()


async def test_remove_thing_from_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_thing_from_thing_group()
    mock_client.call.assert_called_once()


async def test_remove_thing_from_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_thing_from_thing_group()


async def test_replace_topic_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await replace_topic_rule("test-rule_name", {}, )
    mock_client.call.assert_called_once()


async def test_replace_topic_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replace_topic_rule("test-rule_name", {}, )


async def test_run_authorization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_authorization([], )
    mock_client.call.assert_called_once()


async def test_run_authorization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_authorization([], )


async def test_run_invoke_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_invoke_authorizer("test-authorizer_name", )
    mock_client.call.assert_called_once()


async def test_run_invoke_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_invoke_authorizer("test-authorizer_name", )


async def test_search_index(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_index("test-query_string", )
    mock_client.call.assert_called_once()


async def test_search_index_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_index("test-query_string", )


async def test_set_default_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_default_authorizer("test-authorizer_name", )
    mock_client.call.assert_called_once()


async def test_set_default_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_default_authorizer("test-authorizer_name", )


async def test_set_default_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_default_policy_version("test-policy_name", "test-policy_version_id", )
    mock_client.call.assert_called_once()


async def test_set_default_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_default_policy_version("test-policy_name", "test-policy_version_id", )


async def test_set_logging_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_logging_options({}, )
    mock_client.call.assert_called_once()


async def test_set_logging_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_logging_options({}, )


async def test_set_v2_logging_level(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_v2_logging_level({}, "test-log_level", )
    mock_client.call.assert_called_once()


async def test_set_v2_logging_level_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_v2_logging_level({}, "test-log_level", )


async def test_set_v2_logging_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_v2_logging_options()
    mock_client.call.assert_called_once()


async def test_set_v2_logging_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_v2_logging_options()


async def test_start_audit_mitigation_actions_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_audit_mitigation_actions_task("test-task_id", {}, {}, "test-client_request_token", )
    mock_client.call.assert_called_once()


async def test_start_audit_mitigation_actions_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_audit_mitigation_actions_task("test-task_id", {}, {}, "test-client_request_token", )


async def test_start_detect_mitigation_actions_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_detect_mitigation_actions_task("test-task_id", {}, [], "test-client_request_token", )
    mock_client.call.assert_called_once()


async def test_start_detect_mitigation_actions_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_detect_mitigation_actions_task("test-task_id", {}, [], "test-client_request_token", )


async def test_start_on_demand_audit_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_on_demand_audit_task([], )
    mock_client.call.assert_called_once()


async def test_start_on_demand_audit_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_on_demand_audit_task([], )


async def test_start_thing_registration_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_thing_registration_task("test-template_body", "test-input_file_bucket", "test-input_file_key", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_start_thing_registration_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_thing_registration_task("test-template_body", "test-input_file_bucket", "test-input_file_key", "test-role_arn", )


async def test_stop_thing_registration_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_thing_registration_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_stop_thing_registration_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_thing_registration_task("test-task_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_transfer_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await transfer_certificate("test-certificate_id", "test-target_aws_account", )
    mock_client.call.assert_called_once()


async def test_transfer_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await transfer_certificate("test-certificate_id", "test-target_aws_account", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_account_audit_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_audit_configuration()
    mock_client.call.assert_called_once()


async def test_update_account_audit_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_audit_configuration()


async def test_update_audit_suppression(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_audit_suppression("test-check_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_audit_suppression_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_audit_suppression("test-check_name", {}, )


async def test_update_authorizer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_authorizer("test-authorizer_name", )
    mock_client.call.assert_called_once()


async def test_update_authorizer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_authorizer("test-authorizer_name", )


async def test_update_billing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_billing_group("test-billing_group_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_billing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_billing_group("test-billing_group_name", {}, )


async def test_update_ca_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ca_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_update_ca_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ca_certificate("test-certificate_id", )


async def test_update_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_certificate("test-certificate_id", "test-new_status", )
    mock_client.call.assert_called_once()


async def test_update_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_certificate("test-certificate_id", "test-new_status", )


async def test_update_certificate_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_certificate_provider("test-certificate_provider_name", )
    mock_client.call.assert_called_once()


async def test_update_certificate_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_certificate_provider("test-certificate_provider_name", )


async def test_update_command(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_command("test-command_id", )
    mock_client.call.assert_called_once()


async def test_update_command_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_command("test-command_id", )


async def test_update_custom_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_custom_metric("test-metric_name", "test-display_name", )
    mock_client.call.assert_called_once()


async def test_update_custom_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_custom_metric("test-metric_name", "test-display_name", )


async def test_update_dimension(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dimension("test-name", [], )
    mock_client.call.assert_called_once()


async def test_update_dimension_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dimension("test-name", [], )


async def test_update_domain_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_domain_configuration("test-domain_configuration_name", )
    mock_client.call.assert_called_once()


async def test_update_domain_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_domain_configuration("test-domain_configuration_name", )


async def test_update_dynamic_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_dynamic_thing_group("test-thing_group_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_dynamic_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_dynamic_thing_group("test-thing_group_name", {}, )


async def test_update_encryption_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_encryption_configuration("test-encryption_type", )
    mock_client.call.assert_called_once()


async def test_update_encryption_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_encryption_configuration("test-encryption_type", )


async def test_update_event_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_event_configurations()
    mock_client.call.assert_called_once()


async def test_update_event_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_event_configurations()


async def test_update_fleet_metric(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_fleet_metric("test-metric_name", "test-index_name", )
    mock_client.call.assert_called_once()


async def test_update_fleet_metric_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_fleet_metric("test-metric_name", "test-index_name", )


async def test_update_indexing_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_indexing_configuration()
    mock_client.call.assert_called_once()


async def test_update_indexing_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_indexing_configuration()


async def test_update_job(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_job("test-job_id", )
    mock_client.call.assert_called_once()


async def test_update_job_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_job("test-job_id", )


async def test_update_mitigation_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_mitigation_action("test-action_name", )
    mock_client.call.assert_called_once()


async def test_update_mitigation_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_mitigation_action("test-action_name", )


async def test_update_package(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_package("test-package_name", )
    mock_client.call.assert_called_once()


async def test_update_package_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_package("test-package_name", )


async def test_update_package_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_package_configuration()
    mock_client.call.assert_called_once()


async def test_update_package_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_package_configuration()


async def test_update_package_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_package_version("test-package_name", "test-version_name", )
    mock_client.call.assert_called_once()


async def test_update_package_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_package_version("test-package_name", "test-version_name", )


async def test_update_provisioning_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_provisioning_template("test-template_name", )
    mock_client.call.assert_called_once()


async def test_update_provisioning_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_provisioning_template("test-template_name", )


async def test_update_role_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_role_alias("test-role_alias", )
    mock_client.call.assert_called_once()


async def test_update_role_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_role_alias("test-role_alias", )


async def test_update_scheduled_audit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_scheduled_audit("test-scheduled_audit_name", )
    mock_client.call.assert_called_once()


async def test_update_scheduled_audit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_scheduled_audit("test-scheduled_audit_name", )


async def test_update_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_security_profile("test-security_profile_name", )
    mock_client.call.assert_called_once()


async def test_update_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_security_profile("test-security_profile_name", )


async def test_update_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_stream("test-stream_id", )
    mock_client.call.assert_called_once()


async def test_update_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_stream("test-stream_id", )


async def test_update_thing_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_thing_group("test-thing_group_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_thing_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_thing_group("test-thing_group_name", {}, )


async def test_update_thing_groups_for_thing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_thing_groups_for_thing()
    mock_client.call.assert_called_once()


async def test_update_thing_groups_for_thing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_thing_groups_for_thing()


async def test_update_thing_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_thing_type("test-thing_type_name", )
    mock_client.call.assert_called_once()


async def test_update_thing_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_thing_type("test-thing_type_name", )


async def test_update_topic_rule_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_topic_rule_destination("test-arn", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_topic_rule_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_topic_rule_destination("test-arn", "test-status", )


async def test_validate_security_profile_behaviors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    await validate_security_profile_behaviors([], )
    mock_client.call.assert_called_once()


async def test_validate_security_profile_behaviors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iot.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await validate_security_profile_behaviors([], )


@pytest.mark.asyncio
async def test_update_thing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_thing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_thing("test-thing_name", thing_type_name="test-thing_type_name", attributes="test-attributes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_thing_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_thing_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_thing_type("test-thing_type_name", searchable_attributes="test-searchable_attributes", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_thing_group("test-thing_group_name", parent_group_name="test-parent_group_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_accept_certificate_transfer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import accept_certificate_transfer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await accept_certificate_transfer("test-certificate_id", set_as_active="test-set_as_active", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_add_thing_to_billing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import add_thing_to_billing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await add_thing_to_billing_group(billing_group_name="test-billing_group_name", billing_group_arn="test-billing_group_arn", thing_name="test-thing_name", thing_arn="test-thing_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_sbom_with_package_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import associate_sbom_with_package_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await associate_sbom_with_package_version("test-package_name", "test-version_name", "test-sbom", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_targets_with_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import associate_targets_with_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await associate_targets_with_job("test-targets", "test-job_id", comment="test-comment", namespace_id="test-namespace_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_attach_thing_principal_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import attach_thing_principal
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await attach_thing_principal("test-thing_name", "test-principal", thing_principal_type="test-thing_principal_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_cancel_job_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import cancel_job_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await cancel_job_execution("test-job_id", "test-thing_name", force=True, expected_version="test-expected_version", status_details="test-status_details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_audit_suppression_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_audit_suppression
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_audit_suppression("test-check_name", "test-resource_identifier", "test-client_request_token", expiration_date="test-expiration_date", suppress_indefinitely="test-suppress_indefinitely", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_authorizer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_authorizer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_authorizer("test-authorizer_name", "test-authorizer_function_arn", token_key_name="test-token_key_name", token_signing_public_keys="test-token_signing_public_keys", status="test-status", tags=[{"Key": "k", "Value": "v"}], signing_disabled="test-signing_disabled", enable_caching_for_http=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_billing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_billing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_billing_group("test-billing_group_name", billing_group_properties={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_certificate_from_csr_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_certificate_from_csr
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_certificate_from_csr("test-certificate_signing_request", set_as_active="test-set_as_active", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_certificate_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_certificate_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_certificate_provider("test-certificate_provider_name", "test-lambda_function_arn", 1, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_command_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_command
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_command("test-command_id", namespace="test-namespace", display_name="test-display_name", description="test-description", payload="test-payload", mandatory_parameters="test-mandatory_parameters", role_arn="test-role_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_custom_metric_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_custom_metric
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_custom_metric("test-metric_name", "test-metric_type", "test-client_request_token", display_name="test-display_name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dimension_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_dimension
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_dimension("test-name", "test-type_value", "test-string_values", "test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_domain_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_domain_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_domain_configuration({}, domain_name="test-domain_name", server_certificate_arns="test-server_certificate_arns", validation_certificate_arn="test-validation_certificate_arn", authorizer_config={}, service_type="test-service_type", tags=[{"Key": "k", "Value": "v"}], tls_config={}, server_certificate_config={}, authentication_type="test-authentication_type", application_protocol="test-application_protocol", client_certificate_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_dynamic_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_dynamic_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_dynamic_thing_group("test-thing_group_name", "test-query_string", thing_group_properties={}, index_name="test-index_name", query_version="test-query_version", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_fleet_metric_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_fleet_metric
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_fleet_metric("test-metric_name", "test-query_string", "test-aggregation_type", "test-period", "test-aggregation_field", description="test-description", query_version="test-query_version", index_name="test-index_name", unit="test-unit", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_job_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_job_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_job_template("test-job_template_id", "test-description", job_arn="test-job_arn", document_source="test-document_source", document="test-document", presigned_url_config={}, job_executions_rollout_config={}, abort_config={}, timeout_config=1, tags=[{"Key": "k", "Value": "v"}], job_executions_retry_config={}, maintenance_windows="test-maintenance_windows", destination_package_versions="test-destination_package_versions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_keys_and_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_keys_and_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_keys_and_certificate(set_as_active="test-set_as_active", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_mitigation_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_mitigation_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_mitigation_action("test-action_name", "test-role_arn", "test-action_params", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ota_update_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_ota_update
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_ota_update("test-ota_update_id", "test-targets", "test-files", "test-role_arn", description="test-description", protocols="test-protocols", target_selection="test-target_selection", aws_job_executions_rollout_config={}, aws_job_presigned_url_config={}, aws_job_abort_config={}, aws_job_timeout_config=1, additional_parameters="test-additional_parameters", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_package_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_package
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_package("test-package_name", description="test-description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_package_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_package_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_package_version("test-package_name", "test-version_name", description="test-description", attributes="test-attributes", artifact="test-artifact", recipe="test-recipe", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_policy_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_policy_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_policy_version("test-policy_name", "test-policy_document", set_as_default="test-set_as_default", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_provisioning_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_provisioning_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_provisioning_template("test-template_name", "test-template_body", "test-provisioning_role_arn", description="test-description", enabled=True, pre_provisioning_hook="test-pre_provisioning_hook", tags=[{"Key": "k", "Value": "v"}], type_value="test-type_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_provisioning_template_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_provisioning_template_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_provisioning_template_version("test-template_name", "test-template_body", set_as_default="test-set_as_default", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_role_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_role_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_role_alias("test-role_alias", "test-role_arn", credential_duration_seconds=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_scheduled_audit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_scheduled_audit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_scheduled_audit("test-frequency", "test-target_check_names", "test-scheduled_audit_name", day_of_month="test-day_of_month", day_of_week="test-day_of_week", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_security_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_security_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_security_profile("test-security_profile_name", security_profile_description="test-security_profile_description", behaviors="test-behaviors", alert_targets="test-alert_targets", additional_metrics_to_retain="test-additional_metrics_to_retain", additional_metrics_to_retain_v2="test-additional_metrics_to_retain_v2", tags=[{"Key": "k", "Value": "v"}], metrics_export_config=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import create_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await create_stream("test-stream_id", "test-files", "test-role_arn", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_account_audit_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_account_audit_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_account_audit_configuration(delete_scheduled_audits=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_billing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_billing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_billing_group("test-billing_group_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_certificate("test-certificate_id", force_delete=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_dynamic_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_dynamic_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_dynamic_thing_group("test-thing_group_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_fleet_metric_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_fleet_metric
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_fleet_metric("test-metric_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_job("test-job_id", force=True, namespace_id="test-namespace_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_job_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_job_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_job_execution("test-job_id", "test-thing_name", "test-execution_number", force=True, namespace_id="test-namespace_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_ota_update_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_ota_update
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_ota_update("test-ota_update_id", delete_stream=True, force_delete_aws_job=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_package_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_package
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_package("test-package_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_package_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_package_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_package_version("test-package_name", "test-version_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_security_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_security_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_security_profile("test-security_profile_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import delete_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await delete_thing_group("test-thing_group_name", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deprecate_thing_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import deprecate_thing_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await deprecate_thing_type("test-thing_type_name", undo_deprecate="test-undo_deprecate", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import describe_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await describe_endpoint(endpoint_type="test-endpoint_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_job_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import describe_job_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await describe_job_execution("test-job_id", "test-thing_name", execution_number="test-execution_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_managed_job_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import describe_managed_job_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await describe_managed_job_template("test-template_name", template_version="test-template_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_sbom_from_package_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import disassociate_sbom_from_package_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await disassociate_sbom_from_package_version("test-package_name", "test-version_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_behavior_model_training_summaries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_behavior_model_training_summaries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_behavior_model_training_summaries(security_profile_name="test-security_profile_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_buckets_aggregation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_buckets_aggregation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_buckets_aggregation("test-query_string", "test-aggregation_field", "test-buckets_aggregation_type", index_name="test-index_name", query_version="test-query_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_cardinality_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_cardinality
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_cardinality("test-query_string", index_name="test-index_name", aggregation_field="test-aggregation_field", query_version="test-query_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_command_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_command_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_command_execution("test-execution_id", "test-target_arn", include_result=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_effective_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_effective_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_effective_policies(principal="test-principal", cognito_identity_pool_id="test-cognito_identity_pool_id", thing_name="test-thing_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_job_document_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_job_document
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_job_document("test-job_id", before_substitution="test-before_substitution", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_percentiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_percentiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_percentiles("test-query_string", index_name="test-index_name", aggregation_field="test-aggregation_field", query_version="test-query_version", percents="test-percents", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_statistics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import get_statistics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await get_statistics("test-query_string", index_name="test-index_name", aggregation_field="test-aggregation_field", query_version="test-query_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_active_violations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_active_violations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_active_violations(thing_name="test-thing_name", security_profile_name="test-security_profile_name", behavior_criteria_type="test-behavior_criteria_type", list_suppressed_alerts="test-list_suppressed_alerts", verification_state="test-verification_state", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_attached_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_attached_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_attached_policies("test-target", recursive=True, marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_audit_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_audit_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_audit_findings(task_id="test-task_id", check_name="test-check_name", resource_identifier="test-resource_identifier", max_results=1, next_token="test-next_token", start_time="test-start_time", end_time="test-end_time", list_suppressed_findings="test-list_suppressed_findings", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_audit_mitigation_actions_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_audit_mitigation_actions_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_audit_mitigation_actions_executions("test-task_id", "test-finding_id", action_status="test-action_status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_audit_mitigation_actions_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_audit_mitigation_actions_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_audit_mitigation_actions_tasks("test-start_time", "test-end_time", audit_task_id="test-audit_task_id", finding_id="test-finding_id", task_status="test-task_status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_audit_suppressions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_audit_suppressions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_audit_suppressions(check_name="test-check_name", resource_identifier="test-resource_identifier", ascending_order="test-ascending_order", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_audit_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_audit_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_audit_tasks("test-start_time", "test-end_time", task_type="test-task_type", task_status="test-task_status", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_authorizers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_authorizers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_authorizers(page_size=1, marker="test-marker", ascending_order="test-ascending_order", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_billing_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_billing_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_billing_groups(next_token="test-next_token", max_results=1, name_prefix_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ca_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_ca_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_ca_certificates(page_size=1, marker="test-marker", ascending_order="test-ascending_order", template_name="test-template_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_certificate_providers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_certificate_providers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_certificate_providers(next_token="test-next_token", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_certificates(page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_certificates_by_ca_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_certificates_by_ca
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_certificates_by_ca("test-ca_certificate_id", page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_command_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_command_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_command_executions(max_results=1, next_token="test-next_token", namespace="test-namespace", status="test-status", sort_order="test-sort_order", started_time_filter=[{}], completed_time_filter=[{}], target_arn="test-target_arn", command_arn="test-command_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_commands_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_commands
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_commands(max_results=1, next_token="test-next_token", namespace="test-namespace", command_parameter_name="test-command_parameter_name", sort_order="test-sort_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_custom_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_custom_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_custom_metrics(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_detect_mitigation_actions_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_detect_mitigation_actions_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_detect_mitigation_actions_executions(task_id="test-task_id", violation_id="test-violation_id", thing_name="test-thing_name", start_time="test-start_time", end_time="test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_detect_mitigation_actions_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_detect_mitigation_actions_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_detect_mitigation_actions_tasks("test-start_time", "test-end_time", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_dimensions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_dimensions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_dimensions(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_domain_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_domain_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_domain_configurations(marker="test-marker", page_size=1, service_type="test-service_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_fleet_metrics_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_fleet_metrics
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_fleet_metrics(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_indices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_indices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_indices(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_job_executions_for_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_job_executions_for_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_job_executions_for_job("test-job_id", status="test-status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_job_executions_for_thing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_job_executions_for_thing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_job_executions_for_thing("test-thing_name", status="test-status", namespace_id="test-namespace_id", max_results=1, next_token="test-next_token", job_id="test-job_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_job_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_job_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_job_templates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_managed_job_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_managed_job_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_managed_job_templates(template_name="test-template_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_metric_values_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_metric_values
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_metric_values("test-thing_name", "test-metric_name", "test-start_time", "test-end_time", dimension_name="test-dimension_name", dimension_value_operator="test-dimension_value_operator", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_mitigation_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_mitigation_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_mitigation_actions(action_type="test-action_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ota_updates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_ota_updates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_ota_updates(max_results=1, next_token="test-next_token", ota_update_status="test-ota_update_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_outgoing_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_outgoing_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_outgoing_certificates(page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_package_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_package_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_package_versions("test-package_name", status="test-status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_packages_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_packages
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_packages(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_policy_principals_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_policy_principals
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_policy_principals("test-policy_name", marker="test-marker", page_size=1, ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_principal_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_principal_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_principal_policies("test-principal", marker="test-marker", page_size=1, ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_principal_things_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_principal_things
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_principal_things("test-principal", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_principal_things_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_principal_things_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_principal_things_v2("test-principal", next_token="test-next_token", max_results=1, thing_principal_type="test-thing_principal_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_provisioning_template_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_provisioning_template_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_provisioning_template_versions("test-template_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_provisioning_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_provisioning_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_provisioning_templates(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_related_resources_for_audit_finding_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_related_resources_for_audit_finding
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_related_resources_for_audit_finding("test-finding_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_role_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_role_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_role_aliases(page_size=1, marker="test-marker", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sbom_validation_results_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_sbom_validation_results
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_sbom_validation_results("test-package_name", "test-version_name", validation_result="test-validation_result", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_scheduled_audits_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_scheduled_audits
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_scheduled_audits(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_security_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_security_profiles(next_token="test-next_token", max_results=1, dimension_name="test-dimension_name", metric_name="test-metric_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_profiles_for_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_security_profiles_for_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_security_profiles_for_target("test-security_profile_target_arn", next_token="test-next_token", max_results=1, recursive=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_streams_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_streams
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_streams(max_results=1, next_token="test-next_token", ascending_order="test-ascending_order", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_targets_for_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_targets_for_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_targets_for_policy("test-policy_name", marker="test-marker", page_size=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_targets_for_security_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_targets_for_security_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_targets_for_security_profile("test-security_profile_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_thing_groups_for_thing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_thing_groups_for_thing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_thing_groups_for_thing("test-thing_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_thing_principals_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_thing_principals
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_thing_principals("test-thing_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_thing_principals_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_thing_principals_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_thing_principals_v2("test-thing_name", next_token="test-next_token", max_results=1, thing_principal_type="test-thing_principal_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_thing_registration_task_reports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_thing_registration_task_reports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_thing_registration_task_reports("test-task_id", 1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_thing_registration_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_thing_registration_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_thing_registration_tasks(next_token="test-next_token", max_results=1, status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_things_in_billing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_things_in_billing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_things_in_billing_group("test-billing_group_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_things_in_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_things_in_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_things_in_thing_group("test-thing_group_name", recursive=True, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_topic_rule_destinations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_topic_rule_destinations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_topic_rule_destinations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_v2_logging_levels_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_v2_logging_levels
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_v2_logging_levels(target_type="test-target_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_violation_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import list_violation_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await list_violation_events("test-start_time", "test-end_time", thing_name="test-thing_name", security_profile_name="test-security_profile_name", behavior_criteria_type="test-behavior_criteria_type", list_suppressed_alerts="test-list_suppressed_alerts", verification_state="test-verification_state", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_verification_state_on_violation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import put_verification_state_on_violation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await put_verification_state_on_violation("test-violation_id", "test-verification_state", verification_state_description="test-verification_state_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_ca_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import register_ca_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await register_ca_certificate("test-ca_certificate", verification_certificate="test-verification_certificate", set_as_active="test-set_as_active", allow_auto_registration=True, registration_config={}, tags=[{"Key": "k", "Value": "v"}], certificate_mode="test-certificate_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import register_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await register_certificate("test-certificate_pem", ca_certificate_pem="test-ca_certificate_pem", set_as_active="test-set_as_active", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_certificate_without_ca_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import register_certificate_without_ca
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await register_certificate_without_ca("test-certificate_pem", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_thing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import register_thing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await register_thing("test-template_body", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reject_certificate_transfer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import reject_certificate_transfer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await reject_certificate_transfer("test-certificate_id", reject_reason="test-reject_reason", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_thing_from_billing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import remove_thing_from_billing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await remove_thing_from_billing_group(billing_group_name="test-billing_group_name", billing_group_arn="test-billing_group_arn", thing_name="test-thing_name", thing_arn="test-thing_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_thing_from_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import remove_thing_from_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await remove_thing_from_thing_group(thing_group_name="test-thing_group_name", thing_group_arn="test-thing_group_arn", thing_name="test-thing_name", thing_arn="test-thing_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_authorization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import run_authorization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await run_authorization("test-auth_infos", principal="test-principal", cognito_identity_pool_id="test-cognito_identity_pool_id", client_id="test-client_id", policy_names_to_add="test-policy_names_to_add", policy_names_to_skip="test-policy_names_to_skip", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_run_invoke_authorizer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import run_invoke_authorizer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await run_invoke_authorizer("test-authorizer_name", token="test-token", token_signature="test-token_signature", http_context={}, mqtt_context={}, tls_context={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_index_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import search_index
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await search_index("test-query_string", index_name="test-index_name", next_token="test-next_token", max_results=1, query_version="test-query_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_v2_logging_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import set_v2_logging_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await set_v2_logging_options(role_arn="test-role_arn", default_log_level="test-default_log_level", disable_all_logs=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_detect_mitigation_actions_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import start_detect_mitigation_actions_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await start_detect_mitigation_actions_task("test-task_id", "test-target", "test-actions", "test-client_request_token", violation_event_occurrence_range="test-violation_event_occurrence_range", include_only_active_violations=True, include_suppressed_alerts=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_transfer_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import transfer_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await transfer_certificate("test-certificate_id", 1, transfer_message="test-transfer_message", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_account_audit_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_account_audit_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_account_audit_configuration(role_arn="test-role_arn", audit_notification_target_configurations={}, audit_check_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_audit_suppression_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_audit_suppression
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_audit_suppression("test-check_name", "test-resource_identifier", expiration_date="test-expiration_date", suppress_indefinitely="test-suppress_indefinitely", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_authorizer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_authorizer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_authorizer("test-authorizer_name", authorizer_function_arn="test-authorizer_function_arn", token_key_name="test-token_key_name", token_signing_public_keys="test-token_signing_public_keys", status="test-status", enable_caching_for_http=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_billing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_billing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_billing_group("test-billing_group_name", {}, expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_ca_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_ca_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_ca_certificate("test-certificate_id", new_status="test-new_status", new_auto_registration_status="test-new_auto_registration_status", registration_config={}, remove_auto_registration="test-remove_auto_registration", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_certificate_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_certificate_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_certificate_provider("test-certificate_provider_name", lambda_function_arn="test-lambda_function_arn", account_default_for_operations=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_command_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_command
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_command("test-command_id", display_name="test-display_name", description="test-description", deprecated="test-deprecated", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_domain_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_domain_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_domain_configuration({}, authorizer_config={}, domain_configuration_status={}, remove_authorizer_config={}, tls_config={}, server_certificate_config={}, authentication_type="test-authentication_type", application_protocol="test-application_protocol", client_certificate_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_dynamic_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_dynamic_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_dynamic_thing_group("test-thing_group_name", {}, expected_version="test-expected_version", index_name="test-index_name", query_string="test-query_string", query_version="test-query_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_encryption_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_encryption_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_encryption_configuration("test-encryption_type", kms_key_arn="test-kms_key_arn", kms_access_role_arn="test-kms_access_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_event_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_event_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_event_configurations(event_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_fleet_metric_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_fleet_metric
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_fleet_metric("test-metric_name", "test-index_name", query_string="test-query_string", aggregation_type="test-aggregation_type", period="test-period", aggregation_field="test-aggregation_field", description="test-description", query_version="test-query_version", unit="test-unit", expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_indexing_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_indexing_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_indexing_configuration(thing_indexing_configuration={}, thing_group_indexing_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_job_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_job
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_job("test-job_id", description="test-description", presigned_url_config={}, job_executions_rollout_config={}, abort_config={}, timeout_config=1, namespace_id="test-namespace_id", job_executions_retry_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_mitigation_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_mitigation_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_mitigation_action("test-action_name", role_arn="test-role_arn", action_params="test-action_params", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_package_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_package
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_package("test-package_name", description="test-description", default_version_name="test-default_version_name", unset_default_version="test-unset_default_version", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_package_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_package_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_package_configuration(version_update_by_jobs_config={}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_package_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_package_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_package_version("test-package_name", "test-version_name", description="test-description", attributes="test-attributes", artifact="test-artifact", action="test-action", recipe="test-recipe", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_provisioning_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_provisioning_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_provisioning_template("test-template_name", description="test-description", enabled=True, default_version_id="test-default_version_id", provisioning_role_arn="test-provisioning_role_arn", pre_provisioning_hook="test-pre_provisioning_hook", remove_pre_provisioning_hook="test-remove_pre_provisioning_hook", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_role_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_role_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_role_alias("test-role_alias", role_arn="test-role_arn", credential_duration_seconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_scheduled_audit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_scheduled_audit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_scheduled_audit("test-scheduled_audit_name", frequency="test-frequency", day_of_month="test-day_of_month", day_of_week="test-day_of_week", target_check_names="test-target_check_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_security_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_security_profile("test-security_profile_name", security_profile_description="test-security_profile_description", behaviors="test-behaviors", alert_targets="test-alert_targets", additional_metrics_to_retain="test-additional_metrics_to_retain", additional_metrics_to_retain_v2="test-additional_metrics_to_retain_v2", delete_behaviors=True, delete_alert_targets=True, delete_additional_metrics_to_retain=True, expected_version="test-expected_version", metrics_export_config=1, delete_metrics_export_config=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_stream("test-stream_id", description="test-description", files="test-files", role_arn="test-role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_thing_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_thing_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_thing_group("test-thing_group_name", {}, expected_version="test-expected_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_thing_groups_for_thing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_thing_groups_for_thing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_thing_groups_for_thing(thing_name="test-thing_name", thing_groups_to_add="test-thing_groups_to_add", thing_groups_to_remove="test-thing_groups_to_remove", override_dynamic_groups="test-override_dynamic_groups", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_thing_type_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iot import update_thing_type
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iot.async_client", lambda *a, **kw: mock_client)
    await update_thing_type("test-thing_type_name", thing_type_properties={}, region_name="us-east-1")
    mock_client.call.assert_called_once()
