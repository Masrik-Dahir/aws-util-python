"""Tests for aws_util.iam module."""
from __future__ import annotations

import json
from botocore.exceptions import ClientError
from unittest.mock import MagicMock
import pytest

from aws_util.iam import (
    IAMPolicy,
    IAMRole,
    attach_role_policy,
    create_policy,
    create_role,
    create_role_with_policies,
    delete_policy,
    delete_role,
    detach_role_policy,
    ensure_role,
    get_role,
    list_policies,
    list_roles,
    list_users,
    add_client_id_to_open_id_connect_provider,
    add_role_to_instance_profile,
    add_user_to_group,
    attach_group_policy,
    attach_user_policy,
    change_password,
    create_access_key,
    create_account_alias,
    create_delegation_request,
    create_group,
    create_instance_profile,
    create_login_profile,
    create_open_id_connect_provider,
    create_policy_version,
    create_saml_provider,
    create_service_linked_role,
    create_service_specific_credential,
    create_user,
    create_virtual_mfa_device,
    deactivate_mfa_device,
    delete_access_key,
    delete_account_alias,
    delete_account_password_policy,
    delete_group,
    delete_group_policy,
    delete_instance_profile,
    delete_login_profile,
    delete_open_id_connect_provider,
    delete_policy_version,
    delete_role_permissions_boundary,
    delete_role_policy,
    delete_saml_provider,
    delete_server_certificate,
    delete_service_linked_role,
    delete_service_specific_credential,
    delete_signing_certificate,
    delete_ssh_public_key,
    delete_user,
    delete_user_permissions_boundary,
    delete_user_policy,
    delete_virtual_mfa_device,
    detach_group_policy,
    detach_user_policy,
    disable_organizations_root_credentials_management,
    disable_organizations_root_sessions,
    enable_mfa_device,
    enable_organizations_root_credentials_management,
    enable_organizations_root_sessions,
    generate_credential_report,
    generate_organizations_access_report,
    generate_service_last_accessed_details,
    get_access_key_last_used,
    get_account_authorization_details,
    get_account_password_policy,
    get_account_summary,
    get_context_keys_for_custom_policy,
    get_context_keys_for_principal_policy,
    get_credential_report,
    get_group,
    get_group_policy,
    get_instance_profile,
    get_login_profile,
    get_mfa_device,
    get_open_id_connect_provider,
    get_organizations_access_report,
    get_policy,
    get_policy_version,
    get_role_policy,
    get_saml_provider,
    get_server_certificate,
    get_service_last_accessed_details,
    get_service_last_accessed_details_with_entities,
    get_service_linked_role_deletion_status,
    get_ssh_public_key,
    get_user,
    get_user_policy,
    list_access_keys,
    list_account_aliases,
    list_attached_group_policies,
    list_attached_role_policies,
    list_attached_user_policies,
    list_entities_for_policy,
    list_group_policies,
    list_groups,
    list_groups_for_user,
    list_instance_profile_tags,
    list_instance_profiles,
    list_instance_profiles_for_role,
    list_mfa_device_tags,
    list_mfa_devices,
    list_open_id_connect_provider_tags,
    list_open_id_connect_providers,
    list_organizations_features,
    list_policies_granting_service_access,
    list_policy_tags,
    list_policy_versions,
    list_role_policies,
    list_role_tags,
    list_saml_provider_tags,
    list_saml_providers,
    list_server_certificate_tags,
    list_server_certificates,
    list_service_specific_credentials,
    list_signing_certificates,
    list_ssh_public_keys,
    list_user_policies,
    list_user_tags,
    list_virtual_mfa_devices,
    put_group_policy,
    put_role_permissions_boundary,
    put_role_policy,
    put_user_permissions_boundary,
    put_user_policy,
    remove_client_id_from_open_id_connect_provider,
    remove_role_from_instance_profile,
    remove_user_from_group,
    reset_service_specific_credential,
    resync_mfa_device,
    set_default_policy_version,
    set_security_token_service_preferences,
    simulate_custom_policy,
    simulate_principal_policy,
    tag_instance_profile,
    tag_mfa_device,
    tag_open_id_connect_provider,
    tag_policy,
    tag_role,
    tag_saml_provider,
    tag_server_certificate,
    tag_user,
    untag_instance_profile,
    untag_mfa_device,
    untag_open_id_connect_provider,
    untag_policy,
    untag_role,
    untag_saml_provider,
    untag_server_certificate,
    untag_user,
    update_access_key,
    update_account_password_policy,
    update_assume_role_policy,
    update_group,
    update_login_profile,
    update_open_id_connect_provider_thumbprint,
    update_role,
    update_role_description,
    update_saml_provider,
    update_server_certificate,
    update_service_specific_credential,
    update_signing_certificate,
    update_ssh_public_key,
    update_user,
    upload_server_certificate,
    upload_signing_certificate,
    upload_ssh_public_key,
)

REGION = "us-east-1"

TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }
    ],
}

POLICY_DOCUMENT = {
    "Version": "2012-10-17",
    "Statement": [{"Effect": "Allow", "Action": "s3:*", "Resource": "*"}],
}


# ---------------------------------------------------------------------------
# create_role / get_role / delete_role
# ---------------------------------------------------------------------------


def test_create_role_returns_iam_role(iam_client):
    role = create_role("my-role", TRUST_POLICY, region_name=REGION)
    assert isinstance(role, IAMRole)
    assert role.role_name == "my-role"
    assert role.arn.startswith("arn:aws:iam::")


def test_create_role_with_description(iam_client):
    role = create_role(
        "desc-role",
        TRUST_POLICY,
        description="My role description",
        region_name=REGION,
    )
    assert role.role_name == "desc-role"


def test_create_role_with_path(iam_client):
    role = create_role("path-role", TRUST_POLICY, path="/myapp/", region_name=REGION)
    assert role.path == "/myapp/"


