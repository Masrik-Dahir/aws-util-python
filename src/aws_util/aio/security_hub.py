"""Native async Security Hub utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.security_hub import (
    BatchDeleteAutomationRulesResult,
    BatchGetAutomationRulesResult,
    BatchGetConfigurationPolicyAssociationsResult,
    BatchGetSecurityControlsResult,
    BatchGetStandardsControlAssociationsResult,
    BatchImportFindingsResult,
    BatchUpdateAutomationRulesResult,
    BatchUpdateFindingsResult,
    BatchUpdateFindingsV2Result,
    BatchUpdateStandardsControlAssociationsResult,
    ConnectorRegistrationsV2Result,
    CreateActionTargetResult,
    CreateAggregatorV2Result,
    CreateAutomationRuleResult,
    CreateAutomationRuleV2Result,
    CreateConfigurationPolicyResult,
    CreateConnectorV2Result,
    CreateFindingAggregatorResult,
    CreateTicketV2Result,
    DeclineInvitationsResult,
    DeleteActionTargetResult,
    DeleteInvitationsResult,
    DescribeActionTargetsResult,
    DescribeOrganizationConfigurationResult,
    DescribeProductsResult,
    DescribeProductsV2Result,
    DescribeSecurityHubV2Result,
    EnableOrganizationAdminAccountResult,
    EnableSecurityHubV2Result,
    FindingResult,
    GetAggregatorV2Result,
    GetAutomationRuleV2Result,
    GetConfigurationPolicyAssociationResult,
    GetConfigurationPolicyResult,
    GetConnectorV2Result,
    GetFindingAggregatorResult,
    GetFindingHistoryResult,
    GetFindingStatisticsV2Result,
    GetFindingsV2Result,
    GetInsightsResult,
    GetInvitationsCountResult,
    GetMasterAccountResult,
    GetResourcesStatisticsV2Result,
    GetResourcesV2Result,
    GetSecurityControlDefinitionResult,
    HubResult,
    InsightResult,
    ListAggregatorsV2Result,
    ListAutomationRulesResult,
    ListAutomationRulesV2Result,
    ListConfigurationPoliciesResult,
    ListConfigurationPolicyAssociationsResult,
    ListConnectorsV2Result,
    ListFindingAggregatorsResult,
    ListInvitationsResult,
    ListOrganizationAdminAccountsResult,
    ListSecurityControlDefinitionsResult,
    ListStandardsControlAssociationsResult,
    ListTagsForResourceResult,
    MemberResult,
    StandardResult,
    StartConfigurationPolicyAssociationResult,
    UpdateAggregatorV2Result,
    UpdateConfigurationPolicyResult,
    UpdateFindingAggregatorResult,
    _parse_finding,
    _parse_member,
)

__all__ = [
    "BatchDeleteAutomationRulesResult",
    "BatchGetAutomationRulesResult",
    "BatchGetConfigurationPolicyAssociationsResult",
    "BatchGetSecurityControlsResult",
    "BatchGetStandardsControlAssociationsResult",
    "BatchImportFindingsResult",
    "BatchUpdateAutomationRulesResult",
    "BatchUpdateFindingsResult",
    "BatchUpdateFindingsV2Result",
    "BatchUpdateStandardsControlAssociationsResult",
    "ConnectorRegistrationsV2Result",
    "CreateActionTargetResult",
    "CreateAggregatorV2Result",
    "CreateAutomationRuleResult",
    "CreateAutomationRuleV2Result",
    "CreateConfigurationPolicyResult",
    "CreateConnectorV2Result",
    "CreateFindingAggregatorResult",
    "CreateTicketV2Result",
    "DeclineInvitationsResult",
    "DeleteActionTargetResult",
    "DeleteInvitationsResult",
    "DescribeActionTargetsResult",
    "DescribeOrganizationConfigurationResult",
    "DescribeProductsResult",
    "DescribeProductsV2Result",
    "DescribeSecurityHubV2Result",
    "EnableOrganizationAdminAccountResult",
    "EnableSecurityHubV2Result",
    "FindingResult",
    "GetAggregatorV2Result",
    "GetAutomationRuleV2Result",
    "GetConfigurationPolicyAssociationResult",
    "GetConfigurationPolicyResult",
    "GetConnectorV2Result",
    "GetFindingAggregatorResult",
    "GetFindingHistoryResult",
    "GetFindingStatisticsV2Result",
    "GetFindingsV2Result",
    "GetInsightsResult",
    "GetInvitationsCountResult",
    "GetMasterAccountResult",
    "GetResourcesStatisticsV2Result",
    "GetResourcesV2Result",
    "GetSecurityControlDefinitionResult",
    "HubResult",
    "InsightResult",
    "ListAggregatorsV2Result",
    "ListAutomationRulesResult",
    "ListAutomationRulesV2Result",
    "ListConfigurationPoliciesResult",
    "ListConfigurationPolicyAssociationsResult",
    "ListConnectorsV2Result",
    "ListFindingAggregatorsResult",
    "ListInvitationsResult",
    "ListOrganizationAdminAccountsResult",
    "ListSecurityControlDefinitionsResult",
    "ListStandardsControlAssociationsResult",
    "ListTagsForResourceResult",
    "MemberResult",
    "StandardResult",
    "StartConfigurationPolicyAssociationResult",
    "UpdateAggregatorV2Result",
    "UpdateConfigurationPolicyResult",
    "UpdateFindingAggregatorResult",
    "accept_administrator_invitation",
    "accept_invitation",
    "batch_delete_automation_rules",
    "batch_disable_standards",
    "batch_enable_standards",
    "batch_get_automation_rules",
    "batch_get_configuration_policy_associations",
    "batch_get_security_controls",
    "batch_get_standards_control_associations",
    "batch_import_findings",
    "batch_update_automation_rules",
    "batch_update_findings",
    "batch_update_findings_v2",
    "batch_update_standards_control_associations",
    "connector_registrations_v2",
    "create_action_target",
    "create_aggregator_v2",
    "create_automation_rule",
    "create_automation_rule_v2",
    "create_configuration_policy",
    "create_connector_v2",
    "create_finding_aggregator",
    "create_insight",
    "create_members",
    "create_ticket_v2",
    "decline_invitations",
    "delete_action_target",
    "delete_aggregator_v2",
    "delete_automation_rule_v2",
    "delete_configuration_policy",
    "delete_connector_v2",
    "delete_finding_aggregator",
    "delete_insight",
    "delete_invitations",
    "delete_members",
    "describe_action_targets",
    "describe_hub",
    "describe_organization_configuration",
    "describe_products",
    "describe_products_v2",
    "describe_security_hub_v2",
    "describe_standards",
    "describe_standards_controls",
    "disable_import_findings_for_product",
    "disable_organization_admin_account",
    "disable_security_hub",
    "disable_security_hub_v2",
    "disassociate_from_administrator_account",
    "disassociate_from_master_account",
    "disassociate_members",
    "enable_import_findings_for_product",
    "enable_organization_admin_account",
    "enable_security_hub",
    "enable_security_hub_v2",
    "get_administrator_account",
    "get_aggregator_v2",
    "get_automation_rule_v2",
    "get_configuration_policy",
    "get_configuration_policy_association",
    "get_connector_v2",
    "get_enabled_standards",
    "get_finding_aggregator",
    "get_finding_history",
    "get_finding_statistics_v2",
    "get_findings",
    "get_findings_v2",
    "get_insight_results",
    "get_insights",
    "get_invitations_count",
    "get_master_account",
    "get_members",
    "get_resources_statistics_v2",
    "get_resources_v2",
    "get_security_control_definition",
    "invite_members",
    "list_aggregators_v2",
    "list_automation_rules",
    "list_automation_rules_v2",
    "list_configuration_policies",
    "list_configuration_policy_associations",
    "list_connectors_v2",
    "list_enabled_products_for_import",
    "list_finding_aggregators",
    "list_insights",
    "list_invitations",
    "list_members",
    "list_organization_admin_accounts",
    "list_security_control_definitions",
    "list_standards_control_associations",
    "list_tags_for_resource",
    "start_configuration_policy_association",
    "start_configuration_policy_disassociation",
    "tag_resource",
    "untag_resource",
    "update_action_target",
    "update_aggregator_v2",
    "update_automation_rule_v2",
    "update_configuration_policy",
    "update_connector_v2",
    "update_finding_aggregator",
    "update_findings",
    "update_insight",
    "update_organization_configuration",
    "update_security_control",
    "update_security_hub_configuration",
    "update_standards_control",
]


# ---------------------------------------------------------------------------
# Hub management
# ---------------------------------------------------------------------------


async def enable_security_hub(
    *,
    enable_default_standards: bool = True,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Enable AWS Security Hub in the account.

    Args:
        enable_default_standards: Whether to enable the default
            standards.
        tags: Optional tags for the hub resource.
        region_name: AWS region override.

    Returns:
        The hub ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {
        "EnableDefaultStandards": enable_default_standards,
    }
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("EnableSecurityHub", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "enable_security_hub failed") from exc
    return resp.get("HubArn", "")


async def disable_security_hub(
    *,
    region_name: str | None = None,
) -> None:
    """Disable AWS Security Hub in the account.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        await client.call("DisableSecurityHub")
    except Exception as exc:
        raise wrap_aws_error(exc, "disable_security_hub failed") from exc


