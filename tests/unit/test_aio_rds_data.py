"""Tests for aws_util.aio.rds_data -- 100 % line coverage."""
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from aws_util.aio.rds_data import (
    BatchExecuteResult,
    ColumnMetadata,
    ExecuteResult,
    TransactionResult,
    batch_execute_statement,
    begin_transaction,
    commit_transaction,
    execute_statement,
    rollback_transaction,
    run_query,
    run_transaction,
    execute_sql,
)
from aws_util.exceptions import AwsServiceError


REGION = "us-east-1"
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


RESOURCE_ARN = "arn:aws:rds:us-east-1:123456789:cluster:my-cluster"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:123456789:secret:cred"
DATABASE = "mydb"
SCHEMA = "public"
TXN_ID = "txn-abc-123"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client: AsyncMock) -> object:
    return lambda *a, **kw: mock_client


def _execute_resp(**kwargs: object) -> dict:
    defaults: dict = {
        "numberOfRecordsUpdated": 1,
        "records": [[{"stringValue": "hello"}]],
        "columnMetadata": [
            {
                "name": "col1",
                "typeName": "varchar",
                "label": "col1",
                "nullable": 1,
                "precision": 255,
                "scale": 0,
            }
        ],
        "generatedFields": [{"longValue": 42}],
        "formattedRecords": '{"records":[]}',
    }
    defaults.update(kwargs)
    return defaults


def _batch_resp(**kwargs: object) -> dict:
    defaults: dict = {
        "updateResults": [
            {"generatedFields": [{"longValue": 1}]},
            {"generatedFields": [{"longValue": 2}]},
        ],
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# execute_statement
# ---------------------------------------------------------------------------


async def test_execute_statement_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _execute_resp()
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await execute_statement(
        "SELECT 1",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert isinstance(result, ExecuteResult)
    assert result.number_of_records_updated == 1


async def test_execute_statement_all_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _execute_resp()
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    params = [{"name": "id", "value": {"longValue": 1}}]
    result = await execute_statement(
        "SELECT 1",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
        database=DATABASE,
        schema=SCHEMA,
        parameters=params,
        transaction_id=TXN_ID,
        include_result_metadata=True,
        continue_after_timeout=True,
        format_records_as="JSON",
        region_name=REGION,
    )
    assert isinstance(result, ExecuteResult)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["database"] == DATABASE
    assert call_kwargs["schema"] == SCHEMA
    assert call_kwargs["parameters"] == params
    assert call_kwargs["transactionId"] == TXN_ID
    assert call_kwargs["includeResultMetadata"] is True
    assert call_kwargs["continueAfterTimeout"] is True
    assert call_kwargs["formatRecordsAs"] == "JSON"


async def test_execute_statement_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await execute_statement(
            "SELECT 1",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


async def test_execute_statement_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="execute_statement failed"
    ):
        await execute_statement(
            "SELECT 1",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


# ---------------------------------------------------------------------------
# batch_execute_statement
# ---------------------------------------------------------------------------


async def test_batch_execute_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _batch_resp()
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await batch_execute_statement(
        "INSERT INTO t VALUES (:id)",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert isinstance(result, BatchExecuteResult)
    assert len(result.update_results) == 2


async def test_batch_execute_all_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _batch_resp()
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    psets = [
        [{"name": "id", "value": {"longValue": 1}}],
        [{"name": "id", "value": {"longValue": 2}}],
    ]
    result = await batch_execute_statement(
        "INSERT INTO t VALUES (:id)",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
        database=DATABASE,
        schema=SCHEMA,
        parameter_sets=psets,
        transaction_id=TXN_ID,
        region_name=REGION,
    )
    assert isinstance(result, BatchExecuteResult)
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["database"] == DATABASE
    assert call_kwargs["schema"] == SCHEMA
    assert call_kwargs["parameterSets"] == psets
    assert call_kwargs["transactionId"] == TXN_ID


async def test_batch_execute_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("fail")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="fail"):
        await batch_execute_statement(
            "INSERT INTO t VALUES (:id)",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


async def test_batch_execute_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="batch_execute_statement failed"
    ):
        await batch_execute_statement(
            "INSERT INTO t VALUES (:id)",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


# ---------------------------------------------------------------------------
# begin_transaction
# ---------------------------------------------------------------------------


async def test_begin_transaction_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "transactionId": TXN_ID
    }
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await begin_transaction(
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert isinstance(result, TransactionResult)
    assert result.transaction_id == TXN_ID


async def test_begin_transaction_all_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "transactionId": TXN_ID
    }
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await begin_transaction(
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
        database=DATABASE,
        schema=SCHEMA,
        region_name=REGION,
    )
    assert result.transaction_id == TXN_ID
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["database"] == DATABASE
    assert call_kwargs["schema"] == SCHEMA


async def test_begin_transaction_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await begin_transaction(
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


async def test_begin_transaction_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="begin_transaction failed"
    ):
        await begin_transaction(
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


# ---------------------------------------------------------------------------
# commit_transaction
# ---------------------------------------------------------------------------


async def test_commit_transaction_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "transactionStatus": "Transaction Committed"
    }
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await commit_transaction(
        TXN_ID,
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert result == "Transaction Committed"


async def test_commit_transaction_missing_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await commit_transaction(
        TXN_ID,
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert result == ""


async def test_commit_transaction_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await commit_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


async def test_commit_transaction_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="commit_transaction failed"
    ):
        await commit_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


# ---------------------------------------------------------------------------
# rollback_transaction
# ---------------------------------------------------------------------------


async def test_rollback_transaction_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "transactionStatus": "Transaction Rolledback"
    }
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await rollback_transaction(
        TXN_ID,
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert result == "Transaction Rolledback"


async def test_rollback_transaction_missing_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await rollback_transaction(
        TXN_ID,
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert result == ""


async def test_rollback_transaction_runtime_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="err"):
        await rollback_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


async def test_rollback_transaction_generic_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(
        RuntimeError, match="rollback_transaction failed"
    ):
        await rollback_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


async def test_run_query_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _execute_resp()
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await run_query(
        "SELECT 1",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
        database=DATABASE,
        schema=SCHEMA,
        parameters=[{"name": "x", "value": {"longValue": 1}}],
        format_records_as="JSON",
        region_name=REGION,
    )
    assert isinstance(result, ExecuteResult)
    assert result.number_of_records_updated == 1
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["includeResultMetadata"] is True


async def test_run_query_minimal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.return_value = _execute_resp()
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await run_query(
        "SELECT 1",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
    )
    assert isinstance(result, ExecuteResult)


# ---------------------------------------------------------------------------
# run_transaction
# ---------------------------------------------------------------------------


async def test_run_transaction_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"transactionId": TXN_ID},  # begin
        _execute_resp(),  # execute
        {"transactionStatus": "Transaction Committed"},  # commit
    ]
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    result = await run_transaction(
        "INSERT INTO t VALUES (1)",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
        database=DATABASE,
        schema=SCHEMA,
        parameters=[{"name": "x", "value": {"longValue": 1}}],
        region_name=REGION,
    )
    assert isinstance(result, ExecuteResult)
    assert result.number_of_records_updated == 1


async def test_run_transaction_execute_error_rollback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"transactionId": TXN_ID},  # begin
        AwsServiceError("exec failed"),  # execute error
        {"transactionStatus": "Transaction Rolledback"},  # rollback
    ]
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="exec failed"):
        await run_transaction(
            "BAD SQL",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )
    # Verify rollback was called (3rd call)
    assert mock_client.call.call_count == 3
    rollback_call = mock_client.call.call_args_list[2]
    assert rollback_call[0][0] == "RollbackTransaction"


