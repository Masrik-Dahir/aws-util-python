"""Tests for aws_util.rds_data module."""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.rds_data as mod
from aws_util.exceptions import AwsServiceError
from aws_util.rds_data import (
    BatchExecuteResult,
    ColumnMetadata,
    ExecuteResult,
    TransactionResult,
    _build_execute_kwargs,
    _parse_column_metadata,
    _parse_execute_result,
    batch_execute_statement,
    begin_transaction,
    commit_transaction,
    execute_statement,
    rollback_transaction,
    run_query,
    run_transaction,
    execute_sql,
)

REGION = "us-east-1"
RESOURCE_ARN = "arn:aws:rds:us-east-1:123456789:cluster:my-cluster"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:123456789:secret:cred"
DATABASE = "mydb"
SCHEMA = "public"
TXN_ID = "txn-abc-123"


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


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


def _client_error(
    code: str = "BadRequestException",
    msg: str = "error",
    op: str = "Op",
) -> ClientError:
    return ClientError(
        {"Error": {"Code": code, "Message": msg}}, op
    )


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class TestModels:
    def test_column_metadata_defaults(self) -> None:
        cm = ColumnMetadata()
        assert cm.name == ""
        assert cm.type_name == ""
        assert cm.label == ""
        assert cm.nullable == 0
        assert cm.precision == 0
        assert cm.scale == 0

    def test_column_metadata_full(self) -> None:
        cm = ColumnMetadata(
            name="id",
            type_name="int4",
            label="ID",
            nullable=1,
            precision=10,
            scale=2,
        )
        assert cm.name == "id"
        assert cm.type_name == "int4"
        assert cm.nullable == 1

    def test_execute_result_defaults(self) -> None:
        er = ExecuteResult()
        assert er.number_of_records_updated == 0
        assert er.records == []
        assert er.column_metadata == []
        assert er.generated_fields == []
        assert er.formatted_records is None

    def test_execute_result_full(self) -> None:
        er = ExecuteResult(
            number_of_records_updated=5,
            records=[[{"stringValue": "a"}]],
            column_metadata=[ColumnMetadata(name="x")],
            generated_fields=[{"longValue": 1}],
            formatted_records="json",
        )
        assert er.number_of_records_updated == 5
        assert len(er.records) == 1
        assert er.formatted_records == "json"

    def test_batch_execute_result_defaults(self) -> None:
        br = BatchExecuteResult()
        assert br.update_results == []

    def test_batch_execute_result_full(self) -> None:
        br = BatchExecuteResult(
            update_results=[{"generatedFields": []}]
        )
        assert len(br.update_results) == 1

    def test_transaction_result(self) -> None:
        tr = TransactionResult(transaction_id=TXN_ID)
        assert tr.transaction_id == TXN_ID


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_column_metadata(self) -> None:
        raw = [
            {
                "name": "id",
                "typeName": "int4",
                "label": "ID",
                "nullable": 1,
                "precision": 10,
                "scale": 2,
            }
        ]
        result = _parse_column_metadata(raw)
        assert len(result) == 1
        assert result[0].name == "id"
        assert result[0].type_name == "int4"

    def test_parse_column_metadata_empty(self) -> None:
        result = _parse_column_metadata([])
        assert result == []

    def test_parse_column_metadata_missing_keys(self) -> None:
        result = _parse_column_metadata([{}])
        assert result[0].name == ""
        assert result[0].type_name == ""

    def test_parse_execute_result(self) -> None:
        result = _parse_execute_result(_execute_resp())
        assert result.number_of_records_updated == 1
        assert len(result.records) == 1
        assert len(result.column_metadata) == 1
        assert result.column_metadata[0].name == "col1"
        assert len(result.generated_fields) == 1
        assert result.formatted_records is not None

    def test_parse_execute_result_empty(self) -> None:
        result = _parse_execute_result({})
        assert result.number_of_records_updated == 0
        assert result.records == []
        assert result.column_metadata == []
        assert result.generated_fields == []
        assert result.formatted_records is None

    def test_build_execute_kwargs_minimal(self) -> None:
        kwargs = _build_execute_kwargs(
            "SELECT 1",
            RESOURCE_ARN,
            SECRET_ARN,
            None,
            None,
            None,
            None,
            False,
            False,
            None,
        )
        assert kwargs["sql"] == "SELECT 1"
        assert kwargs["resourceArn"] == RESOURCE_ARN
        assert kwargs["secretArn"] == SECRET_ARN
        assert "database" not in kwargs
        assert "schema" not in kwargs
        assert "parameters" not in kwargs
        assert "transactionId" not in kwargs
        assert "includeResultMetadata" not in kwargs
        assert "continueAfterTimeout" not in kwargs
        assert "formatRecordsAs" not in kwargs

    def test_build_execute_kwargs_full(self) -> None:
        params = [{"name": "id", "value": {"longValue": 1}}]
        kwargs = _build_execute_kwargs(
            "SELECT 1",
            RESOURCE_ARN,
            SECRET_ARN,
            DATABASE,
            SCHEMA,
            params,
            TXN_ID,
            True,
            True,
            "JSON",
        )
        assert kwargs["database"] == DATABASE
        assert kwargs["schema"] == SCHEMA
        assert kwargs["parameters"] == params
        assert kwargs["transactionId"] == TXN_ID
        assert kwargs["includeResultMetadata"] is True
        assert kwargs["continueAfterTimeout"] is True
        assert kwargs["formatRecordsAs"] == "JSON"


