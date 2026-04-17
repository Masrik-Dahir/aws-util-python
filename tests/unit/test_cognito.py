"""Tests for aws_util.cognito module."""
from __future__ import annotations

import pytest
import boto3
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.cognito as cognito_mod
from aws_util.cognito import (
    CognitoUser,
    CognitoUserPool,
    AuthResult,
    admin_create_user,
    admin_get_user,
    admin_delete_user,
    admin_set_user_password,
    admin_add_user_to_group,
    admin_remove_user_from_group,
    list_users,
    admin_initiate_auth,
    list_user_pools,
    get_or_create_user,
    bulk_create_users,
    reset_user_password,
    add_custom_attributes,
    admin_confirm_sign_up,
    admin_delete_user_attributes,
    admin_disable_provider_for_user,
    admin_disable_user,
    admin_enable_user,
    admin_forget_device,
    admin_get_device,
    admin_link_provider_for_user,
    admin_list_devices,
    admin_list_groups_for_user,
    admin_list_user_auth_events,
    admin_reset_user_password,
    admin_respond_to_auth_challenge,
    admin_set_user_mfa_preference,
    admin_set_user_settings,
    admin_update_auth_event_feedback,
    admin_update_device_status,
    admin_update_user_attributes,
    admin_user_global_sign_out,
    associate_software_token,
    change_password,
    complete_web_authn_registration,
    confirm_device,
    confirm_forgot_password,
    confirm_sign_up,
    create_group,
    create_identity_provider,
    create_managed_login_branding,
    create_resource_server,
    create_terms,
    create_user_import_job,
    create_user_pool,
    create_user_pool_client,
    create_user_pool_domain,
    delete_group,
    delete_identity_provider,
    delete_managed_login_branding,
    delete_resource_server,
    delete_terms,
    delete_user,
    delete_user_attributes,
    delete_user_pool,
    delete_user_pool_client,
    delete_user_pool_domain,
    delete_web_authn_credential,
    describe_identity_provider,
    describe_managed_login_branding,
    describe_managed_login_branding_by_client,
    describe_resource_server,
    describe_risk_configuration,
    describe_terms,
    describe_user_import_job,
    describe_user_pool,
    describe_user_pool_client,
    describe_user_pool_domain,
    forget_device,
    forgot_password,
    get_csv_header,
    get_device,
    get_group,
    get_identity_provider_by_identifier,
    get_log_delivery_configuration,
    get_signing_certificate,
    get_tokens_from_refresh_token,
    get_ui_customization,
    get_user,
    get_user_attribute_verification_code,
    get_user_auth_factors,
    get_user_pool_mfa_config,
    global_sign_out,
    initiate_auth,
    list_devices,
    list_groups,
    list_identity_providers,
    list_resource_servers,
    list_tags_for_resource,
    list_terms,
    list_user_import_jobs,
    list_user_pool_clients,
    list_users_in_group,
    list_web_authn_credentials,
    resend_confirmation_code,
    respond_to_auth_challenge,
    revoke_token,
    set_log_delivery_configuration,
    set_risk_configuration,
    set_ui_customization,
    set_user_mfa_preference,
    set_user_pool_mfa_config,
    set_user_settings,
    sign_up,
    start_user_import_job,
    start_web_authn_registration,
    stop_user_import_job,
    tag_resource,
    untag_resource,
    update_auth_event_feedback,
    update_device_status,
    update_group,
    update_identity_provider,
    update_managed_login_branding,
    update_resource_server,
    update_terms,
    update_user_attributes,
    update_user_pool,
    update_user_pool_client,
    update_user_pool_domain,
    verify_software_token,
    verify_user_attribute,
)

REGION = "us-east-1"
USERNAME = "testuser"
PASSWORD = "TestPass123!"


@pytest.fixture
def user_pool():
    client = boto3.client("cognito-idp", region_name=REGION)
    resp = client.create_user_pool(PoolName="TestPool")
    pool_id = resp["UserPool"]["Id"]
    return pool_id


@pytest.fixture
def user_pool_with_client(user_pool):
    client = boto3.client("cognito-idp", region_name=REGION)
    resp = client.create_user_pool_client(
        UserPoolId=user_pool,
        ClientName="TestClient",
        ExplicitAuthFlows=["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"],
    )
    client_id = resp["UserPoolClient"]["ClientId"]
    return user_pool, client_id


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

def test_cognito_user_model():
    user = CognitoUser(username=USERNAME, user_status="CONFIRMED")
    assert user.username == USERNAME
    assert user.enabled is True
    assert user.attributes == {}


def test_cognito_user_pool_model():
    pool = CognitoUserPool(pool_id="us-east-1_abc", pool_name="TestPool")
    assert pool.pool_name == "TestPool"


def test_auth_result_model():
    result = AuthResult(access_token="token123", expires_in=3600)
    assert result.access_token == "token123"


# ---------------------------------------------------------------------------
# admin_create_user
# ---------------------------------------------------------------------------

def test_admin_create_user_success(user_pool):
    user = admin_create_user(
        user_pool,
        USERNAME,
        temp_password=PASSWORD,
        attributes={"email": "test@example.com"},
        suppress_welcome_email=True,
        region_name=REGION,
    )
    assert isinstance(user, CognitoUser)
    assert user.username == USERNAME


def test_admin_create_user_no_password(user_pool):
    user = admin_create_user(user_pool, "nopass_user", suppress_welcome_email=True, region_name=REGION)
    assert user.username == "nopass_user"


def test_admin_create_user_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_create_user.side_effect = ClientError(
        {"Error": {"Code": "UsernameExistsException", "Message": "exists"}}, "AdminCreateUser"
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create Cognito user"):
        admin_create_user("pool-id", "existing-user", region_name=REGION)


# ---------------------------------------------------------------------------
# admin_get_user
# ---------------------------------------------------------------------------

def test_admin_get_user_found(user_pool):
    admin_create_user(user_pool, USERNAME, suppress_welcome_email=True, region_name=REGION)
    user = admin_get_user(user_pool, USERNAME, region_name=REGION)
    assert user is not None
    assert user.username == USERNAME


def test_admin_get_user_not_found(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_get_user.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "not found"}}, "AdminGetUser"
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    result = admin_get_user("pool-id", "nobody", region_name=REGION)
    assert result is None


def test_admin_get_user_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_get_user.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "AdminGetUser"
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="admin_get_user failed"):
        admin_get_user("pool-id", "user", region_name=REGION)


# ---------------------------------------------------------------------------
# admin_delete_user
# ---------------------------------------------------------------------------

def test_admin_delete_user_success(user_pool):
    admin_create_user(user_pool, USERNAME, suppress_welcome_email=True, region_name=REGION)
    admin_delete_user(user_pool, USERNAME, region_name=REGION)
    # Verify deleted
    result = admin_get_user(user_pool, USERNAME, region_name=REGION)
    assert result is None


def test_admin_delete_user_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_delete_user.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "not found"}}, "AdminDeleteUser"
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete Cognito user"):
        admin_delete_user("pool-id", "nobody", region_name=REGION)


# ---------------------------------------------------------------------------
# admin_set_user_password
# ---------------------------------------------------------------------------

def test_admin_set_user_password_success(user_pool):
    admin_create_user(user_pool, USERNAME, suppress_welcome_email=True, region_name=REGION)
    admin_set_user_password(user_pool, USERNAME, PASSWORD, permanent=True, region_name=REGION)


def test_admin_set_user_password_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_set_user_password.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "not found"}},
        "AdminSetUserPassword",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set password"):
        admin_set_user_password("pool-id", "nobody", "pass", region_name=REGION)


# ---------------------------------------------------------------------------
# admin_add_user_to_group / admin_remove_user_from_group
# ---------------------------------------------------------------------------

def test_admin_add_and_remove_user_from_group(user_pool):
    client = boto3.client("cognito-idp", region_name=REGION)
    client.create_group(UserPoolId=user_pool, GroupName="admins")
    admin_create_user(user_pool, USERNAME, suppress_welcome_email=True, region_name=REGION)
    admin_add_user_to_group(user_pool, USERNAME, "admins", region_name=REGION)
    admin_remove_user_from_group(user_pool, USERNAME, "admins", region_name=REGION)


def test_admin_add_user_to_group_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_add_user_to_group.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "group not found"}},
        "AdminAddUserToGroup",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add"):
        admin_add_user_to_group("pool-id", "user", "nonexistent-group", region_name=REGION)


def test_admin_remove_user_from_group_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_remove_user_from_group.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "group not found"}},
        "AdminRemoveUserFromGroup",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove"):
        admin_remove_user_from_group("pool-id", "user", "nonexistent-group", region_name=REGION)


