"""Tests for aws_util.aio.redshift_data -- 100 % line coverage."""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.redshift_data import (
    QueryResult,
    StatementDescription,
    StatementResult,
    batch_execute_statement,
    cancel_statement,
    describe_statement,
    execute_statement,
    get_statement_result,
    list_statements,
    run_query,
    describe_table,
    get_statement_result_v2,
    list_databases,
    list_schemas,
    list_tables,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError


REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


STMT_ID = "stmt-abc-123"
CLUSTER = "my-cluster"
DATABASE = "mydb"
WORKGROUP = "my-workgroup"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:123:secret:cred"
DB_USER = "admin"


def _mock_factory(mock_client: AsyncMock) -> object:
    return lambda *a, **kw: mock_client


def _desc_resp(**kwargs: object) -> dict:
    defaults: dict = {
        "Id": STMT_ID,
        "Status": "FINISHED",
        "QueryString": "SELECT 1",
        "ResultRows": 1,
        "ResultSize": 10,
        "Duration": 500,
        "HasResultSet": True,
        "ClusterIdentifier": CLUSTER,
        "Database": DATABASE,
    }
    defaults.update(kwargs)
    return defaults


def _result_resp(**kwargs: object) -> dict:
    defaults: dict = {
        "ColumnMetadata": [{"name": "id", "typeName": "int4"}],
        "Records": [[{"longValue": 1}]],
        "TotalNumRows": 1,
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# execute_statement
# ---------------------------------------------------------------------------


async def test_execute_statement_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Id": STMT_ID}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await execute_statement(
        "SELECT 1",
        database=DATABASE,
        cluster_identifier=CLUSTER,
    )
    assert isinstance(result, StatementResult)
    assert result.statement_id == STMT_ID
    assert result.cluster_identifier == CLUSTER


async def test_execute_statement_workgroup(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Id": STMT_ID}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await execute_statement(
        "SELECT 1",
        database=DATABASE,
        workgroup_name=WORKGROUP,
    )
    assert result.workgroup_name == WORKGROUP
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["WorkgroupName"] == WORKGROUP


async def test_execute_statement_all_params(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Id": STMT_ID}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await execute_statement(
        "SELECT 1",
        database=DATABASE,
        cluster_identifier=CLUSTER,
        secret_arn=SECRET_ARN,
        db_user=DB_USER,
        statement_name="my-stmt",
        with_event=True,
    )
    assert result.secret_arn == SECRET_ARN
    assert result.db_user == DB_USER
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["StatementName"] == "my-stmt"
    assert call_kwargs["WithEvent"] is True


async def test_execute_statement_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await execute_statement(
            "SELECT 1", database=DATABASE
        )


async def test_execute_statement_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="execute_statement failed"):
        await execute_statement(
            "SELECT 1", database=DATABASE
        )


# ---------------------------------------------------------------------------
# batch_execute_statement
# ---------------------------------------------------------------------------


async def test_batch_execute_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Id": STMT_ID}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await batch_execute_statement(
        ["SELECT 1", "SELECT 2"],
        database=DATABASE,
        cluster_identifier=CLUSTER,
    )
    assert result.statement_id == STMT_ID


async def test_batch_execute_all_params(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Id": STMT_ID}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await batch_execute_statement(
        ["SELECT 1"],
        database=DATABASE,
        workgroup_name=WORKGROUP,
        secret_arn=SECRET_ARN,
        db_user=DB_USER,
        statement_name="batch",
        with_event=True,
    )
    assert result.workgroup_name == WORKGROUP
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["StatementName"] == "batch"
    assert call_kwargs["WithEvent"] is True


async def test_batch_execute_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await batch_execute_statement(
            ["SELECT 1"], database=DATABASE
        )


async def test_batch_execute_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="batch_execute_statement failed"
    ):
        await batch_execute_statement(
            ["SELECT 1"], database=DATABASE
        )


