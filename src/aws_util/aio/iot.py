"""Native async IoT Core utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.iot import (
    AssociateSbomWithPackageVersionResult,
    AssociateTargetsWithJobResult,
    CreateAuthorizerResult,
    CreateBillingGroupResult,
    CreateCertificateFromCsrResult,
    CreateCertificateProviderResult,
    CreateCommandResult,
    CreateCustomMetricResult,
    CreateDimensionResult,
    CreateDomainConfigurationResult,
    CreateDynamicThingGroupResult,
    CreateFleetMetricResult,
    CreateJobTemplateResult,
    CreateKeysAndCertificateResult,
    CreateMitigationActionResult,
    CreateOtaUpdateResult,
    CreatePackageResult,
    CreatePackageVersionResult,
    CreatePolicyVersionResult,
    CreateProvisioningClaimResult,
    CreateProvisioningTemplateResult,
    CreateProvisioningTemplateVersionResult,
    CreateRoleAliasResult,
    CreateScheduledAuditResult,
    CreateSecurityProfileResult,
    CreateStreamResult,
    CreateTopicRuleDestinationResult,
    DeleteCommandResult,
    DescribeAccountAuditConfigurationResult,
    DescribeAuditFindingResult,
    DescribeAuditMitigationActionsTaskResult,
    DescribeAuditSuppressionResult,
    DescribeAuditTaskResult,
    DescribeAuthorizerResult,
    DescribeBillingGroupResult,
    DescribeCaCertificateResult,
    DescribeCertificateProviderResult,
    DescribeCertificateResult,
    DescribeCustomMetricResult,
    DescribeDefaultAuthorizerResult,
    DescribeDetectMitigationActionsTaskResult,
    DescribeDimensionResult,
    DescribeDomainConfigurationResult,
    DescribeEncryptionConfigurationResult,
    DescribeEndpointResult,
    DescribeEventConfigurationsResult,
    DescribeFleetMetricResult,
    DescribeIndexResult,
    DescribeJobExecutionResult,
    DescribeJobTemplateResult,
    DescribeManagedJobTemplateResult,
    DescribeMitigationActionResult,
    DescribeProvisioningTemplateResult,
    DescribeProvisioningTemplateVersionResult,
    DescribeRoleAliasResult,
    DescribeScheduledAuditResult,
    DescribeSecurityProfileResult,
    DescribeStreamResult,
    DescribeThingGroupResult,
    DescribeThingRegistrationTaskResult,
    DescribeThingTypeResult,
    GetBehaviorModelTrainingSummariesResult,
    GetBucketsAggregationResult,
    GetCardinalityResult,
    GetCommandExecutionResult,
    GetCommandResult,
    GetEffectivePoliciesResult,
    GetIndexingConfigurationResult,
    GetJobDocumentResult,
    GetLoggingOptionsResult,
    GetOtaUpdateResult,
    GetPackageConfigurationResult,
    GetPackageResult,
    GetPackageVersionResult,
    GetPercentilesResult,
    GetPolicyVersionResult,
    GetRegistrationCodeResult,
    GetStatisticsResult,
    GetThingConnectivityDataResult,
    GetTopicRuleDestinationResult,
    GetV2LoggingOptionsResult,
    IoTJob,
    IoTPolicy,
    IoTThing,
    IoTThingGroup,
    IoTThingType,
    IoTTopicRule,
    ListActiveViolationsResult,
    ListAttachedPoliciesResult,
    ListAuditFindingsResult,
    ListAuditMitigationActionsExecutionsResult,
    ListAuditMitigationActionsTasksResult,
    ListAuditSuppressionsResult,
    ListAuditTasksResult,
    ListAuthorizersResult,
    ListBillingGroupsResult,
    ListCaCertificatesResult,
    ListCertificateProvidersResult,
    ListCertificatesByCaResult,
    ListCertificatesResult,
    ListCommandExecutionsResult,
    ListCommandsResult,
    ListCustomMetricsResult,
    ListDetectMitigationActionsExecutionsResult,
    ListDetectMitigationActionsTasksResult,
    ListDimensionsResult,
    ListDomainConfigurationsResult,
    ListFleetMetricsResult,
    ListIndicesResult,
    ListJobExecutionsForJobResult,
    ListJobExecutionsForThingResult,
    ListJobTemplatesResult,
    ListManagedJobTemplatesResult,
    ListMetricValuesResult,
    ListMitigationActionsResult,
    ListOtaUpdatesResult,
    ListOutgoingCertificatesResult,
    ListPackagesResult,
    ListPackageVersionsResult,
    ListPolicyPrincipalsResult,
    ListPolicyVersionsResult,
    ListPrincipalPoliciesResult,
    ListPrincipalThingsResult,
    ListPrincipalThingsV2Result,
    ListProvisioningTemplatesResult,
    ListProvisioningTemplateVersionsResult,
    ListRelatedResourcesForAuditFindingResult,
    ListRoleAliasesResult,
    ListSbomValidationResultsResult,
    ListScheduledAuditsResult,
    ListSecurityProfilesForTargetResult,
    ListSecurityProfilesResult,
    ListStreamsResult,
    ListTagsForResourceResult,
    ListTargetsForPolicyResult,
    ListTargetsForSecurityProfileResult,
    ListThingGroupsForThingResult,
    ListThingPrincipalsResult,
    ListThingPrincipalsV2Result,
    ListThingRegistrationTaskReportsResult,
    ListThingRegistrationTasksResult,
    ListThingsInBillingGroupResult,
    ListThingsInThingGroupResult,
    ListTopicRuleDestinationsResult,
    ListV2LoggingLevelsResult,
    ListViolationEventsResult,
    RegisterCaCertificateResult,
    RegisterCertificateResult,
    RegisterCertificateWithoutCaResult,
    RegisterThingResult,
    RunAuthorizationResult,
    RunInvokeAuthorizerResult,
    SearchIndexResult,
    SetDefaultAuthorizerResult,
    StartAuditMitigationActionsTaskResult,
    StartDetectMitigationActionsTaskResult,
    StartOnDemandAuditTaskResult,
    StartThingRegistrationTaskResult,
    TransferCertificateResult,
    UpdateAuthorizerResult,
    UpdateBillingGroupResult,
    UpdateCertificateProviderResult,
    UpdateCommandResult,
    UpdateCustomMetricResult,
    UpdateDimensionResult,
    UpdateDomainConfigurationResult,
    UpdateDynamicThingGroupResult,
    UpdateMitigationActionResult,
    UpdateRoleAliasResult,
    UpdateScheduledAuditResult,
    UpdateSecurityProfileResult,
    UpdateStreamResult,
    UpdateThingGroupResult,
    ValidateSecurityProfileBehaviorsResult,
)

__all__ = [
    "AssociateSbomWithPackageVersionResult",
    "AssociateTargetsWithJobResult",
    "CreateAuthorizerResult",
    "CreateBillingGroupResult",
    "CreateCertificateFromCsrResult",
    "CreateCertificateProviderResult",
    "CreateCommandResult",
    "CreateCustomMetricResult",
    "CreateDimensionResult",
    "CreateDomainConfigurationResult",
    "CreateDynamicThingGroupResult",
    "CreateFleetMetricResult",
    "CreateJobTemplateResult",
    "CreateKeysAndCertificateResult",
    "CreateMitigationActionResult",
    "CreateOtaUpdateResult",
    "CreatePackageResult",
    "CreatePackageVersionResult",
    "CreatePolicyVersionResult",
    "CreateProvisioningClaimResult",
    "CreateProvisioningTemplateResult",
    "CreateProvisioningTemplateVersionResult",
    "CreateRoleAliasResult",
    "CreateScheduledAuditResult",
    "CreateSecurityProfileResult",
    "CreateStreamResult",
    "CreateTopicRuleDestinationResult",
    "DeleteCommandResult",
    "DescribeAccountAuditConfigurationResult",
    "DescribeAuditFindingResult",
    "DescribeAuditMitigationActionsTaskResult",
    "DescribeAuditSuppressionResult",
    "DescribeAuditTaskResult",
    "DescribeAuthorizerResult",
    "DescribeBillingGroupResult",
    "DescribeCaCertificateResult",
    "DescribeCertificateProviderResult",
    "DescribeCertificateResult",
    "DescribeCustomMetricResult",
    "DescribeDefaultAuthorizerResult",
    "DescribeDetectMitigationActionsTaskResult",
    "DescribeDimensionResult",
    "DescribeDomainConfigurationResult",
    "DescribeEncryptionConfigurationResult",
    "DescribeEndpointResult",
    "DescribeEventConfigurationsResult",
    "DescribeFleetMetricResult",
    "DescribeIndexResult",
    "DescribeJobExecutionResult",
    "DescribeJobTemplateResult",
    "DescribeManagedJobTemplateResult",
    "DescribeMitigationActionResult",
    "DescribeProvisioningTemplateResult",
    "DescribeProvisioningTemplateVersionResult",
    "DescribeRoleAliasResult",
    "DescribeScheduledAuditResult",
    "DescribeSecurityProfileResult",
    "DescribeStreamResult",
    "DescribeThingGroupResult",
    "DescribeThingRegistrationTaskResult",
    "DescribeThingTypeResult",
    "GetBehaviorModelTrainingSummariesResult",
    "GetBucketsAggregationResult",
    "GetCardinalityResult",
    "GetCommandExecutionResult",
    "GetCommandResult",
    "GetEffectivePoliciesResult",
    "GetIndexingConfigurationResult",
    "GetJobDocumentResult",
    "GetLoggingOptionsResult",
    "GetOtaUpdateResult",
    "GetPackageConfigurationResult",
    "GetPackageResult",
    "GetPackageVersionResult",
    "GetPercentilesResult",
    "GetPolicyVersionResult",
    "GetRegistrationCodeResult",
    "GetStatisticsResult",
    "GetThingConnectivityDataResult",
    "GetTopicRuleDestinationResult",
    "GetV2LoggingOptionsResult",
    "IoTJob",
    "IoTPolicy",
    "IoTThing",
    "IoTThingGroup",
    "IoTThingType",
    "IoTTopicRule",
    "ListActiveViolationsResult",
    "ListAttachedPoliciesResult",
    "ListAuditFindingsResult",
    "ListAuditMitigationActionsExecutionsResult",
    "ListAuditMitigationActionsTasksResult",
    "ListAuditSuppressionsResult",
    "ListAuditTasksResult",
    "ListAuthorizersResult",
    "ListBillingGroupsResult",
    "ListCaCertificatesResult",
    "ListCertificateProvidersResult",
    "ListCertificatesByCaResult",
    "ListCertificatesResult",
    "ListCommandExecutionsResult",
    "ListCommandsResult",
    "ListCustomMetricsResult",
    "ListDetectMitigationActionsExecutionsResult",
    "ListDetectMitigationActionsTasksResult",
    "ListDimensionsResult",
    "ListDomainConfigurationsResult",
    "ListFleetMetricsResult",
    "ListIndicesResult",
    "ListJobExecutionsForJobResult",
    "ListJobExecutionsForThingResult",
    "ListJobTemplatesResult",
    "ListManagedJobTemplatesResult",
    "ListMetricValuesResult",
    "ListMitigationActionsResult",
    "ListOtaUpdatesResult",
    "ListOutgoingCertificatesResult",
    "ListPackageVersionsResult",
    "ListPackagesResult",
    "ListPolicyPrincipalsResult",
    "ListPolicyVersionsResult",
    "ListPrincipalPoliciesResult",
    "ListPrincipalThingsResult",
    "ListPrincipalThingsV2Result",
    "ListProvisioningTemplateVersionsResult",
    "ListProvisioningTemplatesResult",
    "ListRelatedResourcesForAuditFindingResult",
    "ListRoleAliasesResult",
    "ListSbomValidationResultsResult",
    "ListScheduledAuditsResult",
    "ListSecurityProfilesForTargetResult",
    "ListSecurityProfilesResult",
    "ListStreamsResult",
    "ListTagsForResourceResult",
    "ListTargetsForPolicyResult",
    "ListTargetsForSecurityProfileResult",
    "ListThingGroupsForThingResult",
    "ListThingPrincipalsResult",
    "ListThingPrincipalsV2Result",
    "ListThingRegistrationTaskReportsResult",
    "ListThingRegistrationTasksResult",
    "ListThingsInBillingGroupResult",
    "ListThingsInThingGroupResult",
    "ListTopicRuleDestinationsResult",
    "ListV2LoggingLevelsResult",
    "ListViolationEventsResult",
    "RegisterCaCertificateResult",
    "RegisterCertificateResult",
    "RegisterCertificateWithoutCaResult",
    "RegisterThingResult",
    "RunAuthorizationResult",
    "RunInvokeAuthorizerResult",
    "SearchIndexResult",
    "SetDefaultAuthorizerResult",
    "StartAuditMitigationActionsTaskResult",
    "StartDetectMitigationActionsTaskResult",
    "StartOnDemandAuditTaskResult",
    "StartThingRegistrationTaskResult",
    "TransferCertificateResult",
    "UpdateAuthorizerResult",
    "UpdateBillingGroupResult",
    "UpdateCertificateProviderResult",
    "UpdateCommandResult",
    "UpdateCustomMetricResult",
    "UpdateDimensionResult",
    "UpdateDomainConfigurationResult",
    "UpdateDynamicThingGroupResult",
    "UpdateMitigationActionResult",
    "UpdateRoleAliasResult",
    "UpdateScheduledAuditResult",
    "UpdateSecurityProfileResult",
    "UpdateStreamResult",
    "UpdateThingGroupResult",
    "ValidateSecurityProfileBehaviorsResult",
    "accept_certificate_transfer",
    "add_thing_to_billing_group",
    "add_thing_to_thing_group",
    "associate_sbom_with_package_version",
    "associate_targets_with_job",
    "attach_policy",
    "attach_principal_policy",
    "attach_security_profile",
    "attach_thing_principal",
    "cancel_audit_mitigation_actions_task",
    "cancel_audit_task",
    "cancel_certificate_transfer",
    "cancel_detect_mitigation_actions_task",
    "cancel_job",
    "cancel_job_execution",
    "clear_default_authorizer",
    "confirm_topic_rule_destination",
    "create_audit_suppression",
    "create_authorizer",
    "create_billing_group",
    "create_certificate_from_csr",
    "create_certificate_provider",
    "create_command",
    "create_custom_metric",
    "create_dimension",
    "create_domain_configuration",
    "create_dynamic_thing_group",
    "create_fleet_metric",
    "create_job",
    "create_job_template",
    "create_keys_and_certificate",
    "create_mitigation_action",
    "create_ota_update",
    "create_package",
    "create_package_version",
    "create_policy",
    "create_policy_version",
    "create_provisioning_claim",
    "create_provisioning_template",
    "create_provisioning_template_version",
    "create_role_alias",
    "create_scheduled_audit",
    "create_security_profile",
    "create_stream",
    "create_thing",
    "create_thing_group",
    "create_thing_type",
    "create_topic_rule",
    "create_topic_rule_destination",
    "delete_account_audit_configuration",
    "delete_audit_suppression",
    "delete_authorizer",
    "delete_billing_group",
    "delete_ca_certificate",
    "delete_certificate",
    "delete_certificate_provider",
    "delete_command",
    "delete_command_execution",
    "delete_custom_metric",
    "delete_dimension",
    "delete_domain_configuration",
    "delete_dynamic_thing_group",
    "delete_fleet_metric",
    "delete_job",
    "delete_job_execution",
    "delete_job_template",
    "delete_mitigation_action",
    "delete_ota_update",
    "delete_package",
    "delete_package_version",
    "delete_policy",
    "delete_policy_version",
    "delete_provisioning_template",
    "delete_provisioning_template_version",
    "delete_registration_code",
    "delete_role_alias",
    "delete_scheduled_audit",
    "delete_security_profile",
    "delete_stream",
    "delete_thing",
    "delete_thing_group",
    "delete_thing_type",
    "delete_topic_rule",
    "delete_topic_rule_destination",
    "delete_v2_logging_level",
    "deprecate_thing_type",
    "describe_account_audit_configuration",
    "describe_audit_finding",
    "describe_audit_mitigation_actions_task",
    "describe_audit_suppression",
    "describe_audit_task",
    "describe_authorizer",
    "describe_billing_group",
    "describe_ca_certificate",
    "describe_certificate",
    "describe_certificate_provider",
    "describe_custom_metric",
    "describe_default_authorizer",
    "describe_detect_mitigation_actions_task",
    "describe_dimension",
    "describe_domain_configuration",
    "describe_encryption_configuration",
    "describe_endpoint",
    "describe_event_configurations",
    "describe_fleet_metric",
    "describe_index",
    "describe_job",
    "describe_job_execution",
    "describe_job_template",
    "describe_managed_job_template",
    "describe_mitigation_action",
    "describe_provisioning_template",
    "describe_provisioning_template_version",
    "describe_role_alias",
    "describe_scheduled_audit",
    "describe_security_profile",
    "describe_stream",
    "describe_thing",
    "describe_thing_group",
    "describe_thing_registration_task",
    "describe_thing_type",
    "detach_policy",
    "detach_principal_policy",
    "detach_security_profile",
    "detach_thing_principal",
    "disable_topic_rule",
    "disassociate_sbom_from_package_version",
    "enable_topic_rule",
    "get_behavior_model_training_summaries",
    "get_buckets_aggregation",
    "get_cardinality",
    "get_command",
    "get_command_execution",
    "get_effective_policies",
    "get_indexing_configuration",
    "get_job_document",
    "get_logging_options",
    "get_ota_update",
    "get_package",
    "get_package_configuration",
    "get_package_version",
    "get_percentiles",
    "get_policy",
    "get_policy_version",
    "get_registration_code",
    "get_statistics",
    "get_thing_connectivity_data",
    "get_topic_rule",
    "get_topic_rule_destination",
    "get_v2_logging_options",
    "list_active_violations",
    "list_attached_policies",
    "list_audit_findings",
    "list_audit_mitigation_actions_executions",
    "list_audit_mitigation_actions_tasks",
    "list_audit_suppressions",
    "list_audit_tasks",
    "list_authorizers",
    "list_billing_groups",
    "list_ca_certificates",
    "list_certificate_providers",
    "list_certificates",
    "list_certificates_by_ca",
    "list_command_executions",
    "list_commands",
    "list_custom_metrics",
    "list_detect_mitigation_actions_executions",
    "list_detect_mitigation_actions_tasks",
    "list_dimensions",
    "list_domain_configurations",
    "list_fleet_metrics",
    "list_indices",
    "list_job_executions_for_job",
    "list_job_executions_for_thing",
    "list_job_templates",
    "list_jobs",
    "list_managed_job_templates",
    "list_metric_values",
    "list_mitigation_actions",
    "list_ota_updates",
    "list_outgoing_certificates",
    "list_package_versions",
    "list_packages",
    "list_policies",
    "list_policy_principals",
    "list_policy_versions",
    "list_principal_policies",
    "list_principal_things",
    "list_principal_things_v2",
    "list_provisioning_template_versions",
    "list_provisioning_templates",
    "list_related_resources_for_audit_finding",
    "list_role_aliases",
    "list_sbom_validation_results",
    "list_scheduled_audits",
    "list_security_profiles",
    "list_security_profiles_for_target",
    "list_streams",
    "list_tags_for_resource",
    "list_targets_for_policy",
    "list_targets_for_security_profile",
    "list_thing_groups",
    "list_thing_groups_for_thing",
    "list_thing_principals",
    "list_thing_principals_v2",
    "list_thing_registration_task_reports",
    "list_thing_registration_tasks",
    "list_thing_types",
    "list_things",
    "list_things_in_billing_group",
    "list_things_in_thing_group",
    "list_topic_rule_destinations",
    "list_topic_rules",
    "list_v2_logging_levels",
    "list_violation_events",
    "put_verification_state_on_violation",
    "register_ca_certificate",
    "register_certificate",
    "register_certificate_without_ca",
    "register_thing",
    "reject_certificate_transfer",
    "remove_thing_from_billing_group",
    "remove_thing_from_thing_group",
    "replace_topic_rule",
    "run_authorization",
    "run_invoke_authorizer",
    "search_index",
    "set_default_authorizer",
    "set_default_policy_version",
    "set_logging_options",
    "set_v2_logging_level",
    "set_v2_logging_options",
    "start_audit_mitigation_actions_task",
    "start_detect_mitigation_actions_task",
    "start_on_demand_audit_task",
    "start_thing_registration_task",
    "stop_thing_registration_task",
    "tag_resource",
    "transfer_certificate",
    "untag_resource",
    "update_account_audit_configuration",
    "update_audit_suppression",
    "update_authorizer",
    "update_billing_group",
    "update_ca_certificate",
    "update_certificate",
    "update_certificate_provider",
    "update_command",
    "update_custom_metric",
    "update_dimension",
    "update_domain_configuration",
    "update_dynamic_thing_group",
    "update_encryption_configuration",
    "update_event_configurations",
    "update_fleet_metric",
    "update_indexing_configuration",
    "update_job",
    "update_mitigation_action",
    "update_package",
    "update_package_configuration",
    "update_package_version",
    "update_provisioning_template",
    "update_role_alias",
    "update_scheduled_audit",
    "update_security_profile",
    "update_stream",
    "update_thing",
    "update_thing_group",
    "update_thing_groups_for_thing",
    "update_thing_type",
    "update_topic_rule_destination",
    "validate_security_profile_behaviors",
]


# ---------------------------------------------------------------------------
# Thing operations
# ---------------------------------------------------------------------------


async def create_thing(
    thing_name: str,
    thing_type_name: str | None = None,
    attributes: dict[str, str] | None = None,
    region_name: str | None = None,
) -> IoTThing:
    """Create an IoT thing.

    Args:
        thing_name: Name for the thing.
        thing_type_name: Optional thing type to associate.
        attributes: Optional key-value attributes for the thing.
        region_name: AWS region override.

    Returns:
        An :class:`IoTThing` representing the created thing.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {"thingName": thing_name}
    if thing_type_name is not None:
        kwargs["thingTypeName"] = thing_type_name
    if attributes is not None:
        kwargs["attributePayload"] = {"attributes": attributes}
    try:
        resp = await client.call("CreateThing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_thing failed for {thing_name!r}") from exc
    return IoTThing(
        thing_name=resp.get("thingName", thing_name),
        thing_arn=resp.get("thingArn"),
        thing_type_name=thing_type_name,
        attributes=attributes,
    )