async def test_run_transaction_commit_error_rollback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"transactionId": TXN_ID},  # begin
        _execute_resp(),  # execute
        AwsServiceError("commit failed"),  # commit error
        {"transactionStatus": "Transaction Rolledback"},  # rollback
    ]
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="commit failed"):
        await run_transaction(
            "INSERT INTO t VALUES (1)",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )
    assert mock_client.call.call_count == 4


async def test_run_transaction_rollback_failure_suppressed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"transactionId": TXN_ID},  # begin
        AwsServiceError("exec failed"),  # execute error
        AwsServiceError("rollback also failed"),  # rollback error
    ]
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    with pytest.raises(RuntimeError, match="exec failed"):
        await run_transaction(
            "BAD SQL",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
        )


async def test_run_transaction_all_params_forwarded(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"transactionId": TXN_ID},  # begin
        _execute_resp(),  # execute
        {"transactionStatus": "Transaction Committed"},  # commit
    ]
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        _mock_factory(mock_client),
    )
    await run_transaction(
        "SELECT 1",
        resource_arn=RESOURCE_ARN,
        secret_arn=SECRET_ARN,
        database=DATABASE,
        schema=SCHEMA,
        region_name=REGION,
    )
    # Verify begin_transaction received database and schema
    begin_kwargs = mock_client.call.call_args_list[0][1]
    assert begin_kwargs["database"] == DATABASE
    assert begin_kwargs["schema"] == SCHEMA
    # Verify execute got the transaction_id
    exec_kwargs = mock_client.call.call_args_list[1][1]
    assert exec_kwargs["transactionId"] == TXN_ID


async def test_execute_sql(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        lambda *a, **kw: mock_client,
    )
    await execute_sql("test-db_cluster_or_instance_arn", "test-aws_secret_store_arn", "test-sql_statements", )
    mock_client.call.assert_called_once()


async def test_execute_sql_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds_data.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await execute_sql("test-db_cluster_or_instance_arn", "test-aws_secret_store_arn", "test-sql_statements", )


@pytest.mark.asyncio
async def test_execute_sql_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds_data import execute_sql
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds_data.async_client", lambda *a, **kw: mock_client)
    await execute_sql("test-db_cluster_or_instance_arn", "test-aws_secret_store_arn", "test-sql_statements", database="test-database", schema="test-schema", region_name="us-east-1")
    mock_client.call.assert_called_once()
