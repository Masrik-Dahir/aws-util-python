

"""Tests for aws_util.aio.cognito — native async Cognito utilities."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.cognito as cognito_mod
from aws_util.aio.cognito import (

    AuthResult,
    CognitoUser,
    CognitoUserPool,
    _parse_user,
    admin_add_user_to_group,
    admin_create_user,
    admin_delete_user,
    admin_get_user,
    admin_initiate_auth,
    admin_remove_user_from_group,
    admin_set_user_password,
    bulk_create_users,
    get_or_create_user,
    list_user_pools,
    list_users,
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
# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_client(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.cognito.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# _parse_user
# ---------------------------------------------------------------------------


def test_parse_user_full():
    user = {
        "Username": "alice",
        "UserStatus": "CONFIRMED",
        "Enabled": True,
        "UserCreateDate": "2025-01-01T00:00:00Z",
        "UserLastModifiedDate": "2025-06-01T00:00:00Z",
        "Attributes": [
            {"Name": "email", "Value": "alice@example.com"},
            {"Name": "sub", "Value": "abc-123"},
        ],
    }
    result = _parse_user(user)
    assert result.username == "alice"
    assert result.user_status == "CONFIRMED"
    assert result.attributes["email"] == "alice@example.com"


def test_parse_user_minimal():
    user = {"Username": "bob"}
    result = _parse_user(user)
    assert result.username == "bob"
    assert result.user_status == "UNKNOWN"
    assert result.enabled is True
    assert result.attributes == {}


# ---------------------------------------------------------------------------
# admin_create_user
# ---------------------------------------------------------------------------


async def test_admin_create_user_basic(mock_client):
    mock_client.call.return_value = {
        "User": {
            "Username": "alice",
            "UserStatus": "FORCE_CHANGE_PASSWORD",
            "Attributes": [],
        }
    }
    user = await admin_create_user("pool-1", "alice")
    assert user.username == "alice"


async def test_admin_create_user_with_all_options(mock_client):
    mock_client.call.return_value = {
        "User": {
            "Username": "alice",
            "UserStatus": "FORCE_CHANGE_PASSWORD",
            "Attributes": [
                {"Name": "email", "Value": "alice@example.com"}
            ],
        }
    }
    user = await admin_create_user(
        "pool-1",
        "alice",
        temp_password="P@ss123!",
        attributes={"email": "alice@example.com"},
        suppress_welcome_email=True,
    )
    assert user.username == "alice"
    kw = mock_client.call.call_args[1]
    assert kw["TemporaryPassword"] == "P@ss123!"
    assert kw["MessageAction"] == "SUPPRESS"


async def test_admin_create_user_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to create Cognito user"):
        await admin_create_user("pool-1", "alice")


# ---------------------------------------------------------------------------
# admin_get_user
# ---------------------------------------------------------------------------


async def test_admin_get_user_success(mock_client):
    mock_client.call.return_value = {
        "Username": "alice",
        "UserStatus": "CONFIRMED",
        "Enabled": True,
        "UserAttributes": [
            {"Name": "email", "Value": "alice@example.com"}
        ],
    }
    user = await admin_get_user("pool-1", "alice")
    assert user is not None
    assert user.username == "alice"
    assert user.attributes["email"] == "alice@example.com"


async def test_admin_get_user_not_found(mock_client):
    mock_client.call.side_effect = RuntimeError("UserNotFoundException")
    result = await admin_get_user("pool-1", "unknown")
    assert result is None


async def test_admin_get_user_other_error(mock_client):
    mock_client.call.side_effect = RuntimeError("AccessDenied")
    with pytest.raises(RuntimeError, match="admin_get_user failed"):
        await admin_get_user("pool-1", "alice")


# ---------------------------------------------------------------------------
# admin_delete_user
# ---------------------------------------------------------------------------


async def test_admin_delete_user_success(mock_client):
    mock_client.call.return_value = {}
    await admin_delete_user("pool-1", "alice")
    mock_client.call.assert_called_once()


async def test_admin_delete_user_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to delete Cognito user"):
        await admin_delete_user("pool-1", "alice")


# ---------------------------------------------------------------------------
# admin_set_user_password
# ---------------------------------------------------------------------------


async def test_admin_set_user_password_success(mock_client):
    mock_client.call.return_value = {}
    await admin_set_user_password("pool-1", "alice", "NewP@ss!")
    kw = mock_client.call.call_args[1]
    assert kw["Password"] == "NewP@ss!"
    assert kw["Permanent"] is True


async def test_admin_set_user_password_temporary(mock_client):
    mock_client.call.return_value = {}
    await admin_set_user_password(
        "pool-1", "alice", "TempP@ss!", permanent=False
    )
    kw = mock_client.call.call_args[1]
    assert kw["Permanent"] is False


async def test_admin_set_user_password_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to set password"):
        await admin_set_user_password("pool-1", "alice", "pw")


# ---------------------------------------------------------------------------
# admin_add_user_to_group
# ---------------------------------------------------------------------------


async def test_admin_add_user_to_group_success(mock_client):
    mock_client.call.return_value = {}
    await admin_add_user_to_group("pool-1", "alice", "admins")
    mock_client.call.assert_called_once()


async def test_admin_add_user_to_group_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to add"):
        await admin_add_user_to_group("pool-1", "alice", "admins")


# ---------------------------------------------------------------------------
# admin_remove_user_from_group
# ---------------------------------------------------------------------------


async def test_admin_remove_user_from_group_success(mock_client):
    mock_client.call.return_value = {}
    await admin_remove_user_from_group("pool-1", "alice", "admins")
    mock_client.call.assert_called_once()


async def test_admin_remove_user_from_group_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to remove"):
        await admin_remove_user_from_group("pool-1", "alice", "admins")


# ---------------------------------------------------------------------------
# list_users
# ---------------------------------------------------------------------------


async def test_list_users_success(mock_client):
    mock_client.paginate.return_value = [
        {
            "Username": "alice",
            "UserStatus": "CONFIRMED",
            "Attributes": [],
        }
    ]
    users = await list_users("pool-1")
    assert len(users) == 1
    assert users[0].username == "alice"


async def test_list_users_with_filter_and_attrs(mock_client):
    mock_client.paginate.return_value = []
    await list_users(
        "pool-1",
        filter_str='email = "a@example.com"',
        attributes_to_get=["email"],
    )
    kw = mock_client.paginate.call_args[1]
    assert kw["Filter"] == 'email = "a@example.com"'
    assert kw["AttributesToGet"] == ["email"]


async def test_list_users_runtime_error(mock_client):
    mock_client.paginate.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="list_users failed"):
        await list_users("pool-1")


# ---------------------------------------------------------------------------
# admin_initiate_auth
# ---------------------------------------------------------------------------


async def test_admin_initiate_auth_success(mock_client):
    mock_client.call.return_value = {
        "AuthenticationResult": {
            "AccessToken": "access-tok",
            "IdToken": "id-tok",
            "RefreshToken": "refresh-tok",
            "TokenType": "Bearer",
            "ExpiresIn": 3600,
        }
    }
    result = await admin_initiate_auth(
        "pool-1", "client-1", "alice", "password"
    )
    assert result.access_token == "access-tok"
    assert result.id_token == "id-tok"
    assert result.refresh_token == "refresh-tok"
    assert result.token_type == "Bearer"
    assert result.expires_in == 3600


async def test_admin_initiate_auth_empty_result(mock_client):
    mock_client.call.return_value = {}
    result = await admin_initiate_auth(
        "pool-1", "client-1", "alice", "password"
    )
    assert result.access_token is None


async def test_admin_initiate_auth_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="admin_initiate_auth failed"):
        await admin_initiate_auth(
            "pool-1", "client-1", "alice", "password"
        )


# ---------------------------------------------------------------------------
# list_user_pools
# ---------------------------------------------------------------------------


async def test_list_user_pools_success(mock_client):
    mock_client.call.return_value = {
        "UserPools": [
            {
                "Id": "pool-1",
                "Name": "MyPool",
                "Status": "Enabled",
            }
        ]
    }
    pools = await list_user_pools()
    assert len(pools) == 1
    assert pools[0].pool_id == "pool-1"
    assert pools[0].pool_name == "MyPool"


async def test_list_user_pools_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "UserPools": [{"Id": "pool-1", "Name": "A"}],
            "NextToken": "tok",
        },
        {
            "UserPools": [{"Id": "pool-2", "Name": "B"}],
        },
    ]
    pools = await list_user_pools()
    assert len(pools) == 2


async def test_list_user_pools_empty(mock_client):
    mock_client.call.return_value = {"UserPools": []}
    pools = await list_user_pools()
    assert pools == []


async def test_list_user_pools_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="list_user_pools failed"):
        await list_user_pools()


# ---------------------------------------------------------------------------
# get_or_create_user
# ---------------------------------------------------------------------------


async def test_get_or_create_user_existing(monkeypatch):
    existing = CognitoUser(username="alice", user_status="CONFIRMED")
    monkeypatch.setattr(
        cognito_mod,
        "admin_get_user",
        AsyncMock(return_value=existing),
    )
    user, created = await get_or_create_user("pool-1", "alice")
    assert user.username == "alice"
    assert created is False


async def test_get_or_create_user_new(monkeypatch):
    new_user = CognitoUser(
        username="bob", user_status="FORCE_CHANGE_PASSWORD"
    )
    monkeypatch.setattr(
        cognito_mod,
        "admin_get_user",
        AsyncMock(return_value=None),
    )
    monkeypatch.setattr(
        cognito_mod,
        "admin_create_user",
        AsyncMock(return_value=new_user),
    )
    user, created = await get_or_create_user("pool-1", "bob")
    assert user.username == "bob"
    assert created is True


# ---------------------------------------------------------------------------
# bulk_create_users
# ---------------------------------------------------------------------------


async def test_bulk_create_users_success(monkeypatch):
    user1 = CognitoUser(
        username="alice", user_status="FORCE_CHANGE_PASSWORD"
    )
    user2 = CognitoUser(
        username="bob", user_status="FORCE_CHANGE_PASSWORD"
    )
    monkeypatch.setattr(
        cognito_mod,
        "admin_create_user",
        AsyncMock(side_effect=[user1, user2]),
    )
    users_input = [
        {
            "username": "alice",
            "temp_password": "Pass1!",
            "attributes": {"email": "alice@x.com"},
            "suppress_welcome_email": True,
        },
        {"username": "bob"},
    ]
    result = await bulk_create_users("pool-1", users_input)
    assert len(result) == 2
    assert result[0].username == "alice"


async def test_bulk_create_users_empty(monkeypatch):
    result = await bulk_create_users("pool-1", [])
    assert result == []


# ---------------------------------------------------------------------------
# reset_user_password
# ---------------------------------------------------------------------------


async def test_reset_user_password_success(mock_client):
    mock_client.call.return_value = {}
    await reset_user_password("pool-1", "alice")
    mock_client.call.assert_called_once()


async def test_reset_user_password_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="reset_user_password failed"):
        await reset_user_password("pool-1", "alice")


# ---------------------------------------------------------------------------
# Module __all__
# ---------------------------------------------------------------------------


def test_cognito_models_in_all():
    assert "CognitoUser" in cognito_mod.__all__
    assert "CognitoUserPool" in cognito_mod.__all__
    assert "AuthResult" in cognito_mod.__all__


async def test_add_custom_attributes(mock_client):
    mock_client.call.return_value = {}
    await add_custom_attributes("test-user_pool_id", [], )
    mock_client.call.assert_called_once()


async def test_add_custom_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await add_custom_attributes("test-user_pool_id", [], )


async def test_add_custom_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to add custom attributes"):
        await add_custom_attributes("test-user_pool_id", [], )


async def test_admin_confirm_sign_up(mock_client):
    mock_client.call.return_value = {}
    await admin_confirm_sign_up("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_confirm_sign_up_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_confirm_sign_up("test-user_pool_id", "test-username", )


async def test_admin_confirm_sign_up_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin confirm sign up"):
        await admin_confirm_sign_up("test-user_pool_id", "test-username", )


async def test_admin_delete_user_attributes(mock_client):
    mock_client.call.return_value = {}
    await admin_delete_user_attributes("test-user_pool_id", "test-username", [], )
    mock_client.call.assert_called_once()


async def test_admin_delete_user_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_delete_user_attributes("test-user_pool_id", "test-username", [], )


async def test_admin_delete_user_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin delete user attributes"):
        await admin_delete_user_attributes("test-user_pool_id", "test-username", [], )


async def test_admin_disable_provider_for_user(mock_client):
    mock_client.call.return_value = {}
    await admin_disable_provider_for_user("test-user_pool_id", {}, )
    mock_client.call.assert_called_once()


async def test_admin_disable_provider_for_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_disable_provider_for_user("test-user_pool_id", {}, )


async def test_admin_disable_provider_for_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin disable provider for user"):
        await admin_disable_provider_for_user("test-user_pool_id", {}, )


async def test_admin_disable_user(mock_client):
    mock_client.call.return_value = {}
    await admin_disable_user("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_disable_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_disable_user("test-user_pool_id", "test-username", )


async def test_admin_disable_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin disable user"):
        await admin_disable_user("test-user_pool_id", "test-username", )


async def test_admin_enable_user(mock_client):
    mock_client.call.return_value = {}
    await admin_enable_user("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_enable_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_enable_user("test-user_pool_id", "test-username", )


async def test_admin_enable_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin enable user"):
        await admin_enable_user("test-user_pool_id", "test-username", )


async def test_admin_forget_device(mock_client):
    mock_client.call.return_value = {}
    await admin_forget_device("test-user_pool_id", "test-username", "test-device_key", )
    mock_client.call.assert_called_once()


async def test_admin_forget_device_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_forget_device("test-user_pool_id", "test-username", "test-device_key", )


async def test_admin_forget_device_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin forget device"):
        await admin_forget_device("test-user_pool_id", "test-username", "test-device_key", )


async def test_admin_get_device(mock_client):
    mock_client.call.return_value = {}
    await admin_get_device("test-device_key", "test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_get_device_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_get_device("test-device_key", "test-user_pool_id", "test-username", )


async def test_admin_get_device_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin get device"):
        await admin_get_device("test-device_key", "test-user_pool_id", "test-username", )


async def test_admin_link_provider_for_user(mock_client):
    mock_client.call.return_value = {}
    await admin_link_provider_for_user("test-user_pool_id", {}, {}, )
    mock_client.call.assert_called_once()


async def test_admin_link_provider_for_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_link_provider_for_user("test-user_pool_id", {}, {}, )


async def test_admin_link_provider_for_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin link provider for user"):
        await admin_link_provider_for_user("test-user_pool_id", {}, {}, )


async def test_admin_list_devices(mock_client):
    mock_client.call.return_value = {}
    await admin_list_devices("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_list_devices_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_list_devices("test-user_pool_id", "test-username", )


async def test_admin_list_devices_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin list devices"):
        await admin_list_devices("test-user_pool_id", "test-username", )


async def test_admin_list_groups_for_user(mock_client):
    mock_client.call.return_value = {}
    await admin_list_groups_for_user("test-username", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_admin_list_groups_for_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_list_groups_for_user("test-username", "test-user_pool_id", )


async def test_admin_list_groups_for_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin list groups for user"):
        await admin_list_groups_for_user("test-username", "test-user_pool_id", )


async def test_admin_list_user_auth_events(mock_client):
    mock_client.call.return_value = {}
    await admin_list_user_auth_events("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_list_user_auth_events_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_list_user_auth_events("test-user_pool_id", "test-username", )


async def test_admin_list_user_auth_events_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin list user auth events"):
        await admin_list_user_auth_events("test-user_pool_id", "test-username", )


async def test_admin_reset_user_password(mock_client):
    mock_client.call.return_value = {}
    await admin_reset_user_password("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_reset_user_password_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_reset_user_password("test-user_pool_id", "test-username", )


async def test_admin_reset_user_password_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin reset user password"):
        await admin_reset_user_password("test-user_pool_id", "test-username", )


async def test_admin_respond_to_auth_challenge(mock_client):
    mock_client.call.return_value = {}
    await admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", )
    mock_client.call.assert_called_once()


async def test_admin_respond_to_auth_challenge_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", )


async def test_admin_respond_to_auth_challenge_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin respond to auth challenge"):
        await admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", )


async def test_admin_set_user_mfa_preference(mock_client):
    mock_client.call.return_value = {}
    await admin_set_user_mfa_preference("test-username", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_admin_set_user_mfa_preference_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_set_user_mfa_preference("test-username", "test-user_pool_id", )


async def test_admin_set_user_mfa_preference_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin set user mfa preference"):
        await admin_set_user_mfa_preference("test-username", "test-user_pool_id", )


async def test_admin_set_user_settings(mock_client):
    mock_client.call.return_value = {}
    await admin_set_user_settings("test-user_pool_id", "test-username", [], )
    mock_client.call.assert_called_once()


async def test_admin_set_user_settings_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_set_user_settings("test-user_pool_id", "test-username", [], )


async def test_admin_set_user_settings_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin set user settings"):
        await admin_set_user_settings("test-user_pool_id", "test-username", [], )


async def test_admin_update_auth_event_feedback(mock_client):
    mock_client.call.return_value = {}
    await admin_update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_value", )
    mock_client.call.assert_called_once()


async def test_admin_update_auth_event_feedback_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_value", )


async def test_admin_update_auth_event_feedback_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin update auth event feedback"):
        await admin_update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_value", )


async def test_admin_update_device_status(mock_client):
    mock_client.call.return_value = {}
    await admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", )
    mock_client.call.assert_called_once()


async def test_admin_update_device_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", )


async def test_admin_update_device_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin update device status"):
        await admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", )


async def test_admin_update_user_attributes(mock_client):
    mock_client.call.return_value = {}
    await admin_update_user_attributes("test-user_pool_id", "test-username", [], )
    mock_client.call.assert_called_once()


async def test_admin_update_user_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_update_user_attributes("test-user_pool_id", "test-username", [], )


async def test_admin_update_user_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin update user attributes"):
        await admin_update_user_attributes("test-user_pool_id", "test-username", [], )


async def test_admin_user_global_sign_out(mock_client):
    mock_client.call.return_value = {}
    await admin_user_global_sign_out("test-user_pool_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_admin_user_global_sign_out_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await admin_user_global_sign_out("test-user_pool_id", "test-username", )


async def test_admin_user_global_sign_out_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to admin user global sign out"):
        await admin_user_global_sign_out("test-user_pool_id", "test-username", )


async def test_associate_software_token(mock_client):
    mock_client.call.return_value = {}
    await associate_software_token()
    mock_client.call.assert_called_once()


async def test_associate_software_token_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await associate_software_token()


async def test_associate_software_token_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to associate software token"):
        await associate_software_token()


async def test_change_password(mock_client):
    mock_client.call.return_value = {}
    await change_password("test-proposed_password", "test-access_token", )
    mock_client.call.assert_called_once()


async def test_change_password_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await change_password("test-proposed_password", "test-access_token", )


async def test_change_password_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to change password"):
        await change_password("test-proposed_password", "test-access_token", )


async def test_complete_web_authn_registration(mock_client):
    mock_client.call.return_value = {}
    await complete_web_authn_registration("test-access_token", {}, )
    mock_client.call.assert_called_once()


async def test_complete_web_authn_registration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await complete_web_authn_registration("test-access_token", {}, )


async def test_complete_web_authn_registration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to complete web authn registration"):
        await complete_web_authn_registration("test-access_token", {}, )


async def test_confirm_device(mock_client):
    mock_client.call.return_value = {}
    await confirm_device("test-access_token", "test-device_key", )
    mock_client.call.assert_called_once()


async def test_confirm_device_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await confirm_device("test-access_token", "test-device_key", )


async def test_confirm_device_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to confirm device"):
        await confirm_device("test-access_token", "test-device_key", )


async def test_confirm_forgot_password(mock_client):
    mock_client.call.return_value = {}
    await confirm_forgot_password("test-client_id", "test-username", "test-confirmation_code", "test-password", )
    mock_client.call.assert_called_once()


async def test_confirm_forgot_password_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await confirm_forgot_password("test-client_id", "test-username", "test-confirmation_code", "test-password", )


async def test_confirm_forgot_password_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to confirm forgot password"):
        await confirm_forgot_password("test-client_id", "test-username", "test-confirmation_code", "test-password", )


async def test_confirm_sign_up(mock_client):
    mock_client.call.return_value = {}
    await confirm_sign_up("test-client_id", "test-username", "test-confirmation_code", )
    mock_client.call.assert_called_once()


async def test_confirm_sign_up_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await confirm_sign_up("test-client_id", "test-username", "test-confirmation_code", )


async def test_confirm_sign_up_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to confirm sign up"):
        await confirm_sign_up("test-client_id", "test-username", "test-confirmation_code", )


async def test_create_group(mock_client):
    mock_client.call.return_value = {}
    await create_group("test-group_name", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_create_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_group("test-group_name", "test-user_pool_id", )


async def test_create_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create group"):
        await create_group("test-group_name", "test-user_pool_id", )


async def test_create_identity_provider(mock_client):
    mock_client.call.return_value = {}
    await create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", {}, )
    mock_client.call.assert_called_once()


async def test_create_identity_provider_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", {}, )


async def test_create_identity_provider_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create identity provider"):
        await create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", {}, )


async def test_create_managed_login_branding(mock_client):
    mock_client.call.return_value = {}
    await create_managed_login_branding("test-user_pool_id", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_create_managed_login_branding_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_managed_login_branding("test-user_pool_id", "test-client_id", )


async def test_create_managed_login_branding_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create managed login branding"):
        await create_managed_login_branding("test-user_pool_id", "test-client_id", )


async def test_create_resource_server(mock_client):
    mock_client.call.return_value = {}
    await create_resource_server("test-user_pool_id", "test-identifier", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_resource_server_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_resource_server("test-user_pool_id", "test-identifier", "test-name", )


async def test_create_resource_server_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create resource server"):
        await create_resource_server("test-user_pool_id", "test-identifier", "test-name", )


async def test_create_terms(mock_client):
    mock_client.call.return_value = {}
    await create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", )
    mock_client.call.assert_called_once()


async def test_create_terms_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", )


async def test_create_terms_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create terms"):
        await create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", )


async def test_create_user_import_job(mock_client):
    mock_client.call.return_value = {}
    await create_user_import_job("test-job_name", "test-user_pool_id", "test-cloud_watch_logs_role_arn", )
    mock_client.call.assert_called_once()


async def test_create_user_import_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_import_job("test-job_name", "test-user_pool_id", "test-cloud_watch_logs_role_arn", )


async def test_create_user_import_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create user import job"):
        await create_user_import_job("test-job_name", "test-user_pool_id", "test-cloud_watch_logs_role_arn", )


async def test_create_user_pool(mock_client):
    mock_client.call.return_value = {}
    await create_user_pool("test-pool_name", )
    mock_client.call.assert_called_once()


async def test_create_user_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_pool("test-pool_name", )


async def test_create_user_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create user pool"):
        await create_user_pool("test-pool_name", )


async def test_create_user_pool_client(mock_client):
    mock_client.call.return_value = {}
    await create_user_pool_client("test-user_pool_id", "test-client_name", )
    mock_client.call.assert_called_once()


async def test_create_user_pool_client_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_pool_client("test-user_pool_id", "test-client_name", )


async def test_create_user_pool_client_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create user pool client"):
        await create_user_pool_client("test-user_pool_id", "test-client_name", )


async def test_create_user_pool_domain(mock_client):
    mock_client.call.return_value = {}
    await create_user_pool_domain("test-domain", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_create_user_pool_domain_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_pool_domain("test-domain", "test-user_pool_id", )


async def test_create_user_pool_domain_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create user pool domain"):
        await create_user_pool_domain("test-domain", "test-user_pool_id", )


async def test_delete_group(mock_client):
    mock_client.call.return_value = {}
    await delete_group("test-group_name", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_group("test-group_name", "test-user_pool_id", )


async def test_delete_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete group"):
        await delete_group("test-group_name", "test-user_pool_id", )


async def test_delete_identity_provider(mock_client):
    mock_client.call.return_value = {}
    await delete_identity_provider("test-user_pool_id", "test-provider_name", )
    mock_client.call.assert_called_once()


async def test_delete_identity_provider_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_identity_provider("test-user_pool_id", "test-provider_name", )


async def test_delete_identity_provider_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete identity provider"):
        await delete_identity_provider("test-user_pool_id", "test-provider_name", )


async def test_delete_managed_login_branding(mock_client):
    mock_client.call.return_value = {}
    await delete_managed_login_branding("test-managed_login_branding_id", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_managed_login_branding_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_managed_login_branding("test-managed_login_branding_id", "test-user_pool_id", )


async def test_delete_managed_login_branding_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete managed login branding"):
        await delete_managed_login_branding("test-managed_login_branding_id", "test-user_pool_id", )


async def test_delete_resource_server(mock_client):
    mock_client.call.return_value = {}
    await delete_resource_server("test-user_pool_id", "test-identifier", )
    mock_client.call.assert_called_once()


async def test_delete_resource_server_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_server("test-user_pool_id", "test-identifier", )


async def test_delete_resource_server_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete resource server"):
        await delete_resource_server("test-user_pool_id", "test-identifier", )


async def test_delete_terms(mock_client):
    mock_client.call.return_value = {}
    await delete_terms("test-terms_id", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_terms_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_terms("test-terms_id", "test-user_pool_id", )


async def test_delete_terms_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete terms"):
        await delete_terms("test-terms_id", "test-user_pool_id", )


async def test_delete_user(mock_client):
    mock_client.call.return_value = {}
    await delete_user("test-access_token", )
    mock_client.call.assert_called_once()


async def test_delete_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user("test-access_token", )


async def test_delete_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete user"):
        await delete_user("test-access_token", )


async def test_delete_user_attributes(mock_client):
    mock_client.call.return_value = {}
    await delete_user_attributes([], "test-access_token", )
    mock_client.call.assert_called_once()


async def test_delete_user_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_attributes([], "test-access_token", )


async def test_delete_user_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete user attributes"):
        await delete_user_attributes([], "test-access_token", )


async def test_delete_user_pool(mock_client):
    mock_client.call.return_value = {}
    await delete_user_pool("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_pool("test-user_pool_id", )


async def test_delete_user_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete user pool"):
        await delete_user_pool("test-user_pool_id", )


async def test_delete_user_pool_client(mock_client):
    mock_client.call.return_value = {}
    await delete_user_pool_client("test-user_pool_id", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_pool_client_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_pool_client("test-user_pool_id", "test-client_id", )


async def test_delete_user_pool_client_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete user pool client"):
        await delete_user_pool_client("test-user_pool_id", "test-client_id", )


async def test_delete_user_pool_domain(mock_client):
    mock_client.call.return_value = {}
    await delete_user_pool_domain("test-domain", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_pool_domain_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_pool_domain("test-domain", "test-user_pool_id", )


async def test_delete_user_pool_domain_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete user pool domain"):
        await delete_user_pool_domain("test-domain", "test-user_pool_id", )


async def test_delete_web_authn_credential(mock_client):
    mock_client.call.return_value = {}
    await delete_web_authn_credential("test-access_token", "test-credential_id", )
    mock_client.call.assert_called_once()


async def test_delete_web_authn_credential_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_web_authn_credential("test-access_token", "test-credential_id", )


async def test_delete_web_authn_credential_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete web authn credential"):
        await delete_web_authn_credential("test-access_token", "test-credential_id", )


async def test_describe_identity_provider(mock_client):
    mock_client.call.return_value = {}
    await describe_identity_provider("test-user_pool_id", "test-provider_name", )
    mock_client.call.assert_called_once()


async def test_describe_identity_provider_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_identity_provider("test-user_pool_id", "test-provider_name", )


async def test_describe_identity_provider_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe identity provider"):
        await describe_identity_provider("test-user_pool_id", "test-provider_name", )


async def test_describe_managed_login_branding(mock_client):
    mock_client.call.return_value = {}
    await describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", )
    mock_client.call.assert_called_once()


async def test_describe_managed_login_branding_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", )


async def test_describe_managed_login_branding_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe managed login branding"):
        await describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", )


async def test_describe_managed_login_branding_by_client(mock_client):
    mock_client.call.return_value = {}
    await describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_describe_managed_login_branding_by_client_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", )


async def test_describe_managed_login_branding_by_client_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe managed login branding by client"):
        await describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", )


async def test_describe_resource_server(mock_client):
    mock_client.call.return_value = {}
    await describe_resource_server("test-user_pool_id", "test-identifier", )
    mock_client.call.assert_called_once()


async def test_describe_resource_server_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_resource_server("test-user_pool_id", "test-identifier", )


async def test_describe_resource_server_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe resource server"):
        await describe_resource_server("test-user_pool_id", "test-identifier", )


async def test_describe_risk_configuration(mock_client):
    mock_client.call.return_value = {}
    await describe_risk_configuration("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_describe_risk_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_risk_configuration("test-user_pool_id", )


async def test_describe_risk_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe risk configuration"):
        await describe_risk_configuration("test-user_pool_id", )


async def test_describe_terms(mock_client):
    mock_client.call.return_value = {}
    await describe_terms("test-terms_id", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_describe_terms_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_terms("test-terms_id", "test-user_pool_id", )


async def test_describe_terms_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe terms"):
        await describe_terms("test-terms_id", "test-user_pool_id", )


async def test_describe_user_import_job(mock_client):
    mock_client.call.return_value = {}
    await describe_user_import_job("test-user_pool_id", "test-job_id", )
    mock_client.call.assert_called_once()


async def test_describe_user_import_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_import_job("test-user_pool_id", "test-job_id", )


async def test_describe_user_import_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe user import job"):
        await describe_user_import_job("test-user_pool_id", "test-job_id", )


async def test_describe_user_pool(mock_client):
    mock_client.call.return_value = {}
    await describe_user_pool("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_describe_user_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_pool("test-user_pool_id", )


async def test_describe_user_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe user pool"):
        await describe_user_pool("test-user_pool_id", )


async def test_describe_user_pool_client(mock_client):
    mock_client.call.return_value = {}
    await describe_user_pool_client("test-user_pool_id", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_describe_user_pool_client_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_pool_client("test-user_pool_id", "test-client_id", )


async def test_describe_user_pool_client_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe user pool client"):
        await describe_user_pool_client("test-user_pool_id", "test-client_id", )


async def test_describe_user_pool_domain(mock_client):
    mock_client.call.return_value = {}
    await describe_user_pool_domain("test-domain", )
    mock_client.call.assert_called_once()


async def test_describe_user_pool_domain_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_pool_domain("test-domain", )


async def test_describe_user_pool_domain_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to describe user pool domain"):
        await describe_user_pool_domain("test-domain", )


async def test_forget_device(mock_client):
    mock_client.call.return_value = {}
    await forget_device("test-device_key", )
    mock_client.call.assert_called_once()


async def test_forget_device_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await forget_device("test-device_key", )


async def test_forget_device_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to forget device"):
        await forget_device("test-device_key", )


async def test_forgot_password(mock_client):
    mock_client.call.return_value = {}
    await forgot_password("test-client_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_forgot_password_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await forgot_password("test-client_id", "test-username", )


async def test_forgot_password_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to forgot password"):
        await forgot_password("test-client_id", "test-username", )


async def test_get_csv_header(mock_client):
    mock_client.call.return_value = {}
    await get_csv_header("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_csv_header_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_csv_header("test-user_pool_id", )


async def test_get_csv_header_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get csv header"):
        await get_csv_header("test-user_pool_id", )


async def test_get_device(mock_client):
    mock_client.call.return_value = {}
    await get_device("test-device_key", )
    mock_client.call.assert_called_once()


async def test_get_device_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_device("test-device_key", )


async def test_get_device_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get device"):
        await get_device("test-device_key", )


async def test_get_group(mock_client):
    mock_client.call.return_value = {}
    await get_group("test-group_name", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_group("test-group_name", "test-user_pool_id", )


async def test_get_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get group"):
        await get_group("test-group_name", "test-user_pool_id", )


async def test_get_identity_provider_by_identifier(mock_client):
    mock_client.call.return_value = {}
    await get_identity_provider_by_identifier("test-user_pool_id", "test-idp_identifier", )
    mock_client.call.assert_called_once()


async def test_get_identity_provider_by_identifier_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_provider_by_identifier("test-user_pool_id", "test-idp_identifier", )


async def test_get_identity_provider_by_identifier_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get identity provider by identifier"):
        await get_identity_provider_by_identifier("test-user_pool_id", "test-idp_identifier", )


async def test_get_log_delivery_configuration(mock_client):
    mock_client.call.return_value = {}
    await get_log_delivery_configuration("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_log_delivery_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_log_delivery_configuration("test-user_pool_id", )


async def test_get_log_delivery_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get log delivery configuration"):
        await get_log_delivery_configuration("test-user_pool_id", )


async def test_get_signing_certificate(mock_client):
    mock_client.call.return_value = {}
    await get_signing_certificate("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_signing_certificate_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_signing_certificate("test-user_pool_id", )


async def test_get_signing_certificate_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get signing certificate"):
        await get_signing_certificate("test-user_pool_id", )


async def test_get_tokens_from_refresh_token(mock_client):
    mock_client.call.return_value = {}
    await get_tokens_from_refresh_token("test-refresh_token", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_get_tokens_from_refresh_token_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_tokens_from_refresh_token("test-refresh_token", "test-client_id", )


async def test_get_tokens_from_refresh_token_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get tokens from refresh token"):
        await get_tokens_from_refresh_token("test-refresh_token", "test-client_id", )


async def test_get_ui_customization(mock_client):
    mock_client.call.return_value = {}
    await get_ui_customization("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_ui_customization_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_ui_customization("test-user_pool_id", )


async def test_get_ui_customization_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get ui customization"):
        await get_ui_customization("test-user_pool_id", )


async def test_get_user(mock_client):
    mock_client.call.return_value = {}
    await get_user("test-access_token", )
    mock_client.call.assert_called_once()


async def test_get_user_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_user("test-access_token", )


async def test_get_user_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get user"):
        await get_user("test-access_token", )


async def test_get_user_attribute_verification_code(mock_client):
    mock_client.call.return_value = {}
    await get_user_attribute_verification_code("test-access_token", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_get_user_attribute_verification_code_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_user_attribute_verification_code("test-access_token", "test-attribute_name", )


async def test_get_user_attribute_verification_code_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get user attribute verification code"):
        await get_user_attribute_verification_code("test-access_token", "test-attribute_name", )


async def test_get_user_auth_factors(mock_client):
    mock_client.call.return_value = {}
    await get_user_auth_factors("test-access_token", )
    mock_client.call.assert_called_once()


async def test_get_user_auth_factors_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_user_auth_factors("test-access_token", )


async def test_get_user_auth_factors_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get user auth factors"):
        await get_user_auth_factors("test-access_token", )


async def test_get_user_pool_mfa_config(mock_client):
    mock_client.call.return_value = {}
    await get_user_pool_mfa_config("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_user_pool_mfa_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_user_pool_mfa_config("test-user_pool_id", )


async def test_get_user_pool_mfa_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get user pool mfa config"):
        await get_user_pool_mfa_config("test-user_pool_id", )


async def test_global_sign_out(mock_client):
    mock_client.call.return_value = {}
    await global_sign_out("test-access_token", )
    mock_client.call.assert_called_once()


async def test_global_sign_out_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await global_sign_out("test-access_token", )


async def test_global_sign_out_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to global sign out"):
        await global_sign_out("test-access_token", )


async def test_initiate_auth(mock_client):
    mock_client.call.return_value = {}
    await initiate_auth("test-auth_flow", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_initiate_auth_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await initiate_auth("test-auth_flow", "test-client_id", )


async def test_initiate_auth_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to initiate auth"):
        await initiate_auth("test-auth_flow", "test-client_id", )


async def test_list_devices(mock_client):
    mock_client.call.return_value = {}
    await list_devices("test-access_token", )
    mock_client.call.assert_called_once()


async def test_list_devices_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_devices("test-access_token", )


async def test_list_devices_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list devices"):
        await list_devices("test-access_token", )


async def test_list_groups(mock_client):
    mock_client.call.return_value = {}
    await list_groups("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_list_groups_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_groups("test-user_pool_id", )


async def test_list_groups_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list groups"):
        await list_groups("test-user_pool_id", )


async def test_list_identity_providers(mock_client):
    mock_client.call.return_value = {}
    await list_identity_providers("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_list_identity_providers_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_identity_providers("test-user_pool_id", )


async def test_list_identity_providers_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list identity providers"):
        await list_identity_providers("test-user_pool_id", )


async def test_list_resource_servers(mock_client):
    mock_client.call.return_value = {}
    await list_resource_servers("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_list_resource_servers_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_resource_servers("test-user_pool_id", )


async def test_list_resource_servers_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list resource servers"):
        await list_resource_servers("test-user_pool_id", )


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_terms(mock_client):
    mock_client.call.return_value = {}
    await list_terms("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_list_terms_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_terms("test-user_pool_id", )


async def test_list_terms_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list terms"):
        await list_terms("test-user_pool_id", )


async def test_list_user_import_jobs(mock_client):
    mock_client.call.return_value = {}
    await list_user_import_jobs("test-user_pool_id", 1, )
    mock_client.call.assert_called_once()


async def test_list_user_import_jobs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_import_jobs("test-user_pool_id", 1, )


async def test_list_user_import_jobs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list user import jobs"):
        await list_user_import_jobs("test-user_pool_id", 1, )


async def test_list_user_pool_clients(mock_client):
    mock_client.call.return_value = {}
    await list_user_pool_clients("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_list_user_pool_clients_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_user_pool_clients("test-user_pool_id", )


async def test_list_user_pool_clients_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list user pool clients"):
        await list_user_pool_clients("test-user_pool_id", )


async def test_list_users_in_group(mock_client):
    mock_client.call.return_value = {}
    await list_users_in_group("test-user_pool_id", "test-group_name", )
    mock_client.call.assert_called_once()


async def test_list_users_in_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_users_in_group("test-user_pool_id", "test-group_name", )


async def test_list_users_in_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list users in group"):
        await list_users_in_group("test-user_pool_id", "test-group_name", )


async def test_list_web_authn_credentials(mock_client):
    mock_client.call.return_value = {}
    await list_web_authn_credentials("test-access_token", )
    mock_client.call.assert_called_once()


async def test_list_web_authn_credentials_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_web_authn_credentials("test-access_token", )


async def test_list_web_authn_credentials_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list web authn credentials"):
        await list_web_authn_credentials("test-access_token", )


async def test_resend_confirmation_code(mock_client):
    mock_client.call.return_value = {}
    await resend_confirmation_code("test-client_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_resend_confirmation_code_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await resend_confirmation_code("test-client_id", "test-username", )


async def test_resend_confirmation_code_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to resend confirmation code"):
        await resend_confirmation_code("test-client_id", "test-username", )


async def test_respond_to_auth_challenge(mock_client):
    mock_client.call.return_value = {}
    await respond_to_auth_challenge("test-client_id", "test-challenge_name", )
    mock_client.call.assert_called_once()


async def test_respond_to_auth_challenge_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await respond_to_auth_challenge("test-client_id", "test-challenge_name", )


async def test_respond_to_auth_challenge_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to respond to auth challenge"):
        await respond_to_auth_challenge("test-client_id", "test-challenge_name", )


async def test_revoke_token(mock_client):
    mock_client.call.return_value = {}
    await revoke_token("test-token", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_revoke_token_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_token("test-token", "test-client_id", )


async def test_revoke_token_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to revoke token"):
        await revoke_token("test-token", "test-client_id", )


async def test_set_log_delivery_configuration(mock_client):
    mock_client.call.return_value = {}
    await set_log_delivery_configuration("test-user_pool_id", [], )
    mock_client.call.assert_called_once()


async def test_set_log_delivery_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await set_log_delivery_configuration("test-user_pool_id", [], )


async def test_set_log_delivery_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to set log delivery configuration"):
        await set_log_delivery_configuration("test-user_pool_id", [], )


async def test_set_risk_configuration(mock_client):
    mock_client.call.return_value = {}
    await set_risk_configuration("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_set_risk_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await set_risk_configuration("test-user_pool_id", )


async def test_set_risk_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to set risk configuration"):
        await set_risk_configuration("test-user_pool_id", )


async def test_set_ui_customization(mock_client):
    mock_client.call.return_value = {}
    await set_ui_customization("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_set_ui_customization_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await set_ui_customization("test-user_pool_id", )


async def test_set_ui_customization_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to set ui customization"):
        await set_ui_customization("test-user_pool_id", )


async def test_set_user_mfa_preference(mock_client):
    mock_client.call.return_value = {}
    await set_user_mfa_preference("test-access_token", )
    mock_client.call.assert_called_once()


async def test_set_user_mfa_preference_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await set_user_mfa_preference("test-access_token", )


async def test_set_user_mfa_preference_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to set user mfa preference"):
        await set_user_mfa_preference("test-access_token", )


async def test_set_user_pool_mfa_config(mock_client):
    mock_client.call.return_value = {}
    await set_user_pool_mfa_config("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_set_user_pool_mfa_config_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await set_user_pool_mfa_config("test-user_pool_id", )


async def test_set_user_pool_mfa_config_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to set user pool mfa config"):
        await set_user_pool_mfa_config("test-user_pool_id", )


async def test_set_user_settings(mock_client):
    mock_client.call.return_value = {}
    await set_user_settings("test-access_token", [], )
    mock_client.call.assert_called_once()


async def test_set_user_settings_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await set_user_settings("test-access_token", [], )


async def test_set_user_settings_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to set user settings"):
        await set_user_settings("test-access_token", [], )


async def test_sign_up(mock_client):
    mock_client.call.return_value = {}
    await sign_up("test-client_id", "test-username", )
    mock_client.call.assert_called_once()


async def test_sign_up_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await sign_up("test-client_id", "test-username", )


async def test_sign_up_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to sign up"):
        await sign_up("test-client_id", "test-username", )


async def test_start_user_import_job(mock_client):
    mock_client.call.return_value = {}
    await start_user_import_job("test-user_pool_id", "test-job_id", )
    mock_client.call.assert_called_once()


async def test_start_user_import_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_user_import_job("test-user_pool_id", "test-job_id", )


async def test_start_user_import_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start user import job"):
        await start_user_import_job("test-user_pool_id", "test-job_id", )


async def test_start_web_authn_registration(mock_client):
    mock_client.call.return_value = {}
    await start_web_authn_registration("test-access_token", )
    mock_client.call.assert_called_once()


async def test_start_web_authn_registration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_web_authn_registration("test-access_token", )


async def test_start_web_authn_registration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start web authn registration"):
        await start_web_authn_registration("test-access_token", )


async def test_stop_user_import_job(mock_client):
    mock_client.call.return_value = {}
    await stop_user_import_job("test-user_pool_id", "test-job_id", )
    mock_client.call.assert_called_once()


async def test_stop_user_import_job_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_user_import_job("test-user_pool_id", "test-job_id", )


async def test_stop_user_import_job_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop user import job"):
        await stop_user_import_job("test-user_pool_id", "test-job_id", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource_arn", [], )


async def test_update_auth_event_feedback(mock_client):
    mock_client.call.return_value = {}
    await update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_token", "test-feedback_value", )
    mock_client.call.assert_called_once()


async def test_update_auth_event_feedback_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_token", "test-feedback_value", )


async def test_update_auth_event_feedback_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update auth event feedback"):
        await update_auth_event_feedback("test-user_pool_id", "test-username", "test-event_id", "test-feedback_token", "test-feedback_value", )


async def test_update_device_status(mock_client):
    mock_client.call.return_value = {}
    await update_device_status("test-access_token", "test-device_key", )
    mock_client.call.assert_called_once()


async def test_update_device_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_device_status("test-access_token", "test-device_key", )


async def test_update_device_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update device status"):
        await update_device_status("test-access_token", "test-device_key", )


async def test_update_group(mock_client):
    mock_client.call.return_value = {}
    await update_group("test-group_name", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_update_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_group("test-group_name", "test-user_pool_id", )


async def test_update_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update group"):
        await update_group("test-group_name", "test-user_pool_id", )


async def test_update_identity_provider(mock_client):
    mock_client.call.return_value = {}
    await update_identity_provider("test-user_pool_id", "test-provider_name", )
    mock_client.call.assert_called_once()


async def test_update_identity_provider_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_identity_provider("test-user_pool_id", "test-provider_name", )


async def test_update_identity_provider_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update identity provider"):
        await update_identity_provider("test-user_pool_id", "test-provider_name", )


async def test_update_managed_login_branding(mock_client):
    mock_client.call.return_value = {}
    await update_managed_login_branding()
    mock_client.call.assert_called_once()


async def test_update_managed_login_branding_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_managed_login_branding()


async def test_update_managed_login_branding_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update managed login branding"):
        await update_managed_login_branding()


async def test_update_resource_server(mock_client):
    mock_client.call.return_value = {}
    await update_resource_server("test-user_pool_id", "test-identifier", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_resource_server_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_resource_server("test-user_pool_id", "test-identifier", "test-name", )


async def test_update_resource_server_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update resource server"):
        await update_resource_server("test-user_pool_id", "test-identifier", "test-name", )


async def test_update_terms(mock_client):
    mock_client.call.return_value = {}
    await update_terms("test-terms_id", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_update_terms_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_terms("test-terms_id", "test-user_pool_id", )


async def test_update_terms_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update terms"):
        await update_terms("test-terms_id", "test-user_pool_id", )


async def test_update_user_attributes(mock_client):
    mock_client.call.return_value = {}
    await update_user_attributes([], "test-access_token", )
    mock_client.call.assert_called_once()


async def test_update_user_attributes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_attributes([], "test-access_token", )


async def test_update_user_attributes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update user attributes"):
        await update_user_attributes([], "test-access_token", )


async def test_update_user_pool(mock_client):
    mock_client.call.return_value = {}
    await update_user_pool("test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_update_user_pool_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_pool("test-user_pool_id", )


async def test_update_user_pool_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update user pool"):
        await update_user_pool("test-user_pool_id", )


async def test_update_user_pool_client(mock_client):
    mock_client.call.return_value = {}
    await update_user_pool_client("test-user_pool_id", "test-client_id", )
    mock_client.call.assert_called_once()


async def test_update_user_pool_client_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_pool_client("test-user_pool_id", "test-client_id", )


async def test_update_user_pool_client_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update user pool client"):
        await update_user_pool_client("test-user_pool_id", "test-client_id", )


async def test_update_user_pool_domain(mock_client):
    mock_client.call.return_value = {}
    await update_user_pool_domain("test-domain", "test-user_pool_id", )
    mock_client.call.assert_called_once()


async def test_update_user_pool_domain_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_user_pool_domain("test-domain", "test-user_pool_id", )


async def test_update_user_pool_domain_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update user pool domain"):
        await update_user_pool_domain("test-domain", "test-user_pool_id", )


async def test_verify_software_token(mock_client):
    mock_client.call.return_value = {}
    await verify_software_token("test-user_code", )
    mock_client.call.assert_called_once()


async def test_verify_software_token_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await verify_software_token("test-user_code", )


async def test_verify_software_token_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to verify software token"):
        await verify_software_token("test-user_code", )


async def test_verify_user_attribute(mock_client):
    mock_client.call.return_value = {}
    await verify_user_attribute("test-access_token", "test-attribute_name", "test-code", )
    mock_client.call.assert_called_once()


async def test_verify_user_attribute_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await verify_user_attribute("test-access_token", "test-attribute_name", "test-code", )


async def test_verify_user_attribute_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to verify user attribute"):
        await verify_user_attribute("test-access_token", "test-attribute_name", "test-code", )


@pytest.mark.asyncio
async def test_admin_confirm_sign_up_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_confirm_sign_up
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_confirm_sign_up("test-user_pool_id", "test-username", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_list_devices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_list_devices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_list_devices("test-user_pool_id", "test-username", limit=1, pagination_token="test-pagination_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_list_groups_for_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_list_groups_for_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_list_groups_for_user("test-username", "test-user_pool_id", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_list_user_auth_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_list_user_auth_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_list_user_auth_events("test-user_pool_id", "test-username", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_reset_user_password_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_reset_user_password
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_reset_user_password("test-user_pool_id", "test-username", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_respond_to_auth_challenge_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_respond_to_auth_challenge
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_respond_to_auth_challenge("test-user_pool_id", "test-client_id", "test-challenge_name", challenge_responses="test-challenge_responses", session="test-session", analytics_metadata="test-analytics_metadata", context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_set_user_mfa_preference_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_set_user_mfa_preference
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_set_user_mfa_preference("test-username", "test-user_pool_id", sms_mfa_settings={}, software_token_mfa_settings={}, email_mfa_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_update_device_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_update_device_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_update_device_status("test-user_pool_id", "test-username", "test-device_key", device_remembered_status="test-device_remembered_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_admin_update_user_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import admin_update_user_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await admin_update_user_attributes("test-user_pool_id", "test-username", "test-user_attributes", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_software_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import associate_software_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await associate_software_token(access_token="test-access_token", session="test-session", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_change_password_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import change_password
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await change_password("test-proposed_password", "test-access_token", previous_password="test-previous_password", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_confirm_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import confirm_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await confirm_device("test-access_token", "test-device_key", device_secret_verifier_config={}, device_name="test-device_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_confirm_forgot_password_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import confirm_forgot_password
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await confirm_forgot_password("test-client_id", "test-username", True, "test-password", secret_hash="test-secret_hash", analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_confirm_sign_up_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import confirm_sign_up
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await confirm_sign_up("test-client_id", "test-username", True, secret_hash="test-secret_hash", force_alias_creation=True, analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", session="test-session", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_group("test-group_name", "test-user_pool_id", description="test-description", role_arn="test-role_arn", precedence="test-precedence", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_identity_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_identity_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_identity_provider("test-user_pool_id", "test-provider_name", "test-provider_type", "test-provider_details", attribute_mapping={}, idp_identifiers="test-idp_identifiers", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_managed_login_branding_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_managed_login_branding
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_managed_login_branding("test-user_pool_id", "test-client_id", use_cognito_provided_values=True, settings={}, assets="test-assets", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_resource_server_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_resource_server
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_resource_server("test-user_pool_id", "test-identifier", "test-name", scopes="test-scopes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_terms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_terms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_terms("test-user_pool_id", "test-client_id", "test-terms_name", "test-terms_source", "test-enforcement", links="test-links", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_user_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_user_pool("test-pool_name", policies="test-policies", deletion_protection="test-deletion_protection", lambda_config={}, auto_verified_attributes=True, alias_attributes="test-alias_attributes", username_attributes="test-username_attributes", sms_verification_message="test-sms_verification_message", email_verification_message="test-email_verification_message", email_verification_subject="test-email_verification_subject", verification_message_template="test-verification_message_template", sms_authentication_message="test-sms_authentication_message", mfa_configuration={}, user_attribute_update_settings={}, device_configuration={}, email_configuration={}, sms_configuration={}, user_pool_tags=[{"Key": "k", "Value": "v"}], admin_create_user_config={}, schema="test-schema", user_pool_add_ons="test-user_pool_add_ons", username_configuration={}, account_recovery_setting=1, user_pool_tier="test-user_pool_tier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_pool_client_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_user_pool_client
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_user_pool_client("test-user_pool_id", "test-client_name", generate_secret="test-generate_secret", refresh_token_validity="test-refresh_token_validity", access_token_validity="test-access_token_validity", id_token_validity="test-id_token_validity", token_validity_units="test-token_validity_units", read_attributes="test-read_attributes", write_attributes="test-write_attributes", explicit_auth_flows="test-explicit_auth_flows", supported_identity_providers=1, callback_ur_ls="test-callback_ur_ls", logout_ur_ls="test-logout_ur_ls", default_redirect_uri="test-default_redirect_uri", allowed_o_auth_flows=True, allowed_o_auth_scopes=True, allowed_o_auth_flows_user_pool_client=True, analytics_configuration={}, prevent_user_existence_errors="test-prevent_user_existence_errors", enable_token_revocation=True, enable_propagate_additional_user_context_data=True, auth_session_validity="test-auth_session_validity", refresh_token_rotation="test-refresh_token_rotation", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_pool_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import create_user_pool_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await create_user_pool_domain("test-domain", "test-user_pool_id", managed_login_version="test-managed_login_version", custom_domain_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_managed_login_branding_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import describe_managed_login_branding
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await describe_managed_login_branding("test-user_pool_id", "test-managed_login_branding_id", return_merged_resources="test-return_merged_resources", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_managed_login_branding_by_client_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import describe_managed_login_branding_by_client
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await describe_managed_login_branding_by_client("test-user_pool_id", "test-client_id", return_merged_resources="test-return_merged_resources", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_risk_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import describe_risk_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await describe_risk_configuration("test-user_pool_id", client_id="test-client_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_forget_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import forget_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await forget_device("test-device_key", access_token="test-access_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_forgot_password_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import forgot_password
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await forgot_password("test-client_id", "test-username", secret_hash="test-secret_hash", user_context_data={}, analytics_metadata="test-analytics_metadata", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_device_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import get_device
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await get_device("test-device_key", access_token="test-access_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_tokens_from_refresh_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import get_tokens_from_refresh_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await get_tokens_from_refresh_token("test-refresh_token", "test-client_id", client_secret="test-client_secret", device_key="test-device_key", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_ui_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import get_ui_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await get_ui_customization("test-user_pool_id", client_id="test-client_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_user_attribute_verification_code_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import get_user_attribute_verification_code
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await get_user_attribute_verification_code("test-access_token", "test-attribute_name", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_initiate_auth_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import initiate_auth
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await initiate_auth("test-auth_flow", "test-client_id", auth_parameters="test-auth_parameters", client_metadata="test-client_metadata", analytics_metadata="test-analytics_metadata", user_context_data={}, session="test-session", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_devices_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_devices
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_devices("test-access_token", limit=1, pagination_token="test-pagination_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_groups("test-user_pool_id", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_identity_providers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_identity_providers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_identity_providers("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_resource_servers_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_resource_servers
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_resource_servers("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_terms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_terms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_terms("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_import_jobs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_user_import_jobs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_user_import_jobs("test-user_pool_id", 1, pagination_token="test-pagination_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_user_pool_clients_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_user_pool_clients
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_user_pool_clients("test-user_pool_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_users_in_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_users_in_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_users_in_group("test-user_pool_id", "test-group_name", limit=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_web_authn_credentials_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import list_web_authn_credentials
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await list_web_authn_credentials("test-access_token", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_resend_confirmation_code_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import resend_confirmation_code
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await resend_confirmation_code("test-client_id", "test-username", secret_hash="test-secret_hash", user_context_data={}, analytics_metadata="test-analytics_metadata", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_respond_to_auth_challenge_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import respond_to_auth_challenge
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await respond_to_auth_challenge("test-client_id", "test-challenge_name", session="test-session", challenge_responses="test-challenge_responses", analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import revoke_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await revoke_token("test-token", "test-client_id", client_secret="test-client_secret", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_risk_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import set_risk_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await set_risk_configuration("test-user_pool_id", client_id="test-client_id", compromised_credentials_risk_configuration={}, account_takeover_risk_configuration=1, risk_exception_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_ui_customization_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import set_ui_customization
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await set_ui_customization("test-user_pool_id", client_id="test-client_id", css="test-css", image_file="test-image_file", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_user_mfa_preference_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import set_user_mfa_preference
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await set_user_mfa_preference("test-access_token", sms_mfa_settings={}, software_token_mfa_settings={}, email_mfa_settings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_user_pool_mfa_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import set_user_pool_mfa_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await set_user_pool_mfa_config("test-user_pool_id", sms_mfa_configuration={}, software_token_mfa_configuration={}, email_mfa_configuration={}, mfa_configuration={}, web_authn_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_sign_up_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import sign_up
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await sign_up("test-client_id", "test-username", secret_hash="test-secret_hash", password="test-password", user_attributes="test-user_attributes", validation_data="test-validation_data", analytics_metadata="test-analytics_metadata", user_context_data={}, client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_device_status_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_device_status
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_device_status("test-access_token", "test-device_key", device_remembered_status="test-device_remembered_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_group("test-group_name", "test-user_pool_id", description="test-description", role_arn="test-role_arn", precedence="test-precedence", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_identity_provider_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_identity_provider
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_identity_provider("test-user_pool_id", "test-provider_name", provider_details="test-provider_details", attribute_mapping={}, idp_identifiers="test-idp_identifiers", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_managed_login_branding_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_managed_login_branding
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_managed_login_branding(user_pool_id="test-user_pool_id", managed_login_branding_id="test-managed_login_branding_id", use_cognito_provided_values=True, settings={}, assets="test-assets", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_resource_server_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_resource_server
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_resource_server("test-user_pool_id", "test-identifier", "test-name", scopes="test-scopes", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_terms_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_terms
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_terms("test-terms_id", "test-user_pool_id", terms_name="test-terms_name", terms_source="test-terms_source", enforcement="test-enforcement", links="test-links", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_attributes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_user_attributes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_user_attributes("test-user_attributes", "test-access_token", client_metadata="test-client_metadata", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_user_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_user_pool("test-user_pool_id", policies="test-policies", deletion_protection="test-deletion_protection", lambda_config={}, auto_verified_attributes=True, sms_verification_message="test-sms_verification_message", email_verification_message="test-email_verification_message", email_verification_subject="test-email_verification_subject", verification_message_template="test-verification_message_template", sms_authentication_message="test-sms_authentication_message", user_attribute_update_settings={}, mfa_configuration={}, device_configuration={}, email_configuration={}, sms_configuration={}, user_pool_tags=[{"Key": "k", "Value": "v"}], admin_create_user_config={}, user_pool_add_ons="test-user_pool_add_ons", account_recovery_setting=1, pool_name="test-pool_name", user_pool_tier="test-user_pool_tier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_pool_client_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_user_pool_client
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_user_pool_client("test-user_pool_id", "test-client_id", client_name="test-client_name", refresh_token_validity="test-refresh_token_validity", access_token_validity="test-access_token_validity", id_token_validity="test-id_token_validity", token_validity_units="test-token_validity_units", read_attributes="test-read_attributes", write_attributes="test-write_attributes", explicit_auth_flows="test-explicit_auth_flows", supported_identity_providers=1, callback_ur_ls="test-callback_ur_ls", logout_ur_ls="test-logout_ur_ls", default_redirect_uri="test-default_redirect_uri", allowed_o_auth_flows=True, allowed_o_auth_scopes=True, allowed_o_auth_flows_user_pool_client=True, analytics_configuration={}, prevent_user_existence_errors="test-prevent_user_existence_errors", enable_token_revocation=True, enable_propagate_additional_user_context_data=True, auth_session_validity="test-auth_session_validity", refresh_token_rotation="test-refresh_token_rotation", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_user_pool_domain_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import update_user_pool_domain
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await update_user_pool_domain("test-domain", "test-user_pool_id", managed_login_version="test-managed_login_version", custom_domain_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_verify_software_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito import verify_software_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito.async_client", lambda *a, **kw: mock_client)
    await verify_software_token("test-user_code", access_token="test-access_token", session="test-session", friendly_device_name="test-friendly_device_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
