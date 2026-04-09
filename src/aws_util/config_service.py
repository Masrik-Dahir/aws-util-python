"""aws_util.config_service — AWS Config utilities.

Provides functions for managing AWS Config rules, configuration recorders,
compliance evaluation, remediation, resource discovery, and aggregation.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "AssociateResourceTypesResult",
    "BatchGetAggregateResourceConfigResult",
    "BatchGetResourceConfigResult",
    "ComplianceResult",
    "ConfigRuleResult",
    "ConfigurationRecorderResult",
    "DeleteRemediationExceptionsResult",
    "DeleteServiceLinkedConfigurationRecorderResult",
    "DescribeAggregateComplianceByConfigRulesResult",
    "DescribeAggregateComplianceByConformancePacksResult",
    "DescribeAggregationAuthorizationsResult",
    "DescribeComplianceByResourceResult",
    "DescribeConfigRuleEvaluationStatusResult",
    "DescribeConfigurationAggregatorSourcesStatusResult",
    "DescribeConfigurationRecorderStatusResult",
    "DescribeConformancePackComplianceResult",
    "DescribeConformancePackStatusResult",
    "DescribeConformancePacksResult",
    "DescribeDeliveryChannelStatusResult",
    "DescribeDeliveryChannelsResult",
    "DescribeOrganizationConfigRuleStatusesResult",
    "DescribeOrganizationConfigRulesResult",
    "DescribeOrganizationConformancePackStatusesResult",
    "DescribeOrganizationConformancePacksResult",
    "DescribePendingAggregationRequestsResult",
    "DescribeRemediationExceptionsResult",
    "DescribeRemediationExecutionStatusResult",
    "DescribeRetentionConfigurationsResult",
    "DisassociateResourceTypesResult",
    "GetAggregateComplianceDetailsByConfigRuleResult",
    "GetAggregateConfigRuleComplianceSummaryResult",
    "GetAggregateConformancePackComplianceSummaryResult",
    "GetAggregateDiscoveredResourceCountsResult",
    "GetAggregateResourceConfigResult",
    "GetComplianceDetailsByResourceResult",
    "GetComplianceSummaryByConfigRuleResult",
    "GetComplianceSummaryByResourceTypeResult",
    "GetConformancePackComplianceDetailsResult",
    "GetConformancePackComplianceSummaryResult",
    "GetCustomRulePolicyResult",
    "GetDiscoveredResourceCountsResult",
    "GetOrganizationConfigRuleDetailedStatusResult",
    "GetOrganizationConformancePackDetailedStatusResult",
    "GetOrganizationCustomRulePolicyResult",
    "GetResourceEvaluationSummaryResult",
    "GetStoredQueryResult",
    "ListAggregateDiscoveredResourcesResult",
    "ListConfigurationRecordersResult",
    "ListConformancePackComplianceScoresResult",
    "ListResourceEvaluationsResult",
    "ListStoredQueriesResult",
    "ListTagsForResourceResult",
    "PutConfigurationAggregatorResult",
    "PutConformancePackResult",
    "PutEvaluationsResult",
    "PutOrganizationConfigRuleResult",
    "PutOrganizationConformancePackResult",
    "PutRemediationExceptionsResult",
    "PutRetentionConfigurationResult",
    "PutServiceLinkedConfigurationRecorderResult",
    "PutStoredQueryResult",
    "RemediationConfigResult",
    "SelectAggregateResourceConfigResult",
    "SelectResourceConfigResult",
    "StartResourceEvaluationResult",
    "associate_resource_types",
    "batch_get_aggregate_resource_config",
    "batch_get_resource_config",
    "delete_aggregation_authorization",
    "delete_config_rule",
    "delete_configuration_aggregator",
    "delete_configuration_recorder",
    "delete_conformance_pack",
    "delete_delivery_channel",
    "delete_evaluation_results",
    "delete_organization_config_rule",
    "delete_organization_conformance_pack",
    "delete_pending_aggregation_request",
    "delete_remediation_configuration",
    "delete_remediation_exceptions",
    "delete_resource_config",
    "delete_retention_configuration",
    "delete_service_linked_configuration_recorder",
    "delete_stored_query",
    "deliver_config_snapshot",
    "describe_aggregate_compliance_by_config_rules",
    "describe_aggregate_compliance_by_conformance_packs",
    "describe_aggregation_authorizations",
    "describe_compliance_by_config_rule",
    "describe_compliance_by_resource",
    "describe_config_rule_evaluation_status",
    "describe_config_rules",
    "describe_configuration_aggregator_sources_status",
    "describe_configuration_aggregators",
    "describe_configuration_recorder_status",
    "describe_configuration_recorders",
    "describe_conformance_pack_compliance",
    "describe_conformance_pack_status",
    "describe_conformance_packs",
    "describe_delivery_channel_status",
    "describe_delivery_channels",
    "describe_organization_config_rule_statuses",
    "describe_organization_config_rules",
    "describe_organization_conformance_pack_statuses",
    "describe_organization_conformance_packs",
    "describe_pending_aggregation_requests",
    "describe_remediation_configurations",
    "describe_remediation_exceptions",
    "describe_remediation_execution_status",
    "describe_retention_configurations",
    "disassociate_resource_types",
    "get_aggregate_compliance_details_by_config_rule",
    "get_aggregate_config_rule_compliance_summary",
    "get_aggregate_conformance_pack_compliance_summary",
    "get_aggregate_discovered_resource_counts",
    "get_aggregate_resource_config",
    "get_compliance_details_by_config_rule",
    "get_compliance_details_by_resource",
    "get_compliance_summary_by_config_rule",
    "get_compliance_summary_by_resource_type",
    "get_conformance_pack_compliance_details",
    "get_conformance_pack_compliance_summary",
    "get_custom_rule_policy",
    "get_discovered_resource_counts",
    "get_organization_config_rule_detailed_status",
    "get_organization_conformance_pack_detailed_status",
    "get_organization_custom_rule_policy",
    "get_resource_config_history",
    "get_resource_evaluation_summary",
    "get_stored_query",
    "list_aggregate_discovered_resources",
    "list_configuration_recorders",
    "list_conformance_pack_compliance_scores",
    "list_discovered_resources",
    "list_resource_evaluations",
    "list_stored_queries",
    "list_tags_for_resource",
    "put_aggregation_authorization",
    "put_config_rule",
    "put_configuration_aggregator",
    "put_configuration_recorder",
    "put_conformance_pack",
    "put_delivery_channel",
    "put_evaluations",
    "put_external_evaluation",
    "put_organization_config_rule",
    "put_organization_conformance_pack",
    "put_remediation_configurations",
    "put_remediation_exceptions",
    "put_resource_config",
    "put_retention_configuration",
    "put_service_linked_configuration_recorder",
    "put_stored_query",
    "select_aggregate_resource_config",
    "select_resource_config",
    "start_config_rules_evaluation",
    "start_configuration_recorder",
    "start_remediation_execution",
    "start_resource_evaluation",
    "stop_configuration_recorder",
    "tag_resource",
    "untag_resource",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ConfigRuleResult(BaseModel):
    """Metadata for an AWS Config rule."""

    model_config = ConfigDict(frozen=True)

    config_rule_name: str
    config_rule_arn: str | None = None
    config_rule_id: str | None = None
    source: dict[str, Any] = {}
    scope: dict[str, Any] | None = None
    compliance_type: str | None = None
    state: str | None = None
    extra: dict[str, Any] = {}


class ConfigurationRecorderResult(BaseModel):
    """Metadata for an AWS Config configuration recorder."""

    model_config = ConfigDict(frozen=True)

    name: str
    role_arn: str = ""
    recording_group: dict[str, Any] | None = None
    status: str | None = None
    extra: dict[str, Any] = {}


class ComplianceResult(BaseModel):
    """Compliance evaluation result for a Config rule or resource."""

    model_config = ConfigDict(frozen=True)

    config_rule_name: str
    resource_type: str | None = None
    resource_id: str | None = None
    compliance_type: str = ""
    annotation: str | None = None
    ordering_timestamp: str | None = None
    extra: dict[str, Any] = {}


class RemediationConfigResult(BaseModel):
    """Remediation configuration for a Config rule."""

    model_config = ConfigDict(frozen=True)

    config_rule_name: str
    target_type: str = ""
    target_id: str = ""
    parameters: dict[str, Any] | None = None
    automatic: bool = False
    retry_attempt_seconds: int | None = None
    maximum_automatic_attempts: int | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Config Rules
# ---------------------------------------------------------------------------


def put_config_rule(
    config_rule_name: str,
    *,
    source: dict[str, Any],
    scope: dict[str, Any] | None = None,
    input_parameters: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create or update an AWS Config rule.

    Args:
        config_rule_name: Name of the Config rule.
        source: Rule source configuration containing Owner,
            SourceIdentifier, and optionally SourceDetails.
        scope: Optional scope defining which resources trigger evaluation.
        input_parameters: Optional JSON string of rule input parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    rule: dict[str, Any] = {
        "ConfigRuleName": config_rule_name,
        "Source": source,
    }
    if scope is not None:
        rule["Scope"] = scope
    if input_parameters is not None:
        rule["InputParameters"] = input_parameters
    try:
        client.put_config_rule(ConfigRule=rule)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to put config rule {config_rule_name!r}") from exc


def describe_config_rules(
    *,
    config_rule_names: list[str] | None = None,
    region_name: str | None = None,
) -> list[ConfigRuleResult]:
    """Describe one or more AWS Config rules.

    Args:
        config_rule_names: Specific rule names to describe.
            ``None`` returns all rules.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConfigRuleResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if config_rule_names:
        kwargs["ConfigRuleNames"] = config_rule_names
    results: list[ConfigRuleResult] = []
    try:
        paginator = client.get_paginator("describe_config_rules")
        for page in paginator.paginate(**kwargs):
            for rule in page.get("ConfigRules", []):
                results.append(
                    ConfigRuleResult(
                        config_rule_name=rule.get("ConfigRuleName", ""),
                        config_rule_arn=rule.get("ConfigRuleArn"),
                        config_rule_id=rule.get("ConfigRuleId"),
                        source=rule.get("Source", {}),
                        scope=rule.get("Scope"),
                        state=rule.get("ConfigRuleState"),
                        extra={
                            k: v
                            for k, v in rule.items()
                            if k
                            not in {
                                "ConfigRuleName",
                                "ConfigRuleArn",
                                "ConfigRuleId",
                                "Source",
                                "Scope",
                                "ConfigRuleState",
                            }
                        },
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_config_rules failed") from exc
    return results


def delete_config_rule(
    config_rule_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an AWS Config rule.

    Args:
        config_rule_name: Name of the Config rule to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        client.delete_config_rule(ConfigRuleName=config_rule_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to delete config rule {config_rule_name!r}") from exc


def start_config_rules_evaluation(
    config_rule_names: list[str],
    *,
    region_name: str | None = None,
) -> None:
    """Start evaluation for one or more AWS Config rules.

    Args:
        config_rule_names: List of rule names to evaluate.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        client.start_config_rules_evaluation(
            ConfigRuleNames=config_rule_names,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start config rules evaluation") from exc


# ---------------------------------------------------------------------------
# Compliance
# ---------------------------------------------------------------------------


def describe_compliance_by_config_rule(
    *,
    config_rule_names: list[str] | None = None,
    compliance_types: list[str] | None = None,
    region_name: str | None = None,
) -> list[ComplianceResult]:
    """Describe compliance status by Config rule.

    Args:
        config_rule_names: Filter by specific rule names.
        compliance_types: Filter by compliance types, e.g.
            ``["COMPLIANT", "NON_COMPLIANT"]``.
        region_name: AWS region override.

    Returns:
        A list of :class:`ComplianceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if config_rule_names:
        kwargs["ConfigRuleNames"] = config_rule_names
    if compliance_types:
        kwargs["ComplianceTypes"] = compliance_types
    results: list[ComplianceResult] = []
    try:
        paginator = client.get_paginator("describe_compliance_by_config_rule")
        for page in paginator.paginate(**kwargs):
            for item in page.get("ComplianceByConfigRules", []):
                compliance = item.get("Compliance", {})
                results.append(
                    ComplianceResult(
                        config_rule_name=item.get("ConfigRuleName", ""),
                        compliance_type=compliance.get("ComplianceType", ""),
                        extra={
                            k: v
                            for k, v in item.items()
                            if k not in {"ConfigRuleName", "Compliance"}
                        },
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_compliance_by_config_rule failed") from exc
    return results


def get_compliance_details_by_config_rule(
    config_rule_name: str,
    *,
    compliance_types: list[str] | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> list[ComplianceResult]:
    """Get detailed compliance results for a specific Config rule.

    Args:
        config_rule_name: Name of the Config rule.
        compliance_types: Filter by compliance types.
        limit: Maximum number of results to return.
        region_name: AWS region override.

    Returns:
        A list of :class:`ComplianceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {
        "ConfigRuleName": config_rule_name,
    }
    if compliance_types:
        kwargs["ComplianceTypes"] = compliance_types
    if limit is not None:
        kwargs["Limit"] = limit
    results: list[ComplianceResult] = []
    try:
        paginator = client.get_paginator("get_compliance_details_by_config_rule")
        for page in paginator.paginate(**kwargs):
            for item in page.get("EvaluationResults", []):
                eri = item.get("EvaluationResultIdentifier", {})
                qf = eri.get("EvaluationResultQualifier", {})
                results.append(
                    ComplianceResult(
                        config_rule_name=qf.get("ConfigRuleName", config_rule_name),
                        resource_type=qf.get("ResourceType"),
                        resource_id=qf.get("ResourceId"),
                        compliance_type=item.get("ComplianceType", ""),
                        annotation=item.get("Annotation"),
                        ordering_timestamp=str(item["OrderingTimestamp"])
                        if "OrderingTimestamp" in item
                        else None,
                        extra={
                            k: v
                            for k, v in item.items()
                            if k
                            not in {
                                "EvaluationResultIdentifier",
                                "ComplianceType",
                                "Annotation",
                                "OrderingTimestamp",
                            }
                        },
                    )
                )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_compliance_details_by_config_rule failed for {config_rule_name!r}",
        ) from exc
    return results


# ---------------------------------------------------------------------------
# Configuration Recorders
# ---------------------------------------------------------------------------


def describe_configuration_recorders(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[ConfigurationRecorderResult]:
    """Describe AWS Config configuration recorders.

    Args:
        names: Specific recorder names. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of :class:`ConfigurationRecorderResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["ConfigurationRecorderNames"] = names
    try:
        resp = client.describe_configuration_recorders(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_configuration_recorders failed") from exc

    results: list[ConfigurationRecorderResult] = []
    for rec in resp.get("ConfigurationRecorders", []):
        # Attempt to get status for this recorder
        status_str: str | None = None
        try:
            status_resp = client.describe_configuration_recorder_status(
                ConfigurationRecorderNames=[rec.get("name", rec.get("Name", ""))],
            )
            statuses = status_resp.get("ConfigurationRecordersStatus", [])
            if statuses:
                status_str = "recording" if statuses[0].get("recording", False) else "stopped"
        except ClientError:
            pass
        results.append(
            ConfigurationRecorderResult(
                name=rec.get("name", rec.get("Name", "")),
                role_arn=rec.get("roleARN", rec.get("RoleARN", "")),
                recording_group=rec.get("recordingGroup", rec.get("RecordingGroup")),
                status=status_str,
                extra={
                    k: v
                    for k, v in rec.items()
                    if k
                    not in {
                        "name",
                        "Name",
                        "roleARN",
                        "RoleARN",
                        "recordingGroup",
                        "RecordingGroup",
                    }
                },
            )
        )
    return results


def put_configuration_recorder(
    name: str,
    *,
    role_arn: str,
    recording_group: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Create or update a configuration recorder.

    Args:
        name: Name of the configuration recorder.
        role_arn: IAM role ARN that AWS Config uses.
        recording_group: Optional recording group configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    recorder: dict[str, Any] = {
        "name": name,
        "roleARN": role_arn,
    }
    if recording_group is not None:
        recorder["recordingGroup"] = recording_group
    try:
        client.put_configuration_recorder(
            ConfigurationRecorder=recorder,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to put configuration recorder {name!r}") from exc


def start_configuration_recorder(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Start recording configurations for an AWS Config recorder.

    Args:
        name: Name of the configuration recorder.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        client.start_configuration_recorder(
            ConfigurationRecorderName=name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to start configuration recorder {name!r}",
        ) from exc


def stop_configuration_recorder(
    name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Stop recording configurations for an AWS Config recorder.

    Args:
        name: Name of the configuration recorder.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        client.stop_configuration_recorder(
            ConfigurationRecorderName=name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to stop configuration recorder {name!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Delivery Channel / Snapshots
# ---------------------------------------------------------------------------


def deliver_config_snapshot(
    delivery_channel_name: str,
    *,
    region_name: str | None = None,
) -> str:
    """Trigger delivery of a configuration snapshot.

    Args:
        delivery_channel_name: Name of the delivery channel.
        region_name: AWS region override.

    Returns:
        The ``configSnapshotId`` of the triggered snapshot.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        resp = client.deliver_config_snapshot(
            deliveryChannelName=delivery_channel_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to deliver config snapshot for {delivery_channel_name!r}",
        ) from exc
    return resp.get("configSnapshotId", "")


# ---------------------------------------------------------------------------
# Remediation
# ---------------------------------------------------------------------------


def put_remediation_configurations(
    *,
    remediation_configs: list[dict[str, Any]],
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Create or update remediation configurations.

    Args:
        remediation_configs: List of remediation configuration dicts, each
            containing at minimum ConfigRuleName, TargetType, and TargetId.
        region_name: AWS region override.

    Returns:
        A list of failed remediation entries (empty on full success).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        resp = client.put_remediation_configurations(
            RemediationConfigurations=remediation_configs,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put remediation configurations") from exc
    return resp.get("FailedBatches", [])


def describe_remediation_configurations(
    config_rule_names: list[str],
    *,
    region_name: str | None = None,
) -> list[RemediationConfigResult]:
    """Describe remediation configurations for Config rules.

    Args:
        config_rule_names: List of Config rule names.
        region_name: AWS region override.

    Returns:
        A list of :class:`RemediationConfigResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        resp = client.describe_remediation_configurations(
            ConfigRuleNames=config_rule_names,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_remediation_configurations failed") from exc
    results: list[RemediationConfigResult] = []
    for item in resp.get("RemediationConfigurations", []):
        results.append(
            RemediationConfigResult(
                config_rule_name=item.get("ConfigRuleName", ""),
                target_type=item.get("TargetType", ""),
                target_id=item.get("TargetId", ""),
                parameters=item.get("Parameters"),
                automatic=item.get("Automatic", False),
                retry_attempt_seconds=item.get("RetryAttemptSeconds"),
                maximum_automatic_attempts=item.get("MaximumAutomaticAttempts"),
                extra={
                    k: v
                    for k, v in item.items()
                    if k
                    not in {
                        "ConfigRuleName",
                        "TargetType",
                        "TargetId",
                        "Parameters",
                        "Automatic",
                        "RetryAttemptSeconds",
                        "MaximumAutomaticAttempts",
                    }
                },
            )
        )
    return results


def start_remediation_execution(
    config_rule_name: str,
    *,
    resource_keys: list[dict[str, str]],
    region_name: str | None = None,
) -> dict[str, Any]:
    """Start remediation execution for specific resources.

    Args:
        config_rule_name: Name of the Config rule.
        resource_keys: List of dicts each with ``resourceType`` and
            ``resourceId``.
        region_name: AWS region override.

    Returns:
        A dict containing ``FailureMessage`` and
        ``FailedItems`` if any resources failed to remediate.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        resp = client.start_remediation_execution(
            ConfigRuleName=config_rule_name,
            ResourceKeys=resource_keys,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to start remediation execution for {config_rule_name!r}",
        ) from exc
    return {
        "FailureMessage": resp.get("FailureMessage", ""),
        "FailedItems": resp.get("FailedItems", []),
    }


# ---------------------------------------------------------------------------
# Resource Discovery
# ---------------------------------------------------------------------------


def list_discovered_resources(
    resource_type: str,
    *,
    resource_ids: list[str] | None = None,
    resource_name: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """List resources discovered by AWS Config.

    Args:
        resource_type: AWS resource type, e.g.
            ``"AWS::EC2::Instance"``.
        resource_ids: Filter by specific resource IDs.
        resource_name: Filter by resource name.
        limit: Maximum number of results.
        region_name: AWS region override.

    Returns:
        A list of resource identifier dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {
        "resourceType": resource_type,
    }
    if resource_ids:
        kwargs["resourceIds"] = resource_ids
    if resource_name:
        kwargs["resourceName"] = resource_name
    if limit is not None:
        kwargs["limit"] = limit
    results: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("list_discovered_resources")
        for page in paginator.paginate(**kwargs):
            for item in page.get("resourceIdentifiers", []):
                results.append(item)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"list_discovered_resources failed for {resource_type!r}",
        ) from exc
    return results


def get_resource_config_history(
    resource_type: str,
    resource_id: str,
    *,
    limit: int | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Get configuration history for a specific resource.

    Args:
        resource_type: AWS resource type, e.g.
            ``"AWS::EC2::Instance"``.
        resource_id: The resource identifier.
        limit: Maximum number of history items.
        region_name: AWS region override.

    Returns:
        A list of configuration item dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {
        "resourceType": resource_type,
        "resourceId": resource_id,
    }
    if limit is not None:
        kwargs["limit"] = limit
    results: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("get_resource_config_history")
        for page in paginator.paginate(**kwargs):
            for item in page.get("configurationItems", []):
                results.append(item)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"get_resource_config_history failed for {resource_type!r}/{resource_id!r}",
        ) from exc
    return results


# ---------------------------------------------------------------------------
# Aggregators
# ---------------------------------------------------------------------------


def describe_configuration_aggregators(
    *,
    names: list[str] | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Describe AWS Config configuration aggregators.

    Args:
        names: Specific aggregator names. ``None`` returns all.
        region_name: AWS region override.

    Returns:
        A list of aggregator configuration dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if names:
        kwargs["ConfigurationAggregatorNames"] = names
    results: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("describe_configuration_aggregators")
        for page in paginator.paginate(**kwargs):
            for item in page.get("ConfigurationAggregators", []):
                results.append(item)
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_configuration_aggregators failed") from exc
    return results


def put_aggregation_authorization(
    authorized_account_id: str,
    authorized_region: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Authorize an account and region for Config aggregation.

    Args:
        authorized_account_id: AWS account ID to authorize.
        authorized_region: AWS region to authorize.
        region_name: AWS region override.

    Returns:
        The aggregation authorization details dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    try:
        resp = client.put_aggregation_authorization(
            AuthorizedAccountId=authorized_account_id,
            AuthorizedAwsRegion=authorized_region,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"Failed to put aggregation authorization for"
            f" {authorized_account_id!r} in {authorized_region!r}",
        ) from exc
    return resp.get("AggregationAuthorization", {})


class AssociateResourceTypesResult(BaseModel):
    """Result of associate_resource_types."""

    model_config = ConfigDict(frozen=True)

    configuration_recorder: dict[str, Any] | None = None


class BatchGetAggregateResourceConfigResult(BaseModel):
    """Result of batch_get_aggregate_resource_config."""

    model_config = ConfigDict(frozen=True)

    base_configuration_items: list[dict[str, Any]] | None = None
    unprocessed_resource_identifiers: list[dict[str, Any]] | None = None


class BatchGetResourceConfigResult(BaseModel):
    """Result of batch_get_resource_config."""

    model_config = ConfigDict(frozen=True)

    base_configuration_items: list[dict[str, Any]] | None = None
    unprocessed_resource_keys: list[dict[str, Any]] | None = None


class DeleteRemediationExceptionsResult(BaseModel):
    """Result of delete_remediation_exceptions."""

    model_config = ConfigDict(frozen=True)

    failed_batches: list[dict[str, Any]] | None = None


class DeleteServiceLinkedConfigurationRecorderResult(BaseModel):
    """Result of delete_service_linked_configuration_recorder."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    name: str | None = None


class DescribeAggregateComplianceByConfigRulesResult(BaseModel):
    """Result of describe_aggregate_compliance_by_config_rules."""

    model_config = ConfigDict(frozen=True)

    aggregate_compliance_by_config_rules: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeAggregateComplianceByConformancePacksResult(BaseModel):
    """Result of describe_aggregate_compliance_by_conformance_packs."""

    model_config = ConfigDict(frozen=True)

    aggregate_compliance_by_conformance_packs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeAggregationAuthorizationsResult(BaseModel):
    """Result of describe_aggregation_authorizations."""

    model_config = ConfigDict(frozen=True)

    aggregation_authorizations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeComplianceByResourceResult(BaseModel):
    """Result of describe_compliance_by_resource."""

    model_config = ConfigDict(frozen=True)

    compliance_by_resources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeConfigRuleEvaluationStatusResult(BaseModel):
    """Result of describe_config_rule_evaluation_status."""

    model_config = ConfigDict(frozen=True)

    config_rules_evaluation_status: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeConfigurationAggregatorSourcesStatusResult(BaseModel):
    """Result of describe_configuration_aggregator_sources_status."""

    model_config = ConfigDict(frozen=True)

    aggregated_source_status_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeConfigurationRecorderStatusResult(BaseModel):
    """Result of describe_configuration_recorder_status."""

    model_config = ConfigDict(frozen=True)

    configuration_recorders_status: list[dict[str, Any]] | None = None


class DescribeConformancePackComplianceResult(BaseModel):
    """Result of describe_conformance_pack_compliance."""

    model_config = ConfigDict(frozen=True)

    conformance_pack_name: str | None = None
    conformance_pack_rule_compliance_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeConformancePackStatusResult(BaseModel):
    """Result of describe_conformance_pack_status."""

    model_config = ConfigDict(frozen=True)

    conformance_pack_status_details: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeConformancePacksResult(BaseModel):
    """Result of describe_conformance_packs."""

    model_config = ConfigDict(frozen=True)

    conformance_pack_details: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeDeliveryChannelStatusResult(BaseModel):
    """Result of describe_delivery_channel_status."""

    model_config = ConfigDict(frozen=True)

    delivery_channels_status: list[dict[str, Any]] | None = None


class DescribeDeliveryChannelsResult(BaseModel):
    """Result of describe_delivery_channels."""

    model_config = ConfigDict(frozen=True)

    delivery_channels: list[dict[str, Any]] | None = None


class DescribeOrganizationConfigRuleStatusesResult(BaseModel):
    """Result of describe_organization_config_rule_statuses."""

    model_config = ConfigDict(frozen=True)

    organization_config_rule_statuses: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeOrganizationConfigRulesResult(BaseModel):
    """Result of describe_organization_config_rules."""

    model_config = ConfigDict(frozen=True)

    organization_config_rules: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeOrganizationConformancePackStatusesResult(BaseModel):
    """Result of describe_organization_conformance_pack_statuses."""

    model_config = ConfigDict(frozen=True)

    organization_conformance_pack_statuses: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeOrganizationConformancePacksResult(BaseModel):
    """Result of describe_organization_conformance_packs."""

    model_config = ConfigDict(frozen=True)

    organization_conformance_packs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribePendingAggregationRequestsResult(BaseModel):
    """Result of describe_pending_aggregation_requests."""

    model_config = ConfigDict(frozen=True)

    pending_aggregation_requests: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeRemediationExceptionsResult(BaseModel):
    """Result of describe_remediation_exceptions."""

    model_config = ConfigDict(frozen=True)

    remediation_exceptions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeRemediationExecutionStatusResult(BaseModel):
    """Result of describe_remediation_execution_status."""

    model_config = ConfigDict(frozen=True)

    remediation_execution_statuses: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeRetentionConfigurationsResult(BaseModel):
    """Result of describe_retention_configurations."""

    model_config = ConfigDict(frozen=True)

    retention_configurations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DisassociateResourceTypesResult(BaseModel):
    """Result of disassociate_resource_types."""

    model_config = ConfigDict(frozen=True)

    configuration_recorder: dict[str, Any] | None = None


class GetAggregateComplianceDetailsByConfigRuleResult(BaseModel):
    """Result of get_aggregate_compliance_details_by_config_rule."""

    model_config = ConfigDict(frozen=True)

    aggregate_evaluation_results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetAggregateConfigRuleComplianceSummaryResult(BaseModel):
    """Result of get_aggregate_config_rule_compliance_summary."""

    model_config = ConfigDict(frozen=True)

    group_by_key: str | None = None
    aggregate_compliance_counts: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetAggregateConformancePackComplianceSummaryResult(BaseModel):
    """Result of get_aggregate_conformance_pack_compliance_summary."""

    model_config = ConfigDict(frozen=True)

    aggregate_conformance_pack_compliance_summaries: list[dict[str, Any]] | None = None
    group_by_key: str | None = None
    next_token: str | None = None


class GetAggregateDiscoveredResourceCountsResult(BaseModel):
    """Result of get_aggregate_discovered_resource_counts."""

    model_config = ConfigDict(frozen=True)

    total_discovered_resources: int | None = None
    group_by_key: str | None = None
    grouped_resource_counts: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetAggregateResourceConfigResult(BaseModel):
    """Result of get_aggregate_resource_config."""

    model_config = ConfigDict(frozen=True)

    configuration_item: dict[str, Any] | None = None


class GetComplianceDetailsByResourceResult(BaseModel):
    """Result of get_compliance_details_by_resource."""

    model_config = ConfigDict(frozen=True)

    evaluation_results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetComplianceSummaryByConfigRuleResult(BaseModel):
    """Result of get_compliance_summary_by_config_rule."""

    model_config = ConfigDict(frozen=True)

    compliance_summary: dict[str, Any] | None = None


class GetComplianceSummaryByResourceTypeResult(BaseModel):
    """Result of get_compliance_summary_by_resource_type."""

    model_config = ConfigDict(frozen=True)

    compliance_summaries_by_resource_type: list[dict[str, Any]] | None = None


class GetConformancePackComplianceDetailsResult(BaseModel):
    """Result of get_conformance_pack_compliance_details."""

    model_config = ConfigDict(frozen=True)

    conformance_pack_name: str | None = None
    conformance_pack_rule_evaluation_results: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetConformancePackComplianceSummaryResult(BaseModel):
    """Result of get_conformance_pack_compliance_summary."""

    model_config = ConfigDict(frozen=True)

    conformance_pack_compliance_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetCustomRulePolicyResult(BaseModel):
    """Result of get_custom_rule_policy."""

    model_config = ConfigDict(frozen=True)

    policy_text: str | None = None


class GetDiscoveredResourceCountsResult(BaseModel):
    """Result of get_discovered_resource_counts."""

    model_config = ConfigDict(frozen=True)

    total_discovered_resources: int | None = None
    resource_counts: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetOrganizationConfigRuleDetailedStatusResult(BaseModel):
    """Result of get_organization_config_rule_detailed_status."""

    model_config = ConfigDict(frozen=True)

    organization_config_rule_detailed_status: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetOrganizationConformancePackDetailedStatusResult(BaseModel):
    """Result of get_organization_conformance_pack_detailed_status."""

    model_config = ConfigDict(frozen=True)

    organization_conformance_pack_detailed_statuses: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetOrganizationCustomRulePolicyResult(BaseModel):
    """Result of get_organization_custom_rule_policy."""

    model_config = ConfigDict(frozen=True)

    policy_text: str | None = None


class GetResourceEvaluationSummaryResult(BaseModel):
    """Result of get_resource_evaluation_summary."""

    model_config = ConfigDict(frozen=True)

    resource_evaluation_id: str | None = None
    evaluation_mode: str | None = None
    evaluation_status: dict[str, Any] | None = None
    evaluation_start_timestamp: str | None = None
    compliance: str | None = None
    evaluation_context: dict[str, Any] | None = None
    resource_details: dict[str, Any] | None = None


class GetStoredQueryResult(BaseModel):
    """Result of get_stored_query."""

    model_config = ConfigDict(frozen=True)

    stored_query: dict[str, Any] | None = None


class ListAggregateDiscoveredResourcesResult(BaseModel):
    """Result of list_aggregate_discovered_resources."""

    model_config = ConfigDict(frozen=True)

    resource_identifiers: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListConfigurationRecordersResult(BaseModel):
    """Result of list_configuration_recorders."""

    model_config = ConfigDict(frozen=True)

    configuration_recorder_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListConformancePackComplianceScoresResult(BaseModel):
    """Result of list_conformance_pack_compliance_scores."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    conformance_pack_compliance_scores: list[dict[str, Any]] | None = None


class ListResourceEvaluationsResult(BaseModel):
    """Result of list_resource_evaluations."""

    model_config = ConfigDict(frozen=True)

    resource_evaluations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStoredQueriesResult(BaseModel):
    """Result of list_stored_queries."""

    model_config = ConfigDict(frozen=True)

    stored_query_metadata: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutConfigurationAggregatorResult(BaseModel):
    """Result of put_configuration_aggregator."""

    model_config = ConfigDict(frozen=True)

    configuration_aggregator: dict[str, Any] | None = None


class PutConformancePackResult(BaseModel):
    """Result of put_conformance_pack."""

    model_config = ConfigDict(frozen=True)

    conformance_pack_arn: str | None = None


class PutEvaluationsResult(BaseModel):
    """Result of put_evaluations."""

    model_config = ConfigDict(frozen=True)

    failed_evaluations: list[dict[str, Any]] | None = None


class PutOrganizationConfigRuleResult(BaseModel):
    """Result of put_organization_config_rule."""

    model_config = ConfigDict(frozen=True)

    organization_config_rule_arn: str | None = None


class PutOrganizationConformancePackResult(BaseModel):
    """Result of put_organization_conformance_pack."""

    model_config = ConfigDict(frozen=True)

    organization_conformance_pack_arn: str | None = None


class PutRemediationExceptionsResult(BaseModel):
    """Result of put_remediation_exceptions."""

    model_config = ConfigDict(frozen=True)

    failed_batches: list[dict[str, Any]] | None = None


class PutRetentionConfigurationResult(BaseModel):
    """Result of put_retention_configuration."""

    model_config = ConfigDict(frozen=True)

    retention_configuration: dict[str, Any] | None = None


class PutServiceLinkedConfigurationRecorderResult(BaseModel):
    """Result of put_service_linked_configuration_recorder."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    name: str | None = None


class PutStoredQueryResult(BaseModel):
    """Result of put_stored_query."""

    model_config = ConfigDict(frozen=True)

    query_arn: str | None = None


class SelectAggregateResourceConfigResult(BaseModel):
    """Result of select_aggregate_resource_config."""

    model_config = ConfigDict(frozen=True)

    results: list[str] | None = None
    query_info: dict[str, Any] | None = None
    next_token: str | None = None


class SelectResourceConfigResult(BaseModel):
    """Result of select_resource_config."""

    model_config = ConfigDict(frozen=True)

    results: list[str] | None = None
    query_info: dict[str, Any] | None = None
    next_token: str | None = None


class StartResourceEvaluationResult(BaseModel):
    """Result of start_resource_evaluation."""

    model_config = ConfigDict(frozen=True)

    resource_evaluation_id: str | None = None


def associate_resource_types(
    configuration_recorder_arn: str,
    resource_types: list[str],
    region_name: str | None = None,
) -> AssociateResourceTypesResult:
    """Associate resource types.

    Args:
        configuration_recorder_arn: Configuration recorder arn.
        resource_types: Resource types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationRecorderArn"] = configuration_recorder_arn
    kwargs["ResourceTypes"] = resource_types
    try:
        resp = client.associate_resource_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate resource types") from exc
    return AssociateResourceTypesResult(
        configuration_recorder=resp.get("ConfigurationRecorder"),
    )


def batch_get_aggregate_resource_config(
    configuration_aggregator_name: str,
    resource_identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetAggregateResourceConfigResult:
    """Batch get aggregate resource config.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        resource_identifiers: Resource identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    kwargs["ResourceIdentifiers"] = resource_identifiers
    try:
        resp = client.batch_get_aggregate_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get aggregate resource config") from exc
    return BatchGetAggregateResourceConfigResult(
        base_configuration_items=resp.get("BaseConfigurationItems"),
        unprocessed_resource_identifiers=resp.get("UnprocessedResourceIdentifiers"),
    )


def batch_get_resource_config(
    resource_keys: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetResourceConfigResult:
    """Batch get resource config.

    Args:
        resource_keys: Resource keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceKeys"] = resource_keys
    try:
        resp = client.batch_get_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get resource config") from exc
    return BatchGetResourceConfigResult(
        base_configuration_items=resp.get("baseConfigurationItems"),
        unprocessed_resource_keys=resp.get("unprocessedResourceKeys"),
    )


def delete_aggregation_authorization(
    authorized_account_id: str,
    authorized_aws_region: str,
    region_name: str | None = None,
) -> None:
    """Delete aggregation authorization.

    Args:
        authorized_account_id: Authorized account id.
        authorized_aws_region: Authorized aws region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthorizedAccountId"] = authorized_account_id
    kwargs["AuthorizedAwsRegion"] = authorized_aws_region
    try:
        client.delete_aggregation_authorization(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete aggregation authorization") from exc
    return None


def delete_configuration_aggregator(
    configuration_aggregator_name: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration aggregator.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    try:
        client.delete_configuration_aggregator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration aggregator") from exc
    return None


def delete_configuration_recorder(
    configuration_recorder_name: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration recorder.

    Args:
        configuration_recorder_name: Configuration recorder name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationRecorderName"] = configuration_recorder_name
    try:
        client.delete_configuration_recorder(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration recorder") from exc
    return None


def delete_conformance_pack(
    conformance_pack_name: str,
    region_name: str | None = None,
) -> None:
    """Delete conformance pack.

    Args:
        conformance_pack_name: Conformance pack name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConformancePackName"] = conformance_pack_name
    try:
        client.delete_conformance_pack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete conformance pack") from exc
    return None


def delete_delivery_channel(
    delivery_channel_name: str,
    region_name: str | None = None,
) -> None:
    """Delete delivery channel.

    Args:
        delivery_channel_name: Delivery channel name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryChannelName"] = delivery_channel_name
    try:
        client.delete_delivery_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete delivery channel") from exc
    return None


def delete_evaluation_results(
    config_rule_name: str,
    region_name: str | None = None,
) -> None:
    """Delete evaluation results.

    Args:
        config_rule_name: Config rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    try:
        client.delete_evaluation_results(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete evaluation results") from exc
    return None


def delete_organization_config_rule(
    organization_config_rule_name: str,
    region_name: str | None = None,
) -> None:
    """Delete organization config rule.

    Args:
        organization_config_rule_name: Organization config rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConfigRuleName"] = organization_config_rule_name
    try:
        client.delete_organization_config_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete organization config rule") from exc
    return None


def delete_organization_conformance_pack(
    organization_conformance_pack_name: str,
    region_name: str | None = None,
) -> None:
    """Delete organization conformance pack.

    Args:
        organization_conformance_pack_name: Organization conformance pack name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConformancePackName"] = organization_conformance_pack_name
    try:
        client.delete_organization_conformance_pack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete organization conformance pack") from exc
    return None


def delete_pending_aggregation_request(
    requester_account_id: str,
    requester_aws_region: str,
    region_name: str | None = None,
) -> None:
    """Delete pending aggregation request.

    Args:
        requester_account_id: Requester account id.
        requester_aws_region: Requester aws region.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RequesterAccountId"] = requester_account_id
    kwargs["RequesterAwsRegion"] = requester_aws_region
    try:
        client.delete_pending_aggregation_request(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete pending aggregation request") from exc
    return None


def delete_remediation_configuration(
    config_rule_name: str,
    *,
    resource_type: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete remediation configuration.

    Args:
        config_rule_name: Config rule name.
        resource_type: Resource type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    try:
        client.delete_remediation_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete remediation configuration") from exc
    return None


def delete_remediation_exceptions(
    config_rule_name: str,
    resource_keys: list[dict[str, Any]],
    region_name: str | None = None,
) -> DeleteRemediationExceptionsResult:
    """Delete remediation exceptions.

    Args:
        config_rule_name: Config rule name.
        resource_keys: Resource keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    kwargs["ResourceKeys"] = resource_keys
    try:
        resp = client.delete_remediation_exceptions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete remediation exceptions") from exc
    return DeleteRemediationExceptionsResult(
        failed_batches=resp.get("FailedBatches"),
    )


def delete_resource_config(
    resource_type: str,
    resource_id: str,
    region_name: str | None = None,
) -> None:
    """Delete resource config.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["ResourceId"] = resource_id
    try:
        client.delete_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource config") from exc
    return None


def delete_retention_configuration(
    retention_configuration_name: str,
    region_name: str | None = None,
) -> None:
    """Delete retention configuration.

    Args:
        retention_configuration_name: Retention configuration name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RetentionConfigurationName"] = retention_configuration_name
    try:
        client.delete_retention_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete retention configuration") from exc
    return None


def delete_service_linked_configuration_recorder(
    service_principal: str,
    region_name: str | None = None,
) -> DeleteServiceLinkedConfigurationRecorderResult:
    """Delete service linked configuration recorder.

    Args:
        service_principal: Service principal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServicePrincipal"] = service_principal
    try:
        resp = client.delete_service_linked_configuration_recorder(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete service linked configuration recorder") from exc
    return DeleteServiceLinkedConfigurationRecorderResult(
        arn=resp.get("Arn"),
        name=resp.get("Name"),
    )


def delete_stored_query(
    query_name: str,
    region_name: str | None = None,
) -> None:
    """Delete stored query.

    Args:
        query_name: Query name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryName"] = query_name
    try:
        client.delete_stored_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete stored query") from exc
    return None


def describe_aggregate_compliance_by_config_rules(
    configuration_aggregator_name: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAggregateComplianceByConfigRulesResult:
    """Describe aggregate compliance by config rules.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_aggregate_compliance_by_config_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to describe aggregate compliance by config rules"
        ) from exc
    return DescribeAggregateComplianceByConfigRulesResult(
        aggregate_compliance_by_config_rules=resp.get("AggregateComplianceByConfigRules"),
        next_token=resp.get("NextToken"),
    )


def describe_aggregate_compliance_by_conformance_packs(
    configuration_aggregator_name: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAggregateComplianceByConformancePacksResult:
    """Describe aggregate compliance by conformance packs.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_aggregate_compliance_by_conformance_packs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to describe aggregate compliance by conformance packs"
        ) from exc
    return DescribeAggregateComplianceByConformancePacksResult(
        aggregate_compliance_by_conformance_packs=resp.get("AggregateComplianceByConformancePacks"),
        next_token=resp.get("NextToken"),
    )


def describe_aggregation_authorizations(
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeAggregationAuthorizationsResult:
    """Describe aggregation authorizations.

    Args:
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_aggregation_authorizations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe aggregation authorizations") from exc
    return DescribeAggregationAuthorizationsResult(
        aggregation_authorizations=resp.get("AggregationAuthorizations"),
        next_token=resp.get("NextToken"),
    )


def describe_compliance_by_resource(
    *,
    resource_type: str | None = None,
    resource_id: str | None = None,
    compliance_types: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeComplianceByResourceResult:
    """Describe compliance by resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        compliance_types: Compliance types.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    if resource_id is not None:
        kwargs["ResourceId"] = resource_id
    if compliance_types is not None:
        kwargs["ComplianceTypes"] = compliance_types
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_compliance_by_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe compliance by resource") from exc
    return DescribeComplianceByResourceResult(
        compliance_by_resources=resp.get("ComplianceByResources"),
        next_token=resp.get("NextToken"),
    )


def describe_config_rule_evaluation_status(
    *,
    config_rule_names: list[str] | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> DescribeConfigRuleEvaluationStatusResult:
    """Describe config rule evaluation status.

    Args:
        config_rule_names: Config rule names.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if config_rule_names is not None:
        kwargs["ConfigRuleNames"] = config_rule_names
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.describe_config_rule_evaluation_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe config rule evaluation status") from exc
    return DescribeConfigRuleEvaluationStatusResult(
        config_rules_evaluation_status=resp.get("ConfigRulesEvaluationStatus"),
        next_token=resp.get("NextToken"),
    )


def describe_configuration_aggregator_sources_status(
    configuration_aggregator_name: str,
    *,
    update_status: list[str] | None = None,
    next_token: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> DescribeConfigurationAggregatorSourcesStatusResult:
    """Describe configuration aggregator sources status.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        update_status: Update status.
        next_token: Next token.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if update_status is not None:
        kwargs["UpdateStatus"] = update_status
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.describe_configuration_aggregator_sources_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to describe configuration aggregator sources status"
        ) from exc
    return DescribeConfigurationAggregatorSourcesStatusResult(
        aggregated_source_status_list=resp.get("AggregatedSourceStatusList"),
        next_token=resp.get("NextToken"),
    )


def describe_configuration_recorder_status(
    *,
    configuration_recorder_names: list[str] | None = None,
    service_principal: str | None = None,
    arn: str | None = None,
    region_name: str | None = None,
) -> DescribeConfigurationRecorderStatusResult:
    """Describe configuration recorder status.

    Args:
        configuration_recorder_names: Configuration recorder names.
        service_principal: Service principal.
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if configuration_recorder_names is not None:
        kwargs["ConfigurationRecorderNames"] = configuration_recorder_names
    if service_principal is not None:
        kwargs["ServicePrincipal"] = service_principal
    if arn is not None:
        kwargs["Arn"] = arn
    try:
        resp = client.describe_configuration_recorder_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe configuration recorder status") from exc
    return DescribeConfigurationRecorderStatusResult(
        configuration_recorders_status=resp.get("ConfigurationRecordersStatus"),
    )


def describe_conformance_pack_compliance(
    conformance_pack_name: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeConformancePackComplianceResult:
    """Describe conformance pack compliance.

    Args:
        conformance_pack_name: Conformance pack name.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConformancePackName"] = conformance_pack_name
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_conformance_pack_compliance(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe conformance pack compliance") from exc
    return DescribeConformancePackComplianceResult(
        conformance_pack_name=resp.get("ConformancePackName"),
        conformance_pack_rule_compliance_list=resp.get("ConformancePackRuleComplianceList"),
        next_token=resp.get("NextToken"),
    )


def describe_conformance_pack_status(
    *,
    conformance_pack_names: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeConformancePackStatusResult:
    """Describe conformance pack status.

    Args:
        conformance_pack_names: Conformance pack names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if conformance_pack_names is not None:
        kwargs["ConformancePackNames"] = conformance_pack_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_conformance_pack_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe conformance pack status") from exc
    return DescribeConformancePackStatusResult(
        conformance_pack_status_details=resp.get("ConformancePackStatusDetails"),
        next_token=resp.get("NextToken"),
    )


def describe_conformance_packs(
    *,
    conformance_pack_names: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeConformancePacksResult:
    """Describe conformance packs.

    Args:
        conformance_pack_names: Conformance pack names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if conformance_pack_names is not None:
        kwargs["ConformancePackNames"] = conformance_pack_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_conformance_packs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe conformance packs") from exc
    return DescribeConformancePacksResult(
        conformance_pack_details=resp.get("ConformancePackDetails"),
        next_token=resp.get("NextToken"),
    )


def describe_delivery_channel_status(
    *,
    delivery_channel_names: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeDeliveryChannelStatusResult:
    """Describe delivery channel status.

    Args:
        delivery_channel_names: Delivery channel names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if delivery_channel_names is not None:
        kwargs["DeliveryChannelNames"] = delivery_channel_names
    try:
        resp = client.describe_delivery_channel_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe delivery channel status") from exc
    return DescribeDeliveryChannelStatusResult(
        delivery_channels_status=resp.get("DeliveryChannelsStatus"),
    )


def describe_delivery_channels(
    *,
    delivery_channel_names: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeDeliveryChannelsResult:
    """Describe delivery channels.

    Args:
        delivery_channel_names: Delivery channel names.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if delivery_channel_names is not None:
        kwargs["DeliveryChannelNames"] = delivery_channel_names
    try:
        resp = client.describe_delivery_channels(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe delivery channels") from exc
    return DescribeDeliveryChannelsResult(
        delivery_channels=resp.get("DeliveryChannels"),
    )


def describe_organization_config_rule_statuses(
    *,
    organization_config_rule_names: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeOrganizationConfigRuleStatusesResult:
    """Describe organization config rule statuses.

    Args:
        organization_config_rule_names: Organization config rule names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if organization_config_rule_names is not None:
        kwargs["OrganizationConfigRuleNames"] = organization_config_rule_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_organization_config_rule_statuses(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe organization config rule statuses") from exc
    return DescribeOrganizationConfigRuleStatusesResult(
        organization_config_rule_statuses=resp.get("OrganizationConfigRuleStatuses"),
        next_token=resp.get("NextToken"),
    )


def describe_organization_config_rules(
    *,
    organization_config_rule_names: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeOrganizationConfigRulesResult:
    """Describe organization config rules.

    Args:
        organization_config_rule_names: Organization config rule names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if organization_config_rule_names is not None:
        kwargs["OrganizationConfigRuleNames"] = organization_config_rule_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_organization_config_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe organization config rules") from exc
    return DescribeOrganizationConfigRulesResult(
        organization_config_rules=resp.get("OrganizationConfigRules"),
        next_token=resp.get("NextToken"),
    )


def describe_organization_conformance_pack_statuses(
    *,
    organization_conformance_pack_names: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeOrganizationConformancePackStatusesResult:
    """Describe organization conformance pack statuses.

    Args:
        organization_conformance_pack_names: Organization conformance pack names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if organization_conformance_pack_names is not None:
        kwargs["OrganizationConformancePackNames"] = organization_conformance_pack_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_organization_conformance_pack_statuses(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to describe organization conformance pack statuses"
        ) from exc
    return DescribeOrganizationConformancePackStatusesResult(
        organization_conformance_pack_statuses=resp.get("OrganizationConformancePackStatuses"),
        next_token=resp.get("NextToken"),
    )


def describe_organization_conformance_packs(
    *,
    organization_conformance_pack_names: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeOrganizationConformancePacksResult:
    """Describe organization conformance packs.

    Args:
        organization_conformance_pack_names: Organization conformance pack names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if organization_conformance_pack_names is not None:
        kwargs["OrganizationConformancePackNames"] = organization_conformance_pack_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_organization_conformance_packs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe organization conformance packs") from exc
    return DescribeOrganizationConformancePacksResult(
        organization_conformance_packs=resp.get("OrganizationConformancePacks"),
        next_token=resp.get("NextToken"),
    )


def describe_pending_aggregation_requests(
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribePendingAggregationRequestsResult:
    """Describe pending aggregation requests.

    Args:
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_pending_aggregation_requests(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe pending aggregation requests") from exc
    return DescribePendingAggregationRequestsResult(
        pending_aggregation_requests=resp.get("PendingAggregationRequests"),
        next_token=resp.get("NextToken"),
    )


def describe_remediation_exceptions(
    config_rule_name: str,
    *,
    resource_keys: list[dict[str, Any]] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeRemediationExceptionsResult:
    """Describe remediation exceptions.

    Args:
        config_rule_name: Config rule name.
        resource_keys: Resource keys.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    if resource_keys is not None:
        kwargs["ResourceKeys"] = resource_keys
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_remediation_exceptions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe remediation exceptions") from exc
    return DescribeRemediationExceptionsResult(
        remediation_exceptions=resp.get("RemediationExceptions"),
        next_token=resp.get("NextToken"),
    )


def describe_remediation_execution_status(
    config_rule_name: str,
    *,
    resource_keys: list[dict[str, Any]] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeRemediationExecutionStatusResult:
    """Describe remediation execution status.

    Args:
        config_rule_name: Config rule name.
        resource_keys: Resource keys.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    if resource_keys is not None:
        kwargs["ResourceKeys"] = resource_keys
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_remediation_execution_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe remediation execution status") from exc
    return DescribeRemediationExecutionStatusResult(
        remediation_execution_statuses=resp.get("RemediationExecutionStatuses"),
        next_token=resp.get("NextToken"),
    )


def describe_retention_configurations(
    *,
    retention_configuration_names: list[str] | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> DescribeRetentionConfigurationsResult:
    """Describe retention configurations.

    Args:
        retention_configuration_names: Retention configuration names.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if retention_configuration_names is not None:
        kwargs["RetentionConfigurationNames"] = retention_configuration_names
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.describe_retention_configurations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe retention configurations") from exc
    return DescribeRetentionConfigurationsResult(
        retention_configurations=resp.get("RetentionConfigurations"),
        next_token=resp.get("NextToken"),
    )


def disassociate_resource_types(
    configuration_recorder_arn: str,
    resource_types: list[str],
    region_name: str | None = None,
) -> DisassociateResourceTypesResult:
    """Disassociate resource types.

    Args:
        configuration_recorder_arn: Configuration recorder arn.
        resource_types: Resource types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationRecorderArn"] = configuration_recorder_arn
    kwargs["ResourceTypes"] = resource_types
    try:
        resp = client.disassociate_resource_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate resource types") from exc
    return DisassociateResourceTypesResult(
        configuration_recorder=resp.get("ConfigurationRecorder"),
    )


def get_aggregate_compliance_details_by_config_rule(
    configuration_aggregator_name: str,
    config_rule_name: str,
    account_id: str,
    aws_region: str,
    *,
    compliance_type: str | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetAggregateComplianceDetailsByConfigRuleResult:
    """Get aggregate compliance details by config rule.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        config_rule_name: Config rule name.
        account_id: Account id.
        aws_region: Aws region.
        compliance_type: Compliance type.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    kwargs["ConfigRuleName"] = config_rule_name
    kwargs["AccountId"] = account_id
    kwargs["AwsRegion"] = aws_region
    if compliance_type is not None:
        kwargs["ComplianceType"] = compliance_type
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_aggregate_compliance_details_by_config_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to get aggregate compliance details by config rule"
        ) from exc
    return GetAggregateComplianceDetailsByConfigRuleResult(
        aggregate_evaluation_results=resp.get("AggregateEvaluationResults"),
        next_token=resp.get("NextToken"),
    )


def get_aggregate_config_rule_compliance_summary(
    configuration_aggregator_name: str,
    *,
    filters: dict[str, Any] | None = None,
    group_by_key: str | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetAggregateConfigRuleComplianceSummaryResult:
    """Get aggregate config rule compliance summary.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        filters: Filters.
        group_by_key: Group by key.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if filters is not None:
        kwargs["Filters"] = filters
    if group_by_key is not None:
        kwargs["GroupByKey"] = group_by_key
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_aggregate_config_rule_compliance_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get aggregate config rule compliance summary") from exc
    return GetAggregateConfigRuleComplianceSummaryResult(
        group_by_key=resp.get("GroupByKey"),
        aggregate_compliance_counts=resp.get("AggregateComplianceCounts"),
        next_token=resp.get("NextToken"),
    )


def get_aggregate_conformance_pack_compliance_summary(
    configuration_aggregator_name: str,
    *,
    filters: dict[str, Any] | None = None,
    group_by_key: str | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetAggregateConformancePackComplianceSummaryResult:
    """Get aggregate conformance pack compliance summary.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        filters: Filters.
        group_by_key: Group by key.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if filters is not None:
        kwargs["Filters"] = filters
    if group_by_key is not None:
        kwargs["GroupByKey"] = group_by_key
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_aggregate_conformance_pack_compliance_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to get aggregate conformance pack compliance summary"
        ) from exc
    return GetAggregateConformancePackComplianceSummaryResult(
        aggregate_conformance_pack_compliance_summaries=resp.get(
            "AggregateConformancePackComplianceSummaries"
        ),
        group_by_key=resp.get("GroupByKey"),
        next_token=resp.get("NextToken"),
    )


def get_aggregate_discovered_resource_counts(
    configuration_aggregator_name: str,
    *,
    filters: dict[str, Any] | None = None,
    group_by_key: str | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetAggregateDiscoveredResourceCountsResult:
    """Get aggregate discovered resource counts.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        filters: Filters.
        group_by_key: Group by key.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if filters is not None:
        kwargs["Filters"] = filters
    if group_by_key is not None:
        kwargs["GroupByKey"] = group_by_key
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_aggregate_discovered_resource_counts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get aggregate discovered resource counts") from exc
    return GetAggregateDiscoveredResourceCountsResult(
        total_discovered_resources=resp.get("TotalDiscoveredResources"),
        group_by_key=resp.get("GroupByKey"),
        grouped_resource_counts=resp.get("GroupedResourceCounts"),
        next_token=resp.get("NextToken"),
    )


def get_aggregate_resource_config(
    configuration_aggregator_name: str,
    resource_identifier: dict[str, Any],
    region_name: str | None = None,
) -> GetAggregateResourceConfigResult:
    """Get aggregate resource config.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        resource_identifier: Resource identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    kwargs["ResourceIdentifier"] = resource_identifier
    try:
        resp = client.get_aggregate_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get aggregate resource config") from exc
    return GetAggregateResourceConfigResult(
        configuration_item=resp.get("ConfigurationItem"),
    )


def get_compliance_details_by_resource(
    *,
    resource_type: str | None = None,
    resource_id: str | None = None,
    compliance_types: list[str] | None = None,
    next_token: str | None = None,
    resource_evaluation_id: str | None = None,
    region_name: str | None = None,
) -> GetComplianceDetailsByResourceResult:
    """Get compliance details by resource.

    Args:
        resource_type: Resource type.
        resource_id: Resource id.
        compliance_types: Compliance types.
        next_token: Next token.
        resource_evaluation_id: Resource evaluation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if resource_type is not None:
        kwargs["ResourceType"] = resource_type
    if resource_id is not None:
        kwargs["ResourceId"] = resource_id
    if compliance_types is not None:
        kwargs["ComplianceTypes"] = compliance_types
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if resource_evaluation_id is not None:
        kwargs["ResourceEvaluationId"] = resource_evaluation_id
    try:
        resp = client.get_compliance_details_by_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get compliance details by resource") from exc
    return GetComplianceDetailsByResourceResult(
        evaluation_results=resp.get("EvaluationResults"),
        next_token=resp.get("NextToken"),
    )


def get_compliance_summary_by_config_rule(
    region_name: str | None = None,
) -> GetComplianceSummaryByConfigRuleResult:
    """Get compliance summary by config rule.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_compliance_summary_by_config_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get compliance summary by config rule") from exc
    return GetComplianceSummaryByConfigRuleResult(
        compliance_summary=resp.get("ComplianceSummary"),
    )


def get_compliance_summary_by_resource_type(
    *,
    resource_types: list[str] | None = None,
    region_name: str | None = None,
) -> GetComplianceSummaryByResourceTypeResult:
    """Get compliance summary by resource type.

    Args:
        resource_types: Resource types.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if resource_types is not None:
        kwargs["ResourceTypes"] = resource_types
    try:
        resp = client.get_compliance_summary_by_resource_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get compliance summary by resource type") from exc
    return GetComplianceSummaryByResourceTypeResult(
        compliance_summaries_by_resource_type=resp.get("ComplianceSummariesByResourceType"),
    )


def get_conformance_pack_compliance_details(
    conformance_pack_name: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetConformancePackComplianceDetailsResult:
    """Get conformance pack compliance details.

    Args:
        conformance_pack_name: Conformance pack name.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConformancePackName"] = conformance_pack_name
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_conformance_pack_compliance_details(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get conformance pack compliance details") from exc
    return GetConformancePackComplianceDetailsResult(
        conformance_pack_name=resp.get("ConformancePackName"),
        conformance_pack_rule_evaluation_results=resp.get("ConformancePackRuleEvaluationResults"),
        next_token=resp.get("NextToken"),
    )


def get_conformance_pack_compliance_summary(
    conformance_pack_names: list[str],
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetConformancePackComplianceSummaryResult:
    """Get conformance pack compliance summary.

    Args:
        conformance_pack_names: Conformance pack names.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConformancePackNames"] = conformance_pack_names
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_conformance_pack_compliance_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get conformance pack compliance summary") from exc
    return GetConformancePackComplianceSummaryResult(
        conformance_pack_compliance_summary_list=resp.get("ConformancePackComplianceSummaryList"),
        next_token=resp.get("NextToken"),
    )


def get_custom_rule_policy(
    *,
    config_rule_name: str | None = None,
    region_name: str | None = None,
) -> GetCustomRulePolicyResult:
    """Get custom rule policy.

    Args:
        config_rule_name: Config rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if config_rule_name is not None:
        kwargs["ConfigRuleName"] = config_rule_name
    try:
        resp = client.get_custom_rule_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get custom rule policy") from exc
    return GetCustomRulePolicyResult(
        policy_text=resp.get("PolicyText"),
    )


def get_discovered_resource_counts(
    *,
    resource_types: list[str] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetDiscoveredResourceCountsResult:
    """Get discovered resource counts.

    Args:
        resource_types: Resource types.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if resource_types is not None:
        kwargs["resourceTypes"] = resource_types
    if limit is not None:
        kwargs["limit"] = limit
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.get_discovered_resource_counts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get discovered resource counts") from exc
    return GetDiscoveredResourceCountsResult(
        total_discovered_resources=resp.get("totalDiscoveredResources"),
        resource_counts=resp.get("resourceCounts"),
        next_token=resp.get("nextToken"),
    )


def get_organization_config_rule_detailed_status(
    organization_config_rule_name: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetOrganizationConfigRuleDetailedStatusResult:
    """Get organization config rule detailed status.

    Args:
        organization_config_rule_name: Organization config rule name.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConfigRuleName"] = organization_config_rule_name
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_organization_config_rule_detailed_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get organization config rule detailed status") from exc
    return GetOrganizationConfigRuleDetailedStatusResult(
        organization_config_rule_detailed_status=resp.get("OrganizationConfigRuleDetailedStatus"),
        next_token=resp.get("NextToken"),
    )


def get_organization_conformance_pack_detailed_status(
    organization_conformance_pack_name: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetOrganizationConformancePackDetailedStatusResult:
    """Get organization conformance pack detailed status.

    Args:
        organization_conformance_pack_name: Organization conformance pack name.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConformancePackName"] = organization_conformance_pack_name
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.get_organization_conformance_pack_detailed_status(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, "Failed to get organization conformance pack detailed status"
        ) from exc
    return GetOrganizationConformancePackDetailedStatusResult(
        organization_conformance_pack_detailed_statuses=resp.get(
            "OrganizationConformancePackDetailedStatuses"
        ),
        next_token=resp.get("NextToken"),
    )


def get_organization_custom_rule_policy(
    organization_config_rule_name: str,
    region_name: str | None = None,
) -> GetOrganizationCustomRulePolicyResult:
    """Get organization custom rule policy.

    Args:
        organization_config_rule_name: Organization config rule name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConfigRuleName"] = organization_config_rule_name
    try:
        resp = client.get_organization_custom_rule_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get organization custom rule policy") from exc
    return GetOrganizationCustomRulePolicyResult(
        policy_text=resp.get("PolicyText"),
    )


def get_resource_evaluation_summary(
    resource_evaluation_id: str,
    region_name: str | None = None,
) -> GetResourceEvaluationSummaryResult:
    """Get resource evaluation summary.

    Args:
        resource_evaluation_id: Resource evaluation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceEvaluationId"] = resource_evaluation_id
    try:
        resp = client.get_resource_evaluation_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource evaluation summary") from exc
    return GetResourceEvaluationSummaryResult(
        resource_evaluation_id=resp.get("ResourceEvaluationId"),
        evaluation_mode=resp.get("EvaluationMode"),
        evaluation_status=resp.get("EvaluationStatus"),
        evaluation_start_timestamp=resp.get("EvaluationStartTimestamp"),
        compliance=resp.get("Compliance"),
        evaluation_context=resp.get("EvaluationContext"),
        resource_details=resp.get("ResourceDetails"),
    )


def get_stored_query(
    query_name: str,
    region_name: str | None = None,
) -> GetStoredQueryResult:
    """Get stored query.

    Args:
        query_name: Query name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryName"] = query_name
    try:
        resp = client.get_stored_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get stored query") from exc
    return GetStoredQueryResult(
        stored_query=resp.get("StoredQuery"),
    )


def list_aggregate_discovered_resources(
    configuration_aggregator_name: str,
    resource_type: str,
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAggregateDiscoveredResourcesResult:
    """List aggregate discovered resources.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        resource_type: Resource type.
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    kwargs["ResourceType"] = resource_type
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_aggregate_discovered_resources(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list aggregate discovered resources") from exc
    return ListAggregateDiscoveredResourcesResult(
        resource_identifiers=resp.get("ResourceIdentifiers"),
        next_token=resp.get("NextToken"),
    )


def list_configuration_recorders(
    *,
    filters: list[dict[str, Any]] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListConfigurationRecordersResult:
    """List configuration recorders.

    Args:
        filters: Filters.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_configuration_recorders(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list configuration recorders") from exc
    return ListConfigurationRecordersResult(
        configuration_recorder_summaries=resp.get("ConfigurationRecorderSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_conformance_pack_compliance_scores(
    *,
    filters: dict[str, Any] | None = None,
    sort_order: str | None = None,
    sort_by: str | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListConformancePackComplianceScoresResult:
    """List conformance pack compliance scores.

    Args:
        filters: Filters.
        sort_order: Sort order.
        sort_by: Sort by.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if sort_order is not None:
        kwargs["SortOrder"] = sort_order
    if sort_by is not None:
        kwargs["SortBy"] = sort_by
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_conformance_pack_compliance_scores(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list conformance pack compliance scores") from exc
    return ListConformancePackComplianceScoresResult(
        next_token=resp.get("NextToken"),
        conformance_pack_compliance_scores=resp.get("ConformancePackComplianceScores"),
    )


def list_resource_evaluations(
    *,
    filters: dict[str, Any] | None = None,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListResourceEvaluationsResult:
    """List resource evaluations.

    Args:
        filters: Filters.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_resource_evaluations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list resource evaluations") from exc
    return ListResourceEvaluationsResult(
        resource_evaluations=resp.get("ResourceEvaluations"),
        next_token=resp.get("NextToken"),
    )


def list_stored_queries(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStoredQueriesResult:
    """List stored queries.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_stored_queries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list stored queries") from exc
    return ListStoredQueriesResult(
        stored_query_metadata=resp.get("StoredQueryMetadata"),
        next_token=resp.get("NextToken"),
    )


def list_tags_for_resource(
    resource_arn: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


def put_configuration_aggregator(
    configuration_aggregator_name: str,
    *,
    account_aggregation_sources: list[dict[str, Any]] | None = None,
    organization_aggregation_source: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    aggregator_filters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutConfigurationAggregatorResult:
    """Put configuration aggregator.

    Args:
        configuration_aggregator_name: Configuration aggregator name.
        account_aggregation_sources: Account aggregation sources.
        organization_aggregation_source: Organization aggregation source.
        tags: Tags.
        aggregator_filters: Aggregator filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if account_aggregation_sources is not None:
        kwargs["AccountAggregationSources"] = account_aggregation_sources
    if organization_aggregation_source is not None:
        kwargs["OrganizationAggregationSource"] = organization_aggregation_source
    if tags is not None:
        kwargs["Tags"] = tags
    if aggregator_filters is not None:
        kwargs["AggregatorFilters"] = aggregator_filters
    try:
        resp = client.put_configuration_aggregator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put configuration aggregator") from exc
    return PutConfigurationAggregatorResult(
        configuration_aggregator=resp.get("ConfigurationAggregator"),
    )


def put_conformance_pack(
    conformance_pack_name: str,
    *,
    template_s3_uri: str | None = None,
    template_body: str | None = None,
    delivery_s3_bucket: str | None = None,
    delivery_s3_key_prefix: str | None = None,
    conformance_pack_input_parameters: list[dict[str, Any]] | None = None,
    template_ssm_document_details: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutConformancePackResult:
    """Put conformance pack.

    Args:
        conformance_pack_name: Conformance pack name.
        template_s3_uri: Template s3 uri.
        template_body: Template body.
        delivery_s3_bucket: Delivery s3 bucket.
        delivery_s3_key_prefix: Delivery s3 key prefix.
        conformance_pack_input_parameters: Conformance pack input parameters.
        template_ssm_document_details: Template ssm document details.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConformancePackName"] = conformance_pack_name
    if template_s3_uri is not None:
        kwargs["TemplateS3Uri"] = template_s3_uri
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if delivery_s3_bucket is not None:
        kwargs["DeliveryS3Bucket"] = delivery_s3_bucket
    if delivery_s3_key_prefix is not None:
        kwargs["DeliveryS3KeyPrefix"] = delivery_s3_key_prefix
    if conformance_pack_input_parameters is not None:
        kwargs["ConformancePackInputParameters"] = conformance_pack_input_parameters
    if template_ssm_document_details is not None:
        kwargs["TemplateSSMDocumentDetails"] = template_ssm_document_details
    try:
        resp = client.put_conformance_pack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put conformance pack") from exc
    return PutConformancePackResult(
        conformance_pack_arn=resp.get("ConformancePackArn"),
    )


def put_delivery_channel(
    delivery_channel: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put delivery channel.

    Args:
        delivery_channel: Delivery channel.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryChannel"] = delivery_channel
    try:
        client.put_delivery_channel(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put delivery channel") from exc
    return None


def put_evaluations(
    result_token: str,
    *,
    evaluations: list[dict[str, Any]] | None = None,
    run_mode: bool | None = None,
    region_name: str | None = None,
) -> PutEvaluationsResult:
    """Put evaluations.

    Args:
        result_token: Result token.
        evaluations: Evaluations.
        run_mode: Run mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResultToken"] = result_token
    if evaluations is not None:
        kwargs["Evaluations"] = evaluations
    if run_mode is not None:
        kwargs["TestMode"] = run_mode
    try:
        resp = client.put_evaluations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put evaluations") from exc
    return PutEvaluationsResult(
        failed_evaluations=resp.get("FailedEvaluations"),
    )


def put_external_evaluation(
    config_rule_name: str,
    external_evaluation: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Put external evaluation.

    Args:
        config_rule_name: Config rule name.
        external_evaluation: External evaluation.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    kwargs["ExternalEvaluation"] = external_evaluation
    try:
        client.put_external_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put external evaluation") from exc
    return None


def put_organization_config_rule(
    organization_config_rule_name: str,
    *,
    organization_managed_rule_metadata: dict[str, Any] | None = None,
    organization_custom_rule_metadata: dict[str, Any] | None = None,
    excluded_accounts: list[str] | None = None,
    organization_custom_policy_rule_metadata: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> PutOrganizationConfigRuleResult:
    """Put organization config rule.

    Args:
        organization_config_rule_name: Organization config rule name.
        organization_managed_rule_metadata: Organization managed rule metadata.
        organization_custom_rule_metadata: Organization custom rule metadata.
        excluded_accounts: Excluded accounts.
        organization_custom_policy_rule_metadata: Organization custom policy rule metadata.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConfigRuleName"] = organization_config_rule_name
    if organization_managed_rule_metadata is not None:
        kwargs["OrganizationManagedRuleMetadata"] = organization_managed_rule_metadata
    if organization_custom_rule_metadata is not None:
        kwargs["OrganizationCustomRuleMetadata"] = organization_custom_rule_metadata
    if excluded_accounts is not None:
        kwargs["ExcludedAccounts"] = excluded_accounts
    if organization_custom_policy_rule_metadata is not None:
        kwargs["OrganizationCustomPolicyRuleMetadata"] = organization_custom_policy_rule_metadata
    try:
        resp = client.put_organization_config_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put organization config rule") from exc
    return PutOrganizationConfigRuleResult(
        organization_config_rule_arn=resp.get("OrganizationConfigRuleArn"),
    )


def put_organization_conformance_pack(
    organization_conformance_pack_name: str,
    *,
    template_s3_uri: str | None = None,
    template_body: str | None = None,
    delivery_s3_bucket: str | None = None,
    delivery_s3_key_prefix: str | None = None,
    conformance_pack_input_parameters: list[dict[str, Any]] | None = None,
    excluded_accounts: list[str] | None = None,
    region_name: str | None = None,
) -> PutOrganizationConformancePackResult:
    """Put organization conformance pack.

    Args:
        organization_conformance_pack_name: Organization conformance pack name.
        template_s3_uri: Template s3 uri.
        template_body: Template body.
        delivery_s3_bucket: Delivery s3 bucket.
        delivery_s3_key_prefix: Delivery s3 key prefix.
        conformance_pack_input_parameters: Conformance pack input parameters.
        excluded_accounts: Excluded accounts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["OrganizationConformancePackName"] = organization_conformance_pack_name
    if template_s3_uri is not None:
        kwargs["TemplateS3Uri"] = template_s3_uri
    if template_body is not None:
        kwargs["TemplateBody"] = template_body
    if delivery_s3_bucket is not None:
        kwargs["DeliveryS3Bucket"] = delivery_s3_bucket
    if delivery_s3_key_prefix is not None:
        kwargs["DeliveryS3KeyPrefix"] = delivery_s3_key_prefix
    if conformance_pack_input_parameters is not None:
        kwargs["ConformancePackInputParameters"] = conformance_pack_input_parameters
    if excluded_accounts is not None:
        kwargs["ExcludedAccounts"] = excluded_accounts
    try:
        resp = client.put_organization_conformance_pack(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put organization conformance pack") from exc
    return PutOrganizationConformancePackResult(
        organization_conformance_pack_arn=resp.get("OrganizationConformancePackArn"),
    )


def put_remediation_exceptions(
    config_rule_name: str,
    resource_keys: list[dict[str, Any]],
    *,
    message: str | None = None,
    expiration_time: str | None = None,
    region_name: str | None = None,
) -> PutRemediationExceptionsResult:
    """Put remediation exceptions.

    Args:
        config_rule_name: Config rule name.
        resource_keys: Resource keys.
        message: Message.
        expiration_time: Expiration time.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigRuleName"] = config_rule_name
    kwargs["ResourceKeys"] = resource_keys
    if message is not None:
        kwargs["Message"] = message
    if expiration_time is not None:
        kwargs["ExpirationTime"] = expiration_time
    try:
        resp = client.put_remediation_exceptions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put remediation exceptions") from exc
    return PutRemediationExceptionsResult(
        failed_batches=resp.get("FailedBatches"),
    )


def put_resource_config(
    resource_type: str,
    schema_version_id: str,
    resource_id: str,
    configuration: str,
    *,
    resource_name: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Put resource config.

    Args:
        resource_type: Resource type.
        schema_version_id: Schema version id.
        resource_id: Resource id.
        configuration: Configuration.
        resource_name: Resource name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceType"] = resource_type
    kwargs["SchemaVersionId"] = schema_version_id
    kwargs["ResourceId"] = resource_id
    kwargs["Configuration"] = configuration
    if resource_name is not None:
        kwargs["ResourceName"] = resource_name
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        client.put_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource config") from exc
    return None


def put_retention_configuration(
    retention_period_in_days: int,
    region_name: str | None = None,
) -> PutRetentionConfigurationResult:
    """Put retention configuration.

    Args:
        retention_period_in_days: Retention period in days.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RetentionPeriodInDays"] = retention_period_in_days
    try:
        resp = client.put_retention_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put retention configuration") from exc
    return PutRetentionConfigurationResult(
        retention_configuration=resp.get("RetentionConfiguration"),
    )


def put_service_linked_configuration_recorder(
    service_principal: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PutServiceLinkedConfigurationRecorderResult:
    """Put service linked configuration recorder.

    Args:
        service_principal: Service principal.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ServicePrincipal"] = service_principal
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.put_service_linked_configuration_recorder(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put service linked configuration recorder") from exc
    return PutServiceLinkedConfigurationRecorderResult(
        arn=resp.get("Arn"),
        name=resp.get("Name"),
    )


def put_stored_query(
    stored_query: dict[str, Any],
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> PutStoredQueryResult:
    """Put stored query.

    Args:
        stored_query: Stored query.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StoredQuery"] = stored_query
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.put_stored_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put stored query") from exc
    return PutStoredQueryResult(
        query_arn=resp.get("QueryArn"),
    )


def select_aggregate_resource_config(
    expression: str,
    configuration_aggregator_name: str,
    *,
    limit: int | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> SelectAggregateResourceConfigResult:
    """Select aggregate resource config.

    Args:
        expression: Expression.
        configuration_aggregator_name: Configuration aggregator name.
        limit: Limit.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Expression"] = expression
    kwargs["ConfigurationAggregatorName"] = configuration_aggregator_name
    if limit is not None:
        kwargs["Limit"] = limit
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.select_aggregate_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to select aggregate resource config") from exc
    return SelectAggregateResourceConfigResult(
        results=resp.get("Results"),
        query_info=resp.get("QueryInfo"),
        next_token=resp.get("NextToken"),
    )


def select_resource_config(
    expression: str,
    *,
    limit: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> SelectResourceConfigResult:
    """Select resource config.

    Args:
        expression: Expression.
        limit: Limit.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Expression"] = expression
    if limit is not None:
        kwargs["Limit"] = limit
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.select_resource_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to select resource config") from exc
    return SelectResourceConfigResult(
        results=resp.get("Results"),
        query_info=resp.get("QueryInfo"),
        next_token=resp.get("NextToken"),
    )


def start_resource_evaluation(
    resource_details: dict[str, Any],
    evaluation_mode: str,
    *,
    evaluation_context: dict[str, Any] | None = None,
    evaluation_timeout: int | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> StartResourceEvaluationResult:
    """Start resource evaluation.

    Args:
        resource_details: Resource details.
        evaluation_mode: Evaluation mode.
        evaluation_context: Evaluation context.
        evaluation_timeout: Evaluation timeout.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceDetails"] = resource_details
    kwargs["EvaluationMode"] = evaluation_mode
    if evaluation_context is not None:
        kwargs["EvaluationContext"] = evaluation_context
    if evaluation_timeout is not None:
        kwargs["EvaluationTimeout"] = evaluation_timeout
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.start_resource_evaluation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start resource evaluation") from exc
    return StartResourceEvaluationResult(
        resource_evaluation_id=resp.get("ResourceEvaluationId"),
    )


def tag_resource(
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
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
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
    client = get_client("config", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
