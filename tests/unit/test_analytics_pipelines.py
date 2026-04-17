"""Tests for aws_util.analytics_pipelines module."""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.analytics_pipelines as mod
from aws_util.analytics_pipelines import (
    AccessLogAnalysis,
    AthenaToDBResult,
    CrawlerSyncResult,
    DataBrewProfileResult,
    DatasetRefreshResult,
    EMRJobResult,
    GlueToRedshiftResult,
    IndexLifecycleResult,
    NeptuneQueryResult,
    QuickSightEmbedResult,
    RedshiftUnloadResult,
    ServerlessQueryResult,
    TimestreamExportResult,
    athena_result_to_dynamodb,
    elbv2_access_log_analyzer,
    emr_serverless_job_runner,
    glue_crawler_and_catalog_sync,
    glue_databrew_profile_pipeline,
    glue_job_output_to_redshift,
    neptune_graph_query_to_s3,
    opensearch_index_lifecycle_manager,
    quicksight_dashboard_embedder,
    quicksight_dataset_refresher,
    redshift_serverless_query_runner,
    redshift_unload_to_s3,
    timestream_query_to_s3,
)

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _client_error(code: str = "AccessDenied", msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ---------------------------------------------------------------------------
# 1. redshift_unload_to_s3
# ---------------------------------------------------------------------------


class TestRedshiftUnloadToS3:
    def _factory(self, rd: MagicMock, athena: MagicMock):
        def get_client(service: str, region_name=None):
            return {"redshift-data": rd, "athena": athena}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-1"}
        rd.describe_statement.return_value = {
            "Status": "FINISHED",
            "ResultRows": 42,
        }
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        result = redshift_unload_to_s3(
            cluster_identifier="cluster",
            database="db",
            db_user="admin",
            query="SELECT 1",
            s3_path="s3://bkt/pfx/",
            iam_role_arn="arn:role",
            athena_database="adb",
            athena_table="tbl",
            partition_key="dt",
            partition_value="2025-01-01",
            region_name=REGION,
        )
        assert isinstance(result, RedshiftUnloadResult)
        assert result.statement_id == "stmt-1"
        assert result.rows_unloaded == 42
        assert result.partition_added is True

    def test_execute_error(self, monkeypatch) -> None:
        rd = _mock()
        rd.execute_statement.side_effect = _client_error("ValidationException")
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        with pytest.raises(RuntimeError, match="Failed to submit Redshift UNLOAD"):
            redshift_unload_to_s3("c", "db", "u", "q", "s3://b/", "arn:r", "adb", "t", "k", "v")

    def test_describe_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-2"}
        rd.describe_statement.side_effect = _client_error("InternalError")
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        with pytest.raises(RuntimeError, match="Failed to describe statement"):
            redshift_unload_to_s3("c", "db", "u", "q", "s3://b/", "arn:r", "adb", "t", "k", "v")

    def test_statement_failed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-3"}
        rd.describe_statement.return_value = {
            "Status": "FAILED",
            "Error": "syntax error",
        }
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        with pytest.raises(RuntimeError, match="Redshift UNLOAD failed"):
            redshift_unload_to_s3("c", "db", "u", "q", "s3://b/", "arn:r", "adb", "t", "k", "v")

    def test_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-4"}
        rd.describe_statement.return_value = {"Status": "STARTED"}
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        with pytest.raises(RuntimeError, match="did not finish within timeout"):
            redshift_unload_to_s3("c", "db", "u", "q", "s3://b/", "arn:r", "adb", "t", "k", "v")

    def test_athena_partition_failure_logged(self, monkeypatch) -> None:
        """Athena partition failure does not raise, just sets partition_added=False."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-5"}
        rd.describe_statement.return_value = {"Status": "FINISHED", "ResultRows": 10}
        athena = _mock()
        athena.start_query_execution.side_effect = _client_error("InvalidRequestException")
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        result = redshift_unload_to_s3("c", "db", "u", "q", "s3://b/", "arn:r", "adb", "t", "k", "v")
        assert result.partition_added is False

    def test_result_rows_none(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-6"}
        rd.describe_statement.return_value = {"Status": "FINISHED", "ResultRows": None}
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, athena))

        result = redshift_unload_to_s3("c", "db", "u", "q", "s3://b/", "arn:r", "adb", "t", "k", "v")
        assert result.rows_unloaded == 0


# ---------------------------------------------------------------------------
# 2. redshift_serverless_query_runner
# ---------------------------------------------------------------------------


class TestRedshiftServerlessQueryRunner:
    def _factory(self, rd: MagicMock, s3: MagicMock):
        def get_client(service: str, region_name=None):
            return {"redshift-data": rd, "s3": s3}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "stmt-1"}
        rd.describe_statement.return_value = {"Status": "FINISHED"}
        rd.get_statement_result.return_value = {
            "ColumnMetadata": [{"label": "id"}, {"label": "name"}],
            "Records": [
                [{"longValue": 1}, {"stringValue": "Alice"}],
                [{"longValue": 2}, {"stringValue": "Bob"}],
            ],
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        result = redshift_serverless_query_runner(
            workgroup_name="wg",
            database="db",
            sql="SELECT * FROM t",
            bucket="bkt",
            output_key="out.json",
            region_name=REGION,
        )
        assert isinstance(result, ServerlessQueryResult)
        assert result.statement_id == "stmt-1"
        assert result.row_count == 2
        assert result.s3_key == "out.json"
        s3.put_object.assert_called_once()

    def test_execute_error(self, monkeypatch) -> None:
        rd = _mock()
        rd.execute_statement.side_effect = _client_error("ValidationException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        with pytest.raises(RuntimeError, match="Failed to submit Redshift Serverless"):
            redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")

    def test_query_failed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "s1"}
        rd.describe_statement.return_value = {"Status": "FAILED", "Error": "bad sql"}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        with pytest.raises(RuntimeError, match="Redshift Serverless query failed"):
            redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")

    def test_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "s1"}
        rd.describe_statement.return_value = {"Status": "STARTED"}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        with pytest.raises(RuntimeError, match="timed out"):
            redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")

    def test_get_results_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "s1"}
        rd.describe_statement.return_value = {"Status": "FINISHED"}
        rd.get_statement_result.side_effect = _client_error("InternalError")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        with pytest.raises(RuntimeError, match="Failed to retrieve query results"):
            redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")

    def test_s3_put_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "s1"}
        rd.describe_statement.return_value = {"Status": "FINISHED"}
        rd.get_statement_result.return_value = {
            "ColumnMetadata": [{"label": "x"}],
            "Records": [],
        }
        s3 = _mock()
        s3.put_object.side_effect = _client_error("NoSuchBucket")
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        with pytest.raises(RuntimeError, match="Failed to write results"):
            redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")

    def test_pagination(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "s1"}
        rd.describe_statement.return_value = {"Status": "FINISHED"}
        rd.get_statement_result.side_effect = [
            {
                "ColumnMetadata": [{"label": "col"}],
                "Records": [[{"stringValue": "a"}]],
                "NextToken": "tok-2",
            },
            {
                "ColumnMetadata": [{"label": "col"}],
                "Records": [[{"stringValue": "b"}]],
            },
        ]
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        result = redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")
        assert result.row_count == 2

    def test_describe_poll_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "s1"}
        rd.describe_statement.side_effect = _client_error("InternalError")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(rd, s3))

        with pytest.raises(RuntimeError, match="Failed to describe statement"):
            redshift_serverless_query_runner("wg", "db", "sql", "bkt", "k")


# ---------------------------------------------------------------------------
# 3. quicksight_dashboard_embedder
# ---------------------------------------------------------------------------


class TestQuickSightDashboardEmbedder:
    def _factory(self, qs: MagicMock):
        def get_client(service: str, region_name=None):
            return {"quicksight": qs}.get(service, MagicMock())

        return get_client

    def test_registered_user(self, monkeypatch) -> None:
        qs = _mock()
        qs.generate_embed_url_for_registered_user.return_value = {
            "EmbedUrl": "https://embed.example.com/dash",
            "Status": 200,
            "RequestId": "req-1",
        }
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        result = quicksight_dashboard_embedder(
            aws_account_id="123",
            dashboard_id="dash-1",
            user_arn="arn:qs:user",
            region_name=REGION,
        )
        assert isinstance(result, QuickSightEmbedResult)
        assert result.embed_url == "https://embed.example.com/dash"
        assert result.status == 200
        qs.generate_embed_url_for_registered_user.assert_called_once()
        qs.generate_embed_url_for_anonymous_user.assert_not_called()

    def test_anonymous_user(self, monkeypatch) -> None:
        qs = _mock()
        qs.generate_embed_url_for_anonymous_user.return_value = {
            "EmbedUrl": "https://anon.example.com/dash",
            "Status": 200,
            "RequestId": "req-2",
        }
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        result = quicksight_dashboard_embedder(
            aws_account_id="123",
            dashboard_id="dash-2",
        )
        assert result.embed_url == "https://anon.example.com/dash"
        qs.generate_embed_url_for_anonymous_user.assert_called_once()
        qs.generate_embed_url_for_registered_user.assert_not_called()

    def test_client_error(self, monkeypatch) -> None:
        qs = _mock()
        qs.generate_embed_url_for_anonymous_user.side_effect = _client_error(
            "ResourceNotFoundException"
        )
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        with pytest.raises(RuntimeError, match="Failed to generate QuickSight embed"):
            quicksight_dashboard_embedder("123", "dash-bad")


# ---------------------------------------------------------------------------
# 4. quicksight_dataset_refresher
# ---------------------------------------------------------------------------


class TestQuickSightDatasetRefresher:
    def _factory(self, qs: MagicMock, sns: MagicMock | None = None):
        def get_client(service: str, region_name=None):
            clients: dict[str, Any] = {"quicksight": qs}
            if sns is not None:
                clients["sns"] = sns
            return clients.get(service, MagicMock())

        return get_client

    def test_success_completed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 105.0]),
        ))
        qs = _mock()
        qs.describe_ingestion.return_value = {
            "Ingestion": {
                "IngestionStatus": "COMPLETED",
                "RowInfo": {"RowsIngested": 1000},
            }
        }
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        result = quicksight_dataset_refresher(
            aws_account_id="123",
            dataset_id="ds-1",
            ingestion_id="ing-1",
            region_name=REGION,
        )
        assert isinstance(result, DatasetRefreshResult)
        assert result.status == "COMPLETED"
        assert result.rows_ingested == 1000

    def test_create_ingestion_error(self, monkeypatch) -> None:
        qs = _mock()
        qs.create_ingestion.side_effect = _client_error("ResourceNotFoundException")
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        with pytest.raises(RuntimeError, match="Failed to create ingestion"):
            quicksight_dataset_refresher("123", "ds", "ing")

    def test_describe_ingestion_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 105.0]),
        ))
        qs = _mock()
        qs.describe_ingestion.side_effect = _client_error("InternalServiceError")
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        with pytest.raises(RuntimeError, match="Failed to describe ingestion"):
            quicksight_dataset_refresher("123", "ds", "ing")

    def test_with_sns_notification(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 105.0]),
        ))
        qs = _mock()
        qs.describe_ingestion.return_value = {
            "Ingestion": {"IngestionStatus": "COMPLETED", "RowInfo": {"RowsIngested": 50}}
        }
        sns = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(qs, sns))

        result = quicksight_dataset_refresher(
            "123", "ds", "ing", sns_topic_arn="arn:sns:topic"
        )
        assert result.status == "COMPLETED"
        sns.publish.assert_called_once()

    def test_sns_error_logged(self, monkeypatch) -> None:
        """SNS publish failure should be logged, not raised."""
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 105.0]),
        ))
        qs = _mock()
        qs.describe_ingestion.return_value = {
            "Ingestion": {"IngestionStatus": "COMPLETED"}
        }
        sns = _mock()
        sns.publish.side_effect = _client_error("AuthorizationError")
        monkeypatch.setattr(mod, "get_client", self._factory(qs, sns))

        # Should not raise
        result = quicksight_dataset_refresher("123", "ds", "ing", sns_topic_arn="arn:t")
        assert result.status == "COMPLETED"

    def test_ingestion_failed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 105.0]),
        ))
        qs = _mock()
        qs.describe_ingestion.return_value = {
            "Ingestion": {"IngestionStatus": "FAILED"}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(qs))

        result = quicksight_dataset_refresher("123", "ds", "ing")
        assert result.status == "FAILED"
        assert result.rows_ingested is None


# ---------------------------------------------------------------------------
# 5. athena_result_to_dynamodb
# ---------------------------------------------------------------------------


class TestAthenaResultToDynamodb:
    def _factory(self, athena: MagicMock, ddb: MagicMock):
        def get_client(service: str, region_name=None):
            return {"athena": athena, "dynamodb": ddb}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-1"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.return_value = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "id"}, {"VarCharValue": "name"}]},
                    {"Data": [{"VarCharValue": "1"}, {"VarCharValue": "Alice"}]},
                    {"Data": [{"VarCharValue": "2"}, {"VarCharValue": "Bob"}]},
                ]
            }
        }
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        result = athena_result_to_dynamodb(
            query="SELECT * FROM t",
            database="db",
            output_location="s3://bkt/results/",
            table_name="tbl",
            key_column="id",
            region_name=REGION,
        )
        assert isinstance(result, AthenaToDBResult)
        assert result.query_execution_id == "qe-1"
        assert result.rows_written == 2
        assert result.status == "SUCCEEDED"
        assert ddb.put_item.call_count == 2

    def test_start_query_error(self, monkeypatch) -> None:
        athena = _mock()
        athena.start_query_execution.side_effect = _client_error("InvalidRequestException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        with pytest.raises(RuntimeError, match="Failed to start Athena query"):
            athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "pk")

    def test_get_execution_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-2"}
        athena.get_query_execution.side_effect = _client_error()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        with pytest.raises(RuntimeError, match="Failed to get Athena execution"):
            athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "pk")

    def test_query_failed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-3"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {
                "Status": {"State": "FAILED", "StateChangeReason": "syntax error"}
            }
        }
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        with pytest.raises(RuntimeError, match="Athena query failed"):
            athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "pk")

    def test_query_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-4"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "RUNNING"}}
        }
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        with pytest.raises(RuntimeError, match="timed out"):
            athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "pk")

    def test_get_results_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-5"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.side_effect = _client_error()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        with pytest.raises(RuntimeError, match="Failed to retrieve Athena results"):
            athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "pk")

    def test_ddb_put_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-6"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.return_value = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "id"}]},
                    {"Data": [{"VarCharValue": "1"}]},
                ]
            }
        }
        ddb = _mock()
        ddb.put_item.side_effect = _client_error("InternalServiceError")
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        with pytest.raises(RuntimeError, match="Failed to upsert row"):
            athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "id")

    def test_missing_key_column(self, monkeypatch) -> None:
        """When key_column is not in result, use row index as pk."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-7"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.return_value = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "name"}]},
                    {"Data": [{"VarCharValue": "Alice"}]},
                ]
            }
        }
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        result = athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "missing_col")
        assert result.rows_written == 1
        # The put_item call should have "pk" = {"S": "0"} for first row
        call_kwargs = ddb.put_item.call_args
        item = call_kwargs.kwargs.get("Item") or call_kwargs[1].get("Item")
        assert item["pk"] == {"S": "0"}

    def test_pagination(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-8"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.side_effect = [
            {
                "ResultSet": {
                    "Rows": [
                        {"Data": [{"VarCharValue": "id"}]},
                        {"Data": [{"VarCharValue": "1"}]},
                    ]
                },
                "NextToken": "tok-2",
            },
            {
                "ResultSet": {
                    "Rows": [
                        {"Data": [{"VarCharValue": "2"}]},
                    ]
                },
            },
        ]
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(athena, ddb))

        result = athena_result_to_dynamodb("q", "db", "s3://b/", "tbl", "id")
        assert result.rows_written == 2


