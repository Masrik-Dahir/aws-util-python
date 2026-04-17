"""Analytics Pipeline utilities for multi-service orchestration.

Provides helpers for chaining analytics and data services in serverless pipelines:

- **Redshift unload to S3** — Execute a Redshift UNLOAD via Data API, wait for completion,
  then register the output as an Athena partition.
- **Redshift Serverless query runner** — Run SQL against Redshift Serverless, poll for
  results, write output to S3 as JSON.
- **QuickSight dashboard embedder** — Generate an embedding URL for a QuickSight dashboard.
- **QuickSight dataset refresher** — Trigger a SPICE ingestion refresh and notify via SNS.
- **Athena result to DynamoDB** — Run an Athena query and upsert result rows into DynamoDB.
- **Glue crawler and catalog sync** — Start a Glue Crawler and compare schema against DynamoDB.
- **Glue DataBrew profile pipeline** — Run a DataBrew profile job and publish stats to CloudWatch.
- **EMR Serverless job runner** — Submit a Spark job, push metrics to CloudWatch and DynamoDB.
- **Timestream query to S3** — Execute a Timestream query and write results as CSV to S3.
- **Neptune graph query to S3** — Run a Neptune Analytics query and serialize results to S3.
- **ELBv2 access log analyzer** — Enable access logging, create Athena table, run error query.
- **Glue job output to Redshift** — Run a Glue ETL job then COPY output into Redshift Serverless.
- **OpenSearch index lifecycle manager** — Check collection status and publish stats to CloudWatch.
"""

from __future__ import annotations

import csv
import io
import json
import logging
import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "AccessLogAnalysis",
    "AthenaToDBResult",
    "CrawlerSyncResult",
    "DataBrewProfileResult",
    "DatasetRefreshResult",
    "EMRJobResult",
    "GlueToRedshiftResult",
    "IndexLifecycleResult",
    "NeptuneQueryResult",
    "QuickSightEmbedResult",
    "RedshiftUnloadResult",
    "ServerlessQueryResult",
    "TimestreamExportResult",
    "athena_result_to_dynamodb",
    "elbv2_access_log_analyzer",
    "emr_serverless_job_runner",
    "glue_crawler_and_catalog_sync",
    "glue_databrew_profile_pipeline",
    "glue_job_output_to_redshift",
    "neptune_graph_query_to_s3",
    "opensearch_index_lifecycle_manager",
    "quicksight_dashboard_embedder",
    "quicksight_dataset_refresher",
    "redshift_serverless_query_runner",
    "redshift_unload_to_s3",
    "timestream_query_to_s3",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class RedshiftUnloadResult(BaseModel):
    """Result of a Redshift UNLOAD operation with Athena partition registration."""

    model_config = ConfigDict(frozen=True)

    statement_id: str
    rows_unloaded: int
    s3_path: str
    partition_added: bool


class ServerlessQueryResult(BaseModel):
    """Result of a Redshift Serverless SQL query written to S3."""

    model_config = ConfigDict(frozen=True)

    statement_id: str
    row_count: int
    s3_key: str


class QuickSightEmbedResult(BaseModel):
    """Result of a QuickSight dashboard embedding URL generation."""

    model_config = ConfigDict(frozen=True)

    embed_url: str
    status: int
    request_id: str


class DatasetRefreshResult(BaseModel):
    """Result of a QuickSight SPICE dataset ingestion refresh."""

    model_config = ConfigDict(frozen=True)

    ingestion_id: str
    status: str
    rows_ingested: int | None
    duration_seconds: float


class AthenaToDBResult(BaseModel):
    """Result of an Athena query with rows upserted into DynamoDB."""

    model_config = ConfigDict(frozen=True)

    query_execution_id: str
    rows_written: int
    status: str


class CrawlerSyncResult(BaseModel):
    """Result of a Glue Crawler run with schema comparison."""

    model_config = ConfigDict(frozen=True)

    crawler_name: str
    tables_found: int
    schema_changes: list[str]
    reference_updated: bool


class DataBrewProfileResult(BaseModel):
    """Result of a DataBrew profile job with CloudWatch metrics."""

    model_config = ConfigDict(frozen=True)

    run_id: str
    status: str
    metrics_published: int
    dataset_rows: int | None


class EMRJobResult(BaseModel):
    """Result of an EMR Serverless Spark job submission."""

    model_config = ConfigDict(frozen=True)

    job_run_id: str
    status: str
    duration_seconds: float
    metrics_published: int


class TimestreamExportResult(BaseModel):
    """Result of a Timestream query exported to S3 as CSV."""

    model_config = ConfigDict(frozen=True)

    row_count: int
    s3_key: str
    column_names: list[str]


class NeptuneQueryResult(BaseModel):
    """Result of a Neptune Analytics graph query exported to S3."""

    model_config = ConfigDict(frozen=True)

    result_count: int
    s3_key: str


class AccessLogAnalysis(BaseModel):
    """Result of ELBv2 access log enablement and Athena error query."""

    model_config = ConfigDict(frozen=True)

    logging_enabled: bool
    athena_table_created: bool
    query_execution_id: str
    top_errors: list[dict[str, Any]]


class GlueToRedshiftResult(BaseModel):
    """Result of a Glue ETL job with output COPYed into Redshift."""

    model_config = ConfigDict(frozen=True)

    job_run_id: str
    glue_status: str
    copy_statement_id: str
    copy_status: str


class IndexLifecycleResult(BaseModel):
    """Result of OpenSearch Serverless collection lifecycle check."""

    model_config = ConfigDict(frozen=True)

    collections_checked: int
    active_collections: int
    metrics_published: int


# ---------------------------------------------------------------------------
# 1. redshift_unload_to_s3
# ---------------------------------------------------------------------------


