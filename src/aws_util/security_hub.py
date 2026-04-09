"""aws_util.security_hub --- AWS Security Hub utilities.

Provides functions for managing AWS Security Hub: enabling/disabling the hub,
managing findings, insights, standards, product integrations, and member
accounts.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

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
# Models
# ---------------------------------------------------------------------------


class HubResult(BaseModel):
    """Metadata for an AWS Security Hub instance."""

    model_config = ConfigDict(frozen=True)

    hub_arn: str | None = None
    subscribed_at: str | None = None
    auto_enable_controls: bool = True
    extra: dict[str, Any] = {}


class FindingResult(BaseModel):
    """A Security Hub finding."""

    model_config = ConfigDict(frozen=True)

    finding_id: str = ""
    product_arn: str = ""
    generator_id: str = ""
    aws_account_id: str = ""
    title: str = ""
    description: str = ""
    severity_label: str = ""
    workflow_status: str = ""
    record_state: str = ""
    extra: dict[str, Any] = {}


class InsightResult(BaseModel):
    """A Security Hub insight."""

    model_config = ConfigDict(frozen=True)

    insight_arn: str = ""
    name: str = ""
    filters: dict[str, Any] = {}
    group_by_attribute: str = ""
    extra: dict[str, Any] = {}


class StandardResult(BaseModel):
    """A Security Hub standard or standards subscription."""

    model_config = ConfigDict(frozen=True)

    standards_arn: str | None = None
    standards_subscription_arn: str | None = None
    standards_status: str | None = None
    name: str = ""
    description: str = ""
    extra: dict[str, Any] = {}


class MemberResult(BaseModel):
    """A Security Hub member account."""

    model_config = ConfigDict(frozen=True)

    account_id: str = ""
    email: str = ""
    member_status: str = ""
    invited_at: str | None = None
    updated_at: str | None = None
    administrator_id: str | None = None
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Hub management
# ---------------------------------------------------------------------------


def enable_security_hub(
    *,
    enable_default_standards: bool = True,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> str:
    """Enable AWS Security Hub in the account.

    Args:
        enable_default_standards: Whether to enable the default
            standards (e.g. CIS, PCI DSS).
        tags: Optional tags for the hub resource.
        region_name: AWS region override.

    Returns:
        The hub ARN.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {
        "EnableDefaultStandards": enable_default_standards,
    }
    if tags:
        kwargs["Tags"] = tags
    try:
        resp = client.enable_security_hub(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "enable_security_hub failed") from exc
    return resp.get("HubArn", "")