# ---------------------------------------------------------------------------
# describe_statement
# ---------------------------------------------------------------------------


async def test_describe_statement_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _desc_resp()
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await describe_statement(STMT_ID)
    assert isinstance(result, StatementDescription)
    assert result.status == "FINISHED"


async def test_describe_statement_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_statement(STMT_ID)


async def test_describe_statement_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="describe_statement failed"
    ):
        await describe_statement(STMT_ID)


# ---------------------------------------------------------------------------
# get_statement_result
# ---------------------------------------------------------------------------


async def test_get_result_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _result_resp()
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await get_statement_result(STMT_ID)
    assert isinstance(result, QueryResult)
    assert result.total_num_rows == 1


async def test_get_result_with_next_token(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _result_resp()
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    await get_statement_result(STMT_ID, next_token="tok")
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["NextToken"] == "tok"


async def test_get_result_no_next_token(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _result_resp()
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    await get_statement_result(STMT_ID)
    call_kwargs = mock_client.call.call_args[1]
    assert "NextToken" not in call_kwargs


async def test_get_result_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_statement_result(STMT_ID)


async def test_get_result_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="get_statement_result failed"
    ):
        await get_statement_result(STMT_ID)


# ---------------------------------------------------------------------------
# list_statements
# ---------------------------------------------------------------------------


async def test_list_statements_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Statements": [_desc_resp()],
        "NextToken": "tok2",
    }
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    stmts, token = await list_statements()
    assert len(stmts) == 1
    assert token == "tok2"


async def test_list_statements_all_filters(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Statements": []}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    stmts, token = await list_statements(
        status="FINISHED",
        statement_name="my-stmt",
        max_results=10,
        next_token="tok",
    )
    assert stmts == []
    assert token is None
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Status"] == "FINISHED"
    assert call_kwargs["StatementName"] == "my-stmt"
    assert call_kwargs["MaxResults"] == 10
    assert call_kwargs["NextToken"] == "tok"


async def test_list_statements_no_filters(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Statements": []}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    await list_statements()
    call_kwargs = mock_client.call.call_args[1]
    assert "Status" not in call_kwargs
    assert "StatementName" not in call_kwargs
    assert "MaxResults" not in call_kwargs
    assert "NextToken" not in call_kwargs


async def test_list_statements_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_statements()


async def test_list_statements_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="list_statements failed"):
        await list_statements()


# ---------------------------------------------------------------------------
# cancel_statement
# ---------------------------------------------------------------------------


async def test_cancel_statement_success(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Status": True}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await cancel_statement(STMT_ID)
    assert result is True


async def test_cancel_statement_false(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {"Status": False}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await cancel_statement(STMT_ID)
    assert result is False


async def test_cancel_statement_missing_status(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await cancel_statement(STMT_ID)
    assert result is False


async def test_cancel_statement_runtime_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await cancel_statement(STMT_ID)


async def test_cancel_statement_generic_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="cancel_statement failed"
    ):
        await cancel_statement(STMT_ID)


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


async def test_run_query_immediate(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="FINISHED"),  # describe
        _result_resp(),  # get_result
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await run_query(
        "SELECT 1",
        database=DATABASE,
        cluster_identifier=CLUSTER,
    )
    assert isinstance(result, QueryResult)
    assert result.total_num_rows == 1


async def test_run_query_poll_then_finish(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="STARTED"),  # describe - poll 1
        _desc_resp(Status="FINISHED"),  # describe - poll 2
        _result_resp(TotalNumRows=3),  # get_result
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with patch(
        "aws_util.aio.redshift_data.asyncio.sleep",
        new_callable=AsyncMock,
    ):
        result = await run_query(
            "SELECT 1",
            database=DATABASE,
            timeout=300,
            poll_interval=0.01,
        )
    assert result.total_num_rows == 3


async def test_run_query_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="FAILED", Error="syntax error"),  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(AwsServiceError, match="FAILED"):
        await run_query("BAD SQL", database=DATABASE)


async def test_run_query_aborted(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="ABORTED"),  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(AwsServiceError, match="ABORTED"):
        await run_query("SELECT 1", database=DATABASE)


async def test_run_query_failure_no_error(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="FAILED"),  # describe (no Error key)
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(AwsServiceError, match="no error details"):
        await run_query("SELECT 1", database=DATABASE)


async def test_run_query_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="STARTED"),  # describe
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    with patch(
        "aws_util.aio.redshift_data.asyncio.sleep",
        new_callable=AsyncMock,
    ):
        with pytest.raises((TimeoutError, AwsTimeoutError)):
            await run_query(
                "SELECT 1",
                database=DATABASE,
                timeout=0.0,
                poll_interval=0.001,
            )