def redshift_unload_to_s3(
    cluster_identifier: str,
    database: str,
    db_user: str,
    query: str,
    s3_path: str,
    iam_role_arn: str,
    athena_database: str,
    athena_table: str,
    partition_key: str,
    partition_value: str,
    region_name: str | None = None,
) -> RedshiftUnloadResult:
    """Execute a Redshift UNLOAD via Data API, then add an Athena partition.

    Submits a UNLOAD statement to Redshift via the Data API, polls until the
    statement completes, and registers the output S3 path as a new Athena
    partition using ``ALTER TABLE ADD PARTITION``.

    Args:
        cluster_identifier: Redshift cluster identifier.
        database: Redshift database name.
        db_user: Database user for the Data API.
        query: SELECT query whose results will be UNLOADed.
        s3_path: S3 destination path for the UNLOAD output (e.g. ``"s3://bucket/prefix/"``).
        iam_role_arn: IAM role ARN that Redshift will use to write to S3.
        athena_database: Athena/Glue catalog database containing the target table.
        athena_table: Athena table to which the new partition is added.
        partition_key: Partition key column name.
        partition_value: Partition key value for the new partition.
        region_name: AWS region override.

    Returns:
        A :class:`RedshiftUnloadResult` with statement ID, rows unloaded,
        S3 path, and partition registration status.

    Raises:
        RuntimeError: If the UNLOAD or Athena DDL statement fails.
    """
    redshift_data = get_client("redshift-data", region_name=region_name)
    athena = get_client("athena", region_name=region_name)

    unload_sql = (
        f"UNLOAD ('{query}') TO '{s3_path}' "
        f"IAM_ROLE '{iam_role_arn}' FORMAT AS PARQUET ALLOWOVERWRITE"
    )

    try:
        exec_resp = redshift_data.execute_statement(
            ClusterIdentifier=cluster_identifier,
            Database=database,
            DbUser=db_user,
            Sql=unload_sql,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to submit Redshift UNLOAD statement") from exc

    statement_id: str = exec_resp["Id"]

    # Poll for completion
    terminal = {"FINISHED", "FAILED", "ABORTED"}
    for _ in range(60):
        try:
            desc = redshift_data.describe_statement(Id=statement_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe statement {statement_id}") from exc
        state = desc.get("Status", "")
        if state in terminal:
            break
        time.sleep(5)
    else:
        raise RuntimeError(f"Redshift statement {statement_id} did not finish within timeout")

    if state != "FINISHED":
        err = desc.get("Error", "unknown error")
        raise RuntimeError(f"Redshift UNLOAD failed [{state}]: {err}")

    rows_unloaded: int = desc.get("ResultRows", 0) or 0

    # Add Athena partition
    partition_added = False
    location = f"{s3_path.rstrip('/')}/{partition_key}={partition_value}/"
    ddl = (
        f"ALTER TABLE {athena_database}.{athena_table} "
        f"ADD IF NOT EXISTS PARTITION ({partition_key}='{partition_value}') "
        f"LOCATION '{location}'"
    )
    try:
        athena.start_query_execution(
            QueryString=ddl,
            QueryExecutionContext={"Database": athena_database},
        )
        partition_added = True
    except ClientError as exc:
        logger.warning("Failed to add Athena partition: %s", exc)

    return RedshiftUnloadResult(
        statement_id=statement_id,
        rows_unloaded=rows_unloaded,
        s3_path=s3_path,
        partition_added=partition_added,
    )


# ---------------------------------------------------------------------------
# 2. redshift_serverless_query_runner
# ---------------------------------------------------------------------------


def redshift_serverless_query_runner(
    workgroup_name: str,
    database: str,
    sql: str,
    bucket: str,
    output_key: str,
    region_name: str | None = None,
) -> ServerlessQueryResult:
    """Run SQL against Redshift Serverless, poll for results, write to S3 as JSON.

    Executes the provided SQL statement against a Redshift Serverless workgroup
    via the Data API, polls until completion, retrieves all result rows, and
    writes them as a JSON array to S3.

    Args:
        workgroup_name: Name of the Redshift Serverless workgroup.
        database: Database to run the query against.
        sql: SQL statement to execute.
        bucket: S3 bucket for the JSON output.
        output_key: S3 object key for the JSON output file.
        region_name: AWS region override.

    Returns:
        A :class:`ServerlessQueryResult` with statement ID, row count, and S3 key.

    Raises:
        RuntimeError: If the query fails or times out.
    """
    redshift_data = get_client("redshift-data", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)

    try:
        exec_resp = redshift_data.execute_statement(
            WorkgroupName=workgroup_name,
            Database=database,
            Sql=sql,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to submit Redshift Serverless query") from exc

    statement_id: str = exec_resp["Id"]

    terminal = {"FINISHED", "FAILED", "ABORTED"}
    for _ in range(60):
        try:
            desc = redshift_data.describe_statement(Id=statement_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe statement {statement_id}") from exc
        state = desc.get("Status", "")
        if state in terminal:
            break
        time.sleep(5)
    else:
        raise RuntimeError(f"Redshift Serverless statement {statement_id} timed out")

    if state != "FINISHED":
        err = desc.get("Error", "unknown error")
        raise RuntimeError(f"Redshift Serverless query failed [{state}]: {err}")

    # Collect all result pages
    rows: list[dict[str, Any]] = []
    columns: list[str] = []
    paginator_kwargs: dict[str, Any] = {"Id": statement_id}
    first_page = True

    while True:
        try:
            page = redshift_data.get_statement_result(**paginator_kwargs)
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to retrieve query results") from exc

        if first_page:
            columns = [c.get("label", c.get("name", "")) for c in page.get("ColumnMetadata", [])]
            first_page = False

        for record in page.get("Records", []):
            row: dict[str, Any] = {}
            for col, cell in zip(columns, record, strict=False):
                val = next(iter(cell.values()), None) if cell else None
                row[col] = val
            rows.append(row)

        next_token = page.get("NextToken")
        if not next_token:
            break
        paginator_kwargs["NextToken"] = next_token

    try:
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=json.dumps(rows, default=str).encode("utf-8"),
            ContentType="application/json",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to write results to s3://{bucket}/{output_key}") from exc

    return ServerlessQueryResult(
        statement_id=statement_id,
        row_count=len(rows),
        s3_key=output_key,
    )


# ---------------------------------------------------------------------------
# 3. quicksight_dashboard_embedder
# ---------------------------------------------------------------------------


def quicksight_dashboard_embedder(
    aws_account_id: str,
    dashboard_id: str,
    user_arn: str | None = None,
    namespace: str = "default",
    session_lifetime: int = 600,
    region_name: str | None = None,
) -> QuickSightEmbedResult:
    """Generate a QuickSight dashboard embedding URL.

    Produces an anonymous or registered-user embedding URL for the specified
    QuickSight dashboard.  When *user_arn* is provided a registered-user URL
    is generated; otherwise an anonymous (unauthenticated) URL is returned.

    Args:
        aws_account_id: AWS account ID that owns the QuickSight resources.
        dashboard_id: QuickSight dashboard ID.
        user_arn: ARN of a registered QuickSight user.  ``None`` generates an
            anonymous embed URL.
        namespace: QuickSight namespace (default ``"default"``).
        session_lifetime: Embed session lifetime in seconds (default 600).
        region_name: AWS region override.

    Returns:
        A :class:`QuickSightEmbedResult` with embed URL, HTTP status, and request ID.

    Raises:
        RuntimeError: If the QuickSight API call fails.
    """
    qs = get_client("quicksight", region_name=region_name)

    try:
        if user_arn:
            resp = qs.generate_embed_url_for_registered_user(
                AwsAccountId=aws_account_id,
                SessionLifetimeInMinutes=max(1, session_lifetime // 60),
                UserArn=user_arn,
                ExperienceConfiguration={"Dashboard": {"InitialDashboardId": dashboard_id}},
            )
        else:
            resp = qs.generate_embed_url_for_anonymous_user(
                AwsAccountId=aws_account_id,
                SessionLifetimeInMinutes=max(1, session_lifetime // 60),
                Namespace=namespace,
                AuthorizedResourceArns=[
                    f"arn:aws:quicksight:{region_name or 'us-east-1'}:{aws_account_id}:dashboard/{dashboard_id}"
                ],
                ExperienceConfiguration={"Dashboard": {"InitialDashboardId": dashboard_id}},
            )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to generate QuickSight embed URL for {dashboard_id}"
        ) from exc

    return QuickSightEmbedResult(
        embed_url=resp.get("EmbedUrl", ""),
        status=resp.get("Status", 200),
        request_id=resp.get("RequestId", ""),
    )


# ---------------------------------------------------------------------------
# 4. quicksight_dataset_refresher
# ---------------------------------------------------------------------------


def quicksight_dataset_refresher(
    aws_account_id: str,
    dataset_id: str,
    ingestion_id: str,
    sns_topic_arn: str | None = None,
    poll_interval: int = 10,
    region_name: str | None = None,
) -> DatasetRefreshResult:
    """Trigger a QuickSight SPICE dataset ingestion and poll for completion.

    Creates a new SPICE ingestion for the specified dataset, polls until the
    ingestion reaches a terminal state, then optionally sends a completion
    notification via SNS.

    Args:
        aws_account_id: AWS account ID.
        dataset_id: QuickSight dataset ID to refresh.
        ingestion_id: Unique identifier for this ingestion run.
        sns_topic_arn: Optional SNS topic ARN for completion notification.
        poll_interval: Seconds between status polls (default 10).
        region_name: AWS region override.

    Returns:
        A :class:`DatasetRefreshResult` with ingestion ID, status, rows ingested,
        and elapsed duration in seconds.

    Raises:
        RuntimeError: If the ingestion creation or polling fails.
    """
    qs = get_client("quicksight", region_name=region_name)

    try:
        qs.create_ingestion(
            DataSetId=dataset_id,
            IngestionId=ingestion_id,
            AwsAccountId=aws_account_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to create ingestion {ingestion_id}") from exc

    start_time = time.time()
    terminal = {"COMPLETED", "FAILED", "CANCELLED"}
    status = "INITIALIZED"
    rows_ingested: int | None = None

    for _ in range(120):
        try:
            desc = qs.describe_ingestion(
                DataSetId=dataset_id,
                IngestionId=ingestion_id,
                AwsAccountId=aws_account_id,
            )
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe ingestion {ingestion_id}") from exc

        ingestion = desc.get("Ingestion", {})
        status = ingestion.get("IngestionStatus", status)
        row_info = ingestion.get("RowInfo", {})
        if row_info:
            rows_ingested = row_info.get("RowsIngested")

        if status in terminal:
            break
        time.sleep(poll_interval)

    duration = time.time() - start_time

    if sns_topic_arn:
        sns = get_client("sns", region_name=region_name)
        try:
            sns.publish(
                TopicArn=sns_topic_arn,
                Subject=f"QuickSight ingestion {ingestion_id} {status}",
                Message=json.dumps(
                    {
                        "dataset_id": dataset_id,
                        "ingestion_id": ingestion_id,
                        "status": status,
                        "rows_ingested": rows_ingested,
                        "duration_seconds": round(duration, 2),
                    }
                ),
            )
        except ClientError as exc:
            logger.warning("Failed to send SNS notification: %s", exc)

    return DatasetRefreshResult(
        ingestion_id=ingestion_id,
        status=status,
        rows_ingested=rows_ingested,
        duration_seconds=round(duration, 2),
    )


# ---------------------------------------------------------------------------
# 5. athena_result_to_dynamodb
# ---------------------------------------------------------------------------


def athena_result_to_dynamodb(
    query: str,
    database: str,
    output_location: str,
    table_name: str,
    key_column: str,
    region_name: str | None = None,
) -> AthenaToDBResult:
    """Run an Athena query and upsert result rows into DynamoDB.

    Executes the query via Athena, polls for completion, paginates through all
    result rows, and upserts each row into the specified DynamoDB table using
    *key_column* as the partition key.

    Args:
        query: SQL query to execute in Athena.
        database: Athena/Glue catalog database to run the query against.
        output_location: S3 path for Athena query results (e.g. ``"s3://bucket/prefix/"``).
        table_name: DynamoDB table name for the upserted rows.
        key_column: Result column name to use as the DynamoDB partition key (``"pk"``).
        region_name: AWS region override.

    Returns:
        An :class:`AthenaToDBResult` with execution ID, rows written, and final status.

    Raises:
        RuntimeError: If the Athena query or DynamoDB writes fail.
    """
    athena = get_client("athena", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    try:
        start_resp = athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": output_location},
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start Athena query") from exc

    execution_id: str = start_resp["QueryExecutionId"]

    terminal = {"SUCCEEDED", "FAILED", "CANCELLED"}
    status = "RUNNING"
    for _ in range(60):
        try:
            exec_resp = athena.get_query_execution(QueryExecutionId=execution_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to get Athena execution {execution_id}") from exc
        status = exec_resp["QueryExecution"]["Status"]["State"]
        if status in terminal:
            break
        time.sleep(5)
    else:
        raise RuntimeError(f"Athena query {execution_id} timed out")

    if status != "SUCCEEDED":
        reason = exec_resp["QueryExecution"]["Status"].get("StateChangeReason", "unknown")
        raise RuntimeError(f"Athena query failed [{status}]: {reason}")

    # Paginate results and upsert into DynamoDB
    columns: list[str] = []
    rows_written = 0
    paginator_kwargs: dict[str, Any] = {"QueryExecutionId": execution_id}
    first_page = True

    while True:
        try:
            page = athena.get_query_results(**paginator_kwargs)
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to retrieve Athena results") from exc

        result_set = page.get("ResultSet", {})
        result_rows = result_set.get("Rows", [])

        if first_page and result_rows:
            columns = [c.get("VarCharValue", "") for c in result_rows[0].get("Data", [])]
            result_rows = result_rows[1:]
            first_page = False

        for row in result_rows:
            cells = [c.get("VarCharValue", "") for c in row.get("Data", [])]
            item: dict[str, Any] = {}
            for col, val in zip(columns, cells, strict=False):
                item[col] = {"S": val}
            # Rename the key column to "pk"
            if key_column in item:
                item["pk"] = item.pop(key_column)
            else:
                item["pk"] = {"S": str(rows_written)}
            try:
                ddb.put_item(TableName=table_name, Item=item)
            except ClientError as exc:
                raise wrap_aws_error(exc, f"Failed to upsert row into {table_name}") from exc
            rows_written += 1

        next_token = page.get("NextToken")
        if not next_token:
            break
        paginator_kwargs["NextToken"] = next_token

    return AthenaToDBResult(
        query_execution_id=execution_id,
        rows_written=rows_written,
        status=status,
    )


# ---------------------------------------------------------------------------
# 6. glue_crawler_and_catalog_sync
# ---------------------------------------------------------------------------


def glue_crawler_and_catalog_sync(
    crawler_name: str,
    table_name: str,
    reference_key: str,
    region_name: str | None = None,
) -> CrawlerSyncResult:
    """Start a Glue Crawler, wait for completion, and compare schema to DynamoDB reference.

    Starts the named Glue Crawler, polls until it completes, retrieves the
    tables it created or updated, serialises their schemas, and compares them
    against a reference schema stored in DynamoDB.  If differences are found
    the reference is updated.

    Args:
        crawler_name: Name of the Glue Crawler to run.
        table_name: DynamoDB table name storing the schema reference.
        reference_key: DynamoDB partition key value for the reference item.
        region_name: AWS region override.

    Returns:
        A :class:`CrawlerSyncResult` with crawler name, table count, schema
        changes, and whether the reference was updated.

    Raises:
        RuntimeError: If the crawler fails to start or encounters an error.
    """
    glue = get_client("glue", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    try:
        glue.start_crawler(Name=crawler_name)
    except ClientError as exc:
        if "CrawlerRunningException" not in str(exc):
            raise wrap_aws_error(exc, f"Failed to start crawler {crawler_name}") from exc

    terminal = {"READY", "STOPPING"}
    for _ in range(120):
        try:
            desc = glue.get_crawler(Name=crawler_name)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe crawler {crawler_name}") from exc
        crawler_state = desc.get("Crawler", {}).get("State", "")
        if crawler_state in terminal:
            break
        time.sleep(10)
    else:
        raise RuntimeError(f"Glue crawler {crawler_name} did not finish within timeout")

    # Get tables discovered by the crawler
    crawler_info = desc.get("Crawler", {})
    db_name = ""
    targets = crawler_info.get("Targets", {})
    targets.get("S3Targets", [])
    catalog_targets = targets.get("CatalogTargets", [])
    if catalog_targets:
        db_name = catalog_targets[0].get("DatabaseName", "")

    tables_found = 0
    current_schema: dict[str, Any] = {}

    if db_name:
        try:
            tables_resp = glue.get_tables(DatabaseName=db_name)
            table_list = tables_resp.get("TableList", [])
            tables_found = len(table_list)
            for tbl in table_list:
                tbl_name = tbl.get("Name", "")
                cols = [
                    {"name": c.get("Name"), "type": c.get("Type")}
                    for c in tbl.get("StorageDescriptor", {}).get("Columns", [])
                ]
                current_schema[tbl_name] = cols
        except ClientError as exc:
            logger.warning("Failed to list Glue tables: %s", exc)

    # Compare against DynamoDB reference
    schema_changes: list[str] = []
    reference_updated = False
    ref_item: dict[str, Any] = {}

    try:
        ref_resp = ddb.get_item(
            TableName=table_name,
            Key={"pk": {"S": reference_key}},
        )
        ref_item = ref_resp.get("Item", {})
        ref_schema = json.loads(ref_item.get("schema", {}).get("S", "{}"))
    except ClientError as exc:
        logger.warning("Failed to read schema reference from DynamoDB: %s", exc)
        ref_schema = {}

    for tbl, cols in current_schema.items():
        if tbl not in ref_schema:
            schema_changes.append(f"NEW TABLE: {tbl}")
        elif json.dumps(cols, sort_keys=True) != json.dumps(
            ref_schema.get(tbl, []), sort_keys=True
        ):
            schema_changes.append(f"SCHEMA CHANGED: {tbl}")

    for tbl in ref_schema:
        if tbl not in current_schema:
            schema_changes.append(f"TABLE DROPPED: {tbl}")

    if schema_changes or not ref_item:
        try:
            ddb.put_item(
                TableName=table_name,
                Item={
                    "pk": {"S": reference_key},
                    "schema": {"S": json.dumps(current_schema)},
                    "updated_at": {"N": str(int(time.time()))},
                    "crawler_name": {"S": crawler_name},
                },
            )
            reference_updated = True
        except ClientError as exc:
            logger.warning("Failed to update schema reference: %s", exc)

    return CrawlerSyncResult(
        crawler_name=crawler_name,
        tables_found=tables_found,
        schema_changes=schema_changes,
        reference_updated=reference_updated,
    )


# ---------------------------------------------------------------------------
# 7. glue_databrew_profile_pipeline
# ---------------------------------------------------------------------------


def glue_databrew_profile_pipeline(
    job_name: str,
    metric_namespace: str,
    region_name: str | None = None,
) -> DataBrewProfileResult:
    """Start a DataBrew profile job, wait for completion, publish stats to CloudWatch.

    Triggers the specified DataBrew profile job, polls until a terminal state
    is reached, extracts summary statistics from the job output, and publishes
    them as CloudWatch custom metrics.

    Args:
        job_name: Name of the DataBrew profile job to run.
        metric_namespace: CloudWatch metric namespace for publishing statistics.
        region_name: AWS region override.

    Returns:
        A :class:`DataBrewProfileResult` with run ID, status, metrics published,
        and optional dataset row count.

    Raises:
        RuntimeError: If the DataBrew job fails to start or encounters an error.
    """
    databrew = get_client("databrew", region_name=region_name)
    cw = get_client("cloudwatch", region_name=region_name)

    try:
        run_resp = databrew.start_job_run(Name=job_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start DataBrew job {job_name}") from exc

    run_id: str = run_resp["RunId"]

    terminal = {"SUCCEEDED", "FAILED", "STOPPED", "TIMEOUT"}
    status = "RUNNING"
    dataset_rows: int | None = None

    for _ in range(120):
        try:
            desc = databrew.describe_job_run(Name=job_name, RunId=run_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe DataBrew run {run_id}") from exc
        status = desc.get("State", status)
        if status in terminal:
            dataset_rows = desc.get("DatasetStatistics", {}).get("TotalNumberOfRows")
            break
        time.sleep(10)
    else:
        raise RuntimeError(f"DataBrew job {job_name} run {run_id} timed out")

    # Publish metrics to CloudWatch
    metrics_published = 0
    metric_data = [
        {
            "MetricName": "ProfileJobRun",
            "Dimensions": [{"Name": "JobName", "Value": job_name}],
            "Value": 1.0,
            "Unit": "Count",
        },
        {
            "MetricName": "ProfileJobSuccess",
            "Dimensions": [{"Name": "JobName", "Value": job_name}],
            "Value": 1.0 if status == "SUCCEEDED" else 0.0,
            "Unit": "Count",
        },
    ]
    if dataset_rows is not None:
        metric_data.append(
            {
                "MetricName": "DatasetRows",
                "Dimensions": [{"Name": "JobName", "Value": job_name}],
                "Value": float(dataset_rows),
                "Unit": "Count",
            }
        )

    try:
        cw.put_metric_data(Namespace=metric_namespace, MetricData=metric_data)
        metrics_published = len(metric_data)
    except ClientError as exc:
        logger.warning("Failed to publish CloudWatch metrics: %s", exc)

    return DataBrewProfileResult(
        run_id=run_id,
        status=status,
        metrics_published=metrics_published,
        dataset_rows=dataset_rows,
    )


# ---------------------------------------------------------------------------
# 8. emr_serverless_job_runner
# ---------------------------------------------------------------------------


def emr_serverless_job_runner(
    application_id: str,
    execution_role_arn: str,
    job_driver: dict[str, Any],
    table_name: str,
    metric_namespace: str,
    region_name: str | None = None,
) -> EMRJobResult:
    """Submit an EMR Serverless Spark job, push metrics, record manifest to DynamoDB.

    Starts a job run on an EMR Serverless application, polls until the job
    reaches a terminal state, publishes duration and status metrics to
    CloudWatch, and writes an output manifest record to DynamoDB.

    Args:
        application_id: EMR Serverless application ID.
        execution_role_arn: IAM role ARN for the job execution.
        job_driver: Job driver configuration dict (e.g. SparkSubmit parameters).
        table_name: DynamoDB table for the output manifest record.
        metric_namespace: CloudWatch metric namespace.
        region_name: AWS region override.

    Returns:
        An :class:`EMRJobResult` with job run ID, status, duration, and metrics count.

    Raises:
        RuntimeError: If the job submission or polling fails.
    """
    emr = get_client("emr-serverless", region_name=region_name)
    cw = get_client("cloudwatch", region_name=region_name)
    ddb = get_client("dynamodb", region_name=region_name)

    try:
        start_resp = emr.start_job_run(
            applicationId=application_id,
            executionRoleArn=execution_role_arn,
            jobDriver=job_driver,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to start EMR Serverless job on {application_id}"
        ) from exc

    job_run_id: str = start_resp["jobRunId"]
    start_ts = time.time()

    terminal = {"SUCCESS", "FAILED", "CANCELLING", "CANCELLED"}
    status = "PENDING"

    for _ in range(180):
        try:
            desc = emr.get_job_run(applicationId=application_id, jobRunId=job_run_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe EMR job run {job_run_id}") from exc
        status = desc.get("jobRun", {}).get("state", status)
        if status in terminal:
            break
        time.sleep(10)
    else:
        raise RuntimeError(f"EMR Serverless job {job_run_id} timed out")

    duration = round(time.time() - start_ts, 2)

    # Publish CloudWatch metrics
    metrics_published = 0
    try:
        cw.put_metric_data(
            Namespace=metric_namespace,
            MetricData=[
                {
                    "MetricName": "EMRServerlessJobDuration",
                    "Dimensions": [{"Name": "ApplicationId", "Value": application_id}],
                    "Value": duration,
                    "Unit": "Seconds",
                },
                {
                    "MetricName": "EMRServerlessJobSuccess",
                    "Dimensions": [{"Name": "ApplicationId", "Value": application_id}],
                    "Value": 1.0 if status == "SUCCESS" else 0.0,
                    "Unit": "Count",
                },
            ],
        )
        metrics_published = 2
    except ClientError as exc:
        logger.warning("Failed to publish EMR CloudWatch metrics: %s", exc)

    # Write manifest to DynamoDB
    try:
        ddb.put_item(
            TableName=table_name,
            Item={
                "pk": {"S": f"emr-job#{job_run_id}"},
                "application_id": {"S": application_id},
                "status": {"S": status},
                "duration_seconds": {"N": str(duration)},
                "completed_at": {"N": str(int(time.time()))},
            },
        )
    except ClientError as exc:
        logger.warning("Failed to write EMR job manifest to DynamoDB: %s", exc)

    return EMRJobResult(
        job_run_id=job_run_id,
        status=status,
        duration_seconds=duration,
        metrics_published=metrics_published,
    )


# ---------------------------------------------------------------------------
# 9. timestream_query_to_s3
# ---------------------------------------------------------------------------


def timestream_query_to_s3(
    query_string: str,
    bucket: str,
    output_key: str,
    region_name: str | None = None,
) -> TimestreamExportResult:
    """Execute a Timestream query, paginate results, and write CSV to S3.

    Runs the provided Timestream Query SQL, iterates through all result pages,
    serialises all rows as CSV, and writes the file to S3.

    Args:
        query_string: Timestream SQL query to execute.
        bucket: S3 bucket for the CSV output.
        output_key: S3 object key for the output CSV file.
        region_name: AWS region override.

    Returns:
        A :class:`TimestreamExportResult` with row count, S3 key, and column names.

    Raises:
        RuntimeError: If the Timestream query or S3 write fails.
    """
    ts_query = get_client("timestream-query", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)

    column_names: list[str] = []
    rows: list[list[str]] = []
    first_page = True
    paginator_kwargs: dict[str, Any] = {"QueryString": query_string}

    while True:
        try:
            page = ts_query.query(**paginator_kwargs)
        except ClientError as exc:
            raise wrap_aws_error(exc, "Timestream query failed") from exc

        if first_page:
            column_names = [c["Name"] for c in page.get("ColumnInfo", [])]
            first_page = False

        for row in page.get("Rows", []):
            cells = [next(iter(d.values()), "") if d else "" for d in row.get("Data", [])]
            rows.append([str(c) for c in cells])

        next_token = page.get("NextToken")
        if not next_token:
            break
        paginator_kwargs["NextToken"] = next_token

    # Serialise to CSV
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(column_names)
    writer.writerows(rows)
    csv_bytes = buf.getvalue().encode("utf-8")

    try:
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=csv_bytes,
            ContentType="text/csv",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to write CSV to s3://{bucket}/{output_key}") from exc

    return TimestreamExportResult(
        row_count=len(rows),
        s3_key=output_key,
        column_names=column_names,
    )


# ---------------------------------------------------------------------------
# 10. neptune_graph_query_to_s3
# ---------------------------------------------------------------------------


def neptune_graph_query_to_s3(
    graph_identifier: str,
    query_string: str,
    language: str,
    bucket: str,
    output_key: str,
    region_name: str | None = None,
) -> NeptuneQueryResult:
    """Run a Neptune Analytics graph query and write results as JSON to S3.

    Executes the provided query against a Neptune Analytics graph using
    ``executeQuery``, collects all results, serialises them to JSON, and
    writes the output to S3.

    Args:
        graph_identifier: Neptune Analytics graph identifier.
        query_string: Graph query string (openCypher or NQUAD).
        language: Query language — ``"OPEN_CYPHER"`` or ``"NQUAD"``.
        bucket: S3 bucket for the JSON output.
        output_key: S3 object key for the JSON file.
        region_name: AWS region override.

    Returns:
        A :class:`NeptuneQueryResult` with result count and S3 key.

    Raises:
        RuntimeError: If the Neptune or S3 call fails.
    """
    neptune = get_client("neptune-graph", region_name=region_name)
    s3 = get_client("s3", region_name=region_name)

    try:
        resp = neptune.execute_query(
            graphIdentifier=graph_identifier,
            queryString=query_string,
            language=language,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Neptune graph query failed on {graph_identifier}") from exc

    # The response payload is a streaming body containing JSON
    raw = resp.get("payload", b"")
    if hasattr(raw, "read"):
        raw = raw.read()

    try:
        results = json.loads(raw) if raw else []
    except (ValueError, TypeError):
        results = []

    if isinstance(results, dict):
        results = results.get("results", [results])

    result_count = len(results) if isinstance(results, list) else 1

    try:
        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=json.dumps(results, default=str).encode("utf-8"),
            ContentType="application/json",
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"Failed to write Neptune results to s3://{bucket}/{output_key}"
        ) from exc

    return NeptuneQueryResult(
        result_count=result_count,
        s3_key=output_key,
    )


# ---------------------------------------------------------------------------
# 11. elbv2_access_log_analyzer
# ---------------------------------------------------------------------------


def elbv2_access_log_analyzer(
    load_balancer_arn: str,
    bucket: str,
    log_prefix: str,
    athena_database: str,
    athena_output_location: str,
    region_name: str | None = None,
) -> AccessLogAnalysis:
    """Enable ELBv2 access logging, create Athena table, run top-error-codes query.

    Enables access logging on the specified load balancer (if not already
    enabled), creates an Athena table over the log S3 location if it does not
    exist, and runs a query to identify the top HTTP error codes in the logs.

    Args:
        load_balancer_arn: ARN of the Application or Network Load Balancer.
        bucket: S3 bucket where access logs are (or will be) stored.
        log_prefix: S3 key prefix for the access log objects.
        athena_database: Athena/Glue database for the log table.
        athena_output_location: S3 path for Athena query results.
        region_name: AWS region override.

    Returns:
        An :class:`AccessLogAnalysis` with logging status, table creation flag,
        query execution ID, and top error codes.

    Raises:
        RuntimeError: If attribute modification or Athena queries fail.
    """
    elbv2 = get_client("elbv2", region_name=region_name)
    athena = get_client("athena", region_name=region_name)

    # Check / enable access logging
    logging_enabled = False
    try:
        attrs_resp = elbv2.describe_load_balancer_attributes(LoadBalancerArn=load_balancer_arn)
        attrs = {a["Key"]: a["Value"] for a in attrs_resp.get("Attributes", [])}
        if attrs.get("access_logs.s3.enabled") == "true":
            logging_enabled = True
        else:
            elbv2.modify_load_balancer_attributes(
                LoadBalancerArn=load_balancer_arn,
                Attributes=[
                    {"Key": "access_logs.s3.enabled", "Value": "true"},
                    {"Key": "access_logs.s3.bucket", "Value": bucket},
                    {"Key": "access_logs.s3.prefix", "Value": log_prefix},
                ],
            )
            logging_enabled = True
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to configure ELBv2 access logging") from exc

    # Create Athena table
    athena_table_created = False
    lb_id = load_balancer_arn.split("/")[-1]
    table_ddl = f"""
    CREATE EXTERNAL TABLE IF NOT EXISTS {athena_database}.elb_logs_{lb_id} (
        type STRING, time STRING, elb STRING, client_ip STRING,
        client_port INT, target_ip STRING, target_port INT,
        request_processing_time DOUBLE, target_processing_time DOUBLE,
        response_processing_time DOUBLE, elb_status_code INT,
        target_status_code INT, received_bytes BIGINT, sent_bytes BIGINT,
        request STRING, user_agent STRING, ssl_cipher STRING,
        ssl_protocol STRING, target_group_arn STRING,
        trace_id STRING, domain_name STRING, chosen_cert_arn STRING,
        matched_rule_priority INT, request_creation_time STRING,
        actions_executed STRING, redirect_url STRING,
        lambda_error_reason STRING, target_port_list STRING,
        target_status_code_list STRING, classification STRING,
        classification_reason STRING
    )
    ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
    WITH SERDEPROPERTIES ('serialization.format' = '1',
        'input.regex' = '([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*):([0-9]*) ([^ ]*)[:-]([0-9]*) ([-.0-9]*) ([-.0-9]*) ([-.0-9]*) (|[-0-9]*) (-|[-0-9]*) ([-0-9]*) ([-0-9]*) \"([^ ]*) (.*) (- |[^ ]*)\" \"([^\"]*)\" ([A-Z0-9-_]+) ([A-Za-z0-9.-]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^\"]*)\" ([-.0-9]*) ([^ ]*) \"([^\"]*)\" \"([^\"]*)\" \"([^ ]*)\" \"([^\\s]+?)\" \"([^\\s]+)\" \"([^ ]*)\" \"([^ ]*)\"')
    LOCATION 's3://{bucket}/{log_prefix}/'
    """

    try:
        athena.start_query_execution(
            QueryString=table_ddl,
            QueryExecutionContext={"Database": athena_database},
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        athena_table_created = True
    except ClientError as exc:
        logger.warning("Failed to create Athena ELB log table: %s", exc)

    # Run top error codes query
    error_query = (
        f"SELECT elb_status_code, COUNT(*) AS count "
        f"FROM {athena_database}.elb_logs_{lb_id} "
        f"WHERE elb_status_code >= 400 "
        f"GROUP BY elb_status_code ORDER BY count DESC LIMIT 10"
    )

    try:
        exec_resp = athena.start_query_execution(
            QueryString=error_query,
            QueryExecutionContext={"Database": athena_database},
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start Athena error codes query") from exc

    query_execution_id: str = exec_resp["QueryExecutionId"]

    # Poll for the error query
    terminal = {"SUCCEEDED", "FAILED", "CANCELLED"}
    for _ in range(30):
        try:
            qexec = athena.get_query_execution(QueryExecutionId=query_execution_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, "Failed to poll Athena query") from exc
        qstate = qexec["QueryExecution"]["Status"]["State"]
        if qstate in terminal:
            break
        time.sleep(5)

    top_errors: list[dict[str, Any]] = []
    if qstate == "SUCCEEDED":
        try:
            results = athena.get_query_results(QueryExecutionId=query_execution_id)
            rows = results.get("ResultSet", {}).get("Rows", [])
            # Skip header row
            for row in rows[1:]:
                cells = [c.get("VarCharValue", "") for c in row.get("Data", [])]
                if len(cells) >= 2:
                    top_errors.append({"status_code": cells[0], "count": cells[1]})
        except ClientError as exc:
            logger.warning("Failed to retrieve Athena error query results: %s", exc)

    return AccessLogAnalysis(
        logging_enabled=logging_enabled,
        athena_table_created=athena_table_created,
        query_execution_id=query_execution_id,
        top_errors=top_errors,
    )


# ---------------------------------------------------------------------------
# 12. glue_job_output_to_redshift
# ---------------------------------------------------------------------------


def glue_job_output_to_redshift(
    job_name: str,
    job_arguments: dict[str, str],
    workgroup_name: str,
    database: str,
    target_table: str,
    iam_role_arn: str,
    s3_output_path: str,
    region_name: str | None = None,
) -> GlueToRedshiftResult:
    """Run a Glue ETL job, wait, then COPY output into Redshift Serverless.

    Starts the named Glue ETL job with the provided arguments, polls until
    completion, then executes a Redshift ``COPY`` statement via the Data API
    to load the output from S3 into the target Redshift table.

    Args:
        job_name: Name of the Glue ETL job.
        job_arguments: Dictionary of Glue job arguments (``--key: value`` pairs).
        workgroup_name: Redshift Serverless workgroup name.
        database: Redshift database for the COPY statement.
        target_table: Redshift target table to load.
        iam_role_arn: IAM role ARN for the COPY command.
        s3_output_path: S3 path where the Glue job writes its output.
        region_name: AWS region override.

    Returns:
        A :class:`GlueToRedshiftResult` with Glue run ID, Glue status,
        COPY statement ID, and COPY status.

    Raises:
        RuntimeError: If the Glue job or Redshift COPY fails.
    """
    glue = get_client("glue", region_name=region_name)
    redshift_data = get_client("redshift-data", region_name=region_name)

    try:
        run_resp = glue.start_job_run(JobName=job_name, Arguments=job_arguments)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to start Glue job {job_name}") from exc

    job_run_id: str = run_resp["JobRunId"]

    terminal_glue = {"SUCCEEDED", "FAILED", "STOPPED", "TIMEOUT", "ERROR"}
    glue_status = "STARTING"

    for _ in range(120):
        try:
            desc = glue.get_job_run(JobName=job_name, RunId=job_run_id)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"Failed to describe Glue run {job_run_id}") from exc
        glue_status = desc.get("JobRun", {}).get("JobRunState", glue_status)
        if glue_status in terminal_glue:
            break
        time.sleep(15)
    else:
        raise RuntimeError(f"Glue job {job_name} run {job_run_id} timed out")

    if glue_status != "SUCCEEDED":
        raise RuntimeError(f"Glue job {job_name} failed with status: {glue_status}")

    # COPY into Redshift
    copy_sql = (
        f"COPY {target_table} FROM '{s3_output_path}' IAM_ROLE '{iam_role_arn}' FORMAT AS PARQUET"
    )

    try:
        copy_resp = redshift_data.execute_statement(
            WorkgroupName=workgroup_name,
            Database=database,
            Sql=copy_sql,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"Failed to submit Redshift COPY for {target_table}") from exc

    copy_statement_id: str = copy_resp["Id"]

    terminal_rs = {"FINISHED", "FAILED", "ABORTED"}
    copy_status = "STARTED"

    for _ in range(60):
        try:
            copy_desc = redshift_data.describe_statement(Id=copy_statement_id)
        except ClientError as exc:
            raise wrap_aws_error(
                exc, f"Failed to describe COPY statement {copy_statement_id}"
            ) from exc
        copy_status = copy_desc.get("Status", copy_status)
        if copy_status in terminal_rs:
            break
        time.sleep(5)
    else:
        raise RuntimeError(f"Redshift COPY statement {copy_statement_id} timed out")

    return GlueToRedshiftResult(
        job_run_id=job_run_id,
        glue_status=glue_status,
        copy_statement_id=copy_statement_id,
        copy_status=copy_status,
    )


# ---------------------------------------------------------------------------
# 13. opensearch_index_lifecycle_manager
# ---------------------------------------------------------------------------


def opensearch_index_lifecycle_manager(
    collection_names: list[str],
    metric_namespace: str,
    region_name: str | None = None,
) -> IndexLifecycleResult:
    """Check OpenSearch Serverless collection status and publish metrics to CloudWatch.

    Retrieves the status of each specified OpenSearch Serverless collection,
    counts active collections, and publishes summary statistics as CloudWatch
    custom metrics.

    Args:
        collection_names: List of OpenSearch Serverless collection names to check.
        metric_namespace: CloudWatch metric namespace for publishing statistics.
        region_name: AWS region override.

    Returns:
        An :class:`IndexLifecycleResult` with collections checked, active count,
        and metrics published.

    Raises:
        RuntimeError: If the OpenSearch Serverless or CloudWatch API calls fail.
    """
    oss = get_client("opensearchserverless", region_name=region_name)
    cw = get_client("cloudwatch", region_name=region_name)

    collections_checked = 0
    active_collections = 0

    try:
        resp = oss.batch_get_collection(names=collection_names)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe OpenSearch Serverless collections") from exc

    collection_details = resp.get("collectionDetails", [])
    collections_checked = len(collection_details)

    for col in collection_details:
        col_status = col.get("status", "")
        if col_status == "ACTIVE":
            active_collections += 1

    # Publish metrics
    metrics_published = 0
    metric_data = [
        {
            "MetricName": "CollectionsChecked",
            "Dimensions": [{"Name": "Namespace", "Value": metric_namespace}],
            "Value": float(collections_checked),
            "Unit": "Count",
        },
        {
            "MetricName": "ActiveCollections",
            "Dimensions": [{"Name": "Namespace", "Value": metric_namespace}],
            "Value": float(active_collections),
            "Unit": "Count",
        },
        {
            "MetricName": "InactiveCollections",
            "Dimensions": [{"Name": "Namespace", "Value": metric_namespace}],
            "Value": float(collections_checked - active_collections),
            "Unit": "Count",
        },
    ]

    try:
        cw.put_metric_data(Namespace=metric_namespace, MetricData=metric_data)
        metrics_published = len(metric_data)
    except ClientError as exc:
        logger.warning("Failed to publish OpenSearch lifecycle metrics: %s", exc)

    return IndexLifecycleResult(
        collections_checked=collections_checked,
        active_collections=active_collections,
        metrics_published=metrics_published,
    )