# ---------------------------------------------------------------------------
# list_users
# ---------------------------------------------------------------------------

def test_list_users_returns_list(user_pool):
    admin_create_user(user_pool, USERNAME, suppress_welcome_email=True, region_name=REGION)
    result = list_users(user_pool, region_name=REGION)
    assert isinstance(result, list)
    assert any(u.username == USERNAME for u in result)


def test_list_users_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "pool not found"}}, "ListUsers"
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_users failed"):
        list_users("nonexistent-pool", region_name=REGION)


# ---------------------------------------------------------------------------
# list_user_pools
# ---------------------------------------------------------------------------

def test_list_user_pools_returns_list(user_pool):
    result = list_user_pools(region_name=REGION)
    assert isinstance(result, list)
    assert any(p.pool_id == user_pool for p in result)


def test_list_user_pools_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_paginator.side_effect = ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "denied"}}, "ListUserPools"
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="list_user_pools failed"):
        list_user_pools(region_name=REGION)


# ---------------------------------------------------------------------------
# admin_initiate_auth
# ---------------------------------------------------------------------------

def test_admin_initiate_auth_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_initiate_auth.side_effect = ClientError(
        {"Error": {"Code": "NotAuthorizedException", "Message": "bad password"}},
        "AdminInitiateAuth",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="admin_initiate_auth failed"):
        admin_initiate_auth("pool-id", "client-id", "user", "wrong-pass", region_name=REGION)


def test_admin_initiate_auth_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_initiate_auth.return_value = {
        "AuthenticationResult": {
            "AccessToken": "access123",
            "IdToken": "id123",
            "RefreshToken": "refresh123",
            "TokenType": "Bearer",
            "ExpiresIn": 3600,
        }
    }
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    result = admin_initiate_auth("pool-id", "client-id", "user", "pass", region_name=REGION)
    assert isinstance(result, AuthResult)
    assert result.access_token == "access123"


# ---------------------------------------------------------------------------
# get_or_create_user
# ---------------------------------------------------------------------------

def test_get_or_create_user_creates_new(user_pool):
    user, created = get_or_create_user(
        user_pool, "new_user", temp_password=PASSWORD, region_name=REGION
    )
    assert created is True
    assert user.username == "new_user"


def test_get_or_create_user_returns_existing(user_pool):
    admin_create_user(user_pool, USERNAME, suppress_welcome_email=True, region_name=REGION)
    user, created = get_or_create_user(user_pool, USERNAME, region_name=REGION)
    assert created is False
    assert user.username == USERNAME


# ---------------------------------------------------------------------------
# bulk_create_users
# ---------------------------------------------------------------------------

def test_bulk_create_users(user_pool):
    users_def = [
        {"username": "bulk_user_1", "suppress_welcome_email": True},
        {"username": "bulk_user_2", "suppress_welcome_email": True},
    ]
    result = bulk_create_users(user_pool, users_def, region_name=REGION)
    assert len(result) == 2
    names = {u.username for u in result}
    assert "bulk_user_1" in names
    assert "bulk_user_2" in names


# ---------------------------------------------------------------------------
# reset_user_password
# ---------------------------------------------------------------------------

def test_reset_user_password_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_reset_user_password.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    reset_user_password("pool-id", USERNAME, region_name=REGION)
    mock_client.admin_reset_user_password.assert_called_once()


def test_reset_user_password_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_reset_user_password.side_effect = ClientError(
        {"Error": {"Code": "UserNotFoundException", "Message": "not found"}},
        "AdminResetUserPassword",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="reset_user_password failed"):
        reset_user_password("pool-id", "nobody", region_name=REGION)


def test_list_users_with_filter_and_attributes(monkeypatch):
    """Covers filter_str and attributes_to_get branches in list_users (lines 266, 268)."""
    import aws_util.cognito as cognito_mod

    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [{"Users": []}]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    result = list_users(
        "pool-id",
        filter_str='username = "testuser"',
        attributes_to_get=["email"],
        region_name=REGION,
    )
    assert result == []
    call_kwargs = mock_paginator.paginate.call_args[1]
    assert call_kwargs.get("Filter") == 'username = "testuser"'
    assert call_kwargs.get("AttributesToGet") == ["email"]


def test_add_custom_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_custom_attributes.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    add_custom_attributes("test-user_pool_id", [], region_name=REGION)
    mock_client.add_custom_attributes.assert_called_once()


def test_add_custom_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_custom_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_custom_attributes",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add custom attributes"):
        add_custom_attributes("test-user_pool_id", [], region_name=REGION)


def test_admin_confirm_sign_up(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_confirm_sign_up.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_confirm_sign_up("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_confirm_sign_up.assert_called_once()


def test_admin_confirm_sign_up_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_confirm_sign_up.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_confirm_sign_up",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin confirm sign up"):
        admin_confirm_sign_up("test-user_pool_id", "test-username", region_name=REGION)


def test_admin_delete_user_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_delete_user_attributes.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_delete_user_attributes("test-user_pool_id", "test-username", [], region_name=REGION)
    mock_client.admin_delete_user_attributes.assert_called_once()


def test_admin_delete_user_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_delete_user_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_delete_user_attributes",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin delete user attributes"):
        admin_delete_user_attributes("test-user_pool_id", "test-username", [], region_name=REGION)


def test_admin_disable_provider_for_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_disable_provider_for_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_disable_provider_for_user("test-user_pool_id", {}, region_name=REGION)
    mock_client.admin_disable_provider_for_user.assert_called_once()


def test_admin_disable_provider_for_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_disable_provider_for_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_disable_provider_for_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin disable provider for user"):
        admin_disable_provider_for_user("test-user_pool_id", {}, region_name=REGION)


def test_admin_disable_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_disable_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_disable_user("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_disable_user.assert_called_once()


def test_admin_disable_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_disable_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_disable_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin disable user"):
        admin_disable_user("test-user_pool_id", "test-username", region_name=REGION)


def test_admin_enable_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_enable_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_enable_user("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_enable_user.assert_called_once()


def test_admin_enable_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_enable_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_enable_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin enable user"):
        admin_enable_user("test-user_pool_id", "test-username", region_name=REGION)


def test_admin_forget_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_forget_device.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_forget_device("test-user_pool_id", "test-username", "test-device_key", region_name=REGION)
    mock_client.admin_forget_device.assert_called_once()


def test_admin_forget_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_forget_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_forget_device",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin forget device"):
        admin_forget_device("test-user_pool_id", "test-username", "test-device_key", region_name=REGION)


def test_admin_get_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_get_device.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_get_device("test-device_key", "test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_get_device.assert_called_once()


def test_admin_get_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_get_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_get_device",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin get device"):
        admin_get_device("test-device_key", "test-user_pool_id", "test-username", region_name=REGION)


def test_admin_link_provider_for_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_link_provider_for_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_link_provider_for_user("test-user_pool_id", {}, {}, region_name=REGION)
    mock_client.admin_link_provider_for_user.assert_called_once()


def test_admin_link_provider_for_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_link_provider_for_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_link_provider_for_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin link provider for user"):
        admin_link_provider_for_user("test-user_pool_id", {}, {}, region_name=REGION)


def test_admin_list_devices(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_list_devices.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_list_devices("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_list_devices.assert_called_once()


def test_admin_list_devices_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_list_devices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_list_devices",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin list devices"):
        admin_list_devices("test-user_pool_id", "test-username", region_name=REGION)


def test_admin_list_groups_for_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_list_groups_for_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_list_groups_for_user("test-username", "test-user_pool_id", region_name=REGION)
    mock_client.admin_list_groups_for_user.assert_called_once()


def test_admin_list_groups_for_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_list_groups_for_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_list_groups_for_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin list groups for user"):
        admin_list_groups_for_user("test-username", "test-user_pool_id", region_name=REGION)


def test_admin_list_user_auth_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_list_user_auth_events.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_list_user_auth_events("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_list_user_auth_events.assert_called_once()


def test_admin_list_user_auth_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_list_user_auth_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_list_user_auth_events",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin list user auth events"):
        admin_list_user_auth_events("test-user_pool_id", "test-username", region_name=REGION)


def test_admin_reset_user_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_reset_user_password.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_reset_user_password("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_reset_user_password.assert_called_once()


def test_admin_reset_user_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_reset_user_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_reset_user_password",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin reset user password"):
        admin_reset_user_password("test-user_pool_id", "test-username", region_name=REGION)


def test_admin_respond_to_auth_challenge(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_respond_to_auth_challenge.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", region_name=REGION)
    mock_client.admin_respond_to_auth_challenge.assert_called_once()


def test_admin_respond_to_auth_challenge_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_respond_to_auth_challenge.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_respond_to_auth_challenge",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin respond to auth challenge"):
        admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", region_name=REGION)


def test_admin_set_user_mfa_preference(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_set_user_mfa_preference.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_set_user_mfa_preference("test-username", "test-user_pool_id", region_name=REGION)
    mock_client.admin_set_user_mfa_preference.assert_called_once()


def test_admin_set_user_mfa_preference_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_set_user_mfa_preference.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_set_user_mfa_preference",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin set user mfa preference"):
        admin_set_user_mfa_preference("test-username", "test-user_pool_id", region_name=REGION)


def test_admin_set_user_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_set_user_settings.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_set_user_settings("test-user_pool_id", "test-username", [], region_name=REGION)
    mock_client.admin_set_user_settings.assert_called_once()


def test_admin_set_user_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_set_user_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_set_user_settings",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin set user settings"):
        admin_set_user_settings("test-user_pool_id", "test-username", [], region_name=REGION)


def test_admin_update_auth_event_feedback(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_update_auth_event_feedback.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_value", region_name=REGION)
    mock_client.admin_update_auth_event_feedback.assert_called_once()


def test_admin_update_auth_event_feedback_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_update_auth_event_feedback.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_update_auth_event_feedback",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin update auth event feedback"):
        admin_update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_value", region_name=REGION)


def test_admin_update_device_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_update_device_status.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", region_name=REGION)
    mock_client.admin_update_device_status.assert_called_once()


def test_admin_update_device_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_update_device_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_update_device_status",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin update device status"):
        admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", region_name=REGION)


