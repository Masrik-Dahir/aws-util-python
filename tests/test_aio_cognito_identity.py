"""Tests for aws_util.aio.cognito_identity -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.cognito_identity import (
    CredentialsResult,
    IdentityPoolResult,
    IdentityResult,
    OpenIdTokenResult,
    create_identity_pool,
    delete_identities,
    delete_identity_pool,
    describe_identity,
    describe_identity_pool,
    get_credentials_for_identity,
    get_id,
    get_open_id_token,
    list_identities,
    list_identity_pools,
    update_identity_pool,
    get_identity_pool_roles,
    get_open_id_token_for_developer_identity,
    get_principal_tag_attribute_map,
    list_tags_for_resource,
    lookup_developer_identity,
    merge_developer_identities,
    set_identity_pool_roles,
    set_principal_tag_attribute_map,
    tag_resource,
    unlink_developer_identity,
    unlink_identity,
    untag_resource,
)

POOL_ID = "us-east-1:abc-123"
IDENTITY_ID = "us-east-1:id-456"


def _mock_factory(mc):
    return lambda *a, **kw: mc


def _pool_resp(**kw):
    d = {
        "IdentityPoolId": POOL_ID,
        "IdentityPoolName": "mypool",
        "AllowUnauthenticatedIdentities": False,
    }
    d.update(kw)
    return d


def _identity_resp(**kw):
    d = {"IdentityId": IDENTITY_ID}
    d.update(kw)
    return d


# ---------------------------------------------------------------------------
# Identity Pool CRUD
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_identity_pool_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = _pool_resp()
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await create_identity_pool("mypool")
    assert isinstance(r, IdentityPoolResult)


@pytest.mark.asyncio
async def test_create_identity_pool_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = _pool_resp()
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await create_identity_pool(
        "mypool", True,
        supported_login_providers={"p": "id"},
        developer_provider_name="dev",
        open_id_connect_provider_arns=["arn:oidc"],
        cognito_identity_providers=[{"ProviderName": "p"}],
        saml_provider_arns=["arn:saml"],
        tags={"k": "v"},
    )
    assert isinstance(r, IdentityPoolResult)


@pytest.mark.asyncio
async def test_create_identity_pool_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_identity_pool("mypool")


@pytest.mark.asyncio
async def test_describe_identity_pool_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = _pool_resp()
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await describe_identity_pool(POOL_ID)
    assert isinstance(r, IdentityPoolResult)


@pytest.mark.asyncio
async def test_describe_identity_pool_not_found(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("ResourceNotFoundException: not found")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await describe_identity_pool(POOL_ID)
    assert r is None


@pytest.mark.asyncio
async def test_describe_identity_pool_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("SomeOtherError")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_identity_pool(POOL_ID)


@pytest.mark.asyncio
async def test_list_identity_pools_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "IdentityPools": [
            {"IdentityPoolId": POOL_ID, "IdentityPoolName": "mypool"},
        ],
    }
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await list_identity_pools()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_identity_pools_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {
            "IdentityPools": [
                {"IdentityPoolId": "p1", "IdentityPoolName": "pool1"},
            ],
            "NextToken": "tok",
        },
        {
            "IdentityPools": [
                {"IdentityPoolId": "p2", "IdentityPoolName": "pool2"},
            ],
        },
    ]
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await list_identity_pools()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_identity_pools_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_identity_pools()


@pytest.mark.asyncio
async def test_update_identity_pool_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = _pool_resp()
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await update_identity_pool(POOL_ID, "mypool")
    assert isinstance(r, IdentityPoolResult)


@pytest.mark.asyncio
async def test_update_identity_pool_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = _pool_resp()
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await update_identity_pool(
        POOL_ID, "mypool", True,
        supported_login_providers={"p": "id"},
        developer_provider_name="dev",
        open_id_connect_provider_arns=["arn:oidc"],
        cognito_identity_providers=[{"ProviderName": "p"}],
        saml_provider_arns=["arn:saml"],
    )
    assert isinstance(r, IdentityPoolResult)


@pytest.mark.asyncio
async def test_update_identity_pool_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await update_identity_pool(POOL_ID, "mypool")


@pytest.mark.asyncio
async def test_delete_identity_pool_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    await delete_identity_pool(POOL_ID)
    mc.call.assert_called_once()


@pytest.mark.asyncio
async def test_delete_identity_pool_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_identity_pool(POOL_ID)


# ---------------------------------------------------------------------------
# Identity operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_id_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"IdentityId": IDENTITY_ID}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_id(POOL_ID)
    assert r == IDENTITY_ID


@pytest.mark.asyncio
async def test_get_id_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"IdentityId": IDENTITY_ID}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_id(POOL_ID, account_id="123", logins={"p": "tok"})
    assert r == IDENTITY_ID


@pytest.mark.asyncio
async def test_get_id_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_id(POOL_ID)


@pytest.mark.asyncio
async def test_get_credentials_for_identity_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "IdentityId": IDENTITY_ID,
        "Credentials": {
            "AccessKeyId": "AK",
            "SecretKey": "SK",
            "SessionToken": "ST",
            "Expiration": "2025-01-01",
        },
    }
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_credentials_for_identity(IDENTITY_ID)
    assert r.access_key_id == "AK"
    assert r.expiration == "2025-01-01"


@pytest.mark.asyncio
async def test_get_credentials_for_identity_no_expiration(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"IdentityId": IDENTITY_ID, "Credentials": {}}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_credentials_for_identity(IDENTITY_ID)
    assert r.expiration is None


@pytest.mark.asyncio
async def test_get_credentials_for_identity_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Credentials": {"Expiration": "2025"}}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_credentials_for_identity(
        IDENTITY_ID, logins={"p": "tok"}, custom_role_arn="arn:role",
    )
    assert isinstance(r, CredentialsResult)


@pytest.mark.asyncio
async def test_get_credentials_for_identity_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_credentials_for_identity(IDENTITY_ID)


@pytest.mark.asyncio
async def test_get_open_id_token_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"IdentityId": IDENTITY_ID, "Token": "tok"}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_open_id_token(IDENTITY_ID)
    assert r.token == "tok"


@pytest.mark.asyncio
async def test_get_open_id_token_with_logins(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"IdentityId": IDENTITY_ID, "Token": "tok"}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await get_open_id_token(IDENTITY_ID, logins={"p": "tok"})
    assert isinstance(r, OpenIdTokenResult)


@pytest.mark.asyncio
async def test_get_open_id_token_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_open_id_token(IDENTITY_ID)


@pytest.mark.asyncio
async def test_list_identities_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Identities": [_identity_resp()]}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await list_identities(POOL_ID)
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_identities_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Identities": [_identity_resp()], "NextToken": "tok"},
        {"Identities": [_identity_resp(IdentityId="id2")]},
    ]
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await list_identities(POOL_ID)
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_identities_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_identities(POOL_ID)


@pytest.mark.asyncio
async def test_describe_identity_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = _identity_resp()
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await describe_identity(IDENTITY_ID)
    assert isinstance(r, IdentityResult)


@pytest.mark.asyncio
async def test_describe_identity_not_found(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("ResourceNotFoundException: not found")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await describe_identity(IDENTITY_ID)
    assert r is None


@pytest.mark.asyncio
async def test_describe_identity_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("SomeOtherError")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await describe_identity(IDENTITY_ID)


@pytest.mark.asyncio
async def test_delete_identities_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"UnprocessedIdentityIds": []}
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    r = await delete_identities([IDENTITY_ID])
    assert r == []


@pytest.mark.asyncio
async def test_delete_identities_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_identities([IDENTITY_ID])


async def test_get_identity_pool_roles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_identity_pool_roles("test-identity_pool_id", )
    mock_client.call.assert_called_once()


async def test_get_identity_pool_roles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_identity_pool_roles("test-identity_pool_id", )


async def test_get_open_id_token_for_developer_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_open_id_token_for_developer_identity("test-identity_pool_id", {}, )
    mock_client.call.assert_called_once()


async def test_get_open_id_token_for_developer_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_open_id_token_for_developer_identity("test-identity_pool_id", {}, )


async def test_get_principal_tag_attribute_map(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", )
    mock_client.call.assert_called_once()


async def test_get_principal_tag_attribute_map_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_lookup_developer_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await lookup_developer_identity("test-identity_pool_id", )
    mock_client.call.assert_called_once()


async def test_lookup_developer_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await lookup_developer_identity("test-identity_pool_id", )


async def test_merge_developer_identities(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await merge_developer_identities("test-source_user_identifier", "test-destination_user_identifier", "test-developer_provider_name", "test-identity_pool_id", )
    mock_client.call.assert_called_once()


async def test_merge_developer_identities_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await merge_developer_identities("test-source_user_identifier", "test-destination_user_identifier", "test-developer_provider_name", "test-identity_pool_id", )


async def test_set_identity_pool_roles(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_identity_pool_roles("test-identity_pool_id", {}, )
    mock_client.call.assert_called_once()


async def test_set_identity_pool_roles_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_identity_pool_roles("test-identity_pool_id", {}, )


async def test_set_principal_tag_attribute_map(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await set_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", )
    mock_client.call.assert_called_once()


async def test_set_principal_tag_attribute_map_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await set_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_unlink_developer_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await unlink_developer_identity("test-identity_id", "test-identity_pool_id", "test-developer_provider_name", "test-developer_user_identifier", )
    mock_client.call.assert_called_once()


async def test_unlink_developer_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unlink_developer_identity("test-identity_id", "test-identity_pool_id", "test-developer_provider_name", "test-developer_user_identifier", )


async def test_unlink_identity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await unlink_identity("test-identity_id", {}, [], )
    mock_client.call.assert_called_once()


async def test_unlink_identity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await unlink_identity("test-identity_id", {}, [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.cognito_identity.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_create_identity_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import create_identity_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await create_identity_pool("test-identity_pool_name", supported_login_providers=1, developer_provider_name="test-developer_provider_name", open_id_connect_provider_arns="test-open_id_connect_provider_arns", cognito_identity_providers="test-cognito_identity_providers", saml_provider_arns="test-saml_provider_arns", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_identity_pool_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import update_identity_pool
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await update_identity_pool("test-identity_pool_id", "test-identity_pool_name", supported_login_providers=1, developer_provider_name="test-developer_provider_name", open_id_connect_provider_arns="test-open_id_connect_provider_arns", cognito_identity_providers="test-cognito_identity_providers", saml_provider_arns="test-saml_provider_arns", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_id_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import get_id
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await get_id("test-identity_pool_id", account_id=1, logins="test-logins", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_credentials_for_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import get_credentials_for_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await get_credentials_for_identity("test-identity_id", logins="test-logins", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_open_id_token_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import get_open_id_token
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await get_open_id_token("test-identity_id", logins="test-logins", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_open_id_token_for_developer_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import get_open_id_token_for_developer_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await get_open_id_token_for_developer_identity("test-identity_pool_id", "test-logins", identity_id="test-identity_id", principal_tags=[{"Key": "k", "Value": "v"}], token_duration=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_lookup_developer_identity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import lookup_developer_identity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await lookup_developer_identity("test-identity_pool_id", identity_id="test-identity_id", developer_user_identifier="test-developer_user_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_identity_pool_roles_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import set_identity_pool_roles
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await set_identity_pool_roles("test-identity_pool_id", "test-roles", role_mappings={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_set_principal_tag_attribute_map_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.cognito_identity import set_principal_tag_attribute_map
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.cognito_identity.async_client", lambda *a, **kw: mock_client)
    await set_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", use_defaults=True, principal_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()
