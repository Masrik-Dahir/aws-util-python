"""Tests for aws_util.security_hub module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.security_hub as mod
from aws_util.security_hub import (
    FindingResult,
    HubResult,
    InsightResult,
    MemberResult,
    StandardResult,
    _parse_finding,
    _parse_member,
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
# Helpers
# ---------------------------------------------------------------------------


def _client_error(
    code: str = "InternalError", message: str = "boom"
) -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": message}},
        "TestOp",
    )


def _mock_paginator(pages: list[dict]) -> MagicMock:
    """Return a mock client whose paginator yields given pages."""
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = iter(pages)
    mock.get_paginator.return_value = paginator
    return mock


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_hub_result_defaults(self):
        r = HubResult()
        assert r.hub_arn is None
        assert r.subscribed_at is None
        assert r.auto_enable_controls is True
        assert r.extra == {}

    def test_hub_result_frozen(self):
        r = HubResult(hub_arn="arn:hub")
        with pytest.raises(Exception):
            r.hub_arn = "other"  # type: ignore[misc]

    def test_finding_result_defaults(self):
        r = FindingResult()
        assert r.finding_id == ""
        assert r.product_arn == ""
        assert r.generator_id == ""
        assert r.aws_account_id == ""
        assert r.title == ""
        assert r.description == ""
        assert r.severity_label == ""
        assert r.workflow_status == ""
        assert r.record_state == ""
        assert r.extra == {}

    def test_finding_result_frozen(self):
        r = FindingResult(finding_id="f-1")
        with pytest.raises(Exception):
            r.finding_id = "other"  # type: ignore[misc]

    def test_insight_result_defaults(self):
        r = InsightResult()
        assert r.insight_arn == ""
        assert r.name == ""
        assert r.filters == {}
        assert r.group_by_attribute == ""
        assert r.extra == {}

    def test_standard_result_defaults(self):
        r = StandardResult()
        assert r.standards_arn is None
        assert r.standards_subscription_arn is None
        assert r.standards_status is None
        assert r.name == ""
        assert r.description == ""
        assert r.extra == {}

    def test_member_result_defaults(self):
        r = MemberResult()
        assert r.account_id == ""
        assert r.email == ""
        assert r.member_status == ""
        assert r.invited_at is None
        assert r.updated_at is None
        assert r.administrator_id is None
        assert r.extra == {}

    def test_member_result_full(self):
        r = MemberResult(
            account_id="123",
            email="a@b.com",
            member_status="Associated",
            invited_at="2025-01-01",
            updated_at="2025-01-02",
            administrator_id="456",
            extra={"Foo": "bar"},
        )
        assert r.account_id == "123"
        assert r.administrator_id == "456"


# ---------------------------------------------------------------------------
# _parse_finding / _parse_member
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_finding_full(self):
        raw = {
            "Id": "f-1",
            "ProductArn": "arn:product",
            "GeneratorId": "gen-1",
            "AwsAccountId": "123",
            "Title": "Test",
            "Description": "desc",
            "Severity": {"Label": "HIGH"},
            "Workflow": {"Status": "NEW"},
            "RecordState": "ACTIVE",
            "Extra": "val",
        }
        r = _parse_finding(raw)
        assert r.finding_id == "f-1"
        assert r.severity_label == "HIGH"
        assert r.workflow_status == "NEW"
        assert r.extra == {"Extra": "val"}

    def test_parse_finding_minimal(self):
        r = _parse_finding({})
        assert r.finding_id == ""
        assert r.severity_label == ""
        assert r.workflow_status == ""

    def test_parse_member_full(self):
        raw = {
            "AccountId": "123",
            "Email": "a@b.com",
            "MemberStatus": "Associated",
            "InvitedAt": "2025-01-01T00:00:00Z",
            "UpdatedAt": "2025-01-02T00:00:00Z",
            "AdministratorId": "456",
            "Extra": "val",
        }
        r = _parse_member(raw)
        assert r.account_id == "123"
        assert r.invited_at is not None
        assert r.updated_at is not None
        assert r.extra == {"Extra": "val"}

    def test_parse_member_minimal(self):
        r = _parse_member({})
        assert r.account_id == ""
        assert r.invited_at is None
        assert r.updated_at is None


# ---------------------------------------------------------------------------
# enable_security_hub
# ---------------------------------------------------------------------------


class TestEnableSecurityHub:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.enable_security_hub.return_value = {
            "HubArn": "arn:hub"
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = enable_security_hub(region_name=REGION)
        assert result == "arn:hub"

    def test_with_tags(self, monkeypatch):
        mock = MagicMock()
        mock.enable_security_hub.return_value = {
            "HubArn": "arn:hub"
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        enable_security_hub(
            tags={"env": "prod"}, region_name=REGION
        )
        call_kwargs = mock.enable_security_hub.call_args[1]
        assert call_kwargs["Tags"] == {"env": "prod"}

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.enable_security_hub.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="enable_security_hub failed"
        ):
            enable_security_hub(region_name=REGION)


# ---------------------------------------------------------------------------
# disable_security_hub
# ---------------------------------------------------------------------------


class TestDisableSecurityHub:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.disable_security_hub.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        disable_security_hub(region_name=REGION)
        mock.disable_security_hub.assert_called_once()

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.disable_security_hub.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="disable_security_hub failed"
        ):
            disable_security_hub(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_hub
# ---------------------------------------------------------------------------


class TestDescribeHub:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.describe_hub.return_value = {
            "HubArn": "arn:hub",
            "SubscribedAt": "2025-01-01",
            "AutoEnableControls": False,
            "ResponseMetadata": {},
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_hub(region_name=REGION)
        assert result.hub_arn == "arn:hub"
        assert result.auto_enable_controls is False

    def test_with_hub_arn(self, monkeypatch):
        mock = MagicMock()
        mock.describe_hub.return_value = {
            "HubArn": "arn:hub",
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        describe_hub(hub_arn="arn:hub", region_name=REGION)
        call_kwargs = mock.describe_hub.call_args[1]
        assert call_kwargs["HubArn"] == "arn:hub"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_hub.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="describe_hub failed"
        ):
            describe_hub(region_name=REGION)

    def test_extra_fields(self, monkeypatch):
        mock = MagicMock()
        mock.describe_hub.return_value = {
            "HubArn": "arn:hub",
            "CustomField": "custom",
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_hub(region_name=REGION)
        assert result.extra["CustomField"] == "custom"


# ---------------------------------------------------------------------------
# get_findings
# ---------------------------------------------------------------------------


class TestGetFindings:
    def test_empty(self, monkeypatch):
        mock = _mock_paginator([{"Findings": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_findings(region_name=REGION)
        assert result == []

    def test_with_results(self, monkeypatch):
        mock = _mock_paginator([
            {
                "Findings": [
                    {
                        "Id": "f-1",
                        "ProductArn": "arn:p",
                        "Severity": {"Label": "MEDIUM"},
                        "Workflow": {"Status": "NEW"},
                    }
                ]
            }
        ])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_findings(region_name=REGION)
        assert len(result) == 1
        assert result[0].finding_id == "f-1"

    def test_with_filters(self, monkeypatch):
        mock = _mock_paginator([{"Findings": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        get_findings(
            filters={"SeverityLabel": [{"Value": "HIGH"}]},
            region_name=REGION,
        )

    def test_with_sort_criteria(self, monkeypatch):
        mock = _mock_paginator([{"Findings": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        get_findings(
            sort_criteria=[{"Field": "Title", "SortOrder": "asc"}],
            region_name=REGION,
        )

    def test_with_max_results(self, monkeypatch):
        mock = _mock_paginator([{"Findings": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        get_findings(max_results=10, region_name=REGION)

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_findings failed"
        ):
            get_findings(region_name=REGION)


# ---------------------------------------------------------------------------
# update_findings
# ---------------------------------------------------------------------------


class TestUpdateFindings:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.batch_update_findings.return_value = {
            "ProcessedFindings": [{"Id": "f-1"}],
            "UnprocessedFindings": [],
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = update_findings(
            [{"Id": "f-1", "ProductArn": "arn:p"}],
            region_name=REGION,
        )
        assert len(result["ProcessedFindings"]) == 1

    def test_with_note(self, monkeypatch):
        mock = MagicMock()
        mock.batch_update_findings.return_value = {
            "ProcessedFindings": [],
            "UnprocessedFindings": [],
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_findings(
            [{"Id": "f-1", "ProductArn": "arn:p"}],
            note={"Text": "note", "UpdatedBy": "user"},
            region_name=REGION,
        )
        call_kwargs = mock.batch_update_findings.call_args[1]
        assert "Note" in call_kwargs

    def test_with_severity(self, monkeypatch):
        mock = MagicMock()
        mock.batch_update_findings.return_value = {
            "ProcessedFindings": [],
            "UnprocessedFindings": [],
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_findings(
            [{"Id": "f-1", "ProductArn": "arn:p"}],
            severity={"Label": "LOW"},
            region_name=REGION,
        )

    def test_with_workflow(self, monkeypatch):
        mock = MagicMock()
        mock.batch_update_findings.return_value = {
            "ProcessedFindings": [],
            "UnprocessedFindings": [],
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_findings(
            [{"Id": "f-1", "ProductArn": "arn:p"}],
            workflow={"Status": "RESOLVED"},
            region_name=REGION,
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.batch_update_findings.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="update_findings failed"
        ):
            update_findings(
                [{"Id": "f-1", "ProductArn": "arn:p"}],
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# get_insight_results
# ---------------------------------------------------------------------------


class TestGetInsightResults:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.get_insight_results.return_value = {
            "InsightResults": {"InsightArn": "arn:i", "ResultValues": []}
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_insight_results(
            "arn:i", region_name=REGION
        )
        assert result["InsightArn"] == "arn:i"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_insight_results.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_insight_results failed"
        ):
            get_insight_results("arn:i", region_name=REGION)


# ---------------------------------------------------------------------------
# list_insights
# ---------------------------------------------------------------------------


class TestListInsights:
    def test_empty(self, monkeypatch):
        mock = _mock_paginator([{"Insights": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_insights(region_name=REGION)
        assert result == []

    def test_with_results(self, monkeypatch):
        mock = _mock_paginator([
            {
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
        ])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_insights(region_name=REGION)
        assert len(result) == 1
        assert result[0].name == "My Insight"
        assert result[0].extra == {"Extra": "val"}

    def test_with_max_results(self, monkeypatch):
        mock = _mock_paginator([{"Insights": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        list_insights(max_results=5, region_name=REGION)

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_insights failed"
        ):
            list_insights(region_name=REGION)


# ---------------------------------------------------------------------------
# create_insight
# ---------------------------------------------------------------------------


class TestCreateInsight:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.create_insight.return_value = {
            "InsightArn": "arn:new-insight"
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        arn = create_insight(
            "test",
            filters={"f": "v"},
            group_by_attribute="ResourceId",
            region_name=REGION,
        )
        assert arn == "arn:new-insight"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.create_insight.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="create_insight failed"
        ):
            create_insight(
                "test",
                filters={},
                group_by_attribute="ResourceId",
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# update_insight
# ---------------------------------------------------------------------------


class TestUpdateInsight:
    def test_success_name(self, monkeypatch):
        mock = MagicMock()
        mock.update_insight.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_insight(
            "arn:i", name="New Name", region_name=REGION
        )
        call_kwargs = mock.update_insight.call_args[1]
        assert call_kwargs["Name"] == "New Name"

    def test_success_filters(self, monkeypatch):
        mock = MagicMock()
        mock.update_insight.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_insight(
            "arn:i",
            filters={"f": "v"},
            region_name=REGION,
        )

    def test_success_group_by(self, monkeypatch):
        mock = MagicMock()
        mock.update_insight.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_insight(
            "arn:i",
            group_by_attribute="AccountId",
            region_name=REGION,
        )

    def test_no_optional_params(self, monkeypatch):
        mock = MagicMock()
        mock.update_insight.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_insight("arn:i", region_name=REGION)
        call_kwargs = mock.update_insight.call_args[1]
        assert "Name" not in call_kwargs
        assert "Filters" not in call_kwargs
        assert "GroupByAttribute" not in call_kwargs

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.update_insight.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="update_insight failed"
        ):
            update_insight("arn:i", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_insight
# ---------------------------------------------------------------------------


class TestDeleteInsight:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.delete_insight.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        delete_insight("arn:i", region_name=REGION)
        mock.delete_insight.assert_called_once()

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.delete_insight.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="delete_insight failed"
        ):
            delete_insight("arn:i", region_name=REGION)


# ---------------------------------------------------------------------------
# enable_import_findings_for_product
# ---------------------------------------------------------------------------


class TestEnableImportFindings:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.enable_import_findings_for_product.return_value = {
            "ProductSubscriptionArn": "arn:sub"
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = enable_import_findings_for_product(
            "arn:product", region_name=REGION
        )
        assert result == "arn:sub"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.enable_import_findings_for_product.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="enable_import_findings_for_product failed",
        ):
            enable_import_findings_for_product(
                "arn:product", region_name=REGION
            )


# ---------------------------------------------------------------------------
# disable_import_findings_for_product
# ---------------------------------------------------------------------------


class TestDisableImportFindings:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.disable_import_findings_for_product.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        disable_import_findings_for_product(
            "arn:sub", region_name=REGION
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.disable_import_findings_for_product.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="disable_import_findings_for_product failed",
        ):
            disable_import_findings_for_product(
                "arn:sub", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_enabled_products_for_import
# ---------------------------------------------------------------------------


class TestListEnabledProducts:
    def test_empty(self, monkeypatch):
        mock = MagicMock()
        mock.list_enabled_products_for_import.return_value = {
            "ProductSubscriptions": []
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_enabled_products_for_import(
            region_name=REGION
        )
        assert result == []

    def test_with_results(self, monkeypatch):
        mock = MagicMock()
        mock.list_enabled_products_for_import.return_value = {
            "ProductSubscriptions": ["arn:sub1", "arn:sub2"]
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_enabled_products_for_import(
            region_name=REGION
        )
        assert len(result) == 2

    def test_pagination(self, monkeypatch):
        mock = MagicMock()
        mock.list_enabled_products_for_import.side_effect = [
            {
                "ProductSubscriptions": ["arn:sub1"],
                "NextToken": "tok1",
            },
            {"ProductSubscriptions": ["arn:sub2"]},
        ]
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_enabled_products_for_import(
            region_name=REGION
        )
        assert len(result) == 2

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.list_enabled_products_for_import.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="list_enabled_products_for_import failed",
        ):
            list_enabled_products_for_import(region_name=REGION)


# ---------------------------------------------------------------------------
# get_enabled_standards
# ---------------------------------------------------------------------------


class TestGetEnabledStandards:
    def test_empty(self, monkeypatch):
        mock = _mock_paginator(
            [{"StandardsSubscriptions": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_enabled_standards(region_name=REGION)
        assert result == []

    def test_with_results(self, monkeypatch):
        mock = _mock_paginator([
            {
                "StandardsSubscriptions": [
                    {
                        "StandardsArn": "arn:std",
                        "StandardsSubscriptionArn": "arn:sub",
                        "StandardsStatus": "READY",
                        "Extra": "val",
                    }
                ]
            }
        ])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_enabled_standards(region_name=REGION)
        assert len(result) == 1
        assert result[0].standards_arn == "arn:std"
        assert result[0].extra == {"Extra": "val"}

    def test_with_filter(self, monkeypatch):
        mock = _mock_paginator(
            [{"StandardsSubscriptions": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        get_enabled_standards(
            standards_subscription_arns=["arn:sub"],
            region_name=REGION,
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="get_enabled_standards failed",
        ):
            get_enabled_standards(region_name=REGION)


# ---------------------------------------------------------------------------
# batch_enable_standards
# ---------------------------------------------------------------------------


class TestBatchEnableStandards:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.batch_enable_standards.return_value = {
            "StandardsSubscriptions": [
                {
                    "StandardsArn": "arn:std",
                    "StandardsSubscriptionArn": "arn:sub",
                    "StandardsStatus": "READY",
                    "Extra": "val",
                }
            ]
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = batch_enable_standards(
            [{"StandardsArn": "arn:std"}],
            region_name=REGION,
        )
        assert len(result) == 1
        assert result[0].standards_status == "READY"
        assert result[0].extra == {"Extra": "val"}

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.batch_enable_standards.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="batch_enable_standards failed",
        ):
            batch_enable_standards(
                [{"StandardsArn": "arn:std"}],
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# batch_disable_standards
# ---------------------------------------------------------------------------


class TestBatchDisableStandards:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.batch_disable_standards.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        batch_disable_standards(
            ["arn:sub"], region_name=REGION
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.batch_disable_standards.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="batch_disable_standards failed",
        ):
            batch_disable_standards(
                ["arn:sub"], region_name=REGION
            )


# ---------------------------------------------------------------------------
# describe_standards
# ---------------------------------------------------------------------------


class TestDescribeStandards:
    def test_empty(self, monkeypatch):
        mock = _mock_paginator([{"Standards": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_standards(region_name=REGION)
        assert result == []

    def test_with_results(self, monkeypatch):
        mock = _mock_paginator([
            {
                "Standards": [
                    {
                        "StandardsArn": "arn:std",
                        "Name": "CIS",
                        "Description": "CIS Benchmark",
                        "Extra": "val",
                    }
                ]
            }
        ])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_standards(region_name=REGION)
        assert len(result) == 1
        assert result[0].name == "CIS"
        assert result[0].extra == {"Extra": "val"}

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="describe_standards failed"
        ):
            describe_standards(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_standards_controls
# ---------------------------------------------------------------------------


class TestDescribeStandardsControls:
    def test_success(self, monkeypatch):
        mock = _mock_paginator([
            {
                "Controls": [
                    {"StandardsControlArn": "arn:ctrl"}
                ]
            }
        ])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_standards_controls(
            "arn:sub", region_name=REGION
        )
        assert len(result) == 1

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="describe_standards_controls failed",
        ):
            describe_standards_controls(
                "arn:sub", region_name=REGION
            )


# ---------------------------------------------------------------------------
# update_standards_control
# ---------------------------------------------------------------------------


class TestUpdateStandardsControl:
    def test_enable(self, monkeypatch):
        mock = MagicMock()
        mock.update_standards_control.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_standards_control(
            "arn:ctrl",
            control_status="ENABLED",
            region_name=REGION,
        )

    def test_disable_with_reason(self, monkeypatch):
        mock = MagicMock()
        mock.update_standards_control.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        update_standards_control(
            "arn:ctrl",
            control_status="DISABLED",
            disabled_reason="Not applicable",
            region_name=REGION,
        )
        call_kwargs = mock.update_standards_control.call_args[1]
        assert call_kwargs["DisabledReason"] == "Not applicable"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.update_standards_control.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="update_standards_control failed",
        ):
            update_standards_control(
                "arn:ctrl",
                control_status="ENABLED",
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# invite_members
# ---------------------------------------------------------------------------


class TestInviteMembers:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.invite_members.return_value = {
            "UnprocessedAccounts": []
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = invite_members(
            ["123"], region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.invite_members.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="invite_members failed"
        ):
            invite_members(["123"], region_name=REGION)


# ---------------------------------------------------------------------------
# list_members
# ---------------------------------------------------------------------------


class TestListMembers:
    def test_empty(self, monkeypatch):
        mock = _mock_paginator([{"Members": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_members(region_name=REGION)
        assert result == []

    def test_with_results(self, monkeypatch):
        mock = _mock_paginator([
            {
                "Members": [
                    {
                        "AccountId": "123",
                        "Email": "a@b.com",
                        "MemberStatus": "Associated",
                    }
                ]
            }
        ])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_members(region_name=REGION)
        assert len(result) == 1
        assert result[0].account_id == "123"

    def test_not_only_associated(self, monkeypatch):
        mock = _mock_paginator([{"Members": []}])
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        list_members(
            only_associated=False, region_name=REGION
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_paginator.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_members failed"
        ):
            list_members(region_name=REGION)


# ---------------------------------------------------------------------------
# get_members
# ---------------------------------------------------------------------------


class TestGetMembers:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.get_members.return_value = {
            "Members": [
                {
                    "AccountId": "123",
                    "Email": "a@b.com",
                    "MemberStatus": "Associated",
                }
            ]
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_members(["123"], region_name=REGION)
        assert len(result) == 1

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_members.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="get_members failed"
        ):
            get_members(["123"], region_name=REGION)


# ---------------------------------------------------------------------------
# create_members
# ---------------------------------------------------------------------------


class TestCreateMembers:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.create_members.return_value = {
            "UnprocessedAccounts": []
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = create_members(
            [{"AccountId": "123"}], region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.create_members.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="create_members failed"
        ):
            create_members(
                [{"AccountId": "123"}], region_name=REGION
            )


# ---------------------------------------------------------------------------
# delete_members
# ---------------------------------------------------------------------------


class TestDeleteMembers:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.delete_members.return_value = {
            "UnprocessedAccounts": []
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = delete_members(
            ["123"], region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.delete_members.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="delete_members failed"
        ):
            delete_members(["123"], region_name=REGION)


# ---------------------------------------------------------------------------
# get_administrator_account
# ---------------------------------------------------------------------------


class TestGetAdministratorAccount:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.get_administrator_account.return_value = {
            "Administrator": {
                "AccountId": "456",
                "InvitationId": "inv-1",
            }
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = get_administrator_account(
            region_name=REGION
        )
        assert result["AccountId"] == "456"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.get_administrator_account.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="get_administrator_account failed",
        ):
            get_administrator_account(region_name=REGION)


# ---------------------------------------------------------------------------
# accept_administrator_invitation
# ---------------------------------------------------------------------------


class TestAcceptAdministratorInvitation:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.accept_administrator_invitation.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        accept_administrator_invitation(
            "456", "inv-1", region_name=REGION
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.accept_administrator_invitation.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="accept_administrator_invitation failed",
        ):
            accept_administrator_invitation(
                "456", "inv-1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    """Verify __all__ contains all expected symbols."""
    for name in mod.__all__:
        assert hasattr(mod, name), f"Missing export: {name}"


def test_accept_invitation(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_invitation.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    accept_invitation("test-master_id", "test-invitation_id", region_name=REGION)
    mock_client.accept_invitation.assert_called_once()


def test_accept_invitation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_invitation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_invitation",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept invitation"):
        accept_invitation("test-master_id", "test-invitation_id", region_name=REGION)


def test_batch_delete_automation_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_automation_rules.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_delete_automation_rules([], region_name=REGION)
    mock_client.batch_delete_automation_rules.assert_called_once()


def test_batch_delete_automation_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_automation_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_automation_rules",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete automation rules"):
        batch_delete_automation_rules([], region_name=REGION)


def test_batch_get_automation_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_automation_rules.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_get_automation_rules([], region_name=REGION)
    mock_client.batch_get_automation_rules.assert_called_once()


def test_batch_get_automation_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_automation_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_automation_rules",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get automation rules"):
        batch_get_automation_rules([], region_name=REGION)


def test_batch_get_configuration_policy_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_configuration_policy_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_get_configuration_policy_associations([], region_name=REGION)
    mock_client.batch_get_configuration_policy_associations.assert_called_once()


def test_batch_get_configuration_policy_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_configuration_policy_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_configuration_policy_associations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get configuration policy associations"):
        batch_get_configuration_policy_associations([], region_name=REGION)


def test_batch_get_security_controls(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_security_controls.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_get_security_controls([], region_name=REGION)
    mock_client.batch_get_security_controls.assert_called_once()


def test_batch_get_security_controls_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_security_controls.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_security_controls",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get security controls"):
        batch_get_security_controls([], region_name=REGION)


def test_batch_get_standards_control_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_standards_control_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_get_standards_control_associations([], region_name=REGION)
    mock_client.batch_get_standards_control_associations.assert_called_once()


def test_batch_get_standards_control_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_standards_control_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_standards_control_associations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get standards control associations"):
        batch_get_standards_control_associations([], region_name=REGION)


def test_batch_import_findings(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_import_findings.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_import_findings([], region_name=REGION)
    mock_client.batch_import_findings.assert_called_once()


def test_batch_import_findings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_import_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_import_findings",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch import findings"):
        batch_import_findings([], region_name=REGION)


def test_batch_update_automation_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_automation_rules.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_update_automation_rules([], region_name=REGION)
    mock_client.batch_update_automation_rules.assert_called_once()


def test_batch_update_automation_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_automation_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_automation_rules",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch update automation rules"):
        batch_update_automation_rules([], region_name=REGION)


def test_batch_update_findings(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_findings.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_update_findings([], region_name=REGION)
    mock_client.batch_update_findings.assert_called_once()


def test_batch_update_findings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_findings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_findings",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch update findings"):
        batch_update_findings([], region_name=REGION)


def test_batch_update_findings_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_findings_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_update_findings_v2(region_name=REGION)
    mock_client.batch_update_findings_v2.assert_called_once()


def test_batch_update_findings_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_findings_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_findings_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch update findings v2"):
        batch_update_findings_v2(region_name=REGION)


def test_batch_update_standards_control_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_standards_control_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_update_standards_control_associations([], region_name=REGION)
    mock_client.batch_update_standards_control_associations.assert_called_once()


def test_batch_update_standards_control_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_update_standards_control_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_standards_control_associations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch update standards control associations"):
        batch_update_standards_control_associations([], region_name=REGION)


def test_connector_registrations_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.connector_registrations_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    connector_registrations_v2("test-auth_code", "test-auth_state", region_name=REGION)
    mock_client.connector_registrations_v2.assert_called_once()


def test_connector_registrations_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.connector_registrations_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "connector_registrations_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to connector registrations v2"):
        connector_registrations_v2("test-auth_code", "test-auth_state", region_name=REGION)


def test_create_action_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_action_target.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_action_target("test-name", "test-description", "test-id", region_name=REGION)
    mock_client.create_action_target.assert_called_once()


def test_create_action_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_action_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_action_target",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create action target"):
        create_action_target("test-name", "test-description", "test-id", region_name=REGION)


def test_create_aggregator_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_aggregator_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_aggregator_v2("test-region_linking_mode", region_name=REGION)
    mock_client.create_aggregator_v2.assert_called_once()


def test_create_aggregator_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_aggregator_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_aggregator_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create aggregator v2"):
        create_aggregator_v2("test-region_linking_mode", region_name=REGION)


def test_create_automation_rule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automation_rule.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_automation_rule(1, "test-rule_name", "test-description", {}, [], region_name=REGION)
    mock_client.create_automation_rule.assert_called_once()


def test_create_automation_rule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automation_rule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_automation_rule",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create automation rule"):
        create_automation_rule(1, "test-rule_name", "test-description", {}, [], region_name=REGION)


def test_create_automation_rule_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automation_rule_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_automation_rule_v2("test-rule_name", "test-description", 1.0, {}, [], region_name=REGION)
    mock_client.create_automation_rule_v2.assert_called_once()


def test_create_automation_rule_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_automation_rule_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_automation_rule_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create automation rule v2"):
        create_automation_rule_v2("test-rule_name", "test-description", 1.0, {}, [], region_name=REGION)


def test_create_configuration_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_policy.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_configuration_policy("test-name", {}, region_name=REGION)
    mock_client.create_configuration_policy.assert_called_once()


def test_create_configuration_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_configuration_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_configuration_policy",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create configuration policy"):
        create_configuration_policy("test-name", {}, region_name=REGION)


def test_create_connector_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connector_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_connector_v2("test-name", {}, region_name=REGION)
    mock_client.create_connector_v2.assert_called_once()


def test_create_connector_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_connector_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_connector_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create connector v2"):
        create_connector_v2("test-name", {}, region_name=REGION)


def test_create_finding_aggregator(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_finding_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_finding_aggregator("test-region_linking_mode", region_name=REGION)
    mock_client.create_finding_aggregator.assert_called_once()


def test_create_finding_aggregator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_finding_aggregator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_finding_aggregator",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create finding aggregator"):
        create_finding_aggregator("test-region_linking_mode", region_name=REGION)


def test_create_ticket_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ticket_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_ticket_v2("test-connector_id", "test-finding_metadata_uid", region_name=REGION)
    mock_client.create_ticket_v2.assert_called_once()


def test_create_ticket_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_ticket_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_ticket_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create ticket v2"):
        create_ticket_v2("test-connector_id", "test-finding_metadata_uid", region_name=REGION)


def test_decline_invitations(monkeypatch):
    mock_client = MagicMock()
    mock_client.decline_invitations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    decline_invitations([], region_name=REGION)
    mock_client.decline_invitations.assert_called_once()


def test_decline_invitations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.decline_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decline_invitations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to decline invitations"):
        decline_invitations([], region_name=REGION)


def test_delete_action_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_action_target.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_action_target("test-action_target_arn", region_name=REGION)
    mock_client.delete_action_target.assert_called_once()


def test_delete_action_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_action_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_action_target",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete action target"):
        delete_action_target("test-action_target_arn", region_name=REGION)


def test_delete_aggregator_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_aggregator_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_aggregator_v2("test-aggregator_v2_arn", region_name=REGION)
    mock_client.delete_aggregator_v2.assert_called_once()


def test_delete_aggregator_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_aggregator_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_aggregator_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete aggregator v2"):
        delete_aggregator_v2("test-aggregator_v2_arn", region_name=REGION)


def test_delete_automation_rule_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automation_rule_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_automation_rule_v2("test-identifier", region_name=REGION)
    mock_client.delete_automation_rule_v2.assert_called_once()


def test_delete_automation_rule_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_automation_rule_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_automation_rule_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete automation rule v2"):
        delete_automation_rule_v2("test-identifier", region_name=REGION)


def test_delete_configuration_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_policy.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_configuration_policy("test-identifier", region_name=REGION)
    mock_client.delete_configuration_policy.assert_called_once()


def test_delete_configuration_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration_policy",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration policy"):
        delete_configuration_policy("test-identifier", region_name=REGION)


def test_delete_connector_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connector_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_connector_v2("test-connector_id", region_name=REGION)
    mock_client.delete_connector_v2.assert_called_once()


def test_delete_connector_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_connector_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_connector_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete connector v2"):
        delete_connector_v2("test-connector_id", region_name=REGION)


def test_delete_finding_aggregator(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_finding_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_finding_aggregator("test-finding_aggregator_arn", region_name=REGION)
    mock_client.delete_finding_aggregator.assert_called_once()


def test_delete_finding_aggregator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_finding_aggregator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_finding_aggregator",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete finding aggregator"):
        delete_finding_aggregator("test-finding_aggregator_arn", region_name=REGION)


def test_delete_invitations(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_invitations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    delete_invitations([], region_name=REGION)
    mock_client.delete_invitations.assert_called_once()


def test_delete_invitations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_invitations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete invitations"):
        delete_invitations([], region_name=REGION)


def test_describe_action_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_action_targets.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_action_targets(region_name=REGION)
    mock_client.describe_action_targets.assert_called_once()


def test_describe_action_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_action_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_action_targets",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe action targets"):
        describe_action_targets(region_name=REGION)


def test_describe_organization_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_configuration.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_organization_configuration(region_name=REGION)
    mock_client.describe_organization_configuration.assert_called_once()


def test_describe_organization_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_configuration",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe organization configuration"):
        describe_organization_configuration(region_name=REGION)


def test_describe_products(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_products.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_products(region_name=REGION)
    mock_client.describe_products.assert_called_once()


def test_describe_products_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_products.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_products",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe products"):
        describe_products(region_name=REGION)


def test_describe_products_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_products_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_products_v2(region_name=REGION)
    mock_client.describe_products_v2.assert_called_once()


def test_describe_products_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_products_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_products_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe products v2"):
        describe_products_v2(region_name=REGION)


def test_describe_security_hub_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_hub_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_security_hub_v2(region_name=REGION)
    mock_client.describe_security_hub_v2.assert_called_once()


def test_describe_security_hub_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_security_hub_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_security_hub_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe security hub v2"):
        describe_security_hub_v2(region_name=REGION)


def test_disable_organization_admin_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    disable_organization_admin_account("test-admin_account_id", region_name=REGION)
    mock_client.disable_organization_admin_account.assert_called_once()


def test_disable_organization_admin_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_organization_admin_account",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable organization admin account"):
        disable_organization_admin_account("test-admin_account_id", region_name=REGION)


def test_disable_security_hub_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_security_hub_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    disable_security_hub_v2(region_name=REGION)
    mock_client.disable_security_hub_v2.assert_called_once()


def test_disable_security_hub_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_security_hub_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_security_hub_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable security hub v2"):
        disable_security_hub_v2(region_name=REGION)


def test_disassociate_from_administrator_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_from_administrator_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    disassociate_from_administrator_account(region_name=REGION)
    mock_client.disassociate_from_administrator_account.assert_called_once()


def test_disassociate_from_administrator_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_from_administrator_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_from_administrator_account",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate from administrator account"):
        disassociate_from_administrator_account(region_name=REGION)


def test_disassociate_from_master_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_from_master_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    disassociate_from_master_account(region_name=REGION)
    mock_client.disassociate_from_master_account.assert_called_once()


def test_disassociate_from_master_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_from_master_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_from_master_account",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate from master account"):
        disassociate_from_master_account(region_name=REGION)


def test_disassociate_members(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_members.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    disassociate_members([], region_name=REGION)
    mock_client.disassociate_members.assert_called_once()


def test_disassociate_members_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_members.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_members",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate members"):
        disassociate_members([], region_name=REGION)


def test_enable_organization_admin_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    enable_organization_admin_account("test-admin_account_id", region_name=REGION)
    mock_client.enable_organization_admin_account.assert_called_once()


def test_enable_organization_admin_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_organization_admin_account",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable organization admin account"):
        enable_organization_admin_account("test-admin_account_id", region_name=REGION)


def test_enable_security_hub_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_security_hub_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    enable_security_hub_v2(region_name=REGION)
    mock_client.enable_security_hub_v2.assert_called_once()


def test_enable_security_hub_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_security_hub_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_security_hub_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable security hub v2"):
        enable_security_hub_v2(region_name=REGION)


def test_get_aggregator_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregator_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_aggregator_v2("test-aggregator_v2_arn", region_name=REGION)
    mock_client.get_aggregator_v2.assert_called_once()


def test_get_aggregator_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_aggregator_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_aggregator_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get aggregator v2"):
        get_aggregator_v2("test-aggregator_v2_arn", region_name=REGION)


def test_get_automation_rule_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automation_rule_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_automation_rule_v2("test-identifier", region_name=REGION)
    mock_client.get_automation_rule_v2.assert_called_once()


def test_get_automation_rule_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_automation_rule_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_automation_rule_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get automation rule v2"):
        get_automation_rule_v2("test-identifier", region_name=REGION)


def test_get_configuration_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_configuration_policy.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_configuration_policy("test-identifier", region_name=REGION)
    mock_client.get_configuration_policy.assert_called_once()


def test_get_configuration_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_configuration_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_configuration_policy",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get configuration policy"):
        get_configuration_policy("test-identifier", region_name=REGION)


def test_get_configuration_policy_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_configuration_policy_association.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_configuration_policy_association({}, region_name=REGION)
    mock_client.get_configuration_policy_association.assert_called_once()


def test_get_configuration_policy_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_configuration_policy_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_configuration_policy_association",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get configuration policy association"):
        get_configuration_policy_association({}, region_name=REGION)


def test_get_connector_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connector_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_connector_v2("test-connector_id", region_name=REGION)
    mock_client.get_connector_v2.assert_called_once()


def test_get_connector_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_connector_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_connector_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get connector v2"):
        get_connector_v2("test-connector_id", region_name=REGION)


def test_get_finding_aggregator(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_finding_aggregator("test-finding_aggregator_arn", region_name=REGION)
    mock_client.get_finding_aggregator.assert_called_once()


def test_get_finding_aggregator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_aggregator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_finding_aggregator",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get finding aggregator"):
        get_finding_aggregator("test-finding_aggregator_arn", region_name=REGION)


def test_get_finding_history(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_history.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_finding_history({}, region_name=REGION)
    mock_client.get_finding_history.assert_called_once()


def test_get_finding_history_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_history.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_finding_history",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get finding history"):
        get_finding_history({}, region_name=REGION)


def test_get_finding_statistics_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_statistics_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_finding_statistics_v2([], region_name=REGION)
    mock_client.get_finding_statistics_v2.assert_called_once()


def test_get_finding_statistics_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_finding_statistics_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_finding_statistics_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get finding statistics v2"):
        get_finding_statistics_v2([], region_name=REGION)


def test_get_findings_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_findings_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_findings_v2(region_name=REGION)
    mock_client.get_findings_v2.assert_called_once()


def test_get_findings_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_findings_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_findings_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get findings v2"):
        get_findings_v2(region_name=REGION)


def test_get_insights(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_insights.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_insights(region_name=REGION)
    mock_client.get_insights.assert_called_once()


def test_get_insights_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_insights.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_insights",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get insights"):
        get_insights(region_name=REGION)


def test_get_invitations_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invitations_count.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_invitations_count(region_name=REGION)
    mock_client.get_invitations_count.assert_called_once()


def test_get_invitations_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_invitations_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_invitations_count",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get invitations count"):
        get_invitations_count(region_name=REGION)


def test_get_master_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_master_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_master_account(region_name=REGION)
    mock_client.get_master_account.assert_called_once()


def test_get_master_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_master_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_master_account",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get master account"):
        get_master_account(region_name=REGION)


def test_get_resources_statistics_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources_statistics_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_resources_statistics_v2([], region_name=REGION)
    mock_client.get_resources_statistics_v2.assert_called_once()


def test_get_resources_statistics_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources_statistics_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resources_statistics_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resources statistics v2"):
        get_resources_statistics_v2([], region_name=REGION)


def test_get_resources_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_resources_v2(region_name=REGION)
    mock_client.get_resources_v2.assert_called_once()


def test_get_resources_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resources_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resources_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resources v2"):
        get_resources_v2(region_name=REGION)


def test_get_security_control_definition(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_control_definition.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_security_control_definition("test-security_control_id", region_name=REGION)
    mock_client.get_security_control_definition.assert_called_once()


def test_get_security_control_definition_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_security_control_definition.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_security_control_definition",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get security control definition"):
        get_security_control_definition("test-security_control_id", region_name=REGION)


def test_list_aggregators_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aggregators_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_aggregators_v2(region_name=REGION)
    mock_client.list_aggregators_v2.assert_called_once()


def test_list_aggregators_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aggregators_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aggregators_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list aggregators v2"):
        list_aggregators_v2(region_name=REGION)


def test_list_automation_rules(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automation_rules.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_automation_rules(region_name=REGION)
    mock_client.list_automation_rules.assert_called_once()


def test_list_automation_rules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automation_rules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automation_rules",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list automation rules"):
        list_automation_rules(region_name=REGION)


def test_list_automation_rules_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automation_rules_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_automation_rules_v2(region_name=REGION)
    mock_client.list_automation_rules_v2.assert_called_once()


def test_list_automation_rules_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_automation_rules_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_automation_rules_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list automation rules v2"):
        list_automation_rules_v2(region_name=REGION)


def test_list_configuration_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_policies.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_configuration_policies(region_name=REGION)
    mock_client.list_configuration_policies.assert_called_once()


def test_list_configuration_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_configuration_policies",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list configuration policies"):
        list_configuration_policies(region_name=REGION)


def test_list_configuration_policy_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_policy_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_configuration_policy_associations(region_name=REGION)
    mock_client.list_configuration_policy_associations.assert_called_once()


def test_list_configuration_policy_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_policy_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_configuration_policy_associations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list configuration policy associations"):
        list_configuration_policy_associations(region_name=REGION)


def test_list_connectors_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connectors_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_connectors_v2(region_name=REGION)
    mock_client.list_connectors_v2.assert_called_once()


def test_list_connectors_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_connectors_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_connectors_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list connectors v2"):
        list_connectors_v2(region_name=REGION)


def test_list_finding_aggregators(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_finding_aggregators.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_finding_aggregators(region_name=REGION)
    mock_client.list_finding_aggregators.assert_called_once()


def test_list_finding_aggregators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_finding_aggregators.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_finding_aggregators",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list finding aggregators"):
        list_finding_aggregators(region_name=REGION)


def test_list_invitations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invitations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_invitations(region_name=REGION)
    mock_client.list_invitations.assert_called_once()


def test_list_invitations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_invitations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_invitations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list invitations"):
        list_invitations(region_name=REGION)


def test_list_organization_admin_accounts(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_organization_admin_accounts.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_organization_admin_accounts(region_name=REGION)
    mock_client.list_organization_admin_accounts.assert_called_once()


def test_list_organization_admin_accounts_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_organization_admin_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_organization_admin_accounts",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list organization admin accounts"):
        list_organization_admin_accounts(region_name=REGION)


def test_list_security_control_definitions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_control_definitions.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_security_control_definitions(region_name=REGION)
    mock_client.list_security_control_definitions.assert_called_once()


def test_list_security_control_definitions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_security_control_definitions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_security_control_definitions",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list security control definitions"):
        list_security_control_definitions(region_name=REGION)


def test_list_standards_control_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_standards_control_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_standards_control_associations("test-security_control_id", region_name=REGION)
    mock_client.list_standards_control_associations.assert_called_once()


def test_list_standards_control_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_standards_control_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_standards_control_associations",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list standards control associations"):
        list_standards_control_associations("test-security_control_id", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_start_configuration_policy_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_configuration_policy_association.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    start_configuration_policy_association("test-configuration_policy_identifier", {}, region_name=REGION)
    mock_client.start_configuration_policy_association.assert_called_once()


def test_start_configuration_policy_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_configuration_policy_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_configuration_policy_association",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start configuration policy association"):
        start_configuration_policy_association("test-configuration_policy_identifier", {}, region_name=REGION)


def test_start_configuration_policy_disassociation(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_configuration_policy_disassociation.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    start_configuration_policy_disassociation("test-configuration_policy_identifier", region_name=REGION)
    mock_client.start_configuration_policy_disassociation.assert_called_once()


def test_start_configuration_policy_disassociation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_configuration_policy_disassociation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_configuration_policy_disassociation",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start configuration policy disassociation"):
        start_configuration_policy_disassociation("test-configuration_policy_identifier", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_action_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_action_target.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_action_target("test-action_target_arn", region_name=REGION)
    mock_client.update_action_target.assert_called_once()


def test_update_action_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_action_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_action_target",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update action target"):
        update_action_target("test-action_target_arn", region_name=REGION)


def test_update_aggregator_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_aggregator_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", region_name=REGION)
    mock_client.update_aggregator_v2.assert_called_once()


def test_update_aggregator_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_aggregator_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_aggregator_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update aggregator v2"):
        update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", region_name=REGION)


def test_update_automation_rule_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automation_rule_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_automation_rule_v2("test-identifier", region_name=REGION)
    mock_client.update_automation_rule_v2.assert_called_once()


def test_update_automation_rule_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_automation_rule_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_automation_rule_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update automation rule v2"):
        update_automation_rule_v2("test-identifier", region_name=REGION)


def test_update_configuration_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_policy.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_configuration_policy("test-identifier", region_name=REGION)
    mock_client.update_configuration_policy.assert_called_once()


def test_update_configuration_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration_policy",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration policy"):
        update_configuration_policy("test-identifier", region_name=REGION)


def test_update_connector_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connector_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_connector_v2("test-connector_id", region_name=REGION)
    mock_client.update_connector_v2.assert_called_once()


def test_update_connector_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connector_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connector_v2",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update connector v2"):
        update_connector_v2("test-connector_id", region_name=REGION)


def test_update_finding_aggregator(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_finding_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", region_name=REGION)
    mock_client.update_finding_aggregator.assert_called_once()


def test_update_finding_aggregator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_finding_aggregator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_finding_aggregator",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update finding aggregator"):
        update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", region_name=REGION)


def test_update_organization_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_organization_configuration.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_organization_configuration(True, region_name=REGION)
    mock_client.update_organization_configuration.assert_called_once()


def test_update_organization_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_organization_configuration",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update organization configuration"):
        update_organization_configuration(True, region_name=REGION)


def test_update_security_control(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_control.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_security_control("test-security_control_id", {}, region_name=REGION)
    mock_client.update_security_control.assert_called_once()


def test_update_security_control_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_control.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security_control",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update security control"):
        update_security_control("test-security_control_id", {}, region_name=REGION)


def test_update_security_hub_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_hub_configuration.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_security_hub_configuration(region_name=REGION)
    mock_client.update_security_hub_configuration.assert_called_once()


def test_update_security_hub_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security_hub_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security_hub_configuration",
    )
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update security hub configuration"):
        update_security_hub_configuration(region_name=REGION)


def test_update_insight_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_insight
    mock_client = MagicMock()
    mock_client.update_insight.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_insight("test-insight_arn", name="test-name", filters=[{}], group_by_attribute="test-group_by_attribute", region_name="us-east-1")
    mock_client.update_insight.assert_called_once()

def test_batch_update_findings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import batch_update_findings
    mock_client = MagicMock()
    mock_client.batch_update_findings.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_update_findings("test-finding_identifiers", note="test-note", severity="test-severity", verification_state="test-verification_state", confidence="test-confidence", criticality="test-criticality", types="test-types", user_defined_fields="test-user_defined_fields", workflow="test-workflow", related_findings="test-related_findings", region_name="us-east-1")
    mock_client.batch_update_findings.assert_called_once()

def test_batch_update_findings_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import batch_update_findings_v2
    mock_client = MagicMock()
    mock_client.batch_update_findings_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    batch_update_findings_v2(metadata_uids="test-metadata_uids", finding_identifiers="test-finding_identifiers", comment="test-comment", severity_id="test-severity_id", status_id="test-status_id", region_name="us-east-1")
    mock_client.batch_update_findings_v2.assert_called_once()

def test_create_aggregator_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_aggregator_v2
    mock_client = MagicMock()
    mock_client.create_aggregator_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_aggregator_v2("test-region_linking_mode", linked_regions="test-linked_regions", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_aggregator_v2.assert_called_once()

def test_create_automation_rule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_automation_rule
    mock_client = MagicMock()
    mock_client.create_automation_rule.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_automation_rule("test-rule_order", "test-rule_name", "test-description", "test-criteria", "test-actions", tags=[{"Key": "k", "Value": "v"}], rule_status="test-rule_status", is_terminal=True, region_name="us-east-1")
    mock_client.create_automation_rule.assert_called_once()

def test_create_automation_rule_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_automation_rule_v2
    mock_client = MagicMock()
    mock_client.create_automation_rule_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_automation_rule_v2("test-rule_name", "test-description", "test-rule_order", "test-criteria", "test-actions", rule_status="test-rule_status", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_automation_rule_v2.assert_called_once()

def test_create_configuration_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_configuration_policy
    mock_client = MagicMock()
    mock_client.create_configuration_policy.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_configuration_policy("test-name", "{}", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_configuration_policy.assert_called_once()

def test_create_connector_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_connector_v2
    mock_client = MagicMock()
    mock_client.create_connector_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_connector_v2("test-name", "test-provider", description="test-description", kms_key_arn="test-kms_key_arn", tags=[{"Key": "k", "Value": "v"}], client_token="test-client_token", region_name="us-east-1")
    mock_client.create_connector_v2.assert_called_once()

def test_create_finding_aggregator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_finding_aggregator
    mock_client = MagicMock()
    mock_client.create_finding_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_finding_aggregator("test-region_linking_mode", regions="test-regions", region_name="us-east-1")
    mock_client.create_finding_aggregator.assert_called_once()

def test_create_ticket_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import create_ticket_v2
    mock_client = MagicMock()
    mock_client.create_ticket_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    create_ticket_v2("test-connector_id", "test-finding_metadata_uid", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_ticket_v2.assert_called_once()

def test_describe_action_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import describe_action_targets
    mock_client = MagicMock()
    mock_client.describe_action_targets.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_action_targets(action_target_arns="test-action_target_arns", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_action_targets.assert_called_once()

def test_describe_products_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import describe_products
    mock_client = MagicMock()
    mock_client.describe_products.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_products(next_token="test-next_token", max_results=1, product_arn="test-product_arn", region_name="us-east-1")
    mock_client.describe_products.assert_called_once()

def test_describe_products_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import describe_products_v2
    mock_client = MagicMock()
    mock_client.describe_products_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    describe_products_v2(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_products_v2.assert_called_once()

def test_disable_organization_admin_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import disable_organization_admin_account
    mock_client = MagicMock()
    mock_client.disable_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    disable_organization_admin_account(1, feature="test-feature", region_name="us-east-1")
    mock_client.disable_organization_admin_account.assert_called_once()

def test_enable_organization_admin_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import enable_organization_admin_account
    mock_client = MagicMock()
    mock_client.enable_organization_admin_account.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    enable_organization_admin_account(1, feature="test-feature", region_name="us-east-1")
    mock_client.enable_organization_admin_account.assert_called_once()

def test_enable_security_hub_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import enable_security_hub_v2
    mock_client = MagicMock()
    mock_client.enable_security_hub_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    enable_security_hub_v2(tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.enable_security_hub_v2.assert_called_once()

def test_get_finding_history_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import get_finding_history
    mock_client = MagicMock()
    mock_client.get_finding_history.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_finding_history("test-finding_identifier", start_time="test-start_time", end_time="test-end_time", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_finding_history.assert_called_once()

def test_get_finding_statistics_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import get_finding_statistics_v2
    mock_client = MagicMock()
    mock_client.get_finding_statistics_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_finding_statistics_v2("test-group_by_rules", sort_order="test-sort_order", max_statistic_results=1, region_name="us-east-1")
    mock_client.get_finding_statistics_v2.assert_called_once()

def test_get_findings_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import get_findings_v2
    mock_client = MagicMock()
    mock_client.get_findings_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_findings_v2(filters=[{}], sort_criteria="test-sort_criteria", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_findings_v2.assert_called_once()

def test_get_insights_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import get_insights
    mock_client = MagicMock()
    mock_client.get_insights.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_insights(insight_arns="test-insight_arns", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_insights.assert_called_once()

def test_get_resources_statistics_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import get_resources_statistics_v2
    mock_client = MagicMock()
    mock_client.get_resources_statistics_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_resources_statistics_v2("test-group_by_rules", sort_order="test-sort_order", max_statistic_results=1, region_name="us-east-1")
    mock_client.get_resources_statistics_v2.assert_called_once()

def test_get_resources_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import get_resources_v2
    mock_client = MagicMock()
    mock_client.get_resources_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    get_resources_v2(filters=[{}], sort_criteria="test-sort_criteria", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.get_resources_v2.assert_called_once()

def test_list_aggregators_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_aggregators_v2
    mock_client = MagicMock()
    mock_client.list_aggregators_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_aggregators_v2(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_aggregators_v2.assert_called_once()

def test_list_automation_rules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_automation_rules
    mock_client = MagicMock()
    mock_client.list_automation_rules.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_automation_rules(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_automation_rules.assert_called_once()

def test_list_automation_rules_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_automation_rules_v2
    mock_client = MagicMock()
    mock_client.list_automation_rules_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_automation_rules_v2(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_automation_rules_v2.assert_called_once()

def test_list_configuration_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_configuration_policies
    mock_client = MagicMock()
    mock_client.list_configuration_policies.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_configuration_policies(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_configuration_policies.assert_called_once()

def test_list_configuration_policy_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_configuration_policy_associations
    mock_client = MagicMock()
    mock_client.list_configuration_policy_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_configuration_policy_associations(next_token="test-next_token", max_results=1, filters=[{}], region_name="us-east-1")
    mock_client.list_configuration_policy_associations.assert_called_once()

def test_list_connectors_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_connectors_v2
    mock_client = MagicMock()
    mock_client.list_connectors_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_connectors_v2(next_token="test-next_token", max_results=1, provider_name="test-provider_name", connector_status="test-connector_status", region_name="us-east-1")
    mock_client.list_connectors_v2.assert_called_once()

def test_list_finding_aggregators_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_finding_aggregators
    mock_client = MagicMock()
    mock_client.list_finding_aggregators.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_finding_aggregators(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_finding_aggregators.assert_called_once()

def test_list_invitations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_invitations
    mock_client = MagicMock()
    mock_client.list_invitations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_invitations(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_invitations.assert_called_once()

def test_list_organization_admin_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_organization_admin_accounts
    mock_client = MagicMock()
    mock_client.list_organization_admin_accounts.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_organization_admin_accounts(max_results=1, next_token="test-next_token", feature="test-feature", region_name="us-east-1")
    mock_client.list_organization_admin_accounts.assert_called_once()

def test_list_security_control_definitions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_security_control_definitions
    mock_client = MagicMock()
    mock_client.list_security_control_definitions.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_security_control_definitions(standards_arn="test-standards_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_security_control_definitions.assert_called_once()

def test_list_standards_control_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import list_standards_control_associations
    mock_client = MagicMock()
    mock_client.list_standards_control_associations.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    list_standards_control_associations("test-security_control_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_standards_control_associations.assert_called_once()

def test_start_configuration_policy_disassociation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import start_configuration_policy_disassociation
    mock_client = MagicMock()
    mock_client.start_configuration_policy_disassociation.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    start_configuration_policy_disassociation({}, target="test-target", region_name="us-east-1")
    mock_client.start_configuration_policy_disassociation.assert_called_once()

def test_update_action_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_action_target
    mock_client = MagicMock()
    mock_client.update_action_target.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_action_target("test-action_target_arn", name="test-name", description="test-description", region_name="us-east-1")
    mock_client.update_action_target.assert_called_once()

def test_update_aggregator_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_aggregator_v2
    mock_client = MagicMock()
    mock_client.update_aggregator_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_aggregator_v2("test-aggregator_v2_arn", "test-region_linking_mode", linked_regions="test-linked_regions", region_name="us-east-1")
    mock_client.update_aggregator_v2.assert_called_once()

def test_update_automation_rule_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_automation_rule_v2
    mock_client = MagicMock()
    mock_client.update_automation_rule_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_automation_rule_v2("test-identifier", rule_status="test-rule_status", rule_order="test-rule_order", description="test-description", rule_name="test-rule_name", criteria="test-criteria", actions="test-actions", region_name="us-east-1")
    mock_client.update_automation_rule_v2.assert_called_once()

def test_update_configuration_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_configuration_policy
    mock_client = MagicMock()
    mock_client.update_configuration_policy.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_configuration_policy("test-identifier", name="test-name", description="test-description", updated_reason="test-updated_reason", configuration_policy="{}", region_name="us-east-1")
    mock_client.update_configuration_policy.assert_called_once()

def test_update_connector_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_connector_v2
    mock_client = MagicMock()
    mock_client.update_connector_v2.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_connector_v2("test-connector_id", client_secret="test-client_secret", description="test-description", provider="test-provider", region_name="us-east-1")
    mock_client.update_connector_v2.assert_called_once()

def test_update_finding_aggregator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_finding_aggregator
    mock_client = MagicMock()
    mock_client.update_finding_aggregator.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_finding_aggregator("test-finding_aggregator_arn", "test-region_linking_mode", regions="test-regions", region_name="us-east-1")
    mock_client.update_finding_aggregator.assert_called_once()

def test_update_organization_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_organization_configuration
    mock_client = MagicMock()
    mock_client.update_organization_configuration.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_organization_configuration(True, auto_enable_standards=True, organization_configuration={}, region_name="us-east-1")
    mock_client.update_organization_configuration.assert_called_once()

def test_update_security_control_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_security_control
    mock_client = MagicMock()
    mock_client.update_security_control.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_security_control("test-security_control_id", "test-parameters", last_update_reason="test-last_update_reason", region_name="us-east-1")
    mock_client.update_security_control.assert_called_once()

def test_update_security_hub_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.security_hub import update_security_hub_configuration
    mock_client = MagicMock()
    mock_client.update_security_hub_configuration.return_value = {}
    monkeypatch.setattr("aws_util.security_hub.get_client", lambda *a, **kw: mock_client)
    update_security_hub_configuration(auto_enable_controls=True, control_finding_generator="test-control_finding_generator", region_name="us-east-1")
    mock_client.update_security_hub_configuration.assert_called_once()
