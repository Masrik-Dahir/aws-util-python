"""aws_util.rds_data — AWS RDS Data API utilities.

Provides helpers for executing SQL statements against Amazon Aurora
Serverless clusters via the RDS Data API.  Each function wraps a single
boto3 ``rds-data`` API call with structured Pydantic result models and
consistent error handling.

The :func:`run_query` composite wraps :func:`execute_statement` and
returns structured results.  The :func:`run_transaction` composite
orchestrates begin + execute + commit (with automatic rollback on error).
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "BatchExecuteResult",
    "ColumnMetadata",
    "ExecuteResult",
    "ExecuteSqlResult",
    "TransactionResult",
    "batch_execute_statement",
    "begin_transaction",
    "commit_transaction",
    "execute_sql",
    "execute_statement",
    "rollback_transaction",
    "run_query",
    "run_transaction",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class ColumnMetadata(BaseModel):
    """Metadata for a single column in a result set."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str = ""
    type_name: str = ""
    label: str = ""
    nullable: int = 0
    precision: int = 0
    scale: int = 0


class ExecuteResult(BaseModel):
    """Result from :func:`execute_statement`."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    number_of_records_updated: int = 0
    records: list[list[dict[str, Any]]] = []
    column_metadata: list[ColumnMetadata] = []
    generated_fields: list[dict[str, Any]] = []
    formatted_records: str | None = None


class BatchExecuteResult(BaseModel):
    """Result from :func:`batch_execute_statement`."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    update_results: list[dict[str, Any]] = []


class TransactionResult(BaseModel):
    """Result from :func:`begin_transaction` or :func:`commit_transaction`."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    transaction_id: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_column_metadata(
    raw: list[dict[str, Any]],
) -> list[ColumnMetadata]:
    """Parse raw column metadata dicts into models."""
    return [
        ColumnMetadata(
            name=col.get("name", ""),
            type_name=col.get("typeName", ""),
            label=col.get("label", ""),
            nullable=col.get("nullable", 0),
            precision=col.get("precision", 0),
            scale=col.get("scale", 0),
        )
        for col in raw
    ]


def _parse_execute_result(resp: dict[str, Any]) -> ExecuteResult:
    """Parse an ExecuteStatement response into a model."""
    return ExecuteResult(
        number_of_records_updated=resp.get("numberOfRecordsUpdated", 0),
        records=resp.get("records", []),
        column_metadata=_parse_column_metadata(resp.get("columnMetadata", [])),
        generated_fields=resp.get("generatedFields", []),
        formatted_records=resp.get("formattedRecords"),
    )


def _build_execute_kwargs(
    sql: str,
    resource_arn: str,
    secret_arn: str,
    database: str | None,
    schema: str | None,
    parameters: list[dict[str, Any]] | None,
    transaction_id: str | None,
    include_result_metadata: bool,
    continue_after_timeout: bool,
    format_records_as: str | None,
) -> dict[str, Any]:
    """Build kwargs for ExecuteStatement."""
    kwargs: dict[str, Any] = {
        "resourceArn": resource_arn,
        "secretArn": secret_arn,
        "sql": sql,
    }
    if database is not None:
        kwargs["database"] = database
    if schema is not None:
        kwargs["schema"] = schema
    if parameters is not None:
        kwargs["parameters"] = parameters
    if transaction_id is not None:
        kwargs["transactionId"] = transaction_id
    if include_result_metadata:
        kwargs["includeResultMetadata"] = True
    if continue_after_timeout:
        kwargs["continueAfterTimeout"] = True
    if format_records_as is not None:
        kwargs["formatRecordsAs"] = format_records_as
    return kwargs


# ---------------------------------------------------------------------------
# Statement operations
# ---------------------------------------------------------------------------


def execute_statement(
    sql: str,
    *,
    resource_arn: str,
    secret_arn: str,
    database: str | None = None,
    schema: str | None = None,
    parameters: list[dict[str, Any]] | None = None,
    transaction_id: str | None = None,
    include_result_metadata: bool = False,
    continue_after_timeout: bool = False,
    format_records_as: str | None = None,
    region_name: str | None = None,
) -> ExecuteResult:
    """Execute a single SQL statement via the RDS Data API.

    Args:
        sql: SQL statement to execute.
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        database: Target database name.
        schema: Database schema name.
        parameters: List of parameter dicts for parameterised queries.
        transaction_id: Transaction ID to execute within.
        include_result_metadata: Whether to include column metadata.
        continue_after_timeout: Whether to continue running after timeout.
        format_records_as: Format for the result records (``"JSON"`` or
            ``"NONE"``).
        region_name: AWS region override.

    Returns:
        An :class:`ExecuteResult` with the statement results.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds-data", region_name)
    kwargs = _build_execute_kwargs(
        sql,
        resource_arn,
        secret_arn,
        database,
        schema,
        parameters,
        transaction_id,
        include_result_metadata,
        continue_after_timeout,
        format_records_as,
    )

    try:
        resp = client.execute_statement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "execute_statement failed") from exc

    return _parse_execute_result(resp)


