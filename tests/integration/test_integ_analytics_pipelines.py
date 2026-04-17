"""Integration tests for aws_util.analytics_pipelines against LocalStack."""
from __future__ import annotations

import json
import time

import pytest
from botocore.exceptions import ClientError

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. redshift_unload_to_s3
# ---------------------------------------------------------------------------


class TestRedshiftUnloadToS3:
    @pytest.mark.skip(reason="Redshift Data API not available in LocalStack community")
    def test_unloads_and_partitions(self, s3_bucket):
        from aws_util.analytics_pipelines import redshift_unload_to_s3

        result = redshift_unload_to_s3(
            cluster_identifier="test-cluster",
            database="testdb",
            db_user="admin",
            query="SELECT 1 AS id, 'hello' AS msg",
            s3_path=f"s3://{s3_bucket}/unload/",
            iam_role_arn="arn:aws:iam::000000000000:role/test-role",
            athena_database="default",
            athena_table="test_table",
            partition_key="dt",
            partition_value="2024-01-01",
            region_name=REGION,
        )
        assert isinstance(result.statement_id, str)
        assert isinstance(result.rows_unloaded, int)
        assert result.s3_path == f"s3://{s3_bucket}/unload/"


# ---------------------------------------------------------------------------
# 2. redshift_serverless_query_runner
# ---------------------------------------------------------------------------


class TestRedshiftServerlessQueryRunner:
    @pytest.mark.skip(reason="Redshift Serverless not available in LocalStack community")
    def test_runs_query_to_s3(self, s3_bucket):
        from aws_util.analytics_pipelines import redshift_serverless_query_runner

        result = redshift_serverless_query_runner(
            workgroup_name="test-workgroup",
            database="testdb",
            sql="SELECT 1 AS id",
            bucket=s3_bucket,
            output_key="query-results/output.json",
            region_name=REGION,
        )
        assert isinstance(result.statement_id, str)
        assert result.s3_key == "query-results/output.json"
        assert isinstance(result.row_count, int)


# ---------------------------------------------------------------------------
# 3. quicksight_dashboard_embedder
# ---------------------------------------------------------------------------


class TestQuickSightDashboardEmbedder:
    @pytest.mark.skip(reason="QuickSight not available in LocalStack community")
    def test_generates_embed_url(self):
        from aws_util.analytics_pipelines import quicksight_dashboard_embedder

        result = quicksight_dashboard_embedder(
            aws_account_id="000000000000",
            dashboard_id="test-dashboard-id",
            user_arn=None,
            namespace="default",
            session_lifetime=600,
            region_name=REGION,
        )
        assert isinstance(result.embed_url, str)
        assert isinstance(result.status, int)
        assert isinstance(result.request_id, str)


# ---------------------------------------------------------------------------
# 4. quicksight_dataset_refresher
# ---------------------------------------------------------------------------


class TestQuickSightDatasetRefresher:
    @pytest.mark.skip(reason="QuickSight not available in LocalStack community")
    def test_refreshes_dataset(self, sns_topic):
        from aws_util.analytics_pipelines import quicksight_dataset_refresher

        ingestion_id = f"ingestion-{int(time.time())}"
        result = quicksight_dataset_refresher(
            aws_account_id="000000000000",
            dataset_id="test-dataset-id",
            ingestion_id=ingestion_id,
            sns_topic_arn=sns_topic,
            poll_interval=1,
            region_name=REGION,
        )
        assert result.ingestion_id == ingestion_id
        assert isinstance(result.status, str)
        assert isinstance(result.duration_seconds, float)


# ---------------------------------------------------------------------------
# 5. athena_result_to_dynamodb
# ---------------------------------------------------------------------------


class TestAthenaResultToDynamodb:
    @pytest.mark.skip(reason="Athena not available in LocalStack community")
    def test_writes_results_to_dynamodb(self, dynamodb_pk_table, s3_bucket):
        from aws_util.analytics_pipelines import athena_result_to_dynamodb

        result = athena_result_to_dynamodb(
            query="SELECT 'key1' AS pk, 'val1' AS data",
            database="default",
            output_location=f"s3://{s3_bucket}/athena-results/",
            table_name=dynamodb_pk_table,
            key_column="pk",
            region_name=REGION,
        )
        assert isinstance(result.query_execution_id, str)
        assert isinstance(result.rows_written, int)
        assert result.status == "SUCCEEDED"


# ---------------------------------------------------------------------------
# 6. glue_crawler_and_catalog_sync
# ---------------------------------------------------------------------------


class TestGlueCrawlerAndCatalogSync:
    @pytest.mark.skip(reason="Glue not available in LocalStack community")
    def test_syncs_catalog(self, dynamodb_pk_table):
        from aws_util.analytics_pipelines import glue_crawler_and_catalog_sync

        result = glue_crawler_and_catalog_sync(
            crawler_name="test-crawler",
            table_name=dynamodb_pk_table,
            reference_key="schema-ref-001",
            region_name=REGION,
        )
        assert result.crawler_name == "test-crawler"
        assert isinstance(result.tables_found, int)
        assert isinstance(result.schema_changes, list)
        assert isinstance(result.reference_updated, bool)


# ---------------------------------------------------------------------------
# 7. glue_databrew_profile_pipeline
# ---------------------------------------------------------------------------