async def describe_hub(
    *,
    hub_arn: str | None = None,
    region_name: str | None = None,
) -> HubResult:
    """Describe the Security Hub configuration.

    Args:
        hub_arn: Optional hub ARN to describe.
        region_name: AWS region override.

    Returns:
        A :class:`HubResult` with hub metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if hub_arn:
        kwargs["HubArn"] = hub_arn
    try:
        resp = await client.call("DescribeHub", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_hub failed") from exc
    return HubResult(
        hub_arn=resp.get("HubArn"),
        subscribed_at=resp.get("SubscribedAt"),
        auto_enable_controls=resp.get("AutoEnableControls", True),
        extra={
            k: v
            for k, v in resp.items()
            if k
            not in {
                "HubArn",
                "SubscribedAt",
                "AutoEnableControls",
                "ResponseMetadata",
            }
        },
    )


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


async def get_findings(
    *,
    filters: dict[str, Any] | None = None,
    sort_criteria: list[dict[str, str]] | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[FindingResult]:
    """Retrieve Security Hub findings.

    Args:
        filters: ASFF-format filters dict.
        sort_criteria: List of sort criterion dicts.
        max_results: Maximum number of findings per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`FindingResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters
    if sort_criteria:
        kwargs["SortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[FindingResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("GetFindings", **kwargs)
            for f in resp.get("Findings", []):
                results.append(_parse_finding(f))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "get_findings failed") from exc
    return results


async def update_findings(
    finding_identifiers: list[dict[str, str]],
    *,
    note: dict[str, str] | None = None,
    severity: dict[str, Any] | None = None,
    workflow: dict[str, str] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update Security Hub findings.

    Args:
        finding_identifiers: List of dicts with ``Id`` and
            ``ProductArn`` keys.
        note: Optional note to attach.
        severity: Optional severity update dict.
        workflow: Optional workflow status update dict.
        region_name: AWS region override.

    Returns:
        A dict with ``ProcessedFindings`` and ``UnprocessedFindings``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {
        "FindingIdentifiers": finding_identifiers,
    }
    if note:
        kwargs["Note"] = note
    if severity:
        kwargs["Severity"] = severity
    if workflow:
        kwargs["Workflow"] = workflow
    try:
        resp = await client.call("BatchUpdateFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "update_findings failed") from exc
    return {
        "ProcessedFindings": resp.get("ProcessedFindings", []),
        "UnprocessedFindings": resp.get("UnprocessedFindings", []),
    }


# ---------------------------------------------------------------------------
# Insights
# ---------------------------------------------------------------------------


async def get_insight_results(
    insight_arn: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Get results for a Security Hub insight.

    Args:
        insight_arn: ARN of the insight.
        region_name: AWS region override.

    Returns:
        The insight results dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call("GetInsightResults", InsightArn=insight_arn)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_insight_results failed for {insight_arn!r}",
        ) from exc
    return resp.get("InsightResults", {})


async def list_insights(
    *,
    max_results: int | None = None,
    region_name: str | None = None,
) -> list[InsightResult]:
    """List Security Hub insights.

    Args:
        max_results: Maximum number of results per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`InsightResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[InsightResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("GetInsights", **kwargs)
            for insight in resp.get("Insights", []):
                results.append(
                    InsightResult(
                        insight_arn=insight.get("InsightArn", ""),
                        name=insight.get("Name", ""),
                        filters=insight.get("Filters", {}),
                        group_by_attribute=insight.get("GroupByAttribute", ""),
                        extra={
                            k: v
                            for k, v in insight.items()
                            if k
                            not in {
                                "InsightArn",
                                "Name",
                                "Filters",
                                "GroupByAttribute",
                            }
                        },
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_insights failed") from exc
    return results


async def create_insight(
    name: str,
    *,
    filters: dict[str, Any],
    group_by_attribute: str,
    region_name: str | None = None,
) -> str:
    """Create a Security Hub insight.

    Args:
        name: Display name for the insight.
        filters: ASFF-format filters dict.
        group_by_attribute: Attribute to group results by.
        region_name: AWS region override.

    Returns:
        The ARN of the newly created insight.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call(
            "CreateInsight",
            Name=name,
            Filters=filters,
            GroupByAttribute=group_by_attribute,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_insight failed for {name!r}") from exc
    return resp.get("InsightArn", "")


async def update_insight(
    insight_arn: str,
    *,
    name: str | None = None,
    filters: dict[str, Any] | None = None,
    group_by_attribute: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update an existing Security Hub insight.

    Args:
        insight_arn: ARN of the insight to update.
        name: New display name.
        filters: New ASFF-format filters dict.
        group_by_attribute: New grouping attribute.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {"InsightArn": insight_arn}
    if name is not None:
        kwargs["Name"] = name
    if filters is not None:
        kwargs["Filters"] = filters
    if group_by_attribute is not None:
        kwargs["GroupByAttribute"] = group_by_attribute
    try:
        await client.call("UpdateInsight", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_insight failed for {insight_arn!r}") from exc


async def delete_insight(
    insight_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Security Hub insight.

    Args:
        insight_arn: ARN of the insight to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        await client.call("DeleteInsight", InsightArn=insight_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_insight failed for {insight_arn!r}") from exc


# ---------------------------------------------------------------------------
# Product integrations
# ---------------------------------------------------------------------------


async def enable_import_findings_for_product(
    product_arn: str,
    *,
    region_name: str | None = None,
) -> str:
    """Enable importing findings from an integrated product.

    Args:
        product_arn: ARN of the product to enable.
        region_name: AWS region override.

    Returns:
        The product subscription ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call(
            "EnableImportFindingsForProduct",
            ProductArn=product_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"enable_import_findings_for_product failed for {product_arn!r}",
        ) from exc
    return resp.get("ProductSubscriptionArn", "")


async def disable_import_findings_for_product(
    product_subscription_arn: str,
    *,
    region_name: str | None = None,
) -> None:
    """Disable importing findings from an integrated product.

    Args:
        product_subscription_arn: The product subscription ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        await client.call(
            "DisableImportFindingsForProduct",
            ProductSubscriptionArn=product_subscription_arn,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"disable_import_findings_for_product failed for {product_subscription_arn!r}",
        ) from exc


async def list_enabled_products_for_import(
    *,
    region_name: str | None = None,
) -> list[str]:
    """List product subscription ARNs enabled for import.

    Args:
        region_name: AWS region override.

    Returns:
        A list of product subscription ARN strings.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    arns: list[str] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {}
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("ListEnabledProductsForImport", **kwargs)
            arns.extend(resp.get("ProductSubscriptions", []))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_enabled_products_for_import failed") from exc
    return arns


# ---------------------------------------------------------------------------
# Standards
# ---------------------------------------------------------------------------


async def get_enabled_standards(
    *,
    standards_subscription_arns: list[str] | None = None,
    region_name: str | None = None,
) -> list[StandardResult]:
    """Get enabled standards subscriptions.

    Args:
        standards_subscription_arns: Filter by subscription ARNs.
        region_name: AWS region override.

    Returns:
        A list of :class:`StandardResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if standards_subscription_arns:
        kwargs["StandardsSubscriptionArns"] = standards_subscription_arns
    results: list[StandardResult] = []
    try:
        token: str | None = None
        while True:
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("GetEnabledStandards", **kwargs)
            for std in resp.get("StandardsSubscriptions", []):
                results.append(
                    StandardResult(
                        standards_arn=std.get("StandardsArn"),
                        standards_subscription_arn=std.get("StandardsSubscriptionArn"),
                        standards_status=std.get("StandardsStatus"),
                        extra={
                            k: v
                            for k, v in std.items()
                            if k
                            not in {
                                "StandardsArn",
                                "StandardsSubscriptionArn",
                                "StandardsStatus",
                            }
                        },
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "get_enabled_standards failed") from exc
    return results


async def batch_enable_standards(
    standards_subscription_requests: list[dict[str, Any]],
    *,
    region_name: str | None = None,
) -> list[StandardResult]:
    """Enable one or more security standards.

    Args:
        standards_subscription_requests: List of dicts, each with
            ``StandardsArn`` and optionally ``StandardsInput``.
        region_name: AWS region override.

    Returns:
        A list of :class:`StandardResult` for the enabled standards.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call(
            "BatchEnableStandards",
            StandardsSubscriptionRequests=(standards_subscription_requests),
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "batch_enable_standards failed") from exc
    results: list[StandardResult] = []
    for std in resp.get("StandardsSubscriptions", []):
        results.append(
            StandardResult(
                standards_arn=std.get("StandardsArn"),
                standards_subscription_arn=std.get("StandardsSubscriptionArn"),
                standards_status=std.get("StandardsStatus"),
                extra={
                    k: v
                    for k, v in std.items()
                    if k
                    not in {
                        "StandardsArn",
                        "StandardsSubscriptionArn",
                        "StandardsStatus",
                    }
                },
            )
        )
    return results


async def batch_disable_standards(
    standards_subscription_arns: list[str],
    *,
    region_name: str | None = None,
) -> None:
    """Disable one or more security standards.

    Args:
        standards_subscription_arns: List of subscription ARNs to
            disable.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        await client.call(
            "BatchDisableStandards",
            StandardsSubscriptionArns=(standards_subscription_arns),
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "batch_disable_standards failed") from exc


async def describe_standards(
    *,
    region_name: str | None = None,
) -> list[StandardResult]:
    """Describe available security standards.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`StandardResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    results: list[StandardResult] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {}
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("DescribeStandards", **kwargs)
            for std in resp.get("Standards", []):
                results.append(
                    StandardResult(
                        standards_arn=std.get("StandardsArn"),
                        name=std.get("Name", ""),
                        description=std.get("Description", ""),
                        extra={
                            k: v
                            for k, v in std.items()
                            if k
                            not in {
                                "StandardsArn",
                                "Name",
                                "Description",
                            }
                        },
                    )
                )
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "describe_standards failed") from exc
    return results


async def describe_standards_controls(
    standards_subscription_arn: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Describe controls for an enabled standard.

    Args:
        standards_subscription_arn: The subscription ARN.
        region_name: AWS region override.

    Returns:
        A list of control detail dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    results: list[dict[str, Any]] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "StandardsSubscriptionArn": (standards_subscription_arn),
            }
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("DescribeStandardsControls", **kwargs)
            results.extend(resp.get("Controls", []))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_standards_controls failed for {standards_subscription_arn!r}",
        ) from exc
    return results


async def update_standards_control(
    standards_control_arn: str,
    *,
    control_status: str,
    disabled_reason: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update the status of a standards control.

    Args:
        standards_control_arn: ARN of the control to update.
        control_status: ``"ENABLED"`` or ``"DISABLED"``.
        disabled_reason: Required when disabling a control.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {
        "StandardsControlArn": standards_control_arn,
        "ControlStatus": control_status,
    }
    if disabled_reason is not None:
        kwargs["DisabledReason"] = disabled_reason
    try:
        await client.call("UpdateStandardsControl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_standards_control failed for {standards_control_arn!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------


async def invite_members(
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Invite member accounts to Security Hub.

    Args:
        account_ids: List of AWS account IDs to invite.
        region_name: AWS region override.

    Returns:
        A list of unprocessed account dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call("InviteMembers", AccountIds=account_ids)
    except Exception as exc:
        raise wrap_aws_error(exc, "invite_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


async def list_members(
    *,
    only_associated: bool = True,
    region_name: str | None = None,
) -> list[MemberResult]:
    """List Security Hub member accounts.

    Args:
        only_associated: If ``True``, only return associated
            members.
        region_name: AWS region override.

    Returns:
        A list of :class:`MemberResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    results: list[MemberResult] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {
                "OnlyAssociated": only_associated,
            }
            if token:
                kwargs["NextToken"] = token
            resp = await client.call("ListMembers", **kwargs)
            for m in resp.get("Members", []):
                results.append(_parse_member(m))
            token = resp.get("NextToken")
            if not token:
                break
    except Exception as exc:
        raise wrap_aws_error(exc, "list_members failed") from exc
    return results


async def get_members(
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[MemberResult]:
    """Get details for specific member accounts.

    Args:
        account_ids: List of AWS account IDs.
        region_name: AWS region override.

    Returns:
        A list of :class:`MemberResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call("GetMembers", AccountIds=account_ids)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_members failed") from exc
    return [_parse_member(m) for m in resp.get("Members", [])]


async def create_members(
    account_details: list[dict[str, str]],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Create member account associations.

    Args:
        account_details: List of dicts with ``AccountId`` and
            optionally ``Email``.
        region_name: AWS region override.

    Returns:
        A list of unprocessed account dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call("CreateMembers", AccountDetails=account_details)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


async def delete_members(
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Delete member account associations.

    Args:
        account_ids: List of AWS account IDs to remove.
        region_name: AWS region override.

    Returns:
        A list of unprocessed account dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call("DeleteMembers", AccountIds=account_ids)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


async def get_administrator_account(
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Get the administrator account for the current member.

    Args:
        region_name: AWS region override.

    Returns:
        A dict with administrator account details.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        resp = await client.call("GetAdministratorAccount")
    except Exception as exc:
        raise wrap_aws_error(exc, "get_administrator_account failed") from exc
    return resp.get("Administrator", {})


async def accept_administrator_invitation(
    administrator_id: str,
    invitation_id: str,
    *,
    region_name: str | None = None,
) -> None:
    """Accept an invitation from an administrator account.

    Args:
        administrator_id: Account ID of the administrator.
        invitation_id: The invitation identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    try:
        await client.call(
            "AcceptAdministratorInvitation",
            AdministratorId=administrator_id,
            InvitationId=invitation_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "accept_administrator_invitation failed") from exc


async def accept_invitation(
    master_id: str,
    invitation_id: str,
    region_name: str | None = None,
) -> None:
    """Accept invitation.

    Args:
        master_id: Master id.
        invitation_id: Invitation id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MasterId"] = master_id
    kwargs["InvitationId"] = invitation_id
    try:
        await client.call("AcceptInvitation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to accept invitation") from exc
    return None


async def batch_delete_automation_rules(
    automation_rules_arns: list[str],
    region_name: str | None = None,
) -> BatchDeleteAutomationRulesResult:
    """Batch delete automation rules.

    Args:
        automation_rules_arns: Automation rules arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationRulesArns"] = automation_rules_arns
    try:
        resp = await client.call("BatchDeleteAutomationRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch delete automation rules") from exc
    return BatchDeleteAutomationRulesResult(
        processed_automation_rules=resp.get("ProcessedAutomationRules"),
        unprocessed_automation_rules=resp.get("UnprocessedAutomationRules"),
    )


async def batch_get_automation_rules(
    automation_rules_arns: list[str],
    region_name: str | None = None,
) -> BatchGetAutomationRulesResult:
    """Batch get automation rules.

    Args:
        automation_rules_arns: Automation rules arns.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationRulesArns"] = automation_rules_arns
    try:
        resp = await client.call("BatchGetAutomationRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get automation rules") from exc
    return BatchGetAutomationRulesResult(
        rules=resp.get("Rules"),
        unprocessed_automation_rules=resp.get("UnprocessedAutomationRules"),
    )


async def batch_get_configuration_policy_associations(
    configuration_policy_association_identifiers: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetConfigurationPolicyAssociationsResult:
    """Batch get configuration policy associations.

    Args:
        configuration_policy_association_identifiers: Configuration policy association identifiers.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationPolicyAssociationIdentifiers"] = (
        configuration_policy_association_identifiers
    )
    try:
        resp = await client.call("BatchGetConfigurationPolicyAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get configuration policy associations") from exc
    return BatchGetConfigurationPolicyAssociationsResult(
        configuration_policy_associations=resp.get("ConfigurationPolicyAssociations"),
        unprocessed_configuration_policy_associations=resp.get(
            "UnprocessedConfigurationPolicyAssociations"
        ),
    )


async def batch_get_security_controls(
    security_control_ids: list[str],
    region_name: str | None = None,
) -> BatchGetSecurityControlsResult:
    """Batch get security controls.

    Args:
        security_control_ids: Security control ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlIds"] = security_control_ids
    try:
        resp = await client.call("BatchGetSecurityControls", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get security controls") from exc
    return BatchGetSecurityControlsResult(
        security_controls=resp.get("SecurityControls"),
        unprocessed_ids=resp.get("UnprocessedIds"),
    )


async def batch_get_standards_control_associations(
    standards_control_association_ids: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchGetStandardsControlAssociationsResult:
    """Batch get standards control associations.

    Args:
        standards_control_association_ids: Standards control association ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StandardsControlAssociationIds"] = standards_control_association_ids
    try:
        resp = await client.call("BatchGetStandardsControlAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get standards control associations") from exc
    return BatchGetStandardsControlAssociationsResult(
        standards_control_association_details=resp.get("StandardsControlAssociationDetails"),
        unprocessed_associations=resp.get("UnprocessedAssociations"),
    )


async def batch_import_findings(
    findings: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchImportFindingsResult:
    """Batch import findings.

    Args:
        findings: Findings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Findings"] = findings
    try:
        resp = await client.call("BatchImportFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch import findings") from exc
    return BatchImportFindingsResult(
        failed_count=resp.get("FailedCount"),
        success_count=resp.get("SuccessCount"),
        failed_findings=resp.get("FailedFindings"),
    )


async def batch_update_automation_rules(
    update_automation_rules_request_items: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchUpdateAutomationRulesResult:
    """Batch update automation rules.

    Args:
        update_automation_rules_request_items: Update automation rules request items.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UpdateAutomationRulesRequestItems"] = update_automation_rules_request_items
    try:
        resp = await client.call("BatchUpdateAutomationRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update automation rules") from exc
    return BatchUpdateAutomationRulesResult(
        processed_automation_rules=resp.get("ProcessedAutomationRules"),
        unprocessed_automation_rules=resp.get("UnprocessedAutomationRules"),
    )


async def batch_update_findings(
    finding_identifiers: list[dict[str, Any]],
    *,
    note: dict[str, Any] | None = None,
    severity: dict[str, Any] | None = None,
    verification_state: str | None = None,
    confidence: int | None = None,
    criticality: int | None = None,
    types: list[str] | None = None,
    user_defined_fields: dict[str, Any] | None = None,
    workflow: dict[str, Any] | None = None,
    related_findings: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> BatchUpdateFindingsResult:
    """Batch update findings.

    Args:
        finding_identifiers: Finding identifiers.
        note: Note.
        severity: Severity.
        verification_state: Verification state.
        confidence: Confidence.
        criticality: Criticality.
        types: Types.
        user_defined_fields: User defined fields.
        workflow: Workflow.
        related_findings: Related findings.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingIdentifiers"] = finding_identifiers
    if note is not None:
        kwargs["Note"] = note
    if severity is not None:
        kwargs["Severity"] = severity
    if verification_state is not None:
        kwargs["VerificationState"] = verification_state
    if confidence is not None:
        kwargs["Confidence"] = confidence
    if criticality is not None:
        kwargs["Criticality"] = criticality
    if types is not None:
        kwargs["Types"] = types
    if user_defined_fields is not None:
        kwargs["UserDefinedFields"] = user_defined_fields
    if workflow is not None:
        kwargs["Workflow"] = workflow
    if related_findings is not None:
        kwargs["RelatedFindings"] = related_findings
    try:
        resp = await client.call("BatchUpdateFindings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update findings") from exc
    return BatchUpdateFindingsResult(
        processed_findings=resp.get("ProcessedFindings"),
        unprocessed_findings=resp.get("UnprocessedFindings"),
    )


async def batch_update_findings_v2(
    *,
    metadata_uids: list[str] | None = None,
    finding_identifiers: list[dict[str, Any]] | None = None,
    comment: str | None = None,
    severity_id: int | None = None,
    status_id: int | None = None,
    region_name: str | None = None,
) -> BatchUpdateFindingsV2Result:
    """Batch update findings v2.

    Args:
        metadata_uids: Metadata uids.
        finding_identifiers: Finding identifiers.
        comment: Comment.
        severity_id: Severity id.
        status_id: Status id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if metadata_uids is not None:
        kwargs["MetadataUids"] = metadata_uids
    if finding_identifiers is not None:
        kwargs["FindingIdentifiers"] = finding_identifiers
    if comment is not None:
        kwargs["Comment"] = comment
    if severity_id is not None:
        kwargs["SeverityId"] = severity_id
    if status_id is not None:
        kwargs["StatusId"] = status_id
    try:
        resp = await client.call("BatchUpdateFindingsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update findings v2") from exc
    return BatchUpdateFindingsV2Result(
        processed_findings=resp.get("ProcessedFindings"),
        unprocessed_findings=resp.get("UnprocessedFindings"),
    )


async def batch_update_standards_control_associations(
    standards_control_association_updates: list[dict[str, Any]],
    region_name: str | None = None,
) -> BatchUpdateStandardsControlAssociationsResult:
    """Batch update standards control associations.

    Args:
        standards_control_association_updates: Standards control association updates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StandardsControlAssociationUpdates"] = standards_control_association_updates
    try:
        resp = await client.call("BatchUpdateStandardsControlAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch update standards control associations") from exc
    return BatchUpdateStandardsControlAssociationsResult(
        unprocessed_association_updates=resp.get("UnprocessedAssociationUpdates"),
    )


async def connector_registrations_v2(
    auth_code: str,
    auth_state: str,
    region_name: str | None = None,
) -> ConnectorRegistrationsV2Result:
    """Connector registrations v2.

    Args:
        auth_code: Auth code.
        auth_state: Auth state.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthCode"] = auth_code
    kwargs["AuthState"] = auth_state
    try:
        resp = await client.call("ConnectorRegistrationsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to connector registrations v2") from exc
    return ConnectorRegistrationsV2Result(
        connector_arn=resp.get("ConnectorArn"),
        connector_id=resp.get("ConnectorId"),
    )


async def create_action_target(
    name: str,
    description: str,
    id: str,
    region_name: str | None = None,
) -> CreateActionTargetResult:
    """Create action target.

    Args:
        name: Name.
        description: Description.
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Description"] = description
    kwargs["Id"] = id
    try:
        resp = await client.call("CreateActionTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create action target") from exc
    return CreateActionTargetResult(
        action_target_arn=resp.get("ActionTargetArn"),
    )


async def create_aggregator_v2(
    region_linking_mode: str,
    *,
    linked_regions: list[str] | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateAggregatorV2Result:
    """Create aggregator v2.

    Args:
        region_linking_mode: Region linking mode.
        linked_regions: Linked regions.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegionLinkingMode"] = region_linking_mode
    if linked_regions is not None:
        kwargs["LinkedRegions"] = linked_regions
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("CreateAggregatorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create aggregator v2") from exc
    return CreateAggregatorV2Result(
        aggregator_v2_arn=resp.get("AggregatorV2Arn"),
        aggregation_region=resp.get("AggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        linked_regions=resp.get("LinkedRegions"),
    )


async def create_automation_rule(
    rule_order: int,
    rule_name: str,
    description: str,
    criteria: dict[str, Any],
    actions: list[dict[str, Any]],
    *,
    tags: dict[str, Any] | None = None,
    rule_status: str | None = None,
    is_terminal: bool | None = None,
    region_name: str | None = None,
) -> CreateAutomationRuleResult:
    """Create automation rule.

    Args:
        rule_order: Rule order.
        rule_name: Rule name.
        description: Description.
        criteria: Criteria.
        actions: Actions.
        tags: Tags.
        rule_status: Rule status.
        is_terminal: Is terminal.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleOrder"] = rule_order
    kwargs["RuleName"] = rule_name
    kwargs["Description"] = description
    kwargs["Criteria"] = criteria
    kwargs["Actions"] = actions
    if tags is not None:
        kwargs["Tags"] = tags
    if rule_status is not None:
        kwargs["RuleStatus"] = rule_status
    if is_terminal is not None:
        kwargs["IsTerminal"] = is_terminal
    try:
        resp = await client.call("CreateAutomationRule", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create automation rule") from exc
    return CreateAutomationRuleResult(
        rule_arn=resp.get("RuleArn"),
    )


async def create_automation_rule_v2(
    rule_name: str,
    description: str,
    rule_order: float,
    criteria: dict[str, Any],
    actions: list[dict[str, Any]],
    *,
    rule_status: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateAutomationRuleV2Result:
    """Create automation rule v2.

    Args:
        rule_name: Rule name.
        description: Description.
        rule_order: Rule order.
        criteria: Criteria.
        actions: Actions.
        rule_status: Rule status.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RuleName"] = rule_name
    kwargs["Description"] = description
    kwargs["RuleOrder"] = rule_order
    kwargs["Criteria"] = criteria
    kwargs["Actions"] = actions
    if rule_status is not None:
        kwargs["RuleStatus"] = rule_status
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("CreateAutomationRuleV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create automation rule v2") from exc
    return CreateAutomationRuleV2Result(
        rule_arn=resp.get("RuleArn"),
        rule_id=resp.get("RuleId"),
    )


async def create_configuration_policy(
    name: str,
    configuration_policy: dict[str, Any],
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateConfigurationPolicyResult:
    """Create configuration policy.

    Args:
        name: Name.
        configuration_policy: Configuration policy.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ConfigurationPolicy"] = configuration_policy
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateConfigurationPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create configuration policy") from exc
    return CreateConfigurationPolicyResult(
        arn=resp.get("Arn"),
        id=resp.get("Id"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        updated_at=resp.get("UpdatedAt"),
        created_at=resp.get("CreatedAt"),
        configuration_policy=resp.get("ConfigurationPolicy"),
    )


async def create_connector_v2(
    name: str,
    provider: dict[str, Any],
    *,
    description: str | None = None,
    kms_key_arn: str | None = None,
    tags: dict[str, Any] | None = None,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateConnectorV2Result:
    """Create connector v2.

    Args:
        name: Name.
        provider: Provider.
        description: Description.
        kms_key_arn: Kms key arn.
        tags: Tags.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Provider"] = provider
    if description is not None:
        kwargs["Description"] = description
    if kms_key_arn is not None:
        kwargs["KmsKeyArn"] = kms_key_arn
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("CreateConnectorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create connector v2") from exc
    return CreateConnectorV2Result(
        connector_arn=resp.get("ConnectorArn"),
        connector_id=resp.get("ConnectorId"),
        auth_url=resp.get("AuthUrl"),
    )


async def create_finding_aggregator(
    region_linking_mode: str,
    *,
    regions: list[str] | None = None,
    region_name: str | None = None,
) -> CreateFindingAggregatorResult:
    """Create finding aggregator.

    Args:
        region_linking_mode: Region linking mode.
        regions: Regions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegionLinkingMode"] = region_linking_mode
    if regions is not None:
        kwargs["Regions"] = regions
    try:
        resp = await client.call("CreateFindingAggregator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create finding aggregator") from exc
    return CreateFindingAggregatorResult(
        finding_aggregator_arn=resp.get("FindingAggregatorArn"),
        finding_aggregation_region=resp.get("FindingAggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        regions=resp.get("Regions"),
    )


async def create_ticket_v2(
    connector_id: str,
    finding_metadata_uid: str,
    *,
    client_token: str | None = None,
    region_name: str | None = None,
) -> CreateTicketV2Result:
    """Create ticket v2.

    Args:
        connector_id: Connector id.
        finding_metadata_uid: Finding metadata uid.
        client_token: Client token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    kwargs["FindingMetadataUid"] = finding_metadata_uid
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = await client.call("CreateTicketV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create ticket v2") from exc
    return CreateTicketV2Result(
        ticket_id=resp.get("TicketId"),
        ticket_src_url=resp.get("TicketSrcUrl"),
    )


async def decline_invitations(
    account_ids: list[str],
    region_name: str | None = None,
) -> DeclineInvitationsResult:
    """Decline invitations.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountIds"] = account_ids
    try:
        resp = await client.call("DeclineInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to decline invitations") from exc
    return DeclineInvitationsResult(
        unprocessed_accounts=resp.get("UnprocessedAccounts"),
    )


async def delete_action_target(
    action_target_arn: str,
    region_name: str | None = None,
) -> DeleteActionTargetResult:
    """Delete action target.

    Args:
        action_target_arn: Action target arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionTargetArn"] = action_target_arn
    try:
        resp = await client.call("DeleteActionTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete action target") from exc
    return DeleteActionTargetResult(
        action_target_arn=resp.get("ActionTargetArn"),
    )


async def delete_aggregator_v2(
    aggregator_v2_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete aggregator v2.

    Args:
        aggregator_v2_arn: Aggregator v2 arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AggregatorV2Arn"] = aggregator_v2_arn
    try:
        await client.call("DeleteAggregatorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete aggregator v2") from exc
    return None


async def delete_automation_rule_v2(
    identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete automation rule v2.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        await client.call("DeleteAutomationRuleV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete automation rule v2") from exc
    return None


async def delete_configuration_policy(
    identifier: str,
    region_name: str | None = None,
) -> None:
    """Delete configuration policy.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        await client.call("DeleteConfigurationPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration policy") from exc
    return None


async def delete_connector_v2(
    connector_id: str,
    region_name: str | None = None,
) -> None:
    """Delete connector v2.

    Args:
        connector_id: Connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        await client.call("DeleteConnectorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete connector v2") from exc
    return None


async def delete_finding_aggregator(
    finding_aggregator_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete finding aggregator.

    Args:
        finding_aggregator_arn: Finding aggregator arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingAggregatorArn"] = finding_aggregator_arn
    try:
        await client.call("DeleteFindingAggregator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete finding aggregator") from exc
    return None


async def delete_invitations(
    account_ids: list[str],
    region_name: str | None = None,
) -> DeleteInvitationsResult:
    """Delete invitations.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountIds"] = account_ids
    try:
        resp = await client.call("DeleteInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete invitations") from exc
    return DeleteInvitationsResult(
        unprocessed_accounts=resp.get("UnprocessedAccounts"),
    )


async def describe_action_targets(
    *,
    action_target_arns: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeActionTargetsResult:
    """Describe action targets.

    Args:
        action_target_arns: Action target arns.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if action_target_arns is not None:
        kwargs["ActionTargetArns"] = action_target_arns
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeActionTargets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe action targets") from exc
    return DescribeActionTargetsResult(
        action_targets=resp.get("ActionTargets"),
        next_token=resp.get("NextToken"),
    )


async def describe_organization_configuration(
    region_name: str | None = None,
) -> DescribeOrganizationConfigurationResult:
    """Describe organization configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe organization configuration") from exc
    return DescribeOrganizationConfigurationResult(
        auto_enable=resp.get("AutoEnable"),
        member_account_limit_reached=resp.get("MemberAccountLimitReached"),
        auto_enable_standards=resp.get("AutoEnableStandards"),
        organization_configuration=resp.get("OrganizationConfiguration"),
    )


async def describe_products(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    product_arn: str | None = None,
    region_name: str | None = None,
) -> DescribeProductsResult:
    """Describe products.

    Args:
        next_token: Next token.
        max_results: Max results.
        product_arn: Product arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if product_arn is not None:
        kwargs["ProductArn"] = product_arn
    try:
        resp = await client.call("DescribeProducts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe products") from exc
    return DescribeProductsResult(
        products=resp.get("Products"),
        next_token=resp.get("NextToken"),
    )


async def describe_products_v2(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> DescribeProductsV2Result:
    """Describe products v2.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("DescribeProductsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe products v2") from exc
    return DescribeProductsV2Result(
        products_v2=resp.get("ProductsV2"),
        next_token=resp.get("NextToken"),
    )


async def describe_security_hub_v2(
    region_name: str | None = None,
) -> DescribeSecurityHubV2Result:
    """Describe security hub v2.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeSecurityHubV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe security hub v2") from exc
    return DescribeSecurityHubV2Result(
        hub_v2_arn=resp.get("HubV2Arn"),
        subscribed_at=resp.get("SubscribedAt"),
    )


async def disable_organization_admin_account(
    admin_account_id: str,
    *,
    feature: str | None = None,
    region_name: str | None = None,
) -> None:
    """Disable organization admin account.

    Args:
        admin_account_id: Admin account id.
        feature: Feature.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdminAccountId"] = admin_account_id
    if feature is not None:
        kwargs["Feature"] = feature
    try:
        await client.call("DisableOrganizationAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable organization admin account") from exc
    return None


async def disable_security_hub_v2(
    region_name: str | None = None,
) -> None:
    """Disable security hub v2.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisableSecurityHubV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable security hub v2") from exc
    return None


async def disassociate_from_administrator_account(
    region_name: str | None = None,
) -> None:
    """Disassociate from administrator account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisassociateFromAdministratorAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate from administrator account") from exc
    return None


async def disassociate_from_master_account(
    region_name: str | None = None,
) -> None:
    """Disassociate from master account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        await client.call("DisassociateFromMasterAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate from master account") from exc
    return None


async def disassociate_members(
    account_ids: list[str],
    region_name: str | None = None,
) -> None:
    """Disassociate members.

    Args:
        account_ids: Account ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountIds"] = account_ids
    try:
        await client.call("DisassociateMembers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate members") from exc
    return None


async def enable_organization_admin_account(
    admin_account_id: str,
    *,
    feature: str | None = None,
    region_name: str | None = None,
) -> EnableOrganizationAdminAccountResult:
    """Enable organization admin account.

    Args:
        admin_account_id: Admin account id.
        feature: Feature.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdminAccountId"] = admin_account_id
    if feature is not None:
        kwargs["Feature"] = feature
    try:
        resp = await client.call("EnableOrganizationAdminAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable organization admin account") from exc
    return EnableOrganizationAdminAccountResult(
        admin_account_id=resp.get("AdminAccountId"),
        feature=resp.get("Feature"),
    )


async def enable_security_hub_v2(
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> EnableSecurityHubV2Result:
    """Enable security hub v2.

    Args:
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("EnableSecurityHubV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable security hub v2") from exc
    return EnableSecurityHubV2Result(
        hub_v2_arn=resp.get("HubV2Arn"),
    )


async def get_aggregator_v2(
    aggregator_v2_arn: str,
    region_name: str | None = None,
) -> GetAggregatorV2Result:
    """Get aggregator v2.

    Args:
        aggregator_v2_arn: Aggregator v2 arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AggregatorV2Arn"] = aggregator_v2_arn
    try:
        resp = await client.call("GetAggregatorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get aggregator v2") from exc
    return GetAggregatorV2Result(
        aggregator_v2_arn=resp.get("AggregatorV2Arn"),
        aggregation_region=resp.get("AggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        linked_regions=resp.get("LinkedRegions"),
    )


async def get_automation_rule_v2(
    identifier: str,
    region_name: str | None = None,
) -> GetAutomationRuleV2Result:
    """Get automation rule v2.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = await client.call("GetAutomationRuleV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get automation rule v2") from exc
    return GetAutomationRuleV2Result(
        rule_arn=resp.get("RuleArn"),
        rule_id=resp.get("RuleId"),
        rule_order=resp.get("RuleOrder"),
        rule_name=resp.get("RuleName"),
        rule_status=resp.get("RuleStatus"),
        description=resp.get("Description"),
        criteria=resp.get("Criteria"),
        actions=resp.get("Actions"),
        created_at=resp.get("CreatedAt"),
        updated_at=resp.get("UpdatedAt"),
    )


async def get_configuration_policy(
    identifier: str,
    region_name: str | None = None,
) -> GetConfigurationPolicyResult:
    """Get configuration policy.

    Args:
        identifier: Identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = await client.call("GetConfigurationPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get configuration policy") from exc
    return GetConfigurationPolicyResult(
        arn=resp.get("Arn"),
        id=resp.get("Id"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        updated_at=resp.get("UpdatedAt"),
        created_at=resp.get("CreatedAt"),
        configuration_policy=resp.get("ConfigurationPolicy"),
    )


async def get_configuration_policy_association(
    target: dict[str, Any],
    region_name: str | None = None,
) -> GetConfigurationPolicyAssociationResult:
    """Get configuration policy association.

    Args:
        target: Target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Target"] = target
    try:
        resp = await client.call("GetConfigurationPolicyAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get configuration policy association") from exc
    return GetConfigurationPolicyAssociationResult(
        configuration_policy_id=resp.get("ConfigurationPolicyId"),
        target_id=resp.get("TargetId"),
        target_type=resp.get("TargetType"),
        association_type=resp.get("AssociationType"),
        updated_at=resp.get("UpdatedAt"),
        association_status=resp.get("AssociationStatus"),
        association_status_message=resp.get("AssociationStatusMessage"),
    )


async def get_connector_v2(
    connector_id: str,
    region_name: str | None = None,
) -> GetConnectorV2Result:
    """Get connector v2.

    Args:
        connector_id: Connector id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        resp = await client.call("GetConnectorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get connector v2") from exc
    return GetConnectorV2Result(
        connector_arn=resp.get("ConnectorArn"),
        connector_id=resp.get("ConnectorId"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        kms_key_arn=resp.get("KmsKeyArn"),
        created_at=resp.get("CreatedAt"),
        last_updated_at=resp.get("LastUpdatedAt"),
        health=resp.get("Health"),
        provider_detail=resp.get("ProviderDetail"),
    )


async def get_finding_aggregator(
    finding_aggregator_arn: str,
    region_name: str | None = None,
) -> GetFindingAggregatorResult:
    """Get finding aggregator.

    Args:
        finding_aggregator_arn: Finding aggregator arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingAggregatorArn"] = finding_aggregator_arn
    try:
        resp = await client.call("GetFindingAggregator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get finding aggregator") from exc
    return GetFindingAggregatorResult(
        finding_aggregator_arn=resp.get("FindingAggregatorArn"),
        finding_aggregation_region=resp.get("FindingAggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        regions=resp.get("Regions"),
    )


async def get_finding_history(
    finding_identifier: dict[str, Any],
    *,
    start_time: str | None = None,
    end_time: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetFindingHistoryResult:
    """Get finding history.

    Args:
        finding_identifier: Finding identifier.
        start_time: Start time.
        end_time: End time.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingIdentifier"] = finding_identifier
    if start_time is not None:
        kwargs["StartTime"] = start_time
    if end_time is not None:
        kwargs["EndTime"] = end_time
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetFindingHistory", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get finding history") from exc
    return GetFindingHistoryResult(
        records=resp.get("Records"),
        next_token=resp.get("NextToken"),
    )


async def get_finding_statistics_v2(
    group_by_rules: list[dict[str, Any]],
    *,
    sort_order: str | None = None,
    max_statistic_results: int | None = None,
    region_name: str | None = None,
) -> GetFindingStatisticsV2Result:
    """Get finding statistics v2.

    Args:
        group_by_rules: Group by rules.
        sort_order: Sort order.
        max_statistic_results: Max statistic results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupByRules"] = group_by_rules
    if sort_order is not None:
        kwargs["SortOrder"] = sort_order
    if max_statistic_results is not None:
        kwargs["MaxStatisticResults"] = max_statistic_results
    try:
        resp = await client.call("GetFindingStatisticsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get finding statistics v2") from exc
    return GetFindingStatisticsV2Result(
        group_by_results=resp.get("GroupByResults"),
    )


async def get_findings_v2(
    *,
    filters: dict[str, Any] | None = None,
    sort_criteria: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetFindingsV2Result:
    """Get findings v2.

    Args:
        filters: Filters.
        sort_criteria: Sort criteria.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if sort_criteria is not None:
        kwargs["SortCriteria"] = sort_criteria
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetFindingsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get findings v2") from exc
    return GetFindingsV2Result(
        findings=resp.get("Findings"),
        next_token=resp.get("NextToken"),
    )


async def get_insights(
    *,
    insight_arns: list[str] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetInsightsResult:
    """Get insights.

    Args:
        insight_arns: Insight arns.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if insight_arns is not None:
        kwargs["InsightArns"] = insight_arns
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetInsights", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get insights") from exc
    return GetInsightsResult(
        insights=resp.get("Insights"),
        next_token=resp.get("NextToken"),
    )


async def get_invitations_count(
    region_name: str | None = None,
) -> GetInvitationsCountResult:
    """Get invitations count.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetInvitationsCount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get invitations count") from exc
    return GetInvitationsCountResult(
        invitations_count=resp.get("InvitationsCount"),
    )


async def get_master_account(
    region_name: str | None = None,
) -> GetMasterAccountResult:
    """Get master account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("GetMasterAccount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get master account") from exc
    return GetMasterAccountResult(
        master=resp.get("Master"),
    )


async def get_resources_statistics_v2(
    group_by_rules: list[dict[str, Any]],
    *,
    sort_order: str | None = None,
    max_statistic_results: int | None = None,
    region_name: str | None = None,
) -> GetResourcesStatisticsV2Result:
    """Get resources statistics v2.

    Args:
        group_by_rules: Group by rules.
        sort_order: Sort order.
        max_statistic_results: Max statistic results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupByRules"] = group_by_rules
    if sort_order is not None:
        kwargs["SortOrder"] = sort_order
    if max_statistic_results is not None:
        kwargs["MaxStatisticResults"] = max_statistic_results
    try:
        resp = await client.call("GetResourcesStatisticsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resources statistics v2") from exc
    return GetResourcesStatisticsV2Result(
        group_by_results=resp.get("GroupByResults"),
    )


async def get_resources_v2(
    *,
    filters: dict[str, Any] | None = None,
    sort_criteria: list[dict[str, Any]] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> GetResourcesV2Result:
    """Get resources v2.

    Args:
        filters: Filters.
        sort_criteria: Sort criteria.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if filters is not None:
        kwargs["Filters"] = filters
    if sort_criteria is not None:
        kwargs["SortCriteria"] = sort_criteria
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("GetResourcesV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resources v2") from exc
    return GetResourcesV2Result(
        resources=resp.get("Resources"),
        next_token=resp.get("NextToken"),
    )


async def get_security_control_definition(
    security_control_id: str,
    region_name: str | None = None,
) -> GetSecurityControlDefinitionResult:
    """Get security control definition.

    Args:
        security_control_id: Security control id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlId"] = security_control_id
    try:
        resp = await client.call("GetSecurityControlDefinition", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get security control definition") from exc
    return GetSecurityControlDefinitionResult(
        security_control_definition=resp.get("SecurityControlDefinition"),
    )


async def list_aggregators_v2(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAggregatorsV2Result:
    """List aggregators v2.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListAggregatorsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list aggregators v2") from exc
    return ListAggregatorsV2Result(
        aggregators_v2=resp.get("AggregatorsV2"),
        next_token=resp.get("NextToken"),
    )


async def list_automation_rules(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAutomationRulesResult:
    """List automation rules.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListAutomationRules", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list automation rules") from exc
    return ListAutomationRulesResult(
        automation_rules_metadata=resp.get("AutomationRulesMetadata"),
        next_token=resp.get("NextToken"),
    )


async def list_automation_rules_v2(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListAutomationRulesV2Result:
    """List automation rules v2.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListAutomationRulesV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list automation rules v2") from exc
    return ListAutomationRulesV2Result(
        rules=resp.get("Rules"),
        next_token=resp.get("NextToken"),
    )


async def list_configuration_policies(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListConfigurationPoliciesResult:
    """List configuration policies.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListConfigurationPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list configuration policies") from exc
    return ListConfigurationPoliciesResult(
        configuration_policy_summaries=resp.get("ConfigurationPolicySummaries"),
        next_token=resp.get("NextToken"),
    )


async def list_configuration_policy_associations(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    filters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ListConfigurationPolicyAssociationsResult:
    """List configuration policy associations.

    Args:
        next_token: Next token.
        max_results: Max results.
        filters: Filters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = await client.call("ListConfigurationPolicyAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list configuration policy associations") from exc
    return ListConfigurationPolicyAssociationsResult(
        configuration_policy_association_summaries=resp.get(
            "ConfigurationPolicyAssociationSummaries"
        ),
        next_token=resp.get("NextToken"),
    )


async def list_connectors_v2(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    provider_name: str | None = None,
    connector_status: str | None = None,
    region_name: str | None = None,
) -> ListConnectorsV2Result:
    """List connectors v2.

    Args:
        next_token: Next token.
        max_results: Max results.
        provider_name: Provider name.
        connector_status: Connector status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if provider_name is not None:
        kwargs["ProviderName"] = provider_name
    if connector_status is not None:
        kwargs["ConnectorStatus"] = connector_status
    try:
        resp = await client.call("ListConnectorsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list connectors v2") from exc
    return ListConnectorsV2Result(
        next_token=resp.get("NextToken"),
        connectors=resp.get("Connectors"),
    )


async def list_finding_aggregators(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListFindingAggregatorsResult:
    """List finding aggregators.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListFindingAggregators", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list finding aggregators") from exc
    return ListFindingAggregatorsResult(
        finding_aggregators=resp.get("FindingAggregators"),
        next_token=resp.get("NextToken"),
    )


async def list_invitations(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListInvitationsResult:
    """List invitations.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListInvitations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list invitations") from exc
    return ListInvitationsResult(
        invitations=resp.get("Invitations"),
        next_token=resp.get("NextToken"),
    )


async def list_organization_admin_accounts(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    feature: str | None = None,
    region_name: str | None = None,
) -> ListOrganizationAdminAccountsResult:
    """List organization admin accounts.

    Args:
        max_results: Max results.
        next_token: Next token.
        feature: Feature.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if feature is not None:
        kwargs["Feature"] = feature
    try:
        resp = await client.call("ListOrganizationAdminAccounts", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list organization admin accounts") from exc
    return ListOrganizationAdminAccountsResult(
        admin_accounts=resp.get("AdminAccounts"),
        next_token=resp.get("NextToken"),
        feature=resp.get("Feature"),
    )


async def list_security_control_definitions(
    *,
    standards_arn: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListSecurityControlDefinitionsResult:
    """List security control definitions.

    Args:
        standards_arn: Standards arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if standards_arn is not None:
        kwargs["StandardsArn"] = standards_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListSecurityControlDefinitions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list security control definitions") from exc
    return ListSecurityControlDefinitionsResult(
        security_control_definitions=resp.get("SecurityControlDefinitions"),
        next_token=resp.get("NextToken"),
    )


async def list_standards_control_associations(
    security_control_id: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListStandardsControlAssociationsResult:
    """List standards control associations.

    Args:
        security_control_id: Security control id.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlId"] = security_control_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListStandardsControlAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list standards control associations") from exc
    return ListStandardsControlAssociationsResult(
        standards_control_association_summaries=resp.get("StandardsControlAssociationSummaries"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
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
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def start_configuration_policy_association(
    configuration_policy_identifier: str,
    target: dict[str, Any],
    region_name: str | None = None,
) -> StartConfigurationPolicyAssociationResult:
    """Start configuration policy association.

    Args:
        configuration_policy_identifier: Configuration policy identifier.
        target: Target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationPolicyIdentifier"] = configuration_policy_identifier
    kwargs["Target"] = target
    try:
        resp = await client.call("StartConfigurationPolicyAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start configuration policy association") from exc
    return StartConfigurationPolicyAssociationResult(
        configuration_policy_id=resp.get("ConfigurationPolicyId"),
        target_id=resp.get("TargetId"),
        target_type=resp.get("TargetType"),
        association_type=resp.get("AssociationType"),
        updated_at=resp.get("UpdatedAt"),
        association_status=resp.get("AssociationStatus"),
        association_status_message=resp.get("AssociationStatusMessage"),
    )


async def start_configuration_policy_disassociation(
    configuration_policy_identifier: str,
    *,
    target: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Start configuration policy disassociation.

    Args:
        configuration_policy_identifier: Configuration policy identifier.
        target: Target.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationPolicyIdentifier"] = configuration_policy_identifier
    if target is not None:
        kwargs["Target"] = target
    try:
        await client.call("StartConfigurationPolicyDisassociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start configuration policy disassociation") from exc
    return None


async def tag_resource(
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
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


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
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_action_target(
    action_target_arn: str,
    *,
    name: str | None = None,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update action target.

    Args:
        action_target_arn: Action target arn.
        name: Name.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionTargetArn"] = action_target_arn
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        await client.call("UpdateActionTarget", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update action target") from exc
    return None


async def update_aggregator_v2(
    aggregator_v2_arn: str,
    region_linking_mode: str,
    *,
    linked_regions: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateAggregatorV2Result:
    """Update aggregator v2.

    Args:
        aggregator_v2_arn: Aggregator v2 arn.
        region_linking_mode: Region linking mode.
        linked_regions: Linked regions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AggregatorV2Arn"] = aggregator_v2_arn
    kwargs["RegionLinkingMode"] = region_linking_mode
    if linked_regions is not None:
        kwargs["LinkedRegions"] = linked_regions
    try:
        resp = await client.call("UpdateAggregatorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update aggregator v2") from exc
    return UpdateAggregatorV2Result(
        aggregator_v2_arn=resp.get("AggregatorV2Arn"),
        aggregation_region=resp.get("AggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        linked_regions=resp.get("LinkedRegions"),
    )


async def update_automation_rule_v2(
    identifier: str,
    *,
    rule_status: str | None = None,
    rule_order: float | None = None,
    description: str | None = None,
    rule_name: str | None = None,
    criteria: dict[str, Any] | None = None,
    actions: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Update automation rule v2.

    Args:
        identifier: Identifier.
        rule_status: Rule status.
        rule_order: Rule order.
        description: Description.
        rule_name: Rule name.
        criteria: Criteria.
        actions: Actions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    if rule_status is not None:
        kwargs["RuleStatus"] = rule_status
    if rule_order is not None:
        kwargs["RuleOrder"] = rule_order
    if description is not None:
        kwargs["Description"] = description
    if rule_name is not None:
        kwargs["RuleName"] = rule_name
    if criteria is not None:
        kwargs["Criteria"] = criteria
    if actions is not None:
        kwargs["Actions"] = actions
    try:
        await client.call("UpdateAutomationRuleV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update automation rule v2") from exc
    return None


async def update_configuration_policy(
    identifier: str,
    *,
    name: str | None = None,
    description: str | None = None,
    updated_reason: str | None = None,
    configuration_policy: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateConfigurationPolicyResult:
    """Update configuration policy.

    Args:
        identifier: Identifier.
        name: Name.
        description: Description.
        updated_reason: Updated reason.
        configuration_policy: Configuration policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    if updated_reason is not None:
        kwargs["UpdatedReason"] = updated_reason
    if configuration_policy is not None:
        kwargs["ConfigurationPolicy"] = configuration_policy
    try:
        resp = await client.call("UpdateConfigurationPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update configuration policy") from exc
    return UpdateConfigurationPolicyResult(
        arn=resp.get("Arn"),
        id=resp.get("Id"),
        name=resp.get("Name"),
        description=resp.get("Description"),
        updated_at=resp.get("UpdatedAt"),
        created_at=resp.get("CreatedAt"),
        configuration_policy=resp.get("ConfigurationPolicy"),
    )


async def update_connector_v2(
    connector_id: str,
    *,
    client_secret: str | None = None,
    description: str | None = None,
    provider: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update connector v2.

    Args:
        connector_id: Connector id.
        client_secret: Client secret.
        description: Description.
        provider: Provider.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    if client_secret is not None:
        kwargs["ClientSecret"] = client_secret
    if description is not None:
        kwargs["Description"] = description
    if provider is not None:
        kwargs["Provider"] = provider
    try:
        await client.call("UpdateConnectorV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update connector v2") from exc
    return None


async def update_finding_aggregator(
    finding_aggregator_arn: str,
    region_linking_mode: str,
    *,
    regions: list[str] | None = None,
    region_name: str | None = None,
) -> UpdateFindingAggregatorResult:
    """Update finding aggregator.

    Args:
        finding_aggregator_arn: Finding aggregator arn.
        region_linking_mode: Region linking mode.
        regions: Regions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingAggregatorArn"] = finding_aggregator_arn
    kwargs["RegionLinkingMode"] = region_linking_mode
    if regions is not None:
        kwargs["Regions"] = regions
    try:
        resp = await client.call("UpdateFindingAggregator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update finding aggregator") from exc
    return UpdateFindingAggregatorResult(
        finding_aggregator_arn=resp.get("FindingAggregatorArn"),
        finding_aggregation_region=resp.get("FindingAggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        regions=resp.get("Regions"),
    )


async def update_organization_configuration(
    auto_enable: bool,
    *,
    auto_enable_standards: str | None = None,
    organization_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update organization configuration.

    Args:
        auto_enable: Auto enable.
        auto_enable_standards: Auto enable standards.
        organization_configuration: Organization configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoEnable"] = auto_enable
    if auto_enable_standards is not None:
        kwargs["AutoEnableStandards"] = auto_enable_standards
    if organization_configuration is not None:
        kwargs["OrganizationConfiguration"] = organization_configuration
    try:
        await client.call("UpdateOrganizationConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update organization configuration") from exc
    return None


async def update_security_control(
    security_control_id: str,
    parameters: dict[str, Any],
    *,
    last_update_reason: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update security control.

    Args:
        security_control_id: Security control id.
        parameters: Parameters.
        last_update_reason: Last update reason.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlId"] = security_control_id
    kwargs["Parameters"] = parameters
    if last_update_reason is not None:
        kwargs["LastUpdateReason"] = last_update_reason
    try:
        await client.call("UpdateSecurityControl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update security control") from exc
    return None


async def update_security_hub_configuration(
    *,
    auto_enable_controls: bool | None = None,
    control_finding_generator: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update security hub configuration.

    Args:
        auto_enable_controls: Auto enable controls.
        control_finding_generator: Control finding generator.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if auto_enable_controls is not None:
        kwargs["AutoEnableControls"] = auto_enable_controls
    if control_finding_generator is not None:
        kwargs["ControlFindingGenerator"] = control_finding_generator
    try:
        await client.call("UpdateSecurityHubConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update security hub configuration") from exc
    return None
