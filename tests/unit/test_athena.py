"""Tests for aws_util.athena module."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from botocore.exceptions import ClientError

import aws_util.athena as athena_mod
from aws_util.athena import (
    AthenaExecution,
    start_query,
    get_query_execution,
    get_query_results,
    wait_for_query,
    run_query,
    get_table_schema,
    run_ddl,
    stop_query,
    _parse_execution,
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
DATABASE = "test_db"
OUTPUT = "s3://my-bucket/athena-results/"
QID = "query-exec-id-123"


def _mock_execution(state: str = "SUCCEEDED") -> dict:
    return {
        "QueryExecutionId": QID,
        "Query": "SELECT 1",
        "Status": {"State": state},
        "QueryExecutionContext": {"Database": DATABASE},
        "ResultConfiguration": {"OutputLocation": OUTPUT},
        "Statistics": {"DataScannedInBytes": 1024, "EngineExecutionTimeInMillis": 500},
    }


# ---------------------------------------------------------------------------
# AthenaExecution model
# ---------------------------------------------------------------------------

def test_athena_execution_succeeded():
    ex = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="SUCCEEDED")
    assert ex.succeeded is True
    assert ex.finished is True


def test_athena_execution_failed():
    ex = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="FAILED")
    assert ex.succeeded is False
    assert ex.finished is True


def test_athena_execution_running():
    ex = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="RUNNING")
    assert ex.succeeded is False
    assert ex.finished is False


def test_athena_execution_cancelled():
    ex = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="CANCELLED")
    assert ex.finished is True


# ---------------------------------------------------------------------------
# _parse_execution
# ---------------------------------------------------------------------------

def test_parse_execution_full():
    ex = _parse_execution(_mock_execution())
    assert ex.query_execution_id == QID
    assert ex.state == "SUCCEEDED"
    assert ex.database == DATABASE
    assert ex.data_scanned_bytes == 1024


def test_parse_execution_minimal():
    ex = _parse_execution({"QueryExecutionId": "abc", "Status": {}, "Query": ""})
    assert ex.state == "UNKNOWN"


# ---------------------------------------------------------------------------
# start_query
# ---------------------------------------------------------------------------

def test_start_query_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_query_execution.return_value = {"QueryExecutionId": QID}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    result = start_query("SELECT 1", DATABASE, OUTPUT, region_name=REGION)
    assert result == QID


def test_start_query_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_query_execution.side_effect = ClientError(
        {"Error": {"Code": "InvalidRequestException", "Message": "bad query"}},
        "StartQueryExecution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start Athena query"):
        start_query("BAD SQL", DATABASE, OUTPUT, region_name=REGION)


# ---------------------------------------------------------------------------
# get_query_execution
# ---------------------------------------------------------------------------

def test_get_query_execution_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query_execution.return_value = {"QueryExecution": _mock_execution()}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_query_execution(QID, region_name=REGION)
    assert isinstance(result, AthenaExecution)
    assert result.state == "SUCCEEDED"


def test_get_query_execution_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query_execution.side_effect = ClientError(
        {"Error": {"Code": "InvalidRequestException", "Message": "not found"}},
        "GetQueryExecution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_query_execution failed"):
        get_query_execution("nonexistent", region_name=REGION)


# ---------------------------------------------------------------------------
# get_query_results
# ---------------------------------------------------------------------------

def test_get_query_results_success(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "col1"}, {"VarCharValue": "col2"}]},
                    {"Data": [{"VarCharValue": "val1"}, {"VarCharValue": "val2"}]},
                ]
            }
        }
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_query_results(QID, region_name=REGION)
    assert result == [{"col1": "val1", "col2": "val2"}]


def test_get_query_results_with_max_rows(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.return_value = [
        {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "col1"}]},
                    {"Data": [{"VarCharValue": "row1"}]},
                    {"Data": [{"VarCharValue": "row2"}]},
                    {"Data": [{"VarCharValue": "row3"}]},
                ]
            }
        }
    ]
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    result = get_query_results(QID, max_rows=2, region_name=REGION)
    assert len(result) == 2


def test_get_query_results_runtime_error(monkeypatch):
    mock_paginator = MagicMock()
    mock_paginator.paginate.side_effect = ClientError(
        {"Error": {"Code": "InvalidRequestException", "Message": "error"}}, "GetQueryResults"
    )
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = mock_paginator
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="get_query_results failed"):
        get_query_results("bad-id", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_query
# ---------------------------------------------------------------------------

def test_wait_for_query_already_done(monkeypatch):
    finished = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="SUCCEEDED")
    monkeypatch.setattr(athena_mod, "get_query_execution", lambda qid, region_name=None: finished)
    result = wait_for_query(QID, timeout=5.0, poll_interval=0.01, region_name=REGION)
    assert result.succeeded


def test_wait_for_query_timeout(monkeypatch):
    running = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="RUNNING")
    monkeypatch.setattr(athena_mod, "get_query_execution", lambda qid, region_name=None: running)
    with pytest.raises(TimeoutError):
        wait_for_query(QID, timeout=0.0, poll_interval=0.0, region_name=REGION)


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------

def test_run_query_success(monkeypatch):
    monkeypatch.setattr(athena_mod, "start_query", lambda *a, **kw: QID)
    finished = AthenaExecution(query_execution_id=QID, query="SELECT 1", state="SUCCEEDED")
    monkeypatch.setattr(athena_mod, "wait_for_query", lambda qid, **kw: finished)
    monkeypatch.setattr(
        athena_mod, "get_query_results", lambda qid, max_rows=None, region_name=None: [{"a": "1"}]
    )
    result = run_query("SELECT 1", DATABASE, OUTPUT, region_name=REGION)
    assert result == [{"a": "1"}]


def test_run_query_failed_raises(monkeypatch):
    monkeypatch.setattr(athena_mod, "start_query", lambda *a, **kw: QID)
    failed = AthenaExecution(
        query_execution_id=QID, query="SELECT 1", state="FAILED",
        state_change_reason="Syntax error"
    )
    monkeypatch.setattr(athena_mod, "wait_for_query", lambda qid, **kw: failed)
    with pytest.raises(RuntimeError, match="FAILED"):
        run_query("BAD SQL", DATABASE, OUTPUT, region_name=REGION)


# ---------------------------------------------------------------------------
# stop_query
# ---------------------------------------------------------------------------

def test_stop_query_success(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_query_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    stop_query(QID, region_name=REGION)
    mock_client.stop_query_execution.assert_called_once_with(QueryExecutionId=QID)


def test_stop_query_runtime_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_query_execution.side_effect = ClientError(
        {"Error": {"Code": "InvalidRequestException", "Message": "not running"}},
        "StopQueryExecution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="stop_query failed"):
        stop_query("bad-id", region_name=REGION)


# ---------------------------------------------------------------------------
# get_table_schema
# ---------------------------------------------------------------------------

def test_get_table_schema(monkeypatch):
    rows = [{"col_name": "id", "data_type": "int"}, {"#  ": "", "": ""}]

    def fake_run_query(query, database, output_location, workgroup="primary", **kw):
        return rows

    monkeypatch.setattr(athena_mod, "run_query", fake_run_query)
    result = get_table_schema(DATABASE, "my_table", OUTPUT, region_name=REGION)
    assert isinstance(result, list)


# ---------------------------------------------------------------------------
# run_ddl
# ---------------------------------------------------------------------------

def test_run_ddl_success(monkeypatch):
    monkeypatch.setattr(athena_mod, "start_query", lambda *a, **kw: QID)
    finished = AthenaExecution(query_execution_id=QID, query="CREATE TABLE t", state="SUCCEEDED")
    monkeypatch.setattr(athena_mod, "wait_for_query", lambda qid, **kw: finished)
    result = run_ddl("CREATE TABLE t (id INT)", DATABASE, OUTPUT, region_name=REGION)
    assert result.succeeded


def test_run_ddl_failed_raises(monkeypatch):
    monkeypatch.setattr(athena_mod, "start_query", lambda *a, **kw: QID)
    failed = AthenaExecution(
        query_execution_id=QID, query="CREATE TABLE t", state="FAILED",
        state_change_reason="Table already exists"
    )
    monkeypatch.setattr(athena_mod, "wait_for_query", lambda qid, **kw: failed)
    with pytest.raises(RuntimeError, match="DDL statement failed"):
        run_ddl("CREATE TABLE t (id INT)", DATABASE, OUTPUT, region_name=REGION)


def test_wait_for_query_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_query (line 188)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
    import aws_util.athena as athena_mod
    from aws_util.athena import AthenaExecution, wait_for_query

    call_count = {"n": 0}

    def fake_get(qid, region_name=None):
        call_count["n"] += 1
        if call_count["n"] < 2:
            return AthenaExecution(query_execution_id=qid, query="SELECT 1", state="RUNNING")
        return AthenaExecution(query_execution_id=qid, query="SELECT 1", state="SUCCEEDED")

    monkeypatch.setattr(athena_mod, "get_query_execution", fake_get)
    result = wait_for_query("qid-1", timeout=10.0, poll_interval=0.001, region_name="us-east-1")
    assert result.state == "SUCCEEDED"


def test_batch_get_named_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_named_query.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_named_query([], region_name=REGION)
    mock_client.batch_get_named_query.assert_called_once()


def test_batch_get_named_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_named_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_named_query",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get named query"):
        batch_get_named_query([], region_name=REGION)


def test_batch_get_prepared_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_prepared_statement.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_prepared_statement([], "test-work_group", region_name=REGION)
    mock_client.batch_get_prepared_statement.assert_called_once()


def test_batch_get_prepared_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_prepared_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_prepared_statement",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get prepared statement"):
        batch_get_prepared_statement([], "test-work_group", region_name=REGION)


def test_batch_get_query_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_query_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    batch_get_query_execution([], region_name=REGION)
    mock_client.batch_get_query_execution.assert_called_once()


def test_batch_get_query_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_get_query_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_get_query_execution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch get query execution"):
        batch_get_query_execution([], region_name=REGION)


def test_cancel_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_capacity_reservation.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_capacity_reservation("test-name", region_name=REGION)
    mock_client.cancel_capacity_reservation.assert_called_once()


def test_cancel_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_capacity_reservation",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel capacity reservation"):
        cancel_capacity_reservation("test-name", region_name=REGION)


def test_create_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation(1, "test-name", region_name=REGION)
    mock_client.create_capacity_reservation.assert_called_once()


def test_create_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_capacity_reservation",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create capacity reservation"):
        create_capacity_reservation(1, "test-name", region_name=REGION)


def test_create_data_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_catalog.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_data_catalog("test-name", "test-type_value", region_name=REGION)
    mock_client.create_data_catalog.assert_called_once()


def test_create_data_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_data_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_data_catalog",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create data catalog"):
        create_data_catalog("test-name", "test-type_value", region_name=REGION)


def test_create_named_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_named_query.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_named_query("test-name", "test-database", "test-query_string", region_name=REGION)
    mock_client.create_named_query.assert_called_once()


def test_create_named_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_named_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_named_query",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create named query"):
        create_named_query("test-name", "test-database", "test-query_string", region_name=REGION)


def test_create_notebook(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_notebook.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_notebook("test-work_group", "test-name", region_name=REGION)
    mock_client.create_notebook.assert_called_once()


def test_create_notebook_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_notebook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_notebook",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create notebook"):
        create_notebook("test-work_group", "test-name", region_name=REGION)


def test_create_prepared_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prepared_statement.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", region_name=REGION)
    mock_client.create_prepared_statement.assert_called_once()


def test_create_prepared_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_prepared_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_prepared_statement",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create prepared statement"):
        create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", region_name=REGION)


def test_create_presigned_notebook_url(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_presigned_notebook_url.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_presigned_notebook_url("test-session_id", region_name=REGION)
    mock_client.create_presigned_notebook_url.assert_called_once()


def test_create_presigned_notebook_url_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_presigned_notebook_url.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_presigned_notebook_url",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create presigned notebook url"):
        create_presigned_notebook_url("test-session_id", region_name=REGION)


def test_create_work_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_work_group.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    create_work_group("test-name", region_name=REGION)
    mock_client.create_work_group.assert_called_once()


def test_create_work_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_work_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_work_group",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create work group"):
        create_work_group("test-name", region_name=REGION)


def test_delete_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_capacity_reservation.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    delete_capacity_reservation("test-name", region_name=REGION)
    mock_client.delete_capacity_reservation.assert_called_once()


def test_delete_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_capacity_reservation",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete capacity reservation"):
        delete_capacity_reservation("test-name", region_name=REGION)


def test_delete_data_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_catalog.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    delete_data_catalog("test-name", region_name=REGION)
    mock_client.delete_data_catalog.assert_called_once()


def test_delete_data_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_data_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_data_catalog",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete data catalog"):
        delete_data_catalog("test-name", region_name=REGION)


def test_delete_named_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_named_query.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    delete_named_query("test-named_query_id", region_name=REGION)
    mock_client.delete_named_query.assert_called_once()


def test_delete_named_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_named_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_named_query",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete named query"):
        delete_named_query("test-named_query_id", region_name=REGION)


def test_delete_notebook(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_notebook.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    delete_notebook("test-notebook_id", region_name=REGION)
    mock_client.delete_notebook.assert_called_once()


def test_delete_notebook_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_notebook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_notebook",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete notebook"):
        delete_notebook("test-notebook_id", region_name=REGION)


def test_delete_prepared_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prepared_statement.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    delete_prepared_statement("test-statement_name", "test-work_group", region_name=REGION)
    mock_client.delete_prepared_statement.assert_called_once()


def test_delete_prepared_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_prepared_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_prepared_statement",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete prepared statement"):
        delete_prepared_statement("test-statement_name", "test-work_group", region_name=REGION)


def test_delete_work_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_work_group.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    delete_work_group("test-work_group", region_name=REGION)
    mock_client.delete_work_group.assert_called_once()


def test_delete_work_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_work_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_work_group",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete work group"):
        delete_work_group("test-work_group", region_name=REGION)


def test_export_notebook(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_notebook.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    export_notebook("test-notebook_id", region_name=REGION)
    mock_client.export_notebook.assert_called_once()


def test_export_notebook_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_notebook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_notebook",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export notebook"):
        export_notebook("test-notebook_id", region_name=REGION)


def test_get_calculation_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calculation_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_calculation_execution("test-calculation_execution_id", region_name=REGION)
    mock_client.get_calculation_execution.assert_called_once()


def test_get_calculation_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calculation_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_calculation_execution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get calculation execution"):
        get_calculation_execution("test-calculation_execution_id", region_name=REGION)


def test_get_calculation_execution_code(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calculation_execution_code.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_calculation_execution_code("test-calculation_execution_id", region_name=REGION)
    mock_client.get_calculation_execution_code.assert_called_once()


def test_get_calculation_execution_code_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calculation_execution_code.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_calculation_execution_code",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get calculation execution code"):
        get_calculation_execution_code("test-calculation_execution_id", region_name=REGION)


def test_get_calculation_execution_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calculation_execution_status.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_calculation_execution_status("test-calculation_execution_id", region_name=REGION)
    mock_client.get_calculation_execution_status.assert_called_once()


def test_get_calculation_execution_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_calculation_execution_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_calculation_execution_status",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get calculation execution status"):
        get_calculation_execution_status("test-calculation_execution_id", region_name=REGION)


def test_get_capacity_assignment_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_assignment_configuration.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_capacity_assignment_configuration("test-capacity_reservation_name", region_name=REGION)
    mock_client.get_capacity_assignment_configuration.assert_called_once()


def test_get_capacity_assignment_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_assignment_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_capacity_assignment_configuration",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get capacity assignment configuration"):
        get_capacity_assignment_configuration("test-capacity_reservation_name", region_name=REGION)


def test_get_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_reservation.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_capacity_reservation("test-name", region_name=REGION)
    mock_client.get_capacity_reservation.assert_called_once()


def test_get_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_capacity_reservation",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get capacity reservation"):
        get_capacity_reservation("test-name", region_name=REGION)


def test_get_data_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_catalog.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_data_catalog("test-name", region_name=REGION)
    mock_client.get_data_catalog.assert_called_once()


def test_get_data_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_data_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_data_catalog",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get data catalog"):
        get_data_catalog("test-name", region_name=REGION)


def test_get_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_database.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_database("test-catalog_name", "test-database_name", region_name=REGION)
    mock_client.get_database.assert_called_once()


def test_get_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_database",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get database"):
        get_database("test-catalog_name", "test-database_name", region_name=REGION)


def test_get_named_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_named_query.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_named_query("test-named_query_id", region_name=REGION)
    mock_client.get_named_query.assert_called_once()


def test_get_named_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_named_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_named_query",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get named query"):
        get_named_query("test-named_query_id", region_name=REGION)


def test_get_notebook_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_notebook_metadata.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_notebook_metadata("test-notebook_id", region_name=REGION)
    mock_client.get_notebook_metadata.assert_called_once()


def test_get_notebook_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_notebook_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_notebook_metadata",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get notebook metadata"):
        get_notebook_metadata("test-notebook_id", region_name=REGION)


def test_get_prepared_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prepared_statement.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_prepared_statement("test-statement_name", "test-work_group", region_name=REGION)
    mock_client.get_prepared_statement.assert_called_once()


def test_get_prepared_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_prepared_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_prepared_statement",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get prepared statement"):
        get_prepared_statement("test-statement_name", "test-work_group", region_name=REGION)


def test_get_query_runtime_statistics(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query_runtime_statistics.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_query_runtime_statistics("test-query_execution_id", region_name=REGION)
    mock_client.get_query_runtime_statistics.assert_called_once()


def test_get_query_runtime_statistics_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query_runtime_statistics.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_query_runtime_statistics",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get query runtime statistics"):
        get_query_runtime_statistics("test-query_execution_id", region_name=REGION)


def test_get_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_session("test-session_id", region_name=REGION)
    mock_client.get_session.assert_called_once()


def test_get_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_session",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get session"):
        get_session("test-session_id", region_name=REGION)


def test_get_session_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session_status.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_session_status("test-session_id", region_name=REGION)
    mock_client.get_session_status.assert_called_once()


def test_get_session_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_session_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_session_status",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get session status"):
        get_session_status("test-session_id", region_name=REGION)


def test_get_table_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_metadata.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", region_name=REGION)
    mock_client.get_table_metadata.assert_called_once()


def test_get_table_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_table_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_table_metadata",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get table metadata"):
        get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", region_name=REGION)


def test_get_work_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_work_group.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    get_work_group("test-work_group", region_name=REGION)
    mock_client.get_work_group.assert_called_once()


def test_get_work_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_work_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_work_group",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get work group"):
        get_work_group("test-work_group", region_name=REGION)


def test_import_notebook(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_notebook.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    import_notebook("test-work_group", "test-name", "test-type_value", region_name=REGION)
    mock_client.import_notebook.assert_called_once()


def test_import_notebook_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.import_notebook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "import_notebook",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to import notebook"):
        import_notebook("test-work_group", "test-name", "test-type_value", region_name=REGION)


def test_list_application_dpu_sizes(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_dpu_sizes.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_application_dpu_sizes(region_name=REGION)
    mock_client.list_application_dpu_sizes.assert_called_once()


def test_list_application_dpu_sizes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_application_dpu_sizes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_application_dpu_sizes",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list application dpu sizes"):
        list_application_dpu_sizes(region_name=REGION)


def test_list_calculation_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_calculation_executions.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_calculation_executions("test-session_id", region_name=REGION)
    mock_client.list_calculation_executions.assert_called_once()


def test_list_calculation_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_calculation_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_calculation_executions",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list calculation executions"):
        list_calculation_executions("test-session_id", region_name=REGION)


def test_list_capacity_reservations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_capacity_reservations.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_capacity_reservations(region_name=REGION)
    mock_client.list_capacity_reservations.assert_called_once()


def test_list_capacity_reservations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_capacity_reservations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_capacity_reservations",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list capacity reservations"):
        list_capacity_reservations(region_name=REGION)


def test_list_data_catalogs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_catalogs.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_data_catalogs(region_name=REGION)
    mock_client.list_data_catalogs.assert_called_once()


def test_list_data_catalogs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_data_catalogs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_data_catalogs",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list data catalogs"):
        list_data_catalogs(region_name=REGION)


def test_list_databases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_databases.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_databases("test-catalog_name", region_name=REGION)
    mock_client.list_databases.assert_called_once()


def test_list_databases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_databases",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list databases"):
        list_databases("test-catalog_name", region_name=REGION)


def test_list_engine_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_engine_versions.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_engine_versions(region_name=REGION)
    mock_client.list_engine_versions.assert_called_once()


def test_list_engine_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_engine_versions",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list engine versions"):
        list_engine_versions(region_name=REGION)


def test_list_executors(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_executors.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_executors("test-session_id", region_name=REGION)
    mock_client.list_executors.assert_called_once()


def test_list_executors_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_executors.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_executors",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list executors"):
        list_executors("test-session_id", region_name=REGION)


def test_list_named_queries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_named_queries.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_named_queries(region_name=REGION)
    mock_client.list_named_queries.assert_called_once()


def test_list_named_queries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_named_queries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_named_queries",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list named queries"):
        list_named_queries(region_name=REGION)


def test_list_notebook_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_notebook_metadata.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_notebook_metadata("test-work_group", region_name=REGION)
    mock_client.list_notebook_metadata.assert_called_once()


def test_list_notebook_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_notebook_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_notebook_metadata",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list notebook metadata"):
        list_notebook_metadata("test-work_group", region_name=REGION)


def test_list_notebook_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_notebook_sessions.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_notebook_sessions("test-notebook_id", region_name=REGION)
    mock_client.list_notebook_sessions.assert_called_once()


def test_list_notebook_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_notebook_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_notebook_sessions",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list notebook sessions"):
        list_notebook_sessions("test-notebook_id", region_name=REGION)


def test_list_prepared_statements(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prepared_statements.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_prepared_statements("test-work_group", region_name=REGION)
    mock_client.list_prepared_statements.assert_called_once()


def test_list_prepared_statements_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_prepared_statements.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_prepared_statements",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list prepared statements"):
        list_prepared_statements("test-work_group", region_name=REGION)


def test_list_query_executions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_query_executions.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_query_executions(region_name=REGION)
    mock_client.list_query_executions.assert_called_once()


def test_list_query_executions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_query_executions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_query_executions",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list query executions"):
        list_query_executions(region_name=REGION)


def test_list_sessions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sessions.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_sessions("test-work_group", region_name=REGION)
    mock_client.list_sessions.assert_called_once()


def test_list_sessions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_sessions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_sessions",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list sessions"):
        list_sessions("test-work_group", region_name=REGION)


def test_list_table_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_table_metadata.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_table_metadata("test-catalog_name", "test-database_name", region_name=REGION)
    mock_client.list_table_metadata.assert_called_once()


def test_list_table_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_table_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_table_metadata",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list table metadata"):
        list_table_metadata("test-catalog_name", "test-database_name", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_work_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_work_groups.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    list_work_groups(region_name=REGION)
    mock_client.list_work_groups.assert_called_once()


def test_list_work_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_work_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_work_groups",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list work groups"):
        list_work_groups(region_name=REGION)


def test_put_capacity_assignment_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_capacity_assignment_configuration.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    put_capacity_assignment_configuration("test-capacity_reservation_name", [], region_name=REGION)
    mock_client.put_capacity_assignment_configuration.assert_called_once()


def test_put_capacity_assignment_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_capacity_assignment_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_capacity_assignment_configuration",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put capacity assignment configuration"):
        put_capacity_assignment_configuration("test-capacity_reservation_name", [], region_name=REGION)


def test_start_calculation_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_calculation_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    start_calculation_execution("test-session_id", region_name=REGION)
    mock_client.start_calculation_execution.assert_called_once()


def test_start_calculation_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_calculation_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_calculation_execution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start calculation execution"):
        start_calculation_execution("test-session_id", region_name=REGION)


def test_start_query_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_query_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    start_query_execution("test-query_string", region_name=REGION)
    mock_client.start_query_execution.assert_called_once()


def test_start_query_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_query_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_query_execution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start query execution"):
        start_query_execution("test-query_string", region_name=REGION)


def test_start_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_session.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    start_session("test-work_group", {}, region_name=REGION)
    mock_client.start_session.assert_called_once()


def test_start_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_session",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start session"):
        start_session("test-work_group", {}, region_name=REGION)


def test_stop_calculation_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_calculation_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    stop_calculation_execution("test-calculation_execution_id", region_name=REGION)
    mock_client.stop_calculation_execution.assert_called_once()


def test_stop_calculation_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_calculation_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_calculation_execution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop calculation execution"):
        stop_calculation_execution("test-calculation_execution_id", region_name=REGION)


def test_stop_query_execution(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_query_execution.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    stop_query_execution("test-query_execution_id", region_name=REGION)
    mock_client.stop_query_execution.assert_called_once()


def test_stop_query_execution_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_query_execution.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_query_execution",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop query execution"):
        stop_query_execution("test-query_execution_id", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


def test_terminate_session(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_session.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    terminate_session("test-session_id", region_name=REGION)
    mock_client.terminate_session.assert_called_once()


def test_terminate_session_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.terminate_session.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "terminate_session",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to terminate session"):
        terminate_session("test-session_id", region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_capacity_reservation(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_capacity_reservation.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_capacity_reservation(1, "test-name", region_name=REGION)
    mock_client.update_capacity_reservation.assert_called_once()


def test_update_capacity_reservation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_capacity_reservation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_capacity_reservation",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update capacity reservation"):
        update_capacity_reservation(1, "test-name", region_name=REGION)


def test_update_data_catalog(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_catalog.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_data_catalog("test-name", "test-type_value", region_name=REGION)
    mock_client.update_data_catalog.assert_called_once()


def test_update_data_catalog_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_data_catalog.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_data_catalog",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update data catalog"):
        update_data_catalog("test-name", "test-type_value", region_name=REGION)


def test_update_named_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_named_query.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_named_query("test-named_query_id", "test-name", "test-query_string", region_name=REGION)
    mock_client.update_named_query.assert_called_once()


def test_update_named_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_named_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_named_query",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update named query"):
        update_named_query("test-named_query_id", "test-name", "test-query_string", region_name=REGION)


def test_update_notebook(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_notebook.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_notebook("test-notebook_id", "test-payload", "test-type_value", region_name=REGION)
    mock_client.update_notebook.assert_called_once()


def test_update_notebook_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_notebook.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_notebook",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update notebook"):
        update_notebook("test-notebook_id", "test-payload", "test-type_value", region_name=REGION)


def test_update_notebook_metadata(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_notebook_metadata.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_notebook_metadata("test-notebook_id", "test-name", region_name=REGION)
    mock_client.update_notebook_metadata.assert_called_once()


def test_update_notebook_metadata_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_notebook_metadata.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_notebook_metadata",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update notebook metadata"):
        update_notebook_metadata("test-notebook_id", "test-name", region_name=REGION)


def test_update_prepared_statement(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_prepared_statement.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", region_name=REGION)
    mock_client.update_prepared_statement.assert_called_once()


def test_update_prepared_statement_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_prepared_statement.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_prepared_statement",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update prepared statement"):
        update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", region_name=REGION)


def test_update_work_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_work_group.return_value = {}
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    update_work_group("test-work_group", region_name=REGION)
    mock_client.update_work_group.assert_called_once()


def test_update_work_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_work_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_work_group",
    )
    monkeypatch.setattr(athena_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update work group"):
        update_work_group("test-work_group", region_name=REGION)


def test_create_capacity_reservation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import create_capacity_reservation
    mock_client = MagicMock()
    mock_client.create_capacity_reservation.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    create_capacity_reservation("test-target_dpus", "test-name", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_capacity_reservation.assert_called_once()

def test_create_data_catalog_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import create_data_catalog
    mock_client = MagicMock()
    mock_client.create_data_catalog.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    create_data_catalog("test-name", "test-type_value", description="test-description", parameters="test-parameters", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_data_catalog.assert_called_once()

def test_create_named_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import create_named_query
    mock_client = MagicMock()
    mock_client.create_named_query.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    create_named_query("test-name", "test-database", "test-query_string", description="test-description", client_request_token="test-client_request_token", work_group="test-work_group", region_name="us-east-1")
    mock_client.create_named_query.assert_called_once()

def test_create_notebook_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import create_notebook
    mock_client = MagicMock()
    mock_client.create_notebook.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    create_notebook("test-work_group", "test-name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.create_notebook.assert_called_once()

def test_create_prepared_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import create_prepared_statement
    mock_client = MagicMock()
    mock_client.create_prepared_statement.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    create_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", description="test-description", region_name="us-east-1")
    mock_client.create_prepared_statement.assert_called_once()

def test_create_work_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import create_work_group
    mock_client = MagicMock()
    mock_client.create_work_group.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    create_work_group("test-name", configuration={}, description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_work_group.assert_called_once()

def test_delete_data_catalog_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import delete_data_catalog
    mock_client = MagicMock()
    mock_client.delete_data_catalog.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    delete_data_catalog("test-name", delete_catalog_only=True, region_name="us-east-1")
    mock_client.delete_data_catalog.assert_called_once()

def test_delete_work_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import delete_work_group
    mock_client = MagicMock()
    mock_client.delete_work_group.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    delete_work_group("test-work_group", recursive_delete_option=True, region_name="us-east-1")
    mock_client.delete_work_group.assert_called_once()

def test_get_data_catalog_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import get_data_catalog
    mock_client = MagicMock()
    mock_client.get_data_catalog.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    get_data_catalog("test-name", work_group="test-work_group", region_name="us-east-1")
    mock_client.get_data_catalog.assert_called_once()

def test_get_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import get_database
    mock_client = MagicMock()
    mock_client.get_database.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    get_database("test-catalog_name", "test-database_name", work_group="test-work_group", region_name="us-east-1")
    mock_client.get_database.assert_called_once()

def test_get_table_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import get_table_metadata
    mock_client = MagicMock()
    mock_client.get_table_metadata.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    get_table_metadata("test-catalog_name", "test-database_name", "test-table_name", work_group="test-work_group", region_name="us-east-1")
    mock_client.get_table_metadata.assert_called_once()

def test_import_notebook_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import import_notebook
    mock_client = MagicMock()
    mock_client.import_notebook.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    import_notebook("test-work_group", "test-name", "test-type_value", payload="test-payload", notebook_s3_location_uri="test-notebook_s3_location_uri", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.import_notebook.assert_called_once()

def test_list_application_dpu_sizes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_application_dpu_sizes
    mock_client = MagicMock()
    mock_client.list_application_dpu_sizes.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_application_dpu_sizes(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_application_dpu_sizes.assert_called_once()

def test_list_calculation_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_calculation_executions
    mock_client = MagicMock()
    mock_client.list_calculation_executions.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_calculation_executions("test-session_id", state_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_calculation_executions.assert_called_once()

def test_list_capacity_reservations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_capacity_reservations
    mock_client = MagicMock()
    mock_client.list_capacity_reservations.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_capacity_reservations(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_capacity_reservations.assert_called_once()

def test_list_data_catalogs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_data_catalogs
    mock_client = MagicMock()
    mock_client.list_data_catalogs.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_data_catalogs(next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.list_data_catalogs.assert_called_once()

def test_list_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_databases
    mock_client = MagicMock()
    mock_client.list_databases.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_databases("test-catalog_name", next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.list_databases.assert_called_once()

def test_list_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_engine_versions
    mock_client = MagicMock()
    mock_client.list_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_engine_versions(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_engine_versions.assert_called_once()

def test_list_executors_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_executors
    mock_client = MagicMock()
    mock_client.list_executors.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_executors("test-session_id", executor_state_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_executors.assert_called_once()

def test_list_named_queries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_named_queries
    mock_client = MagicMock()
    mock_client.list_named_queries.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_named_queries(next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.list_named_queries.assert_called_once()

def test_list_notebook_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_notebook_metadata
    mock_client = MagicMock()
    mock_client.list_notebook_metadata.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_notebook_metadata("test-work_group", filters=[{}], next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_notebook_metadata.assert_called_once()

def test_list_notebook_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_notebook_sessions
    mock_client = MagicMock()
    mock_client.list_notebook_sessions.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_notebook_sessions("test-notebook_id", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_notebook_sessions.assert_called_once()

def test_list_prepared_statements_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_prepared_statements
    mock_client = MagicMock()
    mock_client.list_prepared_statements.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_prepared_statements("test-work_group", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_prepared_statements.assert_called_once()

def test_list_query_executions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_query_executions
    mock_client = MagicMock()
    mock_client.list_query_executions.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_query_executions(next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.list_query_executions.assert_called_once()

def test_list_sessions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_sessions
    mock_client = MagicMock()
    mock_client.list_sessions.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_sessions("test-work_group", state_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_sessions.assert_called_once()

def test_list_table_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_table_metadata
    mock_client = MagicMock()
    mock_client.list_table_metadata.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_table_metadata("test-catalog_name", "test-database_name", expression="test-expression", next_token="test-next_token", max_results=1, work_group="test-work_group", region_name="us-east-1")
    mock_client.list_table_metadata.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_list_work_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import list_work_groups
    mock_client = MagicMock()
    mock_client.list_work_groups.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    list_work_groups(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_work_groups.assert_called_once()

def test_start_calculation_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import start_calculation_execution
    mock_client = MagicMock()
    mock_client.start_calculation_execution.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    start_calculation_execution("test-session_id", description="test-description", calculation_configuration={}, code_block="test-code_block", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.start_calculation_execution.assert_called_once()

def test_start_query_execution_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import start_query_execution
    mock_client = MagicMock()
    mock_client.start_query_execution.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    start_query_execution("test-query_string", client_request_token="test-client_request_token", query_execution_context={}, result_configuration={}, work_group="test-work_group", execution_parameters="test-execution_parameters", result_reuse_configuration={}, region_name="us-east-1")
    mock_client.start_query_execution.assert_called_once()

def test_start_session_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import start_session
    mock_client = MagicMock()
    mock_client.start_session.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    start_session("test-work_group", {}, description="test-description", notebook_version="test-notebook_version", session_idle_timeout_in_minutes=1, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.start_session.assert_called_once()

def test_update_data_catalog_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import update_data_catalog
    mock_client = MagicMock()
    mock_client.update_data_catalog.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    update_data_catalog("test-name", "test-type_value", description="test-description", parameters="test-parameters", region_name="us-east-1")
    mock_client.update_data_catalog.assert_called_once()

def test_update_named_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import update_named_query
    mock_client = MagicMock()
    mock_client.update_named_query.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    update_named_query("test-named_query_id", "test-name", "test-query_string", description="test-description", region_name="us-east-1")
    mock_client.update_named_query.assert_called_once()

def test_update_notebook_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import update_notebook
    mock_client = MagicMock()
    mock_client.update_notebook.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    update_notebook("test-notebook_id", "test-payload", "test-type_value", session_id="test-session_id", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_notebook.assert_called_once()

def test_update_notebook_metadata_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import update_notebook_metadata
    mock_client = MagicMock()
    mock_client.update_notebook_metadata.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    update_notebook_metadata("test-notebook_id", "test-name", client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_notebook_metadata.assert_called_once()

def test_update_prepared_statement_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import update_prepared_statement
    mock_client = MagicMock()
    mock_client.update_prepared_statement.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    update_prepared_statement("test-statement_name", "test-work_group", "test-query_statement", description="test-description", region_name="us-east-1")
    mock_client.update_prepared_statement.assert_called_once()

def test_update_work_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.athena import update_work_group
    mock_client = MagicMock()
    mock_client.update_work_group.return_value = {}
    monkeypatch.setattr("aws_util.athena.get_client", lambda *a, **kw: mock_client)
    update_work_group("test-work_group", description="test-description", configuration_updates={}, state="test-state", region_name="us-east-1")
    mock_client.update_work_group.assert_called_once()