# ---------------------------------------------------------------------------
# 6. glue_crawler_and_catalog_sync
# ---------------------------------------------------------------------------


class TestGlueCrawlerAndCatalogSync:
    def _factory(self, glue: MagicMock, ddb: MagicMock):
        def get_client(service: str, region_name=None):
            return {"glue": glue, "dynamodb": ddb}.get(service, MagicMock())

        return get_client

    def test_success_with_schema_change(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None, time=lambda: 1000))
        glue = _mock()
        glue.get_crawler.return_value = {
            "Crawler": {
                "State": "READY",
                "Targets": {
                    "CatalogTargets": [{"DatabaseName": "mydb"}],
                },
            }
        }
        glue.get_tables.return_value = {
            "TableList": [
                {
                    "Name": "tbl_a",
                    "StorageDescriptor": {
                        "Columns": [{"Name": "col1", "Type": "string"}]
                    },
                }
            ]
        }
        ddb = _mock()
        ddb.get_item.return_value = {
            "Item": {
                "pk": {"S": "ref-key"},
                "schema": {"S": json.dumps({})},
            }
        }
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        result = glue_crawler_and_catalog_sync(
            crawler_name="my-crawler",
            table_name="schema-ref",
            reference_key="ref-key",
            region_name=REGION,
        )
        assert isinstance(result, CrawlerSyncResult)
        assert result.crawler_name == "my-crawler"
        assert result.tables_found == 1
        assert "NEW TABLE: tbl_a" in result.schema_changes
        assert result.reference_updated is True

    def test_start_crawler_error(self, monkeypatch) -> None:
        glue = _mock()
        glue.start_crawler.side_effect = _client_error("EntityNotFoundException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        with pytest.raises(RuntimeError, match="Failed to start crawler"):
            glue_crawler_and_catalog_sync("c", "t", "k")

    def test_crawler_already_running(self, monkeypatch) -> None:
        """CrawlerRunningException should be tolerated."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None, time=lambda: 1000))
        glue = _mock()
        glue.start_crawler.side_effect = ClientError(
            {"Error": {"Code": "CrawlerRunningException", "Message": "already running"}},
            "StartCrawler",
        )
        glue.get_crawler.return_value = {
            "Crawler": {"State": "READY", "Targets": {"CatalogTargets": []}}
        }
        ddb = _mock()
        ddb.get_item.return_value = {"Item": {"pk": {"S": "k"}, "schema": {"S": "{}"}}}
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        # Should not raise
        result = glue_crawler_and_catalog_sync("c", "t", "k")
        assert result.tables_found == 0

    def test_get_crawler_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.get_crawler.side_effect = _client_error("InternalServiceException")
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        with pytest.raises(RuntimeError, match="Failed to describe crawler"):
            glue_crawler_and_catalog_sync("c", "t", "k")

    def test_crawler_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.get_crawler.return_value = {
            "Crawler": {"State": "RUNNING", "Targets": {}}
        }
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        with pytest.raises(RuntimeError, match="did not finish within timeout"):
            glue_crawler_and_catalog_sync("c", "t", "k")

    def test_no_catalog_targets_no_db(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None, time=lambda: 1000))
        glue = _mock()
        glue.get_crawler.return_value = {
            "Crawler": {"State": "READY", "Targets": {"S3Targets": [{"Path": "s3://b/"}]}}
        }
        ddb = _mock()
        ddb.get_item.return_value = {"Item": {"pk": {"S": "k"}, "schema": {"S": "{}"}}}
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        result = glue_crawler_and_catalog_sync("c", "t", "k")
        assert result.tables_found == 0

    def test_table_dropped_detected(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None, time=lambda: 1000))
        glue = _mock()
        glue.get_crawler.return_value = {
            "Crawler": {"State": "READY", "Targets": {"CatalogTargets": [{"DatabaseName": "db"}]}}
        }
        glue.get_tables.return_value = {"TableList": []}
        ddb = _mock()
        ddb.get_item.return_value = {
            "Item": {
                "pk": {"S": "k"},
                "schema": {"S": json.dumps({"old_table": [{"name": "c", "type": "s"}]})},
            }
        }
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        result = glue_crawler_and_catalog_sync("c", "t", "k")
        assert "TABLE DROPPED: old_table" in result.schema_changes

    def test_ddb_ref_read_error_logged(self, monkeypatch) -> None:
        """DynamoDB read failure for reference should log warning, not raise."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None, time=lambda: 1000))
        glue = _mock()
        glue.get_crawler.return_value = {
            "Crawler": {"State": "READY", "Targets": {"CatalogTargets": [{"DatabaseName": "db"}]}}
        }
        glue.get_tables.return_value = {"TableList": []}
        ddb = _mock()
        ddb.get_item.side_effect = _client_error("InternalServiceError")
        monkeypatch.setattr(mod, "get_client", self._factory(glue, ddb))

        # Should not raise — warning is logged
        result = glue_crawler_and_catalog_sync("c", "t", "k")
        assert result.tables_found == 0


# ---------------------------------------------------------------------------
# 7. glue_databrew_profile_pipeline
# ---------------------------------------------------------------------------


class TestGlueDatabrewProfilePipeline:
    def _factory(self, databrew: MagicMock, cw: MagicMock):
        def get_client(service: str, region_name=None):
            return {"databrew": databrew, "cloudwatch": cw}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        databrew = _mock()
        databrew.start_job_run.return_value = {"RunId": "run-1"}
        databrew.describe_job_run.return_value = {
            "State": "SUCCEEDED",
            "DatasetStatistics": {"TotalNumberOfRows": 5000},
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(databrew, cw))

        result = glue_databrew_profile_pipeline(
            job_name="profile-job",
            metric_namespace="MyApp/DataBrew",
            region_name=REGION,
        )
        assert isinstance(result, DataBrewProfileResult)
        assert result.run_id == "run-1"
        assert result.status == "SUCCEEDED"
        assert result.dataset_rows == 5000
        assert result.metrics_published == 3  # run, success, rows
        cw.put_metric_data.assert_called_once()

    def test_start_error(self, monkeypatch) -> None:
        databrew = _mock()
        databrew.start_job_run.side_effect = _client_error("ResourceNotFoundException")
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(databrew, cw))

        with pytest.raises(RuntimeError, match="Failed to start DataBrew job"):
            glue_databrew_profile_pipeline("job", "ns")

    def test_describe_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        databrew = _mock()
        databrew.start_job_run.return_value = {"RunId": "r1"}
        databrew.describe_job_run.side_effect = _client_error()
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(databrew, cw))

        with pytest.raises(RuntimeError, match="Failed to describe DataBrew run"):
            glue_databrew_profile_pipeline("job", "ns")

    def test_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        databrew = _mock()
        databrew.start_job_run.return_value = {"RunId": "r1"}
        databrew.describe_job_run.return_value = {"State": "RUNNING"}
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(databrew, cw))

        with pytest.raises(RuntimeError, match="timed out"):
            glue_databrew_profile_pipeline("job", "ns")

    def test_cw_error_logged(self, monkeypatch) -> None:
        """CloudWatch metric publish failure should be logged, not raised."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        databrew = _mock()
        databrew.start_job_run.return_value = {"RunId": "r1"}
        databrew.describe_job_run.return_value = {"State": "SUCCEEDED"}
        cw = _mock()
        cw.put_metric_data.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(databrew, cw))

        result = glue_databrew_profile_pipeline("job", "ns")
        assert result.metrics_published == 0

    def test_no_dataset_rows(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        databrew = _mock()
        databrew.start_job_run.return_value = {"RunId": "r1"}
        databrew.describe_job_run.return_value = {"State": "SUCCEEDED"}
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(databrew, cw))

        result = glue_databrew_profile_pipeline("job", "ns")
        assert result.dataset_rows is None
        # Only 2 metrics published (no rows metric)
        assert result.metrics_published == 2


# ---------------------------------------------------------------------------
# 8. emr_serverless_job_runner
# ---------------------------------------------------------------------------


class TestEmrServerlessJobRunner:
    def _factory(self, emr: MagicMock, cw: MagicMock, ddb: MagicMock):
        def get_client(service: str, region_name=None):
            return {"emr-serverless": emr, "cloudwatch": cw, "dynamodb": ddb}.get(
                service, MagicMock()
            )

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 110.0, 110]),
        ))
        emr = _mock()
        emr.start_job_run.return_value = {"jobRunId": "jr-1"}
        emr.get_job_run.return_value = {"jobRun": {"state": "SUCCESS"}}
        cw = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(emr, cw, ddb))

        result = emr_serverless_job_runner(
            application_id="app-1",
            execution_role_arn="arn:role",
            job_driver={"sparkSubmit": {"entryPoint": "s3://b/j.py"}},
            table_name="manifest",
            metric_namespace="MyApp/EMR",
            region_name=REGION,
        )
        assert isinstance(result, EMRJobResult)
        assert result.job_run_id == "jr-1"
        assert result.status == "SUCCESS"
        assert result.metrics_published == 2
        cw.put_metric_data.assert_called_once()
        ddb.put_item.assert_called_once()

    def test_start_error(self, monkeypatch) -> None:
        emr = _mock()
        emr.start_job_run.side_effect = _client_error("ValidationException")
        cw = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(emr, cw, ddb))

        with pytest.raises(RuntimeError, match="Failed to start EMR Serverless"):
            emr_serverless_job_runner("app", "arn:r", {}, "tbl", "ns")

    def test_get_job_run_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0]),
        ))
        emr = _mock()
        emr.start_job_run.return_value = {"jobRunId": "jr-2"}
        emr.get_job_run.side_effect = _client_error()
        cw = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(emr, cw, ddb))

        with pytest.raises(RuntimeError, match="Failed to describe EMR job run"):
            emr_serverless_job_runner("app", "arn:r", {}, "tbl", "ns")

    def test_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0]),
        ))
        emr = _mock()
        emr.start_job_run.return_value = {"jobRunId": "jr-3"}
        emr.get_job_run.return_value = {"jobRun": {"state": "RUNNING"}}
        cw = _mock()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(emr, cw, ddb))

        with pytest.raises(RuntimeError, match="timed out"):
            emr_serverless_job_runner("app", "arn:r", {}, "tbl", "ns")

    def test_cw_error_logged(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 110.0, 110]),
        ))
        emr = _mock()
        emr.start_job_run.return_value = {"jobRunId": "jr-4"}
        emr.get_job_run.return_value = {"jobRun": {"state": "SUCCESS"}}
        cw = _mock()
        cw.put_metric_data.side_effect = _client_error()
        ddb = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(emr, cw, ddb))

        result = emr_serverless_job_runner("app", "arn:r", {}, "tbl", "ns")
        assert result.metrics_published == 0

    def test_ddb_error_logged(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(
            sleep=lambda *a: None,
            time=MagicMock(side_effect=[100.0, 110.0, 110]),
        ))
        emr = _mock()
        emr.start_job_run.return_value = {"jobRunId": "jr-5"}
        emr.get_job_run.return_value = {"jobRun": {"state": "SUCCESS"}}
        cw = _mock()
        ddb = _mock()
        ddb.put_item.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(emr, cw, ddb))

        # Should not raise
        result = emr_serverless_job_runner("app", "arn:r", {}, "tbl", "ns")
        assert result.status == "SUCCESS"


# ---------------------------------------------------------------------------
# 9. timestream_query_to_s3
# ---------------------------------------------------------------------------


class TestTimestreamQueryToS3:
    def _factory(self, ts: MagicMock, s3: MagicMock):
        def get_client(service: str, region_name=None):
            return {"timestream-query": ts, "s3": s3}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        ts = _mock()
        ts.query.return_value = {
            "ColumnInfo": [{"Name": "time"}, {"Name": "value"}],
            "Rows": [
                {"Data": [{"ScalarValue": "2025-01-01"}, {"ScalarValue": "42"}]},
                {"Data": [{"ScalarValue": "2025-01-02"}, {"ScalarValue": "43"}]},
            ],
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ts, s3))

        result = timestream_query_to_s3(
            query_string="SELECT * FROM db.tbl",
            bucket="bkt",
            output_key="out.csv",
            region_name=REGION,
        )
        assert isinstance(result, TimestreamExportResult)
        assert result.row_count == 2
        assert result.s3_key == "out.csv"
        assert result.column_names == ["time", "value"]
        s3.put_object.assert_called_once()

    def test_query_error(self, monkeypatch) -> None:
        ts = _mock()
        ts.query.side_effect = _client_error("ValidationException")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ts, s3))

        with pytest.raises(RuntimeError, match="Timestream query failed"):
            timestream_query_to_s3("q", "bkt", "k")

    def test_s3_put_error(self, monkeypatch) -> None:
        ts = _mock()
        ts.query.return_value = {
            "ColumnInfo": [{"Name": "c"}],
            "Rows": [],
        }
        s3 = _mock()
        s3.put_object.side_effect = _client_error("NoSuchBucket")
        monkeypatch.setattr(mod, "get_client", self._factory(ts, s3))

        with pytest.raises(RuntimeError, match="Failed to write CSV"):
            timestream_query_to_s3("q", "bkt", "k")

    def test_pagination(self, monkeypatch) -> None:
        ts = _mock()
        ts.query.side_effect = [
            {
                "ColumnInfo": [{"Name": "c"}],
                "Rows": [{"Data": [{"ScalarValue": "a"}]}],
                "NextToken": "tok-2",
            },
            {
                "ColumnInfo": [{"Name": "c"}],
                "Rows": [{"Data": [{"ScalarValue": "b"}]}],
            },
        ]
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ts, s3))

        result = timestream_query_to_s3("q", "bkt", "k")
        assert result.row_count == 2

    def test_empty_results(self, monkeypatch) -> None:
        ts = _mock()
        ts.query.return_value = {
            "ColumnInfo": [{"Name": "c"}],
            "Rows": [],
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(ts, s3))

        result = timestream_query_to_s3("q", "bkt", "k")
        assert result.row_count == 0


# ---------------------------------------------------------------------------
# 10. neptune_graph_query_to_s3
# ---------------------------------------------------------------------------


class TestNeptuneGraphQueryToS3:
    def _factory(self, neptune: MagicMock, s3: MagicMock):
        def get_client(service: str, region_name=None):
            return {"neptune-graph": neptune, "s3": s3}.get(service, MagicMock())

        return get_client

    def test_success_list_results(self, monkeypatch) -> None:
        neptune = _mock()
        neptune.execute_query.return_value = {
            "payload": json.dumps([{"n": "Alice"}, {"n": "Bob"}]).encode()
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        result = neptune_graph_query_to_s3(
            graph_identifier="g-1",
            query_string="MATCH (n) RETURN n",
            language="OPEN_CYPHER",
            bucket="bkt",
            output_key="out.json",
            region_name=REGION,
        )
        assert isinstance(result, NeptuneQueryResult)
        assert result.result_count == 2
        assert result.s3_key == "out.json"
        s3.put_object.assert_called_once()

    def test_dict_results(self, monkeypatch) -> None:
        """When payload is a dict with 'results' key."""
        neptune = _mock()
        neptune.execute_query.return_value = {
            "payload": json.dumps({"results": [{"a": 1}]}).encode()
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        result = neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")
        assert result.result_count == 1

    def test_dict_without_results_key(self, monkeypatch) -> None:
        """Dict without 'results' wraps itself."""
        neptune = _mock()
        neptune.execute_query.return_value = {
            "payload": json.dumps({"foo": "bar"}).encode()
        }
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        result = neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")
        assert result.result_count == 1  # [{"foo": "bar"}]

    def test_streaming_body(self, monkeypatch) -> None:
        """Payload with .read() method (streaming body)."""
        neptune = _mock()
        body = MagicMock()
        body.read.return_value = json.dumps([{"x": 1}]).encode()
        neptune.execute_query.return_value = {"payload": body}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        result = neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")
        assert result.result_count == 1

    def test_empty_payload(self, monkeypatch) -> None:
        neptune = _mock()
        neptune.execute_query.return_value = {"payload": b""}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        result = neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")
        assert result.result_count == 0

    def test_invalid_json_payload(self, monkeypatch) -> None:
        neptune = _mock()
        neptune.execute_query.return_value = {"payload": b"not json"}
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        result = neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")
        assert result.result_count == 0  # empty list fallback

    def test_query_error(self, monkeypatch) -> None:
        neptune = _mock()
        neptune.execute_query.side_effect = _client_error("InternalError")
        s3 = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        with pytest.raises(RuntimeError, match="Neptune graph query failed"):
            neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")

    def test_s3_put_error(self, monkeypatch) -> None:
        neptune = _mock()
        neptune.execute_query.return_value = {"payload": json.dumps([]).encode()}
        s3 = _mock()
        s3.put_object.side_effect = _client_error("NoSuchBucket")
        monkeypatch.setattr(mod, "get_client", self._factory(neptune, s3))

        with pytest.raises(RuntimeError, match="Failed to write Neptune results"):
            neptune_graph_query_to_s3("g", "q", "OPEN_CYPHER", "bkt", "k")


# ---------------------------------------------------------------------------
# 11. elbv2_access_log_analyzer
# ---------------------------------------------------------------------------


class TestElbv2AccessLogAnalyzer:
    def _factory(self, elbv2: MagicMock, athena: MagicMock):
        def get_client(service: str, region_name=None):
            return {"elbv2": elbv2, "athena": athena}.get(service, MagicMock())

        return get_client

    def test_success_logging_enabled(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [
                {"Key": "access_logs.s3.enabled", "Value": "true"},
                {"Key": "access_logs.s3.bucket", "Value": "bkt"},
            ]
        }
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-1"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.return_value = {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "status_code"}, {"VarCharValue": "count"}]},
                    {"Data": [{"VarCharValue": "500"}, {"VarCharValue": "42"}]},
                    {"Data": [{"VarCharValue": "404"}, {"VarCharValue": "10"}]},
                ]
            }
        }
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        result = elbv2_access_log_analyzer(
            load_balancer_arn="arn:aws:elbv2:us-east-1:123:loadbalancer/app/lb/abc123",
            bucket="bkt",
            log_prefix="logs",
            athena_database="adb",
            athena_output_location="s3://bkt/athena/",
            region_name=REGION,
        )
        assert isinstance(result, AccessLogAnalysis)
        assert result.logging_enabled is True
        assert result.athena_table_created is True
        assert len(result.top_errors) == 2
        assert result.top_errors[0] == {"status_code": "500", "count": "42"}

    def test_logging_not_enabled_modifies(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [{"Key": "access_logs.s3.enabled", "Value": "false"}]
        }
        athena = _mock()
        athena.start_query_execution.return_value = {"QueryExecutionId": "qe-2"}
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.return_value = {"ResultSet": {"Rows": []}}
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        result = elbv2_access_log_analyzer(
            "arn:elb/lb/abc", "bkt", "logs", "db", "s3://o/"
        )
        assert result.logging_enabled is True
        elbv2.modify_load_balancer_attributes.assert_called_once()

    def test_elbv2_error(self, monkeypatch) -> None:
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.side_effect = _client_error()
        athena = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        with pytest.raises(RuntimeError, match="Failed to configure ELBv2"):
            elbv2_access_log_analyzer("arn:lb", "bkt", "pfx", "db", "s3://o/")

    def test_athena_table_creation_error_logged(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [{"Key": "access_logs.s3.enabled", "Value": "true"}]
        }
        athena = _mock()
        # First call is for table DDL, second for error query
        athena.start_query_execution.side_effect = [
            _client_error("InvalidRequestException"),  # DDL fails
            {"QueryExecutionId": "qe-3"},  # error query succeeds
        ]
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.return_value = {"ResultSet": {"Rows": []}}
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        result = elbv2_access_log_analyzer("arn:lb/lb/x", "bkt", "pfx", "db", "s3://o/")
        assert result.athena_table_created is False

    def test_error_query_start_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [{"Key": "access_logs.s3.enabled", "Value": "true"}]
        }
        athena = _mock()
        athena.start_query_execution.side_effect = [
            {"QueryExecutionId": "qe-ddl"},  # DDL OK
            _client_error("InvalidRequestException"),  # error query fails
        ]
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        with pytest.raises(RuntimeError, match="Failed to start Athena error codes query"):
            elbv2_access_log_analyzer("arn:lb/lb/x", "bkt", "pfx", "db", "s3://o/")

    def test_error_query_poll_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [{"Key": "access_logs.s3.enabled", "Value": "true"}]
        }
        athena = _mock()
        athena.start_query_execution.side_effect = [
            {"QueryExecutionId": "qe-ddl"},
            {"QueryExecutionId": "qe-err"},
        ]
        athena.get_query_execution.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        with pytest.raises(RuntimeError, match="Failed to poll Athena query"):
            elbv2_access_log_analyzer("arn:lb/lb/x", "bkt", "pfx", "db", "s3://o/")

    def test_error_query_failed_returns_empty(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [{"Key": "access_logs.s3.enabled", "Value": "true"}]
        }
        athena = _mock()
        athena.start_query_execution.side_effect = [
            {"QueryExecutionId": "qe-ddl"},
            {"QueryExecutionId": "qe-err"},
        ]
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "FAILED"}}
        }
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        result = elbv2_access_log_analyzer("arn:lb/lb/x", "bkt", "pfx", "db", "s3://o/")
        assert result.top_errors == []

    def test_get_query_results_error_logged(self, monkeypatch) -> None:
        """get_query_results failure is logged, returns empty errors."""
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        elbv2 = _mock()
        elbv2.describe_load_balancer_attributes.return_value = {
            "Attributes": [{"Key": "access_logs.s3.enabled", "Value": "true"}]
        }
        athena = _mock()
        athena.start_query_execution.side_effect = [
            {"QueryExecutionId": "qe-ddl"},
            {"QueryExecutionId": "qe-err"},
        ]
        athena.get_query_execution.return_value = {
            "QueryExecution": {"Status": {"State": "SUCCEEDED"}}
        }
        athena.get_query_results.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(elbv2, athena))

        result = elbv2_access_log_analyzer("arn:lb/lb/x", "bkt", "pfx", "db", "s3://o/")
        assert result.top_errors == []


# ---------------------------------------------------------------------------
# 12. glue_job_output_to_redshift
# ---------------------------------------------------------------------------


class TestGlueJobOutputToRedshift:
    def _factory(self, glue: MagicMock, rd: MagicMock):
        def get_client(service: str, region_name=None):
            return {"glue": glue, "redshift-data": rd}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-1"}
        glue.get_job_run.return_value = {"JobRun": {"JobRunState": "SUCCEEDED"}}
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "copy-1"}
        rd.describe_statement.return_value = {"Status": "FINISHED"}
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        result = glue_job_output_to_redshift(
            job_name="etl-job",
            job_arguments={"--key": "val"},
            workgroup_name="wg",
            database="db",
            target_table="target",
            iam_role_arn="arn:role",
            s3_output_path="s3://bkt/out/",
            region_name=REGION,
        )
        assert isinstance(result, GlueToRedshiftResult)
        assert result.job_run_id == "jr-1"
        assert result.glue_status == "SUCCEEDED"
        assert result.copy_statement_id == "copy-1"
        assert result.copy_status == "FINISHED"

    def test_start_glue_error(self, monkeypatch) -> None:
        glue = _mock()
        glue.start_job_run.side_effect = _client_error("EntityNotFoundException")
        rd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="Failed to start Glue job"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")

    def test_get_job_run_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-2"}
        glue.get_job_run.side_effect = _client_error()
        rd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="Failed to describe Glue run"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")

    def test_glue_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-3"}
        glue.get_job_run.return_value = {"JobRun": {"JobRunState": "RUNNING"}}
        rd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="timed out"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")

    def test_glue_failed(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-4"}
        glue.get_job_run.return_value = {"JobRun": {"JobRunState": "FAILED"}}
        rd = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="Glue job .* failed"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")

    def test_copy_execute_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-5"}
        glue.get_job_run.return_value = {"JobRun": {"JobRunState": "SUCCEEDED"}}
        rd = _mock()
        rd.execute_statement.side_effect = _client_error("ValidationException")
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="Failed to submit Redshift COPY"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")

    def test_copy_describe_error(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-6"}
        glue.get_job_run.return_value = {"JobRun": {"JobRunState": "SUCCEEDED"}}
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "copy-2"}
        rd.describe_statement.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="Failed to describe COPY statement"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")

    def test_copy_timeout(self, monkeypatch) -> None:
        monkeypatch.setattr(mod, "time", MagicMock(sleep=lambda *a: None))
        glue = _mock()
        glue.start_job_run.return_value = {"JobRunId": "jr-7"}
        glue.get_job_run.return_value = {"JobRun": {"JobRunState": "SUCCEEDED"}}
        rd = _mock()
        rd.execute_statement.return_value = {"Id": "copy-3"}
        rd.describe_statement.return_value = {"Status": "STARTED"}
        monkeypatch.setattr(mod, "get_client", self._factory(glue, rd))

        with pytest.raises(RuntimeError, match="Redshift COPY statement .* timed out"):
            glue_job_output_to_redshift("j", {}, "wg", "db", "t", "arn:r", "s3://")


# ---------------------------------------------------------------------------
# 13. opensearch_index_lifecycle_manager
# ---------------------------------------------------------------------------


class TestOpensearchIndexLifecycleManager:
    def _factory(self, oss: MagicMock, cw: MagicMock):
        def get_client(service: str, region_name=None):
            return {"opensearchserverless": oss, "cloudwatch": cw}.get(service, MagicMock())

        return get_client

    def test_success(self, monkeypatch) -> None:
        oss = _mock()
        oss.batch_get_collection.return_value = {
            "collectionDetails": [
                {"name": "col-1", "status": "ACTIVE"},
                {"name": "col-2", "status": "CREATING"},
                {"name": "col-3", "status": "ACTIVE"},
            ]
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(oss, cw))

        result = opensearch_index_lifecycle_manager(
            collection_names=["col-1", "col-2", "col-3"],
            metric_namespace="MyApp/OpenSearch",
            region_name=REGION,
        )
        assert isinstance(result, IndexLifecycleResult)
        assert result.collections_checked == 3
        assert result.active_collections == 2
        assert result.metrics_published == 3
        cw.put_metric_data.assert_called_once()

    def test_batch_get_error(self, monkeypatch) -> None:
        oss = _mock()
        oss.batch_get_collection.side_effect = _client_error("ValidationException")
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(oss, cw))

        with pytest.raises(RuntimeError, match="Failed to describe OpenSearch"):
            opensearch_index_lifecycle_manager(["col-1"], "ns")

    def test_cw_error_logged(self, monkeypatch) -> None:
        oss = _mock()
        oss.batch_get_collection.return_value = {
            "collectionDetails": [{"name": "c", "status": "ACTIVE"}]
        }
        cw = _mock()
        cw.put_metric_data.side_effect = _client_error()
        monkeypatch.setattr(mod, "get_client", self._factory(oss, cw))

        result = opensearch_index_lifecycle_manager(["c"], "ns")
        assert result.metrics_published == 0
        assert result.active_collections == 1

    def test_empty_collections(self, monkeypatch) -> None:
        oss = _mock()
        oss.batch_get_collection.return_value = {"collectionDetails": []}
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(oss, cw))

        result = opensearch_index_lifecycle_manager([], "ns")
        assert result.collections_checked == 0
        assert result.active_collections == 0

    def test_no_active_collections(self, monkeypatch) -> None:
        oss = _mock()
        oss.batch_get_collection.return_value = {
            "collectionDetails": [
                {"name": "c1", "status": "CREATING"},
                {"name": "c2", "status": "DELETING"},
            ]
        }
        cw = _mock()
        monkeypatch.setattr(mod, "get_client", self._factory(oss, cw))

        result = opensearch_index_lifecycle_manager(["c1", "c2"], "ns")
        assert result.collections_checked == 2
        assert result.active_collections == 0