def test_admin_update_user_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_update_user_attributes.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_update_user_attributes("test-user_pool_id", "test-username", [], region_name=REGION)
    mock_client.admin_update_user_attributes.assert_called_once()


def test_admin_update_user_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_update_user_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_update_user_attributes",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin update user attributes"):
        admin_update_user_attributes("test-user_pool_id", "test-username", [], region_name=REGION)


def test_admin_user_global_sign_out(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_user_global_sign_out.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    admin_user_global_sign_out("test-user_pool_id", "test-username", region_name=REGION)
    mock_client.admin_user_global_sign_out.assert_called_once()


def test_admin_user_global_sign_out_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.admin_user_global_sign_out.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "admin_user_global_sign_out",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to admin user global sign out"):
        admin_user_global_sign_out("test-user_pool_id", "test-username", region_name=REGION)


def test_associate_software_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_software_token.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    associate_software_token(region_name=REGION)
    mock_client.associate_software_token.assert_called_once()


def test_associate_software_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_software_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_software_token",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate software token"):
        associate_software_token(region_name=REGION)


def test_change_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_password.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    change_password("test-proposed_password", "test-access_token", region_name=REGION)
    mock_client.change_password.assert_called_once()


def test_change_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.change_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "change_password",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to change password"):
        change_password("test-proposed_password", "test-access_token", region_name=REGION)


def test_complete_web_authn_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_web_authn_registration.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    complete_web_authn_registration("test-access_token", {}, region_name=REGION)
    mock_client.complete_web_authn_registration.assert_called_once()


def test_complete_web_authn_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_web_authn_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "complete_web_authn_registration",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to complete web authn registration"):
        complete_web_authn_registration("test-access_token", {}, region_name=REGION)


def test_confirm_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_device.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    confirm_device("test-access_token", "test-device_key", region_name=REGION)
    mock_client.confirm_device.assert_called_once()


def test_confirm_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "confirm_device",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to confirm device"):
        confirm_device("test-access_token", "test-device_key", region_name=REGION)


def test_confirm_forgot_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_forgot_password.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    confirm_forgot_password("test-client_id", "test-username", "test-confirmation_code", "test-password", region_name=REGION)
    mock_client.confirm_forgot_password.assert_called_once()


def test_confirm_forgot_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_forgot_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "confirm_forgot_password",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to confirm forgot password"):
        confirm_forgot_password("test-client_id", "test-username", "test-confirmation_code", "test-password", region_name=REGION)


def test_confirm_sign_up(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_sign_up.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    confirm_sign_up("test-client_id", "test-username", "test-confirmation_code", region_name=REGION)
    mock_client.confirm_sign_up.assert_called_once()


def test_confirm_sign_up_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.confirm_sign_up.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "confirm_sign_up",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to confirm sign up"):
        confirm_sign_up("test-client_id", "test-username", "test-confirmation_code", region_name=REGION)


def test_create_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_group("test-group_name", "test-user_pool_id", region_name=REGION)
    mock_client.create_group.assert_called_once()


def test_create_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_group",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create group"):
        create_group("test-group_name", "test-user_pool_id", region_name=REGION)


def test_create_identity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_identity_provider.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", {}, region_name=REGION)
    mock_client.create_identity_provider.assert_called_once()


def test_create_identity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_identity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_identity_provider",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create identity provider"):
        create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", {}, region_name=REGION)


def test_create_managed_login_branding(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_managed_login_branding.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_managed_login_branding("test-user_pool_id", "test-client_id", region_name=REGION)
    mock_client.create_managed_login_branding.assert_called_once()


def test_create_managed_login_branding_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_managed_login_branding.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_managed_login_branding",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create managed login branding"):
        create_managed_login_branding("test-user_pool_id", "test-client_id", region_name=REGION)


def test_create_resource_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_server.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_resource_server("test-user_pool_id", "test-identifier", "test-name", region_name=REGION)
    mock_client.create_resource_server.assert_called_once()


def test_create_resource_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_resource_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_resource_server",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create resource server"):
        create_resource_server("test-user_pool_id", "test-identifier", "test-name", region_name=REGION)


def test_create_terms(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_terms.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", region_name=REGION)
    mock_client.create_terms.assert_called_once()


def test_create_terms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_terms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_terms",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create terms"):
        create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", region_name=REGION)


def test_create_user_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_import_job.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_user_import_job("test-job_name", "test-user_pool_id", "test-cloud_watch_logs_role_arn", region_name=REGION)
    mock_client.create_user_import_job.assert_called_once()


def test_create_user_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_import_job",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user import job"):
        create_user_import_job("test-job_name", "test-user_pool_id", "test-cloud_watch_logs_role_arn", region_name=REGION)


def test_create_user_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_pool.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_user_pool("test-pool_name", region_name=REGION)
    mock_client.create_user_pool.assert_called_once()


def test_create_user_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_pool",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user pool"):
        create_user_pool("test-pool_name", region_name=REGION)


def test_create_user_pool_client(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_pool_client.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_user_pool_client("test-user_pool_id", "test-client_name", region_name=REGION)
    mock_client.create_user_pool_client.assert_called_once()


def test_create_user_pool_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_pool_client.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_pool_client",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user pool client"):
        create_user_pool_client("test-user_pool_id", "test-client_name", region_name=REGION)


def test_create_user_pool_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_pool_domain.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    create_user_pool_domain("test-domain", "test-user_pool_id", region_name=REGION)
    mock_client.create_user_pool_domain.assert_called_once()


def test_create_user_pool_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_pool_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_pool_domain",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user pool domain"):
        create_user_pool_domain("test-domain", "test-user_pool_id", region_name=REGION)


def test_delete_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_group("test-group_name", "test-user_pool_id", region_name=REGION)
    mock_client.delete_group.assert_called_once()


def test_delete_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_group",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete group"):
        delete_group("test-group_name", "test-user_pool_id", region_name=REGION)


def test_delete_identity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity_provider.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_identity_provider("test-user_pool_id", "test-provider_name", region_name=REGION)
    mock_client.delete_identity_provider.assert_called_once()


def test_delete_identity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_identity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_identity_provider",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete identity provider"):
        delete_identity_provider("test-user_pool_id", "test-provider_name", region_name=REGION)


def test_delete_managed_login_branding(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_managed_login_branding.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_managed_login_branding("test-managed_login_branding_id", "test-user_pool_id", region_name=REGION)
    mock_client.delete_managed_login_branding.assert_called_once()


def test_delete_managed_login_branding_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_managed_login_branding.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_managed_login_branding",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete managed login branding"):
        delete_managed_login_branding("test-managed_login_branding_id", "test-user_pool_id", region_name=REGION)


def test_delete_resource_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_server.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_resource_server("test-user_pool_id", "test-identifier", region_name=REGION)
    mock_client.delete_resource_server.assert_called_once()