def batch_execute_statement(
    sql: str,
    *,
    resource_arn: str,
    secret_arn: str,
    database: str | None = None,
    schema: str | None = None,
    parameter_sets: list[list[dict[str, Any]]] | None = None,
    transaction_id: str | None = None,
    region_name: str | None = None,
) -> BatchExecuteResult:
    """Execute a batch of SQL statements via the RDS Data API.

    Args:
        sql: SQL statement to execute (same SQL for each parameter set).
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        database: Target database name.
        schema: Database schema name.
        parameter_sets: List of parameter sets for batch execution.
        transaction_id: Transaction ID to execute within.
        region_name: AWS region override.

    Returns:
        A :class:`BatchExecuteResult` with update results.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds-data", region_name)
    kwargs: dict[str, Any] = {
        "resourceArn": resource_arn,
        "secretArn": secret_arn,
        "sql": sql,
    }
    if database is not None:
        kwargs["database"] = database
    if schema is not None:
        kwargs["schema"] = schema
    if parameter_sets is not None:
        kwargs["parameterSets"] = parameter_sets
    if transaction_id is not None:
        kwargs["transactionId"] = transaction_id

    try:
        resp = client.batch_execute_statement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "batch_execute_statement failed") from exc

    return BatchExecuteResult(update_results=resp.get("updateResults", []))


# ---------------------------------------------------------------------------
# Transaction operations
# ---------------------------------------------------------------------------


def begin_transaction(
    *,
    resource_arn: str,
    secret_arn: str,
    database: str | None = None,
    schema: str | None = None,
    region_name: str | None = None,
) -> TransactionResult:
    """Begin a new transaction.

    Args:
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        database: Target database name.
        schema: Database schema name.
        region_name: AWS region override.

    Returns:
        A :class:`TransactionResult` with the transaction ID.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds-data", region_name)
    kwargs: dict[str, Any] = {
        "resourceArn": resource_arn,
        "secretArn": secret_arn,
    }
    if database is not None:
        kwargs["database"] = database
    if schema is not None:
        kwargs["schema"] = schema

    try:
        resp = client.begin_transaction(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "begin_transaction failed") from exc

    return TransactionResult(transaction_id=resp["transactionId"])


def commit_transaction(
    transaction_id: str,
    *,
    resource_arn: str,
    secret_arn: str,
    region_name: str | None = None,
) -> str:
    """Commit a transaction.

    Args:
        transaction_id: The transaction ID to commit.
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        region_name: AWS region override.

    Returns:
        The transaction status string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds-data", region_name)
    try:
        resp = client.commit_transaction(
            resourceArn=resource_arn,
            secretArn=secret_arn,
            transactionId=transaction_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "commit_transaction failed") from exc

    return resp.get("transactionStatus", "")


def rollback_transaction(
    transaction_id: str,
    *,
    resource_arn: str,
    secret_arn: str,
    region_name: str | None = None,
) -> str:
    """Rollback a transaction.

    Args:
        transaction_id: The transaction ID to rollback.
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        region_name: AWS region override.

    Returns:
        The transaction status string.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds-data", region_name)
    try:
        resp = client.rollback_transaction(
            resourceArn=resource_arn,
            secretArn=secret_arn,
            transactionId=transaction_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "rollback_transaction failed") from exc

    return resp.get("transactionStatus", "")


