"""Tests for aws_util.detective -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.detective import (
    GraphResult,
    IndicatorResult,
    InvestigationResult,
    InvitationResult,
    MemberResult,
    _parse_graph,
    _parse_indicator,
    _parse_investigation,
    _parse_invitation,
    _parse_member,
    accept_invitation,
    create_graph,
    create_members,
    delete_graph,
    delete_members,
    get_investigation,
    get_members,
    list_graphs,
    list_indicators,
    list_investigations,
    list_invitations,
    list_members,
    reject_invitation,
    start_investigation,
    batch_get_graph_member_datasources,
    batch_get_membership_datasources,
    describe_organization_configuration,
    disable_organization_admin_account,
    disassociate_membership,
    enable_organization_admin_account,
    list_datasource_packages,
    list_organization_admin_accounts,
    list_tags_for_resource,
    start_monitoring_member,
    tag_resource,
    untag_resource,
    update_datasource_packages,
    update_investigation_state,
    update_organization_configuration,
)

GRAPH_ARN = "arn:aws:detective:us-east-1:123456789012:graph:abc123"


def _client_error(code: str = "ValidationException") -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": "boom"}}, "Op"
    )


# ---------------------------------------------------------------------------
# Parser unit tests
# ---------------------------------------------------------------------------


def test_parse_graph(monkeypatch):
    g = _parse_graph({"Arn": GRAPH_ARN, "CreatedTime": "2024-01-01T00:00:00Z", "Extra": 1})
    assert isinstance(g, GraphResult)
    assert g.graph_arn == GRAPH_ARN
    assert g.created_at == "2024-01-01T00:00:00Z"
    assert g.extra == {"Extra": 1}


def test_parse_graph_minimal():
    g = _parse_graph({})
    assert g.graph_arn == ""
    assert g.created_at is None


def test_parse_member():
    m = _parse_member({
        "AccountId": "111",
        "EmailAddress": "a@b.com",
        "Status": "ENABLED",
        "InvitedTime": "2024-01-01",
        "UpdatedTime": "2024-06-01",
        "GraphArn": GRAPH_ARN,
        "Extra": "x",
    })
    assert isinstance(m, MemberResult)
    assert m.account_id == "111"
    assert m.email_address == "a@b.com"
    assert m.extra == {"Extra": "x"}


def test_parse_member_minimal():
    m = _parse_member({})
    assert m.invited_time is None
    assert m.updated_time is None


def test_parse_invitation():
    inv = _parse_invitation({
        "GraphArn": GRAPH_ARN,
        "AccountId": "111",
        "EmailAddress": "a@b.com",
        "Status": "INVITED",
        "Extra": True,
    })
    assert isinstance(inv, InvitationResult)
    assert inv.status == "INVITED"
    assert inv.extra == {"Extra": True}


def test_parse_investigation():
    inv = _parse_investigation({
        "InvestigationId": "inv-1",
        "GraphArn": GRAPH_ARN,
        "EntityArn": "arn:entity",
        "EntityType": "IAM_USER",
        "Status": "RUNNING",
        "Severity": "HIGH",
        "CreatedTime": "2024-01-01",
        "Extra": 42,
    })
    assert isinstance(inv, InvestigationResult)
    assert inv.investigation_id == "inv-1"
    assert inv.extra == {"Extra": 42}


def test_parse_investigation_minimal():
    inv = _parse_investigation({})
    assert inv.created_time is None


def test_parse_indicator():
    ind = _parse_indicator({
        "IndicatorType": "TTP_OBSERVED",
        "IndicatorDetail": {"key": "val"},
        "Extra": 1,
    })
    assert isinstance(ind, IndicatorResult)
    assert ind.indicator_type == "TTP_OBSERVED"
    assert ind.extra == {"Extra": 1}


# ---------------------------------------------------------------------------
# create_graph
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_create_graph(mock_gc):
    client = MagicMock()
    client.create_graph.return_value = {"GraphArn": GRAPH_ARN}
    mock_gc.return_value = client
    result = create_graph()
    assert result == GRAPH_ARN


@patch("aws_util.detective.get_client")
def test_create_graph_with_tags(mock_gc):
    client = MagicMock()
    client.create_graph.return_value = {"GraphArn": GRAPH_ARN}
    mock_gc.return_value = client
    create_graph(tags={"env": "prod"})
    call_kwargs = client.create_graph.call_args[1]
    assert call_kwargs["Tags"] == {"env": "prod"}


@patch("aws_util.detective.get_client")
def test_create_graph_error(mock_gc):
    client = MagicMock()
    client.create_graph.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError, match="create_graph failed"):
        create_graph()


# ---------------------------------------------------------------------------
# delete_graph
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_delete_graph(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_graph(GRAPH_ARN)
    client.delete_graph.assert_called_once_with(GraphArn=GRAPH_ARN)


@patch("aws_util.detective.get_client")
def test_delete_graph_error(mock_gc):
    client = MagicMock()
    client.delete_graph.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_graph(GRAPH_ARN)


# ---------------------------------------------------------------------------
# list_graphs
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_list_graphs(mock_gc):
    client = MagicMock()
    client.list_graphs.return_value = {
        "GraphList": [{"Arn": GRAPH_ARN}],
    }
    mock_gc.return_value = client
    result = list_graphs()
    assert len(result) == 1
    assert isinstance(result[0], GraphResult)


@patch("aws_util.detective.get_client")
def test_list_graphs_pagination(mock_gc):
    client = MagicMock()
    client.list_graphs.side_effect = [
        {"GraphList": [{"Arn": "g1"}], "NextToken": "tok"},
        {"GraphList": [{"Arn": "g2"}]},
    ]
    mock_gc.return_value = client
    result = list_graphs(max_results=1)
    assert len(result) == 2


@patch("aws_util.detective.get_client")
def test_list_graphs_error(mock_gc):
    client = MagicMock()
    client.list_graphs.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_graphs()


# ---------------------------------------------------------------------------
# create_members
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_create_members(mock_gc):
    client = MagicMock()
    client.create_members.return_value = {
        "Members": [{"AccountId": "111", "EmailAddress": "a@b.com", "Status": "INVITED", "GraphArn": GRAPH_ARN}],
        "UnprocessedAccounts": [],
    }
    mock_gc.return_value = client
    result = create_members(GRAPH_ARN, [{"AccountId": "111", "EmailAddress": "a@b.com"}])
    assert len(result["Members"]) == 1
    assert result["UnprocessedAccounts"] == []


@patch("aws_util.detective.get_client")
def test_create_members_with_message(mock_gc):
    client = MagicMock()
    client.create_members.return_value = {"Members": [], "UnprocessedAccounts": []}
    mock_gc.return_value = client
    create_members(
        GRAPH_ARN,
        [],
        message="hello",
        disable_email_notification=True,
    )
    call_kwargs = client.create_members.call_args[1]
    assert call_kwargs["Message"] == "hello"
    assert call_kwargs["DisableEmailNotification"] is True


@patch("aws_util.detective.get_client")
def test_create_members_error(mock_gc):
    client = MagicMock()
    client.create_members.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_members(GRAPH_ARN, [])


# ---------------------------------------------------------------------------
# list_members
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_list_members(mock_gc):
    client = MagicMock()
    client.list_members.return_value = {
        "MemberDetails": [{"AccountId": "111", "EmailAddress": "a@b.com", "Status": "ENABLED", "GraphArn": GRAPH_ARN}],
    }
    mock_gc.return_value = client
    result = list_members(GRAPH_ARN)
    assert len(result) == 1


@patch("aws_util.detective.get_client")
def test_list_members_pagination(mock_gc):
    client = MagicMock()
    client.list_members.side_effect = [
        {"MemberDetails": [{"AccountId": "1", "EmailAddress": "", "Status": "", "GraphArn": ""}], "NextToken": "t"},
        {"MemberDetails": [{"AccountId": "2", "EmailAddress": "", "Status": "", "GraphArn": ""}]},
    ]
    mock_gc.return_value = client
    result = list_members(GRAPH_ARN, max_results=1)
    assert len(result) == 2


@patch("aws_util.detective.get_client")
def test_list_members_error(mock_gc):
    client = MagicMock()
    client.list_members.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_members(GRAPH_ARN)


# ---------------------------------------------------------------------------
# get_members
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_get_members(mock_gc):
    client = MagicMock()
    client.get_members.return_value = {
        "MemberDetails": [{"AccountId": "111", "EmailAddress": "", "Status": "", "GraphArn": ""}],
    }
    mock_gc.return_value = client
    result = get_members(GRAPH_ARN, ["111"])
    assert len(result) == 1


@patch("aws_util.detective.get_client")
def test_get_members_error(mock_gc):
    client = MagicMock()
    client.get_members.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_members(GRAPH_ARN, ["111"])


# ---------------------------------------------------------------------------
# delete_members
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_delete_members(mock_gc):
    client = MagicMock()
    client.delete_members.return_value = {"UnprocessedAccounts": []}
    mock_gc.return_value = client
    result = delete_members(GRAPH_ARN, ["111"])
    assert result == []


@patch("aws_util.detective.get_client")
def test_delete_members_error(mock_gc):
    client = MagicMock()
    client.delete_members.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_members(GRAPH_ARN, ["111"])


# ---------------------------------------------------------------------------
# accept_invitation / reject_invitation
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_accept_invitation(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    accept_invitation(GRAPH_ARN)
    client.accept_invitation.assert_called_once_with(GraphArn=GRAPH_ARN)


@patch("aws_util.detective.get_client")
def test_accept_invitation_error(mock_gc):
    client = MagicMock()
    client.accept_invitation.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        accept_invitation(GRAPH_ARN)


@patch("aws_util.detective.get_client")
def test_reject_invitation(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    reject_invitation(GRAPH_ARN)
    client.reject_invitation.assert_called_once_with(GraphArn=GRAPH_ARN)


@patch("aws_util.detective.get_client")
def test_reject_invitation_error(mock_gc):
    client = MagicMock()
    client.reject_invitation.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        reject_invitation(GRAPH_ARN)


# ---------------------------------------------------------------------------
# list_invitations
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_list_invitations(mock_gc):
    client = MagicMock()
    client.list_invitations.return_value = {
        "Invitations": [{"GraphArn": GRAPH_ARN, "AccountId": "111", "EmailAddress": "a@b.com", "Status": "INVITED"}],
    }
    mock_gc.return_value = client
    result = list_invitations()
    assert len(result) == 1
    assert isinstance(result[0], InvitationResult)


@patch("aws_util.detective.get_client")
def test_list_invitations_pagination(mock_gc):
    client = MagicMock()
    client.list_invitations.side_effect = [
        {"Invitations": [{"GraphArn": "", "AccountId": "", "EmailAddress": "", "Status": ""}], "NextToken": "t"},
        {"Invitations": [{"GraphArn": "", "AccountId": "", "EmailAddress": "", "Status": ""}]},
    ]
    mock_gc.return_value = client
    result = list_invitations(max_results=1)
    assert len(result) == 2


@patch("aws_util.detective.get_client")
def test_list_invitations_error(mock_gc):
    client = MagicMock()
    client.list_invitations.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_invitations()


# ---------------------------------------------------------------------------
# start_investigation
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_start_investigation(mock_gc):
    client = MagicMock()
    client.start_investigation.return_value = {"InvestigationId": "inv-1"}
    mock_gc.return_value = client
    result = start_investigation(GRAPH_ARN, "arn:entity", "2024-01-01", "2024-01-02")
    assert result == "inv-1"


@patch("aws_util.detective.get_client")
def test_start_investigation_error(mock_gc):
    client = MagicMock()
    client.start_investigation.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        start_investigation(GRAPH_ARN, "arn:entity", "2024-01-01", "2024-01-02")


# ---------------------------------------------------------------------------
# get_investigation
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_get_investigation(mock_gc):
    client = MagicMock()
    client.get_investigation.return_value = {
        "InvestigationId": "inv-1",
        "GraphArn": GRAPH_ARN,
        "EntityArn": "arn:entity",
        "EntityType": "IAM_USER",
        "Status": "RUNNING",
        "Severity": "HIGH",
    }
    mock_gc.return_value = client
    result = get_investigation(GRAPH_ARN, "inv-1")
    assert isinstance(result, InvestigationResult)
    assert result.investigation_id == "inv-1"


@patch("aws_util.detective.get_client")
def test_get_investigation_error(mock_gc):
    client = MagicMock()
    client.get_investigation.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        get_investigation(GRAPH_ARN, "inv-1")


# ---------------------------------------------------------------------------
# list_investigations
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_list_investigations(mock_gc):
    client = MagicMock()
    client.list_investigations.return_value = {
        "InvestigationDetails": [{"InvestigationId": "inv-1", "GraphArn": GRAPH_ARN}],
    }
    mock_gc.return_value = client
    result = list_investigations(GRAPH_ARN)
    assert len(result) == 1


@patch("aws_util.detective.get_client")
def test_list_investigations_pagination(mock_gc):
    client = MagicMock()
    client.list_investigations.side_effect = [
        {"InvestigationDetails": [{"InvestigationId": "1"}], "NextToken": "t"},
        {"InvestigationDetails": [{"InvestigationId": "2"}]},
    ]
    mock_gc.return_value = client
    result = list_investigations(GRAPH_ARN)
    assert len(result) == 2


@patch("aws_util.detective.get_client")
def test_list_investigations_error(mock_gc):
    client = MagicMock()
    client.list_investigations.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_investigations(GRAPH_ARN)


# ---------------------------------------------------------------------------
# list_indicators
# ---------------------------------------------------------------------------


@patch("aws_util.detective.get_client")
def test_list_indicators(mock_gc):
    client = MagicMock()
    client.list_indicators.return_value = {
        "Indicators": [{"IndicatorType": "TTP", "IndicatorDetail": {}}],
    }
    mock_gc.return_value = client
    result = list_indicators(GRAPH_ARN, "inv-1")
    assert len(result) == 1
    assert isinstance(result[0], IndicatorResult)


@patch("aws_util.detective.get_client")
def test_list_indicators_pagination(mock_gc):
    client = MagicMock()
    client.list_indicators.side_effect = [
        {"Indicators": [{"IndicatorType": "A"}], "NextToken": "t"},
        {"Indicators": [{"IndicatorType": "B"}]},
    ]
    mock_gc.return_value = client
    result = list_indicators(GRAPH_ARN, "inv-1")
    assert len(result) == 2


@patch("aws_util.detective.get_client")
def test_list_indicators_error(mock_gc):
    client = MagicMock()
    client.list_indicators.side_effect = _client_error()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        list_indicators(GRAPH_ARN, "inv-1")


REGION = "us-east-1"


@patch("aws_util.detective.get_client")
def test_batch_get_graph_member_datasources(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_graph_member_datasources.return_value = {}
    batch_get_graph_member_datasources("test-graph_arn", [], region_name=REGION)
    mock_client.batch_get_graph_member_datasources.assert_called_once()


@patch("aws_util.detective.get_client")
def test_batch_get_graph_member_datasources_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_graph_member_datasources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_graph_member_datasources",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get graph member datasources"):
        batch_get_graph_member_datasources("test-graph_arn", [], region_name=REGION)


@patch("aws_util.detective.get_client")
def test_batch_get_membership_datasources(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_membership_datasources.return_value = {}
    batch_get_membership_datasources([], region_name=REGION)
    mock_client.batch_get_membership_datasources.assert_called_once()


@patch("aws_util.detective.get_client")
def test_batch_get_membership_datasources_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_get_membership_datasources.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_membership_datasources",
    )
    with pytest.raises(RuntimeError, match="Failed to batch get membership datasources"):
        batch_get_membership_datasources([], region_name=REGION)


@patch("aws_util.detective.get_client")
def test_describe_organization_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_organization_configuration.return_value = {}
    describe_organization_configuration("test-graph_arn", region_name=REGION)
    mock_client.describe_organization_configuration.assert_called_once()


@patch("aws_util.detective.get_client")
def test_describe_organization_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_organization_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to describe organization configuration"):
        describe_organization_configuration("test-graph_arn", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_disable_organization_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_organization_admin_account.return_value = {}
    disable_organization_admin_account(region_name=REGION)
    mock_client.disable_organization_admin_account.assert_called_once()


@patch("aws_util.detective.get_client")
def test_disable_organization_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disable_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_organization_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to disable organization admin account"):
        disable_organization_admin_account(region_name=REGION)


@patch("aws_util.detective.get_client")
def test_disassociate_membership(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_membership.return_value = {}
    disassociate_membership("test-graph_arn", region_name=REGION)
    mock_client.disassociate_membership.assert_called_once()


@patch("aws_util.detective.get_client")
def test_disassociate_membership_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.disassociate_membership.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_membership",
    )
    with pytest.raises(RuntimeError, match="Failed to disassociate membership"):
        disassociate_membership("test-graph_arn", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_enable_organization_admin_account(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_organization_admin_account.return_value = {}
    enable_organization_admin_account("test-account_id", region_name=REGION)
    mock_client.enable_organization_admin_account.assert_called_once()


@patch("aws_util.detective.get_client")
def test_enable_organization_admin_account_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.enable_organization_admin_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_organization_admin_account",
    )
    with pytest.raises(RuntimeError, match="Failed to enable organization admin account"):
        enable_organization_admin_account("test-account_id", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_list_datasource_packages(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_datasource_packages.return_value = {}
    list_datasource_packages("test-graph_arn", region_name=REGION)
    mock_client.list_datasource_packages.assert_called_once()


@patch("aws_util.detective.get_client")
def test_list_datasource_packages_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_datasource_packages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_datasource_packages",
    )
    with pytest.raises(RuntimeError, match="Failed to list datasource packages"):
        list_datasource_packages("test-graph_arn", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_list_organization_admin_accounts(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_organization_admin_accounts.return_value = {}
    list_organization_admin_accounts(region_name=REGION)
    mock_client.list_organization_admin_accounts.assert_called_once()


@patch("aws_util.detective.get_client")
def test_list_organization_admin_accounts_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_organization_admin_accounts.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_organization_admin_accounts",
    )
    with pytest.raises(RuntimeError, match="Failed to list organization admin accounts"):
        list_organization_admin_accounts(region_name=REGION)


@patch("aws_util.detective.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.detective.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_start_monitoring_member(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_monitoring_member.return_value = {}
    start_monitoring_member("test-graph_arn", "test-account_id", region_name=REGION)
    mock_client.start_monitoring_member.assert_called_once()


@patch("aws_util.detective.get_client")
def test_start_monitoring_member_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_monitoring_member.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_monitoring_member",
    )
    with pytest.raises(RuntimeError, match="Failed to start monitoring member"):
        start_monitoring_member("test-graph_arn", "test-account_id", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.detective.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.detective.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.detective.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.detective.get_client")
def test_update_datasource_packages(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_datasource_packages.return_value = {}
    update_datasource_packages("test-graph_arn", [], region_name=REGION)
    mock_client.update_datasource_packages.assert_called_once()


@patch("aws_util.detective.get_client")
def test_update_datasource_packages_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_datasource_packages.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_datasource_packages",
    )
    with pytest.raises(RuntimeError, match="Failed to update datasource packages"):
        update_datasource_packages("test-graph_arn", [], region_name=REGION)


@patch("aws_util.detective.get_client")
def test_update_investigation_state(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_investigation_state.return_value = {}
    update_investigation_state("test-graph_arn", "test-investigation_id", "test-state", region_name=REGION)
    mock_client.update_investigation_state.assert_called_once()


@patch("aws_util.detective.get_client")
def test_update_investigation_state_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_investigation_state.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_investigation_state",
    )
    with pytest.raises(RuntimeError, match="Failed to update investigation state"):
        update_investigation_state("test-graph_arn", "test-investigation_id", "test-state", region_name=REGION)


@patch("aws_util.detective.get_client")
def test_update_organization_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_organization_configuration.return_value = {}
    update_organization_configuration("test-graph_arn", region_name=REGION)
    mock_client.update_organization_configuration.assert_called_once()


@patch("aws_util.detective.get_client")
def test_update_organization_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_organization_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_organization_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update organization configuration"):
        update_organization_configuration("test-graph_arn", region_name=REGION)


def test_list_graphs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_graphs
    mock_client = MagicMock()
    mock_client.list_graphs.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_graphs(max_results=1, region_name="us-east-1")
    mock_client.list_graphs.assert_called_once()

def test_list_members_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_members
    mock_client = MagicMock()
    mock_client.list_members.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_members("test-graph_arn", max_results=1, region_name="us-east-1")
    mock_client.list_members.assert_called_once()

def test_list_invitations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_invitations
    mock_client = MagicMock()
    mock_client.list_invitations.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_invitations(max_results=1, region_name="us-east-1")
    mock_client.list_invitations.assert_called_once()

def test_list_investigations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_investigations
    mock_client = MagicMock()
    mock_client.list_investigations.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_investigations("test-graph_arn", max_results=1, region_name="us-east-1")
    mock_client.list_investigations.assert_called_once()

def test_list_indicators_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_indicators
    mock_client = MagicMock()
    mock_client.list_indicators.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_indicators("test-graph_arn", "test-investigation_id", max_results=1, region_name="us-east-1")
    mock_client.list_indicators.assert_called_once()

def test_list_datasource_packages_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_datasource_packages
    mock_client = MagicMock()
    mock_client.list_datasource_packages.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_datasource_packages("test-graph_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_datasource_packages.assert_called_once()

def test_list_organization_admin_accounts_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_organization_admin_accounts
    mock_client = MagicMock()
    mock_client.list_organization_admin_accounts.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_organization_admin_accounts(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_organization_admin_accounts.assert_called_once()

def test_update_organization_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import update_organization_configuration
    mock_client = MagicMock()
    mock_client.update_organization_configuration.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    update_organization_configuration("test-graph_arn", auto_enable=True, region_name="us-east-1")
    mock_client.update_organization_configuration.assert_called_once()


def test_list_indicators_optional_params(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_indicators
    mock_client = MagicMock()
    mock_client.list_indicators.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: mock_client)
    list_indicators("test-graph_arn", "test-investigation_id", indicator_type="test-indicator_type", region_name="us-east-1")
    mock_client.list_indicators.assert_called_once()

def test_list_investigations_opts(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.detective import list_investigations
    m = MagicMock(); m.list_investigations.return_value = {}
    monkeypatch.setattr("aws_util.detective.get_client", lambda *a, **kw: m)
    list_investigations("graph-arn", filter_criteria={"State": "OPEN"}, sort_criteria={"Field": "CREATED_TIME"}, region_name="us-east-1")