def test_delete_resource_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_server",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource server"):
        delete_resource_server("test-user_pool_id", "test-identifier", region_name=REGION)


def test_delete_terms(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_terms.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_terms("test-terms_id", "test-user_pool_id", region_name=REGION)
    mock_client.delete_terms.assert_called_once()


def test_delete_terms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_terms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_terms",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete terms"):
        delete_terms("test-terms_id", "test-user_pool_id", region_name=REGION)


def test_delete_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_user("test-access_token", region_name=REGION)
    mock_client.delete_user.assert_called_once()


def test_delete_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user"):
        delete_user("test-access_token", region_name=REGION)


def test_delete_user_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_attributes.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_user_attributes([], "test-access_token", region_name=REGION)
    mock_client.delete_user_attributes.assert_called_once()


def test_delete_user_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_attributes",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user attributes"):
        delete_user_attributes([], "test-access_token", region_name=REGION)


def test_delete_user_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_pool.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_user_pool("test-user_pool_id", region_name=REGION)
    mock_client.delete_user_pool.assert_called_once()


def test_delete_user_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_pool",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user pool"):
        delete_user_pool("test-user_pool_id", region_name=REGION)


def test_delete_user_pool_client(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_pool_client.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_user_pool_client("test-user_pool_id", "test-client_id", region_name=REGION)
    mock_client.delete_user_pool_client.assert_called_once()


def test_delete_user_pool_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_pool_client.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_pool_client",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user pool client"):
        delete_user_pool_client("test-user_pool_id", "test-client_id", region_name=REGION)


def test_delete_user_pool_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_pool_domain.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_user_pool_domain("test-domain", "test-user_pool_id", region_name=REGION)
    mock_client.delete_user_pool_domain.assert_called_once()


def test_delete_user_pool_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_pool_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_pool_domain",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user pool domain"):
        delete_user_pool_domain("test-domain", "test-user_pool_id", region_name=REGION)


def test_delete_web_authn_credential(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_web_authn_credential.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    delete_web_authn_credential("test-access_token", "test-credential_id", region_name=REGION)
    mock_client.delete_web_authn_credential.assert_called_once()


def test_delete_web_authn_credential_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_web_authn_credential.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_web_authn_credential",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete web authn credential"):
        delete_web_authn_credential("test-access_token", "test-credential_id", region_name=REGION)


def test_describe_identity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_identity_provider.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_identity_provider("test-user_pool_id", "test-provider_name", region_name=REGION)
    mock_client.describe_identity_provider.assert_called_once()


def test_describe_identity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_identity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_identity_provider",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe identity provider"):
        describe_identity_provider("test-user_pool_id", "test-provider_name", region_name=REGION)


def test_describe_managed_login_branding(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_managed_login_branding.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", region_name=REGION)
    mock_client.describe_managed_login_branding.assert_called_once()


def test_describe_managed_login_branding_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_managed_login_branding.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_managed_login_branding",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe managed login branding"):
        describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", region_name=REGION)


def test_describe_managed_login_branding_by_client(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_managed_login_branding_by_client.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", region_name=REGION)
    mock_client.describe_managed_login_branding_by_client.assert_called_once()


def test_describe_managed_login_branding_by_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_managed_login_branding_by_client.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_managed_login_branding_by_client",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe managed login branding by client"):
        describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", region_name=REGION)


def test_describe_resource_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_server.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_resource_server("test-user_pool_id", "test-identifier", region_name=REGION)
    mock_client.describe_resource_server.assert_called_once()


def test_describe_resource_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resource_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_resource_server",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe resource server"):
        describe_resource_server("test-user_pool_id", "test-identifier", region_name=REGION)


def test_describe_risk_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_risk_configuration.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_risk_configuration("test-user_pool_id", region_name=REGION)
    mock_client.describe_risk_configuration.assert_called_once()


def test_describe_risk_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_risk_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_risk_configuration",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe risk configuration"):
        describe_risk_configuration("test-user_pool_id", region_name=REGION)


def test_describe_terms(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_terms.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_terms("test-terms_id", "test-user_pool_id", region_name=REGION)
    mock_client.describe_terms.assert_called_once()


def test_describe_terms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_terms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_terms",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe terms"):
        describe_terms("test-terms_id", "test-user_pool_id", region_name=REGION)


def test_describe_user_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_import_job.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_user_import_job("test-user_pool_id", "test-job_id", region_name=REGION)
    mock_client.describe_user_import_job.assert_called_once()


def test_describe_user_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_import_job",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user import job"):
        describe_user_import_job("test-user_pool_id", "test-job_id", region_name=REGION)


def test_describe_user_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_pool.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_user_pool("test-user_pool_id", region_name=REGION)
    mock_client.describe_user_pool.assert_called_once()


def test_describe_user_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_pool",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user pool"):
        describe_user_pool("test-user_pool_id", region_name=REGION)


def test_describe_user_pool_client(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_pool_client.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_user_pool_client("test-user_pool_id", "test-client_id", region_name=REGION)
    mock_client.describe_user_pool_client.assert_called_once()


def test_describe_user_pool_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_pool_client.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_pool_client",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user pool client"):
        describe_user_pool_client("test-user_pool_id", "test-client_id", region_name=REGION)


def test_describe_user_pool_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_pool_domain.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    describe_user_pool_domain("test-domain", region_name=REGION)
    mock_client.describe_user_pool_domain.assert_called_once()


def test_describe_user_pool_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_pool_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_pool_domain",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user pool domain"):
        describe_user_pool_domain("test-domain", region_name=REGION)


def test_forget_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.forget_device.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    forget_device("test-device_key", region_name=REGION)
    mock_client.forget_device.assert_called_once()


def test_forget_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.forget_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "forget_device",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to forget device"):
        forget_device("test-device_key", region_name=REGION)


def test_forgot_password(monkeypatch):
    mock_client = MagicMock()
    mock_client.forgot_password.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    forgot_password("test-client_id", "test-username", region_name=REGION)
    mock_client.forgot_password.assert_called_once()


def test_forgot_password_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.forgot_password.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "forgot_password",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to forgot password"):
        forgot_password("test-client_id", "test-username", region_name=REGION)


def test_get_csv_header(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_csv_header.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_csv_header("test-user_pool_id", region_name=REGION)
    mock_client.get_csv_header.assert_called_once()


def test_get_csv_header_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_csv_header.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_csv_header",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get csv header"):
        get_csv_header("test-user_pool_id", region_name=REGION)


def test_get_device(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_device.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_device("test-device_key", region_name=REGION)
    mock_client.get_device.assert_called_once()


def test_get_device_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_device.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_device",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get device"):
        get_device("test-device_key", region_name=REGION)


def test_get_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_group.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_group("test-group_name", "test-user_pool_id", region_name=REGION)
    mock_client.get_group.assert_called_once()


def test_get_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_group",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get group"):
        get_group("test-group_name", "test-user_pool_id", region_name=REGION)


def test_get_identity_provider_by_identifier(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_provider_by_identifier.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_identity_provider_by_identifier("test-user_pool_id", "test-idp_identifier", region_name=REGION)
    mock_client.get_identity_provider_by_identifier.assert_called_once()


def test_get_identity_provider_by_identifier_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_provider_by_identifier.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_provider_by_identifier",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity provider by identifier"):
        get_identity_provider_by_identifier("test-user_pool_id", "test-idp_identifier", region_name=REGION)


def test_get_log_delivery_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_log_delivery_configuration.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_log_delivery_configuration("test-user_pool_id", region_name=REGION)
    mock_client.get_log_delivery_configuration.assert_called_once()


def test_get_log_delivery_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_log_delivery_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_log_delivery_configuration",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get log delivery configuration"):
        get_log_delivery_configuration("test-user_pool_id", region_name=REGION)


def test_get_signing_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_signing_certificate.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_signing_certificate("test-user_pool_id", region_name=REGION)
    mock_client.get_signing_certificate.assert_called_once()


def test_get_signing_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_signing_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_signing_certificate",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get signing certificate"):
        get_signing_certificate("test-user_pool_id", region_name=REGION)


def test_get_tokens_from_refresh_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tokens_from_refresh_token.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_tokens_from_refresh_token("test-refresh_token", "test-client_id", region_name=REGION)
    mock_client.get_tokens_from_refresh_token.assert_called_once()


def test_get_tokens_from_refresh_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_tokens_from_refresh_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_tokens_from_refresh_token",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get tokens from refresh token"):
        get_tokens_from_refresh_token("test-refresh_token", "test-client_id", region_name=REGION)


def test_get_ui_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ui_customization.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_ui_customization("test-user_pool_id", region_name=REGION)
    mock_client.get_ui_customization.assert_called_once()