async def describe_thing(
    thing_name: str,
    region_name: str | None = None,
) -> IoTThing:
    """Describe an IoT thing.

    Args:
        thing_name: Name of the thing.
        region_name: AWS region override.

    Returns:
        An :class:`IoTThing` with the thing's details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        resp = await client.call("DescribeThing", thingName=thing_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_thing failed for {thing_name!r}") from exc
    return IoTThing(
        thing_name=resp["thingName"],
        thing_arn=resp.get("thingArn"),
        thing_type_name=resp.get("thingTypeName"),
        attributes=resp.get("attributes"),
        version=resp.get("version"),
    )


async def list_things(
    region_name: str | None = None,
) -> list[IoTThing]:
    """List all IoT things in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`IoTThing` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        items = await client.paginate("ListThings", "things")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_things failed") from exc
    return [
        IoTThing(
            thing_name=t["thingName"],
            thing_arn=t.get("thingArn"),
            thing_type_name=t.get("thingTypeName"),
            attributes=t.get("attributes"),
            version=t.get("version"),
        )
        for t in items
    ]


async def delete_thing(
    thing_name: str,
    region_name: str | None = None,
) -> None:
    """Delete an IoT thing.

    Args:
        thing_name: Name of the thing to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        await client.call("DeleteThing", thingName=thing_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_thing failed for {thing_name!r}") from exc


async def update_thing(
    thing_name: str,
    thing_type_name: str | None = None,
    attributes: dict[str, str] | None = None,
    remove_thing_type: bool = False,
    region_name: str | None = None,
) -> None:
    """Update an IoT thing.

    Args:
        thing_name: Name of the thing to update.
        thing_type_name: New thing type to associate.
        attributes: New key-value attributes (replaces existing).
        remove_thing_type: If ``True``, disassociate the current thing type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {"thingName": thing_name}
    if thing_type_name is not None:
        kwargs["thingTypeName"] = thing_type_name
    if attributes is not None:
        kwargs["attributePayload"] = {"attributes": attributes}
    if remove_thing_type:
        kwargs["removeThingType"] = True
    try:
        await client.call("UpdateThing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_thing failed for {thing_name!r}") from exc


# ---------------------------------------------------------------------------
# Thing type operations
# ---------------------------------------------------------------------------