def test_create_role_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.create_role.side_effect = ClientError(
        {"Error": {"Code": "LimitExceeded", "Message": "limit exceeded"}},
        "CreateRole",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create IAM role"):
        create_role("r", TRUST_POLICY, region_name=REGION)


def test_get_role_existing(iam_client):
    iam_client.create_role(
        RoleName="existing-role",
        AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
    )
    result = get_role("existing-role", region_name=REGION)
    assert result is not None
    assert result.role_name == "existing-role"


def test_get_role_nonexistent_returns_none(iam_client):
    result = get_role("nonexistent-role", region_name=REGION)
    assert result is None


def test_get_role_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.get_role.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "GetRole",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_role failed"):
        get_role("r", region_name=REGION)


def test_delete_role(iam_client):
    iam_client.create_role(
        RoleName="del-role",
        AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
    )
    delete_role("del-role", region_name=REGION)
    result = get_role("del-role", region_name=REGION)
    assert result is None


def test_delete_role_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.delete_role.side_effect = ClientError(
        {"Error": {"Code": "NoSuchEntity", "Message": "not found"}},
        "DeleteRole",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete IAM role"):
        delete_role("r", region_name=REGION)


# ---------------------------------------------------------------------------
# list_roles
# ---------------------------------------------------------------------------


def test_list_roles(iam_client):
    iam_client.create_role(
        RoleName="lr-role",
        AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
    )
    roles = list_roles(region_name=REGION)
    assert any(r.role_name == "lr-role" for r in roles)


def test_list_roles_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "ListRoles",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_roles failed"):
        list_roles(region_name=REGION)


# ---------------------------------------------------------------------------
# attach_role_policy / detach_role_policy
# ---------------------------------------------------------------------------


def test_attach_and_detach_role_policy(iam_client):
    iam_client.create_role(
        RoleName="policy-role",
        AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
    )
    policy = iam_client.create_policy(
        PolicyName="test-policy",
        PolicyDocument=json.dumps(POLICY_DOCUMENT),
    )
    policy_arn = policy["Policy"]["Arn"]

    attach_role_policy("policy-role", policy_arn, region_name=REGION)
    # Should not raise

    detach_role_policy("policy-role", policy_arn, region_name=REGION)


def test_attach_role_policy_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.attach_role_policy.side_effect = ClientError(
        {"Error": {"Code": "NoSuchEntity", "Message": "not found"}},
        "AttachRolePolicy",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach policy"):
        attach_role_policy("r", "arn:aws:iam::123:policy/p", region_name=REGION)


def test_detach_role_policy_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.detach_role_policy.side_effect = ClientError(
        {"Error": {"Code": "NoSuchEntity", "Message": "not found"}},
        "DetachRolePolicy",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach policy"):
        detach_role_policy("r", "arn:aws:iam::123:policy/p", region_name=REGION)


# ---------------------------------------------------------------------------
# create_policy / delete_policy / list_policies
# ---------------------------------------------------------------------------


def test_create_policy_returns_iam_policy(iam_client):
    policy = create_policy(
        "my-policy",
        POLICY_DOCUMENT,
        description="Test policy",
        region_name=REGION,
    )
    assert isinstance(policy, IAMPolicy)
    assert policy.policy_name == "my-policy"
    assert policy.arn.startswith("arn:aws:iam::")


def test_create_policy_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.create_policy.side_effect = ClientError(
        {"Error": {"Code": "LimitExceeded", "Message": "limit exceeded"}},
        "CreatePolicy",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create IAM policy"):
        create_policy("p", {}, region_name=REGION)


def test_delete_policy(iam_client):
    policy = iam_client.create_policy(
        PolicyName="del-policy",
        PolicyDocument=json.dumps(POLICY_DOCUMENT),
    )
    policy_arn = policy["Policy"]["Arn"]
    delete_policy(policy_arn, region_name=REGION)


def test_delete_policy_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.delete_policy.side_effect = ClientError(
        {"Error": {"Code": "NoSuchEntity", "Message": "not found"}},
        "DeletePolicy",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete IAM policy"):
        delete_policy("arn:aws:iam::123:policy/nonexistent", region_name=REGION)


def test_list_policies(iam_client):
    iam_client.create_policy(
        PolicyName="lp-policy",
        PolicyDocument=json.dumps(POLICY_DOCUMENT),
    )
    policies = list_policies(region_name=REGION)
    assert any(p.policy_name == "lp-policy" for p in policies)


def test_list_policies_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "ListPolicies",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_policies failed"):
        list_policies(region_name=REGION)


# ---------------------------------------------------------------------------
# list_users
# ---------------------------------------------------------------------------


def test_list_users(iam_client):
    iam_client.create_user(UserName="test-user")
    users = list_users(region_name=REGION)
    assert any(u.user_name == "test-user" for u in users)


def test_list_users_runtime_error(monkeypatch):
    from botocore.exceptions import ClientError
    from unittest.mock import MagicMock
    import aws_util.iam as iammod

    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
        "ListUsers",
    )
    monkeypatch.setattr(iammod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_users failed"):
        list_users(region_name=REGION)


# ---------------------------------------------------------------------------
# create_role_with_policies
# ---------------------------------------------------------------------------


def test_create_role_with_managed_policies(iam_client):
    policy = iam_client.create_policy(
        PolicyName="managed-p",
        PolicyDocument=json.dumps(POLICY_DOCUMENT),
    )
    policy_arn = policy["Policy"]["Arn"]

    role = create_role_with_policies(
        "full-role",
        TRUST_POLICY,
        managed_policy_arns=[policy_arn],
        region_name=REGION,
    )
    assert role.role_name == "full-role"


def test_create_role_with_inline_policies(iam_client):
    role = create_role_with_policies(
        "inline-role",
        TRUST_POLICY,
        inline_policies={"s3-access": POLICY_DOCUMENT},
        region_name=REGION,
    )
    assert role.role_name == "inline-role"


def test_create_role_with_no_policies(iam_client):
    role = create_role_with_policies("bare-role", TRUST_POLICY, region_name=REGION)
    assert role.role_name == "bare-role"


def test_create_role_with_inline_policy_runtime_error(iam_client, monkeypatch):
    """Inline policy put failure raises RuntimeError."""
    from botocore.exceptions import ClientError
    import aws_util.iam as iammod

    real_get_client = iammod.get_client

    def patched_get_client(service, region_name=None):
        client = real_get_client(service, region_name=region_name)

        def failing_put(**kwargs):
            raise ClientError(
                {"Error": {"Code": "AccessDenied", "Message": "Denied"}},
                "PutRolePolicy",
            )

        client.put_role_policy = failing_put
        return client

    monkeypatch.setattr(iammod, "get_client", patched_get_client)
    with pytest.raises(RuntimeError, match="Failed to put inline policy"):
        create_role_with_policies(
            "err-role",
            TRUST_POLICY,
            inline_policies={"bad-policy": POLICY_DOCUMENT},
            region_name=REGION,
        )


# ---------------------------------------------------------------------------
# ensure_role
# ---------------------------------------------------------------------------


def test_ensure_role_creates_when_not_exists(iam_client):
    role, created = ensure_role("new-ensure-role", TRUST_POLICY, region_name=REGION)
    assert created is True
    assert role.role_name == "new-ensure-role"


def test_ensure_role_returns_existing_when_exists(iam_client):
    iam_client.create_role(
        RoleName="existing-ensure-role",
        AssumeRolePolicyDocument=json.dumps(TRUST_POLICY),
    )
    role, created = ensure_role("existing-ensure-role", TRUST_POLICY, region_name=REGION)
    assert created is False
    assert role.role_name == "existing-ensure-role"


def test_ensure_role_with_managed_policies(iam_client):
    policy = iam_client.create_policy(
        PolicyName="ensure-p",
        PolicyDocument=json.dumps(POLICY_DOCUMENT),
    )
    policy_arn = policy["Policy"]["Arn"]
    role, created = ensure_role(
        "ensure-with-policy",
        TRUST_POLICY,
        managed_policy_arns=[policy_arn],
        region_name=REGION,
    )
    assert created is True


def test_add_client_id_to_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_client_id_to_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    add_client_id_to_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", region_name=REGION)
    mock_client.add_client_id_to_open_id_connect_provider.assert_called_once()


def test_add_client_id_to_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_client_id_to_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_client_id_to_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add client id to open id connect provider"):
        add_client_id_to_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", region_name=REGION)


def test_add_role_to_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_role_to_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    add_role_to_instance_profile("test-instance_profile_name", "test-role_name", region_name=REGION)
    mock_client.add_role_to_instance_profile.assert_called_once()


def test_add_role_to_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_role_to_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_role_to_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add role to instance profile"):
        add_role_to_instance_profile("test-instance_profile_name", "test-role_name", region_name=REGION)


def test_add_user_to_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_user_to_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    add_user_to_group("test-group_name", "test-user_name", region_name=REGION)
    mock_client.add_user_to_group.assert_called_once()


def test_add_user_to_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_user_to_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_user_to_group",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add user to group"):
        add_user_to_group("test-group_name", "test-user_name", region_name=REGION)


def test_attach_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    attach_group_policy("test-group_name", "test-policy_arn", region_name=REGION)
    mock_client.attach_group_policy.assert_called_once()


def test_attach_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_group_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach group policy"):
        attach_group_policy("test-group_name", "test-policy_arn", region_name=REGION)


def test_attach_user_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_user_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    attach_user_policy("test-user_name", "test-policy_arn", region_name=REGION)
    mock_client.attach_user_policy.assert_called_once()


def test_attach_user_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.attach_user_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "attach_user_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to attach user policy"):
        attach_user_policy("test-user_name", "test-policy_arn", region_name=REGION)


def test_change_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_password.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    change_password("test-old_password", "test-new_password", region_name=REGION)
    mock_client.change_password.assert_called_once()


def test_change_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "change_password",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to change password"):
        change_password("test-old_password", "test-new_password", region_name=REGION)


def test_create_access_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_access_key(region_name=REGION)
    mock_client.create_access_key.assert_called_once()


def test_create_access_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_access_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create access key"):
        create_access_key(region_name=REGION)


def test_create_account_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_account_alias.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_account_alias("test-account_alias", region_name=REGION)
    mock_client.create_account_alias.assert_called_once()


def test_create_account_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_account_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_account_alias",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create account alias"):
        create_account_alias("test-account_alias", region_name=REGION)


def test_create_delegation_request(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_delegation_request.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_delegation_request("test-description", {}, "test-requestor_workflow_id", "test-notification_channel", 1, region_name=REGION)
    mock_client.create_delegation_request.assert_called_once()


def test_create_delegation_request_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_delegation_request.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_delegation_request",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create delegation request"):
        create_delegation_request("test-description", {}, "test-requestor_workflow_id", "test-notification_channel", 1, region_name=REGION)


def test_create_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_group("test-group_name", region_name=REGION)
    mock_client.create_group.assert_called_once()


def test_create_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_group",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create group"):
        create_group("test-group_name", region_name=REGION)


def test_create_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_instance_profile("test-instance_profile_name", region_name=REGION)
    mock_client.create_instance_profile.assert_called_once()


def test_create_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create instance profile"):
        create_instance_profile("test-instance_profile_name", region_name=REGION)


def test_create_login_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_login_profile(region_name=REGION)
    mock_client.create_login_profile.assert_called_once()


def test_create_login_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_login_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_login_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create login profile"):
        create_login_profile(region_name=REGION)


def test_create_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_open_id_connect_provider("test-url", region_name=REGION)
    mock_client.create_open_id_connect_provider.assert_called_once()


def test_create_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create open id connect provider"):
        create_open_id_connect_provider("test-url", region_name=REGION)


def test_create_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_policy_version("test-policy_arn", "test-policy_document", region_name=REGION)
    mock_client.create_policy_version.assert_called_once()


def test_create_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_policy_version",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create policy version"):
        create_policy_version("test-policy_arn", "test-policy_document", region_name=REGION)


def test_create_saml_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_saml_provider("test-saml_metadata_document", "test-name", region_name=REGION)
    mock_client.create_saml_provider.assert_called_once()


def test_create_saml_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_saml_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_saml_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create saml provider"):
        create_saml_provider("test-saml_metadata_document", "test-name", region_name=REGION)


def test_create_service_linked_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_linked_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_service_linked_role("test-aws_service_name", region_name=REGION)
    mock_client.create_service_linked_role.assert_called_once()


def test_create_service_linked_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_linked_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service_linked_role",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service linked role"):
        create_service_linked_role("test-aws_service_name", region_name=REGION)


def test_create_service_specific_credential(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_service_specific_credential("test-user_name", "test-service_name", region_name=REGION)
    mock_client.create_service_specific_credential.assert_called_once()


def test_create_service_specific_credential_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_service_specific_credential.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_service_specific_credential",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create service specific credential"):
        create_service_specific_credential("test-user_name", "test-service_name", region_name=REGION)


def test_create_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_user("test-user_name", region_name=REGION)
    mock_client.create_user.assert_called_once()


def test_create_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user"):
        create_user("test-user_name", region_name=REGION)


def test_create_virtual_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_virtual_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_virtual_mfa_device("test-virtual_mfa_device_name", region_name=REGION)
    mock_client.create_virtual_mfa_device.assert_called_once()


def test_create_virtual_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_virtual_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_virtual_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create virtual mfa device"):
        create_virtual_mfa_device("test-virtual_mfa_device_name", region_name=REGION)


def test_deactivate_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    deactivate_mfa_device("test-serial_number", region_name=REGION)
    mock_client.deactivate_mfa_device.assert_called_once()


def test_deactivate_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deactivate_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deactivate_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deactivate mfa device"):
        deactivate_mfa_device("test-serial_number", region_name=REGION)


