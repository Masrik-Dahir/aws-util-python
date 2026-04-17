

"""Tests for aws_util.aio.security_hub --- native async Security Hub utilities."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.security_hub import (
    FindingResult,
    HubResult,
    InsightResult,
    MemberResult,
    StandardResult,
)

import aws_util.aio.security_hub as mod
from aws_util.aio.security_hub import (

    accept_administrator_invitation,
    batch_disable_standards,
    batch_enable_standards,
    create_insight,
    create_members,
    delete_insight,
    delete_members,
    describe_hub,
    describe_standards,
    describe_standards_controls,
    disable_import_findings_for_product,
    disable_security_hub,
    enable_import_findings_for_product,
    enable_security_hub,
    get_administrator_account,
    get_enabled_standards,
    get_findings,
    get_insight_results,
    get_members,
    invite_members,
    list_enabled_products_for_import,
    list_insights,
    list_members,
    update_findings,
    update_insight,
    update_standards_control,
    accept_invitation,
    batch_delete_automation_rules,
    batch_get_automation_rules,
    batch_get_configuration_policy_associations,
    batch_get_security_controls,
    batch_get_standards_control_associations,
    batch_import_findings,
    batch_update_automation_rules,
    batch_update_findings,
    batch_update_findings_v2,
    batch_update_standards_control_associations,
    connector_registrations_v2,
    create_action_target,
    create_aggregator_v2,
    create_automation_rule,
    create_automation_rule_v2,
    create_configuration_policy,
    create_connector_v2,
    create_finding_aggregator,
    create_ticket_v2,
    decline_invitations,
    delete_action_target,
    delete_aggregator_v2,
    delete_automation_rule_v2,
    delete_configuration_policy,
    delete_connector_v2,
    delete_finding_aggregator,
    delete_invitations,
    describe_action_targets,
    describe_organization_configuration,
    describe_products,
    describe_products_v2,
    describe_security_hub_v2,
    disable_organization_admin_account,
    disable_security_hub_v2,
    disassociate_from_administrator_account,
    disassociate_from_master_account,
    disassociate_members,
    enable_organization_admin_account,
    enable_security_hub_v2,
    get_aggregator_v2,
    get_automation_rule_v2,
    get_configuration_policy,
    get_configuration_policy_association,
    get_connector_v2,
    get_finding_aggregator,
    get_finding_history,
    get_finding_statistics_v2,
    get_findings_v2,
    get_insights,
    get_invitations_count,
    get_master_account,
    get_resources_statistics_v2,
    get_resources_v2,
    get_security_control_definition,
    list_aggregators_v2,
    list_automation_rules,
    list_automation_rules_v2,
    list_configuration_policies,
    list_configuration_policy_associations,
    list_connectors_v2,
    list_finding_aggregators,
    list_invitations,
    list_organization_admin_accounts,
    list_security_control_definitions,
    list_standards_control_associations,
    list_tags_for_resource,
    start_configuration_policy_association,
    start_configuration_policy_disassociation,
    tag_resource,
    untag_resource,
    update_action_target,
    update_aggregator_v2,
    update_automation_rule_v2,
    update_configuration_policy,
    update_connector_v2,
    update_finding_aggregator,
    update_organization_configuration,
    update_security_control,
    update_security_hub_configuration,
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
        "aws_util.aio.security_hub.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# enable_security_hub
# ---------------------------------------------------------------------------


async def test_enable_security_hub_success(mock_client):
    mock_client.call.return_value = {"HubArn": "arn:hub"}
    result = await enable_security_hub()
    assert result == "arn:hub"


async def test_enable_security_hub_with_tags(mock_client):
    mock_client.call.return_value = {"HubArn": "arn:hub"}
    await enable_security_hub(tags={"env": "prod"})
    kw = mock_client.call.call_args[1]
    assert kw["Tags"] == {"env": "prod"}


async def test_enable_security_hub_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="enable_security_hub failed"):
        await enable_security_hub()


async def test_enable_security_hub_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await enable_security_hub()


# ---------------------------------------------------------------------------
# disable_security_hub
# ---------------------------------------------------------------------------


async def test_disable_security_hub_success(mock_client):
    mock_client.call.return_value = {}
    await disable_security_hub()
    mock_client.call.assert_called_once()


async def test_disable_security_hub_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="disable_security_hub failed"):
        await disable_security_hub()


# ---------------------------------------------------------------------------
# describe_hub
# ---------------------------------------------------------------------------


async def test_describe_hub_success(mock_client):
    mock_client.call.return_value = {
        "HubArn": "arn:hub",
        "SubscribedAt": "2025-01-01",
        "AutoEnableControls": False,
        "ResponseMetadata": {},
    }
    result = await describe_hub()
    assert result.hub_arn == "arn:hub"
    assert result.auto_enable_controls is False


async def test_describe_hub_with_arn(mock_client):
    mock_client.call.return_value = {"HubArn": "arn:hub"}
    await describe_hub(hub_arn="arn:hub")
    kw = mock_client.call.call_args[1]
    assert kw["HubArn"] == "arn:hub"


async def test_describe_hub_extra(mock_client):
    mock_client.call.return_value = {
        "HubArn": "arn:hub",
        "CustomField": "val",
    }
    result = await describe_hub()
    assert result.extra["CustomField"] == "val"


async def test_describe_hub_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="describe_hub failed"):
        await describe_hub()


# ---------------------------------------------------------------------------
# get_findings
# ---------------------------------------------------------------------------


async def test_get_findings_empty(mock_client):
    mock_client.call.return_value = {"Findings": []}
    result = await get_findings()
    assert result == []


async def test_get_findings_single_page(mock_client):
    mock_client.call.return_value = {
        "Findings": [
            {
                "Id": "f-1",
                "ProductArn": "arn:p",
                "Severity": {"Label": "HIGH"},
                "Workflow": {"Status": "NEW"},
            }
        ]
    }
    result = await get_findings()
    assert len(result) == 1
    assert result[0].finding_id == "f-1"
    assert result[0].severity_label == "HIGH"


async def test_get_findings_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "Findings": [{"Id": "f-1", "ProductArn": "arn:p"}],
            "NextToken": "tok1",
        },
        {"Findings": [{"Id": "f-2", "ProductArn": "arn:p"}]},
    ]
    result = await get_findings()
    assert len(result) == 2


async def test_get_findings_with_filters(mock_client):
    mock_client.call.return_value = {"Findings": []}
    await get_findings(filters={"SeverityLabel": [{"Value": "HIGH"}]})
    kw = mock_client.call.call_args[1]
    assert "Filters" in kw


async def test_get_findings_with_sort(mock_client):
    mock_client.call.return_value = {"Findings": []}
    await get_findings(sort_criteria=[{"Field": "Title", "SortOrder": "asc"}])


async def test_get_findings_with_max_results(mock_client):
    mock_client.call.return_value = {"Findings": []}
    await get_findings(max_results=10)


async def test_get_findings_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="get_findings failed"):
        await get_findings()


# ---------------------------------------------------------------------------
# update_findings
# ---------------------------------------------------------------------------


async def test_update_findings_success(mock_client):
    mock_client.call.return_value = {
        "ProcessedFindings": [{"Id": "f-1"}],
        "UnprocessedFindings": [],
    }
    result = await update_findings([{"Id": "f-1", "ProductArn": "arn:p"}])
    assert len(result["ProcessedFindings"]) == 1


async def test_update_findings_with_note(mock_client):
    mock_client.call.return_value = {
        "ProcessedFindings": [],
        "UnprocessedFindings": [],
    }
    await update_findings(
        [{"Id": "f-1", "ProductArn": "arn:p"}],
        note={"Text": "note", "UpdatedBy": "user"},
    )
    kw = mock_client.call.call_args[1]
    assert "Note" in kw


async def test_update_findings_with_severity(mock_client):
    mock_client.call.return_value = {
        "ProcessedFindings": [],
        "UnprocessedFindings": [],
    }
    await update_findings(
        [{"Id": "f-1", "ProductArn": "arn:p"}],
        severity={"Label": "LOW"},
    )


async def test_update_findings_with_workflow(mock_client):
    mock_client.call.return_value = {
        "ProcessedFindings": [],
        "UnprocessedFindings": [],
    }
    await update_findings(
        [{"Id": "f-1", "ProductArn": "arn:p"}],
        workflow={"Status": "RESOLVED"},
    )


async def test_update_findings_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="update_findings failed"):
        await update_findings([{"Id": "f-1", "ProductArn": "arn:p"}])


# ---------------------------------------------------------------------------
# get_insight_results
# ---------------------------------------------------------------------------


async def test_get_insight_results_success(mock_client):
    mock_client.call.return_value = {
        "InsightResults": {"InsightArn": "arn:i", "ResultValues": []}
    }
    result = await get_insight_results("arn:i")
    assert result["InsightArn"] == "arn:i"


async def test_get_insight_results_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="get_insight_results failed"):
        await get_insight_results("arn:i")


# ---------------------------------------------------------------------------
# list_insights
# ---------------------------------------------------------------------------


async def test_list_insights_empty(mock_client):
    mock_client.call.return_value = {"Insights": []}
    result = await list_insights()
    assert result == []


async def test_list_insights_with_results(mock_client):
    mock_client.call.return_value = {
        "Insights": [
            {
                "InsightArn": "arn:i",
                "Name": "My Insight",
                "Filters": {"f": "v"},
                "GroupByAttribute": "ResourceId",
                "Extra": "val",
            }
        ]
    }
    result = await list_insights()
    assert len(result) == 1
    assert result[0].name == "My Insight"
    assert result[0].extra == {"Extra": "val"}


async def test_list_insights_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "Insights": [{"InsightArn": "arn:i1", "Name": "I1"}],
            "NextToken": "tok1",
        },
        {"Insights": [{"InsightArn": "arn:i2", "Name": "I2"}]},
    ]
    result = await list_insights()
    assert len(result) == 2


async def test_list_insights_with_max_results(mock_client):
    mock_client.call.return_value = {"Insights": []}
    await list_insights(max_results=5)


async def test_list_insights_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="list_insights failed"):
        await list_insights()


# ---------------------------------------------------------------------------
# create_insight
# ---------------------------------------------------------------------------


async def test_create_insight_success(mock_client):
    mock_client.call.return_value = {"InsightArn": "arn:new"}
    arn = await create_insight(
        "test", filters={"f": "v"}, group_by_attribute="ResourceId"
    )
    assert arn == "arn:new"


async def test_create_insight_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="create_insight failed"):
        await create_insight(
            "test", filters={}, group_by_attribute="ResourceId"
        )


# ---------------------------------------------------------------------------
# update_insight
# ---------------------------------------------------------------------------


async def test_update_insight_name(mock_client):
    mock_client.call.return_value = {}
    await update_insight("arn:i", name="New Name")
    kw = mock_client.call.call_args[1]
    assert kw["Name"] == "New Name"


async def test_update_insight_filters(mock_client):
    mock_client.call.return_value = {}
    await update_insight("arn:i", filters={"f": "v"})


async def test_update_insight_group_by(mock_client):
    mock_client.call.return_value = {}
    await update_insight("arn:i", group_by_attribute="AccountId")


async def test_update_insight_no_optional(mock_client):
    mock_client.call.return_value = {}
    await update_insight("arn:i")
    kw = mock_client.call.call_args[1]
    assert "Name" not in kw
    assert "Filters" not in kw
    assert "GroupByAttribute" not in kw


async def test_update_insight_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="update_insight failed"):
        await update_insight("arn:i")


# ---------------------------------------------------------------------------
# delete_insight
# ---------------------------------------------------------------------------


async def test_delete_insight_success(mock_client):
    mock_client.call.return_value = {}
    await delete_insight("arn:i")
    mock_client.call.assert_called_once()


async def test_delete_insight_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(RuntimeError, match="delete_insight failed"):
        await delete_insight("arn:i")


# ---------------------------------------------------------------------------
# enable_import_findings_for_product
# ---------------------------------------------------------------------------


async def test_enable_import_findings_success(mock_client):
    mock_client.call.return_value = {
        "ProductSubscriptionArn": "arn:sub"
    }
    result = await enable_import_findings_for_product("arn:product")
    assert result == "arn:sub"


async def test_enable_import_findings_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="enable_import_findings_for_product failed",
    ):
        await enable_import_findings_for_product("arn:product")


# ---------------------------------------------------------------------------
# disable_import_findings_for_product
# ---------------------------------------------------------------------------


async def test_disable_import_findings_success(mock_client):
    mock_client.call.return_value = {}
    await disable_import_findings_for_product("arn:sub")
    mock_client.call.assert_called_once()


async def test_disable_import_findings_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="disable_import_findings_for_product failed",
    ):
        await disable_import_findings_for_product("arn:sub")


# ---------------------------------------------------------------------------
# list_enabled_products_for_import
# ---------------------------------------------------------------------------


async def test_list_enabled_products_empty(mock_client):
    mock_client.call.return_value = {"ProductSubscriptions": []}
    result = await list_enabled_products_for_import()
    assert result == []


async def test_list_enabled_products_with_results(mock_client):
    mock_client.call.return_value = {
        "ProductSubscriptions": ["arn:sub1", "arn:sub2"]
    }
    result = await list_enabled_products_for_import()
    assert len(result) == 2


async def test_list_enabled_products_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "ProductSubscriptions": ["arn:sub1"],
            "NextToken": "tok1",
        },
        {"ProductSubscriptions": ["arn:sub2"]},
    ]
    result = await list_enabled_products_for_import()
    assert len(result) == 2


async def test_list_enabled_products_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="list_enabled_products_for_import failed",
    ):
        await list_enabled_products_for_import()


# ---------------------------------------------------------------------------
# get_enabled_standards
# ---------------------------------------------------------------------------


async def test_get_enabled_standards_empty(mock_client):
    mock_client.call.return_value = {"StandardsSubscriptions": []}
    result = await get_enabled_standards()
    assert result == []


async def test_get_enabled_standards_with_results(mock_client):
    mock_client.call.return_value = {
        "StandardsSubscriptions": [
            {
                "StandardsArn": "arn:std",
                "StandardsSubscriptionArn": "arn:sub",
                "StandardsStatus": "READY",
                "Extra": "val",
            }
        ]
    }
    result = await get_enabled_standards()
    assert len(result) == 1
    assert result[0].standards_arn == "arn:std"
    assert result[0].extra == {"Extra": "val"}


async def test_get_enabled_standards_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "StandardsSubscriptions": [
                {"StandardsArn": "arn:std1"}
            ],
            "NextToken": "tok1",
        },
        {
            "StandardsSubscriptions": [
                {"StandardsArn": "arn:std2"}
            ],
        },
    ]
    result = await get_enabled_standards()
    assert len(result) == 2


async def test_get_enabled_standards_with_filter(mock_client):
    mock_client.call.return_value = {"StandardsSubscriptions": []}
    await get_enabled_standards(
        standards_subscription_arns=["arn:sub"]
    )
    kw = mock_client.call.call_args[1]
    assert kw["StandardsSubscriptionArns"] == ["arn:sub"]


async def test_get_enabled_standards_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="get_enabled_standards failed"
    ):
        await get_enabled_standards()


# ---------------------------------------------------------------------------
# batch_enable_standards
# ---------------------------------------------------------------------------


async def test_batch_enable_standards_success(mock_client):
    mock_client.call.return_value = {
        "StandardsSubscriptions": [
            {
                "StandardsArn": "arn:std",
                "StandardsSubscriptionArn": "arn:sub",
                "StandardsStatus": "READY",
                "Extra": "val",
            }
        ]
    }
    result = await batch_enable_standards(
        [{"StandardsArn": "arn:std"}]
    )
    assert len(result) == 1
    assert result[0].standards_status == "READY"
    assert result[0].extra == {"Extra": "val"}


async def test_batch_enable_standards_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="batch_enable_standards failed"
    ):
        await batch_enable_standards(
            [{"StandardsArn": "arn:std"}]
        )


# ---------------------------------------------------------------------------
# batch_disable_standards
# ---------------------------------------------------------------------------


async def test_batch_disable_standards_success(mock_client):
    mock_client.call.return_value = {}
    await batch_disable_standards(["arn:sub"])
    mock_client.call.assert_called_once()


async def test_batch_disable_standards_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="batch_disable_standards failed"
    ):
        await batch_disable_standards(["arn:sub"])


# ---------------------------------------------------------------------------
# describe_standards
# ---------------------------------------------------------------------------


async def test_describe_standards_empty(mock_client):
    mock_client.call.return_value = {"Standards": []}
    result = await describe_standards()
    assert result == []


async def test_describe_standards_with_results(mock_client):
    mock_client.call.return_value = {
        "Standards": [
            {
                "StandardsArn": "arn:std",
                "Name": "CIS",
                "Description": "CIS Benchmark",
                "Extra": "val",
            }
        ]
    }
    result = await describe_standards()
    assert len(result) == 1
    assert result[0].name == "CIS"
    assert result[0].extra == {"Extra": "val"}


async def test_describe_standards_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "Standards": [{"StandardsArn": "arn:std1", "Name": "S1"}],
            "NextToken": "tok1",
        },
        {
            "Standards": [{"StandardsArn": "arn:std2", "Name": "S2"}],
        },
    ]
    result = await describe_standards()
    assert len(result) == 2


async def test_describe_standards_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="describe_standards failed"
    ):
        await describe_standards()


# ---------------------------------------------------------------------------
# describe_standards_controls
# ---------------------------------------------------------------------------


async def test_describe_standards_controls_success(mock_client):
    mock_client.call.return_value = {
        "Controls": [{"StandardsControlArn": "arn:ctrl"}]
    }
    result = await describe_standards_controls("arn:sub")
    assert len(result) == 1


async def test_describe_standards_controls_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "Controls": [{"StandardsControlArn": "arn:ctrl1"}],
            "NextToken": "tok1",
        },
        {"Controls": [{"StandardsControlArn": "arn:ctrl2"}]},
    ]
    result = await describe_standards_controls("arn:sub")
    assert len(result) == 2


async def test_describe_standards_controls_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="describe_standards_controls failed",
    ):
        await describe_standards_controls("arn:sub")


# ---------------------------------------------------------------------------
# update_standards_control
# ---------------------------------------------------------------------------


async def test_update_standards_control_enable(mock_client):
    mock_client.call.return_value = {}
    await update_standards_control(
        "arn:ctrl", control_status="ENABLED"
    )


async def test_update_standards_control_disable(mock_client):
    mock_client.call.return_value = {}
    await update_standards_control(
        "arn:ctrl",
        control_status="DISABLED",
        disabled_reason="Not applicable",
    )
    kw = mock_client.call.call_args[1]
    assert kw["DisabledReason"] == "Not applicable"


async def test_update_standards_control_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="update_standards_control failed",
    ):
        await update_standards_control(
            "arn:ctrl", control_status="ENABLED"
        )


# ---------------------------------------------------------------------------
# invite_members
# ---------------------------------------------------------------------------


async def test_invite_members_success(mock_client):
    mock_client.call.return_value = {"UnprocessedAccounts": []}
    result = await invite_members(["123"])
    assert result == []


async def test_invite_members_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="invite_members failed"
    ):
        await invite_members(["123"])


# ---------------------------------------------------------------------------
# list_members
# ---------------------------------------------------------------------------


async def test_list_members_empty(mock_client):
    mock_client.call.return_value = {"Members": []}
    result = await list_members()
    assert result == []


async def test_list_members_with_results(mock_client):
    mock_client.call.return_value = {
        "Members": [
            {
                "AccountId": "123",
                "Email": "a@b.com",
                "MemberStatus": "Associated",
            }
        ]
    }
    result = await list_members()
    assert len(result) == 1
    assert result[0].account_id == "123"


async def test_list_members_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "Members": [
                {"AccountId": "123", "MemberStatus": "Associated"}
            ],
            "NextToken": "tok1",
        },
        {
            "Members": [
                {"AccountId": "456", "MemberStatus": "Associated"}
            ],
        },
    ]
    result = await list_members()
    assert len(result) == 2


async def test_list_members_not_only_associated(mock_client):
    mock_client.call.return_value = {"Members": []}
    await list_members(only_associated=False)


async def test_list_members_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="list_members failed"
    ):
        await list_members()


# ---------------------------------------------------------------------------
# get_members
# ---------------------------------------------------------------------------


async def test_get_members_success(mock_client):
    mock_client.call.return_value = {
        "Members": [
            {
                "AccountId": "123",
                "Email": "a@b.com",
                "MemberStatus": "Associated",
            }
        ]
    }
    result = await get_members(["123"])
    assert len(result) == 1


async def test_get_members_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="get_members failed"
    ):
        await get_members(["123"])


# ---------------------------------------------------------------------------
# create_members
# ---------------------------------------------------------------------------


async def test_create_members_success(mock_client):
    mock_client.call.return_value = {"UnprocessedAccounts": []}
    result = await create_members([{"AccountId": "123"}])
    assert result == []


async def test_create_members_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="create_members failed"
    ):
        await create_members([{"AccountId": "123"}])


# ---------------------------------------------------------------------------
# delete_members
# ---------------------------------------------------------------------------


async def test_delete_members_success(mock_client):
    mock_client.call.return_value = {"UnprocessedAccounts": []}
    result = await delete_members(["123"])
    assert result == []


async def test_delete_members_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError, match="delete_members failed"
    ):
        await delete_members(["123"])


# ---------------------------------------------------------------------------
# get_administrator_account
# ---------------------------------------------------------------------------


async def test_get_administrator_account_success(mock_client):
    mock_client.call.return_value = {
        "Administrator": {
            "AccountId": "456",
            "InvitationId": "inv-1",
        }
    }
    result = await get_administrator_account()
    assert result["AccountId"] == "456"


async def test_get_administrator_account_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="get_administrator_account failed",
    ):
        await get_administrator_account()


# ---------------------------------------------------------------------------
# accept_administrator_invitation
# ---------------------------------------------------------------------------


async def test_accept_admin_invitation_success(mock_client):
    mock_client.call.return_value = {}
    await accept_administrator_invitation("456", "inv-1")
    mock_client.call.assert_called_once()


async def test_accept_admin_invitation_error(mock_client):
    mock_client.call.side_effect = ValueError("boom")
    with pytest.raises(
        RuntimeError,
        match="accept_administrator_invitation failed",
    ):
        await accept_administrator_invitation("456", "inv-1")


# ---------------------------------------------------------------------------
# __all__ re-exports
# ---------------------------------------------------------------------------


def test_all_exports():
    """Verify __all__ contains all expected symbols."""
    for name in mod.__all__:
            assert hasattr(mod, name), f"Missing export: {name}"


def test_models_reexported():
    """Verify models are re-exported from the sync module."""
    assert "HubResult" in mod.__all__
    assert "FindingResult" in mod.__all__
    assert "InsightResult" in mod.__all__
    assert "StandardResult" in mod.__all__
    assert "MemberResult" in mod.__all__


async def test_accept_invitation(mock_client):
    mock_client.call.return_value = {}
    await accept_invitation("test-master_id", "test-invitation_id", )
    mock_client.call.assert_called_once()


async def test_accept_invitation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await accept_invitation("test-master_id", "test-invitation_id", )


async def test_accept_invitation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to accept invitation"):
        await accept_invitation("test-master_id", "test-invitation_id", )


async def test_batch_delete_automation_rules(mock_client):
    mock_client.call.return_value = {}
    await batch_delete_automation_rules([], )
    mock_client.call.assert_called_once()


async def test_batch_delete_automation_rules_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_delete_automation_rules([], )


async def test_batch_delete_automation_rules_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch delete automation rules"):
        await batch_delete_automation_rules([], )


async def test_batch_get_automation_rules(mock_client):
    mock_client.call.return_value = {}
    await batch_get_automation_rules([], )
    mock_client.call.assert_called_once()


async def test_batch_get_automation_rules_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_automation_rules([], )


async def test_batch_get_automation_rules_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get automation rules"):
        await batch_get_automation_rules([], )


async def test_batch_get_configuration_policy_associations(mock_client):
    mock_client.call.return_value = {}
    await batch_get_configuration_policy_associations([], )
    mock_client.call.assert_called_once()


async def test_batch_get_configuration_policy_associations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_configuration_policy_associations([], )


async def test_batch_get_configuration_policy_associations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get configuration policy associations"):
        await batch_get_configuration_policy_associations([], )


async def test_batch_get_security_controls(mock_client):
    mock_client.call.return_value = {}
    await batch_get_security_controls([], )
    mock_client.call.assert_called_once()


async def test_batch_get_security_controls_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_security_controls([], )


async def test_batch_get_security_controls_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get security controls"):
        await batch_get_security_controls([], )


async def test_batch_get_standards_control_associations(mock_client):
    mock_client.call.return_value = {}
    await batch_get_standards_control_associations([], )
    mock_client.call.assert_called_once()


async def test_batch_get_standards_control_associations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_standards_control_associations([], )


async def test_batch_get_standards_control_associations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get standards control associations"):
        await batch_get_standards_control_associations([], )


async def test_batch_import_findings(mock_client):
    mock_client.call.return_value = {}
    await batch_import_findings([], )
    mock_client.call.assert_called_once()


async def test_batch_import_findings_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_import_findings([], )


async def test_batch_import_findings_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch import findings"):
        await batch_import_findings([], )


async def test_batch_update_automation_rules(mock_client):
    mock_client.call.return_value = {}
    await batch_update_automation_rules([], )
    mock_client.call.assert_called_once()


async def test_batch_update_automation_rules_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_automation_rules([], )


async def test_batch_update_automation_rules_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch update automation rules"):
        await batch_update_automation_rules([], )


async def test_batch_update_findings(mock_client):
    mock_client.call.return_value = {}
    await batch_update_findings([], )
    mock_client.call.assert_called_once()


async def test_batch_update_findings_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_findings([], )


async def test_batch_update_findings_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch update findings"):
        await batch_update_findings([], )


async def test_batch_update_findings_v2(mock_client):
    mock_client.call.return_value = {}
    await batch_update_findings_v2()
    mock_client.call.assert_called_once()


async def test_batch_update_findings_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_findings_v2()


async def test_batch_update_findings_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch update findings v2"):
        await batch_update_findings_v2()


async def test_batch_update_standards_control_associations(mock_client):
    mock_client.call.return_value = {}
    await batch_update_standards_control_associations([], )
    mock_client.call.assert_called_once()


async def test_batch_update_standards_control_associations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_standards_control_associations([], )


async def test_batch_update_standards_control_associations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch update standards control associations"):
        await batch_update_standards_control_associations([], )


async def test_connector_registrations_v2(mock_client):
    mock_client.call.return_value = {}
    await connector_registrations_v2("test-auth_code", "test-auth_state", )
    mock_client.call.assert_called_once()


async def test_connector_registrations_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await connector_registrations_v2("test-auth_code", "test-auth_state", )


async def test_connector_registrations_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to connector registrations v2"):
        await connector_registrations_v2("test-auth_code", "test-auth_state", )


async def test_create_action_target(mock_client):
    mock_client.call.return_value = {}
    await create_action_target("test-name", "test-description", "test-id", )
    mock_client.call.assert_called_once()


async def test_create_action_target_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_action_target("test-name", "test-description", "test-id", )


async def test_create_action_target_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create action target"):
        await create_action_target("test-name", "test-description", "test-id", )


async def test_create_aggregator_v2(mock_client):
    mock_client.call.return_value = {}
    await create_aggregator_v2("test-region_linking_mode", )
    mock_client.call.assert_called_once()


async def test_create_aggregator_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_aggregator_v2("test-region_linking_mode", )


async def test_create_aggregator_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create aggregator v2"):
        await create_aggregator_v2("test-region_linking_mode", )


async def test_create_automation_rule(mock_client):
    mock_client.call.return_value = {}
    await create_automation_rule(1, "test-rule_name", "test-description", {}, [], )
    mock_client.call.assert_called_once()


async def test_create_automation_rule_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_automation_rule(1, "test-rule_name", "test-description", {}, [], )


async def test_create_automation_rule_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create automation rule"):
        await create_automation_rule(1, "test-rule_name", "test-description", {}, [], )


async def test_create_automation_rule_v2(mock_client):
    mock_client.call.return_value = {}
    await create_automation_rule_v2("test-rule_name", "test-description", 1.0, {}, [], )
    mock_client.call.assert_called_once()


async def test_create_automation_rule_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_automation_rule_v2("test-rule_name", "test-description", 1.0, {}, [], )


async def test_create_automation_rule_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create automation rule v2"):
        await create_automation_rule_v2("test-rule_name", "test-description", 1.0, {}, [], )


async def test_create_configuration_policy(mock_client):
    mock_client.call.return_value = {}
    await create_configuration_policy("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_configuration_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_configuration_policy("test-name", {}, )


async def test_create_configuration_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create configuration policy"):
        await create_configuration_policy("test-name", {}, )


async def test_create_connector_v2(mock_client):
    mock_client.call.return_value = {}
    await create_connector_v2("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_connector_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_connector_v2("test-name", {}, )


async def test_create_connector_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create connector v2"):
        await create_connector_v2("test-name", {}, )


async def test_create_finding_aggregator(mock_client):
    mock_client.call.return_value = {}
    await create_finding_aggregator("test-region_linking_mode", )
    mock_client.call.assert_called_once()


async def test_create_finding_aggregator_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_finding_aggregator("test-region_linking_mode", )


async def test_create_finding_aggregator_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create finding aggregator"):
        await create_finding_aggregator("test-region_linking_mode", )


async def test_create_ticket_v2(mock_client):
    mock_client.call.return_value = {}
    await create_ticket_v2("test-connector_id", "test-finding_metadata_uid", )
    mock_client.call.assert_called_once()


async def test_create_ticket_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_ticket_v2("test-connector_id", "test-finding_metadata_uid", )


async def test_create_ticket_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create ticket v2"):
        await create_ticket_v2("test-connector_id", "test-finding_metadata_uid", )


async def test_decline_invitations(mock_client):
    mock_client.call.return_value = {}
    await decline_invitations([], )
    mock_client.call.assert_called_once()


async def test_decline_invitations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await decline_invitations([], )


async def test_decline_invitations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to decline invitations"):
        await decline_invitations([], )


async def test_delete_action_target(mock_client):
    mock_client.call.return_value = {}
    await delete_action_target("test-action_target_arn", )
    mock_client.call.assert_called_once()


async def test_delete_action_target_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_action_target("test-action_target_arn", )


async def test_delete_action_target_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete action target"):
        await delete_action_target("test-action_target_arn", )


async def test_delete_aggregator_v2(mock_client):
    mock_client.call.return_value = {}
    await delete_aggregator_v2("test-aggregator_v2_arn", )
    mock_client.call.assert_called_once()


async def test_delete_aggregator_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_aggregator_v2("test-aggregator_v2_arn", )


async def test_delete_aggregator_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete aggregator v2"):
        await delete_aggregator_v2("test-aggregator_v2_arn", )


async def test_delete_automation_rule_v2(mock_client):
    mock_client.call.return_value = {}
    await delete_automation_rule_v2("test-identifier", )
    mock_client.call.assert_called_once()


async def test_delete_automation_rule_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_automation_rule_v2("test-identifier", )


async def test_delete_automation_rule_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete automation rule v2"):
        await delete_automation_rule_v2("test-identifier", )


async def test_delete_configuration_policy(mock_client):
    mock_client.call.return_value = {}
    await delete_configuration_policy("test-identifier", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration_policy("test-identifier", )


async def test_delete_configuration_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete configuration policy"):
        await delete_configuration_policy("test-identifier", )


async def test_delete_connector_v2(mock_client):
    mock_client.call.return_value = {}
    await delete_connector_v2("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_delete_connector_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_connector_v2("test-connector_id", )


async def test_delete_connector_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete connector v2"):
        await delete_connector_v2("test-connector_id", )


async def test_delete_finding_aggregator(mock_client):
    mock_client.call.return_value = {}
    await delete_finding_aggregator("test-finding_aggregator_arn", )
    mock_client.call.assert_called_once()


async def test_delete_finding_aggregator_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_finding_aggregator("test-finding_aggregator_arn", )


async def test_delete_finding_aggregator_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete finding aggregator"):
        await delete_finding_aggregator("test-finding_aggregator_arn", )


async def test_delete_invitations(mock_client):
    mock_client.call.return_value = {}
    await delete_invitations([], )
    mock_client.call.assert_called_once()


async def test_delete_invitations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_invitations([], )


async def test_delete_invitations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete invitations"):
        await delete_invitations([], )


async def test_describe_action_targets(mock_client):
    mock_client.call.return_value = {}
    await describe_action_targets()
    mock_client.call.assert_called_once()


async def test_describe_action_targets_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_action_targets()


async def test_describe_action_targets_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe action targets"):
        await describe_action_targets()


async def test_describe_organization_configuration(mock_client):
    mock_client.call.return_value = {}
    await describe_organization_configuration()
    mock_client.call.assert_called_once()


async def test_describe_organization_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_configuration()


async def test_describe_organization_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe organization configuration"):
        await describe_organization_configuration()


async def test_describe_products(mock_client):
    mock_client.call.return_value = {}
    await describe_products()
    mock_client.call.assert_called_once()


async def test_describe_products_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_products()


async def test_describe_products_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe products"):
        await describe_products()


async def test_describe_products_v2(mock_client):
    mock_client.call.return_value = {}
    await describe_products_v2()
    mock_client.call.assert_called_once()


async def test_describe_products_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_products_v2()


async def test_describe_products_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe products v2"):
        await describe_products_v2()


async def test_describe_security_hub_v2(mock_client):
    mock_client.call.return_value = {}
    await describe_security_hub_v2()
    mock_client.call.assert_called_once()


async def test_describe_security_hub_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_security_hub_v2()


async def test_describe_security_hub_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe security hub v2"):
        await describe_security_hub_v2()


async def test_disable_organization_admin_account(mock_client):
    mock_client.call.return_value = {}
    await disable_organization_admin_account("test-admin_account_id", )
    mock_client.call.assert_called_once()


async def test_disable_organization_admin_account_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disable_organization_admin_account("test-admin_account_id", )


async def test_disable_organization_admin_account_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disable organization admin account"):
        await disable_organization_admin_account("test-admin_account_id", )


async def test_disable_security_hub_v2(mock_client):
    mock_client.call.return_value = {}
    await disable_security_hub_v2()
    mock_client.call.assert_called_once()


async def test_disable_security_hub_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disable_security_hub_v2()


async def test_disable_security_hub_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disable security hub v2"):
        await disable_security_hub_v2()


async def test_disassociate_from_administrator_account(mock_client):
    mock_client.call.return_value = {}
    await disassociate_from_administrator_account()
    mock_client.call.assert_called_once()


async def test_disassociate_from_administrator_account_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_from_administrator_account()


async def test_disassociate_from_administrator_account_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disassociate from administrator account"):
        await disassociate_from_administrator_account()


async def test_disassociate_from_master_account(mock_client):
    mock_client.call.return_value = {}
    await disassociate_from_master_account()
    mock_client.call.assert_called_once()


async def test_disassociate_from_master_account_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_from_master_account()


async def test_disassociate_from_master_account_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disassociate from master account"):
        await disassociate_from_master_account()


async def test_disassociate_members(mock_client):
    mock_client.call.return_value = {}
    await disassociate_members([], )
    mock_client.call.assert_called_once()


async def test_disassociate_members_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_members([], )


async def test_disassociate_members_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to disassociate members"):
        await disassociate_members([], )


async def test_enable_organization_admin_account(mock_client):
    mock_client.call.return_value = {}
    await enable_organization_admin_account("test-admin_account_id", )
    mock_client.call.assert_called_once()


async def test_enable_organization_admin_account_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await enable_organization_admin_account("test-admin_account_id", )


async def test_enable_organization_admin_account_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to enable organization admin account"):
        await enable_organization_admin_account("test-admin_account_id", )


async def test_enable_security_hub_v2(mock_client):
    mock_client.call.return_value = {}
    await enable_security_hub_v2()
    mock_client.call.assert_called_once()


async def test_enable_security_hub_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await enable_security_hub_v2()


async def test_enable_security_hub_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to enable security hub v2"):
        await enable_security_hub_v2()


async def test_get_aggregator_v2(mock_client):
    mock_client.call.return_value = {}
    await get_aggregator_v2("test-aggregator_v2_arn", )
    mock_client.call.assert_called_once()


async def test_get_aggregator_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_aggregator_v2("test-aggregator_v2_arn", )


async def test_get_aggregator_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get aggregator v2"):
        await get_aggregator_v2("test-aggregator_v2_arn", )


async def test_get_automation_rule_v2(mock_client):
    mock_client.call.return_value = {}
    await get_automation_rule_v2("test-identifier", )
    mock_client.call.assert_called_once()


async def test_get_automation_rule_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_automation_rule_v2("test-identifier", )


async def test_get_automation_rule_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get automation rule v2"):
        await get_automation_rule_v2("test-identifier", )


async def test_get_configuration_policy(mock_client):
    mock_client.call.return_value = {}
    await get_configuration_policy("test-identifier", )
    mock_client.call.assert_called_once()


async def test_get_configuration_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_configuration_policy("test-identifier", )


async def test_get_configuration_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get configuration policy"):
        await get_configuration_policy("test-identifier", )


async def test_get_configuration_policy_association(mock_client):
    mock_client.call.return_value = {}
    await get_configuration_policy_association({}, )
    mock_client.call.assert_called_once()


async def test_get_configuration_policy_association_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_configuration_policy_association({}, )


async def test_get_configuration_policy_association_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get configuration policy association"):
        await get_configuration_policy_association({}, )


async def test_get_connector_v2(mock_client):
    mock_client.call.return_value = {}
    await get_connector_v2("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_get_connector_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_connector_v2("test-connector_id", )


async def test_get_connector_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get connector v2"):
        await get_connector_v2("test-connector_id", )


async def test_get_finding_aggregator(mock_client):
    mock_client.call.return_value = {}
    await get_finding_aggregator("test-finding_aggregator_arn", )
    mock_client.call.assert_called_once()


async def test_get_finding_aggregator_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_finding_aggregator("test-finding_aggregator_arn", )


async def test_get_finding_aggregator_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get finding aggregator"):
        await get_finding_aggregator("test-finding_aggregator_arn", )


async def test_get_finding_history(mock_client):
    mock_client.call.return_value = {}
    await get_finding_history({}, )
    mock_client.call.assert_called_once()


async def test_get_finding_history_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_finding_history({}, )


async def test_get_finding_history_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get finding history"):
        await get_finding_history({}, )


async def test_get_finding_statistics_v2(mock_client):
    mock_client.call.return_value = {}
    await get_finding_statistics_v2([], )
    mock_client.call.assert_called_once()


async def test_get_finding_statistics_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_finding_statistics_v2([], )


async def test_get_finding_statistics_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get finding statistics v2"):
        await get_finding_statistics_v2([], )


async def test_get_findings_v2(mock_client):
    mock_client.call.return_value = {}
    await get_findings_v2()
    mock_client.call.assert_called_once()


async def test_get_findings_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_findings_v2()


async def test_get_findings_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get findings v2"):
        await get_findings_v2()


async def test_get_insights(mock_client):
    mock_client.call.return_value = {}
    await get_insights()
    mock_client.call.assert_called_once()


async def test_get_insights_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_insights()


async def test_get_insights_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get insights"):
        await get_insights()


async def test_get_invitations_count(mock_client):
    mock_client.call.return_value = {}
    await get_invitations_count()
    mock_client.call.assert_called_once()


async def test_get_invitations_count_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_invitations_count()


async def test_get_invitations_count_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get invitations count"):
        await get_invitations_count()


async def test_get_master_account(mock_client):
    mock_client.call.return_value = {}
    await get_master_account()
    mock_client.call.assert_called_once()


async def test_get_master_account_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_master_account()


async def test_get_master_account_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get master account"):
        await get_master_account()


async def test_get_resources_statistics_v2(mock_client):
    mock_client.call.return_value = {}
    await get_resources_statistics_v2([], )
    mock_client.call.assert_called_once()


async def test_get_resources_statistics_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_resources_statistics_v2([], )


async def test_get_resources_statistics_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get resources statistics v2"):
        await get_resources_statistics_v2([], )


async def test_get_resources_v2(mock_client):
    mock_client.call.return_value = {}
    await get_resources_v2()
    mock_client.call.assert_called_once()


async def test_get_resources_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_resources_v2()


async def test_get_resources_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get resources v2"):
        await get_resources_v2()


async def test_get_security_control_definition(mock_client):
    mock_client.call.return_value = {}
    await get_security_control_definition("test-security_control_id", )
    mock_client.call.assert_called_once()


async def test_get_security_control_definition_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_security_control_definition("test-security_control_id", )


async def test_get_security_control_definition_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get security control definition"):
        await get_security_control_definition("test-security_control_id", )


async def test_list_aggregators_v2(mock_client):
    mock_client.call.return_value = {}
    await list_aggregators_v2()
    mock_client.call.assert_called_once()


async def test_list_aggregators_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_aggregators_v2()


async def test_list_aggregators_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list aggregators v2"):
        await list_aggregators_v2()


async def test_list_automation_rules(mock_client):
    mock_client.call.return_value = {}
    await list_automation_rules()
    mock_client.call.assert_called_once()


async def test_list_automation_rules_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_automation_rules()


async def test_list_automation_rules_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list automation rules"):
        await list_automation_rules()


async def test_list_automation_rules_v2(mock_client):
    mock_client.call.return_value = {}
    await list_automation_rules_v2()
    mock_client.call.assert_called_once()


async def test_list_automation_rules_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_automation_rules_v2()


async def test_list_automation_rules_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list automation rules v2"):
        await list_automation_rules_v2()


async def test_list_configuration_policies(mock_client):
    mock_client.call.return_value = {}
    await list_configuration_policies()
    mock_client.call.assert_called_once()


async def test_list_configuration_policies_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_configuration_policies()


async def test_list_configuration_policies_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list configuration policies"):
        await list_configuration_policies()


async def test_list_configuration_policy_associations(mock_client):
    mock_client.call.return_value = {}
    await list_configuration_policy_associations()
    mock_client.call.assert_called_once()


async def test_list_configuration_policy_associations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_configuration_policy_associations()


async def test_list_configuration_policy_associations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list configuration policy associations"):
        await list_configuration_policy_associations()


async def test_list_connectors_v2(mock_client):
    mock_client.call.return_value = {}
    await list_connectors_v2()
    mock_client.call.assert_called_once()


async def test_list_connectors_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_connectors_v2()


async def test_list_connectors_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list connectors v2"):
        await list_connectors_v2()


async def test_list_finding_aggregators(mock_client):
    mock_client.call.return_value = {}
    await list_finding_aggregators()
    mock_client.call.assert_called_once()


async def test_list_finding_aggregators_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_finding_aggregators()


async def test_list_finding_aggregators_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list finding aggregators"):
        await list_finding_aggregators()


async def test_list_invitations(mock_client):
    mock_client.call.return_value = {}
    await list_invitations()
    mock_client.call.assert_called_once()


async def test_list_invitations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_invitations()


async def test_list_invitations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list invitations"):
        await list_invitations()


async def test_list_organization_admin_accounts(mock_client):
    mock_client.call.return_value = {}
    await list_organization_admin_accounts()
    mock_client.call.assert_called_once()


async def test_list_organization_admin_accounts_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_organization_admin_accounts()


async def test_list_organization_admin_accounts_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list organization admin accounts"):
        await list_organization_admin_accounts()


async def test_list_security_control_definitions(mock_client):
    mock_client.call.return_value = {}
    await list_security_control_definitions()
    mock_client.call.assert_called_once()


async def test_list_security_control_definitions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_security_control_definitions()


async def test_list_security_control_definitions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list security control definitions"):
        await list_security_control_definitions()


async def test_list_standards_control_associations(mock_client):
    mock_client.call.return_value = {}
    await list_standards_control_associations("test-security_control_id", )
    mock_client.call.assert_called_once()


async def test_list_standards_control_associations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_standards_control_associations("test-security_control_id", )


async def test_list_standards_control_associations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list standards control associations"):
        await list_standards_control_associations("test-security_control_id", )


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


async def test_start_configuration_policy_association(mock_client):
    mock_client.call.return_value = {}
    await start_configuration_policy_association("test-configuration_policy_identifier", {}, )
    mock_client.call.assert_called_once()


async def test_start_configuration_policy_association_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_configuration_policy_association("test-configuration_policy_identifier", {}, )


async def test_start_configuration_policy_association_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start configuration policy association"):
        await start_configuration_policy_association("test-configuration_policy_identifier", {}, )


async def test_start_configuration_policy_disassociation(mock_client):
    mock_client.call.return_value = {}
    await start_configuration_policy_disassociation("test-configuration_policy_identifier", )
    mock_client.call.assert_called_once()


async def test_start_configuration_policy_disassociation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_configuration_policy_disassociation("test-configuration_policy_identifier", )


async def test_start_configuration_policy_disassociation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start configuration policy disassociation"):
        await start_configuration_policy_disassociation("test-configuration_policy_identifier", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", {}, )


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


async def test_update_action_target(mock_client):
    mock_client.call.return_value = {}
    await update_action_target("test-action_target_arn", )
    mock_client.call.assert_called_once()


async def test_update_action_target_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_action_target("test-action_target_arn", )


async def test_update_action_target_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update action target"):
        await update_action_target("test-action_target_arn", )


async def test_update_aggregator_v2(mock_client):
    mock_client.call.return_value = {}
    await update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", )
    mock_client.call.assert_called_once()


async def test_update_aggregator_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", )


async def test_update_aggregator_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update aggregator v2"):
        await update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", )


async def test_update_automation_rule_v2(mock_client):
    mock_client.call.return_value = {}
    await update_automation_rule_v2("test-identifier", )
    mock_client.call.assert_called_once()


async def test_update_automation_rule_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_automation_rule_v2("test-identifier", )


async def test_update_automation_rule_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update automation rule v2"):
        await update_automation_rule_v2("test-identifier", )


async def test_update_configuration_policy(mock_client):
    mock_client.call.return_value = {}
    await update_configuration_policy("test-identifier", )
    mock_client.call.assert_called_once()


async def test_update_configuration_policy_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration_policy("test-identifier", )


async def test_update_configuration_policy_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update configuration policy"):
        await update_configuration_policy("test-identifier", )


async def test_update_connector_v2(mock_client):
    mock_client.call.return_value = {}
    await update_connector_v2("test-connector_id", )
    mock_client.call.assert_called_once()


async def test_update_connector_v2_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_connector_v2("test-connector_id", )


async def test_update_connector_v2_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update connector v2"):
        await update_connector_v2("test-connector_id", )


async def test_update_finding_aggregator(mock_client):
    mock_client.call.return_value = {}
    await update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", )
    mock_client.call.assert_called_once()


async def test_update_finding_aggregator_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", )


async def test_update_finding_aggregator_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update finding aggregator"):
        await update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", )


async def test_update_organization_configuration(mock_client):
    mock_client.call.return_value = {}
    await update_organization_configuration(True, )
    mock_client.call.assert_called_once()


async def test_update_organization_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_organization_configuration(True, )


async def test_update_organization_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update organization configuration"):
        await update_organization_configuration(True, )


async def test_update_security_control(mock_client):
    mock_client.call.return_value = {}
    await update_security_control("test-security_control_id", {}, )
    mock_client.call.assert_called_once()


async def test_update_security_control_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_security_control("test-security_control_id", {}, )


async def test_update_security_control_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update security control"):
        await update_security_control("test-security_control_id", {}, )


async def test_update_security_hub_configuration(mock_client):
    mock_client.call.return_value = {}
    await update_security_hub_configuration()
    mock_client.call.assert_called_once()


async def test_update_security_hub_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_security_hub_configuration()


async def test_update_security_hub_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update security hub configuration"):
        await update_security_hub_configuration()


@pytest.mark.asyncio
async def test_get_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_findings(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_insights_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_insights
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_insights(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_insight_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_insight
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_insight("test-insight_arn", name="test-name", filters=[{}], group_by_attribute="test-group_by_attribute", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_update_findings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import batch_update_findings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await batch_update_findings("test-finding_identifiers", note="test-note", severity="test-severity", verification_state="test-verification_state", confidence="test-confidence", criticality="test-criticality", types="test-types", user_defined_fields="test-user_defined_fields", workflow="test-workflow", related_findings="test-related_findings", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_update_findings_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import batch_update_findings_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await batch_update_findings_v2(metadata_uids="test-metadata_uids", finding_identifiers="test-finding_identifiers", comment="test-comment", severity_id="test-severity_id", status_id="test-status_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_aggregator_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_aggregator_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_aggregator_v2("test-region_linking_mode", linked_regions="test-linked_regions", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_automation_rule_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_automation_rule
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_automation_rule("test-rule_order", "test-rule_name", "test-description", "test-criteria", "test-actions", tags=[{"Key": "k", "Value": "v"}], rule_status="test-rule_status", is_terminal=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_automation_rule_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_automation_rule_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_automation_rule_v2("test-rule_name", "test-description", "test-rule_order", "test-criteria", "test-actions", rule_status="test-rule_status", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_configuration_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_configuration_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_configuration_policy("test-name", "{}", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_connector_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_connector_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_connector_v2("test-name", "test-provider", description="test-description", kms_key_arn="test-kms_key_arn", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_finding_aggregator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_finding_aggregator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_finding_aggregator("test-region_linking_mode", regions="test-regions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_ticket_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import create_ticket_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await create_ticket_v2("test-connector_id", "test-finding_metadata_uid", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_action_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import describe_action_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await describe_action_targets(action_target_arns="test-action_target_arns", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_products_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import describe_products
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await describe_products(next_token="test-next_token", max_results=1, product_arn="test-product_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_products_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import describe_products_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await describe_products_v2(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_organization_admin_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import disable_organization_admin_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await disable_organization_admin_account(1, feature="test-feature", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_organization_admin_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import enable_organization_admin_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await enable_organization_admin_account(1, feature="test-feature", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_security_hub_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import enable_security_hub_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await enable_security_hub_v2(tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_finding_history_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_finding_history
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_finding_history("test-finding_identifier", start_time="test-start_time", end_time="test-end_time", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_finding_statistics_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_finding_statistics_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_finding_statistics_v2("test-group_by_rules", sort_order="test-sort_order", max_statistic_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_findings_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_findings_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_findings_v2(filters=[{}], sort_criteria="test-sort_criteria", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_insights_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_insights
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_insights(insight_arns="test-insight_arns", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_resources_statistics_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_resources_statistics_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_resources_statistics_v2("test-group_by_rules", sort_order="test-sort_order", max_statistic_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_resources_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import get_resources_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await get_resources_v2(filters=[{}], sort_criteria="test-sort_criteria", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aggregators_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_aggregators_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_aggregators_v2(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_automation_rules_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_automation_rules
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_automation_rules(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_automation_rules_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_automation_rules_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_automation_rules_v2(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_configuration_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_configuration_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_configuration_policies(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_configuration_policy_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_configuration_policy_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_configuration_policy_associations(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_connectors_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_connectors_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_connectors_v2(next_token="test-next_token", max_results=1, provider_name="test-provider_name", connector_status="test-connector_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_finding_aggregators_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_finding_aggregators
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_finding_aggregators(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_invitations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_invitations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_invitations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_organization_admin_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_organization_admin_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_organization_admin_accounts(max_results=1, next_token="test-next_token", feature="test-feature", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_security_control_definitions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_security_control_definitions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_security_control_definitions(standards_arn="test-standards_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_standards_control_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import list_standards_control_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await list_standards_control_associations("test-security_control_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_configuration_policy_disassociation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import start_configuration_policy_disassociation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await start_configuration_policy_disassociation({}, target="test-target", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_action_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_action_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_action_target("test-action_target_arn", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_aggregator_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_aggregator_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", linked_regions="test-linked_regions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_automation_rule_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_automation_rule_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_automation_rule_v2("test-identifier", rule_status="test-rule_status", rule_order="test-rule_order", description="test-description", rule_name="test-rule_name", criteria="test-criteria", actions="test-actions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_configuration_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_configuration_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_configuration_policy("test-identifier", name="test-name", description="test-description", updated_reason="test-updated_reason", configuration_policy="{}", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_connector_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_connector_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_connector_v2("test-connector_id", client_secret="test-client_secret", description="test-description", provider="test-provider", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_finding_aggregator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_finding_aggregator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", regions="test-regions", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_organization_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_organization_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_organization_configuration(True, auto_enable_standards=True, organization_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_control_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_security_control
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_security_control("test-security_control_id", "test-parameters", last_update_reason="test-last_update_reason", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_hub_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.security_hub import update_security_hub_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.security_hub.async_client", lambda *a, **kw: mock_client)
    await update_security_hub_configuration(auto_enable_controls=True, control_finding_generator="test-control_finding_generator", region_name="us-east-1")
    mock_client.call.assert_called_once()
