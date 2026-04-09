

"""Tests for aws_util.aio.sso_admin -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.sso_admin as mod
from aws_util.aio.sso_admin import (

    create_instance,
    create_permission_set,
    update_permission_set,
    provision_permission_set,
    create_application,
    create_trusted_token_issuer,
    list_account_assignment_creation_status,
    list_account_assignment_deletion_status,
    list_account_assignments_for_principal,
    list_application_access_scopes,
    list_application_assignments,
    list_application_assignments_for_principal,
    list_application_authentication_methods,
    list_application_grants,
    list_application_providers,
    list_applications,
    list_customer_managed_policy_references_in_permission_set,
    list_permission_set_provisioning_status,
    list_permission_sets_provisioned_to_account,
    list_tags_for_resource,
    list_trusted_token_issuers,
    put_application_access_scope,
    put_application_session_configuration,
    tag_resource,
    untag_resource,
    update_application,
    update_instance,
    update_trusted_token_issuer,
    attach_customer_managed_policy_reference_to_permission_set,
    create_application_assignment,
    create_instance_access_control_attribute_configuration,
    delete_application,
    delete_application_access_scope,
    delete_application_assignment,
    delete_application_authentication_method,
    delete_application_grant,
    delete_instance_access_control_attribute_configuration,
    delete_permissions_boundary_from_permission_set,
    delete_trusted_token_issuer,
    describe_account_assignment_creation_status,
    describe_account_assignment_deletion_status,
    describe_application,
    describe_application_assignment,
    describe_application_provider,
    describe_instance_access_control_attribute_configuration,
    describe_permission_set_provisioning_status,
    describe_trusted_token_issuer,
    detach_customer_managed_policy_reference_from_permission_set,
    get_application_access_scope,
    get_application_assignment_configuration,
    get_application_authentication_method,
    get_application_grant,
    get_application_session_configuration,
    get_permissions_boundary_for_permission_set,
    put_application_assignment_configuration,
    put_application_authentication_method,
    put_application_grant,
    put_permissions_boundary_to_permission_set,
    update_instance_access_control_attribute_configuration,
)


REGION = "us-east-1"
_INST = {"InstanceArn": "arn:inst", "IdentityStoreId": "ds-1", "Name": "inst",
         "Status": "ACTIVE", "OwnerAccountId": "123", "CreatedDate": "2025-01-01"}
_PS = {"PermissionSetArn": "arn:ps", "Name": "ps1", "Description": "d",
       "SessionDuration": "PT1H", "RelayState": "", "CreatedDate": "2025-01-01"}
_MP = {"Name": "ReadOnly", "Arn": "arn:pol"}
_AA = {"AccountId": "123", "PermissionSetArn": "arn:ps",
       "PrincipalType": "USER", "PrincipalId": "uid"}
_AAS = {"Status": "SUCCEEDED", "RequestId": "r1", "FailureReason": "",
        "TargetId": "123", "TargetType": "AWS_ACCOUNT",
        "PermissionSetArn": "arn:ps", "PrincipalType": "USER",
        "PrincipalId": "uid", "CreatedDate": "2025-01-01"}
_PROV = {"Status": "SUCCEEDED", "RequestId": "r2", "AccountId": "123",
         "PermissionSetArn": "arn:ps", "FailureReason": "", "CreatedDate": "2025-01-01"}


@pytest.fixture()
def mc(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: client)
    return client


async def test_create_instance_success(mc):
    mc.call.return_value = _INST
    r = await mod.create_instance(name="inst")
    assert r.instance_arn == "arn:inst"

async def test_create_instance_no_name(mc):
    mc.call.return_value = _INST
    await mod.create_instance()
    mc.call.assert_called_once()

async def test_create_instance_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_instance failed"):
        await mod.create_instance()


async def test_list_instances_success(mc):
    mc.call.return_value = {"Instances": [_INST]}
    r = await mod.list_instances()
    assert len(r) == 1

async def test_list_instances_pagination(mc):
    mc.call.side_effect = [
        {"Instances": [_INST], "NextToken": "t"},
        {"Instances": [_INST]},
    ]
    r = await mod.list_instances()
    assert len(r) == 2

async def test_list_instances_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_instances failed"):
        await mod.list_instances()


async def test_describe_instance_success(mc):
    mc.call.return_value = _INST
    r = await mod.describe_instance("arn:inst")
    assert r.instance_arn == "arn:inst"

async def test_describe_instance_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_instance failed"):
        await mod.describe_instance("arn:inst")


async def test_delete_instance_success(mc):
    mc.call.return_value = {}
    await mod.delete_instance("arn:inst")
    mc.call.assert_called_once()

async def test_delete_instance_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_instance failed"):
        await mod.delete_instance("arn:inst")


async def test_create_permission_set_success(mc):
    mc.call.return_value = {"PermissionSet": _PS}
    r = await mod.create_permission_set("arn:inst", "ps1", description="d", relay_state="https://x")
    assert r.name == "ps1"

async def test_create_permission_set_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_permission_set failed"):
        await mod.create_permission_set("arn:inst", "ps1")


async def test_describe_permission_set_success(mc):
    mc.call.return_value = {"PermissionSet": _PS}
    r = await mod.describe_permission_set("arn:inst", "arn:ps")
    assert r.name == "ps1"

async def test_describe_permission_set_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="describe_permission_set failed"):
        await mod.describe_permission_set("arn:inst", "arn:ps")


async def test_list_permission_sets_success(mc):
    mc.call.return_value = {"PermissionSets": ["arn:ps"]}
    r = await mod.list_permission_sets("arn:inst")
    assert r == ["arn:ps"]

async def test_list_permission_sets_pagination(mc):
    mc.call.side_effect = [
        {"PermissionSets": ["arn:ps1"], "NextToken": "t"},
        {"PermissionSets": ["arn:ps2"]},
    ]
    r = await mod.list_permission_sets("arn:inst")
    assert len(r) == 2

async def test_list_permission_sets_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_permission_sets failed"):
        await mod.list_permission_sets("arn:inst")


async def test_update_permission_set_success(mc):
    mc.call.return_value = {}
    await mod.update_permission_set("arn:inst", "arn:ps", description="d",
                                    session_duration="PT2H", relay_state="https://x")
    mc.call.assert_called_once()

async def test_update_permission_set_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_permission_set failed"):
        await mod.update_permission_set("arn:inst", "arn:ps")


async def test_delete_permission_set_success(mc):
    mc.call.return_value = {}
    await mod.delete_permission_set("arn:inst", "arn:ps")
    mc.call.assert_called_once()

async def test_delete_permission_set_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_permission_set failed"):
        await mod.delete_permission_set("arn:inst", "arn:ps")


async def test_attach_managed_policy_success(mc):
    mc.call.return_value = {}
    await mod.attach_managed_policy_to_permission_set("arn:inst", "arn:ps", "arn:pol")
    mc.call.assert_called_once()

async def test_attach_managed_policy_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="attach_managed_policy_to_permission_set failed"):
        await mod.attach_managed_policy_to_permission_set("arn:inst", "arn:ps", "arn:pol")


async def test_detach_managed_policy_success(mc):
    mc.call.return_value = {}
    await mod.detach_managed_policy_from_permission_set("arn:inst", "arn:ps", "arn:pol")
    mc.call.assert_called_once()

async def test_detach_managed_policy_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="detach_managed_policy_from_permission_set failed"):
        await mod.detach_managed_policy_from_permission_set("arn:inst", "arn:ps", "arn:pol")


async def test_list_managed_policies_success(mc):
    mc.call.return_value = {"AttachedManagedPolicies": [_MP]}
    r = await mod.list_managed_policies_in_permission_set("arn:inst", "arn:ps")
    assert len(r) == 1

async def test_list_managed_policies_pagination(mc):
    mc.call.side_effect = [
        {"AttachedManagedPolicies": [_MP], "NextToken": "t"},
        {"AttachedManagedPolicies": [_MP]},
    ]
    r = await mod.list_managed_policies_in_permission_set("arn:inst", "arn:ps")
    assert len(r) == 2

async def test_list_managed_policies_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_managed_policies_in_permission_set failed"):
        await mod.list_managed_policies_in_permission_set("arn:inst", "arn:ps")


async def test_put_inline_policy_success(mc):
    mc.call.return_value = {}
    await mod.put_inline_policy_to_permission_set("arn:inst", "arn:ps", "{}")
    mc.call.assert_called_once()

async def test_put_inline_policy_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="put_inline_policy_to_permission_set failed"):
        await mod.put_inline_policy_to_permission_set("arn:inst", "arn:ps", "{}")


async def test_get_inline_policy_success(mc):
    mc.call.return_value = {"InlinePolicy": "{}"}
    r = await mod.get_inline_policy_for_permission_set("arn:inst", "arn:ps")
    assert r == "{}"

async def test_get_inline_policy_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_inline_policy_for_permission_set failed"):
        await mod.get_inline_policy_for_permission_set("arn:inst", "arn:ps")


async def test_delete_inline_policy_success(mc):
    mc.call.return_value = {}
    await mod.delete_inline_policy_from_permission_set("arn:inst", "arn:ps")
    mc.call.assert_called_once()

async def test_delete_inline_policy_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_inline_policy_from_permission_set failed"):
        await mod.delete_inline_policy_from_permission_set("arn:inst", "arn:ps")


async def test_create_account_assignment_success(mc):
    mc.call.return_value = {"AccountAssignmentCreationStatus": _AAS}
    r = await mod.create_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid")
    assert r.status == "SUCCEEDED"

async def test_create_account_assignment_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_account_assignment failed"):
        await mod.create_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid")


async def test_list_account_assignments_success(mc):
    mc.call.return_value = {"AccountAssignments": [_AA]}
    r = await mod.list_account_assignments("arn:inst", "123", "arn:ps")
    assert len(r) == 1

async def test_list_account_assignments_pagination(mc):
    mc.call.side_effect = [
        {"AccountAssignments": [_AA], "NextToken": "t"},
        {"AccountAssignments": [_AA]},
    ]
    r = await mod.list_account_assignments("arn:inst", "123", "arn:ps")
    assert len(r) == 2

async def test_list_account_assignments_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_account_assignments failed"):
        await mod.list_account_assignments("arn:inst", "123", "arn:ps")


async def test_delete_account_assignment_success(mc):
    mc.call.return_value = {"AccountAssignmentDeletionStatus": _AAS}
    r = await mod.delete_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid")
    assert r.status == "SUCCEEDED"

async def test_delete_account_assignment_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_account_assignment failed"):
        await mod.delete_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid")


async def test_list_accounts_for_provisioned_ps_success(mc):
    mc.call.return_value = {"AccountIds": ["123"]}
    r = await mod.list_accounts_for_provisioned_permission_set("arn:inst", "arn:ps")
    assert r == ["123"]

async def test_list_accounts_for_provisioned_ps_pagination(mc):
    mc.call.side_effect = [
        {"AccountIds": ["123"], "NextToken": "t"},
        {"AccountIds": ["456"]},
    ]
    r = await mod.list_accounts_for_provisioned_permission_set("arn:inst", "arn:ps")
    assert r == ["123", "456"]

async def test_list_accounts_for_provisioned_ps_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_accounts_for_provisioned_permission_set failed"):
        await mod.list_accounts_for_provisioned_permission_set("arn:inst", "arn:ps")


async def test_provision_permission_set_success(mc):
    mc.call.return_value = {"PermissionSetProvisioningStatus": _PROV}
    r = await mod.provision_permission_set("arn:inst", "arn:ps", target_id="123")
    assert r.status == "SUCCEEDED"

async def test_provision_permission_set_error(mc):
    mc.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="provision_permission_set failed"):
        await mod.provision_permission_set("arn:inst", "arn:ps")


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_attach_customer_managed_policy_reference_to_permission_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_customer_managed_policy_reference_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, )
    mock_client.call.assert_called_once()


async def test_attach_customer_managed_policy_reference_to_permission_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_customer_managed_policy_reference_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, )


async def test_create_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_application("test-instance_arn", "test-application_provider_arn", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_application("test-instance_arn", "test-application_provider_arn", "test-name", )


async def test_create_application_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", )
    mock_client.call.assert_called_once()


async def test_create_application_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", )


async def test_create_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instance_access_control_attribute_configuration("test-instance_arn", {}, )
    mock_client.call.assert_called_once()


async def test_create_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instance_access_control_attribute_configuration("test-instance_arn", {}, )


async def test_create_trusted_token_issuer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_trusted_token_issuer("test-instance_arn", "test-name", "test-trusted_token_issuer_type", {}, )
    mock_client.call.assert_called_once()


async def test_create_trusted_token_issuer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_trusted_token_issuer("test-instance_arn", "test-name", "test-trusted_token_issuer_type", {}, )


async def test_delete_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_delete_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application("test-application_arn", )


async def test_delete_application_access_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_access_scope("test-application_arn", "test-scope", )
    mock_client.call.assert_called_once()


async def test_delete_application_access_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_access_scope("test-application_arn", "test-scope", )


async def test_delete_application_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", )
    mock_client.call.assert_called_once()


async def test_delete_application_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", )


async def test_delete_application_authentication_method(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_authentication_method("test-application_arn", "test-authentication_method_type", )
    mock_client.call.assert_called_once()


async def test_delete_application_authentication_method_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_authentication_method("test-application_arn", "test-authentication_method_type", )


async def test_delete_application_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_application_grant("test-application_arn", "test-grant_type", )
    mock_client.call.assert_called_once()


async def test_delete_application_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_application_grant("test-application_arn", "test-grant_type", )


async def test_delete_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_instance_access_control_attribute_configuration("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_delete_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_instance_access_control_attribute_configuration("test-instance_arn", )


async def test_delete_permissions_boundary_from_permission_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_permissions_boundary_from_permission_set("test-instance_arn", "test-permission_set_arn", )
    mock_client.call.assert_called_once()


async def test_delete_permissions_boundary_from_permission_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_permissions_boundary_from_permission_set("test-instance_arn", "test-permission_set_arn", )


async def test_delete_trusted_token_issuer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_trusted_token_issuer("test-trusted_token_issuer_arn", )
    mock_client.call.assert_called_once()


async def test_delete_trusted_token_issuer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_trusted_token_issuer("test-trusted_token_issuer_arn", )


async def test_describe_account_assignment_creation_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_assignment_creation_status("test-instance_arn", "test-account_assignment_creation_request_id", )
    mock_client.call.assert_called_once()


async def test_describe_account_assignment_creation_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_assignment_creation_status("test-instance_arn", "test-account_assignment_creation_request_id", )


async def test_describe_account_assignment_deletion_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_assignment_deletion_status("test-instance_arn", "test-account_assignment_deletion_request_id", )
    mock_client.call.assert_called_once()


async def test_describe_account_assignment_deletion_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_assignment_deletion_status("test-instance_arn", "test-account_assignment_deletion_request_id", )


async def test_describe_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_describe_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application("test-application_arn", )


async def test_describe_application_assignment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", )
    mock_client.call.assert_called_once()


async def test_describe_application_assignment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", )


async def test_describe_application_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_application_provider("test-application_provider_arn", )
    mock_client.call.assert_called_once()


async def test_describe_application_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_application_provider("test-application_provider_arn", )


async def test_describe_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_instance_access_control_attribute_configuration("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_describe_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_instance_access_control_attribute_configuration("test-instance_arn", )


async def test_describe_permission_set_provisioning_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_permission_set_provisioning_status("test-instance_arn", "test-provision_permission_set_request_id", )
    mock_client.call.assert_called_once()


async def test_describe_permission_set_provisioning_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_permission_set_provisioning_status("test-instance_arn", "test-provision_permission_set_request_id", )


async def test_describe_trusted_token_issuer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_trusted_token_issuer("test-trusted_token_issuer_arn", )
    mock_client.call.assert_called_once()


async def test_describe_trusted_token_issuer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_trusted_token_issuer("test-trusted_token_issuer_arn", )


async def test_detach_customer_managed_policy_reference_from_permission_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_customer_managed_policy_reference_from_permission_set("test-instance_arn", "test-permission_set_arn", {}, )
    mock_client.call.assert_called_once()


async def test_detach_customer_managed_policy_reference_from_permission_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_customer_managed_policy_reference_from_permission_set("test-instance_arn", "test-permission_set_arn", {}, )


async def test_get_application_access_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_application_access_scope("test-application_arn", "test-scope", )
    mock_client.call.assert_called_once()


async def test_get_application_access_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_application_access_scope("test-application_arn", "test-scope", )


async def test_get_application_assignment_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_application_assignment_configuration("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_get_application_assignment_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_application_assignment_configuration("test-application_arn", )


async def test_get_application_authentication_method(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_application_authentication_method("test-application_arn", "test-authentication_method_type", )
    mock_client.call.assert_called_once()


async def test_get_application_authentication_method_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_application_authentication_method("test-application_arn", "test-authentication_method_type", )


async def test_get_application_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_application_grant("test-application_arn", "test-grant_type", )
    mock_client.call.assert_called_once()


async def test_get_application_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_application_grant("test-application_arn", "test-grant_type", )


async def test_get_application_session_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_application_session_configuration("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_get_application_session_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_application_session_configuration("test-application_arn", )


async def test_get_permissions_boundary_for_permission_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_permissions_boundary_for_permission_set("test-instance_arn", "test-permission_set_arn", )
    mock_client.call.assert_called_once()


async def test_get_permissions_boundary_for_permission_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_permissions_boundary_for_permission_set("test-instance_arn", "test-permission_set_arn", )


async def test_list_account_assignment_creation_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_account_assignment_creation_status("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_list_account_assignment_creation_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_account_assignment_creation_status("test-instance_arn", )


async def test_list_account_assignment_deletion_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_account_assignment_deletion_status("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_list_account_assignment_deletion_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_account_assignment_deletion_status("test-instance_arn", )


async def test_list_account_assignments_for_principal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_account_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", )
    mock_client.call.assert_called_once()


async def test_list_account_assignments_for_principal_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_account_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", )


async def test_list_application_access_scopes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_access_scopes("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_list_application_access_scopes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_access_scopes("test-application_arn", )


async def test_list_application_assignments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_assignments("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_list_application_assignments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_assignments("test-application_arn", )


async def test_list_application_assignments_for_principal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", )
    mock_client.call.assert_called_once()


async def test_list_application_assignments_for_principal_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", )


async def test_list_application_authentication_methods(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_authentication_methods("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_list_application_authentication_methods_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_authentication_methods("test-application_arn", )


async def test_list_application_grants(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_grants("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_list_application_grants_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_grants("test-application_arn", )


async def test_list_application_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_application_providers()
    mock_client.call.assert_called_once()


async def test_list_application_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_providers()


async def test_list_applications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_applications("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_list_applications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_applications("test-instance_arn", )


async def test_list_customer_managed_policy_references_in_permission_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_customer_managed_policy_references_in_permission_set("test-instance_arn", "test-permission_set_arn", )
    mock_client.call.assert_called_once()


async def test_list_customer_managed_policy_references_in_permission_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_customer_managed_policy_references_in_permission_set("test-instance_arn", "test-permission_set_arn", )


async def test_list_permission_set_provisioning_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_permission_set_provisioning_status("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_list_permission_set_provisioning_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_permission_set_provisioning_status("test-instance_arn", )


async def test_list_permission_sets_provisioned_to_account(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_permission_sets_provisioned_to_account("test-instance_arn", "test-account_id", )
    mock_client.call.assert_called_once()


async def test_list_permission_sets_provisioned_to_account_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_permission_sets_provisioned_to_account("test-instance_arn", "test-account_id", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_trusted_token_issuers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_trusted_token_issuers("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_list_trusted_token_issuers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_trusted_token_issuers("test-instance_arn", )


async def test_put_application_access_scope(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_application_access_scope("test-scope", "test-application_arn", )
    mock_client.call.assert_called_once()


async def test_put_application_access_scope_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_application_access_scope("test-scope", "test-application_arn", )


async def test_put_application_assignment_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_application_assignment_configuration("test-application_arn", True, )
    mock_client.call.assert_called_once()


async def test_put_application_assignment_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_application_assignment_configuration("test-application_arn", True, )


async def test_put_application_authentication_method(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_application_authentication_method("test-application_arn", "test-authentication_method_type", {}, )
    mock_client.call.assert_called_once()


async def test_put_application_authentication_method_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_application_authentication_method("test-application_arn", "test-authentication_method_type", {}, )


async def test_put_application_grant(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_application_grant("test-application_arn", "test-grant_type", {}, )
    mock_client.call.assert_called_once()


async def test_put_application_grant_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_application_grant("test-application_arn", "test-grant_type", {}, )


async def test_put_application_session_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_application_session_configuration("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_put_application_session_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_application_session_configuration("test-application_arn", )


async def test_put_permissions_boundary_to_permission_set(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_permissions_boundary_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, )
    mock_client.call.assert_called_once()


async def test_put_permissions_boundary_to_permission_set_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_permissions_boundary_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_application(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_application("test-application_arn", )
    mock_client.call.assert_called_once()


async def test_update_application_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_application("test-application_arn", )


async def test_update_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_instance("test-instance_arn", )
    mock_client.call.assert_called_once()


async def test_update_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_instance("test-instance_arn", )


async def test_update_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_instance_access_control_attribute_configuration("test-instance_arn", {}, )
    mock_client.call.assert_called_once()


async def test_update_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_instance_access_control_attribute_configuration("test-instance_arn", {}, )


async def test_update_trusted_token_issuer(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_trusted_token_issuer("test-trusted_token_issuer_arn", )
    mock_client.call.assert_called_once()


async def test_update_trusted_token_issuer_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.sso_admin.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_trusted_token_issuer("test-trusted_token_issuer_arn", )


@pytest.mark.asyncio
async def test_create_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import create_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await create_instance(name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_permission_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import update_permission_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await update_permission_set("test-instance_arn", "test-permission_set_arn", description="test-description", session_duration=1, relay_state="test-relay_state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_provision_permission_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import provision_permission_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await provision_permission_set("test-instance_arn", "test-permission_set_arn", target_id="test-target_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import create_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await create_application("test-instance_arn", "test-application_provider_arn", "test-name", description="test-description", portal_options=1, tags=[{"Key": "k", "Value": "v"}], status="test-status", client_token="test-client_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_trusted_token_issuer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import create_trusted_token_issuer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await create_trusted_token_issuer("test-instance_arn", "test-name", "test-trusted_token_issuer_type", {}, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_account_assignment_creation_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_account_assignment_creation_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_account_assignment_creation_status("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_account_assignment_deletion_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_account_assignment_deletion_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_account_assignment_deletion_status("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_account_assignments_for_principal_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_account_assignments_for_principal
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_account_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_access_scopes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_application_access_scopes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_application_access_scopes("test-application_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_assignments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_application_assignments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_application_assignments("test-application_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_assignments_for_principal_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_application_assignments_for_principal
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_application_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_authentication_methods_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_application_authentication_methods
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_application_authentication_methods("test-application_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_grants_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_application_grants
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_application_grants("test-application_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_providers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_application_providers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_application_providers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_applications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_applications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_applications("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_customer_managed_policy_references_in_permission_set_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_customer_managed_policy_references_in_permission_set
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_customer_managed_policy_references_in_permission_set("test-instance_arn", "test-permission_set_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_permission_set_provisioning_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_permission_set_provisioning_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_permission_set_provisioning_status("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_permission_sets_provisioned_to_account_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_permission_sets_provisioned_to_account
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_permission_sets_provisioned_to_account("test-instance_arn", 1, provisioning_status="test-provisioning_status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", instance_arn="test-instance_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_trusted_token_issuers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import list_trusted_token_issuers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await list_trusted_token_issuers("test-instance_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_application_access_scope_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import put_application_access_scope
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await put_application_access_scope("test-scope", "test-application_arn", authorized_targets="test-authorized_targets", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_application_session_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import put_application_session_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await put_application_session_configuration("test-application_arn", user_background_session_application_status="test-user_background_session_application_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_tag_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import tag_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await tag_resource("test-resource_arn", [{"Key": "k", "Value": "v"}], instance_arn="test-instance_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_untag_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import untag_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await untag_resource("test-resource_arn", "test-tag_keys", instance_arn="test-instance_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_application_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import update_application
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await update_application("test-application_arn", name="test-name", description="test-description", status="test-status", portal_options=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import update_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await update_instance("test-instance_arn", name="test-name", encryption_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_trusted_token_issuer_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.sso_admin import update_trusted_token_issuer
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.sso_admin.async_client", lambda *a, **kw: mock_client)
    await update_trusted_token_issuer("test-trusted_token_issuer_arn", name="test-name", trusted_token_issuer_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()
