"""Tests for aws_util.aio.keyspaces -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.keyspaces import (
    KeyspaceResult,
    TableResult,
    create_keyspace,
    create_table,
    delete_keyspace,
    delete_table,
    get_keyspace,
    get_table,
    list_keyspaces,
    list_tables,
    list_tags_for_resource,
    restore_table,
    tag_resource,
    update_table,
    create_type,
    delete_type,
    get_table_auto_scaling_settings,
    get_type,
    list_types,
    untag_resource,
    update_keyspace,
)


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


def test_models_re_exported():
    assert KeyspaceResult is not None
    assert TableResult is not None


# ---------------------------------------------------------------------------
# Keyspace operations
# ---------------------------------------------------------------------------


class TestCreateKeyspace:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"resourceArn": "arn:ks"})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await create_keyspace("ks")
        assert result.keyspace_name == "ks"
        assert result.resource_arn == "arn:ks"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await create_keyspace("ks")


class TestGetKeyspace:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"keyspaceName": "ks", "resourceArn": "arn:ks"})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await get_keyspace("ks")
        assert result.keyspace_name == "ks"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await get_keyspace("ks")


class TestListKeyspaces:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"keyspaces": [{"keyspaceName": "ks1", "resourceArn": "arn:ks1"}], "nextToken": "tok"},
            {"keyspaces": [{"keyspaceName": "ks2", "resourceArn": "arn:ks2"}]},
        ]
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await list_keyspaces()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_keyspaces()


class TestDeleteKeyspace:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        await delete_keyspace("ks")

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await delete_keyspace("ks")


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


class TestCreateTable:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"resourceArn": "arn:tbl"})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await create_table("ks", "tbl", {"columns": []})
        assert result.table_name == "tbl"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await create_table("ks", "tbl", {"columns": []})


class TestGetTable:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({
            "keyspaceName": "ks", "tableName": "tbl",
            "resourceArn": "arn:tbl", "status": "ACTIVE",
        })
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await get_table("ks", "tbl")
        assert result.status == "ACTIVE"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await get_table("ks", "tbl")


class TestListTables:
    @pytest.mark.asyncio
    async def test_pagination(self, monkeypatch):
        mc = _mc()
        mc.call.side_effect = [
            {"tables": [{"keyspaceName": "ks", "tableName": "t1", "resourceArn": "arn:t1"}], "nextToken": "tok"},
            {"tables": [{"keyspaceName": "ks", "tableName": "t2", "resourceArn": "arn:t2"}]},
        ]
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await list_tables("ks")
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_tables("ks")


class TestDeleteTable:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        await delete_table("ks", "tbl")

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await delete_table("ks", "tbl")


class TestUpdateTable:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"resourceArn": "arn:tbl"})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await update_table("ks", "tbl")
        assert result == "arn:tbl"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await update_table("ks", "tbl")


class TestRestoreTable:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"restoredTableARN": "arn:restored"})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await restore_table("ks1", "tbl1", "ks2", "tbl2")
        assert result == "arn:restored"

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await restore_table("ks1", "tbl1", "ks2", "tbl2")


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


class TestTagResource:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        await tag_resource("arn:ks", [{"key": "env", "value": "dev"}])

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await tag_resource("arn:ks", [{"key": "env", "value": "dev"}])


class TestListTagsForResource:
    @pytest.mark.asyncio
    async def test_success(self, monkeypatch):
        mc = _mc({"tags": [{"key": "env", "value": "dev"}]})
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        result = await list_tags_for_resource("arn:ks")
        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_error(self, monkeypatch):
        mc = _mc(se=Exception("boom"))
        monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mc)
        with pytest.raises(RuntimeError):
            await list_tags_for_resource("arn:ks")


async def test_create_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_type("test-keyspace_name", "test-type_name", [], )
    mock_client.call.assert_called_once()


async def test_create_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_type("test-keyspace_name", "test-type_name", [], )


async def test_delete_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_type("test-keyspace_name", "test-type_name", )
    mock_client.call.assert_called_once()


async def test_delete_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_type("test-keyspace_name", "test-type_name", )


async def test_get_table_auto_scaling_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_table_auto_scaling_settings("test-keyspace_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_table_auto_scaling_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_table_auto_scaling_settings("test-keyspace_name", "test-table_name", )


async def test_get_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_type("test-keyspace_name", "test-type_name", )
    mock_client.call.assert_called_once()


async def test_get_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_type("test-keyspace_name", "test-type_name", )


async def test_list_types(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_types("test-keyspace_name", )
    mock_client.call.assert_called_once()


async def test_list_types_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_types("test-keyspace_name", )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_keyspace(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_keyspace("test-keyspace_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_keyspace_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.keyspaces.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_keyspace("test-keyspace_name", {}, )


@pytest.mark.asyncio
async def test_list_types_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.keyspaces import list_types
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mock_client)
    await list_types("test-keyspace_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_keyspace_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.keyspaces import update_keyspace
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.keyspaces.async_client", lambda *a, **kw: mock_client)
    await update_keyspace("test-keyspace_name", {}, client_side_timestamps="test-client_side_timestamps", region_name="us-east-1")
    mock_client.call.assert_called_once()
