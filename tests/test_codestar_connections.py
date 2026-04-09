"""Tests for aws_util.codestar_connections -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.codestar_connections import (
    ConnectionResult,
    HostResult,
    TagResult,
    _parse_connection,
    _parse_host,
    create_connection,
    create_host,
    delete_connection,
    delete_host,
    get_connection,
    get_host,
    list_connections,
    list_hosts,
    list_tags_for_resource,
    tag_resource,
    create_repository_link,
    create_sync_configuration,
    delete_repository_link,
    delete_sync_configuration,
    get_repository_link,
    get_repository_sync_status,
    get_resource_sync_status,
    get_sync_blocker_summary,
    get_sync_configuration,
    list_repository_links,
    list_repository_sync_definitions,
    list_sync_configurations,
    untag_resource,
    update_host,
    update_repository_link,
    update_sync_blocker,
    update_sync_configuration,
)

CONN_ARN = "arn:aws:codestar-connections:us-east-1:123:connection/abc"
HOST_ARN = "arn:aws:codestar-connections:us-east-1:123:host/abc"
RESOURCE_ARN = CONN_ARN


def _ce(code: str = "SomeError", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "Op")


def _conn_dict(**kw):
    d = {"ConnectionArn": CONN_ARN, "ConnectionName": "myconn"}
    d.update(kw)
    return d


def _host_dict(**kw):
    d = {"HostArn": HOST_ARN, "Name": "myhost"}
    d.update(kw)
    return d


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------


class TestParseConnection:
    def test_minimal(self):
        r = _parse_connection({"ConnectionArn": CONN_ARN})
        assert isinstance(r, ConnectionResult)
        assert r.connection_arn == CONN_ARN

    def test_full(self):
        r = _parse_connection(_conn_dict(
            ProviderType="GitHub", OwnerAccountId="123",
            ConnectionStatus="AVAILABLE", HostArn=HOST_ARN,
            Custom="x",
        ))
        assert r.provider_type == "GitHub"
        assert r.owner_account_id == "123"
        assert r.connection_status == "AVAILABLE"
        assert r.host_arn == HOST_ARN
        assert r.extra == {"Custom": "x"}


class TestParseHost:
    def test_minimal(self):
        r = _parse_host({"HostArn": HOST_ARN})
        assert isinstance(r, HostResult)
        assert r.host_arn == HOST_ARN

    def test_full(self):
        r = _parse_host(_host_dict(
            ProviderType="GitHubEnterpriseServer",
            ProviderEndpoint="https://ghe",
            Status="AVAILABLE",
            VpcConfiguration={"VpcId": "vpc-1"},
            Custom="x",
        ))
        assert r.provider_type == "GitHubEnterpriseServer"
        assert r.provider_endpoint == "https://ghe"
        assert r.status == "AVAILABLE"
        assert r.vpc_configuration == {"VpcId": "vpc-1"}
        assert r.extra == {"Custom": "x"}


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_tag_result(self):
        r = TagResult(key="k", value="v")
        assert r.key == "k"
        assert r.value == "v"


# ---------------------------------------------------------------------------
# Connection operations
# ---------------------------------------------------------------------------


class TestCreateConnection:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_connection.return_value = {"ConnectionArn": CONN_ARN}
        r = create_connection("myconn")
        assert r == CONN_ARN

    @patch("aws_util.codestar_connections.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_connection.return_value = {"ConnectionArn": CONN_ARN}
        r = create_connection(
            "myconn", provider_type="GitHub",
            tags=[{"Key": "k", "Value": "v"}],
            host_arn=HOST_ARN,
        )
        assert r == CONN_ARN

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_connection.side_effect = _ce()
        with pytest.raises(Exception):
            create_connection("myconn")


class TestGetConnection:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_connection.return_value = {"Connection": _conn_dict()}
        r = get_connection(CONN_ARN)
        assert isinstance(r, ConnectionResult)

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_connection.side_effect = _ce()
        with pytest.raises(Exception):
            get_connection(CONN_ARN)


class TestListConnections:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_connections.return_value = {
            "Connections": [_conn_dict()],
        }
        r = list_connections()
        assert len(r) == 1

    @patch("aws_util.codestar_connections.get_client")
    def test_with_filters(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_connections.return_value = {"Connections": []}
        r = list_connections(
            provider_type_filter="GitHub", host_arn_filter=HOST_ARN,
        )
        assert r == []

    @patch("aws_util.codestar_connections.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_connections.side_effect = [
            {"Connections": [_conn_dict()], "NextToken": "tok"},
            {"Connections": [_conn_dict(ConnectionName="c2")]},
        ]
        r = list_connections()
        assert len(r) == 2

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_connections.side_effect = _ce()
        with pytest.raises(Exception):
            list_connections()


class TestDeleteConnection:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_connection.return_value = {}
        delete_connection(CONN_ARN)
        client.delete_connection.assert_called_once()

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_connection.side_effect = _ce()
        with pytest.raises(Exception):
            delete_connection(CONN_ARN)


# ---------------------------------------------------------------------------
# Host operations
# ---------------------------------------------------------------------------


class TestCreateHost:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_host.return_value = {"HostArn": HOST_ARN}
        r = create_host("myhost", "GitHubEnterpriseServer", "https://ghe")
        assert r == HOST_ARN

    @patch("aws_util.codestar_connections.get_client")
    def test_all_opts(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_host.return_value = {"HostArn": HOST_ARN}
        r = create_host(
            "myhost", "GitHubEnterpriseServer", "https://ghe",
            vpc_configuration={"VpcId": "vpc-1"},
            tags=[{"Key": "k", "Value": "v"}],
        )
        assert r == HOST_ARN

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.create_host.side_effect = _ce()
        with pytest.raises(Exception):
            create_host("myhost", "GitHubEnterpriseServer", "https://ghe")


class TestGetHost:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_host.return_value = {
            "Name": "myhost",
            "ProviderType": "GitHubEnterpriseServer",
            "ProviderEndpoint": "https://ghe",
            "Status": "AVAILABLE",
            "VpcConfiguration": {"VpcId": "vpc-1"},
        }
        r = get_host(HOST_ARN)
        assert isinstance(r, HostResult)
        assert r.host_arn == HOST_ARN
        assert r.name == "myhost"

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.get_host.side_effect = _ce()
        with pytest.raises(Exception):
            get_host(HOST_ARN)


class TestListHosts:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_hosts.return_value = {"Hosts": [_host_dict()]}
        r = list_hosts()
        assert len(r) == 1

    @patch("aws_util.codestar_connections.get_client")
    def test_pagination(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_hosts.side_effect = [
            {"Hosts": [_host_dict()], "NextToken": "tok"},
            {"Hosts": [_host_dict(Name="h2")]},
        ]
        r = list_hosts()
        assert len(r) == 2

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_hosts.side_effect = _ce()
        with pytest.raises(Exception):
            list_hosts()


class TestDeleteHost:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_host.return_value = {}
        delete_host(HOST_ARN)
        client.delete_host.assert_called_once()

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.delete_host.side_effect = _ce()
        with pytest.raises(Exception):
            delete_host(HOST_ARN)


# ---------------------------------------------------------------------------
# Tag operations
# ---------------------------------------------------------------------------


class TestTagResource:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.tag_resource.return_value = {}
        tag_resource(RESOURCE_ARN, [{"Key": "k", "Value": "v"}])
        client.tag_resource.assert_called_once()

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.tag_resource.side_effect = _ce()
        with pytest.raises(Exception):
            tag_resource(RESOURCE_ARN, [{"Key": "k", "Value": "v"}])


class TestListTagsForResource:
    @patch("aws_util.codestar_connections.get_client")
    def test_success(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_tags_for_resource.return_value = {
            "Tags": [{"Key": "k", "Value": "v"}],
        }
        r = list_tags_for_resource(RESOURCE_ARN)
        assert len(r) == 1
        assert r[0].key == "k"

    @patch("aws_util.codestar_connections.get_client")
    def test_empty(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_tags_for_resource.return_value = {}
        r = list_tags_for_resource(RESOURCE_ARN)
        assert r == []

    @patch("aws_util.codestar_connections.get_client")
    def test_error(self, mock_gc):
        client = MagicMock()
        mock_gc.return_value = client
        client.list_tags_for_resource.side_effect = _ce()
        with pytest.raises(Exception):
            list_tags_for_resource(RESOURCE_ARN)


REGION = "us-east-1"


@patch("aws_util.codestar_connections.get_client")
def test_create_repository_link(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_repository_link.return_value = {}
    create_repository_link("test-connection_arn", "test-owner_id", "test-repository_name", region_name=REGION)
    mock_client.create_repository_link.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_create_repository_link_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_repository_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_repository_link",
    )
    with pytest.raises(RuntimeError, match="Failed to create repository link"):
        create_repository_link("test-connection_arn", "test-owner_id", "test-repository_name", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_create_sync_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_sync_configuration.return_value = {}
    create_sync_configuration("test-branch", "test-config_file", "test-repository_link_id", "test-resource_name", "test-role_arn", "test-sync_type", region_name=REGION)
    mock_client.create_sync_configuration.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_create_sync_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_sync_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_sync_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to create sync configuration"):
        create_sync_configuration("test-branch", "test-config_file", "test-repository_link_id", "test-resource_name", "test-role_arn", "test-sync_type", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_delete_repository_link(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_repository_link.return_value = {}
    delete_repository_link("test-repository_link_id", region_name=REGION)
    mock_client.delete_repository_link.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_delete_repository_link_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_repository_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_repository_link",
    )
    with pytest.raises(RuntimeError, match="Failed to delete repository link"):
        delete_repository_link("test-repository_link_id", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_delete_sync_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_sync_configuration.return_value = {}
    delete_sync_configuration("test-sync_type", "test-resource_name", region_name=REGION)
    mock_client.delete_sync_configuration.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_delete_sync_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_sync_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_sync_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to delete sync configuration"):
        delete_sync_configuration("test-sync_type", "test-resource_name", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_get_repository_link(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_link.return_value = {}
    get_repository_link("test-repository_link_id", region_name=REGION)
    mock_client.get_repository_link.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_get_repository_link_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_repository_link",
    )
    with pytest.raises(RuntimeError, match="Failed to get repository link"):
        get_repository_link("test-repository_link_id", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_get_repository_sync_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_sync_status.return_value = {}
    get_repository_sync_status("test-branch", "test-repository_link_id", "test-sync_type", region_name=REGION)
    mock_client.get_repository_sync_status.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_get_repository_sync_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_repository_sync_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_repository_sync_status",
    )
    with pytest.raises(RuntimeError, match="Failed to get repository sync status"):
        get_repository_sync_status("test-branch", "test-repository_link_id", "test-sync_type", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_get_resource_sync_status(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_resource_sync_status.return_value = {}
    get_resource_sync_status("test-resource_name", "test-sync_type", region_name=REGION)
    mock_client.get_resource_sync_status.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_get_resource_sync_status_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_resource_sync_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_sync_status",
    )
    with pytest.raises(RuntimeError, match="Failed to get resource sync status"):
        get_resource_sync_status("test-resource_name", "test-sync_type", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_get_sync_blocker_summary(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sync_blocker_summary.return_value = {}
    get_sync_blocker_summary("test-sync_type", "test-resource_name", region_name=REGION)
    mock_client.get_sync_blocker_summary.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_get_sync_blocker_summary_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sync_blocker_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sync_blocker_summary",
    )
    with pytest.raises(RuntimeError, match="Failed to get sync blocker summary"):
        get_sync_blocker_summary("test-sync_type", "test-resource_name", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_get_sync_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sync_configuration.return_value = {}
    get_sync_configuration("test-sync_type", "test-resource_name", region_name=REGION)
    mock_client.get_sync_configuration.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_get_sync_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.get_sync_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_sync_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to get sync configuration"):
        get_sync_configuration("test-sync_type", "test-resource_name", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_list_repository_links(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repository_links.return_value = {}
    list_repository_links(region_name=REGION)
    mock_client.list_repository_links.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_list_repository_links_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repository_links.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_repository_links",
    )
    with pytest.raises(RuntimeError, match="Failed to list repository links"):
        list_repository_links(region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_list_repository_sync_definitions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repository_sync_definitions.return_value = {}
    list_repository_sync_definitions("test-repository_link_id", "test-sync_type", region_name=REGION)
    mock_client.list_repository_sync_definitions.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_list_repository_sync_definitions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_repository_sync_definitions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_repository_sync_definitions",
    )
    with pytest.raises(RuntimeError, match="Failed to list repository sync definitions"):
        list_repository_sync_definitions("test-repository_link_id", "test-sync_type", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_list_sync_configurations(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sync_configurations.return_value = {}
    list_sync_configurations("test-repository_link_id", "test-sync_type", region_name=REGION)
    mock_client.list_sync_configurations.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_list_sync_configurations_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_sync_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sync_configurations",
    )
    with pytest.raises(RuntimeError, match="Failed to list sync configurations"):
        list_sync_configurations("test-repository_link_id", "test-sync_type", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_update_host(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_host.return_value = {}
    update_host("test-host_arn", region_name=REGION)
    mock_client.update_host.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_update_host_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_host.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_host",
    )
    with pytest.raises(RuntimeError, match="Failed to update host"):
        update_host("test-host_arn", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_update_repository_link(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_repository_link.return_value = {}
    update_repository_link("test-repository_link_id", region_name=REGION)
    mock_client.update_repository_link.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_update_repository_link_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_repository_link.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_repository_link",
    )
    with pytest.raises(RuntimeError, match="Failed to update repository link"):
        update_repository_link("test-repository_link_id", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_update_sync_blocker(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_sync_blocker.return_value = {}
    update_sync_blocker("test-id", "test-sync_type", "test-resource_name", "test-resolved_reason", region_name=REGION)
    mock_client.update_sync_blocker.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_update_sync_blocker_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_sync_blocker.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_sync_blocker",
    )
    with pytest.raises(RuntimeError, match="Failed to update sync blocker"):
        update_sync_blocker("test-id", "test-sync_type", "test-resource_name", "test-resolved_reason", region_name=REGION)


@patch("aws_util.codestar_connections.get_client")
def test_update_sync_configuration(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_sync_configuration.return_value = {}
    update_sync_configuration("test-resource_name", "test-sync_type", region_name=REGION)
    mock_client.update_sync_configuration.assert_called_once()


@patch("aws_util.codestar_connections.get_client")
def test_update_sync_configuration_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_sync_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_sync_configuration",
    )
    with pytest.raises(RuntimeError, match="Failed to update sync configuration"):
        update_sync_configuration("test-resource_name", "test-sync_type", region_name=REGION)


def test_list_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import list_connections
    mock_client = MagicMock()
    mock_client.list_connections.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    list_connections(provider_type_filter=[{}], host_arn_filter=[{}], region_name="us-east-1")
    mock_client.list_connections.assert_called_once()

def test_create_repository_link_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import create_repository_link
    mock_client = MagicMock()
    mock_client.create_repository_link.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    create_repository_link("test-connection_arn", "test-owner_id", "test-repository_name", encryption_key_arn="test-encryption_key_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_repository_link.assert_called_once()

def test_create_sync_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import create_sync_configuration
    mock_client = MagicMock()
    mock_client.create_sync_configuration.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    create_sync_configuration("test-branch", {}, "test-repository_link_id", "test-resource_name", "test-role_arn", "test-sync_type", publish_deployment_status=True, trigger_resource_update_on="test-trigger_resource_update_on", region_name="us-east-1")
    mock_client.create_sync_configuration.assert_called_once()

def test_list_repository_links_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import list_repository_links
    mock_client = MagicMock()
    mock_client.list_repository_links.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    list_repository_links(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_repository_links.assert_called_once()

def test_list_sync_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import list_sync_configurations
    mock_client = MagicMock()
    mock_client.list_sync_configurations.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    list_sync_configurations("test-repository_link_id", "test-sync_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sync_configurations.assert_called_once()

def test_update_host_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import update_host
    mock_client = MagicMock()
    mock_client.update_host.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    update_host("test-host_arn", provider_endpoint="test-provider_endpoint", vpc_configuration={}, region_name="us-east-1")
    mock_client.update_host.assert_called_once()

def test_update_repository_link_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import update_repository_link
    mock_client = MagicMock()
    mock_client.update_repository_link.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    update_repository_link("test-repository_link_id", connection_arn="test-connection_arn", encryption_key_arn="test-encryption_key_arn", region_name="us-east-1")
    mock_client.update_repository_link.assert_called_once()

def test_update_sync_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.codestar_connections import update_sync_configuration
    mock_client = MagicMock()
    mock_client.update_sync_configuration.return_value = {}
    monkeypatch.setattr("aws_util.codestar_connections.get_client", lambda *a, **kw: mock_client)
    update_sync_configuration("test-resource_name", "test-sync_type", branch="test-branch", config_file={}, repository_link_id="test-repository_link_id", role_arn="test-role_arn", publish_deployment_status=True, trigger_resource_update_on="test-trigger_resource_update_on", region_name="us-east-1")
    mock_client.update_sync_configuration.assert_called_once()
