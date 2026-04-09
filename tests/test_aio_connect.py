"""Tests for aws_util.aio.connect -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.connect import (
    ConnectContactFlow,
    ConnectInstance,
    ConnectQueue,
    ConnectRoutingProfile,
    ConnectUser,
    ContactResult,
    MetricResult,
    create_contact_flow,
    create_instance,
    create_queue,
    create_routing_profile,
    create_user,
    delete_instance,
    delete_user,
    describe_contact_flow,
    describe_instance,
    describe_queue,
    describe_routing_profile,
    describe_user,
    get_contact_attributes,
    get_current_metric_data,
    list_contact_flows,
    list_instances,
    list_queues,
    list_routing_profiles,
    list_users,
    start_chat_contact,
    start_outbound_voice_contact,
    start_task_contact,
    stop_contact,
    update_contact_attributes,
    update_contact_flow_content,
    update_queue_status,
    update_user_routing_profile,
    activate_evaluation_form,
    associate_analytics_data_set,
    associate_approved_origin,
    associate_bot,
    associate_contact_with_user,
    associate_default_vocabulary,
    associate_email_address_alias,
    associate_flow,
    associate_instance_storage_config,
    associate_lambda_function,
    associate_lex_bot,
    associate_phone_number_contact_flow,
    associate_queue_quick_connects,
    associate_routing_profile_queues,
    associate_security_key,
    associate_traffic_distribution_group_user,
    associate_user_proficiencies,
    batch_associate_analytics_data_set,
    batch_disassociate_analytics_data_set,
    batch_get_attached_file_metadata,
    batch_get_flow_association,
    batch_put_contact,
    claim_phone_number,
    complete_attached_file_upload,
    create_agent_status,
    create_contact,
    create_contact_flow_module,
    create_contact_flow_version,
    create_email_address,
    create_evaluation_form,
    create_hours_of_operation,
    create_hours_of_operation_override,
    create_integration_association,
    create_participant,
    create_persistent_contact_association,
    create_predefined_attribute,
    create_prompt,
    create_push_notification_registration,
    create_quick_connect,
    create_rule,
    create_security_profile,
    create_task_template,
    create_traffic_distribution_group,
    create_use_case,
    create_user_hierarchy_group,
    create_view,
    create_view_version,
    create_vocabulary,
    deactivate_evaluation_form,
    delete_attached_file,
    delete_contact_evaluation,
    delete_contact_flow,
    delete_contact_flow_module,
    delete_contact_flow_version,
    delete_email_address,
    delete_evaluation_form,
    delete_hours_of_operation,
    delete_hours_of_operation_override,
    delete_integration_association,
    delete_predefined_attribute,
    delete_prompt,
    delete_push_notification_registration,
    delete_queue,
    delete_quick_connect,
    delete_routing_profile,
    delete_rule,
    delete_security_profile,
    delete_task_template,
    delete_traffic_distribution_group,
    delete_use_case,
    delete_user_hierarchy_group,
    delete_view,
    delete_view_version,
    delete_vocabulary,
    describe_agent_status,
    describe_authentication_profile,
    describe_contact,
    describe_contact_evaluation,
    describe_contact_flow_module,
    describe_email_address,
    describe_evaluation_form,
    describe_hours_of_operation,
    describe_hours_of_operation_override,
    describe_instance_attribute,
    describe_instance_storage_config,
    describe_phone_number,
    describe_predefined_attribute,
    describe_prompt,
    describe_quick_connect,
    describe_rule,
    describe_security_profile,
    describe_traffic_distribution_group,
    describe_user_hierarchy_group,
    describe_user_hierarchy_structure,
    describe_view,
    describe_vocabulary,
    disassociate_analytics_data_set,
    disassociate_approved_origin,
    disassociate_bot,
    disassociate_email_address_alias,
    disassociate_flow,
    disassociate_instance_storage_config,
    disassociate_lambda_function,
    disassociate_lex_bot,
    disassociate_phone_number_contact_flow,
    disassociate_queue_quick_connects,
    disassociate_routing_profile_queues,
    disassociate_security_key,
    disassociate_traffic_distribution_group_user,
    disassociate_user_proficiencies,
    dismiss_user_contact,
    get_attached_file,
    get_contact_metrics,
    get_current_user_data,
    get_effective_hours_of_operations,
    get_federation_token,
    get_flow_association,
    get_metric_data,
    get_metric_data_v2,
    get_prompt_file,
    get_task_template,
    get_traffic_distribution,
    import_phone_number,
    list_agent_statuses,
    list_analytics_data_associations,
    list_analytics_data_lake_data_sets,
    list_approved_origins,
    list_associated_contacts,
    list_authentication_profiles,
    list_bots,
    list_contact_evaluations,
    list_contact_flow_modules,
    list_contact_flow_versions,
    list_contact_references,
    list_default_vocabularies,
    list_evaluation_form_versions,
    list_evaluation_forms,
    list_flow_associations,
    list_hours_of_operation_overrides,
    list_hours_of_operations,
    list_instance_attributes,
    list_instance_storage_configs,
    list_integration_associations,
    list_lambda_functions,
    list_lex_bots,
    list_phone_numbers,
    list_phone_numbers_v2,
    list_predefined_attributes,
    list_prompts,
    list_queue_quick_connects,
    list_quick_connects,
    list_realtime_contact_analysis_segments_v2,
    list_routing_profile_manual_assignment_queues,
    list_routing_profile_queues,
    list_rules,
    list_security_keys,
    list_security_profile_applications,
    list_security_profile_permissions,
    list_security_profiles,
    list_tags_for_resource,
    list_task_templates,
    list_traffic_distribution_group_users,
    list_traffic_distribution_groups,
    list_use_cases,
    list_user_hierarchy_groups,
    list_user_proficiencies,
    list_view_versions,
    list_views,
    monitor_contact,
    pause_contact,
    put_user_status,
    release_phone_number,
    replicate_instance,
    resume_contact,
    resume_contact_recording,
    search_agent_statuses,
    search_available_phone_numbers,
    search_contact_evaluations,
    search_contact_flow_modules,
    search_contact_flows,
    search_contacts,
    search_email_addresses,
    search_evaluation_forms,
    search_hours_of_operation_overrides,
    search_hours_of_operations,
    search_predefined_attributes,
    search_prompts,
    search_queues,
    search_quick_connects,
    search_resource_tags,
    search_routing_profiles,
    search_security_profiles,
    search_user_hierarchy_groups,
    search_users,
    search_vocabularies,
    send_chat_integration_event,
    send_outbound_email,
    start_attached_file_upload,
    start_contact_evaluation,
    start_contact_recording,
    start_contact_streaming,
    start_email_contact,
    start_outbound_chat_contact,
    start_outbound_email_contact,
    start_screen_sharing,
    start_web_rtc_contact,
    stop_contact_recording,
    stop_contact_streaming,
    submit_contact_evaluation,
    suspend_contact_recording,
    tag_contact,
    tag_resource,
    transfer_contact,
    untag_contact,
    untag_resource,
    update_agent_status,
    update_authentication_profile,
    update_contact,
    update_contact_evaluation,
    update_contact_flow_metadata,
    update_contact_flow_module_content,
    update_contact_flow_module_metadata,
    update_contact_flow_name,
    update_contact_routing_data,
    update_contact_schedule,
    update_email_address_metadata,
    update_evaluation_form,
    update_hours_of_operation,
    update_hours_of_operation_override,
    update_instance_attribute,
    update_instance_storage_config,
    update_participant_authentication,
    update_participant_role_config,
    update_phone_number,
    update_phone_number_metadata,
    update_predefined_attribute,
    update_prompt,
    update_queue_hours_of_operation,
    update_queue_max_contacts,
    update_queue_name,
    update_queue_outbound_caller_config,
    update_queue_outbound_email_config,
    update_quick_connect_config,
    update_quick_connect_name,
    update_routing_profile_agent_availability_timer,
    update_routing_profile_concurrency,
    update_routing_profile_default_outbound_queue,
    update_routing_profile_name,
    update_routing_profile_queues,
    update_rule,
    update_security_profile,
    update_task_template,
    update_traffic_distribution,
    update_user_hierarchy,
    update_user_hierarchy_group_name,
    update_user_hierarchy_structure,
    update_user_identity_info,
    update_user_phone_config,
    update_user_proficiencies,
    update_user_security_profiles,
    update_view_content,
    update_view_metadata,
)

INST = "inst-123"
CF = "cf-123"
QID = "q-123"
RPID = "rp-123"
UID = "u-123"


def _mf(mc):
    return lambda *a, **kw: mc


async def test_create_instance(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"Id": INST, "Arn": "arn:inst"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await create_instance("SAML"); assert isinstance(r, ConnectInstance)

async def test_create_instance_with_alias(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"Id": INST}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await create_instance("SAML", instance_alias="my-inst")
    assert mc.call.call_args[1]["InstanceAlias"] == "my-inst"

async def test_create_instance_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_instance("SAML")

async def test_describe_instance(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"Instance": {"Id": INST, "InstanceAlias": "a", "Arn": "arn"}}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await describe_instance(INST); assert r.instance_id == INST

async def test_describe_instance_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await describe_instance(INST)

async def test_list_instances(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"InstanceSummaryList": [{"Id": INST}]}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await list_instances(); assert len(r) == 1

async def test_list_instances_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"InstanceSummaryList": [{"Id": "i1"}], "NextToken": "t"}, {"InstanceSummaryList": [{"Id": "i2"}]}]
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_instances()) == 2

async def test_list_instances_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_instances()

async def test_delete_instance(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await delete_instance(INST)

async def test_delete_instance_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await delete_instance(INST)

async def test_create_contact_flow(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactFlowId": CF, "ContactFlowArn": "arn"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await create_contact_flow(INST, "flow", "CONTACT_FLOW", "{}"); assert isinstance(r, ConnectContactFlow)

async def test_create_contact_flow_with_desc(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactFlowId": CF}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await create_contact_flow(INST, "f", "CONTACT_FLOW", "{}", description="desc")
    assert mc.call.call_args[1]["Description"] == "desc"

async def test_create_contact_flow_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_contact_flow(INST, "f", "T", "{}")

async def test_describe_contact_flow(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactFlow": {"Id": CF, "Name": "f"}}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await describe_contact_flow(INST, CF); assert r.contact_flow_id == CF

async def test_describe_contact_flow_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await describe_contact_flow(INST, CF)

async def test_list_contact_flows(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactFlowSummaryList": [{"Id": CF, "Name": "f"}]}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_contact_flows(INST)) == 1

async def test_list_contact_flows_with_types(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactFlowSummaryList": []}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await list_contact_flows(INST, contact_flow_types=["CONTACT_FLOW"])

async def test_list_contact_flows_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"ContactFlowSummaryList": [{"Id": "c1", "Name": "f1"}], "NextToken": "t"}, {"ContactFlowSummaryList": [{"Id": "c2", "Name": "f2"}]}]
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_contact_flows(INST)) == 2

async def test_list_contact_flows_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_contact_flows(INST)

async def test_update_contact_flow_content(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await update_contact_flow_content(INST, CF, "{}")

async def test_update_contact_flow_content_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await update_contact_flow_content(INST, CF, "{}")

async def test_create_queue(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"QueueId": QID, "QueueArn": "arn"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await create_queue(INST, "q", "hop-1"); assert isinstance(r, ConnectQueue)

async def test_create_queue_with_desc(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"QueueId": QID}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await create_queue(INST, "q", "hop-1", description="d")
    assert mc.call.call_args[1]["Description"] == "d"

async def test_create_queue_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_queue(INST, "q", "hop-1")

async def test_describe_queue(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"Queue": {"QueueId": QID, "Name": "q"}}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert (await describe_queue(INST, QID)).queue_id == QID

async def test_describe_queue_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await describe_queue(INST, QID)

async def test_list_queues(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"QueueSummaryList": [{"Id": QID, "Name": "q"}]}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_queues(INST)) == 1

async def test_list_queues_with_types(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"QueueSummaryList": []}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await list_queues(INST, queue_types=["STANDARD"])

async def test_list_queues_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"QueueSummaryList": [{"Id": "q1", "Name": "q1"}], "NextToken": "t"}, {"QueueSummaryList": [{"Id": "q2", "Name": "q2"}]}]
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_queues(INST)) == 2

async def test_list_queues_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_queues(INST)

async def test_update_queue_status(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await update_queue_status(INST, QID, "ENABLED")

async def test_update_queue_status_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await update_queue_status(INST, QID, "ENABLED")

async def test_create_routing_profile(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"RoutingProfileId": RPID, "RoutingProfileArn": "arn"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await create_routing_profile(INST, "rp", QID, "desc", [{"Channel": "VOICE", "Concurrency": 1}])
    assert isinstance(r, ConnectRoutingProfile)

async def test_create_routing_profile_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_routing_profile(INST, "rp", QID, "d", [])

async def test_describe_routing_profile(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"RoutingProfile": {"RoutingProfileId": RPID, "Name": "rp"}}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert (await describe_routing_profile(INST, RPID)).routing_profile_id == RPID

async def test_describe_routing_profile_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await describe_routing_profile(INST, RPID)

async def test_list_routing_profiles(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"RoutingProfileSummaryList": [{"Id": RPID, "Name": "rp"}]}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_routing_profiles(INST)) == 1

async def test_list_routing_profiles_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"RoutingProfileSummaryList": [{"Id": "r1", "Name": "r1"}], "NextToken": "t"}, {"RoutingProfileSummaryList": [{"Id": "r2", "Name": "r2"}]}]
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_routing_profiles(INST)) == 2

async def test_list_routing_profiles_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_routing_profiles(INST)

async def test_create_user(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"UserId": UID, "UserArn": "arn"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await create_user(INST, "user1", {"PhoneType": "SOFT_PHONE"}, ["sp-1"], RPID)
    assert isinstance(r, ConnectUser)
async def test_create_user_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await create_user(INST, "u", {}, [], RPID)

async def test_describe_user(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"User": {"Id": UID, "Username": "u"}}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert (await describe_user(INST, UID)).user_id == UID

async def test_describe_user_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await describe_user(INST, UID)

async def test_list_users(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"UserSummaryList": [{"Id": UID}]}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_users(INST)) == 1

async def test_list_users_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [{"UserSummaryList": [{"Id": "u1"}], "NextToken": "t"}, {"UserSummaryList": [{"Id": "u2"}]}]
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert len(await list_users(INST)) == 2

async def test_list_users_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await list_users(INST)

async def test_update_user_routing_profile(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await update_user_routing_profile(INST, UID, RPID)

async def test_update_user_routing_profile_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await update_user_routing_profile(INST, UID, RPID)

async def test_delete_user(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await delete_user(INST, UID)

async def test_delete_user_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await delete_user(INST, UID)

async def test_start_outbound_voice_contact(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await start_outbound_voice_contact(INST, CF, "+15555555555"); assert isinstance(r, ContactResult)

async def test_start_outbound_voice_contact_with_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await start_outbound_voice_contact(INST, CF, "+15555555555", source_phone_number="+14444444444", queue_id=QID, attributes={"k": "v"})
    assert mc.call.call_args[1]["SourcePhoneNumber"] == "+14444444444"

async def test_start_outbound_voice_contact_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await start_outbound_voice_contact(INST, CF, "+1")

async def test_start_chat_contact(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await start_chat_contact(INST, CF, {"DisplayName": "U"}); assert isinstance(r, ContactResult)

async def test_start_chat_contact_with_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await start_chat_contact(INST, CF, {"DisplayName": "U"}, attributes={"k": "v"}, initial_message={"ContentType": "text/plain", "Content": "hi"})

async def test_start_chat_contact_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await start_chat_contact(INST, CF, {})

async def test_stop_contact(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await stop_contact("c-1", INST)

async def test_stop_contact_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await stop_contact("c-1", INST)

async def test_get_contact_attributes(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"Attributes": {"k": "v"}}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    assert (await get_contact_attributes(INST, "c-1")) == {"k": "v"}

async def test_get_contact_attributes_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await get_contact_attributes(INST, "c-1")

async def test_update_contact_attributes(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await update_contact_attributes(INST, "c-1", {"k": "v"})

async def test_update_contact_attributes_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await update_contact_attributes(INST, "c-1", {})

async def test_get_current_metric_data(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"MetricResults": [{"Dimensions": {}, "Collections": []}]}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await get_current_metric_data(INST, {"Queues": [QID]}, [{"Name": "AGENTS_ONLINE", "Unit": "COUNT"}])
    assert len(r) == 1 and isinstance(r[0], MetricResult)

async def test_get_current_metric_data_with_groupings(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"MetricResults": []}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await get_current_metric_data(INST, {}, [], groupings=["QUEUE"])
    assert mc.call.call_args[1]["Groupings"] == ["QUEUE"]

async def test_get_current_metric_data_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await get_current_metric_data(INST, {}, [])

async def test_start_task_contact(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    r = await start_task_contact(INST, CF, "task"); assert isinstance(r, ContactResult)

async def test_start_task_contact_with_opts(monkeypatch):
    mc = AsyncMock(); mc.call.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    await start_task_contact(INST, CF, "task", references={"r": {"Type": "URL", "Value": "http://x"}}, description="d", attributes={"k": "v"})
    kw = mc.call.call_args[1]; assert "References" in kw; assert kw["Description"] == "d"

async def test_start_task_contact_error(monkeypatch):
    mc = AsyncMock(); mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.connect.async_client", _mf(mc))
    with pytest.raises(RuntimeError): await start_task_contact(INST, CF, "task")


async def test_activate_evaluation_form(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await activate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, )
    mock_client.call.assert_called_once()


async def test_activate_evaluation_form_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await activate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, )


async def test_associate_analytics_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_analytics_data_set("test-instance_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_associate_analytics_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_analytics_data_set("test-instance_id", "test-data_set_id", )


async def test_associate_approved_origin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_approved_origin("test-instance_id", "test-origin", )
    mock_client.call.assert_called_once()


async def test_associate_approved_origin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_approved_origin("test-instance_id", "test-origin", )


async def test_associate_bot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_bot("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_associate_bot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_bot("test-instance_id", )


async def test_associate_contact_with_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_contact_with_user("test-instance_id", "test-contact_id", "test-user_id", )
    mock_client.call.assert_called_once()


async def test_associate_contact_with_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_contact_with_user("test-instance_id", "test-contact_id", "test-user_id", )


async def test_associate_default_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_default_vocabulary("test-instance_id", "test-language_code", )
    mock_client.call.assert_called_once()


async def test_associate_default_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_default_vocabulary("test-instance_id", "test-language_code", )


async def test_associate_email_address_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_email_address_alias("test-email_address_id", "test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_associate_email_address_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_email_address_alias("test-email_address_id", "test-instance_id", {}, )


async def test_associate_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_flow("test-instance_id", "test-resource_id", "test-flow_id", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_associate_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_flow("test-instance_id", "test-resource_id", "test-flow_id", "test-resource_type", )


async def test_associate_instance_storage_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_instance_storage_config("test-instance_id", "test-resource_type", {}, )
    mock_client.call.assert_called_once()


async def test_associate_instance_storage_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_instance_storage_config("test-instance_id", "test-resource_type", {}, )


async def test_associate_lambda_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_lambda_function("test-instance_id", "test-function_arn", )
    mock_client.call.assert_called_once()


async def test_associate_lambda_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_lambda_function("test-instance_id", "test-function_arn", )


async def test_associate_lex_bot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_lex_bot("test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_associate_lex_bot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_lex_bot("test-instance_id", {}, )


async def test_associate_phone_number_contact_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_associate_phone_number_contact_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", "test-contact_flow_id", )


async def test_associate_queue_quick_connects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_queue_quick_connects("test-instance_id", "test-queue_id", [], )
    mock_client.call.assert_called_once()


async def test_associate_queue_quick_connects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_queue_quick_connects("test-instance_id", "test-queue_id", [], )


async def test_associate_routing_profile_queues(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_routing_profile_queues("test-instance_id", "test-routing_profile_id", )
    mock_client.call.assert_called_once()


async def test_associate_routing_profile_queues_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_routing_profile_queues("test-instance_id", "test-routing_profile_id", )


async def test_associate_security_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_security_key("test-instance_id", "test-key", )
    mock_client.call.assert_called_once()


async def test_associate_security_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_security_key("test-instance_id", "test-key", )


async def test_associate_traffic_distribution_group_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_associate_traffic_distribution_group_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", )


async def test_associate_user_proficiencies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_user_proficiencies("test-instance_id", "test-user_id", [], )
    mock_client.call.assert_called_once()


async def test_associate_user_proficiencies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_user_proficiencies("test-instance_id", "test-user_id", [], )


async def test_batch_associate_analytics_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_associate_analytics_data_set("test-instance_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_associate_analytics_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_associate_analytics_data_set("test-instance_id", [], )


async def test_batch_disassociate_analytics_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_disassociate_analytics_data_set("test-instance_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_disassociate_analytics_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_disassociate_analytics_data_set("test-instance_id", [], )


async def test_batch_get_attached_file_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_attached_file_metadata([], "test-instance_id", "test-associated_resource_arn", )
    mock_client.call.assert_called_once()


async def test_batch_get_attached_file_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_attached_file_metadata([], "test-instance_id", "test-associated_resource_arn", )


async def test_batch_get_flow_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_flow_association("test-instance_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_flow_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_flow_association("test-instance_id", [], )


async def test_batch_put_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_put_contact("test-instance_id", [], )
    mock_client.call.assert_called_once()


async def test_batch_put_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_put_contact("test-instance_id", [], )


async def test_claim_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await claim_phone_number("test-phone_number", )
    mock_client.call.assert_called_once()


async def test_claim_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await claim_phone_number("test-phone_number", )


async def test_complete_attached_file_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await complete_attached_file_upload("test-instance_id", "test-file_id", "test-associated_resource_arn", )
    mock_client.call.assert_called_once()


async def test_complete_attached_file_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await complete_attached_file_upload("test-instance_id", "test-file_id", "test-associated_resource_arn", )


async def test_create_agent_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_agent_status("test-instance_id", "test-name", "test-state", )
    mock_client.call.assert_called_once()


async def test_create_agent_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_agent_status("test-instance_id", "test-name", "test-state", )


async def test_create_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_contact("test-instance_id", "test-channel", "test-initiation_method", )
    mock_client.call.assert_called_once()


async def test_create_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_contact("test-instance_id", "test-channel", "test-initiation_method", )


async def test_create_contact_flow_module(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_contact_flow_module("test-instance_id", "test-name", "test-content", )
    mock_client.call.assert_called_once()


async def test_create_contact_flow_module_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_contact_flow_module("test-instance_id", "test-name", "test-content", )


async def test_create_contact_flow_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_contact_flow_version("test-instance_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_create_contact_flow_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_contact_flow_version("test-instance_id", "test-contact_flow_id", )


async def test_create_email_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_email_address("test-instance_id", "test-email_address", )
    mock_client.call.assert_called_once()


async def test_create_email_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_email_address("test-instance_id", "test-email_address", )


async def test_create_evaluation_form(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_evaluation_form("test-instance_id", "test-title", [], )
    mock_client.call.assert_called_once()


async def test_create_evaluation_form_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_evaluation_form("test-instance_id", "test-title", [], )


async def test_create_hours_of_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_hours_of_operation("test-instance_id", "test-name", "test-time_zone", [], )
    mock_client.call.assert_called_once()


async def test_create_hours_of_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_hours_of_operation("test-instance_id", "test-name", "test-time_zone", [], )


async def test_create_hours_of_operation_override(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-name", [], "test-effective_from", "test-effective_till", )
    mock_client.call.assert_called_once()


async def test_create_hours_of_operation_override_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-name", [], "test-effective_from", "test-effective_till", )


async def test_create_integration_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_integration_association("test-instance_id", "test-integration_type", "test-integration_arn", )
    mock_client.call.assert_called_once()


async def test_create_integration_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_integration_association("test-instance_id", "test-integration_type", "test-integration_arn", )


async def test_create_participant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_participant("test-instance_id", "test-contact_id", {}, )
    mock_client.call.assert_called_once()


async def test_create_participant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_participant("test-instance_id", "test-contact_id", {}, )


async def test_create_persistent_contact_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_persistent_contact_association("test-instance_id", "test-initial_contact_id", "test-rehydration_type", "test-source_contact_id", )
    mock_client.call.assert_called_once()


async def test_create_persistent_contact_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_persistent_contact_association("test-instance_id", "test-initial_contact_id", "test-rehydration_type", "test-source_contact_id", )


async def test_create_predefined_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_predefined_attribute("test-instance_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_predefined_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_predefined_attribute("test-instance_id", "test-name", )


async def test_create_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_prompt("test-instance_id", "test-name", "test-s3_uri", )
    mock_client.call.assert_called_once()


async def test_create_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_prompt("test-instance_id", "test-name", "test-s3_uri", )


async def test_create_push_notification_registration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_push_notification_registration("test-instance_id", "test-pinpoint_app_arn", "test-device_token", "test-device_type", {}, )
    mock_client.call.assert_called_once()


async def test_create_push_notification_registration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_push_notification_registration("test-instance_id", "test-pinpoint_app_arn", "test-device_token", "test-device_type", {}, )


async def test_create_quick_connect(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_quick_connect("test-instance_id", "test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_quick_connect_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_quick_connect("test-instance_id", "test-name", {}, )


async def test_create_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_rule("test-instance_id", "test-name", {}, "test-function", [], "test-publish_status", )
    mock_client.call.assert_called_once()


async def test_create_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_rule("test-instance_id", "test-name", {}, "test-function", [], "test-publish_status", )


async def test_create_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_security_profile("test-security_profile_name", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_create_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_security_profile("test-security_profile_name", "test-instance_id", )


async def test_create_task_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_task_template("test-instance_id", "test-name", [], )
    mock_client.call.assert_called_once()


async def test_create_task_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_task_template("test-instance_id", "test-name", [], )


async def test_create_traffic_distribution_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_traffic_distribution_group("test-name", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_create_traffic_distribution_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_traffic_distribution_group("test-name", "test-instance_id", )


async def test_create_use_case(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_use_case("test-instance_id", "test-integration_association_id", "test-use_case_type", )
    mock_client.call.assert_called_once()


async def test_create_use_case_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_use_case("test-instance_id", "test-integration_association_id", "test-use_case_type", )


async def test_create_user_hierarchy_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_user_hierarchy_group("test-name", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_create_user_hierarchy_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_hierarchy_group("test-name", "test-instance_id", )


async def test_create_view(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_view("test-instance_id", "test-status", {}, "test-name", )
    mock_client.call.assert_called_once()


async def test_create_view_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_view("test-instance_id", "test-status", {}, "test-name", )


async def test_create_view_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_view_version("test-instance_id", "test-view_id", )
    mock_client.call.assert_called_once()


async def test_create_view_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_view_version("test-instance_id", "test-view_id", )


async def test_create_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vocabulary("test-instance_id", "test-vocabulary_name", "test-language_code", "test-content", )
    mock_client.call.assert_called_once()


async def test_create_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vocabulary("test-instance_id", "test-vocabulary_name", "test-language_code", "test-content", )


async def test_deactivate_evaluation_form(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await deactivate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, )
    mock_client.call.assert_called_once()


async def test_deactivate_evaluation_form_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deactivate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, )


async def test_delete_attached_file(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_attached_file_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", )


async def test_delete_contact_evaluation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_contact_evaluation("test-instance_id", "test-evaluation_id", )
    mock_client.call.assert_called_once()


async def test_delete_contact_evaluation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_contact_evaluation("test-instance_id", "test-evaluation_id", )


async def test_delete_contact_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_contact_flow("test-instance_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_delete_contact_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_contact_flow("test-instance_id", "test-contact_flow_id", )


async def test_delete_contact_flow_module(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_contact_flow_module("test-instance_id", "test-contact_flow_module_id", )
    mock_client.call.assert_called_once()


async def test_delete_contact_flow_module_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_contact_flow_module("test-instance_id", "test-contact_flow_module_id", )


async def test_delete_contact_flow_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_contact_flow_version("test-instance_id", "test-contact_flow_id", 1, )
    mock_client.call.assert_called_once()


async def test_delete_contact_flow_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_contact_flow_version("test-instance_id", "test-contact_flow_id", 1, )


async def test_delete_email_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_email_address("test-instance_id", "test-email_address_id", )
    mock_client.call.assert_called_once()


async def test_delete_email_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_email_address("test-instance_id", "test-email_address_id", )


async def test_delete_evaluation_form(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_evaluation_form("test-instance_id", "test-evaluation_form_id", )
    mock_client.call.assert_called_once()


async def test_delete_evaluation_form_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_evaluation_form("test-instance_id", "test-evaluation_form_id", )


async def test_delete_hours_of_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_hours_of_operation("test-instance_id", "test-hours_of_operation_id", )
    mock_client.call.assert_called_once()


async def test_delete_hours_of_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_hours_of_operation("test-instance_id", "test-hours_of_operation_id", )


async def test_delete_hours_of_operation_override(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", )
    mock_client.call.assert_called_once()


async def test_delete_hours_of_operation_override_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", )


async def test_delete_integration_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_integration_association("test-instance_id", "test-integration_association_id", )
    mock_client.call.assert_called_once()


async def test_delete_integration_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_integration_association("test-instance_id", "test-integration_association_id", )


async def test_delete_predefined_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_predefined_attribute("test-instance_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_delete_predefined_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_predefined_attribute("test-instance_id", "test-name", )


async def test_delete_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_prompt("test-instance_id", "test-prompt_id", )
    mock_client.call.assert_called_once()


async def test_delete_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_prompt("test-instance_id", "test-prompt_id", )


async def test_delete_push_notification_registration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_push_notification_registration("test-instance_id", "test-registration_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_delete_push_notification_registration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_push_notification_registration("test-instance_id", "test-registration_id", "test-contact_id", )


async def test_delete_queue(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_queue("test-instance_id", "test-queue_id", )
    mock_client.call.assert_called_once()


async def test_delete_queue_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_queue("test-instance_id", "test-queue_id", )


async def test_delete_quick_connect(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_quick_connect("test-instance_id", "test-quick_connect_id", )
    mock_client.call.assert_called_once()


async def test_delete_quick_connect_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_quick_connect("test-instance_id", "test-quick_connect_id", )


async def test_delete_routing_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_routing_profile("test-instance_id", "test-routing_profile_id", )
    mock_client.call.assert_called_once()


async def test_delete_routing_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_routing_profile("test-instance_id", "test-routing_profile_id", )


async def test_delete_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_rule("test-instance_id", "test-rule_id", )
    mock_client.call.assert_called_once()


async def test_delete_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_rule("test-instance_id", "test-rule_id", )


async def test_delete_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_security_profile("test-instance_id", "test-security_profile_id", )
    mock_client.call.assert_called_once()


async def test_delete_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_security_profile("test-instance_id", "test-security_profile_id", )


async def test_delete_task_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_task_template("test-instance_id", "test-task_template_id", )
    mock_client.call.assert_called_once()


async def test_delete_task_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_task_template("test-instance_id", "test-task_template_id", )


async def test_delete_traffic_distribution_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_traffic_distribution_group("test-traffic_distribution_group_id", )
    mock_client.call.assert_called_once()


async def test_delete_traffic_distribution_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_traffic_distribution_group("test-traffic_distribution_group_id", )


async def test_delete_use_case(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_use_case("test-instance_id", "test-integration_association_id", "test-use_case_id", )
    mock_client.call.assert_called_once()


async def test_delete_use_case_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_use_case("test-instance_id", "test-integration_association_id", "test-use_case_id", )


async def test_delete_user_hierarchy_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_hierarchy_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", )


async def test_delete_view(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_view("test-instance_id", "test-view_id", )
    mock_client.call.assert_called_once()


async def test_delete_view_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_view("test-instance_id", "test-view_id", )


async def test_delete_view_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_view_version("test-instance_id", "test-view_id", 1, )
    mock_client.call.assert_called_once()


async def test_delete_view_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_view_version("test-instance_id", "test-view_id", 1, )


async def test_delete_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vocabulary("test-instance_id", "test-vocabulary_id", )
    mock_client.call.assert_called_once()


async def test_delete_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vocabulary("test-instance_id", "test-vocabulary_id", )


async def test_describe_agent_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_agent_status("test-instance_id", "test-agent_status_id", )
    mock_client.call.assert_called_once()


async def test_describe_agent_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_agent_status("test-instance_id", "test-agent_status_id", )


async def test_describe_authentication_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_authentication_profile("test-authentication_profile_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_authentication_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_authentication_profile("test-authentication_profile_id", "test-instance_id", )


async def test_describe_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_contact("test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_describe_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_contact("test-instance_id", "test-contact_id", )


async def test_describe_contact_evaluation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_contact_evaluation("test-instance_id", "test-evaluation_id", )
    mock_client.call.assert_called_once()


async def test_describe_contact_evaluation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_contact_evaluation("test-instance_id", "test-evaluation_id", )


async def test_describe_contact_flow_module(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_contact_flow_module("test-instance_id", "test-contact_flow_module_id", )
    mock_client.call.assert_called_once()


async def test_describe_contact_flow_module_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_contact_flow_module("test-instance_id", "test-contact_flow_module_id", )


async def test_describe_email_address(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_email_address("test-instance_id", "test-email_address_id", )
    mock_client.call.assert_called_once()


async def test_describe_email_address_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_email_address("test-instance_id", "test-email_address_id", )


async def test_describe_evaluation_form(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_evaluation_form("test-instance_id", "test-evaluation_form_id", )
    mock_client.call.assert_called_once()


async def test_describe_evaluation_form_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_evaluation_form("test-instance_id", "test-evaluation_form_id", )


async def test_describe_hours_of_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_hours_of_operation("test-instance_id", "test-hours_of_operation_id", )
    mock_client.call.assert_called_once()


async def test_describe_hours_of_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_hours_of_operation("test-instance_id", "test-hours_of_operation_id", )


async def test_describe_hours_of_operation_override(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", )
    mock_client.call.assert_called_once()


async def test_describe_hours_of_operation_override_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", )


async def test_describe_instance_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_attribute("test-instance_id", "test-attribute_type", )
    mock_client.call.assert_called_once()


async def test_describe_instance_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_attribute("test-instance_id", "test-attribute_type", )


async def test_describe_instance_storage_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_describe_instance_storage_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", )


async def test_describe_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_phone_number("test-phone_number_id", )
    mock_client.call.assert_called_once()


async def test_describe_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_phone_number("test-phone_number_id", )


async def test_describe_predefined_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_predefined_attribute("test-instance_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_describe_predefined_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_predefined_attribute("test-instance_id", "test-name", )


async def test_describe_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_prompt("test-instance_id", "test-prompt_id", )
    mock_client.call.assert_called_once()


async def test_describe_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_prompt("test-instance_id", "test-prompt_id", )


async def test_describe_quick_connect(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_quick_connect("test-instance_id", "test-quick_connect_id", )
    mock_client.call.assert_called_once()


async def test_describe_quick_connect_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_quick_connect("test-instance_id", "test-quick_connect_id", )


async def test_describe_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_rule("test-instance_id", "test-rule_id", )
    mock_client.call.assert_called_once()


async def test_describe_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_rule("test-instance_id", "test-rule_id", )


async def test_describe_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_security_profile("test-security_profile_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_profile("test-security_profile_id", "test-instance_id", )


async def test_describe_traffic_distribution_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_traffic_distribution_group("test-traffic_distribution_group_id", )
    mock_client.call.assert_called_once()


async def test_describe_traffic_distribution_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_traffic_distribution_group("test-traffic_distribution_group_id", )


async def test_describe_user_hierarchy_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_user_hierarchy_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", )


async def test_describe_user_hierarchy_structure(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_user_hierarchy_structure("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_describe_user_hierarchy_structure_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_hierarchy_structure("test-instance_id", )


async def test_describe_view(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_view("test-instance_id", "test-view_id", )
    mock_client.call.assert_called_once()


async def test_describe_view_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_view("test-instance_id", "test-view_id", )


async def test_describe_vocabulary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vocabulary("test-instance_id", "test-vocabulary_id", )
    mock_client.call.assert_called_once()


async def test_describe_vocabulary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vocabulary("test-instance_id", "test-vocabulary_id", )


async def test_disassociate_analytics_data_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_analytics_data_set("test-instance_id", "test-data_set_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_analytics_data_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_analytics_data_set("test-instance_id", "test-data_set_id", )


async def test_disassociate_approved_origin(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_approved_origin("test-instance_id", "test-origin", )
    mock_client.call.assert_called_once()


async def test_disassociate_approved_origin_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_approved_origin("test-instance_id", "test-origin", )


async def test_disassociate_bot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_bot("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_bot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_bot("test-instance_id", )


async def test_disassociate_email_address_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_email_address_alias("test-email_address_id", "test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_disassociate_email_address_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_email_address_alias("test-email_address_id", "test-instance_id", {}, )


async def test_disassociate_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_flow("test-instance_id", "test-resource_id", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_disassociate_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_flow("test-instance_id", "test-resource_id", "test-resource_type", )


async def test_disassociate_instance_storage_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_disassociate_instance_storage_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", )


async def test_disassociate_lambda_function(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_lambda_function("test-instance_id", "test-function_arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_lambda_function_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_lambda_function("test-instance_id", "test-function_arn", )


async def test_disassociate_lex_bot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_lex_bot("test-instance_id", "test-bot_name", "test-lex_region", )
    mock_client.call.assert_called_once()


async def test_disassociate_lex_bot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_lex_bot("test-instance_id", "test-bot_name", "test-lex_region", )


async def test_disassociate_phone_number_contact_flow(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_phone_number_contact_flow_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", )


async def test_disassociate_queue_quick_connects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_queue_quick_connects("test-instance_id", "test-queue_id", [], )
    mock_client.call.assert_called_once()


async def test_disassociate_queue_quick_connects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_queue_quick_connects("test-instance_id", "test-queue_id", [], )


async def test_disassociate_routing_profile_queues(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_routing_profile_queues("test-instance_id", "test-routing_profile_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_routing_profile_queues_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_routing_profile_queues("test-instance_id", "test-routing_profile_id", )


async def test_disassociate_security_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_security_key("test-instance_id", "test-association_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_security_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_security_key("test-instance_id", "test-association_id", )


async def test_disassociate_traffic_distribution_group_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_disassociate_traffic_distribution_group_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", )


async def test_disassociate_user_proficiencies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_user_proficiencies("test-instance_id", "test-user_id", [], )
    mock_client.call.assert_called_once()


async def test_disassociate_user_proficiencies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_user_proficiencies("test-instance_id", "test-user_id", [], )


async def test_dismiss_user_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await dismiss_user_contact("test-user_id", "test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_dismiss_user_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await dismiss_user_contact("test-user_id", "test-instance_id", "test-contact_id", )


async def test_get_attached_file(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_attached_file_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", )


async def test_get_contact_metrics(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_contact_metrics("test-instance_id", "test-contact_id", [], )
    mock_client.call.assert_called_once()


async def test_get_contact_metrics_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_contact_metrics("test-instance_id", "test-contact_id", [], )


async def test_get_current_user_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_current_user_data("test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_get_current_user_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_current_user_data("test-instance_id", {}, )


async def test_get_effective_hours_of_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_effective_hours_of_operations("test-instance_id", "test-hours_of_operation_id", "test-from_date", "test-to_date", )
    mock_client.call.assert_called_once()


async def test_get_effective_hours_of_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_effective_hours_of_operations("test-instance_id", "test-hours_of_operation_id", "test-from_date", "test-to_date", )


async def test_get_federation_token(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_federation_token("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_get_federation_token_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_federation_token("test-instance_id", )


async def test_get_flow_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_flow_association("test-instance_id", "test-resource_id", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_get_flow_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_flow_association("test-instance_id", "test-resource_id", "test-resource_type", )


async def test_get_metric_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_metric_data("test-instance_id", "test-start_time", "test-end_time", {}, [], )
    mock_client.call.assert_called_once()


async def test_get_metric_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_metric_data("test-instance_id", "test-start_time", "test-end_time", {}, [], )


async def test_get_metric_data_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_metric_data_v2("test-resource_arn", "test-start_time", "test-end_time", [], [], )
    mock_client.call.assert_called_once()


async def test_get_metric_data_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_metric_data_v2("test-resource_arn", "test-start_time", "test-end_time", [], [], )


async def test_get_prompt_file(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_prompt_file("test-instance_id", "test-prompt_id", )
    mock_client.call.assert_called_once()


async def test_get_prompt_file_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_prompt_file("test-instance_id", "test-prompt_id", )


async def test_get_task_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_task_template("test-instance_id", "test-task_template_id", )
    mock_client.call.assert_called_once()


async def test_get_task_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_task_template("test-instance_id", "test-task_template_id", )


async def test_get_traffic_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_traffic_distribution("test-id", )
    mock_client.call.assert_called_once()


async def test_get_traffic_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_traffic_distribution("test-id", )


async def test_import_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_phone_number("test-instance_id", "test-source_phone_number_arn", )
    mock_client.call.assert_called_once()


async def test_import_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_phone_number("test-instance_id", "test-source_phone_number_arn", )


async def test_list_agent_statuses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_agent_statuses("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_agent_statuses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_agent_statuses("test-instance_id", )


async def test_list_analytics_data_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_analytics_data_associations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_analytics_data_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_analytics_data_associations("test-instance_id", )


async def test_list_analytics_data_lake_data_sets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_analytics_data_lake_data_sets("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_analytics_data_lake_data_sets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_analytics_data_lake_data_sets("test-instance_id", )


async def test_list_approved_origins(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_approved_origins("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_approved_origins_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_approved_origins("test-instance_id", )


async def test_list_associated_contacts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_associated_contacts("test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_list_associated_contacts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_associated_contacts("test-instance_id", "test-contact_id", )


async def test_list_authentication_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_authentication_profiles("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_authentication_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_authentication_profiles("test-instance_id", )


async def test_list_bots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_bots("test-instance_id", "test-lex_version", )
    mock_client.call.assert_called_once()


async def test_list_bots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_bots("test-instance_id", "test-lex_version", )


async def test_list_contact_evaluations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_contact_evaluations("test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_list_contact_evaluations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_contact_evaluations("test-instance_id", "test-contact_id", )


async def test_list_contact_flow_modules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_contact_flow_modules("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_contact_flow_modules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_contact_flow_modules("test-instance_id", )


async def test_list_contact_flow_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_contact_flow_versions("test-instance_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_list_contact_flow_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_contact_flow_versions("test-instance_id", "test-contact_flow_id", )


async def test_list_contact_references(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_contact_references("test-instance_id", "test-contact_id", [], )
    mock_client.call.assert_called_once()


async def test_list_contact_references_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_contact_references("test-instance_id", "test-contact_id", [], )


async def test_list_default_vocabularies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_default_vocabularies("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_default_vocabularies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_default_vocabularies("test-instance_id", )


async def test_list_evaluation_form_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_evaluation_form_versions("test-instance_id", "test-evaluation_form_id", )
    mock_client.call.assert_called_once()


async def test_list_evaluation_form_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_evaluation_form_versions("test-instance_id", "test-evaluation_form_id", )


async def test_list_evaluation_forms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_evaluation_forms("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_evaluation_forms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_evaluation_forms("test-instance_id", )


async def test_list_flow_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_flow_associations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_flow_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_flow_associations("test-instance_id", )


async def test_list_hours_of_operation_overrides(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_hours_of_operation_overrides("test-instance_id", "test-hours_of_operation_id", )
    mock_client.call.assert_called_once()


async def test_list_hours_of_operation_overrides_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_hours_of_operation_overrides("test-instance_id", "test-hours_of_operation_id", )


async def test_list_hours_of_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_hours_of_operations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_hours_of_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_hours_of_operations("test-instance_id", )


async def test_list_instance_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instance_attributes("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_instance_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instance_attributes("test-instance_id", )


async def test_list_instance_storage_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instance_storage_configs("test-instance_id", "test-resource_type", )
    mock_client.call.assert_called_once()


async def test_list_instance_storage_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instance_storage_configs("test-instance_id", "test-resource_type", )


async def test_list_integration_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_integration_associations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_integration_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_integration_associations("test-instance_id", )


async def test_list_lambda_functions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_lambda_functions("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_lambda_functions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_lambda_functions("test-instance_id", )


async def test_list_lex_bots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_lex_bots("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_lex_bots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_lex_bots("test-instance_id", )


async def test_list_phone_numbers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_phone_numbers("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_phone_numbers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_phone_numbers("test-instance_id", )


async def test_list_phone_numbers_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_phone_numbers_v2()
    mock_client.call.assert_called_once()


async def test_list_phone_numbers_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_phone_numbers_v2()


async def test_list_predefined_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_predefined_attributes("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_predefined_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_predefined_attributes("test-instance_id", )


async def test_list_prompts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_prompts("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_prompts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_prompts("test-instance_id", )


async def test_list_queue_quick_connects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_queue_quick_connects("test-instance_id", "test-queue_id", )
    mock_client.call.assert_called_once()


async def test_list_queue_quick_connects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_queue_quick_connects("test-instance_id", "test-queue_id", )


async def test_list_quick_connects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_quick_connects("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_quick_connects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_quick_connects("test-instance_id", )


async def test_list_realtime_contact_analysis_segments_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_realtime_contact_analysis_segments_v2("test-instance_id", "test-contact_id", "test-output_type", [], )
    mock_client.call.assert_called_once()


async def test_list_realtime_contact_analysis_segments_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_realtime_contact_analysis_segments_v2("test-instance_id", "test-contact_id", "test-output_type", [], )


async def test_list_routing_profile_manual_assignment_queues(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_routing_profile_manual_assignment_queues("test-instance_id", "test-routing_profile_id", )
    mock_client.call.assert_called_once()


async def test_list_routing_profile_manual_assignment_queues_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_routing_profile_manual_assignment_queues("test-instance_id", "test-routing_profile_id", )


async def test_list_routing_profile_queues(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_routing_profile_queues("test-instance_id", "test-routing_profile_id", )
    mock_client.call.assert_called_once()


async def test_list_routing_profile_queues_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_routing_profile_queues("test-instance_id", "test-routing_profile_id", )


async def test_list_rules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_rules("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_rules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_rules("test-instance_id", )


async def test_list_security_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_keys("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_security_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_keys("test-instance_id", )


async def test_list_security_profile_applications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_profile_applications("test-security_profile_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_security_profile_applications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_profile_applications("test-security_profile_id", "test-instance_id", )


async def test_list_security_profile_permissions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_profile_permissions("test-security_profile_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_security_profile_permissions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_profile_permissions("test-security_profile_id", "test-instance_id", )


async def test_list_security_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_security_profiles("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_security_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_profiles("test-instance_id", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_task_templates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_task_templates("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_task_templates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_task_templates("test-instance_id", )


async def test_list_traffic_distribution_group_users(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_distribution_group_users("test-traffic_distribution_group_id", )
    mock_client.call.assert_called_once()


async def test_list_traffic_distribution_group_users_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_distribution_group_users("test-traffic_distribution_group_id", )


async def test_list_traffic_distribution_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_traffic_distribution_groups()
    mock_client.call.assert_called_once()


async def test_list_traffic_distribution_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_traffic_distribution_groups()


async def test_list_use_cases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_use_cases("test-instance_id", "test-integration_association_id", )
    mock_client.call.assert_called_once()


async def test_list_use_cases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_use_cases("test-instance_id", "test-integration_association_id", )


async def test_list_user_hierarchy_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_user_hierarchy_groups("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_user_hierarchy_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_hierarchy_groups("test-instance_id", )


async def test_list_user_proficiencies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_user_proficiencies("test-instance_id", "test-user_id", )
    mock_client.call.assert_called_once()


async def test_list_user_proficiencies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_proficiencies("test-instance_id", "test-user_id", )


async def test_list_view_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_view_versions("test-instance_id", "test-view_id", )
    mock_client.call.assert_called_once()


async def test_list_view_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_view_versions("test-instance_id", "test-view_id", )


async def test_list_views(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_views("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_list_views_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_views("test-instance_id", )


async def test_monitor_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await monitor_contact("test-instance_id", "test-contact_id", "test-user_id", )
    mock_client.call.assert_called_once()


async def test_monitor_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await monitor_contact("test-instance_id", "test-contact_id", "test-user_id", )


async def test_pause_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await pause_contact("test-contact_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_pause_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await pause_contact("test-contact_id", "test-instance_id", )


async def test_put_user_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_user_status("test-user_id", "test-instance_id", "test-agent_status_id", )
    mock_client.call.assert_called_once()


async def test_put_user_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_user_status("test-user_id", "test-instance_id", "test-agent_status_id", )


async def test_release_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await release_phone_number("test-phone_number_id", )
    mock_client.call.assert_called_once()


async def test_release_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await release_phone_number("test-phone_number_id", )


async def test_replicate_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await replicate_instance("test-instance_id", "test-replica_region", "test-replica_alias", )
    mock_client.call.assert_called_once()


async def test_replicate_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await replicate_instance("test-instance_id", "test-replica_region", "test-replica_alias", )


async def test_resume_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_contact("test-contact_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_resume_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_contact("test-contact_id", "test-instance_id", )


async def test_resume_contact_recording(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", )
    mock_client.call.assert_called_once()


async def test_resume_contact_recording_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", )


async def test_search_agent_statuses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_agent_statuses("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_agent_statuses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_agent_statuses("test-instance_id", )


async def test_search_available_phone_numbers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_available_phone_numbers("test-phone_number_country_code", "test-phone_number_type", )
    mock_client.call.assert_called_once()


async def test_search_available_phone_numbers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_available_phone_numbers("test-phone_number_country_code", "test-phone_number_type", )


async def test_search_contact_evaluations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_contact_evaluations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_contact_evaluations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_contact_evaluations("test-instance_id", )


async def test_search_contact_flow_modules(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_contact_flow_modules("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_contact_flow_modules_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_contact_flow_modules("test-instance_id", )


async def test_search_contact_flows(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_contact_flows("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_contact_flows_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_contact_flows("test-instance_id", )


async def test_search_contacts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_contacts("test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_search_contacts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_contacts("test-instance_id", {}, )


async def test_search_email_addresses(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_email_addresses("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_email_addresses_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_email_addresses("test-instance_id", )


async def test_search_evaluation_forms(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_evaluation_forms("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_evaluation_forms_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_evaluation_forms("test-instance_id", )


async def test_search_hours_of_operation_overrides(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_hours_of_operation_overrides("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_hours_of_operation_overrides_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_hours_of_operation_overrides("test-instance_id", )


async def test_search_hours_of_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_hours_of_operations("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_hours_of_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_hours_of_operations("test-instance_id", )


async def test_search_predefined_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_predefined_attributes("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_predefined_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_predefined_attributes("test-instance_id", )


async def test_search_prompts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_prompts("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_prompts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_prompts("test-instance_id", )


async def test_search_queues(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_queues("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_queues_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_queues("test-instance_id", )


async def test_search_quick_connects(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_quick_connects("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_quick_connects_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_quick_connects("test-instance_id", )


async def test_search_resource_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_resource_tags("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_resource_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_resource_tags("test-instance_id", )


async def test_search_routing_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_routing_profiles("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_routing_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_routing_profiles("test-instance_id", )


async def test_search_security_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_security_profiles("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_security_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_security_profiles("test-instance_id", )


async def test_search_user_hierarchy_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_user_hierarchy_groups("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_user_hierarchy_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_user_hierarchy_groups("test-instance_id", )


async def test_search_users(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_users("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_users_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_users("test-instance_id", )


async def test_search_vocabularies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await search_vocabularies("test-instance_id", )
    mock_client.call.assert_called_once()


async def test_search_vocabularies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await search_vocabularies("test-instance_id", )


async def test_send_chat_integration_event(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_chat_integration_event("test-source_id", "test-destination_id", {}, )
    mock_client.call.assert_called_once()


async def test_send_chat_integration_event_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_chat_integration_event("test-source_id", "test-destination_id", {}, )


async def test_send_outbound_email(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await send_outbound_email("test-instance_id", {}, {}, {}, "test-traffic_type", )
    mock_client.call.assert_called_once()


async def test_send_outbound_email_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await send_outbound_email("test-instance_id", {}, {}, {}, "test-traffic_type", )


async def test_start_attached_file_upload(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_attached_file_upload("test-instance_id", "test-file_name", 1, "test-file_use_case_type", "test-associated_resource_arn", )
    mock_client.call.assert_called_once()


async def test_start_attached_file_upload_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_attached_file_upload("test-instance_id", "test-file_name", 1, "test-file_use_case_type", "test-associated_resource_arn", )


async def test_start_contact_evaluation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_contact_evaluation("test-instance_id", "test-contact_id", "test-evaluation_form_id", )
    mock_client.call.assert_called_once()


async def test_start_contact_evaluation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_contact_evaluation("test-instance_id", "test-contact_id", "test-evaluation_form_id", )


async def test_start_contact_recording(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", {}, )
    mock_client.call.assert_called_once()


async def test_start_contact_recording_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", {}, )


async def test_start_contact_streaming(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_contact_streaming("test-instance_id", "test-contact_id", {}, "test-client_token", )
    mock_client.call.assert_called_once()


async def test_start_contact_streaming_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_contact_streaming("test-instance_id", "test-contact_id", {}, "test-client_token", )


async def test_start_email_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_email_contact("test-instance_id", {}, "test-destination_email_address", {}, )
    mock_client.call.assert_called_once()


async def test_start_email_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_email_contact("test-instance_id", {}, "test-destination_email_address", {}, )


async def test_start_outbound_chat_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_outbound_chat_contact({}, {}, "test-instance_id", {}, "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_start_outbound_chat_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_outbound_chat_contact({}, {}, "test-instance_id", {}, "test-contact_flow_id", )


async def test_start_outbound_email_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_outbound_email_contact("test-instance_id", "test-contact_id", {}, {}, )
    mock_client.call.assert_called_once()


async def test_start_outbound_email_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_outbound_email_contact("test-instance_id", "test-contact_id", {}, {}, )


async def test_start_screen_sharing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_screen_sharing("test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_start_screen_sharing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_screen_sharing("test-instance_id", "test-contact_id", )


async def test_start_web_rtc_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_web_rtc_contact("test-contact_flow_id", "test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_start_web_rtc_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_web_rtc_contact("test-contact_flow_id", "test-instance_id", {}, )


async def test_stop_contact_recording(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", )
    mock_client.call.assert_called_once()


async def test_stop_contact_recording_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", )


async def test_stop_contact_streaming(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_contact_streaming("test-instance_id", "test-contact_id", "test-streaming_id", )
    mock_client.call.assert_called_once()


async def test_stop_contact_streaming_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_contact_streaming("test-instance_id", "test-contact_id", "test-streaming_id", )


async def test_submit_contact_evaluation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await submit_contact_evaluation("test-instance_id", "test-evaluation_id", )
    mock_client.call.assert_called_once()


async def test_submit_contact_evaluation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await submit_contact_evaluation("test-instance_id", "test-evaluation_id", )


async def test_suspend_contact_recording(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await suspend_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", )
    mock_client.call.assert_called_once()


async def test_suspend_contact_recording_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await suspend_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", )


async def test_tag_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_contact("test-contact_id", "test-instance_id", {}, )
    mock_client.call.assert_called_once()


async def test_tag_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_contact("test-contact_id", "test-instance_id", {}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_transfer_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await transfer_contact("test-instance_id", "test-contact_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_transfer_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await transfer_contact("test-instance_id", "test-contact_id", "test-contact_flow_id", )


async def test_untag_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_contact("test-contact_id", "test-instance_id", [], )
    mock_client.call.assert_called_once()


async def test_untag_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_contact("test-contact_id", "test-instance_id", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_agent_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_agent_status("test-instance_id", "test-agent_status_id", )
    mock_client.call.assert_called_once()


async def test_update_agent_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_agent_status("test-instance_id", "test-agent_status_id", )


async def test_update_authentication_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_authentication_profile("test-authentication_profile_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_authentication_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_authentication_profile("test-authentication_profile_id", "test-instance_id", )


async def test_update_contact(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact("test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_update_contact_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact("test-instance_id", "test-contact_id", )


async def test_update_contact_evaluation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_evaluation("test-instance_id", "test-evaluation_id", )
    mock_client.call.assert_called_once()


async def test_update_contact_evaluation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_evaluation("test-instance_id", "test-evaluation_id", )


async def test_update_contact_flow_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_flow_metadata("test-instance_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_update_contact_flow_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_flow_metadata("test-instance_id", "test-contact_flow_id", )


async def test_update_contact_flow_module_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_flow_module_content("test-instance_id", "test-contact_flow_module_id", "test-content", )
    mock_client.call.assert_called_once()


async def test_update_contact_flow_module_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_flow_module_content("test-instance_id", "test-contact_flow_module_id", "test-content", )


async def test_update_contact_flow_module_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_flow_module_metadata("test-instance_id", "test-contact_flow_module_id", )
    mock_client.call.assert_called_once()


async def test_update_contact_flow_module_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_flow_module_metadata("test-instance_id", "test-contact_flow_module_id", )


async def test_update_contact_flow_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_flow_name("test-instance_id", "test-contact_flow_id", )
    mock_client.call.assert_called_once()


async def test_update_contact_flow_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_flow_name("test-instance_id", "test-contact_flow_id", )


async def test_update_contact_routing_data(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_routing_data("test-instance_id", "test-contact_id", )
    mock_client.call.assert_called_once()


async def test_update_contact_routing_data_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_routing_data("test-instance_id", "test-contact_id", )


async def test_update_contact_schedule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contact_schedule("test-instance_id", "test-contact_id", "test-scheduled_time", )
    mock_client.call.assert_called_once()


async def test_update_contact_schedule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contact_schedule("test-instance_id", "test-contact_id", "test-scheduled_time", )


async def test_update_email_address_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_email_address_metadata("test-instance_id", "test-email_address_id", )
    mock_client.call.assert_called_once()


async def test_update_email_address_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_email_address_metadata("test-instance_id", "test-email_address_id", )


async def test_update_evaluation_form(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, "test-title", [], )
    mock_client.call.assert_called_once()


async def test_update_evaluation_form_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, "test-title", [], )


async def test_update_hours_of_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_hours_of_operation("test-instance_id", "test-hours_of_operation_id", )
    mock_client.call.assert_called_once()


async def test_update_hours_of_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_hours_of_operation("test-instance_id", "test-hours_of_operation_id", )


async def test_update_hours_of_operation_override(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", )
    mock_client.call.assert_called_once()


async def test_update_hours_of_operation_override_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", )


async def test_update_instance_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_instance_attribute("test-instance_id", "test-attribute_type", "test-value", )
    mock_client.call.assert_called_once()


async def test_update_instance_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_instance_attribute("test-instance_id", "test-attribute_type", "test-value", )


async def test_update_instance_storage_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", {}, )
    mock_client.call.assert_called_once()


async def test_update_instance_storage_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", {}, )


async def test_update_participant_authentication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_participant_authentication("test-state", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_participant_authentication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_participant_authentication("test-state", "test-instance_id", )


async def test_update_participant_role_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_participant_role_config("test-instance_id", "test-contact_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_participant_role_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_participant_role_config("test-instance_id", "test-contact_id", {}, )


async def test_update_phone_number(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_phone_number("test-phone_number_id", )
    mock_client.call.assert_called_once()


async def test_update_phone_number_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_phone_number("test-phone_number_id", )


async def test_update_phone_number_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_phone_number_metadata("test-phone_number_id", )
    mock_client.call.assert_called_once()


async def test_update_phone_number_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_phone_number_metadata("test-phone_number_id", )


async def test_update_predefined_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_predefined_attribute("test-instance_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_predefined_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_predefined_attribute("test-instance_id", "test-name", )


async def test_update_prompt(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_prompt("test-instance_id", "test-prompt_id", )
    mock_client.call.assert_called_once()


async def test_update_prompt_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_prompt("test-instance_id", "test-prompt_id", )


async def test_update_queue_hours_of_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_queue_hours_of_operation("test-instance_id", "test-queue_id", "test-hours_of_operation_id", )
    mock_client.call.assert_called_once()


async def test_update_queue_hours_of_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_queue_hours_of_operation("test-instance_id", "test-queue_id", "test-hours_of_operation_id", )


async def test_update_queue_max_contacts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_queue_max_contacts("test-instance_id", "test-queue_id", )
    mock_client.call.assert_called_once()


async def test_update_queue_max_contacts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_queue_max_contacts("test-instance_id", "test-queue_id", )


async def test_update_queue_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_queue_name("test-instance_id", "test-queue_id", )
    mock_client.call.assert_called_once()


async def test_update_queue_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_queue_name("test-instance_id", "test-queue_id", )


async def test_update_queue_outbound_caller_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_queue_outbound_caller_config("test-instance_id", "test-queue_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_queue_outbound_caller_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_queue_outbound_caller_config("test-instance_id", "test-queue_id", {}, )


async def test_update_queue_outbound_email_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_queue_outbound_email_config("test-instance_id", "test-queue_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_queue_outbound_email_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_queue_outbound_email_config("test-instance_id", "test-queue_id", {}, )


async def test_update_quick_connect_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_quick_connect_config("test-instance_id", "test-quick_connect_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_quick_connect_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_quick_connect_config("test-instance_id", "test-quick_connect_id", {}, )


async def test_update_quick_connect_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_quick_connect_name("test-instance_id", "test-quick_connect_id", )
    mock_client.call.assert_called_once()


async def test_update_quick_connect_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_quick_connect_name("test-instance_id", "test-quick_connect_id", )


async def test_update_routing_profile_agent_availability_timer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_routing_profile_agent_availability_timer("test-instance_id", "test-routing_profile_id", "test-agent_availability_timer", )
    mock_client.call.assert_called_once()


async def test_update_routing_profile_agent_availability_timer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_routing_profile_agent_availability_timer("test-instance_id", "test-routing_profile_id", "test-agent_availability_timer", )


async def test_update_routing_profile_concurrency(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_routing_profile_concurrency("test-instance_id", "test-routing_profile_id", [], )
    mock_client.call.assert_called_once()


async def test_update_routing_profile_concurrency_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_routing_profile_concurrency("test-instance_id", "test-routing_profile_id", [], )


async def test_update_routing_profile_default_outbound_queue(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_routing_profile_default_outbound_queue("test-instance_id", "test-routing_profile_id", "test-default_outbound_queue_id", )
    mock_client.call.assert_called_once()


async def test_update_routing_profile_default_outbound_queue_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_routing_profile_default_outbound_queue("test-instance_id", "test-routing_profile_id", "test-default_outbound_queue_id", )


async def test_update_routing_profile_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_routing_profile_name("test-instance_id", "test-routing_profile_id", )
    mock_client.call.assert_called_once()


async def test_update_routing_profile_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_routing_profile_name("test-instance_id", "test-routing_profile_id", )


async def test_update_routing_profile_queues(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_routing_profile_queues("test-instance_id", "test-routing_profile_id", [], )
    mock_client.call.assert_called_once()


async def test_update_routing_profile_queues_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_routing_profile_queues("test-instance_id", "test-routing_profile_id", [], )


async def test_update_rule(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_rule("test-rule_id", "test-instance_id", "test-name", "test-function", [], "test-publish_status", )
    mock_client.call.assert_called_once()


async def test_update_rule_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_rule("test-rule_id", "test-instance_id", "test-name", "test-function", [], "test-publish_status", )


async def test_update_security_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_security_profile("test-security_profile_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_security_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_security_profile("test-security_profile_id", "test-instance_id", )


async def test_update_task_template(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_task_template("test-task_template_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_task_template_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_task_template("test-task_template_id", "test-instance_id", )


async def test_update_traffic_distribution(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_traffic_distribution("test-id", )
    mock_client.call.assert_called_once()


async def test_update_traffic_distribution_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_traffic_distribution("test-id", )


async def test_update_user_hierarchy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_hierarchy("test-user_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_user_hierarchy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_hierarchy("test-user_id", "test-instance_id", )


async def test_update_user_hierarchy_group_name(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_hierarchy_group_name("test-name", "test-hierarchy_group_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_user_hierarchy_group_name_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_hierarchy_group_name("test-name", "test-hierarchy_group_id", "test-instance_id", )


async def test_update_user_hierarchy_structure(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_hierarchy_structure({}, "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_user_hierarchy_structure_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_hierarchy_structure({}, "test-instance_id", )


async def test_update_user_identity_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_identity_info({}, "test-user_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_user_identity_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_identity_info({}, "test-user_id", "test-instance_id", )


async def test_update_user_phone_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_phone_config({}, "test-user_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_user_phone_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_phone_config({}, "test-user_id", "test-instance_id", )


async def test_update_user_proficiencies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_proficiencies("test-instance_id", "test-user_id", [], )
    mock_client.call.assert_called_once()


async def test_update_user_proficiencies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_proficiencies("test-instance_id", "test-user_id", [], )


async def test_update_user_security_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user_security_profiles([], "test-user_id", "test-instance_id", )
    mock_client.call.assert_called_once()


async def test_update_user_security_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_security_profiles([], "test-user_id", "test-instance_id", )


async def test_update_view_content(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_view_content("test-instance_id", "test-view_id", "test-status", {}, )
    mock_client.call.assert_called_once()


async def test_update_view_content_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_view_content("test-instance_id", "test-view_id", "test-status", {}, )


async def test_update_view_metadata(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_view_metadata("test-instance_id", "test-view_id", )
    mock_client.call.assert_called_once()


async def test_update_view_metadata_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.connect.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_view_metadata("test-instance_id", "test-view_id", )


@pytest.mark.asyncio
async def test_list_contact_flows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_contact_flows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_contact_flows("test-instance_id", contact_flow_types="test-contact_flow_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_queues("test-instance_id", queue_types="test-queue_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_current_metric_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import get_current_metric_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await get_current_metric_data("test-instance_id", [{}], "test-current_metrics", groupings="test-groupings", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_analytics_data_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_analytics_data_set("test-instance_id", "test-data_set_id", target_account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_approved_origin_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_approved_origin
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_approved_origin("test-instance_id", "test-origin", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_bot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_bot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_bot("test-instance_id", lex_bot="test-lex_bot", lex_v2_bot="test-lex_v2_bot", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_default_vocabulary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_default_vocabulary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_default_vocabulary("test-instance_id", "test-language_code", vocabulary_id="test-vocabulary_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_email_address_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_email_address_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_email_address_alias("test-email_address_id", "test-instance_id", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_instance_storage_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_instance_storage_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_instance_storage_config("test-instance_id", "test-resource_type", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_lambda_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_lambda_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_lambda_function("test-instance_id", "test-function_arn", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_lex_bot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_lex_bot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_lex_bot("test-instance_id", "test-lex_bot", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_routing_profile_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_routing_profile_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_routing_profile_queues("test-instance_id", "test-routing_profile_id", queue_configs={}, manual_assignment_queue_configs={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_security_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import associate_security_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await associate_security_key("test-instance_id", "test-key", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_associate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import batch_associate_analytics_data_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await batch_associate_analytics_data_set("test-instance_id", "test-data_set_ids", target_account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_disassociate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import batch_disassociate_analytics_data_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await batch_disassociate_analytics_data_set("test-instance_id", "test-data_set_ids", target_account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_flow_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import batch_get_flow_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await batch_get_flow_association("test-instance_id", "test-resource_ids", resource_type="test-resource_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_put_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import batch_put_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await batch_put_contact("test-instance_id", "test-contact_data_request_list", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_claim_phone_number_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import claim_phone_number
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await claim_phone_number("test-phone_number", target_arn="test-target_arn", instance_id="test-instance_id", phone_number_description="test-phone_number_description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_agent_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_agent_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_agent_status("test-instance_id", "test-name", "test-state", description="test-description", display_order="test-display_order", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_contact("test-instance_id", "test-channel", "test-initiation_method", client_token="test-client_token", related_contact_id="test-related_contact_id", attributes="test-attributes", references="test-references", expiry_duration_in_minutes=1, user_info="test-user_info", initiate_as="test-initiate_as", name="test-name", description="test-description", segment_attributes="test-segment_attributes", previous_contact_id="test-previous_contact_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_contact_flow_module_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_contact_flow_module
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_contact_flow_module("test-instance_id", "test-name", "test-content", description="test-description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_contact_flow_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_contact_flow_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_contact_flow_version("test-instance_id", "test-contact_flow_id", description="test-description", flow_content_sha256="test-flow_content_sha256", contact_flow_version="test-contact_flow_version", last_modified_time="test-last_modified_time", last_modified_region="test-last_modified_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_email_address_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_email_address
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_email_address("test-instance_id", "test-email_address", description="test-description", display_name="test-display_name", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_evaluation_form_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_evaluation_form
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_evaluation_form("test-instance_id", "test-title", "test-items", description="test-description", scoring_strategy="test-scoring_strategy", auto_evaluation_configuration=True, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_hours_of_operation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_hours_of_operation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_hours_of_operation("test-instance_id", "test-name", "test-time_zone", {}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_hours_of_operation_override_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_hours_of_operation_override
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-name", {}, "test-effective_from", "test-effective_till", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_integration_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_integration_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_integration_association("test-instance_id", "test-integration_type", "test-integration_arn", source_application_url="test-source_application_url", source_application_name="test-source_application_name", source_type="test-source_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_participant_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_participant
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_participant("test-instance_id", "test-contact_id", "test-participant_details", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_persistent_contact_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_persistent_contact_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_persistent_contact_association("test-instance_id", "test-initial_contact_id", "test-rehydration_type", "test-source_contact_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_predefined_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_predefined_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_predefined_attribute("test-instance_id", "test-name", values="test-values", purposes="test-purposes", attribute_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_prompt_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_prompt
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_prompt("test-instance_id", "test-name", "test-s3_uri", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_push_notification_registration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_push_notification_registration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_push_notification_registration("test-instance_id", "test-pinpoint_app_arn", "test-device_token", "test-device_type", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_quick_connect_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_quick_connect
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_quick_connect("test-instance_id", "test-name", {}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_rule("test-instance_id", "test-name", "test-trigger_event_source", "test-function", "test-actions", True, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_security_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_security_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_security_profile("test-security_profile_name", "test-instance_id", description="test-description", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], allowed_access_control_tags=True, tag_restricted_resources="test-tag_restricted_resources", applications="test-applications", hierarchy_restricted_resources="test-hierarchy_restricted_resources", allowed_access_control_hierarchy_group_id=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_task_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_task_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_task_template("test-instance_id", "test-name", "test-fields", description="test-description", contact_flow_id="test-contact_flow_id", self_assign_flow_id="test-self_assign_flow_id", constraints="test-constraints", defaults="test-defaults", status="test-status", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_traffic_distribution_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_traffic_distribution_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_traffic_distribution_group("test-name", "test-instance_id", description="test-description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_use_case_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_use_case
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_use_case("test-instance_id", "test-integration_association_id", True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_hierarchy_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_user_hierarchy_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_user_hierarchy_group("test-name", "test-instance_id", parent_group_id="test-parent_group_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_view_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_view
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_view("test-instance_id", "test-status", "test-content", "test-name", client_token="test-client_token", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_view_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_view_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_view_version("test-instance_id", "test-view_id", version_description="test-version_description", view_content_sha256="test-view_content_sha256", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vocabulary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_vocabulary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_vocabulary("test-instance_id", "test-vocabulary_name", "test-language_code", "test-content", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_evaluation_form_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import delete_evaluation_form
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await delete_evaluation_form("test-instance_id", "test-evaluation_form_id", evaluation_form_version="test-evaluation_form_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_evaluation_form_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import describe_evaluation_form
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await describe_evaluation_form("test-instance_id", "test-evaluation_form_id", evaluation_form_version="test-evaluation_form_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_analytics_data_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_analytics_data_set("test-instance_id", "test-data_set_id", target_account_id=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_approved_origin_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_approved_origin
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_approved_origin("test-instance_id", "test-origin", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_bot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_bot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_bot("test-instance_id", lex_bot="test-lex_bot", lex_v2_bot="test-lex_v2_bot", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_email_address_alias_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_email_address_alias
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_email_address_alias("test-email_address_id", "test-instance_id", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_instance_storage_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_instance_storage_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_lambda_function_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_lambda_function
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_lambda_function("test-instance_id", "test-function_arn", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_lex_bot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_lex_bot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_lex_bot("test-instance_id", "test-bot_name", "test-lex_region", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_routing_profile_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_routing_profile_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_routing_profile_queues("test-instance_id", "test-routing_profile_id", queue_references="test-queue_references", manual_assignment_queue_references="test-manual_assignment_queue_references", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_security_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import disassociate_security_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await disassociate_security_key("test-instance_id", "test-association_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_attached_file_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import get_attached_file
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await get_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", url_expiry_in_seconds="test-url_expiry_in_seconds", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_current_user_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import get_current_user_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await get_current_user_data("test-instance_id", [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_metric_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import get_metric_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await get_metric_data("test-instance_id", "test-start_time", "test-end_time", [{}], "test-historical_metrics", groupings="test-groupings", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_metric_data_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import get_metric_data_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await get_metric_data_v2("test-resource_arn", "test-start_time", "test-end_time", [{}], "test-metrics", interval="test-interval", groupings="test-groupings", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_task_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import get_task_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await get_task_template("test-instance_id", "test-task_template_id", snapshot_version="test-snapshot_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_phone_number_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import import_phone_number
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await import_phone_number("test-instance_id", "test-source_phone_number_arn", phone_number_description="test-phone_number_description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_agent_statuses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_agent_statuses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_agent_statuses("test-instance_id", next_token="test-next_token", max_results=1, agent_status_types="test-agent_status_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_analytics_data_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_analytics_data_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_analytics_data_associations("test-instance_id", data_set_id="test-data_set_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_analytics_data_lake_data_sets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_analytics_data_lake_data_sets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_analytics_data_lake_data_sets("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_approved_origins_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_approved_origins
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_approved_origins("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_associated_contacts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_associated_contacts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_associated_contacts("test-instance_id", "test-contact_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_authentication_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_authentication_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_authentication_profiles("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_bots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_bots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_bots("test-instance_id", "test-lex_version", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contact_evaluations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_contact_evaluations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_contact_evaluations("test-instance_id", "test-contact_id", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contact_flow_modules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_contact_flow_modules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_contact_flow_modules("test-instance_id", next_token="test-next_token", max_results=1, contact_flow_module_state="test-contact_flow_module_state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contact_flow_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_contact_flow_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_contact_flow_versions("test-instance_id", "test-contact_flow_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contact_references_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_contact_references
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_contact_references("test-instance_id", "test-contact_id", "test-reference_types", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_default_vocabularies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_default_vocabularies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_default_vocabularies("test-instance_id", language_code="test-language_code", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_evaluation_form_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_evaluation_form_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_evaluation_form_versions("test-instance_id", "test-evaluation_form_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_evaluation_forms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_evaluation_forms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_evaluation_forms("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_flow_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_flow_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_flow_associations("test-instance_id", resource_type="test-resource_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_hours_of_operation_overrides_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_hours_of_operation_overrides
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_hours_of_operation_overrides("test-instance_id", "test-hours_of_operation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_hours_of_operations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_hours_of_operations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_hours_of_operations("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instance_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_instance_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_instance_attributes("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instance_storage_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_instance_storage_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_instance_storage_configs("test-instance_id", "test-resource_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_integration_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_integration_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_integration_associations("test-instance_id", integration_type="test-integration_type", next_token="test-next_token", max_results=1, integration_arn="test-integration_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_lambda_functions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_lambda_functions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_lambda_functions("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_lex_bots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_lex_bots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_lex_bots("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_phone_numbers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_phone_numbers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_phone_numbers("test-instance_id", phone_number_types="test-phone_number_types", phone_number_country_codes=1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_phone_numbers_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_phone_numbers_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_phone_numbers_v2(target_arn="test-target_arn", instance_id="test-instance_id", max_results=1, next_token="test-next_token", phone_number_country_codes=1, phone_number_types="test-phone_number_types", phone_number_prefix="test-phone_number_prefix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_predefined_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_predefined_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_predefined_attributes("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_prompts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_prompts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_prompts("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_queue_quick_connects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_queue_quick_connects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_queue_quick_connects("test-instance_id", "test-queue_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_quick_connects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_quick_connects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_quick_connects("test-instance_id", next_token="test-next_token", max_results=1, quick_connect_types="test-quick_connect_types", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_realtime_contact_analysis_segments_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_realtime_contact_analysis_segments_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_realtime_contact_analysis_segments_v2("test-instance_id", "test-contact_id", "test-output_type", "test-segment_types", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_routing_profile_manual_assignment_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_routing_profile_manual_assignment_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_routing_profile_manual_assignment_queues("test-instance_id", "test-routing_profile_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_routing_profile_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_routing_profile_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_routing_profile_queues("test-instance_id", "test-routing_profile_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_rules("test-instance_id", publish_status=True, event_source_name="test-event_source_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_security_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_security_keys("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_profile_applications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_security_profile_applications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_security_profile_applications("test-security_profile_id", "test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_profile_permissions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_security_profile_permissions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_security_profile_permissions("test-security_profile_id", "test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_security_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_security_profiles("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_task_templates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_task_templates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_task_templates("test-instance_id", next_token="test-next_token", max_results=1, status="test-status", name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_distribution_group_users_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_traffic_distribution_group_users
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_traffic_distribution_group_users("test-traffic_distribution_group_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_traffic_distribution_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_traffic_distribution_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_traffic_distribution_groups(max_results=1, next_token="test-next_token", instance_id="test-instance_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_use_cases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_use_cases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_use_cases("test-instance_id", "test-integration_association_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_hierarchy_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_user_hierarchy_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_user_hierarchy_groups("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_proficiencies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_user_proficiencies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_user_proficiencies("test-instance_id", "test-user_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_view_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_view_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_view_versions("test-instance_id", "test-view_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_views_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import list_views
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await list_views("test-instance_id", type_value="test-type_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_monitor_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import monitor_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await monitor_contact("test-instance_id", "test-contact_id", "test-user_id", allowed_monitor_capabilities=True, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_pause_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import pause_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await pause_contact("test-contact_id", "test-instance_id", contact_flow_id="test-contact_flow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_release_phone_number_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import release_phone_number
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await release_phone_number("test-phone_number_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_replicate_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import replicate_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await replicate_instance("test-instance_id", "test-replica_region", "test-replica_alias", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_resume_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import resume_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await resume_contact("test-contact_id", "test-instance_id", contact_flow_id="test-contact_flow_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_resume_contact_recording_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import resume_contact_recording
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await resume_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", contact_recording_type="test-contact_recording_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_agent_statuses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_agent_statuses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_agent_statuses("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_available_phone_numbers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_available_phone_numbers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_available_phone_numbers(1, "test-phone_number_type", target_arn="test-target_arn", instance_id="test-instance_id", phone_number_prefix="test-phone_number_prefix", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_contact_evaluations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_contact_evaluations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_contact_evaluations("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_contact_flow_modules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_contact_flow_modules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_contact_flow_modules("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_contact_flows_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_contact_flows
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_contact_flows("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_contacts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_contacts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_contacts("test-instance_id", "test-time_range", search_criteria="test-search_criteria", max_results=1, next_token="test-next_token", sort="test-sort", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_email_addresses_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_email_addresses
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_email_addresses("test-instance_id", max_results=1, next_token="test-next_token", search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_evaluation_forms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_evaluation_forms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_evaluation_forms("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_hours_of_operation_overrides_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_hours_of_operation_overrides
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_hours_of_operation_overrides("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_hours_of_operations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_hours_of_operations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_hours_of_operations("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_predefined_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_predefined_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_predefined_attributes("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_prompts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_prompts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_prompts("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_queues_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_queues
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_queues("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_quick_connects_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_quick_connects
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_quick_connects("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_resource_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_resource_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_resource_tags("test-instance_id", resource_types="test-resource_types", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_routing_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_routing_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_routing_profiles("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_security_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_security_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_security_profiles("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_user_hierarchy_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_user_hierarchy_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_user_hierarchy_groups("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_users_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_users
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_users("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_search_vocabularies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import search_vocabularies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await search_vocabularies("test-instance_id", max_results=1, next_token="test-next_token", state="test-state", name_starts_with="test-name_starts_with", language_code="test-language_code", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_chat_integration_event_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import send_chat_integration_event
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await send_chat_integration_event("test-source_id", "test-destination_id", "test-event", subtype="test-subtype", new_session_details="test-new_session_details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_send_outbound_email_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import send_outbound_email
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await send_outbound_email("test-instance_id", "test-from_email_address", "test-destination_email_address", "test-email_message", "test-traffic_type", additional_recipients="test-additional_recipients", source_campaign="test-source_campaign", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_attached_file_upload_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_attached_file_upload
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_attached_file_upload("test-instance_id", "test-file_name", 1, "test-file_use_case_type", "test-associated_resource_arn", client_token="test-client_token", url_expiry_in_seconds="test-url_expiry_in_seconds", created_by="test-created_by", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_contact_evaluation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_contact_evaluation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_contact_evaluation("test-instance_id", "test-contact_id", "test-evaluation_form_id", auto_evaluation_configuration=True, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_email_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_email_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_email_contact("test-instance_id", "test-from_email_address", "test-destination_email_address", "test-email_message", description="test-description", references="test-references", name="test-name", additional_recipients="test-additional_recipients", attachments="test-attachments", contact_flow_id="test-contact_flow_id", related_contact_id="test-related_contact_id", attributes="test-attributes", segment_attributes="test-segment_attributes", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_outbound_chat_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_outbound_chat_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_outbound_chat_contact("test-source_endpoint", "test-destination_endpoint", "test-instance_id", "test-segment_attributes", "test-contact_flow_id", attributes="test-attributes", chat_duration_in_minutes=1, participant_details="test-participant_details", initial_system_message="test-initial_system_message", related_contact_id="test-related_contact_id", supported_messaging_content_types=1, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_outbound_email_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_outbound_email_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_outbound_email_contact("test-instance_id", "test-contact_id", "test-destination_email_address", "test-email_message", from_email_address="test-from_email_address", additional_recipients="test-additional_recipients", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_screen_sharing_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_screen_sharing
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_screen_sharing("test-instance_id", "test-contact_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_web_rtc_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import start_web_rtc_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await start_web_rtc_contact("test-contact_flow_id", "test-instance_id", "test-participant_details", attributes="test-attributes", client_token="test-client_token", allowed_capabilities=True, related_contact_id="test-related_contact_id", references="test-references", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_contact_recording_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import stop_contact_recording
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await stop_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", contact_recording_type="test-contact_recording_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_submit_contact_evaluation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import submit_contact_evaluation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await submit_contact_evaluation("test-instance_id", "test-evaluation_id", answers="test-answers", notes="test-notes", submitted_by="test-submitted_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_suspend_contact_recording_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import suspend_contact_recording
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await suspend_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", contact_recording_type="test-contact_recording_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_transfer_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import transfer_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await transfer_contact("test-instance_id", "test-contact_id", "test-contact_flow_id", queue_id="test-queue_id", user_id="test-user_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_agent_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_agent_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_agent_status("test-instance_id", "test-agent_status_id", name="test-name", description="test-description", state="test-state", display_order="test-display_order", reset_order_number="test-reset_order_number", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_authentication_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_authentication_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_authentication_profile("test-authentication_profile_id", "test-instance_id", name="test-name", description="test-description", allowed_ips=True, blocked_ips="test-blocked_ips", periodic_session_duration=1, session_inactivity_duration=1, session_inactivity_handling_enabled="test-session_inactivity_handling_enabled", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_contact
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_contact("test-instance_id", "test-contact_id", name="test-name", description="test-description", references="test-references", segment_attributes="test-segment_attributes", queue_info="test-queue_info", user_info="test-user_info", customer_endpoint="test-customer_endpoint", system_endpoint="test-system_endpoint", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_evaluation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_contact_evaluation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_contact_evaluation("test-instance_id", "test-evaluation_id", answers="test-answers", notes="test-notes", updated_by="test-updated_by", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_flow_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_contact_flow_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_contact_flow_metadata("test-instance_id", "test-contact_flow_id", name="test-name", description="test-description", contact_flow_state="test-contact_flow_state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_flow_module_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_contact_flow_module_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_contact_flow_module_metadata("test-instance_id", "test-contact_flow_module_id", name="test-name", description="test-description", state="test-state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_flow_name_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_contact_flow_name
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_contact_flow_name("test-instance_id", "test-contact_flow_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contact_routing_data_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_contact_routing_data
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_contact_routing_data("test-instance_id", "test-contact_id", queue_time_adjustment_seconds="test-queue_time_adjustment_seconds", queue_priority="test-queue_priority", routing_criteria="test-routing_criteria", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_email_address_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_email_address_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_email_address_metadata("test-instance_id", "test-email_address_id", description="test-description", display_name="test-display_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_evaluation_form_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_evaluation_form
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_evaluation_form("test-instance_id", "test-evaluation_form_id", "test-evaluation_form_version", "test-title", "test-items", create_new_version="test-create_new_version", description="test-description", scoring_strategy="test-scoring_strategy", auto_evaluation_configuration=True, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_hours_of_operation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_hours_of_operation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_hours_of_operation("test-instance_id", "test-hours_of_operation_id", name="test-name", description="test-description", time_zone="test-time_zone", config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_hours_of_operation_override_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_hours_of_operation_override
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", name="test-name", description="test-description", config={}, effective_from="test-effective_from", effective_till="test-effective_till", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_instance_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_instance_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_instance_attribute("test-instance_id", "test-attribute_type", "test-value", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_instance_storage_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_instance_storage_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_participant_authentication_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_participant_authentication
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_participant_authentication("test-state", "test-instance_id", code="test-code", error="test-error", error_description="test-error_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_phone_number_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_phone_number
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_phone_number("test-phone_number_id", target_arn="test-target_arn", instance_id="test-instance_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_phone_number_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_phone_number_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_phone_number_metadata("test-phone_number_id", phone_number_description="test-phone_number_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_predefined_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_predefined_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_predefined_attribute("test-instance_id", "test-name", values="test-values", purposes="test-purposes", attribute_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_prompt_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_prompt
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_prompt("test-instance_id", "test-prompt_id", name="test-name", description="test-description", s3_uri="test-s3_uri", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_queue_max_contacts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_queue_max_contacts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_queue_max_contacts("test-instance_id", "test-queue_id", max_contacts=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_queue_name_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_queue_name
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_queue_name("test-instance_id", "test-queue_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_quick_connect_name_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_quick_connect_name
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_quick_connect_name("test-instance_id", "test-quick_connect_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_routing_profile_name_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_routing_profile_name
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_routing_profile_name("test-instance_id", "test-routing_profile_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_security_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_security_profile("test-security_profile_id", "test-instance_id", description="test-description", permissions="test-permissions", allowed_access_control_tags=True, tag_restricted_resources="test-tag_restricted_resources", applications="test-applications", hierarchy_restricted_resources="test-hierarchy_restricted_resources", allowed_access_control_hierarchy_group_id=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_task_template_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_task_template
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_task_template("test-task_template_id", "test-instance_id", name="test-name", description="test-description", contact_flow_id="test-contact_flow_id", self_assign_flow_id="test-self_assign_flow_id", constraints="test-constraints", defaults="test-defaults", status="test-status", fields="test-fields", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_traffic_distribution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_traffic_distribution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_traffic_distribution("test-id", telephony_config={}, sign_in_config={}, agent_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_hierarchy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_user_hierarchy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_user_hierarchy("test-user_id", "test-instance_id", hierarchy_group_id="test-hierarchy_group_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_view_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import update_view_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await update_view_metadata("test-instance_id", "test-view_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={"UserId": "u-1"})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: mock_client)
    await create_user("i-1", "user", {}, [], "rp", password="pw", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_all_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.connect import create_user
    m = AsyncMock(); m.call = AsyncMock(return_value={"UserId": "u"})
    monkeypatch.setattr("aws_util.aio.connect.async_client", lambda *a, **kw: m)
    await create_user("i", "u", {}, [], "r", identity_info={"FirstName": "t"}, password="pw", region_name="us-east-1")