def test_get_ui_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_ui_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_ui_customization",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get ui customization"):
        get_ui_customization("test-user_pool_id", region_name=REGION)


def test_get_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_user("test-access_token", region_name=REGION)
    mock_client.get_user.assert_called_once()


def test_get_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user"):
        get_user("test-access_token", region_name=REGION)


def test_get_user_attribute_verification_code(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_attribute_verification_code.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_user_attribute_verification_code("test-access_token", "test-attribute_name", region_name=REGION)
    mock_client.get_user_attribute_verification_code.assert_called_once()


def test_get_user_attribute_verification_code_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_attribute_verification_code.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user_attribute_verification_code",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user attribute verification code"):
        get_user_attribute_verification_code("test-access_token", "test-attribute_name", region_name=REGION)


def test_get_user_auth_factors(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_auth_factors.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_user_auth_factors("test-access_token", region_name=REGION)
    mock_client.get_user_auth_factors.assert_called_once()


def test_get_user_auth_factors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_auth_factors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user_auth_factors",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user auth factors"):
        get_user_auth_factors("test-access_token", region_name=REGION)


def test_get_user_pool_mfa_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_pool_mfa_config.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    get_user_pool_mfa_config("test-user_pool_id", region_name=REGION)
    mock_client.get_user_pool_mfa_config.assert_called_once()


def test_get_user_pool_mfa_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_user_pool_mfa_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_user_pool_mfa_config",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get user pool mfa config"):
        get_user_pool_mfa_config("test-user_pool_id", region_name=REGION)


def test_global_sign_out(monkeypatch):
    mock_client = MagicMock()
    mock_client.global_sign_out.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    global_sign_out("test-access_token", region_name=REGION)
    mock_client.global_sign_out.assert_called_once()


def test_global_sign_out_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.global_sign_out.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "global_sign_out",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to global sign out"):
        global_sign_out("test-access_token", region_name=REGION)


def test_initiate_auth(monkeypatch):
    mock_client = MagicMock()
    mock_client.initiate_auth.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    initiate_auth("test-auth_flow", "test-client_id", region_name=REGION)
    mock_client.initiate_auth.assert_called_once()


def test_initiate_auth_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.initiate_auth.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "initiate_auth",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to initiate auth"):
        initiate_auth("test-auth_flow", "test-client_id", region_name=REGION)


def test_list_devices(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_devices.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_devices("test-access_token", region_name=REGION)
    mock_client.list_devices.assert_called_once()


def test_list_devices_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_devices.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_devices",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list devices"):
        list_devices("test-access_token", region_name=REGION)


def test_list_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_groups("test-user_pool_id", region_name=REGION)
    mock_client.list_groups.assert_called_once()


def test_list_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_groups",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list groups"):
        list_groups("test-user_pool_id", region_name=REGION)


def test_list_identity_providers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_providers.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_identity_providers("test-user_pool_id", region_name=REGION)
    mock_client.list_identity_providers.assert_called_once()


def test_list_identity_providers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_providers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_identity_providers",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list identity providers"):
        list_identity_providers("test-user_pool_id", region_name=REGION)


def test_list_resource_servers(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_servers.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_resource_servers("test-user_pool_id", region_name=REGION)
    mock_client.list_resource_servers.assert_called_once()


def test_list_resource_servers_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_resource_servers.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_resource_servers",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list resource servers"):
        list_resource_servers("test-user_pool_id", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_terms(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_terms.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_terms("test-user_pool_id", region_name=REGION)
    mock_client.list_terms.assert_called_once()


def test_list_terms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_terms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_terms",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list terms"):
        list_terms("test-user_pool_id", region_name=REGION)


def test_list_user_import_jobs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_import_jobs.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_user_import_jobs("test-user_pool_id", 1, region_name=REGION)
    mock_client.list_user_import_jobs.assert_called_once()


def test_list_user_import_jobs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_import_jobs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_import_jobs",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user import jobs"):
        list_user_import_jobs("test-user_pool_id", 1, region_name=REGION)


def test_list_user_pool_clients(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_pool_clients.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_user_pool_clients("test-user_pool_id", region_name=REGION)
    mock_client.list_user_pool_clients.assert_called_once()


def test_list_user_pool_clients_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_user_pool_clients.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_user_pool_clients",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list user pool clients"):
        list_user_pool_clients("test-user_pool_id", region_name=REGION)


def test_list_users_in_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_users_in_group.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_users_in_group("test-user_pool_id", "test-group_name", region_name=REGION)
    mock_client.list_users_in_group.assert_called_once()


def test_list_users_in_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_users_in_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_users_in_group",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list users in group"):
        list_users_in_group("test-user_pool_id", "test-group_name", region_name=REGION)


def test_list_web_authn_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_web_authn_credentials.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    list_web_authn_credentials("test-access_token", region_name=REGION)
    mock_client.list_web_authn_credentials.assert_called_once()


def test_list_web_authn_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_web_authn_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_web_authn_credentials",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list web authn credentials"):
        list_web_authn_credentials("test-access_token", region_name=REGION)


def test_resend_confirmation_code(monkeypatch):
    mock_client = MagicMock()
    mock_client.resend_confirmation_code.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    resend_confirmation_code("test-client_id", "test-username", region_name=REGION)
    mock_client.resend_confirmation_code.assert_called_once()


def test_resend_confirmation_code_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resend_confirmation_code.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resend_confirmation_code",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resend confirmation code"):
        resend_confirmation_code("test-client_id", "test-username", region_name=REGION)


def test_respond_to_auth_challenge(monkeypatch):
    mock_client = MagicMock()
    mock_client.respond_to_auth_challenge.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    respond_to_auth_challenge("test-client_id", "test-challenge_name", region_name=REGION)
    mock_client.respond_to_auth_challenge.assert_called_once()


def test_respond_to_auth_challenge_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.respond_to_auth_challenge.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "respond_to_auth_challenge",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to respond to auth challenge"):
        respond_to_auth_challenge("test-client_id", "test-challenge_name", region_name=REGION)


def test_revoke_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_token.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    revoke_token("test-token", "test-client_id", region_name=REGION)
    mock_client.revoke_token.assert_called_once()


def test_revoke_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_token",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke token"):
        revoke_token("test-token", "test-client_id", region_name=REGION)


def test_set_log_delivery_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_log_delivery_configuration.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    set_log_delivery_configuration("test-user_pool_id", [], region_name=REGION)
    mock_client.set_log_delivery_configuration.assert_called_once()


def test_set_log_delivery_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_log_delivery_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_log_delivery_configuration",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set log delivery configuration"):
        set_log_delivery_configuration("test-user_pool_id", [], region_name=REGION)


def test_set_risk_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_risk_configuration.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    set_risk_configuration("test-user_pool_id", region_name=REGION)
    mock_client.set_risk_configuration.assert_called_once()


def test_set_risk_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_risk_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_risk_configuration",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set risk configuration"):
        set_risk_configuration("test-user_pool_id", region_name=REGION)


def test_set_ui_customization(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_ui_customization.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    set_ui_customization("test-user_pool_id", region_name=REGION)
    mock_client.set_ui_customization.assert_called_once()


def test_set_ui_customization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_ui_customization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_ui_customization",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set ui customization"):
        set_ui_customization("test-user_pool_id", region_name=REGION)


def test_set_user_mfa_preference(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_user_mfa_preference.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    set_user_mfa_preference("test-access_token", region_name=REGION)
    mock_client.set_user_mfa_preference.assert_called_once()


def test_set_user_mfa_preference_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_user_mfa_preference.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_user_mfa_preference",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set user mfa preference"):
        set_user_mfa_preference("test-access_token", region_name=REGION)


def test_set_user_pool_mfa_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_user_pool_mfa_config.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    set_user_pool_mfa_config("test-user_pool_id", region_name=REGION)
    mock_client.set_user_pool_mfa_config.assert_called_once()


def test_set_user_pool_mfa_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_user_pool_mfa_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_user_pool_mfa_config",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set user pool mfa config"):
        set_user_pool_mfa_config("test-user_pool_id", region_name=REGION)


def test_set_user_settings(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_user_settings.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    set_user_settings("test-access_token", [], region_name=REGION)
    mock_client.set_user_settings.assert_called_once()


def test_set_user_settings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.set_user_settings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_user_settings",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to set user settings"):
        set_user_settings("test-access_token", [], region_name=REGION)


def test_sign_up(monkeypatch):
    mock_client = MagicMock()
    mock_client.sign_up.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    sign_up("test-client_id", "test-username", region_name=REGION)
    mock_client.sign_up.assert_called_once()


