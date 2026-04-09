

"""Tests for aws_util.aio.athena — native async Athena utilities."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

import aws_util.aio.athena as athena_mod
from aws_util.aio.athena import (

    AthenaExecution,
    _parse_execution,
    get_query_execution,
    get_query_results,
    get_table_schema,
    run_ddl,
    run_query,
    start_query,
    stop_query,
    wait_for_query,
    batch_get_named_query,
    batch_get_prepared_statement,
    batch_get_query_execution,
    cancel_capacity_reservation,
    create_capacity_reservation,
    create_data_catalog,
    create_named_query,
    create_notebook,
    create_prepared_statement,
    create_presigned_notebook_url,
    create_work_group,
    delete_capacity_reservation,
    delete_data_catalog,
    delete_named_query,
    delete_notebook,
    delete_prepared_statement,
    delete_work_group,
    export_notebook,
    get_calculation_execution,
    get_calculation_execution_code,
    get_calculation_execution_status,
    get_capacity_assignment_configuration,
    get_capacity_reservation,
    get_data_catalog,
    get_database,
    get_named_query,
    get_notebook_metadata,
    get_prepared_statement,
    get_query_runtime_statistics,
    get_session,
    get_session_status,
    get_table_metadata,
    get_work_group,
    import_notebook,
    list_application_dpu_sizes,
    list_calculation_executions,
    list_capacity_reservations,
    list_data_catalogs,
    list_databases,
    list_engine_versions,
    list_executors,
    list_named_queries,
    list_notebook_metadata,
    list_notebook_sessions,
    list_prepared_statements,
    list_query_executions,
    list_sessions,
    list_table_metadata,
    list_tags_for_resource,
    list_work_groups,
    put_capacity_assignment_configuration,
    start_calculation_execution,
    start_query_execution,
    start_session,
    stop_calculation_execution,
    stop_query_execution,
    tag_resource,
    terminate_session,
    untag_resource,
    update_capacity_reservation,
    update_data_catalog,
    update_named_query,
    update_notebook,
    update_notebook_metadata,
    update_prepared_statement,
    update_work_group,
)



REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_client(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.athena.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# _parse_execution
# ---------------------------------------------------------------------------


def test_parse_execution_full():
    ex = {
        "QueryExecutionId": "qid-1",
        "Query": "SELECT 1",
        "Status": {
            "State": "SUCCEEDED",
            "StateChangeReason": "done",
            "SubmissionDateTime": "2025-01-01T00:00:00Z",
            "CompletionDateTime": "2025-01-01T00:01:00Z",
        },
        "QueryExecutionContext": {"Database": "mydb"},
        "ResultConfiguration": {"OutputLocation": "s3://bucket/"},
        "Statistics": {
            "DataScannedInBytes": 1024,
            "EngineExecutionTimeInMillis": 500,
        },
    }
    result = _parse_execution(ex)
    assert result.query_execution_id == "qid-1"
    assert result.query == "SELECT 1"
    assert result.state == "SUCCEEDED"
    assert result.database == "mydb"
    assert result.output_location == "s3://bucket/"
    assert result.data_scanned_bytes == 1024
    assert result.engine_execution_time_ms == 500


def test_parse_execution_minimal():
    ex = {"QueryExecutionId": "qid-2"}
    result = _parse_execution(ex)
    assert result.query_execution_id == "qid-2"
    assert result.query == ""
    assert result.state == "UNKNOWN"
    assert result.state_change_reason is None
    assert result.database is None
    assert result.output_location is None
    assert result.data_scanned_bytes is None
    assert result.engine_execution_time_ms is None


# ---------------------------------------------------------------------------
# start_query
# ---------------------------------------------------------------------------


async def test_start_query_success(mock_client):
    mock_client.call.return_value = {"QueryExecutionId": "qid-1"}
    result = await start_query(
        "SELECT 1", "mydb", "s3://bucket/", "primary"
    )
    assert result == "qid-1"


async def test_start_query_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="Failed to start Athena query"):
        await start_query("SELECT 1", "mydb", "s3://bucket/")


# ---------------------------------------------------------------------------
# get_query_execution
# ---------------------------------------------------------------------------


async def test_get_query_execution_success(mock_client):
    mock_client.call.return_value = {
        "QueryExecution": {
            "QueryExecutionId": "qid-1",
            "Query": "SELECT 1",
            "Status": {"State": "SUCCEEDED"},
        }
    }
    result = await get_query_execution("qid-1")
    assert result.state == "SUCCEEDED"


async def test_get_query_execution_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="get_query_execution failed"):
        await get_query_execution("qid-1")


# ---------------------------------------------------------------------------
# get_query_results
# ---------------------------------------------------------------------------


async def test_get_query_results_single_page(mock_client):
    mock_client.call.return_value = {
        "ResultSet": {
            "Rows": [
                {"Data": [{"VarCharValue": "col_a"}, {"VarCharValue": "col_b"}]},
                {"Data": [{"VarCharValue": "v1"}, {"VarCharValue": "v2"}]},
            ]
        }
    }
    rows = await get_query_results("qid-1")
    assert len(rows) == 1
    assert rows[0] == {"col_a": "v1", "col_b": "v2"}


async def test_get_query_results_pagination(mock_client):
    mock_client.call.side_effect = [
        {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "id"}]},
                    {"Data": [{"VarCharValue": "1"}]},
                ]
            },
            "NextToken": "tok",
        },
        {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "2"}]},
                ]
            },
        },
    ]
    rows = await get_query_results("qid-1")
    assert len(rows) == 2
    assert rows[0] == {"id": "1"}
    assert rows[1] == {"id": "2"}


async def test_get_query_results_max_rows(mock_client):
    mock_client.call.return_value = {
        "ResultSet": {
            "Rows": [
                {"Data": [{"VarCharValue": "id"}]},
                {"Data": [{"VarCharValue": "1"}]},
                {"Data": [{"VarCharValue": "2"}]},
                {"Data": [{"VarCharValue": "3"}]},
            ]
        }
    }
    rows = await get_query_results("qid-1", max_rows=2)
    assert len(rows) == 2


async def test_get_query_results_missing_value(mock_client):
    mock_client.call.return_value = {
        "ResultSet": {
            "Rows": [
                {"Data": [{"VarCharValue": "col_a"}]},
                {"Data": [{}]},
            ]
        }
    }
    rows = await get_query_results("qid-1")
    assert rows[0] == {"col_a": ""}


async def test_get_query_results_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="get_query_results failed"):
        await get_query_results("qid-1")


# ---------------------------------------------------------------------------
# wait_for_query
# ---------------------------------------------------------------------------


async def test_wait_for_query_immediately_finished(monkeypatch):
    execution = AthenaExecution(
        query_execution_id="qid-1",
        query="SELECT 1",
        state="SUCCEEDED",
    )
    monkeypatch.setattr(
        athena_mod,
        "get_query_execution",
        AsyncMock(return_value=execution),
    )
    result = await wait_for_query("qid-1")
    assert result.state == "SUCCEEDED"


async def test_wait_for_query_polls_then_succeeds(monkeypatch):
    running = AthenaExecution(
        query_execution_id="qid-1",
        query="SELECT 1",
        state="RUNNING",
    )
    succeeded = AthenaExecution(
        query_execution_id="qid-1",
        query="SELECT 1",
        state="SUCCEEDED",
    )
    monkeypatch.setattr(
        athena_mod,
        "get_query_execution",
        AsyncMock(side_effect=[running, succeeded]),
    )
    monkeypatch.setattr("aws_util.aio.athena.asyncio.sleep", AsyncMock())
    result = await wait_for_query("qid-1", timeout=9999.0)
    assert result.state == "SUCCEEDED"


async def test_wait_for_query_timeout(monkeypatch):
    running = AthenaExecution(
        query_execution_id="qid-1",
        query="SELECT 1",
        state="RUNNING",
    )
    monkeypatch.setattr(
        athena_mod,
        "get_query_execution",
        AsyncMock(return_value=running),
    )
    monkeypatch.setattr("aws_util.aio.athena.asyncio.sleep", AsyncMock())
    counter = {"val": 0.0}

    def fake_monotonic():
        counter["val"] += 1000.0
        return counter["val"]

    monkeypatch.setattr(time, "monotonic", fake_monotonic)
    with pytest.raises(TimeoutError, match="did not finish"):
        await wait_for_query("qid-1", timeout=1.0)


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


async def test_run_query_success(monkeypatch):
    monkeypatch.setattr(
        athena_mod,
        "start_query",
        AsyncMock(return_value="qid-1"),
    )
    monkeypatch.setattr(
        athena_mod,
        "wait_for_query",
        AsyncMock(
            return_value=AthenaExecution(
                query_execution_id="qid-1",
                query="SELECT 1",
                state="SUCCEEDED",
            )
        ),
    )
    monkeypatch.setattr(
        athena_mod,
        "get_query_results",
        AsyncMock(return_value=[{"id": "1"}]),
    )
    rows = await run_query("SELECT 1", "mydb", "s3://bucket/")
    assert rows == [{"id": "1"}]


async def test_run_query_failed(monkeypatch):
    monkeypatch.setattr(
        athena_mod,
        "start_query",
        AsyncMock(return_value="qid-1"),
    )
    monkeypatch.setattr(
        athena_mod,
        "wait_for_query",
        AsyncMock(
            return_value=AthenaExecution(
                query_execution_id="qid-1",
                query="SELECT 1",
                state="FAILED",
                state_change_reason="syntax error",
            )
        ),
    )
    with pytest.raises(RuntimeError, match="finished with state"):
        await run_query("SELECT 1", "mydb", "s3://bucket/")


# ---------------------------------------------------------------------------
# get_table_schema
# ---------------------------------------------------------------------------


async def test_get_table_schema_success(monkeypatch):
    monkeypatch.setattr(
        athena_mod,
        "run_query",
        AsyncMock(
            return_value=[
                {"col1": "id", "col2": "int"},
                {"col1": "name", "col2": "string"},
                {"col1": "# comment", "col2": "ignore"},
                {"col1": "", "col2": "ignore"},
            ]
        ),
    )
    schema = await get_table_schema("mydb", "tbl", "s3://bucket/")
    assert len(schema) == 2
    assert schema[0] == {"name": "id", "type": "int"}
    assert schema[1] == {"name": "name", "type": "string"}


async def test_get_table_schema_empty(monkeypatch):
    monkeypatch.setattr(
        athena_mod,
        "run_query",
        AsyncMock(return_value=[]),
    )
    schema = await get_table_schema("mydb", "tbl", "s3://bucket/")
    assert schema == []


async def test_get_table_schema_single_value_row(monkeypatch):
    """Row with fewer than 2 values => skipped."""
    monkeypatch.setattr(
        athena_mod,
        "run_query",
        AsyncMock(return_value=[{"col1": "solo"}]),
    )
    schema = await get_table_schema("mydb", "tbl", "s3://bucket/")
    assert schema == []


# ---------------------------------------------------------------------------
# run_ddl
# ---------------------------------------------------------------------------


async def test_run_ddl_success(monkeypatch):
    monkeypatch.setattr(
        athena_mod,
        "start_query",
        AsyncMock(return_value="qid-1"),
    )
    succeeded = AthenaExecution(
        query_execution_id="qid-1",
        query="CREATE TABLE ...",
        state="SUCCEEDED",
    )
    monkeypatch.setattr(
        athena_mod,
        "wait_for_query",
        AsyncMock(return_value=succeeded),
    )
    result = await run_ddl("CREATE TABLE ...", "mydb", "s3://bucket/")
    assert result.state == "SUCCEEDED"


async def test_run_ddl_failed(monkeypatch):
    monkeypatch.setattr(
        athena_mod,
        "start_query",
        AsyncMock(return_value="qid-1"),
    )
    failed = AthenaExecution(
        query_execution_id="qid-1",
        query="DROP TABLE ...",
        state="FAILED",
        state_change_reason="access denied",
    )
    monkeypatch.setattr(
        athena_mod,
        "wait_for_query",
        AsyncMock(return_value=failed),
    )
    with pytest.raises(RuntimeError, match="DDL statement failed"):
        await run_ddl("DROP TABLE ...", "mydb", "s3://bucket/")


# ---------------------------------------------------------------------------
# stop_query
# ---------------------------------------------------------------------------


async def test_stop_query_success(mock_client):
    mock_client.call.return_value = {}
    await stop_query("qid-1")
    mock_client.call.assert_called_once()


async def test_stop_query_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="stop_query failed"):
        await stop_query("qid-1")


# ---------------------------------------------------------------------------
# Module __all__
# ---------------------------------------------------------------------------


def test_athena_execution_in_all():
    assert "AthenaExecution" in athena_mod.__all__


async def test_batch_get_named_query(mock_client):
    mock_client.call.return_value = {}
    await batch_get_named_query([], )
    mock_client.call.assert_called_once()


async def test_batch_get_named_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_named_query([], )


async def test_batch_get_named_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get named query"):
        await batch_get_named_query([], )


async def test_batch_get_prepared_statement(mock_client):
    mock_client.call.return_value = {}
    await batch_get_prepared_statement([], "test-work_group", )
    mock_client.call.assert_called_once()


async def test_batch_get_prepared_statement_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_prepared_statement([], "test-work_group", )


async def test_batch_get_prepared_statement_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get prepared statement"):
        await batch_get_prepared_statement([], "test-work_group", )


async def test_batch_get_query_execution(mock_client):
    mock_client.call.return_value = {}
    await batch_get_query_execution([], )
    mock_client.call.assert_called_once()


async def test_batch_get_query_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await batch_get_query_execution([], )


async def test_batch_get_query_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to batch get query execution"):
        await batch_get_query_execution([], )


async def test_cancel_capacity_reservation(mock_client):
    mock_client.call.return_value = {}
    await cancel_capacity_reservation("test-name", )
    mock_client.call.assert_called_once()


async def test_cancel_capacity_reservation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_capacity_reservation("test-name", )


async def test_cancel_capacity_reservation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to cancel capacity reservation"):
        await cancel_capacity_reservation("test-name", )


async def test_create_capacity_reservation(mock_client):
    mock_client.call.return_value = {}
    await create_capacity_reservation(1, "test-name", )
    mock_client.call.assert_called_once()


async def test_create_capacity_reservation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_capacity_reservation(1, "test-name", )


async def test_create_capacity_reservation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create capacity reservation"):
        await create_capacity_reservation(1, "test-name", )


async def test_create_data_catalog(mock_client):
    mock_client.call.return_value = {}
    await create_data_catalog("test-name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_create_data_catalog_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_data_catalog("test-name", "test-type_value", )


async def test_create_data_catalog_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create data catalog"):
        await create_data_catalog("test-name", "test-type_value", )


async def test_create_named_query(mock_client):
    mock_client.call.return_value = {}
    await create_named_query("test-name", "test-database", "test-query_string", )
    mock_client.call.assert_called_once()


async def test_create_named_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_named_query("test-name", "test-database", "test-query_string", )


async def test_create_named_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create named query"):
        await create_named_query("test-name", "test-database", "test-query_string", )


async def test_create_notebook(mock_client):
    mock_client.call.return_value = {}
    await create_notebook("test-work_group", "test-name", )
    mock_client.call.assert_called_once()


async def test_create_notebook_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_notebook("test-work_group", "test-name", )


async def test_create_notebook_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create notebook"):
        await create_notebook("test-work_group", "test-name", )


async def test_create_prepared_statement(mock_client):
    mock_client.call.return_value = {}
    await create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", )
    mock_client.call.assert_called_once()


async def test_create_prepared_statement_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", )


async def test_create_prepared_statement_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create prepared statement"):
        await create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", )


async def test_create_presigned_notebook_url(mock_client):
    mock_client.call.return_value = {}
    await create_presigned_notebook_url("test-session_id", )
    mock_client.call.assert_called_once()


async def test_create_presigned_notebook_url_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_presigned_notebook_url("test-session_id", )


async def test_create_presigned_notebook_url_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create presigned notebook url"):
        await create_presigned_notebook_url("test-session_id", )


async def test_create_work_group(mock_client):
    mock_client.call.return_value = {}
    await create_work_group("test-name", )
    mock_client.call.assert_called_once()


async def test_create_work_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_work_group("test-name", )


async def test_create_work_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create work group"):
        await create_work_group("test-name", )


async def test_delete_capacity_reservation(mock_client):
    mock_client.call.return_value = {}
    await delete_capacity_reservation("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_capacity_reservation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_capacity_reservation("test-name", )


async def test_delete_capacity_reservation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete capacity reservation"):
        await delete_capacity_reservation("test-name", )


async def test_delete_data_catalog(mock_client):
    mock_client.call.return_value = {}
    await delete_data_catalog("test-name", )
    mock_client.call.assert_called_once()


async def test_delete_data_catalog_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_data_catalog("test-name", )


async def test_delete_data_catalog_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete data catalog"):
        await delete_data_catalog("test-name", )


async def test_delete_named_query(mock_client):
    mock_client.call.return_value = {}
    await delete_named_query("test-named_query_id", )
    mock_client.call.assert_called_once()


async def test_delete_named_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_named_query("test-named_query_id", )


async def test_delete_named_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete named query"):
        await delete_named_query("test-named_query_id", )


async def test_delete_notebook(mock_client):
    mock_client.call.return_value = {}
    await delete_notebook("test-notebook_id", )
    mock_client.call.assert_called_once()


async def test_delete_notebook_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_notebook("test-notebook_id", )


async def test_delete_notebook_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete notebook"):
        await delete_notebook("test-notebook_id", )


async def test_delete_prepared_statement(mock_client):
    mock_client.call.return_value = {}
    await delete_prepared_statement("test-statement_name", "test-work_group", )
    mock_client.call.assert_called_once()


async def test_delete_prepared_statement_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_prepared_statement("test-statement_name", "test-work_group", )


async def test_delete_prepared_statement_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete prepared statement"):
        await delete_prepared_statement("test-statement_name", "test-work_group", )


async def test_delete_work_group(mock_client):
    mock_client.call.return_value = {}
    await delete_work_group("test-work_group", )
    mock_client.call.assert_called_once()


async def test_delete_work_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_work_group("test-work_group", )


async def test_delete_work_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete work group"):
        await delete_work_group("test-work_group", )


async def test_export_notebook(mock_client):
    mock_client.call.return_value = {}
    await export_notebook("test-notebook_id", )
    mock_client.call.assert_called_once()


async def test_export_notebook_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await export_notebook("test-notebook_id", )


async def test_export_notebook_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to export notebook"):
        await export_notebook("test-notebook_id", )


async def test_get_calculation_execution(mock_client):
    mock_client.call.return_value = {}
    await get_calculation_execution("test-calculation_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_calculation_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_calculation_execution("test-calculation_execution_id", )


async def test_get_calculation_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get calculation execution"):
        await get_calculation_execution("test-calculation_execution_id", )


async def test_get_calculation_execution_code(mock_client):
    mock_client.call.return_value = {}
    await get_calculation_execution_code("test-calculation_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_calculation_execution_code_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_calculation_execution_code("test-calculation_execution_id", )


async def test_get_calculation_execution_code_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get calculation execution code"):
        await get_calculation_execution_code("test-calculation_execution_id", )


async def test_get_calculation_execution_status(mock_client):
    mock_client.call.return_value = {}
    await get_calculation_execution_status("test-calculation_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_calculation_execution_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_calculation_execution_status("test-calculation_execution_id", )


async def test_get_calculation_execution_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get calculation execution status"):
        await get_calculation_execution_status("test-calculation_execution_id", )


async def test_get_capacity_assignment_configuration(mock_client):
    mock_client.call.return_value = {}
    await get_capacity_assignment_configuration("test-capacity_reservation_name", )
    mock_client.call.assert_called_once()


async def test_get_capacity_assignment_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_capacity_assignment_configuration("test-capacity_reservation_name", )


async def test_get_capacity_assignment_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get capacity assignment configuration"):
        await get_capacity_assignment_configuration("test-capacity_reservation_name", )


async def test_get_capacity_reservation(mock_client):
    mock_client.call.return_value = {}
    await get_capacity_reservation("test-name", )
    mock_client.call.assert_called_once()


async def test_get_capacity_reservation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_capacity_reservation("test-name", )


async def test_get_capacity_reservation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get capacity reservation"):
        await get_capacity_reservation("test-name", )


async def test_get_data_catalog(mock_client):
    mock_client.call.return_value = {}
    await get_data_catalog("test-name", )
    mock_client.call.assert_called_once()


async def test_get_data_catalog_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_data_catalog("test-name", )


async def test_get_data_catalog_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get data catalog"):
        await get_data_catalog("test-name", )


async def test_get_database(mock_client):
    mock_client.call.return_value = {}
    await get_database("test-catalog_name", "test-database_name", )
    mock_client.call.assert_called_once()


async def test_get_database_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_database("test-catalog_name", "test-database_name", )


async def test_get_database_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get database"):
        await get_database("test-catalog_name", "test-database_name", )


async def test_get_named_query(mock_client):
    mock_client.call.return_value = {}
    await get_named_query("test-named_query_id", )
    mock_client.call.assert_called_once()


async def test_get_named_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_named_query("test-named_query_id", )


async def test_get_named_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get named query"):
        await get_named_query("test-named_query_id", )


async def test_get_notebook_metadata(mock_client):
    mock_client.call.return_value = {}
    await get_notebook_metadata("test-notebook_id", )
    mock_client.call.assert_called_once()


async def test_get_notebook_metadata_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_notebook_metadata("test-notebook_id", )


async def test_get_notebook_metadata_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get notebook metadata"):
        await get_notebook_metadata("test-notebook_id", )


async def test_get_prepared_statement(mock_client):
    mock_client.call.return_value = {}
    await get_prepared_statement("test-statement_name", "test-work_group", )
    mock_client.call.assert_called_once()


async def test_get_prepared_statement_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_prepared_statement("test-statement_name", "test-work_group", )


async def test_get_prepared_statement_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get prepared statement"):
        await get_prepared_statement("test-statement_name", "test-work_group", )


async def test_get_query_runtime_statistics(mock_client):
    mock_client.call.return_value = {}
    await get_query_runtime_statistics("test-query_execution_id", )
    mock_client.call.assert_called_once()


async def test_get_query_runtime_statistics_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_query_runtime_statistics("test-query_execution_id", )


async def test_get_query_runtime_statistics_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get query runtime statistics"):
        await get_query_runtime_statistics("test-query_execution_id", )


async def test_get_session(mock_client):
    mock_client.call.return_value = {}
    await get_session("test-session_id", )
    mock_client.call.assert_called_once()


async def test_get_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_session("test-session_id", )


async def test_get_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get session"):
        await get_session("test-session_id", )


async def test_get_session_status(mock_client):
    mock_client.call.return_value = {}
    await get_session_status("test-session_id", )
    mock_client.call.assert_called_once()


async def test_get_session_status_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_session_status("test-session_id", )


async def test_get_session_status_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get session status"):
        await get_session_status("test-session_id", )


async def test_get_table_metadata(mock_client):
    mock_client.call.return_value = {}
    await get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", )
    mock_client.call.assert_called_once()


async def test_get_table_metadata_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", )


async def test_get_table_metadata_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get table metadata"):
        await get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", )


async def test_get_work_group(mock_client):
    mock_client.call.return_value = {}
    await get_work_group("test-work_group", )
    mock_client.call.assert_called_once()


async def test_get_work_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_work_group("test-work_group", )


async def test_get_work_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get work group"):
        await get_work_group("test-work_group", )


async def test_import_notebook(mock_client):
    mock_client.call.return_value = {}
    await import_notebook("test-work_group", "test-name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_import_notebook_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await import_notebook("test-work_group", "test-name", "test-type_value", )


async def test_import_notebook_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to import notebook"):
        await import_notebook("test-work_group", "test-name", "test-type_value", )


async def test_list_application_dpu_sizes(mock_client):
    mock_client.call.return_value = {}
    await list_application_dpu_sizes()
    mock_client.call.assert_called_once()


async def test_list_application_dpu_sizes_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_application_dpu_sizes()


async def test_list_application_dpu_sizes_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list application dpu sizes"):
        await list_application_dpu_sizes()


async def test_list_calculation_executions(mock_client):
    mock_client.call.return_value = {}
    await list_calculation_executions("test-session_id", )
    mock_client.call.assert_called_once()


async def test_list_calculation_executions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_calculation_executions("test-session_id", )


async def test_list_calculation_executions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list calculation executions"):
        await list_calculation_executions("test-session_id", )


async def test_list_capacity_reservations(mock_client):
    mock_client.call.return_value = {}
    await list_capacity_reservations()
    mock_client.call.assert_called_once()


async def test_list_capacity_reservations_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_capacity_reservations()


async def test_list_capacity_reservations_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list capacity reservations"):
        await list_capacity_reservations()


async def test_list_data_catalogs(mock_client):
    mock_client.call.return_value = {}
    await list_data_catalogs()
    mock_client.call.assert_called_once()


async def test_list_data_catalogs_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_data_catalogs()


async def test_list_data_catalogs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list data catalogs"):
        await list_data_catalogs()


async def test_list_databases(mock_client):
    mock_client.call.return_value = {}
    await list_databases("test-catalog_name", )
    mock_client.call.assert_called_once()


async def test_list_databases_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_databases("test-catalog_name", )


async def test_list_databases_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list databases"):
        await list_databases("test-catalog_name", )


async def test_list_engine_versions(mock_client):
    mock_client.call.return_value = {}
    await list_engine_versions()
    mock_client.call.assert_called_once()


async def test_list_engine_versions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_engine_versions()


async def test_list_engine_versions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list engine versions"):
        await list_engine_versions()


async def test_list_executors(mock_client):
    mock_client.call.return_value = {}
    await list_executors("test-session_id", )
    mock_client.call.assert_called_once()


async def test_list_executors_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_executors("test-session_id", )


async def test_list_executors_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list executors"):
        await list_executors("test-session_id", )


async def test_list_named_queries(mock_client):
    mock_client.call.return_value = {}
    await list_named_queries()
    mock_client.call.assert_called_once()


async def test_list_named_queries_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_named_queries()


async def test_list_named_queries_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list named queries"):
        await list_named_queries()


async def test_list_notebook_metadata(mock_client):
    mock_client.call.return_value = {}
    await list_notebook_metadata("test-work_group", )
    mock_client.call.assert_called_once()


async def test_list_notebook_metadata_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_notebook_metadata("test-work_group", )


async def test_list_notebook_metadata_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list notebook metadata"):
        await list_notebook_metadata("test-work_group", )


async def test_list_notebook_sessions(mock_client):
    mock_client.call.return_value = {}
    await list_notebook_sessions("test-notebook_id", )
    mock_client.call.assert_called_once()


async def test_list_notebook_sessions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_notebook_sessions("test-notebook_id", )


async def test_list_notebook_sessions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list notebook sessions"):
        await list_notebook_sessions("test-notebook_id", )


async def test_list_prepared_statements(mock_client):
    mock_client.call.return_value = {}
    await list_prepared_statements("test-work_group", )
    mock_client.call.assert_called_once()


async def test_list_prepared_statements_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_prepared_statements("test-work_group", )


async def test_list_prepared_statements_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list prepared statements"):
        await list_prepared_statements("test-work_group", )


async def test_list_query_executions(mock_client):
    mock_client.call.return_value = {}
    await list_query_executions()
    mock_client.call.assert_called_once()


async def test_list_query_executions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_query_executions()


async def test_list_query_executions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list query executions"):
        await list_query_executions()


async def test_list_sessions(mock_client):
    mock_client.call.return_value = {}
    await list_sessions("test-work_group", )
    mock_client.call.assert_called_once()


async def test_list_sessions_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_sessions("test-work_group", )


async def test_list_sessions_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list sessions"):
        await list_sessions("test-work_group", )


async def test_list_table_metadata(mock_client):
    mock_client.call.return_value = {}
    await list_table_metadata("test-catalog_name", "test-database_name", )
    mock_client.call.assert_called_once()


async def test_list_table_metadata_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_table_metadata("test-catalog_name", "test-database_name", )


async def test_list_table_metadata_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list table metadata"):
        await list_table_metadata("test-catalog_name", "test-database_name", )


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


async def test_list_work_groups(mock_client):
    mock_client.call.return_value = {}
    await list_work_groups()
    mock_client.call.assert_called_once()


async def test_list_work_groups_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_work_groups()


async def test_list_work_groups_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list work groups"):
        await list_work_groups()


async def test_put_capacity_assignment_configuration(mock_client):
    mock_client.call.return_value = {}
    await put_capacity_assignment_configuration("test-capacity_reservation_name", [], )
    mock_client.call.assert_called_once()


async def test_put_capacity_assignment_configuration_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await put_capacity_assignment_configuration("test-capacity_reservation_name", [], )


async def test_put_capacity_assignment_configuration_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to put capacity assignment configuration"):
        await put_capacity_assignment_configuration("test-capacity_reservation_name", [], )


async def test_start_calculation_execution(mock_client):
    mock_client.call.return_value = {}
    await start_calculation_execution("test-session_id", )
    mock_client.call.assert_called_once()


async def test_start_calculation_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_calculation_execution("test-session_id", )


async def test_start_calculation_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start calculation execution"):
        await start_calculation_execution("test-session_id", )


async def test_start_query_execution(mock_client):
    mock_client.call.return_value = {}
    await start_query_execution("test-query_string", )
    mock_client.call.assert_called_once()


async def test_start_query_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_query_execution("test-query_string", )


async def test_start_query_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start query execution"):
        await start_query_execution("test-query_string", )


async def test_start_session(mock_client):
    mock_client.call.return_value = {}
    await start_session("test-work_group", {}, )
    mock_client.call.assert_called_once()


async def test_start_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_session("test-work_group", {}, )


async def test_start_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start session"):
        await start_session("test-work_group", {}, )


async def test_stop_calculation_execution(mock_client):
    mock_client.call.return_value = {}
    await stop_calculation_execution("test-calculation_execution_id", )
    mock_client.call.assert_called_once()


async def test_stop_calculation_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_calculation_execution("test-calculation_execution_id", )


async def test_stop_calculation_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop calculation execution"):
        await stop_calculation_execution("test-calculation_execution_id", )


async def test_stop_query_execution(mock_client):
    mock_client.call.return_value = {}
    await stop_query_execution("test-query_execution_id", )
    mock_client.call.assert_called_once()


async def test_stop_query_execution_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_query_execution("test-query_execution_id", )


async def test_stop_query_execution_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop query execution"):
        await stop_query_execution("test-query_execution_id", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", [], )


async def test_terminate_session(mock_client):
    mock_client.call.return_value = {}
    await terminate_session("test-session_id", )
    mock_client.call.assert_called_once()


async def test_terminate_session_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await terminate_session("test-session_id", )


async def test_terminate_session_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to terminate session"):
        await terminate_session("test-session_id", )


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


async def test_update_capacity_reservation(mock_client):
    mock_client.call.return_value = {}
    await update_capacity_reservation(1, "test-name", )
    mock_client.call.assert_called_once()


async def test_update_capacity_reservation_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_capacity_reservation(1, "test-name", )


async def test_update_capacity_reservation_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update capacity reservation"):
        await update_capacity_reservation(1, "test-name", )


async def test_update_data_catalog(mock_client):
    mock_client.call.return_value = {}
    await update_data_catalog("test-name", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_update_data_catalog_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_data_catalog("test-name", "test-type_value", )


async def test_update_data_catalog_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update data catalog"):
        await update_data_catalog("test-name", "test-type_value", )


async def test_update_named_query(mock_client):
    mock_client.call.return_value = {}
    await update_named_query("test-named_query_id", "test-name", "test-query_string", )
    mock_client.call.assert_called_once()


async def test_update_named_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_named_query("test-named_query_id", "test-name", "test-query_string", )


async def test_update_named_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update named query"):
        await update_named_query("test-named_query_id", "test-name", "test-query_string", )


async def test_update_notebook(mock_client):
    mock_client.call.return_value = {}
    await update_notebook("test-notebook_id", "test-payload", "test-type_value", )
    mock_client.call.assert_called_once()


async def test_update_notebook_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_notebook("test-notebook_id", "test-payload", "test-type_value", )


async def test_update_notebook_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update notebook"):
        await update_notebook("test-notebook_id", "test-payload", "test-type_value", )


async def test_update_notebook_metadata(mock_client):
    mock_client.call.return_value = {}
    await update_notebook_metadata("test-notebook_id", "test-name", )
    mock_client.call.assert_called_once()


async def test_update_notebook_metadata_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_notebook_metadata("test-notebook_id", "test-name", )


async def test_update_notebook_metadata_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update notebook metadata"):
        await update_notebook_metadata("test-notebook_id", "test-name", )


async def test_update_prepared_statement(mock_client):
    mock_client.call.return_value = {}
    await update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", )
    mock_client.call.assert_called_once()


async def test_update_prepared_statement_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", )


async def test_update_prepared_statement_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update prepared statement"):
        await update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", )


async def test_update_work_group(mock_client):
    mock_client.call.return_value = {}
    await update_work_group("test-work_group", )
    mock_client.call.assert_called_once()


async def test_update_work_group_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await update_work_group("test-work_group", )


async def test_update_work_group_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to update work group"):
        await update_work_group("test-work_group", )


@pytest.mark.asyncio
async def test_create_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import create_capacity_reservation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await create_capacity_reservation("test-target_dpus", "test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_data_catalog_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import create_data_catalog
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await create_data_catalog("test-name", "test-type_value", description="test-description", parameters="test-parameters", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_named_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import create_named_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await create_named_query("test-name", "test-database", "test-query_string", description="test-description", client_request_token="test-client_request_token", work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_notebook_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import create_notebook
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await create_notebook("test-work_group", "test-name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_prepared_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import create_prepared_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_work_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import create_work_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await create_work_group("test-name", configuration={}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_data_catalog_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import delete_data_catalog
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await delete_data_catalog("test-name", delete_catalog_only=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_work_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import delete_work_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await delete_work_group("test-work_group", recursive_delete_option=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_data_catalog_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import get_data_catalog
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await get_data_catalog("test-name", work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import get_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await get_database("test-catalog_name", "test-database_name", work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_table_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import get_table_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_import_notebook_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import import_notebook
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await import_notebook("test-work_group", "test-name", "test-type_value", payload="test-payload", notebook_s3_location_uri="test-notebook_s3_location_uri", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_application_dpu_sizes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_application_dpu_sizes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_application_dpu_sizes(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_calculation_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_calculation_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_calculation_executions("test-session_id", state_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_capacity_reservations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_capacity_reservations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_capacity_reservations(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_data_catalogs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_data_catalogs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_data_catalogs(next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_databases("test-catalog_name", next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_engine_versions(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_executors_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_executors
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_executors("test-session_id", executor_state_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_named_queries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_named_queries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_named_queries(next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_notebook_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_notebook_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_notebook_metadata("test-work_group", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_notebook_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_notebook_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_notebook_sessions("test-notebook_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_prepared_statements_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_prepared_statements
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_prepared_statements("test-work_group", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_query_executions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_query_executions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_query_executions(next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_sessions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_sessions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_sessions("test-work_group", state_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_table_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_table_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_table_metadata("test-catalog_name", "test-database_name", expression="test-expression", next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_work_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import list_work_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await list_work_groups(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_calculation_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import start_calculation_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await start_calculation_execution("test-session_id", description="test-description", calculation_configuration={}, code_block="test-code_block", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_query_execution_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import start_query_execution
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await start_query_execution("test-query_string", client_request_token="test-client_request_token", query_execution_context={}, result_configuration={}, work_group="test-work_group", execution_parameters="test-execution_parameters", result_reuse_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_session_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import start_session
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await start_session("test-work_group", {}, description="test-description", notebook_version="test-notebook_version", session_idle_timeout_in_minutes=1, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_data_catalog_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import update_data_catalog
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await update_data_catalog("test-name", "test-type_value", description="test-description", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_named_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import update_named_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await update_named_query("test-named_query_id", "test-name", "test-query_string", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_notebook_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import update_notebook
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await update_notebook("test-notebook_id", "test-payload", "test-type_value", session_id="test-session_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_notebook_metadata_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import update_notebook_metadata
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await update_notebook_metadata("test-notebook_id", "test-name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_prepared_statement_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import update_prepared_statement
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_work_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.athena import update_work_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.athena.async_client", lambda *a, **kw: mock_client)
    await update_work_group("test-work_group", description="test-description", configuration_updates={}, state="test-state", region_name="us-east-1")
    mock_client.call.assert_called_once()