def test_delete_access_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_access_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_access_key("test-access_key_id", region_name=REGION)
    mock_client.delete_access_key.assert_called_once()


def test_delete_access_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_access_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_access_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete access key"):
        delete_access_key("test-access_key_id", region_name=REGION)


def test_delete_account_alias(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_alias.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_account_alias("test-account_alias", region_name=REGION)
    mock_client.delete_account_alias.assert_called_once()


def test_delete_account_alias_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_alias.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_alias",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete account alias"):
        delete_account_alias("test-account_alias", region_name=REGION)


def test_delete_account_password_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_password_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_account_password_policy(region_name=REGION)
    mock_client.delete_account_password_policy.assert_called_once()


def test_delete_account_password_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_account_password_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_account_password_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete account password policy"):
        delete_account_password_policy(region_name=REGION)


def test_delete_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_group("test-group_name", region_name=REGION)
    mock_client.delete_group.assert_called_once()


def test_delete_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_group",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete group"):
        delete_group("test-group_name", region_name=REGION)


def test_delete_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_group_policy("test-group_name", "test-policy_name", region_name=REGION)
    mock_client.delete_group_policy.assert_called_once()


def test_delete_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_group_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete group policy"):
        delete_group_policy("test-group_name", "test-policy_name", region_name=REGION)


def test_delete_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_instance_profile("test-instance_profile_name", region_name=REGION)
    mock_client.delete_instance_profile.assert_called_once()


def test_delete_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete instance profile"):
        delete_instance_profile("test-instance_profile_name", region_name=REGION)


def test_delete_login_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_login_profile(region_name=REGION)
    mock_client.delete_login_profile.assert_called_once()


def test_delete_login_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_login_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_login_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete login profile"):
        delete_login_profile(region_name=REGION)


def test_delete_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_open_id_connect_provider("test-open_id_connect_provider_arn", region_name=REGION)
    mock_client.delete_open_id_connect_provider.assert_called_once()


def test_delete_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete open id connect provider"):
        delete_open_id_connect_provider("test-open_id_connect_provider_arn", region_name=REGION)


def test_delete_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_policy_version("test-policy_arn", "test-version_id", region_name=REGION)
    mock_client.delete_policy_version.assert_called_once()


def test_delete_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_policy_version",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete policy version"):
        delete_policy_version("test-policy_arn", "test-version_id", region_name=REGION)


def test_delete_role_permissions_boundary(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_permissions_boundary.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_role_permissions_boundary("test-role_name", region_name=REGION)
    mock_client.delete_role_permissions_boundary.assert_called_once()


def test_delete_role_permissions_boundary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_permissions_boundary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_role_permissions_boundary",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete role permissions boundary"):
        delete_role_permissions_boundary("test-role_name", region_name=REGION)


def test_delete_role_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_role_policy("test-role_name", "test-policy_name", region_name=REGION)
    mock_client.delete_role_policy.assert_called_once()


def test_delete_role_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_role_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_role_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete role policy"):
        delete_role_policy("test-role_name", "test-policy_name", region_name=REGION)


def test_delete_saml_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_saml_provider("test-saml_provider_arn", region_name=REGION)
    mock_client.delete_saml_provider.assert_called_once()


def test_delete_saml_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_saml_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_saml_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete saml provider"):
        delete_saml_provider("test-saml_provider_arn", region_name=REGION)


def test_delete_server_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_server_certificate("test-server_certificate_name", region_name=REGION)
    mock_client.delete_server_certificate.assert_called_once()


def test_delete_server_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_server_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_server_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete server certificate"):
        delete_server_certificate("test-server_certificate_name", region_name=REGION)


def test_delete_service_linked_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_linked_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_service_linked_role("test-role_name", region_name=REGION)
    mock_client.delete_service_linked_role.assert_called_once()


def test_delete_service_linked_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_linked_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_linked_role",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service linked role"):
        delete_service_linked_role("test-role_name", region_name=REGION)


def test_delete_service_specific_credential(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_service_specific_credential("test-service_specific_credential_id", region_name=REGION)
    mock_client.delete_service_specific_credential.assert_called_once()


def test_delete_service_specific_credential_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_service_specific_credential.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_service_specific_credential",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete service specific credential"):
        delete_service_specific_credential("test-service_specific_credential_id", region_name=REGION)


def test_delete_signing_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_signing_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_signing_certificate("test-certificate_id", region_name=REGION)
    mock_client.delete_signing_certificate.assert_called_once()


def test_delete_signing_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_signing_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_signing_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete signing certificate"):
        delete_signing_certificate("test-certificate_id", region_name=REGION)


def test_delete_ssh_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ssh_public_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_ssh_public_key("test-user_name", "test-ssh_public_key_id", region_name=REGION)
    mock_client.delete_ssh_public_key.assert_called_once()


def test_delete_ssh_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_ssh_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_ssh_public_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete ssh public key"):
        delete_ssh_public_key("test-user_name", "test-ssh_public_key_id", region_name=REGION)


def test_delete_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_user("test-user_name", region_name=REGION)
    mock_client.delete_user.assert_called_once()


def test_delete_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user"):
        delete_user("test-user_name", region_name=REGION)


def test_delete_user_permissions_boundary(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_permissions_boundary.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_user_permissions_boundary("test-user_name", region_name=REGION)
    mock_client.delete_user_permissions_boundary.assert_called_once()


def test_delete_user_permissions_boundary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_permissions_boundary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_permissions_boundary",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user permissions boundary"):
        delete_user_permissions_boundary("test-user_name", region_name=REGION)


def test_delete_user_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_user_policy("test-user_name", "test-policy_name", region_name=REGION)
    mock_client.delete_user_policy.assert_called_once()


def test_delete_user_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user policy"):
        delete_user_policy("test-user_name", "test-policy_name", region_name=REGION)


def test_delete_virtual_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_virtual_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_virtual_mfa_device("test-serial_number", region_name=REGION)
    mock_client.delete_virtual_mfa_device.assert_called_once()


def test_delete_virtual_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_virtual_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_virtual_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete virtual mfa device"):
        delete_virtual_mfa_device("test-serial_number", region_name=REGION)


def test_detach_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    detach_group_policy("test-group_name", "test-policy_arn", region_name=REGION)
    mock_client.detach_group_policy.assert_called_once()


def test_detach_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_group_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach group policy"):
        detach_group_policy("test-group_name", "test-policy_arn", region_name=REGION)


def test_detach_user_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_user_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    detach_user_policy("test-user_name", "test-policy_arn", region_name=REGION)
    mock_client.detach_user_policy.assert_called_once()


def test_detach_user_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.detach_user_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "detach_user_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to detach user policy"):
        detach_user_policy("test-user_name", "test-policy_arn", region_name=REGION)


def test_disable_organizations_root_credentials_management(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_organizations_root_credentials_management.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    disable_organizations_root_credentials_management(region_name=REGION)
    mock_client.disable_organizations_root_credentials_management.assert_called_once()


def test_disable_organizations_root_credentials_management_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_organizations_root_credentials_management.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_organizations_root_credentials_management",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable organizations root credentials management"):
        disable_organizations_root_credentials_management(region_name=REGION)


def test_disable_organizations_root_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_organizations_root_sessions.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    disable_organizations_root_sessions(region_name=REGION)
    mock_client.disable_organizations_root_sessions.assert_called_once()


def test_disable_organizations_root_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_organizations_root_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_organizations_root_sessions",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable organizations root sessions"):
        disable_organizations_root_sessions(region_name=REGION)


def test_enable_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    enable_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", region_name=REGION)
    mock_client.enable_mfa_device.assert_called_once()


def test_enable_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable mfa device"):
        enable_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", region_name=REGION)


def test_enable_organizations_root_credentials_management(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_organizations_root_credentials_management.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    enable_organizations_root_credentials_management(region_name=REGION)
    mock_client.enable_organizations_root_credentials_management.assert_called_once()


def test_enable_organizations_root_credentials_management_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_organizations_root_credentials_management.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_organizations_root_credentials_management",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable organizations root credentials management"):
        enable_organizations_root_credentials_management(region_name=REGION)


def test_enable_organizations_root_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_organizations_root_sessions.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    enable_organizations_root_sessions(region_name=REGION)
    mock_client.enable_organizations_root_sessions.assert_called_once()


def test_enable_organizations_root_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_organizations_root_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_organizations_root_sessions",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable organizations root sessions"):
        enable_organizations_root_sessions(region_name=REGION)


def test_generate_credential_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_credential_report.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    generate_credential_report(region_name=REGION)
    mock_client.generate_credential_report.assert_called_once()


def test_generate_credential_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_credential_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_credential_report",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate credential report"):
        generate_credential_report(region_name=REGION)


def test_generate_organizations_access_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_organizations_access_report.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    generate_organizations_access_report("test-entity_path", region_name=REGION)
    mock_client.generate_organizations_access_report.assert_called_once()


def test_generate_organizations_access_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_organizations_access_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_organizations_access_report",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate organizations access report"):
        generate_organizations_access_report("test-entity_path", region_name=REGION)


