"""Tests for aws_util.aio.dynamodb -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.dynamodb import (
    Attr,
    DynamoKey,
    Key,
    _build_update_expression,
    _serialize_key,
    atomic_increment,
    batch_get,
    batch_write,
    delete_item,
    get_item,
    put_if_not_exists,
    put_item,
    query,
    scan,
    transact_get,
    transact_write,
    update_item,
    update_item_raw,
    batch_execute_statement,
    batch_get_item,
    batch_write_item,
    create_backup,
    create_global_table,
    create_table,
    delete_backup,
    delete_resource_policy,
    delete_table,
    describe_backup,
    describe_continuous_backups,
    describe_contributor_insights,
    describe_endpoints,
    describe_export,
    describe_global_table,
    describe_global_table_settings,
    describe_import,
    describe_kinesis_streaming_destination,
    describe_limits,
    describe_table,
    describe_table_replica_auto_scaling,
    describe_time_to_live,
    disable_kinesis_streaming_destination,
    enable_kinesis_streaming_destination,
    execute_statement,
    execute_transaction,
    export_table_to_point_in_time,
    get_resource_policy,
    import_table,
    list_backups,
    list_contributor_insights,
    list_exports,
    list_global_tables,
    list_imports,
    list_tables,
    list_tags_of_resource,
    put_resource_policy,
    restore_table_from_backup,
    restore_table_to_point_in_time,
    tag_resource,
    transact_get_items,
    transact_write_items,
    untag_resource,
    update_continuous_backups,
    update_contributor_insights,
    update_global_table,
    update_global_table_settings,
    update_kinesis_streaming_destination,
    update_table,
    update_table_replica_auto_scaling,
    update_time_to_live,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def test_serialize_key_dynamokey():
    k = DynamoKey(partition_key="pk", partition_value="v1")
    assert _serialize_key(k) == {"pk": "v1"}


def test_serialize_key_dict():
    d = {"pk": "v1"}
    assert _serialize_key(d) == {"pk": "v1"}


def test_build_update_expression():
    expr, names, values = _build_update_expression({"name": "alice", "age": 30})
    assert expr == "SET #attr_0 = :val_0, #attr_1 = :val_1"
    assert names == {"#attr_0": "name", "#attr_1": "age"}
    assert values == {":val_0": "alice", ":val_1": 30}


# ---------------------------------------------------------------------------
# get_item
# ---------------------------------------------------------------------------


async def test_get_item_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value={"pk": "v1", "data": 42}),
    )
    result = await get_item("table", {"pk": "v1"})
    assert result == {"pk": "v1", "data": 42}


async def test_get_item_none(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    result = await get_item("table", {"pk": "v1"}, consistent_read=True)
    assert result is None


async def test_get_item_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_item("table", {"pk": "v1"})


# ---------------------------------------------------------------------------
# put_item
# ---------------------------------------------------------------------------


async def test_put_item_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    await put_item("table", {"pk": "v1"})


async def test_put_item_with_condition(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    await put_item("table", {"pk": "v1"}, condition="some_condition")


async def test_put_item_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_item("table", {"pk": "v1"})


# ---------------------------------------------------------------------------
# update_item
# ---------------------------------------------------------------------------


async def test_update_item_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value={"pk": "v1", "name": "new"}),
    )
    result = await update_item("table", {"pk": "v1"}, {"name": "new"})
    assert result["name"] == "new"


async def test_update_item_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_item("table", {"pk": "v1"}, {"name": "x"})


# ---------------------------------------------------------------------------
# delete_item
# ---------------------------------------------------------------------------


async def test_delete_item_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    await delete_item("table", {"pk": "v1"})


async def test_delete_item_with_condition(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    await delete_item("table", {"pk": "v1"}, condition="cond")


async def test_delete_item_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_item("table", {"pk": "v1"})


# ---------------------------------------------------------------------------
# query
# ---------------------------------------------------------------------------


async def test_query_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=[{"pk": "v1"}]),
    )
    result = await query("table", "key_cond")
    assert len(result) == 1


async def test_query_with_all_params(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=[]),
    )
    result = await query(
        "table",
        "key_cond",
        filter_condition="filter",
        index_name="gsi",
        limit=10,
        scan_index_forward=False,
    )
    assert result == []


async def test_query_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await query("table", "key_cond")


# ---------------------------------------------------------------------------
# scan
# ---------------------------------------------------------------------------


async def test_scan_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=[{"pk": "v1"}]),
    )
    result = await scan("table")
    assert len(result) == 1


async def test_scan_with_all_params(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=[]),
    )
    result = await scan(
        "table",
        filter_condition="filter",
        index_name="gsi",
        limit=5,
    )
    assert result == []


async def test_scan_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await scan("table")


# ---------------------------------------------------------------------------
# batch_get
# ---------------------------------------------------------------------------


async def test_batch_get_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=[{"pk": "v1"}, {"pk": "v2"}]),
    )
    result = await batch_get("table", [{"pk": "v1"}, {"pk": "v2"}])
    assert len(result) == 2


async def test_batch_get_too_many_keys():
    keys = [{"pk": f"v{i}"} for i in range(101)]
    with pytest.raises(ValueError, match="at most 100 keys"):
        await batch_get("table", keys)


async def test_batch_get_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get("table", [{"pk": "v1"}])


# ---------------------------------------------------------------------------
# batch_write
# ---------------------------------------------------------------------------


async def test_batch_write_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    await batch_write("table", [{"pk": "v1"}])


async def test_batch_write_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_write("table", [{"pk": "v1"}])


# ---------------------------------------------------------------------------
# transact_write
# ---------------------------------------------------------------------------


async def test_transact_write_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=None),
    )
    await transact_write([{"Put": {"TableName": "t", "Item": {}}}])


async def test_transact_write_too_many():
    ops = [{"Put": {"TableName": "t"}} for _ in range(101)]
    with pytest.raises(ValueError, match="at most 100 operations"):
        await transact_write(ops)


async def test_transact_write_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await transact_write([{"Put": {}}])


# ---------------------------------------------------------------------------
# transact_get
# ---------------------------------------------------------------------------


async def test_transact_get_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=[{"pk": "v1"}, None]),
    )
    result = await transact_get([{"Get": {"TableName": "t", "Key": {}}}])
    assert len(result) == 2


async def test_transact_get_too_many():
    items = [{"Get": {"TableName": "t", "Key": {}}} for _ in range(101)]
    with pytest.raises(ValueError, match="at most 100 items"):
        await transact_get(items)


async def test_transact_get_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await transact_get([{"Get": {}}])


# ---------------------------------------------------------------------------
# atomic_increment
# ---------------------------------------------------------------------------


async def test_atomic_increment_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=5),
    )
    result = await atomic_increment("table", {"pk": "v1"}, "counter", amount=2)
    assert result == 5


async def test_atomic_increment_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await atomic_increment("table", {"pk": "v1"}, "counter")


# ---------------------------------------------------------------------------
# put_if_not_exists
# ---------------------------------------------------------------------------


async def test_put_if_not_exists_true(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=True),
    )
    result = await put_if_not_exists("table", {"pk": "v1"}, "pk")
    assert result is True


async def test_put_if_not_exists_false(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value=False),
    )
    result = await put_if_not_exists("table", {"pk": "v1"}, "pk")
    assert result is False


async def test_put_if_not_exists_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_if_not_exists("table", {"pk": "v1"}, "pk")


# ---------------------------------------------------------------------------
# update_item_raw
# ---------------------------------------------------------------------------


async def test_update_item_raw_ok(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(return_value={"pk": "v1", "counter": 1}),
    )
    result = await update_item_raw(
        "table",
        {"pk": "v1"},
        "SET #c = :v",
        expression_attribute_names={"#c": "counter"},
        expression_attribute_values={":v": 1},
        condition_expression="attribute_exists(pk)",
        return_values="ALL_NEW",
    )
    assert result == {"pk": "v1", "counter": 1}


async def test_update_item_raw_runtime_error(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.asyncio.to_thread",
        AsyncMock(side_effect=RuntimeError("boom")),
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_item_raw(
            "table",
            {"pk": "v1"},
            "SET #c = :v",
            expression_attribute_names={"#c": "counter"},
            expression_attribute_values={":v": 1},
        )


# ---------------------------------------------------------------------------
# Re-exports: Key & Attr
# ---------------------------------------------------------------------------


def test_key_reexport():
    from boto3.dynamodb.conditions import Key as BotoKey

    assert Key is BotoKey


def test_attr_reexport():
    from boto3.dynamodb.conditions import Attr as BotoAttr

    assert Attr is BotoAttr


async def test_batch_execute_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_execute_statement([], )
    mock_client.call.assert_called_once()


async def test_batch_execute_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_execute_statement([], )


async def test_batch_get_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_get_item({}, )
    mock_client.call.assert_called_once()


async def test_batch_get_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_item({}, )


async def test_batch_write_item(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_write_item({}, )
    mock_client.call.assert_called_once()


async def test_batch_write_item_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_write_item({}, )


async def test_create_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_backup("test-table_name", "test-backup_name", )
    mock_client.call.assert_called_once()


async def test_create_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_backup("test-table_name", "test-backup_name", )


async def test_create_global_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_global_table("test-global_table_name", [], )
    mock_client.call.assert_called_once()


async def test_create_global_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_global_table("test-global_table_name", [], )


async def test_create_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_table([], "test-table_name", [], )
    mock_client.call.assert_called_once()


async def test_create_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_table([], "test-table_name", [], )


async def test_delete_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_backup("test-backup_arn", )
    mock_client.call.assert_called_once()


async def test_delete_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_backup("test-backup_arn", )


async def test_delete_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_delete_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_resource_policy("test-resource_arn", )


async def test_delete_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_table("test-table_name", )
    mock_client.call.assert_called_once()


async def test_delete_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_table("test-table_name", )


async def test_describe_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_backup("test-backup_arn", )
    mock_client.call.assert_called_once()


async def test_describe_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_backup("test-backup_arn", )


async def test_describe_continuous_backups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_continuous_backups("test-table_name", )
    mock_client.call.assert_called_once()


async def test_describe_continuous_backups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_continuous_backups("test-table_name", )


async def test_describe_contributor_insights(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_contributor_insights("test-table_name", )
    mock_client.call.assert_called_once()


async def test_describe_contributor_insights_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_contributor_insights("test-table_name", )


async def test_describe_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoints()


async def test_describe_export(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_export("test-export_arn", )
    mock_client.call.assert_called_once()


async def test_describe_export_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_export("test-export_arn", )


async def test_describe_global_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_global_table("test-global_table_name", )
    mock_client.call.assert_called_once()


async def test_describe_global_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_global_table("test-global_table_name", )


async def test_describe_global_table_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_global_table_settings("test-global_table_name", )
    mock_client.call.assert_called_once()


async def test_describe_global_table_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_global_table_settings("test-global_table_name", )


async def test_describe_import(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_import("test-import_arn", )
    mock_client.call.assert_called_once()


async def test_describe_import_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_import("test-import_arn", )


async def test_describe_kinesis_streaming_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_kinesis_streaming_destination("test-table_name", )
    mock_client.call.assert_called_once()


async def test_describe_kinesis_streaming_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_kinesis_streaming_destination("test-table_name", )


async def test_describe_limits(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_limits()
    mock_client.call.assert_called_once()


async def test_describe_limits_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_limits()


async def test_describe_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_table("test-table_name", )
    mock_client.call.assert_called_once()


async def test_describe_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_table("test-table_name", )


async def test_describe_table_replica_auto_scaling(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_table_replica_auto_scaling("test-table_name", )
    mock_client.call.assert_called_once()


async def test_describe_table_replica_auto_scaling_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_table_replica_auto_scaling("test-table_name", )


async def test_describe_time_to_live(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_time_to_live("test-table_name", )
    mock_client.call.assert_called_once()


async def test_describe_time_to_live_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_time_to_live("test-table_name", )


async def test_disable_kinesis_streaming_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_kinesis_streaming_destination("test-table_name", "test-stream_arn", )
    mock_client.call.assert_called_once()


async def test_disable_kinesis_streaming_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_kinesis_streaming_destination("test-table_name", "test-stream_arn", )


async def test_enable_kinesis_streaming_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_kinesis_streaming_destination("test-table_name", "test-stream_arn", )
    mock_client.call.assert_called_once()


async def test_enable_kinesis_streaming_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_kinesis_streaming_destination("test-table_name", "test-stream_arn", )


async def test_execute_statement(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_statement("test-statement", )
    mock_client.call.assert_called_once()


async def test_execute_statement_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_statement("test-statement", )


async def test_execute_transaction(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_transaction([], )
    mock_client.call.assert_called_once()


async def test_execute_transaction_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_transaction([], )


async def test_export_table_to_point_in_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_table_to_point_in_time("test-table_arn", "test-s3_bucket", )
    mock_client.call.assert_called_once()


async def test_export_table_to_point_in_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_table_to_point_in_time("test-table_arn", "test-s3_bucket", )


async def test_get_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_resource_policy("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_get_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_resource_policy("test-resource_arn", )


async def test_import_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await import_table({}, "test-input_format", {}, )
    mock_client.call.assert_called_once()


async def test_import_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await import_table({}, "test-input_format", {}, )


async def test_list_backups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_backups()
    mock_client.call.assert_called_once()


async def test_list_backups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_backups()


async def test_list_contributor_insights(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_contributor_insights()
    mock_client.call.assert_called_once()


async def test_list_contributor_insights_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_contributor_insights()


async def test_list_exports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_exports()
    mock_client.call.assert_called_once()


async def test_list_exports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_exports()


async def test_list_global_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_global_tables()
    mock_client.call.assert_called_once()


async def test_list_global_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_global_tables()


async def test_list_imports(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_imports()
    mock_client.call.assert_called_once()


async def test_list_imports_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_imports()


async def test_list_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tables()
    mock_client.call.assert_called_once()


async def test_list_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tables()


async def test_list_tags_of_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_of_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_of_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_of_resource("test-resource_arn", )


async def test_put_resource_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_resource_policy("test-resource_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_resource_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_resource_policy("test-resource_arn", "test-policy", )


async def test_restore_table_from_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_table_from_backup("test-target_table_name", "test-backup_arn", )
    mock_client.call.assert_called_once()


async def test_restore_table_from_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_table_from_backup("test-target_table_name", "test-backup_arn", )


async def test_restore_table_to_point_in_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_table_to_point_in_time("test-target_table_name", )
    mock_client.call.assert_called_once()


async def test_restore_table_to_point_in_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_table_to_point_in_time("test-target_table_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_transact_get_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await transact_get_items([], )
    mock_client.call.assert_called_once()


async def test_transact_get_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await transact_get_items([], )


async def test_transact_write_items(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await transact_write_items([], )
    mock_client.call.assert_called_once()


async def test_transact_write_items_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await transact_write_items([], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_continuous_backups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_continuous_backups("test-table_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_continuous_backups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_continuous_backups("test-table_name", {}, )


async def test_update_contributor_insights(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_contributor_insights("test-table_name", "test-contributor_insights_action", )
    mock_client.call.assert_called_once()


async def test_update_contributor_insights_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_contributor_insights("test-table_name", "test-contributor_insights_action", )


async def test_update_global_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_global_table("test-global_table_name", [], )
    mock_client.call.assert_called_once()


async def test_update_global_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_global_table("test-global_table_name", [], )


async def test_update_global_table_settings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_global_table_settings("test-global_table_name", )
    mock_client.call.assert_called_once()


async def test_update_global_table_settings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_global_table_settings("test-global_table_name", )


async def test_update_kinesis_streaming_destination(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_kinesis_streaming_destination("test-table_name", "test-stream_arn", )
    mock_client.call.assert_called_once()


async def test_update_kinesis_streaming_destination_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_kinesis_streaming_destination("test-table_name", "test-stream_arn", )


async def test_update_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_table("test-table_name", )
    mock_client.call.assert_called_once()


async def test_update_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_table("test-table_name", )


async def test_update_table_replica_auto_scaling(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_table_replica_auto_scaling("test-table_name", )
    mock_client.call.assert_called_once()


async def test_update_table_replica_auto_scaling_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_table_replica_auto_scaling("test-table_name", )


async def test_update_time_to_live(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_time_to_live("test-table_name", {}, )
    mock_client.call.assert_called_once()


async def test_update_time_to_live_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.dynamodb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_time_to_live("test-table_name", {}, )


@pytest.mark.asyncio
async def test_batch_execute_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import batch_execute_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await batch_execute_statement("test-statements", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_get_item_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import batch_get_item
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await batch_get_item("test-request_items", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_write_item_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import batch_write_item
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await batch_write_item("test-request_items", return_consumed_capacity="test-return_consumed_capacity", return_item_collection_metrics="test-return_item_collection_metrics", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import create_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await create_table({}, "test-table_name", "test-key_schema", local_secondary_indexes="test-local_secondary_indexes", global_secondary_indexes="test-global_secondary_indexes", billing_mode="test-billing_mode", provisioned_throughput="test-provisioned_throughput", stream_specification={}, sse_specification={}, tags=[{"Key": "k", "Value": "v"}], table_class="test-table_class", deletion_protection_enabled="test-deletion_protection_enabled", warm_throughput="test-warm_throughput", resource_policy="{}", on_demand_throughput="test-on_demand_throughput", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import delete_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await delete_resource_policy("test-resource_arn", expected_revision_id="test-expected_revision_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_contributor_insights_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import describe_contributor_insights
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await describe_contributor_insights("test-table_name", index_name="test-index_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disable_kinesis_streaming_destination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import disable_kinesis_streaming_destination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await disable_kinesis_streaming_destination("test-table_name", "test-stream_arn", enable_kinesis_streaming_configuration=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_enable_kinesis_streaming_destination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import enable_kinesis_streaming_destination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await enable_kinesis_streaming_destination("test-table_name", "test-stream_arn", enable_kinesis_streaming_configuration=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import execute_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await execute_statement("test-statement", parameters="test-parameters", consistent_read="test-consistent_read", next_token="test-next_token", return_consumed_capacity="test-return_consumed_capacity", limit=1, return_values_on_condition_check_failure="test-return_values_on_condition_check_failure", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_transaction_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import execute_transaction
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await execute_transaction("test-transact_statements", client_request_token="test-client_request_token", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_export_table_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import export_table_to_point_in_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await export_table_to_point_in_time("test-table_arn", "test-s3_bucket", export_time=1, client_token="test-client_token", s3_bucket_owner="test-s3_bucket_owner", s3_prefix="test-s3_prefix", s3_sse_algorithm="test-s3_sse_algorithm", s3_sse_kms_key_id="test-s3_sse_kms_key_id", export_format=1, export_type=1, incremental_export_specification=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import import_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await import_table("test-s3_bucket_source", "test-input_format", "test-table_creation_parameters", client_token="test-client_token", input_format_options={}, input_compression_type="test-input_compression_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_backups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_backups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_backups(table_name="test-table_name", limit=1, time_range_lower_bound="test-time_range_lower_bound", time_range_upper_bound="test-time_range_upper_bound", exclusive_start_backup_arn="test-exclusive_start_backup_arn", backup_type="test-backup_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_contributor_insights_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_contributor_insights
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_contributor_insights(table_name="test-table_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_exports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_exports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_exports(table_arn="test-table_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_global_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_global_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_global_tables(exclusive_start_global_table_name="test-exclusive_start_global_table_name", limit=1, target_region_name="test-target_region_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_imports_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_imports
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_imports(table_arn="test-table_arn", page_size=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_tables(exclusive_start_table_name="test-exclusive_start_table_name", limit=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_of_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import list_tags_of_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await list_tags_of_resource("test-resource_arn", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_resource_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import put_resource_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await put_resource_policy("test-resource_arn", "{}", expected_revision_id="test-expected_revision_id", confirm_remove_self_resource_access=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_table_from_backup_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import restore_table_from_backup
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await restore_table_from_backup("test-target_table_name", "test-backup_arn", billing_mode_override="test-billing_mode_override", global_secondary_index_override="test-global_secondary_index_override", local_secondary_index_override="test-local_secondary_index_override", provisioned_throughput_override="test-provisioned_throughput_override", on_demand_throughput_override="test-on_demand_throughput_override", sse_specification_override={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_table_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import restore_table_to_point_in_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await restore_table_to_point_in_time("test-target_table_name", source_table_arn="test-source_table_arn", source_table_name="test-source_table_name", use_latest_restorable_time=True, restore_date_time="test-restore_date_time", billing_mode_override="test-billing_mode_override", global_secondary_index_override="test-global_secondary_index_override", local_secondary_index_override="test-local_secondary_index_override", provisioned_throughput_override="test-provisioned_throughput_override", on_demand_throughput_override="test-on_demand_throughput_override", sse_specification_override={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_transact_get_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import transact_get_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await transact_get_items("test-transact_items", return_consumed_capacity="test-return_consumed_capacity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_transact_write_items_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import transact_write_items
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await transact_write_items("test-transact_items", return_consumed_capacity="test-return_consumed_capacity", return_item_collection_metrics="test-return_item_collection_metrics", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_contributor_insights_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import update_contributor_insights
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await update_contributor_insights("test-table_name", "test-contributor_insights_action", index_name="test-index_name", contributor_insights_mode="test-contributor_insights_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_global_table_settings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import update_global_table_settings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await update_global_table_settings("test-global_table_name", global_table_billing_mode="test-global_table_billing_mode", global_table_provisioned_write_capacity_units="test-global_table_provisioned_write_capacity_units", global_table_provisioned_write_capacity_auto_scaling_settings_update={}, global_table_global_secondary_index_settings_update={}, replica_settings_update={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_kinesis_streaming_destination_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import update_kinesis_streaming_destination
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await update_kinesis_streaming_destination("test-table_name", "test-stream_arn", update_kinesis_streaming_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import update_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await update_table("test-table_name", attribute_definitions={}, billing_mode="test-billing_mode", provisioned_throughput="test-provisioned_throughput", global_secondary_index_updates="test-global_secondary_index_updates", stream_specification={}, sse_specification={}, replica_updates="test-replica_updates", table_class="test-table_class", deletion_protection_enabled="test-deletion_protection_enabled", multi_region_consistency=True, global_table_witness_updates="test-global_table_witness_updates", on_demand_throughput="test-on_demand_throughput", warm_throughput="test-warm_throughput", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_table_replica_auto_scaling_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.dynamodb import update_table_replica_auto_scaling
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.dynamodb.async_client", lambda *a, **kw: mock_client)
    await update_table_replica_auto_scaling("test-table_name", global_secondary_index_updates="test-global_secondary_index_updates", provisioned_write_capacity_auto_scaling_update="test-provisioned_write_capacity_auto_scaling_update", replica_updates="test-replica_updates", region_name="us-east-1")
    mock_client.call.assert_called_once()