def disable_security_hub(
    *,
    region_name: str | None = None,
) -> None:
    """Disable AWS Security Hub in the account.

    Args:
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    try:
        client.disable_security_hub()
    except ClientError as exc:
        raise wrap_aws_error(exc, "disable_security_hub failed") from exc


def describe_hub(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if hub_arn:
        kwargs["HubArn"] = hub_arn
    try:
        resp = client.describe_hub(**kwargs)
    except ClientError as exc:
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


def _parse_finding(f: dict[str, Any]) -> FindingResult:
    """Parse a raw finding dict into a :class:`FindingResult`."""
    severity = f.get("Severity", {})
    workflow = f.get("Workflow", {})
    return FindingResult(
        finding_id=f.get("Id", ""),
        product_arn=f.get("ProductArn", ""),
        generator_id=f.get("GeneratorId", ""),
        aws_account_id=f.get("AwsAccountId", ""),
        title=f.get("Title", ""),
        description=f.get("Description", ""),
        severity_label=severity.get("Label", ""),
        workflow_status=workflow.get("Status", ""),
        record_state=f.get("RecordState", ""),
        extra={
            k: v
            for k, v in f.items()
            if k
            not in {
                "Id",
                "ProductArn",
                "GeneratorId",
                "AwsAccountId",
                "Title",
                "Description",
                "Severity",
                "Workflow",
                "RecordState",
            }
        },
    )


def get_findings(
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
        max_results: Maximum number of findings to return per page.
        region_name: AWS region override.

    Returns:
        A list of :class:`FindingResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if filters:
        kwargs["Filters"] = filters
    if sort_criteria:
        kwargs["SortCriteria"] = sort_criteria
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[FindingResult] = []
    try:
        paginator = client.get_paginator("get_findings")
        for page in paginator.paginate(**kwargs):
            for f in page.get("Findings", []):
                results.append(_parse_finding(f))
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_findings failed") from exc
    return results


def update_findings(
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
        note: Optional note to attach (``Text`` and ``UpdatedBy``).
        severity: Optional severity update dict.
        workflow: Optional workflow status update dict.
        region_name: AWS region override.

    Returns:
        A dict with ``ProcessedFindings`` and ``UnprocessedFindings``.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
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
        resp = client.batch_update_findings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_findings failed") from exc
    return {
        "ProcessedFindings": resp.get("ProcessedFindings", []),
        "UnprocessedFindings": resp.get("UnprocessedFindings", []),
    }


# ---------------------------------------------------------------------------
# Insights
# ---------------------------------------------------------------------------


def get_insight_results(
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
    client = get_client("securityhub", region_name)
    try:
        resp = client.get_insight_results(InsightArn=insight_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_insight_results failed for {insight_arn!r}") from exc
    return resp.get("InsightResults", {})


def list_insights(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    results: list[InsightResult] = []
    try:
        paginator = client.get_paginator("get_insights")
        for page in paginator.paginate(**kwargs):
            for insight in page.get("Insights", []):
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
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_insights failed") from exc
    return results


def create_insight(
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
    client = get_client("securityhub", region_name)
    try:
        resp = client.create_insight(
            Name=name,
            Filters=filters,
            GroupByAttribute=group_by_attribute,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_insight failed for {name!r}") from exc
    return resp.get("InsightArn", "")


def update_insight(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {"InsightArn": insight_arn}
    if name is not None:
        kwargs["Name"] = name
    if filters is not None:
        kwargs["Filters"] = filters
    if group_by_attribute is not None:
        kwargs["GroupByAttribute"] = group_by_attribute
    try:
        client.update_insight(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_insight failed for {insight_arn!r}") from exc


def delete_insight(
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
    client = get_client("securityhub", region_name)
    try:
        client.delete_insight(InsightArn=insight_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_insight failed for {insight_arn!r}") from exc


# ---------------------------------------------------------------------------
# Product integrations
# ---------------------------------------------------------------------------


def enable_import_findings_for_product(
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
    client = get_client("securityhub", region_name)
    try:
        resp = client.enable_import_findings_for_product(
            ProductArn=product_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"enable_import_findings_for_product failed for {product_arn!r}",
        ) from exc
    return resp.get("ProductSubscriptionArn", "")


def disable_import_findings_for_product(
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
    client = get_client("securityhub", region_name)
    try:
        client.disable_import_findings_for_product(
            ProductSubscriptionArn=product_subscription_arn,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"disable_import_findings_for_product failed for {product_subscription_arn!r}",
        ) from exc


def list_enabled_products_for_import(
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
    client = get_client("securityhub", region_name)
    arns: list[str] = []
    try:
        token: str | None = None
        while True:
            kwargs: dict[str, Any] = {}
            if token:
                kwargs["NextToken"] = token
            resp = client.list_enabled_products_for_import(**kwargs)
            arns.extend(resp.get("ProductSubscriptions", []))
            token = resp.get("NextToken")
            if not token:
                break
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_enabled_products_for_import failed") from exc
    return arns


# ---------------------------------------------------------------------------
# Standards
# ---------------------------------------------------------------------------


def get_enabled_standards(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if standards_subscription_arns:
        kwargs["StandardsSubscriptionArns"] = standards_subscription_arns
    results: list[StandardResult] = []
    try:
        paginator = client.get_paginator("get_enabled_standards")
        for page in paginator.paginate(**kwargs):
            for std in page.get("StandardsSubscriptions", []):
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
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_enabled_standards failed") from exc
    return results


def batch_enable_standards(
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
    client = get_client("securityhub", region_name)
    try:
        resp = client.batch_enable_standards(
            StandardsSubscriptionRequests=(standards_subscription_requests),
        )
    except ClientError as exc:
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


def batch_disable_standards(
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
    client = get_client("securityhub", region_name)
    try:
        client.batch_disable_standards(
            StandardsSubscriptionArns=standards_subscription_arns,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "batch_disable_standards failed") from exc


def describe_standards(
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
    client = get_client("securityhub", region_name)
    results: list[StandardResult] = []
    try:
        paginator = client.get_paginator("describe_standards")
        for page in paginator.paginate():
            for std in page.get("Standards", []):
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
    except ClientError as exc:
        raise wrap_aws_error(exc, "describe_standards failed") from exc
    return results


def describe_standards_controls(
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
    client = get_client("securityhub", region_name)
    results: list[dict[str, Any]] = []
    try:
        paginator = client.get_paginator("describe_standards_controls")
        for page in paginator.paginate(
            StandardsSubscriptionArn=standards_subscription_arn,
        ):
            results.extend(page.get("Controls", []))
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_standards_controls failed for {standards_subscription_arn!r}",
        ) from exc
    return results


def update_standards_control(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {
        "StandardsControlArn": standards_control_arn,
        "ControlStatus": control_status,
    }
    if disabled_reason is not None:
        kwargs["DisabledReason"] = disabled_reason
    try:
        client.update_standards_control(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"update_standards_control failed for {standards_control_arn!r}",
        ) from exc


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------


def invite_members(
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Invite member accounts to Security Hub.

    Args:
        account_ids: List of AWS account IDs to invite.
        region_name: AWS region override.

    Returns:
        A list of unprocessed account dicts (empty on full success).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    try:
        resp = client.invite_members(AccountIds=account_ids)
    except ClientError as exc:
        raise wrap_aws_error(exc, "invite_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


def list_members(
    *,
    only_associated: bool = True,
    region_name: str | None = None,
) -> list[MemberResult]:
    """List Security Hub member accounts.

    Args:
        only_associated: If ``True``, only return associated members.
        region_name: AWS region override.

    Returns:
        A list of :class:`MemberResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    results: list[MemberResult] = []
    try:
        paginator = client.get_paginator("list_members")
        for page in paginator.paginate(
            OnlyAssociated=only_associated,
        ):
            for m in page.get("Members", []):
                results.append(_parse_member(m))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_members failed") from exc
    return results


def get_members(
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
    client = get_client("securityhub", region_name)
    try:
        resp = client.get_members(AccountIds=account_ids)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_members failed") from exc
    return [_parse_member(m) for m in resp.get("Members", [])]


def create_members(
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
        A list of unprocessed account dicts (empty on full success).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    try:
        resp = client.create_members(AccountDetails=account_details)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


def delete_members(
    account_ids: list[str],
    *,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Delete member account associations.

    Args:
        account_ids: List of AWS account IDs to remove.
        region_name: AWS region override.

    Returns:
        A list of unprocessed account dicts (empty on full success).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    try:
        resp = client.delete_members(AccountIds=account_ids)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_members failed") from exc
    return resp.get("UnprocessedAccounts", [])


def get_administrator_account(
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
    client = get_client("securityhub", region_name)
    try:
        resp = client.get_administrator_account()
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_administrator_account failed") from exc
    return resp.get("Administrator", {})


def accept_administrator_invitation(
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
    client = get_client("securityhub", region_name)
    try:
        client.accept_administrator_invitation(
            AdministratorId=administrator_id,
            InvitationId=invitation_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "accept_administrator_invitation failed") from exc


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_member(m: dict[str, Any]) -> MemberResult:
    """Parse a raw member dict into a :class:`MemberResult`."""
    return MemberResult(
        account_id=m.get("AccountId", ""),
        email=m.get("Email", ""),
        member_status=m.get("MemberStatus", ""),
        invited_at=str(m["InvitedAt"]) if "InvitedAt" in m else None,
        updated_at=str(m["UpdatedAt"]) if "UpdatedAt" in m else None,
        administrator_id=m.get("AdministratorId"),
        extra={
            k: v
            for k, v in m.items()
            if k
            not in {
                "AccountId",
                "Email",
                "MemberStatus",
                "InvitedAt",
                "UpdatedAt",
                "AdministratorId",
            }
        },
    )


class BatchDeleteAutomationRulesResult(BaseModel):
    """Result of batch_delete_automation_rules."""

    model_config = ConfigDict(frozen=True)

    processed_automation_rules: list[str] | None = None
    unprocessed_automation_rules: list[dict[str, Any]] | None = None


class BatchGetAutomationRulesResult(BaseModel):
    """Result of batch_get_automation_rules."""

    model_config = ConfigDict(frozen=True)

    rules: list[dict[str, Any]] | None = None
    unprocessed_automation_rules: list[dict[str, Any]] | None = None


class BatchGetConfigurationPolicyAssociationsResult(BaseModel):
    """Result of batch_get_configuration_policy_associations."""

    model_config = ConfigDict(frozen=True)

    configuration_policy_associations: list[dict[str, Any]] | None = None
    unprocessed_configuration_policy_associations: list[dict[str, Any]] | None = None


class BatchGetSecurityControlsResult(BaseModel):
    """Result of batch_get_security_controls."""

    model_config = ConfigDict(frozen=True)

    security_controls: list[dict[str, Any]] | None = None
    unprocessed_ids: list[dict[str, Any]] | None = None


class BatchGetStandardsControlAssociationsResult(BaseModel):
    """Result of batch_get_standards_control_associations."""

    model_config = ConfigDict(frozen=True)

    standards_control_association_details: list[dict[str, Any]] | None = None
    unprocessed_associations: list[dict[str, Any]] | None = None


class BatchImportFindingsResult(BaseModel):
    """Result of batch_import_findings."""

    model_config = ConfigDict(frozen=True)

    failed_count: int | None = None
    success_count: int | None = None
    failed_findings: list[dict[str, Any]] | None = None


class BatchUpdateAutomationRulesResult(BaseModel):
    """Result of batch_update_automation_rules."""

    model_config = ConfigDict(frozen=True)

    processed_automation_rules: list[str] | None = None
    unprocessed_automation_rules: list[dict[str, Any]] | None = None


class BatchUpdateFindingsResult(BaseModel):
    """Result of batch_update_findings."""

    model_config = ConfigDict(frozen=True)

    processed_findings: list[dict[str, Any]] | None = None
    unprocessed_findings: list[dict[str, Any]] | None = None


class BatchUpdateFindingsV2Result(BaseModel):
    """Result of batch_update_findings_v2."""

    model_config = ConfigDict(frozen=True)

    processed_findings: list[dict[str, Any]] | None = None
    unprocessed_findings: list[dict[str, Any]] | None = None


class BatchUpdateStandardsControlAssociationsResult(BaseModel):
    """Result of batch_update_standards_control_associations."""

    model_config = ConfigDict(frozen=True)

    unprocessed_association_updates: list[dict[str, Any]] | None = None


class ConnectorRegistrationsV2Result(BaseModel):
    """Result of connector_registrations_v2."""

    model_config = ConfigDict(frozen=True)

    connector_arn: str | None = None
    connector_id: str | None = None


class CreateActionTargetResult(BaseModel):
    """Result of create_action_target."""

    model_config = ConfigDict(frozen=True)

    action_target_arn: str | None = None


class CreateAggregatorV2Result(BaseModel):
    """Result of create_aggregator_v2."""

    model_config = ConfigDict(frozen=True)

    aggregator_v2_arn: str | None = None
    aggregation_region: str | None = None
    region_linking_mode: str | None = None
    linked_regions: list[str] | None = None


class CreateAutomationRuleResult(BaseModel):
    """Result of create_automation_rule."""

    model_config = ConfigDict(frozen=True)

    rule_arn: str | None = None


class CreateAutomationRuleV2Result(BaseModel):
    """Result of create_automation_rule_v2."""

    model_config = ConfigDict(frozen=True)

    rule_arn: str | None = None
    rule_id: str | None = None


class CreateConfigurationPolicyResult(BaseModel):
    """Result of create_configuration_policy."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    description: str | None = None
    updated_at: str | None = None
    created_at: str | None = None
    configuration_policy: dict[str, Any] | None = None


class CreateConnectorV2Result(BaseModel):
    """Result of create_connector_v2."""

    model_config = ConfigDict(frozen=True)

    connector_arn: str | None = None
    connector_id: str | None = None
    auth_url: str | None = None


class CreateFindingAggregatorResult(BaseModel):
    """Result of create_finding_aggregator."""

    model_config = ConfigDict(frozen=True)

    finding_aggregator_arn: str | None = None
    finding_aggregation_region: str | None = None
    region_linking_mode: str | None = None
    regions: list[str] | None = None


class CreateTicketV2Result(BaseModel):
    """Result of create_ticket_v2."""

    model_config = ConfigDict(frozen=True)

    ticket_id: str | None = None
    ticket_src_url: str | None = None


class DeclineInvitationsResult(BaseModel):
    """Result of decline_invitations."""

    model_config = ConfigDict(frozen=True)

    unprocessed_accounts: list[dict[str, Any]] | None = None


class DeleteActionTargetResult(BaseModel):
    """Result of delete_action_target."""

    model_config = ConfigDict(frozen=True)

    action_target_arn: str | None = None


class DeleteInvitationsResult(BaseModel):
    """Result of delete_invitations."""

    model_config = ConfigDict(frozen=True)

    unprocessed_accounts: list[dict[str, Any]] | None = None


class DescribeActionTargetsResult(BaseModel):
    """Result of describe_action_targets."""

    model_config = ConfigDict(frozen=True)

    action_targets: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeOrganizationConfigurationResult(BaseModel):
    """Result of describe_organization_configuration."""

    model_config = ConfigDict(frozen=True)

    auto_enable: bool | None = None
    member_account_limit_reached: bool | None = None
    auto_enable_standards: str | None = None
    organization_configuration: dict[str, Any] | None = None


class DescribeProductsResult(BaseModel):
    """Result of describe_products."""

    model_config = ConfigDict(frozen=True)

    products: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeProductsV2Result(BaseModel):
    """Result of describe_products_v2."""

    model_config = ConfigDict(frozen=True)

    products_v2: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeSecurityHubV2Result(BaseModel):
    """Result of describe_security_hub_v2."""

    model_config = ConfigDict(frozen=True)

    hub_v2_arn: str | None = None
    subscribed_at: str | None = None


class EnableOrganizationAdminAccountResult(BaseModel):
    """Result of enable_organization_admin_account."""

    model_config = ConfigDict(frozen=True)

    admin_account_id: str | None = None
    feature: str | None = None


class EnableSecurityHubV2Result(BaseModel):
    """Result of enable_security_hub_v2."""

    model_config = ConfigDict(frozen=True)

    hub_v2_arn: str | None = None


class GetAggregatorV2Result(BaseModel):
    """Result of get_aggregator_v2."""

    model_config = ConfigDict(frozen=True)

    aggregator_v2_arn: str | None = None
    aggregation_region: str | None = None
    region_linking_mode: str | None = None
    linked_regions: list[str] | None = None


class GetAutomationRuleV2Result(BaseModel):
    """Result of get_automation_rule_v2."""

    model_config = ConfigDict(frozen=True)

    rule_arn: str | None = None
    rule_id: str | None = None
    rule_order: float | None = None
    rule_name: str | None = None
    rule_status: str | None = None
    description: str | None = None
    criteria: dict[str, Any] | None = None
    actions: list[dict[str, Any]] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class GetConfigurationPolicyResult(BaseModel):
    """Result of get_configuration_policy."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    description: str | None = None
    updated_at: str | None = None
    created_at: str | None = None
    configuration_policy: dict[str, Any] | None = None


class GetConfigurationPolicyAssociationResult(BaseModel):
    """Result of get_configuration_policy_association."""

    model_config = ConfigDict(frozen=True)

    configuration_policy_id: str | None = None
    target_id: str | None = None
    target_type: str | None = None
    association_type: str | None = None
    updated_at: str | None = None
    association_status: str | None = None
    association_status_message: str | None = None


class GetConnectorV2Result(BaseModel):
    """Result of get_connector_v2."""

    model_config = ConfigDict(frozen=True)

    connector_arn: str | None = None
    connector_id: str | None = None
    name: str | None = None
    description: str | None = None
    kms_key_arn: str | None = None
    created_at: str | None = None
    last_updated_at: str | None = None
    health: dict[str, Any] | None = None
    provider_detail: dict[str, Any] | None = None


class GetFindingAggregatorResult(BaseModel):
    """Result of get_finding_aggregator."""

    model_config = ConfigDict(frozen=True)

    finding_aggregator_arn: str | None = None
    finding_aggregation_region: str | None = None
    region_linking_mode: str | None = None
    regions: list[str] | None = None


class GetFindingHistoryResult(BaseModel):
    """Result of get_finding_history."""

    model_config = ConfigDict(frozen=True)

    records: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetFindingStatisticsV2Result(BaseModel):
    """Result of get_finding_statistics_v2."""

    model_config = ConfigDict(frozen=True)

    group_by_results: list[dict[str, Any]] | None = None


class GetFindingsV2Result(BaseModel):
    """Result of get_findings_v2."""

    model_config = ConfigDict(frozen=True)

    findings: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetInsightsResult(BaseModel):
    """Result of get_insights."""

    model_config = ConfigDict(frozen=True)

    insights: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetInvitationsCountResult(BaseModel):
    """Result of get_invitations_count."""

    model_config = ConfigDict(frozen=True)

    invitations_count: int | None = None


class GetMasterAccountResult(BaseModel):
    """Result of get_master_account."""

    model_config = ConfigDict(frozen=True)

    master: dict[str, Any] | None = None


class GetResourcesStatisticsV2Result(BaseModel):
    """Result of get_resources_statistics_v2."""

    model_config = ConfigDict(frozen=True)

    group_by_results: list[dict[str, Any]] | None = None


class GetResourcesV2Result(BaseModel):
    """Result of get_resources_v2."""

    model_config = ConfigDict(frozen=True)

    resources: list[dict[str, Any]] | None = None
    next_token: str | None = None


class GetSecurityControlDefinitionResult(BaseModel):
    """Result of get_security_control_definition."""

    model_config = ConfigDict(frozen=True)

    security_control_definition: dict[str, Any] | None = None


class ListAggregatorsV2Result(BaseModel):
    """Result of list_aggregators_v2."""

    model_config = ConfigDict(frozen=True)

    aggregators_v2: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAutomationRulesResult(BaseModel):
    """Result of list_automation_rules."""

    model_config = ConfigDict(frozen=True)

    automation_rules_metadata: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAutomationRulesV2Result(BaseModel):
    """Result of list_automation_rules_v2."""

    model_config = ConfigDict(frozen=True)

    rules: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListConfigurationPoliciesResult(BaseModel):
    """Result of list_configuration_policies."""

    model_config = ConfigDict(frozen=True)

    configuration_policy_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListConfigurationPolicyAssociationsResult(BaseModel):
    """Result of list_configuration_policy_associations."""

    model_config = ConfigDict(frozen=True)

    configuration_policy_association_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListConnectorsV2Result(BaseModel):
    """Result of list_connectors_v2."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    connectors: list[dict[str, Any]] | None = None


class ListFindingAggregatorsResult(BaseModel):
    """Result of list_finding_aggregators."""

    model_config = ConfigDict(frozen=True)

    finding_aggregators: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInvitationsResult(BaseModel):
    """Result of list_invitations."""

    model_config = ConfigDict(frozen=True)

    invitations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListOrganizationAdminAccountsResult(BaseModel):
    """Result of list_organization_admin_accounts."""

    model_config = ConfigDict(frozen=True)

    admin_accounts: list[dict[str, Any]] | None = None
    next_token: str | None = None
    feature: str | None = None


class ListSecurityControlDefinitionsResult(BaseModel):
    """Result of list_security_control_definitions."""

    model_config = ConfigDict(frozen=True)

    security_control_definitions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListStandardsControlAssociationsResult(BaseModel):
    """Result of list_standards_control_associations."""

    model_config = ConfigDict(frozen=True)

    standards_control_association_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class StartConfigurationPolicyAssociationResult(BaseModel):
    """Result of start_configuration_policy_association."""

    model_config = ConfigDict(frozen=True)

    configuration_policy_id: str | None = None
    target_id: str | None = None
    target_type: str | None = None
    association_type: str | None = None
    updated_at: str | None = None
    association_status: str | None = None
    association_status_message: str | None = None


class UpdateAggregatorV2Result(BaseModel):
    """Result of update_aggregator_v2."""

    model_config = ConfigDict(frozen=True)

    aggregator_v2_arn: str | None = None
    aggregation_region: str | None = None
    region_linking_mode: str | None = None
    linked_regions: list[str] | None = None


class UpdateConfigurationPolicyResult(BaseModel):
    """Result of update_configuration_policy."""

    model_config = ConfigDict(frozen=True)

    arn: str | None = None
    id: str | None = None
    name: str | None = None
    description: str | None = None
    updated_at: str | None = None
    created_at: str | None = None
    configuration_policy: dict[str, Any] | None = None


class UpdateFindingAggregatorResult(BaseModel):
    """Result of update_finding_aggregator."""

    model_config = ConfigDict(frozen=True)

    finding_aggregator_arn: str | None = None
    finding_aggregation_region: str | None = None
    region_linking_mode: str | None = None
    regions: list[str] | None = None


def accept_invitation(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MasterId"] = master_id
    kwargs["InvitationId"] = invitation_id
    try:
        client.accept_invitation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to accept invitation") from exc
    return None


def batch_delete_automation_rules(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationRulesArns"] = automation_rules_arns
    try:
        resp = client.batch_delete_automation_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch delete automation rules") from exc
    return BatchDeleteAutomationRulesResult(
        processed_automation_rules=resp.get("ProcessedAutomationRules"),
        unprocessed_automation_rules=resp.get("UnprocessedAutomationRules"),
    )


def batch_get_automation_rules(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutomationRulesArns"] = automation_rules_arns
    try:
        resp = client.batch_get_automation_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get automation rules") from exc
    return BatchGetAutomationRulesResult(
        rules=resp.get("Rules"),
        unprocessed_automation_rules=resp.get("UnprocessedAutomationRules"),
    )


def batch_get_configuration_policy_associations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationPolicyAssociationIdentifiers"] = (
        configuration_policy_association_identifiers
    )
    try:
        resp = client.batch_get_configuration_policy_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get configuration policy associations") from exc
    return BatchGetConfigurationPolicyAssociationsResult(
        configuration_policy_associations=resp.get("ConfigurationPolicyAssociations"),
        unprocessed_configuration_policy_associations=resp.get(
            "UnprocessedConfigurationPolicyAssociations"
        ),
    )


def batch_get_security_controls(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlIds"] = security_control_ids
    try:
        resp = client.batch_get_security_controls(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get security controls") from exc
    return BatchGetSecurityControlsResult(
        security_controls=resp.get("SecurityControls"),
        unprocessed_ids=resp.get("UnprocessedIds"),
    )


def batch_get_standards_control_associations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StandardsControlAssociationIds"] = standards_control_association_ids
    try:
        resp = client.batch_get_standards_control_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get standards control associations") from exc
    return BatchGetStandardsControlAssociationsResult(
        standards_control_association_details=resp.get("StandardsControlAssociationDetails"),
        unprocessed_associations=resp.get("UnprocessedAssociations"),
    )


def batch_import_findings(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Findings"] = findings
    try:
        resp = client.batch_import_findings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch import findings") from exc
    return BatchImportFindingsResult(
        failed_count=resp.get("FailedCount"),
        success_count=resp.get("SuccessCount"),
        failed_findings=resp.get("FailedFindings"),
    )


def batch_update_automation_rules(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["UpdateAutomationRulesRequestItems"] = update_automation_rules_request_items
    try:
        resp = client.batch_update_automation_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch update automation rules") from exc
    return BatchUpdateAutomationRulesResult(
        processed_automation_rules=resp.get("ProcessedAutomationRules"),
        unprocessed_automation_rules=resp.get("UnprocessedAutomationRules"),
    )


def batch_update_findings(
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
    client = get_client("securityhub", region_name)
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
        resp = client.batch_update_findings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch update findings") from exc
    return BatchUpdateFindingsResult(
        processed_findings=resp.get("ProcessedFindings"),
        unprocessed_findings=resp.get("UnprocessedFindings"),
    )


def batch_update_findings_v2(
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
    client = get_client("securityhub", region_name)
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
        resp = client.batch_update_findings_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch update findings v2") from exc
    return BatchUpdateFindingsV2Result(
        processed_findings=resp.get("ProcessedFindings"),
        unprocessed_findings=resp.get("UnprocessedFindings"),
    )


def batch_update_standards_control_associations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StandardsControlAssociationUpdates"] = standards_control_association_updates
    try:
        resp = client.batch_update_standards_control_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch update standards control associations") from exc
    return BatchUpdateStandardsControlAssociationsResult(
        unprocessed_association_updates=resp.get("UnprocessedAssociationUpdates"),
    )


def connector_registrations_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AuthCode"] = auth_code
    kwargs["AuthState"] = auth_state
    try:
        resp = client.connector_registrations_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to connector registrations v2") from exc
    return ConnectorRegistrationsV2Result(
        connector_arn=resp.get("ConnectorArn"),
        connector_id=resp.get("ConnectorId"),
    )


def create_action_target(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Description"] = description
    kwargs["Id"] = id
    try:
        resp = client.create_action_target(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create action target") from exc
    return CreateActionTargetResult(
        action_target_arn=resp.get("ActionTargetArn"),
    )


def create_aggregator_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegionLinkingMode"] = region_linking_mode
    if linked_regions is not None:
        kwargs["LinkedRegions"] = linked_regions
    if tags is not None:
        kwargs["Tags"] = tags
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_aggregator_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create aggregator v2") from exc
    return CreateAggregatorV2Result(
        aggregator_v2_arn=resp.get("AggregatorV2Arn"),
        aggregation_region=resp.get("AggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        linked_regions=resp.get("LinkedRegions"),
    )


def create_automation_rule(
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
    client = get_client("securityhub", region_name)
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
        resp = client.create_automation_rule(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create automation rule") from exc
    return CreateAutomationRuleResult(
        rule_arn=resp.get("RuleArn"),
    )


def create_automation_rule_v2(
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
    client = get_client("securityhub", region_name)
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
        resp = client.create_automation_rule_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create automation rule v2") from exc
    return CreateAutomationRuleV2Result(
        rule_arn=resp.get("RuleArn"),
        rule_id=resp.get("RuleId"),
    )


def create_configuration_policy(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["ConfigurationPolicy"] = configuration_policy
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_configuration_policy(**kwargs)
    except ClientError as exc:
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


def create_connector_v2(
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
    client = get_client("securityhub", region_name)
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
        resp = client.create_connector_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create connector v2") from exc
    return CreateConnectorV2Result(
        connector_arn=resp.get("ConnectorArn"),
        connector_id=resp.get("ConnectorId"),
        auth_url=resp.get("AuthUrl"),
    )


def create_finding_aggregator(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RegionLinkingMode"] = region_linking_mode
    if regions is not None:
        kwargs["Regions"] = regions
    try:
        resp = client.create_finding_aggregator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create finding aggregator") from exc
    return CreateFindingAggregatorResult(
        finding_aggregator_arn=resp.get("FindingAggregatorArn"),
        finding_aggregation_region=resp.get("FindingAggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        regions=resp.get("Regions"),
    )


def create_ticket_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    kwargs["FindingMetadataUid"] = finding_metadata_uid
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    try:
        resp = client.create_ticket_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create ticket v2") from exc
    return CreateTicketV2Result(
        ticket_id=resp.get("TicketId"),
        ticket_src_url=resp.get("TicketSrcUrl"),
    )


def decline_invitations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountIds"] = account_ids
    try:
        resp = client.decline_invitations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to decline invitations") from exc
    return DeclineInvitationsResult(
        unprocessed_accounts=resp.get("UnprocessedAccounts"),
    )


def delete_action_target(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionTargetArn"] = action_target_arn
    try:
        resp = client.delete_action_target(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete action target") from exc
    return DeleteActionTargetResult(
        action_target_arn=resp.get("ActionTargetArn"),
    )


def delete_aggregator_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AggregatorV2Arn"] = aggregator_v2_arn
    try:
        client.delete_aggregator_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete aggregator v2") from exc
    return None


def delete_automation_rule_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        client.delete_automation_rule_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete automation rule v2") from exc
    return None


def delete_configuration_policy(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        client.delete_configuration_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration policy") from exc
    return None


def delete_connector_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        client.delete_connector_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete connector v2") from exc
    return None


def delete_finding_aggregator(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingAggregatorArn"] = finding_aggregator_arn
    try:
        client.delete_finding_aggregator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete finding aggregator") from exc
    return None


def delete_invitations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountIds"] = account_ids
    try:
        resp = client.delete_invitations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete invitations") from exc
    return DeleteInvitationsResult(
        unprocessed_accounts=resp.get("UnprocessedAccounts"),
    )


def describe_action_targets(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if action_target_arns is not None:
        kwargs["ActionTargetArns"] = action_target_arns
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_action_targets(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe action targets") from exc
    return DescribeActionTargetsResult(
        action_targets=resp.get("ActionTargets"),
        next_token=resp.get("NextToken"),
    )


def describe_organization_configuration(
    region_name: str | None = None,
) -> DescribeOrganizationConfigurationResult:
    """Describe organization configuration.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_organization_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe organization configuration") from exc
    return DescribeOrganizationConfigurationResult(
        auto_enable=resp.get("AutoEnable"),
        member_account_limit_reached=resp.get("MemberAccountLimitReached"),
        auto_enable_standards=resp.get("AutoEnableStandards"),
        organization_configuration=resp.get("OrganizationConfiguration"),
    )


def describe_products(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if product_arn is not None:
        kwargs["ProductArn"] = product_arn
    try:
        resp = client.describe_products(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe products") from exc
    return DescribeProductsResult(
        products=resp.get("Products"),
        next_token=resp.get("NextToken"),
    )


def describe_products_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.describe_products_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe products v2") from exc
    return DescribeProductsV2Result(
        products_v2=resp.get("ProductsV2"),
        next_token=resp.get("NextToken"),
    )


def describe_security_hub_v2(
    region_name: str | None = None,
) -> DescribeSecurityHubV2Result:
    """Describe security hub v2.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_security_hub_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe security hub v2") from exc
    return DescribeSecurityHubV2Result(
        hub_v2_arn=resp.get("HubV2Arn"),
        subscribed_at=resp.get("SubscribedAt"),
    )


def disable_organization_admin_account(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdminAccountId"] = admin_account_id
    if feature is not None:
        kwargs["Feature"] = feature
    try:
        client.disable_organization_admin_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable organization admin account") from exc
    return None


def disable_security_hub_v2(
    region_name: str | None = None,
) -> None:
    """Disable security hub v2.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.disable_security_hub_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable security hub v2") from exc
    return None


def disassociate_from_administrator_account(
    region_name: str | None = None,
) -> None:
    """Disassociate from administrator account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.disassociate_from_administrator_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate from administrator account") from exc
    return None


def disassociate_from_master_account(
    region_name: str | None = None,
) -> None:
    """Disassociate from master account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        client.disassociate_from_master_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate from master account") from exc
    return None


def disassociate_members(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AccountIds"] = account_ids
    try:
        client.disassociate_members(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate members") from exc
    return None


def enable_organization_admin_account(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AdminAccountId"] = admin_account_id
    if feature is not None:
        kwargs["Feature"] = feature
    try:
        resp = client.enable_organization_admin_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable organization admin account") from exc
    return EnableOrganizationAdminAccountResult(
        admin_account_id=resp.get("AdminAccountId"),
        feature=resp.get("Feature"),
    )


def enable_security_hub_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.enable_security_hub_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable security hub v2") from exc
    return EnableSecurityHubV2Result(
        hub_v2_arn=resp.get("HubV2Arn"),
    )


def get_aggregator_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AggregatorV2Arn"] = aggregator_v2_arn
    try:
        resp = client.get_aggregator_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get aggregator v2") from exc
    return GetAggregatorV2Result(
        aggregator_v2_arn=resp.get("AggregatorV2Arn"),
        aggregation_region=resp.get("AggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        linked_regions=resp.get("LinkedRegions"),
    )


def get_automation_rule_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = client.get_automation_rule_v2(**kwargs)
    except ClientError as exc:
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


def get_configuration_policy(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Identifier"] = identifier
    try:
        resp = client.get_configuration_policy(**kwargs)
    except ClientError as exc:
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


def get_configuration_policy_association(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Target"] = target
    try:
        resp = client.get_configuration_policy_association(**kwargs)
    except ClientError as exc:
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


def get_connector_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    try:
        resp = client.get_connector_v2(**kwargs)
    except ClientError as exc:
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


def get_finding_aggregator(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingAggregatorArn"] = finding_aggregator_arn
    try:
        resp = client.get_finding_aggregator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get finding aggregator") from exc
    return GetFindingAggregatorResult(
        finding_aggregator_arn=resp.get("FindingAggregatorArn"),
        finding_aggregation_region=resp.get("FindingAggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        regions=resp.get("Regions"),
    )


def get_finding_history(
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
    client = get_client("securityhub", region_name)
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
        resp = client.get_finding_history(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get finding history") from exc
    return GetFindingHistoryResult(
        records=resp.get("Records"),
        next_token=resp.get("NextToken"),
    )


def get_finding_statistics_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupByRules"] = group_by_rules
    if sort_order is not None:
        kwargs["SortOrder"] = sort_order
    if max_statistic_results is not None:
        kwargs["MaxStatisticResults"] = max_statistic_results
    try:
        resp = client.get_finding_statistics_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get finding statistics v2") from exc
    return GetFindingStatisticsV2Result(
        group_by_results=resp.get("GroupByResults"),
    )


def get_findings_v2(
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
    client = get_client("securityhub", region_name)
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
        resp = client.get_findings_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get findings v2") from exc
    return GetFindingsV2Result(
        findings=resp.get("Findings"),
        next_token=resp.get("NextToken"),
    )


def get_insights(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if insight_arns is not None:
        kwargs["InsightArns"] = insight_arns
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.get_insights(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get insights") from exc
    return GetInsightsResult(
        insights=resp.get("Insights"),
        next_token=resp.get("NextToken"),
    )


def get_invitations_count(
    region_name: str | None = None,
) -> GetInvitationsCountResult:
    """Get invitations count.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_invitations_count(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get invitations count") from exc
    return GetInvitationsCountResult(
        invitations_count=resp.get("InvitationsCount"),
    )


def get_master_account(
    region_name: str | None = None,
) -> GetMasterAccountResult:
    """Get master account.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.get_master_account(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get master account") from exc
    return GetMasterAccountResult(
        master=resp.get("Master"),
    )


def get_resources_statistics_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GroupByRules"] = group_by_rules
    if sort_order is not None:
        kwargs["SortOrder"] = sort_order
    if max_statistic_results is not None:
        kwargs["MaxStatisticResults"] = max_statistic_results
    try:
        resp = client.get_resources_statistics_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resources statistics v2") from exc
    return GetResourcesStatisticsV2Result(
        group_by_results=resp.get("GroupByResults"),
    )


def get_resources_v2(
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
    client = get_client("securityhub", region_name)
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
        resp = client.get_resources_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resources v2") from exc
    return GetResourcesV2Result(
        resources=resp.get("Resources"),
        next_token=resp.get("NextToken"),
    )


def get_security_control_definition(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlId"] = security_control_id
    try:
        resp = client.get_security_control_definition(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get security control definition") from exc
    return GetSecurityControlDefinitionResult(
        security_control_definition=resp.get("SecurityControlDefinition"),
    )


def list_aggregators_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_aggregators_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list aggregators v2") from exc
    return ListAggregatorsV2Result(
        aggregators_v2=resp.get("AggregatorsV2"),
        next_token=resp.get("NextToken"),
    )


def list_automation_rules(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_automation_rules(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list automation rules") from exc
    return ListAutomationRulesResult(
        automation_rules_metadata=resp.get("AutomationRulesMetadata"),
        next_token=resp.get("NextToken"),
    )


def list_automation_rules_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_automation_rules_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list automation rules v2") from exc
    return ListAutomationRulesV2Result(
        rules=resp.get("Rules"),
        next_token=resp.get("NextToken"),
    )


def list_configuration_policies(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_configuration_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list configuration policies") from exc
    return ListConfigurationPoliciesResult(
        configuration_policy_summaries=resp.get("ConfigurationPolicySummaries"),
        next_token=resp.get("NextToken"),
    )


def list_configuration_policy_associations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if filters is not None:
        kwargs["Filters"] = filters
    try:
        resp = client.list_configuration_policy_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list configuration policy associations") from exc
    return ListConfigurationPolicyAssociationsResult(
        configuration_policy_association_summaries=resp.get(
            "ConfigurationPolicyAssociationSummaries"
        ),
        next_token=resp.get("NextToken"),
    )


def list_connectors_v2(
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
    client = get_client("securityhub", region_name)
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
        resp = client.list_connectors_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list connectors v2") from exc
    return ListConnectorsV2Result(
        next_token=resp.get("NextToken"),
        connectors=resp.get("Connectors"),
    )


def list_finding_aggregators(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_finding_aggregators(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list finding aggregators") from exc
    return ListFindingAggregatorsResult(
        finding_aggregators=resp.get("FindingAggregators"),
        next_token=resp.get("NextToken"),
    )


def list_invitations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_invitations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list invitations") from exc
    return ListInvitationsResult(
        invitations=resp.get("Invitations"),
        next_token=resp.get("NextToken"),
    )


def list_organization_admin_accounts(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if feature is not None:
        kwargs["Feature"] = feature
    try:
        resp = client.list_organization_admin_accounts(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list organization admin accounts") from exc
    return ListOrganizationAdminAccountsResult(
        admin_accounts=resp.get("AdminAccounts"),
        next_token=resp.get("NextToken"),
        feature=resp.get("Feature"),
    )


def list_security_control_definitions(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if standards_arn is not None:
        kwargs["StandardsArn"] = standards_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_security_control_definitions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list security control definitions") from exc
    return ListSecurityControlDefinitionsResult(
        security_control_definitions=resp.get("SecurityControlDefinitions"),
        next_token=resp.get("NextToken"),
    )


def list_standards_control_associations(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlId"] = security_control_id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_standards_control_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list standards control associations") from exc
    return ListStandardsControlAssociationsResult(
        standards_control_association_summaries=resp.get("StandardsControlAssociationSummaries"),
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def start_configuration_policy_association(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationPolicyIdentifier"] = configuration_policy_identifier
    kwargs["Target"] = target
    try:
        resp = client.start_configuration_policy_association(**kwargs)
    except ClientError as exc:
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


def start_configuration_policy_disassociation(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConfigurationPolicyIdentifier"] = configuration_policy_identifier
    if target is not None:
        kwargs["Target"] = target
    try:
        client.start_configuration_policy_disassociation(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start configuration policy disassociation") from exc
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
    client = get_client("securityhub", region_name)
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_action_target(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ActionTargetArn"] = action_target_arn
    if name is not None:
        kwargs["Name"] = name
    if description is not None:
        kwargs["Description"] = description
    try:
        client.update_action_target(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update action target") from exc
    return None


def update_aggregator_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AggregatorV2Arn"] = aggregator_v2_arn
    kwargs["RegionLinkingMode"] = region_linking_mode
    if linked_regions is not None:
        kwargs["LinkedRegions"] = linked_regions
    try:
        resp = client.update_aggregator_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update aggregator v2") from exc
    return UpdateAggregatorV2Result(
        aggregator_v2_arn=resp.get("AggregatorV2Arn"),
        aggregation_region=resp.get("AggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        linked_regions=resp.get("LinkedRegions"),
    )


def update_automation_rule_v2(
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
    client = get_client("securityhub", region_name)
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
        client.update_automation_rule_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update automation rule v2") from exc
    return None


def update_configuration_policy(
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
    client = get_client("securityhub", region_name)
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
        resp = client.update_configuration_policy(**kwargs)
    except ClientError as exc:
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


def update_connector_v2(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConnectorId"] = connector_id
    if client_secret is not None:
        kwargs["ClientSecret"] = client_secret
    if description is not None:
        kwargs["Description"] = description
    if provider is not None:
        kwargs["Provider"] = provider
    try:
        client.update_connector_v2(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update connector v2") from exc
    return None


def update_finding_aggregator(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["FindingAggregatorArn"] = finding_aggregator_arn
    kwargs["RegionLinkingMode"] = region_linking_mode
    if regions is not None:
        kwargs["Regions"] = regions
    try:
        resp = client.update_finding_aggregator(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update finding aggregator") from exc
    return UpdateFindingAggregatorResult(
        finding_aggregator_arn=resp.get("FindingAggregatorArn"),
        finding_aggregation_region=resp.get("FindingAggregationRegion"),
        region_linking_mode=resp.get("RegionLinkingMode"),
        regions=resp.get("Regions"),
    )


def update_organization_configuration(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AutoEnable"] = auto_enable
    if auto_enable_standards is not None:
        kwargs["AutoEnableStandards"] = auto_enable_standards
    if organization_configuration is not None:
        kwargs["OrganizationConfiguration"] = organization_configuration
    try:
        client.update_organization_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update organization configuration") from exc
    return None


def update_security_control(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SecurityControlId"] = security_control_id
    kwargs["Parameters"] = parameters
    if last_update_reason is not None:
        kwargs["LastUpdateReason"] = last_update_reason
    try:
        client.update_security_control(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update security control") from exc
    return None


def update_security_hub_configuration(
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
    client = get_client("securityhub", region_name)
    kwargs: dict[str, Any] = {}
    if auto_enable_controls is not None:
        kwargs["AutoEnableControls"] = auto_enable_controls
    if control_finding_generator is not None:
        kwargs["ControlFindingGenerator"] = control_finding_generator
    try:
        client.update_security_hub_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update security hub configuration") from exc
    return None
