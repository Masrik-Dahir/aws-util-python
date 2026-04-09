from __future__ import annotations

import json
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.iam import (
    IAMPolicy,
    IAMRole,
    IAMUser,
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


_TRUST = {"Version": "2012-10-17", "Statement": []}

_ROLE_RESP = {
    "Role": {
        "RoleId": "AROA123",
        "RoleName": "test-role",
        "Arn": "arn:aws:iam::123:role/test-role",
        "Path": "/",
        "Description": "Test",
    }
}

_POLICY_RESP = {
    "Policy": {
        "PolicyId": "ANPA123",
        "PolicyName": "test-policy",
        "Arn": "arn:aws:iam::123:policy/test-policy",
        "Path": "/",
        "DefaultVersionId": "v1",
        "AttachmentCount": 0,
    }
}


# ---------------------------------------------------------------------------
# create_role
# ---------------------------------------------------------------------------


async def test_create_role_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _ROLE_RESP
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    role = await create_role("test-role", _TRUST, description="Test")
    assert role.role_name == "test-role"


async def test_create_role_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_role("r", _TRUST)


async def test_create_role_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to create IAM role"):
        await create_role("r", _TRUST)


# ---------------------------------------------------------------------------
# get_role
# ---------------------------------------------------------------------------


async def test_get_role_found(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _ROLE_RESP
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    role = await get_role("test-role")
    assert role is not None
    assert role.role_name == "test-role"


async def test_get_role_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("NoSuchEntity")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await get_role("missing")
    assert result is None


async def test_get_role_other_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="AccessDenied"):
        await get_role("r")


# ---------------------------------------------------------------------------
# delete_role
# ---------------------------------------------------------------------------


async def test_delete_role_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_role("test-role")
    mock_client.call.assert_awaited_once()


async def test_delete_role_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_role("r")


async def test_delete_role_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to delete IAM role"):
        await delete_role("r")


# ---------------------------------------------------------------------------
# list_roles
# ---------------------------------------------------------------------------


async def test_list_roles_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Roles": [
            {
                "RoleId": "AROA1",
                "RoleName": "r1",
                "Arn": "arn:aws:iam::123:role/r1",
                "Path": "/",
            }
        ],
        "IsTruncated": False,
    }
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_roles()
    assert len(result) == 1


async def test_list_roles_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "Roles": [
                    {
                        "RoleId": "A1",
                        "RoleName": "r1",
                        "Arn": "arn:1",
                        "Path": "/",
                    }
                ],
                "IsTruncated": True,
                "Marker": "tok",
            }
        return {
            "Roles": [
                {
                    "RoleId": "A2",
                    "RoleName": "r2",
                    "Arn": "arn:2",
                    "Path": "/",
                }
            ],
            "IsTruncated": False,
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_roles()
    assert len(result) == 2


async def test_list_roles_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_roles()


async def test_list_roles_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_roles failed"):
        await list_roles()


# ---------------------------------------------------------------------------
# attach_role_policy
# ---------------------------------------------------------------------------


async def test_attach_role_policy_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_role_policy("role", "arn:aws:iam::aws:policy/ReadOnly")
    mock_client.call.assert_awaited_once()


async def test_attach_role_policy_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_role_policy("r", "arn")


async def test_attach_role_policy_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to attach policy"):
        await attach_role_policy("r", "arn")


# ---------------------------------------------------------------------------
# detach_role_policy
# ---------------------------------------------------------------------------


async def test_detach_role_policy_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_role_policy("role", "arn:aws:iam::aws:policy/ReadOnly")
    mock_client.call.assert_awaited_once()


async def test_detach_role_policy_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_role_policy("r", "arn")


async def test_detach_role_policy_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to detach policy"):
        await detach_role_policy("r", "arn")


# ---------------------------------------------------------------------------
# create_policy
# ---------------------------------------------------------------------------


async def test_create_policy_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _POLICY_RESP
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    pol = await create_policy("test-policy", {"Version": "2012-10-17", "Statement": []})
    assert pol.policy_name == "test-policy"


async def test_create_policy_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_policy("p", {})


async def test_create_policy_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to create IAM policy"):
        await create_policy("p", {})


# ---------------------------------------------------------------------------
# delete_policy
# ---------------------------------------------------------------------------


async def test_delete_policy_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_policy("arn:aws:iam::123:policy/test")
    mock_client.call.assert_awaited_once()


async def test_delete_policy_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_policy("arn")


async def test_delete_policy_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="Failed to delete IAM policy"):
        await delete_policy("arn")


# ---------------------------------------------------------------------------
# list_policies
# ---------------------------------------------------------------------------


async def test_list_policies_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Policies": [
            {
                "PolicyId": "P1",
                "PolicyName": "p1",
                "Arn": "arn:1",
                "Path": "/",
                "DefaultVersionId": "v1",
                "AttachmentCount": 0,
            }
        ],
        "IsTruncated": False,
    }
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_policies()
    assert len(result) == 1


async def test_list_policies_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "Policies": [
                    {
                        "PolicyId": "P1",
                        "PolicyName": "p1",
                        "Arn": "arn:1",
                        "Path": "/",
                    }
                ],
                "IsTruncated": True,
                "Marker": "tok",
            }
        return {
            "Policies": [
                {
                    "PolicyId": "P2",
                    "PolicyName": "p2",
                    "Arn": "arn:2",
                    "Path": "/",
                }
            ],
            "IsTruncated": False,
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_policies()
    assert len(result) == 2


async def test_list_policies_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policies()


async def test_list_policies_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_policies failed"):
        await list_policies()


# ---------------------------------------------------------------------------
# list_users
# ---------------------------------------------------------------------------


async def test_list_users_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Users": [
            {
                "UserId": "U1",
                "UserName": "alice",
                "Arn": "arn:aws:iam::123:user/alice",
                "Path": "/",
                "CreateDate": "2024-01-01",
            }
        ],
        "IsTruncated": False,
    }
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_users()
    assert len(result) == 1
    assert result[0].user_name == "alice"