async def test_run_query_all_params(monkeypatch: pytest.MonkeyPatch) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"Id": STMT_ID},  # execute
        _desc_resp(Status="FINISHED"),  # describe
        _result_resp(),  # get_result
    ]
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        _mock_factory(mock_client),
    )
    result = await run_query(
        "SELECT 1",
        database=DATABASE,
        cluster_identifier=CLUSTER,
        workgroup_name=WORKGROUP,
        secret_arn=SECRET_ARN,
        db_user=DB_USER,
    )
    assert isinstance(result, QueryResult)
    # Verify execute call received all params
    exec_kwargs = mock_client.call.call_args_list[0][1]
    assert exec_kwargs["Database"] == DATABASE
    assert exec_kwargs["ClusterIdentifier"] == CLUSTER
    assert exec_kwargs["WorkgroupName"] == WORKGROUP
    assert exec_kwargs["SecretArn"] == SECRET_ARN
    assert exec_kwargs["DbUser"] == DB_USER


async def test_describe_table(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_table("test-database", )
    mock_client.call.assert_called_once()


async def test_describe_table_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_table("test-database", )


async def test_get_statement_result_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_statement_result_v2("test-id", )
    mock_client.call.assert_called_once()


async def test_get_statement_result_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_statement_result_v2("test-id", )


async def test_list_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_databases("test-database", )
    mock_client.call.assert_called_once()


async def test_list_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_databases("test-database", )


async def test_list_schemas(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_schemas("test-database", )
    mock_client.call.assert_called_once()


async def test_list_schemas_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_schemas("test-database", )


async def test_list_tables(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tables("test-database", )
    mock_client.call.assert_called_once()


async def test_list_tables_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.redshift_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tables("test-database", )


@pytest.mark.asyncio
async def test_get_statement_result_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import get_statement_result
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await get_statement_result("test-statement_id", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_statements_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import list_statements
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await list_statements(status="test-status", statement_name="test-statement_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_table_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import describe_table
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await describe_table("test-database", cluster_identifier="test-cluster_identifier", connected_database="test-connected_database", db_user="test-db_user", max_results=1, next_token="test-next_token", schema="test-schema", secret_arn="test-secret_arn", table="test-table", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_statement_result_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import get_statement_result_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await get_statement_result_v2("test-id", next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import list_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await list_databases("test-database", cluster_identifier="test-cluster_identifier", db_user="test-db_user", max_results=1, next_token="test-next_token", secret_arn="test-secret_arn", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_schemas_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import list_schemas
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await list_schemas("test-database", cluster_identifier="test-cluster_identifier", connected_database="test-connected_database", db_user="test-db_user", max_results=1, next_token="test-next_token", schema_pattern="test-schema_pattern", secret_arn="test-secret_arn", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tables_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.redshift_data import list_tables
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.redshift_data.async_client", lambda *a, **kw: mock_client)
    await list_tables("test-database", cluster_identifier="test-cluster_identifier", connected_database="test-connected_database", db_user="test-db_user", max_results=1, next_token="test-next_token", schema_pattern="test-schema_pattern", secret_arn="test-secret_arn", table_pattern="test-table_pattern", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.call.assert_called_once()
