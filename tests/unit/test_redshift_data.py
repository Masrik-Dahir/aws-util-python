"""Tests for aws_util.redshift_data module."""
from __future__ import annotations

import time as _time

import pytest
from botocore.exceptions import ClientError
from unittest.mock import MagicMock

import aws_util.redshift_data as rd_mod
from aws_util.redshift_data import (
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
    _parse_description,
    _parse_result,
    describe_table,
    get_statement_result_v2,
    list_databases,
    list_schemas,
    list_tables,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError

REGION = "us-east-1"
STMT_ID = "stmt-abc-123"
CLUSTER = "my-cluster"
DATABASE = "mydb"
WORKGROUP = "my-workgroup"
SECRET_ARN = "arn:aws:secretsmanager:us-east-1:123:secret:cred"
DB_USER = "admin"


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _desc_dict(**kwargs: object) -> dict:
    defaults: dict = {
        "Id": STMT_ID,
        "Status": "FINISHED",
        "QueryString": "SELECT 1",
        "ResultRows": 1,
        "ResultSize": 10,
        "Duration": 500,
        "Error": None,
        "HasResultSet": True,
        "ClusterIdentifier": CLUSTER,
        "Database": DATABASE,
        "SecretArn": SECRET_ARN,
        "DbUser": DB_USER,
        "WorkgroupName": None,
    }
    defaults.update(kwargs)
    return defaults


def _result_dict(**kwargs: object) -> dict:
    defaults: dict = {
        "ColumnMetadata": [{"name": "id", "typeName": "int4"}],
        "Records": [[{"longValue": 1}]],
        "TotalNumRows": 1,
    }
    defaults.update(kwargs)
    return defaults


def _client_error(
    code: str = "ClientException",
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
    def test_statement_result_defaults(self) -> None:
        sr = StatementResult(statement_id=STMT_ID)
        assert sr.statement_id == STMT_ID
        assert sr.cluster_identifier is None
        assert sr.database is None
        assert sr.secret_arn is None
        assert sr.db_user is None
        assert sr.workgroup_name is None

    def test_statement_result_full(self) -> None:
        sr = StatementResult(
            statement_id=STMT_ID,
            cluster_identifier=CLUSTER,
            database=DATABASE,
            secret_arn=SECRET_ARN,
            db_user=DB_USER,
            workgroup_name=WORKGROUP,
        )
        assert sr.cluster_identifier == CLUSTER
        assert sr.workgroup_name == WORKGROUP

    def test_statement_description_defaults(self) -> None:
        sd = StatementDescription(
            statement_id=STMT_ID, status="FINISHED"
        )
        assert sd.result_rows == 0
        assert sd.result_size == 0
        assert sd.duration == 0
        assert sd.error is None
        assert sd.has_result_set is False
        assert sd.query_string is None
        assert sd.extra == {}

    def test_statement_description_full(self) -> None:
        sd = StatementDescription(
            statement_id=STMT_ID,
            status="FINISHED",
            query_string="SELECT 1",
            result_rows=5,
            result_size=100,
            duration=42,
            error="oops",
            has_result_set=True,
            cluster_identifier=CLUSTER,
            database=DATABASE,
            secret_arn=SECRET_ARN,
            db_user=DB_USER,
            workgroup_name=WORKGROUP,
            extra={"foo": "bar"},
        )
        assert sd.result_rows == 5
        assert sd.extra == {"foo": "bar"}

    def test_query_result_defaults(self) -> None:
        qr = QueryResult()
        assert qr.column_metadata == []
        assert qr.records == []
        assert qr.total_num_rows == 0
        assert qr.next_token is None

    def test_query_result_full(self) -> None:
        qr = QueryResult(
            column_metadata=[{"name": "x"}],
            records=[[{"longValue": 1}]],
            total_num_rows=1,
            next_token="tok",
        )
        assert qr.total_num_rows == 1
        assert qr.next_token == "tok"


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_description(self) -> None:
        result = _parse_description(_desc_dict())
        assert result.statement_id == STMT_ID
        assert result.status == "FINISHED"
        assert result.query_string == "SELECT 1"
        assert result.has_result_set is True

    def test_parse_description_extra_fields(self) -> None:
        data = _desc_dict(CreatedAt=123456789)
        result = _parse_description(data)
        assert "CreatedAt" in result.extra

    def test_parse_description_missing_optional(self) -> None:
        data = {"Id": STMT_ID, "Status": "SUBMITTED"}
        result = _parse_description(data)
        assert result.query_string is None
        assert result.result_rows == 0
        assert result.error is None

    def test_parse_result(self) -> None:
        result = _parse_result(_result_dict())
        assert len(result.column_metadata) == 1
        assert result.total_num_rows == 1
        assert result.next_token is None

    def test_parse_result_with_token(self) -> None:
        result = _parse_result(_result_dict(NextToken="abc"))
        assert result.next_token == "abc"

    def test_parse_result_empty(self) -> None:
        result = _parse_result({})
        assert result.column_metadata == []
        assert result.records == []
        assert result.total_num_rows == 0


# ---------------------------------------------------------------------------
# execute_statement
# ---------------------------------------------------------------------------


class TestExecuteStatement:
    def test_success_with_cluster(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.return_value = {"Id": STMT_ID}
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = execute_statement(
            "SELECT 1",
            database=DATABASE,
            cluster_identifier=CLUSTER,
            region_name=REGION,
        )
        assert isinstance(result, StatementResult)
        assert result.statement_id == STMT_ID
        assert result.cluster_identifier == CLUSTER

    def test_success_with_workgroup(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.return_value = {"Id": STMT_ID}
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = execute_statement(
            "SELECT 1",
            database=DATABASE,
            workgroup_name=WORKGROUP,
            region_name=REGION,
        )
        assert result.workgroup_name == WORKGROUP

    def test_success_all_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.return_value = {"Id": STMT_ID}
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = execute_statement(
            "SELECT 1",
            database=DATABASE,
            cluster_identifier=CLUSTER,
            secret_arn=SECRET_ARN,
            db_user=DB_USER,
            statement_name="my-stmt",
            with_event=True,
            region_name=REGION,
        )
        assert result.secret_arn == SECRET_ARN
        assert result.db_user == DB_USER
        call_kwargs = mock_client.execute_statement.call_args[1]
        assert call_kwargs["StatementName"] == "my-stmt"
        assert call_kwargs["WithEvent"] is True

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.execute_statement.side_effect = _client_error()
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="execute_statement failed"):
            execute_statement(
                "SELECT 1", database=DATABASE, region_name=REGION
            )


# ---------------------------------------------------------------------------
# batch_execute_statement
# ---------------------------------------------------------------------------


class TestBatchExecuteStatement:
    def test_success_with_cluster(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.batch_execute_statement.return_value = {
            "Id": STMT_ID
        }
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = batch_execute_statement(
            ["SELECT 1", "SELECT 2"],
            database=DATABASE,
            cluster_identifier=CLUSTER,
            region_name=REGION,
        )
        assert result.statement_id == STMT_ID

    def test_success_all_params(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.batch_execute_statement.return_value = {
            "Id": STMT_ID
        }
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = batch_execute_statement(
            ["SELECT 1"],
            database=DATABASE,
            workgroup_name=WORKGROUP,
            secret_arn=SECRET_ARN,
            db_user=DB_USER,
            statement_name="batch-stmt",
            with_event=True,
            region_name=REGION,
        )
        assert result.workgroup_name == WORKGROUP
        call_kwargs = (
            mock_client.batch_execute_statement.call_args[1]
        )
        assert call_kwargs["StatementName"] == "batch-stmt"
        assert call_kwargs["WithEvent"] is True

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.batch_execute_statement.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="batch_execute_statement failed"
        ):
            batch_execute_statement(
                ["SELECT 1"], database=DATABASE, region_name=REGION
            )


# ---------------------------------------------------------------------------
# describe_statement
# ---------------------------------------------------------------------------


class TestDescribeStatement:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.describe_statement.return_value = _desc_dict()
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_statement(STMT_ID, region_name=REGION)
        assert isinstance(result, StatementDescription)
        assert result.status == "FINISHED"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.describe_statement.side_effect = _client_error()
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="describe_statement failed"
        ):
            describe_statement(STMT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# get_statement_result
# ---------------------------------------------------------------------------


class TestGetStatementResult:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.get_statement_result.return_value = (
            _result_dict()
        )
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = get_statement_result(STMT_ID, region_name=REGION)
        assert isinstance(result, QueryResult)
        assert result.total_num_rows == 1

    def test_with_next_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.get_statement_result.return_value = (
            _result_dict()
        )
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        get_statement_result(
            STMT_ID, next_token="tok", region_name=REGION
        )
        call_kwargs = (
            mock_client.get_statement_result.call_args[1]
        )
        assert call_kwargs["NextToken"] == "tok"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.get_statement_result.side_effect = (
            _client_error()
        )
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="get_statement_result failed"
        ):
            get_statement_result(STMT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# list_statements
# ---------------------------------------------------------------------------


class TestListStatements:
    def test_success_no_filters(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_statements.return_value = {
            "Statements": [_desc_dict()],
            "NextToken": "tok2",
        }
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        stmts, token = list_statements(region_name=REGION)
        assert len(stmts) == 1
        assert token == "tok2"

    def test_all_filters(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_statements.return_value = {
            "Statements": [],
        }
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        stmts, token = list_statements(
            status="FINISHED",
            statement_name="my-stmt",
            max_results=10,
            next_token="tok",
            region_name=REGION,
        )
        assert stmts == []
        assert token is None
        call_kwargs = mock_client.list_statements.call_args[1]
        assert call_kwargs["Status"] == "FINISHED"
        assert call_kwargs["StatementName"] == "my-stmt"
        assert call_kwargs["MaxResults"] == 10
        assert call_kwargs["NextToken"] == "tok"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.list_statements.side_effect = _client_error()
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_statements failed"):
            list_statements(region_name=REGION)


# ---------------------------------------------------------------------------
# cancel_statement
# ---------------------------------------------------------------------------


class TestCancelStatement:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.cancel_statement.return_value = {"Status": True}
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = cancel_statement(STMT_ID, region_name=REGION)
        assert result is True

    def test_success_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.cancel_statement.return_value = {"Status": False}
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = cancel_statement(STMT_ID, region_name=REGION)
        assert result is False

    def test_missing_status_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.cancel_statement.return_value = {}
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        result = cancel_statement(STMT_ID, region_name=REGION)
        assert result is False

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_client = MagicMock()
        mock_client.cancel_statement.side_effect = _client_error()
        monkeypatch.setattr(rd_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="cancel_statement failed"
        ):
            cancel_statement(STMT_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# run_query
# ---------------------------------------------------------------------------


class TestRunQuery:
    def test_success_immediate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            rd_mod,
            "execute_statement",
            lambda *a, **kw: StatementResult(
                statement_id=STMT_ID, database=DATABASE
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "describe_statement",
            lambda *a, **kw: StatementDescription(
                statement_id=STMT_ID, status="FINISHED"
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "get_statement_result",
            lambda *a, **kw: QueryResult(total_num_rows=5),
        )
        result = run_query(
            "SELECT 1",
            database=DATABASE,
            cluster_identifier=CLUSTER,
            region_name=REGION,
        )
        assert result.total_num_rows == 5

    def test_poll_then_finish(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            rd_mod,
            "execute_statement",
            lambda *a, **kw: StatementResult(
                statement_id=STMT_ID, database=DATABASE
            ),
        )
        monkeypatch.setattr(_time, "sleep", lambda s: None)

        call_count = {"n": 0}

        def fake_describe(*a: object, **kw: object) -> StatementDescription:
            call_count["n"] += 1
            if call_count["n"] < 2:
                return StatementDescription(
                    statement_id=STMT_ID, status="STARTED"
                )
            return StatementDescription(
                statement_id=STMT_ID, status="FINISHED"
            )

        monkeypatch.setattr(rd_mod, "describe_statement", fake_describe)
        monkeypatch.setattr(
            rd_mod,
            "get_statement_result",
            lambda *a, **kw: QueryResult(total_num_rows=3),
        )
        result = run_query(
            "SELECT 1",
            database=DATABASE,
            timeout=60,
            poll_interval=0.001,
            region_name=REGION,
        )
        assert result.total_num_rows == 3

    def test_failure_status(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            rd_mod,
            "execute_statement",
            lambda *a, **kw: StatementResult(
                statement_id=STMT_ID, database=DATABASE
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "describe_statement",
            lambda *a, **kw: StatementDescription(
                statement_id=STMT_ID,
                status="FAILED",
                error="syntax error",
            ),
        )
        with pytest.raises(AwsServiceError, match="FAILED"):
            run_query(
                "BAD SQL",
                database=DATABASE,
                region_name=REGION,
            )

    def test_aborted_status(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            rd_mod,
            "execute_statement",
            lambda *a, **kw: StatementResult(
                statement_id=STMT_ID, database=DATABASE
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "describe_statement",
            lambda *a, **kw: StatementDescription(
                statement_id=STMT_ID, status="ABORTED"
            ),
        )
        with pytest.raises(AwsServiceError, match="ABORTED"):
            run_query(
                "SELECT 1",
                database=DATABASE,
                region_name=REGION,
            )

    def test_failure_no_error_detail(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            rd_mod,
            "execute_statement",
            lambda *a, **kw: StatementResult(
                statement_id=STMT_ID, database=DATABASE
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "describe_statement",
            lambda *a, **kw: StatementDescription(
                statement_id=STMT_ID, status="FAILED"
            ),
        )
        with pytest.raises(AwsServiceError, match="no error details"):
            run_query(
                "BAD SQL",
                database=DATABASE,
                region_name=REGION,
            )

    def test_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            rd_mod,
            "execute_statement",
            lambda *a, **kw: StatementResult(
                statement_id=STMT_ID, database=DATABASE
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "describe_statement",
            lambda *a, **kw: StatementDescription(
                statement_id=STMT_ID, status="STARTED"
            ),
        )
        with pytest.raises((TimeoutError, AwsTimeoutError)):
            run_query(
                "SELECT 1",
                database=DATABASE,
                timeout=0.0,
                poll_interval=0.0,
                region_name=REGION,
            )

    def test_all_params_forwarded(self, monkeypatch: pytest.MonkeyPatch) -> None:
        captured: dict[str, Any] = {}

        def fake_execute(*a: object, **kw: object) -> StatementResult:
            captured.update(kw)
            return StatementResult(
                statement_id=STMT_ID, database=DATABASE
            )

        monkeypatch.setattr(rd_mod, "execute_statement", fake_execute)
        monkeypatch.setattr(
            rd_mod,
            "describe_statement",
            lambda *a, **kw: StatementDescription(
                statement_id=STMT_ID, status="FINISHED"
            ),
        )
        monkeypatch.setattr(
            rd_mod,
            "get_statement_result",
            lambda *a, **kw: QueryResult(),
        )
        run_query(
            "SELECT 1",
            database=DATABASE,
            cluster_identifier=CLUSTER,
            workgroup_name=WORKGROUP,
            secret_arn=SECRET_ARN,
            db_user=DB_USER,
            region_name=REGION,
        )
        assert captured["database"] == DATABASE
        assert captured["cluster_identifier"] == CLUSTER
        assert captured["workgroup_name"] == WORKGROUP
        assert captured["secret_arn"] == SECRET_ARN
        assert captured["db_user"] == DB_USER


def test_describe_table(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    describe_table("test-database", region_name=REGION)
    mock_client.describe_table.assert_called_once()


def test_describe_table_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_table",
    )
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe table"):
        describe_table("test-database", region_name=REGION)


def test_get_statement_result_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_statement_result_v2.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    get_statement_result_v2("test-id", region_name=REGION)
    mock_client.get_statement_result_v2.assert_called_once()


def test_get_statement_result_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_statement_result_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_statement_result_v2",
    )
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get statement result v2"):
        get_statement_result_v2("test-id", region_name=REGION)


def test_list_databases(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_databases.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_databases("test-database", region_name=REGION)
    mock_client.list_databases.assert_called_once()


def test_list_databases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_databases",
    )
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list databases"):
        list_databases("test-database", region_name=REGION)


def test_list_schemas(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schemas.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_schemas("test-database", region_name=REGION)
    mock_client.list_schemas.assert_called_once()


def test_list_schemas_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_schemas.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_schemas",
    )
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list schemas"):
        list_schemas("test-database", region_name=REGION)


def test_list_tables(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tables.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_tables("test-database", region_name=REGION)
    mock_client.list_tables.assert_called_once()


def test_list_tables_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tables.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tables",
    )
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tables"):
        list_tables("test-database", region_name=REGION)


def test_get_statement_result_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import get_statement_result
    mock_client = MagicMock()
    mock_client.get_statement_result.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    get_statement_result("test-statement_id", next_token="test-next_token", region_name="us-east-1")
    mock_client.get_statement_result.assert_called_once()

def test_list_statements_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import list_statements
    mock_client = MagicMock()
    mock_client.list_statements.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_statements(status="test-status", statement_name="test-statement_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_statements.assert_called_once()

def test_describe_table_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import describe_table
    mock_client = MagicMock()
    mock_client.describe_table.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    describe_table("test-database", cluster_identifier="test-cluster_identifier", connected_database="test-connected_database", db_user="test-db_user", max_results=1, next_token="test-next_token", schema="test-schema", secret_arn="test-secret_arn", table="test-table", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.describe_table.assert_called_once()

def test_get_statement_result_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import get_statement_result_v2
    mock_client = MagicMock()
    mock_client.get_statement_result_v2.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    get_statement_result_v2("test-id", next_token="test-next_token", region_name="us-east-1")
    mock_client.get_statement_result_v2.assert_called_once()

def test_list_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import list_databases
    mock_client = MagicMock()
    mock_client.list_databases.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_databases("test-database", cluster_identifier="test-cluster_identifier", db_user="test-db_user", max_results=1, next_token="test-next_token", secret_arn="test-secret_arn", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.list_databases.assert_called_once()

def test_list_schemas_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import list_schemas
    mock_client = MagicMock()
    mock_client.list_schemas.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_schemas("test-database", cluster_identifier="test-cluster_identifier", connected_database="test-connected_database", db_user="test-db_user", max_results=1, next_token="test-next_token", schema_pattern="test-schema_pattern", secret_arn="test-secret_arn", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.list_schemas.assert_called_once()

def test_list_tables_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift_data import list_tables
    mock_client = MagicMock()
    mock_client.list_tables.return_value = {}
    monkeypatch.setattr("aws_util.redshift_data.get_client", lambda *a, **kw: mock_client)
    list_tables("test-database", cluster_identifier="test-cluster_identifier", connected_database="test-connected_database", db_user="test-db_user", max_results=1, next_token="test-next_token", schema_pattern="test-schema_pattern", secret_arn="test-secret_arn", table_pattern="test-table_pattern", workgroup_name="test-workgroup_name", region_name="us-east-1")
    mock_client.list_tables.assert_called_once()
