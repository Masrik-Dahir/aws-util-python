"""aws_util.connect -- Amazon Connect utilities.

Provides high-level helpers for managing Amazon Connect instances,
contact flows, queues, routing profiles, users, and contacts.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "ActivateEvaluationFormResult",
    "AssociateAnalyticsDataSetResult",
    "AssociateInstanceStorageConfigResult",
    "AssociateSecurityKeyResult",
    "BatchAssociateAnalyticsDataSetResult",
    "BatchDisassociateAnalyticsDataSetResult",
    "BatchGetAttachedFileMetadataResult",
    "BatchGetFlowAssociationResult",
    "BatchPutContactResult",
    "ClaimPhoneNumberResult",
    "ConnectContactFlow",
    "ConnectInstance",
    "ConnectQueue",
    "ConnectRoutingProfile",
    "ConnectUser",
    "ContactResult",
    "CreateAgentStatusResult",
    "CreateContactFlowModuleResult",
    "CreateContactFlowVersionResult",
    "CreateContactResult",
    "CreateEmailAddressResult",
    "CreateEvaluationFormResult",
    "CreateHoursOfOperationOverrideResult",
    "CreateHoursOfOperationResult",
    "CreateIntegrationAssociationResult",
    "CreateParticipantResult",
    "CreatePersistentContactAssociationResult",
    "CreatePromptResult",
    "CreatePushNotificationRegistrationResult",
    "CreateQuickConnectResult",
    "CreateRuleResult",
    "CreateSecurityProfileResult",
    "CreateTaskTemplateResult",
    "CreateTrafficDistributionGroupResult",
    "CreateUseCaseResult",
    "CreateUserHierarchyGroupResult",
    "CreateViewResult",
    "CreateViewVersionResult",
    "CreateVocabularyResult",
    "DeactivateEvaluationFormResult",
    "DeleteVocabularyResult",
    "DescribeAgentStatusResult",
    "DescribeAuthenticationProfileResult",
    "DescribeContactEvaluationResult",
    "DescribeContactFlowModuleResult",
    "DescribeContactResult",
    "DescribeEmailAddressResult",
    "DescribeEvaluationFormResult",
    "DescribeHoursOfOperationOverrideResult",
    "DescribeHoursOfOperationResult",
    "DescribeInstanceAttributeResult",
    "DescribeInstanceStorageConfigResult",
    "DescribePhoneNumberResult",
    "DescribePredefinedAttributeResult",
    "DescribePromptResult",
    "DescribeQuickConnectResult",
    "DescribeRuleResult",
    "DescribeSecurityProfileResult",
    "DescribeTrafficDistributionGroupResult",
    "DescribeUserHierarchyGroupResult",
    "DescribeUserHierarchyStructureResult",
    "DescribeViewResult",
    "DescribeVocabularyResult",
    "GetAttachedFileResult",
    "GetContactMetricsResult",
    "GetCurrentUserDataResult",
    "GetEffectiveHoursOfOperationsResult",
    "GetFederationTokenResult",
    "GetFlowAssociationResult",
    "GetMetricDataResult",
    "GetMetricDataV2Result",
    "GetPromptFileResult",
    "GetTaskTemplateResult",
    "GetTrafficDistributionResult",
    "ImportPhoneNumberResult",
    "ListAgentStatusesResult",
    "ListAnalyticsDataAssociationsResult",
    "ListAnalyticsDataLakeDataSetsResult",
    "ListApprovedOriginsResult",
    "ListAssociatedContactsResult",
    "ListAuthenticationProfilesResult",
    "ListBotsResult",
    "ListContactEvaluationsResult",
    "ListContactFlowModulesResult",
    "ListContactFlowVersionsResult",
    "ListContactReferencesResult",
    "ListDefaultVocabulariesResult",
    "ListEvaluationFormVersionsResult",
    "ListEvaluationFormsResult",
    "ListFlowAssociationsResult",
    "ListHoursOfOperationOverridesResult",
    "ListHoursOfOperationsResult",
    "ListInstanceAttributesResult",
    "ListInstanceStorageConfigsResult",
    "ListIntegrationAssociationsResult",
    "ListLambdaFunctionsResult",
    "ListLexBotsResult",
    "ListPhoneNumbersResult",
    "ListPhoneNumbersV2Result",
    "ListPredefinedAttributesResult",
    "ListPromptsResult",
    "ListQueueQuickConnectsResult",
    "ListQuickConnectsResult",
    "ListRealtimeContactAnalysisSegmentsV2Result",
    "ListRoutingProfileManualAssignmentQueuesResult",
    "ListRoutingProfileQueuesResult",
    "ListRulesResult",
    "ListSecurityKeysResult",
    "ListSecurityProfileApplicationsResult",
    "ListSecurityProfilePermissionsResult",
    "ListSecurityProfilesResult",
    "ListTagsForResourceResult",
    "ListTaskTemplatesResult",
    "ListTrafficDistributionGroupUsersResult",
    "ListTrafficDistributionGroupsResult",
    "ListUseCasesResult",
    "ListUserHierarchyGroupsResult",
    "ListUserProficienciesResult",
    "ListViewVersionsResult",
    "ListViewsResult",
    "MetricResult",
    "MonitorContactResult",
    "ReplicateInstanceResult",
    "SearchAgentStatusesResult",
    "SearchAvailablePhoneNumbersResult",
    "SearchContactEvaluationsResult",
    "SearchContactFlowModulesResult",
    "SearchContactFlowsResult",
    "SearchContactsResult",
    "SearchEmailAddressesResult",
    "SearchEvaluationFormsResult",
    "SearchHoursOfOperationOverridesResult",
    "SearchHoursOfOperationsResult",
    "SearchPredefinedAttributesResult",
    "SearchPromptsResult",
    "SearchQueuesResult",
    "SearchQuickConnectsResult",
    "SearchResourceTagsResult",
    "SearchRoutingProfilesResult",
    "SearchSecurityProfilesResult",
    "SearchUserHierarchyGroupsResult",
    "SearchUsersResult",
    "SearchVocabulariesResult",
    "SendChatIntegrationEventResult",
    "StartAttachedFileUploadResult",
    "StartContactEvaluationResult",
    "StartContactStreamingResult",
    "StartEmailContactResult",
    "StartOutboundChatContactResult",
    "StartOutboundEmailContactResult",
    "StartWebRtcContactResult",
    "SubmitContactEvaluationResult",
    "TransferContactResult",
    "UpdateContactEvaluationResult",
    "UpdateEmailAddressMetadataResult",
    "UpdateEvaluationFormResult",
    "UpdatePhoneNumberResult",
    "UpdatePromptResult",
    "UpdateTaskTemplateResult",
    "UpdateViewContentResult",
    "activate_evaluation_form",
    "associate_analytics_data_set",
    "associate_approved_origin",
    "associate_bot",
    "associate_contact_with_user",
    "associate_default_vocabulary",
    "associate_email_address_alias",
    "associate_flow",
    "associate_instance_storage_config",
    "associate_lambda_function",
    "associate_lex_bot",
    "associate_phone_number_contact_flow",
    "associate_queue_quick_connects",
    "associate_routing_profile_queues",
    "associate_security_key",
    "associate_traffic_distribution_group_user",
    "associate_user_proficiencies",
    "batch_associate_analytics_data_set",
    "batch_disassociate_analytics_data_set",
    "batch_get_attached_file_metadata",
    "batch_get_flow_association",
    "batch_put_contact",
    "claim_phone_number",
    "complete_attached_file_upload",
    "create_agent_status",
    "create_contact",
    "create_contact_flow",
    "create_contact_flow_module",
    "create_contact_flow_version",
    "create_email_address",
    "create_evaluation_form",
    "create_hours_of_operation",
    "create_hours_of_operation_override",
    "create_instance",
    "create_integration_association",
    "create_participant",
    "create_persistent_contact_association",
    "create_predefined_attribute",
    "create_prompt",
    "create_push_notification_registration",
    "create_queue",
    "create_quick_connect",
    "create_routing_profile",
    "create_rule",
    "create_security_profile",
    "create_task_template",
    "create_traffic_distribution_group",
    "create_use_case",
    "create_user",
    "create_user_hierarchy_group",
    "create_view",
    "create_view_version",
    "create_vocabulary",
    "deactivate_evaluation_form",
    "delete_attached_file",
    "delete_contact_evaluation",
    "delete_contact_flow",
    "delete_contact_flow_module",
    "delete_contact_flow_version",
    "delete_email_address",
    "delete_evaluation_form",
    "delete_hours_of_operation",
    "delete_hours_of_operation_override",
    "delete_instance",
    "delete_integration_association",
    "delete_predefined_attribute",
    "delete_prompt",
    "delete_push_notification_registration",
    "delete_queue",
    "delete_quick_connect",
    "delete_routing_profile",
    "delete_rule",
    "delete_security_profile",
    "delete_task_template",
    "delete_traffic_distribution_group",
    "delete_use_case",
    "delete_user",
    "delete_user_hierarchy_group",
    "delete_view",
    "delete_view_version",
    "delete_vocabulary",
    "describe_agent_status",
    "describe_authentication_profile",
    "describe_contact",
    "describe_contact_evaluation",
    "describe_contact_flow",
    "describe_contact_flow_module",
    "describe_email_address",
    "describe_evaluation_form",
    "describe_hours_of_operation",
    "describe_hours_of_operation_override",
    "describe_instance",
    "describe_instance_attribute",
    "describe_instance_storage_config",
    "describe_phone_number",
    "describe_predefined_attribute",
    "describe_prompt",
    "describe_queue",
    "describe_quick_connect",
    "describe_routing_profile",
    "describe_rule",
    "describe_security_profile",
    "describe_traffic_distribution_group",
    "describe_user",
    "describe_user_hierarchy_group",
    "describe_user_hierarchy_structure",
    "describe_view",
    "describe_vocabulary",
    "disassociate_analytics_data_set",
    "disassociate_approved_origin",
    "disassociate_bot",
    "disassociate_email_address_alias",
    "disassociate_flow",
    "disassociate_instance_storage_config",
    "disassociate_lambda_function",
    "disassociate_lex_bot",
    "disassociate_phone_number_contact_flow",
    "disassociate_queue_quick_connects",
    "disassociate_routing_profile_queues",
    "disassociate_security_key",
    "disassociate_traffic_distribution_group_user",
    "disassociate_user_proficiencies",
    "dismiss_user_contact",
    "get_attached_file",
    "get_contact_attributes",
    "get_contact_metrics",
    "get_current_metric_data",
    "get_current_user_data",
    "get_effective_hours_of_operations",
    "get_federation_token",
    "get_flow_association",
    "get_metric_data",
    "get_metric_data_v2",
    "get_prompt_file",
    "get_task_template",
    "get_traffic_distribution",
    "import_phone_number",
    "list_agent_statuses",
    "list_analytics_data_associations",
    "list_analytics_data_lake_data_sets",
    "list_approved_origins",
    "list_associated_contacts",
    "list_authentication_profiles",
    "list_bots",
    "list_contact_evaluations",
    "list_contact_flow_modules",
    "list_contact_flow_versions",
    "list_contact_flows",
    "list_contact_references",
    "list_default_vocabularies",
    "list_evaluation_form_versions",
    "list_evaluation_forms",
    "list_flow_associations",
    "list_hours_of_operation_overrides",
    "list_hours_of_operations",
    "list_instance_attributes",
    "list_instance_storage_configs",
    "list_instances",
    "list_integration_associations",
    "list_lambda_functions",
    "list_lex_bots",
    "list_phone_numbers",
    "list_phone_numbers_v2",
    "list_predefined_attributes",
    "list_prompts",
    "list_queue_quick_connects",
    "list_queues",
    "list_quick_connects",
    "list_realtime_contact_analysis_segments_v2",
    "list_routing_profile_manual_assignment_queues",
    "list_routing_profile_queues",
    "list_routing_profiles",
    "list_rules",
    "list_security_keys",
    "list_security_profile_applications",
    "list_security_profile_permissions",
    "list_security_profiles",
    "list_tags_for_resource",
    "list_task_templates",
    "list_traffic_distribution_group_users",
    "list_traffic_distribution_groups",
    "list_use_cases",
    "list_user_hierarchy_groups",
    "list_user_proficiencies",
    "list_users",
    "list_view_versions",
    "list_views",
    "monitor_contact",
    "pause_contact",
    "put_user_status",
    "release_phone_number",
    "replicate_instance",
    "resume_contact",
    "resume_contact_recording",
    "search_agent_statuses",
    "search_available_phone_numbers",
    "search_contact_evaluations",
    "search_contact_flow_modules",
    "search_contact_flows",
    "search_contacts",
    "search_email_addresses",
    "search_evaluation_forms",
    "search_hours_of_operation_overrides",
    "search_hours_of_operations",
    "search_predefined_attributes",
    "search_prompts",
    "search_queues",
    "search_quick_connects",
    "search_resource_tags",
    "search_routing_profiles",
    "search_security_profiles",
    "search_user_hierarchy_groups",
    "search_users",
    "search_vocabularies",
    "send_chat_integration_event",
    "send_outbound_email",
    "start_attached_file_upload",
    "start_chat_contact",
    "start_contact_evaluation",
    "start_contact_recording",
    "start_contact_streaming",
    "start_email_contact",
    "start_outbound_chat_contact",
    "start_outbound_email_contact",
    "start_outbound_voice_contact",
    "start_screen_sharing",
    "start_task_contact",
    "start_web_rtc_contact",
    "stop_contact",
    "stop_contact_recording",
    "stop_contact_streaming",
    "submit_contact_evaluation",
    "suspend_contact_recording",
    "tag_contact",
    "tag_resource",
    "transfer_contact",
    "untag_contact",
    "untag_resource",
    "update_agent_status",
    "update_authentication_profile",
    "update_contact",
    "update_contact_attributes",
    "update_contact_evaluation",
    "update_contact_flow_content",
    "update_contact_flow_metadata",
    "update_contact_flow_module_content",
    "update_contact_flow_module_metadata",
    "update_contact_flow_name",
    "update_contact_routing_data",
    "update_contact_schedule",
    "update_email_address_metadata",
    "update_evaluation_form",
    "update_hours_of_operation",
    "update_hours_of_operation_override",
    "update_instance_attribute",
    "update_instance_storage_config",
    "update_participant_authentication",
    "update_participant_role_config",
    "update_phone_number",
    "update_phone_number_metadata",
    "update_predefined_attribute",
    "update_prompt",
    "update_queue_hours_of_operation",
    "update_queue_max_contacts",
    "update_queue_name",
    "update_queue_outbound_caller_config",
    "update_queue_outbound_email_config",
    "update_queue_status",
    "update_quick_connect_config",
    "update_quick_connect_name",
    "update_routing_profile_agent_availability_timer",
    "update_routing_profile_concurrency",
    "update_routing_profile_default_outbound_queue",
    "update_routing_profile_name",
    "update_routing_profile_queues",
    "update_rule",
    "update_security_profile",
    "update_task_template",
    "update_traffic_distribution",
    "update_user_hierarchy",
    "update_user_hierarchy_group_name",
    "update_user_hierarchy_structure",
    "update_user_identity_info",
    "update_user_phone_config",
    "update_user_proficiencies",
    "update_user_routing_profile",
    "update_user_security_profiles",
    "update_view_content",
    "update_view_metadata",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ConnectInstance(BaseModel):
    """Metadata for an Amazon Connect instance."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    instance_id: str
    instance_alias: str | None = None
    arn: str | None = None
    identity_management_type: str | None = None
    instance_status: str | None = None
    created_time: Any = None


class ConnectContactFlow(BaseModel):
    """Metadata for an Amazon Connect contact flow."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    contact_flow_id: str
    name: str
    arn: str | None = None
    type: str | None = None
    state: str | None = None
    content: str | None = None


class ConnectQueue(BaseModel):
    """Metadata for an Amazon Connect queue."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    queue_id: str
    name: str
    arn: str | None = None
    status: str | None = None
    description: str | None = None


class ConnectRoutingProfile(BaseModel):
    """Metadata for an Amazon Connect routing profile."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    routing_profile_id: str
    name: str
    arn: str | None = None
    description: str | None = None
    default_outbound_queue_id: str | None = None


class ConnectUser(BaseModel):
    """Metadata for an Amazon Connect user."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    user_id: str
    username: str | None = None
    arn: str | None = None
    routing_profile_id: str | None = None
    security_profile_ids: list[str] = []


class ContactResult(BaseModel):
    """Result of starting a contact (voice, chat, or task)."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    contact_id: str


class MetricResult(BaseModel):
    """A single metric result from GetCurrentMetricData."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    dimensions: dict[str, Any] = {}
    collections: list[dict[str, Any]] = []


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


