"""Tests for aws_util.aio.codestar_connections -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.codestar_connections import (
    ConnectionResult,
    HostResult,
    TagResult,
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


def _conn_dict(**kw):
    d = {"ConnectionArn": CONN_ARN, "ConnectionName": "myconn"}
    d.update(kw)
    return d


def _host_dict(**kw):
    d = {"HostArn": HOST_ARN, "Name": "myhost"}
    d.update(kw)
    return d


def _mock_factory(mc):
    return lambda *a, **kw: mc


# ---------------------------------------------------------------------------
# Connection operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_connection_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"ConnectionArn": CONN_ARN}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await create_connection("myconn")
    assert r == CONN_ARN


@pytest.mark.asyncio
async def test_create_connection_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"ConnectionArn": CONN_ARN}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await create_connection(
        "myconn", provider_type="GitHub",
        tags=[{"Key": "k", "Value": "v"}],
        host_arn=HOST_ARN,
    )
    assert r == CONN_ARN


@pytest.mark.asyncio
async def test_create_connection_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_connection("myconn")


@pytest.mark.asyncio
async def test_get_connection_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Connection": _conn_dict()}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await get_connection(CONN_ARN)
    assert isinstance(r, ConnectionResult)


@pytest.mark.asyncio
async def test_get_connection_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_connection(CONN_ARN)


@pytest.mark.asyncio
async def test_list_connections_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Connections": [_conn_dict()]}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_connections()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_connections_with_filters(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Connections": []}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_connections(
        provider_type_filter="GitHub", host_arn_filter=HOST_ARN,
    )
    assert r == []


@pytest.mark.asyncio
async def test_list_connections_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Connections": [_conn_dict()], "NextToken": "tok"},
        {"Connections": [_conn_dict(ConnectionName="c2")]},
    ]
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_connections()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_connections_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_connections()


@pytest.mark.asyncio
async def test_delete_connection_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    await delete_connection(CONN_ARN)
    mc.call.assert_called_once()


@pytest.mark.asyncio
async def test_delete_connection_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_connection(CONN_ARN)


# ---------------------------------------------------------------------------
# Host operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_host_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"HostArn": HOST_ARN}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await create_host("myhost", "GitHubEnterpriseServer", "https://ghe")
    assert r == HOST_ARN


@pytest.mark.asyncio
async def test_create_host_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"HostArn": HOST_ARN}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await create_host(
        "myhost", "GitHubEnterpriseServer", "https://ghe",
        vpc_configuration={"VpcId": "vpc-1"},
        tags=[{"Key": "k", "Value": "v"}],
    )
    assert r == HOST_ARN


@pytest.mark.asyncio
async def test_create_host_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await create_host("myhost", "GitHubEnterpriseServer", "https://ghe")


@pytest.mark.asyncio
async def test_get_host_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Name": "myhost",
        "ProviderType": "GitHubEnterpriseServer",
        "ProviderEndpoint": "https://ghe",
        "Status": "AVAILABLE",
        "VpcConfiguration": {"VpcId": "vpc-1"},
    }
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await get_host(HOST_ARN)
    assert isinstance(r, HostResult)
    assert r.host_arn == HOST_ARN


@pytest.mark.asyncio
async def test_get_host_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await get_host(HOST_ARN)


@pytest.mark.asyncio
async def test_list_hosts_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Hosts": [_host_dict()]}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_hosts()
    assert len(r) == 1


@pytest.mark.asyncio
async def test_list_hosts_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Hosts": [_host_dict()], "NextToken": "tok"},
        {"Hosts": [_host_dict(Name="h2")]},
    ]
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_hosts()
    assert len(r) == 2


@pytest.mark.asyncio
async def test_list_hosts_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_hosts()


@pytest.mark.asyncio
async def test_delete_host_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    await delete_host(HOST_ARN)
    mc.call.assert_called_once()


@pytest.mark.asyncio
async def test_delete_host_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await delete_host(HOST_ARN)


# ---------------------------------------------------------------------------
# Tag operations
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_tag_resource_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    await tag_resource(RESOURCE_ARN, [{"Key": "k", "Value": "v"}])
    mc.call.assert_called_once()


@pytest.mark.asyncio
async def test_tag_resource_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await tag_resource(RESOURCE_ARN, [{"Key": "k", "Value": "v"}])


@pytest.mark.asyncio
async def test_list_tags_for_resource_success(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Tags": [{"Key": "k", "Value": "v"}]}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_tags_for_resource(RESOURCE_ARN)
    assert len(r) == 1
    assert r[0].key == "k"


@pytest.mark.asyncio
async def test_list_tags_for_resource_empty(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    r = await list_tags_for_resource(RESOURCE_ARN)
    assert r == []


@pytest.mark.asyncio
async def test_list_tags_for_resource_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = Exception("fail")
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", _mock_factory(mc))
    with pytest.raises(Exception):
        await list_tags_for_resource(RESOURCE_ARN)


async def test_create_repository_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_repository_link("test-connection_arn", "test-owner_id", "test-repository_name", )
    mock_client.call.assert_called_once()


async def test_create_repository_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_repository_link("test-connection_arn", "test-owner_id", "test-repository_name", )


async def test_create_sync_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_sync_configuration("test-branch", "test-config_file", "test-repository_link_id", "test-resource_name", "test-role_arn", "test-sync_type", )
    mock_client.call.assert_called_once()


async def test_create_sync_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_sync_configuration("test-branch", "test-config_file", "test-repository_link_id", "test-resource_name", "test-role_arn", "test-sync_type", )


async def test_delete_repository_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_repository_link("test-repository_link_id", )
    mock_client.call.assert_called_once()


async def test_delete_repository_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_repository_link("test-repository_link_id", )


async def test_delete_sync_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_sync_configuration("test-sync_type", "test-resource_name", )
    mock_client.call.assert_called_once()


async def test_delete_sync_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_sync_configuration("test-sync_type", "test-resource_name", )


async def test_get_repository_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_repository_link("test-repository_link_id", )
    mock_client.call.assert_called_once()


async def test_get_repository_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_repository_link("test-repository_link_id", )


async def test_get_repository_sync_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_repository_sync_status("test-branch", "test-repository_link_id", "test-sync_type", )
    mock_client.call.assert_called_once()


async def test_get_repository_sync_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_repository_sync_status("test-branch", "test-repository_link_id", "test-sync_type", )


async def test_get_resource_sync_status(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_sync_status("test-resource_name", "test-sync_type", )
    mock_client.call.assert_called_once()


async def test_get_resource_sync_status_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_sync_status("test-resource_name", "test-sync_type", )


async def test_get_sync_blocker_summary(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sync_blocker_summary("test-sync_type", "test-resource_name", )
    mock_client.call.assert_called_once()


async def test_get_sync_blocker_summary_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sync_blocker_summary("test-sync_type", "test-resource_name", )


async def test_get_sync_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_sync_configuration("test-sync_type", "test-resource_name", )
    mock_client.call.assert_called_once()


async def test_get_sync_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_sync_configuration("test-sync_type", "test-resource_name", )


async def test_list_repository_links(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_repository_links()
    mock_client.call.assert_called_once()


async def test_list_repository_links_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_repository_links()


async def test_list_repository_sync_definitions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_repository_sync_definitions("test-repository_link_id", "test-sync_type", )
    mock_client.call.assert_called_once()


async def test_list_repository_sync_definitions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_repository_sync_definitions("test-repository_link_id", "test-sync_type", )


async def test_list_sync_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_sync_configurations("test-repository_link_id", "test-sync_type", )
    mock_client.call.assert_called_once()


async def test_list_sync_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_sync_configurations("test-repository_link_id", "test-sync_type", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_host(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_host("test-host_arn", )
    mock_client.call.assert_called_once()


async def test_update_host_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_host("test-host_arn", )


async def test_update_repository_link(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_repository_link("test-repository_link_id", )
    mock_client.call.assert_called_once()


async def test_update_repository_link_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_repository_link("test-repository_link_id", )


async def test_update_sync_blocker(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_sync_blocker("test-id", "test-sync_type", "test-resource_name", "test-resolved_reason", )
    mock_client.call.assert_called_once()


async def test_update_sync_blocker_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_sync_blocker("test-id", "test-sync_type", "test-resource_name", "test-resolved_reason", )


async def test_update_sync_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_sync_configuration("test-resource_name", "test-sync_type", )
    mock_client.call.assert_called_once()


async def test_update_sync_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.codestar_connections.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_sync_configuration("test-resource_name", "test-sync_type", )


@pytest.mark.asyncio
async def test_list_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import list_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await list_connections(provider_type_filter=[{}], host_arn_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_repository_link_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import create_repository_link
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await create_repository_link("test-connection_arn", "test-owner_id", "test-repository_name", encryption_key_arn="test-encryption_key_arn", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_sync_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import create_sync_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await create_sync_configuration("test-branch", {}, "test-repository_link_id", "test-resource_name", "test-role_arn", "test-sync_type", publish_deployment_status=True, trigger_resource_update_on="test-trigger_resource_update_on", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_repository_links_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import list_repository_links
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await list_repository_links(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sync_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import list_sync_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await list_sync_configurations("test-repository_link_id", "test-sync_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_host_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import update_host
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await update_host("test-host_arn", provider_endpoint="test-provider_endpoint", vpc_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_repository_link_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import update_repository_link
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await update_repository_link("test-repository_link_id", connection_arn="test-connection_arn", encryption_key_arn="test-encryption_key_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_sync_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.codestar_connections import update_sync_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.codestar_connections.async_client", lambda *a, **kw: mock_client)
    await update_sync_configuration("test-resource_name", "test-sync_type", branch="test-branch", config_file={}, repository_link_id="test-repository_link_id", role_arn="test-role_arn", publish_deployment_status=True, trigger_resource_update_on="test-trigger_resource_update_on", region_name="us-east-1")
    mock_client.call.assert_called_once()
