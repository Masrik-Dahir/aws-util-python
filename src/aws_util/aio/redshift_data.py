"""Native async AWS Redshift Data API utilities.

Uses :mod:`aws_util.aio._engine` for true non-blocking I/O.  Pydantic
models and pure-compute helpers are re-exported from the sync module.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, AwsTimeoutError, wrap_aws_error
from aws_util.redshift_data import (
    DescribeTableResult,
    GetStatementResultV2Result,
    ListDatabasesResult,
    ListSchemasResult,
    ListTablesResult,
    QueryResult,
    StatementDescription,
    StatementResult,
    _parse_description,
    _parse_result,
)

__all__ = [
    "DescribeTableResult",
    "GetStatementResultV2Result",
    "ListDatabasesResult",
    "ListSchemasResult",
    "ListTablesResult",
    "QueryResult",
    "StatementDescription",
    "StatementResult",
    "batch_execute_statement",
    "cancel_statement",
    "describe_statement",
    "describe_table",
    "execute_statement",
    "get_statement_result",
    "get_statement_result_v2",
    "list_databases",
    "list_schemas",
    "list_statements",
    "list_tables",
    "run_query",
]


# ---------------------------------------------------------------------------
# Statement operations
# ---------------------------------------------------------------------------


async def execute_statement(
    sql: str,
    *,
    database: str,
    cluster_identifier: str | None = None,
    workgroup_name: str | None = None,
    secret_arn: str | None = None,
    db_user: str | None = None,
    statement_name: str | None = None,
    with_event: bool = False,
    region_name: str | None = None,
) -> StatementResult:
    """Execute a single SQL statement via the Redshift Data API.

    Either *cluster_identifier* or *workgroup_name* must be provided.

    Args:
        sql: SQL statement to execute.
        database: Target database name.
        cluster_identifier: Redshift cluster identifier.
        workgroup_name: Redshift Serverless workgroup name.
        secret_arn: Secrets Manager ARN for authentication.
        db_user: Database user for temporary credentials.
        statement_name: Optional name for the statement.
        with_event: Whether to send an event to EventBridge.
        region_name: AWS region override.

    Returns:
        A :class:`StatementResult` with the statement ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {"Sql": sql, "Database": database}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if statement_name is not None:
        kwargs["StatementName"] = statement_name
    if with_event:
        kwargs["WithEvent"] = True

    try:
        resp = await client.call("ExecuteStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "execute_statement failed") from exc

    return StatementResult(
        statement_id=resp["Id"],
        cluster_identifier=cluster_identifier,
        database=database,
        secret_arn=secret_arn,
        db_user=db_user,
        workgroup_name=workgroup_name,
    )


async def batch_execute_statement(
    sqls: list[str],
    *,
    database: str,
    cluster_identifier: str | None = None,
    workgroup_name: str | None = None,
    secret_arn: str | None = None,
    db_user: str | None = None,
    statement_name: str | None = None,
    with_event: bool = False,
    region_name: str | None = None,
) -> StatementResult:
    """Execute multiple SQL statements as a batch.

    Either *cluster_identifier* or *workgroup_name* must be provided.

    Args:
        sqls: List of SQL statements to execute.
        database: Target database name.
        cluster_identifier: Redshift cluster identifier.
        workgroup_name: Redshift Serverless workgroup name.
        secret_arn: Secrets Manager ARN for authentication.
        db_user: Database user for temporary credentials.
        statement_name: Optional name for the batch.
        with_event: Whether to send an event to EventBridge.
        region_name: AWS region override.

    Returns:
        A :class:`StatementResult` with the statement ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {"Sqls": sqls, "Database": database}
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if statement_name is not None:
        kwargs["StatementName"] = statement_name
    if with_event:
        kwargs["WithEvent"] = True

    try:
        resp = await client.call("BatchExecuteStatement", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "batch_execute_statement failed") from exc

    return StatementResult(
        statement_id=resp["Id"],
        cluster_identifier=cluster_identifier,
        database=database,
        secret_arn=secret_arn,
        db_user=db_user,
        workgroup_name=workgroup_name,
    )


async def describe_statement(
    statement_id: str,
    *,
    region_name: str | None = None,
) -> StatementDescription:
    """Describe a submitted statement.

    Args:
        statement_id: The statement identifier to describe.
        region_name: AWS region override.

    Returns:
        A :class:`StatementDescription`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    try:
        resp = await client.call("DescribeStatement", Id=statement_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_statement failed for {statement_id!r}",
        ) from exc

    return _parse_description(resp)


async def get_statement_result(
    statement_id: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> QueryResult:
    """Retrieve the result set for a finished statement.

    Args:
        statement_id: The statement identifier.
        next_token: Pagination token for additional rows.
        region_name: AWS region override.

    Returns:
        A :class:`QueryResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {"Id": statement_id}
    if next_token is not None:
        kwargs["NextToken"] = next_token

    try:
        resp = await client.call("GetStatementResult", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"get_statement_result failed for {statement_id!r}",
        ) from exc

    return _parse_result(resp)


async def list_statements(
    *,
    status: str | None = None,
    statement_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> tuple[list[StatementDescription], str | None]:
    """List submitted statements, optionally filtered.

    Args:
        status: Filter by status (e.g. ``"FINISHED"``, ``"FAILED"``).
        statement_name: Filter by statement name.
        max_results: Maximum number of statements to return.
        next_token: Pagination token.
        region_name: AWS region override.

    Returns:
        A tuple of (list of :class:`StatementDescription`, next_token).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {}
    if status is not None:
        kwargs["Status"] = status
    if statement_name is not None:
        kwargs["StatementName"] = statement_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token

    try:
        resp = await client.call("ListStatements", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_statements failed") from exc

    statements = [_parse_description(s) for s in resp.get("Statements", [])]
    return statements, resp.get("NextToken")


async def cancel_statement(
    statement_id: str,
    *,
    region_name: str | None = None,
) -> bool:
    """Cancel a running statement.

    Args:
        statement_id: The statement identifier to cancel.
        region_name: AWS region override.

    Returns:
        ``True`` if the cancellation was successful.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    try:
        resp = await client.call("CancelStatement", Id=statement_id)
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"cancel_statement failed for {statement_id!r}",
        ) from exc

    return resp.get("Status", False)


# ---------------------------------------------------------------------------
# Composite operation
# ---------------------------------------------------------------------------


async def run_query(
    sql: str,
    *,
    database: str,
    cluster_identifier: str | None = None,
    workgroup_name: str | None = None,
    secret_arn: str | None = None,
    db_user: str | None = None,
    timeout: float = 300,
    poll_interval: float = 2,
    region_name: str | None = None,
) -> QueryResult:
    """Execute a query and wait for results.

    Combines :func:`execute_statement`, polling via
    :func:`describe_statement`, and :func:`get_statement_result` into
    a single async call.

    Args:
        sql: SQL statement to execute.
        database: Target database name.
        cluster_identifier: Redshift cluster identifier.
        workgroup_name: Redshift Serverless workgroup name.
        secret_arn: Secrets Manager ARN for authentication.
        db_user: Database user for temporary credentials.
        timeout: Maximum seconds to wait for completion.
        poll_interval: Seconds between status polls.
        region_name: AWS region override.

    Returns:
        A :class:`QueryResult` with the full result set.

    Raises:
        AwsTimeoutError: If the statement does not finish in time.
        AwsServiceError: If the statement fails or is aborted.
        RuntimeError: If an API call fails.
    """
    stmt = await execute_statement(
        sql,
        database=database,
        cluster_identifier=cluster_identifier,
        workgroup_name=workgroup_name,
        secret_arn=secret_arn,
        db_user=db_user,
        region_name=region_name,
    )
    deadline = time.monotonic() + timeout
    while True:
        desc = await describe_statement(stmt.statement_id, region_name=region_name)
        if desc.status == "FINISHED":
            return await get_statement_result(stmt.statement_id, region_name=region_name)
        if desc.status in ("FAILED", "ABORTED"):
            raise AwsServiceError(
                f"Statement {stmt.statement_id!r} {desc.status}: {desc.error or 'no error details'}"
            )
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Statement {stmt.statement_id!r} did not finish "
                f"within {timeout}s (current: {desc.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def describe_table(
    database: str,
    *,
    cluster_identifier: str | None = None,
    connected_database: str | None = None,
    db_user: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    schema: str | None = None,
    secret_arn: str | None = None,
    table: str | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> DescribeTableResult:
    """Describe table.

    Args:
        database: Database.
        cluster_identifier: Cluster identifier.
        connected_database: Connected database.
        db_user: Db user.
        max_results: Max results.
        next_token: Next token.
        schema: Schema.
        secret_arn: Secret arn.
        table: Table.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Database"] = database
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if connected_database is not None:
        kwargs["ConnectedDatabase"] = connected_database
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if schema is not None:
        kwargs["Schema"] = schema
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if table is not None:
        kwargs["Table"] = table
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    try:
        resp = await client.call("DescribeTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe table") from exc
    return DescribeTableResult(
        column_list=resp.get("ColumnList"),
        next_token=resp.get("NextToken"),
        table_name=resp.get("TableName"),
    )


async def get_statement_result_v2(
    id: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> GetStatementResultV2Result:
    """Get statement result v2.

    Args:
        id: Id.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Id"] = id
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("GetStatementResultV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get statement result v2") from exc
    return GetStatementResultV2Result(
        column_metadata=resp.get("ColumnMetadata"),
        next_token=resp.get("NextToken"),
        records=resp.get("Records"),
        result_format=resp.get("ResultFormat"),
        total_num_rows=resp.get("TotalNumRows"),
    )


async def list_databases(
    database: str,
    *,
    cluster_identifier: str | None = None,
    db_user: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    secret_arn: str | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> ListDatabasesResult:
    """List databases.

    Args:
        database: Database.
        cluster_identifier: Cluster identifier.
        db_user: Db user.
        max_results: Max results.
        next_token: Next token.
        secret_arn: Secret arn.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Database"] = database
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    try:
        resp = await client.call("ListDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list databases") from exc
    return ListDatabasesResult(
        databases=resp.get("Databases"),
        next_token=resp.get("NextToken"),
    )


async def list_schemas(
    database: str,
    *,
    cluster_identifier: str | None = None,
    connected_database: str | None = None,
    db_user: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    schema_pattern: str | None = None,
    secret_arn: str | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> ListSchemasResult:
    """List schemas.

    Args:
        database: Database.
        cluster_identifier: Cluster identifier.
        connected_database: Connected database.
        db_user: Db user.
        max_results: Max results.
        next_token: Next token.
        schema_pattern: Schema pattern.
        secret_arn: Secret arn.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Database"] = database
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if connected_database is not None:
        kwargs["ConnectedDatabase"] = connected_database
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if schema_pattern is not None:
        kwargs["SchemaPattern"] = schema_pattern
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    try:
        resp = await client.call("ListSchemas", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list schemas") from exc
    return ListSchemasResult(
        next_token=resp.get("NextToken"),
        schemas=resp.get("Schemas"),
    )


async def list_tables(
    database: str,
    *,
    cluster_identifier: str | None = None,
    connected_database: str | None = None,
    db_user: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    schema_pattern: str | None = None,
    secret_arn: str | None = None,
    table_pattern: str | None = None,
    workgroup_name: str | None = None,
    region_name: str | None = None,
) -> ListTablesResult:
    """List tables.

    Args:
        database: Database.
        cluster_identifier: Cluster identifier.
        connected_database: Connected database.
        db_user: Db user.
        max_results: Max results.
        next_token: Next token.
        schema_pattern: Schema pattern.
        secret_arn: Secret arn.
        table_pattern: Table pattern.
        workgroup_name: Workgroup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("redshift-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Database"] = database
    if cluster_identifier is not None:
        kwargs["ClusterIdentifier"] = cluster_identifier
    if connected_database is not None:
        kwargs["ConnectedDatabase"] = connected_database
    if db_user is not None:
        kwargs["DbUser"] = db_user
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if schema_pattern is not None:
        kwargs["SchemaPattern"] = schema_pattern
    if secret_arn is not None:
        kwargs["SecretArn"] = secret_arn
    if table_pattern is not None:
        kwargs["TablePattern"] = table_pattern
    if workgroup_name is not None:
        kwargs["WorkgroupName"] = workgroup_name
    try:
        resp = await client.call("ListTables", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tables") from exc
    return ListTablesResult(
        next_token=resp.get("NextToken"),
        tables=resp.get("Tables"),
    )