async def test_list_users_pagination(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    call_count = 0

    async def _mock_call(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return {
                "Users": [
                    {
                        "UserId": "U1",
                        "UserName": "alice",
                        "Arn": "arn:1",
                        "Path": "/",
                    }
                ],
                "IsTruncated": True,
                "Marker": "tok",
            }
        return {
            "Users": [
                {
                    "UserId": "U2",
                    "UserName": "bob",
                    "Arn": "arn:2",
                    "Path": "/",
                }
            ],
            "IsTruncated": False,
        }

    mock_client.call = _mock_call
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    result = await list_users()
    assert len(result) == 2


async def test_list_users_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_users()


async def test_list_users_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="list_users failed"):
        await list_users()


# ---------------------------------------------------------------------------
# create_role_with_policies
# ---------------------------------------------------------------------------


async def test_create_role_with_policies_basic(monkeypatch: pytest.MonkeyPatch) -> None:
    role = IAMRole(
        role_id="AROA1",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_create(name, policy, **kw):
        return role

    monkeypatch.setattr(
        "aws_util.aio.iam.create_role", _fake_create
    )
    result = await create_role_with_policies("r", _TRUST)
    assert result.role_name == "r"


async def test_create_role_with_managed_policies(monkeypatch: pytest.MonkeyPatch) -> None:
    role = IAMRole(
        role_id="AROA1",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_create(name, policy, **kw):
        return role

    attach_calls = []

    async def _fake_attach(role_name, arn, region_name=None):
        attach_calls.append(arn)

    monkeypatch.setattr("aws_util.aio.iam.create_role", _fake_create)
    monkeypatch.setattr("aws_util.aio.iam.attach_role_policy", _fake_attach)

    result = await create_role_with_policies(
        "r",
        _TRUST,
        managed_policy_arns=["arn:aws:iam::aws:policy/ReadOnly"],
    )
    assert result.role_name == "r"
    assert len(attach_calls) == 1


async def test_create_role_with_inline_policies(monkeypatch: pytest.MonkeyPatch) -> None:
    role = IAMRole(
        role_id="AROA1",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_create(name, policy, **kw):
        return role

    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.iam.create_role", _fake_create)
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )

    result = await create_role_with_policies(
        "r",
        _TRUST,
        inline_policies={"pol1": {"Version": "2012-10-17", "Statement": []}},
    )
    assert result.role_name == "r"
    mock_client.call.assert_awaited()


async def test_create_role_with_inline_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    role = IAMRole(
        role_id="AROA1",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_create(name, policy, **kw):
        return role

    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr("aws_util.aio.iam.create_role", _fake_create)
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )

    with pytest.raises(RuntimeError, match="boom"):
        await create_role_with_policies(
            "r",
            _TRUST,
            inline_policies={"pol1": {}},
        )


async def test_create_role_with_inline_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    role = IAMRole(
        role_id="AROA1",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_create(name, policy, **kw):
        return role

    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr("aws_util.aio.iam.create_role", _fake_create)
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )

    with pytest.raises(RuntimeError, match="Failed to put inline policy"):
        await create_role_with_policies(
            "r",
            _TRUST,
            inline_policies={"pol1": {}},
        )


# ---------------------------------------------------------------------------
# ensure_role
# ---------------------------------------------------------------------------


async def test_ensure_role_already_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    existing = IAMRole(
        role_id="AROA1",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_get(name, region_name=None):
        return existing

    monkeypatch.setattr("aws_util.aio.iam.get_role", _fake_get)
    role, created = await ensure_role("r", _TRUST)
    assert role is existing
    assert created is False


async def test_ensure_role_creates_new(monkeypatch: pytest.MonkeyPatch) -> None:
    new_role = IAMRole(
        role_id="AROA2",
        role_name="r",
        arn="arn:aws:iam::123:role/r",
        path="/",
    )

    async def _fake_get(name, region_name=None):
        return None

    async def _fake_create_with(name, trust, **kw):
        return new_role

    monkeypatch.setattr("aws_util.aio.iam.get_role", _fake_get)
    monkeypatch.setattr(
        "aws_util.aio.iam.create_role_with_policies", _fake_create_with
    )
    role, created = await ensure_role(
        "r",
        _TRUST,
        managed_policy_arns=["arn:aws:iam::aws:policy/ReadOnly"],
        description="new",
    )
    assert role is new_role
    assert created is True


async def test_add_client_id_to_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_client_id_to_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_add_client_id_to_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_client_id_to_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", )


async def test_add_role_to_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_role_to_instance_profile("test-instance_profile_name", "test-role_name", )
    mock_client.call.assert_called_once()


async def test_add_role_to_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_role_to_instance_profile("test-instance_profile_name", "test-role_name", )


async def test_add_user_to_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_user_to_group("test-group_name", "test-user_name", )
    mock_client.call.assert_called_once()


async def test_add_user_to_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_user_to_group("test-group_name", "test-user_name", )


async def test_attach_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_group_policy("test-group_name", "test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_attach_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_group_policy("test-group_name", "test-policy_arn", )


async def test_attach_user_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await attach_user_policy("test-user_name", "test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_attach_user_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await attach_user_policy("test-user_name", "test-policy_arn", )


async def test_change_password(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await change_password("test-old_password", "test-new_password", )
    mock_client.call.assert_called_once()


async def test_change_password_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await change_password("test-old_password", "test-new_password", )


async def test_create_access_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_access_key()
    mock_client.call.assert_called_once()


async def test_create_access_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_access_key()


async def test_create_account_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_account_alias("test-account_alias", )
    mock_client.call.assert_called_once()


async def test_create_account_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_account_alias("test-account_alias", )


async def test_create_delegation_request(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_delegation_request("test-description", {}, "test-requestor_workflow_id", "test-notification_channel", 1, )
    mock_client.call.assert_called_once()


async def test_create_delegation_request_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_delegation_request("test-description", {}, "test-requestor_workflow_id", "test-notification_channel", 1, )


async def test_create_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_group("test-group_name", )
    mock_client.call.assert_called_once()


async def test_create_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_group("test-group_name", )


async def test_create_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_instance_profile("test-instance_profile_name", )
    mock_client.call.assert_called_once()


async def test_create_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_instance_profile("test-instance_profile_name", )


async def test_create_login_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_login_profile()
    mock_client.call.assert_called_once()


async def test_create_login_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_login_profile()


async def test_create_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_open_id_connect_provider("test-url", )
    mock_client.call.assert_called_once()


async def test_create_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_open_id_connect_provider("test-url", )


async def test_create_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_policy_version("test-policy_arn", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_create_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_policy_version("test-policy_arn", "test-policy_document", )


async def test_create_saml_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_saml_provider("test-saml_metadata_document", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_saml_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_saml_provider("test-saml_metadata_document", "test-name", )


async def test_create_service_linked_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service_linked_role("test-aws_service_name", )
    mock_client.call.assert_called_once()


async def test_create_service_linked_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service_linked_role("test-aws_service_name", )


async def test_create_service_specific_credential(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_service_specific_credential("test-user_name", "test-service_name", )
    mock_client.call.assert_called_once()


async def test_create_service_specific_credential_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_service_specific_credential("test-user_name", "test-service_name", )


async def test_create_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_user("test-user_name", )
    mock_client.call.assert_called_once()


async def test_create_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_user("test-user_name", )


async def test_create_virtual_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_virtual_mfa_device("test-virtual_mfa_device_name", )
    mock_client.call.assert_called_once()


async def test_create_virtual_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_virtual_mfa_device("test-virtual_mfa_device_name", )


async def test_deactivate_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await deactivate_mfa_device("test-serial_number", )
    mock_client.call.assert_called_once()


async def test_deactivate_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deactivate_mfa_device("test-serial_number", )


async def test_delete_access_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_access_key("test-access_key_id", )
    mock_client.call.assert_called_once()


async def test_delete_access_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_access_key("test-access_key_id", )


async def test_delete_account_alias(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_alias("test-account_alias", )
    mock_client.call.assert_called_once()


async def test_delete_account_alias_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_alias("test-account_alias", )


async def test_delete_account_password_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_account_password_policy()
    mock_client.call.assert_called_once()


async def test_delete_account_password_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_account_password_policy()


async def test_delete_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_group("test-group_name", )
    mock_client.call.assert_called_once()


async def test_delete_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_group("test-group_name", )


async def test_delete_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_group_policy("test-group_name", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_delete_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_group_policy("test-group_name", "test-policy_name", )


async def test_delete_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_instance_profile("test-instance_profile_name", )
    mock_client.call.assert_called_once()


async def test_delete_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_instance_profile("test-instance_profile_name", )


async def test_delete_login_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_login_profile()
    mock_client.call.assert_called_once()


async def test_delete_login_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_login_profile()


async def test_delete_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_open_id_connect_provider("test-open_id_connect_provider_arn", )
    mock_client.call.assert_called_once()


async def test_delete_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_open_id_connect_provider("test-open_id_connect_provider_arn", )


async def test_delete_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_policy_version("test-policy_arn", "test-version_id", )
    mock_client.call.assert_called_once()


async def test_delete_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_policy_version("test-policy_arn", "test-version_id", )


async def test_delete_role_permissions_boundary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_role_permissions_boundary("test-role_name", )
    mock_client.call.assert_called_once()


async def test_delete_role_permissions_boundary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_role_permissions_boundary("test-role_name", )


async def test_delete_role_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_role_policy("test-role_name", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_delete_role_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_role_policy("test-role_name", "test-policy_name", )


async def test_delete_saml_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_saml_provider("test-saml_provider_arn", )
    mock_client.call.assert_called_once()


async def test_delete_saml_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_saml_provider("test-saml_provider_arn", )


async def test_delete_server_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_server_certificate("test-server_certificate_name", )
    mock_client.call.assert_called_once()


async def test_delete_server_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_server_certificate("test-server_certificate_name", )


async def test_delete_service_linked_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_linked_role("test-role_name", )
    mock_client.call.assert_called_once()


async def test_delete_service_linked_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_linked_role("test-role_name", )


async def test_delete_service_specific_credential(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_service_specific_credential("test-service_specific_credential_id", )
    mock_client.call.assert_called_once()


async def test_delete_service_specific_credential_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_service_specific_credential("test-service_specific_credential_id", )


async def test_delete_signing_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_signing_certificate("test-certificate_id", )
    mock_client.call.assert_called_once()


async def test_delete_signing_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_signing_certificate("test-certificate_id", )


async def test_delete_ssh_public_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_ssh_public_key("test-user_name", "test-ssh_public_key_id", )
    mock_client.call.assert_called_once()


async def test_delete_ssh_public_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_ssh_public_key("test-user_name", "test-ssh_public_key_id", )


async def test_delete_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user("test-user_name", )
    mock_client.call.assert_called_once()


async def test_delete_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user("test-user_name", )


async def test_delete_user_permissions_boundary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_permissions_boundary("test-user_name", )
    mock_client.call.assert_called_once()


async def test_delete_user_permissions_boundary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_permissions_boundary("test-user_name", )


async def test_delete_user_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_policy("test-user_name", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_delete_user_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_policy("test-user_name", "test-policy_name", )


async def test_delete_virtual_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_virtual_mfa_device("test-serial_number", )
    mock_client.call.assert_called_once()


async def test_delete_virtual_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_virtual_mfa_device("test-serial_number", )


async def test_detach_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_group_policy("test-group_name", "test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_detach_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_group_policy("test-group_name", "test-policy_arn", )


async def test_detach_user_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await detach_user_policy("test-user_name", "test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_detach_user_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await detach_user_policy("test-user_name", "test-policy_arn", )


async def test_disable_organizations_root_credentials_management(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_organizations_root_credentials_management()
    mock_client.call.assert_called_once()


async def test_disable_organizations_root_credentials_management_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_organizations_root_credentials_management()


async def test_disable_organizations_root_sessions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_organizations_root_sessions()
    mock_client.call.assert_called_once()


async def test_disable_organizations_root_sessions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_organizations_root_sessions()


async def test_enable_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", )
    mock_client.call.assert_called_once()


async def test_enable_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", )


async def test_enable_organizations_root_credentials_management(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_organizations_root_credentials_management()
    mock_client.call.assert_called_once()


async def test_enable_organizations_root_credentials_management_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_organizations_root_credentials_management()


async def test_enable_organizations_root_sessions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_organizations_root_sessions()
    mock_client.call.assert_called_once()


async def test_enable_organizations_root_sessions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_organizations_root_sessions()


async def test_generate_credential_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_credential_report()
    mock_client.call.assert_called_once()


async def test_generate_credential_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_credential_report()


async def test_generate_organizations_access_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_organizations_access_report("test-entity_path", )
    mock_client.call.assert_called_once()


async def test_generate_organizations_access_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_organizations_access_report("test-entity_path", )


async def test_generate_service_last_accessed_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await generate_service_last_accessed_details("test-arn", )
    mock_client.call.assert_called_once()


async def test_generate_service_last_accessed_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await generate_service_last_accessed_details("test-arn", )


async def test_get_access_key_last_used(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_access_key_last_used("test-access_key_id", )
    mock_client.call.assert_called_once()


async def test_get_access_key_last_used_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_access_key_last_used("test-access_key_id", )


async def test_get_account_authorization_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_authorization_details()
    mock_client.call.assert_called_once()


async def test_get_account_authorization_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_authorization_details()


async def test_get_account_password_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_password_policy()
    mock_client.call.assert_called_once()


async def test_get_account_password_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_password_policy()


async def test_get_account_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_account_summary()
    mock_client.call.assert_called_once()


async def test_get_account_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_account_summary()


async def test_get_context_keys_for_custom_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_context_keys_for_custom_policy([], )
    mock_client.call.assert_called_once()


async def test_get_context_keys_for_custom_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_context_keys_for_custom_policy([], )


async def test_get_context_keys_for_principal_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_context_keys_for_principal_policy("test-policy_source_arn", )
    mock_client.call.assert_called_once()


async def test_get_context_keys_for_principal_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_context_keys_for_principal_policy("test-policy_source_arn", )


async def test_get_credential_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_credential_report()
    mock_client.call.assert_called_once()


async def test_get_credential_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_credential_report()


async def test_get_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_group("test-group_name", )
    mock_client.call.assert_called_once()


async def test_get_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_group("test-group_name", )


async def test_get_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_group_policy("test-group_name", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_get_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_group_policy("test-group_name", "test-policy_name", )


async def test_get_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_instance_profile("test-instance_profile_name", )
    mock_client.call.assert_called_once()


async def test_get_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_instance_profile("test-instance_profile_name", )


async def test_get_login_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_login_profile()
    mock_client.call.assert_called_once()


async def test_get_login_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_login_profile()


async def test_get_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_mfa_device("test-serial_number", )
    mock_client.call.assert_called_once()


async def test_get_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_mfa_device("test-serial_number", )


async def test_get_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_open_id_connect_provider("test-open_id_connect_provider_arn", )
    mock_client.call.assert_called_once()


async def test_get_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_open_id_connect_provider("test-open_id_connect_provider_arn", )


async def test_get_organizations_access_report(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_organizations_access_report("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_organizations_access_report_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_organizations_access_report("test-job_id", )


async def test_get_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_policy("test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_get_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_policy("test-policy_arn", )


async def test_get_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_policy_version("test-policy_arn", "test-version_id", )
    mock_client.call.assert_called_once()


async def test_get_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_policy_version("test-policy_arn", "test-version_id", )


async def test_get_role_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_role_policy("test-role_name", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_get_role_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_role_policy("test-role_name", "test-policy_name", )


async def test_get_saml_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_saml_provider("test-saml_provider_arn", )
    mock_client.call.assert_called_once()


async def test_get_saml_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_saml_provider("test-saml_provider_arn", )


async def test_get_server_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_server_certificate("test-server_certificate_name", )
    mock_client.call.assert_called_once()


async def test_get_server_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_server_certificate("test-server_certificate_name", )


async def test_get_service_last_accessed_details(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_last_accessed_details("test-job_id", )
    mock_client.call.assert_called_once()


async def test_get_service_last_accessed_details_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_last_accessed_details("test-job_id", )


async def test_get_service_last_accessed_details_with_entities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_last_accessed_details_with_entities("test-job_id", "test-service_namespace", )
    mock_client.call.assert_called_once()


async def test_get_service_last_accessed_details_with_entities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_last_accessed_details_with_entities("test-job_id", "test-service_namespace", )


async def test_get_service_linked_role_deletion_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_service_linked_role_deletion_status("test-deletion_task_id", )
    mock_client.call.assert_called_once()


async def test_get_service_linked_role_deletion_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_service_linked_role_deletion_status("test-deletion_task_id", )


async def test_get_ssh_public_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-encoding", )
    mock_client.call.assert_called_once()


async def test_get_ssh_public_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-encoding", )


async def test_get_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_user()
    mock_client.call.assert_called_once()


async def test_get_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_user()


async def test_get_user_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_user_policy("test-user_name", "test-policy_name", )
    mock_client.call.assert_called_once()


async def test_get_user_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_user_policy("test-user_name", "test-policy_name", )


async def test_list_access_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_keys()
    mock_client.call.assert_called_once()


async def test_list_access_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_keys()


async def test_list_account_aliases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_account_aliases()
    mock_client.call.assert_called_once()


async def test_list_account_aliases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_account_aliases()


async def test_list_attached_group_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_attached_group_policies("test-group_name", )
    mock_client.call.assert_called_once()


async def test_list_attached_group_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_attached_group_policies("test-group_name", )


async def test_list_attached_role_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_attached_role_policies("test-role_name", )
    mock_client.call.assert_called_once()


async def test_list_attached_role_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_attached_role_policies("test-role_name", )


async def test_list_attached_user_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_attached_user_policies("test-user_name", )
    mock_client.call.assert_called_once()


async def test_list_attached_user_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_attached_user_policies("test-user_name", )


async def test_list_entities_for_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_entities_for_policy("test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_list_entities_for_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_entities_for_policy("test-policy_arn", )


async def test_list_group_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_group_policies("test-group_name", )
    mock_client.call.assert_called_once()


async def test_list_group_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_group_policies("test-group_name", )


async def test_list_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_groups()
    mock_client.call.assert_called_once()


async def test_list_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_groups()


async def test_list_groups_for_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_groups_for_user("test-user_name", )
    mock_client.call.assert_called_once()


async def test_list_groups_for_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_groups_for_user("test-user_name", )


async def test_list_instance_profile_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instance_profile_tags("test-instance_profile_name", )
    mock_client.call.assert_called_once()


async def test_list_instance_profile_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instance_profile_tags("test-instance_profile_name", )


async def test_list_instance_profiles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instance_profiles()
    mock_client.call.assert_called_once()


async def test_list_instance_profiles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instance_profiles()


async def test_list_instance_profiles_for_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_instance_profiles_for_role("test-role_name", )
    mock_client.call.assert_called_once()


async def test_list_instance_profiles_for_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_instance_profiles_for_role("test-role_name", )


async def test_list_mfa_device_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_mfa_device_tags("test-serial_number", )
    mock_client.call.assert_called_once()


async def test_list_mfa_device_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_mfa_device_tags("test-serial_number", )


async def test_list_mfa_devices(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_mfa_devices()
    mock_client.call.assert_called_once()


async def test_list_mfa_devices_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_mfa_devices()


async def test_list_open_id_connect_provider_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_open_id_connect_provider_tags("test-open_id_connect_provider_arn", )
    mock_client.call.assert_called_once()


async def test_list_open_id_connect_provider_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_open_id_connect_provider_tags("test-open_id_connect_provider_arn", )


async def test_list_open_id_connect_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_open_id_connect_providers()
    mock_client.call.assert_called_once()


async def test_list_open_id_connect_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_open_id_connect_providers()


async def test_list_organizations_features(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_organizations_features()
    mock_client.call.assert_called_once()


async def test_list_organizations_features_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_organizations_features()


async def test_list_policies_granting_service_access(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policies_granting_service_access("test-arn", [], )
    mock_client.call.assert_called_once()


async def test_list_policies_granting_service_access_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policies_granting_service_access("test-arn", [], )


async def test_list_policy_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policy_tags("test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_list_policy_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policy_tags("test-policy_arn", )


async def test_list_policy_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_policy_versions("test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_list_policy_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_policy_versions("test-policy_arn", )


async def test_list_role_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_role_policies("test-role_name", )
    mock_client.call.assert_called_once()


async def test_list_role_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_role_policies("test-role_name", )


async def test_list_role_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_role_tags("test-role_name", )
    mock_client.call.assert_called_once()


async def test_list_role_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_role_tags("test-role_name", )


async def test_list_saml_provider_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_saml_provider_tags("test-saml_provider_arn", )
    mock_client.call.assert_called_once()


async def test_list_saml_provider_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_saml_provider_tags("test-saml_provider_arn", )


async def test_list_saml_providers(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_saml_providers()
    mock_client.call.assert_called_once()


async def test_list_saml_providers_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_saml_providers()


async def test_list_server_certificate_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_server_certificate_tags("test-server_certificate_name", )
    mock_client.call.assert_called_once()


async def test_list_server_certificate_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_server_certificate_tags("test-server_certificate_name", )


async def test_list_server_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_server_certificates()
    mock_client.call.assert_called_once()


async def test_list_server_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_server_certificates()


async def test_list_service_specific_credentials(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_service_specific_credentials()
    mock_client.call.assert_called_once()


async def test_list_service_specific_credentials_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_service_specific_credentials()


async def test_list_signing_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_signing_certificates()
    mock_client.call.assert_called_once()


async def test_list_signing_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_signing_certificates()


async def test_list_ssh_public_keys(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_ssh_public_keys()
    mock_client.call.assert_called_once()


async def test_list_ssh_public_keys_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_ssh_public_keys()


async def test_list_user_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_user_policies("test-user_name", )
    mock_client.call.assert_called_once()


async def test_list_user_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_policies("test-user_name", )


async def test_list_user_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_user_tags("test-user_name", )
    mock_client.call.assert_called_once()


async def test_list_user_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_tags("test-user_name", )


async def test_list_virtual_mfa_devices(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_virtual_mfa_devices()
    mock_client.call.assert_called_once()


async def test_list_virtual_mfa_devices_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_virtual_mfa_devices()


async def test_put_group_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_group_policy("test-group_name", "test-policy_name", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_group_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_group_policy("test-group_name", "test-policy_name", "test-policy_document", )


async def test_put_role_permissions_boundary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_role_permissions_boundary("test-role_name", "test-permissions_boundary", )
    mock_client.call.assert_called_once()


async def test_put_role_permissions_boundary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_role_permissions_boundary("test-role_name", "test-permissions_boundary", )


async def test_put_role_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_role_policy("test-role_name", "test-policy_name", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_role_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_role_policy("test-role_name", "test-policy_name", "test-policy_document", )


async def test_put_user_permissions_boundary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_user_permissions_boundary("test-user_name", "test-permissions_boundary", )
    mock_client.call.assert_called_once()


async def test_put_user_permissions_boundary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_user_permissions_boundary("test-user_name", "test-permissions_boundary", )


async def test_put_user_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_user_policy("test-user_name", "test-policy_name", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_put_user_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_user_policy("test-user_name", "test-policy_name", "test-policy_document", )


async def test_remove_client_id_from_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_client_id_from_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_remove_client_id_from_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_client_id_from_open_id_connect_provider("test-open_id_connect_provider_arn", "test-client_id", )


async def test_remove_role_from_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_role_from_instance_profile("test-instance_profile_name", "test-role_name", )
    mock_client.call.assert_called_once()


async def test_remove_role_from_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_role_from_instance_profile("test-instance_profile_name", "test-role_name", )


async def test_remove_user_from_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_user_from_group("test-group_name", "test-user_name", )
    mock_client.call.assert_called_once()


async def test_remove_user_from_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_user_from_group("test-group_name", "test-user_name", )


async def test_reset_service_specific_credential(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_service_specific_credential("test-service_specific_credential_id", )
    mock_client.call.assert_called_once()


async def test_reset_service_specific_credential_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_service_specific_credential("test-service_specific_credential_id", )


async def test_resync_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await resync_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", )
    mock_client.call.assert_called_once()


async def test_resync_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resync_mfa_device("test-user_name", "test-serial_number", "test-authentication_code1", "test-authentication_code2", )


async def test_set_default_policy_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_default_policy_version("test-policy_arn", "test-version_id", )
    mock_client.call.assert_called_once()


async def test_set_default_policy_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_default_policy_version("test-policy_arn", "test-version_id", )


async def test_set_security_token_service_preferences(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_security_token_service_preferences("test-global_endpoint_token_version", )
    mock_client.call.assert_called_once()


async def test_set_security_token_service_preferences_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_security_token_service_preferences("test-global_endpoint_token_version", )


async def test_simulate_custom_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await simulate_custom_policy([], [], )
    mock_client.call.assert_called_once()


async def test_simulate_custom_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await simulate_custom_policy([], [], )


async def test_simulate_principal_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await simulate_principal_policy("test-policy_source_arn", [], )
    mock_client.call.assert_called_once()


async def test_simulate_principal_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await simulate_principal_policy("test-policy_source_arn", [], )


async def test_tag_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_instance_profile("test-instance_profile_name", [], )
    mock_client.call.assert_called_once()


async def test_tag_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_instance_profile("test-instance_profile_name", [], )


async def test_tag_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_mfa_device("test-serial_number", [], )
    mock_client.call.assert_called_once()


async def test_tag_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_mfa_device("test-serial_number", [], )


async def test_tag_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_open_id_connect_provider("test-open_id_connect_provider_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_open_id_connect_provider("test-open_id_connect_provider_arn", [], )


async def test_tag_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_policy("test-policy_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_policy("test-policy_arn", [], )


async def test_tag_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_role("test-role_name", [], )
    mock_client.call.assert_called_once()


async def test_tag_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_role("test-role_name", [], )


async def test_tag_saml_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_saml_provider("test-saml_provider_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_saml_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_saml_provider("test-saml_provider_arn", [], )


async def test_tag_server_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_server_certificate("test-server_certificate_name", [], )
    mock_client.call.assert_called_once()


async def test_tag_server_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_server_certificate("test-server_certificate_name", [], )


async def test_tag_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_user("test-user_name", [], )
    mock_client.call.assert_called_once()


async def test_tag_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_user("test-user_name", [], )


async def test_untag_instance_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_instance_profile("test-instance_profile_name", [], )
    mock_client.call.assert_called_once()


async def test_untag_instance_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_instance_profile("test-instance_profile_name", [], )


async def test_untag_mfa_device(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_mfa_device("test-serial_number", [], )
    mock_client.call.assert_called_once()


async def test_untag_mfa_device_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_mfa_device("test-serial_number", [], )


async def test_untag_open_id_connect_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_open_id_connect_provider("test-open_id_connect_provider_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_open_id_connect_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_open_id_connect_provider("test-open_id_connect_provider_arn", [], )


async def test_untag_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_policy("test-policy_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_policy("test-policy_arn", [], )


async def test_untag_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_role("test-role_name", [], )
    mock_client.call.assert_called_once()


async def test_untag_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_role("test-role_name", [], )


async def test_untag_saml_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_saml_provider("test-saml_provider_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_saml_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_saml_provider("test-saml_provider_arn", [], )


async def test_untag_server_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_server_certificate("test-server_certificate_name", [], )
    mock_client.call.assert_called_once()


async def test_untag_server_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_server_certificate("test-server_certificate_name", [], )


async def test_untag_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_user("test-user_name", [], )
    mock_client.call.assert_called_once()


async def test_untag_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_user("test-user_name", [], )


async def test_update_access_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_access_key("test-access_key_id", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_access_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_access_key("test-access_key_id", "test-status", )


async def test_update_account_password_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_account_password_policy()
    mock_client.call.assert_called_once()


async def test_update_account_password_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_account_password_policy()


async def test_update_assume_role_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_assume_role_policy("test-role_name", "test-policy_document", )
    mock_client.call.assert_called_once()


async def test_update_assume_role_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_assume_role_policy("test-role_name", "test-policy_document", )


async def test_update_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_group("test-group_name", )
    mock_client.call.assert_called_once()


async def test_update_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_group("test-group_name", )


async def test_update_login_profile(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_login_profile("test-user_name", )
    mock_client.call.assert_called_once()


async def test_update_login_profile_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_login_profile("test-user_name", )


async def test_update_open_id_connect_provider_thumbprint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_open_id_connect_provider_thumbprint("test-open_id_connect_provider_arn", [], )
    mock_client.call.assert_called_once()


async def test_update_open_id_connect_provider_thumbprint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_open_id_connect_provider_thumbprint("test-open_id_connect_provider_arn", [], )


async def test_update_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_role("test-role_name", )
    mock_client.call.assert_called_once()


async def test_update_role_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_role("test-role_name", )


async def test_update_role_description(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_role_description("test-role_name", "test-description", )
    mock_client.call.assert_called_once()


async def test_update_role_description_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_role_description("test-role_name", "test-description", )


async def test_update_saml_provider(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_saml_provider("test-saml_provider_arn", )
    mock_client.call.assert_called_once()


async def test_update_saml_provider_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_saml_provider("test-saml_provider_arn", )


async def test_update_server_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_server_certificate("test-server_certificate_name", )
    mock_client.call.assert_called_once()


async def test_update_server_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_server_certificate("test-server_certificate_name", )


async def test_update_service_specific_credential(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_service_specific_credential("test-service_specific_credential_id", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_service_specific_credential_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_service_specific_credential("test-service_specific_credential_id", "test-status", )


async def test_update_signing_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_signing_certificate("test-certificate_id", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_signing_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_signing_certificate("test-certificate_id", "test-status", )


async def test_update_ssh_public_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-status", )
    mock_client.call.assert_called_once()


async def test_update_ssh_public_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_ssh_public_key("test-user_name", "test-ssh_public_key_id", "test-status", )


async def test_update_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_user("test-user_name", )
    mock_client.call.assert_called_once()


async def test_update_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_user("test-user_name", )


async def test_upload_server_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await upload_server_certificate("test-server_certificate_name", "test-certificate_body", "test-private_key", )
    mock_client.call.assert_called_once()


async def test_upload_server_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await upload_server_certificate("test-server_certificate_name", "test-certificate_body", "test-private_key", )


async def test_upload_signing_certificate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await upload_signing_certificate("test-certificate_body", )
    mock_client.call.assert_called_once()


async def test_upload_signing_certificate_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await upload_signing_certificate("test-certificate_body", )


async def test_upload_ssh_public_key(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    await upload_ssh_public_key("test-user_name", "test-ssh_public_key_body", )
    mock_client.call.assert_called_once()


async def test_upload_ssh_public_key_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.iam.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await upload_ssh_public_key("test-user_name", "test-ssh_public_key_body", )


@pytest.mark.asyncio
async def test_create_access_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_access_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_access_key(user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_delegation_request_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_delegation_request
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_delegation_request("test-description", "test-permissions", "test-requestor_workflow_id", "test-notification_channel", 1, owner_account_id=1, request_message="test-request_message", redirect_url="test-redirect_url", only_send_by_owner="test-only_send_by_owner", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_group("test-group_name", path="test-path", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_instance_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_instance_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_instance_profile("test-instance_profile_name", path="test-path", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_login_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_login_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_login_profile(user_name="test-user_name", password="test-password", password_reset_required="test-password_reset_required", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_open_id_connect_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_open_id_connect_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_open_id_connect_provider("test-url", client_id_list="test-client_id_list", thumbprint_list="test-thumbprint_list", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_policy_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_policy_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_policy_version("test-policy_arn", "test-policy_document", set_as_default="test-set_as_default", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_saml_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_saml_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_saml_provider("test-saml_metadata_document", "test-name", tags=[{"Key": "k", "Value": "v"}], assertion_encryption_mode="test-assertion_encryption_mode", add_private_key="test-add_private_key", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_linked_role_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_service_linked_role
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_service_linked_role("test-aws_service_name", description="test-description", custom_suffix="test-custom_suffix", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_service_specific_credential
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_service_specific_credential("test-user_name", "test-service_name", credential_age_days="test-credential_age_days", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_user("test-user_name", path="test-path", permissions_boundary="test-permissions_boundary", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_virtual_mfa_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import create_virtual_mfa_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await create_virtual_mfa_device("test-virtual_mfa_device_name", path="test-path", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deactivate_mfa_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import deactivate_mfa_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await deactivate_mfa_device("test-serial_number", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_access_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import delete_access_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await delete_access_key("test-access_key_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_login_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import delete_login_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await delete_login_profile(user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import delete_service_specific_credential
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await delete_service_specific_credential("test-service_specific_credential_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_signing_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import delete_signing_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await delete_signing_certificate("test-certificate_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_organizations_access_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import generate_organizations_access_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await generate_organizations_access_report("test-entity_path", organizations_policy_id="test-organizations_policy_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_generate_service_last_accessed_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import generate_service_last_accessed_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await generate_service_last_accessed_details("test-arn", granularity="test-granularity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_account_authorization_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_account_authorization_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_account_authorization_details(filter="test-filter", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_context_keys_for_principal_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_context_keys_for_principal_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_context_keys_for_principal_policy("test-policy_source_arn", policy_input_list="test-policy_input_list", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_group("test-group_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_login_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_login_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_login_profile(user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_mfa_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_mfa_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_mfa_device("test-serial_number", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_organizations_access_report_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_organizations_access_report
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_organizations_access_report("test-job_id", max_items=1, marker="test-marker", sort_key="test-sort_key", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_service_last_accessed_details_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_service_last_accessed_details
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_service_last_accessed_details("test-job_id", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_service_last_accessed_details_with_entities_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_service_last_accessed_details_with_entities
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_service_last_accessed_details_with_entities("test-job_id", "test-service_namespace", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import get_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await get_user(user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_access_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_access_keys(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_account_aliases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_account_aliases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_account_aliases(marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_attached_group_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_attached_group_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_attached_group_policies("test-group_name", path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_attached_role_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_attached_role_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_attached_role_policies("test-role_name", path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_attached_user_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_attached_user_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_attached_user_policies("test-user_name", path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_entities_for_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_entities_for_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_entities_for_policy("test-policy_arn", entity_filter=[{}], path_prefix="test-path_prefix", policy_usage_filter=[{}], marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_group_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_group_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_group_policies("test-group_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_groups(path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_groups_for_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_groups_for_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_groups_for_user("test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instance_profile_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_instance_profile_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_instance_profile_tags("test-instance_profile_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instance_profiles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_instance_profiles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_instance_profiles(path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_instance_profiles_for_role_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_instance_profiles_for_role
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_instance_profiles_for_role("test-role_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_mfa_device_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_mfa_device_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_mfa_device_tags("test-serial_number", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_mfa_devices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_mfa_devices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_mfa_devices(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_open_id_connect_provider_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_open_id_connect_provider_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_open_id_connect_provider_tags("test-open_id_connect_provider_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_policies_granting_service_access_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_policies_granting_service_access
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_policies_granting_service_access("test-arn", "test-service_namespaces", marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_policy_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_policy_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_policy_tags("test-policy_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_policy_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_policy_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_policy_versions("test-policy_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_role_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_role_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_role_policies("test-role_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_role_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_role_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_role_tags("test-role_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_saml_provider_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_saml_provider_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_saml_provider_tags("test-saml_provider_arn", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_server_certificate_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_server_certificate_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_server_certificate_tags("test-server_certificate_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_server_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_server_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_server_certificates(path_prefix="test-path_prefix", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_service_specific_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_service_specific_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_service_specific_credentials(user_name="test-user_name", service_name="test-service_name", all_users="test-all_users", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_signing_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_signing_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_signing_certificates(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_ssh_public_keys_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_ssh_public_keys
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_ssh_public_keys(user_name="test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_user_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_user_policies("test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_user_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_user_tags("test-user_name", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_virtual_mfa_devices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import list_virtual_mfa_devices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await list_virtual_mfa_devices(assignment_status="test-assignment_status", marker="test-marker", max_items=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import reset_service_specific_credential
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await reset_service_specific_credential("test-service_specific_credential_id", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_simulate_custom_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import simulate_custom_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await simulate_custom_policy("test-policy_input_list", "test-action_names", permissions_boundary_policy_input_list="test-permissions_boundary_policy_input_list", resource_arns="test-resource_arns", resource_policy="{}", resource_owner="test-resource_owner", caller_arn="test-caller_arn", context_entries={}, resource_handling_option="test-resource_handling_option", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_simulate_principal_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import simulate_principal_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await simulate_principal_policy("test-policy_source_arn", "test-action_names", policy_input_list="test-policy_input_list", permissions_boundary_policy_input_list="test-permissions_boundary_policy_input_list", resource_arns="test-resource_arns", resource_policy="{}", resource_owner="test-resource_owner", caller_arn="test-caller_arn", context_entries={}, resource_handling_option="test-resource_handling_option", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_access_key_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_access_key
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_access_key("test-access_key_id", "test-status", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_account_password_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_account_password_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_account_password_policy(minimum_password_length="test-minimum_password_length", require_symbols=True, require_numbers=True, require_uppercase_characters=True, require_lowercase_characters=True, allow_users_to_change_password=True, max_password_age=1, password_reuse_prevention="test-password_reuse_prevention", hard_expiry="test-hard_expiry", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_group("test-group_name", new_path="test-new_path", new_group_name="test-new_group_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_login_profile_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_login_profile
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_login_profile("test-user_name", password="test-password", password_reset_required="test-password_reset_required", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_role_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_role
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_role("test-role_name", description="test-description", max_session_duration=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_saml_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_saml_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_saml_provider("test-saml_provider_arn", saml_metadata_document="test-saml_metadata_document", assertion_encryption_mode="test-assertion_encryption_mode", add_private_key="test-add_private_key", remove_private_key="test-remove_private_key", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_server_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_server_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_server_certificate("test-server_certificate_name", new_path="test-new_path", new_server_certificate_name="test-new_server_certificate_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_service_specific_credential_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_service_specific_credential
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_service_specific_credential("test-service_specific_credential_id", "test-status", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_signing_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_signing_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_signing_certificate("test-certificate_id", "test-status", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import update_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await update_user("test-user_name", new_path="test-new_path", new_user_name="test-new_user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_upload_server_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import upload_server_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await upload_server_certificate("test-server_certificate_name", "test-certificate_body", "test-private_key", path="test-path", certificate_chain="test-certificate_chain", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_upload_signing_certificate_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.iam import upload_signing_certificate
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.iam.async_client", lambda *a, **kw: mock_client)
    await upload_signing_certificate("test-certificate_body", user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
