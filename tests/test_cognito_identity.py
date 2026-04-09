"""Tests for aws_util.cognito_identity -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.cognito_identity import (
    CredentialsResult,
    IdentityPoolResult,
    IdentityResult,
    OpenIdTokenResult,
    _parse_identity,
    _parse_identity_pool,
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


def _ce(code: str = "SomeError", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "Op")


def _rnf() -> ClientError:
    return ClientError(
        {"Error": {"Code": "ResourceNotFoundException", "Message": "not found"}},
        "Op",
    )


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
# Parsers
# ---------------------------------------------------------------------------


class TestParseIdentityPool:
    def test_minimal(self):
        r = _parse_identity_pool(_pool_resp())
        assert isinstance(r, IdentityPoolResult)
        assert r.identity_pool_id == POOL_ID

    def test_full(self):
        r = _parse_identity_pool(_pool_resp(
            AllowClassicFlow=True,
            SupportedLoginProviders={"provider": "id"},
            DeveloperProviderName="dev",
            OpenIdConnectProviderARNs=["arn:oidc"],
            CognitoIdentityProviders=[{"ProviderName": "p"}],
            SamlProviderARNs=["arn:saml"],
            IdentityPoolTags={"k": "v"},
            CustomField="x",
        ))
        assert r.allow_classic_flow is True
        assert r.supported_login_providers == {"provider": "id"}
        assert r.developer_provider_name == "dev"
        assert len(r.open_id_connect_provider_arns) == 1
        assert len(r.cognito_identity_providers) == 1
        assert len(r.saml_provider_arns) == 1
        assert r.identity_pool_tags == {"k": "v"}
        assert "CustomField" in r.extra


class TestParseIdentity:
    def test_minimal(self):
        r = _parse_identity(_identity_resp())
        assert isinstance(r, IdentityResult)
        assert r.identity_id == IDENTITY_ID

    def test_full(self):
        r = _parse_identity(_identity_resp(
            Logins=["provider"],
            CreationDate="2024-01-01",
            LastModifiedDate="2024-06-01",
            CustomField="x",
        ))
        assert r.logins == ["provider"]
        assert r.creation_date == "2024-01-01"
        assert r.last_modified_date == "2024-06-01"
        assert "CustomField" in r.extra


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_credentials_result(self):
        r = CredentialsResult(identity_id="id")
        assert r.access_key_id == ""
        assert r.expiration is None

    def test_open_id_token_result(self):
        r = OpenIdTokenResult(identity_id="id")
        assert r.token == ""


# ---------------------------------------------------------------------------
# Identity Pool CRUD
# ---------------------------------------------------------------------------


class TestCreateIdentityPool:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_identity_pool.return_value = _pool_resp()
        r = create_identity_pool("mypool")
        assert isinstance(r, IdentityPoolResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_identity_pool.return_value = _pool_resp()
        r = create_identity_pool(
            "mypool", True,
            supported_login_providers={"p": "id"},
            developer_provider_name="dev",
            open_id_connect_provider_arns=["arn:oidc"],
            cognito_identity_providers=[{"ProviderName": "p"}],
            saml_provider_arns=["arn:saml"],
            tags={"k": "v"},
        )
        assert isinstance(r, IdentityPoolResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_identity_pool.side_effect = _ce()
        with pytest.raises(Exception):
            create_identity_pool("mypool")


class TestDescribeIdentityPool:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_identity_pool.return_value = _pool_resp()
        r = describe_identity_pool(POOL_ID)
        assert isinstance(r, IdentityPoolResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_not_found(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_identity_pool.side_effect = _rnf()
        r = describe_identity_pool(POOL_ID)
        assert r is None

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_identity_pool.side_effect = _ce()
        with pytest.raises(Exception):
            describe_identity_pool(POOL_ID)


class TestListIdentityPools:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_identity_pools.return_value = {
            "IdentityPools": [
                {"IdentityPoolId": POOL_ID, "IdentityPoolName": "mypool"},
            ],
        }
        r = list_identity_pools()
        assert len(r) == 1

    @patch("aws_util.cognito_identity.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_identity_pools.side_effect = [
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
        r = list_identity_pools()
        assert len(r) == 2

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_identity_pools.side_effect = _ce()
        with pytest.raises(Exception):
            list_identity_pools()


class TestUpdateIdentityPool:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.update_identity_pool.return_value = _pool_resp()
        r = update_identity_pool(POOL_ID, "mypool")
        assert isinstance(r, IdentityPoolResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.update_identity_pool.return_value = _pool_resp()
        r = update_identity_pool(
            POOL_ID, "mypool", True,
            supported_login_providers={"p": "id"},
            developer_provider_name="dev",
            open_id_connect_provider_arns=["arn:oidc"],
            cognito_identity_providers=[{"ProviderName": "p"}],
            saml_provider_arns=["arn:saml"],
        )
        assert isinstance(r, IdentityPoolResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.update_identity_pool.side_effect = _ce()
        with pytest.raises(Exception):
            update_identity_pool(POOL_ID, "mypool")


class TestDeleteIdentityPool:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_identity_pool.return_value = {}
        delete_identity_pool(POOL_ID)
        client.delete_identity_pool.assert_called_once()

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_identity_pool.side_effect = _ce()
        with pytest.raises(Exception):
            delete_identity_pool(POOL_ID)


# ---------------------------------------------------------------------------
# Identity operations
# ---------------------------------------------------------------------------


class TestGetId:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_id.return_value = {"IdentityId": IDENTITY_ID}
        r = get_id(POOL_ID)
        assert r == IDENTITY_ID

    @patch("aws_util.cognito_identity.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_id.return_value = {"IdentityId": IDENTITY_ID}
        r = get_id(POOL_ID, account_id="123", logins={"p": "tok"})
        assert r == IDENTITY_ID

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_id.side_effect = _ce()
        with pytest.raises(Exception):
            get_id(POOL_ID)


class TestGetCredentialsForIdentity:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_credentials_for_identity.return_value = {
            "IdentityId": IDENTITY_ID,
            "Credentials": {
                "AccessKeyId": "AK",
                "SecretKey": "SK",
                "SessionToken": "ST",
                "Expiration": "2025-01-01",
            },
        }
        r = get_credentials_for_identity(IDENTITY_ID)
        assert r.access_key_id == "AK"
        assert r.expiration == "2025-01-01"

    @patch("aws_util.cognito_identity.get_client")
    def test_no_expiration(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_credentials_for_identity.return_value = {
            "IdentityId": IDENTITY_ID,
            "Credentials": {},
        }
        r = get_credentials_for_identity(IDENTITY_ID)
        assert r.expiration is None

    @patch("aws_util.cognito_identity.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_credentials_for_identity.return_value = {
            "Credentials": {"Expiration": "2025-01-01"},
        }
        r = get_credentials_for_identity(
            IDENTITY_ID, logins={"p": "tok"}, custom_role_arn="arn:role",
        )
        assert isinstance(r, CredentialsResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_credentials_for_identity.side_effect = _ce()
        with pytest.raises(Exception):
            get_credentials_for_identity(IDENTITY_ID)


class TestGetOpenIdToken:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_open_id_token.return_value = {
            "IdentityId": IDENTITY_ID,
            "Token": "tok",
        }
        r = get_open_id_token(IDENTITY_ID)
        assert r.token == "tok"

    @patch("aws_util.cognito_identity.get_client")
    def test_with_logins(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_open_id_token.return_value = {
            "IdentityId": IDENTITY_ID,
            "Token": "tok",
        }
        r = get_open_id_token(IDENTITY_ID, logins={"p": "tok"})
        assert isinstance(r, OpenIdTokenResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_open_id_token.side_effect = _ce()
        with pytest.raises(Exception):
            get_open_id_token(IDENTITY_ID)


class TestListIdentities:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_identities.return_value = {
            "Identities": [_identity_resp()],
        }
        r = list_identities(POOL_ID)
        assert len(r) == 1

    @patch("aws_util.cognito_identity.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_identities.side_effect = [
            {"Identities": [_identity_resp()], "NextToken": "tok"},
            {"Identities": [_identity_resp(IdentityId="id2")]},
        ]
        r = list_identities(POOL_ID)
        assert len(r) == 2

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_identities.side_effect = _ce()
        with pytest.raises(Exception):
            list_identities(POOL_ID)


class TestDescribeIdentity:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_identity.return_value = _identity_resp()
        r = describe_identity(IDENTITY_ID)
        assert isinstance(r, IdentityResult)

    @patch("aws_util.cognito_identity.get_client")
    def test_not_found(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_identity.side_effect = _rnf()
        r = describe_identity(IDENTITY_ID)
        assert r is None

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.describe_identity.side_effect = _ce()
        with pytest.raises(Exception):
            describe_identity(IDENTITY_ID)


class TestDeleteIdentities:
    @patch("aws_util.cognito_identity.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_identities.return_value = {"UnprocessedIdentityIds": []}
        r = delete_identities([IDENTITY_ID])
        assert r == []

    @patch("aws_util.cognito_identity.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_identities.side_effect = _ce()
        with pytest.raises(Exception):
            delete_identities([IDENTITY_ID])


REGION = "us-east-1"


@patch("aws_util.cognito_identity.get_client")
def test_get_identity_pool_roles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_identity_pool_roles.return_value = {}
    get_identity_pool_roles("test-identity_pool_id", region_name=REGION)
    mock_client.get_identity_pool_roles.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_get_identity_pool_roles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_identity_pool_roles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_pool_roles",
    )
    with pytest.raises(RuntimeError, match="Failed to get identity pool roles"):
        get_identity_pool_roles("test-identity_pool_id", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_get_open_id_token_for_developer_identity(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_open_id_token_for_developer_identity.return_value = {}
    get_open_id_token_for_developer_identity("test-identity_pool_id", {}, region_name=REGION)
    mock_client.get_open_id_token_for_developer_identity.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_get_open_id_token_for_developer_identity_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_open_id_token_for_developer_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_open_id_token_for_developer_identity",
    )
    with pytest.raises(RuntimeError, match="Failed to get open id token for developer identity"):
        get_open_id_token_for_developer_identity("test-identity_pool_id", {}, region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_get_principal_tag_attribute_map(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_principal_tag_attribute_map.return_value = {}
    get_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", region_name=REGION)
    mock_client.get_principal_tag_attribute_map.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_get_principal_tag_attribute_map_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_principal_tag_attribute_map.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_principal_tag_attribute_map",
    )
    with pytest.raises(RuntimeError, match="Failed to get principal tag attribute map"):
        get_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_lookup_developer_identity(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.lookup_developer_identity.return_value = {}
    lookup_developer_identity("test-identity_pool_id", region_name=REGION)
    mock_client.lookup_developer_identity.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_lookup_developer_identity_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.lookup_developer_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "lookup_developer_identity",
    )
    with pytest.raises(RuntimeError, match="Failed to lookup developer identity"):
        lookup_developer_identity("test-identity_pool_id", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_merge_developer_identities(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_developer_identities.return_value = {}
    merge_developer_identities("test-source_user_identifier", "test-destination_user_identifier", "test-developer_provider_name", "test-identity_pool_id", region_name=REGION)
    mock_client.merge_developer_identities.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_merge_developer_identities_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.merge_developer_identities.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "merge_developer_identities",
    )
    with pytest.raises(RuntimeError, match="Failed to merge developer identities"):
        merge_developer_identities("test-source_user_identifier", "test-destination_user_identifier", "test-developer_provider_name", "test-identity_pool_id", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_set_identity_pool_roles(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_identity_pool_roles.return_value = {}
    set_identity_pool_roles("test-identity_pool_id", {}, region_name=REGION)
    mock_client.set_identity_pool_roles.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_set_identity_pool_roles_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_identity_pool_roles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_identity_pool_roles",
    )
    with pytest.raises(RuntimeError, match="Failed to set identity pool roles"):
        set_identity_pool_roles("test-identity_pool_id", {}, region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_set_principal_tag_attribute_map(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_principal_tag_attribute_map.return_value = {}
    set_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", region_name=REGION)
    mock_client.set_principal_tag_attribute_map.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_set_principal_tag_attribute_map_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.set_principal_tag_attribute_map.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "set_principal_tag_attribute_map",
    )
    with pytest.raises(RuntimeError, match="Failed to set principal tag attribute map"):
        set_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_unlink_developer_identity(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.unlink_developer_identity.return_value = {}
    unlink_developer_identity("test-identity_id", "test-identity_pool_id", "test-developer_provider_name", "test-developer_user_identifier", region_name=REGION)
    mock_client.unlink_developer_identity.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_unlink_developer_identity_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.unlink_developer_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unlink_developer_identity",
    )
    with pytest.raises(RuntimeError, match="Failed to unlink developer identity"):
        unlink_developer_identity("test-identity_id", "test-identity_pool_id", "test-developer_provider_name", "test-developer_user_identifier", region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_unlink_identity(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.unlink_identity.return_value = {}
    unlink_identity("test-identity_id", {}, [], region_name=REGION)
    mock_client.unlink_identity.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_unlink_identity_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.unlink_identity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "unlink_identity",
    )
    with pytest.raises(RuntimeError, match="Failed to unlink identity"):
        unlink_identity("test-identity_id", {}, [], region_name=REGION)


@patch("aws_util.cognito_identity.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.cognito_identity.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_create_identity_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import create_identity_pool
    mock_client = MagicMock()
    mock_client.create_identity_pool.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    create_identity_pool("test-identity_pool_name", supported_login_providers=1, developer_provider_name="test-developer_provider_name", open_id_connect_provider_arns="test-open_id_connect_provider_arns", cognito_identity_providers="test-cognito_identity_providers", saml_provider_arns="test-saml_provider_arns", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_identity_pool.assert_called_once()

def test_update_identity_pool_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import update_identity_pool
    mock_client = MagicMock()
    mock_client.update_identity_pool.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    update_identity_pool("test-identity_pool_id", "test-identity_pool_name", supported_login_providers=1, developer_provider_name="test-developer_provider_name", open_id_connect_provider_arns="test-open_id_connect_provider_arns", cognito_identity_providers="test-cognito_identity_providers", saml_provider_arns="test-saml_provider_arns", region_name="us-east-1")
    mock_client.update_identity_pool.assert_called_once()

def test_get_id_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import get_id
    mock_client = MagicMock()
    mock_client.get_id.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    get_id("test-identity_pool_id", account_id=1, logins="test-logins", region_name="us-east-1")
    mock_client.get_id.assert_called_once()

def test_get_credentials_for_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import get_credentials_for_identity
    mock_client = MagicMock()
    mock_client.get_credentials_for_identity.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    get_credentials_for_identity("test-identity_id", logins="test-logins", custom_role_arn="test-custom_role_arn", region_name="us-east-1")
    mock_client.get_credentials_for_identity.assert_called_once()

def test_get_open_id_token_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import get_open_id_token
    mock_client = MagicMock()
    mock_client.get_open_id_token.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    get_open_id_token("test-identity_id", logins="test-logins", region_name="us-east-1")
    mock_client.get_open_id_token.assert_called_once()

def test_get_open_id_token_for_developer_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import get_open_id_token_for_developer_identity
    mock_client = MagicMock()
    mock_client.get_open_id_token_for_developer_identity.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    get_open_id_token_for_developer_identity("test-identity_pool_id", "test-logins", identity_id="test-identity_id", principal_tags=[{"Key": "k", "Value": "v"}], token_duration=1, region_name="us-east-1")
    mock_client.get_open_id_token_for_developer_identity.assert_called_once()

def test_lookup_developer_identity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import lookup_developer_identity
    mock_client = MagicMock()
    mock_client.lookup_developer_identity.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    lookup_developer_identity("test-identity_pool_id", identity_id="test-identity_id", developer_user_identifier="test-developer_user_identifier", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.lookup_developer_identity.assert_called_once()

def test_set_identity_pool_roles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import set_identity_pool_roles
    mock_client = MagicMock()
    mock_client.set_identity_pool_roles.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    set_identity_pool_roles("test-identity_pool_id", "test-roles", role_mappings={}, region_name="us-east-1")
    mock_client.set_identity_pool_roles.assert_called_once()

def test_set_principal_tag_attribute_map_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.cognito_identity import set_principal_tag_attribute_map
    mock_client = MagicMock()
    mock_client.set_principal_tag_attribute_map.return_value = {}
    monkeypatch.setattr("aws_util.cognito_identity.get_client", lambda *a, **kw: mock_client)
    set_principal_tag_attribute_map("test-identity_pool_id", "test-identity_provider_name", use_defaults=True, principal_tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.set_principal_tag_attribute_map.assert_called_once()