def test_sign_up_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.sign_up.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "sign_up",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to sign up"):
        sign_up("test-client_id", "test-username", region_name=REGION)


def test_start_user_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_user_import_job.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    start_user_import_job("test-user_pool_id", "test-job_id", region_name=REGION)
    mock_client.start_user_import_job.assert_called_once()


def test_start_user_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_user_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_user_import_job",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start user import job"):
        start_user_import_job("test-user_pool_id", "test-job_id", region_name=REGION)


def test_start_web_authn_registration(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_web_authn_registration.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    start_web_authn_registration("test-access_token", region_name=REGION)
    mock_client.start_web_authn_registration.assert_called_once()


def test_start_web_authn_registration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_web_authn_registration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_web_authn_registration",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start web authn registration"):
        start_web_authn_registration("test-access_token", region_name=REGION)


def test_stop_user_import_job(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_user_import_job.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    stop_user_import_job("test-user_pool_id", "test-job_id", region_name=REGION)
    mock_client.stop_user_import_job.assert_called_once()


def test_stop_user_import_job_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_user_import_job.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_user_import_job",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop user import job"):
        stop_user_import_job("test-user_pool_id", "test-job_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_auth_event_feedback(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_auth_event_feedback.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_token", "test-feedback_value", region_name=REGION)
    mock_client.update_auth_event_feedback.assert_called_once()


def test_update_auth_event_feedback_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_auth_event_feedback.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_auth_event_feedback",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update auth event feedback"):
        update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_token", "test-feedback_value", region_name=REGION)


def test_update_device_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_device_status.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_device_status("test-access_token", "test-device_key", region_name=REGION)
    mock_client.update_device_status.assert_called_once()


def test_update_device_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_device_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_device_status",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update device status"):
        update_device_status("test-access_token", "test-device_key", region_name=REGION)


def test_update_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_group.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_group("test-group_name", "test-user_pool_id", region_name=REGION)
    mock_client.update_group.assert_called_once()


def test_update_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_group",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update group"):
        update_group("test-group_name", "test-user_pool_id", region_name=REGION)


def test_update_identity_provider(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_identity_provider.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_identity_provider("test-user_pool_id", "test-provider_name", region_name=REGION)
    mock_client.update_identity_provider.assert_called_once()


def test_update_identity_provider_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_identity_provider.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_identity_provider",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update identity provider"):
        update_identity_provider("test-user_pool_id", "test-provider_name", region_name=REGION)


def test_update_managed_login_branding(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_managed_login_branding.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_managed_login_branding(region_name=REGION)
    mock_client.update_managed_login_branding.assert_called_once()


def test_update_managed_login_branding_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_managed_login_branding.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_managed_login_branding",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update managed login branding"):
        update_managed_login_branding(region_name=REGION)


def test_update_resource_server(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_server.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_resource_server("test-user_pool_id", "test-identifier", "test-name", region_name=REGION)
    mock_client.update_resource_server.assert_called_once()


def test_update_resource_server_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_resource_server.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_resource_server",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update resource server"):
        update_resource_server("test-user_pool_id", "test-identifier", "test-name", region_name=REGION)


def test_update_terms(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_terms.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_terms("test-terms_id", "test-user_pool_id", region_name=REGION)
    mock_client.update_terms.assert_called_once()


def test_update_terms_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_terms.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_terms",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update terms"):
        update_terms("test-terms_id", "test-user_pool_id", region_name=REGION)


def test_update_user_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_attributes.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_user_attributes([], "test-access_token", region_name=REGION)
    mock_client.update_user_attributes.assert_called_once()


def test_update_user_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_attributes",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user attributes"):
        update_user_attributes([], "test-access_token", region_name=REGION)


def test_update_user_pool(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_pool.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_user_pool("test-user_pool_id", region_name=REGION)
    mock_client.update_user_pool.assert_called_once()


def test_update_user_pool_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_pool.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_pool",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user pool"):
        update_user_pool("test-user_pool_id", region_name=REGION)


def test_update_user_pool_client(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_pool_client.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_user_pool_client("test-user_pool_id", "test-client_id", region_name=REGION)
    mock_client.update_user_pool_client.assert_called_once()


def test_update_user_pool_client_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_pool_client.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_pool_client",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user pool client"):
        update_user_pool_client("test-user_pool_id", "test-client_id", region_name=REGION)


def test_update_user_pool_domain(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_pool_domain.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    update_user_pool_domain("test-domain", "test-user_pool_id", region_name=REGION)
    mock_client.update_user_pool_domain.assert_called_once()


def test_update_user_pool_domain_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_user_pool_domain.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_user_pool_domain",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update user pool domain"):
        update_user_pool_domain("test-domain", "test-user_pool_id", region_name=REGION)


def test_verify_software_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_software_token.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    verify_software_token("test-user_code", region_name=REGION)
    mock_client.verify_software_token.assert_called_once()


def test_verify_software_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_software_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_software_token",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify software token"):
        verify_software_token("test-user_code", region_name=REGION)


def test_verify_user_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_user_attribute.return_value = {}
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    verify_user_attribute("test-access_token", "test-attribute_name", "test-code", region_name=REGION)
    mock_client.verify_user_attribute.assert_called_once()