# ---------------------------------------------------------------------------
# Composite operations
# ---------------------------------------------------------------------------


def run_query(
    sql: str,
    *,
    resource_arn: str,
    secret_arn: str,
    database: str | None = None,
    schema: str | None = None,
    parameters: list[dict[str, Any]] | None = None,
    format_records_as: str | None = None,
    region_name: str | None = None,
) -> ExecuteResult:
    """Execute a query and return structured results.

    Wraps :func:`execute_statement` with ``include_result_metadata=True``
    for a convenient one-call query interface.

    Args:
        sql: SQL statement to execute.
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        database: Target database name.
        schema: Database schema name.
        parameters: List of parameter dicts for parameterised queries.
        format_records_as: Format for the result records.
        region_name: AWS region override.

    Returns:
        An :class:`ExecuteResult` with full metadata and records.

    Raises:
        RuntimeError: If the API call fails.
    """
    return execute_statement(
        sql,
        resource_arn=resource_arn,
        secret_arn=secret_arn,
        database=database,
        schema=schema,
        parameters=parameters,
        include_result_metadata=True,
        format_records_as=format_records_as,
        region_name=region_name,
    )


def run_transaction(
    sql: str,
    *,
    resource_arn: str,
    secret_arn: str,
    database: str | None = None,
    schema: str | None = None,
    parameters: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> ExecuteResult:
    """Execute a statement inside a managed transaction.

    Orchestrates :func:`begin_transaction`, :func:`execute_statement`,
    and :func:`commit_transaction`.  On any error during execution or
    commit the transaction is automatically rolled back.

    Args:
        sql: SQL statement to execute.
        resource_arn: ARN of the Aurora Serverless DB cluster.
        secret_arn: ARN of the Secrets Manager secret for authentication.
        database: Target database name.
        schema: Database schema name.
        parameters: List of parameter dicts for parameterised queries.
        region_name: AWS region override.

    Returns:
        An :class:`ExecuteResult` with the statement results.

    Raises:
        RuntimeError: If any API call fails (transaction is rolled back).
    """
    txn = begin_transaction(
        resource_arn=resource_arn,
        secret_arn=secret_arn,
        database=database,
        schema=schema,
        region_name=region_name,
    )
    try:
        result = execute_statement(
            sql,
            resource_arn=resource_arn,
            secret_arn=secret_arn,
            database=database,
            schema=schema,
            parameters=parameters,
            transaction_id=txn.transaction_id,
            region_name=region_name,
        )
        commit_transaction(
            txn.transaction_id,
            resource_arn=resource_arn,
            secret_arn=secret_arn,
            region_name=region_name,
        )
    except Exception:
        try:
            rollback_transaction(
                txn.transaction_id,
                resource_arn=resource_arn,
                secret_arn=secret_arn,
                region_name=region_name,
            )
        except Exception:
            pass
        raise
    return result


class ExecuteSqlResult(BaseModel):
    """Result of execute_sql."""

    model_config = ConfigDict(frozen=True)

    sql_statement_results: list[dict[str, Any]] | None = None


def execute_sql(
    db_cluster_or_instance_arn: str,
    aws_secret_store_arn: str,
    sql_statements: str,
    *,
    database: str | None = None,
    schema: str | None = None,
    region_name: str | None = None,
) -> ExecuteSqlResult:
    """Execute sql.

    Args:
        db_cluster_or_instance_arn: Db cluster or instance arn.
        aws_secret_store_arn: Aws secret store arn.
        sql_statements: Sql statements.
        database: Database.
        schema: Schema.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("rds-data", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["dbClusterOrInstanceArn"] = db_cluster_or_instance_arn
    kwargs["awsSecretStoreArn"] = aws_secret_store_arn
    kwargs["sqlStatements"] = sql_statements
    if database is not None:
        kwargs["database"] = database
    if schema is not None:
        kwargs["schema"] = schema
    try:
        resp = client.execute_sql(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute sql") from exc
    return ExecuteSqlResult(
        sql_statement_results=resp.get("sqlStatementResults"),
    )
