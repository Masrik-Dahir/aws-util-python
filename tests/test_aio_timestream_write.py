"""Tests for aws_util.aio.timestream_write module."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from aws_util.aio.timestream_write import (
    DatabaseDescription,
    Record,
    TableDescription,
    WriteRecordsResult,
    create_database,
    create_table,
    delete_database,
    delete_table,
    describe_database,
    describe_table,
    list_databases,
    list_tables,
    update_database,
    update_table,
    write_records,
    create_batch_load_task,
    describe_batch_load_task,
    describe_endpoints,
    list_batch_load_tasks,
    list_tags_for_resource,
    resume_batch_load_task,
    tag_resource,
    untag_resource,
)


REGION = "us-east-1"
DB_NAME = "my-db"
TABLE_NAME = "my-table"


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _db_dict(**overrides):
    d = {"DatabaseName": DB_NAME, "Arn": "arn:...", "TableCount": 1}
    d.update(overrides)
    return d


def _table_dict(**overrides):
    d = {
        "DatabaseName": DB_NAME,
        "TableName": TABLE_NAME,
        "Arn": "arn:...",
        "TableStatus": "ACTIVE",
        "RetentionProperties": {
            "MemoryStoreRetentionPeriodInHours": 24,
            "MagneticStoreRetentionPeriodInDays": 365,
        },
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------


async def test_create_database_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Database": _db_dict()}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await create_database(DB_NAME, region_name=REGION)
    assert result.database_name == DB_NAME

async def test_create_database_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_database(DB_NAME, region_name=REGION)


async def test_describe_database_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Database": _db_dict()}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await describe_database(DB_NAME, region_name=REGION)
    assert result.database_name == DB_NAME


async def test_describe_database_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await describe_database(DB_NAME, region_name=REGION)


async def test_list_databases_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Databases": [_db_dict()], "NextToken": "tok",
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    dbs, token = await list_databases(max_results=10, region_name=REGION)
    assert len(dbs) == 1
    assert token == "tok"


async def test_list_databases_with_token(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Databases": []}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    dbs, token = await list_databases(next_token="prev", region_name=REGION)
    assert dbs == []


async def test_list_databases_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_databases(region_name=REGION)


async def test_delete_database_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await delete_database(DB_NAME, region_name=REGION)
    assert result is True


async def test_delete_database_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_database(DB_NAME, region_name=REGION)


async def test_update_database_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Database": _db_dict()}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await update_database(
        DB_NAME, kms_key_id="arn:aws:kms:...", region_name=REGION,
    )
    assert result.database_name == DB_NAME


async def test_update_database_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await update_database(
            DB_NAME, kms_key_id="arn:...", region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


async def test_create_table_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Table": _table_dict()}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await create_table(DB_NAME, TABLE_NAME, region_name=REGION)
    assert result.table_name == TABLE_NAME

async def test_create_table_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await create_table(DB_NAME, TABLE_NAME, region_name=REGION)


async def test_describe_table_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Table": _table_dict()}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await describe_table(DB_NAME, TABLE_NAME, region_name=REGION)
    assert result.table_name == TABLE_NAME


async def test_describe_table_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await describe_table(DB_NAME, TABLE_NAME, region_name=REGION)


async def test_list_tables_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "Tables": [_table_dict()], "NextToken": "tok",
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    tables, token = await list_tables(
        database_name=DB_NAME, max_results=10, region_name=REGION,
    )
    assert len(tables) == 1
    assert token == "tok"


async def test_list_tables_with_token(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Tables": []}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    tables, token = await list_tables(next_token="prev", region_name=REGION)
    assert tables == []


async def test_list_tables_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await list_tables(region_name=REGION)


async def test_delete_table_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await delete_table(DB_NAME, TABLE_NAME, region_name=REGION)
    assert result is True


async def test_delete_table_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await delete_table(DB_NAME, TABLE_NAME, region_name=REGION)


async def test_update_table_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"Table": _table_dict()}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await update_table(
        DB_NAME, TABLE_NAME,
        retention_properties={"MemoryStoreRetentionPeriodInHours": 48},
        magnetic_store_write_properties={"EnableMagneticStoreWrites": True},
        region_name=REGION,
    )
    assert result.table_name == TABLE_NAME


async def test_update_table_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await update_table(DB_NAME, TABLE_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# write_records
# ---------------------------------------------------------------------------


async def test_write_records_success(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "RecordsIngested": {"Total": 2, "MemoryStore": 2, "MagneticStore": 0},
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    records = [
        Record(
            measure_name="cpu", measure_value="0.8",
            time="1234567890000", time_unit="MILLISECONDS",
            dimensions=[{"Name": "host", "Value": "h1"}],
        ),
    ]
    result = await write_records(
        DB_NAME, TABLE_NAME, records, region_name=REGION,
    )
    assert result.records_ingested_total == 2


async def test_write_records_with_common_attrs(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "RecordsIngested": {"Total": 1, "MemoryStore": 1, "MagneticStore": 0},
    }
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    result = await write_records(
        DB_NAME, TABLE_NAME,
        [{"MeasureName": "cpu", "MeasureValue": "0.5"}],
        common_attributes={"MeasureName": "cpu"},
        region_name=REGION,
    )
    assert result.records_ingested_total == 1


async def test_write_records_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client", _mock_factory(client),
    )
    with pytest.raises(RuntimeError):
        await write_records(
            DB_NAME, TABLE_NAME, [{"MeasureName": "x"}], region_name=REGION,
        )


async def test_create_batch_load_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_batch_load_task({}, {}, "test-target_database_name", "test-target_table_name", )
    mock_client.call.assert_called_once()


async def test_create_batch_load_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_batch_load_task({}, {}, "test-target_database_name", "test-target_table_name", )


async def test_describe_batch_load_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_batch_load_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_describe_batch_load_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_batch_load_task("test-task_id", )


async def test_describe_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_endpoints()


async def test_list_batch_load_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_batch_load_tasks()
    mock_client.call.assert_called_once()


async def test_list_batch_load_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_batch_load_tasks()


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_resume_batch_load_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await resume_batch_load_task("test-task_id", )
    mock_client.call.assert_called_once()


async def test_resume_batch_load_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await resume_batch_load_task("test-task_id", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.timestream_write.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_create_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import create_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await create_database("test-database_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import list_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await list_databases(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import create_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await create_table("test-database_name", "test-table_name", retention_properties={}, magnetic_store_write_properties={}, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import list_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await list_tables(database_name="test-database_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import update_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await update_table("test-database_name", "test-table_name", retention_properties={}, magnetic_store_write_properties={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_batch_load_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import create_batch_load_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await create_batch_load_task({}, 1, "test-target_database_name", "test-target_table_name", client_token="test-client_token", data_model_configuration={}, record_version="test-record_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_batch_load_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.timestream_write import list_batch_load_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.timestream_write.async_client", lambda *a, **kw: mock_client)
    await list_batch_load_tasks(next_token="test-next_token", max_results=1, task_status="test-task_status", region_name="us-east-1")
    mock_client.call.assert_called_once()