def test_generate_service_last_accessed_details(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_service_last_accessed_details.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    generate_service_last_accessed_details("test-arn", region_name=REGION)
    mock_client.generate_service_last_accessed_details.assert_called_once()


def test_generate_service_last_accessed_details_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.generate_service_last_accessed_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "generate_service_last_accessed_details",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to generate service last accessed details"):
        generate_service_last_accessed_details("test-arn", region_name=REGION)


def test_get_access_key_last_used(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_key_last_used.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_access_key_last_used("test-access_key_id", region_name=REGION)
    mock_client.get_access_key_last_used.assert_called_once()


def test_get_access_key_last_used_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_access_key_last_used.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_access_key_last_used",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get access key last used"):
        get_access_key_last_used("test-access_key_id", region_name=REGION)


def test_get_account_authorization_details(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_authorization_details.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_account_authorization_details(region_name=REGION)
    mock_client.get_account_authorization_details.assert_called_once()


def test_get_account_authorization_details_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_authorization_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_authorization_details",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account authorization details"):
        get_account_authorization_details(region_name=REGION)


def test_get_account_password_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_password_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_account_password_policy(region_name=REGION)
    mock_client.get_account_password_policy.assert_called_once()


def test_get_account_password_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_password_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_password_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account password policy"):
        get_account_password_policy(region_name=REGION)


def test_get_account_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_summary.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_account_summary(region_name=REGION)
    mock_client.get_account_summary.assert_called_once()


def test_get_account_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_account_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_account_summary",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get account summary"):
        get_account_summary(region_name=REGION)


def test_get_context_keys_for_custom_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_context_keys_for_custom_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_context_keys_for_custom_policy([], region_name=REGION)
    mock_client.get_context_keys_for_custom_policy.assert_called_once()


def test_get_context_keys_for_custom_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_context_keys_for_custom_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_context_keys_for_custom_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get context keys for custom policy"):
        get_context_keys_for_custom_policy([], region_name=REGION)


def test_get_context_keys_for_principal_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_context_keys_for_principal_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_context_keys_for_principal_policy("test-policy_source_arn", region_name=REGION)
    mock_client.get_context_keys_for_principal_policy.assert_called_once()


def test_get_context_keys_for_principal_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_context_keys_for_principal_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_context_keys_for_principal_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get context keys for principal policy"):
        get_context_keys_for_principal_policy("test-policy_source_arn", region_name=REGION)


def test_get_credential_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_credential_report.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_credential_report(region_name=REGION)
    mock_client.get_credential_report.assert_called_once()


def test_get_credential_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_credential_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_credential_report",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get credential report"):
        get_credential_report(region_name=REGION)


def test_get_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_group("test-group_name", region_name=REGION)
    mock_client.get_group.assert_called_once()


def test_get_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_group",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get group"):
        get_group("test-group_name", region_name=REGION)


def test_get_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_group_policy("test-group_name", "test-policy_name", region_name=REGION)
    mock_client.get_group_policy.assert_called_once()


def test_get_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_group_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get group policy"):
        get_group_policy("test-group_name", "test-policy_name", region_name=REGION)


def test_get_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_instance_profile("test-instance_profile_name", region_name=REGION)
    mock_client.get_instance_profile.assert_called_once()


def test_get_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get instance profile"):
        get_instance_profile("test-instance_profile_name", region_name=REGION)


def test_get_login_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_login_profile(region_name=REGION)
    mock_client.get_login_profile.assert_called_once()


def test_get_login_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_login_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_login_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get login profile"):
        get_login_profile(region_name=REGION)


def test_get_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_mfa_device("test-serial_number", region_name=REGION)
    mock_client.get_mfa_device.assert_called_once()


def test_get_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get mfa device"):
        get_mfa_device("test-serial_number", region_name=REGION)


def test_get_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_open_id_connect_provider("test-open_id_connect_provider_arn", region_name=REGION)
    mock_client.get_open_id_connect_provider.assert_called_once()


def test_get_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get open id connect provider"):
        get_open_id_connect_provider("test-open_id_connect_provider_arn", region_name=REGION)


def test_get_organizations_access_report(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organizations_access_report.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_organizations_access_report("test-job_id", region_name=REGION)
    mock_client.get_organizations_access_report.assert_called_once()


def test_get_organizations_access_report_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_organizations_access_report.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_organizations_access_report",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get organizations access report"):
        get_organizations_access_report("test-job_id", region_name=REGION)


def test_get_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_policy("test-policy_arn", region_name=REGION)
    mock_client.get_policy.assert_called_once()


def test_get_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get policy"):
        get_policy("test-policy_arn", region_name=REGION)


def test_get_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_policy_version("test-policy_arn", "test-version_id", region_name=REGION)
    mock_client.get_policy_version.assert_called_once()


def test_get_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_policy_version",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get policy version"):
        get_policy_version("test-policy_arn", "test-version_id", region_name=REGION)


def test_get_role_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_role_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_role_policy("test-role_name", "test-policy_name", region_name=REGION)
    mock_client.get_role_policy.assert_called_once()


def test_get_role_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_role_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_role_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get role policy"):
        get_role_policy("test-role_name", "test-policy_name", region_name=REGION)


def test_get_saml_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_saml_provider("test-saml_provider_arn", region_name=REGION)
    mock_client.get_saml_provider.assert_called_once()


def test_get_saml_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_saml_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_saml_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get saml provider"):
        get_saml_provider("test-saml_provider_arn", region_name=REGION)


def test_get_server_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_server_certificate("test-server_certificate_name", region_name=REGION)
    mock_client.get_server_certificate.assert_called_once()


def test_get_server_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_server_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_server_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get server certificate"):
        get_server_certificate("test-server_certificate_name", region_name=REGION)


def test_get_service_last_accessed_details(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_last_accessed_details.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_service_last_accessed_details("test-job_id", region_name=REGION)
    mock_client.get_service_last_accessed_details.assert_called_once()


def test_get_service_last_accessed_details_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_last_accessed_details.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_last_accessed_details",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service last accessed details"):
        get_service_last_accessed_details("test-job_id", region_name=REGION)


def test_get_service_last_accessed_details_with_entities(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_last_accessed_details_with_entities.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_service_last_accessed_details_with_entities("test-job_id", "test-service_namespace", region_name=REGION)
    mock_client.get_service_last_accessed_details_with_entities.assert_called_once()


def test_get_service_last_accessed_details_with_entities_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_last_accessed_details_with_entities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_last_accessed_details_with_entities",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service last accessed details with entities"):
        get_service_last_accessed_details_with_entities("test-job_id", "test-service_namespace", region_name=REGION)


def test_get_service_linked_role_deletion_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_linked_role_deletion_status.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_service_linked_role_deletion_status("test-deletion_task_id", region_name=REGION)
    mock_client.get_service_linked_role_deletion_status.assert_called_once()


def test_get_service_linked_role_deletion_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_service_linked_role_deletion_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_service_linked_role_deletion_status",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get service linked role deletion status"):
        get_service_linked_role_deletion_status("test-deletion_task_id", region_name=REGION)


def test_get_ssh_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ssh_public_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-encoding", region_name=REGION)
    mock_client.get_ssh_public_key.assert_called_once()


def test_get_ssh_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ssh_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ssh_public_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ssh public key"):
        get_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-encoding", region_name=REGION)


def test_get_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_user(region_name=REGION)
    mock_client.get_user.assert_called_once()


def test_get_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user"):
        get_user(region_name=REGION)


def test_get_user_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_user_policy("test-user_name", "test-policy_name", region_name=REGION)
    mock_client.get_user_policy.assert_called_once()


def test_get_user_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user policy"):
        get_user_policy("test-user_name", "test-policy_name", region_name=REGION)


def test_list_access_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_keys.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_access_keys(region_name=REGION)
    mock_client.list_access_keys.assert_called_once()


def test_list_access_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_keys",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list access keys"):
        list_access_keys(region_name=REGION)


def test_list_account_aliases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_aliases.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_account_aliases(region_name=REGION)
    mock_client.list_account_aliases.assert_called_once()


def test_list_account_aliases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_account_aliases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_account_aliases",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list account aliases"):
        list_account_aliases(region_name=REGION)


def test_list_attached_group_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attached_group_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_attached_group_policies("test-group_name", region_name=REGION)
    mock_client.list_attached_group_policies.assert_called_once()


def test_list_attached_group_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attached_group_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_attached_group_policies",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list attached group policies"):
        list_attached_group_policies("test-group_name", region_name=REGION)


def test_list_attached_role_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attached_role_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_attached_role_policies("test-role_name", region_name=REGION)
    mock_client.list_attached_role_policies.assert_called_once()


def test_list_attached_role_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attached_role_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_attached_role_policies",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list attached role policies"):
        list_attached_role_policies("test-role_name", region_name=REGION)


def test_list_attached_user_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attached_user_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_attached_user_policies("test-user_name", region_name=REGION)
    mock_client.list_attached_user_policies.assert_called_once()


def test_list_attached_user_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_attached_user_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_attached_user_policies",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list attached user policies"):
        list_attached_user_policies("test-user_name", region_name=REGION)


def test_list_entities_for_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entities_for_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_entities_for_policy("test-policy_arn", region_name=REGION)
    mock_client.list_entities_for_policy.assert_called_once()


def test_list_entities_for_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_entities_for_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_entities_for_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list entities for policy"):
        list_entities_for_policy("test-policy_arn", region_name=REGION)


def test_list_group_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_group_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_group_policies("test-group_name", region_name=REGION)
    mock_client.list_group_policies.assert_called_once()


def test_list_group_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_group_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_group_policies",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list group policies"):
        list_group_policies("test-group_name", region_name=REGION)


def test_list_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_groups(region_name=REGION)
    mock_client.list_groups.assert_called_once()


def test_list_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_groups",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list groups"):
        list_groups(region_name=REGION)


def test_list_groups_for_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups_for_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_groups_for_user("test-user_name", region_name=REGION)
    mock_client.list_groups_for_user.assert_called_once()


def test_list_groups_for_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups_for_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_groups_for_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list groups for user"):
        list_groups_for_user("test-user_name", region_name=REGION)


def test_list_instance_profile_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_profile_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_instance_profile_tags("test-instance_profile_name", region_name=REGION)
    mock_client.list_instance_profile_tags.assert_called_once()


def test_list_instance_profile_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_profile_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instance_profile_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instance profile tags"):
        list_instance_profile_tags("test-instance_profile_name", region_name=REGION)


