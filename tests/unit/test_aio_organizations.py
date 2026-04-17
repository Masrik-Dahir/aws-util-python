"""Tests for aws_util.aio.organizations — 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.organizations import (
    AccountResult,
    HandshakeResult,
    OUResult,
    OrgResult,
    PolicyResult,
    PolicySummaryResult,
    RootResult,
    accept_handshake,
    attach_policy,
    create_account,
    create_organization,
    create_organizational_unit,
    create_policy,
    delete_policy,
    describe_account,
    describe_organization,
    describe_organizational_unit,
    describe_policy,
    detach_policy,
    disable_policy_type,
    enable_policy_type,
    invite_account_to_organization,
    list_accounts,
    list_accounts_for_parent,
    list_children,
    list_organizational_units_for_parent,
    list_parents,
    list_policies,
    list_roots,
    list_tags_for_resource,
    move_account,
    remove_account_from_organization,
    tag_resource,
    update_policy,
    cancel_handshake,
    close_account,
    create_gov_cloud_account,
    decline_handshake,
    delete_organization,
    delete_organizational_unit,
    delete_resource_policy,
    deregister_delegated_administrator,
    describe_create_account_status,
    describe_effective_policy,
    describe_handshake,
    describe_resource_policy,
    disable_aws_service_access,
    enable_all_features,
    enable_aws_service_access,
    leave_organization,
    list_accounts_with_invalid_effective_policy,
    list_aws_service_access_for_organization,
    list_create_account_status,
    list_delegated_administrators,
    list_delegated_services_for_account,
    list_effective_policy_validation_errors,
    list_handshakes_for_account,
    list_handshakes_for_organization,
    list_policies_for_target,
    list_targets_for_policy,
    put_resource_policy,
    register_delegated_administrator,
    untag_resource,
    update_organizational_unit,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _org_dict(**overrides: object) -> dict:
    base = {
        "Id": "o-abc123",
        "Arn": "arn:aws:organizations::111:organization/o-abc123",
        "MasterAccountArn": "arn:aws:organizations::111:account/o-abc123/111",
        "MasterAccountId": "111111111111",
        "MasterAccountEmail": "root@example.com",
        "FeatureSet": "ALL",
        "AvailablePolicyTypes": [
            {"Type": "SERVICE_CONTROL_POLICY", "Status": "ENABLED"}
        ],
    }
    base.update(overrides)
    return base


def _ou_dict(**overrides: object) -> dict:
    base = {
        "Id": "ou-abc-123",
        "Arn": "arn:aws:organizations::111:ou/o-abc123/ou-abc-123",
        "Name": "Engineering",
    }
    base.update(overrides)
    return base


def _account_dict(**overrides: object) -> dict:
    base = {
        "Id": "222222222222",
        "Arn": "arn:aws:organizations::111:account/o-abc123/222222222222",
        "Name": "dev-account",
        "Email": "dev@example.com",
        "Status": "ACTIVE",
        "JoinedMethod": "CREATED",
        "JoinedTimestamp": "2024-01-01T00:00:00Z",
    }
    base.update(overrides)
    return base


def _policy_dict(**overrides: object) -> dict:
    base = {
        "PolicySummary": {
            "Id": "p-abc123",
            "Arn": "arn:aws:organizations::111:policy/o-abc123/scp/p-abc123",
            "Name": "DenyS3",
            "Description": "Deny S3 access",
            "Type": "SERVICE_CONTROL_POLICY",
            "AwsManaged": False,
        },
        "Content": '{"Version":"2012-10-17","Statement":[]}',
    }
    base.update(overrides)
    return base


def _policy_summary_dict(**overrides: object) -> dict:
    base = {
        "Id": "p-abc123",
        "Arn": "arn:aws:organizations::111:policy/o-abc123/scp/p-abc123",
        "Name": "DenyS3",
        "Description": "Deny S3 access",
        "Type": "SERVICE_CONTROL_POLICY",
        "AwsManaged": False,
    }
    base.update(overrides)
    return base


def _handshake_dict(**overrides: object) -> dict:
    base = {
        "Id": "h-abc123",
        "Arn": "arn:aws:organizations::111:handshake/o-abc123/invite/h-abc123",
        "State": "OPEN",
        "Action": "INVITE",
        "Resources": [],
        "Parties": [{"Id": "111", "Type": "ORGANIZATION"}],
        "RequestedTimestamp": "2024-01-01T00:00:00Z",
        "ExpirationTimestamp": "2024-01-15T00:00:00Z",
    }
    base.update(overrides)
    return base


def _root_dict(**overrides: object) -> dict:
    base = {
        "Id": "r-abc1",
        "Arn": "arn:aws:organizations::111:root/o-abc123/r-abc1",
        "Name": "Root",
        "PolicyTypes": [
            {"Type": "SERVICE_CONTROL_POLICY", "Status": "ENABLED"}
        ],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# create_organization
# ---------------------------------------------------------------------------


async def test_create_organization_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Organization": _org_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await create_organization()
    assert isinstance(result, OrgResult)
    assert result.id == "o-abc123"

async def test_create_organization_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("denied")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="denied"):
        await create_organization()


async def test_create_organization_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="create_organization failed"
    ):
        await create_organization()


# ---------------------------------------------------------------------------
# describe_organization
# ---------------------------------------------------------------------------


async def test_describe_organization_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Organization": _org_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_organization()
    assert isinstance(result, OrgResult)
    assert result.id == "o-abc123"


async def test_describe_organization_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Organization": _org_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_organization(
        region_name="us-west-2"
    )
    assert result.id == "o-abc123"


async def test_describe_organization_runtime_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await describe_organization()


async def test_describe_organization_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="describe_organization failed"
    ):
        await describe_organization()


# ---------------------------------------------------------------------------
# create_organizational_unit
# ---------------------------------------------------------------------------


async def test_create_ou_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "OrganizationalUnit": _ou_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await create_organizational_unit(
        "r-abc1", "Engineering"
    )
    assert isinstance(result, OUResult)
    assert result.name == "Engineering"


async def test_create_ou_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "OrganizationalUnit": _ou_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await create_organizational_unit(
        "r-abc1", "Engineering", region_name="us-east-1"
    )
    assert result.name == "Engineering"


async def test_create_ou_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await create_organizational_unit("r-1", "X")


async def test_create_ou_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="create_organizational_unit failed",
    ):
        await create_organizational_unit("r-1", "X")


# ---------------------------------------------------------------------------
# describe_organizational_unit
# ---------------------------------------------------------------------------


async def test_describe_ou_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "OrganizationalUnit": _ou_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_organizational_unit("ou-abc-123")
    assert isinstance(result, OUResult)
    assert result.id == "ou-abc-123"


async def test_describe_ou_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_organizational_unit("ou-bad")


async def test_describe_ou_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="describe_organizational_unit failed",
    ):
        await describe_organizational_unit("ou-bad")


# ---------------------------------------------------------------------------
# list_organizational_units_for_parent
# ---------------------------------------------------------------------------


async def test_list_ous_for_parent_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "OrganizationalUnits": [_ou_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_organizational_units_for_parent(
        "r-abc1"
    )
    assert len(result) == 1
    assert isinstance(result[0], OUResult)


async def test_list_ous_for_parent_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "OrganizationalUnits": [
                _ou_dict(Id="ou-1", Name="OU1")
            ],
            "NextToken": "tok",
        },
        {
            "OrganizationalUnits": [
                _ou_dict(Id="ou-2", Name="OU2")
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_organizational_units_for_parent(
        "r-abc1"
    )
    assert len(result) == 2


async def test_list_ous_for_parent_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "OrganizationalUnits": []
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_organizational_units_for_parent(
        "r-abc1"
    )
    assert result == []


async def test_list_ous_for_parent_runtime_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_organizational_units_for_parent("r-1")


async def test_list_ous_for_parent_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="list_organizational_units_for_parent failed",
    ):
        await list_organizational_units_for_parent("r-1")


# ---------------------------------------------------------------------------
# list_accounts
# ---------------------------------------------------------------------------


async def test_list_accounts_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Accounts": [_account_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_accounts()
    assert len(result) == 1
    assert isinstance(result[0], AccountResult)


async def test_list_accounts_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Accounts": [_account_dict(Id="111", Name="a1")],
            "NextToken": "tok",
        },
        {
            "Accounts": [_account_dict(Id="222", Name="a2")]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_accounts()
    assert len(result) == 2


async def test_list_accounts_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Accounts": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_accounts()
    assert result == []


async def test_list_accounts_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_accounts()


async def test_list_accounts_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_accounts failed"
    ):
        await list_accounts()


# ---------------------------------------------------------------------------
# list_accounts_for_parent
# ---------------------------------------------------------------------------


async def test_list_accounts_for_parent_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Accounts": [_account_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_accounts_for_parent("r-abc1")
    assert len(result) == 1


async def test_list_accounts_for_parent_pagination(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Accounts": [_account_dict(Id="111")],
            "NextToken": "tok",
        },
        {"Accounts": [_account_dict(Id="222")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_accounts_for_parent("r-abc1")
    assert len(result) == 2


async def test_list_accounts_for_parent_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Accounts": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_accounts_for_parent("r-abc1")
    assert result == []


async def test_list_accounts_for_parent_runtime_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_accounts_for_parent("r-1")


async def test_list_accounts_for_parent_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="list_accounts_for_parent failed",
    ):
        await list_accounts_for_parent("r-1")


# ---------------------------------------------------------------------------
# describe_account
# ---------------------------------------------------------------------------


async def test_describe_account_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Account": _account_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_account("222222222222")
    assert isinstance(result, AccountResult)
    assert result.id == "222222222222"


async def test_describe_account_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Account": _account_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_account(
        "222222222222", region_name="us-east-1"
    )
    assert result.id == "222222222222"


async def test_describe_account_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_account("bad")


async def test_describe_account_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="describe_account failed"
    ):
        await describe_account("bad")


# ---------------------------------------------------------------------------
# create_account
# ---------------------------------------------------------------------------


async def test_create_account_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "CreateAccountStatus": {
            "Id": "car-abc",
            "State": "IN_PROGRESS",
        }
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await create_account(
        "new@example.com", "new-acct"
    )
    assert result["State"] == "IN_PROGRESS"


async def test_create_account_with_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "CreateAccountStatus": {"Id": "car-abc"}
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await create_account(
        "new@example.com",
        "new-acct",
        role_name="MyRole",
        region_name="us-east-1",
    )
    kw = mock_client.call.call_args[1]
    assert kw["RoleName"] == "MyRole"


async def test_create_account_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await create_account("x@y.com", "acct")


async def test_create_account_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="create_account failed"
    ):
        await create_account("x@y.com", "acct")


# ---------------------------------------------------------------------------
# invite_account_to_organization
# ---------------------------------------------------------------------------


async def test_invite_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Handshake": _handshake_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await invite_account_to_organization(
        "333333333333"
    )
    assert isinstance(result, HandshakeResult)
    assert result.id == "h-abc123"


async def test_invite_with_notes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Handshake": _handshake_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await invite_account_to_organization(
        "333333333333",
        notes="Please join",
        region_name="us-east-1",
    )
    kw = mock_client.call.call_args[1]
    assert kw["Notes"] == "Please join"


async def test_invite_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await invite_account_to_organization("bad")


async def test_invite_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="invite_account_to_organization failed",
    ):
        await invite_account_to_organization("bad")


# ---------------------------------------------------------------------------
# accept_handshake
# ---------------------------------------------------------------------------


async def test_accept_handshake_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Handshake": _handshake_dict(State="ACCEPTED")
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await accept_handshake("h-abc123")
    assert isinstance(result, HandshakeResult)
    assert result.state == "ACCEPTED"


async def test_accept_handshake_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await accept_handshake("bad")


async def test_accept_handshake_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="accept_handshake failed"
    ):
        await accept_handshake("bad")


# ---------------------------------------------------------------------------
# move_account
# ---------------------------------------------------------------------------


async def test_move_account_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await move_account("222", "r-abc1", "ou-abc-123")
    mock_client.call.assert_awaited_once()


async def test_move_account_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await move_account(
        "222", "r-abc1", "ou-abc-123",
        region_name="us-east-1",
    )
    mock_client.call.assert_awaited_once()


async def test_move_account_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await move_account("bad", "r-1", "ou-1")


async def test_move_account_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="move_account failed"
    ):
        await move_account("bad", "r-1", "ou-1")


# ---------------------------------------------------------------------------
# remove_account_from_organization
# ---------------------------------------------------------------------------


async def test_remove_account_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await remove_account_from_organization("222")
    mock_client.call.assert_awaited_once()


async def test_remove_account_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await remove_account_from_organization("bad")


async def test_remove_account_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError,
        match="remove_account_from_organization failed",
    ):
        await remove_account_from_organization("bad")


# ---------------------------------------------------------------------------
# list_roots
# ---------------------------------------------------------------------------


async def test_list_roots_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Roots": [_root_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_roots()
    assert len(result) == 1
    assert isinstance(result[0], RootResult)


async def test_list_roots_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Roots": [_root_dict(Id="r-1")],
            "NextToken": "tok",
        },
        {"Roots": [_root_dict(Id="r-2")]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_roots()
    assert len(result) == 2


async def test_list_roots_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Roots": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_roots()
    assert result == []


async def test_list_roots_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_roots()


async def test_list_roots_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_roots failed"
    ):
        await list_roots()


# ---------------------------------------------------------------------------
# list_children
# ---------------------------------------------------------------------------


async def test_list_children_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Children": [{"Id": "222", "Type": "ACCOUNT"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_children("r-abc1", "ACCOUNT")
    assert len(result) == 1
    assert result[0]["Id"] == "222"


async def test_list_children_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Children": [{"Id": "111", "Type": "ACCOUNT"}],
            "NextToken": "tok",
        },
        {
            "Children": [{"Id": "222", "Type": "ACCOUNT"}]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_children("r-abc1", "ACCOUNT")
    assert len(result) == 2


async def test_list_children_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Children": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_children("r-abc1", "ACCOUNT")
    assert result == []


async def test_list_children_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_children("r-1", "ACCOUNT")


async def test_list_children_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_children failed"
    ):
        await list_children("r-1", "ACCOUNT")


# ---------------------------------------------------------------------------
# list_parents
# ---------------------------------------------------------------------------


async def test_list_parents_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Parents": [{"Id": "r-abc1", "Type": "ROOT"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_parents("222222222222")
    assert len(result) == 1
    assert result[0]["Type"] == "ROOT"


async def test_list_parents_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Parents": [{"Id": "r-1", "Type": "ROOT"}],
            "NextToken": "tok",
        },
        {"Parents": [{"Id": "ou-1", "Type": "OU"}]},
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_parents("222")
    assert len(result) == 2


async def test_list_parents_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Parents": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_parents("222")
    assert result == []


async def test_list_parents_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_parents("bad")


async def test_list_parents_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_parents failed"
    ):
        await list_parents("bad")


# ---------------------------------------------------------------------------
# list_policies
# ---------------------------------------------------------------------------


async def test_list_policies_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policies": [_policy_summary_dict()]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_policies()
    assert len(result) == 1
    assert isinstance(result[0], PolicySummaryResult)


async def test_list_policies_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Policies": [
                _policy_summary_dict(Id="p-1", Name="P1")
            ],
            "NextToken": "tok",
        },
        {
            "Policies": [
                _policy_summary_dict(Id="p-2", Name="P2")
            ]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_policies()
    assert len(result) == 2


async def test_list_policies_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Policies": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_policies()
    assert result == []


async def test_list_policies_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_policies()


async def test_list_policies_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_policies failed"
    ):
        await list_policies()


# ---------------------------------------------------------------------------
# describe_policy
# ---------------------------------------------------------------------------


async def test_describe_policy_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policy": _policy_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_policy("p-abc123")
    assert isinstance(result, PolicyResult)
    assert result.id == "p-abc123"
    assert result.content != ""


async def test_describe_policy_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_policy("bad")


async def test_describe_policy_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="describe_policy failed"
    ):
        await describe_policy("bad")


# ---------------------------------------------------------------------------
# create_policy
# ---------------------------------------------------------------------------


async def test_create_policy_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policy": _policy_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await create_policy(
        "DenyS3", "{}", "Deny S3 access"
    )
    assert isinstance(result, PolicyResult)
    assert result.name == "DenyS3"


async def test_create_policy_with_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policy": _policy_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await create_policy(
        "Deny",
        "{}",
        "desc",
        policy_type="TAG_POLICY",
        region_name="us-east-1",
    )
    kw = mock_client.call.call_args[1]
    assert kw["Type"] == "TAG_POLICY"


async def test_create_policy_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await create_policy("X", "{}", "desc")


async def test_create_policy_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="create_policy failed"
    ):
        await create_policy("X", "{}", "desc")


# ---------------------------------------------------------------------------
# update_policy
# ---------------------------------------------------------------------------


async def test_update_policy_all_fields(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policy": _policy_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await update_policy(
        "p-abc123",
        name="New",
        content="{}",
        description="Updated",
    )
    assert isinstance(result, PolicyResult)
    kw = mock_client.call.call_args[1]
    assert kw["Name"] == "New"
    assert kw["Content"] == "{}"
    assert kw["Description"] == "Updated"


async def test_update_policy_no_optional(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policy": _policy_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await update_policy("p-abc123", region_name="us-east-1")
    kw = mock_client.call.call_args[1]
    assert "Name" not in kw
    assert "Content" not in kw
    assert "Description" not in kw


async def test_update_policy_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_policy("bad")


async def test_update_policy_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="update_policy failed"
    ):
        await update_policy("bad")


# ---------------------------------------------------------------------------
# delete_policy
# ---------------------------------------------------------------------------


async def test_delete_policy_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await delete_policy("p-abc123")
    mock_client.call.assert_awaited_once()


async def test_delete_policy_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_policy("bad")


async def test_delete_policy_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="delete_policy failed"
    ):
        await delete_policy("bad")


# ---------------------------------------------------------------------------
# attach_policy
# ---------------------------------------------------------------------------


async def test_attach_policy_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await attach_policy("p-abc123", "r-abc1")
    mock_client.call.assert_awaited_once()


async def test_attach_policy_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await attach_policy(
        "p-abc123", "r-abc1", region_name="us-east-1"
    )
    mock_client.call.assert_awaited_once()


async def test_attach_policy_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await attach_policy("bad", "bad")


async def test_attach_policy_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="attach_policy failed"
    ):
        await attach_policy("bad", "bad")


# ---------------------------------------------------------------------------
# detach_policy
# ---------------------------------------------------------------------------


async def test_detach_policy_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await detach_policy("p-abc123", "r-abc1")
    mock_client.call.assert_awaited_once()


async def test_detach_policy_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await detach_policy("bad", "bad")


async def test_detach_policy_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="detach_policy failed"
    ):
        await detach_policy("bad", "bad")


# ---------------------------------------------------------------------------
# enable_policy_type
# ---------------------------------------------------------------------------


async def test_enable_policy_type_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Root": _root_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await enable_policy_type("r-abc1")
    assert isinstance(result, RootResult)
    assert result.id == "r-abc1"

async def test_enable_policy_type_runtime_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await enable_policy_type("bad")


async def test_enable_policy_type_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="enable_policy_type failed"
    ):
        await enable_policy_type("bad")


# ---------------------------------------------------------------------------
# disable_policy_type
# ---------------------------------------------------------------------------


async def test_disable_policy_type_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Root": _root_dict()
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await disable_policy_type("r-abc1")
    assert isinstance(result, RootResult)
    assert result.id == "r-abc1"


async def test_disable_policy_type_runtime_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await disable_policy_type("bad")


async def test_disable_policy_type_generic_error(
    monkeypatch,
):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="disable_policy_type failed"
    ):
        await disable_policy_type("bad")


# ---------------------------------------------------------------------------
# list_tags_for_resource
# ---------------------------------------------------------------------------


async def test_list_tags_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Tags": [{"Key": "env", "Value": "prod"}]
    }
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_tags_for_resource("222222222222")
    assert len(result) == 1
    assert result[0]["Key"] == "env"


async def test_list_tags_pagination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {
            "Tags": [{"Key": "env", "Value": "prod"}],
            "NextToken": "tok",
        },
        {
            "Tags": [{"Key": "team", "Value": "eng"}]
        },
    ]
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_tags_for_resource("222222222222")
    assert len(result) == 2


async def test_list_tags_empty(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Tags": []}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    result = await list_tags_for_resource("222222222222")
    assert result == []


async def test_list_tags_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await list_tags_for_resource("bad")


async def test_list_tags_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="list_tags_for_resource failed"
    ):
        await list_tags_for_resource("bad")


# ---------------------------------------------------------------------------
# tag_resource
# ---------------------------------------------------------------------------


async def test_tag_resource_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await tag_resource(
        "222222222222",
        [{"Key": "env", "Value": "prod"}],
    )
    mock_client.call.assert_awaited_once()


async def test_tag_resource_with_region(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    await tag_resource(
        "222222222222",
        [{"Key": "env", "Value": "prod"}],
        region_name="us-east-1",
    )
    mock_client.call.assert_awaited_once()


async def test_tag_resource_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await tag_resource("bad", [{"Key": "k", "Value": "v"}])


async def test_tag_resource_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="tag_resource failed"
    ):
        await tag_resource("bad", [{"Key": "k", "Value": "v"}])


async def test_cancel_handshake(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_handshake("test-handshake_id", )
    mock_client.call.assert_called_once()


async def test_cancel_handshake_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_handshake("test-handshake_id", )


async def test_close_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await close_account("test-account_id", )
    mock_client.call.assert_called_once()


async def test_close_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await close_account("test-account_id", )


async def test_create_gov_cloud_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_gov_cloud_account("test-email", "test-account_name", )
    mock_client.call.assert_called_once()


async def test_create_gov_cloud_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_gov_cloud_account("test-email", "test-account_name", )


async def test_decline_handshake(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await decline_handshake("test-handshake_id", )
    mock_client.call.assert_called_once()


async def test_decline_handshake_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await decline_handshake("test-handshake_id", )


async def test_delete_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_organization()
    mock_client.call.assert_called_once()


async def test_delete_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_organization()


async def test_delete_organizational_unit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_organizational_unit("test-organizational_unit_id", )
    mock_client.call.assert_called_once()


async def test_delete_organizational_unit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_organizational_unit("test-organizational_unit_id", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy()
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy()


async def test_deregister_delegated_administrator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_delegated_administrator("test-account_id", "test-service_principal", )
    mock_client.call.assert_called_once()


async def test_deregister_delegated_administrator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_delegated_administrator("test-account_id", "test-service_principal", )


async def test_describe_create_account_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_create_account_status("test-create_account_request_id", )
    mock_client.call.assert_called_once()


async def test_describe_create_account_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_create_account_status("test-create_account_request_id", )


async def test_describe_effective_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_effective_policy("test-policy_type", )
    mock_client.call.assert_called_once()


async def test_describe_effective_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_effective_policy("test-policy_type", )


async def test_describe_handshake(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_handshake("test-handshake_id", )
    mock_client.call.assert_called_once()


async def test_describe_handshake_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_handshake("test-handshake_id", )


async def test_describe_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_resource_policy()
    mock_client.call.assert_called_once()


async def test_describe_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_resource_policy()


async def test_disable_aws_service_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_aws_service_access("test-service_principal", )
    mock_client.call.assert_called_once()


async def test_disable_aws_service_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_aws_service_access("test-service_principal", )


async def test_enable_all_features(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_all_features()
    mock_client.call.assert_called_once()


async def test_enable_all_features_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_all_features()


async def test_enable_aws_service_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_aws_service_access("test-service_principal", )
    mock_client.call.assert_called_once()


async def test_enable_aws_service_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_aws_service_access("test-service_principal", )


async def test_leave_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await leave_organization()
    mock_client.call.assert_called_once()


async def test_leave_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await leave_organization()


async def test_list_accounts_with_invalid_effective_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_accounts_with_invalid_effective_policy("test-policy_type", )
    mock_client.call.assert_called_once()


async def test_list_accounts_with_invalid_effective_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_accounts_with_invalid_effective_policy("test-policy_type", )


async def test_list_aws_service_access_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_aws_service_access_for_organization()
    mock_client.call.assert_called_once()


async def test_list_aws_service_access_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_aws_service_access_for_organization()


async def test_list_create_account_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_create_account_status()
    mock_client.call.assert_called_once()


async def test_list_create_account_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_create_account_status()


async def test_list_delegated_administrators(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_delegated_administrators()
    mock_client.call.assert_called_once()


async def test_list_delegated_administrators_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_delegated_administrators()


async def test_list_delegated_services_for_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_delegated_services_for_account("test-account_id", )
    mock_client.call.assert_called_once()


async def test_list_delegated_services_for_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_delegated_services_for_account("test-account_id", )


async def test_list_effective_policy_validation_errors(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_effective_policy_validation_errors("test-account_id", "test-policy_type", )
    mock_client.call.assert_called_once()


async def test_list_effective_policy_validation_errors_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_effective_policy_validation_errors("test-account_id", "test-policy_type", )


async def test_list_handshakes_for_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_handshakes_for_account()
    mock_client.call.assert_called_once()


async def test_list_handshakes_for_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_handshakes_for_account()


async def test_list_handshakes_for_organization(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_handshakes_for_organization()
    mock_client.call.assert_called_once()


async def test_list_handshakes_for_organization_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_handshakes_for_organization()


async def test_list_policies_for_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policies_for_target("test-target_id", "test-filter", )
    mock_client.call.assert_called_once()


async def test_list_policies_for_target_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policies_for_target("test-target_id", "test-filter", )


async def test_list_targets_for_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_targets_for_policy("test-policy_id", )
    mock_client.call.assert_called_once()


async def test_list_targets_for_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_targets_for_policy("test-policy_id", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-content", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-content", )


async def test_register_delegated_administrator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_delegated_administrator("test-account_id", "test-service_principal", )
    mock_client.call.assert_called_once()


async def test_register_delegated_administrator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_delegated_administrator("test-account_id", "test-service_principal", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_id", [], )


async def test_update_organizational_unit(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_organizational_unit("test-organizational_unit_id", )
    mock_client.call.assert_called_once()


async def test_update_organizational_unit_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.organizations.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_organizational_unit("test-organizational_unit_id", )


@pytest.mark.asyncio
async def test_create_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import create_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await create_account("test-email", 1, role_name="test-role_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_gov_cloud_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import create_gov_cloud_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await create_gov_cloud_account("test-email", 1, role_name="test-role_name", iam_user_access_to_billing="test-iam_user_access_to_billing", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_effective_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import describe_effective_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await describe_effective_policy("test-policy_type", target_id="test-target_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_accounts_with_invalid_effective_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_accounts_with_invalid_effective_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_accounts_with_invalid_effective_policy("test-policy_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_aws_service_access_for_organization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_aws_service_access_for_organization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_aws_service_access_for_organization(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_create_account_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_create_account_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_create_account_status(states="test-states", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_delegated_administrators_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_delegated_administrators
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_delegated_administrators(service_principal="test-service_principal", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_delegated_services_for_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_delegated_services_for_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_delegated_services_for_account(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_effective_policy_validation_errors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_effective_policy_validation_errors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_effective_policy_validation_errors(1, "test-policy_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_handshakes_for_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_handshakes_for_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_handshakes_for_account(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_handshakes_for_organization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_handshakes_for_organization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_handshakes_for_organization(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_policies_for_target_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_policies_for_target
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_policies_for_target("test-target_id", "test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_targets_for_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import list_targets_for_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await list_targets_for_policy("test-policy_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import put_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await put_resource_policy("test-content", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_organizational_unit_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.organizations import update_organizational_unit
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.organizations.async_client", lambda *a, **kw: mock_client)
    await update_organizational_unit("test-organizational_unit_id", name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()
