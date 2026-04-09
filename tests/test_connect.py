"""Tests for aws_util.connect -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.connect import (
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

P = "aws_util.connect.get_client"


def _ce(code: str = "InternalError", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


@patch(P)
def test_create_instance(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_instance.return_value = {"Id": "i-1", "Arn": "arn:i"}
    r = create_instance("CONNECT_MANAGED")
    assert r.instance_id == "i-1"
    assert r.arn == "arn:i"


@patch(P)
def test_create_instance_with_alias(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_instance.return_value = {"Id": "i-2"}
    r = create_instance("CONNECT_MANAGED", instance_alias="test")
    assert r.instance_id == "i-2"


@patch(P)
def test_create_instance_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_instance.side_effect = _ce()
    with pytest.raises(RuntimeError):
        create_instance("CONNECT_MANAGED")


@patch(P)
def test_describe_instance(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_instance.return_value = {
        "Instance": {
            "Id": "i-1",
            "InstanceAlias": "a",
            "Arn": "arn",
            "IdentityManagementType": "CONNECT_MANAGED",
            "InstanceStatus": "ACTIVE",
            "CreatedTime": "2024-01-01",
        }
    }
    r = describe_instance("i-1")
    assert r.instance_id == "i-1"
    assert r.instance_alias == "a"


@patch(P)
def test_describe_instance_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_instance.side_effect = _ce()
    with pytest.raises(RuntimeError):
        describe_instance("i-1")


@patch(P)
def test_list_instances(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_instances.return_value = {
        "InstanceSummaryList": [
            {
                "Id": "i-1",
                "InstanceAlias": "a",
                "Arn": "arn",
                "IdentityManagementType": "CM",
                "InstanceStatus": "ACTIVE",
                "CreatedTime": "t",
            }
        ]
    }
    r = list_instances()
    assert len(r) == 1


@patch(P)
def test_list_instances_pagination(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_instances.side_effect = [
        {"InstanceSummaryList": [{"Id": "i-1"}], "NextToken": "t"},
        {"InstanceSummaryList": [{"Id": "i-2"}]},
    ]
    r = list_instances()
    assert len(r) == 2


@patch(P)
def test_list_instances_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_instances.side_effect = _ce()
    with pytest.raises(RuntimeError):
        list_instances()


@patch(P)
def test_delete_instance(gc):
    c = MagicMock()
    gc.return_value = c
    c.delete_instance.return_value = {}
    delete_instance("i-1")
    c.delete_instance.assert_called_once()


@patch(P)
def test_delete_instance_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.delete_instance.side_effect = _ce()
    with pytest.raises(RuntimeError):
        delete_instance("i-1")


# ---------------------------------------------------------------------------
# Contact flow operations
# ---------------------------------------------------------------------------


@patch(P)
def test_create_contact_flow(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_contact_flow.return_value = {
        "ContactFlowId": "cf-1",
        "ContactFlowArn": "arn:cf",
    }
    r = create_contact_flow("i-1", "flow", "CONTACT_FLOW", "{}")
    assert r.contact_flow_id == "cf-1"


@patch(P)
def test_create_contact_flow_with_desc(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_contact_flow.return_value = {"ContactFlowId": "cf-2"}
    r = create_contact_flow("i-1", "f", "CONTACT_FLOW", "{}", description="d")
    assert r.contact_flow_id == "cf-2"


@patch(P)
def test_create_contact_flow_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_contact_flow.side_effect = _ce()
    with pytest.raises(RuntimeError):
        create_contact_flow("i-1", "f", "CONTACT_FLOW", "{}")


@patch(P)
def test_describe_contact_flow(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_contact_flow.return_value = {
        "ContactFlow": {
            "Id": "cf-1",
            "Name": "n",
            "Arn": "a",
            "Type": "CONTACT_FLOW",
            "State": "ACTIVE",
            "Content": "{}",
        }
    }
    r = describe_contact_flow("i-1", "cf-1")
    assert r.name == "n"


@patch(P)
def test_describe_contact_flow_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_contact_flow.side_effect = _ce()
    with pytest.raises(RuntimeError):
        describe_contact_flow("i-1", "cf-1")


@patch(P)
def test_list_contact_flows(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_contact_flows.return_value = {
        "ContactFlowSummaryList": [
            {"Id": "cf-1", "Name": "n", "Arn": "a", "ContactFlowType": "T", "ContactFlowState": "S"}
        ]
    }
    r = list_contact_flows("i-1")
    assert len(r) == 1


@patch(P)
def test_list_contact_flows_with_types(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_contact_flows.return_value = {"ContactFlowSummaryList": [{"Id": "cf-1", "Name": "n"}]}
    r = list_contact_flows("i-1", contact_flow_types=["CONTACT_FLOW"])
    assert len(r) == 1


@patch(P)
def test_list_contact_flows_pagination(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_contact_flows.side_effect = [
        {"ContactFlowSummaryList": [{"Id": "cf-1", "Name": "a"}], "NextToken": "t"},
        {"ContactFlowSummaryList": [{"Id": "cf-2", "Name": "b"}]},
    ]
    r = list_contact_flows("i-1")
    assert len(r) == 2


@patch(P)
def test_list_contact_flows_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_contact_flows.side_effect = _ce()
    with pytest.raises(RuntimeError):
        list_contact_flows("i-1")


@patch(P)
def test_update_contact_flow_content(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_contact_flow_content.return_value = {}
    update_contact_flow_content("i-1", "cf-1", "{}")


@patch(P)
def test_update_contact_flow_content_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_contact_flow_content.side_effect = _ce()
    with pytest.raises(RuntimeError):
        update_contact_flow_content("i-1", "cf-1", "{}")


# ---------------------------------------------------------------------------
# Queue operations
# ---------------------------------------------------------------------------


@patch(P)
def test_create_queue(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_queue.return_value = {"QueueId": "q-1", "QueueArn": "arn:q"}
    r = create_queue("i-1", "queue", "hop-1")
    assert r.queue_id == "q-1"


@patch(P)
def test_create_queue_with_desc(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_queue.return_value = {"QueueId": "q-2"}
    r = create_queue("i-1", "q", "hop-1", description="d")
    assert r.queue_id == "q-2"


@patch(P)
def test_create_queue_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_queue.side_effect = _ce()
    with pytest.raises(RuntimeError):
        create_queue("i-1", "q", "hop-1")


@patch(P)
def test_describe_queue(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_queue.return_value = {
        "Queue": {"QueueId": "q-1", "Name": "n", "QueueArn": "a", "Status": "ENABLED", "Description": "d"}
    }
    r = describe_queue("i-1", "q-1")
    assert r.name == "n"


@patch(P)
def test_describe_queue_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_queue.side_effect = _ce()
    with pytest.raises(RuntimeError):
        describe_queue("i-1", "q-1")


@patch(P)
def test_list_queues(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_queues.return_value = {
        "QueueSummaryList": [{"Id": "q-1", "Name": "n", "Arn": "a", "QueueType": "STANDARD"}]
    }
    r = list_queues("i-1")
    assert len(r) == 1


@patch(P)
def test_list_queues_with_types(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_queues.return_value = {"QueueSummaryList": [{"Id": "q-1", "Name": "n"}]}
    r = list_queues("i-1", queue_types=["STANDARD"])
    assert len(r) == 1


@patch(P)
def test_list_queues_pagination(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_queues.side_effect = [
        {"QueueSummaryList": [{"Id": "q-1", "Name": "a"}], "NextToken": "t"},
        {"QueueSummaryList": [{"Id": "q-2", "Name": "b"}]},
    ]
    r = list_queues("i-1")
    assert len(r) == 2


@patch(P)
def test_list_queues_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_queues.side_effect = _ce()
    with pytest.raises(RuntimeError):
        list_queues("i-1")


@patch(P)
def test_update_queue_status(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_queue_status.return_value = {}
    update_queue_status("i-1", "q-1", "ENABLED")


@patch(P)
def test_update_queue_status_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_queue_status.side_effect = _ce()
    with pytest.raises(RuntimeError):
        update_queue_status("i-1", "q-1", "ENABLED")


# ---------------------------------------------------------------------------
# Routing profile operations
# ---------------------------------------------------------------------------


@patch(P)
def test_create_routing_profile(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_routing_profile.return_value = {"RoutingProfileId": "rp-1", "RoutingProfileArn": "arn"}
    r = create_routing_profile("i-1", "rp", "q-1", "desc", [{"Channel": "VOICE", "Concurrency": 1}])
    assert r.routing_profile_id == "rp-1"


@patch(P)
def test_create_routing_profile_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_routing_profile.side_effect = _ce()
    with pytest.raises(RuntimeError):
        create_routing_profile("i-1", "rp", "q-1", "d", [])


@patch(P)
def test_describe_routing_profile(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_routing_profile.return_value = {
        "RoutingProfile": {
            "RoutingProfileId": "rp-1",
            "Name": "n",
            "RoutingProfileArn": "a",
            "Description": "d",
            "DefaultOutboundQueueId": "q-1",
        }
    }
    r = describe_routing_profile("i-1", "rp-1")
    assert r.name == "n"


@patch(P)
def test_describe_routing_profile_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_routing_profile.side_effect = _ce()
    with pytest.raises(RuntimeError):
        describe_routing_profile("i-1", "rp-1")


@patch(P)
def test_list_routing_profiles(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_routing_profiles.return_value = {
        "RoutingProfileSummaryList": [{"Id": "rp-1", "Name": "n", "Arn": "a"}]
    }
    r = list_routing_profiles("i-1")
    assert len(r) == 1


@patch(P)
def test_list_routing_profiles_pagination(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_routing_profiles.side_effect = [
        {"RoutingProfileSummaryList": [{"Id": "rp-1", "Name": "a"}], "NextToken": "t"},
        {"RoutingProfileSummaryList": [{"Id": "rp-2", "Name": "b"}]},
    ]
    r = list_routing_profiles("i-1")
    assert len(r) == 2


@patch(P)
def test_list_routing_profiles_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_routing_profiles.side_effect = _ce()
    with pytest.raises(RuntimeError):
        list_routing_profiles("i-1")


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


@patch(P)
def test_create_user(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_user.return_value = {"UserId": "u-1", "UserArn": "arn:u"}
    r = create_user("i-1", "user1", {"PhoneType": "SOFT_PHONE"}, ["sp-1"], "rp-1")
    assert r.user_id == "u-1"


@patch(P)
def test_create_user_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.create_user.side_effect = _ce()
    with pytest.raises(RuntimeError):
        create_user("i-1", "u", {}, [], "rp")


@patch(P)
def test_describe_user(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_user.return_value = {
        "User": {
            "Id": "u-1",
            "Username": "n",
            "Arn": "a",
            "RoutingProfileId": "rp",
            "SecurityProfileIds": ["sp"],
        }
    }
    r = describe_user("i-1", "u-1")
    assert r.username == "n"


@patch(P)
def test_describe_user_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.describe_user.side_effect = _ce()
    with pytest.raises(RuntimeError):
        describe_user("i-1", "u-1")


@patch(P)
def test_list_users(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_users.return_value = {
        "UserSummaryList": [{"Id": "u-1", "Username": "n", "Arn": "a"}]
    }
    r = list_users("i-1")
    assert len(r) == 1


@patch(P)
def test_list_users_pagination(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_users.side_effect = [
        {"UserSummaryList": [{"Id": "u-1"}], "NextToken": "t"},
        {"UserSummaryList": [{"Id": "u-2"}]},
    ]
    r = list_users("i-1")
    assert len(r) == 2


@patch(P)
def test_list_users_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.list_users.side_effect = _ce()
    with pytest.raises(RuntimeError):
        list_users("i-1")


@patch(P)
def test_update_user_routing_profile(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_user_routing_profile.return_value = {}
    update_user_routing_profile("i-1", "u-1", "rp-2")


@patch(P)
def test_update_user_routing_profile_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_user_routing_profile.side_effect = _ce()
    with pytest.raises(RuntimeError):
        update_user_routing_profile("i-1", "u-1", "rp-2")


@patch(P)
def test_delete_user(gc):
    c = MagicMock()
    gc.return_value = c
    c.delete_user.return_value = {}
    delete_user("i-1", "u-1")


@patch(P)
def test_delete_user_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.delete_user.side_effect = _ce()
    with pytest.raises(RuntimeError):
        delete_user("i-1", "u-1")


# ---------------------------------------------------------------------------
# Contact operations
# ---------------------------------------------------------------------------


@patch(P)
def test_start_outbound_voice_contact(gc):
    c = MagicMock()
    gc.return_value = c
    c.start_outbound_voice_contact.return_value = {"ContactId": "c-1"}
    r = start_outbound_voice_contact("i-1", "cf-1", "+15551234567")
    assert r.contact_id == "c-1"


@patch(P)
def test_start_outbound_voice_contact_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.start_outbound_voice_contact.side_effect = _ce()
    with pytest.raises(RuntimeError):
        start_outbound_voice_contact("i-1", "cf-1", "+15551234567")


@patch(P)
def test_start_chat_contact(gc):
    c = MagicMock()
    gc.return_value = c
    c.start_chat_contact.return_value = {"ContactId": "c-1"}
    r = start_chat_contact("i-1", "cf-1", {"DisplayName": "User"})
    assert r.contact_id == "c-1"


@patch(P)
def test_start_chat_contact_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.start_chat_contact.side_effect = _ce()
    with pytest.raises(RuntimeError):
        start_chat_contact("i-1", "cf-1", {})


@patch(P)
def test_stop_contact(gc):
    c = MagicMock()
    gc.return_value = c
    c.stop_contact.return_value = {}
    stop_contact("c-1", "i-1")


@patch(P)
def test_stop_contact_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.stop_contact.side_effect = _ce()
    with pytest.raises(RuntimeError):
        stop_contact("c-1", "i-1")


@patch(P)
def test_get_contact_attributes(gc):
    c = MagicMock()
    gc.return_value = c
    c.get_contact_attributes.return_value = {"Attributes": {"key": "val"}}
    r = get_contact_attributes("i-1", "c-1")
    assert r == {"key": "val"}


@patch(P)
def test_get_contact_attributes_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.get_contact_attributes.side_effect = _ce()
    with pytest.raises(RuntimeError):
        get_contact_attributes("i-1", "c-1")


@patch(P)
def test_update_contact_attributes(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_contact_attributes.return_value = {}
    update_contact_attributes("i-1", "c-1", {"key": "val"})


@patch(P)
def test_update_contact_attributes_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.update_contact_attributes.side_effect = _ce()
    with pytest.raises(RuntimeError):
        update_contact_attributes("i-1", "c-1", {"key": "val"})


@patch(P)
def test_get_current_metric_data(gc):
    c = MagicMock()
    gc.return_value = c
    c.get_current_metric_data.return_value = {
        "MetricResults": [{"Dimensions": {"Queue": {"Id": "q-1"}}, "Collections": [{"Metric": {"Name": "AGENTS_ONLINE"}, "Value": 5}]}]
    }
    r = get_current_metric_data("i-1", {"Queues": ["q-1"]}, [{"Name": "AGENTS_ONLINE", "Unit": "COUNT"}])
    assert len(r) == 1


@patch(P)
def test_get_current_metric_data_with_groupings(gc):
    c = MagicMock()
    gc.return_value = c
    c.get_current_metric_data.return_value = {"MetricResults": []}
    r = get_current_metric_data("i-1", {}, [], groupings=["QUEUE"])
    assert r == []


@patch(P)
def test_get_current_metric_data_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.get_current_metric_data.side_effect = _ce()
    with pytest.raises(RuntimeError):
        get_current_metric_data("i-1", {}, [])


@patch(P)
def test_start_task_contact(gc):
    c = MagicMock()
    gc.return_value = c
    c.start_task_contact.return_value = {"ContactId": "c-1"}
    r = start_task_contact("i-1", "cf-1", "task1")
    assert r.contact_id == "c-1"


@patch(P)
def test_start_task_contact_error(gc):
    c = MagicMock()
    gc.return_value = c
    c.start_task_contact.side_effect = _ce()
    with pytest.raises(RuntimeError):
        start_task_contact("i-1", "cf-1", "t")


REGION = "us-east-1"


def test_activate_evaluation_form(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    activate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, region_name=REGION)
    mock_client.activate_evaluation_form.assert_called_once()


def test_activate_evaluation_form_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.activate_evaluation_form.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "activate_evaluation_form",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to activate evaluation form"):
        activate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, region_name=REGION)


def test_associate_analytics_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_analytics_data_set("test-instance_id", "test-data_set_id", region_name=REGION)
    mock_client.associate_analytics_data_set.assert_called_once()


def test_associate_analytics_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_analytics_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_analytics_data_set",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate analytics data set"):
        associate_analytics_data_set("test-instance_id", "test-data_set_id", region_name=REGION)


def test_associate_approved_origin(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_approved_origin.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_approved_origin("test-instance_id", "test-origin", region_name=REGION)
    mock_client.associate_approved_origin.assert_called_once()


def test_associate_approved_origin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_approved_origin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_approved_origin",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate approved origin"):
        associate_approved_origin("test-instance_id", "test-origin", region_name=REGION)


def test_associate_bot(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_bot("test-instance_id", region_name=REGION)
    mock_client.associate_bot.assert_called_once()


def test_associate_bot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_bot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_bot",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate bot"):
        associate_bot("test-instance_id", region_name=REGION)


def test_associate_contact_with_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_contact_with_user.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_contact_with_user("test-instance_id", "test-contact_id", "test-user_id", region_name=REGION)
    mock_client.associate_contact_with_user.assert_called_once()


def test_associate_contact_with_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_contact_with_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_contact_with_user",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate contact with user"):
        associate_contact_with_user("test-instance_id", "test-contact_id", "test-user_id", region_name=REGION)


def test_associate_default_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_default_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_default_vocabulary("test-instance_id", "test-language_code", region_name=REGION)
    mock_client.associate_default_vocabulary.assert_called_once()


def test_associate_default_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_default_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_default_vocabulary",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate default vocabulary"):
        associate_default_vocabulary("test-instance_id", "test-language_code", region_name=REGION)


def test_associate_email_address_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_email_address_alias.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_email_address_alias("test-email_address_id", "test-instance_id", {}, region_name=REGION)
    mock_client.associate_email_address_alias.assert_called_once()


def test_associate_email_address_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_email_address_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_email_address_alias",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate email address alias"):
        associate_email_address_alias("test-email_address_id", "test-instance_id", {}, region_name=REGION)


def test_associate_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_flow.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_flow("test-instance_id", "test-resource_id", "test-flow_id", "test-resource_type", region_name=REGION)
    mock_client.associate_flow.assert_called_once()


def test_associate_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_flow",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate flow"):
        associate_flow("test-instance_id", "test-resource_id", "test-flow_id", "test-resource_type", region_name=REGION)


def test_associate_instance_storage_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_instance_storage_config("test-instance_id", "test-resource_type", {}, region_name=REGION)
    mock_client.associate_instance_storage_config.assert_called_once()


def test_associate_instance_storage_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_instance_storage_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_instance_storage_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate instance storage config"):
        associate_instance_storage_config("test-instance_id", "test-resource_type", {}, region_name=REGION)


def test_associate_lambda_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_lambda_function.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_lambda_function("test-instance_id", "test-function_arn", region_name=REGION)
    mock_client.associate_lambda_function.assert_called_once()


def test_associate_lambda_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_lambda_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_lambda_function",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate lambda function"):
        associate_lambda_function("test-instance_id", "test-function_arn", region_name=REGION)


def test_associate_lex_bot(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_lex_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_lex_bot("test-instance_id", {}, region_name=REGION)
    mock_client.associate_lex_bot.assert_called_once()


def test_associate_lex_bot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_lex_bot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_lex_bot",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate lex bot"):
        associate_lex_bot("test-instance_id", {}, region_name=REGION)


def test_associate_phone_number_contact_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_phone_number_contact_flow.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", "test-contact_flow_id", region_name=REGION)
    mock_client.associate_phone_number_contact_flow.assert_called_once()


def test_associate_phone_number_contact_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_phone_number_contact_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_phone_number_contact_flow",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate phone number contact flow"):
        associate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", "test-contact_flow_id", region_name=REGION)


def test_associate_queue_quick_connects(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_queue_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_queue_quick_connects("test-instance_id", "test-queue_id", [], region_name=REGION)
    mock_client.associate_queue_quick_connects.assert_called_once()


def test_associate_queue_quick_connects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_queue_quick_connects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_queue_quick_connects",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate queue quick connects"):
        associate_queue_quick_connects("test-instance_id", "test-queue_id", [], region_name=REGION)


def test_associate_routing_profile_queues(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_routing_profile_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)
    mock_client.associate_routing_profile_queues.assert_called_once()


def test_associate_routing_profile_queues_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_routing_profile_queues.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_routing_profile_queues",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate routing profile queues"):
        associate_routing_profile_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)


def test_associate_security_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_security_key.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_security_key("test-instance_id", "test-key", region_name=REGION)
    mock_client.associate_security_key.assert_called_once()


def test_associate_security_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_security_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_security_key",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate security key"):
        associate_security_key("test-instance_id", "test-key", region_name=REGION)


def test_associate_traffic_distribution_group_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_traffic_distribution_group_user.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", region_name=REGION)
    mock_client.associate_traffic_distribution_group_user.assert_called_once()


def test_associate_traffic_distribution_group_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_traffic_distribution_group_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_traffic_distribution_group_user",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate traffic distribution group user"):
        associate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", region_name=REGION)


def test_associate_user_proficiencies(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_user_proficiencies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_user_proficiencies("test-instance_id", "test-user_id", [], region_name=REGION)
    mock_client.associate_user_proficiencies.assert_called_once()


def test_associate_user_proficiencies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_user_proficiencies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_user_proficiencies",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate user proficiencies"):
        associate_user_proficiencies("test-instance_id", "test-user_id", [], region_name=REGION)


def test_batch_associate_analytics_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_associate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_associate_analytics_data_set("test-instance_id", [], region_name=REGION)
    mock_client.batch_associate_analytics_data_set.assert_called_once()


def test_batch_associate_analytics_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_associate_analytics_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_associate_analytics_data_set",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch associate analytics data set"):
        batch_associate_analytics_data_set("test-instance_id", [], region_name=REGION)


def test_batch_disassociate_analytics_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_disassociate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_disassociate_analytics_data_set("test-instance_id", [], region_name=REGION)
    mock_client.batch_disassociate_analytics_data_set.assert_called_once()


def test_batch_disassociate_analytics_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_disassociate_analytics_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_disassociate_analytics_data_set",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch disassociate analytics data set"):
        batch_disassociate_analytics_data_set("test-instance_id", [], region_name=REGION)


def test_batch_get_attached_file_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_attached_file_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_get_attached_file_metadata([], "test-instance_id", "test-associated_resource_arn", region_name=REGION)
    mock_client.batch_get_attached_file_metadata.assert_called_once()


def test_batch_get_attached_file_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_attached_file_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_attached_file_metadata",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get attached file metadata"):
        batch_get_attached_file_metadata([], "test-instance_id", "test-associated_resource_arn", region_name=REGION)


def test_batch_get_flow_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_flow_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_get_flow_association("test-instance_id", [], region_name=REGION)
    mock_client.batch_get_flow_association.assert_called_once()


def test_batch_get_flow_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_flow_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_flow_association",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get flow association"):
        batch_get_flow_association("test-instance_id", [], region_name=REGION)


def test_batch_put_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_put_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_put_contact("test-instance_id", [], region_name=REGION)
    mock_client.batch_put_contact.assert_called_once()


def test_batch_put_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_put_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_put_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch put contact"):
        batch_put_contact("test-instance_id", [], region_name=REGION)


def test_claim_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.claim_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    claim_phone_number("test-phone_number", region_name=REGION)
    mock_client.claim_phone_number.assert_called_once()


def test_claim_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.claim_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "claim_phone_number",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to claim phone number"):
        claim_phone_number("test-phone_number", region_name=REGION)


def test_complete_attached_file_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_attached_file_upload.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    complete_attached_file_upload("test-instance_id", "test-file_id", "test-associated_resource_arn", region_name=REGION)
    mock_client.complete_attached_file_upload.assert_called_once()


def test_complete_attached_file_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_attached_file_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "complete_attached_file_upload",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to complete attached file upload"):
        complete_attached_file_upload("test-instance_id", "test-file_id", "test-associated_resource_arn", region_name=REGION)


def test_create_agent_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agent_status.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_agent_status("test-instance_id", "test-name", "test-state", region_name=REGION)
    mock_client.create_agent_status.assert_called_once()


def test_create_agent_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_agent_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_agent_status",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create agent status"):
        create_agent_status("test-instance_id", "test-name", "test-state", region_name=REGION)


def test_create_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_contact("test-instance_id", "test-channel", "test-initiation_method", region_name=REGION)
    mock_client.create_contact.assert_called_once()


def test_create_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create contact"):
        create_contact("test-instance_id", "test-channel", "test-initiation_method", region_name=REGION)


def test_create_contact_flow_module(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_contact_flow_module.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_contact_flow_module("test-instance_id", "test-name", "test-content", region_name=REGION)
    mock_client.create_contact_flow_module.assert_called_once()


def test_create_contact_flow_module_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_contact_flow_module.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_contact_flow_module",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create contact flow module"):
        create_contact_flow_module("test-instance_id", "test-name", "test-content", region_name=REGION)


def test_create_contact_flow_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_contact_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_contact_flow_version("test-instance_id", "test-contact_flow_id", region_name=REGION)
    mock_client.create_contact_flow_version.assert_called_once()


def test_create_contact_flow_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_contact_flow_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_contact_flow_version",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create contact flow version"):
        create_contact_flow_version("test-instance_id", "test-contact_flow_id", region_name=REGION)


def test_create_email_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_email_address.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_email_address("test-instance_id", "test-email_address", region_name=REGION)
    mock_client.create_email_address.assert_called_once()


def test_create_email_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_email_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_email_address",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create email address"):
        create_email_address("test-instance_id", "test-email_address", region_name=REGION)


def test_create_evaluation_form(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_evaluation_form("test-instance_id", "test-title", [], region_name=REGION)
    mock_client.create_evaluation_form.assert_called_once()


def test_create_evaluation_form_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_evaluation_form.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_evaluation_form",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create evaluation form"):
        create_evaluation_form("test-instance_id", "test-title", [], region_name=REGION)


def test_create_hours_of_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_hours_of_operation("test-instance_id", "test-name", "test-time_zone", [], region_name=REGION)
    mock_client.create_hours_of_operation.assert_called_once()


def test_create_hours_of_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hours_of_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_hours_of_operation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create hours of operation"):
        create_hours_of_operation("test-instance_id", "test-name", "test-time_zone", [], region_name=REGION)


def test_create_hours_of_operation_override(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hours_of_operation_override.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-name", [], "test-effective_from", "test-effective_till", region_name=REGION)
    mock_client.create_hours_of_operation_override.assert_called_once()


def test_create_hours_of_operation_override_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hours_of_operation_override.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_hours_of_operation_override",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create hours of operation override"):
        create_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-name", [], "test-effective_from", "test-effective_till", region_name=REGION)


def test_create_integration_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_integration_association("test-instance_id", "test-integration_type", "test-integration_arn", region_name=REGION)
    mock_client.create_integration_association.assert_called_once()


def test_create_integration_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_integration_association",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create integration association"):
        create_integration_association("test-instance_id", "test-integration_type", "test-integration_arn", region_name=REGION)


def test_create_participant(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_participant.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_participant("test-instance_id", "test-contact_id", {}, region_name=REGION)
    mock_client.create_participant.assert_called_once()


def test_create_participant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_participant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_participant",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create participant"):
        create_participant("test-instance_id", "test-contact_id", {}, region_name=REGION)


def test_create_persistent_contact_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_persistent_contact_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_persistent_contact_association("test-instance_id", "test-initial_contact_id", "test-rehydration_type", "test-source_contact_id", region_name=REGION)
    mock_client.create_persistent_contact_association.assert_called_once()


def test_create_persistent_contact_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_persistent_contact_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_persistent_contact_association",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create persistent contact association"):
        create_persistent_contact_association("test-instance_id", "test-initial_contact_id", "test-rehydration_type", "test-source_contact_id", region_name=REGION)


def test_create_predefined_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_predefined_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_predefined_attribute("test-instance_id", "test-name", region_name=REGION)
    mock_client.create_predefined_attribute.assert_called_once()


def test_create_predefined_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_predefined_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_predefined_attribute",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create predefined attribute"):
        create_predefined_attribute("test-instance_id", "test-name", region_name=REGION)


def test_create_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_prompt("test-instance_id", "test-name", "test-s3_uri", region_name=REGION)
    mock_client.create_prompt.assert_called_once()


def test_create_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_prompt",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create prompt"):
        create_prompt("test-instance_id", "test-name", "test-s3_uri", region_name=REGION)


def test_create_push_notification_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_push_notification_registration.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_push_notification_registration("test-instance_id", "test-pinpoint_app_arn", "test-device_token", "test-device_type", {}, region_name=REGION)
    mock_client.create_push_notification_registration.assert_called_once()


def test_create_push_notification_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_push_notification_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_push_notification_registration",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create push notification registration"):
        create_push_notification_registration("test-instance_id", "test-pinpoint_app_arn", "test-device_token", "test-device_type", {}, region_name=REGION)


def test_create_quick_connect(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_quick_connect.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_quick_connect("test-instance_id", "test-name", {}, region_name=REGION)
    mock_client.create_quick_connect.assert_called_once()


def test_create_quick_connect_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_quick_connect.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_quick_connect",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create quick connect"):
        create_quick_connect("test-instance_id", "test-name", {}, region_name=REGION)


def test_create_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rule.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_rule("test-instance_id", "test-name", {}, "test-function", [], "test-publish_status", region_name=REGION)
    mock_client.create_rule.assert_called_once()


def test_create_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_rule",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create rule"):
        create_rule("test-instance_id", "test-name", {}, "test-function", [], "test-publish_status", region_name=REGION)


def test_create_security_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_security_profile("test-security_profile_name", "test-instance_id", region_name=REGION)
    mock_client.create_security_profile.assert_called_once()


def test_create_security_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_security_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create security profile"):
        create_security_profile("test-security_profile_name", "test-instance_id", region_name=REGION)


def test_create_task_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_task_template("test-instance_id", "test-name", [], region_name=REGION)
    mock_client.create_task_template.assert_called_once()


def test_create_task_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_task_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_task_template",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create task template"):
        create_task_template("test-instance_id", "test-name", [], region_name=REGION)


def test_create_traffic_distribution_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_distribution_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_traffic_distribution_group("test-name", "test-instance_id", region_name=REGION)
    mock_client.create_traffic_distribution_group.assert_called_once()


def test_create_traffic_distribution_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_traffic_distribution_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_traffic_distribution_group",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create traffic distribution group"):
        create_traffic_distribution_group("test-name", "test-instance_id", region_name=REGION)


def test_create_use_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_use_case.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_use_case("test-instance_id", "test-integration_association_id", "test-use_case_type", region_name=REGION)
    mock_client.create_use_case.assert_called_once()


def test_create_use_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_use_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_use_case",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create use case"):
        create_use_case("test-instance_id", "test-integration_association_id", "test-use_case_type", region_name=REGION)


def test_create_user_hierarchy_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_hierarchy_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_user_hierarchy_group("test-name", "test-instance_id", region_name=REGION)
    mock_client.create_user_hierarchy_group.assert_called_once()


def test_create_user_hierarchy_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_hierarchy_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_hierarchy_group",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user hierarchy group"):
        create_user_hierarchy_group("test-name", "test-instance_id", region_name=REGION)


def test_create_view(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_view.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_view("test-instance_id", "test-status", {}, "test-name", region_name=REGION)
    mock_client.create_view.assert_called_once()


def test_create_view_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_view.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_view",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create view"):
        create_view("test-instance_id", "test-status", {}, "test-name", region_name=REGION)


def test_create_view_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_view_version.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_view_version("test-instance_id", "test-view_id", region_name=REGION)
    mock_client.create_view_version.assert_called_once()


def test_create_view_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_view_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_view_version",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create view version"):
        create_view_version("test-instance_id", "test-view_id", region_name=REGION)


def test_create_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_vocabulary("test-instance_id", "test-vocabulary_name", "test-language_code", "test-content", region_name=REGION)
    mock_client.create_vocabulary.assert_called_once()


def test_create_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vocabulary",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vocabulary"):
        create_vocabulary("test-instance_id", "test-vocabulary_name", "test-language_code", "test-content", region_name=REGION)


def test_deactivate_evaluation_form(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    deactivate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, region_name=REGION)
    mock_client.deactivate_evaluation_form.assert_called_once()


def test_deactivate_evaluation_form_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_evaluation_form.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deactivate_evaluation_form",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deactivate evaluation form"):
        deactivate_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, region_name=REGION)


def test_delete_attached_file(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_attached_file.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", region_name=REGION)
    mock_client.delete_attached_file.assert_called_once()


def test_delete_attached_file_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_attached_file.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_attached_file",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete attached file"):
        delete_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", region_name=REGION)


def test_delete_contact_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)
    mock_client.delete_contact_evaluation.assert_called_once()


def test_delete_contact_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_contact_evaluation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete contact evaluation"):
        delete_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)


def test_delete_contact_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_flow.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_contact_flow("test-instance_id", "test-contact_flow_id", region_name=REGION)
    mock_client.delete_contact_flow.assert_called_once()


def test_delete_contact_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_contact_flow",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete contact flow"):
        delete_contact_flow("test-instance_id", "test-contact_flow_id", region_name=REGION)


def test_delete_contact_flow_module(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_flow_module.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_contact_flow_module("test-instance_id", "test-contact_flow_module_id", region_name=REGION)
    mock_client.delete_contact_flow_module.assert_called_once()


def test_delete_contact_flow_module_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_flow_module.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_contact_flow_module",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete contact flow module"):
        delete_contact_flow_module("test-instance_id", "test-contact_flow_module_id", region_name=REGION)


def test_delete_contact_flow_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_contact_flow_version("test-instance_id", "test-contact_flow_id", 1, region_name=REGION)
    mock_client.delete_contact_flow_version.assert_called_once()


def test_delete_contact_flow_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_contact_flow_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_contact_flow_version",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete contact flow version"):
        delete_contact_flow_version("test-instance_id", "test-contact_flow_id", 1, region_name=REGION)


def test_delete_email_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_email_address.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_email_address("test-instance_id", "test-email_address_id", region_name=REGION)
    mock_client.delete_email_address.assert_called_once()


def test_delete_email_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_email_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_email_address",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete email address"):
        delete_email_address("test-instance_id", "test-email_address_id", region_name=REGION)


def test_delete_evaluation_form(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_evaluation_form("test-instance_id", "test-evaluation_form_id", region_name=REGION)
    mock_client.delete_evaluation_form.assert_called_once()


def test_delete_evaluation_form_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_evaluation_form.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_evaluation_form",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete evaluation form"):
        delete_evaluation_form("test-instance_id", "test-evaluation_form_id", region_name=REGION)


def test_delete_hours_of_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_hours_of_operation("test-instance_id", "test-hours_of_operation_id", region_name=REGION)
    mock_client.delete_hours_of_operation.assert_called_once()


def test_delete_hours_of_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hours_of_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_hours_of_operation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete hours of operation"):
        delete_hours_of_operation("test-instance_id", "test-hours_of_operation_id", region_name=REGION)


def test_delete_hours_of_operation_override(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hours_of_operation_override.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", region_name=REGION)
    mock_client.delete_hours_of_operation_override.assert_called_once()


def test_delete_hours_of_operation_override_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hours_of_operation_override.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_hours_of_operation_override",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete hours of operation override"):
        delete_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", region_name=REGION)


def test_delete_integration_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_integration_association("test-instance_id", "test-integration_association_id", region_name=REGION)
    mock_client.delete_integration_association.assert_called_once()


def test_delete_integration_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration_association",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete integration association"):
        delete_integration_association("test-instance_id", "test-integration_association_id", region_name=REGION)


def test_delete_predefined_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_predefined_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_predefined_attribute("test-instance_id", "test-name", region_name=REGION)
    mock_client.delete_predefined_attribute.assert_called_once()


def test_delete_predefined_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_predefined_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_predefined_attribute",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete predefined attribute"):
        delete_predefined_attribute("test-instance_id", "test-name", region_name=REGION)


def test_delete_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prompt.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_prompt("test-instance_id", "test-prompt_id", region_name=REGION)
    mock_client.delete_prompt.assert_called_once()


def test_delete_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_prompt",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete prompt"):
        delete_prompt("test-instance_id", "test-prompt_id", region_name=REGION)


def test_delete_push_notification_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_push_notification_registration.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_push_notification_registration("test-instance_id", "test-registration_id", "test-contact_id", region_name=REGION)
    mock_client.delete_push_notification_registration.assert_called_once()


def test_delete_push_notification_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_push_notification_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_push_notification_registration",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete push notification registration"):
        delete_push_notification_registration("test-instance_id", "test-registration_id", "test-contact_id", region_name=REGION)


def test_delete_queue(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_queue.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_queue("test-instance_id", "test-queue_id", region_name=REGION)
    mock_client.delete_queue.assert_called_once()


def test_delete_queue_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_queue.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_queue",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete queue"):
        delete_queue("test-instance_id", "test-queue_id", region_name=REGION)


def test_delete_quick_connect(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_quick_connect.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_quick_connect("test-instance_id", "test-quick_connect_id", region_name=REGION)
    mock_client.delete_quick_connect.assert_called_once()


def test_delete_quick_connect_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_quick_connect.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_quick_connect",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete quick connect"):
        delete_quick_connect("test-instance_id", "test-quick_connect_id", region_name=REGION)


def test_delete_routing_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_routing_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_routing_profile("test-instance_id", "test-routing_profile_id", region_name=REGION)
    mock_client.delete_routing_profile.assert_called_once()


def test_delete_routing_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_routing_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_routing_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete routing profile"):
        delete_routing_profile("test-instance_id", "test-routing_profile_id", region_name=REGION)


def test_delete_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rule.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_rule("test-instance_id", "test-rule_id", region_name=REGION)
    mock_client.delete_rule.assert_called_once()


def test_delete_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_rule",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete rule"):
        delete_rule("test-instance_id", "test-rule_id", region_name=REGION)


def test_delete_security_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_security_profile("test-instance_id", "test-security_profile_id", region_name=REGION)
    mock_client.delete_security_profile.assert_called_once()


def test_delete_security_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_security_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete security profile"):
        delete_security_profile("test-instance_id", "test-security_profile_id", region_name=REGION)


def test_delete_task_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_task_template("test-instance_id", "test-task_template_id", region_name=REGION)
    mock_client.delete_task_template.assert_called_once()


def test_delete_task_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_task_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_task_template",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete task template"):
        delete_task_template("test-instance_id", "test-task_template_id", region_name=REGION)


def test_delete_traffic_distribution_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_distribution_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_traffic_distribution_group("test-traffic_distribution_group_id", region_name=REGION)
    mock_client.delete_traffic_distribution_group.assert_called_once()


def test_delete_traffic_distribution_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_traffic_distribution_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_traffic_distribution_group",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete traffic distribution group"):
        delete_traffic_distribution_group("test-traffic_distribution_group_id", region_name=REGION)


def test_delete_use_case(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_use_case.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_use_case("test-instance_id", "test-integration_association_id", "test-use_case_id", region_name=REGION)
    mock_client.delete_use_case.assert_called_once()


def test_delete_use_case_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_use_case.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_use_case",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete use case"):
        delete_use_case("test-instance_id", "test-integration_association_id", "test-use_case_id", region_name=REGION)


def test_delete_user_hierarchy_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_hierarchy_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", region_name=REGION)
    mock_client.delete_user_hierarchy_group.assert_called_once()


def test_delete_user_hierarchy_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_hierarchy_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_hierarchy_group",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user hierarchy group"):
        delete_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", region_name=REGION)


def test_delete_view(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_view.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_view("test-instance_id", "test-view_id", region_name=REGION)
    mock_client.delete_view.assert_called_once()


def test_delete_view_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_view.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_view",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete view"):
        delete_view("test-instance_id", "test-view_id", region_name=REGION)


def test_delete_view_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_view_version.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_view_version("test-instance_id", "test-view_id", 1, region_name=REGION)
    mock_client.delete_view_version.assert_called_once()


def test_delete_view_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_view_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_view_version",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete view version"):
        delete_view_version("test-instance_id", "test-view_id", 1, region_name=REGION)


def test_delete_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_vocabulary("test-instance_id", "test-vocabulary_id", region_name=REGION)
    mock_client.delete_vocabulary.assert_called_once()


def test_delete_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vocabulary",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vocabulary"):
        delete_vocabulary("test-instance_id", "test-vocabulary_id", region_name=REGION)


def test_describe_agent_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_agent_status.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_agent_status("test-instance_id", "test-agent_status_id", region_name=REGION)
    mock_client.describe_agent_status.assert_called_once()


def test_describe_agent_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_agent_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_agent_status",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe agent status"):
        describe_agent_status("test-instance_id", "test-agent_status_id", region_name=REGION)


def test_describe_authentication_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_authentication_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_authentication_profile("test-authentication_profile_id", "test-instance_id", region_name=REGION)
    mock_client.describe_authentication_profile.assert_called_once()


def test_describe_authentication_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_authentication_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_authentication_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe authentication profile"):
        describe_authentication_profile("test-authentication_profile_id", "test-instance_id", region_name=REGION)


def test_describe_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_contact("test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.describe_contact.assert_called_once()


def test_describe_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe contact"):
        describe_contact("test-instance_id", "test-contact_id", region_name=REGION)


def test_describe_contact_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)
    mock_client.describe_contact_evaluation.assert_called_once()


def test_describe_contact_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contact_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_contact_evaluation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe contact evaluation"):
        describe_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)


def test_describe_contact_flow_module(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contact_flow_module.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_contact_flow_module("test-instance_id", "test-contact_flow_module_id", region_name=REGION)
    mock_client.describe_contact_flow_module.assert_called_once()


def test_describe_contact_flow_module_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_contact_flow_module.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_contact_flow_module",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe contact flow module"):
        describe_contact_flow_module("test-instance_id", "test-contact_flow_module_id", region_name=REGION)


def test_describe_email_address(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_email_address.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_email_address("test-instance_id", "test-email_address_id", region_name=REGION)
    mock_client.describe_email_address.assert_called_once()


def test_describe_email_address_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_email_address.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_email_address",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe email address"):
        describe_email_address("test-instance_id", "test-email_address_id", region_name=REGION)


def test_describe_evaluation_form(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_evaluation_form("test-instance_id", "test-evaluation_form_id", region_name=REGION)
    mock_client.describe_evaluation_form.assert_called_once()


def test_describe_evaluation_form_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_evaluation_form.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_evaluation_form",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe evaluation form"):
        describe_evaluation_form("test-instance_id", "test-evaluation_form_id", region_name=REGION)


def test_describe_hours_of_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_hours_of_operation("test-instance_id", "test-hours_of_operation_id", region_name=REGION)
    mock_client.describe_hours_of_operation.assert_called_once()


def test_describe_hours_of_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hours_of_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_hours_of_operation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe hours of operation"):
        describe_hours_of_operation("test-instance_id", "test-hours_of_operation_id", region_name=REGION)


def test_describe_hours_of_operation_override(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hours_of_operation_override.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", region_name=REGION)
    mock_client.describe_hours_of_operation_override.assert_called_once()


def test_describe_hours_of_operation_override_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hours_of_operation_override.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_hours_of_operation_override",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe hours of operation override"):
        describe_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", region_name=REGION)


def test_describe_instance_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_instance_attribute("test-instance_id", "test-attribute_type", region_name=REGION)
    mock_client.describe_instance_attribute.assert_called_once()


def test_describe_instance_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_attribute",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance attribute"):
        describe_instance_attribute("test-instance_id", "test-attribute_type", region_name=REGION)


def test_describe_instance_storage_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", region_name=REGION)
    mock_client.describe_instance_storage_config.assert_called_once()


def test_describe_instance_storage_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_storage_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_storage_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance storage config"):
        describe_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", region_name=REGION)


def test_describe_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_phone_number("test-phone_number_id", region_name=REGION)
    mock_client.describe_phone_number.assert_called_once()


def test_describe_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_phone_number",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe phone number"):
        describe_phone_number("test-phone_number_id", region_name=REGION)


def test_describe_predefined_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_predefined_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_predefined_attribute("test-instance_id", "test-name", region_name=REGION)
    mock_client.describe_predefined_attribute.assert_called_once()


def test_describe_predefined_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_predefined_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_predefined_attribute",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe predefined attribute"):
        describe_predefined_attribute("test-instance_id", "test-name", region_name=REGION)


def test_describe_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_prompt.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_prompt("test-instance_id", "test-prompt_id", region_name=REGION)
    mock_client.describe_prompt.assert_called_once()


def test_describe_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_prompt",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe prompt"):
        describe_prompt("test-instance_id", "test-prompt_id", region_name=REGION)


def test_describe_quick_connect(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_quick_connect.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_quick_connect("test-instance_id", "test-quick_connect_id", region_name=REGION)
    mock_client.describe_quick_connect.assert_called_once()


def test_describe_quick_connect_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_quick_connect.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_quick_connect",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe quick connect"):
        describe_quick_connect("test-instance_id", "test-quick_connect_id", region_name=REGION)


def test_describe_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_rule.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_rule("test-instance_id", "test-rule_id", region_name=REGION)
    mock_client.describe_rule.assert_called_once()


def test_describe_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_rule",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe rule"):
        describe_rule("test-instance_id", "test-rule_id", region_name=REGION)


def test_describe_security_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_security_profile("test-security_profile_id", "test-instance_id", region_name=REGION)
    mock_client.describe_security_profile.assert_called_once()


def test_describe_security_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security profile"):
        describe_security_profile("test-security_profile_id", "test-instance_id", region_name=REGION)


def test_describe_traffic_distribution_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_distribution_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_traffic_distribution_group("test-traffic_distribution_group_id", region_name=REGION)
    mock_client.describe_traffic_distribution_group.assert_called_once()


def test_describe_traffic_distribution_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_traffic_distribution_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_traffic_distribution_group",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe traffic distribution group"):
        describe_traffic_distribution_group("test-traffic_distribution_group_id", region_name=REGION)


def test_describe_user_hierarchy_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_hierarchy_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", region_name=REGION)
    mock_client.describe_user_hierarchy_group.assert_called_once()


def test_describe_user_hierarchy_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_hierarchy_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_hierarchy_group",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user hierarchy group"):
        describe_user_hierarchy_group("test-hierarchy_group_id", "test-instance_id", region_name=REGION)


def test_describe_user_hierarchy_structure(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_hierarchy_structure.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_user_hierarchy_structure("test-instance_id", region_name=REGION)
    mock_client.describe_user_hierarchy_structure.assert_called_once()


def test_describe_user_hierarchy_structure_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_hierarchy_structure.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_hierarchy_structure",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user hierarchy structure"):
        describe_user_hierarchy_structure("test-instance_id", region_name=REGION)


def test_describe_view(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_view.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_view("test-instance_id", "test-view_id", region_name=REGION)
    mock_client.describe_view.assert_called_once()


def test_describe_view_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_view.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_view",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe view"):
        describe_view("test-instance_id", "test-view_id", region_name=REGION)


def test_describe_vocabulary(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_vocabulary("test-instance_id", "test-vocabulary_id", region_name=REGION)
    mock_client.describe_vocabulary.assert_called_once()


def test_describe_vocabulary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vocabulary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vocabulary",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vocabulary"):
        describe_vocabulary("test-instance_id", "test-vocabulary_id", region_name=REGION)


def test_disassociate_analytics_data_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_analytics_data_set("test-instance_id", "test-data_set_id", region_name=REGION)
    mock_client.disassociate_analytics_data_set.assert_called_once()


def test_disassociate_analytics_data_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_analytics_data_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_analytics_data_set",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate analytics data set"):
        disassociate_analytics_data_set("test-instance_id", "test-data_set_id", region_name=REGION)


def test_disassociate_approved_origin(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_approved_origin.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_approved_origin("test-instance_id", "test-origin", region_name=REGION)
    mock_client.disassociate_approved_origin.assert_called_once()


def test_disassociate_approved_origin_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_approved_origin.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_approved_origin",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate approved origin"):
        disassociate_approved_origin("test-instance_id", "test-origin", region_name=REGION)


def test_disassociate_bot(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_bot("test-instance_id", region_name=REGION)
    mock_client.disassociate_bot.assert_called_once()


def test_disassociate_bot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_bot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_bot",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate bot"):
        disassociate_bot("test-instance_id", region_name=REGION)


def test_disassociate_email_address_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_email_address_alias.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_email_address_alias("test-email_address_id", "test-instance_id", {}, region_name=REGION)
    mock_client.disassociate_email_address_alias.assert_called_once()


def test_disassociate_email_address_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_email_address_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_email_address_alias",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate email address alias"):
        disassociate_email_address_alias("test-email_address_id", "test-instance_id", {}, region_name=REGION)


def test_disassociate_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_flow.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_flow("test-instance_id", "test-resource_id", "test-resource_type", region_name=REGION)
    mock_client.disassociate_flow.assert_called_once()


def test_disassociate_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_flow",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate flow"):
        disassociate_flow("test-instance_id", "test-resource_id", "test-resource_type", region_name=REGION)


def test_disassociate_instance_storage_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", region_name=REGION)
    mock_client.disassociate_instance_storage_config.assert_called_once()


def test_disassociate_instance_storage_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_instance_storage_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_instance_storage_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate instance storage config"):
        disassociate_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", region_name=REGION)


def test_disassociate_lambda_function(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_lambda_function.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_lambda_function("test-instance_id", "test-function_arn", region_name=REGION)
    mock_client.disassociate_lambda_function.assert_called_once()


def test_disassociate_lambda_function_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_lambda_function.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_lambda_function",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate lambda function"):
        disassociate_lambda_function("test-instance_id", "test-function_arn", region_name=REGION)


def test_disassociate_lex_bot(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_lex_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_lex_bot("test-instance_id", "test-bot_name", "test-lex_region", region_name=REGION)
    mock_client.disassociate_lex_bot.assert_called_once()


def test_disassociate_lex_bot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_lex_bot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_lex_bot",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate lex bot"):
        disassociate_lex_bot("test-instance_id", "test-bot_name", "test-lex_region", region_name=REGION)


def test_disassociate_phone_number_contact_flow(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_phone_number_contact_flow.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", region_name=REGION)
    mock_client.disassociate_phone_number_contact_flow.assert_called_once()


def test_disassociate_phone_number_contact_flow_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_phone_number_contact_flow.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_phone_number_contact_flow",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate phone number contact flow"):
        disassociate_phone_number_contact_flow("test-phone_number_id", "test-instance_id", region_name=REGION)


def test_disassociate_queue_quick_connects(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_queue_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_queue_quick_connects("test-instance_id", "test-queue_id", [], region_name=REGION)
    mock_client.disassociate_queue_quick_connects.assert_called_once()


def test_disassociate_queue_quick_connects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_queue_quick_connects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_queue_quick_connects",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate queue quick connects"):
        disassociate_queue_quick_connects("test-instance_id", "test-queue_id", [], region_name=REGION)


def test_disassociate_routing_profile_queues(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_routing_profile_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)
    mock_client.disassociate_routing_profile_queues.assert_called_once()


def test_disassociate_routing_profile_queues_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_routing_profile_queues.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_routing_profile_queues",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate routing profile queues"):
        disassociate_routing_profile_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)


def test_disassociate_security_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_security_key.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_security_key("test-instance_id", "test-association_id", region_name=REGION)
    mock_client.disassociate_security_key.assert_called_once()


def test_disassociate_security_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_security_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_security_key",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate security key"):
        disassociate_security_key("test-instance_id", "test-association_id", region_name=REGION)


def test_disassociate_traffic_distribution_group_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_traffic_distribution_group_user.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", region_name=REGION)
    mock_client.disassociate_traffic_distribution_group_user.assert_called_once()


def test_disassociate_traffic_distribution_group_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_traffic_distribution_group_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_traffic_distribution_group_user",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate traffic distribution group user"):
        disassociate_traffic_distribution_group_user("test-traffic_distribution_group_id", "test-user_id", "test-instance_id", region_name=REGION)


def test_disassociate_user_proficiencies(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_user_proficiencies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_user_proficiencies("test-instance_id", "test-user_id", [], region_name=REGION)
    mock_client.disassociate_user_proficiencies.assert_called_once()


def test_disassociate_user_proficiencies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_user_proficiencies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_user_proficiencies",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate user proficiencies"):
        disassociate_user_proficiencies("test-instance_id", "test-user_id", [], region_name=REGION)


def test_dismiss_user_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.dismiss_user_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    dismiss_user_contact("test-user_id", "test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.dismiss_user_contact.assert_called_once()


def test_dismiss_user_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.dismiss_user_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "dismiss_user_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to dismiss user contact"):
        dismiss_user_contact("test-user_id", "test-instance_id", "test-contact_id", region_name=REGION)


def test_get_attached_file(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_attached_file.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", region_name=REGION)
    mock_client.get_attached_file.assert_called_once()


def test_get_attached_file_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_attached_file.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_attached_file",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get attached file"):
        get_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", region_name=REGION)


def test_get_contact_metrics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_contact_metrics.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_contact_metrics("test-instance_id", "test-contact_id", [], region_name=REGION)
    mock_client.get_contact_metrics.assert_called_once()


def test_get_contact_metrics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_contact_metrics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_contact_metrics",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get contact metrics"):
        get_contact_metrics("test-instance_id", "test-contact_id", [], region_name=REGION)


def test_get_current_user_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_current_user_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_current_user_data("test-instance_id", {}, region_name=REGION)
    mock_client.get_current_user_data.assert_called_once()


def test_get_current_user_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_current_user_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_current_user_data",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get current user data"):
        get_current_user_data("test-instance_id", {}, region_name=REGION)


def test_get_effective_hours_of_operations(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_effective_hours_of_operations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_effective_hours_of_operations("test-instance_id", "test-hours_of_operation_id", "test-from_date", "test-to_date", region_name=REGION)
    mock_client.get_effective_hours_of_operations.assert_called_once()


def test_get_effective_hours_of_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_effective_hours_of_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_effective_hours_of_operations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get effective hours of operations"):
        get_effective_hours_of_operations("test-instance_id", "test-hours_of_operation_id", "test-from_date", "test-to_date", region_name=REGION)


def test_get_federation_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_federation_token.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_federation_token("test-instance_id", region_name=REGION)
    mock_client.get_federation_token.assert_called_once()


def test_get_federation_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_federation_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_federation_token",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get federation token"):
        get_federation_token("test-instance_id", region_name=REGION)


def test_get_flow_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_flow_association("test-instance_id", "test-resource_id", "test-resource_type", region_name=REGION)
    mock_client.get_flow_association.assert_called_once()


def test_get_flow_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_flow_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_flow_association",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get flow association"):
        get_flow_association("test-instance_id", "test-resource_id", "test-resource_type", region_name=REGION)


def test_get_metric_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_metric_data("test-instance_id", "test-start_time", "test-end_time", {}, [], region_name=REGION)
    mock_client.get_metric_data.assert_called_once()


def test_get_metric_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_metric_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_metric_data",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get metric data"):
        get_metric_data("test-instance_id", "test-start_time", "test-end_time", {}, [], region_name=REGION)


def test_get_metric_data_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_metric_data_v2.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_metric_data_v2("test-resource_arn", "test-start_time", "test-end_time", [], [], region_name=REGION)
    mock_client.get_metric_data_v2.assert_called_once()


def test_get_metric_data_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_metric_data_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_metric_data_v2",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get metric data v2"):
        get_metric_data_v2("test-resource_arn", "test-start_time", "test-end_time", [], [], region_name=REGION)


def test_get_prompt_file(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prompt_file.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_prompt_file("test-instance_id", "test-prompt_id", region_name=REGION)
    mock_client.get_prompt_file.assert_called_once()


def test_get_prompt_file_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prompt_file.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_prompt_file",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get prompt file"):
        get_prompt_file("test-instance_id", "test-prompt_id", region_name=REGION)


def test_get_task_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_task_template("test-instance_id", "test-task_template_id", region_name=REGION)
    mock_client.get_task_template.assert_called_once()


def test_get_task_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_task_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_task_template",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get task template"):
        get_task_template("test-instance_id", "test-task_template_id", region_name=REGION)


def test_get_traffic_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_distribution.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_traffic_distribution("test-id", region_name=REGION)
    mock_client.get_traffic_distribution.assert_called_once()


def test_get_traffic_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_traffic_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_traffic_distribution",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get traffic distribution"):
        get_traffic_distribution("test-id", region_name=REGION)


def test_import_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    import_phone_number("test-instance_id", "test-source_phone_number_arn", region_name=REGION)
    mock_client.import_phone_number.assert_called_once()


def test_import_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_phone_number",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import phone number"):
        import_phone_number("test-instance_id", "test-source_phone_number_arn", region_name=REGION)


def test_list_agent_statuses(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_statuses.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_agent_statuses("test-instance_id", region_name=REGION)
    mock_client.list_agent_statuses.assert_called_once()


def test_list_agent_statuses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_agent_statuses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_agent_statuses",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list agent statuses"):
        list_agent_statuses("test-instance_id", region_name=REGION)


def test_list_analytics_data_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_analytics_data_associations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_analytics_data_associations("test-instance_id", region_name=REGION)
    mock_client.list_analytics_data_associations.assert_called_once()


def test_list_analytics_data_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_analytics_data_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_analytics_data_associations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list analytics data associations"):
        list_analytics_data_associations("test-instance_id", region_name=REGION)


def test_list_analytics_data_lake_data_sets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_analytics_data_lake_data_sets.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_analytics_data_lake_data_sets("test-instance_id", region_name=REGION)
    mock_client.list_analytics_data_lake_data_sets.assert_called_once()


def test_list_analytics_data_lake_data_sets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_analytics_data_lake_data_sets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_analytics_data_lake_data_sets",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list analytics data lake data sets"):
        list_analytics_data_lake_data_sets("test-instance_id", region_name=REGION)


def test_list_approved_origins(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_approved_origins.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_approved_origins("test-instance_id", region_name=REGION)
    mock_client.list_approved_origins.assert_called_once()


def test_list_approved_origins_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_approved_origins.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_approved_origins",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list approved origins"):
        list_approved_origins("test-instance_id", region_name=REGION)


def test_list_associated_contacts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_associated_contacts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_associated_contacts("test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.list_associated_contacts.assert_called_once()


def test_list_associated_contacts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_associated_contacts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_associated_contacts",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list associated contacts"):
        list_associated_contacts("test-instance_id", "test-contact_id", region_name=REGION)


def test_list_authentication_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_authentication_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_authentication_profiles("test-instance_id", region_name=REGION)
    mock_client.list_authentication_profiles.assert_called_once()


def test_list_authentication_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_authentication_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_authentication_profiles",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list authentication profiles"):
        list_authentication_profiles("test-instance_id", region_name=REGION)


def test_list_bots(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bots.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_bots("test-instance_id", "test-lex_version", region_name=REGION)
    mock_client.list_bots.assert_called_once()


def test_list_bots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_bots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_bots",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list bots"):
        list_bots("test-instance_id", "test-lex_version", region_name=REGION)


def test_list_contact_evaluations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_evaluations("test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.list_contact_evaluations.assert_called_once()


def test_list_contact_evaluations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_evaluations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_contact_evaluations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list contact evaluations"):
        list_contact_evaluations("test-instance_id", "test-contact_id", region_name=REGION)


def test_list_contact_flow_modules(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_flow_modules.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_flow_modules("test-instance_id", region_name=REGION)
    mock_client.list_contact_flow_modules.assert_called_once()


def test_list_contact_flow_modules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_flow_modules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_contact_flow_modules",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list contact flow modules"):
        list_contact_flow_modules("test-instance_id", region_name=REGION)


def test_list_contact_flow_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_flow_versions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_flow_versions("test-instance_id", "test-contact_flow_id", region_name=REGION)
    mock_client.list_contact_flow_versions.assert_called_once()


def test_list_contact_flow_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_flow_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_contact_flow_versions",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list contact flow versions"):
        list_contact_flow_versions("test-instance_id", "test-contact_flow_id", region_name=REGION)


def test_list_contact_references(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_references.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_references("test-instance_id", "test-contact_id", [], region_name=REGION)
    mock_client.list_contact_references.assert_called_once()


def test_list_contact_references_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_contact_references.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_contact_references",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list contact references"):
        list_contact_references("test-instance_id", "test-contact_id", [], region_name=REGION)


def test_list_default_vocabularies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_default_vocabularies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_default_vocabularies("test-instance_id", region_name=REGION)
    mock_client.list_default_vocabularies.assert_called_once()


def test_list_default_vocabularies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_default_vocabularies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_default_vocabularies",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list default vocabularies"):
        list_default_vocabularies("test-instance_id", region_name=REGION)


def test_list_evaluation_form_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_form_versions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_evaluation_form_versions("test-instance_id", "test-evaluation_form_id", region_name=REGION)
    mock_client.list_evaluation_form_versions.assert_called_once()


def test_list_evaluation_form_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_form_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_evaluation_form_versions",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list evaluation form versions"):
        list_evaluation_form_versions("test-instance_id", "test-evaluation_form_id", region_name=REGION)


def test_list_evaluation_forms(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_forms.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_evaluation_forms("test-instance_id", region_name=REGION)
    mock_client.list_evaluation_forms.assert_called_once()


def test_list_evaluation_forms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_evaluation_forms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_evaluation_forms",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list evaluation forms"):
        list_evaluation_forms("test-instance_id", region_name=REGION)


def test_list_flow_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_associations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_flow_associations("test-instance_id", region_name=REGION)
    mock_client.list_flow_associations.assert_called_once()


def test_list_flow_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_flow_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_flow_associations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list flow associations"):
        list_flow_associations("test-instance_id", region_name=REGION)


def test_list_hours_of_operation_overrides(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hours_of_operation_overrides.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_hours_of_operation_overrides("test-instance_id", "test-hours_of_operation_id", region_name=REGION)
    mock_client.list_hours_of_operation_overrides.assert_called_once()


def test_list_hours_of_operation_overrides_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hours_of_operation_overrides.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_hours_of_operation_overrides",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list hours of operation overrides"):
        list_hours_of_operation_overrides("test-instance_id", "test-hours_of_operation_id", region_name=REGION)


def test_list_hours_of_operations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hours_of_operations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_hours_of_operations("test-instance_id", region_name=REGION)
    mock_client.list_hours_of_operations.assert_called_once()


def test_list_hours_of_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_hours_of_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_hours_of_operations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list hours of operations"):
        list_hours_of_operations("test-instance_id", region_name=REGION)


def test_list_instance_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_attributes.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_instance_attributes("test-instance_id", region_name=REGION)
    mock_client.list_instance_attributes.assert_called_once()


def test_list_instance_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instance_attributes",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instance attributes"):
        list_instance_attributes("test-instance_id", region_name=REGION)


def test_list_instance_storage_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_storage_configs.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_instance_storage_configs("test-instance_id", "test-resource_type", region_name=REGION)
    mock_client.list_instance_storage_configs.assert_called_once()


def test_list_instance_storage_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_storage_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instance_storage_configs",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instance storage configs"):
        list_instance_storage_configs("test-instance_id", "test-resource_type", region_name=REGION)


def test_list_integration_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_integration_associations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_integration_associations("test-instance_id", region_name=REGION)
    mock_client.list_integration_associations.assert_called_once()


def test_list_integration_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_integration_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_integration_associations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list integration associations"):
        list_integration_associations("test-instance_id", region_name=REGION)


def test_list_lambda_functions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lambda_functions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_lambda_functions("test-instance_id", region_name=REGION)
    mock_client.list_lambda_functions.assert_called_once()


def test_list_lambda_functions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lambda_functions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_lambda_functions",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list lambda functions"):
        list_lambda_functions("test-instance_id", region_name=REGION)


def test_list_lex_bots(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lex_bots.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_lex_bots("test-instance_id", region_name=REGION)
    mock_client.list_lex_bots.assert_called_once()


def test_list_lex_bots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_lex_bots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_lex_bots",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list lex bots"):
        list_lex_bots("test-instance_id", region_name=REGION)


def test_list_phone_numbers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_phone_numbers.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_phone_numbers("test-instance_id", region_name=REGION)
    mock_client.list_phone_numbers.assert_called_once()


def test_list_phone_numbers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_phone_numbers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_phone_numbers",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list phone numbers"):
        list_phone_numbers("test-instance_id", region_name=REGION)


def test_list_phone_numbers_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_phone_numbers_v2.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_phone_numbers_v2(region_name=REGION)
    mock_client.list_phone_numbers_v2.assert_called_once()


def test_list_phone_numbers_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_phone_numbers_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_phone_numbers_v2",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list phone numbers v2"):
        list_phone_numbers_v2(region_name=REGION)


def test_list_predefined_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_predefined_attributes.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_predefined_attributes("test-instance_id", region_name=REGION)
    mock_client.list_predefined_attributes.assert_called_once()


def test_list_predefined_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_predefined_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_predefined_attributes",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list predefined attributes"):
        list_predefined_attributes("test-instance_id", region_name=REGION)


def test_list_prompts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_prompts("test-instance_id", region_name=REGION)
    mock_client.list_prompts.assert_called_once()


def test_list_prompts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prompts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_prompts",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list prompts"):
        list_prompts("test-instance_id", region_name=REGION)


def test_list_queue_quick_connects(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_queue_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_queue_quick_connects("test-instance_id", "test-queue_id", region_name=REGION)
    mock_client.list_queue_quick_connects.assert_called_once()


def test_list_queue_quick_connects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_queue_quick_connects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_queue_quick_connects",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list queue quick connects"):
        list_queue_quick_connects("test-instance_id", "test-queue_id", region_name=REGION)


def test_list_quick_connects(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_quick_connects("test-instance_id", region_name=REGION)
    mock_client.list_quick_connects.assert_called_once()


def test_list_quick_connects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_quick_connects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_quick_connects",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list quick connects"):
        list_quick_connects("test-instance_id", region_name=REGION)


def test_list_realtime_contact_analysis_segments_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_realtime_contact_analysis_segments_v2.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_realtime_contact_analysis_segments_v2("test-instance_id", "test-contact_id", "test-output_type", [], region_name=REGION)
    mock_client.list_realtime_contact_analysis_segments_v2.assert_called_once()


def test_list_realtime_contact_analysis_segments_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_realtime_contact_analysis_segments_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_realtime_contact_analysis_segments_v2",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list realtime contact analysis segments v2"):
        list_realtime_contact_analysis_segments_v2("test-instance_id", "test-contact_id", "test-output_type", [], region_name=REGION)


def test_list_routing_profile_manual_assignment_queues(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_routing_profile_manual_assignment_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_routing_profile_manual_assignment_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)
    mock_client.list_routing_profile_manual_assignment_queues.assert_called_once()


def test_list_routing_profile_manual_assignment_queues_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_routing_profile_manual_assignment_queues.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_routing_profile_manual_assignment_queues",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list routing profile manual assignment queues"):
        list_routing_profile_manual_assignment_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)


def test_list_routing_profile_queues(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_routing_profile_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)
    mock_client.list_routing_profile_queues.assert_called_once()


def test_list_routing_profile_queues_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_routing_profile_queues.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_routing_profile_queues",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list routing profile queues"):
        list_routing_profile_queues("test-instance_id", "test-routing_profile_id", region_name=REGION)


def test_list_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_rules.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_rules("test-instance_id", region_name=REGION)
    mock_client.list_rules.assert_called_once()


def test_list_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_rules",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list rules"):
        list_rules("test-instance_id", region_name=REGION)


def test_list_security_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_keys.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_keys("test-instance_id", region_name=REGION)
    mock_client.list_security_keys.assert_called_once()


def test_list_security_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_keys",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list security keys"):
        list_security_keys("test-instance_id", region_name=REGION)


def test_list_security_profile_applications(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_profile_applications.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_profile_applications("test-security_profile_id", "test-instance_id", region_name=REGION)
    mock_client.list_security_profile_applications.assert_called_once()


def test_list_security_profile_applications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_profile_applications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_profile_applications",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list security profile applications"):
        list_security_profile_applications("test-security_profile_id", "test-instance_id", region_name=REGION)


def test_list_security_profile_permissions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_profile_permissions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_profile_permissions("test-security_profile_id", "test-instance_id", region_name=REGION)
    mock_client.list_security_profile_permissions.assert_called_once()


def test_list_security_profile_permissions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_profile_permissions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_profile_permissions",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list security profile permissions"):
        list_security_profile_permissions("test-security_profile_id", "test-instance_id", region_name=REGION)


def test_list_security_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_profiles("test-instance_id", region_name=REGION)
    mock_client.list_security_profiles.assert_called_once()


def test_list_security_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_profiles",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list security profiles"):
        list_security_profiles("test-instance_id", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_task_templates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_task_templates.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_task_templates("test-instance_id", region_name=REGION)
    mock_client.list_task_templates.assert_called_once()


def test_list_task_templates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_task_templates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_task_templates",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list task templates"):
        list_task_templates("test-instance_id", region_name=REGION)


def test_list_traffic_distribution_group_users(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_distribution_group_users.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_traffic_distribution_group_users("test-traffic_distribution_group_id", region_name=REGION)
    mock_client.list_traffic_distribution_group_users.assert_called_once()


def test_list_traffic_distribution_group_users_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_distribution_group_users.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_distribution_group_users",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic distribution group users"):
        list_traffic_distribution_group_users("test-traffic_distribution_group_id", region_name=REGION)


def test_list_traffic_distribution_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_distribution_groups.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_traffic_distribution_groups(region_name=REGION)
    mock_client.list_traffic_distribution_groups.assert_called_once()


def test_list_traffic_distribution_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_traffic_distribution_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_traffic_distribution_groups",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list traffic distribution groups"):
        list_traffic_distribution_groups(region_name=REGION)


def test_list_use_cases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_use_cases.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_use_cases("test-instance_id", "test-integration_association_id", region_name=REGION)
    mock_client.list_use_cases.assert_called_once()


def test_list_use_cases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_use_cases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_use_cases",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list use cases"):
        list_use_cases("test-instance_id", "test-integration_association_id", region_name=REGION)


def test_list_user_hierarchy_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_hierarchy_groups.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_user_hierarchy_groups("test-instance_id", region_name=REGION)
    mock_client.list_user_hierarchy_groups.assert_called_once()


def test_list_user_hierarchy_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_hierarchy_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_hierarchy_groups",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user hierarchy groups"):
        list_user_hierarchy_groups("test-instance_id", region_name=REGION)


def test_list_user_proficiencies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_proficiencies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_user_proficiencies("test-instance_id", "test-user_id", region_name=REGION)
    mock_client.list_user_proficiencies.assert_called_once()


def test_list_user_proficiencies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_proficiencies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_proficiencies",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user proficiencies"):
        list_user_proficiencies("test-instance_id", "test-user_id", region_name=REGION)


def test_list_view_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_view_versions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_view_versions("test-instance_id", "test-view_id", region_name=REGION)
    mock_client.list_view_versions.assert_called_once()


def test_list_view_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_view_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_view_versions",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list view versions"):
        list_view_versions("test-instance_id", "test-view_id", region_name=REGION)


def test_list_views(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_views.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_views("test-instance_id", region_name=REGION)
    mock_client.list_views.assert_called_once()


def test_list_views_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_views.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_views",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list views"):
        list_views("test-instance_id", region_name=REGION)


def test_monitor_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.monitor_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    monitor_contact("test-instance_id", "test-contact_id", "test-user_id", region_name=REGION)
    mock_client.monitor_contact.assert_called_once()


def test_monitor_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.monitor_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "monitor_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to monitor contact"):
        monitor_contact("test-instance_id", "test-contact_id", "test-user_id", region_name=REGION)


def test_pause_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.pause_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    pause_contact("test-contact_id", "test-instance_id", region_name=REGION)
    mock_client.pause_contact.assert_called_once()


def test_pause_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.pause_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "pause_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to pause contact"):
        pause_contact("test-contact_id", "test-instance_id", region_name=REGION)


def test_put_user_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_user_status.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    put_user_status("test-user_id", "test-instance_id", "test-agent_status_id", region_name=REGION)
    mock_client.put_user_status.assert_called_once()


def test_put_user_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_user_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_user_status",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put user status"):
        put_user_status("test-user_id", "test-instance_id", "test-agent_status_id", region_name=REGION)


def test_release_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    release_phone_number("test-phone_number_id", region_name=REGION)
    mock_client.release_phone_number.assert_called_once()


def test_release_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.release_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "release_phone_number",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to release phone number"):
        release_phone_number("test-phone_number_id", region_name=REGION)


def test_replicate_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.replicate_instance.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    replicate_instance("test-instance_id", "test-replica_region", "test-replica_alias", region_name=REGION)
    mock_client.replicate_instance.assert_called_once()


def test_replicate_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.replicate_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "replicate_instance",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to replicate instance"):
        replicate_instance("test-instance_id", "test-replica_region", "test-replica_alias", region_name=REGION)


def test_resume_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    resume_contact("test-contact_id", "test-instance_id", region_name=REGION)
    mock_client.resume_contact.assert_called_once()


def test_resume_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume contact"):
        resume_contact("test-contact_id", "test-instance_id", region_name=REGION)


def test_resume_contact_recording(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    resume_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", region_name=REGION)
    mock_client.resume_contact_recording.assert_called_once()


def test_resume_contact_recording_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_contact_recording.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_contact_recording",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume contact recording"):
        resume_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", region_name=REGION)


def test_search_agent_statuses(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_agent_statuses.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_agent_statuses("test-instance_id", region_name=REGION)
    mock_client.search_agent_statuses.assert_called_once()


def test_search_agent_statuses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_agent_statuses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_agent_statuses",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search agent statuses"):
        search_agent_statuses("test-instance_id", region_name=REGION)


def test_search_available_phone_numbers(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_available_phone_numbers.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_available_phone_numbers("test-phone_number_country_code", "test-phone_number_type", region_name=REGION)
    mock_client.search_available_phone_numbers.assert_called_once()


def test_search_available_phone_numbers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_available_phone_numbers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_available_phone_numbers",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search available phone numbers"):
        search_available_phone_numbers("test-phone_number_country_code", "test-phone_number_type", region_name=REGION)


def test_search_contact_evaluations(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contact_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contact_evaluations("test-instance_id", region_name=REGION)
    mock_client.search_contact_evaluations.assert_called_once()


def test_search_contact_evaluations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contact_evaluations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_contact_evaluations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search contact evaluations"):
        search_contact_evaluations("test-instance_id", region_name=REGION)


def test_search_contact_flow_modules(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contact_flow_modules.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contact_flow_modules("test-instance_id", region_name=REGION)
    mock_client.search_contact_flow_modules.assert_called_once()


def test_search_contact_flow_modules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contact_flow_modules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_contact_flow_modules",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search contact flow modules"):
        search_contact_flow_modules("test-instance_id", region_name=REGION)


def test_search_contact_flows(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contact_flows.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contact_flows("test-instance_id", region_name=REGION)
    mock_client.search_contact_flows.assert_called_once()


def test_search_contact_flows_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contact_flows.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_contact_flows",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search contact flows"):
        search_contact_flows("test-instance_id", region_name=REGION)


def test_search_contacts(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contacts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contacts("test-instance_id", {}, region_name=REGION)
    mock_client.search_contacts.assert_called_once()


def test_search_contacts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_contacts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_contacts",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search contacts"):
        search_contacts("test-instance_id", {}, region_name=REGION)


def test_search_email_addresses(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_email_addresses.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_email_addresses("test-instance_id", region_name=REGION)
    mock_client.search_email_addresses.assert_called_once()


def test_search_email_addresses_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_email_addresses.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_email_addresses",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search email addresses"):
        search_email_addresses("test-instance_id", region_name=REGION)


def test_search_evaluation_forms(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_evaluation_forms.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_evaluation_forms("test-instance_id", region_name=REGION)
    mock_client.search_evaluation_forms.assert_called_once()


def test_search_evaluation_forms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_evaluation_forms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_evaluation_forms",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search evaluation forms"):
        search_evaluation_forms("test-instance_id", region_name=REGION)


def test_search_hours_of_operation_overrides(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_hours_of_operation_overrides.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_hours_of_operation_overrides("test-instance_id", region_name=REGION)
    mock_client.search_hours_of_operation_overrides.assert_called_once()


def test_search_hours_of_operation_overrides_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_hours_of_operation_overrides.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_hours_of_operation_overrides",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search hours of operation overrides"):
        search_hours_of_operation_overrides("test-instance_id", region_name=REGION)


def test_search_hours_of_operations(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_hours_of_operations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_hours_of_operations("test-instance_id", region_name=REGION)
    mock_client.search_hours_of_operations.assert_called_once()


def test_search_hours_of_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_hours_of_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_hours_of_operations",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search hours of operations"):
        search_hours_of_operations("test-instance_id", region_name=REGION)


def test_search_predefined_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_predefined_attributes.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_predefined_attributes("test-instance_id", region_name=REGION)
    mock_client.search_predefined_attributes.assert_called_once()


def test_search_predefined_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_predefined_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_predefined_attributes",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search predefined attributes"):
        search_predefined_attributes("test-instance_id", region_name=REGION)


def test_search_prompts(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_prompts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_prompts("test-instance_id", region_name=REGION)
    mock_client.search_prompts.assert_called_once()


def test_search_prompts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_prompts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_prompts",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search prompts"):
        search_prompts("test-instance_id", region_name=REGION)


def test_search_queues(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_queues("test-instance_id", region_name=REGION)
    mock_client.search_queues.assert_called_once()


def test_search_queues_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_queues.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_queues",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search queues"):
        search_queues("test-instance_id", region_name=REGION)


def test_search_quick_connects(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_quick_connects("test-instance_id", region_name=REGION)
    mock_client.search_quick_connects.assert_called_once()


def test_search_quick_connects_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_quick_connects.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_quick_connects",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search quick connects"):
        search_quick_connects("test-instance_id", region_name=REGION)


def test_search_resource_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_resource_tags.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_resource_tags("test-instance_id", region_name=REGION)
    mock_client.search_resource_tags.assert_called_once()


def test_search_resource_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_resource_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_resource_tags",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search resource tags"):
        search_resource_tags("test-instance_id", region_name=REGION)


def test_search_routing_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_routing_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_routing_profiles("test-instance_id", region_name=REGION)
    mock_client.search_routing_profiles.assert_called_once()


def test_search_routing_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_routing_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_routing_profiles",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search routing profiles"):
        search_routing_profiles("test-instance_id", region_name=REGION)


def test_search_security_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_security_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_security_profiles("test-instance_id", region_name=REGION)
    mock_client.search_security_profiles.assert_called_once()


def test_search_security_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_security_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_security_profiles",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search security profiles"):
        search_security_profiles("test-instance_id", region_name=REGION)


def test_search_user_hierarchy_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_user_hierarchy_groups.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_user_hierarchy_groups("test-instance_id", region_name=REGION)
    mock_client.search_user_hierarchy_groups.assert_called_once()


def test_search_user_hierarchy_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_user_hierarchy_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_user_hierarchy_groups",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search user hierarchy groups"):
        search_user_hierarchy_groups("test-instance_id", region_name=REGION)


def test_search_users(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_users.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_users("test-instance_id", region_name=REGION)
    mock_client.search_users.assert_called_once()


def test_search_users_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_users.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_users",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search users"):
        search_users("test-instance_id", region_name=REGION)


def test_search_vocabularies(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_vocabularies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_vocabularies("test-instance_id", region_name=REGION)
    mock_client.search_vocabularies.assert_called_once()


def test_search_vocabularies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.search_vocabularies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "search_vocabularies",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to search vocabularies"):
        search_vocabularies("test-instance_id", region_name=REGION)


def test_send_chat_integration_event(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_chat_integration_event.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    send_chat_integration_event("test-source_id", "test-destination_id", {}, region_name=REGION)
    mock_client.send_chat_integration_event.assert_called_once()


def test_send_chat_integration_event_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_chat_integration_event.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_chat_integration_event",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send chat integration event"):
        send_chat_integration_event("test-source_id", "test-destination_id", {}, region_name=REGION)


def test_send_outbound_email(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_outbound_email.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    send_outbound_email("test-instance_id", {}, {}, {}, "test-traffic_type", region_name=REGION)
    mock_client.send_outbound_email.assert_called_once()


def test_send_outbound_email_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.send_outbound_email.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "send_outbound_email",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to send outbound email"):
        send_outbound_email("test-instance_id", {}, {}, {}, "test-traffic_type", region_name=REGION)


def test_start_attached_file_upload(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_attached_file_upload.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_attached_file_upload("test-instance_id", "test-file_name", 1, "test-file_use_case_type", "test-associated_resource_arn", region_name=REGION)
    mock_client.start_attached_file_upload.assert_called_once()


def test_start_attached_file_upload_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_attached_file_upload.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_attached_file_upload",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start attached file upload"):
        start_attached_file_upload("test-instance_id", "test-file_name", 1, "test-file_use_case_type", "test-associated_resource_arn", region_name=REGION)


def test_start_contact_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_contact_evaluation("test-instance_id", "test-contact_id", "test-evaluation_form_id", region_name=REGION)
    mock_client.start_contact_evaluation.assert_called_once()


def test_start_contact_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_contact_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_contact_evaluation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start contact evaluation"):
        start_contact_evaluation("test-instance_id", "test-contact_id", "test-evaluation_form_id", region_name=REGION)


def test_start_contact_recording(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", {}, region_name=REGION)
    mock_client.start_contact_recording.assert_called_once()


def test_start_contact_recording_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_contact_recording.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_contact_recording",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start contact recording"):
        start_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", {}, region_name=REGION)


def test_start_contact_streaming(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_contact_streaming.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_contact_streaming("test-instance_id", "test-contact_id", {}, "test-client_token", region_name=REGION)
    mock_client.start_contact_streaming.assert_called_once()


def test_start_contact_streaming_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_contact_streaming.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_contact_streaming",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start contact streaming"):
        start_contact_streaming("test-instance_id", "test-contact_id", {}, "test-client_token", region_name=REGION)


def test_start_email_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_email_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_email_contact("test-instance_id", {}, "test-destination_email_address", {}, region_name=REGION)
    mock_client.start_email_contact.assert_called_once()


def test_start_email_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_email_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_email_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start email contact"):
        start_email_contact("test-instance_id", {}, "test-destination_email_address", {}, region_name=REGION)


def test_start_outbound_chat_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_outbound_chat_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_outbound_chat_contact({}, {}, "test-instance_id", {}, "test-contact_flow_id", region_name=REGION)
    mock_client.start_outbound_chat_contact.assert_called_once()


def test_start_outbound_chat_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_outbound_chat_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_outbound_chat_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start outbound chat contact"):
        start_outbound_chat_contact({}, {}, "test-instance_id", {}, "test-contact_flow_id", region_name=REGION)


def test_start_outbound_email_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_outbound_email_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_outbound_email_contact("test-instance_id", "test-contact_id", {}, {}, region_name=REGION)
    mock_client.start_outbound_email_contact.assert_called_once()


def test_start_outbound_email_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_outbound_email_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_outbound_email_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start outbound email contact"):
        start_outbound_email_contact("test-instance_id", "test-contact_id", {}, {}, region_name=REGION)


def test_start_screen_sharing(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_screen_sharing.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_screen_sharing("test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.start_screen_sharing.assert_called_once()


def test_start_screen_sharing_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_screen_sharing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_screen_sharing",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start screen sharing"):
        start_screen_sharing("test-instance_id", "test-contact_id", region_name=REGION)


def test_start_web_rtc_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_web_rtc_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_web_rtc_contact("test-contact_flow_id", "test-instance_id", {}, region_name=REGION)
    mock_client.start_web_rtc_contact.assert_called_once()


def test_start_web_rtc_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_web_rtc_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_web_rtc_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start web rtc contact"):
        start_web_rtc_contact("test-contact_flow_id", "test-instance_id", {}, region_name=REGION)


def test_stop_contact_recording(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    stop_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", region_name=REGION)
    mock_client.stop_contact_recording.assert_called_once()


def test_stop_contact_recording_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_contact_recording.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_contact_recording",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop contact recording"):
        stop_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", region_name=REGION)


def test_stop_contact_streaming(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_contact_streaming.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    stop_contact_streaming("test-instance_id", "test-contact_id", "test-streaming_id", region_name=REGION)
    mock_client.stop_contact_streaming.assert_called_once()


def test_stop_contact_streaming_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_contact_streaming.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_contact_streaming",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop contact streaming"):
        stop_contact_streaming("test-instance_id", "test-contact_id", "test-streaming_id", region_name=REGION)


def test_submit_contact_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    submit_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)
    mock_client.submit_contact_evaluation.assert_called_once()


def test_submit_contact_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.submit_contact_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "submit_contact_evaluation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to submit contact evaluation"):
        submit_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)


def test_suspend_contact_recording(monkeypatch):
    mock_client = MagicMock()
    mock_client.suspend_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    suspend_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", region_name=REGION)
    mock_client.suspend_contact_recording.assert_called_once()


def test_suspend_contact_recording_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.suspend_contact_recording.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "suspend_contact_recording",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to suspend contact recording"):
        suspend_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", region_name=REGION)


def test_tag_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    tag_contact("test-contact_id", "test-instance_id", {}, region_name=REGION)
    mock_client.tag_contact.assert_called_once()


def test_tag_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag contact"):
        tag_contact("test-contact_id", "test-instance_id", {}, region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_transfer_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.transfer_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    transfer_contact("test-instance_id", "test-contact_id", "test-contact_flow_id", region_name=REGION)
    mock_client.transfer_contact.assert_called_once()


def test_transfer_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.transfer_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "transfer_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to transfer contact"):
        transfer_contact("test-instance_id", "test-contact_id", "test-contact_flow_id", region_name=REGION)


def test_untag_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    untag_contact("test-contact_id", "test-instance_id", [], region_name=REGION)
    mock_client.untag_contact.assert_called_once()


def test_untag_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag contact"):
        untag_contact("test-contact_id", "test-instance_id", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_agent_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_status.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_agent_status("test-instance_id", "test-agent_status_id", region_name=REGION)
    mock_client.update_agent_status.assert_called_once()


def test_update_agent_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_agent_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_agent_status",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update agent status"):
        update_agent_status("test-instance_id", "test-agent_status_id", region_name=REGION)


def test_update_authentication_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_authentication_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_authentication_profile("test-authentication_profile_id", "test-instance_id", region_name=REGION)
    mock_client.update_authentication_profile.assert_called_once()


def test_update_authentication_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_authentication_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_authentication_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update authentication profile"):
        update_authentication_profile("test-authentication_profile_id", "test-instance_id", region_name=REGION)


def test_update_contact(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact("test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.update_contact.assert_called_once()


def test_update_contact_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact"):
        update_contact("test-instance_id", "test-contact_id", region_name=REGION)


def test_update_contact_evaluation(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)
    mock_client.update_contact_evaluation.assert_called_once()


def test_update_contact_evaluation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_evaluation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_evaluation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact evaluation"):
        update_contact_evaluation("test-instance_id", "test-evaluation_id", region_name=REGION)


def test_update_contact_flow_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_metadata("test-instance_id", "test-contact_flow_id", region_name=REGION)
    mock_client.update_contact_flow_metadata.assert_called_once()


def test_update_contact_flow_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_flow_metadata",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact flow metadata"):
        update_contact_flow_metadata("test-instance_id", "test-contact_flow_id", region_name=REGION)


def test_update_contact_flow_module_content(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_module_content.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_module_content("test-instance_id", "test-contact_flow_module_id", "test-content", region_name=REGION)
    mock_client.update_contact_flow_module_content.assert_called_once()


def test_update_contact_flow_module_content_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_module_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_flow_module_content",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact flow module content"):
        update_contact_flow_module_content("test-instance_id", "test-contact_flow_module_id", "test-content", region_name=REGION)


def test_update_contact_flow_module_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_module_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_module_metadata("test-instance_id", "test-contact_flow_module_id", region_name=REGION)
    mock_client.update_contact_flow_module_metadata.assert_called_once()


def test_update_contact_flow_module_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_module_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_flow_module_metadata",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact flow module metadata"):
        update_contact_flow_module_metadata("test-instance_id", "test-contact_flow_module_id", region_name=REGION)


def test_update_contact_flow_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_name("test-instance_id", "test-contact_flow_id", region_name=REGION)
    mock_client.update_contact_flow_name.assert_called_once()


def test_update_contact_flow_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_flow_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_flow_name",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact flow name"):
        update_contact_flow_name("test-instance_id", "test-contact_flow_id", region_name=REGION)


def test_update_contact_routing_data(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_routing_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_routing_data("test-instance_id", "test-contact_id", region_name=REGION)
    mock_client.update_contact_routing_data.assert_called_once()


def test_update_contact_routing_data_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_routing_data.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_routing_data",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact routing data"):
        update_contact_routing_data("test-instance_id", "test-contact_id", region_name=REGION)


def test_update_contact_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_schedule.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_schedule("test-instance_id", "test-contact_id", "test-scheduled_time", region_name=REGION)
    mock_client.update_contact_schedule.assert_called_once()


def test_update_contact_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_contact_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_contact_schedule",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update contact schedule"):
        update_contact_schedule("test-instance_id", "test-contact_id", "test-scheduled_time", region_name=REGION)


def test_update_email_address_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_email_address_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_email_address_metadata("test-instance_id", "test-email_address_id", region_name=REGION)
    mock_client.update_email_address_metadata.assert_called_once()


def test_update_email_address_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_email_address_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_email_address_metadata",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update email address metadata"):
        update_email_address_metadata("test-instance_id", "test-email_address_id", region_name=REGION)


def test_update_evaluation_form(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, "test-title", [], region_name=REGION)
    mock_client.update_evaluation_form.assert_called_once()


def test_update_evaluation_form_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_evaluation_form.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_evaluation_form",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update evaluation form"):
        update_evaluation_form("test-instance_id", "test-evaluation_form_id", 1, "test-title", [], region_name=REGION)


def test_update_hours_of_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_hours_of_operation("test-instance_id", "test-hours_of_operation_id", region_name=REGION)
    mock_client.update_hours_of_operation.assert_called_once()


def test_update_hours_of_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_hours_of_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_hours_of_operation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update hours of operation"):
        update_hours_of_operation("test-instance_id", "test-hours_of_operation_id", region_name=REGION)


def test_update_hours_of_operation_override(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_hours_of_operation_override.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", region_name=REGION)
    mock_client.update_hours_of_operation_override.assert_called_once()


def test_update_hours_of_operation_override_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_hours_of_operation_override.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_hours_of_operation_override",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update hours of operation override"):
        update_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", region_name=REGION)


def test_update_instance_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_instance_attribute("test-instance_id", "test-attribute_type", "test-value", region_name=REGION)
    mock_client.update_instance_attribute.assert_called_once()


def test_update_instance_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_instance_attribute",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update instance attribute"):
        update_instance_attribute("test-instance_id", "test-attribute_type", "test-value", region_name=REGION)


def test_update_instance_storage_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", {}, region_name=REGION)
    mock_client.update_instance_storage_config.assert_called_once()


def test_update_instance_storage_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance_storage_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_instance_storage_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update instance storage config"):
        update_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", {}, region_name=REGION)


def test_update_participant_authentication(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_participant_authentication.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_participant_authentication("test-state", "test-instance_id", region_name=REGION)
    mock_client.update_participant_authentication.assert_called_once()


def test_update_participant_authentication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_participant_authentication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_participant_authentication",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update participant authentication"):
        update_participant_authentication("test-state", "test-instance_id", region_name=REGION)


def test_update_participant_role_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_participant_role_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_participant_role_config("test-instance_id", "test-contact_id", {}, region_name=REGION)
    mock_client.update_participant_role_config.assert_called_once()


def test_update_participant_role_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_participant_role_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_participant_role_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update participant role config"):
        update_participant_role_config("test-instance_id", "test-contact_id", {}, region_name=REGION)


def test_update_phone_number(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_phone_number("test-phone_number_id", region_name=REGION)
    mock_client.update_phone_number.assert_called_once()


def test_update_phone_number_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_phone_number.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_phone_number",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update phone number"):
        update_phone_number("test-phone_number_id", region_name=REGION)


def test_update_phone_number_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_phone_number_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_phone_number_metadata("test-phone_number_id", region_name=REGION)
    mock_client.update_phone_number_metadata.assert_called_once()


def test_update_phone_number_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_phone_number_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_phone_number_metadata",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update phone number metadata"):
        update_phone_number_metadata("test-phone_number_id", region_name=REGION)


def test_update_predefined_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_predefined_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_predefined_attribute("test-instance_id", "test-name", region_name=REGION)
    mock_client.update_predefined_attribute.assert_called_once()


def test_update_predefined_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_predefined_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_predefined_attribute",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update predefined attribute"):
        update_predefined_attribute("test-instance_id", "test-name", region_name=REGION)


def test_update_prompt(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_prompt.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_prompt("test-instance_id", "test-prompt_id", region_name=REGION)
    mock_client.update_prompt.assert_called_once()


def test_update_prompt_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_prompt.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_prompt",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update prompt"):
        update_prompt("test-instance_id", "test-prompt_id", region_name=REGION)


def test_update_queue_hours_of_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_hours_of_operation("test-instance_id", "test-queue_id", "test-hours_of_operation_id", region_name=REGION)
    mock_client.update_queue_hours_of_operation.assert_called_once()


def test_update_queue_hours_of_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_hours_of_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_queue_hours_of_operation",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update queue hours of operation"):
        update_queue_hours_of_operation("test-instance_id", "test-queue_id", "test-hours_of_operation_id", region_name=REGION)


def test_update_queue_max_contacts(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_max_contacts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_max_contacts("test-instance_id", "test-queue_id", region_name=REGION)
    mock_client.update_queue_max_contacts.assert_called_once()


def test_update_queue_max_contacts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_max_contacts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_queue_max_contacts",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update queue max contacts"):
        update_queue_max_contacts("test-instance_id", "test-queue_id", region_name=REGION)


def test_update_queue_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_name("test-instance_id", "test-queue_id", region_name=REGION)
    mock_client.update_queue_name.assert_called_once()


def test_update_queue_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_queue_name",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update queue name"):
        update_queue_name("test-instance_id", "test-queue_id", region_name=REGION)


def test_update_queue_outbound_caller_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_outbound_caller_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_outbound_caller_config("test-instance_id", "test-queue_id", {}, region_name=REGION)
    mock_client.update_queue_outbound_caller_config.assert_called_once()


def test_update_queue_outbound_caller_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_outbound_caller_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_queue_outbound_caller_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update queue outbound caller config"):
        update_queue_outbound_caller_config("test-instance_id", "test-queue_id", {}, region_name=REGION)


def test_update_queue_outbound_email_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_outbound_email_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_outbound_email_config("test-instance_id", "test-queue_id", {}, region_name=REGION)
    mock_client.update_queue_outbound_email_config.assert_called_once()


def test_update_queue_outbound_email_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_queue_outbound_email_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_queue_outbound_email_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update queue outbound email config"):
        update_queue_outbound_email_config("test-instance_id", "test-queue_id", {}, region_name=REGION)


def test_update_quick_connect_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_quick_connect_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_quick_connect_config("test-instance_id", "test-quick_connect_id", {}, region_name=REGION)
    mock_client.update_quick_connect_config.assert_called_once()


def test_update_quick_connect_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_quick_connect_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_quick_connect_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update quick connect config"):
        update_quick_connect_config("test-instance_id", "test-quick_connect_id", {}, region_name=REGION)


def test_update_quick_connect_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_quick_connect_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_quick_connect_name("test-instance_id", "test-quick_connect_id", region_name=REGION)
    mock_client.update_quick_connect_name.assert_called_once()


def test_update_quick_connect_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_quick_connect_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_quick_connect_name",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update quick connect name"):
        update_quick_connect_name("test-instance_id", "test-quick_connect_id", region_name=REGION)


def test_update_routing_profile_agent_availability_timer(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_agent_availability_timer.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_routing_profile_agent_availability_timer("test-instance_id", "test-routing_profile_id", "test-agent_availability_timer", region_name=REGION)
    mock_client.update_routing_profile_agent_availability_timer.assert_called_once()


def test_update_routing_profile_agent_availability_timer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_agent_availability_timer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_routing_profile_agent_availability_timer",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update routing profile agent availability timer"):
        update_routing_profile_agent_availability_timer("test-instance_id", "test-routing_profile_id", "test-agent_availability_timer", region_name=REGION)


def test_update_routing_profile_concurrency(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_concurrency.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_routing_profile_concurrency("test-instance_id", "test-routing_profile_id", [], region_name=REGION)
    mock_client.update_routing_profile_concurrency.assert_called_once()


def test_update_routing_profile_concurrency_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_concurrency.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_routing_profile_concurrency",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update routing profile concurrency"):
        update_routing_profile_concurrency("test-instance_id", "test-routing_profile_id", [], region_name=REGION)


def test_update_routing_profile_default_outbound_queue(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_default_outbound_queue.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_routing_profile_default_outbound_queue("test-instance_id", "test-routing_profile_id", "test-default_outbound_queue_id", region_name=REGION)
    mock_client.update_routing_profile_default_outbound_queue.assert_called_once()


def test_update_routing_profile_default_outbound_queue_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_default_outbound_queue.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_routing_profile_default_outbound_queue",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update routing profile default outbound queue"):
        update_routing_profile_default_outbound_queue("test-instance_id", "test-routing_profile_id", "test-default_outbound_queue_id", region_name=REGION)


def test_update_routing_profile_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_routing_profile_name("test-instance_id", "test-routing_profile_id", region_name=REGION)
    mock_client.update_routing_profile_name.assert_called_once()


def test_update_routing_profile_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_routing_profile_name",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update routing profile name"):
        update_routing_profile_name("test-instance_id", "test-routing_profile_id", region_name=REGION)


def test_update_routing_profile_queues(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_routing_profile_queues("test-instance_id", "test-routing_profile_id", [], region_name=REGION)
    mock_client.update_routing_profile_queues.assert_called_once()


def test_update_routing_profile_queues_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_routing_profile_queues.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_routing_profile_queues",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update routing profile queues"):
        update_routing_profile_queues("test-instance_id", "test-routing_profile_id", [], region_name=REGION)


def test_update_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rule.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_rule("test-rule_id", "test-instance_id", "test-name", "test-function", [], "test-publish_status", region_name=REGION)
    mock_client.update_rule.assert_called_once()


def test_update_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_rule",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update rule"):
        update_rule("test-rule_id", "test-instance_id", "test-name", "test-function", [], "test-publish_status", region_name=REGION)


def test_update_security_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_security_profile("test-security_profile_id", "test-instance_id", region_name=REGION)
    mock_client.update_security_profile.assert_called_once()


def test_update_security_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security_profile",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update security profile"):
        update_security_profile("test-security_profile_id", "test-instance_id", region_name=REGION)


def test_update_task_template(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_task_template("test-task_template_id", "test-instance_id", region_name=REGION)
    mock_client.update_task_template.assert_called_once()


def test_update_task_template_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_task_template.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_task_template",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update task template"):
        update_task_template("test-task_template_id", "test-instance_id", region_name=REGION)


def test_update_traffic_distribution(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_traffic_distribution.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_traffic_distribution("test-id", region_name=REGION)
    mock_client.update_traffic_distribution.assert_called_once()


def test_update_traffic_distribution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_traffic_distribution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_traffic_distribution",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update traffic distribution"):
        update_traffic_distribution("test-id", region_name=REGION)


def test_update_user_hierarchy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_hierarchy.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_hierarchy("test-user_id", "test-instance_id", region_name=REGION)
    mock_client.update_user_hierarchy.assert_called_once()


def test_update_user_hierarchy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_hierarchy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_hierarchy",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user hierarchy"):
        update_user_hierarchy("test-user_id", "test-instance_id", region_name=REGION)


def test_update_user_hierarchy_group_name(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_hierarchy_group_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_hierarchy_group_name("test-name", "test-hierarchy_group_id", "test-instance_id", region_name=REGION)
    mock_client.update_user_hierarchy_group_name.assert_called_once()


def test_update_user_hierarchy_group_name_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_hierarchy_group_name.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_hierarchy_group_name",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user hierarchy group name"):
        update_user_hierarchy_group_name("test-name", "test-hierarchy_group_id", "test-instance_id", region_name=REGION)


def test_update_user_hierarchy_structure(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_hierarchy_structure.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_hierarchy_structure({}, "test-instance_id", region_name=REGION)
    mock_client.update_user_hierarchy_structure.assert_called_once()


def test_update_user_hierarchy_structure_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_hierarchy_structure.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_hierarchy_structure",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user hierarchy structure"):
        update_user_hierarchy_structure({}, "test-instance_id", region_name=REGION)


def test_update_user_identity_info(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_identity_info.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_identity_info({}, "test-user_id", "test-instance_id", region_name=REGION)
    mock_client.update_user_identity_info.assert_called_once()


def test_update_user_identity_info_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_identity_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_identity_info",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user identity info"):
        update_user_identity_info({}, "test-user_id", "test-instance_id", region_name=REGION)


def test_update_user_phone_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_phone_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_phone_config({}, "test-user_id", "test-instance_id", region_name=REGION)
    mock_client.update_user_phone_config.assert_called_once()


def test_update_user_phone_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_phone_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_phone_config",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user phone config"):
        update_user_phone_config({}, "test-user_id", "test-instance_id", region_name=REGION)


def test_update_user_proficiencies(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_proficiencies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_proficiencies("test-instance_id", "test-user_id", [], region_name=REGION)
    mock_client.update_user_proficiencies.assert_called_once()


def test_update_user_proficiencies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_proficiencies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_proficiencies",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user proficiencies"):
        update_user_proficiencies("test-instance_id", "test-user_id", [], region_name=REGION)


def test_update_user_security_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_security_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_security_profiles([], "test-user_id", "test-instance_id", region_name=REGION)
    mock_client.update_user_security_profiles.assert_called_once()


def test_update_user_security_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_security_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_security_profiles",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user security profiles"):
        update_user_security_profiles([], "test-user_id", "test-instance_id", region_name=REGION)


def test_update_view_content(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_view_content.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_view_content("test-instance_id", "test-view_id", "test-status", {}, region_name=REGION)
    mock_client.update_view_content.assert_called_once()


def test_update_view_content_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_view_content.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_view_content",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update view content"):
        update_view_content("test-instance_id", "test-view_id", "test-status", {}, region_name=REGION)


def test_update_view_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_view_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_view_metadata("test-instance_id", "test-view_id", region_name=REGION)
    mock_client.update_view_metadata.assert_called_once()


def test_update_view_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_view_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_view_metadata",
    )
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update view metadata"):
        update_view_metadata("test-instance_id", "test-view_id", region_name=REGION)


def test_list_contact_flows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_contact_flows
    mock_client = MagicMock()
    mock_client.list_contact_flows.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_flows("test-instance_id", contact_flow_types="test-contact_flow_types", region_name="us-east-1")
    mock_client.list_contact_flows.assert_called_once()

def test_list_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_queues
    mock_client = MagicMock()
    mock_client.list_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_queues("test-instance_id", queue_types="test-queue_types", region_name="us-east-1")
    mock_client.list_queues.assert_called_once()

def test_get_current_metric_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import get_current_metric_data
    mock_client = MagicMock()
    mock_client.get_current_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_current_metric_data("test-instance_id", [{}], "test-current_metrics", groupings="test-groupings", region_name="us-east-1")
    mock_client.get_current_metric_data.assert_called_once()

def test_associate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_analytics_data_set
    mock_client = MagicMock()
    mock_client.associate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_analytics_data_set("test-instance_id", "test-data_set_id", target_account_id=1, region_name="us-east-1")
    mock_client.associate_analytics_data_set.assert_called_once()

def test_associate_approved_origin_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_approved_origin
    mock_client = MagicMock()
    mock_client.associate_approved_origin.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_approved_origin("test-instance_id", "test-origin", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_approved_origin.assert_called_once()

def test_associate_bot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_bot
    mock_client = MagicMock()
    mock_client.associate_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_bot("test-instance_id", lex_bot="test-lex_bot", lex_v2_bot="test-lex_v2_bot", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_bot.assert_called_once()

def test_associate_default_vocabulary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_default_vocabulary
    mock_client = MagicMock()
    mock_client.associate_default_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_default_vocabulary("test-instance_id", "test-language_code", vocabulary_id="test-vocabulary_id", region_name="us-east-1")
    mock_client.associate_default_vocabulary.assert_called_once()

def test_associate_email_address_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_email_address_alias
    mock_client = MagicMock()
    mock_client.associate_email_address_alias.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_email_address_alias("test-email_address_id", "test-instance_id", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_email_address_alias.assert_called_once()

def test_associate_instance_storage_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_instance_storage_config
    mock_client = MagicMock()
    mock_client.associate_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_instance_storage_config("test-instance_id", "test-resource_type", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_instance_storage_config.assert_called_once()

def test_associate_lambda_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_lambda_function
    mock_client = MagicMock()
    mock_client.associate_lambda_function.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_lambda_function("test-instance_id", "test-function_arn", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_lambda_function.assert_called_once()

def test_associate_lex_bot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_lex_bot
    mock_client = MagicMock()
    mock_client.associate_lex_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_lex_bot("test-instance_id", "test-lex_bot", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_lex_bot.assert_called_once()

def test_associate_routing_profile_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_routing_profile_queues
    mock_client = MagicMock()
    mock_client.associate_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_routing_profile_queues("test-instance_id", "test-routing_profile_id", queue_configs={}, manual_assignment_queue_configs={}, region_name="us-east-1")
    mock_client.associate_routing_profile_queues.assert_called_once()

def test_associate_security_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import associate_security_key
    mock_client = MagicMock()
    mock_client.associate_security_key.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    associate_security_key("test-instance_id", "test-key", client_token="test-client_token", region_name="us-east-1")
    mock_client.associate_security_key.assert_called_once()

def test_batch_associate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import batch_associate_analytics_data_set
    mock_client = MagicMock()
    mock_client.batch_associate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_associate_analytics_data_set("test-instance_id", "test-data_set_ids", target_account_id=1, region_name="us-east-1")
    mock_client.batch_associate_analytics_data_set.assert_called_once()

def test_batch_disassociate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import batch_disassociate_analytics_data_set
    mock_client = MagicMock()
    mock_client.batch_disassociate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_disassociate_analytics_data_set("test-instance_id", "test-data_set_ids", target_account_id=1, region_name="us-east-1")
    mock_client.batch_disassociate_analytics_data_set.assert_called_once()

def test_batch_get_flow_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import batch_get_flow_association
    mock_client = MagicMock()
    mock_client.batch_get_flow_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_get_flow_association("test-instance_id", "test-resource_ids", resource_type="test-resource_type", region_name="us-east-1")
    mock_client.batch_get_flow_association.assert_called_once()

def test_batch_put_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import batch_put_contact
    mock_client = MagicMock()
    mock_client.batch_put_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    batch_put_contact("test-instance_id", "test-contact_data_request_list", client_token="test-client_token", region_name="us-east-1")
    mock_client.batch_put_contact.assert_called_once()

def test_claim_phone_number_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import claim_phone_number
    mock_client = MagicMock()
    mock_client.claim_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    claim_phone_number("test-phone_number", target_arn="test-target_arn", instance_id="test-instance_id", phone_number_description="test-phone_number_description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.claim_phone_number.assert_called_once()

def test_create_agent_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_agent_status
    mock_client = MagicMock()
    mock_client.create_agent_status.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_agent_status("test-instance_id", "test-name", "test-state", description="test-description", display_order="test-display_order", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_agent_status.assert_called_once()

def test_create_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_contact
    mock_client = MagicMock()
    mock_client.create_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_contact("test-instance_id", "test-channel", "test-initiation_method", client_token="test-client_token", related_contact_id="test-related_contact_id", attributes="test-attributes", references="test-references", expiry_duration_in_minutes=1, user_info="test-user_info", initiate_as="test-initiate_as", name="test-name", description="test-description", segment_attributes="test-segment_attributes", previous_contact_id="test-previous_contact_id", region_name="us-east-1")
    mock_client.create_contact.assert_called_once()

def test_create_contact_flow_module_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_contact_flow_module
    mock_client = MagicMock()
    mock_client.create_contact_flow_module.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_contact_flow_module("test-instance_id", "test-name", "test-content", description="test-description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_contact_flow_module.assert_called_once()

def test_create_contact_flow_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_contact_flow_version
    mock_client = MagicMock()
    mock_client.create_contact_flow_version.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_contact_flow_version("test-instance_id", "test-contact_flow_id", description="test-description", flow_content_sha256="test-flow_content_sha256", contact_flow_version="test-contact_flow_version", last_modified_time="test-last_modified_time", last_modified_region="test-last_modified_region", region_name="us-east-1")
    mock_client.create_contact_flow_version.assert_called_once()

def test_create_email_address_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_email_address
    mock_client = MagicMock()
    mock_client.create_email_address.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_email_address("test-instance_id", "test-email_address", description="test-description", display_name="test-display_name", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_email_address.assert_called_once()

def test_create_evaluation_form_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_evaluation_form
    mock_client = MagicMock()
    mock_client.create_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_evaluation_form("test-instance_id", "test-title", "test-items", description="test-description", scoring_strategy="test-scoring_strategy", auto_evaluation_configuration=True, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_evaluation_form.assert_called_once()

def test_create_hours_of_operation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_hours_of_operation
    mock_client = MagicMock()
    mock_client.create_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_hours_of_operation("test-instance_id", "test-name", "test-time_zone", {}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_hours_of_operation.assert_called_once()

def test_create_hours_of_operation_override_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_hours_of_operation_override
    mock_client = MagicMock()
    mock_client.create_hours_of_operation_override.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-name", {}, "test-effective_from", "test-effective_till", description="test-description", region_name="us-east-1")
    mock_client.create_hours_of_operation_override.assert_called_once()

def test_create_integration_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_integration_association
    mock_client = MagicMock()
    mock_client.create_integration_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_integration_association("test-instance_id", "test-integration_type", "test-integration_arn", source_application_url="test-source_application_url", source_application_name="test-source_application_name", source_type="test-source_type", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_integration_association.assert_called_once()

def test_create_participant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_participant
    mock_client = MagicMock()
    mock_client.create_participant.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_participant("test-instance_id", "test-contact_id", "test-participant_details", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_participant.assert_called_once()

def test_create_persistent_contact_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_persistent_contact_association
    mock_client = MagicMock()
    mock_client.create_persistent_contact_association.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_persistent_contact_association("test-instance_id", "test-initial_contact_id", "test-rehydration_type", "test-source_contact_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_persistent_contact_association.assert_called_once()

def test_create_predefined_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_predefined_attribute
    mock_client = MagicMock()
    mock_client.create_predefined_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_predefined_attribute("test-instance_id", "test-name", values="test-values", purposes="test-purposes", attribute_configuration={}, region_name="us-east-1")
    mock_client.create_predefined_attribute.assert_called_once()

def test_create_prompt_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_prompt
    mock_client = MagicMock()
    mock_client.create_prompt.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_prompt("test-instance_id", "test-name", "test-s3_uri", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_prompt.assert_called_once()

def test_create_push_notification_registration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_push_notification_registration
    mock_client = MagicMock()
    mock_client.create_push_notification_registration.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_push_notification_registration("test-instance_id", "test-pinpoint_app_arn", "test-device_token", "test-device_type", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_push_notification_registration.assert_called_once()

def test_create_quick_connect_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_quick_connect
    mock_client = MagicMock()
    mock_client.create_quick_connect.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_quick_connect("test-instance_id", "test-name", {}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_quick_connect.assert_called_once()

def test_create_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_rule
    mock_client = MagicMock()
    mock_client.create_rule.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_rule("test-instance_id", "test-name", "test-trigger_event_source", "test-function", "test-actions", True, client_token="test-client_token", region_name="us-east-1")
    mock_client.create_rule.assert_called_once()

def test_create_security_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_security_profile
    mock_client = MagicMock()
    mock_client.create_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_security_profile("test-security_profile_name", "test-instance_id", description="test-description", permissions="test-permissions", tags=[{"Key": "k", "Value": "v"}], allowed_access_control_tags=True, tag_restricted_resources="test-tag_restricted_resources", applications="test-applications", hierarchy_restricted_resources="test-hierarchy_restricted_resources", allowed_access_control_hierarchy_group_id=True, region_name="us-east-1")
    mock_client.create_security_profile.assert_called_once()

def test_create_task_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_task_template
    mock_client = MagicMock()
    mock_client.create_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_task_template("test-instance_id", "test-name", "test-fields", description="test-description", contact_flow_id="test-contact_flow_id", self_assign_flow_id="test-self_assign_flow_id", constraints="test-constraints", defaults="test-defaults", status="test-status", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_task_template.assert_called_once()

def test_create_traffic_distribution_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_traffic_distribution_group
    mock_client = MagicMock()
    mock_client.create_traffic_distribution_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_traffic_distribution_group("test-name", "test-instance_id", description="test-description", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_traffic_distribution_group.assert_called_once()

def test_create_use_case_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_use_case
    mock_client = MagicMock()
    mock_client.create_use_case.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_use_case("test-instance_id", "test-integration_association_id", True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_use_case.assert_called_once()

def test_create_user_hierarchy_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_user_hierarchy_group
    mock_client = MagicMock()
    mock_client.create_user_hierarchy_group.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_user_hierarchy_group("test-name", "test-instance_id", parent_group_id="test-parent_group_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_user_hierarchy_group.assert_called_once()

def test_create_view_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_view
    mock_client = MagicMock()
    mock_client.create_view.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_view("test-instance_id", "test-status", "test-content", "test-name", client_token="test-client_token", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_view.assert_called_once()

def test_create_view_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_view_version
    mock_client = MagicMock()
    mock_client.create_view_version.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_view_version("test-instance_id", "test-view_id", version_description="test-version_description", view_content_sha256="test-view_content_sha256", region_name="us-east-1")
    mock_client.create_view_version.assert_called_once()

def test_create_vocabulary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_vocabulary
    mock_client = MagicMock()
    mock_client.create_vocabulary.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    create_vocabulary("test-instance_id", "test-vocabulary_name", "test-language_code", "test-content", client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_vocabulary.assert_called_once()

def test_delete_evaluation_form_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import delete_evaluation_form
    mock_client = MagicMock()
    mock_client.delete_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    delete_evaluation_form("test-instance_id", "test-evaluation_form_id", evaluation_form_version="test-evaluation_form_version", region_name="us-east-1")
    mock_client.delete_evaluation_form.assert_called_once()

def test_describe_evaluation_form_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import describe_evaluation_form
    mock_client = MagicMock()
    mock_client.describe_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    describe_evaluation_form("test-instance_id", "test-evaluation_form_id", evaluation_form_version="test-evaluation_form_version", region_name="us-east-1")
    mock_client.describe_evaluation_form.assert_called_once()

def test_disassociate_analytics_data_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_analytics_data_set
    mock_client = MagicMock()
    mock_client.disassociate_analytics_data_set.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_analytics_data_set("test-instance_id", "test-data_set_id", target_account_id=1, region_name="us-east-1")
    mock_client.disassociate_analytics_data_set.assert_called_once()

def test_disassociate_approved_origin_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_approved_origin
    mock_client = MagicMock()
    mock_client.disassociate_approved_origin.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_approved_origin("test-instance_id", "test-origin", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_approved_origin.assert_called_once()

def test_disassociate_bot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_bot
    mock_client = MagicMock()
    mock_client.disassociate_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_bot("test-instance_id", lex_bot="test-lex_bot", lex_v2_bot="test-lex_v2_bot", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_bot.assert_called_once()

def test_disassociate_email_address_alias_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_email_address_alias
    mock_client = MagicMock()
    mock_client.disassociate_email_address_alias.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_email_address_alias("test-email_address_id", "test-instance_id", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_email_address_alias.assert_called_once()

def test_disassociate_instance_storage_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_instance_storage_config
    mock_client = MagicMock()
    mock_client.disassociate_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_instance_storage_config.assert_called_once()

def test_disassociate_lambda_function_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_lambda_function
    mock_client = MagicMock()
    mock_client.disassociate_lambda_function.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_lambda_function("test-instance_id", "test-function_arn", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_lambda_function.assert_called_once()

def test_disassociate_lex_bot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_lex_bot
    mock_client = MagicMock()
    mock_client.disassociate_lex_bot.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_lex_bot("test-instance_id", "test-bot_name", "test-lex_region", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_lex_bot.assert_called_once()

def test_disassociate_routing_profile_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_routing_profile_queues
    mock_client = MagicMock()
    mock_client.disassociate_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_routing_profile_queues("test-instance_id", "test-routing_profile_id", queue_references="test-queue_references", manual_assignment_queue_references="test-manual_assignment_queue_references", region_name="us-east-1")
    mock_client.disassociate_routing_profile_queues.assert_called_once()

def test_disassociate_security_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import disassociate_security_key
    mock_client = MagicMock()
    mock_client.disassociate_security_key.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    disassociate_security_key("test-instance_id", "test-association_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.disassociate_security_key.assert_called_once()

def test_get_attached_file_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import get_attached_file
    mock_client = MagicMock()
    mock_client.get_attached_file.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_attached_file("test-instance_id", "test-file_id", "test-associated_resource_arn", url_expiry_in_seconds="test-url_expiry_in_seconds", region_name="us-east-1")
    mock_client.get_attached_file.assert_called_once()

def test_get_current_user_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import get_current_user_data
    mock_client = MagicMock()
    mock_client.get_current_user_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_current_user_data("test-instance_id", [{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_current_user_data.assert_called_once()

def test_get_metric_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import get_metric_data
    mock_client = MagicMock()
    mock_client.get_metric_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_metric_data("test-instance_id", "test-start_time", "test-end_time", [{}], "test-historical_metrics", groupings="test-groupings", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_metric_data.assert_called_once()

def test_get_metric_data_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import get_metric_data_v2
    mock_client = MagicMock()
    mock_client.get_metric_data_v2.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_metric_data_v2("test-resource_arn", "test-start_time", "test-end_time", [{}], "test-metrics", interval="test-interval", groupings="test-groupings", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_metric_data_v2.assert_called_once()

def test_get_task_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import get_task_template
    mock_client = MagicMock()
    mock_client.get_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    get_task_template("test-instance_id", "test-task_template_id", snapshot_version="test-snapshot_version", region_name="us-east-1")
    mock_client.get_task_template.assert_called_once()

def test_import_phone_number_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import import_phone_number
    mock_client = MagicMock()
    mock_client.import_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    import_phone_number("test-instance_id", "test-source_phone_number_arn", phone_number_description="test-phone_number_description", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.import_phone_number.assert_called_once()

def test_list_agent_statuses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_agent_statuses
    mock_client = MagicMock()
    mock_client.list_agent_statuses.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_agent_statuses("test-instance_id", next_token="test-next_token", max_results=1, agent_status_types="test-agent_status_types", region_name="us-east-1")
    mock_client.list_agent_statuses.assert_called_once()

def test_list_analytics_data_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_analytics_data_associations
    mock_client = MagicMock()
    mock_client.list_analytics_data_associations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_analytics_data_associations("test-instance_id", data_set_id="test-data_set_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_analytics_data_associations.assert_called_once()

def test_list_analytics_data_lake_data_sets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_analytics_data_lake_data_sets
    mock_client = MagicMock()
    mock_client.list_analytics_data_lake_data_sets.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_analytics_data_lake_data_sets("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_analytics_data_lake_data_sets.assert_called_once()

def test_list_approved_origins_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_approved_origins
    mock_client = MagicMock()
    mock_client.list_approved_origins.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_approved_origins("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_approved_origins.assert_called_once()

def test_list_associated_contacts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_associated_contacts
    mock_client = MagicMock()
    mock_client.list_associated_contacts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_associated_contacts("test-instance_id", "test-contact_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_associated_contacts.assert_called_once()

def test_list_authentication_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_authentication_profiles
    mock_client = MagicMock()
    mock_client.list_authentication_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_authentication_profiles("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_authentication_profiles.assert_called_once()

def test_list_bots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_bots
    mock_client = MagicMock()
    mock_client.list_bots.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_bots("test-instance_id", "test-lex_version", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_bots.assert_called_once()

def test_list_contact_evaluations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_contact_evaluations
    mock_client = MagicMock()
    mock_client.list_contact_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_evaluations("test-instance_id", "test-contact_id", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_contact_evaluations.assert_called_once()

def test_list_contact_flow_modules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_contact_flow_modules
    mock_client = MagicMock()
    mock_client.list_contact_flow_modules.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_flow_modules("test-instance_id", next_token="test-next_token", max_results=1, contact_flow_module_state="test-contact_flow_module_state", region_name="us-east-1")
    mock_client.list_contact_flow_modules.assert_called_once()

def test_list_contact_flow_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_contact_flow_versions
    mock_client = MagicMock()
    mock_client.list_contact_flow_versions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_flow_versions("test-instance_id", "test-contact_flow_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_contact_flow_versions.assert_called_once()

def test_list_contact_references_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_contact_references
    mock_client = MagicMock()
    mock_client.list_contact_references.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_contact_references("test-instance_id", "test-contact_id", "test-reference_types", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_contact_references.assert_called_once()

def test_list_default_vocabularies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_default_vocabularies
    mock_client = MagicMock()
    mock_client.list_default_vocabularies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_default_vocabularies("test-instance_id", language_code="test-language_code", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_default_vocabularies.assert_called_once()

def test_list_evaluation_form_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_evaluation_form_versions
    mock_client = MagicMock()
    mock_client.list_evaluation_form_versions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_evaluation_form_versions("test-instance_id", "test-evaluation_form_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_evaluation_form_versions.assert_called_once()

def test_list_evaluation_forms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_evaluation_forms
    mock_client = MagicMock()
    mock_client.list_evaluation_forms.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_evaluation_forms("test-instance_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_evaluation_forms.assert_called_once()

def test_list_flow_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_flow_associations
    mock_client = MagicMock()
    mock_client.list_flow_associations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_flow_associations("test-instance_id", resource_type="test-resource_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_flow_associations.assert_called_once()

def test_list_hours_of_operation_overrides_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_hours_of_operation_overrides
    mock_client = MagicMock()
    mock_client.list_hours_of_operation_overrides.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_hours_of_operation_overrides("test-instance_id", "test-hours_of_operation_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_hours_of_operation_overrides.assert_called_once()

def test_list_hours_of_operations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_hours_of_operations
    mock_client = MagicMock()
    mock_client.list_hours_of_operations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_hours_of_operations("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_hours_of_operations.assert_called_once()

def test_list_instance_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_instance_attributes
    mock_client = MagicMock()
    mock_client.list_instance_attributes.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_instance_attributes("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_instance_attributes.assert_called_once()

def test_list_instance_storage_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_instance_storage_configs
    mock_client = MagicMock()
    mock_client.list_instance_storage_configs.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_instance_storage_configs("test-instance_id", "test-resource_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_instance_storage_configs.assert_called_once()

def test_list_integration_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_integration_associations
    mock_client = MagicMock()
    mock_client.list_integration_associations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_integration_associations("test-instance_id", integration_type="test-integration_type", next_token="test-next_token", max_results=1, integration_arn="test-integration_arn", region_name="us-east-1")
    mock_client.list_integration_associations.assert_called_once()

def test_list_lambda_functions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_lambda_functions
    mock_client = MagicMock()
    mock_client.list_lambda_functions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_lambda_functions("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_lambda_functions.assert_called_once()

def test_list_lex_bots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_lex_bots
    mock_client = MagicMock()
    mock_client.list_lex_bots.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_lex_bots("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_lex_bots.assert_called_once()

def test_list_phone_numbers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_phone_numbers
    mock_client = MagicMock()
    mock_client.list_phone_numbers.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_phone_numbers("test-instance_id", phone_number_types="test-phone_number_types", phone_number_country_codes=1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_phone_numbers.assert_called_once()

def test_list_phone_numbers_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_phone_numbers_v2
    mock_client = MagicMock()
    mock_client.list_phone_numbers_v2.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_phone_numbers_v2(target_arn="test-target_arn", instance_id="test-instance_id", max_results=1, next_token="test-next_token", phone_number_country_codes=1, phone_number_types="test-phone_number_types", phone_number_prefix="test-phone_number_prefix", region_name="us-east-1")
    mock_client.list_phone_numbers_v2.assert_called_once()

def test_list_predefined_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_predefined_attributes
    mock_client = MagicMock()
    mock_client.list_predefined_attributes.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_predefined_attributes("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_predefined_attributes.assert_called_once()

def test_list_prompts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_prompts
    mock_client = MagicMock()
    mock_client.list_prompts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_prompts("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_prompts.assert_called_once()

def test_list_queue_quick_connects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_queue_quick_connects
    mock_client = MagicMock()
    mock_client.list_queue_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_queue_quick_connects("test-instance_id", "test-queue_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_queue_quick_connects.assert_called_once()

def test_list_quick_connects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_quick_connects
    mock_client = MagicMock()
    mock_client.list_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_quick_connects("test-instance_id", next_token="test-next_token", max_results=1, quick_connect_types="test-quick_connect_types", region_name="us-east-1")
    mock_client.list_quick_connects.assert_called_once()

def test_list_realtime_contact_analysis_segments_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_realtime_contact_analysis_segments_v2
    mock_client = MagicMock()
    mock_client.list_realtime_contact_analysis_segments_v2.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_realtime_contact_analysis_segments_v2("test-instance_id", "test-contact_id", "test-output_type", "test-segment_types", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_realtime_contact_analysis_segments_v2.assert_called_once()

def test_list_routing_profile_manual_assignment_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_routing_profile_manual_assignment_queues
    mock_client = MagicMock()
    mock_client.list_routing_profile_manual_assignment_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_routing_profile_manual_assignment_queues("test-instance_id", "test-routing_profile_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_routing_profile_manual_assignment_queues.assert_called_once()

def test_list_routing_profile_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_routing_profile_queues
    mock_client = MagicMock()
    mock_client.list_routing_profile_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_routing_profile_queues("test-instance_id", "test-routing_profile_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_routing_profile_queues.assert_called_once()

def test_list_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_rules
    mock_client = MagicMock()
    mock_client.list_rules.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_rules("test-instance_id", publish_status=True, event_source_name="test-event_source_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_rules.assert_called_once()

def test_list_security_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_security_keys
    mock_client = MagicMock()
    mock_client.list_security_keys.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_keys("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_security_keys.assert_called_once()

def test_list_security_profile_applications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_security_profile_applications
    mock_client = MagicMock()
    mock_client.list_security_profile_applications.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_profile_applications("test-security_profile_id", "test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_security_profile_applications.assert_called_once()

def test_list_security_profile_permissions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_security_profile_permissions
    mock_client = MagicMock()
    mock_client.list_security_profile_permissions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_profile_permissions("test-security_profile_id", "test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_security_profile_permissions.assert_called_once()

def test_list_security_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_security_profiles
    mock_client = MagicMock()
    mock_client.list_security_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_security_profiles("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_security_profiles.assert_called_once()

def test_list_task_templates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_task_templates
    mock_client = MagicMock()
    mock_client.list_task_templates.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_task_templates("test-instance_id", next_token="test-next_token", max_results=1, status="test-status", name="test-name", region_name="us-east-1")
    mock_client.list_task_templates.assert_called_once()

def test_list_traffic_distribution_group_users_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_traffic_distribution_group_users
    mock_client = MagicMock()
    mock_client.list_traffic_distribution_group_users.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_traffic_distribution_group_users("test-traffic_distribution_group_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_traffic_distribution_group_users.assert_called_once()

def test_list_traffic_distribution_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_traffic_distribution_groups
    mock_client = MagicMock()
    mock_client.list_traffic_distribution_groups.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_traffic_distribution_groups(max_results=1, next_token="test-next_token", instance_id="test-instance_id", region_name="us-east-1")
    mock_client.list_traffic_distribution_groups.assert_called_once()

def test_list_use_cases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_use_cases
    mock_client = MagicMock()
    mock_client.list_use_cases.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_use_cases("test-instance_id", "test-integration_association_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_use_cases.assert_called_once()

def test_list_user_hierarchy_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_user_hierarchy_groups
    mock_client = MagicMock()
    mock_client.list_user_hierarchy_groups.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_user_hierarchy_groups("test-instance_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_user_hierarchy_groups.assert_called_once()

def test_list_user_proficiencies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_user_proficiencies
    mock_client = MagicMock()
    mock_client.list_user_proficiencies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_user_proficiencies("test-instance_id", "test-user_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_user_proficiencies.assert_called_once()

def test_list_view_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_view_versions
    mock_client = MagicMock()
    mock_client.list_view_versions.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_view_versions("test-instance_id", "test-view_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_view_versions.assert_called_once()

def test_list_views_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import list_views
    mock_client = MagicMock()
    mock_client.list_views.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    list_views("test-instance_id", type_value="test-type_value", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_views.assert_called_once()

def test_monitor_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import monitor_contact
    mock_client = MagicMock()
    mock_client.monitor_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    monitor_contact("test-instance_id", "test-contact_id", "test-user_id", allowed_monitor_capabilities=True, client_token="test-client_token", region_name="us-east-1")
    mock_client.monitor_contact.assert_called_once()

def test_pause_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import pause_contact
    mock_client = MagicMock()
    mock_client.pause_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    pause_contact("test-contact_id", "test-instance_id", contact_flow_id="test-contact_flow_id", region_name="us-east-1")
    mock_client.pause_contact.assert_called_once()

def test_release_phone_number_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import release_phone_number
    mock_client = MagicMock()
    mock_client.release_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    release_phone_number("test-phone_number_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.release_phone_number.assert_called_once()

def test_replicate_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import replicate_instance
    mock_client = MagicMock()
    mock_client.replicate_instance.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    replicate_instance("test-instance_id", "test-replica_region", "test-replica_alias", client_token="test-client_token", region_name="us-east-1")
    mock_client.replicate_instance.assert_called_once()

def test_resume_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import resume_contact
    mock_client = MagicMock()
    mock_client.resume_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    resume_contact("test-contact_id", "test-instance_id", contact_flow_id="test-contact_flow_id", region_name="us-east-1")
    mock_client.resume_contact.assert_called_once()

def test_resume_contact_recording_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import resume_contact_recording
    mock_client = MagicMock()
    mock_client.resume_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    resume_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", contact_recording_type="test-contact_recording_type", region_name="us-east-1")
    mock_client.resume_contact_recording.assert_called_once()

def test_search_agent_statuses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_agent_statuses
    mock_client = MagicMock()
    mock_client.search_agent_statuses.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_agent_statuses("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_agent_statuses.assert_called_once()

def test_search_available_phone_numbers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_available_phone_numbers
    mock_client = MagicMock()
    mock_client.search_available_phone_numbers.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_available_phone_numbers(1, "test-phone_number_type", target_arn="test-target_arn", instance_id="test-instance_id", phone_number_prefix="test-phone_number_prefix", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.search_available_phone_numbers.assert_called_once()

def test_search_contact_evaluations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_contact_evaluations
    mock_client = MagicMock()
    mock_client.search_contact_evaluations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contact_evaluations("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.search_contact_evaluations.assert_called_once()

def test_search_contact_flow_modules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_contact_flow_modules
    mock_client = MagicMock()
    mock_client.search_contact_flow_modules.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contact_flow_modules("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_contact_flow_modules.assert_called_once()

def test_search_contact_flows_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_contact_flows
    mock_client = MagicMock()
    mock_client.search_contact_flows.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contact_flows("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_contact_flows.assert_called_once()

def test_search_contacts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_contacts
    mock_client = MagicMock()
    mock_client.search_contacts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_contacts("test-instance_id", "test-time_range", search_criteria="test-search_criteria", max_results=1, next_token="test-next_token", sort="test-sort", region_name="us-east-1")
    mock_client.search_contacts.assert_called_once()

def test_search_email_addresses_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_email_addresses
    mock_client = MagicMock()
    mock_client.search_email_addresses.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_email_addresses("test-instance_id", max_results=1, next_token="test-next_token", search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.search_email_addresses.assert_called_once()

def test_search_evaluation_forms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_evaluation_forms
    mock_client = MagicMock()
    mock_client.search_evaluation_forms.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_evaluation_forms("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.search_evaluation_forms.assert_called_once()

def test_search_hours_of_operation_overrides_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_hours_of_operation_overrides
    mock_client = MagicMock()
    mock_client.search_hours_of_operation_overrides.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_hours_of_operation_overrides("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_hours_of_operation_overrides.assert_called_once()

def test_search_hours_of_operations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_hours_of_operations
    mock_client = MagicMock()
    mock_client.search_hours_of_operations.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_hours_of_operations("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_hours_of_operations.assert_called_once()

def test_search_predefined_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_predefined_attributes
    mock_client = MagicMock()
    mock_client.search_predefined_attributes.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_predefined_attributes("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_predefined_attributes.assert_called_once()

def test_search_prompts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_prompts
    mock_client = MagicMock()
    mock_client.search_prompts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_prompts("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_prompts.assert_called_once()

def test_search_queues_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_queues
    mock_client = MagicMock()
    mock_client.search_queues.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_queues("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_queues.assert_called_once()

def test_search_quick_connects_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_quick_connects
    mock_client = MagicMock()
    mock_client.search_quick_connects.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_quick_connects("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_quick_connects.assert_called_once()

def test_search_resource_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_resource_tags
    mock_client = MagicMock()
    mock_client.search_resource_tags.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_resource_tags("test-instance_id", resource_types="test-resource_types", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_resource_tags.assert_called_once()

def test_search_routing_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_routing_profiles
    mock_client = MagicMock()
    mock_client.search_routing_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_routing_profiles("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_routing_profiles.assert_called_once()

def test_search_security_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_security_profiles
    mock_client = MagicMock()
    mock_client.search_security_profiles.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_security_profiles("test-instance_id", next_token="test-next_token", max_results=1, search_criteria="test-search_criteria", search_filter=[{}], region_name="us-east-1")
    mock_client.search_security_profiles.assert_called_once()

def test_search_user_hierarchy_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_user_hierarchy_groups
    mock_client = MagicMock()
    mock_client.search_user_hierarchy_groups.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_user_hierarchy_groups("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_user_hierarchy_groups.assert_called_once()

def test_search_users_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_users
    mock_client = MagicMock()
    mock_client.search_users.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_users("test-instance_id", next_token="test-next_token", max_results=1, search_filter=[{}], search_criteria="test-search_criteria", region_name="us-east-1")
    mock_client.search_users.assert_called_once()

def test_search_vocabularies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import search_vocabularies
    mock_client = MagicMock()
    mock_client.search_vocabularies.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    search_vocabularies("test-instance_id", max_results=1, next_token="test-next_token", state="test-state", name_starts_with="test-name_starts_with", language_code="test-language_code", region_name="us-east-1")
    mock_client.search_vocabularies.assert_called_once()

def test_send_chat_integration_event_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import send_chat_integration_event
    mock_client = MagicMock()
    mock_client.send_chat_integration_event.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    send_chat_integration_event("test-source_id", "test-destination_id", "test-event", subtype="test-subtype", new_session_details="test-new_session_details", region_name="us-east-1")
    mock_client.send_chat_integration_event.assert_called_once()

def test_send_outbound_email_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import send_outbound_email
    mock_client = MagicMock()
    mock_client.send_outbound_email.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    send_outbound_email("test-instance_id", "test-from_email_address", "test-destination_email_address", "test-email_message", "test-traffic_type", additional_recipients="test-additional_recipients", source_campaign="test-source_campaign", client_token="test-client_token", region_name="us-east-1")
    mock_client.send_outbound_email.assert_called_once()

def test_start_attached_file_upload_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_attached_file_upload
    mock_client = MagicMock()
    mock_client.start_attached_file_upload.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_attached_file_upload("test-instance_id", "test-file_name", 1, "test-file_use_case_type", "test-associated_resource_arn", client_token="test-client_token", url_expiry_in_seconds="test-url_expiry_in_seconds", created_by="test-created_by", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_attached_file_upload.assert_called_once()

def test_start_contact_evaluation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_contact_evaluation
    mock_client = MagicMock()
    mock_client.start_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_contact_evaluation("test-instance_id", "test-contact_id", "test-evaluation_form_id", auto_evaluation_configuration=True, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_contact_evaluation.assert_called_once()

def test_start_email_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_email_contact
    mock_client = MagicMock()
    mock_client.start_email_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_email_contact("test-instance_id", "test-from_email_address", "test-destination_email_address", "test-email_message", description="test-description", references="test-references", name="test-name", additional_recipients="test-additional_recipients", attachments="test-attachments", contact_flow_id="test-contact_flow_id", related_contact_id="test-related_contact_id", attributes="test-attributes", segment_attributes="test-segment_attributes", client_token="test-client_token", region_name="us-east-1")
    mock_client.start_email_contact.assert_called_once()

def test_start_outbound_chat_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_outbound_chat_contact
    mock_client = MagicMock()
    mock_client.start_outbound_chat_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_outbound_chat_contact("test-source_endpoint", "test-destination_endpoint", "test-instance_id", "test-segment_attributes", "test-contact_flow_id", attributes="test-attributes", chat_duration_in_minutes=1, participant_details="test-participant_details", initial_system_message="test-initial_system_message", related_contact_id="test-related_contact_id", supported_messaging_content_types=1, client_token="test-client_token", region_name="us-east-1")
    mock_client.start_outbound_chat_contact.assert_called_once()

def test_start_outbound_email_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_outbound_email_contact
    mock_client = MagicMock()
    mock_client.start_outbound_email_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_outbound_email_contact("test-instance_id", "test-contact_id", "test-destination_email_address", "test-email_message", from_email_address="test-from_email_address", additional_recipients="test-additional_recipients", client_token="test-client_token", region_name="us-east-1")
    mock_client.start_outbound_email_contact.assert_called_once()

def test_start_screen_sharing_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_screen_sharing
    mock_client = MagicMock()
    mock_client.start_screen_sharing.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_screen_sharing("test-instance_id", "test-contact_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.start_screen_sharing.assert_called_once()

def test_start_web_rtc_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_web_rtc_contact
    mock_client = MagicMock()
    mock_client.start_web_rtc_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_web_rtc_contact("test-contact_flow_id", "test-instance_id", "test-participant_details", attributes="test-attributes", client_token="test-client_token", allowed_capabilities=True, related_contact_id="test-related_contact_id", references="test-references", description="test-description", region_name="us-east-1")
    mock_client.start_web_rtc_contact.assert_called_once()

def test_stop_contact_recording_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import stop_contact_recording
    mock_client = MagicMock()
    mock_client.stop_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    stop_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", contact_recording_type="test-contact_recording_type", region_name="us-east-1")
    mock_client.stop_contact_recording.assert_called_once()

def test_submit_contact_evaluation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import submit_contact_evaluation
    mock_client = MagicMock()
    mock_client.submit_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    submit_contact_evaluation("test-instance_id", "test-evaluation_id", answers="test-answers", notes="test-notes", submitted_by="test-submitted_by", region_name="us-east-1")
    mock_client.submit_contact_evaluation.assert_called_once()

def test_suspend_contact_recording_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import suspend_contact_recording
    mock_client = MagicMock()
    mock_client.suspend_contact_recording.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    suspend_contact_recording("test-instance_id", "test-contact_id", "test-initial_contact_id", contact_recording_type="test-contact_recording_type", region_name="us-east-1")
    mock_client.suspend_contact_recording.assert_called_once()

def test_transfer_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import transfer_contact
    mock_client = MagicMock()
    mock_client.transfer_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    transfer_contact("test-instance_id", "test-contact_id", "test-contact_flow_id", queue_id="test-queue_id", user_id="test-user_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.transfer_contact.assert_called_once()

def test_update_agent_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_agent_status
    mock_client = MagicMock()
    mock_client.update_agent_status.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_agent_status("test-instance_id", "test-agent_status_id", name="test-name", description="test-description", state="test-state", display_order="test-display_order", reset_order_number="test-reset_order_number", region_name="us-east-1")
    mock_client.update_agent_status.assert_called_once()

def test_update_authentication_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_authentication_profile
    mock_client = MagicMock()
    mock_client.update_authentication_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_authentication_profile("test-authentication_profile_id", "test-instance_id", name="test-name", description="test-description", allowed_ips=True, blocked_ips="test-blocked_ips", periodic_session_duration=1, session_inactivity_duration=1, session_inactivity_handling_enabled="test-session_inactivity_handling_enabled", region_name="us-east-1")
    mock_client.update_authentication_profile.assert_called_once()

def test_update_contact_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_contact
    mock_client = MagicMock()
    mock_client.update_contact.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact("test-instance_id", "test-contact_id", name="test-name", description="test-description", references="test-references", segment_attributes="test-segment_attributes", queue_info="test-queue_info", user_info="test-user_info", customer_endpoint="test-customer_endpoint", system_endpoint="test-system_endpoint", region_name="us-east-1")
    mock_client.update_contact.assert_called_once()

def test_update_contact_evaluation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_contact_evaluation
    mock_client = MagicMock()
    mock_client.update_contact_evaluation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_evaluation("test-instance_id", "test-evaluation_id", answers="test-answers", notes="test-notes", updated_by="test-updated_by", region_name="us-east-1")
    mock_client.update_contact_evaluation.assert_called_once()

def test_update_contact_flow_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_contact_flow_metadata
    mock_client = MagicMock()
    mock_client.update_contact_flow_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_metadata("test-instance_id", "test-contact_flow_id", name="test-name", description="test-description", contact_flow_state="test-contact_flow_state", region_name="us-east-1")
    mock_client.update_contact_flow_metadata.assert_called_once()

def test_update_contact_flow_module_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_contact_flow_module_metadata
    mock_client = MagicMock()
    mock_client.update_contact_flow_module_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_module_metadata("test-instance_id", "test-contact_flow_module_id", name="test-name", description="test-description", state="test-state", region_name="us-east-1")
    mock_client.update_contact_flow_module_metadata.assert_called_once()

def test_update_contact_flow_name_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_contact_flow_name
    mock_client = MagicMock()
    mock_client.update_contact_flow_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_flow_name("test-instance_id", "test-contact_flow_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_contact_flow_name.assert_called_once()

def test_update_contact_routing_data_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_contact_routing_data
    mock_client = MagicMock()
    mock_client.update_contact_routing_data.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_contact_routing_data("test-instance_id", "test-contact_id", queue_time_adjustment_seconds="test-queue_time_adjustment_seconds", queue_priority="test-queue_priority", routing_criteria="test-routing_criteria", region_name="us-east-1")
    mock_client.update_contact_routing_data.assert_called_once()

def test_update_email_address_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_email_address_metadata
    mock_client = MagicMock()
    mock_client.update_email_address_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_email_address_metadata("test-instance_id", "test-email_address_id", description="test-description", display_name="test-display_name", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_email_address_metadata.assert_called_once()

def test_update_evaluation_form_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_evaluation_form
    mock_client = MagicMock()
    mock_client.update_evaluation_form.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_evaluation_form("test-instance_id", "test-evaluation_form_id", "test-evaluation_form_version", "test-title", "test-items", create_new_version="test-create_new_version", description="test-description", scoring_strategy="test-scoring_strategy", auto_evaluation_configuration=True, client_token="test-client_token", region_name="us-east-1")
    mock_client.update_evaluation_form.assert_called_once()

def test_update_hours_of_operation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_hours_of_operation
    mock_client = MagicMock()
    mock_client.update_hours_of_operation.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_hours_of_operation("test-instance_id", "test-hours_of_operation_id", name="test-name", description="test-description", time_zone="test-time_zone", config={}, region_name="us-east-1")
    mock_client.update_hours_of_operation.assert_called_once()

def test_update_hours_of_operation_override_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_hours_of_operation_override
    mock_client = MagicMock()
    mock_client.update_hours_of_operation_override.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_hours_of_operation_override("test-instance_id", "test-hours_of_operation_id", "test-hours_of_operation_override_id", name="test-name", description="test-description", config={}, effective_from="test-effective_from", effective_till="test-effective_till", region_name="us-east-1")
    mock_client.update_hours_of_operation_override.assert_called_once()

def test_update_instance_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_instance_attribute
    mock_client = MagicMock()
    mock_client.update_instance_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_instance_attribute("test-instance_id", "test-attribute_type", "test-value", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_instance_attribute.assert_called_once()

def test_update_instance_storage_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_instance_storage_config
    mock_client = MagicMock()
    mock_client.update_instance_storage_config.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_instance_storage_config("test-instance_id", "test-association_id", "test-resource_type", {}, client_token="test-client_token", region_name="us-east-1")
    mock_client.update_instance_storage_config.assert_called_once()

def test_update_participant_authentication_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_participant_authentication
    mock_client = MagicMock()
    mock_client.update_participant_authentication.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_participant_authentication("test-state", "test-instance_id", code="test-code", error="test-error", error_description="test-error_description", region_name="us-east-1")
    mock_client.update_participant_authentication.assert_called_once()

def test_update_phone_number_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_phone_number
    mock_client = MagicMock()
    mock_client.update_phone_number.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_phone_number("test-phone_number_id", target_arn="test-target_arn", instance_id="test-instance_id", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_phone_number.assert_called_once()

def test_update_phone_number_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_phone_number_metadata
    mock_client = MagicMock()
    mock_client.update_phone_number_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_phone_number_metadata("test-phone_number_id", phone_number_description="test-phone_number_description", client_token="test-client_token", region_name="us-east-1")
    mock_client.update_phone_number_metadata.assert_called_once()

def test_update_predefined_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_predefined_attribute
    mock_client = MagicMock()
    mock_client.update_predefined_attribute.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_predefined_attribute("test-instance_id", "test-name", values="test-values", purposes="test-purposes", attribute_configuration={}, region_name="us-east-1")
    mock_client.update_predefined_attribute.assert_called_once()

def test_update_prompt_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_prompt
    mock_client = MagicMock()
    mock_client.update_prompt.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_prompt("test-instance_id", "test-prompt_id", name="test-name", description="test-description", s3_uri="test-s3_uri", region_name="us-east-1")
    mock_client.update_prompt.assert_called_once()

def test_update_queue_max_contacts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_queue_max_contacts
    mock_client = MagicMock()
    mock_client.update_queue_max_contacts.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_max_contacts("test-instance_id", "test-queue_id", max_contacts=1, region_name="us-east-1")
    mock_client.update_queue_max_contacts.assert_called_once()

def test_update_queue_name_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_queue_name
    mock_client = MagicMock()
    mock_client.update_queue_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_queue_name("test-instance_id", "test-queue_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_queue_name.assert_called_once()

def test_update_quick_connect_name_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_quick_connect_name
    mock_client = MagicMock()
    mock_client.update_quick_connect_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_quick_connect_name("test-instance_id", "test-quick_connect_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_quick_connect_name.assert_called_once()

def test_update_routing_profile_name_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_routing_profile_name
    mock_client = MagicMock()
    mock_client.update_routing_profile_name.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_routing_profile_name("test-instance_id", "test-routing_profile_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_routing_profile_name.assert_called_once()

def test_update_security_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_security_profile
    mock_client = MagicMock()
    mock_client.update_security_profile.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_security_profile("test-security_profile_id", "test-instance_id", description="test-description", permissions="test-permissions", allowed_access_control_tags=True, tag_restricted_resources="test-tag_restricted_resources", applications="test-applications", hierarchy_restricted_resources="test-hierarchy_restricted_resources", allowed_access_control_hierarchy_group_id=True, region_name="us-east-1")
    mock_client.update_security_profile.assert_called_once()

def test_update_task_template_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_task_template
    mock_client = MagicMock()
    mock_client.update_task_template.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_task_template("test-task_template_id", "test-instance_id", name="test-name", description="test-description", contact_flow_id="test-contact_flow_id", self_assign_flow_id="test-self_assign_flow_id", constraints="test-constraints", defaults="test-defaults", status="test-status", fields="test-fields", region_name="us-east-1")
    mock_client.update_task_template.assert_called_once()

def test_update_traffic_distribution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_traffic_distribution
    mock_client = MagicMock()
    mock_client.update_traffic_distribution.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_traffic_distribution("test-id", telephony_config={}, sign_in_config={}, agent_config={}, region_name="us-east-1")
    mock_client.update_traffic_distribution.assert_called_once()

def test_update_user_hierarchy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_user_hierarchy
    mock_client = MagicMock()
    mock_client.update_user_hierarchy.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_user_hierarchy("test-user_id", "test-instance_id", hierarchy_group_id="test-hierarchy_group_id", region_name="us-east-1")
    mock_client.update_user_hierarchy.assert_called_once()

def test_update_view_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import update_view_metadata
    mock_client = MagicMock()
    mock_client.update_view_metadata.return_value = {}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    update_view_metadata("test-instance_id", "test-view_id", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_view_metadata.assert_called_once()


def test_start_task_contact_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_task_contact
    mock_client = MagicMock()
    mock_client.start_task_contact.return_value = {"ContactId": "c-1"}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: mock_client)
    start_task_contact("i-1", "cf-1", "task", attributes={"k": "v"}, region_name="us-east-1")
    mock_client.start_task_contact.assert_called_once()


def test_create_user_all_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import create_user
    m = MagicMock(); m.create_user.return_value = {"UserId": "u"}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: m)
    create_user("i", "u", {}, [], "r", identity_info={"FirstName": "t"}, password="pw", region_name="us-east-1")

def test_start_outbound_voice_contact_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_outbound_voice_contact
    m = MagicMock(); m.start_outbound_voice_contact.return_value = {"ContactId": "c"}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: m)
    start_outbound_voice_contact("i", "cf", "+1", source_phone_number="+2", queue_id="q", attributes={"k": "v"}, region_name="us-east-1")

def test_start_chat_contact_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_chat_contact
    m = MagicMock(); m.start_chat_contact.return_value = {"ContactId": "c", "ParticipantId": "p", "ParticipantToken": "t"}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: m)
    start_chat_contact("i", "cf", {"DisplayName": "u"}, attributes={"k": "v"}, initial_message={"Content": "hi"}, region_name="us-east-1")

def test_start_task_contact_all_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.connect import start_task_contact
    m = MagicMock(); m.start_task_contact.return_value = {"ContactId": "c"}
    monkeypatch.setattr("aws_util.connect.get_client", lambda *a, **kw: m)
    start_task_contact("i", "cf", "task", attributes={"k": "v"}, references={"r": "v"}, description="desc", region_name="us-east-1")