def test_list_instance_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_profiles.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_instance_profiles(region_name=REGION)
    mock_client.list_instance_profiles.assert_called_once()


def test_list_instance_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instance_profiles",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instance profiles"):
        list_instance_profiles(region_name=REGION)


def test_list_instance_profiles_for_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_profiles_for_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_instance_profiles_for_role("test-role_name", region_name=REGION)
    mock_client.list_instance_profiles_for_role.assert_called_once()


def test_list_instance_profiles_for_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_instance_profiles_for_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_instance_profiles_for_role",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list instance profiles for role"):
        list_instance_profiles_for_role("test-role_name", region_name=REGION)


def test_list_mfa_device_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_mfa_device_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_mfa_device_tags("test-serial_number", region_name=REGION)
    mock_client.list_mfa_device_tags.assert_called_once()


def test_list_mfa_device_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_mfa_device_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_mfa_device_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list mfa device tags"):
        list_mfa_device_tags("test-serial_number", region_name=REGION)


def test_list_mfa_devices(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_mfa_devices.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_mfa_devices(region_name=REGION)
    mock_client.list_mfa_devices.assert_called_once()


def test_list_mfa_devices_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_mfa_devices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_mfa_devices",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list mfa devices"):
        list_mfa_devices(region_name=REGION)


def test_list_open_id_connect_provider_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_open_id_connect_provider_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_open_id_connect_provider_tags("test-open_id_connect_provider_arn", region_name=REGION)
    mock_client.list_open_id_connect_provider_tags.assert_called_once()


def test_list_open_id_connect_provider_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_open_id_connect_provider_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_open_id_connect_provider_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list open id connect provider tags"):
        list_open_id_connect_provider_tags("test-open_id_connect_provider_arn", region_name=REGION)


def test_list_open_id_connect_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_open_id_connect_providers.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_open_id_connect_providers(region_name=REGION)
    mock_client.list_open_id_connect_providers.assert_called_once()


def test_list_open_id_connect_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_open_id_connect_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_open_id_connect_providers",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list open id connect providers"):
        list_open_id_connect_providers(region_name=REGION)


def test_list_organizations_features(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_organizations_features.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_organizations_features(region_name=REGION)
    mock_client.list_organizations_features.assert_called_once()


def test_list_organizations_features_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_organizations_features.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_organizations_features",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list organizations features"):
        list_organizations_features(region_name=REGION)


def test_list_policies_granting_service_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policies_granting_service_access.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_policies_granting_service_access("test-arn", [], region_name=REGION)
    mock_client.list_policies_granting_service_access.assert_called_once()


def test_list_policies_granting_service_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policies_granting_service_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policies_granting_service_access",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list policies granting service access"):
        list_policies_granting_service_access("test-arn", [], region_name=REGION)


def test_list_policy_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policy_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_policy_tags("test-policy_arn", region_name=REGION)
    mock_client.list_policy_tags.assert_called_once()


def test_list_policy_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policy_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policy_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list policy tags"):
        list_policy_tags("test-policy_arn", region_name=REGION)


def test_list_policy_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policy_versions.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_policy_versions("test-policy_arn", region_name=REGION)
    mock_client.list_policy_versions.assert_called_once()


def test_list_policy_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_policy_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_policy_versions",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list policy versions"):
        list_policy_versions("test-policy_arn", region_name=REGION)


def test_list_role_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_role_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_role_policies("test-role_name", region_name=REGION)
    mock_client.list_role_policies.assert_called_once()


def test_list_role_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_role_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_role_policies",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list role policies"):
        list_role_policies("test-role_name", region_name=REGION)


def test_list_role_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_role_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_role_tags("test-role_name", region_name=REGION)
    mock_client.list_role_tags.assert_called_once()


def test_list_role_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_role_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_role_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list role tags"):
        list_role_tags("test-role_name", region_name=REGION)


def test_list_saml_provider_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_saml_provider_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_saml_provider_tags("test-saml_provider_arn", region_name=REGION)
    mock_client.list_saml_provider_tags.assert_called_once()


def test_list_saml_provider_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_saml_provider_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_saml_provider_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list saml provider tags"):
        list_saml_provider_tags("test-saml_provider_arn", region_name=REGION)


def test_list_saml_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_saml_providers.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_saml_providers(region_name=REGION)
    mock_client.list_saml_providers.assert_called_once()


def test_list_saml_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_saml_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_saml_providers",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list saml providers"):
        list_saml_providers(region_name=REGION)


def test_list_server_certificate_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_server_certificate_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_server_certificate_tags("test-server_certificate_name", region_name=REGION)
    mock_client.list_server_certificate_tags.assert_called_once()


def test_list_server_certificate_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_server_certificate_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_server_certificate_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list server certificate tags"):
        list_server_certificate_tags("test-server_certificate_name", region_name=REGION)


def test_list_server_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_server_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_server_certificates(region_name=REGION)
    mock_client.list_server_certificates.assert_called_once()


def test_list_server_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_server_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_server_certificates",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list server certificates"):
        list_server_certificates(region_name=REGION)


def test_list_service_specific_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_specific_credentials.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_service_specific_credentials(region_name=REGION)
    mock_client.list_service_specific_credentials.assert_called_once()


def test_list_service_specific_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_service_specific_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_service_specific_credentials",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list service specific credentials"):
        list_service_specific_credentials(region_name=REGION)


def test_list_signing_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_signing_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_signing_certificates(region_name=REGION)
    mock_client.list_signing_certificates.assert_called_once()


def test_list_signing_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_signing_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_signing_certificates",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list signing certificates"):
        list_signing_certificates(region_name=REGION)


def test_list_ssh_public_keys(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ssh_public_keys.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_ssh_public_keys(region_name=REGION)
    mock_client.list_ssh_public_keys.assert_called_once()


def test_list_ssh_public_keys_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_ssh_public_keys.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_ssh_public_keys",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list ssh public keys"):
        list_ssh_public_keys(region_name=REGION)


def test_list_user_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_user_policies("test-user_name", region_name=REGION)
    mock_client.list_user_policies.assert_called_once()


def test_list_user_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_policies",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user policies"):
        list_user_policies("test-user_name", region_name=REGION)


def test_list_user_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_user_tags("test-user_name", region_name=REGION)
    mock_client.list_user_tags.assert_called_once()


def test_list_user_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_tags",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user tags"):
        list_user_tags("test-user_name", region_name=REGION)


def test_list_virtual_mfa_devices(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_virtual_mfa_devices.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_virtual_mfa_devices(region_name=REGION)
    mock_client.list_virtual_mfa_devices.assert_called_once()


def test_list_virtual_mfa_devices_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_virtual_mfa_devices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_virtual_mfa_devices",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list virtual mfa devices"):
        list_virtual_mfa_devices(region_name=REGION)


def test_put_group_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_group_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    put_group_policy("test-group_name", "test-policy_name", "test-policy_document", region_name=REGION)
    mock_client.put_group_policy.assert_called_once()


def test_put_group_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_group_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_group_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put group policy"):
        put_group_policy("test-group_name", "test-policy_name", "test-policy_document", region_name=REGION)


def test_put_role_permissions_boundary(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_role_permissions_boundary.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    put_role_permissions_boundary("test-role_name", "test-permissions_boundary", region_name=REGION)
    mock_client.put_role_permissions_boundary.assert_called_once()


def test_put_role_permissions_boundary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_role_permissions_boundary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_role_permissions_boundary",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put role permissions boundary"):
        put_role_permissions_boundary("test-role_name", "test-permissions_boundary", region_name=REGION)


def test_put_role_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_role_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    put_role_policy("test-role_name", "test-policy_name", "test-policy_document", region_name=REGION)
    mock_client.put_role_policy.assert_called_once()


def test_put_role_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_role_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_role_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put role policy"):
        put_role_policy("test-role_name", "test-policy_name", "test-policy_document", region_name=REGION)


def test_put_user_permissions_boundary(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_user_permissions_boundary.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    put_user_permissions_boundary("test-user_name", "test-permissions_boundary", region_name=REGION)
    mock_client.put_user_permissions_boundary.assert_called_once()


def test_put_user_permissions_boundary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_user_permissions_boundary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_user_permissions_boundary",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put user permissions boundary"):
        put_user_permissions_boundary("test-user_name", "test-permissions_boundary", region_name=REGION)


def test_put_user_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_user_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    put_user_policy("test-user_name", "test-policy_name", "test-policy_document", region_name=REGION)
    mock_client.put_user_policy.assert_called_once()


def test_put_user_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_user_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_user_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put user policy"):
        put_user_policy("test-user_name", "test-policy_name", "test-policy_document", region_name=REGION)


def test_remove_client_id_from_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_client_id_from_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    remove_client_id_from_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", region_name=REGION)
    mock_client.remove_client_id_from_open_id_connect_provider.assert_called_once()


def test_remove_client_id_from_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_client_id_from_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_client_id_from_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove client id from open id connect provider"):
        remove_client_id_from_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", region_name=REGION)


def test_remove_role_from_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_role_from_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    remove_role_from_instance_profile("test-instance_profile_name", "test-role_name", region_name=REGION)
    mock_client.remove_role_from_instance_profile.assert_called_once()


def test_remove_role_from_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_role_from_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_role_from_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove role from instance profile"):
        remove_role_from_instance_profile("test-instance_profile_name", "test-role_name", region_name=REGION)


def test_remove_user_from_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_user_from_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    remove_user_from_group("test-group_name", "test-user_name", region_name=REGION)
    mock_client.remove_user_from_group.assert_called_once()


def test_remove_user_from_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_user_from_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_user_from_group",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove user from group"):
        remove_user_from_group("test-group_name", "test-user_name", region_name=REGION)