def test_verify_user_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.verify_user_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "verify_user_attribute",
    )
    monkeypatch.setattr(cognito_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to verify user attribute"):
        verify_user_attribute("test-access_token", "test-attribute_name", "test-code", region_name=REGION)


def test_admin_confirm_sign_up_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_confirm_sign_up
    mock_client = MagicMock()
    mock_client.admin_confirm_sign_up.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_confirm_sign_up("test-user_pool_id", "test-username", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.admin_confirm_sign_up.assert_called_once()

def test_admin_list_devices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_list_devices
    mock_client = MagicMock()
    mock_client.admin_list_devices.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_list_devices("test-user_pool_id", "test-username", limit=1, pagination_token="test-pagination_token", region_name="us-east-1")
    mock_client.admin_list_devices.assert_called_once()

def test_admin_list_groups_for_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_list_groups_for_user
    mock_client = MagicMock()
    mock_client.admin_list_groups_for_user.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_list_groups_for_user("test-username", "test-user_pool_id", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.admin_list_groups_for_user.assert_called_once()

def test_admin_list_user_auth_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_list_user_auth_events
    mock_client = MagicMock()
    mock_client.admin_list_user_auth_events.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_list_user_auth_events("test-user_pool_id", "test-username", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.admin_list_user_auth_events.assert_called_once()

def test_admin_reset_user_password_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_reset_user_password
    mock_client = MagicMock()
    mock_client.admin_reset_user_password.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_reset_user_password("test-user_pool_id", "test-username", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.admin_reset_user_password.assert_called_once()

def test_admin_respond_to_auth_challenge_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_respond_to_auth_challenge
    mock_client = MagicMock()
    mock_client.admin_respond_to_auth_challenge.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", challenge_responses="test-challenge_responses", session="test-session", analytics_metadata="test-analytics_metadata", context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.admin_respond_to_auth_challenge.assert_called_once()

def test_admin_set_user_mfa_preference_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_set_user_mfa_preference
    mock_client = MagicMock()
    mock_client.admin_set_user_mfa_preference.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_set_user_mfa_preference("test-username", "test-user_pool_id", sms_mfa_settings={}, software_token_mfa_settings={}, email_mfa_settings={}, region_name="us-east-1")
    mock_client.admin_set_user_mfa_preference.assert_called_once()

def test_admin_update_device_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_update_device_status
    mock_client = MagicMock()
    mock_client.admin_update_device_status.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", device_remembered_status="test-device_remembered_status", region_name="us-east-1")
    mock_client.admin_update_device_status.assert_called_once()

def test_admin_update_user_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import admin_update_user_attributes
    mock_client = MagicMock()
    mock_client.admin_update_user_attributes.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    admin_update_user_attributes("test-user_pool_id", "test-username", "test-user_attributes", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.admin_update_user_attributes.assert_called_once()

def test_associate_software_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import associate_software_token
    mock_client = MagicMock()
    mock_client.associate_software_token.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    associate_software_token(access_token="test-access_token", session="test-session", region_name="us-east-1")
    mock_client.associate_software_token.assert_called_once()

def test_change_password_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import change_password
    mock_client = MagicMock()
    mock_client.change_password.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    change_password("test-proposed_password", "test-access_token", previous_password="test-previous_password", region_name="us-east-1")
    mock_client.change_password.assert_called_once()

def test_confirm_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import confirm_device
    mock_client = MagicMock()
    mock_client.confirm_device.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    confirm_device("test-access_token", "test-device_key", device_secret_verifier_config={}, device_name="test-device_name", region_name="us-east-1")
    mock_client.confirm_device.assert_called_once()

def test_confirm_forgot_password_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import confirm_forgot_password
    mock_client = MagicMock()
    mock_client.confirm_forgot_password.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    confirm_forgot_password("test-client_id", "test-username", True, "test-password", secret_hash="test-secret_hash", analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.confirm_forgot_password.assert_called_once()

def test_confirm_sign_up_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import confirm_sign_up
    mock_client = MagicMock()
    mock_client.confirm_sign_up.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    confirm_sign_up("test-client_id", "test-username", True, secret_hash="test-secret_hash", force_alias_creation=True, analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", session="test-session", region_name="us-east-1")
    mock_client.confirm_sign_up.assert_called_once()

def test_create_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_group
    mock_client = MagicMock()
    mock_client.create_group.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_group("test-group_name", "test-user_pool_id", description="test-description", role_arn="test-role_arn", precedence="test-precedence", region_name="us-east-1")
    mock_client.create_group.assert_called_once()

def test_create_identity_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_identity_provider
    mock_client = MagicMock()
    mock_client.create_identity_provider.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", "test-provider_details", attribute_mapping={}, idp_identifiers="test-idp_identifiers", region_name="us-east-1")
    mock_client.create_identity_provider.assert_called_once()

def test_create_managed_login_branding_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_managed_login_branding
    mock_client = MagicMock()
    mock_client.create_managed_login_branding.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_managed_login_branding("test-user_pool_id", "test-client_id", use_cognito_provided_values=True, settings={}, assets="test-assets", region_name="us-east-1")
    mock_client.create_managed_login_branding.assert_called_once()

def test_create_resource_server_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_resource_server
    mock_client = MagicMock()
    mock_client.create_resource_server.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_resource_server("test-user_pool_id", "test-identifier", "test-name", scopes="test-scopes", region_name="us-east-1")
    mock_client.create_resource_server.assert_called_once()

def test_create_terms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_terms
    mock_client = MagicMock()
    mock_client.create_terms.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", links="test-links", region_name="us-east-1")
    mock_client.create_terms.assert_called_once()

def test_create_user_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_user_pool
    mock_client = MagicMock()
    mock_client.create_user_pool.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_user_pool("test-pool_name", policies="test-policies", deletion_protection="test-deletion_protection", lambda_config={}, auto_verified_attributes=True, alias_attributes="test-alias_attributes", username_attributes="test-username_attributes", sms_verification_message="test-sms_verification_message", email_verification_message="test-email_verification_message", email_verification_subject="test-email_verification_subject", verification_message_template="test-verification_message_template", sms_authentication_message="test-sms_authentication_message", mfa_configuration={}, user_attribute_update_settings={}, device_configuration={}, email_configuration={}, sms_configuration={}, user_pool_tags=[{"Key": "k", "Value": "v"}], admin_create_user_config={}, schema="test-schema", user_pool_add_ons="test-user_pool_add_ons", username_configuration={}, account_recovery_setting=1, user_pool_tier="test-user_pool_tier", region_name="us-east-1")
    mock_client.create_user_pool.assert_called_once()

def test_create_user_pool_client_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_user_pool_client
    mock_client = MagicMock()
    mock_client.create_user_pool_client.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_user_pool_client("test-user_pool_id", "test-client_name", generate_secret="test-generate_secret", refresh_token_validity="test-refresh_token_validity", access_token_validity="test-access_token_validity", id_token_validity="test-id_token_validity", token_validity_units="test-token_validity_units", read_attributes="test-read_attributes", write_attributes="test-write_attributes", explicit_auth_flows="test-explicit_auth_flows", supported_identity_providers=1, callback_ur_ls="test-callback_ur_ls", logout_ur_ls="test-logout_ur_ls", default_redirect_uri="test-default_redirect_uri", allowed_o_auth_flows=True, allowed_o_auth_scopes=True, allowed_o_auth_flows_user_pool_client=True, analytics_configuration={}, prevent_user_existence_errors="test-prevent_user_existence_errors", enable_token_revocation=True, enable_propagate_additional_user_context_data=True, auth_session_validity="test-auth_session_validity", refresh_token_rotation="test-refresh_token_rotation", region_name="us-east-1")
    mock_client.create_user_pool_client.assert_called_once()

def test_create_user_pool_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import create_user_pool_domain
    mock_client = MagicMock()
    mock_client.create_user_pool_domain.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    create_user_pool_domain("test-domain", "test-user_pool_id", managed_login_version="test-managed_login_version", custom_domain_config={}, region_name="us-east-1")
    mock_client.create_user_pool_domain.assert_called_once()

def test_describe_managed_login_branding_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import describe_managed_login_branding
    mock_client = MagicMock()
    mock_client.describe_managed_login_branding.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", return_merged_resources="test-return_merged_resources", region_name="us-east-1")
    mock_client.describe_managed_login_branding.assert_called_once()

def test_describe_managed_login_branding_by_client_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import describe_managed_login_branding_by_client
    mock_client = MagicMock()
    mock_client.describe_managed_login_branding_by_client.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", return_merged_resources="test-return_merged_resources", region_name="us-east-1")
    mock_client.describe_managed_login_branding_by_client.assert_called_once()

def test_describe_risk_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import describe_risk_configuration
    mock_client = MagicMock()
    mock_client.describe_risk_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    describe_risk_configuration("test-user_pool_id", client_id="test-client_id", region_name="us-east-1")
    mock_client.describe_risk_configuration.assert_called_once()

def test_forget_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import forget_device
    mock_client = MagicMock()
    mock_client.forget_device.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    forget_device("test-device_key", access_token="test-access_token", region_name="us-east-1")
    mock_client.forget_device.assert_called_once()

def test_forgot_password_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import forgot_password
    mock_client = MagicMock()
    mock_client.forgot_password.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    forgot_password("test-client_id", "test-username", secret_hash="test-secret_hash", user_context_data={}, analytics_metadata="test-analytics_metadata", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.forgot_password.assert_called_once()

def test_get_device_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import get_device
    mock_client = MagicMock()
    mock_client.get_device.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    get_device("test-device_key", access_token="test-access_token", region_name="us-east-1")
    mock_client.get_device.assert_called_once()

def test_get_tokens_from_refresh_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import get_tokens_from_refresh_token
    mock_client = MagicMock()
    mock_client.get_tokens_from_refresh_token.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    get_tokens_from_refresh_token("test-refresh_token", "test-client_id", client_secret="test-client_secret", device_key="test-device_key", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.get_tokens_from_refresh_token.assert_called_once()

def test_get_ui_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import get_ui_customization
    mock_client = MagicMock()
    mock_client.get_ui_customization.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    get_ui_customization("test-user_pool_id", client_id="test-client_id", region_name="us-east-1")
    mock_client.get_ui_customization.assert_called_once()

def test_get_user_attribute_verification_code_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import get_user_attribute_verification_code
    mock_client = MagicMock()
    mock_client.get_user_attribute_verification_code.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    get_user_attribute_verification_code("test-access_token", "test-attribute_name", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.get_user_attribute_verification_code.assert_called_once()

def test_initiate_auth_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import initiate_auth
    mock_client = MagicMock()
    mock_client.initiate_auth.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    initiate_auth("test-auth_flow", "test-client_id", auth_parameters="test-auth_parameters", client_metadata="test-client_metadata", analytics_metadata="test-analytics_metadata", user_context_data={}, session="test-session", region_name="us-east-1")
    mock_client.initiate_auth.assert_called_once()

def test_list_devices_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_devices
    mock_client = MagicMock()
    mock_client.list_devices.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_devices("test-access_token", limit=1, pagination_token="test-pagination_token", region_name="us-east-1")
    mock_client.list_devices.assert_called_once()

def test_list_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_groups
    mock_client = MagicMock()
    mock_client.list_groups.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_groups("test-user_pool_id", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_groups.assert_called_once()

def test_list_identity_providers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_identity_providers
    mock_client = MagicMock()
    mock_client.list_identity_providers.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_identity_providers("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_identity_providers.assert_called_once()

def test_list_resource_servers_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_resource_servers
    mock_client = MagicMock()
    mock_client.list_resource_servers.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_resource_servers("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_resource_servers.assert_called_once()

def test_list_terms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_terms
    mock_client = MagicMock()
    mock_client.list_terms.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_terms("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_terms.assert_called_once()

def test_list_user_import_jobs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_user_import_jobs
    mock_client = MagicMock()
    mock_client.list_user_import_jobs.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_user_import_jobs("test-user_pool_id", 1, pagination_token="test-pagination_token", region_name="us-east-1")
    mock_client.list_user_import_jobs.assert_called_once()

def test_list_user_pool_clients_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_user_pool_clients
    mock_client = MagicMock()
    mock_client.list_user_pool_clients.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_user_pool_clients("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_user_pool_clients.assert_called_once()

def test_list_users_in_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_users_in_group
    mock_client = MagicMock()
    mock_client.list_users_in_group.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_users_in_group("test-user_pool_id", "test-group_name", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_users_in_group.assert_called_once()

def test_list_web_authn_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import list_web_authn_credentials
    mock_client = MagicMock()
    mock_client.list_web_authn_credentials.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    list_web_authn_credentials("test-access_token", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_web_authn_credentials.assert_called_once()

def test_resend_confirmation_code_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import resend_confirmation_code
    mock_client = MagicMock()
    mock_client.resend_confirmation_code.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    resend_confirmation_code("test-client_id", "test-username", secret_hash="test-secret_hash", user_context_data={}, analytics_metadata="test-analytics_metadata", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.resend_confirmation_code.assert_called_once()

def test_respond_to_auth_challenge_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import respond_to_auth_challenge
    mock_client = MagicMock()
    mock_client.respond_to_auth_challenge.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    respond_to_auth_challenge("test-client_id", "test-challenge_name", session="test-session", challenge_responses="test-challenge_responses", analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.respond_to_auth_challenge.assert_called_once()

def test_revoke_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import revoke_token
    mock_client = MagicMock()
    mock_client.revoke_token.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    revoke_token("test-token", "test-client_id", client_secret="test-client_secret", region_name="us-east-1")
    mock_client.revoke_token.assert_called_once()

def test_set_risk_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import set_risk_configuration
    mock_client = MagicMock()
    mock_client.set_risk_configuration.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    set_risk_configuration("test-user_pool_id", client_id="test-client_id", compromised_credentials_risk_configuration={}, account_takeover_risk_configuration=1, risk_exception_configuration={}, region_name="us-east-1")
    mock_client.set_risk_configuration.assert_called_once()

def test_set_ui_customization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import set_ui_customization
    mock_client = MagicMock()
    mock_client.set_ui_customization.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    set_ui_customization("test-user_pool_id", client_id="test-client_id", css="test-css", image_file="test-image_file", region_name="us-east-1")
    mock_client.set_ui_customization.assert_called_once()

def test_set_user_mfa_preference_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import set_user_mfa_preference
    mock_client = MagicMock()
    mock_client.set_user_mfa_preference.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    set_user_mfa_preference("test-access_token", sms_mfa_settings={}, software_token_mfa_settings={}, email_mfa_settings={}, region_name="us-east-1")
    mock_client.set_user_mfa_preference.assert_called_once()

def test_set_user_pool_mfa_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import set_user_pool_mfa_config
    mock_client = MagicMock()
    mock_client.set_user_pool_mfa_config.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    set_user_pool_mfa_config("test-user_pool_id", sms_mfa_configuration={}, software_token_mfa_configuration={}, email_mfa_configuration={}, mfa_configuration={}, web_authn_configuration={}, region_name="us-east-1")
    mock_client.set_user_pool_mfa_config.assert_called_once()

def test_sign_up_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import sign_up
    mock_client = MagicMock()
    mock_client.sign_up.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    sign_up("test-client_id", "test-username", secret_hash="test-secret_hash", password="test-password", user_attributes="test-user_attributes", validation_data="test-validation_data", analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.sign_up.assert_called_once()

def test_update_device_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_device_status
    mock_client = MagicMock()
    mock_client.update_device_status.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_device_status("test-access_token", "test-device_key", device_remembered_status="test-device_remembered_status", region_name="us-east-1")
    mock_client.update_device_status.assert_called_once()

def test_update_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_group
    mock_client = MagicMock()
    mock_client.update_group.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_group("test-group_name", "test-user_pool_id", description="test-description", role_arn="test-role_arn", precedence="test-precedence", region_name="us-east-1")
    mock_client.update_group.assert_called_once()

def test_update_identity_provider_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_identity_provider
    mock_client = MagicMock()
    mock_client.update_identity_provider.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_identity_provider("test-user_pool_id", "test-provider_name", provider_details="test-provider_details", attribute_mapping={}, idp_identifiers="test-idp_identifiers", region_name="us-east-1")
    mock_client.update_identity_provider.assert_called_once()

def test_update_managed_login_branding_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_managed_login_branding
    mock_client = MagicMock()
    mock_client.update_managed_login_branding.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_managed_login_branding(user_pool_id="test-user_pool_id", managed_login_branding_id="test-managed_login_branding_id", use_cognito_provided_values=True, settings={}, assets="test-assets", region_name="us-east-1")
    mock_client.update_managed_login_branding.assert_called_once()

def test_update_resource_server_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_resource_server
    mock_client = MagicMock()
    mock_client.update_resource_server.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_resource_server("test-user_pool_id", "test-identifier", "test-name", scopes="test-scopes", region_name="us-east-1")
    mock_client.update_resource_server.assert_called_once()

def test_update_terms_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_terms
    mock_client = MagicMock()
    mock_client.update_terms.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_terms("test-terms_id", "test-user_pool_id", terms_name="test-terms_name", terms_source="test-terms_source", enforcement="test-enforcement", links="test-links", region_name="us-east-1")
    mock_client.update_terms.assert_called_once()

def test_update_user_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_user_attributes
    mock_client = MagicMock()
    mock_client.update_user_attributes.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_user_attributes("test-user_attributes", "test-access_token", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.update_user_attributes.assert_called_once()

def test_update_user_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_user_pool
    mock_client = MagicMock()
    mock_client.update_user_pool.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_user_pool("test-user_pool_id", policies="test-policies", deletion_protection="test-deletion_protection", lambda_config={}, auto_verified_attributes=True, sms_verification_message="test-sms_verification_message", email_verification_message="test-email_verification_message", email_verification_subject="test-email_verification_subject", verification_message_template="test-verification_message_template", sms_authentication_message="test-sms_authentication_message", user_attribute_update_settings={}, mfa_configuration={}, device_configuration={}, email_configuration={}, sms_configuration={}, user_pool_tags=[{"Key": "k", "Value": "v"}], admin_create_user_config={}, user_pool_add_ons="test-user_pool_add_ons", account_recovery_setting=1, pool_name="test-pool_name", user_pool_tier="test-user_pool_tier", region_name="us-east-1")
    mock_client.update_user_pool.assert_called_once()

def test_update_user_pool_client_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_user_pool_client
    mock_client = MagicMock()
    mock_client.update_user_pool_client.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_user_pool_client("test-user_pool_id", "test-client_id", client_name="test-client_name", refresh_token_validity="test-refresh_token_validity", access_token_validity="test-access_token_validity", id_token_validity="test-id_token_validity", token_validity_units="test-token_validity_units", read_attributes="test-read_attributes", write_attributes="test-write_attributes", explicit_auth_flows="test-explicit_auth_flows", supported_identity_providers=1, callback_ur_ls="test-callback_ur_ls", logout_ur_ls="test-logout_ur_ls", default_redirect_uri="test-default_redirect_uri", allowed_o_auth_flows=True, allowed_o_auth_scopes=True, allowed_o_auth_flows_user_pool_client=True, analytics_configuration={}, prevent_user_existence_errors="test-prevent_user_existence_errors", enable_token_revocation=True, enable_propagate_additional_user_context_data=True, auth_session_validity="test-auth_session_validity", refresh_token_rotation="test-refresh_token_rotation", region_name="us-east-1")
    mock_client.update_user_pool_client.assert_called_once()

def test_update_user_pool_domain_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import update_user_pool_domain
    mock_client = MagicMock()
    mock_client.update_user_pool_domain.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    update_user_pool_domain("test-domain", "test-user_pool_id", managed_login_version="test-managed_login_version", custom_domain_config={}, region_name="us-east-1")
    mock_client.update_user_pool_domain.assert_called_once()

def test_verify_software_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito import verify_software_token
    mock_client = MagicMock()
    mock_client.verify_software_token.return_value = {}
    monkeypatch.setattr("aws_util.cognito.get_client", lambda *a, **kw: mock_client)
    verify_software_token("test-user_code", access_token="test-access_token", session="test-session", friendly_device_name="test-friendly_device_name", region_name="us-east-1")
    mock_client.verify_software_token.assert_called_once()
