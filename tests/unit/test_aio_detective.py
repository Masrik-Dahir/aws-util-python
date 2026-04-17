"""Tests for aws_util.aio.detective -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.detective import (
    GraphResult,
    IndicatorResult,
    InvestigationResult,
    InvitationResult,
    MemberResult,
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


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


# ---------------------------------------------------------------------------
# create_graph
# ---------------------------------------------------------------------------


async def test_create_graph(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"GraphArn": GRAPH_ARN}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await create_graph()
    assert result == GRAPH_ARN


async def test_create_graph_with_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"GraphArn": GRAPH_ARN}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    await create_graph(tags={"env": "prod"})
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Tags"] == {"env": "prod"}


async def test_create_graph_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError, match="create_graph failed"):
        await create_graph()


# ---------------------------------------------------------------------------
# delete_graph
# ---------------------------------------------------------------------------


async def test_delete_graph(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    await delete_graph(GRAPH_ARN)
    mock_client.call.assert_called_once_with("DeleteGraph", GraphArn=GRAPH_ARN)


async def test_delete_graph_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await delete_graph(GRAPH_ARN)


# ---------------------------------------------------------------------------
# list_graphs
# ---------------------------------------------------------------------------


async def test_list_graphs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"GraphList": [{"Arn": GRAPH_ARN}]}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_graphs()
    assert len(result) == 1
    assert isinstance(result[0], GraphResult)


async def test_list_graphs_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"GraphList": [{"Arn": "g1"}], "NextToken": "tok"},
        {"GraphList": [{"Arn": "g2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_graphs(max_results=1)
    assert len(result) == 2


async def test_list_graphs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_graphs()


# ---------------------------------------------------------------------------
# create_members
# ---------------------------------------------------------------------------


async def test_create_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Members": [{"AccountId": "111", "EmailAddress": "a@b.com", "Status": "INVITED", "GraphArn": GRAPH_ARN}],
        "UnprocessedAccounts": [],
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await create_members(GRAPH_ARN, [{"AccountId": "111", "EmailAddress": "a@b.com"}])
    assert len(result["Members"]) == 1


async def test_create_members_with_message(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Members": [], "UnprocessedAccounts": []}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    await create_members(GRAPH_ARN, [], message="hello", disable_email_notification=True)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Message"] == "hello"


async def test_create_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await create_members(GRAPH_ARN, [])


# ---------------------------------------------------------------------------
# list_members
# ---------------------------------------------------------------------------


async def test_list_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "MemberDetails": [{"AccountId": "111", "EmailAddress": "", "Status": "", "GraphArn": ""}],
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_members(GRAPH_ARN)
    assert len(result) == 1


async def test_list_members_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"MemberDetails": [{"AccountId": "1"}], "NextToken": "t"},
        {"MemberDetails": [{"AccountId": "2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_members(GRAPH_ARN, max_results=1)
    assert len(result) == 2


async def test_list_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_members(GRAPH_ARN)


# ---------------------------------------------------------------------------
# get_members
# ---------------------------------------------------------------------------


async def test_get_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "MemberDetails": [{"AccountId": "111"}],
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await get_members(GRAPH_ARN, ["111"])
    assert len(result) == 1


async def test_get_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await get_members(GRAPH_ARN, ["111"])


# ---------------------------------------------------------------------------
# delete_members
# ---------------------------------------------------------------------------


async def test_delete_members(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"UnprocessedAccounts": []}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await delete_members(GRAPH_ARN, ["111"])
    assert result == []


async def test_delete_members_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await delete_members(GRAPH_ARN, ["111"])


# ---------------------------------------------------------------------------
# accept_invitation / reject_invitation
# ---------------------------------------------------------------------------


async def test_accept_invitation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    await accept_invitation(GRAPH_ARN)
    mock_client.call.assert_called_once_with("AcceptInvitation", GraphArn=GRAPH_ARN)


async def test_accept_invitation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await accept_invitation(GRAPH_ARN)


async def test_reject_invitation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    await reject_invitation(GRAPH_ARN)
    mock_client.call.assert_called_once_with("RejectInvitation", GraphArn=GRAPH_ARN)


async def test_reject_invitation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await reject_invitation(GRAPH_ARN)


# ---------------------------------------------------------------------------
# list_invitations
# ---------------------------------------------------------------------------


async def test_list_invitations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Invitations": [{"GraphArn": GRAPH_ARN, "AccountId": "111", "EmailAddress": "a@b.com", "Status": "INVITED"}],
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_invitations()
    assert len(result) == 1


async def test_list_invitations_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Invitations": [{"GraphArn": ""}], "NextToken": "t"},
        {"Invitations": [{"GraphArn": ""}]},
    ]
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_invitations(max_results=1)
    assert len(result) == 2


async def test_list_invitations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_invitations()


# ---------------------------------------------------------------------------
# start_investigation
# ---------------------------------------------------------------------------


async def test_start_investigation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"InvestigationId": "inv-1"}
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await start_investigation(GRAPH_ARN, "arn:entity", "2024-01-01", "2024-01-02")
    assert result == "inv-1"


async def test_start_investigation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await start_investigation(GRAPH_ARN, "arn:entity", "2024-01-01", "2024-01-02")


# ---------------------------------------------------------------------------
# get_investigation
# ---------------------------------------------------------------------------


async def test_get_investigation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "InvestigationId": "inv-1",
        "GraphArn": GRAPH_ARN,
        "EntityArn": "arn:entity",
        "EntityType": "IAM_USER",
        "Status": "RUNNING",
        "Severity": "HIGH",
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await get_investigation(GRAPH_ARN, "inv-1")
    assert isinstance(result, InvestigationResult)


async def test_get_investigation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await get_investigation(GRAPH_ARN, "inv-1")


# ---------------------------------------------------------------------------
# list_investigations
# ---------------------------------------------------------------------------


async def test_list_investigations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "InvestigationDetails": [{"InvestigationId": "inv-1"}],
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_investigations(GRAPH_ARN)
    assert len(result) == 1

async def test_list_investigations_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"InvestigationDetails": [{"InvestigationId": "1"}], "NextToken": "t"},
        {"InvestigationDetails": [{"InvestigationId": "2"}]},
    ]
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_investigations(GRAPH_ARN)
    assert len(result) == 2


async def test_list_investigations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_investigations(GRAPH_ARN)


# ---------------------------------------------------------------------------
# list_indicators
# ---------------------------------------------------------------------------


async def test_list_indicators(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Indicators": [{"IndicatorType": "TTP", "IndicatorDetail": {}}],
    }
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_indicators(GRAPH_ARN, "inv-1")
    assert len(result) == 1

async def test_list_indicators_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Indicators": [{"IndicatorType": "A"}], "NextToken": "t"},
        {"Indicators": [{"IndicatorType": "B"}]},
    ]
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    result = await list_indicators(GRAPH_ARN, "inv-1")
    assert len(result) == 2


async def test_list_indicators_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.detective.async_client", _mock_factory(mock_client))
    with pytest.raises(RuntimeError):
        await list_indicators(GRAPH_ARN, "inv-1")


async def test_batch_get_graph_member_datasources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_graph_member_datasources("test-graph_arn", [], )
    mock_client.call.assert_called_once()


async def test_batch_get_graph_member_datasources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_graph_member_datasources("test-graph_arn", [], )


async def test_batch_get_membership_datasources(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_membership_datasources([], )
    mock_client.call.assert_called_once()


async def test_batch_get_membership_datasources_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_membership_datasources([], )


async def test_describe_organization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_organization_configuration("test-graph_arn", )
    mock_client.call.assert_called_once()


async def test_describe_organization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_organization_configuration("test-graph_arn", )


async def test_disable_organization_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_organization_admin_account()
    mock_client.call.assert_called_once()


async def test_disable_organization_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_organization_admin_account()


async def test_disassociate_membership(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_membership("test-graph_arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_membership_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_membership("test-graph_arn", )


async def test_enable_organization_admin_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_organization_admin_account("test-account_id", )
    mock_client.call.assert_called_once()


async def test_enable_organization_admin_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_organization_admin_account("test-account_id", )


async def test_list_datasource_packages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_datasource_packages("test-graph_arn", )
    mock_client.call.assert_called_once()


async def test_list_datasource_packages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_datasource_packages("test-graph_arn", )


async def test_list_organization_admin_accounts(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_organization_admin_accounts()
    mock_client.call.assert_called_once()


async def test_list_organization_admin_accounts_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_organization_admin_accounts()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_start_monitoring_member(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_monitoring_member("test-graph_arn", "test-account_id", )
    mock_client.call.assert_called_once()


async def test_start_monitoring_member_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_monitoring_member("test-graph_arn", "test-account_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_datasource_packages(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_datasource_packages("test-graph_arn", [], )
    mock_client.call.assert_called_once()


async def test_update_datasource_packages_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_datasource_packages("test-graph_arn", [], )


async def test_update_investigation_state(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_investigation_state("test-graph_arn", "test-investigation_id", "test-state", )
    mock_client.call.assert_called_once()


async def test_update_investigation_state_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_investigation_state("test-graph_arn", "test-investigation_id", "test-state", )


async def test_update_organization_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_organization_configuration("test-graph_arn", )
    mock_client.call.assert_called_once()


async def test_update_organization_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.detective.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_organization_configuration("test-graph_arn", )


@pytest.mark.asyncio
async def test_list_graphs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_graphs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_graphs(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_members_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_members
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_members("test-graph_arn", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_invitations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_invitations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_invitations(max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_investigations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_investigations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_investigations("test-graph_arn", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_indicators_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_indicators
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_indicators("test-graph_arn", "test-investigation_id", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_datasource_packages_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_datasource_packages
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_datasource_packages("test-graph_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_organization_admin_accounts_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_organization_admin_accounts
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_organization_admin_accounts(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_organization_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import update_organization_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await update_organization_configuration("test-graph_arn", auto_enable=True, region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_list_indicators_optional_params(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_indicators
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: mock_client)
    await list_indicators("test-graph_arn", "test-investigation_id", indicator_type="test-indicator_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_investigations_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.detective import list_investigations
    m = AsyncMock(); m.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.detective.async_client", lambda *a, **kw: m)
    await list_investigations("graph-arn", filter_criteria={"State": "OPEN"}, sort_criteria={"Field": "CREATED_TIME"}, region_name="us-east-1")