def test_reset_service_specific_credential(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    reset_service_specific_credential("test-service_specific_credential_id", region_name=REGION)
    mock_client.reset_service_specific_credential.assert_called_once()


def test_reset_service_specific_credential_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_service_specific_credential.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_service_specific_credential",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset service specific credential"):
        reset_service_specific_credential("test-service_specific_credential_id", region_name=REGION)


def test_resync_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.resync_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    resync_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", region_name=REGION)
    mock_client.resync_mfa_device.assert_called_once()


def test_resync_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resync_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resync_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resync mfa device"):
        resync_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", region_name=REGION)


def test_set_default_policy_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_default_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    set_default_policy_version("test-policy_arn", "test-version_id", region_name=REGION)
    mock_client.set_default_policy_version.assert_called_once()


def test_set_default_policy_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_default_policy_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_default_policy_version",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set default policy version"):
        set_default_policy_version("test-policy_arn", "test-version_id", region_name=REGION)


def test_set_security_token_service_preferences(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_security_token_service_preferences.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    set_security_token_service_preferences("test-global_endpoint_token_version", region_name=REGION)
    mock_client.set_security_token_service_preferences.assert_called_once()


def test_set_security_token_service_preferences_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_security_token_service_preferences.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_security_token_service_preferences",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set security token service preferences"):
        set_security_token_service_preferences("test-global_endpoint_token_version", region_name=REGION)


def test_simulate_custom_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.simulate_custom_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    simulate_custom_policy([], [], region_name=REGION)
    mock_client.simulate_custom_policy.assert_called_once()


def test_simulate_custom_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.simulate_custom_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "simulate_custom_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to simulate custom policy"):
        simulate_custom_policy([], [], region_name=REGION)


def test_simulate_principal_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.simulate_principal_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    simulate_principal_policy("test-policy_source_arn", [], region_name=REGION)
    mock_client.simulate_principal_policy.assert_called_once()


def test_simulate_principal_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.simulate_principal_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "simulate_principal_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to simulate principal policy"):
        simulate_principal_policy("test-policy_source_arn", [], region_name=REGION)


def test_tag_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_instance_profile("test-instance_profile_name", [], region_name=REGION)
    mock_client.tag_instance_profile.assert_called_once()


def test_tag_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag instance profile"):
        tag_instance_profile("test-instance_profile_name", [], region_name=REGION)


def test_tag_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_mfa_device("test-serial_number", [], region_name=REGION)
    mock_client.tag_mfa_device.assert_called_once()


def test_tag_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag mfa device"):
        tag_mfa_device("test-serial_number", [], region_name=REGION)


def test_tag_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_open_id_connect_provider("test-open_id_connect_provider_arn", [], region_name=REGION)
    mock_client.tag_open_id_connect_provider.assert_called_once()


def test_tag_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag open id connect provider"):
        tag_open_id_connect_provider("test-open_id_connect_provider_arn", [], region_name=REGION)


def test_tag_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_policy("test-policy_arn", [], region_name=REGION)
    mock_client.tag_policy.assert_called_once()


def test_tag_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag policy"):
        tag_policy("test-policy_arn", [], region_name=REGION)


def test_tag_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_role("test-role_name", [], region_name=REGION)
    mock_client.tag_role.assert_called_once()


def test_tag_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_role",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag role"):
        tag_role("test-role_name", [], region_name=REGION)


def test_tag_saml_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_saml_provider("test-saml_provider_arn", [], region_name=REGION)
    mock_client.tag_saml_provider.assert_called_once()


def test_tag_saml_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_saml_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_saml_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag saml provider"):
        tag_saml_provider("test-saml_provider_arn", [], region_name=REGION)


def test_tag_server_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_server_certificate("test-server_certificate_name", [], region_name=REGION)
    mock_client.tag_server_certificate.assert_called_once()


def test_tag_server_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_server_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_server_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag server certificate"):
        tag_server_certificate("test-server_certificate_name", [], region_name=REGION)


def test_tag_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    tag_user("test-user_name", [], region_name=REGION)
    mock_client.tag_user.assert_called_once()


def test_tag_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag user"):
        tag_user("test-user_name", [], region_name=REGION)


def test_untag_instance_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_instance_profile("test-instance_profile_name", [], region_name=REGION)
    mock_client.untag_instance_profile.assert_called_once()


def test_untag_instance_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_instance_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_instance_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag instance profile"):
        untag_instance_profile("test-instance_profile_name", [], region_name=REGION)


def test_untag_mfa_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_mfa_device("test-serial_number", [], region_name=REGION)
    mock_client.untag_mfa_device.assert_called_once()


def test_untag_mfa_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_mfa_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_mfa_device",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag mfa device"):
        untag_mfa_device("test-serial_number", [], region_name=REGION)


def test_untag_open_id_connect_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_open_id_connect_provider("test-open_id_connect_provider_arn", [], region_name=REGION)
    mock_client.untag_open_id_connect_provider.assert_called_once()


def test_untag_open_id_connect_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_open_id_connect_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_open_id_connect_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag open id connect provider"):
        untag_open_id_connect_provider("test-open_id_connect_provider_arn", [], region_name=REGION)


def test_untag_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_policy("test-policy_arn", [], region_name=REGION)
    mock_client.untag_policy.assert_called_once()


def test_untag_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag policy"):
        untag_policy("test-policy_arn", [], region_name=REGION)


def test_untag_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_role("test-role_name", [], region_name=REGION)
    mock_client.untag_role.assert_called_once()


def test_untag_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_role",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag role"):
        untag_role("test-role_name", [], region_name=REGION)


def test_untag_saml_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_saml_provider("test-saml_provider_arn", [], region_name=REGION)
    mock_client.untag_saml_provider.assert_called_once()


def test_untag_saml_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_saml_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_saml_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag saml provider"):
        untag_saml_provider("test-saml_provider_arn", [], region_name=REGION)


def test_untag_server_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_server_certificate("test-server_certificate_name", [], region_name=REGION)
    mock_client.untag_server_certificate.assert_called_once()


def test_untag_server_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_server_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_server_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag server certificate"):
        untag_server_certificate("test-server_certificate_name", [], region_name=REGION)


def test_untag_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    untag_user("test-user_name", [], region_name=REGION)
    mock_client.untag_user.assert_called_once()


def test_untag_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag user"):
        untag_user("test-user_name", [], region_name=REGION)


def test_update_access_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_access_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_access_key("test-access_key_id", "test-status", region_name=REGION)
    mock_client.update_access_key.assert_called_once()


def test_update_access_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_access_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_access_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update access key"):
        update_access_key("test-access_key_id", "test-status", region_name=REGION)


def test_update_account_password_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_password_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_account_password_policy(region_name=REGION)
    mock_client.update_account_password_policy.assert_called_once()


def test_update_account_password_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_account_password_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_account_password_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update account password policy"):
        update_account_password_policy(region_name=REGION)


def test_update_assume_role_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_assume_role_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_assume_role_policy("test-role_name", "test-policy_document", region_name=REGION)
    mock_client.update_assume_role_policy.assert_called_once()


def test_update_assume_role_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_assume_role_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_assume_role_policy",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update assume role policy"):
        update_assume_role_policy("test-role_name", "test-policy_document", region_name=REGION)


def test_update_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_group("test-group_name", region_name=REGION)
    mock_client.update_group.assert_called_once()


def test_update_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_group",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update group"):
        update_group("test-group_name", region_name=REGION)


def test_update_login_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_login_profile("test-user_name", region_name=REGION)
    mock_client.update_login_profile.assert_called_once()


def test_update_login_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_login_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_login_profile",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update login profile"):
        update_login_profile("test-user_name", region_name=REGION)


def test_update_open_id_connect_provider_thumbprint(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_open_id_connect_provider_thumbprint.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_open_id_connect_provider_thumbprint("test-open_id_connect_provider_arn", [], region_name=REGION)
    mock_client.update_open_id_connect_provider_thumbprint.assert_called_once()


def test_update_open_id_connect_provider_thumbprint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_open_id_connect_provider_thumbprint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_open_id_connect_provider_thumbprint",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update open id connect provider thumbprint"):
        update_open_id_connect_provider_thumbprint("test-open_id_connect_provider_arn", [], region_name=REGION)


def test_update_role(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_role("test-role_name", region_name=REGION)
    mock_client.update_role.assert_called_once()


def test_update_role_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_role.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_role",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update role"):
        update_role("test-role_name", region_name=REGION)


def test_update_role_description(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_role_description.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_role_description("test-role_name", "test-description", region_name=REGION)
    mock_client.update_role_description.assert_called_once()


def test_update_role_description_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_role_description.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_role_description",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update role description"):
        update_role_description("test-role_name", "test-description", region_name=REGION)


def test_update_saml_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_saml_provider("test-saml_provider_arn", region_name=REGION)
    mock_client.update_saml_provider.assert_called_once()


def test_update_saml_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_saml_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_saml_provider",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update saml provider"):
        update_saml_provider("test-saml_provider_arn", region_name=REGION)


def test_update_server_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_server_certificate("test-server_certificate_name", region_name=REGION)
    mock_client.update_server_certificate.assert_called_once()


def test_update_server_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_server_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_server_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update server certificate"):
        update_server_certificate("test-server_certificate_name", region_name=REGION)


def test_update_service_specific_credential(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_service_specific_credential("test-service_specific_credential_id", "test-status", region_name=REGION)
    mock_client.update_service_specific_credential.assert_called_once()


def test_update_service_specific_credential_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_service_specific_credential.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_service_specific_credential",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update service specific credential"):
        update_service_specific_credential("test-service_specific_credential_id", "test-status", region_name=REGION)


def test_update_signing_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_signing_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_signing_certificate("test-certificate_id", "test-status", region_name=REGION)
    mock_client.update_signing_certificate.assert_called_once()


def test_update_signing_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_signing_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_signing_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update signing certificate"):
        update_signing_certificate("test-certificate_id", "test-status", region_name=REGION)


