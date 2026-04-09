"""Tests for aws_util.organizations module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.organizations as mod
from aws_util.organizations import (
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


def _mock_client_with_paginator(
    pages: list[dict],
) -> MagicMock:
    """Return a mock client whose paginator yields given pages."""
    mock = MagicMock()
    paginator = MagicMock()
    paginator.paginate.return_value = iter(pages)
    mock.get_paginator.return_value = paginator
    return mock


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
            "Arn": "arn:aws:organizations::111:policy/o-abc123/service_control_policy/p-abc123",
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
        "Arn": "arn:aws:organizations::111:policy/o-abc123/service_control_policy/p-abc123",
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
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_org_result_defaults(self):
        r = OrgResult(id="o-1", arn="arn:org")
        assert r.id == "o-1"
        assert r.master_account_arn == ""
        assert r.feature_set == ""
        assert r.available_policy_types == []
        assert r.extra == {}

    def test_org_result_frozen(self):
        r = OrgResult(id="o-1", arn="arn:org")
        with pytest.raises(Exception):
            r.id = "o-2"  # type: ignore[misc]

    def test_ou_result_defaults(self):
        r = OUResult(id="ou-1", arn="arn:ou")
        assert r.name == ""
        assert r.extra == {}

    def test_ou_result_frozen(self):
        r = OUResult(id="ou-1", arn="arn:ou")
        with pytest.raises(Exception):
            r.id = "ou-2"  # type: ignore[misc]

    def test_account_result_defaults(self):
        r = AccountResult(id="111", arn="arn:acct")
        assert r.name == ""
        assert r.email == ""
        assert r.status == ""
        assert r.joined_method == ""
        assert r.joined_timestamp is None
        assert r.extra == {}

    def test_account_result_frozen(self):
        r = AccountResult(id="111", arn="arn:acct")
        with pytest.raises(Exception):
            r.id = "222"  # type: ignore[misc]

    def test_policy_result_defaults(self):
        r = PolicyResult(id="p-1", arn="arn:pol")
        assert r.name == ""
        assert r.content == ""
        assert r.aws_managed is False
        assert r.extra == {}

    def test_policy_summary_result_defaults(self):
        r = PolicySummaryResult(id="p-1", arn="arn:pol")
        assert r.name == ""
        assert r.description == ""
        assert r.type == ""
        assert r.aws_managed is False
        assert r.extra == {}

    def test_handshake_result_defaults(self):
        r = HandshakeResult(id="h-1", arn="arn:hs")
        assert r.state == ""
        assert r.action == ""
        assert r.resources == []
        assert r.parties == []
        assert r.requested_timestamp is None
        assert r.expiration_timestamp is None
        assert r.extra == {}

    def test_root_result_defaults(self):
        r = RootResult(id="r-1", arn="arn:root")
        assert r.name == ""
        assert r.policy_types == []
        assert r.extra == {}


# ---------------------------------------------------------------------------
# create_organization
# ---------------------------------------------------------------------------


class TestCreateOrganization:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.create_organization.return_value = {
            "Organization": _org_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = create_organization(region_name=REGION)
        assert isinstance(result, OrgResult)
        assert result.id == "o-abc123"
        assert result.feature_set == "ALL"
        mock.create_organization.assert_called_once_with(
            FeatureSet="ALL"
        )

    def test_custom_feature_set(self, monkeypatch):
        mock = MagicMock()
        mock.create_organization.return_value = {
            "Organization": _org_dict(
                FeatureSet="CONSOLIDATED_BILLING"
            )
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = create_organization(
            feature_set="CONSOLIDATED_BILLING",
            region_name=REGION,
        )
        assert result.feature_set == "CONSOLIDATED_BILLING"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.create_organization.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="create_organization failed"
        ):
            create_organization(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_organization
# ---------------------------------------------------------------------------


class TestDescribeOrganization:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.describe_organization.return_value = {
            "Organization": _org_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_organization(region_name=REGION)
        assert isinstance(result, OrgResult)
        assert result.id == "o-abc123"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_organization.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="describe_organization failed"
        ):
            describe_organization(region_name=REGION)


# ---------------------------------------------------------------------------
# create_organizational_unit
# ---------------------------------------------------------------------------


class TestCreateOrganizationalUnit:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.create_organizational_unit.return_value = {
            "OrganizationalUnit": _ou_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = create_organizational_unit(
            "r-abc1", "Engineering", region_name=REGION
        )
        assert isinstance(result, OUResult)
        assert result.name == "Engineering"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.create_organizational_unit.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="create_organizational_unit failed",
        ):
            create_organizational_unit(
                "r-abc1", "Bad", region_name=REGION
            )


# ---------------------------------------------------------------------------
# describe_organizational_unit
# ---------------------------------------------------------------------------


class TestDescribeOrganizationalUnit:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.describe_organizational_unit.return_value = {
            "OrganizationalUnit": _ou_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_organizational_unit(
            "ou-abc-123", region_name=REGION
        )
        assert isinstance(result, OUResult)
        assert result.id == "ou-abc-123"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_organizational_unit.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="describe_organizational_unit failed",
        ):
            describe_organizational_unit(
                "ou-bad", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_organizational_units_for_parent
# ---------------------------------------------------------------------------


class TestListOrganizationalUnitsForParent:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"OrganizationalUnits": [_ou_dict()]}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_organizational_units_for_parent(
            "r-abc1", region_name=REGION
        )
        assert len(result) == 1
        assert isinstance(result[0], OUResult)

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"OrganizationalUnits": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_organizational_units_for_parent(
            "r-abc1", region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="list_organizational_units_for_parent failed",
        ):
            list_organizational_units_for_parent(
                "r-abc1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_accounts
# ---------------------------------------------------------------------------


class TestListAccounts:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Accounts": [_account_dict()]}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_accounts(region_name=REGION)
        assert len(result) == 1
        assert isinstance(result[0], AccountResult)
        assert result[0].name == "dev-account"

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Accounts": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_accounts(region_name=REGION)
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_accounts failed"
        ):
            list_accounts(region_name=REGION)


# ---------------------------------------------------------------------------
# list_accounts_for_parent
# ---------------------------------------------------------------------------


class TestListAccountsForParent:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Accounts": [_account_dict()]}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_accounts_for_parent(
            "r-abc1", region_name=REGION
        )
        assert len(result) == 1

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Accounts": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_accounts_for_parent(
            "r-abc1", region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="list_accounts_for_parent failed",
        ):
            list_accounts_for_parent(
                "r-abc1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# describe_account
# ---------------------------------------------------------------------------


class TestDescribeAccount:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.describe_account.return_value = {
            "Account": _account_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_account(
            "222222222222", region_name=REGION
        )
        assert isinstance(result, AccountResult)
        assert result.id == "222222222222"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_account.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="describe_account failed"
        ):
            describe_account("bad-id", region_name=REGION)


# ---------------------------------------------------------------------------
# create_account
# ---------------------------------------------------------------------------


class TestCreateAccount:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.create_account.return_value = {
            "CreateAccountStatus": {
                "Id": "car-abc",
                "AccountName": "new-acct",
                "State": "IN_PROGRESS",
            }
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = create_account(
            "new@example.com",
            "new-acct",
            region_name=REGION,
        )
        assert result["State"] == "IN_PROGRESS"

    def test_with_role_name(self, monkeypatch):
        mock = MagicMock()
        mock.create_account.return_value = {
            "CreateAccountStatus": {"Id": "car-abc"}
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        create_account(
            "new@example.com",
            "new-acct",
            role_name="OrganizationAccountAccessRole",
            region_name=REGION,
        )
        call_kwargs = mock.create_account.call_args[1]
        assert (
            call_kwargs["RoleName"]
            == "OrganizationAccountAccessRole"
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.create_account.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="create_account failed"
        ):
            create_account(
                "x@y.com", "acct", region_name=REGION
            )


# ---------------------------------------------------------------------------
# invite_account_to_organization
# ---------------------------------------------------------------------------


class TestInviteAccountToOrganization:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.invite_account_to_organization.return_value = {
            "Handshake": _handshake_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = invite_account_to_organization(
            "333333333333", region_name=REGION
        )
        assert isinstance(result, HandshakeResult)
        assert result.id == "h-abc123"

    def test_with_notes(self, monkeypatch):
        mock = MagicMock()
        mock.invite_account_to_organization.return_value = {
            "Handshake": _handshake_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        invite_account_to_organization(
            "333333333333",
            notes="Please join",
            region_name=REGION,
        )
        call_kwargs = (
            mock.invite_account_to_organization.call_args[1]
        )
        assert call_kwargs["Notes"] == "Please join"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.invite_account_to_organization.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="invite_account_to_organization failed",
        ):
            invite_account_to_organization(
                "bad", region_name=REGION
            )


# ---------------------------------------------------------------------------
# accept_handshake
# ---------------------------------------------------------------------------


class TestAcceptHandshake:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.accept_handshake.return_value = {
            "Handshake": _handshake_dict(State="ACCEPTED")
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = accept_handshake(
            "h-abc123", region_name=REGION
        )
        assert isinstance(result, HandshakeResult)
        assert result.state == "ACCEPTED"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.accept_handshake.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="accept_handshake failed"
        ):
            accept_handshake("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# move_account
# ---------------------------------------------------------------------------


class TestMoveAccount:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.move_account.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        move_account(
            "222222222222",
            "r-abc1",
            "ou-abc-123",
            region_name=REGION,
        )
        mock.move_account.assert_called_once()

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.move_account.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="move_account failed"
        ):
            move_account(
                "bad", "r-1", "ou-1", region_name=REGION
            )


# ---------------------------------------------------------------------------
# remove_account_from_organization
# ---------------------------------------------------------------------------


class TestRemoveAccountFromOrganization:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.remove_account_from_organization.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        remove_account_from_organization(
            "222222222222", region_name=REGION
        )
        mock.remove_account_from_organization.assert_called_once()

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.remove_account_from_organization.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="remove_account_from_organization failed",
        ):
            remove_account_from_organization(
                "bad", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_roots
# ---------------------------------------------------------------------------


class TestListRoots:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Roots": [_root_dict()]}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_roots(region_name=REGION)
        assert len(result) == 1
        assert isinstance(result[0], RootResult)
        assert result[0].id == "r-abc1"

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Roots": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_roots(region_name=REGION)
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_roots failed"
        ):
            list_roots(region_name=REGION)


# ---------------------------------------------------------------------------
# list_children
# ---------------------------------------------------------------------------


class TestListChildren:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "Children": [
                        {"Id": "222", "Type": "ACCOUNT"}
                    ]
                }
            ]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_children(
            "r-abc1", "ACCOUNT", region_name=REGION
        )
        assert len(result) == 1
        assert result[0]["Id"] == "222"

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Children": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_children(
            "r-abc1", "ACCOUNT", region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_children failed"
        ):
            list_children(
                "r-abc1", "ACCOUNT", region_name=REGION
            )


# ---------------------------------------------------------------------------
# list_parents
# ---------------------------------------------------------------------------


class TestListParents:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "Parents": [
                        {"Id": "r-abc1", "Type": "ROOT"}
                    ]
                }
            ]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_parents(
            "222222222222", region_name=REGION
        )
        assert len(result) == 1
        assert result[0]["Type"] == "ROOT"

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Parents": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_parents(
            "222222222222", region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_parents failed"
        ):
            list_parents("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# list_policies
# ---------------------------------------------------------------------------


class TestListPolicies:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Policies": [_policy_summary_dict()]}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_policies(region_name=REGION)
        assert len(result) == 1
        assert isinstance(result[0], PolicySummaryResult)
        assert result[0].name == "DenyS3"

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Policies": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_policies(region_name=REGION)
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="list_policies failed"
        ):
            list_policies(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_policy
# ---------------------------------------------------------------------------


class TestDescribePolicy:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.describe_policy.return_value = {
            "Policy": _policy_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = describe_policy(
            "p-abc123", region_name=REGION
        )
        assert isinstance(result, PolicyResult)
        assert result.id == "p-abc123"
        assert result.content != ""

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.describe_policy.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="describe_policy failed"
        ):
            describe_policy("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# create_policy
# ---------------------------------------------------------------------------


class TestCreatePolicy:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.create_policy.return_value = {
            "Policy": _policy_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = create_policy(
            "DenyS3",
            '{"Version":"2012-10-17","Statement":[]}',
            "Deny S3 access",
            region_name=REGION,
        )
        assert isinstance(result, PolicyResult)
        assert result.name == "DenyS3"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.create_policy.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="create_policy failed"
        ):
            create_policy(
                "bad", "{}", "desc", region_name=REGION
            )


# ---------------------------------------------------------------------------
# update_policy
# ---------------------------------------------------------------------------


class TestUpdatePolicy:
    def test_success_all_fields(self, monkeypatch):
        mock = MagicMock()
        mock.update_policy.return_value = {
            "Policy": _policy_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = update_policy(
            "p-abc123",
            name="NewName",
            content="{}",
            description="Updated",
            region_name=REGION,
        )
        assert isinstance(result, PolicyResult)
        call_kwargs = mock.update_policy.call_args[1]
        assert call_kwargs["Name"] == "NewName"
        assert call_kwargs["Content"] == "{}"
        assert call_kwargs["Description"] == "Updated"

    def test_success_no_optional(self, monkeypatch):
        mock = MagicMock()
        mock.update_policy.return_value = {
            "Policy": _policy_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = update_policy(
            "p-abc123", region_name=REGION
        )
        assert isinstance(result, PolicyResult)
        call_kwargs = mock.update_policy.call_args[1]
        assert "Name" not in call_kwargs
        assert "Content" not in call_kwargs
        assert "Description" not in call_kwargs

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.update_policy.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="update_policy failed"
        ):
            update_policy("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_policy
# ---------------------------------------------------------------------------


class TestDeletePolicy:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.delete_policy.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        delete_policy("p-abc123", region_name=REGION)
        mock.delete_policy.assert_called_once_with(
            PolicyId="p-abc123"
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.delete_policy.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="delete_policy failed"
        ):
            delete_policy("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# attach_policy
# ---------------------------------------------------------------------------


class TestAttachPolicy:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.attach_policy.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        attach_policy(
            "p-abc123", "r-abc1", region_name=REGION
        )
        mock.attach_policy.assert_called_once_with(
            PolicyId="p-abc123", TargetId="r-abc1"
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.attach_policy.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="attach_policy failed"
        ):
            attach_policy("bad", "bad", region_name=REGION)


# ---------------------------------------------------------------------------
# detach_policy
# ---------------------------------------------------------------------------


class TestDetachPolicy:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.detach_policy.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        detach_policy(
            "p-abc123", "r-abc1", region_name=REGION
        )
        mock.detach_policy.assert_called_once_with(
            PolicyId="p-abc123", TargetId="r-abc1"
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.detach_policy.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="detach_policy failed"
        ):
            detach_policy("bad", "bad", region_name=REGION)


# ---------------------------------------------------------------------------
# enable_policy_type
# ---------------------------------------------------------------------------


class TestEnablePolicyType:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.enable_policy_type.return_value = {
            "Root": _root_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = enable_policy_type(
            "r-abc1", region_name=REGION
        )
        assert isinstance(result, RootResult)
        assert result.id == "r-abc1"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.enable_policy_type.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="enable_policy_type failed"
        ):
            enable_policy_type("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# disable_policy_type
# ---------------------------------------------------------------------------


class TestDisablePolicyType:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.disable_policy_type.return_value = {
            "Root": _root_dict()
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = disable_policy_type(
            "r-abc1", region_name=REGION
        )
        assert isinstance(result, RootResult)
        assert result.id == "r-abc1"

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.disable_policy_type.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="disable_policy_type failed"
        ):
            disable_policy_type("bad", region_name=REGION)


# ---------------------------------------------------------------------------
# list_tags_for_resource
# ---------------------------------------------------------------------------


class TestListTagsForResource:
    def test_success(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [
                {
                    "Tags": [
                        {"Key": "env", "Value": "prod"}
                    ]
                }
            ]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_tags_for_resource(
            "222222222222", region_name=REGION
        )
        assert len(result) == 1
        assert result[0]["Key"] == "env"

    def test_empty(self, monkeypatch):
        mock = _mock_client_with_paginator(
            [{"Tags": []}]
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        result = list_tags_for_resource(
            "222222222222", region_name=REGION
        )
        assert result == []

    def test_error(self, monkeypatch):
        mock = MagicMock()
        paginator = MagicMock()
        paginator.paginate.side_effect = _client_error()
        mock.get_paginator.return_value = paginator
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError,
            match="list_tags_for_resource failed",
        ):
            list_tags_for_resource(
                "bad", region_name=REGION
            )


# ---------------------------------------------------------------------------
# tag_resource
# ---------------------------------------------------------------------------


class TestTagResource:
    def test_success(self, monkeypatch):
        mock = MagicMock()
        mock.tag_resource.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        tag_resource(
            "222222222222",
            [{"Key": "env", "Value": "prod"}],
            region_name=REGION,
        )
        mock.tag_resource.assert_called_once_with(
            ResourceId="222222222222",
            Tags=[{"Key": "env", "Value": "prod"}],
        )

    def test_error(self, monkeypatch):
        mock = MagicMock()
        mock.tag_resource.side_effect = _client_error()
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock
        )
        with pytest.raises(
            RuntimeError, match="tag_resource failed"
        ):
            tag_resource(
                "bad", [{"Key": "k", "Value": "v"}],
                region_name=REGION,
            )


def test_cancel_handshake(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_handshake.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    cancel_handshake("test-handshake_id", region_name=REGION)
    mock_client.cancel_handshake.assert_called_once()


def test_cancel_handshake_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_handshake.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_handshake",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel handshake"):
        cancel_handshake("test-handshake_id", region_name=REGION)


def test_close_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.close_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    close_account("test-account_id", region_name=REGION)
    mock_client.close_account.assert_called_once()


def test_close_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.close_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "close_account",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to close account"):
        close_account("test-account_id", region_name=REGION)


def test_create_gov_cloud_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_gov_cloud_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    create_gov_cloud_account("test-email", "test-account_name", region_name=REGION)
    mock_client.create_gov_cloud_account.assert_called_once()


def test_create_gov_cloud_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_gov_cloud_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_gov_cloud_account",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create gov cloud account"):
        create_gov_cloud_account("test-email", "test-account_name", region_name=REGION)


def test_decline_handshake(monkeypatch):
    mock_client = MagicMock()
    mock_client.decline_handshake.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    decline_handshake("test-handshake_id", region_name=REGION)
    mock_client.decline_handshake.assert_called_once()


def test_decline_handshake_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.decline_handshake.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decline_handshake",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to decline handshake"):
        decline_handshake("test-handshake_id", region_name=REGION)


def test_delete_organization(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organization.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    delete_organization(region_name=REGION)
    mock_client.delete_organization.assert_called_once()


def test_delete_organization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_organization",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete organization"):
        delete_organization(region_name=REGION)


def test_delete_organizational_unit(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organizational_unit.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    delete_organizational_unit("test-organizational_unit_id", region_name=REGION)
    mock_client.delete_organizational_unit.assert_called_once()


def test_delete_organizational_unit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_organizational_unit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_organizational_unit",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete organizational unit"):
        delete_organizational_unit("test-organizational_unit_id", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy(region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy(region_name=REGION)


def test_deregister_delegated_administrator(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_delegated_administrator.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    deregister_delegated_administrator("test-account_id", "test-service_principal", region_name=REGION)
    mock_client.deregister_delegated_administrator.assert_called_once()


def test_deregister_delegated_administrator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_delegated_administrator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_delegated_administrator",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister delegated administrator"):
        deregister_delegated_administrator("test-account_id", "test-service_principal", region_name=REGION)


def test_describe_create_account_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_create_account_status.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    describe_create_account_status("test-create_account_request_id", region_name=REGION)
    mock_client.describe_create_account_status.assert_called_once()


def test_describe_create_account_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_create_account_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_create_account_status",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe create account status"):
        describe_create_account_status("test-create_account_request_id", region_name=REGION)


def test_describe_effective_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_effective_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    describe_effective_policy("test-policy_type", region_name=REGION)
    mock_client.describe_effective_policy.assert_called_once()


def test_describe_effective_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_effective_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_effective_policy",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe effective policy"):
        describe_effective_policy("test-policy_type", region_name=REGION)


def test_describe_handshake(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_handshake.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    describe_handshake("test-handshake_id", region_name=REGION)
    mock_client.describe_handshake.assert_called_once()


def test_describe_handshake_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_handshake.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_handshake",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe handshake"):
        describe_handshake("test-handshake_id", region_name=REGION)


def test_describe_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    describe_resource_policy(region_name=REGION)
    mock_client.describe_resource_policy.assert_called_once()


def test_describe_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_resource_policy",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe resource policy"):
        describe_resource_policy(region_name=REGION)


def test_disable_aws_service_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_aws_service_access.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    disable_aws_service_access("test-service_principal", region_name=REGION)
    mock_client.disable_aws_service_access.assert_called_once()


def test_disable_aws_service_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_aws_service_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_aws_service_access",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable aws service access"):
        disable_aws_service_access("test-service_principal", region_name=REGION)


def test_enable_all_features(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_all_features.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    enable_all_features(region_name=REGION)
    mock_client.enable_all_features.assert_called_once()


def test_enable_all_features_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_all_features.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_all_features",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable all features"):
        enable_all_features(region_name=REGION)


def test_enable_aws_service_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_aws_service_access.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    enable_aws_service_access("test-service_principal", region_name=REGION)
    mock_client.enable_aws_service_access.assert_called_once()


def test_enable_aws_service_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_aws_service_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_aws_service_access",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable aws service access"):
        enable_aws_service_access("test-service_principal", region_name=REGION)


def test_leave_organization(monkeypatch):
    mock_client = MagicMock()
    mock_client.leave_organization.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    leave_organization(region_name=REGION)
    mock_client.leave_organization.assert_called_once()


def test_leave_organization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.leave_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "leave_organization",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to leave organization"):
        leave_organization(region_name=REGION)


def test_list_accounts_with_invalid_effective_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_accounts_with_invalid_effective_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_accounts_with_invalid_effective_policy("test-policy_type", region_name=REGION)
    mock_client.list_accounts_with_invalid_effective_policy.assert_called_once()


def test_list_accounts_with_invalid_effective_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_accounts_with_invalid_effective_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_accounts_with_invalid_effective_policy",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list accounts with invalid effective policy"):
        list_accounts_with_invalid_effective_policy("test-policy_type", region_name=REGION)


def test_list_aws_service_access_for_organization(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aws_service_access_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_aws_service_access_for_organization(region_name=REGION)
    mock_client.list_aws_service_access_for_organization.assert_called_once()


def test_list_aws_service_access_for_organization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_aws_service_access_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_aws_service_access_for_organization",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list aws service access for organization"):
        list_aws_service_access_for_organization(region_name=REGION)


def test_list_create_account_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_create_account_status.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_create_account_status(region_name=REGION)
    mock_client.list_create_account_status.assert_called_once()


def test_list_create_account_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_create_account_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_create_account_status",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list create account status"):
        list_create_account_status(region_name=REGION)


def test_list_delegated_administrators(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delegated_administrators.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_delegated_administrators(region_name=REGION)
    mock_client.list_delegated_administrators.assert_called_once()


def test_list_delegated_administrators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delegated_administrators.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_delegated_administrators",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list delegated administrators"):
        list_delegated_administrators(region_name=REGION)


def test_list_delegated_services_for_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delegated_services_for_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_delegated_services_for_account("test-account_id", region_name=REGION)
    mock_client.list_delegated_services_for_account.assert_called_once()


def test_list_delegated_services_for_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_delegated_services_for_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_delegated_services_for_account",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list delegated services for account"):
        list_delegated_services_for_account("test-account_id", region_name=REGION)


def test_list_effective_policy_validation_errors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_effective_policy_validation_errors.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_effective_policy_validation_errors("test-account_id", "test-policy_type", region_name=REGION)
    mock_client.list_effective_policy_validation_errors.assert_called_once()


def test_list_effective_policy_validation_errors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_effective_policy_validation_errors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_effective_policy_validation_errors",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list effective policy validation errors"):
        list_effective_policy_validation_errors("test-account_id", "test-policy_type", region_name=REGION)


def test_list_handshakes_for_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_handshakes_for_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_handshakes_for_account(region_name=REGION)
    mock_client.list_handshakes_for_account.assert_called_once()


def test_list_handshakes_for_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_handshakes_for_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_handshakes_for_account",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list handshakes for account"):
        list_handshakes_for_account(region_name=REGION)


def test_list_handshakes_for_organization(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_handshakes_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_handshakes_for_organization(region_name=REGION)
    mock_client.list_handshakes_for_organization.assert_called_once()


def test_list_handshakes_for_organization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_handshakes_for_organization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_handshakes_for_organization",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list handshakes for organization"):
        list_handshakes_for_organization(region_name=REGION)


def test_list_policies_for_target(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policies_for_target.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_policies_for_target("test-target_id", "test-filter", region_name=REGION)
    mock_client.list_policies_for_target.assert_called_once()


def test_list_policies_for_target_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policies_for_target.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policies_for_target",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list policies for target"):
        list_policies_for_target("test-target_id", "test-filter", region_name=REGION)


def test_list_targets_for_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_targets_for_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_targets_for_policy("test-policy_id", region_name=REGION)
    mock_client.list_targets_for_policy.assert_called_once()


def test_list_targets_for_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_targets_for_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_targets_for_policy",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list targets for policy"):
        list_targets_for_policy("test-policy_id", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-content", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-content", region_name=REGION)


def test_register_delegated_administrator(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_delegated_administrator.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    register_delegated_administrator("test-account_id", "test-service_principal", region_name=REGION)
    mock_client.register_delegated_administrator.assert_called_once()


def test_register_delegated_administrator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_delegated_administrator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_delegated_administrator",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register delegated administrator"):
        register_delegated_administrator("test-account_id", "test-service_principal", region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_id", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_id", [], region_name=REGION)


def test_update_organizational_unit(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_organizational_unit.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    update_organizational_unit("test-organizational_unit_id", region_name=REGION)
    mock_client.update_organizational_unit.assert_called_once()


def test_update_organizational_unit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_organizational_unit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_organizational_unit",
    )
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update organizational unit"):
        update_organizational_unit("test-organizational_unit_id", region_name=REGION)


def test_create_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import create_account
    mock_client = MagicMock()
    mock_client.create_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    create_account("test-email", 1, role_name="test-role_name", region_name="us-east-1")
    mock_client.create_account.assert_called_once()

def test_create_gov_cloud_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import create_gov_cloud_account
    mock_client = MagicMock()
    mock_client.create_gov_cloud_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    create_gov_cloud_account("test-email", 1, role_name="test-role_name", iam_user_access_to_billing="test-iam_user_access_to_billing", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_gov_cloud_account.assert_called_once()

def test_describe_effective_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import describe_effective_policy
    mock_client = MagicMock()
    mock_client.describe_effective_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    describe_effective_policy("test-policy_type", target_id="test-target_id", region_name="us-east-1")
    mock_client.describe_effective_policy.assert_called_once()

def test_list_accounts_with_invalid_effective_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_accounts_with_invalid_effective_policy
    mock_client = MagicMock()
    mock_client.list_accounts_with_invalid_effective_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_accounts_with_invalid_effective_policy("test-policy_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_accounts_with_invalid_effective_policy.assert_called_once()

def test_list_aws_service_access_for_organization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_aws_service_access_for_organization
    mock_client = MagicMock()
    mock_client.list_aws_service_access_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_aws_service_access_for_organization(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_aws_service_access_for_organization.assert_called_once()

def test_list_create_account_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_create_account_status
    mock_client = MagicMock()
    mock_client.list_create_account_status.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_create_account_status(states="test-states", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_create_account_status.assert_called_once()

def test_list_delegated_administrators_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_delegated_administrators
    mock_client = MagicMock()
    mock_client.list_delegated_administrators.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_delegated_administrators(service_principal="test-service_principal", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_delegated_administrators.assert_called_once()

def test_list_delegated_services_for_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_delegated_services_for_account
    mock_client = MagicMock()
    mock_client.list_delegated_services_for_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_delegated_services_for_account(1, next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_delegated_services_for_account.assert_called_once()

def test_list_effective_policy_validation_errors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_effective_policy_validation_errors
    mock_client = MagicMock()
    mock_client.list_effective_policy_validation_errors.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_effective_policy_validation_errors(1, "test-policy_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_effective_policy_validation_errors.assert_called_once()

def test_list_handshakes_for_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_handshakes_for_account
    mock_client = MagicMock()
    mock_client.list_handshakes_for_account.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_handshakes_for_account(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_handshakes_for_account.assert_called_once()

def test_list_handshakes_for_organization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_handshakes_for_organization
    mock_client = MagicMock()
    mock_client.list_handshakes_for_organization.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_handshakes_for_organization(filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_handshakes_for_organization.assert_called_once()

def test_list_policies_for_target_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_policies_for_target
    mock_client = MagicMock()
    mock_client.list_policies_for_target.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_policies_for_target("test-target_id", "test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_policies_for_target.assert_called_once()

def test_list_targets_for_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import list_targets_for_policy
    mock_client = MagicMock()
    mock_client.list_targets_for_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    list_targets_for_policy("test-policy_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_targets_for_policy.assert_called_once()

def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import put_resource_policy
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-content", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.put_resource_policy.assert_called_once()

def test_update_organizational_unit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.organizations import update_organizational_unit
    mock_client = MagicMock()
    mock_client.update_organizational_unit.return_value = {}
    monkeypatch.setattr("aws_util.organizations.get_client", lambda *a, **kw: mock_client)
    update_organizational_unit("test-organizational_unit_id", name="test-name", region_name="us-east-1")
    mock_client.update_organizational_unit.assert_called_once()