# ---------------------------------------------------------------------------
# execute_statement
# ---------------------------------------------------------------------------


class TestExecuteStatement:
    def test_success_minimal(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.return_value = (
            _execute_resp()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = execute_statement(
            "SELECT 1",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert isinstance(result, ExecuteResult)
        assert result.number_of_records_updated == 1

    def test_success_all_params(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.return_value = (
            _execute_resp()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        params = [{"name": "id", "value": {"longValue": 1}}]
        result = execute_statement(
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
        call_kwargs = mock_client.execute_statement.call_args[1]
        assert call_kwargs["database"] == DATABASE
        assert call_kwargs["schema"] == SCHEMA
        assert call_kwargs["parameters"] == params
        assert call_kwargs["transactionId"] == TXN_ID
        assert call_kwargs["includeResultMetadata"] is True
        assert call_kwargs["continueAfterTimeout"] is True
        assert call_kwargs["formatRecordsAs"] == "JSON"

    def test_client_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="execute_statement failed"
        ):
            execute_statement(
                "SELECT 1",
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# batch_execute_statement
# ---------------------------------------------------------------------------


class TestBatchExecuteStatement:
    def test_success_minimal(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.batch_execute_statement.return_value = (
            _batch_resp()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = batch_execute_statement(
            "INSERT INTO t VALUES (:id)",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert isinstance(result, BatchExecuteResult)
        assert len(result.update_results) == 2

    def test_success_all_params(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.batch_execute_statement.return_value = (
            _batch_resp()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        psets = [
            [{"name": "id", "value": {"longValue": 1}}],
            [{"name": "id", "value": {"longValue": 2}}],
        ]
        result = batch_execute_statement(
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
        call_kwargs = (
            mock_client.batch_execute_statement.call_args[1]
        )
        assert call_kwargs["database"] == DATABASE
        assert call_kwargs["schema"] == SCHEMA
        assert call_kwargs["parameterSets"] == psets
        assert call_kwargs["transactionId"] == TXN_ID

    def test_client_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.batch_execute_statement.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="batch_execute_statement failed"
        ):
            batch_execute_statement(
                "INSERT INTO t VALUES (:id)",
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# begin_transaction
# ---------------------------------------------------------------------------


class TestBeginTransaction:
    def test_success_minimal(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.begin_transaction.return_value = {
            "transactionId": TXN_ID
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = begin_transaction(
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert isinstance(result, TransactionResult)
        assert result.transaction_id == TXN_ID

    def test_success_all_params(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.begin_transaction.return_value = {
            "transactionId": TXN_ID
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = begin_transaction(
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            database=DATABASE,
            schema=SCHEMA,
            region_name=REGION,
        )
        assert result.transaction_id == TXN_ID
        call_kwargs = (
            mock_client.begin_transaction.call_args[1]
        )
        assert call_kwargs["database"] == DATABASE
        assert call_kwargs["schema"] == SCHEMA

    def test_client_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.begin_transaction.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="begin_transaction failed"
        ):
            begin_transaction(
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# commit_transaction
# ---------------------------------------------------------------------------


class TestCommitTransaction:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.commit_transaction.return_value = {
            "transactionStatus": "Transaction Committed"
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = commit_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert result == "Transaction Committed"

    def test_missing_status(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.commit_transaction.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = commit_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert result == ""

    def test_client_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.commit_transaction.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="commit_transaction failed"
        ):
            commit_transaction(
                TXN_ID,
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# rollback_transaction
# ---------------------------------------------------------------------------


class TestRollbackTransaction:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.rollback_transaction.return_value = {
            "transactionStatus": "Transaction Rolledback"
        }
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = rollback_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert result == "Transaction Rolledback"

    def test_missing_status(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.rollback_transaction.return_value = {}
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        result = rollback_transaction(
            TXN_ID,
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert result == ""

    def test_client_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        mock_client = MagicMock()
        mock_client.rollback_transaction.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(
            mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="rollback_transaction failed"
        ):
            rollback_transaction(
                TXN_ID,
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


class TestRunQuery:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        captured: dict[str, Any] = {}

        def fake_execute(
            sql: str, **kw: Any
        ) -> ExecuteResult:
            captured.update(kw)
            return ExecuteResult(
                number_of_records_updated=0,
                records=[[{"stringValue": "hi"}]],
            )

        monkeypatch.setattr(mod, "execute_statement", fake_execute)
        result = run_query(
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
        assert len(result.records) == 1
        assert captured["include_result_metadata"] is True
        assert captured["database"] == DATABASE
        assert captured["schema"] == SCHEMA
        assert captured["format_records_as"] == "JSON"

    def test_forwards_params(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        captured: dict[str, Any] = {}

        def fake_execute(
            sql: str, **kw: Any
        ) -> ExecuteResult:
            captured.update(kw)
            return ExecuteResult()

        monkeypatch.setattr(mod, "execute_statement", fake_execute)
        run_query(
            "SELECT 1",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            region_name=REGION,
        )
        assert captured["include_result_metadata"] is True
        assert captured["resource_arn"] == RESOURCE_ARN
        assert captured["secret_arn"] == SECRET_ARN


# ---------------------------------------------------------------------------
# run_transaction
# ---------------------------------------------------------------------------


class TestRunTransaction:
    def test_success(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            mod,
            "begin_transaction",
            lambda **kw: TransactionResult(transaction_id=TXN_ID),
        )
        exec_captured: dict[str, Any] = {}

        def fake_execute(sql: str, **kw: Any) -> ExecuteResult:
            exec_captured.update(kw)
            return ExecuteResult(number_of_records_updated=1)

        monkeypatch.setattr(
            mod, "execute_statement", fake_execute
        )
        commit_captured: dict[str, Any] = {}

        def fake_commit(txn_id: str, **kw: Any) -> str:
            commit_captured["txn_id"] = txn_id
            return "Transaction Committed"

        monkeypatch.setattr(
            mod, "commit_transaction", fake_commit
        )
        result = run_transaction(
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
        assert exec_captured["transaction_id"] == TXN_ID
        assert commit_captured["txn_id"] == TXN_ID

    def test_execute_error_triggers_rollback(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            mod,
            "begin_transaction",
            lambda **kw: TransactionResult(transaction_id=TXN_ID),
        )
        monkeypatch.setattr(
            mod,
            "execute_statement",
            MagicMock(
                side_effect=AwsServiceError("exec failed")
            ),
        )
        rollback_captured: dict[str, Any] = {}

        def fake_rollback(txn_id: str, **kw: Any) -> str:
            rollback_captured["txn_id"] = txn_id
            return "Transaction Rolledback"

        monkeypatch.setattr(
            mod, "rollback_transaction", fake_rollback
        )
        with pytest.raises(RuntimeError, match="exec failed"):
            run_transaction(
                "BAD SQL",
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )
        assert rollback_captured["txn_id"] == TXN_ID

    def test_commit_error_triggers_rollback(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            mod,
            "begin_transaction",
            lambda **kw: TransactionResult(transaction_id=TXN_ID),
        )
        monkeypatch.setattr(
            mod,
            "execute_statement",
            lambda sql, **kw: ExecuteResult(
                number_of_records_updated=1
            ),
        )
        monkeypatch.setattr(
            mod,
            "commit_transaction",
            MagicMock(
                side_effect=AwsServiceError("commit failed")
            ),
        )
        rollback_captured: dict[str, Any] = {}

        def fake_rollback(txn_id: str, **kw: Any) -> str:
            rollback_captured["txn_id"] = txn_id
            return "Transaction Rolledback"

        monkeypatch.setattr(
            mod, "rollback_transaction", fake_rollback
        )
        with pytest.raises(
            RuntimeError, match="commit failed"
        ):
            run_transaction(
                "INSERT INTO t VALUES (1)",
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )
        assert rollback_captured["txn_id"] == TXN_ID

    def test_rollback_failure_suppressed(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(
            mod,
            "begin_transaction",
            lambda **kw: TransactionResult(transaction_id=TXN_ID),
        )
        monkeypatch.setattr(
            mod,
            "execute_statement",
            MagicMock(
                side_effect=AwsServiceError("exec failed")
            ),
        )
        monkeypatch.setattr(
            mod,
            "rollback_transaction",
            MagicMock(
                side_effect=AwsServiceError("rollback failed")
            ),
        )
        with pytest.raises(RuntimeError, match="exec failed"):
            run_transaction(
                "BAD SQL",
                resource_arn=RESOURCE_ARN,
                secret_arn=SECRET_ARN,
                region_name=REGION,
            )

    def test_forwards_all_params(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        begin_captured: dict[str, Any] = {}

        def fake_begin(**kw: Any) -> TransactionResult:
            begin_captured.update(kw)
            return TransactionResult(transaction_id=TXN_ID)

        monkeypatch.setattr(
            mod, "begin_transaction", fake_begin
        )
        monkeypatch.setattr(
            mod,
            "execute_statement",
            lambda sql, **kw: ExecuteResult(),
        )
        monkeypatch.setattr(
            mod,
            "commit_transaction",
            lambda txn_id, **kw: "ok",
        )
        run_transaction(
            "SELECT 1",
            resource_arn=RESOURCE_ARN,
            secret_arn=SECRET_ARN,
            database=DATABASE,
            schema=SCHEMA,
            region_name=REGION,
        )
        assert begin_captured["database"] == DATABASE
        assert begin_captured["schema"] == SCHEMA
        assert begin_captured["resource_arn"] == RESOURCE_ARN


def test_execute_sql(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_sql.return_value = {}
    monkeypatch.setattr("aws_util.rds_data.get_client", lambda *a, **kw: mock_client)
    execute_sql("test-db_cluster_or_instance_arn", "test-aws_secret_store_arn", "test-sql_statements", region_name=REGION)
    mock_client.execute_sql.assert_called_once()


def test_execute_sql_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_sql.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_sql",
    )
    monkeypatch.setattr("aws_util.rds_data.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute sql"):
        execute_sql("test-db_cluster_or_instance_arn", "test-aws_secret_store_arn", "test-sql_statements", region_name=REGION)


def test_execute_sql_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds_data import execute_sql
    mock_client = MagicMock()
    mock_client.execute_sql.return_value = {}
    monkeypatch.setattr("aws_util.rds_data.get_client", lambda *a, **kw: mock_client)
    execute_sql("test-db_cluster_or_instance_arn", "test-aws_secret_store_arn", "test-sql_statements", database="test-database", schema="test-schema", region_name="us-east-1")
    mock_client.execute_sql.assert_called_once()