async def create_thing_type(
    thing_type_name: str,
    searchable_attributes: list[str] | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> IoTThingType:
    """Create an IoT thing type.

    Args:
        thing_type_name: Name for the thing type.
        searchable_attributes: Optional list of searchable attribute names.
        description: Optional description for the thing type.
        region_name: AWS region override.

    Returns:
        An :class:`IoTThingType` representing the created thing type.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {"thingTypeName": thing_type_name}
    properties: dict[str, Any] = {}
    if searchable_attributes is not None:
        properties["searchableAttributes"] = searchable_attributes
    if description is not None:
        properties["thingTypeDescription"] = description
    if properties:
        kwargs["thingTypeProperties"] = properties
    try:
        resp = await client.call("CreateThingType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_thing_type failed for {thing_type_name!r}") from exc
    return IoTThingType(
        thing_type_name=resp.get("thingTypeName", thing_type_name),
        thing_type_arn=resp.get("thingTypeArn"),
    )


async def list_thing_types(
    region_name: str | None = None,
) -> list[IoTThingType]:
    """List all IoT thing types in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`IoTThingType` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        items = await client.paginate(
            "ListThingTypes",
            "thingTypes",
            token_input="nextToken",
            token_output="nextToken",
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "list_thing_types failed") from exc
    return [
        IoTThingType(
            thing_type_name=tt["thingTypeName"],
            thing_type_arn=tt.get("thingTypeArn"),
        )
        for tt in items
    ]


# ---------------------------------------------------------------------------
# Thing group operations
# ---------------------------------------------------------------------------


async def create_thing_group(
    thing_group_name: str,
    parent_group_name: str | None = None,
    region_name: str | None = None,
) -> IoTThingGroup:
    """Create an IoT thing group.

    Args:
        thing_group_name: Name for the thing group.
        parent_group_name: Optional parent group for nesting.
        region_name: AWS region override.

    Returns:
        An :class:`IoTThingGroup` representing the created group.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {"thingGroupName": thing_group_name}
    if parent_group_name is not None:
        kwargs["parentGroupName"] = parent_group_name
    try:
        resp = await client.call("CreateThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_thing_group failed for {thing_group_name!r}") from exc
    return IoTThingGroup(
        thing_group_name=resp.get("thingGroupName", thing_group_name),
        thing_group_arn=resp.get("thingGroupArn"),
    )


async def list_thing_groups(
    region_name: str | None = None,
) -> list[IoTThingGroup]:
    """List all IoT thing groups in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`IoTThingGroup` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        items = await client.paginate(
            "ListThingGroups",
            "thingGroups",
            token_input="nextToken",
            token_output="nextToken",
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "list_thing_groups failed") from exc
    return [
        IoTThingGroup(
            thing_group_name=g["groupName"],
            thing_group_arn=g.get("groupArn"),
        )
        for g in items
    ]


async def add_thing_to_thing_group(
    thing_name: str,
    thing_group_name: str,
    region_name: str | None = None,
) -> None:
    """Add an IoT thing to a thing group.

    Args:
        thing_name: Name of the thing to add.
        thing_group_name: Name of the target group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        await client.call(
            "AddThingToThingGroup",
            thingName=thing_name,
            thingGroupName=thing_group_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"add_thing_to_thing_group failed for {thing_name!r} -> {thing_group_name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Policy operations
# ---------------------------------------------------------------------------


async def create_policy(
    policy_name: str,
    policy_document: str | dict,
    region_name: str | None = None,
) -> IoTPolicy:
    """Create an IoT policy.

    Args:
        policy_name: Name for the policy.
        policy_document: JSON policy document as a string or dict.
        region_name: AWS region override.

    Returns:
        An :class:`IoTPolicy` representing the created policy.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    doc = json.dumps(policy_document) if isinstance(policy_document, dict) else policy_document
    try:
        resp = await client.call(
            "CreatePolicy",
            policyName=policy_name,
            policyDocument=doc,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_policy failed for {policy_name!r}") from exc
    return IoTPolicy(
        policy_name=resp.get("policyName", policy_name),
        policy_arn=resp.get("policyArn"),
        policy_document=resp.get("policyDocument"),
        default_version_id=resp.get("policyVersionId"),
    )


async def get_policy(
    policy_name: str,
    region_name: str | None = None,
) -> IoTPolicy:
    """Get an IoT policy by name.

    Args:
        policy_name: Name of the policy.
        region_name: AWS region override.

    Returns:
        An :class:`IoTPolicy` with full policy details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        resp = await client.call("GetPolicy", policyName=policy_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_policy failed for {policy_name!r}") from exc
    return IoTPolicy(
        policy_name=resp["policyName"],
        policy_arn=resp.get("policyArn"),
        policy_document=resp.get("policyDocument"),
        default_version_id=resp.get("defaultVersionId"),
    )


async def list_policies(
    region_name: str | None = None,
) -> list[IoTPolicy]:
    """List all IoT policies in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`IoTPolicy` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        items = await client.paginate("ListPolicies", "policies")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_policies failed") from exc
    return [
        IoTPolicy(
            policy_name=p["policyName"],
            policy_arn=p.get("policyArn"),
        )
        for p in items
    ]


async def delete_policy(
    policy_name: str,
    region_name: str | None = None,
) -> None:
    """Delete an IoT policy.

    Args:
        policy_name: Name of the policy to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        await client.call("DeletePolicy", policyName=policy_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_policy failed for {policy_name!r}") from exc


async def attach_policy(
    policy_name: str,
    target: str,
    region_name: str | None = None,
) -> None:
    """Attach an IoT policy to a target.

    Args:
        policy_name: Name of the policy to attach.
        target: ARN of the target to attach the policy to.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        await client.call("AttachPolicy", policyName=policy_name, target=target)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"attach_policy failed for {policy_name!r} -> {target!r}"
        ) from exc


async def detach_policy(
    policy_name: str,
    target: str,
    region_name: str | None = None,
) -> None:
    """Detach an IoT policy from a target.

    Args:
        policy_name: Name of the policy to detach.
        target: ARN of the target to detach from.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        await client.call("DetachPolicy", policyName=policy_name, target=target)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"detach_policy failed for {policy_name!r} -> {target!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Topic rule operations
# ---------------------------------------------------------------------------


async def create_topic_rule(
    rule_name: str,
    sql: str,
    actions: list[dict[str, Any]],
    description: str = "",
    rule_disabled: bool = False,
    region_name: str | None = None,
) -> None:
    """Create an IoT topic rule.

    Args:
        rule_name: Name for the rule.
        sql: SQL statement for the rule.
        actions: List of action dicts (e.g. Lambda, S3, etc.).
        description: Optional description for the rule.
        rule_disabled: Whether the rule should be created in disabled state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    payload: dict[str, Any] = {
        "sql": sql,
        "actions": actions,
        "description": description,
        "ruleDisabled": rule_disabled,
    }
    try:
        await client.call(
            "CreateTopicRule",
            ruleName=rule_name,
            topicRulePayload=payload,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_topic_rule failed for {rule_name!r}") from exc


async def get_topic_rule(
    rule_name: str,
    region_name: str | None = None,
) -> IoTTopicRule:
    """Get an IoT topic rule by name.

    Args:
        rule_name: Name of the rule.
        region_name: AWS region override.

    Returns:
        An :class:`IoTTopicRule` with the rule details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        resp = await client.call("GetTopicRule", ruleName=rule_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_topic_rule failed for {rule_name!r}") from exc
    rule = resp.get("rule", {})
    return IoTTopicRule(
        rule_name=rule.get("ruleName", rule_name),
        rule_arn=resp.get("ruleArn"),
        sql=rule.get("sql"),
        description=rule.get("description"),
        rule_disabled=rule.get("ruleDisabled"),
    )


async def list_topic_rules(
    region_name: str | None = None,
) -> list[IoTTopicRule]:
    """List all IoT topic rules in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`IoTTopicRule` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        items = await client.paginate("ListTopicRules", "rules")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_topic_rules failed") from exc
    return [
        IoTTopicRule(
            rule_name=r["ruleName"],
            rule_arn=r.get("ruleArn"),
            rule_disabled=r.get("ruleDisabled"),
        )
        for r in items
    ]


async def delete_topic_rule(
    rule_name: str,
    region_name: str | None = None,
) -> None:
    """Delete an IoT topic rule.

    Args:
        rule_name: Name of the rule to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        await client.call("DeleteTopicRule", ruleName=rule_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_topic_rule failed for {rule_name!r}") from exc


# ---------------------------------------------------------------------------
# Job operations
# ---------------------------------------------------------------------------


async def create_job(
    job_id: str,
    targets: list[str],
    document_source: str | None = None,
    document: str | dict | None = None,
    description: str = "",
    target_selection: str = "SNAPSHOT",
    region_name: str | None = None,
) -> IoTJob:
    """Create an IoT job.

    Args:
        job_id: Unique identifier for the job.
        targets: List of thing or thing group ARNs to target.
        document_source: S3 URL of the job document.
        document: Inline job document (string or dict, JSON-encoded).
        description: Optional job description.
        target_selection: ``"SNAPSHOT"`` (default) or ``"CONTINUOUS"``.
        region_name: AWS region override.

    Returns:
        An :class:`IoTJob` representing the created job.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {
        "jobId": job_id,
        "targets": targets,
        "description": description,
        "targetSelection": target_selection,
    }
    if document_source is not None:
        kwargs["documentSource"] = document_source
    if document is not None:
        kwargs["document"] = json.dumps(document) if isinstance(document, dict) else document
    try:
        resp = await client.call("CreateJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_job failed for {job_id!r}") from exc
    return IoTJob(
        job_id=resp.get("jobId", job_id),
        job_arn=resp.get("jobArn"),
        description=description,
        target_selection=target_selection,
        targets=targets,
    )


async def describe_job(
    job_id: str,
    region_name: str | None = None,
) -> IoTJob:
    """Describe an IoT job.

    Args:
        job_id: Identifier of the job.
        region_name: AWS region override.

    Returns:
        An :class:`IoTJob` with the job details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    try:
        resp = await client.call("DescribeJob", jobId=job_id)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_job failed for {job_id!r}") from exc
    job = resp.get("job", {})
    return IoTJob(
        job_id=job.get("jobId", job_id),
        job_arn=job.get("jobArn"),
        status=job.get("status"),
        description=job.get("description"),
        target_selection=job.get("targetSelection"),
        targets=job.get("targets"),
    )


async def list_jobs(
    status: str | None = None,
    region_name: str | None = None,
) -> list[IoTJob]:
    """List IoT jobs, optionally filtered by status.

    Args:
        status: Optional status filter (e.g. ``"IN_PROGRESS"``, ``"COMPLETED"``).
        region_name: AWS region override.

    Returns:
        A list of :class:`IoTJob` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["status"] = status
    try:
        items = await client.paginate("ListJobs", "jobs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_jobs failed") from exc
    return [
        IoTJob(
            job_id=j["jobId"],
            job_arn=j.get("jobArn"),
            status=j.get("status"),
            description=j.get("description"),
            target_selection=j.get("targetSelection"),
        )
        for j in items
    ]


async def cancel_job(
    job_id: str,
    reason_code: str = "",
    comment: str = "",
    region_name: str | None = None,
) -> None:
    """Cancel an IoT job.

    Args:
        job_id: Identifier of the job to cancel.
        reason_code: Optional machine-readable reason code.
        comment: Optional human-readable comment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {"jobId": job_id}
    if reason_code:
        kwargs["reasonCode"] = reason_code
    if comment:
        kwargs["comment"] = comment
    try:
        await client.call("CancelJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"cancel_job failed for {job_id!r}") from exc


async def accept_certificate_transfer(
    certificate_id: str,
    *,
    set_as_active: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Accept certificate transfer.

    Args:
        certificate_id: Certificate id.
        set_as_active: Set as active.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    if set_as_active is not None:
        kwargs["setAsActive"] = set_as_active
    try:
        await client.call("AcceptCertificateTransfer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to accept certificate transfer") from exc
    return None


async def add_thing_to_billing_group(
    *,
    billing_group_name: str | None = None,
    billing_group_arn: str | None = None,
    thing_name: str | None = None,
    thing_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Add thing to billing group.

    Args:
        billing_group_name: Billing group name.
        billing_group_arn: Billing group arn.
        thing_name: Thing name.
        thing_arn: Thing arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if billing_group_name is not None:
        kwargs["billingGroupName"] = billing_group_name
    if billing_group_arn is not None:
        kwargs["billingGroupArn"] = billing_group_arn
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if thing_arn is not None:
        kwargs["thingArn"] = thing_arn
    try:
        await client.call("AddThingToBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add thing to billing group") from exc
    return None


async def associate_sbom_with_package_version(
    package_name: str,
    version_name: str,
    sbom: dict[str, Any],
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> AssociateSbomWithPackageVersionResult:
    """Associate sbom with package version.

    Args:
        package_name: Package name.
        version_name: Version name.
        sbom: Sbom.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    kwargs["sbom"] = sbom
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("AssociateSbomWithPackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate sbom with package version") from exc
    return AssociateSbomWithPackageVersionResult(
        package_name=resp.get("packageName"),
        version_name=resp.get("versionName"),
        sbom=resp.get("sbom"),
        sbom_validation_status=resp.get("sbomValidationStatus"),
    )


async def associate_targets_with_job(
    targets: list[str],
    job_id: str,
    *,
    comment: str | None = None,
    namespace_id: str | None = None,
    region_name: str | None = None,
) -> AssociateTargetsWithJobResult:
    """Associate targets with job.

    Args:
        targets: Targets.
        job_id: Job id.
        comment: Comment.
        namespace_id: Namespace id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targets"] = targets
    kwargs["jobId"] = job_id
    if comment is not None:
        kwargs["comment"] = comment
    if namespace_id is not None:
        kwargs["namespaceId"] = namespace_id
    try:
        resp = await client.call("AssociateTargetsWithJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate targets with job") from exc
    return AssociateTargetsWithJobResult(
        job_arn=resp.get("jobArn"),
        job_id=resp.get("jobId"),
        description=resp.get("description"),
    )


async def attach_principal_policy(
    policy_name: str,
    principal: str,
    region_name: str | None = None,
) -> None:
    """Attach principal policy.

    Args:
        policy_name: Policy name.
        principal: Principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    kwargs["principal"] = principal
    try:
        await client.call("AttachPrincipalPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach principal policy") from exc
    return None


async def attach_security_profile(
    security_profile_name: str,
    security_profile_target_arn: str,
    region_name: str | None = None,
) -> None:
    """Attach security profile.

    Args:
        security_profile_name: Security profile name.
        security_profile_target_arn: Security profile target arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    kwargs["securityProfileTargetArn"] = security_profile_target_arn
    try:
        await client.call("AttachSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach security profile") from exc
    return None


async def attach_thing_principal(
    thing_name: str,
    principal: str,
    *,
    thing_principal_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Attach thing principal.

    Args:
        thing_name: Thing name.
        principal: Principal.
        thing_principal_type: Thing principal type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    kwargs["principal"] = principal
    if thing_principal_type is not None:
        kwargs["thingPrincipalType"] = thing_principal_type
    try:
        await client.call("AttachThingPrincipal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to attach thing principal") from exc
    return None


async def cancel_audit_mitigation_actions_task(
    task_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel audit mitigation actions task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        await client.call("CancelAuditMitigationActionsTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel audit mitigation actions task") from exc
    return None


async def cancel_audit_task(
    task_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel audit task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        await client.call("CancelAuditTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel audit task") from exc
    return None


async def cancel_certificate_transfer(
    certificate_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel certificate transfer.

    Args:
        certificate_id: Certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    try:
        await client.call("CancelCertificateTransfer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel certificate transfer") from exc
    return None


async def cancel_detect_mitigation_actions_task(
    task_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel detect mitigation actions task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        await client.call("CancelDetectMitigationActionsTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel detect mitigation actions task") from exc
    return None


async def cancel_job_execution(
    job_id: str,
    thing_name: str,
    *,
    force: bool | None = None,
    expected_version: int | None = None,
    status_details: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Cancel job execution.

    Args:
        job_id: Job id.
        thing_name: Thing name.
        force: Force.
        expected_version: Expected version.
        status_details: Status details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["thingName"] = thing_name
    if force is not None:
        kwargs["force"] = force
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    if status_details is not None:
        kwargs["statusDetails"] = status_details
    try:
        await client.call("CancelJobExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel job execution") from exc
    return None


async def clear_default_authorizer(
    region_name: str | None = None,
) -> None:
    """Clear default authorizer.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("ClearDefaultAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to clear default authorizer") from exc
    return None


async def confirm_topic_rule_destination(
    confirmation_token: str,
    region_name: str | None = None,
) -> None:
    """Confirm topic rule destination.

    Args:
        confirmation_token: Confirmation token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["confirmationToken"] = confirmation_token
    try:
        await client.call("ConfirmTopicRuleDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to confirm topic rule destination") from exc
    return None


async def create_audit_suppression(
    check_name: str,
    resource_identifier: dict[str, Any],
    client_request_token: str,
    *,
    expiration_date: str | None = None,
    suppress_indefinitely: bool | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create audit suppression.

    Args:
        check_name: Check name.
        resource_identifier: Resource identifier.
        client_request_token: Client request token.
        expiration_date: Expiration date.
        suppress_indefinitely: Suppress indefinitely.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["checkName"] = check_name
    kwargs["resourceIdentifier"] = resource_identifier
    kwargs["clientRequestToken"] = client_request_token
    if expiration_date is not None:
        kwargs["expirationDate"] = expiration_date
    if suppress_indefinitely is not None:
        kwargs["suppressIndefinitely"] = suppress_indefinitely
    if description is not None:
        kwargs["description"] = description
    try:
        await client.call("CreateAuditSuppression", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create audit suppression") from exc
    return None


async def create_authorizer(
    authorizer_name: str,
    authorizer_function_arn: str,
    *,
    token_key_name: str | None = None,
    token_signing_public_keys: dict[str, Any] | None = None,
    status: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    signing_disabled: bool | None = None,
    enable_caching_for_http: bool | None = None,
    region_name: str | None = None,
) -> CreateAuthorizerResult:
    """Create authorizer.

    Args:
        authorizer_name: Authorizer name.
        authorizer_function_arn: Authorizer function arn.
        token_key_name: Token key name.
        token_signing_public_keys: Token signing public keys.
        status: Status.
        tags: Tags.
        signing_disabled: Signing disabled.
        enable_caching_for_http: Enable caching for http.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authorizerName"] = authorizer_name
    kwargs["authorizerFunctionArn"] = authorizer_function_arn
    if token_key_name is not None:
        kwargs["tokenKeyName"] = token_key_name
    if token_signing_public_keys is not None:
        kwargs["tokenSigningPublicKeys"] = token_signing_public_keys
    if status is not None:
        kwargs["status"] = status
    if tags is not None:
        kwargs["tags"] = tags
    if signing_disabled is not None:
        kwargs["signingDisabled"] = signing_disabled
    if enable_caching_for_http is not None:
        kwargs["enableCachingForHttp"] = enable_caching_for_http
    try:
        resp = await client.call("CreateAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create authorizer") from exc
    return CreateAuthorizerResult(
        authorizer_name=resp.get("authorizerName"),
        authorizer_arn=resp.get("authorizerArn"),
    )


async def create_billing_group(
    billing_group_name: str,
    *,
    billing_group_properties: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateBillingGroupResult:
    """Create billing group.

    Args:
        billing_group_name: Billing group name.
        billing_group_properties: Billing group properties.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["billingGroupName"] = billing_group_name
    if billing_group_properties is not None:
        kwargs["billingGroupProperties"] = billing_group_properties
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create billing group") from exc
    return CreateBillingGroupResult(
        billing_group_name=resp.get("billingGroupName"),
        billing_group_arn=resp.get("billingGroupArn"),
        billing_group_id=resp.get("billingGroupId"),
    )


async def create_certificate_from_csr(
    certificate_signing_request: str,
    *,
    set_as_active: bool | None = None,
    region_name: str | None = None,
) -> CreateCertificateFromCsrResult:
    """Create certificate from csr.

    Args:
        certificate_signing_request: Certificate signing request.
        set_as_active: Set as active.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateSigningRequest"] = certificate_signing_request
    if set_as_active is not None:
        kwargs["setAsActive"] = set_as_active
    try:
        resp = await client.call("CreateCertificateFromCsr", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create certificate from csr") from exc
    return CreateCertificateFromCsrResult(
        certificate_arn=resp.get("certificateArn"),
        certificate_id=resp.get("certificateId"),
        certificate_pem=resp.get("certificatePem"),
    )


async def create_certificate_provider(
    certificate_provider_name: str,
    lambda_function_arn: str,
    account_default_for_operations: list[str],
    *,
    client_token: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCertificateProviderResult:
    """Create certificate provider.

    Args:
        certificate_provider_name: Certificate provider name.
        lambda_function_arn: Lambda function arn.
        account_default_for_operations: Account default for operations.
        client_token: Client token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateProviderName"] = certificate_provider_name
    kwargs["lambdaFunctionArn"] = lambda_function_arn
    kwargs["accountDefaultForOperations"] = account_default_for_operations
    if client_token is not None:
        kwargs["clientToken"] = client_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCertificateProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create certificate provider") from exc
    return CreateCertificateProviderResult(
        certificate_provider_name=resp.get("certificateProviderName"),
        certificate_provider_arn=resp.get("certificateProviderArn"),
    )


async def create_command(
    command_id: str,
    *,
    namespace: str | None = None,
    display_name: str | None = None,
    description: str | None = None,
    payload: dict[str, Any] | None = None,
    mandatory_parameters: list[dict[str, Any]] | None = None,
    role_arn: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCommandResult:
    """Create command.

    Args:
        command_id: Command id.
        namespace: Namespace.
        display_name: Display name.
        description: Description.
        payload: Payload.
        mandatory_parameters: Mandatory parameters.
        role_arn: Role arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commandId"] = command_id
    if namespace is not None:
        kwargs["namespace"] = namespace
    if display_name is not None:
        kwargs["displayName"] = display_name
    if description is not None:
        kwargs["description"] = description
    if payload is not None:
        kwargs["payload"] = payload
    if mandatory_parameters is not None:
        kwargs["mandatoryParameters"] = mandatory_parameters
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create command") from exc
    return CreateCommandResult(
        command_id=resp.get("commandId"),
        command_arn=resp.get("commandArn"),
    )


async def create_custom_metric(
    metric_name: str,
    metric_type: str,
    client_request_token: str,
    *,
    display_name: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateCustomMetricResult:
    """Create custom metric.

    Args:
        metric_name: Metric name.
        metric_type: Metric type.
        client_request_token: Client request token.
        display_name: Display name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    kwargs["metricType"] = metric_type
    kwargs["clientRequestToken"] = client_request_token
    if display_name is not None:
        kwargs["displayName"] = display_name
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateCustomMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create custom metric") from exc
    return CreateCustomMetricResult(
        metric_name=resp.get("metricName"),
        metric_arn=resp.get("metricArn"),
    )


async def create_dimension(
    name: str,
    type_value: str,
    string_values: list[str],
    client_request_token: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDimensionResult:
    """Create dimension.

    Args:
        name: Name.
        type_value: Type value.
        string_values: String values.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["type"] = type_value
    kwargs["stringValues"] = string_values
    kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDimension", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dimension") from exc
    return CreateDimensionResult(
        name=resp.get("name"),
        arn=resp.get("arn"),
    )


async def create_domain_configuration(
    domain_configuration_name: str,
    *,
    domain_name: str | None = None,
    server_certificate_arns: list[str] | None = None,
    validation_certificate_arn: str | None = None,
    authorizer_config: dict[str, Any] | None = None,
    service_type: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    tls_config: dict[str, Any] | None = None,
    server_certificate_config: dict[str, Any] | None = None,
    authentication_type: str | None = None,
    application_protocol: str | None = None,
    client_certificate_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDomainConfigurationResult:
    """Create domain configuration.

    Args:
        domain_configuration_name: Domain configuration name.
        domain_name: Domain name.
        server_certificate_arns: Server certificate arns.
        validation_certificate_arn: Validation certificate arn.
        authorizer_config: Authorizer config.
        service_type: Service type.
        tags: Tags.
        tls_config: Tls config.
        server_certificate_config: Server certificate config.
        authentication_type: Authentication type.
        application_protocol: Application protocol.
        client_certificate_config: Client certificate config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainConfigurationName"] = domain_configuration_name
    if domain_name is not None:
        kwargs["domainName"] = domain_name
    if server_certificate_arns is not None:
        kwargs["serverCertificateArns"] = server_certificate_arns
    if validation_certificate_arn is not None:
        kwargs["validationCertificateArn"] = validation_certificate_arn
    if authorizer_config is not None:
        kwargs["authorizerConfig"] = authorizer_config
    if service_type is not None:
        kwargs["serviceType"] = service_type
    if tags is not None:
        kwargs["tags"] = tags
    if tls_config is not None:
        kwargs["tlsConfig"] = tls_config
    if server_certificate_config is not None:
        kwargs["serverCertificateConfig"] = server_certificate_config
    if authentication_type is not None:
        kwargs["authenticationType"] = authentication_type
    if application_protocol is not None:
        kwargs["applicationProtocol"] = application_protocol
    if client_certificate_config is not None:
        kwargs["clientCertificateConfig"] = client_certificate_config
    try:
        resp = await client.call("CreateDomainConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create domain configuration") from exc
    return CreateDomainConfigurationResult(
        domain_configuration_name=resp.get("domainConfigurationName"),
        domain_configuration_arn=resp.get("domainConfigurationArn"),
    )


async def create_dynamic_thing_group(
    thing_group_name: str,
    query_string: str,
    *,
    thing_group_properties: dict[str, Any] | None = None,
    index_name: str | None = None,
    query_version: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDynamicThingGroupResult:
    """Create dynamic thing group.

    Args:
        thing_group_name: Thing group name.
        query_string: Query string.
        thing_group_properties: Thing group properties.
        index_name: Index name.
        query_version: Query version.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    kwargs["queryString"] = query_string
    if thing_group_properties is not None:
        kwargs["thingGroupProperties"] = thing_group_properties
    if index_name is not None:
        kwargs["indexName"] = index_name
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateDynamicThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create dynamic thing group") from exc
    return CreateDynamicThingGroupResult(
        thing_group_name=resp.get("thingGroupName"),
        thing_group_arn=resp.get("thingGroupArn"),
        thing_group_id=resp.get("thingGroupId"),
        index_name=resp.get("indexName"),
        query_string=resp.get("queryString"),
        query_version=resp.get("queryVersion"),
    )


async def create_fleet_metric(
    metric_name: str,
    query_string: str,
    aggregation_type: dict[str, Any],
    period: int,
    aggregation_field: str,
    *,
    description: str | None = None,
    query_version: str | None = None,
    index_name: str | None = None,
    unit: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateFleetMetricResult:
    """Create fleet metric.

    Args:
        metric_name: Metric name.
        query_string: Query string.
        aggregation_type: Aggregation type.
        period: Period.
        aggregation_field: Aggregation field.
        description: Description.
        query_version: Query version.
        index_name: Index name.
        unit: Unit.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    kwargs["queryString"] = query_string
    kwargs["aggregationType"] = aggregation_type
    kwargs["period"] = period
    kwargs["aggregationField"] = aggregation_field
    if description is not None:
        kwargs["description"] = description
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    if index_name is not None:
        kwargs["indexName"] = index_name
    if unit is not None:
        kwargs["unit"] = unit
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateFleetMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create fleet metric") from exc
    return CreateFleetMetricResult(
        metric_name=resp.get("metricName"),
        metric_arn=resp.get("metricArn"),
    )


async def create_job_template(
    job_template_id: str,
    description: str,
    *,
    job_arn: str | None = None,
    document_source: str | None = None,
    document: str | None = None,
    presigned_url_config: dict[str, Any] | None = None,
    job_executions_rollout_config: dict[str, Any] | None = None,
    abort_config: dict[str, Any] | None = None,
    timeout_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    job_executions_retry_config: dict[str, Any] | None = None,
    maintenance_windows: list[dict[str, Any]] | None = None,
    destination_package_versions: list[str] | None = None,
    region_name: str | None = None,
) -> CreateJobTemplateResult:
    """Create job template.

    Args:
        job_template_id: Job template id.
        description: Description.
        job_arn: Job arn.
        document_source: Document source.
        document: Document.
        presigned_url_config: Presigned url config.
        job_executions_rollout_config: Job executions rollout config.
        abort_config: Abort config.
        timeout_config: Timeout config.
        tags: Tags.
        job_executions_retry_config: Job executions retry config.
        maintenance_windows: Maintenance windows.
        destination_package_versions: Destination package versions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobTemplateId"] = job_template_id
    kwargs["description"] = description
    if job_arn is not None:
        kwargs["jobArn"] = job_arn
    if document_source is not None:
        kwargs["documentSource"] = document_source
    if document is not None:
        kwargs["document"] = document
    if presigned_url_config is not None:
        kwargs["presignedUrlConfig"] = presigned_url_config
    if job_executions_rollout_config is not None:
        kwargs["jobExecutionsRolloutConfig"] = job_executions_rollout_config
    if abort_config is not None:
        kwargs["abortConfig"] = abort_config
    if timeout_config is not None:
        kwargs["timeoutConfig"] = timeout_config
    if tags is not None:
        kwargs["tags"] = tags
    if job_executions_retry_config is not None:
        kwargs["jobExecutionsRetryConfig"] = job_executions_retry_config
    if maintenance_windows is not None:
        kwargs["maintenanceWindows"] = maintenance_windows
    if destination_package_versions is not None:
        kwargs["destinationPackageVersions"] = destination_package_versions
    try:
        resp = await client.call("CreateJobTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create job template") from exc
    return CreateJobTemplateResult(
        job_template_arn=resp.get("jobTemplateArn"),
        job_template_id=resp.get("jobTemplateId"),
    )


async def create_keys_and_certificate(
    *,
    set_as_active: bool | None = None,
    region_name: str | None = None,
) -> CreateKeysAndCertificateResult:
    """Create keys and certificate.

    Args:
        set_as_active: Set as active.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if set_as_active is not None:
        kwargs["setAsActive"] = set_as_active
    try:
        resp = await client.call("CreateKeysAndCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create keys and certificate") from exc
    return CreateKeysAndCertificateResult(
        certificate_arn=resp.get("certificateArn"),
        certificate_id=resp.get("certificateId"),
        certificate_pem=resp.get("certificatePem"),
        key_pair=resp.get("keyPair"),
    )


async def create_mitigation_action(
    action_name: str,
    role_arn: str,
    action_params: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateMitigationActionResult:
    """Create mitigation action.

    Args:
        action_name: Action name.
        role_arn: Role arn.
        action_params: Action params.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionName"] = action_name
    kwargs["roleArn"] = role_arn
    kwargs["actionParams"] = action_params
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateMitigationAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create mitigation action") from exc
    return CreateMitigationActionResult(
        action_arn=resp.get("actionArn"),
        action_id=resp.get("actionId"),
    )


async def create_ota_update(
    ota_update_id: str,
    targets: list[str],
    files: list[dict[str, Any]],
    role_arn: str,
    *,
    description: str | None = None,
    protocols: list[str] | None = None,
    target_selection: str | None = None,
    aws_job_executions_rollout_config: dict[str, Any] | None = None,
    aws_job_presigned_url_config: dict[str, Any] | None = None,
    aws_job_abort_config: dict[str, Any] | None = None,
    aws_job_timeout_config: dict[str, Any] | None = None,
    additional_parameters: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateOtaUpdateResult:
    """Create ota update.

    Args:
        ota_update_id: Ota update id.
        targets: Targets.
        files: Files.
        role_arn: Role arn.
        description: Description.
        protocols: Protocols.
        target_selection: Target selection.
        aws_job_executions_rollout_config: Aws job executions rollout config.
        aws_job_presigned_url_config: Aws job presigned url config.
        aws_job_abort_config: Aws job abort config.
        aws_job_timeout_config: Aws job timeout config.
        additional_parameters: Additional parameters.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["otaUpdateId"] = ota_update_id
    kwargs["targets"] = targets
    kwargs["files"] = files
    kwargs["roleArn"] = role_arn
    if description is not None:
        kwargs["description"] = description
    if protocols is not None:
        kwargs["protocols"] = protocols
    if target_selection is not None:
        kwargs["targetSelection"] = target_selection
    if aws_job_executions_rollout_config is not None:
        kwargs["awsJobExecutionsRolloutConfig"] = aws_job_executions_rollout_config
    if aws_job_presigned_url_config is not None:
        kwargs["awsJobPresignedUrlConfig"] = aws_job_presigned_url_config
    if aws_job_abort_config is not None:
        kwargs["awsJobAbortConfig"] = aws_job_abort_config
    if aws_job_timeout_config is not None:
        kwargs["awsJobTimeoutConfig"] = aws_job_timeout_config
    if additional_parameters is not None:
        kwargs["additionalParameters"] = additional_parameters
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateOTAUpdate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ota update") from exc
    return CreateOtaUpdateResult(
        ota_update_id=resp.get("otaUpdateId"),
        aws_iot_job_id=resp.get("awsIotJobId"),
        ota_update_arn=resp.get("otaUpdateArn"),
        aws_iot_job_arn=resp.get("awsIotJobArn"),
        ota_update_status=resp.get("otaUpdateStatus"),
    )


async def create_package(
    package_name: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreatePackageResult:
    """Create package.

    Args:
        package_name: Package name.
        description: Description.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("CreatePackage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create package") from exc
    return CreatePackageResult(
        package_name=resp.get("packageName"),
        package_arn=resp.get("packageArn"),
        description=resp.get("description"),
    )


async def create_package_version(
    package_name: str,
    version_name: str,
    *,
    description: str | None = None,
    attributes: dict[str, Any] | None = None,
    artifact: dict[str, Any] | None = None,
    recipe: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreatePackageVersionResult:
    """Create package version.

    Args:
        package_name: Package name.
        version_name: Version name.
        description: Description.
        attributes: Attributes.
        artifact: Artifact.
        recipe: Recipe.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    if description is not None:
        kwargs["description"] = description
    if attributes is not None:
        kwargs["attributes"] = attributes
    if artifact is not None:
        kwargs["artifact"] = artifact
    if recipe is not None:
        kwargs["recipe"] = recipe
    if tags is not None:
        kwargs["tags"] = tags
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        resp = await client.call("CreatePackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create package version") from exc
    return CreatePackageVersionResult(
        package_version_arn=resp.get("packageVersionArn"),
        package_name=resp.get("packageName"),
        version_name=resp.get("versionName"),
        description=resp.get("description"),
        attributes=resp.get("attributes"),
        status=resp.get("status"),
        error_reason=resp.get("errorReason"),
    )


async def create_policy_version(
    policy_name: str,
    policy_document: str,
    *,
    set_as_default: bool | None = None,
    region_name: str | None = None,
) -> CreatePolicyVersionResult:
    """Create policy version.

    Args:
        policy_name: Policy name.
        policy_document: Policy document.
        set_as_default: Set as default.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    kwargs["policyDocument"] = policy_document
    if set_as_default is not None:
        kwargs["setAsDefault"] = set_as_default
    try:
        resp = await client.call("CreatePolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create policy version") from exc
    return CreatePolicyVersionResult(
        policy_arn=resp.get("policyArn"),
        policy_document=resp.get("policyDocument"),
        policy_version_id=resp.get("policyVersionId"),
        is_default_version=resp.get("isDefaultVersion"),
    )


async def create_provisioning_claim(
    template_name: str,
    region_name: str | None = None,
) -> CreateProvisioningClaimResult:
    """Create provisioning claim.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    try:
        resp = await client.call("CreateProvisioningClaim", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create provisioning claim") from exc
    return CreateProvisioningClaimResult(
        certificate_id=resp.get("certificateId"),
        certificate_pem=resp.get("certificatePem"),
        key_pair=resp.get("keyPair"),
        expiration=resp.get("expiration"),
    )


async def create_provisioning_template(
    template_name: str,
    template_body: str,
    provisioning_role_arn: str,
    *,
    description: str | None = None,
    enabled: bool | None = None,
    pre_provisioning_hook: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    type_value: str | None = None,
    region_name: str | None = None,
) -> CreateProvisioningTemplateResult:
    """Create provisioning template.

    Args:
        template_name: Template name.
        template_body: Template body.
        provisioning_role_arn: Provisioning role arn.
        description: Description.
        enabled: Enabled.
        pre_provisioning_hook: Pre provisioning hook.
        tags: Tags.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    kwargs["templateBody"] = template_body
    kwargs["provisioningRoleArn"] = provisioning_role_arn
    if description is not None:
        kwargs["description"] = description
    if enabled is not None:
        kwargs["enabled"] = enabled
    if pre_provisioning_hook is not None:
        kwargs["preProvisioningHook"] = pre_provisioning_hook
    if tags is not None:
        kwargs["tags"] = tags
    if type_value is not None:
        kwargs["type"] = type_value
    try:
        resp = await client.call("CreateProvisioningTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create provisioning template") from exc
    return CreateProvisioningTemplateResult(
        template_arn=resp.get("templateArn"),
        template_name=resp.get("templateName"),
        default_version_id=resp.get("defaultVersionId"),
    )


async def create_provisioning_template_version(
    template_name: str,
    template_body: str,
    *,
    set_as_default: bool | None = None,
    region_name: str | None = None,
) -> CreateProvisioningTemplateVersionResult:
    """Create provisioning template version.

    Args:
        template_name: Template name.
        template_body: Template body.
        set_as_default: Set as default.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    kwargs["templateBody"] = template_body
    if set_as_default is not None:
        kwargs["setAsDefault"] = set_as_default
    try:
        resp = await client.call("CreateProvisioningTemplateVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create provisioning template version") from exc
    return CreateProvisioningTemplateVersionResult(
        template_arn=resp.get("templateArn"),
        template_name=resp.get("templateName"),
        version_id=resp.get("versionId"),
        is_default_version=resp.get("isDefaultVersion"),
    )


async def create_role_alias(
    role_alias: str,
    role_arn: str,
    *,
    credential_duration_seconds: int | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateRoleAliasResult:
    """Create role alias.

    Args:
        role_alias: Role alias.
        role_arn: Role arn.
        credential_duration_seconds: Credential duration seconds.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["roleAlias"] = role_alias
    kwargs["roleArn"] = role_arn
    if credential_duration_seconds is not None:
        kwargs["credentialDurationSeconds"] = credential_duration_seconds
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateRoleAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create role alias") from exc
    return CreateRoleAliasResult(
        role_alias=resp.get("roleAlias"),
        role_alias_arn=resp.get("roleAliasArn"),
    )


async def create_scheduled_audit(
    frequency: str,
    target_check_names: list[str],
    scheduled_audit_name: str,
    *,
    day_of_month: str | None = None,
    day_of_week: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateScheduledAuditResult:
    """Create scheduled audit.

    Args:
        frequency: Frequency.
        target_check_names: Target check names.
        scheduled_audit_name: Scheduled audit name.
        day_of_month: Day of month.
        day_of_week: Day of week.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["frequency"] = frequency
    kwargs["targetCheckNames"] = target_check_names
    kwargs["scheduledAuditName"] = scheduled_audit_name
    if day_of_month is not None:
        kwargs["dayOfMonth"] = day_of_month
    if day_of_week is not None:
        kwargs["dayOfWeek"] = day_of_week
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateScheduledAudit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create scheduled audit") from exc
    return CreateScheduledAuditResult(
        scheduled_audit_arn=resp.get("scheduledAuditArn"),
    )


async def create_security_profile(
    security_profile_name: str,
    *,
    security_profile_description: str | None = None,
    behaviors: list[dict[str, Any]] | None = None,
    alert_targets: dict[str, Any] | None = None,
    additional_metrics_to_retain: list[str] | None = None,
    additional_metrics_to_retain_v2: list[dict[str, Any]] | None = None,
    tags: list[dict[str, Any]] | None = None,
    metrics_export_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateSecurityProfileResult:
    """Create security profile.

    Args:
        security_profile_name: Security profile name.
        security_profile_description: Security profile description.
        behaviors: Behaviors.
        alert_targets: Alert targets.
        additional_metrics_to_retain: Additional metrics to retain.
        additional_metrics_to_retain_v2: Additional metrics to retain v2.
        tags: Tags.
        metrics_export_config: Metrics export config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    if security_profile_description is not None:
        kwargs["securityProfileDescription"] = security_profile_description
    if behaviors is not None:
        kwargs["behaviors"] = behaviors
    if alert_targets is not None:
        kwargs["alertTargets"] = alert_targets
    if additional_metrics_to_retain is not None:
        kwargs["additionalMetricsToRetain"] = additional_metrics_to_retain
    if additional_metrics_to_retain_v2 is not None:
        kwargs["additionalMetricsToRetainV2"] = additional_metrics_to_retain_v2
    if tags is not None:
        kwargs["tags"] = tags
    if metrics_export_config is not None:
        kwargs["metricsExportConfig"] = metrics_export_config
    try:
        resp = await client.call("CreateSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create security profile") from exc
    return CreateSecurityProfileResult(
        security_profile_name=resp.get("securityProfileName"),
        security_profile_arn=resp.get("securityProfileArn"),
    )


async def create_stream(
    stream_id: str,
    files: list[dict[str, Any]],
    role_arn: str,
    *,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateStreamResult:
    """Create stream.

    Args:
        stream_id: Stream id.
        files: Files.
        role_arn: Role arn.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["streamId"] = stream_id
    kwargs["files"] = files
    kwargs["roleArn"] = role_arn
    if description is not None:
        kwargs["description"] = description
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create stream") from exc
    return CreateStreamResult(
        stream_id=resp.get("streamId"),
        stream_arn=resp.get("streamArn"),
        description=resp.get("description"),
        stream_version=resp.get("streamVersion"),
    )


async def create_topic_rule_destination(
    destination_configuration: dict[str, Any],
    region_name: str | None = None,
) -> CreateTopicRuleDestinationResult:
    """Create topic rule destination.

    Args:
        destination_configuration: Destination configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["destinationConfiguration"] = destination_configuration
    try:
        resp = await client.call("CreateTopicRuleDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create topic rule destination") from exc
    return CreateTopicRuleDestinationResult(
        topic_rule_destination=resp.get("topicRuleDestination"),
    )


async def delete_account_audit_configuration(
    *,
    delete_scheduled_audits: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete account audit configuration.

    Args:
        delete_scheduled_audits: Delete scheduled audits.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if delete_scheduled_audits is not None:
        kwargs["deleteScheduledAudits"] = delete_scheduled_audits
    try:
        await client.call("DeleteAccountAuditConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete account audit configuration") from exc
    return None


async def delete_audit_suppression(
    check_name: str,
    resource_identifier: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Delete audit suppression.

    Args:
        check_name: Check name.
        resource_identifier: Resource identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["checkName"] = check_name
    kwargs["resourceIdentifier"] = resource_identifier
    try:
        await client.call("DeleteAuditSuppression", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete audit suppression") from exc
    return None


async def delete_authorizer(
    authorizer_name: str,
    region_name: str | None = None,
) -> None:
    """Delete authorizer.

    Args:
        authorizer_name: Authorizer name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authorizerName"] = authorizer_name
    try:
        await client.call("DeleteAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete authorizer") from exc
    return None


async def delete_billing_group(
    billing_group_name: str,
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Delete billing group.

    Args:
        billing_group_name: Billing group name.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["billingGroupName"] = billing_group_name
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        await client.call("DeleteBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete billing group") from exc
    return None


async def delete_ca_certificate(
    certificate_id: str,
    region_name: str | None = None,
) -> None:
    """Delete ca certificate.

    Args:
        certificate_id: Certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    try:
        await client.call("DeleteCACertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ca certificate") from exc
    return None


async def delete_certificate(
    certificate_id: str,
    *,
    force_delete: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete certificate.

    Args:
        certificate_id: Certificate id.
        force_delete: Force delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    if force_delete is not None:
        kwargs["forceDelete"] = force_delete
    try:
        await client.call("DeleteCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete certificate") from exc
    return None


async def delete_certificate_provider(
    certificate_provider_name: str,
    region_name: str | None = None,
) -> None:
    """Delete certificate provider.

    Args:
        certificate_provider_name: Certificate provider name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateProviderName"] = certificate_provider_name
    try:
        await client.call("DeleteCertificateProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete certificate provider") from exc
    return None


async def delete_command(
    command_id: str,
    region_name: str | None = None,
) -> DeleteCommandResult:
    """Delete command.

    Args:
        command_id: Command id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commandId"] = command_id
    try:
        resp = await client.call("DeleteCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete command") from exc
    return DeleteCommandResult(
        status_code=resp.get("statusCode"),
    )


async def delete_command_execution(
    execution_id: str,
    target_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete command execution.

    Args:
        execution_id: Execution id.
        target_arn: Target arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["executionId"] = execution_id
    kwargs["targetArn"] = target_arn
    try:
        await client.call("DeleteCommandExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete command execution") from exc
    return None


async def delete_custom_metric(
    metric_name: str,
    region_name: str | None = None,
) -> None:
    """Delete custom metric.

    Args:
        metric_name: Metric name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    try:
        await client.call("DeleteCustomMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete custom metric") from exc
    return None


async def delete_dimension(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete dimension.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    try:
        await client.call("DeleteDimension", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dimension") from exc
    return None


async def delete_domain_configuration(
    domain_configuration_name: str,
    region_name: str | None = None,
) -> None:
    """Delete domain configuration.

    Args:
        domain_configuration_name: Domain configuration name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainConfigurationName"] = domain_configuration_name
    try:
        await client.call("DeleteDomainConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete domain configuration") from exc
    return None


async def delete_dynamic_thing_group(
    thing_group_name: str,
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Delete dynamic thing group.

    Args:
        thing_group_name: Thing group name.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        await client.call("DeleteDynamicThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete dynamic thing group") from exc
    return None


async def delete_fleet_metric(
    metric_name: str,
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Delete fleet metric.

    Args:
        metric_name: Metric name.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        await client.call("DeleteFleetMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete fleet metric") from exc
    return None


async def delete_job(
    job_id: str,
    *,
    force: bool | None = None,
    namespace_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete job.

    Args:
        job_id: Job id.
        force: Force.
        namespace_id: Namespace id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    if force is not None:
        kwargs["force"] = force
    if namespace_id is not None:
        kwargs["namespaceId"] = namespace_id
    try:
        await client.call("DeleteJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete job") from exc
    return None


async def delete_job_execution(
    job_id: str,
    thing_name: str,
    execution_number: int,
    *,
    force: bool | None = None,
    namespace_id: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete job execution.

    Args:
        job_id: Job id.
        thing_name: Thing name.
        execution_number: Execution number.
        force: Force.
        namespace_id: Namespace id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["thingName"] = thing_name
    kwargs["executionNumber"] = execution_number
    if force is not None:
        kwargs["force"] = force
    if namespace_id is not None:
        kwargs["namespaceId"] = namespace_id
    try:
        await client.call("DeleteJobExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete job execution") from exc
    return None


async def delete_job_template(
    job_template_id: str,
    region_name: str | None = None,
) -> None:
    """Delete job template.

    Args:
        job_template_id: Job template id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobTemplateId"] = job_template_id
    try:
        await client.call("DeleteJobTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete job template") from exc
    return None


async def delete_mitigation_action(
    action_name: str,
    region_name: str | None = None,
) -> None:
    """Delete mitigation action.

    Args:
        action_name: Action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionName"] = action_name
    try:
        await client.call("DeleteMitigationAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete mitigation action") from exc
    return None


async def delete_ota_update(
    ota_update_id: str,
    *,
    delete_stream: bool | None = None,
    force_delete_aws_job: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete ota update.

    Args:
        ota_update_id: Ota update id.
        delete_stream: Delete stream.
        force_delete_aws_job: Force delete aws job.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["otaUpdateId"] = ota_update_id
    if delete_stream is not None:
        kwargs["deleteStream"] = delete_stream
    if force_delete_aws_job is not None:
        kwargs["forceDeleteAWSJob"] = force_delete_aws_job
    try:
        await client.call("DeleteOTAUpdate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete ota update") from exc
    return None


async def delete_package(
    package_name: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete package.

    Args:
        package_name: Package name.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DeletePackage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete package") from exc
    return None


async def delete_package_version(
    package_name: str,
    version_name: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete package version.

    Args:
        package_name: Package name.
        version_name: Version name.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DeletePackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete package version") from exc
    return None


async def delete_policy_version(
    policy_name: str,
    policy_version_id: str,
    region_name: str | None = None,
) -> None:
    """Delete policy version.

    Args:
        policy_name: Policy name.
        policy_version_id: Policy version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    kwargs["policyVersionId"] = policy_version_id
    try:
        await client.call("DeletePolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete policy version") from exc
    return None


async def delete_provisioning_template(
    template_name: str,
    region_name: str | None = None,
) -> None:
    """Delete provisioning template.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    try:
        await client.call("DeleteProvisioningTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete provisioning template") from exc
    return None


async def delete_provisioning_template_version(
    template_name: str,
    version_id: int,
    region_name: str | None = None,
) -> None:
    """Delete provisioning template version.

    Args:
        template_name: Template name.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    kwargs["versionId"] = version_id
    try:
        await client.call("DeleteProvisioningTemplateVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete provisioning template version") from exc
    return None


async def delete_registration_code(
    region_name: str | None = None,
) -> None:
    """Delete registration code.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DeleteRegistrationCode", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete registration code") from exc
    return None


async def delete_role_alias(
    role_alias: str,
    region_name: str | None = None,
) -> None:
    """Delete role alias.

    Args:
        role_alias: Role alias.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["roleAlias"] = role_alias
    try:
        await client.call("DeleteRoleAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete role alias") from exc
    return None


async def delete_scheduled_audit(
    scheduled_audit_name: str,
    region_name: str | None = None,
) -> None:
    """Delete scheduled audit.

    Args:
        scheduled_audit_name: Scheduled audit name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scheduledAuditName"] = scheduled_audit_name
    try:
        await client.call("DeleteScheduledAudit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete scheduled audit") from exc
    return None


async def delete_security_profile(
    security_profile_name: str,
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Delete security profile.

    Args:
        security_profile_name: Security profile name.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        await client.call("DeleteSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete security profile") from exc
    return None


async def delete_stream(
    stream_id: str,
    region_name: str | None = None,
) -> None:
    """Delete stream.

    Args:
        stream_id: Stream id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["streamId"] = stream_id
    try:
        await client.call("DeleteStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete stream") from exc
    return None


async def delete_thing_group(
    thing_group_name: str,
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Delete thing group.

    Args:
        thing_group_name: Thing group name.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        await client.call("DeleteThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete thing group") from exc
    return None


async def delete_thing_type(
    thing_type_name: str,
    region_name: str | None = None,
) -> None:
    """Delete thing type.

    Args:
        thing_type_name: Thing type name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingTypeName"] = thing_type_name
    try:
        await client.call("DeleteThingType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete thing type") from exc
    return None


async def delete_topic_rule_destination(
    arn: str,
    region_name: str | None = None,
) -> None:
    """Delete topic rule destination.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        await client.call("DeleteTopicRuleDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete topic rule destination") from exc
    return None


async def delete_v2_logging_level(
    target_type: str,
    target_name: str,
    region_name: str | None = None,
) -> None:
    """Delete v2 logging level.

    Args:
        target_type: Target type.
        target_name: Target name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetType"] = target_type
    kwargs["targetName"] = target_name
    try:
        await client.call("DeleteV2LoggingLevel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete v2 logging level") from exc
    return None


async def deprecate_thing_type(
    thing_type_name: str,
    *,
    undo_deprecate: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Deprecate thing type.

    Args:
        thing_type_name: Thing type name.
        undo_deprecate: Undo deprecate.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingTypeName"] = thing_type_name
    if undo_deprecate is not None:
        kwargs["undoDeprecate"] = undo_deprecate
    try:
        await client.call("DeprecateThingType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deprecate thing type") from exc
    return None


async def describe_account_audit_configuration(
    region_name: str | None = None,
) -> DescribeAccountAuditConfigurationResult:
    """Describe account audit configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAccountAuditConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account audit configuration") from exc
    return DescribeAccountAuditConfigurationResult(
        role_arn=resp.get("roleArn"),
        audit_notification_target_configurations=resp.get("auditNotificationTargetConfigurations"),
        audit_check_configurations=resp.get("auditCheckConfigurations"),
    )


async def describe_audit_finding(
    finding_id: str,
    region_name: str | None = None,
) -> DescribeAuditFindingResult:
    """Describe audit finding.

    Args:
        finding_id: Finding id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["findingId"] = finding_id
    try:
        resp = await client.call("DescribeAuditFinding", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe audit finding") from exc
    return DescribeAuditFindingResult(
        finding=resp.get("finding"),
    )


async def describe_audit_mitigation_actions_task(
    task_id: str,
    region_name: str | None = None,
) -> DescribeAuditMitigationActionsTaskResult:
    """Describe audit mitigation actions task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        resp = await client.call("DescribeAuditMitigationActionsTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe audit mitigation actions task") from exc
    return DescribeAuditMitigationActionsTaskResult(
        task_status=resp.get("taskStatus"),
        start_time=resp.get("startTime"),
        end_time=resp.get("endTime"),
        task_statistics=resp.get("taskStatistics"),
        target=resp.get("target"),
        audit_check_to_actions_mapping=resp.get("auditCheckToActionsMapping"),
        actions_definition=resp.get("actionsDefinition"),
    )


async def describe_audit_suppression(
    check_name: str,
    resource_identifier: dict[str, Any],
    region_name: str | None = None,
) -> DescribeAuditSuppressionResult:
    """Describe audit suppression.

    Args:
        check_name: Check name.
        resource_identifier: Resource identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["checkName"] = check_name
    kwargs["resourceIdentifier"] = resource_identifier
    try:
        resp = await client.call("DescribeAuditSuppression", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe audit suppression") from exc
    return DescribeAuditSuppressionResult(
        check_name=resp.get("checkName"),
        resource_identifier=resp.get("resourceIdentifier"),
        expiration_date=resp.get("expirationDate"),
        suppress_indefinitely=resp.get("suppressIndefinitely"),
        description=resp.get("description"),
    )


async def describe_audit_task(
    task_id: str,
    region_name: str | None = None,
) -> DescribeAuditTaskResult:
    """Describe audit task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        resp = await client.call("DescribeAuditTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe audit task") from exc
    return DescribeAuditTaskResult(
        task_status=resp.get("taskStatus"),
        task_type=resp.get("taskType"),
        task_start_time=resp.get("taskStartTime"),
        task_statistics=resp.get("taskStatistics"),
        scheduled_audit_name=resp.get("scheduledAuditName"),
        audit_details=resp.get("auditDetails"),
    )


async def describe_authorizer(
    authorizer_name: str,
    region_name: str | None = None,
) -> DescribeAuthorizerResult:
    """Describe authorizer.

    Args:
        authorizer_name: Authorizer name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authorizerName"] = authorizer_name
    try:
        resp = await client.call("DescribeAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe authorizer") from exc
    return DescribeAuthorizerResult(
        authorizer_description=resp.get("authorizerDescription"),
    )


async def describe_billing_group(
    billing_group_name: str,
    region_name: str | None = None,
) -> DescribeBillingGroupResult:
    """Describe billing group.

    Args:
        billing_group_name: Billing group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["billingGroupName"] = billing_group_name
    try:
        resp = await client.call("DescribeBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe billing group") from exc
    return DescribeBillingGroupResult(
        billing_group_name=resp.get("billingGroupName"),
        billing_group_id=resp.get("billingGroupId"),
        billing_group_arn=resp.get("billingGroupArn"),
        version=resp.get("version"),
        billing_group_properties=resp.get("billingGroupProperties"),
        billing_group_metadata=resp.get("billingGroupMetadata"),
    )


async def describe_ca_certificate(
    certificate_id: str,
    region_name: str | None = None,
) -> DescribeCaCertificateResult:
    """Describe ca certificate.

    Args:
        certificate_id: Certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    try:
        resp = await client.call("DescribeCACertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe ca certificate") from exc
    return DescribeCaCertificateResult(
        certificate_description=resp.get("certificateDescription"),
        registration_config=resp.get("registrationConfig"),
    )


async def describe_certificate(
    certificate_id: str,
    region_name: str | None = None,
) -> DescribeCertificateResult:
    """Describe certificate.

    Args:
        certificate_id: Certificate id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    try:
        resp = await client.call("DescribeCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe certificate") from exc
    return DescribeCertificateResult(
        certificate_description=resp.get("certificateDescription"),
    )


async def describe_certificate_provider(
    certificate_provider_name: str,
    region_name: str | None = None,
) -> DescribeCertificateProviderResult:
    """Describe certificate provider.

    Args:
        certificate_provider_name: Certificate provider name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateProviderName"] = certificate_provider_name
    try:
        resp = await client.call("DescribeCertificateProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe certificate provider") from exc
    return DescribeCertificateProviderResult(
        certificate_provider_name=resp.get("certificateProviderName"),
        certificate_provider_arn=resp.get("certificateProviderArn"),
        lambda_function_arn=resp.get("lambdaFunctionArn"),
        account_default_for_operations=resp.get("accountDefaultForOperations"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def describe_custom_metric(
    metric_name: str,
    region_name: str | None = None,
) -> DescribeCustomMetricResult:
    """Describe custom metric.

    Args:
        metric_name: Metric name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    try:
        resp = await client.call("DescribeCustomMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe custom metric") from exc
    return DescribeCustomMetricResult(
        metric_name=resp.get("metricName"),
        metric_arn=resp.get("metricArn"),
        metric_type=resp.get("metricType"),
        display_name=resp.get("displayName"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def describe_default_authorizer(
    region_name: str | None = None,
) -> DescribeDefaultAuthorizerResult:
    """Describe default authorizer.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeDefaultAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe default authorizer") from exc
    return DescribeDefaultAuthorizerResult(
        authorizer_description=resp.get("authorizerDescription"),
    )


async def describe_detect_mitigation_actions_task(
    task_id: str,
    region_name: str | None = None,
) -> DescribeDetectMitigationActionsTaskResult:
    """Describe detect mitigation actions task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        resp = await client.call("DescribeDetectMitigationActionsTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe detect mitigation actions task") from exc
    return DescribeDetectMitigationActionsTaskResult(
        task_summary=resp.get("taskSummary"),
    )


async def describe_dimension(
    name: str,
    region_name: str | None = None,
) -> DescribeDimensionResult:
    """Describe dimension.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    try:
        resp = await client.call("DescribeDimension", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe dimension") from exc
    return DescribeDimensionResult(
        name=resp.get("name"),
        arn=resp.get("arn"),
        type_value=resp.get("type"),
        string_values=resp.get("stringValues"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def describe_domain_configuration(
    domain_configuration_name: str,
    region_name: str | None = None,
) -> DescribeDomainConfigurationResult:
    """Describe domain configuration.

    Args:
        domain_configuration_name: Domain configuration name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainConfigurationName"] = domain_configuration_name
    try:
        resp = await client.call("DescribeDomainConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe domain configuration") from exc
    return DescribeDomainConfigurationResult(
        domain_configuration_name=resp.get("domainConfigurationName"),
        domain_configuration_arn=resp.get("domainConfigurationArn"),
        domain_name=resp.get("domainName"),
        server_certificates=resp.get("serverCertificates"),
        authorizer_config=resp.get("authorizerConfig"),
        domain_configuration_status=resp.get("domainConfigurationStatus"),
        service_type=resp.get("serviceType"),
        domain_type=resp.get("domainType"),
        last_status_change_date=resp.get("lastStatusChangeDate"),
        tls_config=resp.get("tlsConfig"),
        server_certificate_config=resp.get("serverCertificateConfig"),
        authentication_type=resp.get("authenticationType"),
        application_protocol=resp.get("applicationProtocol"),
        client_certificate_config=resp.get("clientCertificateConfig"),
    )


async def describe_encryption_configuration(
    region_name: str | None = None,
) -> DescribeEncryptionConfigurationResult:
    """Describe encryption configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeEncryptionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe encryption configuration") from exc
    return DescribeEncryptionConfigurationResult(
        encryption_type=resp.get("encryptionType"),
        kms_key_arn=resp.get("kmsKeyArn"),
        kms_access_role_arn=resp.get("kmsAccessRoleArn"),
        configuration_details=resp.get("configurationDetails"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def describe_endpoint(
    *,
    endpoint_type: str | None = None,
    region_name: str | None = None,
) -> DescribeEndpointResult:
    """Describe endpoint.

    Args:
        endpoint_type: Endpoint type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if endpoint_type is not None:
        kwargs["endpointType"] = endpoint_type
    try:
        resp = await client.call("DescribeEndpoint", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoint") from exc
    return DescribeEndpointResult(
        endpoint_address=resp.get("endpointAddress"),
    )


async def describe_event_configurations(
    region_name: str | None = None,
) -> DescribeEventConfigurationsResult:
    """Describe event configurations.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeEventConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe event configurations") from exc
    return DescribeEventConfigurationsResult(
        event_configurations=resp.get("eventConfigurations"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def describe_fleet_metric(
    metric_name: str,
    region_name: str | None = None,
) -> DescribeFleetMetricResult:
    """Describe fleet metric.

    Args:
        metric_name: Metric name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    try:
        resp = await client.call("DescribeFleetMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe fleet metric") from exc
    return DescribeFleetMetricResult(
        metric_name=resp.get("metricName"),
        query_string=resp.get("queryString"),
        aggregation_type=resp.get("aggregationType"),
        period=resp.get("period"),
        aggregation_field=resp.get("aggregationField"),
        description=resp.get("description"),
        query_version=resp.get("queryVersion"),
        index_name=resp.get("indexName"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        unit=resp.get("unit"),
        version=resp.get("version"),
        metric_arn=resp.get("metricArn"),
    )


async def describe_index(
    index_name: str,
    region_name: str | None = None,
) -> DescribeIndexResult:
    """Describe index.

    Args:
        index_name: Index name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["indexName"] = index_name
    try:
        resp = await client.call("DescribeIndex", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe index") from exc
    return DescribeIndexResult(
        index_name=resp.get("indexName"),
        index_status=resp.get("indexStatus"),
        model_schema=resp.get("schema"),
    )


async def describe_job_execution(
    job_id: str,
    thing_name: str,
    *,
    execution_number: int | None = None,
    region_name: str | None = None,
) -> DescribeJobExecutionResult:
    """Describe job execution.

    Args:
        job_id: Job id.
        thing_name: Thing name.
        execution_number: Execution number.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    kwargs["thingName"] = thing_name
    if execution_number is not None:
        kwargs["executionNumber"] = execution_number
    try:
        resp = await client.call("DescribeJobExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe job execution") from exc
    return DescribeJobExecutionResult(
        execution=resp.get("execution"),
    )


async def describe_job_template(
    job_template_id: str,
    region_name: str | None = None,
) -> DescribeJobTemplateResult:
    """Describe job template.

    Args:
        job_template_id: Job template id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobTemplateId"] = job_template_id
    try:
        resp = await client.call("DescribeJobTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe job template") from exc
    return DescribeJobTemplateResult(
        job_template_arn=resp.get("jobTemplateArn"),
        job_template_id=resp.get("jobTemplateId"),
        description=resp.get("description"),
        document_source=resp.get("documentSource"),
        document=resp.get("document"),
        created_at=resp.get("createdAt"),
        presigned_url_config=resp.get("presignedUrlConfig"),
        job_executions_rollout_config=resp.get("jobExecutionsRolloutConfig"),
        abort_config=resp.get("abortConfig"),
        timeout_config=resp.get("timeoutConfig"),
        job_executions_retry_config=resp.get("jobExecutionsRetryConfig"),
        maintenance_windows=resp.get("maintenanceWindows"),
        destination_package_versions=resp.get("destinationPackageVersions"),
    )


async def describe_managed_job_template(
    template_name: str,
    *,
    template_version: str | None = None,
    region_name: str | None = None,
) -> DescribeManagedJobTemplateResult:
    """Describe managed job template.

    Args:
        template_name: Template name.
        template_version: Template version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    if template_version is not None:
        kwargs["templateVersion"] = template_version
    try:
        resp = await client.call("DescribeManagedJobTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe managed job template") from exc
    return DescribeManagedJobTemplateResult(
        template_name=resp.get("templateName"),
        template_arn=resp.get("templateArn"),
        description=resp.get("description"),
        template_version=resp.get("templateVersion"),
        environments=resp.get("environments"),
        document_parameters=resp.get("documentParameters"),
        document=resp.get("document"),
    )


async def describe_mitigation_action(
    action_name: str,
    region_name: str | None = None,
) -> DescribeMitigationActionResult:
    """Describe mitigation action.

    Args:
        action_name: Action name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionName"] = action_name
    try:
        resp = await client.call("DescribeMitigationAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe mitigation action") from exc
    return DescribeMitigationActionResult(
        action_name=resp.get("actionName"),
        action_type=resp.get("actionType"),
        action_arn=resp.get("actionArn"),
        action_id=resp.get("actionId"),
        role_arn=resp.get("roleArn"),
        action_params=resp.get("actionParams"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def describe_provisioning_template(
    template_name: str,
    region_name: str | None = None,
) -> DescribeProvisioningTemplateResult:
    """Describe provisioning template.

    Args:
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    try:
        resp = await client.call("DescribeProvisioningTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe provisioning template") from exc
    return DescribeProvisioningTemplateResult(
        template_arn=resp.get("templateArn"),
        template_name=resp.get("templateName"),
        description=resp.get("description"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        default_version_id=resp.get("defaultVersionId"),
        template_body=resp.get("templateBody"),
        enabled=resp.get("enabled"),
        provisioning_role_arn=resp.get("provisioningRoleArn"),
        pre_provisioning_hook=resp.get("preProvisioningHook"),
        type_value=resp.get("type"),
    )


async def describe_provisioning_template_version(
    template_name: str,
    version_id: int,
    region_name: str | None = None,
) -> DescribeProvisioningTemplateVersionResult:
    """Describe provisioning template version.

    Args:
        template_name: Template name.
        version_id: Version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    kwargs["versionId"] = version_id
    try:
        resp = await client.call("DescribeProvisioningTemplateVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe provisioning template version") from exc
    return DescribeProvisioningTemplateVersionResult(
        version_id=resp.get("versionId"),
        creation_date=resp.get("creationDate"),
        template_body=resp.get("templateBody"),
        is_default_version=resp.get("isDefaultVersion"),
    )


async def describe_role_alias(
    role_alias: str,
    region_name: str | None = None,
) -> DescribeRoleAliasResult:
    """Describe role alias.

    Args:
        role_alias: Role alias.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["roleAlias"] = role_alias
    try:
        resp = await client.call("DescribeRoleAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe role alias") from exc
    return DescribeRoleAliasResult(
        role_alias_description=resp.get("roleAliasDescription"),
    )


async def describe_scheduled_audit(
    scheduled_audit_name: str,
    region_name: str | None = None,
) -> DescribeScheduledAuditResult:
    """Describe scheduled audit.

    Args:
        scheduled_audit_name: Scheduled audit name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scheduledAuditName"] = scheduled_audit_name
    try:
        resp = await client.call("DescribeScheduledAudit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe scheduled audit") from exc
    return DescribeScheduledAuditResult(
        frequency=resp.get("frequency"),
        day_of_month=resp.get("dayOfMonth"),
        day_of_week=resp.get("dayOfWeek"),
        target_check_names=resp.get("targetCheckNames"),
        scheduled_audit_name=resp.get("scheduledAuditName"),
        scheduled_audit_arn=resp.get("scheduledAuditArn"),
    )


async def describe_security_profile(
    security_profile_name: str,
    region_name: str | None = None,
) -> DescribeSecurityProfileResult:
    """Describe security profile.

    Args:
        security_profile_name: Security profile name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    try:
        resp = await client.call("DescribeSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe security profile") from exc
    return DescribeSecurityProfileResult(
        security_profile_name=resp.get("securityProfileName"),
        security_profile_arn=resp.get("securityProfileArn"),
        security_profile_description=resp.get("securityProfileDescription"),
        behaviors=resp.get("behaviors"),
        alert_targets=resp.get("alertTargets"),
        additional_metrics_to_retain=resp.get("additionalMetricsToRetain"),
        additional_metrics_to_retain_v2=resp.get("additionalMetricsToRetainV2"),
        version=resp.get("version"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        metrics_export_config=resp.get("metricsExportConfig"),
    )


async def describe_stream(
    stream_id: str,
    region_name: str | None = None,
) -> DescribeStreamResult:
    """Describe stream.

    Args:
        stream_id: Stream id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["streamId"] = stream_id
    try:
        resp = await client.call("DescribeStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe stream") from exc
    return DescribeStreamResult(
        stream_info=resp.get("streamInfo"),
    )


async def describe_thing_group(
    thing_group_name: str,
    region_name: str | None = None,
) -> DescribeThingGroupResult:
    """Describe thing group.

    Args:
        thing_group_name: Thing group name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    try:
        resp = await client.call("DescribeThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe thing group") from exc
    return DescribeThingGroupResult(
        thing_group_name=resp.get("thingGroupName"),
        thing_group_id=resp.get("thingGroupId"),
        thing_group_arn=resp.get("thingGroupArn"),
        version=resp.get("version"),
        thing_group_properties=resp.get("thingGroupProperties"),
        thing_group_metadata=resp.get("thingGroupMetadata"),
        index_name=resp.get("indexName"),
        query_string=resp.get("queryString"),
        query_version=resp.get("queryVersion"),
        status=resp.get("status"),
    )


async def describe_thing_registration_task(
    task_id: str,
    region_name: str | None = None,
) -> DescribeThingRegistrationTaskResult:
    """Describe thing registration task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        resp = await client.call("DescribeThingRegistrationTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe thing registration task") from exc
    return DescribeThingRegistrationTaskResult(
        task_id=resp.get("taskId"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        template_body=resp.get("templateBody"),
        input_file_bucket=resp.get("inputFileBucket"),
        input_file_key=resp.get("inputFileKey"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
        message=resp.get("message"),
        success_count=resp.get("successCount"),
        failure_count=resp.get("failureCount"),
        percentage_progress=resp.get("percentageProgress"),
    )


async def describe_thing_type(
    thing_type_name: str,
    region_name: str | None = None,
) -> DescribeThingTypeResult:
    """Describe thing type.

    Args:
        thing_type_name: Thing type name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingTypeName"] = thing_type_name
    try:
        resp = await client.call("DescribeThingType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe thing type") from exc
    return DescribeThingTypeResult(
        thing_type_name=resp.get("thingTypeName"),
        thing_type_id=resp.get("thingTypeId"),
        thing_type_arn=resp.get("thingTypeArn"),
        thing_type_properties=resp.get("thingTypeProperties"),
        thing_type_metadata=resp.get("thingTypeMetadata"),
    )


async def detach_principal_policy(
    policy_name: str,
    principal: str,
    region_name: str | None = None,
) -> None:
    """Detach principal policy.

    Args:
        policy_name: Policy name.
        principal: Principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    kwargs["principal"] = principal
    try:
        await client.call("DetachPrincipalPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach principal policy") from exc
    return None


async def detach_security_profile(
    security_profile_name: str,
    security_profile_target_arn: str,
    region_name: str | None = None,
) -> None:
    """Detach security profile.

    Args:
        security_profile_name: Security profile name.
        security_profile_target_arn: Security profile target arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    kwargs["securityProfileTargetArn"] = security_profile_target_arn
    try:
        await client.call("DetachSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach security profile") from exc
    return None


async def detach_thing_principal(
    thing_name: str,
    principal: str,
    region_name: str | None = None,
) -> None:
    """Detach thing principal.

    Args:
        thing_name: Thing name.
        principal: Principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    kwargs["principal"] = principal
    try:
        await client.call("DetachThingPrincipal", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to detach thing principal") from exc
    return None


async def disable_topic_rule(
    rule_name: str,
    region_name: str | None = None,
) -> None:
    """Disable topic rule.

    Args:
        rule_name: Rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ruleName"] = rule_name
    try:
        await client.call("DisableTopicRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable topic rule") from exc
    return None


async def disassociate_sbom_from_package_version(
    package_name: str,
    version_name: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disassociate sbom from package version.

    Args:
        package_name: Package name.
        version_name: Version name.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("DisassociateSbomFromPackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate sbom from package version") from exc
    return None


async def enable_topic_rule(
    rule_name: str,
    region_name: str | None = None,
) -> None:
    """Enable topic rule.

    Args:
        rule_name: Rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ruleName"] = rule_name
    try:
        await client.call("EnableTopicRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable topic rule") from exc
    return None


async def get_behavior_model_training_summaries(
    *,
    security_profile_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetBehaviorModelTrainingSummariesResult:
    """Get behavior model training summaries.

    Args:
        security_profile_name: Security profile name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if security_profile_name is not None:
        kwargs["securityProfileName"] = security_profile_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("GetBehaviorModelTrainingSummaries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get behavior model training summaries") from exc
    return GetBehaviorModelTrainingSummariesResult(
        summaries=resp.get("summaries"),
        next_token=resp.get("nextToken"),
    )


async def get_buckets_aggregation(
    query_string: str,
    aggregation_field: str,
    buckets_aggregation_type: dict[str, Any],
    *,
    index_name: str | None = None,
    query_version: str | None = None,
    region_name: str | None = None,
) -> GetBucketsAggregationResult:
    """Get buckets aggregation.

    Args:
        query_string: Query string.
        aggregation_field: Aggregation field.
        buckets_aggregation_type: Buckets aggregation type.
        index_name: Index name.
        query_version: Query version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryString"] = query_string
    kwargs["aggregationField"] = aggregation_field
    kwargs["bucketsAggregationType"] = buckets_aggregation_type
    if index_name is not None:
        kwargs["indexName"] = index_name
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    try:
        resp = await client.call("GetBucketsAggregation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get buckets aggregation") from exc
    return GetBucketsAggregationResult(
        total_count=resp.get("totalCount"),
        buckets=resp.get("buckets"),
    )


async def get_cardinality(
    query_string: str,
    *,
    index_name: str | None = None,
    aggregation_field: str | None = None,
    query_version: str | None = None,
    region_name: str | None = None,
) -> GetCardinalityResult:
    """Get cardinality.

    Args:
        query_string: Query string.
        index_name: Index name.
        aggregation_field: Aggregation field.
        query_version: Query version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryString"] = query_string
    if index_name is not None:
        kwargs["indexName"] = index_name
    if aggregation_field is not None:
        kwargs["aggregationField"] = aggregation_field
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    try:
        resp = await client.call("GetCardinality", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cardinality") from exc
    return GetCardinalityResult(
        cardinality=resp.get("cardinality"),
    )


async def get_command(
    command_id: str,
    region_name: str | None = None,
) -> GetCommandResult:
    """Get command.

    Args:
        command_id: Command id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commandId"] = command_id
    try:
        resp = await client.call("GetCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get command") from exc
    return GetCommandResult(
        command_id=resp.get("commandId"),
        command_arn=resp.get("commandArn"),
        namespace=resp.get("namespace"),
        display_name=resp.get("displayName"),
        description=resp.get("description"),
        mandatory_parameters=resp.get("mandatoryParameters"),
        payload=resp.get("payload"),
        role_arn=resp.get("roleArn"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
        deprecated=resp.get("deprecated"),
        pending_deletion=resp.get("pendingDeletion"),
    )


async def get_command_execution(
    execution_id: str,
    target_arn: str,
    *,
    include_result: bool | None = None,
    region_name: str | None = None,
) -> GetCommandExecutionResult:
    """Get command execution.

    Args:
        execution_id: Execution id.
        target_arn: Target arn.
        include_result: Include result.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["executionId"] = execution_id
    kwargs["targetArn"] = target_arn
    if include_result is not None:
        kwargs["includeResult"] = include_result
    try:
        resp = await client.call("GetCommandExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get command execution") from exc
    return GetCommandExecutionResult(
        execution_id=resp.get("executionId"),
        command_arn=resp.get("commandArn"),
        target_arn=resp.get("targetArn"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        result=resp.get("result"),
        parameters=resp.get("parameters"),
        execution_timeout_seconds=resp.get("executionTimeoutSeconds"),
        created_at=resp.get("createdAt"),
        last_updated_at=resp.get("lastUpdatedAt"),
        started_at=resp.get("startedAt"),
        completed_at=resp.get("completedAt"),
        time_to_live=resp.get("timeToLive"),
    )


async def get_effective_policies(
    *,
    principal: str | None = None,
    cognito_identity_pool_id: str | None = None,
    thing_name: str | None = None,
    region_name: str | None = None,
) -> GetEffectivePoliciesResult:
    """Get effective policies.

    Args:
        principal: Principal.
        cognito_identity_pool_id: Cognito identity pool id.
        thing_name: Thing name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if principal is not None:
        kwargs["principal"] = principal
    if cognito_identity_pool_id is not None:
        kwargs["cognitoIdentityPoolId"] = cognito_identity_pool_id
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    try:
        resp = await client.call("GetEffectivePolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get effective policies") from exc
    return GetEffectivePoliciesResult(
        effective_policies=resp.get("effectivePolicies"),
    )


async def get_indexing_configuration(
    region_name: str | None = None,
) -> GetIndexingConfigurationResult:
    """Get indexing configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetIndexingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get indexing configuration") from exc
    return GetIndexingConfigurationResult(
        thing_indexing_configuration=resp.get("thingIndexingConfiguration"),
        thing_group_indexing_configuration=resp.get("thingGroupIndexingConfiguration"),
    )


async def get_job_document(
    job_id: str,
    *,
    before_substitution: bool | None = None,
    region_name: str | None = None,
) -> GetJobDocumentResult:
    """Get job document.

    Args:
        job_id: Job id.
        before_substitution: Before substitution.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    if before_substitution is not None:
        kwargs["beforeSubstitution"] = before_substitution
    try:
        resp = await client.call("GetJobDocument", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get job document") from exc
    return GetJobDocumentResult(
        document=resp.get("document"),
    )


async def get_logging_options(
    region_name: str | None = None,
) -> GetLoggingOptionsResult:
    """Get logging options.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetLoggingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get logging options") from exc
    return GetLoggingOptionsResult(
        role_arn=resp.get("roleArn"),
        log_level=resp.get("logLevel"),
    )


async def get_ota_update(
    ota_update_id: str,
    region_name: str | None = None,
) -> GetOtaUpdateResult:
    """Get ota update.

    Args:
        ota_update_id: Ota update id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["otaUpdateId"] = ota_update_id
    try:
        resp = await client.call("GetOTAUpdate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get ota update") from exc
    return GetOtaUpdateResult(
        ota_update_info=resp.get("otaUpdateInfo"),
    )


async def get_package(
    package_name: str,
    region_name: str | None = None,
) -> GetPackageResult:
    """Get package.

    Args:
        package_name: Package name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    try:
        resp = await client.call("GetPackage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get package") from exc
    return GetPackageResult(
        package_name=resp.get("packageName"),
        package_arn=resp.get("packageArn"),
        description=resp.get("description"),
        default_version_name=resp.get("defaultVersionName"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def get_package_configuration(
    region_name: str | None = None,
) -> GetPackageConfigurationResult:
    """Get package configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetPackageConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get package configuration") from exc
    return GetPackageConfigurationResult(
        version_update_by_jobs_config=resp.get("versionUpdateByJobsConfig"),
    )


async def get_package_version(
    package_name: str,
    version_name: str,
    region_name: str | None = None,
) -> GetPackageVersionResult:
    """Get package version.

    Args:
        package_name: Package name.
        version_name: Version name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    try:
        resp = await client.call("GetPackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get package version") from exc
    return GetPackageVersionResult(
        package_version_arn=resp.get("packageVersionArn"),
        package_name=resp.get("packageName"),
        version_name=resp.get("versionName"),
        description=resp.get("description"),
        attributes=resp.get("attributes"),
        artifact=resp.get("artifact"),
        status=resp.get("status"),
        error_reason=resp.get("errorReason"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        sbom=resp.get("sbom"),
        sbom_validation_status=resp.get("sbomValidationStatus"),
        recipe=resp.get("recipe"),
    )


async def get_percentiles(
    query_string: str,
    *,
    index_name: str | None = None,
    aggregation_field: str | None = None,
    query_version: str | None = None,
    percents: list[float] | None = None,
    region_name: str | None = None,
) -> GetPercentilesResult:
    """Get percentiles.

    Args:
        query_string: Query string.
        index_name: Index name.
        aggregation_field: Aggregation field.
        query_version: Query version.
        percents: Percents.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryString"] = query_string
    if index_name is not None:
        kwargs["indexName"] = index_name
    if aggregation_field is not None:
        kwargs["aggregationField"] = aggregation_field
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    if percents is not None:
        kwargs["percents"] = percents
    try:
        resp = await client.call("GetPercentiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get percentiles") from exc
    return GetPercentilesResult(
        percentiles=resp.get("percentiles"),
    )


async def get_policy_version(
    policy_name: str,
    policy_version_id: str,
    region_name: str | None = None,
) -> GetPolicyVersionResult:
    """Get policy version.

    Args:
        policy_name: Policy name.
        policy_version_id: Policy version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    kwargs["policyVersionId"] = policy_version_id
    try:
        resp = await client.call("GetPolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get policy version") from exc
    return GetPolicyVersionResult(
        policy_arn=resp.get("policyArn"),
        policy_name=resp.get("policyName"),
        policy_document=resp.get("policyDocument"),
        policy_version_id=resp.get("policyVersionId"),
        is_default_version=resp.get("isDefaultVersion"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        generation_id=resp.get("generationId"),
    )


async def get_registration_code(
    region_name: str | None = None,
) -> GetRegistrationCodeResult:
    """Get registration code.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetRegistrationCode", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get registration code") from exc
    return GetRegistrationCodeResult(
        registration_code=resp.get("registrationCode"),
    )


async def get_statistics(
    query_string: str,
    *,
    index_name: str | None = None,
    aggregation_field: str | None = None,
    query_version: str | None = None,
    region_name: str | None = None,
) -> GetStatisticsResult:
    """Get statistics.

    Args:
        query_string: Query string.
        index_name: Index name.
        aggregation_field: Aggregation field.
        query_version: Query version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryString"] = query_string
    if index_name is not None:
        kwargs["indexName"] = index_name
    if aggregation_field is not None:
        kwargs["aggregationField"] = aggregation_field
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    try:
        resp = await client.call("GetStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get statistics") from exc
    return GetStatisticsResult(
        statistics=resp.get("statistics"),
    )


async def get_thing_connectivity_data(
    thing_name: str,
    region_name: str | None = None,
) -> GetThingConnectivityDataResult:
    """Get thing connectivity data.

    Args:
        thing_name: Thing name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    try:
        resp = await client.call("GetThingConnectivityData", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get thing connectivity data") from exc
    return GetThingConnectivityDataResult(
        thing_name=resp.get("thingName"),
        connected=resp.get("connected"),
        timestamp=resp.get("timestamp"),
        disconnect_reason=resp.get("disconnectReason"),
    )


async def get_topic_rule_destination(
    arn: str,
    region_name: str | None = None,
) -> GetTopicRuleDestinationResult:
    """Get topic rule destination.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    try:
        resp = await client.call("GetTopicRuleDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get topic rule destination") from exc
    return GetTopicRuleDestinationResult(
        topic_rule_destination=resp.get("topicRuleDestination"),
    )


async def get_v2_logging_options(
    region_name: str | None = None,
) -> GetV2LoggingOptionsResult:
    """Get v2 logging options.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetV2LoggingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get v2 logging options") from exc
    return GetV2LoggingOptionsResult(
        role_arn=resp.get("roleArn"),
        default_log_level=resp.get("defaultLogLevel"),
        disable_all_logs=resp.get("disableAllLogs"),
    )


async def list_active_violations(
    *,
    thing_name: str | None = None,
    security_profile_name: str | None = None,
    behavior_criteria_type: str | None = None,
    list_suppressed_alerts: bool | None = None,
    verification_state: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListActiveViolationsResult:
    """List active violations.

    Args:
        thing_name: Thing name.
        security_profile_name: Security profile name.
        behavior_criteria_type: Behavior criteria type.
        list_suppressed_alerts: List suppressed alerts.
        verification_state: Verification state.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if security_profile_name is not None:
        kwargs["securityProfileName"] = security_profile_name
    if behavior_criteria_type is not None:
        kwargs["behaviorCriteriaType"] = behavior_criteria_type
    if list_suppressed_alerts is not None:
        kwargs["listSuppressedAlerts"] = list_suppressed_alerts
    if verification_state is not None:
        kwargs["verificationState"] = verification_state
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListActiveViolations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list active violations") from exc
    return ListActiveViolationsResult(
        active_violations=resp.get("activeViolations"),
        next_token=resp.get("nextToken"),
    )


async def list_attached_policies(
    target: str,
    *,
    recursive: bool | None = None,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListAttachedPoliciesResult:
    """List attached policies.

    Args:
        target: Target.
        recursive: Recursive.
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["target"] = target
    if recursive is not None:
        kwargs["recursive"] = recursive
    if marker is not None:
        kwargs["marker"] = marker
    if page_size is not None:
        kwargs["pageSize"] = page_size
    try:
        resp = await client.call("ListAttachedPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list attached policies") from exc
    return ListAttachedPoliciesResult(
        policies=resp.get("policies"),
        next_marker=resp.get("nextMarker"),
    )


async def list_audit_findings(
    *,
    task_id: str | None = None,
    check_name: str | None = None,
    resource_identifier: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    list_suppressed_findings: bool | None = None,
    region_name: str | None = None,
) -> ListAuditFindingsResult:
    """List audit findings.

    Args:
        task_id: Task id.
        check_name: Check name.
        resource_identifier: Resource identifier.
        max_results: Max results.
        next_token: Next token.
        start_time: Start time.
        end_time: End time.
        list_suppressed_findings: List suppressed findings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if task_id is not None:
        kwargs["taskId"] = task_id
    if check_name is not None:
        kwargs["checkName"] = check_name
    if resource_identifier is not None:
        kwargs["resourceIdentifier"] = resource_identifier
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if start_time is not None:
        kwargs["startTime"] = start_time
    if end_time is not None:
        kwargs["endTime"] = end_time
    if list_suppressed_findings is not None:
        kwargs["listSuppressedFindings"] = list_suppressed_findings
    try:
        resp = await client.call("ListAuditFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list audit findings") from exc
    return ListAuditFindingsResult(
        findings=resp.get("findings"),
        next_token=resp.get("nextToken"),
    )


async def list_audit_mitigation_actions_executions(
    task_id: str,
    finding_id: str,
    *,
    action_status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAuditMitigationActionsExecutionsResult:
    """List audit mitigation actions executions.

    Args:
        task_id: Task id.
        finding_id: Finding id.
        action_status: Action status.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    kwargs["findingId"] = finding_id
    if action_status is not None:
        kwargs["actionStatus"] = action_status
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAuditMitigationActionsExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list audit mitigation actions executions") from exc
    return ListAuditMitigationActionsExecutionsResult(
        actions_executions=resp.get("actionsExecutions"),
        next_token=resp.get("nextToken"),
    )


async def list_audit_mitigation_actions_tasks(
    start_time: str,
    end_time: str,
    *,
    audit_task_id: str | None = None,
    finding_id: str | None = None,
    task_status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAuditMitigationActionsTasksResult:
    """List audit mitigation actions tasks.

    Args:
        start_time: Start time.
        end_time: End time.
        audit_task_id: Audit task id.
        finding_id: Finding id.
        task_status: Task status.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    if audit_task_id is not None:
        kwargs["auditTaskId"] = audit_task_id
    if finding_id is not None:
        kwargs["findingId"] = finding_id
    if task_status is not None:
        kwargs["taskStatus"] = task_status
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAuditMitigationActionsTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list audit mitigation actions tasks") from exc
    return ListAuditMitigationActionsTasksResult(
        tasks=resp.get("tasks"),
        next_token=resp.get("nextToken"),
    )


async def list_audit_suppressions(
    *,
    check_name: str | None = None,
    resource_identifier: dict[str, Any] | None = None,
    ascending_order: bool | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAuditSuppressionsResult:
    """List audit suppressions.

    Args:
        check_name: Check name.
        resource_identifier: Resource identifier.
        ascending_order: Ascending order.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if check_name is not None:
        kwargs["checkName"] = check_name
    if resource_identifier is not None:
        kwargs["resourceIdentifier"] = resource_identifier
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAuditSuppressions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list audit suppressions") from exc
    return ListAuditSuppressionsResult(
        suppressions=resp.get("suppressions"),
        next_token=resp.get("nextToken"),
    )


async def list_audit_tasks(
    start_time: str,
    end_time: str,
    *,
    task_type: str | None = None,
    task_status: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAuditTasksResult:
    """List audit tasks.

    Args:
        start_time: Start time.
        end_time: End time.
        task_type: Task type.
        task_status: Task status.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    if task_type is not None:
        kwargs["taskType"] = task_type
    if task_status is not None:
        kwargs["taskStatus"] = task_status
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListAuditTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list audit tasks") from exc
    return ListAuditTasksResult(
        tasks=resp.get("tasks"),
        next_token=resp.get("nextToken"),
    )


async def list_authorizers(
    *,
    page_size: int | None = None,
    marker: str | None = None,
    ascending_order: bool | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> ListAuthorizersResult:
    """List authorizers.

    Args:
        page_size: Page size.
        marker: Marker.
        ascending_order: Ascending order.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if marker is not None:
        kwargs["marker"] = marker
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    if status is not None:
        kwargs["status"] = status
    try:
        resp = await client.call("ListAuthorizers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list authorizers") from exc
    return ListAuthorizersResult(
        authorizers=resp.get("authorizers"),
        next_marker=resp.get("nextMarker"),
    )


async def list_billing_groups(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    name_prefix_filter: str | None = None,
    region_name: str | None = None,
) -> ListBillingGroupsResult:
    """List billing groups.

    Args:
        next_token: Next token.
        max_results: Max results.
        name_prefix_filter: Name prefix filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if name_prefix_filter is not None:
        kwargs["namePrefixFilter"] = name_prefix_filter
    try:
        resp = await client.call("ListBillingGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list billing groups") from exc
    return ListBillingGroupsResult(
        billing_groups=resp.get("billingGroups"),
        next_token=resp.get("nextToken"),
    )


async def list_ca_certificates(
    *,
    page_size: int | None = None,
    marker: str | None = None,
    ascending_order: bool | None = None,
    template_name: str | None = None,
    region_name: str | None = None,
) -> ListCaCertificatesResult:
    """List ca certificates.

    Args:
        page_size: Page size.
        marker: Marker.
        ascending_order: Ascending order.
        template_name: Template name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if marker is not None:
        kwargs["marker"] = marker
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    if template_name is not None:
        kwargs["templateName"] = template_name
    try:
        resp = await client.call("ListCACertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ca certificates") from exc
    return ListCaCertificatesResult(
        certificates=resp.get("certificates"),
        next_marker=resp.get("nextMarker"),
    )


async def list_certificate_providers(
    *,
    next_token: str | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListCertificateProvidersResult:
    """List certificate providers.

    Args:
        next_token: Next token.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListCertificateProviders", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list certificate providers") from exc
    return ListCertificateProvidersResult(
        certificate_providers=resp.get("certificateProviders"),
        next_token=resp.get("nextToken"),
    )


async def list_certificates(
    *,
    page_size: int | None = None,
    marker: str | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListCertificatesResult:
    """List certificates.

    Args:
        page_size: Page size.
        marker: Marker.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if marker is not None:
        kwargs["marker"] = marker
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list certificates") from exc
    return ListCertificatesResult(
        certificates=resp.get("certificates"),
        next_marker=resp.get("nextMarker"),
    )


async def list_certificates_by_ca(
    ca_certificate_id: str,
    *,
    page_size: int | None = None,
    marker: str | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListCertificatesByCaResult:
    """List certificates by ca.

    Args:
        ca_certificate_id: Ca certificate id.
        page_size: Page size.
        marker: Marker.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["caCertificateId"] = ca_certificate_id
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if marker is not None:
        kwargs["marker"] = marker
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListCertificatesByCA", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list certificates by ca") from exc
    return ListCertificatesByCaResult(
        certificates=resp.get("certificates"),
        next_marker=resp.get("nextMarker"),
    )


async def list_command_executions(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    namespace: str | None = None,
    status: str | None = None,
    sort_order: str | None = None,
    started_time_filter: dict[str, Any] | None = None,
    completed_time_filter: dict[str, Any] | None = None,
    target_arn: str | None = None,
    command_arn: str | None = None,
    region_name: str | None = None,
) -> ListCommandExecutionsResult:
    """List command executions.

    Args:
        max_results: Max results.
        next_token: Next token.
        namespace: Namespace.
        status: Status.
        sort_order: Sort order.
        started_time_filter: Started time filter.
        completed_time_filter: Completed time filter.
        target_arn: Target arn.
        command_arn: Command arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if namespace is not None:
        kwargs["namespace"] = namespace
    if status is not None:
        kwargs["status"] = status
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    if started_time_filter is not None:
        kwargs["startedTimeFilter"] = started_time_filter
    if completed_time_filter is not None:
        kwargs["completedTimeFilter"] = completed_time_filter
    if target_arn is not None:
        kwargs["targetArn"] = target_arn
    if command_arn is not None:
        kwargs["commandArn"] = command_arn
    try:
        resp = await client.call("ListCommandExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list command executions") from exc
    return ListCommandExecutionsResult(
        command_executions=resp.get("commandExecutions"),
        next_token=resp.get("nextToken"),
    )


async def list_commands(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    namespace: str | None = None,
    command_parameter_name: str | None = None,
    sort_order: str | None = None,
    region_name: str | None = None,
) -> ListCommandsResult:
    """List commands.

    Args:
        max_results: Max results.
        next_token: Next token.
        namespace: Namespace.
        command_parameter_name: Command parameter name.
        sort_order: Sort order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if namespace is not None:
        kwargs["namespace"] = namespace
    if command_parameter_name is not None:
        kwargs["commandParameterName"] = command_parameter_name
    if sort_order is not None:
        kwargs["sortOrder"] = sort_order
    try:
        resp = await client.call("ListCommands", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list commands") from exc
    return ListCommandsResult(
        commands=resp.get("commands"),
        next_token=resp.get("nextToken"),
    )


async def list_custom_metrics(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCustomMetricsResult:
    """List custom metrics.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListCustomMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list custom metrics") from exc
    return ListCustomMetricsResult(
        metric_names=resp.get("metricNames"),
        next_token=resp.get("nextToken"),
    )


async def list_detect_mitigation_actions_executions(
    *,
    task_id: str | None = None,
    violation_id: str | None = None,
    thing_name: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDetectMitigationActionsExecutionsResult:
    """List detect mitigation actions executions.

    Args:
        task_id: Task id.
        violation_id: Violation id.
        thing_name: Thing name.
        start_time: Start time.
        end_time: End time.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if task_id is not None:
        kwargs["taskId"] = task_id
    if violation_id is not None:
        kwargs["violationId"] = violation_id
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if start_time is not None:
        kwargs["startTime"] = start_time
    if end_time is not None:
        kwargs["endTime"] = end_time
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListDetectMitigationActionsExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list detect mitigation actions executions") from exc
    return ListDetectMitigationActionsExecutionsResult(
        actions_executions=resp.get("actionsExecutions"),
        next_token=resp.get("nextToken"),
    )


async def list_detect_mitigation_actions_tasks(
    start_time: str,
    end_time: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListDetectMitigationActionsTasksResult:
    """List detect mitigation actions tasks.

    Args:
        start_time: Start time.
        end_time: End time.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListDetectMitigationActionsTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list detect mitigation actions tasks") from exc
    return ListDetectMitigationActionsTasksResult(
        tasks=resp.get("tasks"),
        next_token=resp.get("nextToken"),
    )


async def list_dimensions(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListDimensionsResult:
    """List dimensions.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListDimensions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list dimensions") from exc
    return ListDimensionsResult(
        dimension_names=resp.get("dimensionNames"),
        next_token=resp.get("nextToken"),
    )


async def list_domain_configurations(
    *,
    marker: str | None = None,
    page_size: int | None = None,
    service_type: str | None = None,
    region_name: str | None = None,
) -> ListDomainConfigurationsResult:
    """List domain configurations.

    Args:
        marker: Marker.
        page_size: Page size.
        service_type: Service type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if marker is not None:
        kwargs["marker"] = marker
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if service_type is not None:
        kwargs["serviceType"] = service_type
    try:
        resp = await client.call("ListDomainConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list domain configurations") from exc
    return ListDomainConfigurationsResult(
        domain_configurations=resp.get("domainConfigurations"),
        next_marker=resp.get("nextMarker"),
    )


async def list_fleet_metrics(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFleetMetricsResult:
    """List fleet metrics.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListFleetMetrics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list fleet metrics") from exc
    return ListFleetMetricsResult(
        fleet_metrics=resp.get("fleetMetrics"),
        next_token=resp.get("nextToken"),
    )


async def list_indices(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListIndicesResult:
    """List indices.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListIndices", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list indices") from exc
    return ListIndicesResult(
        index_names=resp.get("indexNames"),
        next_token=resp.get("nextToken"),
    )


async def list_job_executions_for_job(
    job_id: str,
    *,
    status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListJobExecutionsForJobResult:
    """List job executions for job.

    Args:
        job_id: Job id.
        status: Status.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    if status is not None:
        kwargs["status"] = status
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListJobExecutionsForJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list job executions for job") from exc
    return ListJobExecutionsForJobResult(
        execution_summaries=resp.get("executionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_job_executions_for_thing(
    thing_name: str,
    *,
    status: str | None = None,
    namespace_id: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    job_id: str | None = None,
    region_name: str | None = None,
) -> ListJobExecutionsForThingResult:
    """List job executions for thing.

    Args:
        thing_name: Thing name.
        status: Status.
        namespace_id: Namespace id.
        max_results: Max results.
        next_token: Next token.
        job_id: Job id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    if status is not None:
        kwargs["status"] = status
    if namespace_id is not None:
        kwargs["namespaceId"] = namespace_id
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if job_id is not None:
        kwargs["jobId"] = job_id
    try:
        resp = await client.call("ListJobExecutionsForThing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list job executions for thing") from exc
    return ListJobExecutionsForThingResult(
        execution_summaries=resp.get("executionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_job_templates(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListJobTemplatesResult:
    """List job templates.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListJobTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list job templates") from exc
    return ListJobTemplatesResult(
        job_templates=resp.get("jobTemplates"),
        next_token=resp.get("nextToken"),
    )


async def list_managed_job_templates(
    *,
    template_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListManagedJobTemplatesResult:
    """List managed job templates.

    Args:
        template_name: Template name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if template_name is not None:
        kwargs["templateName"] = template_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListManagedJobTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list managed job templates") from exc
    return ListManagedJobTemplatesResult(
        managed_job_templates=resp.get("managedJobTemplates"),
        next_token=resp.get("nextToken"),
    )


async def list_metric_values(
    thing_name: str,
    metric_name: str,
    start_time: str,
    end_time: str,
    *,
    dimension_name: str | None = None,
    dimension_value_operator: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListMetricValuesResult:
    """List metric values.

    Args:
        thing_name: Thing name.
        metric_name: Metric name.
        start_time: Start time.
        end_time: End time.
        dimension_name: Dimension name.
        dimension_value_operator: Dimension value operator.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    kwargs["metricName"] = metric_name
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    if dimension_name is not None:
        kwargs["dimensionName"] = dimension_name
    if dimension_value_operator is not None:
        kwargs["dimensionValueOperator"] = dimension_value_operator
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListMetricValues", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list metric values") from exc
    return ListMetricValuesResult(
        metric_datum_list=resp.get("metricDatumList"),
        next_token=resp.get("nextToken"),
    )


async def list_mitigation_actions(
    *,
    action_type: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListMitigationActionsResult:
    """List mitigation actions.

    Args:
        action_type: Action type.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if action_type is not None:
        kwargs["actionType"] = action_type
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListMitigationActions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list mitigation actions") from exc
    return ListMitigationActionsResult(
        action_identifiers=resp.get("actionIdentifiers"),
        next_token=resp.get("nextToken"),
    )


async def list_ota_updates(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    ota_update_status: str | None = None,
    region_name: str | None = None,
) -> ListOtaUpdatesResult:
    """List ota updates.

    Args:
        max_results: Max results.
        next_token: Next token.
        ota_update_status: Ota update status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if ota_update_status is not None:
        kwargs["otaUpdateStatus"] = ota_update_status
    try:
        resp = await client.call("ListOTAUpdates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list ota updates") from exc
    return ListOtaUpdatesResult(
        ota_updates=resp.get("otaUpdates"),
        next_token=resp.get("nextToken"),
    )


async def list_outgoing_certificates(
    *,
    page_size: int | None = None,
    marker: str | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListOutgoingCertificatesResult:
    """List outgoing certificates.

    Args:
        page_size: Page size.
        marker: Marker.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if marker is not None:
        kwargs["marker"] = marker
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListOutgoingCertificates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list outgoing certificates") from exc
    return ListOutgoingCertificatesResult(
        outgoing_certificates=resp.get("outgoingCertificates"),
        next_marker=resp.get("nextMarker"),
    )


async def list_package_versions(
    package_name: str,
    *,
    status: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPackageVersionsResult:
    """List package versions.

    Args:
        package_name: Package name.
        status: Status.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    if status is not None:
        kwargs["status"] = status
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPackageVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list package versions") from exc
    return ListPackageVersionsResult(
        package_version_summaries=resp.get("packageVersionSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_packages(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPackagesResult:
    """List packages.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPackages", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list packages") from exc
    return ListPackagesResult(
        package_summaries=resp.get("packageSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_policy_principals(
    policy_name: str,
    *,
    marker: str | None = None,
    page_size: int | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListPolicyPrincipalsResult:
    """List policy principals.

    Args:
        policy_name: Policy name.
        marker: Marker.
        page_size: Page size.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    if marker is not None:
        kwargs["marker"] = marker
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListPolicyPrincipals", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list policy principals") from exc
    return ListPolicyPrincipalsResult(
        principals=resp.get("principals"),
        next_marker=resp.get("nextMarker"),
    )


async def list_policy_versions(
    policy_name: str,
    region_name: str | None = None,
) -> ListPolicyVersionsResult:
    """List policy versions.

    Args:
        policy_name: Policy name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    try:
        resp = await client.call("ListPolicyVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list policy versions") from exc
    return ListPolicyVersionsResult(
        policy_versions=resp.get("policyVersions"),
    )


async def list_principal_policies(
    principal: str,
    *,
    marker: str | None = None,
    page_size: int | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListPrincipalPoliciesResult:
    """List principal policies.

    Args:
        principal: Principal.
        marker: Marker.
        page_size: Page size.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["principal"] = principal
    if marker is not None:
        kwargs["marker"] = marker
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListPrincipalPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list principal policies") from exc
    return ListPrincipalPoliciesResult(
        policies=resp.get("policies"),
        next_marker=resp.get("nextMarker"),
    )


async def list_principal_things(
    principal: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPrincipalThingsResult:
    """List principal things.

    Args:
        principal: Principal.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["principal"] = principal
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListPrincipalThings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list principal things") from exc
    return ListPrincipalThingsResult(
        things=resp.get("things"),
        next_token=resp.get("nextToken"),
    )


async def list_principal_things_v2(
    principal: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    thing_principal_type: str | None = None,
    region_name: str | None = None,
) -> ListPrincipalThingsV2Result:
    """List principal things v2.

    Args:
        principal: Principal.
        next_token: Next token.
        max_results: Max results.
        thing_principal_type: Thing principal type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["principal"] = principal
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if thing_principal_type is not None:
        kwargs["thingPrincipalType"] = thing_principal_type
    try:
        resp = await client.call("ListPrincipalThingsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list principal things v2") from exc
    return ListPrincipalThingsV2Result(
        principal_thing_objects=resp.get("principalThingObjects"),
        next_token=resp.get("nextToken"),
    )


async def list_provisioning_template_versions(
    template_name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListProvisioningTemplateVersionsResult:
    """List provisioning template versions.

    Args:
        template_name: Template name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListProvisioningTemplateVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list provisioning template versions") from exc
    return ListProvisioningTemplateVersionsResult(
        versions=resp.get("versions"),
        next_token=resp.get("nextToken"),
    )


async def list_provisioning_templates(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListProvisioningTemplatesResult:
    """List provisioning templates.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListProvisioningTemplates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list provisioning templates") from exc
    return ListProvisioningTemplatesResult(
        templates=resp.get("templates"),
        next_token=resp.get("nextToken"),
    )


async def list_related_resources_for_audit_finding(
    finding_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListRelatedResourcesForAuditFindingResult:
    """List related resources for audit finding.

    Args:
        finding_id: Finding id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["findingId"] = finding_id
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListRelatedResourcesForAuditFinding", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list related resources for audit finding") from exc
    return ListRelatedResourcesForAuditFindingResult(
        related_resources=resp.get("relatedResources"),
        next_token=resp.get("nextToken"),
    )


async def list_role_aliases(
    *,
    page_size: int | None = None,
    marker: str | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListRoleAliasesResult:
    """List role aliases.

    Args:
        page_size: Page size.
        marker: Marker.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if page_size is not None:
        kwargs["pageSize"] = page_size
    if marker is not None:
        kwargs["marker"] = marker
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListRoleAliases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list role aliases") from exc
    return ListRoleAliasesResult(
        role_aliases=resp.get("roleAliases"),
        next_marker=resp.get("nextMarker"),
    )


async def list_sbom_validation_results(
    package_name: str,
    version_name: str,
    *,
    validation_result: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSbomValidationResultsResult:
    """List sbom validation results.

    Args:
        package_name: Package name.
        version_name: Version name.
        validation_result: Validation result.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    if validation_result is not None:
        kwargs["validationResult"] = validation_result
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListSbomValidationResults", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sbom validation results") from exc
    return ListSbomValidationResultsResult(
        validation_result_summaries=resp.get("validationResultSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_scheduled_audits(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListScheduledAuditsResult:
    """List scheduled audits.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListScheduledAudits", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list scheduled audits") from exc
    return ListScheduledAuditsResult(
        scheduled_audits=resp.get("scheduledAudits"),
        next_token=resp.get("nextToken"),
    )


async def list_security_profiles(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    dimension_name: str | None = None,
    metric_name: str | None = None,
    region_name: str | None = None,
) -> ListSecurityProfilesResult:
    """List security profiles.

    Args:
        next_token: Next token.
        max_results: Max results.
        dimension_name: Dimension name.
        metric_name: Metric name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if dimension_name is not None:
        kwargs["dimensionName"] = dimension_name
    if metric_name is not None:
        kwargs["metricName"] = metric_name
    try:
        resp = await client.call("ListSecurityProfiles", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list security profiles") from exc
    return ListSecurityProfilesResult(
        security_profile_identifiers=resp.get("securityProfileIdentifiers"),
        next_token=resp.get("nextToken"),
    )


async def list_security_profiles_for_target(
    security_profile_target_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    recursive: bool | None = None,
    region_name: str | None = None,
) -> ListSecurityProfilesForTargetResult:
    """List security profiles for target.

    Args:
        security_profile_target_arn: Security profile target arn.
        next_token: Next token.
        max_results: Max results.
        recursive: Recursive.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileTargetArn"] = security_profile_target_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if recursive is not None:
        kwargs["recursive"] = recursive
    try:
        resp = await client.call("ListSecurityProfilesForTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list security profiles for target") from exc
    return ListSecurityProfilesForTargetResult(
        security_profile_target_mappings=resp.get("securityProfileTargetMappings"),
        next_token=resp.get("nextToken"),
    )


async def list_streams(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    ascending_order: bool | None = None,
    region_name: str | None = None,
) -> ListStreamsResult:
    """List streams.

    Args:
        max_results: Max results.
        next_token: Next token.
        ascending_order: Ascending order.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if ascending_order is not None:
        kwargs["ascendingOrder"] = ascending_order
    try:
        resp = await client.call("ListStreams", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list streams") from exc
    return ListStreamsResult(
        streams=resp.get("streams"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
        next_token=resp.get("nextToken"),
    )


async def list_targets_for_policy(
    policy_name: str,
    *,
    marker: str | None = None,
    page_size: int | None = None,
    region_name: str | None = None,
) -> ListTargetsForPolicyResult:
    """List targets for policy.

    Args:
        policy_name: Policy name.
        marker: Marker.
        page_size: Page size.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    if marker is not None:
        kwargs["marker"] = marker
    if page_size is not None:
        kwargs["pageSize"] = page_size
    try:
        resp = await client.call("ListTargetsForPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list targets for policy") from exc
    return ListTargetsForPolicyResult(
        targets=resp.get("targets"),
        next_marker=resp.get("nextMarker"),
    )


async def list_targets_for_security_profile(
    security_profile_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTargetsForSecurityProfileResult:
    """List targets for security profile.

    Args:
        security_profile_name: Security profile name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListTargetsForSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list targets for security profile") from exc
    return ListTargetsForSecurityProfileResult(
        security_profile_targets=resp.get("securityProfileTargets"),
        next_token=resp.get("nextToken"),
    )


async def list_thing_groups_for_thing(
    thing_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThingGroupsForThingResult:
    """List thing groups for thing.

    Args:
        thing_name: Thing name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListThingGroupsForThing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list thing groups for thing") from exc
    return ListThingGroupsForThingResult(
        thing_groups=resp.get("thingGroups"),
        next_token=resp.get("nextToken"),
    )


async def list_thing_principals(
    thing_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThingPrincipalsResult:
    """List thing principals.

    Args:
        thing_name: Thing name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListThingPrincipals", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list thing principals") from exc
    return ListThingPrincipalsResult(
        principals=resp.get("principals"),
        next_token=resp.get("nextToken"),
    )


async def list_thing_principals_v2(
    thing_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    thing_principal_type: str | None = None,
    region_name: str | None = None,
) -> ListThingPrincipalsV2Result:
    """List thing principals v2.

    Args:
        thing_name: Thing name.
        next_token: Next token.
        max_results: Max results.
        thing_principal_type: Thing principal type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingName"] = thing_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if thing_principal_type is not None:
        kwargs["thingPrincipalType"] = thing_principal_type
    try:
        resp = await client.call("ListThingPrincipalsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list thing principals v2") from exc
    return ListThingPrincipalsV2Result(
        thing_principal_objects=resp.get("thingPrincipalObjects"),
        next_token=resp.get("nextToken"),
    )


async def list_thing_registration_task_reports(
    task_id: str,
    report_type: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThingRegistrationTaskReportsResult:
    """List thing registration task reports.

    Args:
        task_id: Task id.
        report_type: Report type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    kwargs["reportType"] = report_type
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListThingRegistrationTaskReports", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list thing registration task reports") from exc
    return ListThingRegistrationTaskReportsResult(
        resource_links=resp.get("resourceLinks"),
        report_type=resp.get("reportType"),
        next_token=resp.get("nextToken"),
    )


async def list_thing_registration_tasks(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> ListThingRegistrationTasksResult:
    """List thing registration tasks.

    Args:
        next_token: Next token.
        max_results: Max results.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if status is not None:
        kwargs["status"] = status
    try:
        resp = await client.call("ListThingRegistrationTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list thing registration tasks") from exc
    return ListThingRegistrationTasksResult(
        task_ids=resp.get("taskIds"),
        next_token=resp.get("nextToken"),
    )


async def list_things_in_billing_group(
    billing_group_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThingsInBillingGroupResult:
    """List things in billing group.

    Args:
        billing_group_name: Billing group name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["billingGroupName"] = billing_group_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListThingsInBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list things in billing group") from exc
    return ListThingsInBillingGroupResult(
        things=resp.get("things"),
        next_token=resp.get("nextToken"),
    )


async def list_things_in_thing_group(
    thing_group_name: str,
    *,
    recursive: bool | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListThingsInThingGroupResult:
    """List things in thing group.

    Args:
        thing_group_name: Thing group name.
        recursive: Recursive.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    if recursive is not None:
        kwargs["recursive"] = recursive
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListThingsInThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list things in thing group") from exc
    return ListThingsInThingGroupResult(
        things=resp.get("things"),
        next_token=resp.get("nextToken"),
    )


async def list_topic_rule_destinations(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTopicRuleDestinationsResult:
    """List topic rule destinations.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListTopicRuleDestinations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list topic rule destinations") from exc
    return ListTopicRuleDestinationsResult(
        destination_summaries=resp.get("destinationSummaries"),
        next_token=resp.get("nextToken"),
    )


async def list_v2_logging_levels(
    *,
    target_type: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListV2LoggingLevelsResult:
    """List v2 logging levels.

    Args:
        target_type: Target type.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if target_type is not None:
        kwargs["targetType"] = target_type
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListV2LoggingLevels", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list v2 logging levels") from exc
    return ListV2LoggingLevelsResult(
        log_target_configurations=resp.get("logTargetConfigurations"),
        next_token=resp.get("nextToken"),
    )


async def list_violation_events(
    start_time: str,
    end_time: str,
    *,
    thing_name: str | None = None,
    security_profile_name: str | None = None,
    behavior_criteria_type: str | None = None,
    list_suppressed_alerts: bool | None = None,
    verification_state: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListViolationEventsResult:
    """List violation events.

    Args:
        start_time: Start time.
        end_time: End time.
        thing_name: Thing name.
        security_profile_name: Security profile name.
        behavior_criteria_type: Behavior criteria type.
        list_suppressed_alerts: List suppressed alerts.
        verification_state: Verification state.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["startTime"] = start_time
    kwargs["endTime"] = end_time
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if security_profile_name is not None:
        kwargs["securityProfileName"] = security_profile_name
    if behavior_criteria_type is not None:
        kwargs["behaviorCriteriaType"] = behavior_criteria_type
    if list_suppressed_alerts is not None:
        kwargs["listSuppressedAlerts"] = list_suppressed_alerts
    if verification_state is not None:
        kwargs["verificationState"] = verification_state
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListViolationEvents", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list violation events") from exc
    return ListViolationEventsResult(
        violation_events=resp.get("violationEvents"),
        next_token=resp.get("nextToken"),
    )


async def put_verification_state_on_violation(
    violation_id: str,
    verification_state: str,
    *,
    verification_state_description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Put verification state on violation.

    Args:
        violation_id: Violation id.
        verification_state: Verification state.
        verification_state_description: Verification state description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["violationId"] = violation_id
    kwargs["verificationState"] = verification_state
    if verification_state_description is not None:
        kwargs["verificationStateDescription"] = verification_state_description
    try:
        await client.call("PutVerificationStateOnViolation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put verification state on violation") from exc
    return None


async def register_ca_certificate(
    ca_certificate: str,
    *,
    verification_certificate: str | None = None,
    set_as_active: bool | None = None,
    allow_auto_registration: bool | None = None,
    registration_config: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    certificate_mode: str | None = None,
    region_name: str | None = None,
) -> RegisterCaCertificateResult:
    """Register ca certificate.

    Args:
        ca_certificate: Ca certificate.
        verification_certificate: Verification certificate.
        set_as_active: Set as active.
        allow_auto_registration: Allow auto registration.
        registration_config: Registration config.
        tags: Tags.
        certificate_mode: Certificate mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["caCertificate"] = ca_certificate
    if verification_certificate is not None:
        kwargs["verificationCertificate"] = verification_certificate
    if set_as_active is not None:
        kwargs["setAsActive"] = set_as_active
    if allow_auto_registration is not None:
        kwargs["allowAutoRegistration"] = allow_auto_registration
    if registration_config is not None:
        kwargs["registrationConfig"] = registration_config
    if tags is not None:
        kwargs["tags"] = tags
    if certificate_mode is not None:
        kwargs["certificateMode"] = certificate_mode
    try:
        resp = await client.call("RegisterCACertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register ca certificate") from exc
    return RegisterCaCertificateResult(
        certificate_arn=resp.get("certificateArn"),
        certificate_id=resp.get("certificateId"),
    )


async def register_certificate(
    certificate_pem: str,
    *,
    ca_certificate_pem: str | None = None,
    set_as_active: bool | None = None,
    status: str | None = None,
    region_name: str | None = None,
) -> RegisterCertificateResult:
    """Register certificate.

    Args:
        certificate_pem: Certificate pem.
        ca_certificate_pem: Ca certificate pem.
        set_as_active: Set as active.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificatePem"] = certificate_pem
    if ca_certificate_pem is not None:
        kwargs["caCertificatePem"] = ca_certificate_pem
    if set_as_active is not None:
        kwargs["setAsActive"] = set_as_active
    if status is not None:
        kwargs["status"] = status
    try:
        resp = await client.call("RegisterCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register certificate") from exc
    return RegisterCertificateResult(
        certificate_arn=resp.get("certificateArn"),
        certificate_id=resp.get("certificateId"),
    )


async def register_certificate_without_ca(
    certificate_pem: str,
    *,
    status: str | None = None,
    region_name: str | None = None,
) -> RegisterCertificateWithoutCaResult:
    """Register certificate without ca.

    Args:
        certificate_pem: Certificate pem.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificatePem"] = certificate_pem
    if status is not None:
        kwargs["status"] = status
    try:
        resp = await client.call("RegisterCertificateWithoutCA", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register certificate without ca") from exc
    return RegisterCertificateWithoutCaResult(
        certificate_arn=resp.get("certificateArn"),
        certificate_id=resp.get("certificateId"),
    )


async def register_thing(
    template_body: str,
    *,
    parameters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RegisterThingResult:
    """Register thing.

    Args:
        template_body: Template body.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateBody"] = template_body
    if parameters is not None:
        kwargs["parameters"] = parameters
    try:
        resp = await client.call("RegisterThing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register thing") from exc
    return RegisterThingResult(
        certificate_pem=resp.get("certificatePem"),
        resource_arns=resp.get("resourceArns"),
    )


async def reject_certificate_transfer(
    certificate_id: str,
    *,
    reject_reason: str | None = None,
    region_name: str | None = None,
) -> None:
    """Reject certificate transfer.

    Args:
        certificate_id: Certificate id.
        reject_reason: Reject reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    if reject_reason is not None:
        kwargs["rejectReason"] = reject_reason
    try:
        await client.call("RejectCertificateTransfer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reject certificate transfer") from exc
    return None


async def remove_thing_from_billing_group(
    *,
    billing_group_name: str | None = None,
    billing_group_arn: str | None = None,
    thing_name: str | None = None,
    thing_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove thing from billing group.

    Args:
        billing_group_name: Billing group name.
        billing_group_arn: Billing group arn.
        thing_name: Thing name.
        thing_arn: Thing arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if billing_group_name is not None:
        kwargs["billingGroupName"] = billing_group_name
    if billing_group_arn is not None:
        kwargs["billingGroupArn"] = billing_group_arn
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if thing_arn is not None:
        kwargs["thingArn"] = thing_arn
    try:
        await client.call("RemoveThingFromBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove thing from billing group") from exc
    return None


async def remove_thing_from_thing_group(
    *,
    thing_group_name: str | None = None,
    thing_group_arn: str | None = None,
    thing_name: str | None = None,
    thing_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove thing from thing group.

    Args:
        thing_group_name: Thing group name.
        thing_group_arn: Thing group arn.
        thing_name: Thing name.
        thing_arn: Thing arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if thing_group_name is not None:
        kwargs["thingGroupName"] = thing_group_name
    if thing_group_arn is not None:
        kwargs["thingGroupArn"] = thing_group_arn
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if thing_arn is not None:
        kwargs["thingArn"] = thing_arn
    try:
        await client.call("RemoveThingFromThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove thing from thing group") from exc
    return None


async def replace_topic_rule(
    rule_name: str,
    topic_rule_payload: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Replace topic rule.

    Args:
        rule_name: Rule name.
        topic_rule_payload: Topic rule payload.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ruleName"] = rule_name
    kwargs["topicRulePayload"] = topic_rule_payload
    try:
        await client.call("ReplaceTopicRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to replace topic rule") from exc
    return None


async def run_authorization(
    auth_infos: list[dict[str, Any]],
    *,
    principal: str | None = None,
    cognito_identity_pool_id: str | None = None,
    client_id: str | None = None,
    policy_names_to_add: list[str] | None = None,
    policy_names_to_skip: list[str] | None = None,
    region_name: str | None = None,
) -> RunAuthorizationResult:
    """Run authorization.

    Args:
        auth_infos: Auth infos.
        principal: Principal.
        cognito_identity_pool_id: Cognito identity pool id.
        client_id: Client id.
        policy_names_to_add: Policy names to add.
        policy_names_to_skip: Policy names to skip.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authInfos"] = auth_infos
    if principal is not None:
        kwargs["principal"] = principal
    if cognito_identity_pool_id is not None:
        kwargs["cognitoIdentityPoolId"] = cognito_identity_pool_id
    if client_id is not None:
        kwargs["clientId"] = client_id
    if policy_names_to_add is not None:
        kwargs["policyNamesToAdd"] = policy_names_to_add
    if policy_names_to_skip is not None:
        kwargs["policyNamesToSkip"] = policy_names_to_skip
    try:
        resp = await client.call("TestAuthorization", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run authorization") from exc
    return RunAuthorizationResult(
        auth_results=resp.get("authResults"),
    )


async def run_invoke_authorizer(
    authorizer_name: str,
    *,
    token: str | None = None,
    token_signature: str | None = None,
    http_context: dict[str, Any] | None = None,
    mqtt_context: dict[str, Any] | None = None,
    tls_context: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RunInvokeAuthorizerResult:
    """Run invoke authorizer.

    Args:
        authorizer_name: Authorizer name.
        token: Token.
        token_signature: Token signature.
        http_context: Http context.
        mqtt_context: Mqtt context.
        tls_context: Tls context.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authorizerName"] = authorizer_name
    if token is not None:
        kwargs["token"] = token
    if token_signature is not None:
        kwargs["tokenSignature"] = token_signature
    if http_context is not None:
        kwargs["httpContext"] = http_context
    if mqtt_context is not None:
        kwargs["mqttContext"] = mqtt_context
    if tls_context is not None:
        kwargs["tlsContext"] = tls_context
    try:
        resp = await client.call("TestInvokeAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to run invoke authorizer") from exc
    return RunInvokeAuthorizerResult(
        is_authenticated=resp.get("isAuthenticated"),
        principal_id=resp.get("principalId"),
        policy_documents=resp.get("policyDocuments"),
        refresh_after_in_seconds=resp.get("refreshAfterInSeconds"),
        disconnect_after_in_seconds=resp.get("disconnectAfterInSeconds"),
    )


async def search_index(
    query_string: str,
    *,
    index_name: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    query_version: str | None = None,
    region_name: str | None = None,
) -> SearchIndexResult:
    """Search index.

    Args:
        query_string: Query string.
        index_name: Index name.
        next_token: Next token.
        max_results: Max results.
        query_version: Query version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["queryString"] = query_string
    if index_name is not None:
        kwargs["indexName"] = index_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    try:
        resp = await client.call("SearchIndex", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to search index") from exc
    return SearchIndexResult(
        next_token=resp.get("nextToken"),
        things=resp.get("things"),
        thing_groups=resp.get("thingGroups"),
    )


async def set_default_authorizer(
    authorizer_name: str,
    region_name: str | None = None,
) -> SetDefaultAuthorizerResult:
    """Set default authorizer.

    Args:
        authorizer_name: Authorizer name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authorizerName"] = authorizer_name
    try:
        resp = await client.call("SetDefaultAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set default authorizer") from exc
    return SetDefaultAuthorizerResult(
        authorizer_name=resp.get("authorizerName"),
        authorizer_arn=resp.get("authorizerArn"),
    )


async def set_default_policy_version(
    policy_name: str,
    policy_version_id: str,
    region_name: str | None = None,
) -> None:
    """Set default policy version.

    Args:
        policy_name: Policy name.
        policy_version_id: Policy version id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["policyName"] = policy_name
    kwargs["policyVersionId"] = policy_version_id
    try:
        await client.call("SetDefaultPolicyVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set default policy version") from exc
    return None


async def set_logging_options(
    logging_options_payload: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Set logging options.

    Args:
        logging_options_payload: Logging options payload.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["loggingOptionsPayload"] = logging_options_payload
    try:
        await client.call("SetLoggingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set logging options") from exc
    return None


async def set_v2_logging_level(
    log_target: dict[str, Any],
    log_level: str,
    region_name: str | None = None,
) -> None:
    """Set v2 logging level.

    Args:
        log_target: Log target.
        log_level: Log level.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["logTarget"] = log_target
    kwargs["logLevel"] = log_level
    try:
        await client.call("SetV2LoggingLevel", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set v2 logging level") from exc
    return None


async def set_v2_logging_options(
    *,
    role_arn: str | None = None,
    default_log_level: str | None = None,
    disable_all_logs: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Set v2 logging options.

    Args:
        role_arn: Role arn.
        default_log_level: Default log level.
        disable_all_logs: Disable all logs.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if default_log_level is not None:
        kwargs["defaultLogLevel"] = default_log_level
    if disable_all_logs is not None:
        kwargs["disableAllLogs"] = disable_all_logs
    try:
        await client.call("SetV2LoggingOptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to set v2 logging options") from exc
    return None


async def start_audit_mitigation_actions_task(
    task_id: str,
    target: dict[str, Any],
    audit_check_to_actions_mapping: dict[str, Any],
    client_request_token: str,
    region_name: str | None = None,
) -> StartAuditMitigationActionsTaskResult:
    """Start audit mitigation actions task.

    Args:
        task_id: Task id.
        target: Target.
        audit_check_to_actions_mapping: Audit check to actions mapping.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    kwargs["target"] = target
    kwargs["auditCheckToActionsMapping"] = audit_check_to_actions_mapping
    kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("StartAuditMitigationActionsTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start audit mitigation actions task") from exc
    return StartAuditMitigationActionsTaskResult(
        task_id=resp.get("taskId"),
    )


async def start_detect_mitigation_actions_task(
    task_id: str,
    target: dict[str, Any],
    actions: list[str],
    client_request_token: str,
    *,
    violation_event_occurrence_range: dict[str, Any] | None = None,
    include_only_active_violations: bool | None = None,
    include_suppressed_alerts: bool | None = None,
    region_name: str | None = None,
) -> StartDetectMitigationActionsTaskResult:
    """Start detect mitigation actions task.

    Args:
        task_id: Task id.
        target: Target.
        actions: Actions.
        client_request_token: Client request token.
        violation_event_occurrence_range: Violation event occurrence range.
        include_only_active_violations: Include only active violations.
        include_suppressed_alerts: Include suppressed alerts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    kwargs["target"] = target
    kwargs["actions"] = actions
    kwargs["clientRequestToken"] = client_request_token
    if violation_event_occurrence_range is not None:
        kwargs["violationEventOccurrenceRange"] = violation_event_occurrence_range
    if include_only_active_violations is not None:
        kwargs["includeOnlyActiveViolations"] = include_only_active_violations
    if include_suppressed_alerts is not None:
        kwargs["includeSuppressedAlerts"] = include_suppressed_alerts
    try:
        resp = await client.call("StartDetectMitigationActionsTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start detect mitigation actions task") from exc
    return StartDetectMitigationActionsTaskResult(
        task_id=resp.get("taskId"),
    )


async def start_on_demand_audit_task(
    target_check_names: list[str],
    region_name: str | None = None,
) -> StartOnDemandAuditTaskResult:
    """Start on demand audit task.

    Args:
        target_check_names: Target check names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["targetCheckNames"] = target_check_names
    try:
        resp = await client.call("StartOnDemandAuditTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start on demand audit task") from exc
    return StartOnDemandAuditTaskResult(
        task_id=resp.get("taskId"),
    )


async def start_thing_registration_task(
    template_body: str,
    input_file_bucket: str,
    input_file_key: str,
    role_arn: str,
    region_name: str | None = None,
) -> StartThingRegistrationTaskResult:
    """Start thing registration task.

    Args:
        template_body: Template body.
        input_file_bucket: Input file bucket.
        input_file_key: Input file key.
        role_arn: Role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateBody"] = template_body
    kwargs["inputFileBucket"] = input_file_bucket
    kwargs["inputFileKey"] = input_file_key
    kwargs["roleArn"] = role_arn
    try:
        resp = await client.call("StartThingRegistrationTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start thing registration task") from exc
    return StartThingRegistrationTaskResult(
        task_id=resp.get("taskId"),
    )


async def stop_thing_registration_task(
    task_id: str,
    region_name: str | None = None,
) -> None:
    """Stop thing registration task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskId"] = task_id
    try:
        await client.call("StopThingRegistrationTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop thing registration task") from exc
    return None


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
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
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def transfer_certificate(
    certificate_id: str,
    target_aws_account: str,
    *,
    transfer_message: str | None = None,
    region_name: str | None = None,
) -> TransferCertificateResult:
    """Transfer certificate.

    Args:
        certificate_id: Certificate id.
        target_aws_account: Target aws account.
        transfer_message: Transfer message.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    kwargs["targetAwsAccount"] = target_aws_account
    if transfer_message is not None:
        kwargs["transferMessage"] = transfer_message
    try:
        resp = await client.call("TransferCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to transfer certificate") from exc
    return TransferCertificateResult(
        transferred_certificate_arn=resp.get("transferredCertificateArn"),
    )


async def untag_resource(
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
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_account_audit_configuration(
    *,
    role_arn: str | None = None,
    audit_notification_target_configurations: dict[str, Any] | None = None,
    audit_check_configurations: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update account audit configuration.

    Args:
        role_arn: Role arn.
        audit_notification_target_configurations: Audit notification target configurations.
        audit_check_configurations: Audit check configurations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if audit_notification_target_configurations is not None:
        kwargs["auditNotificationTargetConfigurations"] = audit_notification_target_configurations
    if audit_check_configurations is not None:
        kwargs["auditCheckConfigurations"] = audit_check_configurations
    try:
        await client.call("UpdateAccountAuditConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account audit configuration") from exc
    return None


async def update_audit_suppression(
    check_name: str,
    resource_identifier: dict[str, Any],
    *,
    expiration_date: str | None = None,
    suppress_indefinitely: bool | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update audit suppression.

    Args:
        check_name: Check name.
        resource_identifier: Resource identifier.
        expiration_date: Expiration date.
        suppress_indefinitely: Suppress indefinitely.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["checkName"] = check_name
    kwargs["resourceIdentifier"] = resource_identifier
    if expiration_date is not None:
        kwargs["expirationDate"] = expiration_date
    if suppress_indefinitely is not None:
        kwargs["suppressIndefinitely"] = suppress_indefinitely
    if description is not None:
        kwargs["description"] = description
    try:
        await client.call("UpdateAuditSuppression", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update audit suppression") from exc
    return None


async def update_authorizer(
    authorizer_name: str,
    *,
    authorizer_function_arn: str | None = None,
    token_key_name: str | None = None,
    token_signing_public_keys: dict[str, Any] | None = None,
    status: str | None = None,
    enable_caching_for_http: bool | None = None,
    region_name: str | None = None,
) -> UpdateAuthorizerResult:
    """Update authorizer.

    Args:
        authorizer_name: Authorizer name.
        authorizer_function_arn: Authorizer function arn.
        token_key_name: Token key name.
        token_signing_public_keys: Token signing public keys.
        status: Status.
        enable_caching_for_http: Enable caching for http.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["authorizerName"] = authorizer_name
    if authorizer_function_arn is not None:
        kwargs["authorizerFunctionArn"] = authorizer_function_arn
    if token_key_name is not None:
        kwargs["tokenKeyName"] = token_key_name
    if token_signing_public_keys is not None:
        kwargs["tokenSigningPublicKeys"] = token_signing_public_keys
    if status is not None:
        kwargs["status"] = status
    if enable_caching_for_http is not None:
        kwargs["enableCachingForHttp"] = enable_caching_for_http
    try:
        resp = await client.call("UpdateAuthorizer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update authorizer") from exc
    return UpdateAuthorizerResult(
        authorizer_name=resp.get("authorizerName"),
        authorizer_arn=resp.get("authorizerArn"),
    )


async def update_billing_group(
    billing_group_name: str,
    billing_group_properties: dict[str, Any],
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> UpdateBillingGroupResult:
    """Update billing group.

    Args:
        billing_group_name: Billing group name.
        billing_group_properties: Billing group properties.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["billingGroupName"] = billing_group_name
    kwargs["billingGroupProperties"] = billing_group_properties
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        resp = await client.call("UpdateBillingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update billing group") from exc
    return UpdateBillingGroupResult(
        version=resp.get("version"),
    )


async def update_ca_certificate(
    certificate_id: str,
    *,
    new_status: str | None = None,
    new_auto_registration_status: str | None = None,
    registration_config: dict[str, Any] | None = None,
    remove_auto_registration: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update ca certificate.

    Args:
        certificate_id: Certificate id.
        new_status: New status.
        new_auto_registration_status: New auto registration status.
        registration_config: Registration config.
        remove_auto_registration: Remove auto registration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    if new_status is not None:
        kwargs["newStatus"] = new_status
    if new_auto_registration_status is not None:
        kwargs["newAutoRegistrationStatus"] = new_auto_registration_status
    if registration_config is not None:
        kwargs["registrationConfig"] = registration_config
    if remove_auto_registration is not None:
        kwargs["removeAutoRegistration"] = remove_auto_registration
    try:
        await client.call("UpdateCACertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update ca certificate") from exc
    return None


async def update_certificate(
    certificate_id: str,
    new_status: str,
    region_name: str | None = None,
) -> None:
    """Update certificate.

    Args:
        certificate_id: Certificate id.
        new_status: New status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateId"] = certificate_id
    kwargs["newStatus"] = new_status
    try:
        await client.call("UpdateCertificate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update certificate") from exc
    return None


async def update_certificate_provider(
    certificate_provider_name: str,
    *,
    lambda_function_arn: str | None = None,
    account_default_for_operations: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateCertificateProviderResult:
    """Update certificate provider.

    Args:
        certificate_provider_name: Certificate provider name.
        lambda_function_arn: Lambda function arn.
        account_default_for_operations: Account default for operations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["certificateProviderName"] = certificate_provider_name
    if lambda_function_arn is not None:
        kwargs["lambdaFunctionArn"] = lambda_function_arn
    if account_default_for_operations is not None:
        kwargs["accountDefaultForOperations"] = account_default_for_operations
    try:
        resp = await client.call("UpdateCertificateProvider", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update certificate provider") from exc
    return UpdateCertificateProviderResult(
        certificate_provider_name=resp.get("certificateProviderName"),
        certificate_provider_arn=resp.get("certificateProviderArn"),
    )


async def update_command(
    command_id: str,
    *,
    display_name: str | None = None,
    description: str | None = None,
    deprecated: bool | None = None,
    region_name: str | None = None,
) -> UpdateCommandResult:
    """Update command.

    Args:
        command_id: Command id.
        display_name: Display name.
        description: Description.
        deprecated: Deprecated.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["commandId"] = command_id
    if display_name is not None:
        kwargs["displayName"] = display_name
    if description is not None:
        kwargs["description"] = description
    if deprecated is not None:
        kwargs["deprecated"] = deprecated
    try:
        resp = await client.call("UpdateCommand", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update command") from exc
    return UpdateCommandResult(
        command_id=resp.get("commandId"),
        display_name=resp.get("displayName"),
        description=resp.get("description"),
        deprecated=resp.get("deprecated"),
        last_updated_at=resp.get("lastUpdatedAt"),
    )


async def update_custom_metric(
    metric_name: str,
    display_name: str,
    region_name: str | None = None,
) -> UpdateCustomMetricResult:
    """Update custom metric.

    Args:
        metric_name: Metric name.
        display_name: Display name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    kwargs["displayName"] = display_name
    try:
        resp = await client.call("UpdateCustomMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update custom metric") from exc
    return UpdateCustomMetricResult(
        metric_name=resp.get("metricName"),
        metric_arn=resp.get("metricArn"),
        metric_type=resp.get("metricType"),
        display_name=resp.get("displayName"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def update_dimension(
    name: str,
    string_values: list[str],
    region_name: str | None = None,
) -> UpdateDimensionResult:
    """Update dimension.

    Args:
        name: Name.
        string_values: String values.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["stringValues"] = string_values
    try:
        resp = await client.call("UpdateDimension", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dimension") from exc
    return UpdateDimensionResult(
        name=resp.get("name"),
        arn=resp.get("arn"),
        type_value=resp.get("type"),
        string_values=resp.get("stringValues"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
    )


async def update_domain_configuration(
    domain_configuration_name: str,
    *,
    authorizer_config: dict[str, Any] | None = None,
    domain_configuration_status: str | None = None,
    remove_authorizer_config: bool | None = None,
    tls_config: dict[str, Any] | None = None,
    server_certificate_config: dict[str, Any] | None = None,
    authentication_type: str | None = None,
    application_protocol: str | None = None,
    client_certificate_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateDomainConfigurationResult:
    """Update domain configuration.

    Args:
        domain_configuration_name: Domain configuration name.
        authorizer_config: Authorizer config.
        domain_configuration_status: Domain configuration status.
        remove_authorizer_config: Remove authorizer config.
        tls_config: Tls config.
        server_certificate_config: Server certificate config.
        authentication_type: Authentication type.
        application_protocol: Application protocol.
        client_certificate_config: Client certificate config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["domainConfigurationName"] = domain_configuration_name
    if authorizer_config is not None:
        kwargs["authorizerConfig"] = authorizer_config
    if domain_configuration_status is not None:
        kwargs["domainConfigurationStatus"] = domain_configuration_status
    if remove_authorizer_config is not None:
        kwargs["removeAuthorizerConfig"] = remove_authorizer_config
    if tls_config is not None:
        kwargs["tlsConfig"] = tls_config
    if server_certificate_config is not None:
        kwargs["serverCertificateConfig"] = server_certificate_config
    if authentication_type is not None:
        kwargs["authenticationType"] = authentication_type
    if application_protocol is not None:
        kwargs["applicationProtocol"] = application_protocol
    if client_certificate_config is not None:
        kwargs["clientCertificateConfig"] = client_certificate_config
    try:
        resp = await client.call("UpdateDomainConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update domain configuration") from exc
    return UpdateDomainConfigurationResult(
        domain_configuration_name=resp.get("domainConfigurationName"),
        domain_configuration_arn=resp.get("domainConfigurationArn"),
    )


async def update_dynamic_thing_group(
    thing_group_name: str,
    thing_group_properties: dict[str, Any],
    *,
    expected_version: int | None = None,
    index_name: str | None = None,
    query_string: str | None = None,
    query_version: str | None = None,
    region_name: str | None = None,
) -> UpdateDynamicThingGroupResult:
    """Update dynamic thing group.

    Args:
        thing_group_name: Thing group name.
        thing_group_properties: Thing group properties.
        expected_version: Expected version.
        index_name: Index name.
        query_string: Query string.
        query_version: Query version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    kwargs["thingGroupProperties"] = thing_group_properties
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    if index_name is not None:
        kwargs["indexName"] = index_name
    if query_string is not None:
        kwargs["queryString"] = query_string
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    try:
        resp = await client.call("UpdateDynamicThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update dynamic thing group") from exc
    return UpdateDynamicThingGroupResult(
        version=resp.get("version"),
    )


async def update_encryption_configuration(
    encryption_type: str,
    *,
    kms_key_arn: str | None = None,
    kms_access_role_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update encryption configuration.

    Args:
        encryption_type: Encryption type.
        kms_key_arn: Kms key arn.
        kms_access_role_arn: Kms access role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["encryptionType"] = encryption_type
    if kms_key_arn is not None:
        kwargs["kmsKeyArn"] = kms_key_arn
    if kms_access_role_arn is not None:
        kwargs["kmsAccessRoleArn"] = kms_access_role_arn
    try:
        await client.call("UpdateEncryptionConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update encryption configuration") from exc
    return None


async def update_event_configurations(
    *,
    event_configurations: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update event configurations.

    Args:
        event_configurations: Event configurations.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if event_configurations is not None:
        kwargs["eventConfigurations"] = event_configurations
    try:
        await client.call("UpdateEventConfigurations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update event configurations") from exc
    return None


async def update_fleet_metric(
    metric_name: str,
    index_name: str,
    *,
    query_string: str | None = None,
    aggregation_type: dict[str, Any] | None = None,
    period: int | None = None,
    aggregation_field: str | None = None,
    description: str | None = None,
    query_version: str | None = None,
    unit: str | None = None,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update fleet metric.

    Args:
        metric_name: Metric name.
        index_name: Index name.
        query_string: Query string.
        aggregation_type: Aggregation type.
        period: Period.
        aggregation_field: Aggregation field.
        description: Description.
        query_version: Query version.
        unit: Unit.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["metricName"] = metric_name
    kwargs["indexName"] = index_name
    if query_string is not None:
        kwargs["queryString"] = query_string
    if aggregation_type is not None:
        kwargs["aggregationType"] = aggregation_type
    if period is not None:
        kwargs["period"] = period
    if aggregation_field is not None:
        kwargs["aggregationField"] = aggregation_field
    if description is not None:
        kwargs["description"] = description
    if query_version is not None:
        kwargs["queryVersion"] = query_version
    if unit is not None:
        kwargs["unit"] = unit
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        await client.call("UpdateFleetMetric", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update fleet metric") from exc
    return None


async def update_indexing_configuration(
    *,
    thing_indexing_configuration: dict[str, Any] | None = None,
    thing_group_indexing_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update indexing configuration.

    Args:
        thing_indexing_configuration: Thing indexing configuration.
        thing_group_indexing_configuration: Thing group indexing configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if thing_indexing_configuration is not None:
        kwargs["thingIndexingConfiguration"] = thing_indexing_configuration
    if thing_group_indexing_configuration is not None:
        kwargs["thingGroupIndexingConfiguration"] = thing_group_indexing_configuration
    try:
        await client.call("UpdateIndexingConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update indexing configuration") from exc
    return None


async def update_job(
    job_id: str,
    *,
    description: str | None = None,
    presigned_url_config: dict[str, Any] | None = None,
    job_executions_rollout_config: dict[str, Any] | None = None,
    abort_config: dict[str, Any] | None = None,
    timeout_config: dict[str, Any] | None = None,
    namespace_id: str | None = None,
    job_executions_retry_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update job.

    Args:
        job_id: Job id.
        description: Description.
        presigned_url_config: Presigned url config.
        job_executions_rollout_config: Job executions rollout config.
        abort_config: Abort config.
        timeout_config: Timeout config.
        namespace_id: Namespace id.
        job_executions_retry_config: Job executions retry config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["jobId"] = job_id
    if description is not None:
        kwargs["description"] = description
    if presigned_url_config is not None:
        kwargs["presignedUrlConfig"] = presigned_url_config
    if job_executions_rollout_config is not None:
        kwargs["jobExecutionsRolloutConfig"] = job_executions_rollout_config
    if abort_config is not None:
        kwargs["abortConfig"] = abort_config
    if timeout_config is not None:
        kwargs["timeoutConfig"] = timeout_config
    if namespace_id is not None:
        kwargs["namespaceId"] = namespace_id
    if job_executions_retry_config is not None:
        kwargs["jobExecutionsRetryConfig"] = job_executions_retry_config
    try:
        await client.call("UpdateJob", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update job") from exc
    return None


async def update_mitigation_action(
    action_name: str,
    *,
    role_arn: str | None = None,
    action_params: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateMitigationActionResult:
    """Update mitigation action.

    Args:
        action_name: Action name.
        role_arn: Role arn.
        action_params: Action params.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["actionName"] = action_name
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if action_params is not None:
        kwargs["actionParams"] = action_params
    try:
        resp = await client.call("UpdateMitigationAction", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update mitigation action") from exc
    return UpdateMitigationActionResult(
        action_arn=resp.get("actionArn"),
        action_id=resp.get("actionId"),
    )


async def update_package(
    package_name: str,
    *,
    description: str | None = None,
    default_version_name: str | None = None,
    unset_default_version: bool | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update package.

    Args:
        package_name: Package name.
        description: Description.
        default_version_name: Default version name.
        unset_default_version: Unset default version.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    if description is not None:
        kwargs["description"] = description
    if default_version_name is not None:
        kwargs["defaultVersionName"] = default_version_name
    if unset_default_version is not None:
        kwargs["unsetDefaultVersion"] = unset_default_version
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("UpdatePackage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update package") from exc
    return None


async def update_package_configuration(
    *,
    version_update_by_jobs_config: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update package configuration.

    Args:
        version_update_by_jobs_config: Version update by jobs config.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if version_update_by_jobs_config is not None:
        kwargs["versionUpdateByJobsConfig"] = version_update_by_jobs_config
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("UpdatePackageConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update package configuration") from exc
    return None


async def update_package_version(
    package_name: str,
    version_name: str,
    *,
    description: str | None = None,
    attributes: dict[str, Any] | None = None,
    artifact: dict[str, Any] | None = None,
    action: str | None = None,
    recipe: str | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update package version.

    Args:
        package_name: Package name.
        version_name: Version name.
        description: Description.
        attributes: Attributes.
        artifact: Artifact.
        action: Action.
        recipe: Recipe.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["packageName"] = package_name
    kwargs["versionName"] = version_name
    if description is not None:
        kwargs["description"] = description
    if attributes is not None:
        kwargs["attributes"] = attributes
    if artifact is not None:
        kwargs["artifact"] = artifact
    if action is not None:
        kwargs["action"] = action
    if recipe is not None:
        kwargs["recipe"] = recipe
    if client_token is not None:
        kwargs["clientToken"] = client_token
    try:
        await client.call("UpdatePackageVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update package version") from exc
    return None


async def update_provisioning_template(
    template_name: str,
    *,
    description: str | None = None,
    enabled: bool | None = None,
    default_version_id: int | None = None,
    provisioning_role_arn: str | None = None,
    pre_provisioning_hook: dict[str, Any] | None = None,
    remove_pre_provisioning_hook: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update provisioning template.

    Args:
        template_name: Template name.
        description: Description.
        enabled: Enabled.
        default_version_id: Default version id.
        provisioning_role_arn: Provisioning role arn.
        pre_provisioning_hook: Pre provisioning hook.
        remove_pre_provisioning_hook: Remove pre provisioning hook.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["templateName"] = template_name
    if description is not None:
        kwargs["description"] = description
    if enabled is not None:
        kwargs["enabled"] = enabled
    if default_version_id is not None:
        kwargs["defaultVersionId"] = default_version_id
    if provisioning_role_arn is not None:
        kwargs["provisioningRoleArn"] = provisioning_role_arn
    if pre_provisioning_hook is not None:
        kwargs["preProvisioningHook"] = pre_provisioning_hook
    if remove_pre_provisioning_hook is not None:
        kwargs["removePreProvisioningHook"] = remove_pre_provisioning_hook
    try:
        await client.call("UpdateProvisioningTemplate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update provisioning template") from exc
    return None


async def update_role_alias(
    role_alias: str,
    *,
    role_arn: str | None = None,
    credential_duration_seconds: int | None = None,
    region_name: str | None = None,
) -> UpdateRoleAliasResult:
    """Update role alias.

    Args:
        role_alias: Role alias.
        role_arn: Role arn.
        credential_duration_seconds: Credential duration seconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["roleAlias"] = role_alias
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if credential_duration_seconds is not None:
        kwargs["credentialDurationSeconds"] = credential_duration_seconds
    try:
        resp = await client.call("UpdateRoleAlias", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update role alias") from exc
    return UpdateRoleAliasResult(
        role_alias=resp.get("roleAlias"),
        role_alias_arn=resp.get("roleAliasArn"),
    )


async def update_scheduled_audit(
    scheduled_audit_name: str,
    *,
    frequency: str | None = None,
    day_of_month: str | None = None,
    day_of_week: str | None = None,
    target_check_names: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateScheduledAuditResult:
    """Update scheduled audit.

    Args:
        scheduled_audit_name: Scheduled audit name.
        frequency: Frequency.
        day_of_month: Day of month.
        day_of_week: Day of week.
        target_check_names: Target check names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["scheduledAuditName"] = scheduled_audit_name
    if frequency is not None:
        kwargs["frequency"] = frequency
    if day_of_month is not None:
        kwargs["dayOfMonth"] = day_of_month
    if day_of_week is not None:
        kwargs["dayOfWeek"] = day_of_week
    if target_check_names is not None:
        kwargs["targetCheckNames"] = target_check_names
    try:
        resp = await client.call("UpdateScheduledAudit", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update scheduled audit") from exc
    return UpdateScheduledAuditResult(
        scheduled_audit_arn=resp.get("scheduledAuditArn"),
    )


async def update_security_profile(
    security_profile_name: str,
    *,
    security_profile_description: str | None = None,
    behaviors: list[dict[str, Any]] | None = None,
    alert_targets: dict[str, Any] | None = None,
    additional_metrics_to_retain: list[str] | None = None,
    additional_metrics_to_retain_v2: list[dict[str, Any]] | None = None,
    delete_behaviors: bool | None = None,
    delete_alert_targets: bool | None = None,
    delete_additional_metrics_to_retain: bool | None = None,
    expected_version: int | None = None,
    metrics_export_config: dict[str, Any] | None = None,
    delete_metrics_export_config: bool | None = None,
    region_name: str | None = None,
) -> UpdateSecurityProfileResult:
    """Update security profile.

    Args:
        security_profile_name: Security profile name.
        security_profile_description: Security profile description.
        behaviors: Behaviors.
        alert_targets: Alert targets.
        additional_metrics_to_retain: Additional metrics to retain.
        additional_metrics_to_retain_v2: Additional metrics to retain v2.
        delete_behaviors: Delete behaviors.
        delete_alert_targets: Delete alert targets.
        delete_additional_metrics_to_retain: Delete additional metrics to retain.
        expected_version: Expected version.
        metrics_export_config: Metrics export config.
        delete_metrics_export_config: Delete metrics export config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["securityProfileName"] = security_profile_name
    if security_profile_description is not None:
        kwargs["securityProfileDescription"] = security_profile_description
    if behaviors is not None:
        kwargs["behaviors"] = behaviors
    if alert_targets is not None:
        kwargs["alertTargets"] = alert_targets
    if additional_metrics_to_retain is not None:
        kwargs["additionalMetricsToRetain"] = additional_metrics_to_retain
    if additional_metrics_to_retain_v2 is not None:
        kwargs["additionalMetricsToRetainV2"] = additional_metrics_to_retain_v2
    if delete_behaviors is not None:
        kwargs["deleteBehaviors"] = delete_behaviors
    if delete_alert_targets is not None:
        kwargs["deleteAlertTargets"] = delete_alert_targets
    if delete_additional_metrics_to_retain is not None:
        kwargs["deleteAdditionalMetricsToRetain"] = delete_additional_metrics_to_retain
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    if metrics_export_config is not None:
        kwargs["metricsExportConfig"] = metrics_export_config
    if delete_metrics_export_config is not None:
        kwargs["deleteMetricsExportConfig"] = delete_metrics_export_config
    try:
        resp = await client.call("UpdateSecurityProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update security profile") from exc
    return UpdateSecurityProfileResult(
        security_profile_name=resp.get("securityProfileName"),
        security_profile_arn=resp.get("securityProfileArn"),
        security_profile_description=resp.get("securityProfileDescription"),
        behaviors=resp.get("behaviors"),
        alert_targets=resp.get("alertTargets"),
        additional_metrics_to_retain=resp.get("additionalMetricsToRetain"),
        additional_metrics_to_retain_v2=resp.get("additionalMetricsToRetainV2"),
        version=resp.get("version"),
        creation_date=resp.get("creationDate"),
        last_modified_date=resp.get("lastModifiedDate"),
        metrics_export_config=resp.get("metricsExportConfig"),
    )


async def update_stream(
    stream_id: str,
    *,
    description: str | None = None,
    files: list[dict[str, Any]] | None = None,
    role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateStreamResult:
    """Update stream.

    Args:
        stream_id: Stream id.
        description: Description.
        files: Files.
        role_arn: Role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["streamId"] = stream_id
    if description is not None:
        kwargs["description"] = description
    if files is not None:
        kwargs["files"] = files
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    try:
        resp = await client.call("UpdateStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update stream") from exc
    return UpdateStreamResult(
        stream_id=resp.get("streamId"),
        stream_arn=resp.get("streamArn"),
        description=resp.get("description"),
        stream_version=resp.get("streamVersion"),
    )


async def update_thing_group(
    thing_group_name: str,
    thing_group_properties: dict[str, Any],
    *,
    expected_version: int | None = None,
    region_name: str | None = None,
) -> UpdateThingGroupResult:
    """Update thing group.

    Args:
        thing_group_name: Thing group name.
        thing_group_properties: Thing group properties.
        expected_version: Expected version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingGroupName"] = thing_group_name
    kwargs["thingGroupProperties"] = thing_group_properties
    if expected_version is not None:
        kwargs["expectedVersion"] = expected_version
    try:
        resp = await client.call("UpdateThingGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update thing group") from exc
    return UpdateThingGroupResult(
        version=resp.get("version"),
    )


async def update_thing_groups_for_thing(
    *,
    thing_name: str | None = None,
    thing_groups_to_add: list[str] | None = None,
    thing_groups_to_remove: list[str] | None = None,
    override_dynamic_groups: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Update thing groups for thing.

    Args:
        thing_name: Thing name.
        thing_groups_to_add: Thing groups to add.
        thing_groups_to_remove: Thing groups to remove.
        override_dynamic_groups: Override dynamic groups.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    if thing_name is not None:
        kwargs["thingName"] = thing_name
    if thing_groups_to_add is not None:
        kwargs["thingGroupsToAdd"] = thing_groups_to_add
    if thing_groups_to_remove is not None:
        kwargs["thingGroupsToRemove"] = thing_groups_to_remove
    if override_dynamic_groups is not None:
        kwargs["overrideDynamicGroups"] = override_dynamic_groups
    try:
        await client.call("UpdateThingGroupsForThing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update thing groups for thing") from exc
    return None


async def update_thing_type(
    thing_type_name: str,
    *,
    thing_type_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update thing type.

    Args:
        thing_type_name: Thing type name.
        thing_type_properties: Thing type properties.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["thingTypeName"] = thing_type_name
    if thing_type_properties is not None:
        kwargs["thingTypeProperties"] = thing_type_properties
    try:
        await client.call("UpdateThingType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update thing type") from exc
    return None


async def update_topic_rule_destination(
    arn: str,
    status: str,
    region_name: str | None = None,
) -> None:
    """Update topic rule destination.

    Args:
        arn: Arn.
        status: Status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["arn"] = arn
    kwargs["status"] = status
    try:
        await client.call("UpdateTopicRuleDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update topic rule destination") from exc
    return None


async def validate_security_profile_behaviors(
    behaviors: list[dict[str, Any]],
    region_name: str | None = None,
) -> ValidateSecurityProfileBehaviorsResult:
    """Validate security profile behaviors.

    Args:
        behaviors: Behaviors.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("iot", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["behaviors"] = behaviors
    try:
        resp = await client.call("ValidateSecurityProfileBehaviors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to validate security profile behaviors") from exc
    return ValidateSecurityProfileBehaviorsResult(
        valid=resp.get("valid"),
        validation_errors=resp.get("validationErrors"),
    )