def test_update_ssh_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ssh_public_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-status", region_name=REGION)
    mock_client.update_ssh_public_key.assert_called_once()


def test_update_ssh_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_ssh_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_ssh_public_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update ssh public key"):
        update_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-status", region_name=REGION)


def test_update_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_user("test-user_name", region_name=REGION)
    mock_client.update_user.assert_called_once()


def test_update_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user"):
        update_user("test-user_name", region_name=REGION)


def test_upload_server_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    upload_server_certificate("test-server_certificate_name", "test-certificate_body", "test-private_key", region_name=REGION)
    mock_client.upload_server_certificate.assert_called_once()


def test_upload_server_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_server_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "upload_server_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload server certificate"):
        upload_server_certificate("test-server_certificate_name", "test-certificate_body", "test-private_key", region_name=REGION)


def test_upload_signing_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_signing_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    upload_signing_certificate("test-certificate_body", region_name=REGION)
    mock_client.upload_signing_certificate.assert_called_once()


def test_upload_signing_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_signing_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "upload_signing_certificate",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload signing certificate"):
        upload_signing_certificate("test-certificate_body", region_name=REGION)


def test_upload_ssh_public_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_ssh_public_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    upload_ssh_public_key("test-user_name", "test-ssh_public_key_body", region_name=REGION)
    mock_client.upload_ssh_public_key.assert_called_once()


def test_upload_ssh_public_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.upload_ssh_public_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "upload_ssh_public_key",
    )
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to upload ssh public key"):
        upload_ssh_public_key("test-user_name", "test-ssh_public_key_body", region_name=REGION)


def test_create_access_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_access_key
    mock_client = MagicMock()
    mock_client.create_access_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_access_key(user_name="test-user_name", region_name="us-east-1")
    mock_client.create_access_key.assert_called_once()

def test_create_delegation_request_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_delegation_request
    mock_client = MagicMock()
    mock_client.create_delegation_request.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_delegation_request("test-description", "test-permissions", "test-requestor_workflow_id", "test-notification_channel", 1, owner_account_id=1, request_message="test-request_message", redirect_url="test-redirect_url", only_send_by_owner="test-only_send_by_owner", region_name="us-east-1")
    mock_client.create_delegation_request.assert_called_once()

def test_create_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_group
    mock_client = MagicMock()
    mock_client.create_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_group("test-group_name", path="test-path", region_name="us-east-1")
    mock_client.create_group.assert_called_once()