class TestGlueDatabrewProfilePipeline:
    @pytest.mark.skip(reason="Glue DataBrew not available in LocalStack community")
    def test_profiles_dataset(self):
        from aws_util.analytics_pipelines import glue_databrew_profile_pipeline

        result = glue_databrew_profile_pipeline(
            job_name="test-profile-job",
            metric_namespace="TestDataBrew",
            region_name=REGION,
        )
        assert isinstance(result.run_id, str)
        assert isinstance(result.status, str)
        assert isinstance(result.metrics_published, int)


# ---------------------------------------------------------------------------
# 8. emr_serverless_job_runner
# ---------------------------------------------------------------------------


class TestEmrServerlessJobRunner:
    @pytest.mark.skip(reason="EMR Serverless not available in LocalStack community")
    def test_runs_spark_job(self, dynamodb_table):
        from aws_util.analytics_pipelines import emr_serverless_job_runner

        result = emr_serverless_job_runner(
            application_id="app-test-001",
            execution_role_arn="arn:aws:iam::000000000000:role/test-role",
            job_driver={
                "sparkSubmit": {
                    "entryPoint": "s3://bucket/script.py",
                    "sparkSubmitParameters": "--conf spark.executor.memory=4g",
                },
            },
            table_name=dynamodb_table,
            metric_namespace="TestEMR",
            region_name=REGION,
        )
        assert isinstance(result.job_run_id, str)
        assert isinstance(result.status, str)
        assert isinstance(result.duration_seconds, float)
        assert isinstance(result.metrics_published, int)


# ---------------------------------------------------------------------------
# 9. timestream_query_to_s3
# ---------------------------------------------------------------------------


class TestTimestreamQueryToS3:
    @pytest.mark.skip(reason="Timestream not available in LocalStack community")
    def test_exports_to_s3(self, s3_bucket):
        from aws_util.analytics_pipelines import timestream_query_to_s3

        result = timestream_query_to_s3(
            query_string="SELECT * FROM testdb.testtable LIMIT 10",
            bucket=s3_bucket,
            output_key="timestream/export.csv",
            region_name=REGION,
        )
        assert result.s3_key == "timestream/export.csv"
        assert isinstance(result.row_count, int)
        assert isinstance(result.column_names, list)


# ---------------------------------------------------------------------------
# 10. neptune_graph_query_to_s3
# ---------------------------------------------------------------------------


class TestNeptuneGraphQueryToS3:
    @pytest.mark.skip(reason="Neptune not available in LocalStack community")
    def test_queries_graph(self, s3_bucket):
        from aws_util.analytics_pipelines import neptune_graph_query_to_s3

        result = neptune_graph_query_to_s3(
            graph_identifier="test-graph",
            query_string="MATCH (n) RETURN n LIMIT 10",
            language="OPEN_CYPHER",
            bucket=s3_bucket,
            output_key="neptune/results.json",
            region_name=REGION,
        )
        assert result.s3_key == "neptune/results.json"
        assert isinstance(result.result_count, int)


# ---------------------------------------------------------------------------
# 11. elbv2_access_log_analyzer
# ---------------------------------------------------------------------------


class TestElbv2AccessLogAnalyzer:
    @pytest.mark.skip(reason="Athena not available in LocalStack community")
    def test_analyzes_access_logs(self, s3_bucket):
        from aws_util.analytics_pipelines import elbv2_access_log_analyzer

        # This function requires both ELBv2 (available) and Athena (not available).
        # Since the function creates an Athena table and runs a query, the overall
        # test must be skipped.
        result = elbv2_access_log_analyzer(
            load_balancer_arn="arn:aws:elasticloadbalancing:us-east-1:000000000000:loadbalancer/app/test-lb/50dc6c495c0c9188",
            bucket=s3_bucket,
            log_prefix="elb-logs",
            athena_database="default",
            athena_output_location=f"s3://{s3_bucket}/athena-output/",
            region_name=REGION,
        )
        assert isinstance(result.logging_enabled, bool)
        assert isinstance(result.athena_table_created, bool)
        assert isinstance(result.query_execution_id, str)
        assert isinstance(result.top_errors, list)


# ---------------------------------------------------------------------------
# 12. glue_job_output_to_redshift
# ---------------------------------------------------------------------------


class TestGlueJobOutputToRedshift:
    @pytest.mark.skip(reason="Glue and Redshift not available in LocalStack community")
    def test_etl_to_redshift(self, s3_bucket):
        from aws_util.analytics_pipelines import glue_job_output_to_redshift

        result = glue_job_output_to_redshift(
            job_name="test-etl-job",
            job_arguments={"--input": f"s3://{s3_bucket}/input/"},
            workgroup_name="test-workgroup",
            database="testdb",
            target_table="public.target_table",
            iam_role_arn="arn:aws:iam::000000000000:role/test-role",
            s3_output_path=f"s3://{s3_bucket}/etl-output/",
            region_name=REGION,
        )
        assert isinstance(result.job_run_id, str)
        assert isinstance(result.glue_status, str)
        assert isinstance(result.copy_statement_id, str)
        assert isinstance(result.copy_status, str)


# ---------------------------------------------------------------------------
# 13. opensearch_index_lifecycle_manager
# ---------------------------------------------------------------------------


class TestOpensearchIndexLifecycleManager:
    @pytest.mark.skip(reason="OpenSearch Serverless not available in LocalStack community")
    def test_checks_collections(self):
        from aws_util.analytics_pipelines import opensearch_index_lifecycle_manager

        result = opensearch_index_lifecycle_manager(
            collection_names=["test-collection"],
            metric_namespace="TestOpenSearch",
            region_name=REGION,
        )
        assert isinstance(result.collections_checked, int)
        assert isinstance(result.active_collections, int)
        assert isinstance(result.metrics_published, int)
