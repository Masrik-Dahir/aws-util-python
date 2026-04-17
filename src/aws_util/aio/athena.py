"""Native async Athena utilities using the async engine."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.athena import (
    AthenaExecution,
    BatchGetNamedQueryResult,
    BatchGetPreparedStatementResult,
    BatchGetQueryExecutionResult,
    CreateDataCatalogResult,
    CreateNamedQueryResult,
    CreateNotebookResult,
    CreatePresignedNotebookUrlResult,
    DeleteDataCatalogResult,
    ExportNotebookResult,
    GetCalculationExecutionCodeResult,
    GetCalculationExecutionResult,
    GetCalculationExecutionStatusResult,
    GetCapacityAssignmentConfigurationResult,
    GetCapacityReservationResult,
    GetDatabaseResult,
    GetDataCatalogResult,
    GetNamedQueryResult,
    GetNotebookMetadataResult,
    GetPreparedStatementResult,
    GetQueryRuntimeStatisticsResult,
    GetSessionResult,
    GetSessionStatusResult,
    GetTableMetadataResult,
    GetWorkGroupResult,
    ImportNotebookResult,
    ListApplicationDpuSizesResult,
    ListCalculationExecutionsResult,
    ListCapacityReservationsResult,
    ListDatabasesResult,
    ListDataCatalogsResult,
    ListEngineVersionsResult,
    ListExecutorsResult,
    ListNamedQueriesResult,
    ListNotebookMetadataResult,
    ListNotebookSessionsResult,
    ListPreparedStatementsResult,
    ListQueryExecutionsResult,
    ListSessionsResult,
    ListTableMetadataResult,
    ListTagsForResourceResult,
    ListWorkGroupsResult,
    StartCalculationExecutionResult,
    StartQueryExecutionResult,
    StartSessionResult,
    StopCalculationExecutionResult,
    TerminateSessionResult,
)
from aws_util.exceptions import AwsServiceError, wrap_aws_error

_TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "CANCELLED"}

__all__ = [
    "AthenaExecution",
    "BatchGetNamedQueryResult",
    "BatchGetPreparedStatementResult",
    "BatchGetQueryExecutionResult",
    "CreateDataCatalogResult",
    "CreateNamedQueryResult",
    "CreateNotebookResult",
    "CreatePresignedNotebookUrlResult",
    "DeleteDataCatalogResult",
    "ExportNotebookResult",
    "GetCalculationExecutionCodeResult",
    "GetCalculationExecutionResult",
    "GetCalculationExecutionStatusResult",
    "GetCapacityAssignmentConfigurationResult",
    "GetCapacityReservationResult",
    "GetDataCatalogResult",
    "GetDatabaseResult",
    "GetNamedQueryResult",
    "GetNotebookMetadataResult",
    "GetPreparedStatementResult",
    "GetQueryRuntimeStatisticsResult",
    "GetSessionResult",
    "GetSessionStatusResult",
    "GetTableMetadataResult",
    "GetWorkGroupResult",
    "ImportNotebookResult",
    "ListApplicationDpuSizesResult",
    "ListCalculationExecutionsResult",
    "ListCapacityReservationsResult",
    "ListDataCatalogsResult",
    "ListDatabasesResult",
    "ListEngineVersionsResult",
    "ListExecutorsResult",
    "ListNamedQueriesResult",
    "ListNotebookMetadataResult",
    "ListNotebookSessionsResult",
    "ListPreparedStatementsResult",
    "ListQueryExecutionsResult",
    "ListSessionsResult",
    "ListTableMetadataResult",
    "ListTagsForResourceResult",
    "ListWorkGroupsResult",
    "StartCalculationExecutionResult",
    "StartQueryExecutionResult",
    "StartSessionResult",
    "StopCalculationExecutionResult",
    "TerminateSessionResult",
    "batch_get_named_query",
    "batch_get_prepared_statement",
    "batch_get_query_execution",
    "cancel_capacity_reservation",
    "create_capacity_reservation",
    "create_data_catalog",
    "create_named_query",
    "create_notebook",
    "create_prepared_statement",
    "create_presigned_notebook_url",
    "create_work_group",
    "delete_capacity_reservation",
    "delete_data_catalog",
    "delete_named_query",
    "delete_notebook",
    "delete_prepared_statement",
    "delete_work_group",
    "export_notebook",
    "get_calculation_execution",
    "get_calculation_execution_code",
    "get_calculation_execution_status",
    "get_capacity_assignment_configuration",
    "get_capacity_reservation",
    "get_data_catalog",
    "get_database",
    "get_named_query",
    "get_notebook_metadata",
    "get_prepared_statement",
    "get_query_execution",
    "get_query_results",
    "get_query_runtime_statistics",
    "get_session",
    "get_session_status",
    "get_table_metadata",
    "get_table_schema",
    "get_work_group",
    "import_notebook",
    "list_application_dpu_sizes",
    "list_calculation_executions",
    "list_capacity_reservations",
    "list_data_catalogs",
    "list_databases",
    "list_engine_versions",
    "list_executors",
    "list_named_queries",
    "list_notebook_metadata",
    "list_notebook_sessions",
    "list_prepared_statements",
    "list_query_executions",
    "list_sessions",
    "list_table_metadata",
    "list_tags_for_resource",
    "list_work_groups",
    "put_capacity_assignment_configuration",
    "run_ddl",
    "run_query",
    "start_calculation_execution",
    "start_query",
    "start_query_execution",
    "start_session",
    "stop_calculation_execution",
    "stop_query",
    "stop_query_execution",
    "tag_resource",
    "terminate_session",
    "untag_resource",
    "update_capacity_reservation",
    "update_data_catalog",
    "update_named_query",
    "update_notebook",
    "update_notebook_metadata",
    "update_prepared_statement",
    "update_work_group",
    "wait_for_query",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_execution(ex: dict) -> AthenaExecution:
    """Convert a raw API execution dict to an :class:`AthenaExecution`."""
    status = ex.get("Status", {})
    stats = ex.get("Statistics", {})
    ctx = ex.get("QueryExecutionContext", {})
    config = ex.get("ResultConfiguration", {})
    return AthenaExecution(
        query_execution_id=ex["QueryExecutionId"],
        query=ex.get("Query", ""),
        state=status.get("State", "UNKNOWN"),
        state_change_reason=status.get("StateChangeReason"),
        database=ctx.get("Database"),
        output_location=config.get("OutputLocation"),
        submission_date_time=status.get("SubmissionDateTime"),
        completion_date_time=status.get("CompletionDateTime"),
        data_scanned_bytes=stats.get("DataScannedInBytes"),
        engine_execution_time_ms=stats.get("EngineExecutionTimeInMillis"),
    )


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def start_query(
    query: str,
    database: str,
    output_location: str,
    workgroup: str = "primary",
    region_name: str | None = None,
) -> str:
    """Submit an Athena SQL query for asynchronous execution.

    Args:
        query: SQL query string.
        database: Glue Data Catalog database to query against.
        output_location: S3 URI where query results are stored, e.g.
            ``"s3://my-bucket/athena-results/"``.
        workgroup: Athena workgroup (default ``"primary"``).
        region_name: AWS region override.

    Returns:
        The query execution ID.

    Raises:
        RuntimeError: If the query submission fails.
    """
    client = async_client("athena", region_name)
    try:
        resp = await client.call(
            "StartQueryExecution",
            QueryString=query,
            QueryExecutionContext={"Database": database},
            ResultConfiguration={"OutputLocation": output_location},
            WorkGroup=workgroup,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "Failed to start Athena query") from exc
    return resp["QueryExecutionId"]


async def get_query_execution(
    query_execution_id: str,
    region_name: str | None = None,
) -> AthenaExecution:
    """Fetch the current status and metadata of an Athena query.

    Args:
        query_execution_id: ID returned by :func:`start_query`.
        region_name: AWS region override.

    Returns:
        An :class:`AthenaExecution` with current state and statistics.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    try:
        resp = await client.call(
            "GetQueryExecution",
            QueryExecutionId=query_execution_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_query_execution failed for {query_execution_id!r}") from exc
    return _parse_execution(resp["QueryExecution"])


async def get_query_results(
    query_execution_id: str,
    max_rows: int | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Fetch the results of a completed Athena query as a list of dicts.

    Column names are used as dict keys.  Handles pagination automatically.

    Args:
        query_execution_id: ID of a completed query execution.
        max_rows: Maximum number of result rows to return.  ``None`` returns
            all rows.
        region_name: AWS region override.

    Returns:
        A list of row dicts mapping column name -> string value.

    Raises:
        RuntimeError: If the result fetch fails.
    """
    client = async_client("athena", region_name)
    rows: list[dict[str, Any]] = []
    column_names: list[str] = []
    first_page = True
    kwargs: dict[str, Any] = {
        "QueryExecutionId": query_execution_id,
    }
    try:
        while True:
            resp = await client.call("GetQueryResults", **kwargs)
            result_rows = resp["ResultSet"]["Rows"]
            if first_page:
                column_names = [col["VarCharValue"] for col in result_rows[0]["Data"]]
                result_rows = result_rows[1:]  # skip header row
                first_page = False
            for row in result_rows:
                row_dict = {
                    column_names[i]: cell.get("VarCharValue", "")
                    for i, cell in enumerate(row["Data"])
                }
                rows.append(row_dict)
                if max_rows is not None and len(rows) >= max_rows:
                    return rows
            next_token = resp.get("NextToken")
            if not next_token:
                break
            kwargs["NextToken"] = next_token
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_query_results failed for {query_execution_id!r}") from exc
    return rows


async def wait_for_query(
    query_execution_id: str,
    poll_interval: float = 3.0,
    timeout: float = 300.0,
    region_name: str | None = None,
) -> AthenaExecution:
    """Poll until an Athena query reaches a terminal state.

    Args:
        query_execution_id: ID of the query execution to wait for.
        poll_interval: Seconds between status checks (default ``3``).
        timeout: Maximum seconds to wait (default ``300`` / 5 min).
        region_name: AWS region override.

    Returns:
        The final :class:`AthenaExecution`.

    Raises:
        TimeoutError: If the query does not finish within *timeout*.
    """
    deadline = time.monotonic() + timeout
    while True:
        execution = await get_query_execution(query_execution_id, region_name=region_name)
        if execution.finished:
            return execution
        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"Athena query {query_execution_id!r} did not finish within {timeout}s"
            )
        await asyncio.sleep(poll_interval)


async def run_query(
    query: str,
    database: str,
    output_location: str,
    workgroup: str = "primary",
    poll_interval: float = 3.0,
    timeout: float = 300.0,
    max_rows: int | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Submit a query, wait for completion, and return results in one call.

    Combines :func:`start_query`, :func:`wait_for_query`, and
    :func:`get_query_results`.

    Args:
        query: SQL query string.
        database: Glue Data Catalog database.
        output_location: S3 result destination URI.
        workgroup: Athena workgroup.
        poll_interval: Seconds between status checks.
        timeout: Maximum seconds to wait for completion.
        max_rows: Maximum result rows to return.
        region_name: AWS region override.

    Returns:
        A list of row dicts mapping column name -> value.

    Raises:
        RuntimeError: If the query fails or is cancelled.
        TimeoutError: If the query does not complete within *timeout*.
    """
    execution_id = await start_query(
        query,
        database,
        output_location,
        workgroup,
        region_name=region_name,
    )
    execution = await wait_for_query(
        execution_id,
        poll_interval=poll_interval,
        timeout=timeout,
        region_name=region_name,
    )
    if not execution.succeeded:
        raise AwsServiceError(
            f"Athena query {execution_id!r} finished with state "
            f"{execution.state!r}: {execution.state_change_reason}"
        )
    return await get_query_results(execution_id, max_rows=max_rows, region_name=region_name)


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def get_table_schema(
    database: str,
    table_name: str,
    output_location: str,
    workgroup: str = "primary",
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """Return the column schema for an Athena/Glue table.

    Runs ``DESCRIBE <table>`` and parses the result into a list of column
    dicts.

    Args:
        database: Glue Data Catalog database containing the table.
        table_name: Table name.
        output_location: S3 URI for Athena query results.
        workgroup: Athena workgroup (default ``"primary"``).
        region_name: AWS region override.

    Returns:
        A list of dicts with ``"name"`` and ``"type"`` keys for each column.

    Raises:
        RuntimeError: If the query fails.
    """
    rows = await run_query(
        query=f"DESCRIBE `{table_name}`",
        database=database,
        output_location=output_location,
        workgroup=workgroup,
        region_name=region_name,
    )
    schema: list[dict[str, str]] = []
    for row in rows:
        values = list(row.values())
        if len(values) >= 2 and values[0] and not values[0].startswith("#"):
            schema.append({"name": values[0].strip(), "type": values[1].strip()})
    return schema


async def run_ddl(
    statement: str,
    database: str,
    output_location: str,
    workgroup: str = "primary",
    timeout: float = 300.0,
    region_name: str | None = None,
) -> AthenaExecution:
    """Execute a DDL statement (``CREATE``, ``DROP``, ``ALTER``) in Athena.

    Submits the statement, waits for completion, and returns the final
    execution state.  Raises if the statement fails.

    Args:
        statement: DDL SQL string.
        database: Glue Data Catalog database context.
        output_location: S3 URI for Athena output.
        workgroup: Athena workgroup (default ``"primary"``).
        timeout: Maximum seconds to wait (default ``300``).
        region_name: AWS region override.

    Returns:
        The final :class:`AthenaExecution` after the DDL completes.

    Raises:
        RuntimeError: If the DDL fails or is cancelled.
        TimeoutError: If the DDL does not complete within *timeout*.
    """
    execution_id = await start_query(
        statement,
        database,
        output_location,
        workgroup,
        region_name=region_name,
    )
    execution = await wait_for_query(execution_id, timeout=timeout, region_name=region_name)
    if not execution.succeeded:
        raise AwsServiceError(
            f"DDL statement failed with state {execution.state!r}: {execution.state_change_reason}"
        )
    return execution


async def stop_query(
    query_execution_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel a running Athena query.

    Args:
        query_execution_id: ID of the query to cancel.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the cancellation fails.
    """
    client = async_client("athena", region_name)
    try:
        await client.call(
            "StopQueryExecution",
            QueryExecutionId=query_execution_id,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"stop_query failed for {query_execution_id!r}") from exc


async def batch_get_named_query(
    named_query_ids: list[str],
    region_name: str | None = None,
) -> BatchGetNamedQueryResult:
    """Batch get named query.

    Args:
        named_query_ids: Named query ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamedQueryIds"] = named_query_ids
    try:
        resp = await client.call("BatchGetNamedQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get named query") from exc
    return BatchGetNamedQueryResult(
        named_queries=resp.get("NamedQueries"),
        unprocessed_named_query_ids=resp.get("UnprocessedNamedQueryIds"),
    )


async def batch_get_prepared_statement(
    prepared_statement_names: list[str],
    work_group: str,
    region_name: str | None = None,
) -> BatchGetPreparedStatementResult:
    """Batch get prepared statement.

    Args:
        prepared_statement_names: Prepared statement names.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["PreparedStatementNames"] = prepared_statement_names
    kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("BatchGetPreparedStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get prepared statement") from exc
    return BatchGetPreparedStatementResult(
        prepared_statements=resp.get("PreparedStatements"),
        unprocessed_prepared_statement_names=resp.get("UnprocessedPreparedStatementNames"),
    )


async def batch_get_query_execution(
    query_execution_ids: list[str],
    region_name: str | None = None,
) -> BatchGetQueryExecutionResult:
    """Batch get query execution.

    Args:
        query_execution_ids: Query execution ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryExecutionIds"] = query_execution_ids
    try:
        resp = await client.call("BatchGetQueryExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch get query execution") from exc
    return BatchGetQueryExecutionResult(
        query_executions=resp.get("QueryExecutions"),
        unprocessed_query_execution_ids=resp.get("UnprocessedQueryExecutionIds"),
    )


async def cancel_capacity_reservation(
    name: str,
    region_name: str | None = None,
) -> None:
    """Cancel capacity reservation.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("CancelCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to cancel capacity reservation") from exc
    return None


async def create_capacity_reservation(
    target_dpus: int,
    name: str,
    *,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Create capacity reservation.

    Args:
        target_dpus: Target dpus.
        name: Name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetDpus"] = target_dpus
    kwargs["Name"] = name
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create capacity reservation") from exc
    return None


async def create_data_catalog(
    name: str,
    type_value: str,
    *,
    description: str | None = None,
    parameters: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> CreateDataCatalogResult:
    """Create data catalog.

    Args:
        name: Name.
        type_value: Type value.
        description: Description.
        parameters: Parameters.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Type"] = type_value
    if description is not None:
        kwargs["Description"] = description
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDataCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create data catalog") from exc
    return CreateDataCatalogResult(
        data_catalog=resp.get("DataCatalog"),
    )


async def create_named_query(
    name: str,
    database: str,
    query_string: str,
    *,
    description: str | None = None,
    client_request_token: str | None = None,
    work_group: str | None = None,
    region_name: str | None = None,
) -> CreateNamedQueryResult:
    """Create named query.

    Args:
        name: Name.
        database: Database.
        query_string: Query string.
        description: Description.
        client_request_token: Client request token.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Database"] = database
    kwargs["QueryString"] = query_string
    if description is not None:
        kwargs["Description"] = description
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("CreateNamedQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create named query") from exc
    return CreateNamedQueryResult(
        named_query_id=resp.get("NamedQueryId"),
    )


async def create_notebook(
    work_group: str,
    name: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> CreateNotebookResult:
    """Create notebook.

    Args:
        work_group: Work group.
        name: Name.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    kwargs["Name"] = name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = await client.call("CreateNotebook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create notebook") from exc
    return CreateNotebookResult(
        notebook_id=resp.get("NotebookId"),
    )


async def create_prepared_statement(
    statement_name: str,
    work_group: str,
    query_statement: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Create prepared statement.

    Args:
        statement_name: Statement name.
        work_group: Work group.
        query_statement: Query statement.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StatementName"] = statement_name
    kwargs["WorkGroup"] = work_group
    kwargs["QueryStatement"] = query_statement
    if description is not None:
        kwargs["Description"] = description
    try:
        await client.call("CreatePreparedStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create prepared statement") from exc
    return None


async def create_presigned_notebook_url(
    session_id: str,
    region_name: str | None = None,
) -> CreatePresignedNotebookUrlResult:
    """Create presigned notebook url.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = await client.call("CreatePresignedNotebookUrl", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create presigned notebook url") from exc
    return CreatePresignedNotebookUrlResult(
        notebook_url=resp.get("NotebookUrl"),
        auth_token=resp.get("AuthToken"),
        auth_token_expiration_time=resp.get("AuthTokenExpirationTime"),
    )


async def create_work_group(
    name: str,
    *,
    configuration: dict[str, Any] | None = None,
    description: str | None = None,
    tags: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> None:
    """Create work group.

    Args:
        name: Name.
        configuration: Configuration.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if configuration is not None:
        kwargs["Configuration"] = configuration
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        await client.call("CreateWorkGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create work group") from exc
    return None


async def delete_capacity_reservation(
    name: str,
    region_name: str | None = None,
) -> None:
    """Delete capacity reservation.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        await client.call("DeleteCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete capacity reservation") from exc
    return None


async def delete_data_catalog(
    name: str,
    *,
    delete_catalog_only: bool | None = None,
    region_name: str | None = None,
) -> DeleteDataCatalogResult:
    """Delete data catalog.

    Args:
        name: Name.
        delete_catalog_only: Delete catalog only.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if delete_catalog_only is not None:
        kwargs["DeleteCatalogOnly"] = delete_catalog_only
    try:
        resp = await client.call("DeleteDataCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete data catalog") from exc
    return DeleteDataCatalogResult(
        data_catalog=resp.get("DataCatalog"),
    )


async def delete_named_query(
    named_query_id: str,
    region_name: str | None = None,
) -> None:
    """Delete named query.

    Args:
        named_query_id: Named query id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamedQueryId"] = named_query_id
    try:
        await client.call("DeleteNamedQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete named query") from exc
    return None


async def delete_notebook(
    notebook_id: str,
    region_name: str | None = None,
) -> None:
    """Delete notebook.

    Args:
        notebook_id: Notebook id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookId"] = notebook_id
    try:
        await client.call("DeleteNotebook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete notebook") from exc
    return None


async def delete_prepared_statement(
    statement_name: str,
    work_group: str,
    region_name: str | None = None,
) -> None:
    """Delete prepared statement.

    Args:
        statement_name: Statement name.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StatementName"] = statement_name
    kwargs["WorkGroup"] = work_group
    try:
        await client.call("DeletePreparedStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete prepared statement") from exc
    return None


async def delete_work_group(
    work_group: str,
    *,
    recursive_delete_option: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete work group.

    Args:
        work_group: Work group.
        recursive_delete_option: Recursive delete option.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    if recursive_delete_option is not None:
        kwargs["RecursiveDeleteOption"] = recursive_delete_option
    try:
        await client.call("DeleteWorkGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete work group") from exc
    return None


async def export_notebook(
    notebook_id: str,
    region_name: str | None = None,
) -> ExportNotebookResult:
    """Export notebook.

    Args:
        notebook_id: Notebook id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookId"] = notebook_id
    try:
        resp = await client.call("ExportNotebook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to export notebook") from exc
    return ExportNotebookResult(
        notebook_metadata=resp.get("NotebookMetadata"),
        payload=resp.get("Payload"),
    )


async def get_calculation_execution(
    calculation_execution_id: str,
    region_name: str | None = None,
) -> GetCalculationExecutionResult:
    """Get calculation execution.

    Args:
        calculation_execution_id: Calculation execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CalculationExecutionId"] = calculation_execution_id
    try:
        resp = await client.call("GetCalculationExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get calculation execution") from exc
    return GetCalculationExecutionResult(
        calculation_execution_id=resp.get("CalculationExecutionId"),
        session_id=resp.get("SessionId"),
        description=resp.get("Description"),
        working_directory=resp.get("WorkingDirectory"),
        status=resp.get("Status"),
        statistics=resp.get("Statistics"),
        result=resp.get("Result"),
    )


async def get_calculation_execution_code(
    calculation_execution_id: str,
    region_name: str | None = None,
) -> GetCalculationExecutionCodeResult:
    """Get calculation execution code.

    Args:
        calculation_execution_id: Calculation execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CalculationExecutionId"] = calculation_execution_id
    try:
        resp = await client.call("GetCalculationExecutionCode", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get calculation execution code") from exc
    return GetCalculationExecutionCodeResult(
        code_block=resp.get("CodeBlock"),
    )


async def get_calculation_execution_status(
    calculation_execution_id: str,
    region_name: str | None = None,
) -> GetCalculationExecutionStatusResult:
    """Get calculation execution status.

    Args:
        calculation_execution_id: Calculation execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CalculationExecutionId"] = calculation_execution_id
    try:
        resp = await client.call("GetCalculationExecutionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get calculation execution status") from exc
    return GetCalculationExecutionStatusResult(
        status=resp.get("Status"),
        statistics=resp.get("Statistics"),
    )


async def get_capacity_assignment_configuration(
    capacity_reservation_name: str,
    region_name: str | None = None,
) -> GetCapacityAssignmentConfigurationResult:
    """Get capacity assignment configuration.

    Args:
        capacity_reservation_name: Capacity reservation name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CapacityReservationName"] = capacity_reservation_name
    try:
        resp = await client.call("GetCapacityAssignmentConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get capacity assignment configuration") from exc
    return GetCapacityAssignmentConfigurationResult(
        capacity_assignment_configuration=resp.get("CapacityAssignmentConfiguration"),
    )


async def get_capacity_reservation(
    name: str,
    region_name: str | None = None,
) -> GetCapacityReservationResult:
    """Get capacity reservation.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    try:
        resp = await client.call("GetCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get capacity reservation") from exc
    return GetCapacityReservationResult(
        capacity_reservation=resp.get("CapacityReservation"),
    )


async def get_data_catalog(
    name: str,
    *,
    work_group: str | None = None,
    region_name: str | None = None,
) -> GetDataCatalogResult:
    """Get data catalog.

    Args:
        name: Name.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("GetDataCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get data catalog") from exc
    return GetDataCatalogResult(
        data_catalog=resp.get("DataCatalog"),
    )


async def get_database(
    catalog_name: str,
    database_name: str,
    *,
    work_group: str | None = None,
    region_name: str | None = None,
) -> GetDatabaseResult:
    """Get database.

    Args:
        catalog_name: Catalog name.
        database_name: Database name.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogName"] = catalog_name
    kwargs["DatabaseName"] = database_name
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("GetDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get database") from exc
    return GetDatabaseResult(
        database=resp.get("Database"),
    )


async def get_named_query(
    named_query_id: str,
    region_name: str | None = None,
) -> GetNamedQueryResult:
    """Get named query.

    Args:
        named_query_id: Named query id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamedQueryId"] = named_query_id
    try:
        resp = await client.call("GetNamedQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get named query") from exc
    return GetNamedQueryResult(
        named_query=resp.get("NamedQuery"),
    )


async def get_notebook_metadata(
    notebook_id: str,
    region_name: str | None = None,
) -> GetNotebookMetadataResult:
    """Get notebook metadata.

    Args:
        notebook_id: Notebook id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookId"] = notebook_id
    try:
        resp = await client.call("GetNotebookMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get notebook metadata") from exc
    return GetNotebookMetadataResult(
        notebook_metadata=resp.get("NotebookMetadata"),
    )


async def get_prepared_statement(
    statement_name: str,
    work_group: str,
    region_name: str | None = None,
) -> GetPreparedStatementResult:
    """Get prepared statement.

    Args:
        statement_name: Statement name.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StatementName"] = statement_name
    kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("GetPreparedStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get prepared statement") from exc
    return GetPreparedStatementResult(
        prepared_statement=resp.get("PreparedStatement"),
    )


async def get_query_runtime_statistics(
    query_execution_id: str,
    region_name: str | None = None,
) -> GetQueryRuntimeStatisticsResult:
    """Get query runtime statistics.

    Args:
        query_execution_id: Query execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryExecutionId"] = query_execution_id
    try:
        resp = await client.call("GetQueryRuntimeStatistics", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get query runtime statistics") from exc
    return GetQueryRuntimeStatisticsResult(
        query_runtime_statistics=resp.get("QueryRuntimeStatistics"),
    )


async def get_session(
    session_id: str,
    region_name: str | None = None,
) -> GetSessionResult:
    """Get session.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = await client.call("GetSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get session") from exc
    return GetSessionResult(
        session_id=resp.get("SessionId"),
        description=resp.get("Description"),
        work_group=resp.get("WorkGroup"),
        engine_version=resp.get("EngineVersion"),
        engine_configuration=resp.get("EngineConfiguration"),
        notebook_version=resp.get("NotebookVersion"),
        session_configuration=resp.get("SessionConfiguration"),
        status=resp.get("Status"),
        statistics=resp.get("Statistics"),
    )


async def get_session_status(
    session_id: str,
    region_name: str | None = None,
) -> GetSessionStatusResult:
    """Get session status.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = await client.call("GetSessionStatus", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get session status") from exc
    return GetSessionStatusResult(
        session_id=resp.get("SessionId"),
        status=resp.get("Status"),
    )


async def get_table_metadata(
    catalog_name: str,
    database_name: str,
    table_name: str,
    *,
    work_group: str | None = None,
    region_name: str | None = None,
) -> GetTableMetadataResult:
    """Get table metadata.

    Args:
        catalog_name: Catalog name.
        database_name: Database name.
        table_name: Table name.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogName"] = catalog_name
    kwargs["DatabaseName"] = database_name
    kwargs["TableName"] = table_name
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("GetTableMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get table metadata") from exc
    return GetTableMetadataResult(
        table_metadata=resp.get("TableMetadata"),
    )


async def get_work_group(
    work_group: str,
    region_name: str | None = None,
) -> GetWorkGroupResult:
    """Get work group.

    Args:
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("GetWorkGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get work group") from exc
    return GetWorkGroupResult(
        work_group=resp.get("WorkGroup"),
    )


async def import_notebook(
    work_group: str,
    name: str,
    type_value: str,
    *,
    payload: str | None = None,
    notebook_s3_location_uri: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> ImportNotebookResult:
    """Import notebook.

    Args:
        work_group: Work group.
        name: Name.
        type_value: Type value.
        payload: Payload.
        notebook_s3_location_uri: Notebook s3 location uri.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    kwargs["Name"] = name
    kwargs["Type"] = type_value
    if payload is not None:
        kwargs["Payload"] = payload
    if notebook_s3_location_uri is not None:
        kwargs["NotebookS3LocationUri"] = notebook_s3_location_uri
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = await client.call("ImportNotebook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to import notebook") from exc
    return ImportNotebookResult(
        notebook_id=resp.get("NotebookId"),
    )


async def list_application_dpu_sizes(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListApplicationDpuSizesResult:
    """List application dpu sizes.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListApplicationDPUSizes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list application dpu sizes") from exc
    return ListApplicationDpuSizesResult(
        application_dpu_sizes=resp.get("ApplicationDPUSizes"),
        next_token=resp.get("NextToken"),
    )


async def list_calculation_executions(
    session_id: str,
    *,
    state_filter: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListCalculationExecutionsResult:
    """List calculation executions.

    Args:
        session_id: Session id.
        state_filter: State filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    if state_filter is not None:
        kwargs["StateFilter"] = state_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListCalculationExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list calculation executions") from exc
    return ListCalculationExecutionsResult(
        next_token=resp.get("NextToken"),
        calculations=resp.get("Calculations"),
    )


async def list_capacity_reservations(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListCapacityReservationsResult:
    """List capacity reservations.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListCapacityReservations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list capacity reservations") from exc
    return ListCapacityReservationsResult(
        next_token=resp.get("NextToken"),
        capacity_reservations=resp.get("CapacityReservations"),
    )


async def list_data_catalogs(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    work_group: str | None = None,
    region_name: str | None = None,
) -> ListDataCatalogsResult:
    """List data catalogs.

    Args:
        next_token: Next token.
        max_results: Max results.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("ListDataCatalogs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list data catalogs") from exc
    return ListDataCatalogsResult(
        data_catalogs_summary=resp.get("DataCatalogsSummary"),
        next_token=resp.get("NextToken"),
    )


async def list_databases(
    catalog_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    work_group: str | None = None,
    region_name: str | None = None,
) -> ListDatabasesResult:
    """List databases.

    Args:
        catalog_name: Catalog name.
        next_token: Next token.
        max_results: Max results.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogName"] = catalog_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("ListDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list databases") from exc
    return ListDatabasesResult(
        database_list=resp.get("DatabaseList"),
        next_token=resp.get("NextToken"),
    )


async def list_engine_versions(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListEngineVersionsResult:
    """List engine versions.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListEngineVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list engine versions") from exc
    return ListEngineVersionsResult(
        engine_versions=resp.get("EngineVersions"),
        next_token=resp.get("NextToken"),
    )


async def list_executors(
    session_id: str,
    *,
    executor_state_filter: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListExecutorsResult:
    """List executors.

    Args:
        session_id: Session id.
        executor_state_filter: Executor state filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    if executor_state_filter is not None:
        kwargs["ExecutorStateFilter"] = executor_state_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListExecutors", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list executors") from exc
    return ListExecutorsResult(
        session_id=resp.get("SessionId"),
        next_token=resp.get("NextToken"),
        executors_summary=resp.get("ExecutorsSummary"),
    )


async def list_named_queries(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    work_group: str | None = None,
    region_name: str | None = None,
) -> ListNamedQueriesResult:
    """List named queries.

    Args:
        next_token: Next token.
        max_results: Max results.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("ListNamedQueries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list named queries") from exc
    return ListNamedQueriesResult(
        named_query_ids=resp.get("NamedQueryIds"),
        next_token=resp.get("NextToken"),
    )


async def list_notebook_metadata(
    work_group: str,
    *,
    filters: dict[str, Any] | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListNotebookMetadataResult:
    """List notebook metadata.

    Args:
        work_group: Work group.
        filters: Filters.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    if filters is not None:
        kwargs["Filters"] = filters
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListNotebookMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list notebook metadata") from exc
    return ListNotebookMetadataResult(
        next_token=resp.get("NextToken"),
        notebook_metadata_list=resp.get("NotebookMetadataList"),
    )


async def list_notebook_sessions(
    notebook_id: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListNotebookSessionsResult:
    """List notebook sessions.

    Args:
        notebook_id: Notebook id.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookId"] = notebook_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListNotebookSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list notebook sessions") from exc
    return ListNotebookSessionsResult(
        notebook_sessions_list=resp.get("NotebookSessionsList"),
        next_token=resp.get("NextToken"),
    )


async def list_prepared_statements(
    work_group: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPreparedStatementsResult:
    """List prepared statements.

    Args:
        work_group: Work group.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListPreparedStatements", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list prepared statements") from exc
    return ListPreparedStatementsResult(
        prepared_statements=resp.get("PreparedStatements"),
        next_token=resp.get("NextToken"),
    )


async def list_query_executions(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    work_group: str | None = None,
    region_name: str | None = None,
) -> ListQueryExecutionsResult:
    """List query executions.

    Args:
        next_token: Next token.
        max_results: Max results.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("ListQueryExecutions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list query executions") from exc
    return ListQueryExecutionsResult(
        query_execution_ids=resp.get("QueryExecutionIds"),
        next_token=resp.get("NextToken"),
    )


async def list_sessions(
    work_group: str,
    *,
    state_filter: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListSessionsResult:
    """List sessions.

    Args:
        work_group: Work group.
        state_filter: State filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    if state_filter is not None:
        kwargs["StateFilter"] = state_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListSessions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list sessions") from exc
    return ListSessionsResult(
        next_token=resp.get("NextToken"),
        sessions=resp.get("Sessions"),
    )


async def list_table_metadata(
    catalog_name: str,
    database_name: str,
    *,
    expression: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    work_group: str | None = None,
    region_name: str | None = None,
) -> ListTableMetadataResult:
    """List table metadata.

    Args:
        catalog_name: Catalog name.
        database_name: Database name.
        expression: Expression.
        next_token: Next token.
        max_results: Max results.
        work_group: Work group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CatalogName"] = catalog_name
    kwargs["DatabaseName"] = database_name
    if expression is not None:
        kwargs["Expression"] = expression
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    try:
        resp = await client.call("ListTableMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list table metadata") from exc
    return ListTableMetadataResult(
        table_metadata_list=resp.get("TableMetadataList"),
        next_token=resp.get("NextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


async def list_work_groups(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListWorkGroupsResult:
    """List work groups.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = await client.call("ListWorkGroups", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list work groups") from exc
    return ListWorkGroupsResult(
        work_groups=resp.get("WorkGroups"),
        next_token=resp.get("NextToken"),
    )


async def put_capacity_assignment_configuration(
    capacity_reservation_name: str,
    capacity_assignments: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Put capacity assignment configuration.

    Args:
        capacity_reservation_name: Capacity reservation name.
        capacity_assignments: Capacity assignments.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CapacityReservationName"] = capacity_reservation_name
    kwargs["CapacityAssignments"] = capacity_assignments
    try:
        await client.call("PutCapacityAssignmentConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put capacity assignment configuration") from exc
    return None


async def start_calculation_execution(
    session_id: str,
    *,
    description: str | None = None,
    calculation_configuration: dict[str, Any] | None = None,
    code_block: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> StartCalculationExecutionResult:
    """Start calculation execution.

    Args:
        session_id: Session id.
        description: Description.
        calculation_configuration: Calculation configuration.
        code_block: Code block.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    if description is not None:
        kwargs["Description"] = description
    if calculation_configuration is not None:
        kwargs["CalculationConfiguration"] = calculation_configuration
    if code_block is not None:
        kwargs["CodeBlock"] = code_block
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = await client.call("StartCalculationExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start calculation execution") from exc
    return StartCalculationExecutionResult(
        calculation_execution_id=resp.get("CalculationExecutionId"),
        state=resp.get("State"),
    )


async def start_query_execution(
    query_string: str,
    *,
    client_request_token: str | None = None,
    query_execution_context: dict[str, Any] | None = None,
    result_configuration: dict[str, Any] | None = None,
    work_group: str | None = None,
    execution_parameters: list[str] | None = None,
    result_reuse_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartQueryExecutionResult:
    """Start query execution.

    Args:
        query_string: Query string.
        client_request_token: Client request token.
        query_execution_context: Query execution context.
        result_configuration: Result configuration.
        work_group: Work group.
        execution_parameters: Execution parameters.
        result_reuse_configuration: Result reuse configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryString"] = query_string
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if query_execution_context is not None:
        kwargs["QueryExecutionContext"] = query_execution_context
    if result_configuration is not None:
        kwargs["ResultConfiguration"] = result_configuration
    if work_group is not None:
        kwargs["WorkGroup"] = work_group
    if execution_parameters is not None:
        kwargs["ExecutionParameters"] = execution_parameters
    if result_reuse_configuration is not None:
        kwargs["ResultReuseConfiguration"] = result_reuse_configuration
    try:
        resp = await client.call("StartQueryExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start query execution") from exc
    return StartQueryExecutionResult(
        query_execution_id=resp.get("QueryExecutionId"),
    )


async def start_session(
    work_group: str,
    engine_configuration: dict[str, Any],
    *,
    description: str | None = None,
    notebook_version: str | None = None,
    session_idle_timeout_in_minutes: int | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> StartSessionResult:
    """Start session.

    Args:
        work_group: Work group.
        engine_configuration: Engine configuration.
        description: Description.
        notebook_version: Notebook version.
        session_idle_timeout_in_minutes: Session idle timeout in minutes.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    kwargs["EngineConfiguration"] = engine_configuration
    if description is not None:
        kwargs["Description"] = description
    if notebook_version is not None:
        kwargs["NotebookVersion"] = notebook_version
    if session_idle_timeout_in_minutes is not None:
        kwargs["SessionIdleTimeoutInMinutes"] = session_idle_timeout_in_minutes
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = await client.call("StartSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start session") from exc
    return StartSessionResult(
        session_id=resp.get("SessionId"),
        state=resp.get("State"),
    )


async def stop_calculation_execution(
    calculation_execution_id: str,
    region_name: str | None = None,
) -> StopCalculationExecutionResult:
    """Stop calculation execution.

    Args:
        calculation_execution_id: Calculation execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CalculationExecutionId"] = calculation_execution_id
    try:
        resp = await client.call("StopCalculationExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop calculation execution") from exc
    return StopCalculationExecutionResult(
        state=resp.get("State"),
    )


async def stop_query_execution(
    query_execution_id: str,
    region_name: str | None = None,
) -> None:
    """Stop query execution.

    Args:
        query_execution_id: Query execution id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["QueryExecutionId"] = query_execution_id
    try:
        await client.call("StopQueryExecution", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop query execution") from exc
    return None


async def tag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def terminate_session(
    session_id: str,
    region_name: str | None = None,
) -> TerminateSessionResult:
    """Terminate session.

    Args:
        session_id: Session id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["SessionId"] = session_id
    try:
        resp = await client.call("TerminateSession", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to terminate session") from exc
    return TerminateSessionResult(
        state=resp.get("State"),
    )


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_capacity_reservation(
    target_dpus: int,
    name: str,
    region_name: str | None = None,
) -> None:
    """Update capacity reservation.

    Args:
        target_dpus: Target dpus.
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetDpus"] = target_dpus
    kwargs["Name"] = name
    try:
        await client.call("UpdateCapacityReservation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update capacity reservation") from exc
    return None


async def update_data_catalog(
    name: str,
    type_value: str,
    *,
    description: str | None = None,
    parameters: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update data catalog.

    Args:
        name: Name.
        type_value: Type value.
        description: Description.
        parameters: Parameters.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Name"] = name
    kwargs["Type"] = type_value
    if description is not None:
        kwargs["Description"] = description
    if parameters is not None:
        kwargs["Parameters"] = parameters
    try:
        await client.call("UpdateDataCatalog", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update data catalog") from exc
    return None


async def update_named_query(
    named_query_id: str,
    name: str,
    query_string: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update named query.

    Args:
        named_query_id: Named query id.
        name: Name.
        query_string: Query string.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NamedQueryId"] = named_query_id
    kwargs["Name"] = name
    kwargs["QueryString"] = query_string
    if description is not None:
        kwargs["Description"] = description
    try:
        await client.call("UpdateNamedQuery", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update named query") from exc
    return None


async def update_notebook(
    notebook_id: str,
    payload: str,
    type_value: str,
    *,
    session_id: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update notebook.

    Args:
        notebook_id: Notebook id.
        payload: Payload.
        type_value: Type value.
        session_id: Session id.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookId"] = notebook_id
    kwargs["Payload"] = payload
    kwargs["Type"] = type_value
    if session_id is not None:
        kwargs["SessionId"] = session_id
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        await client.call("UpdateNotebook", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update notebook") from exc
    return None


async def update_notebook_metadata(
    notebook_id: str,
    name: str,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update notebook metadata.

    Args:
        notebook_id: Notebook id.
        name: Name.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["NotebookId"] = notebook_id
    kwargs["Name"] = name
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        await client.call("UpdateNotebookMetadata", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update notebook metadata") from exc
    return None


async def update_prepared_statement(
    statement_name: str,
    work_group: str,
    query_statement: str,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update prepared statement.

    Args:
        statement_name: Statement name.
        work_group: Work group.
        query_statement: Query statement.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StatementName"] = statement_name
    kwargs["WorkGroup"] = work_group
    kwargs["QueryStatement"] = query_statement
    if description is not None:
        kwargs["Description"] = description
    try:
        await client.call("UpdatePreparedStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update prepared statement") from exc
    return None


async def update_work_group(
    work_group: str,
    *,
    description: str | None = None,
    configuration_updates: dict[str, Any] | None = None,
    state: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update work group.

    Args:
        work_group: Work group.
        description: Description.
        configuration_updates: Configuration updates.
        state: State.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("athena", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WorkGroup"] = work_group
    if description is not None:
        kwargs["Description"] = description
    if configuration_updates is not None:
        kwargs["ConfigurationUpdates"] = configuration_updates
    if state is not None:
        kwargs["State"] = state
    try:
        await client.call("UpdateWorkGroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update work group") from exc
    return None