def test_create_instance_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_instance_profile
    mock_client = MagicMock()
    mock_client.create_instance_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_instance_profile("test-instance_profile_name", path="test-path", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_instance_profile.assert_called_once()

def test_create_login_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_login_profile
    mock_client = MagicMock()
    mock_client.create_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_login_profile(user_name="test-user_name", password="test-password", password_reset_required="test-password_reset_required", region_name="us-east-1")
    mock_client.create_login_profile.assert_called_once()

def test_create_open_id_connect_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_open_id_connect_provider
    mock_client = MagicMock()
    mock_client.create_open_id_connect_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_open_id_connect_provider("test-url", client_id_list="test-client_id_list", thumbprint_list="test-thumbprint_list", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_open_id_connect_provider.assert_called_once()

def test_create_policy_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_policy_version
    mock_client = MagicMock()
    mock_client.create_policy_version.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_policy_version("test-policy_arn", "test-policy_document", set_as_default="test-set_as_default", region_name="us-east-1")
    mock_client.create_policy_version.assert_called_once()

def test_create_saml_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_saml_provider
    mock_client = MagicMock()
    mock_client.create_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_saml_provider("test-saml_metadata_document", "test-name", tags=[{"Key": "k", "Value": "v"}], assertion_encryption_mode="test-assertion_encryption_mode", add_private_key="test-add_private_key", region_name="us-east-1")
    mock_client.create_saml_provider.assert_called_once()

def test_create_service_linked_role_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_service_linked_role
    mock_client = MagicMock()
    mock_client.create_service_linked_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_service_linked_role("test-aws_service_name", description="test-description", custom_suffix="test-custom_suffix", region_name="us-east-1")
    mock_client.create_service_linked_role.assert_called_once()

def test_create_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_service_specific_credential
    mock_client = MagicMock()
    mock_client.create_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_service_specific_credential("test-user_name", "test-service_name", credential_age_days="test-credential_age_days", region_name="us-east-1")
    mock_client.create_service_specific_credential.assert_called_once()

def test_create_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_user
    mock_client = MagicMock()
    mock_client.create_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_user("test-user_name", path="test-path", permissions_boundary="test-permissions_boundary", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_user.assert_called_once()

def test_create_virtual_mfa_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import create_virtual_mfa_device
    mock_client = MagicMock()
    mock_client.create_virtual_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    create_virtual_mfa_device("test-virtual_mfa_device_name", path="test-path", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_virtual_mfa_device.assert_called_once()

def test_deactivate_mfa_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import deactivate_mfa_device
    mock_client = MagicMock()
    mock_client.deactivate_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    deactivate_mfa_device("test-serial_number", user_name="test-user_name", region_name="us-east-1")
    mock_client.deactivate_mfa_device.assert_called_once()

def test_delete_access_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import delete_access_key
    mock_client = MagicMock()
    mock_client.delete_access_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_access_key("test-access_key_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.delete_access_key.assert_called_once()

def test_delete_login_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import delete_login_profile
    mock_client = MagicMock()
    mock_client.delete_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_login_profile(user_name="test-user_name", region_name="us-east-1")
    mock_client.delete_login_profile.assert_called_once()

def test_delete_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import delete_service_specific_credential
    mock_client = MagicMock()
    mock_client.delete_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_service_specific_credential("test-service_specific_credential_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.delete_service_specific_credential.assert_called_once()

def test_delete_signing_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import delete_signing_certificate
    mock_client = MagicMock()
    mock_client.delete_signing_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    delete_signing_certificate("test-certificate_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.delete_signing_certificate.assert_called_once()

def test_generate_organizations_access_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import generate_organizations_access_report
    mock_client = MagicMock()
    mock_client.generate_organizations_access_report.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    generate_organizations_access_report("test-entity_path", organizations_policy_id="test-organizations_policy_id", region_name="us-east-1")
    mock_client.generate_organizations_access_report.assert_called_once()

def test_generate_service_last_accessed_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import generate_service_last_accessed_details
    mock_client = MagicMock()
    mock_client.generate_service_last_accessed_details.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    generate_service_last_accessed_details("test-arn", granularity="test-granularity", region_name="us-east-1")
    mock_client.generate_service_last_accessed_details.assert_called_once()

def test_get_account_authorization_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_account_authorization_details
    mock_client = MagicMock()
    mock_client.get_account_authorization_details.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_account_authorization_details(filter="test-filter", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.get_account_authorization_details.assert_called_once()

def test_get_context_keys_for_principal_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_context_keys_for_principal_policy
    mock_client = MagicMock()
    mock_client.get_context_keys_for_principal_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_context_keys_for_principal_policy("test-policy_source_arn", policy_input_list="test-policy_input_list", region_name="us-east-1")
    mock_client.get_context_keys_for_principal_policy.assert_called_once()

def test_get_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_group
    mock_client = MagicMock()
    mock_client.get_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_group("test-group_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.get_group.assert_called_once()

def test_get_login_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_login_profile
    mock_client = MagicMock()
    mock_client.get_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_login_profile(user_name="test-user_name", region_name="us-east-1")
    mock_client.get_login_profile.assert_called_once()

def test_get_mfa_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_mfa_device
    mock_client = MagicMock()
    mock_client.get_mfa_device.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_mfa_device("test-serial_number", user_name="test-user_name", region_name="us-east-1")
    mock_client.get_mfa_device.assert_called_once()

def test_get_organizations_access_report_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_organizations_access_report
    mock_client = MagicMock()
    mock_client.get_organizations_access_report.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_organizations_access_report("test-job_id", max_items=1, marker="test-marker", sort_key="test-sort_key", region_name="us-east-1")
    mock_client.get_organizations_access_report.assert_called_once()

def test_get_service_last_accessed_details_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_service_last_accessed_details
    mock_client = MagicMock()
    mock_client.get_service_last_accessed_details.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_service_last_accessed_details("test-job_id", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.get_service_last_accessed_details.assert_called_once()

def test_get_service_last_accessed_details_with_entities_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_service_last_accessed_details_with_entities
    mock_client = MagicMock()
    mock_client.get_service_last_accessed_details_with_entities.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_service_last_accessed_details_with_entities("test-job_id", "test-service_namespace", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.get_service_last_accessed_details_with_entities.assert_called_once()

def test_get_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import get_user
    mock_client = MagicMock()
    mock_client.get_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    get_user(user_name="test-user_name", region_name="us-east-1")
    mock_client.get_user.assert_called_once()

def test_list_access_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_access_keys
    mock_client = MagicMock()
    mock_client.list_access_keys.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_access_keys(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_access_keys.assert_called_once()

def test_list_account_aliases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_account_aliases
    mock_client = MagicMock()
    mock_client.list_account_aliases.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_account_aliases(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_account_aliases.assert_called_once()

def test_list_attached_group_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_attached_group_policies
    mock_client = MagicMock()
    mock_client.list_attached_group_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_attached_group_policies("test-group_name", path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_attached_group_policies.assert_called_once()

def test_list_attached_role_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_attached_role_policies
    mock_client = MagicMock()
    mock_client.list_attached_role_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_attached_role_policies("test-role_name", path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_attached_role_policies.assert_called_once()

def test_list_attached_user_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_attached_user_policies
    mock_client = MagicMock()
    mock_client.list_attached_user_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_attached_user_policies("test-user_name", path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_attached_user_policies.assert_called_once()

def test_list_entities_for_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_entities_for_policy
    mock_client = MagicMock()
    mock_client.list_entities_for_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_entities_for_policy("test-policy_arn", entity_filter=[{}], path_prefix="test-path_prefix", policy_usage_filter=[{}], marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_entities_for_policy.assert_called_once()

def test_list_group_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_group_policies
    mock_client = MagicMock()
    mock_client.list_group_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_group_policies("test-group_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_group_policies.assert_called_once()

def test_list_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_groups
    mock_client = MagicMock()
    mock_client.list_groups.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_groups(path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_groups.assert_called_once()

def test_list_groups_for_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_groups_for_user
    mock_client = MagicMock()
    mock_client.list_groups_for_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_groups_for_user("test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_groups_for_user.assert_called_once()

def test_list_instance_profile_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_instance_profile_tags
    mock_client = MagicMock()
    mock_client.list_instance_profile_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_instance_profile_tags("test-instance_profile_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_instance_profile_tags.assert_called_once()

def test_list_instance_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_instance_profiles
    mock_client = MagicMock()
    mock_client.list_instance_profiles.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_instance_profiles(path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_instance_profiles.assert_called_once()

def test_list_instance_profiles_for_role_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_instance_profiles_for_role
    mock_client = MagicMock()
    mock_client.list_instance_profiles_for_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_instance_profiles_for_role("test-role_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_instance_profiles_for_role.assert_called_once()

def test_list_mfa_device_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_mfa_device_tags
    mock_client = MagicMock()
    mock_client.list_mfa_device_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_mfa_device_tags("test-serial_number", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_mfa_device_tags.assert_called_once()

def test_list_mfa_devices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_mfa_devices
    mock_client = MagicMock()
    mock_client.list_mfa_devices.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_mfa_devices(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_mfa_devices.assert_called_once()

def test_list_open_id_connect_provider_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_open_id_connect_provider_tags
    mock_client = MagicMock()
    mock_client.list_open_id_connect_provider_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_open_id_connect_provider_tags("test-open_id_connect_provider_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_open_id_connect_provider_tags.assert_called_once()

def test_list_policies_granting_service_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_policies_granting_service_access
    mock_client = MagicMock()
    mock_client.list_policies_granting_service_access.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_policies_granting_service_access("test-arn", "test-service_namespaces", marker="test-marker", region_name="us-east-1")
    mock_client.list_policies_granting_service_access.assert_called_once()

def test_list_policy_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_policy_tags
    mock_client = MagicMock()
    mock_client.list_policy_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_policy_tags("test-policy_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_policy_tags.assert_called_once()

def test_list_policy_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_policy_versions
    mock_client = MagicMock()
    mock_client.list_policy_versions.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_policy_versions("test-policy_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_policy_versions.assert_called_once()

def test_list_role_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_role_policies
    mock_client = MagicMock()
    mock_client.list_role_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_role_policies("test-role_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_role_policies.assert_called_once()

def test_list_role_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_role_tags
    mock_client = MagicMock()
    mock_client.list_role_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_role_tags("test-role_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_role_tags.assert_called_once()

def test_list_saml_provider_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_saml_provider_tags
    mock_client = MagicMock()
    mock_client.list_saml_provider_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_saml_provider_tags("test-saml_provider_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_saml_provider_tags.assert_called_once()

def test_list_server_certificate_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_server_certificate_tags
    mock_client = MagicMock()
    mock_client.list_server_certificate_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_server_certificate_tags("test-server_certificate_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_server_certificate_tags.assert_called_once()

def test_list_server_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_server_certificates
    mock_client = MagicMock()
    mock_client.list_server_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_server_certificates(path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_server_certificates.assert_called_once()

def test_list_service_specific_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_service_specific_credentials
    mock_client = MagicMock()
    mock_client.list_service_specific_credentials.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_service_specific_credentials(user_name="test-user_name", service_name="test-service_name", all_users="test-all_users", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_service_specific_credentials.assert_called_once()

def test_list_signing_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_signing_certificates
    mock_client = MagicMock()
    mock_client.list_signing_certificates.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_signing_certificates(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_signing_certificates.assert_called_once()

def test_list_ssh_public_keys_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_ssh_public_keys
    mock_client = MagicMock()
    mock_client.list_ssh_public_keys.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_ssh_public_keys(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_ssh_public_keys.assert_called_once()

def test_list_user_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_user_policies
    mock_client = MagicMock()
    mock_client.list_user_policies.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_user_policies("test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_user_policies.assert_called_once()

def test_list_user_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_user_tags
    mock_client = MagicMock()
    mock_client.list_user_tags.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_user_tags("test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_user_tags.assert_called_once()

def test_list_virtual_mfa_devices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import list_virtual_mfa_devices
    mock_client = MagicMock()
    mock_client.list_virtual_mfa_devices.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    list_virtual_mfa_devices(assignment_status="test-assignment_status", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.list_virtual_mfa_devices.assert_called_once()

def test_reset_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import reset_service_specific_credential
    mock_client = MagicMock()
    mock_client.reset_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    reset_service_specific_credential("test-service_specific_credential_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.reset_service_specific_credential.assert_called_once()

def test_simulate_custom_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import simulate_custom_policy
    mock_client = MagicMock()
    mock_client.simulate_custom_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    simulate_custom_policy("test-policy_input_list", "test-action_names", permissions_boundary_policy_input_list="test-permissions_boundary_policy_input_list", resource_arns="test-resource_arns", resource_policy="{}", resource_owner="test-resource_owner", caller_arn="test-caller_arn", context_entries={}, resource_handling_option="test-resource_handling_option", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.simulate_custom_policy.assert_called_once()

def test_simulate_principal_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import simulate_principal_policy
    mock_client = MagicMock()
    mock_client.simulate_principal_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    simulate_principal_policy("test-policy_source_arn", "test-action_names", policy_input_list="test-policy_input_list", permissions_boundary_policy_input_list="test-permissions_boundary_policy_input_list", resource_arns="test-resource_arns", resource_policy="{}", resource_owner="test-resource_owner", caller_arn="test-caller_arn", context_entries={}, resource_handling_option="test-resource_handling_option", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.simulate_principal_policy.assert_called_once()

def test_update_access_key_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_access_key
    mock_client = MagicMock()
    mock_client.update_access_key.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_access_key("test-access_key_id", "test-status", user_name="test-user_name", region_name="us-east-1")
    mock_client.update_access_key.assert_called_once()

def test_update_account_password_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_account_password_policy
    mock_client = MagicMock()
    mock_client.update_account_password_policy.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_account_password_policy(minimum_password_length="test-minimum_password_length", require_symbols=True, require_numbers=True, require_uppercase_characters=True, require_lowercase_characters=True, allow_users_to_change_password=True, max_password_age=1, password_reuse_prevention="test-password_reuse_prevention", hard_expiry="test-hard_expiry", region_name="us-east-1")
    mock_client.update_account_password_policy.assert_called_once()

def test_update_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_group
    mock_client = MagicMock()
    mock_client.update_group.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_group("test-group_name", new_path="test-new_path", new_group_name="test-new_group_name", region_name="us-east-1")
    mock_client.update_group.assert_called_once()

def test_update_login_profile_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_login_profile
    mock_client = MagicMock()
    mock_client.update_login_profile.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_login_profile("test-user_name", password="test-password", password_reset_required="test-password_reset_required", region_name="us-east-1")
    mock_client.update_login_profile.assert_called_once()

def test_update_role_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_role
    mock_client = MagicMock()
    mock_client.update_role.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_role("test-role_name", description="test-description", max_session_duration=1, region_name="us-east-1")
    mock_client.update_role.assert_called_once()

def test_update_saml_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_saml_provider
    mock_client = MagicMock()
    mock_client.update_saml_provider.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_saml_provider("test-saml_provider_arn", saml_metadata_document="test-saml_metadata_document", assertion_encryption_mode="test-assertion_encryption_mode", add_private_key="test-add_private_key", remove_private_key="test-remove_private_key", region_name="us-east-1")
    mock_client.update_saml_provider.assert_called_once()

def test_update_server_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_server_certificate
    mock_client = MagicMock()
    mock_client.update_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_server_certificate("test-server_certificate_name", new_path="test-new_path", new_server_certificate_name="test-new_server_certificate_name", region_name="us-east-1")
    mock_client.update_server_certificate.assert_called_once()

def test_update_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_service_specific_credential
    mock_client = MagicMock()
    mock_client.update_service_specific_credential.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_service_specific_credential("test-service_specific_credential_id", "test-status", user_name="test-user_name", region_name="us-east-1")
    mock_client.update_service_specific_credential.assert_called_once()

def test_update_signing_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_signing_certificate
    mock_client = MagicMock()
    mock_client.update_signing_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_signing_certificate("test-certificate_id", "test-status", user_name="test-user_name", region_name="us-east-1")
    mock_client.update_signing_certificate.assert_called_once()

def test_update_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import update_user
    mock_client = MagicMock()
    mock_client.update_user.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    update_user("test-user_name", new_path="test-new_path", new_user_name="test-new_user_name", region_name="us-east-1")
    mock_client.update_user.assert_called_once()

def test_upload_server_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import upload_server_certificate
    mock_client = MagicMock()
    mock_client.upload_server_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    upload_server_certificate("test-server_certificate_name", "test-certificate_body", "test-private_key", path="test-path", certificate_chain="test-certificate_chain", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.upload_server_certificate.assert_called_once()

def test_upload_signing_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.iam import upload_signing_certificate
    mock_client = MagicMock()
    mock_client.upload_signing_certificate.return_value = {}
    monkeypatch.setattr("aws_util.iam.get_client", lambda *a, **kw: mock_client)
    upload_signing_certificate("test-certificate_body", user_name="test-user_name", region_name="us-east-1")
    mock_client.upload_signing_certificate.assert_called_once()