def create_instance(
    identity_management_type: str,
    inbound_calls_enabled: bool = True,
    outbound_calls_enabled: bool = True,
    instance_alias: str | None = None,
    region_name: str | None = None,
) -> ConnectInstance:
    """Create an Amazon Connect instance.

    Args:
        identity_management_type: Identity management type
            (e.g. ``"CONNECT_MANAGED"``).
        inbound_calls_enabled: Whether inbound calls are enabled.
        outbound_calls_enabled: Whether outbound calls are enabled.
        instance_alias: A friendly name for the instance.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectInstance` with the new instance details.

    Raises:
        RuntimeError: If creation fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "IdentityManagementType": identity_management_type,
        "InboundCallsEnabled": inbound_calls_enabled,
        "OutboundCallsEnabled": outbound_calls_enabled,
    }
    if instance_alias is not None:
        kwargs["InstanceAlias"] = instance_alias
    try:
        resp = client.create_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_instance failed") from exc
    return ConnectInstance(
        instance_id=resp["Id"],
        arn=resp.get("Arn"),
    )


def describe_instance(
    instance_id: str,
    region_name: str | None = None,
) -> ConnectInstance:
    """Describe an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectInstance` with instance details.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.describe_instance(InstanceId=instance_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_instance failed for {instance_id!r}") from exc
    inst = resp["Instance"]
    return ConnectInstance(
        instance_id=inst["Id"],
        instance_alias=inst.get("InstanceAlias"),
        arn=inst.get("Arn"),
        identity_management_type=inst.get("IdentityManagementType"),
        instance_status=inst.get("InstanceStatus"),
        created_time=inst.get("CreatedTime"),
    )


def list_instances(
    region_name: str | None = None,
) -> list[ConnectInstance]:
    """List Amazon Connect instances in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ConnectInstance` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    instances: list[ConnectInstance] = []
    kwargs: dict[str, Any] = {}
    try:
        while True:
            resp = client.list_instances(**kwargs)
            for item in resp.get("InstanceSummaryList", []):
                instances.append(
                    ConnectInstance(
                        instance_id=item["Id"],
                        instance_alias=item.get("InstanceAlias"),
                        arn=item.get("Arn"),
                        identity_management_type=item.get("IdentityManagementType"),
                        instance_status=item.get("InstanceStatus"),
                        created_time=item.get("CreatedTime"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_instances failed") from exc
    return instances


def delete_instance(
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Delete an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = get_client("connect", region_name)
    try:
        client.delete_instance(InstanceId=instance_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_instance failed for {instance_id!r}") from exc


# ---------------------------------------------------------------------------
# Contact flow operations
# ---------------------------------------------------------------------------


def create_contact_flow(
    instance_id: str,
    name: str,
    type: str,
    content: str,
    description: str | None = None,
    region_name: str | None = None,
) -> ConnectContactFlow:
    """Create a contact flow in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        name: Name of the contact flow.
        type: Contact flow type (e.g. ``"CONTACT_FLOW"``).
        content: JSON content of the contact flow.
        description: Optional description.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectContactFlow` with the new flow details.

    Raises:
        RuntimeError: If creation fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "Name": name,
        "Type": type,
        "Content": content,
    }
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.create_contact_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_contact_flow failed for {name!r}") from exc
    return ConnectContactFlow(
        contact_flow_id=resp["ContactFlowId"],
        name=name,
        arn=resp.get("ContactFlowArn"),
        type=type,
    )


def describe_contact_flow(
    instance_id: str,
    contact_flow_id: str,
    region_name: str | None = None,
) -> ConnectContactFlow:
    """Describe a contact flow.

    Args:
        instance_id: The instance identifier.
        contact_flow_id: The contact flow identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectContactFlow` with flow details.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.describe_contact_flow(
            InstanceId=instance_id,
            ContactFlowId=contact_flow_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_contact_flow failed for {contact_flow_id!r}") from exc
    flow = resp["ContactFlow"]
    return ConnectContactFlow(
        contact_flow_id=flow["Id"],
        name=flow["Name"],
        arn=flow.get("Arn"),
        type=flow.get("Type"),
        state=flow.get("State"),
        content=flow.get("Content"),
    )


def list_contact_flows(
    instance_id: str,
    contact_flow_types: list[str] | None = None,
    region_name: str | None = None,
) -> list[ConnectContactFlow]:
    """List contact flows in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        contact_flow_types: Optional filter by contact flow types.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConnectContactFlow` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    flows: list[ConnectContactFlow] = []
    kwargs: dict[str, Any] = {"InstanceId": instance_id}
    if contact_flow_types is not None:
        kwargs["ContactFlowTypes"] = contact_flow_types
    try:
        while True:
            resp = client.list_contact_flows(**kwargs)
            for item in resp.get("ContactFlowSummaryList", []):
                flows.append(
                    ConnectContactFlow(
                        contact_flow_id=item["Id"],
                        name=item["Name"],
                        arn=item.get("Arn"),
                        type=item.get("ContactFlowType"),
                        state=item.get("ContactFlowState"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_contact_flows failed") from exc
    return flows


def update_contact_flow_content(
    instance_id: str,
    contact_flow_id: str,
    content: str,
    region_name: str | None = None,
) -> None:
    """Update the content of a contact flow.

    Args:
        instance_id: The instance identifier.
        contact_flow_id: The contact flow identifier.
        content: New JSON content for the contact flow.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    client = get_client("connect", region_name)
    try:
        client.update_contact_flow_content(
            InstanceId=instance_id,
            ContactFlowId=contact_flow_id,
            Content=content,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"update_contact_flow_content failed for {contact_flow_id!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Queue operations
# ---------------------------------------------------------------------------


def create_queue(
    instance_id: str,
    name: str,
    hours_of_operation_id: str,
    description: str | None = None,
    region_name: str | None = None,
) -> ConnectQueue:
    """Create a queue in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        name: Name of the queue.
        hours_of_operation_id: Hours of operation identifier.
        description: Optional description.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectQueue` with the new queue details.

    Raises:
        RuntimeError: If creation fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "Name": name,
        "HoursOfOperationId": hours_of_operation_id,
    }
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.create_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_queue failed for {name!r}") from exc
    return ConnectQueue(
        queue_id=resp["QueueId"],
        name=name,
        arn=resp.get("QueueArn"),
    )


def describe_queue(
    instance_id: str,
    queue_id: str,
    region_name: str | None = None,
) -> ConnectQueue:
    """Describe a queue.

    Args:
        instance_id: The instance identifier.
        queue_id: The queue identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectQueue` with queue details.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.describe_queue(InstanceId=instance_id, QueueId=queue_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_queue failed for {queue_id!r}") from exc
    queue = resp["Queue"]
    return ConnectQueue(
        queue_id=queue["QueueId"],
        name=queue["Name"],
        arn=queue.get("QueueArn"),
        status=queue.get("Status"),
        description=queue.get("Description"),
    )


def list_queues(
    instance_id: str,
    queue_types: list[str] | None = None,
    region_name: str | None = None,
) -> list[ConnectQueue]:
    """List queues in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        queue_types: Optional filter by queue types.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConnectQueue` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    queues: list[ConnectQueue] = []
    kwargs: dict[str, Any] = {"InstanceId": instance_id}
    if queue_types is not None:
        kwargs["QueueTypes"] = queue_types
    try:
        while True:
            resp = client.list_queues(**kwargs)
            for item in resp.get("QueueSummaryList", []):
                queues.append(
                    ConnectQueue(
                        queue_id=item["Id"],
                        name=item["Name"],
                        arn=item.get("Arn"),
                        status=item.get("QueueType"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_queues failed") from exc
    return queues


def update_queue_status(
    instance_id: str,
    queue_id: str,
    status: str,
    region_name: str | None = None,
) -> None:
    """Update the status of a queue.

    Args:
        instance_id: The instance identifier.
        queue_id: The queue identifier.
        status: New status (``"ENABLED"`` or ``"DISABLED"``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    client = get_client("connect", region_name)
    try:
        client.update_queue_status(
            InstanceId=instance_id,
            QueueId=queue_id,
            Status=status,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_queue_status failed for {queue_id!r}") from exc


# ---------------------------------------------------------------------------
# Routing profile operations
# ---------------------------------------------------------------------------


def create_routing_profile(
    instance_id: str,
    name: str,
    default_outbound_queue_id: str,
    description: str,
    media_concurrencies: list[dict[str, Any]],
    region_name: str | None = None,
) -> ConnectRoutingProfile:
    """Create a routing profile in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        name: Name of the routing profile.
        default_outbound_queue_id: Default outbound queue identifier.
        description: Description of the routing profile.
        media_concurrencies: Media concurrency settings.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectRoutingProfile` with the new profile details.

    Raises:
        RuntimeError: If creation fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.create_routing_profile(
            InstanceId=instance_id,
            Name=name,
            DefaultOutboundQueueId=default_outbound_queue_id,
            Description=description,
            MediaConcurrencies=media_concurrencies,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_routing_profile failed for {name!r}") from exc
    return ConnectRoutingProfile(
        routing_profile_id=resp["RoutingProfileId"],
        name=name,
        arn=resp.get("RoutingProfileArn"),
        description=description,
        default_outbound_queue_id=default_outbound_queue_id,
    )


def describe_routing_profile(
    instance_id: str,
    routing_profile_id: str,
    region_name: str | None = None,
) -> ConnectRoutingProfile:
    """Describe a routing profile.

    Args:
        instance_id: The instance identifier.
        routing_profile_id: The routing profile identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectRoutingProfile` with profile details.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.describe_routing_profile(
            InstanceId=instance_id,
            RoutingProfileId=routing_profile_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"describe_routing_profile failed for {routing_profile_id!r}"
        ) from exc
    profile = resp["RoutingProfile"]
    return ConnectRoutingProfile(
        routing_profile_id=profile["RoutingProfileId"],
        name=profile["Name"],
        arn=profile.get("RoutingProfileArn"),
        description=profile.get("Description"),
        default_outbound_queue_id=profile.get("DefaultOutboundQueueId"),
    )


def list_routing_profiles(
    instance_id: str,
    region_name: str | None = None,
) -> list[ConnectRoutingProfile]:
    """List routing profiles in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConnectRoutingProfile` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    profiles: list[ConnectRoutingProfile] = []
    kwargs: dict[str, Any] = {"InstanceId": instance_id}
    try:
        while True:
            resp = client.list_routing_profiles(**kwargs)
            for item in resp.get("RoutingProfileSummaryList", []):
                profiles.append(
                    ConnectRoutingProfile(
                        routing_profile_id=item["Id"],
                        name=item["Name"],
                        arn=item.get("Arn"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_routing_profiles failed") from exc
    return profiles


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


def create_user(
    instance_id: str,
    username: str,
    phone_config: dict[str, Any],
    security_profile_ids: list[str],
    routing_profile_id: str,
    identity_info: dict[str, Any] | None = None,
    password: str | None = None,
    region_name: str | None = None,
) -> ConnectUser:
    """Create a user in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        username: The username.
        phone_config: Phone configuration dict.
        security_profile_ids: List of security profile identifiers.
        routing_profile_id: Routing profile identifier.
        identity_info: Optional identity information dict.
        password: Optional password for the user.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectUser` with the new user details.

    Raises:
        RuntimeError: If creation fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "Username": username,
        "PhoneConfig": phone_config,
        "SecurityProfileIds": security_profile_ids,
        "RoutingProfileId": routing_profile_id,
    }
    if identity_info is not None:
        kwargs["IdentityInfo"] = identity_info
    if password is not None:
        kwargs["Password"] = password
    try:
        resp = client.create_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_user failed for {username!r}") from exc
    return ConnectUser(
        user_id=resp["UserId"],
        username=username,
        arn=resp.get("UserArn"),
        routing_profile_id=routing_profile_id,
        security_profile_ids=security_profile_ids,
    )


def describe_user(
    instance_id: str,
    user_id: str,
    region_name: str | None = None,
) -> ConnectUser:
    """Describe a user.

    Args:
        instance_id: The instance identifier.
        user_id: The user identifier.
        region_name: AWS region override.

    Returns:
        A :class:`ConnectUser` with user details.

    Raises:
        RuntimeError: If the describe call fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.describe_user(InstanceId=instance_id, UserId=user_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_user failed for {user_id!r}") from exc
    user = resp["User"]
    return ConnectUser(
        user_id=user["Id"],
        username=user.get("Username"),
        arn=user.get("Arn"),
        routing_profile_id=user.get("RoutingProfileId"),
        security_profile_ids=user.get("SecurityProfileIds", []),
    )


def list_users(
    instance_id: str,
    region_name: str | None = None,
) -> list[ConnectUser]:
    """List users in an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConnectUser` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    users: list[ConnectUser] = []
    kwargs: dict[str, Any] = {"InstanceId": instance_id}
    try:
        while True:
            resp = client.list_users(**kwargs)
            for item in resp.get("UserSummaryList", []):
                users.append(
                    ConnectUser(
                        user_id=item["Id"],
                        username=item.get("Username"),
                        arn=item.get("Arn"),
                    )
                )
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_users failed") from exc
    return users


def update_user_routing_profile(
    instance_id: str,
    user_id: str,
    routing_profile_id: str,
    region_name: str | None = None,
) -> None:
    """Update the routing profile assigned to a user.

    Args:
        instance_id: The instance identifier.
        user_id: The user identifier.
        routing_profile_id: New routing profile identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    client = get_client("connect", region_name)
    try:
        client.update_user_routing_profile(
            InstanceId=instance_id,
            UserId=user_id,
            RoutingProfileId=routing_profile_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_user_routing_profile failed for {user_id!r}") from exc


def delete_user(
    instance_id: str,
    user_id: str,
    region_name: str | None = None,
) -> None:
    """Delete a user from an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        user_id: The user identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If deletion fails.
    """
    client = get_client("connect", region_name)
    try:
        client.delete_user(InstanceId=instance_id, UserId=user_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_user failed for {user_id!r}") from exc


# ---------------------------------------------------------------------------
# Contact operations
# ---------------------------------------------------------------------------


def start_outbound_voice_contact(
    instance_id: str,
    contact_flow_id: str,
    destination_phone_number: str,
    source_phone_number: str | None = None,
    queue_id: str | None = None,
    attributes: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ContactResult:
    """Start an outbound voice contact.

    Args:
        instance_id: The instance identifier.
        contact_flow_id: The contact flow to use.
        destination_phone_number: Phone number to call.
        source_phone_number: Caller ID phone number.
        queue_id: Queue identifier for the contact.
        attributes: Contact attributes.
        region_name: AWS region override.

    Returns:
        A :class:`ContactResult` with the contact identifier.

    Raises:
        RuntimeError: If the call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "ContactFlowId": contact_flow_id,
        "DestinationPhoneNumber": destination_phone_number,
    }
    if source_phone_number is not None:
        kwargs["SourcePhoneNumber"] = source_phone_number
    if queue_id is not None:
        kwargs["QueueId"] = queue_id
    if attributes is not None:
        kwargs["Attributes"] = attributes
    try:
        resp = client.start_outbound_voice_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_outbound_voice_contact failed") from exc
    return ContactResult(contact_id=resp["ContactId"])


def start_chat_contact(
    instance_id: str,
    contact_flow_id: str,
    participant_details: dict[str, str],
    attributes: dict[str, str] | None = None,
    initial_message: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ContactResult:
    """Start a chat contact.

    Args:
        instance_id: The instance identifier.
        contact_flow_id: The contact flow to use.
        participant_details: Participant details (e.g. display name).
        attributes: Contact attributes.
        initial_message: Optional initial message dict.
        region_name: AWS region override.

    Returns:
        A :class:`ContactResult` with the contact identifier.

    Raises:
        RuntimeError: If the call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "ContactFlowId": contact_flow_id,
        "ParticipantDetails": participant_details,
    }
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if initial_message is not None:
        kwargs["InitialMessage"] = initial_message
    try:
        resp = client.start_chat_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_chat_contact failed") from exc
    return ContactResult(contact_id=resp["ContactId"])


def stop_contact(
    contact_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Stop an active contact.

    Args:
        contact_id: The contact identifier.
        instance_id: The instance identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If stopping the contact fails.
    """
    client = get_client("connect", region_name)
    try:
        client.stop_contact(ContactId=contact_id, InstanceId=instance_id)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"stop_contact failed for {contact_id!r}") from exc


def get_contact_attributes(
    instance_id: str,
    initial_contact_id: str,
    region_name: str | None = None,
) -> dict[str, str]:
    """Get attributes for a contact.

    Args:
        instance_id: The instance identifier.
        initial_contact_id: The initial contact identifier.
        region_name: AWS region override.

    Returns:
        A dict of contact attribute key-value pairs.

    Raises:
        RuntimeError: If the call fails.
    """
    client = get_client("connect", region_name)
    try:
        resp = client.get_contact_attributes(
            InstanceId=instance_id,
            InitialContactId=initial_contact_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"get_contact_attributes failed for {initial_contact_id!r}"
        ) from exc
    return resp.get("Attributes", {})


def update_contact_attributes(
    instance_id: str,
    initial_contact_id: str,
    attributes: dict[str, str],
    region_name: str | None = None,
) -> None:
    """Update attributes on a contact.

    Args:
        instance_id: The instance identifier.
        initial_contact_id: The initial contact identifier.
        attributes: Attribute key-value pairs to set.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the update fails.
    """
    client = get_client("connect", region_name)
    try:
        client.update_contact_attributes(
            InstanceId=instance_id,
            InitialContactId=initial_contact_id,
            Attributes=attributes,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"update_contact_attributes failed for {initial_contact_id!r}"
        ) from exc


def get_current_metric_data(
    instance_id: str,
    filters: dict[str, Any],
    current_metrics: list[dict[str, str]],
    groupings: list[str] | None = None,
    region_name: str | None = None,
) -> list[MetricResult]:
    """Get current metric data from an Amazon Connect instance.

    Args:
        instance_id: The instance identifier.
        filters: Filters for the metric data query.
        current_metrics: List of metric definitions to retrieve.
        groupings: Optional grouping dimensions.
        region_name: AWS region override.

    Returns:
        A list of :class:`MetricResult` objects.

    Raises:
        RuntimeError: If the call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "Filters": filters,
        "CurrentMetrics": current_metrics,
    }
    if groupings is not None:
        kwargs["Groupings"] = groupings
    try:
        resp = client.get_current_metric_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_current_metric_data failed") from exc
    results: list[MetricResult] = []
    for item in resp.get("MetricResults", []):
        results.append(
            MetricResult(
                dimensions=item.get("Dimensions", {}),
                collections=item.get("Collections", []),
            )
        )
    return results


def start_task_contact(
    instance_id: str,
    contact_flow_id: str,
    name: str,
    references: dict[str, dict[str, str]] | None = None,
    description: str | None = None,
    attributes: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ContactResult:
    """Start a task contact.

    Args:
        instance_id: The instance identifier.
        contact_flow_id: The contact flow to use for the task.
        name: Name of the task.
        references: Optional references dict.
        description: Optional task description.
        attributes: Optional contact attributes.
        region_name: AWS region override.

    Returns:
        A :class:`ContactResult` with the contact identifier.

    Raises:
        RuntimeError: If the call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {
        "InstanceId": instance_id,
        "ContactFlowId": contact_flow_id,
        "Name": name,
    }
    if references is not None:
        kwargs["References"] = references
    if description is not None:
        kwargs["Description"] = description
    if attributes is not None:
        kwargs["Attributes"] = attributes
    try:
        resp = client.start_task_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "start_task_contact failed") from exc
    return ContactResult(contact_id=resp["ContactId"])


class ActivateEvaluationFormResult(BaseModel):
    """Result of activate_evaluation_form."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_id: str | None = None
    evaluation_form_arn: str | None = None
    evaluation_form_version: int | None = None


class AssociateAnalyticsDataSetResult(BaseModel):
    """Result of associate_analytics_data_set."""

    model_config = ConfigDict(frozen=True)

    data_set_id: str | None = None
    target_account_id: str | None = None
    resource_share_id: str | None = None
    resource_share_arn: str | None = None


class AssociateInstanceStorageConfigResult(BaseModel):
    """Result of associate_instance_storage_config."""

    model_config = ConfigDict(frozen=True)

    association_id: str | None = None


class AssociateSecurityKeyResult(BaseModel):
    """Result of associate_security_key."""

    model_config = ConfigDict(frozen=True)

    association_id: str | None = None


class BatchAssociateAnalyticsDataSetResult(BaseModel):
    """Result of batch_associate_analytics_data_set."""

    model_config = ConfigDict(frozen=True)

    created: list[dict[str, Any]] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchDisassociateAnalyticsDataSetResult(BaseModel):
    """Result of batch_disassociate_analytics_data_set."""

    model_config = ConfigDict(frozen=True)

    deleted: list[str] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchGetAttachedFileMetadataResult(BaseModel):
    """Result of batch_get_attached_file_metadata."""

    model_config = ConfigDict(frozen=True)

    files: list[dict[str, Any]] | None = None
    errors: list[dict[str, Any]] | None = None


class BatchGetFlowAssociationResult(BaseModel):
    """Result of batch_get_flow_association."""

    model_config = ConfigDict(frozen=True)

    flow_association_summary_list: list[dict[str, Any]] | None = None


class BatchPutContactResult(BaseModel):
    """Result of batch_put_contact."""

    model_config = ConfigDict(frozen=True)

    successful_request_list: list[dict[str, Any]] | None = None
    failed_request_list: list[dict[str, Any]] | None = None


class ClaimPhoneNumberResult(BaseModel):
    """Result of claim_phone_number."""

    model_config = ConfigDict(frozen=True)

    phone_number_id: str | None = None
    phone_number_arn: str | None = None


class CreateAgentStatusResult(BaseModel):
    """Result of create_agent_status."""

    model_config = ConfigDict(frozen=True)

    agent_status_arn: str | None = None
    agent_status_id: str | None = None


class CreateContactResult(BaseModel):
    """Result of create_contact."""

    model_config = ConfigDict(frozen=True)

    contact_id: str | None = None
    contact_arn: str | None = None


class CreateContactFlowModuleResult(BaseModel):
    """Result of create_contact_flow_module."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None


class CreateContactFlowVersionResult(BaseModel):
    """Result of create_contact_flow_version."""

    model_config = ConfigDict(frozen=True)

    contact_flow_arn: str | None = None
    version: int | None = None


class CreateEmailAddressResult(BaseModel):
    """Result of create_email_address."""

    model_config = ConfigDict(frozen=True)

    email_address_id: str | None = None
    email_address_arn: str | None = None


class CreateEvaluationFormResult(BaseModel):
    """Result of create_evaluation_form."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_id: str | None = None
    evaluation_form_arn: str | None = None


class CreateHoursOfOperationResult(BaseModel):
    """Result of create_hours_of_operation."""

    model_config = ConfigDict(frozen=True)

    hours_of_operation_id: str | None = None
    hours_of_operation_arn: str | None = None


class CreateHoursOfOperationOverrideResult(BaseModel):
    """Result of create_hours_of_operation_override."""

    model_config = ConfigDict(frozen=True)

    hours_of_operation_override_id: str | None = None


class CreateIntegrationAssociationResult(BaseModel):
    """Result of create_integration_association."""

    model_config = ConfigDict(frozen=True)

    integration_association_id: str | None = None
    integration_association_arn: str | None = None


class CreateParticipantResult(BaseModel):
    """Result of create_participant."""

    model_config = ConfigDict(frozen=True)

    participant_credentials: dict[str, Any] | None = None
    participant_id: str | None = None


class CreatePersistentContactAssociationResult(BaseModel):
    """Result of create_persistent_contact_association."""

    model_config = ConfigDict(frozen=True)

    continued_from_contact_id: str | None = None


class CreatePromptResult(BaseModel):
    """Result of create_prompt."""

    model_config = ConfigDict(frozen=True)

    prompt_arn: str | None = None
    prompt_id: str | None = None


class CreatePushNotificationRegistrationResult(BaseModel):
    """Result of create_push_notification_registration."""

    model_config = ConfigDict(frozen=True)

    registration_id: str | None = None


class CreateQuickConnectResult(BaseModel):
    """Result of create_quick_connect."""

    model_config = ConfigDict(frozen=True)

    quick_connect_arn: str | None = None
    quick_connect_id: str | None = None


class CreateRuleResult(BaseModel):
    """Result of create_rule."""

    model_config = ConfigDict(frozen=True)

    rule_arn: str | None = None
    rule_id: str | None = None


class CreateSecurityProfileResult(BaseModel):
    """Result of create_security_profile."""

    model_config = ConfigDict(frozen=True)

    security_profile_id: str | None = None
    security_profile_arn: str | None = None


class CreateTaskTemplateResult(BaseModel):
    """Result of create_task_template."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None


class CreateTrafficDistributionGroupResult(BaseModel):
    """Result of create_traffic_distribution_group."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None


class CreateUseCaseResult(BaseModel):
    """Result of create_use_case."""

    model_config = ConfigDict(frozen=True)

    use_case_id: str | None = None
    use_case_arn: str | None = None


class CreateUserHierarchyGroupResult(BaseModel):
    """Result of create_user_hierarchy_group."""

    model_config = ConfigDict(frozen=True)

    hierarchy_group_id: str | None = None
    hierarchy_group_arn: str | None = None


class CreateViewResult(BaseModel):
    """Result of create_view."""

    model_config = ConfigDict(frozen=True)

    view: dict[str, Any] | None = None


class CreateViewVersionResult(BaseModel):
    """Result of create_view_version."""

    model_config = ConfigDict(frozen=True)

    view: dict[str, Any] | None = None


class CreateVocabularyResult(BaseModel):
    """Result of create_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary_arn: str | None = None
    vocabulary_id: str | None = None
    state: str | None = None


class DeactivateEvaluationFormResult(BaseModel):
    """Result of deactivate_evaluation_form."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_id: str | None = None
    evaluation_form_arn: str | None = None
    evaluation_form_version: int | None = None


class DeleteVocabularyResult(BaseModel):
    """Result of delete_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary_arn: str | None = None
    vocabulary_id: str | None = None
    state: str | None = None


class DescribeAgentStatusResult(BaseModel):
    """Result of describe_agent_status."""

    model_config = ConfigDict(frozen=True)

    agent_status: dict[str, Any] | None = None


class DescribeAuthenticationProfileResult(BaseModel):
    """Result of describe_authentication_profile."""

    model_config = ConfigDict(frozen=True)

    authentication_profile: dict[str, Any] | None = None


class DescribeContactResult(BaseModel):
    """Result of describe_contact."""

    model_config = ConfigDict(frozen=True)

    contact: dict[str, Any] | None = None


class DescribeContactEvaluationResult(BaseModel):
    """Result of describe_contact_evaluation."""

    model_config = ConfigDict(frozen=True)

    evaluation: dict[str, Any] | None = None
    evaluation_form: dict[str, Any] | None = None


class DescribeContactFlowModuleResult(BaseModel):
    """Result of describe_contact_flow_module."""

    model_config = ConfigDict(frozen=True)

    contact_flow_module: dict[str, Any] | None = None


class DescribeEmailAddressResult(BaseModel):
    """Result of describe_email_address."""

    model_config = ConfigDict(frozen=True)

    email_address_id: str | None = None
    email_address_arn: str | None = None
    email_address: str | None = None
    display_name: str | None = None
    description: str | None = None
    create_timestamp: str | None = None
    modified_timestamp: str | None = None
    alias_configurations: list[dict[str, Any]] | None = None
    tags: dict[str, Any] | None = None


class DescribeEvaluationFormResult(BaseModel):
    """Result of describe_evaluation_form."""

    model_config = ConfigDict(frozen=True)

    evaluation_form: dict[str, Any] | None = None


class DescribeHoursOfOperationResult(BaseModel):
    """Result of describe_hours_of_operation."""

    model_config = ConfigDict(frozen=True)

    hours_of_operation: dict[str, Any] | None = None


class DescribeHoursOfOperationOverrideResult(BaseModel):
    """Result of describe_hours_of_operation_override."""

    model_config = ConfigDict(frozen=True)

    hours_of_operation_override: dict[str, Any] | None = None


class DescribeInstanceAttributeResult(BaseModel):
    """Result of describe_instance_attribute."""

    model_config = ConfigDict(frozen=True)

    attribute: dict[str, Any] | None = None


class DescribeInstanceStorageConfigResult(BaseModel):
    """Result of describe_instance_storage_config."""

    model_config = ConfigDict(frozen=True)

    storage_config: dict[str, Any] | None = None


class DescribePhoneNumberResult(BaseModel):
    """Result of describe_phone_number."""

    model_config = ConfigDict(frozen=True)

    claimed_phone_number_summary: dict[str, Any] | None = None


class DescribePredefinedAttributeResult(BaseModel):
    """Result of describe_predefined_attribute."""

    model_config = ConfigDict(frozen=True)

    predefined_attribute: dict[str, Any] | None = None


class DescribePromptResult(BaseModel):
    """Result of describe_prompt."""

    model_config = ConfigDict(frozen=True)

    prompt: dict[str, Any] | None = None


class DescribeQuickConnectResult(BaseModel):
    """Result of describe_quick_connect."""

    model_config = ConfigDict(frozen=True)

    quick_connect: dict[str, Any] | None = None


class DescribeRuleResult(BaseModel):
    """Result of describe_rule."""

    model_config = ConfigDict(frozen=True)

    rule: dict[str, Any] | None = None


class DescribeSecurityProfileResult(BaseModel):
    """Result of describe_security_profile."""

    model_config = ConfigDict(frozen=True)

    security_profile: dict[str, Any] | None = None


class DescribeTrafficDistributionGroupResult(BaseModel):
    """Result of describe_traffic_distribution_group."""

    model_config = ConfigDict(frozen=True)

    traffic_distribution_group: dict[str, Any] | None = None


class DescribeUserHierarchyGroupResult(BaseModel):
    """Result of describe_user_hierarchy_group."""

    model_config = ConfigDict(frozen=True)

    hierarchy_group: dict[str, Any] | None = None


class DescribeUserHierarchyStructureResult(BaseModel):
    """Result of describe_user_hierarchy_structure."""

    model_config = ConfigDict(frozen=True)

    hierarchy_structure: dict[str, Any] | None = None


class DescribeViewResult(BaseModel):
    """Result of describe_view."""

    model_config = ConfigDict(frozen=True)

    view: dict[str, Any] | None = None


class DescribeVocabularyResult(BaseModel):
    """Result of describe_vocabulary."""

    model_config = ConfigDict(frozen=True)

    vocabulary: dict[str, Any] | None = None


class GetAttachedFileResult(BaseModel):
    """Result of get_attached_file."""

    model_config = ConfigDict(frozen=True)

    file_arn: str | None = None
    file_id: str | None = None
    creation_time: str | None = None
    file_status: str | None = None
    file_name: str | None = None
    file_size_in_bytes: int | None = None
    associated_resource_arn: str | None = None
    file_use_case_type: str | None = None
    created_by: dict[str, Any] | None = None
    download_url_metadata: dict[str, Any] | None = None
    tags: dict[str, Any] | None = None


class GetContactMetricsResult(BaseModel):
    """Result of get_contact_metrics."""

    model_config = ConfigDict(frozen=True)

    metric_results: list[dict[str, Any]] | None = None
    id: str | None = None
    arn: str | None = None


class GetCurrentUserDataResult(BaseModel):
    """Result of get_current_user_data."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    user_data_list: list[dict[str, Any]] | None = None
    approximate_total_count: int | None = None


class GetEffectiveHoursOfOperationsResult(BaseModel):
    """Result of get_effective_hours_of_operations."""

    model_config = ConfigDict(frozen=True)

    effective_hours_of_operation_list: list[dict[str, Any]] | None = None
    time_zone: str | None = None


class GetFederationTokenResult(BaseModel):
    """Result of get_federation_token."""

    model_config = ConfigDict(frozen=True)

    credentials: dict[str, Any] | None = None
    sign_in_url: str | None = None
    user_arn: str | None = None
    user_id: str | None = None


class GetFlowAssociationResult(BaseModel):
    """Result of get_flow_association."""

    model_config = ConfigDict(frozen=True)

    resource_id: str | None = None
    flow_id: str | None = None
    resource_type: str | None = None


class GetMetricDataResult(BaseModel):
    """Result of get_metric_data."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    metric_results: list[dict[str, Any]] | None = None


class GetMetricDataV2Result(BaseModel):
    """Result of get_metric_data_v2."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    metric_results: list[dict[str, Any]] | None = None


class GetPromptFileResult(BaseModel):
    """Result of get_prompt_file."""

    model_config = ConfigDict(frozen=True)

    prompt_presigned_url: str | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class GetTaskTemplateResult(BaseModel):
    """Result of get_task_template."""

    model_config = ConfigDict(frozen=True)

    instance_id: str | None = None
    id: str | None = None
    arn: str | None = None
    name: str | None = None
    description: str | None = None
    contact_flow_id: str | None = None
    self_assign_flow_id: str | None = None
    constraints: dict[str, Any] | None = None
    defaults: dict[str, Any] | None = None
    fields: list[dict[str, Any]] | None = None
    status: str | None = None
    last_modified_time: str | None = None
    created_time: str | None = None
    tags: dict[str, Any] | None = None


class GetTrafficDistributionResult(BaseModel):
    """Result of get_traffic_distribution."""

    model_config = ConfigDict(frozen=True)

    telephony_config: dict[str, Any] | None = None
    id: str | None = None
    arn: str | None = None
    sign_in_config: dict[str, Any] | None = None
    agent_config: dict[str, Any] | None = None


class ImportPhoneNumberResult(BaseModel):
    """Result of import_phone_number."""

    model_config = ConfigDict(frozen=True)

    phone_number_id: str | None = None
    phone_number_arn: str | None = None


class ListAgentStatusesResult(BaseModel):
    """Result of list_agent_statuses."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    agent_status_summary_list: list[dict[str, Any]] | None = None


class ListAnalyticsDataAssociationsResult(BaseModel):
    """Result of list_analytics_data_associations."""

    model_config = ConfigDict(frozen=True)

    results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAnalyticsDataLakeDataSetsResult(BaseModel):
    """Result of list_analytics_data_lake_data_sets."""

    model_config = ConfigDict(frozen=True)

    results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListApprovedOriginsResult(BaseModel):
    """Result of list_approved_origins."""

    model_config = ConfigDict(frozen=True)

    origins: list[str] | None = None
    next_token: str | None = None


class ListAssociatedContactsResult(BaseModel):
    """Result of list_associated_contacts."""

    model_config = ConfigDict(frozen=True)

    contact_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAuthenticationProfilesResult(BaseModel):
    """Result of list_authentication_profiles."""

    model_config = ConfigDict(frozen=True)

    authentication_profile_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListBotsResult(BaseModel):
    """Result of list_bots."""

    model_config = ConfigDict(frozen=True)

    lex_bots: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListContactEvaluationsResult(BaseModel):
    """Result of list_contact_evaluations."""

    model_config = ConfigDict(frozen=True)

    evaluation_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListContactFlowModulesResult(BaseModel):
    """Result of list_contact_flow_modules."""

    model_config = ConfigDict(frozen=True)

    contact_flow_modules_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListContactFlowVersionsResult(BaseModel):
    """Result of list_contact_flow_versions."""

    model_config = ConfigDict(frozen=True)

    contact_flow_version_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListContactReferencesResult(BaseModel):
    """Result of list_contact_references."""

    model_config = ConfigDict(frozen=True)

    reference_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListDefaultVocabulariesResult(BaseModel):
    """Result of list_default_vocabularies."""

    model_config = ConfigDict(frozen=True)

    default_vocabulary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEvaluationFormVersionsResult(BaseModel):
    """Result of list_evaluation_form_versions."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_version_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListEvaluationFormsResult(BaseModel):
    """Result of list_evaluation_forms."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListFlowAssociationsResult(BaseModel):
    """Result of list_flow_associations."""

    model_config = ConfigDict(frozen=True)

    flow_association_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListHoursOfOperationOverridesResult(BaseModel):
    """Result of list_hours_of_operation_overrides."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    hours_of_operation_override_list: list[dict[str, Any]] | None = None
    last_modified_region: str | None = None
    last_modified_time: str | None = None


class ListHoursOfOperationsResult(BaseModel):
    """Result of list_hours_of_operations."""

    model_config = ConfigDict(frozen=True)

    hours_of_operation_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInstanceAttributesResult(BaseModel):
    """Result of list_instance_attributes."""

    model_config = ConfigDict(frozen=True)

    attributes: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInstanceStorageConfigsResult(BaseModel):
    """Result of list_instance_storage_configs."""

    model_config = ConfigDict(frozen=True)

    storage_configs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListIntegrationAssociationsResult(BaseModel):
    """Result of list_integration_associations."""

    model_config = ConfigDict(frozen=True)

    integration_association_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListLambdaFunctionsResult(BaseModel):
    """Result of list_lambda_functions."""

    model_config = ConfigDict(frozen=True)

    lambda_functions: list[str] | None = None
    next_token: str | None = None


class ListLexBotsResult(BaseModel):
    """Result of list_lex_bots."""

    model_config = ConfigDict(frozen=True)

    lex_bots: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPhoneNumbersResult(BaseModel):
    """Result of list_phone_numbers."""

    model_config = ConfigDict(frozen=True)

    phone_number_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPhoneNumbersV2Result(BaseModel):
    """Result of list_phone_numbers_v2."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    list_phone_numbers_summary_list: list[dict[str, Any]] | None = None


class ListPredefinedAttributesResult(BaseModel):
    """Result of list_predefined_attributes."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    predefined_attribute_summary_list: list[dict[str, Any]] | None = None


class ListPromptsResult(BaseModel):
    """Result of list_prompts."""

    model_config = ConfigDict(frozen=True)

    prompt_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListQueueQuickConnectsResult(BaseModel):
    """Result of list_queue_quick_connects."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    quick_connect_summary_list: list[dict[str, Any]] | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class ListQuickConnectsResult(BaseModel):
    """Result of list_quick_connects."""

    model_config = ConfigDict(frozen=True)

    quick_connect_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRealtimeContactAnalysisSegmentsV2Result(BaseModel):
    """Result of list_realtime_contact_analysis_segments_v2."""

    model_config = ConfigDict(frozen=True)

    channel: str | None = None
    status: str | None = None
    segments: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListRoutingProfileManualAssignmentQueuesResult(BaseModel):
    """Result of list_routing_profile_manual_assignment_queues."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    routing_profile_manual_assignment_queue_config_summary_list: list[dict[str, Any]] | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class ListRoutingProfileQueuesResult(BaseModel):
    """Result of list_routing_profile_queues."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    routing_profile_queue_config_summary_list: list[dict[str, Any]] | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class ListRulesResult(BaseModel):
    """Result of list_rules."""

    model_config = ConfigDict(frozen=True)

    rule_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSecurityKeysResult(BaseModel):
    """Result of list_security_keys."""

    model_config = ConfigDict(frozen=True)

    security_keys: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListSecurityProfileApplicationsResult(BaseModel):
    """Result of list_security_profile_applications."""

    model_config = ConfigDict(frozen=True)

    applications: list[dict[str, Any]] | None = None
    next_token: str | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class ListSecurityProfilePermissionsResult(BaseModel):
    """Result of list_security_profile_permissions."""

    model_config = ConfigDict(frozen=True)

    permissions: list[str] | None = None
    next_token: str | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class ListSecurityProfilesResult(BaseModel):
    """Result of list_security_profiles."""

    model_config = ConfigDict(frozen=True)

    security_profile_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListTaskTemplatesResult(BaseModel):
    """Result of list_task_templates."""

    model_config = ConfigDict(frozen=True)

    task_templates: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTrafficDistributionGroupUsersResult(BaseModel):
    """Result of list_traffic_distribution_group_users."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    traffic_distribution_group_user_summary_list: list[dict[str, Any]] | None = None


class ListTrafficDistributionGroupsResult(BaseModel):
    """Result of list_traffic_distribution_groups."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    traffic_distribution_group_summary_list: list[dict[str, Any]] | None = None


class ListUseCasesResult(BaseModel):
    """Result of list_use_cases."""

    model_config = ConfigDict(frozen=True)

    use_case_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListUserHierarchyGroupsResult(BaseModel):
    """Result of list_user_hierarchy_groups."""

    model_config = ConfigDict(frozen=True)

    user_hierarchy_group_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListUserProficienciesResult(BaseModel):
    """Result of list_user_proficiencies."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    user_proficiency_list: list[dict[str, Any]] | None = None
    last_modified_time: str | None = None
    last_modified_region: str | None = None


class ListViewVersionsResult(BaseModel):
    """Result of list_view_versions."""

    model_config = ConfigDict(frozen=True)

    view_version_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListViewsResult(BaseModel):
    """Result of list_views."""

    model_config = ConfigDict(frozen=True)

    views_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class MonitorContactResult(BaseModel):
    """Result of monitor_contact."""

    model_config = ConfigDict(frozen=True)

    contact_id: str | None = None
    contact_arn: str | None = None


class ReplicateInstanceResult(BaseModel):
    """Result of replicate_instance."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    arn: str | None = None


class SearchAgentStatusesResult(BaseModel):
    """Result of search_agent_statuses."""

    model_config = ConfigDict(frozen=True)

    agent_statuses: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchAvailablePhoneNumbersResult(BaseModel):
    """Result of search_available_phone_numbers."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    available_numbers_list: list[dict[str, Any]] | None = None


class SearchContactEvaluationsResult(BaseModel):
    """Result of search_contact_evaluations."""

    model_config = ConfigDict(frozen=True)

    evaluation_search_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchContactFlowModulesResult(BaseModel):
    """Result of search_contact_flow_modules."""

    model_config = ConfigDict(frozen=True)

    contact_flow_modules: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchContactFlowsResult(BaseModel):
    """Result of search_contact_flows."""

    model_config = ConfigDict(frozen=True)

    contact_flows: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchContactsResult(BaseModel):
    """Result of search_contacts."""

    model_config = ConfigDict(frozen=True)

    contacts: list[dict[str, Any]] | None = None
    next_token: str | None = None
    total_count: int | None = None


class SearchEmailAddressesResult(BaseModel):
    """Result of search_email_addresses."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    email_addresses: list[dict[str, Any]] | None = None
    approximate_total_count: int | None = None


class SearchEvaluationFormsResult(BaseModel):
    """Result of search_evaluation_forms."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_search_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchHoursOfOperationOverridesResult(BaseModel):
    """Result of search_hours_of_operation_overrides."""

    model_config = ConfigDict(frozen=True)

    hours_of_operation_overrides: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchHoursOfOperationsResult(BaseModel):
    """Result of search_hours_of_operations."""

    model_config = ConfigDict(frozen=True)

    hours_of_operations: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchPredefinedAttributesResult(BaseModel):
    """Result of search_predefined_attributes."""

    model_config = ConfigDict(frozen=True)

    predefined_attributes: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchPromptsResult(BaseModel):
    """Result of search_prompts."""

    model_config = ConfigDict(frozen=True)

    prompts: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchQueuesResult(BaseModel):
    """Result of search_queues."""

    model_config = ConfigDict(frozen=True)

    queues: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchQuickConnectsResult(BaseModel):
    """Result of search_quick_connects."""

    model_config = ConfigDict(frozen=True)

    quick_connects: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchResourceTagsResult(BaseModel):
    """Result of search_resource_tags."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class SearchRoutingProfilesResult(BaseModel):
    """Result of search_routing_profiles."""

    model_config = ConfigDict(frozen=True)

    routing_profiles: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchSecurityProfilesResult(BaseModel):
    """Result of search_security_profiles."""

    model_config = ConfigDict(frozen=True)

    security_profiles: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchUserHierarchyGroupsResult(BaseModel):
    """Result of search_user_hierarchy_groups."""

    model_config = ConfigDict(frozen=True)

    user_hierarchy_groups: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchUsersResult(BaseModel):
    """Result of search_users."""

    model_config = ConfigDict(frozen=True)

    users: list[dict[str, Any]] | None = None
    next_token: str | None = None
    approximate_total_count: int | None = None


class SearchVocabulariesResult(BaseModel):
    """Result of search_vocabularies."""

    model_config = ConfigDict(frozen=True)

    vocabulary_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class SendChatIntegrationEventResult(BaseModel):
    """Result of send_chat_integration_event."""

    model_config = ConfigDict(frozen=True)

    initial_contact_id: str | None = None
    new_chat_created: bool | None = None


class StartAttachedFileUploadResult(BaseModel):
    """Result of start_attached_file_upload."""

    model_config = ConfigDict(frozen=True)

    file_arn: str | None = None
    file_id: str | None = None
    creation_time: str | None = None
    file_status: str | None = None
    created_by: dict[str, Any] | None = None
    upload_url_metadata: dict[str, Any] | None = None


class StartContactEvaluationResult(BaseModel):
    """Result of start_contact_evaluation."""

    model_config = ConfigDict(frozen=True)

    evaluation_id: str | None = None
    evaluation_arn: str | None = None


class StartContactStreamingResult(BaseModel):
    """Result of start_contact_streaming."""

    model_config = ConfigDict(frozen=True)

    streaming_id: str | None = None


class StartEmailContactResult(BaseModel):
    """Result of start_email_contact."""

    model_config = ConfigDict(frozen=True)

    contact_id: str | None = None


class StartOutboundChatContactResult(BaseModel):
    """Result of start_outbound_chat_contact."""

    model_config = ConfigDict(frozen=True)

    contact_id: str | None = None


class StartOutboundEmailContactResult(BaseModel):
    """Result of start_outbound_email_contact."""

    model_config = ConfigDict(frozen=True)

    contact_id: str | None = None


class StartWebRtcContactResult(BaseModel):
    """Result of start_web_rtc_contact."""

    model_config = ConfigDict(frozen=True)

    connection_data: dict[str, Any] | None = None
    contact_id: str | None = None
    participant_id: str | None = None
    participant_token: str | None = None


class SubmitContactEvaluationResult(BaseModel):
    """Result of submit_contact_evaluation."""

    model_config = ConfigDict(frozen=True)

    evaluation_id: str | None = None
    evaluation_arn: str | None = None


class TransferContactResult(BaseModel):
    """Result of transfer_contact."""

    model_config = ConfigDict(frozen=True)

    contact_id: str | None = None
    contact_arn: str | None = None


class UpdateContactEvaluationResult(BaseModel):
    """Result of update_contact_evaluation."""

    model_config = ConfigDict(frozen=True)

    evaluation_id: str | None = None
    evaluation_arn: str | None = None


class UpdateEmailAddressMetadataResult(BaseModel):
    """Result of update_email_address_metadata."""

    model_config = ConfigDict(frozen=True)

    email_address_id: str | None = None
    email_address_arn: str | None = None


class UpdateEvaluationFormResult(BaseModel):
    """Result of update_evaluation_form."""

    model_config = ConfigDict(frozen=True)

    evaluation_form_id: str | None = None
    evaluation_form_arn: str | None = None
    evaluation_form_version: int | None = None


class UpdatePhoneNumberResult(BaseModel):
    """Result of update_phone_number."""

    model_config = ConfigDict(frozen=True)

    phone_number_id: str | None = None
    phone_number_arn: str | None = None


class UpdatePromptResult(BaseModel):
    """Result of update_prompt."""

    model_config = ConfigDict(frozen=True)

    prompt_arn: str | None = None
    prompt_id: str | None = None


class UpdateTaskTemplateResult(BaseModel):
    """Result of update_task_template."""

    model_config = ConfigDict(frozen=True)

    instance_id: str | None = None
    id: str | None = None
    arn: str | None = None
    name: str | None = None
    description: str | None = None
    contact_flow_id: str | None = None
    self_assign_flow_id: str | None = None
    constraints: dict[str, Any] | None = None
    defaults: dict[str, Any] | None = None
    fields: list[dict[str, Any]] | None = None
    status: str | None = None
    last_modified_time: str | None = None
    created_time: str | None = None


class UpdateViewContentResult(BaseModel):
    """Result of update_view_content."""

    model_config = ConfigDict(frozen=True)

    view: dict[str, Any] | None = None


def activate_evaluation_form(
    instance_id: str,
    evaluation_form_id: str,
    evaluation_form_version: int,
    region_name: str | None = None,
) -> ActivateEvaluationFormResult:
    """Activate evaluation form.

    Args:
        instance_id: Instance id.
        evaluation_form_id: Evaluation form id.
        evaluation_form_version: Evaluation form version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    kwargs["EvaluationFormVersion"] = evaluation_form_version
    try:
        resp = client.activate_evaluation_form(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to activate evaluation form") from exc
    return ActivateEvaluationFormResult(
        evaluation_form_id=resp.get("EvaluationFormId"),
        evaluation_form_arn=resp.get("EvaluationFormArn"),
        evaluation_form_version=resp.get("EvaluationFormVersion"),
    )


def associate_analytics_data_set(
    instance_id: str,
    data_set_id: str,
    *,
    target_account_id: str | None = None,
    region_name: str | None = None,
) -> AssociateAnalyticsDataSetResult:
    """Associate analytics data set.

    Args:
        instance_id: Instance id.
        data_set_id: Data set id.
        target_account_id: Target account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["DataSetId"] = data_set_id
    if target_account_id is not None:
        kwargs["TargetAccountId"] = target_account_id
    try:
        resp = client.associate_analytics_data_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate analytics data set") from exc
    return AssociateAnalyticsDataSetResult(
        data_set_id=resp.get("DataSetId"),
        target_account_id=resp.get("TargetAccountId"),
        resource_share_id=resp.get("ResourceShareId"),
        resource_share_arn=resp.get("ResourceShareArn"),
    )


def associate_approved_origin(
    instance_id: str,
    origin: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate approved origin.

    Args:
        instance_id: Instance id.
        origin: Origin.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Origin"] = origin
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.associate_approved_origin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate approved origin") from exc
    return None


def associate_bot(
    instance_id: str,
    *,
    lex_bot: dict[str, Any] | None = None,
    lex_v2_bot: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate bot.

    Args:
        instance_id: Instance id.
        lex_bot: Lex bot.
        lex_v2_bot: Lex v2 bot.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if lex_bot is not None:
        kwargs["LexBot"] = lex_bot
    if lex_v2_bot is not None:
        kwargs["LexV2Bot"] = lex_v2_bot
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.associate_bot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate bot") from exc
    return None


def associate_contact_with_user(
    instance_id: str,
    contact_id: str,
    user_id: str,
    region_name: str | None = None,
) -> None:
    """Associate contact with user.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        user_id: User id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["UserId"] = user_id
    try:
        client.associate_contact_with_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate contact with user") from exc
    return None


def associate_default_vocabulary(
    instance_id: str,
    language_code: str,
    *,
    vocabulary_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate default vocabulary.

    Args:
        instance_id: Instance id.
        language_code: Language code.
        vocabulary_id: Vocabulary id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["LanguageCode"] = language_code
    if vocabulary_id is not None:
        kwargs["VocabularyId"] = vocabulary_id
    try:
        client.associate_default_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate default vocabulary") from exc
    return None


def associate_email_address_alias(
    email_address_id: str,
    instance_id: str,
    alias_configuration: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate email address alias.

    Args:
        email_address_id: Email address id.
        instance_id: Instance id.
        alias_configuration: Alias configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddressId"] = email_address_id
    kwargs["InstanceId"] = instance_id
    kwargs["AliasConfiguration"] = alias_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.associate_email_address_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate email address alias") from exc
    return None


def associate_flow(
    instance_id: str,
    resource_id: str,
    flow_id: str,
    resource_type: str,
    region_name: str | None = None,
) -> None:
    """Associate flow.

    Args:
        instance_id: Instance id.
        resource_id: Resource id.
        flow_id: Flow id.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ResourceId"] = resource_id
    kwargs["FlowId"] = flow_id
    kwargs["ResourceType"] = resource_type
    try:
        client.associate_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate flow") from exc
    return None


def associate_instance_storage_config(
    instance_id: str,
    resource_type: str,
    storage_config: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> AssociateInstanceStorageConfigResult:
    """Associate instance storage config.

    Args:
        instance_id: Instance id.
        resource_type: Resource type.
        storage_config: Storage config.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ResourceType"] = resource_type
    kwargs["StorageConfig"] = storage_config
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.associate_instance_storage_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate instance storage config") from exc
    return AssociateInstanceStorageConfigResult(
        association_id=resp.get("AssociationId"),
    )


def associate_lambda_function(
    instance_id: str,
    function_arn: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate lambda function.

    Args:
        instance_id: Instance id.
        function_arn: Function arn.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FunctionArn"] = function_arn
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.associate_lambda_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate lambda function") from exc
    return None


def associate_lex_bot(
    instance_id: str,
    lex_bot: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Associate lex bot.

    Args:
        instance_id: Instance id.
        lex_bot: Lex bot.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["LexBot"] = lex_bot
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.associate_lex_bot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate lex bot") from exc
    return None


def associate_phone_number_contact_flow(
    phone_number_id: str,
    instance_id: str,
    contact_flow_id: str,
    region_name: str | None = None,
) -> None:
    """Associate phone number contact flow.

    Args:
        phone_number_id: Phone number id.
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberId"] = phone_number_id
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    try:
        client.associate_phone_number_contact_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate phone number contact flow") from exc
    return None


def associate_queue_quick_connects(
    instance_id: str,
    queue_id: str,
    quick_connect_ids: list[str],
    region_name: str | None = None,
) -> None:
    """Associate queue quick connects.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        quick_connect_ids: Quick connect ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    kwargs["QuickConnectIds"] = quick_connect_ids
    try:
        client.associate_queue_quick_connects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate queue quick connects") from exc
    return None


def associate_routing_profile_queues(
    instance_id: str,
    routing_profile_id: str,
    *,
    queue_configs: list[dict[str, Any]] | None = None,
    manual_assignment_queue_configs: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Associate routing profile queues.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        queue_configs: Queue configs.
        manual_assignment_queue_configs: Manual assignment queue configs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    if queue_configs is not None:
        kwargs["QueueConfigs"] = queue_configs
    if manual_assignment_queue_configs is not None:
        kwargs["ManualAssignmentQueueConfigs"] = manual_assignment_queue_configs
    try:
        client.associate_routing_profile_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate routing profile queues") from exc
    return None


def associate_security_key(
    instance_id: str,
    key: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> AssociateSecurityKeyResult:
    """Associate security key.

    Args:
        instance_id: Instance id.
        key: Key.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Key"] = key
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.associate_security_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate security key") from exc
    return AssociateSecurityKeyResult(
        association_id=resp.get("AssociationId"),
    )


def associate_traffic_distribution_group_user(
    traffic_distribution_group_id: str,
    user_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Associate traffic distribution group user.

    Args:
        traffic_distribution_group_id: Traffic distribution group id.
        user_id: User id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrafficDistributionGroupId"] = traffic_distribution_group_id
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    try:
        client.associate_traffic_distribution_group_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate traffic distribution group user") from exc
    return None


def associate_user_proficiencies(
    instance_id: str,
    user_id: str,
    user_proficiencies: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Associate user proficiencies.

    Args:
        instance_id: Instance id.
        user_id: User id.
        user_proficiencies: User proficiencies.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["UserId"] = user_id
    kwargs["UserProficiencies"] = user_proficiencies
    try:
        client.associate_user_proficiencies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate user proficiencies") from exc
    return None


def batch_associate_analytics_data_set(
    instance_id: str,
    data_set_ids: list[str],
    *,
    target_account_id: str | None = None,
    region_name: str | None = None,
) -> BatchAssociateAnalyticsDataSetResult:
    """Batch associate analytics data set.

    Args:
        instance_id: Instance id.
        data_set_ids: Data set ids.
        target_account_id: Target account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["DataSetIds"] = data_set_ids
    if target_account_id is not None:
        kwargs["TargetAccountId"] = target_account_id
    try:
        resp = client.batch_associate_analytics_data_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch associate analytics data set") from exc
    return BatchAssociateAnalyticsDataSetResult(
        created=resp.get("Created"),
        errors=resp.get("Errors"),
    )


def batch_disassociate_analytics_data_set(
    instance_id: str,
    data_set_ids: list[str],
    *,
    target_account_id: str | None = None,
    region_name: str | None = None,
) -> BatchDisassociateAnalyticsDataSetResult:
    """Batch disassociate analytics data set.

    Args:
        instance_id: Instance id.
        data_set_ids: Data set ids.
        target_account_id: Target account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["DataSetIds"] = data_set_ids
    if target_account_id is not None:
        kwargs["TargetAccountId"] = target_account_id
    try:
        resp = client.batch_disassociate_analytics_data_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch disassociate analytics data set") from exc
    return BatchDisassociateAnalyticsDataSetResult(
        deleted=resp.get("Deleted"),
        errors=resp.get("Errors"),
    )


def batch_get_attached_file_metadata(
    file_ids: list[str],
    instance_id: str,
    associated_resource_arn: str,
    region_name: str | None = None,
) -> BatchGetAttachedFileMetadataResult:
    """Batch get attached file metadata.

    Args:
        file_ids: File ids.
        instance_id: Instance id.
        associated_resource_arn: Associated resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FileIds"] = file_ids
    kwargs["InstanceId"] = instance_id
    kwargs["AssociatedResourceArn"] = associated_resource_arn
    try:
        resp = client.batch_get_attached_file_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get attached file metadata") from exc
    return BatchGetAttachedFileMetadataResult(
        files=resp.get("Files"),
        errors=resp.get("Errors"),
    )


def batch_get_flow_association(
    instance_id: str,
    resource_ids: list[str],
    *,
    resource_type: str | None = None,
    region_name: str | None = None,
) -> BatchGetFlowAssociationResult:
    """Batch get flow association.

    Args:
        instance_id: Instance id.
        resource_ids: Resource ids.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ResourceIds"] = resource_ids
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    try:
        resp = client.batch_get_flow_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get flow association") from exc
    return BatchGetFlowAssociationResult(
        flow_association_summary_list=resp.get("FlowAssociationSummaryList"),
    )


def batch_put_contact(
    instance_id: str,
    contact_data_request_list: list[dict[str, Any]],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> BatchPutContactResult:
    """Batch put contact.

    Args:
        instance_id: Instance id.
        contact_data_request_list: Contact data request list.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactDataRequestList"] = contact_data_request_list
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.batch_put_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch put contact") from exc
    return BatchPutContactResult(
        successful_request_list=resp.get("SuccessfulRequestList"),
        failed_request_list=resp.get("FailedRequestList"),
    )


def claim_phone_number(
    phone_number: str,
    *,
    target_arn: str | None = None,
    instance_id: str | None = None,
    phone_number_description: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> ClaimPhoneNumberResult:
    """Claim phone number.

    Args:
        phone_number: Phone number.
        target_arn: Target arn.
        instance_id: Instance id.
        phone_number_description: Phone number description.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumber"] = phone_number
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if phone_number_description is not None:
        kwargs["PhoneNumberDescription"] = phone_number_description
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.claim_phone_number(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to claim phone number") from exc
    return ClaimPhoneNumberResult(
        phone_number_id=resp.get("PhoneNumberId"),
        phone_number_arn=resp.get("PhoneNumberArn"),
    )


def complete_attached_file_upload(
    instance_id: str,
    file_id: str,
    associated_resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Complete attached file upload.

    Args:
        instance_id: Instance id.
        file_id: File id.
        associated_resource_arn: Associated resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FileId"] = file_id
    kwargs["AssociatedResourceArn"] = associated_resource_arn
    try:
        client.complete_attached_file_upload(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to complete attached file upload") from exc
    return None


def create_agent_status(
    instance_id: str,
    name: str,
    state: str,
    *,
    description: str | None = None,
    display_order: int | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateAgentStatusResult:
    """Create agent status.

    Args:
        instance_id: Instance id.
        name: Name.
        state: State.
        description: Description.
        display_order: Display order.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["State"] = state
    if description is not None:
        kwargs["Description"] = description
    if display_order is not None:
        kwargs["DisplayOrder"] = display_order
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_agent_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create agent status") from exc
    return CreateAgentStatusResult(
        agent_status_arn=resp.get("AgentStatusARN"),
        agent_status_id=resp.get("AgentStatusId"),
    )


def create_contact(
    instance_id: str,
    channel: str,
    initiation_method: str,
    *,
    client_token: str | None = None,
    related_contact_id: str | None = None,
    attributes: dict[str, Any] | None = None,
    references: dict[str, Any] | None = None,
    expiry_duration_in_minutes: int | None = None,
    user_info: dict[str, Any] | None = None,
    initiate_as: str | None = None,
    name: str | None = None,
    description: str | None = None,
    segment_attributes: dict[str, Any] | None = None,
    previous_contact_id: str | None = None,
    region_name: str | None = None,
) -> CreateContactResult:
    """Create contact.

    Args:
        instance_id: Instance id.
        channel: Channel.
        initiation_method: Initiation method.
        client_token: Client token.
        related_contact_id: Related contact id.
        attributes: Attributes.
        references: References.
        expiry_duration_in_minutes: Expiry duration in minutes.
        user_info: User info.
        initiate_as: Initiate as.
        name: Name.
        description: Description.
        segment_attributes: Segment attributes.
        previous_contact_id: Previous contact id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Channel"] = channel
    kwargs["InitiationMethod"] = initiation_method
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if related_contact_id is not None:
        kwargs["RelatedContactId"] = related_contact_id
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if references is not None:
        kwargs["References"] = references
    if expiry_duration_in_minutes is not None:
        kwargs["ExpiryDurationInMinutes"] = expiry_duration_in_minutes
    if user_info is not None:
        kwargs["UserInfo"] = user_info
    if initiate_as is not None:
        kwargs["InitiateAs"] = initiate_as
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if segment_attributes is not None:
        kwargs["SegmentAttributes"] = segment_attributes
    if previous_contact_id is not None:
        kwargs["PreviousContactId"] = previous_contact_id
    try:
        resp = client.create_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create contact") from exc
    return CreateContactResult(
        contact_id=resp.get("ContactId"),
        contact_arn=resp.get("ContactArn"),
    )


def create_contact_flow_module(
    instance_id: str,
    name: str,
    content: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateContactFlowModuleResult:
    """Create contact flow module.

    Args:
        instance_id: Instance id.
        name: Name.
        content: Content.
        description: Description.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["Content"] = content
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_contact_flow_module(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create contact flow module") from exc
    return CreateContactFlowModuleResult(
        id=resp.get("Id"),
        arn=resp.get("Arn"),
    )


def create_contact_flow_version(
    instance_id: str,
    contact_flow_id: str,
    *,
    description: str | None = None,
    flow_content_sha256: str | None = None,
    contact_flow_version: int | None = None,
    last_modified_time: str | None = None,
    last_modified_region: str | None = None,
    region_name: str | None = None,
) -> CreateContactFlowVersionResult:
    """Create contact flow version.

    Args:
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        description: Description.
        flow_content_sha256: Flow content sha256.
        contact_flow_version: Contact flow version.
        last_modified_time: Last modified time.
        last_modified_region: Last modified region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    if description is not None:
        kwargs["Description"] = description
    if flow_content_sha256 is not None:
        kwargs["FlowContentSha256"] = flow_content_sha256
    if contact_flow_version is not None:
        kwargs["ContactFlowVersion"] = contact_flow_version
    if last_modified_time is not None:
        kwargs["LastModifiedTime"] = last_modified_time
    if last_modified_region is not None:
        kwargs["LastModifiedRegion"] = last_modified_region
    try:
        resp = client.create_contact_flow_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create contact flow version") from exc
    return CreateContactFlowVersionResult(
        contact_flow_arn=resp.get("ContactFlowArn"),
        version=resp.get("Version"),
    )


def create_email_address(
    instance_id: str,
    email_address: str,
    *,
    description: str | None = None,
    display_name: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateEmailAddressResult:
    """Create email address.

    Args:
        instance_id: Instance id.
        email_address: Email address.
        description: Description.
        display_name: Display name.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EmailAddress"] = email_address
    if description is not None:
        kwargs["Description"] = description
    if display_name is not None:
        kwargs["DisplayName"] = display_name
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_email_address(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create email address") from exc
    return CreateEmailAddressResult(
        email_address_id=resp.get("EmailAddressId"),
        email_address_arn=resp.get("EmailAddressArn"),
    )


def create_evaluation_form(
    instance_id: str,
    title: str,
    items: list[dict[str, Any]],
    *,
    description: str | None = None,
    scoring_strategy: dict[str, Any] | None = None,
    auto_evaluation_configuration: dict[str, Any] | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateEvaluationFormResult:
    """Create evaluation form.

    Args:
        instance_id: Instance id.
        title: Title.
        items: Items.
        description: Description.
        scoring_strategy: Scoring strategy.
        auto_evaluation_configuration: Auto evaluation configuration.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Title"] = title
    kwargs["Items"] = items
    if description is not None:
        kwargs["Description"] = description
    if scoring_strategy is not None:
        kwargs["ScoringStrategy"] = scoring_strategy
    if auto_evaluation_configuration is not None:
        kwargs["AutoEvaluationConfiguration"] = auto_evaluation_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_evaluation_form(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create evaluation form") from exc
    return CreateEvaluationFormResult(
        evaluation_form_id=resp.get("EvaluationFormId"),
        evaluation_form_arn=resp.get("EvaluationFormArn"),
    )


def create_hours_of_operation(
    instance_id: str,
    name: str,
    time_zone: str,
    config: list[dict[str, Any]],
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateHoursOfOperationResult:
    """Create hours of operation.

    Args:
        instance_id: Instance id.
        name: Name.
        time_zone: Time zone.
        config: Config.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["TimeZone"] = time_zone
    kwargs["Config"] = config
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_hours_of_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create hours of operation") from exc
    return CreateHoursOfOperationResult(
        hours_of_operation_id=resp.get("HoursOfOperationId"),
        hours_of_operation_arn=resp.get("HoursOfOperationArn"),
    )


def create_hours_of_operation_override(
    instance_id: str,
    hours_of_operation_id: str,
    name: str,
    config: list[dict[str, Any]],
    effective_from: str,
    effective_till: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> CreateHoursOfOperationOverrideResult:
    """Create hours of operation override.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        name: Name.
        config: Config.
        effective_from: Effective from.
        effective_till: Effective till.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    kwargs["Name"] = name
    kwargs["Config"] = config
    kwargs["EffectiveFrom"] = effective_from
    kwargs["EffectiveTill"] = effective_till
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.create_hours_of_operation_override(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create hours of operation override") from exc
    return CreateHoursOfOperationOverrideResult(
        hours_of_operation_override_id=resp.get("HoursOfOperationOverrideId"),
    )


def create_integration_association(
    instance_id: str,
    integration_type: str,
    integration_arn: str,
    *,
    source_application_url: str | None = None,
    source_application_name: str | None = None,
    source_type: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateIntegrationAssociationResult:
    """Create integration association.

    Args:
        instance_id: Instance id.
        integration_type: Integration type.
        integration_arn: Integration arn.
        source_application_url: Source application url.
        source_application_name: Source application name.
        source_type: Source type.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["IntegrationType"] = integration_type
    kwargs["IntegrationArn"] = integration_arn
    if source_application_url is not None:
        kwargs["SourceApplicationUrl"] = source_application_url
    if source_application_name is not None:
        kwargs["SourceApplicationName"] = source_application_name
    if source_type is not None:
        kwargs["SourceType"] = source_type
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_integration_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create integration association") from exc
    return CreateIntegrationAssociationResult(
        integration_association_id=resp.get("IntegrationAssociationId"),
        integration_association_arn=resp.get("IntegrationAssociationArn"),
    )


def create_participant(
    instance_id: str,
    contact_id: str,
    participant_details: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateParticipantResult:
    """Create participant.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        participant_details: Participant details.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["ParticipantDetails"] = participant_details
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_participant(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create participant") from exc
    return CreateParticipantResult(
        participant_credentials=resp.get("ParticipantCredentials"),
        participant_id=resp.get("ParticipantId"),
    )


def create_persistent_contact_association(
    instance_id: str,
    initial_contact_id: str,
    rehydration_type: str,
    source_contact_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreatePersistentContactAssociationResult:
    """Create persistent contact association.

    Args:
        instance_id: Instance id.
        initial_contact_id: Initial contact id.
        rehydration_type: Rehydration type.
        source_contact_id: Source contact id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["InitialContactId"] = initial_contact_id
    kwargs["RehydrationType"] = rehydration_type
    kwargs["SourceContactId"] = source_contact_id
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_persistent_contact_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create persistent contact association") from exc
    return CreatePersistentContactAssociationResult(
        continued_from_contact_id=resp.get("ContinuedFromContactId"),
    )


def create_predefined_attribute(
    instance_id: str,
    name: str,
    *,
    values: dict[str, Any] | None = None,
    purposes: list[str] | None = None,
    attribute_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create predefined attribute.

    Args:
        instance_id: Instance id.
        name: Name.
        values: Values.
        purposes: Purposes.
        attribute_configuration: Attribute configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    if values is not None:
        kwargs["Values"] = values
    if purposes is not None:
        kwargs["Purposes"] = purposes
    if attribute_configuration is not None:
        kwargs["AttributeConfiguration"] = attribute_configuration
    try:
        client.create_predefined_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create predefined attribute") from exc
    return None


def create_prompt(
    instance_id: str,
    name: str,
    s3_uri: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreatePromptResult:
    """Create prompt.

    Args:
        instance_id: Instance id.
        name: Name.
        s3_uri: S3 uri.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["S3Uri"] = s3_uri
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create prompt") from exc
    return CreatePromptResult(
        prompt_arn=resp.get("PromptARN"),
        prompt_id=resp.get("PromptId"),
    )


def create_push_notification_registration(
    instance_id: str,
    pinpoint_app_arn: str,
    device_token: str,
    device_type: str,
    contact_configuration: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreatePushNotificationRegistrationResult:
    """Create push notification registration.

    Args:
        instance_id: Instance id.
        pinpoint_app_arn: Pinpoint app arn.
        device_token: Device token.
        device_type: Device type.
        contact_configuration: Contact configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["PinpointAppArn"] = pinpoint_app_arn
    kwargs["DeviceToken"] = device_token
    kwargs["DeviceType"] = device_type
    kwargs["ContactConfiguration"] = contact_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_push_notification_registration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create push notification registration") from exc
    return CreatePushNotificationRegistrationResult(
        registration_id=resp.get("RegistrationId"),
    )


def create_quick_connect(
    instance_id: str,
    name: str,
    quick_connect_config: dict[str, Any],
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateQuickConnectResult:
    """Create quick connect.

    Args:
        instance_id: Instance id.
        name: Name.
        quick_connect_config: Quick connect config.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["QuickConnectConfig"] = quick_connect_config
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_quick_connect(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create quick connect") from exc
    return CreateQuickConnectResult(
        quick_connect_arn=resp.get("QuickConnectARN"),
        quick_connect_id=resp.get("QuickConnectId"),
    )


def create_rule(
    instance_id: str,
    name: str,
    trigger_event_source: dict[str, Any],
    function: str,
    actions: list[dict[str, Any]],
    publish_status: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateRuleResult:
    """Create rule.

    Args:
        instance_id: Instance id.
        name: Name.
        trigger_event_source: Trigger event source.
        function: Function.
        actions: Actions.
        publish_status: Publish status.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["TriggerEventSource"] = trigger_event_source
    kwargs["Function"] = function
    kwargs["Actions"] = actions
    kwargs["PublishStatus"] = publish_status
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create rule") from exc
    return CreateRuleResult(
        rule_arn=resp.get("RuleArn"),
        rule_id=resp.get("RuleId"),
    )


def create_security_profile(
    security_profile_name: str,
    instance_id: str,
    *,
    description: str | None = None,
    permissions: list[str] | None = None,
    tags: dict[str, Any] | None = None,
    allowed_access_control_tags: dict[str, Any] | None = None,
    tag_restricted_resources: list[str] | None = None,
    applications: list[dict[str, Any]] | None = None,
    hierarchy_restricted_resources: list[str] | None = None,
    allowed_access_control_hierarchy_group_id: str | None = None,
    region_name: str | None = None,
) -> CreateSecurityProfileResult:
    """Create security profile.

    Args:
        security_profile_name: Security profile name.
        instance_id: Instance id.
        description: Description.
        permissions: Permissions.
        tags: Tags.
        allowed_access_control_tags: Allowed access control tags.
        tag_restricted_resources: Tag restricted resources.
        applications: Applications.
        hierarchy_restricted_resources: Hierarchy restricted resources.
        allowed_access_control_hierarchy_group_id: Allowed access control hierarchy group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityProfileName"] = security_profile_name
    kwargs["InstanceId"] = instance_id
    if description is not None:
        kwargs["Description"] = description
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if tags is not None:
        kwargs["Tags"] = tags
    if allowed_access_control_tags is not None:
        kwargs["AllowedAccessControlTags"] = allowed_access_control_tags
    if tag_restricted_resources is not None:
        kwargs["TagRestrictedResources"] = tag_restricted_resources
    if applications is not None:
        kwargs["Applications"] = applications
    if hierarchy_restricted_resources is not None:
        kwargs["HierarchyRestrictedResources"] = hierarchy_restricted_resources
    if allowed_access_control_hierarchy_group_id is not None:
        kwargs["AllowedAccessControlHierarchyGroupId"] = allowed_access_control_hierarchy_group_id
    try:
        resp = client.create_security_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create security profile") from exc
    return CreateSecurityProfileResult(
        security_profile_id=resp.get("SecurityProfileId"),
        security_profile_arn=resp.get("SecurityProfileArn"),
    )


def create_task_template(
    instance_id: str,
    name: str,
    fields: list[dict[str, Any]],
    *,
    description: str | None = None,
    contact_flow_id: str | None = None,
    self_assign_flow_id: str | None = None,
    constraints: dict[str, Any] | None = None,
    defaults: dict[str, Any] | None = None,
    status: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateTaskTemplateResult:
    """Create task template.

    Args:
        instance_id: Instance id.
        name: Name.
        fields: Fields.
        description: Description.
        contact_flow_id: Contact flow id.
        self_assign_flow_id: Self assign flow id.
        constraints: Constraints.
        defaults: Defaults.
        status: Status.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["Fields"] = fields
    if description is not None:
        kwargs["Description"] = description
    if contact_flow_id is not None:
        kwargs["ContactFlowId"] = contact_flow_id
    if self_assign_flow_id is not None:
        kwargs["SelfAssignFlowId"] = self_assign_flow_id
    if constraints is not None:
        kwargs["Constraints"] = constraints
    if defaults is not None:
        kwargs["Defaults"] = defaults
    if status is not None:
        kwargs["Status"] = status
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_task_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create task template") from exc
    return CreateTaskTemplateResult(
        id=resp.get("Id"),
        arn=resp.get("Arn"),
    )


def create_traffic_distribution_group(
    name: str,
    instance_id: str,
    *,
    description: str | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateTrafficDistributionGroupResult:
    """Create traffic distribution group.

    Args:
        name: Name.
        instance_id: Instance id.
        description: Description.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["InstanceId"] = instance_id
    if description is not None:
        kwargs["Description"] = description
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_traffic_distribution_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create traffic distribution group") from exc
    return CreateTrafficDistributionGroupResult(
        id=resp.get("Id"),
        arn=resp.get("Arn"),
    )


def create_use_case(
    instance_id: str,
    integration_association_id: str,
    use_case_type: str,
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUseCaseResult:
    """Create use case.

    Args:
        instance_id: Instance id.
        integration_association_id: Integration association id.
        use_case_type: Use case type.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["IntegrationAssociationId"] = integration_association_id
    kwargs["UseCaseType"] = use_case_type
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_use_case(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create use case") from exc
    return CreateUseCaseResult(
        use_case_id=resp.get("UseCaseId"),
        use_case_arn=resp.get("UseCaseArn"),
    )


def create_user_hierarchy_group(
    name: str,
    instance_id: str,
    *,
    parent_group_id: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateUserHierarchyGroupResult:
    """Create user hierarchy group.

    Args:
        name: Name.
        instance_id: Instance id.
        parent_group_id: Parent group id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["InstanceId"] = instance_id
    if parent_group_id is not None:
        kwargs["ParentGroupId"] = parent_group_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_user_hierarchy_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create user hierarchy group") from exc
    return CreateUserHierarchyGroupResult(
        hierarchy_group_id=resp.get("HierarchyGroupId"),
        hierarchy_group_arn=resp.get("HierarchyGroupArn"),
    )


def create_view(
    instance_id: str,
    status: str,
    content: dict[str, Any],
    name: str,
    *,
    client_token: str | None = None,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateViewResult:
    """Create view.

    Args:
        instance_id: Instance id.
        status: Status.
        content: Content.
        name: Name.
        client_token: Client token.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Status"] = status
    kwargs["Content"] = content
    kwargs["Name"] = name
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_view(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create view") from exc
    return CreateViewResult(
        view=resp.get("View"),
    )


def create_view_version(
    instance_id: str,
    view_id: str,
    *,
    version_description: str | None = None,
    view_content_sha256: str | None = None,
    region_name: str | None = None,
) -> CreateViewVersionResult:
    """Create view version.

    Args:
        instance_id: Instance id.
        view_id: View id.
        version_description: Version description.
        view_content_sha256: View content sha256.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    if version_description is not None:
        kwargs["VersionDescription"] = version_description
    if view_content_sha256 is not None:
        kwargs["ViewContentSha256"] = view_content_sha256
    try:
        resp = client.create_view_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create view version") from exc
    return CreateViewVersionResult(
        view=resp.get("View"),
    )


def create_vocabulary(
    instance_id: str,
    vocabulary_name: str,
    language_code: str,
    content: str,
    *,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateVocabularyResult:
    """Create vocabulary.

    Args:
        instance_id: Instance id.
        vocabulary_name: Vocabulary name.
        language_code: Language code.
        content: Content.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["VocabularyName"] = vocabulary_name
    kwargs["LanguageCode"] = language_code
    kwargs["Content"] = content
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create vocabulary") from exc
    return CreateVocabularyResult(
        vocabulary_arn=resp.get("VocabularyArn"),
        vocabulary_id=resp.get("VocabularyId"),
        state=resp.get("State"),
    )


def deactivate_evaluation_form(
    instance_id: str,
    evaluation_form_id: str,
    evaluation_form_version: int,
    region_name: str | None = None,
) -> DeactivateEvaluationFormResult:
    """Deactivate evaluation form.

    Args:
        instance_id: Instance id.
        evaluation_form_id: Evaluation form id.
        evaluation_form_version: Evaluation form version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    kwargs["EvaluationFormVersion"] = evaluation_form_version
    try:
        resp = client.deactivate_evaluation_form(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deactivate evaluation form") from exc
    return DeactivateEvaluationFormResult(
        evaluation_form_id=resp.get("EvaluationFormId"),
        evaluation_form_arn=resp.get("EvaluationFormArn"),
        evaluation_form_version=resp.get("EvaluationFormVersion"),
    )


def delete_attached_file(
    instance_id: str,
    file_id: str,
    associated_resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete attached file.

    Args:
        instance_id: Instance id.
        file_id: File id.
        associated_resource_arn: Associated resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FileId"] = file_id
    kwargs["AssociatedResourceArn"] = associated_resource_arn
    try:
        client.delete_attached_file(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete attached file") from exc
    return None


def delete_contact_evaluation(
    instance_id: str,
    evaluation_id: str,
    region_name: str | None = None,
) -> None:
    """Delete contact evaluation.

    Args:
        instance_id: Instance id.
        evaluation_id: Evaluation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationId"] = evaluation_id
    try:
        client.delete_contact_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete contact evaluation") from exc
    return None


def delete_contact_flow(
    instance_id: str,
    contact_flow_id: str,
    region_name: str | None = None,
) -> None:
    """Delete contact flow.

    Args:
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    try:
        client.delete_contact_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete contact flow") from exc
    return None


def delete_contact_flow_module(
    instance_id: str,
    contact_flow_module_id: str,
    region_name: str | None = None,
) -> None:
    """Delete contact flow module.

    Args:
        instance_id: Instance id.
        contact_flow_module_id: Contact flow module id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowModuleId"] = contact_flow_module_id
    try:
        client.delete_contact_flow_module(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete contact flow module") from exc
    return None


def delete_contact_flow_version(
    instance_id: str,
    contact_flow_id: str,
    contact_flow_version: int,
    region_name: str | None = None,
) -> None:
    """Delete contact flow version.

    Args:
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        contact_flow_version: Contact flow version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    kwargs["ContactFlowVersion"] = contact_flow_version
    try:
        client.delete_contact_flow_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete contact flow version") from exc
    return None


def delete_email_address(
    instance_id: str,
    email_address_id: str,
    region_name: str | None = None,
) -> None:
    """Delete email address.

    Args:
        instance_id: Instance id.
        email_address_id: Email address id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EmailAddressId"] = email_address_id
    try:
        client.delete_email_address(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete email address") from exc
    return None


def delete_evaluation_form(
    instance_id: str,
    evaluation_form_id: str,
    *,
    evaluation_form_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Delete evaluation form.

    Args:
        instance_id: Instance id.
        evaluation_form_id: Evaluation form id.
        evaluation_form_version: Evaluation form version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    if evaluation_form_version is not None:
        kwargs["EvaluationFormVersion"] = evaluation_form_version
    try:
        client.delete_evaluation_form(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete evaluation form") from exc
    return None


def delete_hours_of_operation(
    instance_id: str,
    hours_of_operation_id: str,
    region_name: str | None = None,
) -> None:
    """Delete hours of operation.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    try:
        client.delete_hours_of_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete hours of operation") from exc
    return None


def delete_hours_of_operation_override(
    instance_id: str,
    hours_of_operation_id: str,
    hours_of_operation_override_id: str,
    region_name: str | None = None,
) -> None:
    """Delete hours of operation override.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        hours_of_operation_override_id: Hours of operation override id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    kwargs["HoursOfOperationOverrideId"] = hours_of_operation_override_id
    try:
        client.delete_hours_of_operation_override(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete hours of operation override") from exc
    return None


def delete_integration_association(
    instance_id: str,
    integration_association_id: str,
    region_name: str | None = None,
) -> None:
    """Delete integration association.

    Args:
        instance_id: Instance id.
        integration_association_id: Integration association id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["IntegrationAssociationId"] = integration_association_id
    try:
        client.delete_integration_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete integration association") from exc
    return None


def delete_predefined_attribute(
    instance_id: str,
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete predefined attribute.

    Args:
        instance_id: Instance id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    try:
        client.delete_predefined_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete predefined attribute") from exc
    return None


def delete_prompt(
    instance_id: str,
    prompt_id: str,
    region_name: str | None = None,
) -> None:
    """Delete prompt.

    Args:
        instance_id: Instance id.
        prompt_id: Prompt id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["PromptId"] = prompt_id
    try:
        client.delete_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete prompt") from exc
    return None


def delete_push_notification_registration(
    instance_id: str,
    registration_id: str,
    contact_id: str,
    region_name: str | None = None,
) -> None:
    """Delete push notification registration.

    Args:
        instance_id: Instance id.
        registration_id: Registration id.
        contact_id: Contact id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RegistrationId"] = registration_id
    kwargs["ContactId"] = contact_id
    try:
        client.delete_push_notification_registration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete push notification registration") from exc
    return None


def delete_queue(
    instance_id: str,
    queue_id: str,
    region_name: str | None = None,
) -> None:
    """Delete queue.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    try:
        client.delete_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete queue") from exc
    return None


def delete_quick_connect(
    instance_id: str,
    quick_connect_id: str,
    region_name: str | None = None,
) -> None:
    """Delete quick connect.

    Args:
        instance_id: Instance id.
        quick_connect_id: Quick connect id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QuickConnectId"] = quick_connect_id
    try:
        client.delete_quick_connect(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete quick connect") from exc
    return None


def delete_routing_profile(
    instance_id: str,
    routing_profile_id: str,
    region_name: str | None = None,
) -> None:
    """Delete routing profile.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    try:
        client.delete_routing_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete routing profile") from exc
    return None


def delete_rule(
    instance_id: str,
    rule_id: str,
    region_name: str | None = None,
) -> None:
    """Delete rule.

    Args:
        instance_id: Instance id.
        rule_id: Rule id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RuleId"] = rule_id
    try:
        client.delete_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete rule") from exc
    return None


def delete_security_profile(
    instance_id: str,
    security_profile_id: str,
    region_name: str | None = None,
) -> None:
    """Delete security profile.

    Args:
        instance_id: Instance id.
        security_profile_id: Security profile id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["SecurityProfileId"] = security_profile_id
    try:
        client.delete_security_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete security profile") from exc
    return None


def delete_task_template(
    instance_id: str,
    task_template_id: str,
    region_name: str | None = None,
) -> None:
    """Delete task template.

    Args:
        instance_id: Instance id.
        task_template_id: Task template id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["TaskTemplateId"] = task_template_id
    try:
        client.delete_task_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete task template") from exc
    return None


def delete_traffic_distribution_group(
    traffic_distribution_group_id: str,
    region_name: str | None = None,
) -> None:
    """Delete traffic distribution group.

    Args:
        traffic_distribution_group_id: Traffic distribution group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrafficDistributionGroupId"] = traffic_distribution_group_id
    try:
        client.delete_traffic_distribution_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete traffic distribution group") from exc
    return None


def delete_use_case(
    instance_id: str,
    integration_association_id: str,
    use_case_id: str,
    region_name: str | None = None,
) -> None:
    """Delete use case.

    Args:
        instance_id: Instance id.
        integration_association_id: Integration association id.
        use_case_id: Use case id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["IntegrationAssociationId"] = integration_association_id
    kwargs["UseCaseId"] = use_case_id
    try:
        client.delete_use_case(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete use case") from exc
    return None


def delete_user_hierarchy_group(
    hierarchy_group_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Delete user hierarchy group.

    Args:
        hierarchy_group_id: Hierarchy group id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HierarchyGroupId"] = hierarchy_group_id
    kwargs["InstanceId"] = instance_id
    try:
        client.delete_user_hierarchy_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete user hierarchy group") from exc
    return None


def delete_view(
    instance_id: str,
    view_id: str,
    region_name: str | None = None,
) -> None:
    """Delete view.

    Args:
        instance_id: Instance id.
        view_id: View id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    try:
        client.delete_view(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete view") from exc
    return None


def delete_view_version(
    instance_id: str,
    view_id: str,
    view_version: int,
    region_name: str | None = None,
) -> None:
    """Delete view version.

    Args:
        instance_id: Instance id.
        view_id: View id.
        view_version: View version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    kwargs["ViewVersion"] = view_version
    try:
        client.delete_view_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete view version") from exc
    return None


def delete_vocabulary(
    instance_id: str,
    vocabulary_id: str,
    region_name: str | None = None,
) -> DeleteVocabularyResult:
    """Delete vocabulary.

    Args:
        instance_id: Instance id.
        vocabulary_id: Vocabulary id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["VocabularyId"] = vocabulary_id
    try:
        resp = client.delete_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete vocabulary") from exc
    return DeleteVocabularyResult(
        vocabulary_arn=resp.get("VocabularyArn"),
        vocabulary_id=resp.get("VocabularyId"),
        state=resp.get("State"),
    )


def describe_agent_status(
    instance_id: str,
    agent_status_id: str,
    region_name: str | None = None,
) -> DescribeAgentStatusResult:
    """Describe agent status.

    Args:
        instance_id: Instance id.
        agent_status_id: Agent status id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AgentStatusId"] = agent_status_id
    try:
        resp = client.describe_agent_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe agent status") from exc
    return DescribeAgentStatusResult(
        agent_status=resp.get("AgentStatus"),
    )


def describe_authentication_profile(
    authentication_profile_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> DescribeAuthenticationProfileResult:
    """Describe authentication profile.

    Args:
        authentication_profile_id: Authentication profile id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthenticationProfileId"] = authentication_profile_id
    kwargs["InstanceId"] = instance_id
    try:
        resp = client.describe_authentication_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe authentication profile") from exc
    return DescribeAuthenticationProfileResult(
        authentication_profile=resp.get("AuthenticationProfile"),
    )


def describe_contact(
    instance_id: str,
    contact_id: str,
    region_name: str | None = None,
) -> DescribeContactResult:
    """Describe contact.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    try:
        resp = client.describe_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe contact") from exc
    return DescribeContactResult(
        contact=resp.get("Contact"),
    )


def describe_contact_evaluation(
    instance_id: str,
    evaluation_id: str,
    region_name: str | None = None,
) -> DescribeContactEvaluationResult:
    """Describe contact evaluation.

    Args:
        instance_id: Instance id.
        evaluation_id: Evaluation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationId"] = evaluation_id
    try:
        resp = client.describe_contact_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe contact evaluation") from exc
    return DescribeContactEvaluationResult(
        evaluation=resp.get("Evaluation"),
        evaluation_form=resp.get("EvaluationForm"),
    )


def describe_contact_flow_module(
    instance_id: str,
    contact_flow_module_id: str,
    region_name: str | None = None,
) -> DescribeContactFlowModuleResult:
    """Describe contact flow module.

    Args:
        instance_id: Instance id.
        contact_flow_module_id: Contact flow module id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowModuleId"] = contact_flow_module_id
    try:
        resp = client.describe_contact_flow_module(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe contact flow module") from exc
    return DescribeContactFlowModuleResult(
        contact_flow_module=resp.get("ContactFlowModule"),
    )


def describe_email_address(
    instance_id: str,
    email_address_id: str,
    region_name: str | None = None,
) -> DescribeEmailAddressResult:
    """Describe email address.

    Args:
        instance_id: Instance id.
        email_address_id: Email address id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EmailAddressId"] = email_address_id
    try:
        resp = client.describe_email_address(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe email address") from exc
    return DescribeEmailAddressResult(
        email_address_id=resp.get("EmailAddressId"),
        email_address_arn=resp.get("EmailAddressArn"),
        email_address=resp.get("EmailAddress"),
        display_name=resp.get("DisplayName"),
        description=resp.get("Description"),
        create_timestamp=resp.get("CreateTimestamp"),
        modified_timestamp=resp.get("ModifiedTimestamp"),
        alias_configurations=resp.get("AliasConfigurations"),
        tags=resp.get("Tags"),
    )


def describe_evaluation_form(
    instance_id: str,
    evaluation_form_id: str,
    *,
    evaluation_form_version: int | None = None,
    region_name: str | None = None,
) -> DescribeEvaluationFormResult:
    """Describe evaluation form.

    Args:
        instance_id: Instance id.
        evaluation_form_id: Evaluation form id.
        evaluation_form_version: Evaluation form version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    if evaluation_form_version is not None:
        kwargs["EvaluationFormVersion"] = evaluation_form_version
    try:
        resp = client.describe_evaluation_form(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe evaluation form") from exc
    return DescribeEvaluationFormResult(
        evaluation_form=resp.get("EvaluationForm"),
    )


def describe_hours_of_operation(
    instance_id: str,
    hours_of_operation_id: str,
    region_name: str | None = None,
) -> DescribeHoursOfOperationResult:
    """Describe hours of operation.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    try:
        resp = client.describe_hours_of_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe hours of operation") from exc
    return DescribeHoursOfOperationResult(
        hours_of_operation=resp.get("HoursOfOperation"),
    )


def describe_hours_of_operation_override(
    instance_id: str,
    hours_of_operation_id: str,
    hours_of_operation_override_id: str,
    region_name: str | None = None,
) -> DescribeHoursOfOperationOverrideResult:
    """Describe hours of operation override.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        hours_of_operation_override_id: Hours of operation override id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    kwargs["HoursOfOperationOverrideId"] = hours_of_operation_override_id
    try:
        resp = client.describe_hours_of_operation_override(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe hours of operation override") from exc
    return DescribeHoursOfOperationOverrideResult(
        hours_of_operation_override=resp.get("HoursOfOperationOverride"),
    )


def describe_instance_attribute(
    instance_id: str,
    attribute_type: str,
    region_name: str | None = None,
) -> DescribeInstanceAttributeResult:
    """Describe instance attribute.

    Args:
        instance_id: Instance id.
        attribute_type: Attribute type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AttributeType"] = attribute_type
    try:
        resp = client.describe_instance_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe instance attribute") from exc
    return DescribeInstanceAttributeResult(
        attribute=resp.get("Attribute"),
    )


def describe_instance_storage_config(
    instance_id: str,
    association_id: str,
    resource_type: str,
    region_name: str | None = None,
) -> DescribeInstanceStorageConfigResult:
    """Describe instance storage config.

    Args:
        instance_id: Instance id.
        association_id: Association id.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AssociationId"] = association_id
    kwargs["ResourceType"] = resource_type
    try:
        resp = client.describe_instance_storage_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe instance storage config") from exc
    return DescribeInstanceStorageConfigResult(
        storage_config=resp.get("StorageConfig"),
    )


def describe_phone_number(
    phone_number_id: str,
    region_name: str | None = None,
) -> DescribePhoneNumberResult:
    """Describe phone number.

    Args:
        phone_number_id: Phone number id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberId"] = phone_number_id
    try:
        resp = client.describe_phone_number(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe phone number") from exc
    return DescribePhoneNumberResult(
        claimed_phone_number_summary=resp.get("ClaimedPhoneNumberSummary"),
    )


def describe_predefined_attribute(
    instance_id: str,
    name: str,
    region_name: str | None = None,
) -> DescribePredefinedAttributeResult:
    """Describe predefined attribute.

    Args:
        instance_id: Instance id.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    try:
        resp = client.describe_predefined_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe predefined attribute") from exc
    return DescribePredefinedAttributeResult(
        predefined_attribute=resp.get("PredefinedAttribute"),
    )


def describe_prompt(
    instance_id: str,
    prompt_id: str,
    region_name: str | None = None,
) -> DescribePromptResult:
    """Describe prompt.

    Args:
        instance_id: Instance id.
        prompt_id: Prompt id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["PromptId"] = prompt_id
    try:
        resp = client.describe_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe prompt") from exc
    return DescribePromptResult(
        prompt=resp.get("Prompt"),
    )


def describe_quick_connect(
    instance_id: str,
    quick_connect_id: str,
    region_name: str | None = None,
) -> DescribeQuickConnectResult:
    """Describe quick connect.

    Args:
        instance_id: Instance id.
        quick_connect_id: Quick connect id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QuickConnectId"] = quick_connect_id
    try:
        resp = client.describe_quick_connect(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe quick connect") from exc
    return DescribeQuickConnectResult(
        quick_connect=resp.get("QuickConnect"),
    )


def describe_rule(
    instance_id: str,
    rule_id: str,
    region_name: str | None = None,
) -> DescribeRuleResult:
    """Describe rule.

    Args:
        instance_id: Instance id.
        rule_id: Rule id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RuleId"] = rule_id
    try:
        resp = client.describe_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe rule") from exc
    return DescribeRuleResult(
        rule=resp.get("Rule"),
    )


def describe_security_profile(
    security_profile_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> DescribeSecurityProfileResult:
    """Describe security profile.

    Args:
        security_profile_id: Security profile id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityProfileId"] = security_profile_id
    kwargs["InstanceId"] = instance_id
    try:
        resp = client.describe_security_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe security profile") from exc
    return DescribeSecurityProfileResult(
        security_profile=resp.get("SecurityProfile"),
    )


def describe_traffic_distribution_group(
    traffic_distribution_group_id: str,
    region_name: str | None = None,
) -> DescribeTrafficDistributionGroupResult:
    """Describe traffic distribution group.

    Args:
        traffic_distribution_group_id: Traffic distribution group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrafficDistributionGroupId"] = traffic_distribution_group_id
    try:
        resp = client.describe_traffic_distribution_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe traffic distribution group") from exc
    return DescribeTrafficDistributionGroupResult(
        traffic_distribution_group=resp.get("TrafficDistributionGroup"),
    )


def describe_user_hierarchy_group(
    hierarchy_group_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> DescribeUserHierarchyGroupResult:
    """Describe user hierarchy group.

    Args:
        hierarchy_group_id: Hierarchy group id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HierarchyGroupId"] = hierarchy_group_id
    kwargs["InstanceId"] = instance_id
    try:
        resp = client.describe_user_hierarchy_group(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user hierarchy group") from exc
    return DescribeUserHierarchyGroupResult(
        hierarchy_group=resp.get("HierarchyGroup"),
    )


def describe_user_hierarchy_structure(
    instance_id: str,
    region_name: str | None = None,
) -> DescribeUserHierarchyStructureResult:
    """Describe user hierarchy structure.

    Args:
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    try:
        resp = client.describe_user_hierarchy_structure(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe user hierarchy structure") from exc
    return DescribeUserHierarchyStructureResult(
        hierarchy_structure=resp.get("HierarchyStructure"),
    )


def describe_view(
    instance_id: str,
    view_id: str,
    region_name: str | None = None,
) -> DescribeViewResult:
    """Describe view.

    Args:
        instance_id: Instance id.
        view_id: View id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    try:
        resp = client.describe_view(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe view") from exc
    return DescribeViewResult(
        view=resp.get("View"),
    )


def describe_vocabulary(
    instance_id: str,
    vocabulary_id: str,
    region_name: str | None = None,
) -> DescribeVocabularyResult:
    """Describe vocabulary.

    Args:
        instance_id: Instance id.
        vocabulary_id: Vocabulary id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["VocabularyId"] = vocabulary_id
    try:
        resp = client.describe_vocabulary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe vocabulary") from exc
    return DescribeVocabularyResult(
        vocabulary=resp.get("Vocabulary"),
    )


def disassociate_analytics_data_set(
    instance_id: str,
    data_set_id: str,
    *,
    target_account_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate analytics data set.

    Args:
        instance_id: Instance id.
        data_set_id: Data set id.
        target_account_id: Target account id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["DataSetId"] = data_set_id
    if target_account_id is not None:
        kwargs["TargetAccountId"] = target_account_id
    try:
        client.disassociate_analytics_data_set(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate analytics data set") from exc
    return None


def disassociate_approved_origin(
    instance_id: str,
    origin: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate approved origin.

    Args:
        instance_id: Instance id.
        origin: Origin.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Origin"] = origin
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_approved_origin(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate approved origin") from exc
    return None


def disassociate_bot(
    instance_id: str,
    *,
    lex_bot: dict[str, Any] | None = None,
    lex_v2_bot: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate bot.

    Args:
        instance_id: Instance id.
        lex_bot: Lex bot.
        lex_v2_bot: Lex v2 bot.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if lex_bot is not None:
        kwargs["LexBot"] = lex_bot
    if lex_v2_bot is not None:
        kwargs["LexV2Bot"] = lex_v2_bot
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_bot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate bot") from exc
    return None


def disassociate_email_address_alias(
    email_address_id: str,
    instance_id: str,
    alias_configuration: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate email address alias.

    Args:
        email_address_id: Email address id.
        instance_id: Instance id.
        alias_configuration: Alias configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EmailAddressId"] = email_address_id
    kwargs["InstanceId"] = instance_id
    kwargs["AliasConfiguration"] = alias_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_email_address_alias(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate email address alias") from exc
    return None


def disassociate_flow(
    instance_id: str,
    resource_id: str,
    resource_type: str,
    region_name: str | None = None,
) -> None:
    """Disassociate flow.

    Args:
        instance_id: Instance id.
        resource_id: Resource id.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ResourceId"] = resource_id
    kwargs["ResourceType"] = resource_type
    try:
        client.disassociate_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate flow") from exc
    return None


def disassociate_instance_storage_config(
    instance_id: str,
    association_id: str,
    resource_type: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate instance storage config.

    Args:
        instance_id: Instance id.
        association_id: Association id.
        resource_type: Resource type.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AssociationId"] = association_id
    kwargs["ResourceType"] = resource_type
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_instance_storage_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate instance storage config") from exc
    return None


def disassociate_lambda_function(
    instance_id: str,
    function_arn: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate lambda function.

    Args:
        instance_id: Instance id.
        function_arn: Function arn.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FunctionArn"] = function_arn
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_lambda_function(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate lambda function") from exc
    return None


def disassociate_lex_bot(
    instance_id: str,
    bot_name: str,
    lex_region: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate lex bot.

    Args:
        instance_id: Instance id.
        bot_name: Bot name.
        lex_region: Lex region.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["BotName"] = bot_name
    kwargs["LexRegion"] = lex_region
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_lex_bot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate lex bot") from exc
    return None


def disassociate_phone_number_contact_flow(
    phone_number_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate phone number contact flow.

    Args:
        phone_number_id: Phone number id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberId"] = phone_number_id
    kwargs["InstanceId"] = instance_id
    try:
        client.disassociate_phone_number_contact_flow(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate phone number contact flow") from exc
    return None


def disassociate_queue_quick_connects(
    instance_id: str,
    queue_id: str,
    quick_connect_ids: list[str],
    region_name: str | None = None,
) -> None:
    """Disassociate queue quick connects.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        quick_connect_ids: Quick connect ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    kwargs["QuickConnectIds"] = quick_connect_ids
    try:
        client.disassociate_queue_quick_connects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate queue quick connects") from exc
    return None


def disassociate_routing_profile_queues(
    instance_id: str,
    routing_profile_id: str,
    *,
    queue_references: list[dict[str, Any]] | None = None,
    manual_assignment_queue_references: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate routing profile queues.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        queue_references: Queue references.
        manual_assignment_queue_references: Manual assignment queue references.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    if queue_references is not None:
        kwargs["QueueReferences"] = queue_references
    if manual_assignment_queue_references is not None:
        kwargs["ManualAssignmentQueueReferences"] = manual_assignment_queue_references
    try:
        client.disassociate_routing_profile_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate routing profile queues") from exc
    return None


def disassociate_security_key(
    instance_id: str,
    association_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate security key.

    Args:
        instance_id: Instance id.
        association_id: Association id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AssociationId"] = association_id
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.disassociate_security_key(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate security key") from exc
    return None


def disassociate_traffic_distribution_group_user(
    traffic_distribution_group_id: str,
    user_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Disassociate traffic distribution group user.

    Args:
        traffic_distribution_group_id: Traffic distribution group id.
        user_id: User id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrafficDistributionGroupId"] = traffic_distribution_group_id
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    try:
        client.disassociate_traffic_distribution_group_user(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate traffic distribution group user") from exc
    return None


def disassociate_user_proficiencies(
    instance_id: str,
    user_id: str,
    user_proficiencies: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Disassociate user proficiencies.

    Args:
        instance_id: Instance id.
        user_id: User id.
        user_proficiencies: User proficiencies.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["UserId"] = user_id
    kwargs["UserProficiencies"] = user_proficiencies
    try:
        client.disassociate_user_proficiencies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate user proficiencies") from exc
    return None


def dismiss_user_contact(
    user_id: str,
    instance_id: str,
    contact_id: str,
    region_name: str | None = None,
) -> None:
    """Dismiss user contact.

    Args:
        user_id: User id.
        instance_id: Instance id.
        contact_id: Contact id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    try:
        client.dismiss_user_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to dismiss user contact") from exc
    return None


def get_attached_file(
    instance_id: str,
    file_id: str,
    associated_resource_arn: str,
    *,
    url_expiry_in_seconds: int | None = None,
    region_name: str | None = None,
) -> GetAttachedFileResult:
    """Get attached file.

    Args:
        instance_id: Instance id.
        file_id: File id.
        associated_resource_arn: Associated resource arn.
        url_expiry_in_seconds: Url expiry in seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FileId"] = file_id
    kwargs["AssociatedResourceArn"] = associated_resource_arn
    if url_expiry_in_seconds is not None:
        kwargs["UrlExpiryInSeconds"] = url_expiry_in_seconds
    try:
        resp = client.get_attached_file(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get attached file") from exc
    return GetAttachedFileResult(
        file_arn=resp.get("FileArn"),
        file_id=resp.get("FileId"),
        creation_time=resp.get("CreationTime"),
        file_status=resp.get("FileStatus"),
        file_name=resp.get("FileName"),
        file_size_in_bytes=resp.get("FileSizeInBytes"),
        associated_resource_arn=resp.get("AssociatedResourceArn"),
        file_use_case_type=resp.get("FileUseCaseType"),
        created_by=resp.get("CreatedBy"),
        download_url_metadata=resp.get("DownloadUrlMetadata"),
        tags=resp.get("Tags"),
    )


def get_contact_metrics(
    instance_id: str,
    contact_id: str,
    metrics: list[dict[str, Any]],
    region_name: str | None = None,
) -> GetContactMetricsResult:
    """Get contact metrics.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        metrics: Metrics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["Metrics"] = metrics
    try:
        resp = client.get_contact_metrics(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get contact metrics") from exc
    return GetContactMetricsResult(
        metric_results=resp.get("MetricResults"),
        id=resp.get("Id"),
        arn=resp.get("Arn"),
    )


def get_current_user_data(
    instance_id: str,
    filters: dict[str, Any],
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetCurrentUserDataResult:
    """Get current user data.

    Args:
        instance_id: Instance id.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.get_current_user_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get current user data") from exc
    return GetCurrentUserDataResult(
        next_token=resp.get("NextToken"),
        user_data_list=resp.get("UserDataList"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def get_effective_hours_of_operations(
    instance_id: str,
    hours_of_operation_id: str,
    from_date: str,
    to_date: str,
    region_name: str | None = None,
) -> GetEffectiveHoursOfOperationsResult:
    """Get effective hours of operations.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        from_date: From date.
        to_date: To date.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    kwargs["FromDate"] = from_date
    kwargs["ToDate"] = to_date
    try:
        resp = client.get_effective_hours_of_operations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get effective hours of operations") from exc
    return GetEffectiveHoursOfOperationsResult(
        effective_hours_of_operation_list=resp.get("EffectiveHoursOfOperationList"),
        time_zone=resp.get("TimeZone"),
    )


def get_federation_token(
    instance_id: str,
    region_name: str | None = None,
) -> GetFederationTokenResult:
    """Get federation token.

    Args:
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    try:
        resp = client.get_federation_token(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get federation token") from exc
    return GetFederationTokenResult(
        credentials=resp.get("Credentials"),
        sign_in_url=resp.get("SignInUrl"),
        user_arn=resp.get("UserArn"),
        user_id=resp.get("UserId"),
    )


def get_flow_association(
    instance_id: str,
    resource_id: str,
    resource_type: str,
    region_name: str | None = None,
) -> GetFlowAssociationResult:
    """Get flow association.

    Args:
        instance_id: Instance id.
        resource_id: Resource id.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ResourceId"] = resource_id
    kwargs["ResourceType"] = resource_type
    try:
        resp = client.get_flow_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get flow association") from exc
    return GetFlowAssociationResult(
        resource_id=resp.get("ResourceId"),
        flow_id=resp.get("FlowId"),
        resource_type=resp.get("ResourceType"),
    )


def get_metric_data(
    instance_id: str,
    start_time: str,
    end_time: str,
    filters: dict[str, Any],
    historical_metrics: list[dict[str, Any]],
    *,
    groupings: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetMetricDataResult:
    """Get metric data.

    Args:
        instance_id: Instance id.
        start_time: Start time.
        end_time: End time.
        filters: Filters.
        historical_metrics: Historical metrics.
        groupings: Groupings.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["StartTime"] = start_time
    kwargs["EndTime"] = end_time
    kwargs["Filters"] = filters
    kwargs["HistoricalMetrics"] = historical_metrics
    if groupings is not None:
        kwargs["Groupings"] = groupings
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.get_metric_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get metric data") from exc
    return GetMetricDataResult(
        next_token=resp.get("NextToken"),
        metric_results=resp.get("MetricResults"),
    )


def get_metric_data_v2(
    resource_arn: str,
    start_time: str,
    end_time: str,
    filters: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    *,
    interval: dict[str, Any] | None = None,
    groupings: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetMetricDataV2Result:
    """Get metric data v2.

    Args:
        resource_arn: Resource arn.
        start_time: Start time.
        end_time: End time.
        filters: Filters.
        metrics: Metrics.
        interval: Interval.
        groupings: Groupings.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["StartTime"] = start_time
    kwargs["EndTime"] = end_time
    kwargs["Filters"] = filters
    kwargs["Metrics"] = metrics
    if interval is not None:
        kwargs["Interval"] = interval
    if groupings is not None:
        kwargs["Groupings"] = groupings
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.get_metric_data_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get metric data v2") from exc
    return GetMetricDataV2Result(
        next_token=resp.get("NextToken"),
        metric_results=resp.get("MetricResults"),
    )


def get_prompt_file(
    instance_id: str,
    prompt_id: str,
    region_name: str | None = None,
) -> GetPromptFileResult:
    """Get prompt file.

    Args:
        instance_id: Instance id.
        prompt_id: Prompt id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["PromptId"] = prompt_id
    try:
        resp = client.get_prompt_file(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get prompt file") from exc
    return GetPromptFileResult(
        prompt_presigned_url=resp.get("PromptPresignedUrl"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def get_task_template(
    instance_id: str,
    task_template_id: str,
    *,
    snapshot_version: str | None = None,
    region_name: str | None = None,
) -> GetTaskTemplateResult:
    """Get task template.

    Args:
        instance_id: Instance id.
        task_template_id: Task template id.
        snapshot_version: Snapshot version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["TaskTemplateId"] = task_template_id
    if snapshot_version is not None:
        kwargs["SnapshotVersion"] = snapshot_version
    try:
        resp = client.get_task_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get task template") from exc
    return GetTaskTemplateResult(
        instance_id=resp.get("InstanceId"),
        id=resp.get("Id"),
        arn=resp.get("Arn"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        contact_flow_id=resp.get("ContactFlowId"),
        self_assign_flow_id=resp.get("SelfAssignFlowId"),
        constraints=resp.get("Constraints"),
        defaults=resp.get("Defaults"),
        fields=resp.get("Fields"),
        status=resp.get("Status"),
        last_modified_time=resp.get("LastModifiedTime"),
        created_time=resp.get("CreatedTime"),
        tags=resp.get("Tags"),
    )


def get_traffic_distribution(
    id: str,
    region_name: str | None = None,
) -> GetTrafficDistributionResult:
    """Get traffic distribution.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    try:
        resp = client.get_traffic_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get traffic distribution") from exc
    return GetTrafficDistributionResult(
        telephony_config=resp.get("TelephonyConfig"),
        id=resp.get("Id"),
        arn=resp.get("Arn"),
        sign_in_config=resp.get("SignInConfig"),
        agent_config=resp.get("AgentConfig"),
    )


def import_phone_number(
    instance_id: str,
    source_phone_number_arn: str,
    *,
    phone_number_description: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> ImportPhoneNumberResult:
    """Import phone number.

    Args:
        instance_id: Instance id.
        source_phone_number_arn: Source phone number arn.
        phone_number_description: Phone number description.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["SourcePhoneNumberArn"] = source_phone_number_arn
    if phone_number_description is not None:
        kwargs["PhoneNumberDescription"] = phone_number_description
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.import_phone_number(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import phone number") from exc
    return ImportPhoneNumberResult(
        phone_number_id=resp.get("PhoneNumberId"),
        phone_number_arn=resp.get("PhoneNumberArn"),
    )


def list_agent_statuses(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    agent_status_types: list[str] | None = None,
    region_name: str | None = None,
) -> ListAgentStatusesResult:
    """List agent statuses.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        agent_status_types: Agent status types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if agent_status_types is not None:
        kwargs["AgentStatusTypes"] = agent_status_types
    try:
        resp = client.list_agent_statuses(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list agent statuses") from exc
    return ListAgentStatusesResult(
        next_token=resp.get("NextToken"),
        agent_status_summary_list=resp.get("AgentStatusSummaryList"),
    )


def list_analytics_data_associations(
    instance_id: str,
    *,
    data_set_id: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAnalyticsDataAssociationsResult:
    """List analytics data associations.

    Args:
        instance_id: Instance id.
        data_set_id: Data set id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if data_set_id is not None:
        kwargs["DataSetId"] = data_set_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_analytics_data_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list analytics data associations") from exc
    return ListAnalyticsDataAssociationsResult(
        results=resp.get("Results"),
        next_token=resp.get("NextToken"),
    )


def list_analytics_data_lake_data_sets(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAnalyticsDataLakeDataSetsResult:
    """List analytics data lake data sets.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_analytics_data_lake_data_sets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list analytics data lake data sets") from exc
    return ListAnalyticsDataLakeDataSetsResult(
        results=resp.get("Results"),
        next_token=resp.get("NextToken"),
    )


def list_approved_origins(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListApprovedOriginsResult:
    """List approved origins.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_approved_origins(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list approved origins") from exc
    return ListApprovedOriginsResult(
        origins=resp.get("Origins"),
        next_token=resp.get("NextToken"),
    )


def list_associated_contacts(
    instance_id: str,
    contact_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAssociatedContactsResult:
    """List associated contacts.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_associated_contacts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list associated contacts") from exc
    return ListAssociatedContactsResult(
        contact_summary_list=resp.get("ContactSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_authentication_profiles(
    instance_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAuthenticationProfilesResult:
    """List authentication profiles.

    Args:
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_authentication_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list authentication profiles") from exc
    return ListAuthenticationProfilesResult(
        authentication_profile_summary_list=resp.get("AuthenticationProfileSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_bots(
    instance_id: str,
    lex_version: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListBotsResult:
    """List bots.

    Args:
        instance_id: Instance id.
        lex_version: Lex version.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["LexVersion"] = lex_version
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_bots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list bots") from exc
    return ListBotsResult(
        lex_bots=resp.get("LexBots"),
        next_token=resp.get("NextToken"),
    )


def list_contact_evaluations(
    instance_id: str,
    contact_id: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListContactEvaluationsResult:
    """List contact evaluations.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_contact_evaluations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list contact evaluations") from exc
    return ListContactEvaluationsResult(
        evaluation_summary_list=resp.get("EvaluationSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_contact_flow_modules(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    contact_flow_module_state: str | None = None,
    region_name: str | None = None,
) -> ListContactFlowModulesResult:
    """List contact flow modules.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        contact_flow_module_state: Contact flow module state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if contact_flow_module_state is not None:
        kwargs["ContactFlowModuleState"] = contact_flow_module_state
    try:
        resp = client.list_contact_flow_modules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list contact flow modules") from exc
    return ListContactFlowModulesResult(
        contact_flow_modules_summary_list=resp.get("ContactFlowModulesSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_contact_flow_versions(
    instance_id: str,
    contact_flow_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListContactFlowVersionsResult:
    """List contact flow versions.

    Args:
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_contact_flow_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list contact flow versions") from exc
    return ListContactFlowVersionsResult(
        contact_flow_version_summary_list=resp.get("ContactFlowVersionSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_contact_references(
    instance_id: str,
    contact_id: str,
    reference_types: list[str],
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListContactReferencesResult:
    """List contact references.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        reference_types: Reference types.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["ReferenceTypes"] = reference_types
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_contact_references(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list contact references") from exc
    return ListContactReferencesResult(
        reference_summary_list=resp.get("ReferenceSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_default_vocabularies(
    instance_id: str,
    *,
    language_code: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDefaultVocabulariesResult:
    """List default vocabularies.

    Args:
        instance_id: Instance id.
        language_code: Language code.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if language_code is not None:
        kwargs["LanguageCode"] = language_code
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_default_vocabularies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list default vocabularies") from exc
    return ListDefaultVocabulariesResult(
        default_vocabulary_list=resp.get("DefaultVocabularyList"),
        next_token=resp.get("NextToken"),
    )


def list_evaluation_form_versions(
    instance_id: str,
    evaluation_form_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListEvaluationFormVersionsResult:
    """List evaluation form versions.

    Args:
        instance_id: Instance id.
        evaluation_form_id: Evaluation form id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_evaluation_form_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list evaluation form versions") from exc
    return ListEvaluationFormVersionsResult(
        evaluation_form_version_summary_list=resp.get("EvaluationFormVersionSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_evaluation_forms(
    instance_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListEvaluationFormsResult:
    """List evaluation forms.

    Args:
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_evaluation_forms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list evaluation forms") from exc
    return ListEvaluationFormsResult(
        evaluation_form_summary_list=resp.get("EvaluationFormSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_flow_associations(
    instance_id: str,
    *,
    resource_type: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFlowAssociationsResult:
    """List flow associations.

    Args:
        instance_id: Instance id.
        resource_type: Resource type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_flow_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list flow associations") from exc
    return ListFlowAssociationsResult(
        flow_association_summary_list=resp.get("FlowAssociationSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_hours_of_operation_overrides(
    instance_id: str,
    hours_of_operation_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListHoursOfOperationOverridesResult:
    """List hours of operation overrides.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_hours_of_operation_overrides(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list hours of operation overrides") from exc
    return ListHoursOfOperationOverridesResult(
        next_token=resp.get("NextToken"),
        hours_of_operation_override_list=resp.get("HoursOfOperationOverrideList"),
        last_modified_region=resp.get("LastModifiedRegion"),
        last_modified_time=resp.get("LastModifiedTime"),
    )


def list_hours_of_operations(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListHoursOfOperationsResult:
    """List hours of operations.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_hours_of_operations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list hours of operations") from exc
    return ListHoursOfOperationsResult(
        hours_of_operation_summary_list=resp.get("HoursOfOperationSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_instance_attributes(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListInstanceAttributesResult:
    """List instance attributes.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_instance_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list instance attributes") from exc
    return ListInstanceAttributesResult(
        attributes=resp.get("Attributes"),
        next_token=resp.get("NextToken"),
    )


def list_instance_storage_configs(
    instance_id: str,
    resource_type: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListInstanceStorageConfigsResult:
    """List instance storage configs.

    Args:
        instance_id: Instance id.
        resource_type: Resource type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ResourceType"] = resource_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_instance_storage_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list instance storage configs") from exc
    return ListInstanceStorageConfigsResult(
        storage_configs=resp.get("StorageConfigs"),
        next_token=resp.get("NextToken"),
    )


def list_integration_associations(
    instance_id: str,
    *,
    integration_type: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    integration_arn: str | None = None,
    region_name: str | None = None,
) -> ListIntegrationAssociationsResult:
    """List integration associations.

    Args:
        instance_id: Instance id.
        integration_type: Integration type.
        next_token: Next token.
        max_results: Max results.
        integration_arn: Integration arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if integration_type is not None:
        kwargs["IntegrationType"] = integration_type
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if integration_arn is not None:
        kwargs["IntegrationArn"] = integration_arn
    try:
        resp = client.list_integration_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list integration associations") from exc
    return ListIntegrationAssociationsResult(
        integration_association_summary_list=resp.get("IntegrationAssociationSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_lambda_functions(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListLambdaFunctionsResult:
    """List lambda functions.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_lambda_functions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list lambda functions") from exc
    return ListLambdaFunctionsResult(
        lambda_functions=resp.get("LambdaFunctions"),
        next_token=resp.get("NextToken"),
    )


def list_lex_bots(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListLexBotsResult:
    """List lex bots.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_lex_bots(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list lex bots") from exc
    return ListLexBotsResult(
        lex_bots=resp.get("LexBots"),
        next_token=resp.get("NextToken"),
    )


def list_phone_numbers(
    instance_id: str,
    *,
    phone_number_types: list[str] | None = None,
    phone_number_country_codes: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPhoneNumbersResult:
    """List phone numbers.

    Args:
        instance_id: Instance id.
        phone_number_types: Phone number types.
        phone_number_country_codes: Phone number country codes.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if phone_number_types is not None:
        kwargs["PhoneNumberTypes"] = phone_number_types
    if phone_number_country_codes is not None:
        kwargs["PhoneNumberCountryCodes"] = phone_number_country_codes
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_phone_numbers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list phone numbers") from exc
    return ListPhoneNumbersResult(
        phone_number_summary_list=resp.get("PhoneNumberSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_phone_numbers_v2(
    *,
    target_arn: str | None = None,
    instance_id: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    phone_number_country_codes: list[str] | None = None,
    phone_number_types: list[str] | None = None,
    phone_number_prefix: str | None = None,
    region_name: str | None = None,
) -> ListPhoneNumbersV2Result:
    """List phone numbers v2.

    Args:
        target_arn: Target arn.
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        phone_number_country_codes: Phone number country codes.
        phone_number_types: Phone number types.
        phone_number_prefix: Phone number prefix.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if phone_number_country_codes is not None:
        kwargs["PhoneNumberCountryCodes"] = phone_number_country_codes
    if phone_number_types is not None:
        kwargs["PhoneNumberTypes"] = phone_number_types
    if phone_number_prefix is not None:
        kwargs["PhoneNumberPrefix"] = phone_number_prefix
    try:
        resp = client.list_phone_numbers_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list phone numbers v2") from exc
    return ListPhoneNumbersV2Result(
        next_token=resp.get("NextToken"),
        list_phone_numbers_summary_list=resp.get("ListPhoneNumbersSummaryList"),
    )


def list_predefined_attributes(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPredefinedAttributesResult:
    """List predefined attributes.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_predefined_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list predefined attributes") from exc
    return ListPredefinedAttributesResult(
        next_token=resp.get("NextToken"),
        predefined_attribute_summary_list=resp.get("PredefinedAttributeSummaryList"),
    )


def list_prompts(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPromptsResult:
    """List prompts.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_prompts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list prompts") from exc
    return ListPromptsResult(
        prompt_summary_list=resp.get("PromptSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_queue_quick_connects(
    instance_id: str,
    queue_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListQueueQuickConnectsResult:
    """List queue quick connects.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_queue_quick_connects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list queue quick connects") from exc
    return ListQueueQuickConnectsResult(
        next_token=resp.get("NextToken"),
        quick_connect_summary_list=resp.get("QuickConnectSummaryList"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def list_quick_connects(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    quick_connect_types: list[str] | None = None,
    region_name: str | None = None,
) -> ListQuickConnectsResult:
    """List quick connects.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        quick_connect_types: Quick connect types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if quick_connect_types is not None:
        kwargs["QuickConnectTypes"] = quick_connect_types
    try:
        resp = client.list_quick_connects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list quick connects") from exc
    return ListQuickConnectsResult(
        quick_connect_summary_list=resp.get("QuickConnectSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_realtime_contact_analysis_segments_v2(
    instance_id: str,
    contact_id: str,
    output_type: str,
    segment_types: list[str],
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRealtimeContactAnalysisSegmentsV2Result:
    """List realtime contact analysis segments v2.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        output_type: Output type.
        segment_types: Segment types.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["OutputType"] = output_type
    kwargs["SegmentTypes"] = segment_types
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_realtime_contact_analysis_segments_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list realtime contact analysis segments v2") from exc
    return ListRealtimeContactAnalysisSegmentsV2Result(
        channel=resp.get("Channel"),
        status=resp.get("Status"),
        segments=resp.get("Segments"),
        next_token=resp.get("NextToken"),
    )


def list_routing_profile_manual_assignment_queues(
    instance_id: str,
    routing_profile_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRoutingProfileManualAssignmentQueuesResult:
    """List routing profile manual assignment queues.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_routing_profile_manual_assignment_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to list routing profile manual assignment queues"
        ) from exc
    return ListRoutingProfileManualAssignmentQueuesResult(
        next_token=resp.get("NextToken"),
        routing_profile_manual_assignment_queue_config_summary_list=resp.get(
            "RoutingProfileManualAssignmentQueueConfigSummaryList"
        ),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def list_routing_profile_queues(
    instance_id: str,
    routing_profile_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRoutingProfileQueuesResult:
    """List routing profile queues.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_routing_profile_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list routing profile queues") from exc
    return ListRoutingProfileQueuesResult(
        next_token=resp.get("NextToken"),
        routing_profile_queue_config_summary_list=resp.get("RoutingProfileQueueConfigSummaryList"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def list_rules(
    instance_id: str,
    *,
    publish_status: str | None = None,
    event_source_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListRulesResult:
    """List rules.

    Args:
        instance_id: Instance id.
        publish_status: Publish status.
        event_source_name: Event source name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if publish_status is not None:
        kwargs["PublishStatus"] = publish_status
    if event_source_name is not None:
        kwargs["EventSourceName"] = event_source_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list rules") from exc
    return ListRulesResult(
        rule_summary_list=resp.get("RuleSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_security_keys(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSecurityKeysResult:
    """List security keys.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_security_keys(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security keys") from exc
    return ListSecurityKeysResult(
        security_keys=resp.get("SecurityKeys"),
        next_token=resp.get("NextToken"),
    )


def list_security_profile_applications(
    security_profile_id: str,
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSecurityProfileApplicationsResult:
    """List security profile applications.

    Args:
        security_profile_id: Security profile id.
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityProfileId"] = security_profile_id
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_security_profile_applications(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security profile applications") from exc
    return ListSecurityProfileApplicationsResult(
        applications=resp.get("Applications"),
        next_token=resp.get("NextToken"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def list_security_profile_permissions(
    security_profile_id: str,
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSecurityProfilePermissionsResult:
    """List security profile permissions.

    Args:
        security_profile_id: Security profile id.
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityProfileId"] = security_profile_id
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_security_profile_permissions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security profile permissions") from exc
    return ListSecurityProfilePermissionsResult(
        permissions=resp.get("Permissions"),
        next_token=resp.get("NextToken"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def list_security_profiles(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSecurityProfilesResult:
    """List security profiles.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_security_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security profiles") from exc
    return ListSecurityProfilesResult(
        security_profile_summary_list=resp.get("SecurityProfileSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def list_task_templates(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    status: str | None = None,
    name: str | None = None,
    region_name: str | None = None,
) -> ListTaskTemplatesResult:
    """List task templates.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        status: Status.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if status is not None:
        kwargs["Status"] = status
    if name is not None:
        kwargs["Name"] = name
    try:
        resp = client.list_task_templates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list task templates") from exc
    return ListTaskTemplatesResult(
        task_templates=resp.get("TaskTemplates"),
        next_token=resp.get("NextToken"),
    )


def list_traffic_distribution_group_users(
    traffic_distribution_group_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTrafficDistributionGroupUsersResult:
    """List traffic distribution group users.

    Args:
        traffic_distribution_group_id: Traffic distribution group id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TrafficDistributionGroupId"] = traffic_distribution_group_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_traffic_distribution_group_users(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic distribution group users") from exc
    return ListTrafficDistributionGroupUsersResult(
        next_token=resp.get("NextToken"),
        traffic_distribution_group_user_summary_list=resp.get(
            "TrafficDistributionGroupUserSummaryList"
        ),
    )


def list_traffic_distribution_groups(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    instance_id: str | None = None,
    region_name: str | None = None,
) -> ListTrafficDistributionGroupsResult:
    """List traffic distribution groups.

    Args:
        max_results: Max results.
        next_token: Next token.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    try:
        resp = client.list_traffic_distribution_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list traffic distribution groups") from exc
    return ListTrafficDistributionGroupsResult(
        next_token=resp.get("NextToken"),
        traffic_distribution_group_summary_list=resp.get("TrafficDistributionGroupSummaryList"),
    )


def list_use_cases(
    instance_id: str,
    integration_association_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListUseCasesResult:
    """List use cases.

    Args:
        instance_id: Instance id.
        integration_association_id: Integration association id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["IntegrationAssociationId"] = integration_association_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_use_cases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list use cases") from exc
    return ListUseCasesResult(
        use_case_summary_list=resp.get("UseCaseSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_user_hierarchy_groups(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListUserHierarchyGroupsResult:
    """List user hierarchy groups.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_user_hierarchy_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list user hierarchy groups") from exc
    return ListUserHierarchyGroupsResult(
        user_hierarchy_group_summary_list=resp.get("UserHierarchyGroupSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_user_proficiencies(
    instance_id: str,
    user_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListUserProficienciesResult:
    """List user proficiencies.

    Args:
        instance_id: Instance id.
        user_id: User id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["UserId"] = user_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_user_proficiencies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list user proficiencies") from exc
    return ListUserProficienciesResult(
        next_token=resp.get("NextToken"),
        user_proficiency_list=resp.get("UserProficiencyList"),
        last_modified_time=resp.get("LastModifiedTime"),
        last_modified_region=resp.get("LastModifiedRegion"),
    )


def list_view_versions(
    instance_id: str,
    view_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListViewVersionsResult:
    """List view versions.

    Args:
        instance_id: Instance id.
        view_id: View id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_view_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list view versions") from exc
    return ListViewVersionsResult(
        view_version_summary_list=resp.get("ViewVersionSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_views(
    instance_id: str,
    *,
    type_value: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListViewsResult:
    """List views.

    Args:
        instance_id: Instance id.
        type_value: Type value.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if type_value is not None:
        kwargs["Type"] = type_value
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_views(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list views") from exc
    return ListViewsResult(
        views_summary_list=resp.get("ViewsSummaryList"),
        next_token=resp.get("NextToken"),
    )


def monitor_contact(
    instance_id: str,
    contact_id: str,
    user_id: str,
    *,
    allowed_monitor_capabilities: list[str] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> MonitorContactResult:
    """Monitor contact.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        user_id: User id.
        allowed_monitor_capabilities: Allowed monitor capabilities.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["UserId"] = user_id
    if allowed_monitor_capabilities is not None:
        kwargs["AllowedMonitorCapabilities"] = allowed_monitor_capabilities
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.monitor_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to monitor contact") from exc
    return MonitorContactResult(
        contact_id=resp.get("ContactId"),
        contact_arn=resp.get("ContactArn"),
    )


def pause_contact(
    contact_id: str,
    instance_id: str,
    *,
    contact_flow_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Pause contact.

    Args:
        contact_id: Contact id.
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactId"] = contact_id
    kwargs["InstanceId"] = instance_id
    if contact_flow_id is not None:
        kwargs["ContactFlowId"] = contact_flow_id
    try:
        client.pause_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to pause contact") from exc
    return None


def put_user_status(
    user_id: str,
    instance_id: str,
    agent_status_id: str,
    region_name: str | None = None,
) -> None:
    """Put user status.

    Args:
        user_id: User id.
        instance_id: Instance id.
        agent_status_id: Agent status id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    kwargs["AgentStatusId"] = agent_status_id
    try:
        client.put_user_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put user status") from exc
    return None


def release_phone_number(
    phone_number_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Release phone number.

    Args:
        phone_number_id: Phone number id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberId"] = phone_number_id
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.release_phone_number(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to release phone number") from exc
    return None


def replicate_instance(
    instance_id: str,
    replica_region: str,
    replica_alias: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> ReplicateInstanceResult:
    """Replicate instance.

    Args:
        instance_id: Instance id.
        replica_region: Replica region.
        replica_alias: Replica alias.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ReplicaRegion"] = replica_region
    kwargs["ReplicaAlias"] = replica_alias
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.replicate_instance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to replicate instance") from exc
    return ReplicateInstanceResult(
        id=resp.get("Id"),
        arn=resp.get("Arn"),
    )


def resume_contact(
    contact_id: str,
    instance_id: str,
    *,
    contact_flow_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Resume contact.

    Args:
        contact_id: Contact id.
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactId"] = contact_id
    kwargs["InstanceId"] = instance_id
    if contact_flow_id is not None:
        kwargs["ContactFlowId"] = contact_flow_id
    try:
        client.resume_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to resume contact") from exc
    return None


def resume_contact_recording(
    instance_id: str,
    contact_id: str,
    initial_contact_id: str,
    *,
    contact_recording_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Resume contact recording.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        initial_contact_id: Initial contact id.
        contact_recording_type: Contact recording type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["InitialContactId"] = initial_contact_id
    if contact_recording_type is not None:
        kwargs["ContactRecordingType"] = contact_recording_type
    try:
        client.resume_contact_recording(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to resume contact recording") from exc
    return None


def search_agent_statuses(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchAgentStatusesResult:
    """Search agent statuses.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_agent_statuses(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search agent statuses") from exc
    return SearchAgentStatusesResult(
        agent_statuses=resp.get("AgentStatuses"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_available_phone_numbers(
    phone_number_country_code: str,
    phone_number_type: str,
    *,
    target_arn: str | None = None,
    instance_id: str | None = None,
    phone_number_prefix: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> SearchAvailablePhoneNumbersResult:
    """Search available phone numbers.

    Args:
        phone_number_country_code: Phone number country code.
        phone_number_type: Phone number type.
        target_arn: Target arn.
        instance_id: Instance id.
        phone_number_prefix: Phone number prefix.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberCountryCode"] = phone_number_country_code
    kwargs["PhoneNumberType"] = phone_number_type
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if phone_number_prefix is not None:
        kwargs["PhoneNumberPrefix"] = phone_number_prefix
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.search_available_phone_numbers(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search available phone numbers") from exc
    return SearchAvailablePhoneNumbersResult(
        next_token=resp.get("NextToken"),
        available_numbers_list=resp.get("AvailableNumbersList"),
    )


def search_contact_evaluations(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_criteria: dict[str, Any] | None = None,
    search_filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchContactEvaluationsResult:
    """Search contact evaluations.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_criteria: Search criteria.
        search_filter: Search filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    try:
        resp = client.search_contact_evaluations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search contact evaluations") from exc
    return SearchContactEvaluationsResult(
        evaluation_search_summary_list=resp.get("EvaluationSearchSummaryList"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_contact_flow_modules(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchContactFlowModulesResult:
    """Search contact flow modules.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_contact_flow_modules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search contact flow modules") from exc
    return SearchContactFlowModulesResult(
        contact_flow_modules=resp.get("ContactFlowModules"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_contact_flows(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchContactFlowsResult:
    """Search contact flows.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_contact_flows(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search contact flows") from exc
    return SearchContactFlowsResult(
        contact_flows=resp.get("ContactFlows"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_contacts(
    instance_id: str,
    time_range: dict[str, Any],
    *,
    search_criteria: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    sort: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchContactsResult:
    """Search contacts.

    Args:
        instance_id: Instance id.
        time_range: Time range.
        search_criteria: Search criteria.
        max_results: Max results.
        next_token: Next token.
        sort: Sort.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["TimeRange"] = time_range
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if sort is not None:
        kwargs["Sort"] = sort
    try:
        resp = client.search_contacts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search contacts") from exc
    return SearchContactsResult(
        contacts=resp.get("Contacts"),
        next_token=resp.get("NextToken"),
        total_count=resp.get("TotalCount"),
    )


def search_email_addresses(
    instance_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    search_criteria: dict[str, Any] | None = None,
    search_filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchEmailAddressesResult:
    """Search email addresses.

    Args:
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        search_criteria: Search criteria.
        search_filter: Search filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    try:
        resp = client.search_email_addresses(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search email addresses") from exc
    return SearchEmailAddressesResult(
        next_token=resp.get("NextToken"),
        email_addresses=resp.get("EmailAddresses"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_evaluation_forms(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_criteria: dict[str, Any] | None = None,
    search_filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchEvaluationFormsResult:
    """Search evaluation forms.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_criteria: Search criteria.
        search_filter: Search filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    try:
        resp = client.search_evaluation_forms(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search evaluation forms") from exc
    return SearchEvaluationFormsResult(
        evaluation_form_search_summary_list=resp.get("EvaluationFormSearchSummaryList"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_hours_of_operation_overrides(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchHoursOfOperationOverridesResult:
    """Search hours of operation overrides.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_hours_of_operation_overrides(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search hours of operation overrides") from exc
    return SearchHoursOfOperationOverridesResult(
        hours_of_operation_overrides=resp.get("HoursOfOperationOverrides"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_hours_of_operations(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchHoursOfOperationsResult:
    """Search hours of operations.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_hours_of_operations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search hours of operations") from exc
    return SearchHoursOfOperationsResult(
        hours_of_operations=resp.get("HoursOfOperations"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_predefined_attributes(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchPredefinedAttributesResult:
    """Search predefined attributes.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_predefined_attributes(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search predefined attributes") from exc
    return SearchPredefinedAttributesResult(
        predefined_attributes=resp.get("PredefinedAttributes"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_prompts(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchPromptsResult:
    """Search prompts.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_prompts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search prompts") from exc
    return SearchPromptsResult(
        prompts=resp.get("Prompts"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_queues(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchQueuesResult:
    """Search queues.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search queues") from exc
    return SearchQueuesResult(
        queues=resp.get("Queues"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_quick_connects(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchQuickConnectsResult:
    """Search quick connects.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_quick_connects(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search quick connects") from exc
    return SearchQuickConnectsResult(
        quick_connects=resp.get("QuickConnects"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_resource_tags(
    instance_id: str,
    *,
    resource_types: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchResourceTagsResult:
    """Search resource tags.

    Args:
        instance_id: Instance id.
        resource_types: Resource types.
        next_token: Next token.
        max_results: Max results.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if resource_types is not None:
        kwargs["ResourceTypes"] = resource_types
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_resource_tags(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search resource tags") from exc
    return SearchResourceTagsResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


def search_routing_profiles(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchRoutingProfilesResult:
    """Search routing profiles.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_routing_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search routing profiles") from exc
    return SearchRoutingProfilesResult(
        routing_profiles=resp.get("RoutingProfiles"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_security_profiles(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_criteria: dict[str, Any] | None = None,
    search_filter: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchSecurityProfilesResult:
    """Search security profiles.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_criteria: Search criteria.
        search_filter: Search filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    try:
        resp = client.search_security_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search security profiles") from exc
    return SearchSecurityProfilesResult(
        security_profiles=resp.get("SecurityProfiles"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_user_hierarchy_groups(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchUserHierarchyGroupsResult:
    """Search user hierarchy groups.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_user_hierarchy_groups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search user hierarchy groups") from exc
    return SearchUserHierarchyGroupsResult(
        user_hierarchy_groups=resp.get("UserHierarchyGroups"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_users(
    instance_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    search_filter: dict[str, Any] | None = None,
    search_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SearchUsersResult:
    """Search users.

    Args:
        instance_id: Instance id.
        next_token: Next token.
        max_results: Max results.
        search_filter: Search filter.
        search_criteria: Search criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if search_filter is not None:
        kwargs["SearchFilter"] = search_filter
    if search_criteria is not None:
        kwargs["SearchCriteria"] = search_criteria
    try:
        resp = client.search_users(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search users") from exc
    return SearchUsersResult(
        users=resp.get("Users"),
        next_token=resp.get("NextToken"),
        approximate_total_count=resp.get("ApproximateTotalCount"),
    )


def search_vocabularies(
    instance_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    state: str | None = None,
    name_starts_with: str | None = None,
    language_code: str | None = None,
    region_name: str | None = None,
) -> SearchVocabulariesResult:
    """Search vocabularies.

    Args:
        instance_id: Instance id.
        max_results: Max results.
        next_token: Next token.
        state: State.
        name_starts_with: Name starts with.
        language_code: Language code.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if state is not None:
        kwargs["State"] = state
    if name_starts_with is not None:
        kwargs["NameStartsWith"] = name_starts_with
    if language_code is not None:
        kwargs["LanguageCode"] = language_code
    try:
        resp = client.search_vocabularies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to search vocabularies") from exc
    return SearchVocabulariesResult(
        vocabulary_summary_list=resp.get("VocabularySummaryList"),
        next_token=resp.get("NextToken"),
    )


def send_chat_integration_event(
    source_id: str,
    destination_id: str,
    event: dict[str, Any],
    *,
    subtype: str | None = None,
    new_session_details: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SendChatIntegrationEventResult:
    """Send chat integration event.

    Args:
        source_id: Source id.
        destination_id: Destination id.
        event: Event.
        subtype: Subtype.
        new_session_details: New session details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceId"] = source_id
    kwargs["DestinationId"] = destination_id
    kwargs["Event"] = event
    if subtype is not None:
        kwargs["Subtype"] = subtype
    if new_session_details is not None:
        kwargs["NewSessionDetails"] = new_session_details
    try:
        resp = client.send_chat_integration_event(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send chat integration event") from exc
    return SendChatIntegrationEventResult(
        initial_contact_id=resp.get("InitialContactId"),
        new_chat_created=resp.get("NewChatCreated"),
    )


def send_outbound_email(
    instance_id: str,
    from_email_address: dict[str, Any],
    destination_email_address: dict[str, Any],
    email_message: dict[str, Any],
    traffic_type: str,
    *,
    additional_recipients: dict[str, Any] | None = None,
    source_campaign: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Send outbound email.

    Args:
        instance_id: Instance id.
        from_email_address: From email address.
        destination_email_address: Destination email address.
        email_message: Email message.
        traffic_type: Traffic type.
        additional_recipients: Additional recipients.
        source_campaign: Source campaign.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FromEmailAddress"] = from_email_address
    kwargs["DestinationEmailAddress"] = destination_email_address
    kwargs["EmailMessage"] = email_message
    kwargs["TrafficType"] = traffic_type
    if additional_recipients is not None:
        kwargs["AdditionalRecipients"] = additional_recipients
    if source_campaign is not None:
        kwargs["SourceCampaign"] = source_campaign
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.send_outbound_email(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to send outbound email") from exc
    return None


def start_attached_file_upload(
    instance_id: str,
    file_name: str,
    file_size_in_bytes: int,
    file_use_case_type: str,
    associated_resource_arn: str,
    *,
    client_token: str | None = None,
    url_expiry_in_seconds: int | None = None,
    created_by: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartAttachedFileUploadResult:
    """Start attached file upload.

    Args:
        instance_id: Instance id.
        file_name: File name.
        file_size_in_bytes: File size in bytes.
        file_use_case_type: File use case type.
        associated_resource_arn: Associated resource arn.
        client_token: Client token.
        url_expiry_in_seconds: Url expiry in seconds.
        created_by: Created by.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FileName"] = file_name
    kwargs["FileSizeInBytes"] = file_size_in_bytes
    kwargs["FileUseCaseType"] = file_use_case_type
    kwargs["AssociatedResourceArn"] = associated_resource_arn
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if url_expiry_in_seconds is not None:
        kwargs["UrlExpiryInSeconds"] = url_expiry_in_seconds
    if created_by is not None:
        kwargs["CreatedBy"] = created_by
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_attached_file_upload(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start attached file upload") from exc
    return StartAttachedFileUploadResult(
        file_arn=resp.get("FileArn"),
        file_id=resp.get("FileId"),
        creation_time=resp.get("CreationTime"),
        file_status=resp.get("FileStatus"),
        created_by=resp.get("CreatedBy"),
        upload_url_metadata=resp.get("UploadUrlMetadata"),
    )


def start_contact_evaluation(
    instance_id: str,
    contact_id: str,
    evaluation_form_id: str,
    *,
    auto_evaluation_configuration: dict[str, Any] | None = None,
    client_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartContactEvaluationResult:
    """Start contact evaluation.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        evaluation_form_id: Evaluation form id.
        auto_evaluation_configuration: Auto evaluation configuration.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    if auto_evaluation_configuration is not None:
        kwargs["AutoEvaluationConfiguration"] = auto_evaluation_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.start_contact_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start contact evaluation") from exc
    return StartContactEvaluationResult(
        evaluation_id=resp.get("EvaluationId"),
        evaluation_arn=resp.get("EvaluationArn"),
    )


def start_contact_recording(
    instance_id: str,
    contact_id: str,
    initial_contact_id: str,
    voice_recording_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Start contact recording.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        initial_contact_id: Initial contact id.
        voice_recording_configuration: Voice recording configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["InitialContactId"] = initial_contact_id
    kwargs["VoiceRecordingConfiguration"] = voice_recording_configuration
    try:
        client.start_contact_recording(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start contact recording") from exc
    return None


def start_contact_streaming(
    instance_id: str,
    contact_id: str,
    chat_streaming_configuration: dict[str, Any],
    client_token: str,
    region_name: str | None = None,
) -> StartContactStreamingResult:
    """Start contact streaming.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        chat_streaming_configuration: Chat streaming configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["ChatStreamingConfiguration"] = chat_streaming_configuration
    kwargs["ClientToken"] = client_token
    try:
        resp = client.start_contact_streaming(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start contact streaming") from exc
    return StartContactStreamingResult(
        streaming_id=resp.get("StreamingId"),
    )


def start_email_contact(
    instance_id: str,
    from_email_address: dict[str, Any],
    destination_email_address: str,
    email_message: dict[str, Any],
    *,
    description: str | None = None,
    references: dict[str, Any] | None = None,
    name: str | None = None,
    additional_recipients: dict[str, Any] | None = None,
    attachments: list[dict[str, Any]] | None = None,
    contact_flow_id: str | None = None,
    related_contact_id: str | None = None,
    attributes: dict[str, Any] | None = None,
    segment_attributes: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartEmailContactResult:
    """Start email contact.

    Args:
        instance_id: Instance id.
        from_email_address: From email address.
        destination_email_address: Destination email address.
        email_message: Email message.
        description: Description.
        references: References.
        name: Name.
        additional_recipients: Additional recipients.
        attachments: Attachments.
        contact_flow_id: Contact flow id.
        related_contact_id: Related contact id.
        attributes: Attributes.
        segment_attributes: Segment attributes.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["FromEmailAddress"] = from_email_address
    kwargs["DestinationEmailAddress"] = destination_email_address
    kwargs["EmailMessage"] = email_message
    if description is not None:
        kwargs["Description"] = description
    if references is not None:
        kwargs["References"] = references
    if name is not None:
        kwargs["Name"] = name
    if additional_recipients is not None:
        kwargs["AdditionalRecipients"] = additional_recipients
    if attachments is not None:
        kwargs["Attachments"] = attachments
    if contact_flow_id is not None:
        kwargs["ContactFlowId"] = contact_flow_id
    if related_contact_id is not None:
        kwargs["RelatedContactId"] = related_contact_id
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if segment_attributes is not None:
        kwargs["SegmentAttributes"] = segment_attributes
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.start_email_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start email contact") from exc
    return StartEmailContactResult(
        contact_id=resp.get("ContactId"),
    )


def start_outbound_chat_contact(
    source_endpoint: dict[str, Any],
    destination_endpoint: dict[str, Any],
    instance_id: str,
    segment_attributes: dict[str, Any],
    contact_flow_id: str,
    *,
    attributes: dict[str, Any] | None = None,
    chat_duration_in_minutes: int | None = None,
    participant_details: dict[str, Any] | None = None,
    initial_system_message: dict[str, Any] | None = None,
    related_contact_id: str | None = None,
    supported_messaging_content_types: list[str] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartOutboundChatContactResult:
    """Start outbound chat contact.

    Args:
        source_endpoint: Source endpoint.
        destination_endpoint: Destination endpoint.
        instance_id: Instance id.
        segment_attributes: Segment attributes.
        contact_flow_id: Contact flow id.
        attributes: Attributes.
        chat_duration_in_minutes: Chat duration in minutes.
        participant_details: Participant details.
        initial_system_message: Initial system message.
        related_contact_id: Related contact id.
        supported_messaging_content_types: Supported messaging content types.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SourceEndpoint"] = source_endpoint
    kwargs["DestinationEndpoint"] = destination_endpoint
    kwargs["InstanceId"] = instance_id
    kwargs["SegmentAttributes"] = segment_attributes
    kwargs["ContactFlowId"] = contact_flow_id
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if chat_duration_in_minutes is not None:
        kwargs["ChatDurationInMinutes"] = chat_duration_in_minutes
    if participant_details is not None:
        kwargs["ParticipantDetails"] = participant_details
    if initial_system_message is not None:
        kwargs["InitialSystemMessage"] = initial_system_message
    if related_contact_id is not None:
        kwargs["RelatedContactId"] = related_contact_id
    if supported_messaging_content_types is not None:
        kwargs["SupportedMessagingContentTypes"] = supported_messaging_content_types
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.start_outbound_chat_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start outbound chat contact") from exc
    return StartOutboundChatContactResult(
        contact_id=resp.get("ContactId"),
    )


def start_outbound_email_contact(
    instance_id: str,
    contact_id: str,
    destination_email_address: dict[str, Any],
    email_message: dict[str, Any],
    *,
    from_email_address: dict[str, Any] | None = None,
    additional_recipients: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartOutboundEmailContactResult:
    """Start outbound email contact.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        destination_email_address: Destination email address.
        email_message: Email message.
        from_email_address: From email address.
        additional_recipients: Additional recipients.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["DestinationEmailAddress"] = destination_email_address
    kwargs["EmailMessage"] = email_message
    if from_email_address is not None:
        kwargs["FromEmailAddress"] = from_email_address
    if additional_recipients is not None:
        kwargs["AdditionalRecipients"] = additional_recipients
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.start_outbound_email_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start outbound email contact") from exc
    return StartOutboundEmailContactResult(
        contact_id=resp.get("ContactId"),
    )


def start_screen_sharing(
    instance_id: str,
    contact_id: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Start screen sharing.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.start_screen_sharing(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start screen sharing") from exc
    return None


def start_web_rtc_contact(
    contact_flow_id: str,
    instance_id: str,
    participant_details: dict[str, Any],
    *,
    attributes: dict[str, Any] | None = None,
    client_token: str | None = None,
    allowed_capabilities: dict[str, Any] | None = None,
    related_contact_id: str | None = None,
    references: dict[str, Any] | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> StartWebRtcContactResult:
    """Start web rtc contact.

    Args:
        contact_flow_id: Contact flow id.
        instance_id: Instance id.
        participant_details: Participant details.
        attributes: Attributes.
        client_token: Client token.
        allowed_capabilities: Allowed capabilities.
        related_contact_id: Related contact id.
        references: References.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactFlowId"] = contact_flow_id
    kwargs["InstanceId"] = instance_id
    kwargs["ParticipantDetails"] = participant_details
    if attributes is not None:
        kwargs["Attributes"] = attributes
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if allowed_capabilities is not None:
        kwargs["AllowedCapabilities"] = allowed_capabilities
    if related_contact_id is not None:
        kwargs["RelatedContactId"] = related_contact_id
    if references is not None:
        kwargs["References"] = references
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = client.start_web_rtc_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start web rtc contact") from exc
    return StartWebRtcContactResult(
        connection_data=resp.get("ConnectionData"),
        contact_id=resp.get("ContactId"),
        participant_id=resp.get("ParticipantId"),
        participant_token=resp.get("ParticipantToken"),
    )


def stop_contact_recording(
    instance_id: str,
    contact_id: str,
    initial_contact_id: str,
    *,
    contact_recording_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Stop contact recording.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        initial_contact_id: Initial contact id.
        contact_recording_type: Contact recording type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["InitialContactId"] = initial_contact_id
    if contact_recording_type is not None:
        kwargs["ContactRecordingType"] = contact_recording_type
    try:
        client.stop_contact_recording(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop contact recording") from exc
    return None


def stop_contact_streaming(
    instance_id: str,
    contact_id: str,
    streaming_id: str,
    region_name: str | None = None,
) -> None:
    """Stop contact streaming.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        streaming_id: Streaming id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["StreamingId"] = streaming_id
    try:
        client.stop_contact_streaming(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop contact streaming") from exc
    return None


def submit_contact_evaluation(
    instance_id: str,
    evaluation_id: str,
    *,
    answers: dict[str, Any] | None = None,
    notes: dict[str, Any] | None = None,
    submitted_by: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> SubmitContactEvaluationResult:
    """Submit contact evaluation.

    Args:
        instance_id: Instance id.
        evaluation_id: Evaluation id.
        answers: Answers.
        notes: Notes.
        submitted_by: Submitted by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationId"] = evaluation_id
    if answers is not None:
        kwargs["Answers"] = answers
    if notes is not None:
        kwargs["Notes"] = notes
    if submitted_by is not None:
        kwargs["SubmittedBy"] = submitted_by
    try:
        resp = client.submit_contact_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to submit contact evaluation") from exc
    return SubmitContactEvaluationResult(
        evaluation_id=resp.get("EvaluationId"),
        evaluation_arn=resp.get("EvaluationArn"),
    )


def suspend_contact_recording(
    instance_id: str,
    contact_id: str,
    initial_contact_id: str,
    *,
    contact_recording_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Suspend contact recording.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        initial_contact_id: Initial contact id.
        contact_recording_type: Contact recording type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["InitialContactId"] = initial_contact_id
    if contact_recording_type is not None:
        kwargs["ContactRecordingType"] = contact_recording_type
    try:
        client.suspend_contact_recording(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to suspend contact recording") from exc
    return None


def tag_contact(
    contact_id: str,
    instance_id: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag contact.

    Args:
        contact_id: Contact id.
        instance_id: Instance id.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactId"] = contact_id
    kwargs["InstanceId"] = instance_id
    kwargs["Tags"] = tags
    try:
        client.tag_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag contact") from exc
    return None


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def transfer_contact(
    instance_id: str,
    contact_id: str,
    contact_flow_id: str,
    *,
    queue_id: str | None = None,
    user_id: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> TransferContactResult:
    """Transfer contact.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        contact_flow_id: Contact flow id.
        queue_id: Queue id.
        user_id: User id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["ContactFlowId"] = contact_flow_id
    if queue_id is not None:
        kwargs["QueueId"] = queue_id
    if user_id is not None:
        kwargs["UserId"] = user_id
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.transfer_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to transfer contact") from exc
    return TransferContactResult(
        contact_id=resp.get("ContactId"),
        contact_arn=resp.get("ContactArn"),
    )


def untag_contact(
    contact_id: str,
    instance_id: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag contact.

    Args:
        contact_id: Contact id.
        instance_id: Instance id.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ContactId"] = contact_id
    kwargs["InstanceId"] = instance_id
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag contact") from exc
    return None


def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_agent_status(
    instance_id: str,
    agent_status_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    state: str | None = None,
    display_order: int | None = None,
    reset_order_number: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update agent status.

    Args:
        instance_id: Instance id.
        agent_status_id: Agent status id.
        name: Name.
        description: Description.
        state: State.
        display_order: Display order.
        reset_order_number: Reset order number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AgentStatusId"] = agent_status_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if state is not None:
        kwargs["State"] = state
    if display_order is not None:
        kwargs["DisplayOrder"] = display_order
    if reset_order_number is not None:
        kwargs["ResetOrderNumber"] = reset_order_number
    try:
        client.update_agent_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update agent status") from exc
    return None


def update_authentication_profile(
    authentication_profile_id: str,
    instance_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    allowed_ips: list[str] | None = None,
    blocked_ips: list[str] | None = None,
    periodic_session_duration: int | None = None,
    session_inactivity_duration: int | None = None,
    session_inactivity_handling_enabled: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update authentication profile.

    Args:
        authentication_profile_id: Authentication profile id.
        instance_id: Instance id.
        name: Name.
        description: Description.
        allowed_ips: Allowed ips.
        blocked_ips: Blocked ips.
        periodic_session_duration: Periodic session duration.
        session_inactivity_duration: Session inactivity duration.
        session_inactivity_handling_enabled: Session inactivity handling enabled.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthenticationProfileId"] = authentication_profile_id
    kwargs["InstanceId"] = instance_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if allowed_ips is not None:
        kwargs["AllowedIps"] = allowed_ips
    if blocked_ips is not None:
        kwargs["BlockedIps"] = blocked_ips
    if periodic_session_duration is not None:
        kwargs["PeriodicSessionDuration"] = periodic_session_duration
    if session_inactivity_duration is not None:
        kwargs["SessionInactivityDuration"] = session_inactivity_duration
    if session_inactivity_handling_enabled is not None:
        kwargs["SessionInactivityHandlingEnabled"] = session_inactivity_handling_enabled
    try:
        client.update_authentication_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update authentication profile") from exc
    return None


def update_contact(
    instance_id: str,
    contact_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    references: dict[str, Any] | None = None,
    segment_attributes: dict[str, Any] | None = None,
    queue_info: dict[str, Any] | None = None,
    user_info: dict[str, Any] | None = None,
    customer_endpoint: dict[str, Any] | None = None,
    system_endpoint: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update contact.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        name: Name.
        description: Description.
        references: References.
        segment_attributes: Segment attributes.
        queue_info: Queue info.
        user_info: User info.
        customer_endpoint: Customer endpoint.
        system_endpoint: System endpoint.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if references is not None:
        kwargs["References"] = references
    if segment_attributes is not None:
        kwargs["SegmentAttributes"] = segment_attributes
    if queue_info is not None:
        kwargs["QueueInfo"] = queue_info
    if user_info is not None:
        kwargs["UserInfo"] = user_info
    if customer_endpoint is not None:
        kwargs["CustomerEndpoint"] = customer_endpoint
    if system_endpoint is not None:
        kwargs["SystemEndpoint"] = system_endpoint
    try:
        client.update_contact(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact") from exc
    return None


def update_contact_evaluation(
    instance_id: str,
    evaluation_id: str,
    *,
    answers: dict[str, Any] | None = None,
    notes: dict[str, Any] | None = None,
    updated_by: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateContactEvaluationResult:
    """Update contact evaluation.

    Args:
        instance_id: Instance id.
        evaluation_id: Evaluation id.
        answers: Answers.
        notes: Notes.
        updated_by: Updated by.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationId"] = evaluation_id
    if answers is not None:
        kwargs["Answers"] = answers
    if notes is not None:
        kwargs["Notes"] = notes
    if updated_by is not None:
        kwargs["UpdatedBy"] = updated_by
    try:
        resp = client.update_contact_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact evaluation") from exc
    return UpdateContactEvaluationResult(
        evaluation_id=resp.get("EvaluationId"),
        evaluation_arn=resp.get("EvaluationArn"),
    )


def update_contact_flow_metadata(
    instance_id: str,
    contact_flow_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    contact_flow_state: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update contact flow metadata.

    Args:
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        name: Name.
        description: Description.
        contact_flow_state: Contact flow state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if contact_flow_state is not None:
        kwargs["ContactFlowState"] = contact_flow_state
    try:
        client.update_contact_flow_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact flow metadata") from exc
    return None


def update_contact_flow_module_content(
    instance_id: str,
    contact_flow_module_id: str,
    content: str,
    region_name: str | None = None,
) -> None:
    """Update contact flow module content.

    Args:
        instance_id: Instance id.
        contact_flow_module_id: Contact flow module id.
        content: Content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowModuleId"] = contact_flow_module_id
    kwargs["Content"] = content
    try:
        client.update_contact_flow_module_content(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact flow module content") from exc
    return None


def update_contact_flow_module_metadata(
    instance_id: str,
    contact_flow_module_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    state: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update contact flow module metadata.

    Args:
        instance_id: Instance id.
        contact_flow_module_id: Contact flow module id.
        name: Name.
        description: Description.
        state: State.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowModuleId"] = contact_flow_module_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if state is not None:
        kwargs["State"] = state
    try:
        client.update_contact_flow_module_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact flow module metadata") from exc
    return None


def update_contact_flow_name(
    instance_id: str,
    contact_flow_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update contact flow name.

    Args:
        instance_id: Instance id.
        contact_flow_id: Contact flow id.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactFlowId"] = contact_flow_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        client.update_contact_flow_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact flow name") from exc
    return None


def update_contact_routing_data(
    instance_id: str,
    contact_id: str,
    *,
    queue_time_adjustment_seconds: int | None = None,
    queue_priority: int | None = None,
    routing_criteria: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update contact routing data.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        queue_time_adjustment_seconds: Queue time adjustment seconds.
        queue_priority: Queue priority.
        routing_criteria: Routing criteria.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    if queue_time_adjustment_seconds is not None:
        kwargs["QueueTimeAdjustmentSeconds"] = queue_time_adjustment_seconds
    if queue_priority is not None:
        kwargs["QueuePriority"] = queue_priority
    if routing_criteria is not None:
        kwargs["RoutingCriteria"] = routing_criteria
    try:
        client.update_contact_routing_data(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact routing data") from exc
    return None


def update_contact_schedule(
    instance_id: str,
    contact_id: str,
    scheduled_time: str,
    region_name: str | None = None,
) -> None:
    """Update contact schedule.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        scheduled_time: Scheduled time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["ScheduledTime"] = scheduled_time
    try:
        client.update_contact_schedule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contact schedule") from exc
    return None


def update_email_address_metadata(
    instance_id: str,
    email_address_id: str,
    *,
    description: str | None = None,
    display_name: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> UpdateEmailAddressMetadataResult:
    """Update email address metadata.

    Args:
        instance_id: Instance id.
        email_address_id: Email address id.
        description: Description.
        display_name: Display name.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EmailAddressId"] = email_address_id
    if description is not None:
        kwargs["Description"] = description
    if display_name is not None:
        kwargs["DisplayName"] = display_name
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.update_email_address_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update email address metadata") from exc
    return UpdateEmailAddressMetadataResult(
        email_address_id=resp.get("EmailAddressId"),
        email_address_arn=resp.get("EmailAddressArn"),
    )


def update_evaluation_form(
    instance_id: str,
    evaluation_form_id: str,
    evaluation_form_version: int,
    title: str,
    items: list[dict[str, Any]],
    *,
    create_new_version: bool | None = None,
    description: str | None = None,
    scoring_strategy: dict[str, Any] | None = None,
    auto_evaluation_configuration: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> UpdateEvaluationFormResult:
    """Update evaluation form.

    Args:
        instance_id: Instance id.
        evaluation_form_id: Evaluation form id.
        evaluation_form_version: Evaluation form version.
        title: Title.
        items: Items.
        create_new_version: Create new version.
        description: Description.
        scoring_strategy: Scoring strategy.
        auto_evaluation_configuration: Auto evaluation configuration.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["EvaluationFormId"] = evaluation_form_id
    kwargs["EvaluationFormVersion"] = evaluation_form_version
    kwargs["Title"] = title
    kwargs["Items"] = items
    if create_new_version is not None:
        kwargs["CreateNewVersion"] = create_new_version
    if description is not None:
        kwargs["Description"] = description
    if scoring_strategy is not None:
        kwargs["ScoringStrategy"] = scoring_strategy
    if auto_evaluation_configuration is not None:
        kwargs["AutoEvaluationConfiguration"] = auto_evaluation_configuration
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.update_evaluation_form(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update evaluation form") from exc
    return UpdateEvaluationFormResult(
        evaluation_form_id=resp.get("EvaluationFormId"),
        evaluation_form_arn=resp.get("EvaluationFormArn"),
        evaluation_form_version=resp.get("EvaluationFormVersion"),
    )


def update_hours_of_operation(
    instance_id: str,
    hours_of_operation_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    time_zone: str | None = None,
    config: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Update hours of operation.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        name: Name.
        description: Description.
        time_zone: Time zone.
        config: Config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if time_zone is not None:
        kwargs["TimeZone"] = time_zone
    if config is not None:
        kwargs["Config"] = config
    try:
        client.update_hours_of_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update hours of operation") from exc
    return None


def update_hours_of_operation_override(
    instance_id: str,
    hours_of_operation_id: str,
    hours_of_operation_override_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    config: list[dict[str, Any]] | None = None,
    effective_from: str | None = None,
    effective_till: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update hours of operation override.

    Args:
        instance_id: Instance id.
        hours_of_operation_id: Hours of operation id.
        hours_of_operation_override_id: Hours of operation override id.
        name: Name.
        description: Description.
        config: Config.
        effective_from: Effective from.
        effective_till: Effective till.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    kwargs["HoursOfOperationOverrideId"] = hours_of_operation_override_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if config is not None:
        kwargs["Config"] = config
    if effective_from is not None:
        kwargs["EffectiveFrom"] = effective_from
    if effective_till is not None:
        kwargs["EffectiveTill"] = effective_till
    try:
        client.update_hours_of_operation_override(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update hours of operation override") from exc
    return None


def update_instance_attribute(
    instance_id: str,
    attribute_type: str,
    value: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update instance attribute.

    Args:
        instance_id: Instance id.
        attribute_type: Attribute type.
        value: Value.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AttributeType"] = attribute_type
    kwargs["Value"] = value
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.update_instance_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update instance attribute") from exc
    return None


def update_instance_storage_config(
    instance_id: str,
    association_id: str,
    resource_type: str,
    storage_config: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update instance storage config.

    Args:
        instance_id: Instance id.
        association_id: Association id.
        resource_type: Resource type.
        storage_config: Storage config.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["AssociationId"] = association_id
    kwargs["ResourceType"] = resource_type
    kwargs["StorageConfig"] = storage_config
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.update_instance_storage_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update instance storage config") from exc
    return None


def update_participant_authentication(
    state: str,
    instance_id: str,
    *,
    code: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update participant authentication.

    Args:
        state: State.
        instance_id: Instance id.
        code: Code.
        error: Error.
        error_description: Error description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["State"] = state
    kwargs["InstanceId"] = instance_id
    if code is not None:
        kwargs["Code"] = code
    if error is not None:
        kwargs["Error"] = error
    if error_description is not None:
        kwargs["ErrorDescription"] = error_description
    try:
        client.update_participant_authentication(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update participant authentication") from exc
    return None


def update_participant_role_config(
    instance_id: str,
    contact_id: str,
    channel_configuration: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update participant role config.

    Args:
        instance_id: Instance id.
        contact_id: Contact id.
        channel_configuration: Channel configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ContactId"] = contact_id
    kwargs["ChannelConfiguration"] = channel_configuration
    try:
        client.update_participant_role_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update participant role config") from exc
    return None


def update_phone_number(
    phone_number_id: str,
    *,
    target_arn: str | None = None,
    instance_id: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> UpdatePhoneNumberResult:
    """Update phone number.

    Args:
        phone_number_id: Phone number id.
        target_arn: Target arn.
        instance_id: Instance id.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberId"] = phone_number_id
    if target_arn is not None:
        kwargs["TargetArn"] = target_arn
    if instance_id is not None:
        kwargs["InstanceId"] = instance_id
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.update_phone_number(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update phone number") from exc
    return UpdatePhoneNumberResult(
        phone_number_id=resp.get("PhoneNumberId"),
        phone_number_arn=resp.get("PhoneNumberArn"),
    )


def update_phone_number_metadata(
    phone_number_id: str,
    *,
    phone_number_description: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update phone number metadata.

    Args:
        phone_number_id: Phone number id.
        phone_number_description: Phone number description.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneNumberId"] = phone_number_id
    if phone_number_description is not None:
        kwargs["PhoneNumberDescription"] = phone_number_description
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        client.update_phone_number_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update phone number metadata") from exc
    return None


def update_predefined_attribute(
    instance_id: str,
    name: str,
    *,
    values: dict[str, Any] | None = None,
    purposes: list[str] | None = None,
    attribute_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update predefined attribute.

    Args:
        instance_id: Instance id.
        name: Name.
        values: Values.
        purposes: Purposes.
        attribute_configuration: Attribute configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    if values is not None:
        kwargs["Values"] = values
    if purposes is not None:
        kwargs["Purposes"] = purposes
    if attribute_configuration is not None:
        kwargs["AttributeConfiguration"] = attribute_configuration
    try:
        client.update_predefined_attribute(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update predefined attribute") from exc
    return None


def update_prompt(
    instance_id: str,
    prompt_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    s3_uri: str | None = None,
    region_name: str | None = None,
) -> UpdatePromptResult:
    """Update prompt.

    Args:
        instance_id: Instance id.
        prompt_id: Prompt id.
        name: Name.
        description: Description.
        s3_uri: S3 uri.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["PromptId"] = prompt_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if s3_uri is not None:
        kwargs["S3Uri"] = s3_uri
    try:
        resp = client.update_prompt(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update prompt") from exc
    return UpdatePromptResult(
        prompt_arn=resp.get("PromptARN"),
        prompt_id=resp.get("PromptId"),
    )


def update_queue_hours_of_operation(
    instance_id: str,
    queue_id: str,
    hours_of_operation_id: str,
    region_name: str | None = None,
) -> None:
    """Update queue hours of operation.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        hours_of_operation_id: Hours of operation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    kwargs["HoursOfOperationId"] = hours_of_operation_id
    try:
        client.update_queue_hours_of_operation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update queue hours of operation") from exc
    return None


def update_queue_max_contacts(
    instance_id: str,
    queue_id: str,
    *,
    max_contacts: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update queue max contacts.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        max_contacts: Max contacts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    if max_contacts is not None:
        kwargs["MaxContacts"] = max_contacts
    try:
        client.update_queue_max_contacts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update queue max contacts") from exc
    return None


def update_queue_name(
    instance_id: str,
    queue_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update queue name.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        client.update_queue_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update queue name") from exc
    return None


def update_queue_outbound_caller_config(
    instance_id: str,
    queue_id: str,
    outbound_caller_config: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update queue outbound caller config.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        outbound_caller_config: Outbound caller config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    kwargs["OutboundCallerConfig"] = outbound_caller_config
    try:
        client.update_queue_outbound_caller_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update queue outbound caller config") from exc
    return None


def update_queue_outbound_email_config(
    instance_id: str,
    queue_id: str,
    outbound_email_config: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update queue outbound email config.

    Args:
        instance_id: Instance id.
        queue_id: Queue id.
        outbound_email_config: Outbound email config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QueueId"] = queue_id
    kwargs["OutboundEmailConfig"] = outbound_email_config
    try:
        client.update_queue_outbound_email_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update queue outbound email config") from exc
    return None


def update_quick_connect_config(
    instance_id: str,
    quick_connect_id: str,
    quick_connect_config: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Update quick connect config.

    Args:
        instance_id: Instance id.
        quick_connect_id: Quick connect id.
        quick_connect_config: Quick connect config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QuickConnectId"] = quick_connect_id
    kwargs["QuickConnectConfig"] = quick_connect_config
    try:
        client.update_quick_connect_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update quick connect config") from exc
    return None


def update_quick_connect_name(
    instance_id: str,
    quick_connect_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update quick connect name.

    Args:
        instance_id: Instance id.
        quick_connect_id: Quick connect id.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["QuickConnectId"] = quick_connect_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        client.update_quick_connect_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update quick connect name") from exc
    return None


def update_routing_profile_agent_availability_timer(
    instance_id: str,
    routing_profile_id: str,
    agent_availability_timer: str,
    region_name: str | None = None,
) -> None:
    """Update routing profile agent availability timer.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        agent_availability_timer: Agent availability timer.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    kwargs["AgentAvailabilityTimer"] = agent_availability_timer
    try:
        client.update_routing_profile_agent_availability_timer(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to update routing profile agent availability timer"
        ) from exc
    return None


def update_routing_profile_concurrency(
    instance_id: str,
    routing_profile_id: str,
    media_concurrencies: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Update routing profile concurrency.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        media_concurrencies: Media concurrencies.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    kwargs["MediaConcurrencies"] = media_concurrencies
    try:
        client.update_routing_profile_concurrency(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update routing profile concurrency") from exc
    return None


def update_routing_profile_default_outbound_queue(
    instance_id: str,
    routing_profile_id: str,
    default_outbound_queue_id: str,
    region_name: str | None = None,
) -> None:
    """Update routing profile default outbound queue.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        default_outbound_queue_id: Default outbound queue id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    kwargs["DefaultOutboundQueueId"] = default_outbound_queue_id
    try:
        client.update_routing_profile_default_outbound_queue(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to update routing profile default outbound queue"
        ) from exc
    return None


def update_routing_profile_name(
    instance_id: str,
    routing_profile_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update routing profile name.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        client.update_routing_profile_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update routing profile name") from exc
    return None


def update_routing_profile_queues(
    instance_id: str,
    routing_profile_id: str,
    queue_configs: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Update routing profile queues.

    Args:
        instance_id: Instance id.
        routing_profile_id: Routing profile id.
        queue_configs: Queue configs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["RoutingProfileId"] = routing_profile_id
    kwargs["QueueConfigs"] = queue_configs
    try:
        client.update_routing_profile_queues(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update routing profile queues") from exc
    return None


def update_rule(
    rule_id: str,
    instance_id: str,
    name: str,
    function: str,
    actions: list[dict[str, Any]],
    publish_status: str,
    region_name: str | None = None,
) -> None:
    """Update rule.

    Args:
        rule_id: Rule id.
        instance_id: Instance id.
        name: Name.
        function: Function.
        actions: Actions.
        publish_status: Publish status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleId"] = rule_id
    kwargs["InstanceId"] = instance_id
    kwargs["Name"] = name
    kwargs["Function"] = function
    kwargs["Actions"] = actions
    kwargs["PublishStatus"] = publish_status
    try:
        client.update_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update rule") from exc
    return None


def update_security_profile(
    security_profile_id: str,
    instance_id: str,
    *,
    description: str | None = None,
    permissions: list[str] | None = None,
    allowed_access_control_tags: dict[str, Any] | None = None,
    tag_restricted_resources: list[str] | None = None,
    applications: list[dict[str, Any]] | None = None,
    hierarchy_restricted_resources: list[str] | None = None,
    allowed_access_control_hierarchy_group_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update security profile.

    Args:
        security_profile_id: Security profile id.
        instance_id: Instance id.
        description: Description.
        permissions: Permissions.
        allowed_access_control_tags: Allowed access control tags.
        tag_restricted_resources: Tag restricted resources.
        applications: Applications.
        hierarchy_restricted_resources: Hierarchy restricted resources.
        allowed_access_control_hierarchy_group_id: Allowed access control hierarchy group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityProfileId"] = security_profile_id
    kwargs["InstanceId"] = instance_id
    if description is not None:
        kwargs["Description"] = description
    if permissions is not None:
        kwargs["Permissions"] = permissions
    if allowed_access_control_tags is not None:
        kwargs["AllowedAccessControlTags"] = allowed_access_control_tags
    if tag_restricted_resources is not None:
        kwargs["TagRestrictedResources"] = tag_restricted_resources
    if applications is not None:
        kwargs["Applications"] = applications
    if hierarchy_restricted_resources is not None:
        kwargs["HierarchyRestrictedResources"] = hierarchy_restricted_resources
    if allowed_access_control_hierarchy_group_id is not None:
        kwargs["AllowedAccessControlHierarchyGroupId"] = allowed_access_control_hierarchy_group_id
    try:
        client.update_security_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update security profile") from exc
    return None


def update_task_template(
    task_template_id: str,
    instance_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    contact_flow_id: str | None = None,
    self_assign_flow_id: str | None = None,
    constraints: dict[str, Any] | None = None,
    defaults: dict[str, Any] | None = None,
    status: str | None = None,
    fields: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateTaskTemplateResult:
    """Update task template.

    Args:
        task_template_id: Task template id.
        instance_id: Instance id.
        name: Name.
        description: Description.
        contact_flow_id: Contact flow id.
        self_assign_flow_id: Self assign flow id.
        constraints: Constraints.
        defaults: Defaults.
        status: Status.
        fields: Fields.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TaskTemplateId"] = task_template_id
    kwargs["InstanceId"] = instance_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if contact_flow_id is not None:
        kwargs["ContactFlowId"] = contact_flow_id
    if self_assign_flow_id is not None:
        kwargs["SelfAssignFlowId"] = self_assign_flow_id
    if constraints is not None:
        kwargs["Constraints"] = constraints
    if defaults is not None:
        kwargs["Defaults"] = defaults
    if status is not None:
        kwargs["Status"] = status
    if fields is not None:
        kwargs["Fields"] = fields
    try:
        resp = client.update_task_template(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update task template") from exc
    return UpdateTaskTemplateResult(
        instance_id=resp.get("InstanceId"),
        id=resp.get("Id"),
        arn=resp.get("Arn"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        contact_flow_id=resp.get("ContactFlowId"),
        self_assign_flow_id=resp.get("SelfAssignFlowId"),
        constraints=resp.get("Constraints"),
        defaults=resp.get("Defaults"),
        fields=resp.get("Fields"),
        status=resp.get("Status"),
        last_modified_time=resp.get("LastModifiedTime"),
        created_time=resp.get("CreatedTime"),
    )


def update_traffic_distribution(
    id: str,
    *,
    telephony_config: dict[str, Any] | None = None,
    sign_in_config: dict[str, Any] | None = None,
    agent_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update traffic distribution.

    Args:
        id: Id.
        telephony_config: Telephony config.
        sign_in_config: Sign in config.
        agent_config: Agent config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if telephony_config is not None:
        kwargs["TelephonyConfig"] = telephony_config
    if sign_in_config is not None:
        kwargs["SignInConfig"] = sign_in_config
    if agent_config is not None:
        kwargs["AgentConfig"] = agent_config
    try:
        client.update_traffic_distribution(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update traffic distribution") from exc
    return None


def update_user_hierarchy(
    user_id: str,
    instance_id: str,
    *,
    hierarchy_group_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update user hierarchy.

    Args:
        user_id: User id.
        instance_id: Instance id.
        hierarchy_group_id: Hierarchy group id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    if hierarchy_group_id is not None:
        kwargs["HierarchyGroupId"] = hierarchy_group_id
    try:
        client.update_user_hierarchy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user hierarchy") from exc
    return None


def update_user_hierarchy_group_name(
    name: str,
    hierarchy_group_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Update user hierarchy group name.

    Args:
        name: Name.
        hierarchy_group_id: Hierarchy group id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["HierarchyGroupId"] = hierarchy_group_id
    kwargs["InstanceId"] = instance_id
    try:
        client.update_user_hierarchy_group_name(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user hierarchy group name") from exc
    return None


def update_user_hierarchy_structure(
    hierarchy_structure: dict[str, Any],
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Update user hierarchy structure.

    Args:
        hierarchy_structure: Hierarchy structure.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["HierarchyStructure"] = hierarchy_structure
    kwargs["InstanceId"] = instance_id
    try:
        client.update_user_hierarchy_structure(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user hierarchy structure") from exc
    return None


def update_user_identity_info(
    identity_info: dict[str, Any],
    user_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Update user identity info.

    Args:
        identity_info: Identity info.
        user_id: User id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["IdentityInfo"] = identity_info
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    try:
        client.update_user_identity_info(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user identity info") from exc
    return None


def update_user_phone_config(
    phone_config: dict[str, Any],
    user_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Update user phone config.

    Args:
        phone_config: Phone config.
        user_id: User id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PhoneConfig"] = phone_config
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    try:
        client.update_user_phone_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user phone config") from exc
    return None


def update_user_proficiencies(
    instance_id: str,
    user_id: str,
    user_proficiencies: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Update user proficiencies.

    Args:
        instance_id: Instance id.
        user_id: User id.
        user_proficiencies: User proficiencies.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["UserId"] = user_id
    kwargs["UserProficiencies"] = user_proficiencies
    try:
        client.update_user_proficiencies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user proficiencies") from exc
    return None


def update_user_security_profiles(
    security_profile_ids: list[str],
    user_id: str,
    instance_id: str,
    region_name: str | None = None,
) -> None:
    """Update user security profiles.

    Args:
        security_profile_ids: Security profile ids.
        user_id: User id.
        instance_id: Instance id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityProfileIds"] = security_profile_ids
    kwargs["UserId"] = user_id
    kwargs["InstanceId"] = instance_id
    try:
        client.update_user_security_profiles(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update user security profiles") from exc
    return None


def update_view_content(
    instance_id: str,
    view_id: str,
    status: str,
    content: dict[str, Any],
    region_name: str | None = None,
) -> UpdateViewContentResult:
    """Update view content.

    Args:
        instance_id: Instance id.
        view_id: View id.
        status: Status.
        content: Content.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    kwargs["Status"] = status
    kwargs["Content"] = content
    try:
        resp = client.update_view_content(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update view content") from exc
    return UpdateViewContentResult(
        view=resp.get("View"),
    )


def update_view_metadata(
    instance_id: str,
    view_id: str,
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update view metadata.

    Args:
        instance_id: Instance id.
        view_id: View id.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("connect", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["InstanceId"] = instance_id
    kwargs["ViewId"] = view_id
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        client.update_view_metadata(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update view metadata") from exc
    return None
