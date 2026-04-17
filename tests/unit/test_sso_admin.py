"""Tests for aws_util.sso_admin module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.sso_admin as mod
from aws_util.sso_admin import (
    AccountAssignmentResult, AccountAssignmentStatusResult,
    InstanceResult, ManagedPolicyResult, PermissionSetResult,
    ProvisionStatusResult,
    _parse_account_assignment, _parse_assignment_status,
    _parse_instance, _parse_managed_policy,
    _parse_permission_set, _parse_provision_status,
    attach_managed_policy_to_permission_set,
    create_account_assignment, create_instance, create_permission_set,
    delete_account_assignment, delete_inline_policy_from_permission_set,
    delete_instance, delete_permission_set,
    describe_instance, describe_permission_set,
    detach_managed_policy_from_permission_set,
    get_inline_policy_for_permission_set,
    list_account_assignments,
    list_accounts_for_provisioned_permission_set,
    list_instances, list_managed_policies_in_permission_set,
    list_permission_sets,
    provision_permission_set,
    put_inline_policy_to_permission_set,
    update_permission_set,
    attach_customer_managed_policy_reference_to_permission_set,
    create_application,
    create_application_assignment,
    create_instance_access_control_attribute_configuration,
    create_trusted_token_issuer,
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
    put_application_assignment_configuration,
    put_application_authentication_method,
    put_application_grant,
    put_application_session_configuration,
    put_permissions_boundary_to_permission_set,
    tag_resource,
    untag_resource,
    update_application,
    update_instance,
    update_instance_access_control_attribute_configuration,
    update_trusted_token_issuer,
)

REGION = "us-east-1"
_INST = {"InstanceArn": "arn:inst", "IdentityStoreId": "ds-1", "Name": "inst",
         "Status": "ACTIVE", "OwnerAccountId": "123", "CreatedDate": "2025-01-01",
         "extraI": "x"}
_PS = {"PermissionSetArn": "arn:ps", "Name": "ps1", "Description": "d",
       "SessionDuration": "PT1H", "RelayState": "", "CreatedDate": "2025-01-01",
       "extraP": "y"}
_MP = {"Name": "AmazonS3ReadOnly", "Arn": "arn:aws:iam::aws:policy/AmazonS3ReadOnly",
       "extraM": "z"}
_AA = {"AccountId": "123", "PermissionSetArn": "arn:ps",
       "PrincipalType": "USER", "PrincipalId": "uid",
       "extraA": "a"}
_AAS = {"Status": "SUCCEEDED", "RequestId": "req-1", "FailureReason": "",
        "TargetId": "123", "TargetType": "AWS_ACCOUNT",
        "PermissionSetArn": "arn:ps", "PrincipalType": "USER",
        "PrincipalId": "uid", "CreatedDate": "2025-01-01",
        "extraS": "s"}
_PROV = {"Status": "SUCCEEDED", "RequestId": "req-2", "AccountId": "123",
         "PermissionSetArn": "arn:ps", "FailureReason": "",
         "CreatedDate": "2025-01-01", "extraPr": "p"}


def _ce(code="ServiceException", msg="fail"):
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# Models
def test_instance_result():
    r = InstanceResult(instance_arn="arn:i")
    assert r.instance_arn == "arn:i"

def test_permission_set_result():
    r = PermissionSetResult(permission_set_arn="arn:p")
    assert r.permission_set_arn == "arn:p"

def test_managed_policy_result():
    r = ManagedPolicyResult(name="p", arn="arn:p")
    assert r.name == "p"

def test_account_assignment_result():
    r = AccountAssignmentResult(account_id="1")
    assert r.account_id == "1"

def test_account_assignment_status_result():
    r = AccountAssignmentStatusResult(status="OK")
    assert r.status == "OK"

def test_provision_status_result():
    r = ProvisionStatusResult(status="OK")
    assert r.status == "OK"


# Parsers
def test_parse_instance():
    r = _parse_instance(_INST)
    assert r.instance_arn == "arn:inst"
    assert "extraI" in r.extra

def test_parse_permission_set():
    r = _parse_permission_set(_PS)
    assert r.name == "ps1"
    assert "extraP" in r.extra

def test_parse_managed_policy():
    r = _parse_managed_policy(_MP)
    assert r.name == "AmazonS3ReadOnly"
    assert "extraM" in r.extra

def test_parse_account_assignment():
    r = _parse_account_assignment(_AA)
    assert r.account_id == "123"
    assert "extraA" in r.extra

def test_parse_assignment_status():
    r = _parse_assignment_status(_AAS)
    assert r.status == "SUCCEEDED"
    assert "extraS" in r.extra

def test_parse_provision_status():
    r = _parse_provision_status(_PROV)
    assert r.status == "SUCCEEDED"
    assert "extraPr" in r.extra


# create_instance
def test_create_instance_success(monkeypatch):
    client = MagicMock()
    client.create_instance.return_value = _INST
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_instance(region_name=REGION)
    assert r.instance_arn == "arn:inst"

def test_create_instance_with_name(monkeypatch):
    client = MagicMock()
    client.create_instance.return_value = _INST
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    create_instance(name="my-inst", region_name=REGION)
    kw = client.create_instance.call_args[1]
    assert kw["Name"] == "my-inst"

def test_create_instance_error(monkeypatch):
    client = MagicMock()
    client.create_instance.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_instance failed"):
        create_instance(region_name=REGION)


# list_instances
def test_list_instances_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"Instances": [_INST]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_instances(region_name=REGION)
    assert len(r) == 1

def test_list_instances_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_instances failed"):
        list_instances(region_name=REGION)


# describe_instance
def test_describe_instance_success(monkeypatch):
    client = MagicMock()
    client.describe_instance.return_value = _INST
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = describe_instance("arn:inst", region_name=REGION)
    assert r.instance_arn == "arn:inst"

def test_describe_instance_error(monkeypatch):
    client = MagicMock()
    client.describe_instance.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="describe_instance failed"):
        describe_instance("arn:inst", region_name=REGION)


# delete_instance
def test_delete_instance_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_instance("arn:inst", region_name=REGION)
    client.delete_instance.assert_called_once()

def test_delete_instance_error(monkeypatch):
    client = MagicMock()
    client.delete_instance.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_instance failed"):
        delete_instance("arn:inst", region_name=REGION)


# create_permission_set
def test_create_permission_set_success(monkeypatch):
    client = MagicMock()
    client.create_permission_set.return_value = {"PermissionSet": _PS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_permission_set("arn:inst", "ps1", description="d", relay_state="https://x", region_name=REGION)
    assert r.name == "ps1"

def test_create_permission_set_error(monkeypatch):
    client = MagicMock()
    client.create_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_permission_set failed"):
        create_permission_set("arn:inst", "ps1", region_name=REGION)


# describe_permission_set
def test_describe_permission_set_success(monkeypatch):
    client = MagicMock()
    client.describe_permission_set.return_value = {"PermissionSet": _PS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = describe_permission_set("arn:inst", "arn:ps", region_name=REGION)
    assert r.name == "ps1"

def test_describe_permission_set_error(monkeypatch):
    client = MagicMock()
    client.describe_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="describe_permission_set failed"):
        describe_permission_set("arn:inst", "arn:ps", region_name=REGION)


# list_permission_sets
def test_list_permission_sets_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"PermissionSets": ["arn:ps"]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_permission_sets("arn:inst", region_name=REGION)
    assert r == ["arn:ps"]

def test_list_permission_sets_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_permission_sets failed"):
        list_permission_sets("arn:inst", region_name=REGION)


# update_permission_set
def test_update_permission_set_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    update_permission_set("arn:inst", "arn:ps", description="new", session_duration="PT2H",
                          relay_state="https://y", region_name=REGION)
    client.update_permission_set.assert_called_once()

def test_update_permission_set_error(monkeypatch):
    client = MagicMock()
    client.update_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_permission_set failed"):
        update_permission_set("arn:inst", "arn:ps", region_name=REGION)


# delete_permission_set
def test_delete_permission_set_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_permission_set("arn:inst", "arn:ps", region_name=REGION)
    client.delete_permission_set.assert_called_once()

def test_delete_permission_set_error(monkeypatch):
    client = MagicMock()
    client.delete_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_permission_set failed"):
        delete_permission_set("arn:inst", "arn:ps", region_name=REGION)


# managed policy ops
def test_attach_managed_policy_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    attach_managed_policy_to_permission_set("arn:inst", "arn:ps", "arn:pol", region_name=REGION)
    client.attach_managed_policy_to_permission_set.assert_called_once()

def test_attach_managed_policy_error(monkeypatch):
    client = MagicMock()
    client.attach_managed_policy_to_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="attach_managed_policy_to_permission_set failed"):
        attach_managed_policy_to_permission_set("arn:inst", "arn:ps", "arn:pol", region_name=REGION)

def test_detach_managed_policy_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    detach_managed_policy_from_permission_set("arn:inst", "arn:ps", "arn:pol", region_name=REGION)
    client.detach_managed_policy_from_permission_set.assert_called_once()

def test_detach_managed_policy_error(monkeypatch):
    client = MagicMock()
    client.detach_managed_policy_from_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="detach_managed_policy_from_permission_set failed"):
        detach_managed_policy_from_permission_set("arn:inst", "arn:ps", "arn:pol", region_name=REGION)

def test_list_managed_policies_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"AttachedManagedPolicies": [_MP]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_managed_policies_in_permission_set("arn:inst", "arn:ps", region_name=REGION)
    assert len(r) == 1

def test_list_managed_policies_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_managed_policies_in_permission_set failed"):
        list_managed_policies_in_permission_set("arn:inst", "arn:ps", region_name=REGION)


# inline policy ops
def test_put_inline_policy_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    put_inline_policy_to_permission_set("arn:inst", "arn:ps", '{"Version":"2012-10-17"}', region_name=REGION)
    client.put_inline_policy_to_permission_set.assert_called_once()

def test_put_inline_policy_error(monkeypatch):
    client = MagicMock()
    client.put_inline_policy_to_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="put_inline_policy_to_permission_set failed"):
        put_inline_policy_to_permission_set("arn:inst", "arn:ps", "{}", region_name=REGION)

def test_get_inline_policy_success(monkeypatch):
    client = MagicMock()
    client.get_inline_policy_for_permission_set.return_value = {"InlinePolicy": "{}"}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_inline_policy_for_permission_set("arn:inst", "arn:ps", region_name=REGION)
    assert r == "{}"

def test_get_inline_policy_error(monkeypatch):
    client = MagicMock()
    client.get_inline_policy_for_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_inline_policy_for_permission_set failed"):
        get_inline_policy_for_permission_set("arn:inst", "arn:ps", region_name=REGION)

def test_delete_inline_policy_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_inline_policy_from_permission_set("arn:inst", "arn:ps", region_name=REGION)
    client.delete_inline_policy_from_permission_set.assert_called_once()

def test_delete_inline_policy_error(monkeypatch):
    client = MagicMock()
    client.delete_inline_policy_from_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_inline_policy_from_permission_set failed"):
        delete_inline_policy_from_permission_set("arn:inst", "arn:ps", region_name=REGION)


# account assignment ops
def test_create_account_assignment_success(monkeypatch):
    client = MagicMock()
    client.create_account_assignment.return_value = {"AccountAssignmentCreationStatus": _AAS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid", region_name=REGION)
    assert r.status == "SUCCEEDED"

def test_create_account_assignment_error(monkeypatch):
    client = MagicMock()
    client.create_account_assignment.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_account_assignment failed"):
        create_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid", region_name=REGION)

def test_list_account_assignments_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"AccountAssignments": [_AA]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_account_assignments("arn:inst", "123", "arn:ps", region_name=REGION)
    assert len(r) == 1

def test_list_account_assignments_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_account_assignments failed"):
        list_account_assignments("arn:inst", "123", "arn:ps", region_name=REGION)

def test_delete_account_assignment_success(monkeypatch):
    client = MagicMock()
    client.delete_account_assignment.return_value = {"AccountAssignmentDeletionStatus": _AAS}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = delete_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid", region_name=REGION)
    assert r.status == "SUCCEEDED"

def test_delete_account_assignment_error(monkeypatch):
    client = MagicMock()
    client.delete_account_assignment.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_account_assignment failed"):
        delete_account_assignment("arn:inst", "123", "AWS_ACCOUNT", "arn:ps", "USER", "uid", region_name=REGION)

def test_list_accounts_for_provisioned_ps_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"AccountIds": ["123"]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_accounts_for_provisioned_permission_set("arn:inst", "arn:ps", region_name=REGION)
    assert r == ["123"]

def test_list_accounts_for_provisioned_ps_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_accounts_for_provisioned_permission_set"):
        list_accounts_for_provisioned_permission_set("arn:inst", "arn:ps", region_name=REGION)

def test_provision_permission_set_success(monkeypatch):
    client = MagicMock()
    client.provision_permission_set.return_value = {"PermissionSetProvisioningStatus": _PROV}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = provision_permission_set("arn:inst", "arn:ps", target_id="123", region_name=REGION)
    assert r.status == "SUCCEEDED"

def test_provision_permission_set_error(monkeypatch):
    client = MagicMock()
    client.provision_permission_set.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="provision_permission_set failed"):
        provision_permission_set("arn:inst", "arn:ps", region_name=REGION)


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


def test_attach_customer_managed_policy_reference_to_permission_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_customer_managed_policy_reference_to_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    attach_customer_managed_policy_reference_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, region_name=REGION)
    mock_client.attach_customer_managed_policy_reference_to_permission_set.assert_called_once()


def test_attach_customer_managed_policy_reference_to_permission_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_customer_managed_policy_reference_to_permission_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_customer_managed_policy_reference_to_permission_set",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach customer managed policy reference to permission set"):
        attach_customer_managed_policy_reference_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, region_name=REGION)


def test_create_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_application("test-instance_arn", "test-application_provider_arn", "test-name", region_name=REGION)
    mock_client.create_application.assert_called_once()


def test_create_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_application",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create application"):
        create_application("test-instance_arn", "test-application_provider_arn", "test-name", region_name=REGION)


def test_create_application_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application_assignment.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", region_name=REGION)
    mock_client.create_application_assignment.assert_called_once()


def test_create_application_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_application_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_application_assignment",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create application assignment"):
        create_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", region_name=REGION)


def test_create_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_access_control_attribute_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_instance_access_control_attribute_configuration("test-instance_arn", {}, region_name=REGION)
    mock_client.create_instance_access_control_attribute_configuration.assert_called_once()


def test_create_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_access_control_attribute_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instance_access_control_attribute_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create instance access control attribute configuration"):
        create_instance_access_control_attribute_configuration("test-instance_arn", {}, region_name=REGION)


def test_create_trusted_token_issuer(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_trusted_token_issuer.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_trusted_token_issuer("test-instance_arn", "test-name", "test-trusted_token_issuer_type", {}, region_name=REGION)
    mock_client.create_trusted_token_issuer.assert_called_once()


def test_create_trusted_token_issuer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_trusted_token_issuer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_trusted_token_issuer",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create trusted token issuer"):
        create_trusted_token_issuer("test-instance_arn", "test-name", "test-trusted_token_issuer_type", {}, region_name=REGION)


def test_delete_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_application("test-application_arn", region_name=REGION)
    mock_client.delete_application.assert_called_once()


def test_delete_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application"):
        delete_application("test-application_arn", region_name=REGION)


def test_delete_application_access_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_application_access_scope("test-application_arn", "test-scope", region_name=REGION)
    mock_client.delete_application_access_scope.assert_called_once()


def test_delete_application_access_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_access_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_access_scope",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application access scope"):
        delete_application_access_scope("test-application_arn", "test-scope", region_name=REGION)


def test_delete_application_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_assignment.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", region_name=REGION)
    mock_client.delete_application_assignment.assert_called_once()


def test_delete_application_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_assignment",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application assignment"):
        delete_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", region_name=REGION)


def test_delete_application_authentication_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_authentication_method.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_application_authentication_method("test-application_arn", "test-authentication_method_type", region_name=REGION)
    mock_client.delete_application_authentication_method.assert_called_once()


def test_delete_application_authentication_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_authentication_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_authentication_method",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application authentication method"):
        delete_application_authentication_method("test-application_arn", "test-authentication_method_type", region_name=REGION)


def test_delete_application_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_grant.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_application_grant("test-application_arn", "test-grant_type", region_name=REGION)
    mock_client.delete_application_grant.assert_called_once()


def test_delete_application_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_application_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_application_grant",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete application grant"):
        delete_application_grant("test-application_arn", "test-grant_type", region_name=REGION)


def test_delete_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_access_control_attribute_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_instance_access_control_attribute_configuration("test-instance_arn", region_name=REGION)
    mock_client.delete_instance_access_control_attribute_configuration.assert_called_once()


def test_delete_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_access_control_attribute_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_instance_access_control_attribute_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete instance access control attribute configuration"):
        delete_instance_access_control_attribute_configuration("test-instance_arn", region_name=REGION)


def test_delete_permissions_boundary_from_permission_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_permissions_boundary_from_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_permissions_boundary_from_permission_set("test-instance_arn", "test-permission_set_arn", region_name=REGION)
    mock_client.delete_permissions_boundary_from_permission_set.assert_called_once()


def test_delete_permissions_boundary_from_permission_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_permissions_boundary_from_permission_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_permissions_boundary_from_permission_set",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete permissions boundary from permission set"):
        delete_permissions_boundary_from_permission_set("test-instance_arn", "test-permission_set_arn", region_name=REGION)


def test_delete_trusted_token_issuer(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_trusted_token_issuer.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    delete_trusted_token_issuer("test-trusted_token_issuer_arn", region_name=REGION)
    mock_client.delete_trusted_token_issuer.assert_called_once()


def test_delete_trusted_token_issuer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_trusted_token_issuer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_trusted_token_issuer",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete trusted token issuer"):
        delete_trusted_token_issuer("test-trusted_token_issuer_arn", region_name=REGION)


def test_describe_account_assignment_creation_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_assignment_creation_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_account_assignment_creation_status("test-instance_arn", "test-account_assignment_creation_request_id", region_name=REGION)
    mock_client.describe_account_assignment_creation_status.assert_called_once()


def test_describe_account_assignment_creation_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_assignment_creation_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_assignment_creation_status",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account assignment creation status"):
        describe_account_assignment_creation_status("test-instance_arn", "test-account_assignment_creation_request_id", region_name=REGION)


def test_describe_account_assignment_deletion_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_assignment_deletion_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_account_assignment_deletion_status("test-instance_arn", "test-account_assignment_deletion_request_id", region_name=REGION)
    mock_client.describe_account_assignment_deletion_status.assert_called_once()


def test_describe_account_assignment_deletion_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_assignment_deletion_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_assignment_deletion_status",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account assignment deletion status"):
        describe_account_assignment_deletion_status("test-instance_arn", "test-account_assignment_deletion_request_id", region_name=REGION)


def test_describe_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_application("test-application_arn", region_name=REGION)
    mock_client.describe_application.assert_called_once()


def test_describe_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_application",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe application"):
        describe_application("test-application_arn", region_name=REGION)


def test_describe_application_assignment(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_assignment.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", region_name=REGION)
    mock_client.describe_application_assignment.assert_called_once()


def test_describe_application_assignment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_assignment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_application_assignment",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe application assignment"):
        describe_application_assignment("test-application_arn", "test-principal_id", "test-principal_type", region_name=REGION)


def test_describe_application_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_provider.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_application_provider("test-application_provider_arn", region_name=REGION)
    mock_client.describe_application_provider.assert_called_once()


def test_describe_application_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_application_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_application_provider",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe application provider"):
        describe_application_provider("test-application_provider_arn", region_name=REGION)


def test_describe_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_access_control_attribute_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_instance_access_control_attribute_configuration("test-instance_arn", region_name=REGION)
    mock_client.describe_instance_access_control_attribute_configuration.assert_called_once()


def test_describe_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_instance_access_control_attribute_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_instance_access_control_attribute_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe instance access control attribute configuration"):
        describe_instance_access_control_attribute_configuration("test-instance_arn", region_name=REGION)


def test_describe_permission_set_provisioning_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_permission_set_provisioning_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_permission_set_provisioning_status("test-instance_arn", "test-provision_permission_set_request_id", region_name=REGION)
    mock_client.describe_permission_set_provisioning_status.assert_called_once()


def test_describe_permission_set_provisioning_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_permission_set_provisioning_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_permission_set_provisioning_status",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe permission set provisioning status"):
        describe_permission_set_provisioning_status("test-instance_arn", "test-provision_permission_set_request_id", region_name=REGION)


def test_describe_trusted_token_issuer(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trusted_token_issuer.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    describe_trusted_token_issuer("test-trusted_token_issuer_arn", region_name=REGION)
    mock_client.describe_trusted_token_issuer.assert_called_once()


def test_describe_trusted_token_issuer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_trusted_token_issuer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_trusted_token_issuer",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe trusted token issuer"):
        describe_trusted_token_issuer("test-trusted_token_issuer_arn", region_name=REGION)


def test_detach_customer_managed_policy_reference_from_permission_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_customer_managed_policy_reference_from_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    detach_customer_managed_policy_reference_from_permission_set("test-instance_arn", "test-permission_set_arn", {}, region_name=REGION)
    mock_client.detach_customer_managed_policy_reference_from_permission_set.assert_called_once()


def test_detach_customer_managed_policy_reference_from_permission_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_customer_managed_policy_reference_from_permission_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_customer_managed_policy_reference_from_permission_set",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach customer managed policy reference from permission set"):
        detach_customer_managed_policy_reference_from_permission_set("test-instance_arn", "test-permission_set_arn", {}, region_name=REGION)


def test_get_application_access_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    get_application_access_scope("test-application_arn", "test-scope", region_name=REGION)
    mock_client.get_application_access_scope.assert_called_once()


def test_get_application_access_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_access_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_application_access_scope",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get application access scope"):
        get_application_access_scope("test-application_arn", "test-scope", region_name=REGION)


def test_get_application_assignment_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_assignment_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    get_application_assignment_configuration("test-application_arn", region_name=REGION)
    mock_client.get_application_assignment_configuration.assert_called_once()


def test_get_application_assignment_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_assignment_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_application_assignment_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get application assignment configuration"):
        get_application_assignment_configuration("test-application_arn", region_name=REGION)


def test_get_application_authentication_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_authentication_method.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    get_application_authentication_method("test-application_arn", "test-authentication_method_type", region_name=REGION)
    mock_client.get_application_authentication_method.assert_called_once()


def test_get_application_authentication_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_authentication_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_application_authentication_method",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get application authentication method"):
        get_application_authentication_method("test-application_arn", "test-authentication_method_type", region_name=REGION)


def test_get_application_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_grant.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    get_application_grant("test-application_arn", "test-grant_type", region_name=REGION)
    mock_client.get_application_grant.assert_called_once()


def test_get_application_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_application_grant",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get application grant"):
        get_application_grant("test-application_arn", "test-grant_type", region_name=REGION)


def test_get_application_session_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_session_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    get_application_session_configuration("test-application_arn", region_name=REGION)
    mock_client.get_application_session_configuration.assert_called_once()


def test_get_application_session_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_application_session_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_application_session_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get application session configuration"):
        get_application_session_configuration("test-application_arn", region_name=REGION)


def test_get_permissions_boundary_for_permission_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_permissions_boundary_for_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    get_permissions_boundary_for_permission_set("test-instance_arn", "test-permission_set_arn", region_name=REGION)
    mock_client.get_permissions_boundary_for_permission_set.assert_called_once()


def test_get_permissions_boundary_for_permission_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_permissions_boundary_for_permission_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_permissions_boundary_for_permission_set",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get permissions boundary for permission set"):
        get_permissions_boundary_for_permission_set("test-instance_arn", "test-permission_set_arn", region_name=REGION)


def test_list_account_assignment_creation_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_assignment_creation_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_account_assignment_creation_status("test-instance_arn", region_name=REGION)
    mock_client.list_account_assignment_creation_status.assert_called_once()


def test_list_account_assignment_creation_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_assignment_creation_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_account_assignment_creation_status",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list account assignment creation status"):
        list_account_assignment_creation_status("test-instance_arn", region_name=REGION)


def test_list_account_assignment_deletion_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_assignment_deletion_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_account_assignment_deletion_status("test-instance_arn", region_name=REGION)
    mock_client.list_account_assignment_deletion_status.assert_called_once()


def test_list_account_assignment_deletion_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_assignment_deletion_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_account_assignment_deletion_status",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list account assignment deletion status"):
        list_account_assignment_deletion_status("test-instance_arn", region_name=REGION)


def test_list_account_assignments_for_principal(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_assignments_for_principal.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_account_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", region_name=REGION)
    mock_client.list_account_assignments_for_principal.assert_called_once()


def test_list_account_assignments_for_principal_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_assignments_for_principal.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_account_assignments_for_principal",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list account assignments for principal"):
        list_account_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", region_name=REGION)


def test_list_application_access_scopes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_access_scopes.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_access_scopes("test-application_arn", region_name=REGION)
    mock_client.list_application_access_scopes.assert_called_once()


def test_list_application_access_scopes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_access_scopes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_access_scopes",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application access scopes"):
        list_application_access_scopes("test-application_arn", region_name=REGION)


def test_list_application_assignments(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_assignments.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_assignments("test-application_arn", region_name=REGION)
    mock_client.list_application_assignments.assert_called_once()


def test_list_application_assignments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_assignments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_assignments",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application assignments"):
        list_application_assignments("test-application_arn", region_name=REGION)


def test_list_application_assignments_for_principal(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_assignments_for_principal.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", region_name=REGION)
    mock_client.list_application_assignments_for_principal.assert_called_once()


def test_list_application_assignments_for_principal_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_assignments_for_principal.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_assignments_for_principal",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application assignments for principal"):
        list_application_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", region_name=REGION)


def test_list_application_authentication_methods(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_authentication_methods.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_authentication_methods("test-application_arn", region_name=REGION)
    mock_client.list_application_authentication_methods.assert_called_once()


def test_list_application_authentication_methods_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_authentication_methods.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_authentication_methods",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application authentication methods"):
        list_application_authentication_methods("test-application_arn", region_name=REGION)


def test_list_application_grants(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_grants.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_grants("test-application_arn", region_name=REGION)
    mock_client.list_application_grants.assert_called_once()


def test_list_application_grants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_grants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_grants",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application grants"):
        list_application_grants("test-application_arn", region_name=REGION)


def test_list_application_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_providers.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_providers(region_name=REGION)
    mock_client.list_application_providers.assert_called_once()


def test_list_application_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_providers",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application providers"):
        list_application_providers(region_name=REGION)


def test_list_applications(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_applications.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_applications("test-instance_arn", region_name=REGION)
    mock_client.list_applications.assert_called_once()


def test_list_applications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_applications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_applications",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list applications"):
        list_applications("test-instance_arn", region_name=REGION)


def test_list_customer_managed_policy_references_in_permission_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_customer_managed_policy_references_in_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_customer_managed_policy_references_in_permission_set("test-instance_arn", "test-permission_set_arn", region_name=REGION)
    mock_client.list_customer_managed_policy_references_in_permission_set.assert_called_once()


def test_list_customer_managed_policy_references_in_permission_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_customer_managed_policy_references_in_permission_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_customer_managed_policy_references_in_permission_set",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list customer managed policy references in permission set"):
        list_customer_managed_policy_references_in_permission_set("test-instance_arn", "test-permission_set_arn", region_name=REGION)


def test_list_permission_set_provisioning_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_permission_set_provisioning_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_permission_set_provisioning_status("test-instance_arn", region_name=REGION)
    mock_client.list_permission_set_provisioning_status.assert_called_once()


def test_list_permission_set_provisioning_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_permission_set_provisioning_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_permission_set_provisioning_status",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list permission set provisioning status"):
        list_permission_set_provisioning_status("test-instance_arn", region_name=REGION)


def test_list_permission_sets_provisioned_to_account(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_permission_sets_provisioned_to_account.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_permission_sets_provisioned_to_account("test-instance_arn", "test-account_id", region_name=REGION)
    mock_client.list_permission_sets_provisioned_to_account.assert_called_once()


def test_list_permission_sets_provisioned_to_account_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_permission_sets_provisioned_to_account.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_permission_sets_provisioned_to_account",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list permission sets provisioned to account"):
        list_permission_sets_provisioned_to_account("test-instance_arn", "test-account_id", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_trusted_token_issuers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_trusted_token_issuers.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_trusted_token_issuers("test-instance_arn", region_name=REGION)
    mock_client.list_trusted_token_issuers.assert_called_once()


def test_list_trusted_token_issuers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_trusted_token_issuers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_trusted_token_issuers",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list trusted token issuers"):
        list_trusted_token_issuers("test-instance_arn", region_name=REGION)


def test_put_application_access_scope(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_access_scope("test-scope", "test-application_arn", region_name=REGION)
    mock_client.put_application_access_scope.assert_called_once()


def test_put_application_access_scope_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_access_scope.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_application_access_scope",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put application access scope"):
        put_application_access_scope("test-scope", "test-application_arn", region_name=REGION)


def test_put_application_assignment_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_assignment_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_assignment_configuration("test-application_arn", True, region_name=REGION)
    mock_client.put_application_assignment_configuration.assert_called_once()


def test_put_application_assignment_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_assignment_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_application_assignment_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put application assignment configuration"):
        put_application_assignment_configuration("test-application_arn", True, region_name=REGION)


def test_put_application_authentication_method(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_authentication_method.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_authentication_method("test-application_arn", "test-authentication_method_type", {}, region_name=REGION)
    mock_client.put_application_authentication_method.assert_called_once()


def test_put_application_authentication_method_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_authentication_method.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_application_authentication_method",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put application authentication method"):
        put_application_authentication_method("test-application_arn", "test-authentication_method_type", {}, region_name=REGION)


def test_put_application_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_grant.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_grant("test-application_arn", "test-grant_type", {}, region_name=REGION)
    mock_client.put_application_grant.assert_called_once()


def test_put_application_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_application_grant",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put application grant"):
        put_application_grant("test-application_arn", "test-grant_type", {}, region_name=REGION)


def test_put_application_session_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_session_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_session_configuration("test-application_arn", region_name=REGION)
    mock_client.put_application_session_configuration.assert_called_once()


def test_put_application_session_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_application_session_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_application_session_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put application session configuration"):
        put_application_session_configuration("test-application_arn", region_name=REGION)


def test_put_permissions_boundary_to_permission_set(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_permissions_boundary_to_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_permissions_boundary_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, region_name=REGION)
    mock_client.put_permissions_boundary_to_permission_set.assert_called_once()


def test_put_permissions_boundary_to_permission_set_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_permissions_boundary_to_permission_set.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_permissions_boundary_to_permission_set",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put permissions boundary to permission set"):
        put_permissions_boundary_to_permission_set("test-instance_arn", "test-permission_set_arn", {}, region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_application.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_application("test-application_arn", region_name=REGION)
    mock_client.update_application.assert_called_once()


def test_update_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_application",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update application"):
        update_application("test-application_arn", region_name=REGION)


def test_update_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_instance("test-instance_arn", region_name=REGION)
    mock_client.update_instance.assert_called_once()


def test_update_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_instance",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update instance"):
        update_instance("test-instance_arn", region_name=REGION)


def test_update_instance_access_control_attribute_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance_access_control_attribute_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_instance_access_control_attribute_configuration("test-instance_arn", {}, region_name=REGION)
    mock_client.update_instance_access_control_attribute_configuration.assert_called_once()


def test_update_instance_access_control_attribute_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_instance_access_control_attribute_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_instance_access_control_attribute_configuration",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update instance access control attribute configuration"):
        update_instance_access_control_attribute_configuration("test-instance_arn", {}, region_name=REGION)


def test_update_trusted_token_issuer(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_trusted_token_issuer.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_trusted_token_issuer("test-trusted_token_issuer_arn", region_name=REGION)
    mock_client.update_trusted_token_issuer.assert_called_once()


def test_update_trusted_token_issuer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_trusted_token_issuer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_trusted_token_issuer",
    )
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update trusted token issuer"):
        update_trusted_token_issuer("test-trusted_token_issuer_arn", region_name=REGION)


def test_create_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import create_instance
    mock_client = MagicMock()
    mock_client.create_instance.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_instance(name="test-name", region_name="us-east-1")
    mock_client.create_instance.assert_called_once()

def test_update_permission_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import update_permission_set
    mock_client = MagicMock()
    mock_client.update_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_permission_set("test-instance_arn", "test-permission_set_arn", description="test-description", session_duration=1, relay_state="test-relay_state", region_name="us-east-1")
    mock_client.update_permission_set.assert_called_once()

def test_provision_permission_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import provision_permission_set
    mock_client = MagicMock()
    mock_client.provision_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    provision_permission_set("test-instance_arn", "test-permission_set_arn", target_id="test-target_id", region_name="us-east-1")
    mock_client.provision_permission_set.assert_called_once()

def test_create_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import create_application
    mock_client = MagicMock()
    mock_client.create_application.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_application("test-instance_arn", "test-application_provider_arn", "test-name", description="test-description", portal_options=1, tags=[{"Key": "k", "Value": "v"}], status="test-status", client_token="test-client_token", region_name="us-east-1")
    mock_client.create_application.assert_called_once()

def test_create_trusted_token_issuer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import create_trusted_token_issuer
    mock_client = MagicMock()
    mock_client.create_trusted_token_issuer.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    create_trusted_token_issuer("test-instance_arn", "test-name", "test-trusted_token_issuer_type", {}, client_token="test-client_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_trusted_token_issuer.assert_called_once()

def test_list_account_assignment_creation_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_account_assignment_creation_status
    mock_client = MagicMock()
    mock_client.list_account_assignment_creation_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_account_assignment_creation_status("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.list_account_assignment_creation_status.assert_called_once()

def test_list_account_assignment_deletion_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_account_assignment_deletion_status
    mock_client = MagicMock()
    mock_client.list_account_assignment_deletion_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_account_assignment_deletion_status("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.list_account_assignment_deletion_status.assert_called_once()

def test_list_account_assignments_for_principal_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_account_assignments_for_principal
    mock_client = MagicMock()
    mock_client.list_account_assignments_for_principal.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_account_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_account_assignments_for_principal.assert_called_once()

def test_list_application_access_scopes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_application_access_scopes
    mock_client = MagicMock()
    mock_client.list_application_access_scopes.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_access_scopes("test-application_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_access_scopes.assert_called_once()

def test_list_application_assignments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_application_assignments
    mock_client = MagicMock()
    mock_client.list_application_assignments.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_assignments("test-application_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_assignments.assert_called_once()

def test_list_application_assignments_for_principal_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_application_assignments_for_principal
    mock_client = MagicMock()
    mock_client.list_application_assignments_for_principal.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_assignments_for_principal("test-instance_arn", "test-principal_id", "test-principal_type", filter="test-filter", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_application_assignments_for_principal.assert_called_once()

def test_list_application_authentication_methods_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_application_authentication_methods
    mock_client = MagicMock()
    mock_client.list_application_authentication_methods.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_authentication_methods("test-application_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_authentication_methods.assert_called_once()

def test_list_application_grants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_application_grants
    mock_client = MagicMock()
    mock_client.list_application_grants.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_grants("test-application_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_grants.assert_called_once()

def test_list_application_providers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_application_providers
    mock_client = MagicMock()
    mock_client.list_application_providers.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_application_providers(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_providers.assert_called_once()

def test_list_applications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_applications
    mock_client = MagicMock()
    mock_client.list_applications.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_applications("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.list_applications.assert_called_once()

def test_list_customer_managed_policy_references_in_permission_set_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_customer_managed_policy_references_in_permission_set
    mock_client = MagicMock()
    mock_client.list_customer_managed_policy_references_in_permission_set.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_customer_managed_policy_references_in_permission_set("test-instance_arn", "test-permission_set_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_customer_managed_policy_references_in_permission_set.assert_called_once()

def test_list_permission_set_provisioning_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_permission_set_provisioning_status
    mock_client = MagicMock()
    mock_client.list_permission_set_provisioning_status.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_permission_set_provisioning_status("test-instance_arn", max_results=1, next_token="test-next_token", filter="test-filter", region_name="us-east-1")
    mock_client.list_permission_set_provisioning_status.assert_called_once()

def test_list_permission_sets_provisioned_to_account_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_permission_sets_provisioned_to_account
    mock_client = MagicMock()
    mock_client.list_permission_sets_provisioned_to_account.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_permission_sets_provisioned_to_account("test-instance_arn", 1, provisioning_status="test-provisioning_status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_permission_sets_provisioned_to_account.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", instance_arn="test-instance_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_list_trusted_token_issuers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import list_trusted_token_issuers
    mock_client = MagicMock()
    mock_client.list_trusted_token_issuers.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    list_trusted_token_issuers("test-instance_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_trusted_token_issuers.assert_called_once()

def test_put_application_access_scope_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import put_application_access_scope
    mock_client = MagicMock()
    mock_client.put_application_access_scope.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_access_scope("test-scope", "test-application_arn", authorized_targets="test-authorized_targets", region_name="us-east-1")
    mock_client.put_application_access_scope.assert_called_once()

def test_put_application_session_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import put_application_session_configuration
    mock_client = MagicMock()
    mock_client.put_application_session_configuration.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    put_application_session_configuration("test-application_arn", user_background_session_application_status="test-user_background_session_application_status", region_name="us-east-1")
    mock_client.put_application_session_configuration.assert_called_once()

def test_tag_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import tag_resource
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [{"Key": "k", "Value": "v"}], instance_arn="test-instance_arn", region_name="us-east-1")
    mock_client.tag_resource.assert_called_once()

def test_untag_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import untag_resource
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", "test-tag_keys", instance_arn="test-instance_arn", region_name="us-east-1")
    mock_client.untag_resource.assert_called_once()

def test_update_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import update_application
    mock_client = MagicMock()
    mock_client.update_application.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_application("test-application_arn", name="test-name", description="test-description", status="test-status", portal_options=1, region_name="us-east-1")
    mock_client.update_application.assert_called_once()

def test_update_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import update_instance
    mock_client = MagicMock()
    mock_client.update_instance.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_instance("test-instance_arn", name="test-name", encryption_configuration={}, region_name="us-east-1")
    mock_client.update_instance.assert_called_once()

def test_update_trusted_token_issuer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.sso_admin import update_trusted_token_issuer
    mock_client = MagicMock()
    mock_client.update_trusted_token_issuer.return_value = {}
    monkeypatch.setattr("aws_util.sso_admin.get_client", lambda *a, **kw: mock_client)
    update_trusted_token_issuer("test-trusted_token_issuer_arn", name="test-name", trusted_token_issuer_configuration={}, region_name="us-east-1")
    mock_client.update_trusted_token_issuer.assert_called_once()
