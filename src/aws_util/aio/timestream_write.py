"""Native async Amazon Timestream Write utilities.

Uses :mod:`aws_util.aio._engine` for true non-blocking I/O.  Pydantic
models and pure-compute helpers are re-exported from the sync module.
"""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.timestream_write import (
    CreateBatchLoadTaskResult,
    DatabaseDescription,
    DescribeBatchLoadTaskResult,
    DescribeEndpointsResult,
    ListBatchLoadTasksResult,
    ListTagsForResourceResult,
    MagneticStoreWriteProperties,
    Record,
    RetentionProperties,
    TableDescription,
    WriteRecordsResult,
    _build_record,
    _parse_database,
    _parse_table,
)

__all__ = [
    "CreateBatchLoadTaskResult",
    "DatabaseDescription",
    "DescribeBatchLoadTaskResult",
    "DescribeEndpointsResult",
    "ListBatchLoadTasksResult",
    "ListTagsForResourceResult",
    "MagneticStoreWriteProperties",
    "Record",
    "RetentionProperties",
    "TableDescription",
    "WriteRecordsResult",
    "create_batch_load_task",
    "create_database",
    "create_table",
    "delete_database",
    "delete_table",
    "describe_batch_load_task",
    "describe_database",
    "describe_endpoints",
    "describe_table",
    "list_batch_load_tasks",
    "list_databases",
    "list_tables",
    "list_tags_for_resource",
    "resume_batch_load_task",
    "tag_resource",
    "untag_resource",
    "update_database",
    "update_table",
    "write_records",
]


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------


async def create_database(
    database_name: str,
    *,
    kms_key_id: str | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> DatabaseDescription:
    """Create a Timestream database.

    Args:
        database_name: Name for the new database.
        kms_key_id: KMS key ARN for encryption at rest.
        tags: Optional list of ``{"Key": ..., "Value": ...}`` tags.
        region_name: AWS region override.

    Returns:
        A :class:`DatabaseDescription` of the newly created database.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {"DatabaseName": database_name}
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateDatabase", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_database failed") from exc
    return _parse_database(resp.get("Database", {}))


async def describe_database(
    database_name: str,
    *,
    region_name: str | None = None,
) -> DatabaseDescription:
    """Describe a Timestream database.

    Args:
        database_name: Name of the database to describe.
        region_name: AWS region override.

    Returns:
        A :class:`DatabaseDescription`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    try:
        resp = await client.call("DescribeDatabase", DatabaseName=database_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_database failed for {database_name!r}") from exc
    return _parse_database(resp.get("Database", {}))


async def list_databases(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> tuple[list[DatabaseDescription], str | None]:
    """List Timestream databases.

    Args:
        max_results: Maximum number of databases to return.
        next_token: Pagination token.
        region_name: AWS region override.

    Returns:
        A tuple of (list of :class:`DatabaseDescription`, next_token).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListDatabases", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_databases failed") from exc
    databases = [_parse_database(d) for d in resp.get("Databases", [])]
    return databases, resp.get("NextToken")


async def delete_database(
    database_name: str,
    *,
    region_name: str | None = None,
) -> bool:
    """Delete a Timestream database.

    Args:
        database_name: Name of the database to delete.
        region_name: AWS region override.

    Returns:
        ``True`` if the deletion succeeded.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    try:
        await client.call("DeleteDatabase", DatabaseName=database_name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_database failed for {database_name!r}") from exc
    return True


async def update_database(
    database_name: str,
    *,
    kms_key_id: str,
    region_name: str | None = None,
) -> DatabaseDescription:
    """Update a Timestream database (currently only KMS key).

    Args:
        database_name: Name of the database to update.
        kms_key_id: New KMS key ARN.
        region_name: AWS region override.

    Returns:
        A :class:`DatabaseDescription` of the updated database.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    try:
        resp = await client.call(
            "UpdateDatabase",
            DatabaseName=database_name,
            KmsKeyId=kms_key_id,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_database failed for {database_name!r}") from exc
    return _parse_database(resp.get("Database", {}))


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


async def create_table(
    database_name: str,
    table_name: str,
    *,
    retention_properties: dict[str, int] | None = None,
    magnetic_store_write_properties: dict[str, Any] | None = None,
    tags: list[dict[str, str]] | None = None,
    region_name: str | None = None,
) -> TableDescription:
    """Create a Timestream table.

    Args:
        database_name: Database that will contain the table.
        table_name: Name for the new table.
        retention_properties: Dict with retention configuration.
        magnetic_store_write_properties: Dict with magnetic store settings.
        tags: Optional list of ``{"Key": ..., "Value": ...}`` tags.
        region_name: AWS region override.

    Returns:
        A :class:`TableDescription` of the new table.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {
        "DatabaseName": database_name,
        "TableName": table_name,
    }
    if retention_properties is not None:
        kwargs["RetentionProperties"] = retention_properties
    if magnetic_store_write_properties is not None:
        kwargs["MagneticStoreWriteProperties"] = magnetic_store_write_properties
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_table failed") from exc
    return _parse_table(resp.get("Table", {}))


async def describe_table(
    database_name: str,
    table_name: str,
    *,
    region_name: str | None = None,
) -> TableDescription:
    """Describe a Timestream table.

    Args:
        database_name: Database containing the table.
        table_name: Name of the table.
        region_name: AWS region override.

    Returns:
        A :class:`TableDescription`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    try:
        resp = await client.call(
            "DescribeTable",
            DatabaseName=database_name,
            TableName=table_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_table failed for {table_name!r}") from exc
    return _parse_table(resp.get("Table", {}))


async def list_tables(
    *,
    database_name: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> tuple[list[TableDescription], str | None]:
    """List Timestream tables.

    Args:
        database_name: Filter by database name.
        max_results: Maximum number of tables to return.
        next_token: Pagination token.
        region_name: AWS region override.

    Returns:
        A tuple of (list of :class:`TableDescription`, next_token).

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListTables", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_tables failed") from exc
    tables = [_parse_table(t) for t in resp.get("Tables", [])]
    return tables, resp.get("NextToken")


async def delete_table(
    database_name: str,
    table_name: str,
    *,
    region_name: str | None = None,
) -> bool:
    """Delete a Timestream table.

    Args:
        database_name: Database containing the table.
        table_name: Name of the table to delete.
        region_name: AWS region override.

    Returns:
        ``True`` if the deletion succeeded.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    try:
        await client.call(
            "DeleteTable",
            DatabaseName=database_name,
            TableName=table_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_table failed for {table_name!r}") from exc
    return True


async def update_table(
    database_name: str,
    table_name: str,
    *,
    retention_properties: dict[str, int] | None = None,
    magnetic_store_write_properties: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> TableDescription:
    """Update a Timestream table.

    Args:
        database_name: Database containing the table.
        table_name: Name of the table to update.
        retention_properties: New retention configuration.
        magnetic_store_write_properties: New magnetic-store settings.
        region_name: AWS region override.

    Returns:
        A :class:`TableDescription` of the updated table.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {
        "DatabaseName": database_name,
        "TableName": table_name,
    }
    if retention_properties is not None:
        kwargs["RetentionProperties"] = retention_properties
    if magnetic_store_write_properties is not None:
        kwargs["MagneticStoreWriteProperties"] = magnetic_store_write_properties
    try:
        resp = await client.call("UpdateTable", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_table failed for {table_name!r}") from exc
    return _parse_table(resp.get("Table", {}))


# ---------------------------------------------------------------------------
# Write records
# ---------------------------------------------------------------------------


async def write_records(
    database_name: str,
    table_name: str,
    records: list[Record | dict[str, Any]],
    *,
    common_attributes: Record | dict[str, Any] | None = None,
    region_name: str | None = None,
) -> WriteRecordsResult:
    """Write time-series records to a Timestream table.

    Args:
        database_name: Target database name.
        table_name: Target table name.
        records: List of records to ingest.
        common_attributes: Shared attributes applied to all records.
        region_name: AWS region override.

    Returns:
        A :class:`WriteRecordsResult` with ingestion counts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {
        "DatabaseName": database_name,
        "TableName": table_name,
        "Records": [_build_record(r) for r in records],
    }
    if common_attributes is not None:
        kwargs["CommonAttributes"] = _build_record(common_attributes)
    try:
        resp = await client.call("WriteRecords", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "write_records failed") from exc
    ingested = resp.get("RecordsIngested", {})
    return WriteRecordsResult(
        records_ingested_total=ingested.get("Total", 0),
        records_ingested_memory_store=ingested.get("MemoryStore", 0),
        records_ingested_magnetic_store=ingested.get("MagneticStore", 0),
    )


async def create_batch_load_task(
    data_source_configuration: dict[str, Any],
    report_configuration: dict[str, Any],
    target_database_name: str,
    target_table_name: str,
    *,
    client_token: str | None = None,
    data_model_configuration: dict[str, Any] | None = None,
    record_version: int | None = None,
    region_name: str | None = None,
) -> CreateBatchLoadTaskResult:
    """Create batch load task.

    Args:
        data_source_configuration: Data source configuration.
        report_configuration: Report configuration.
        target_database_name: Target database name.
        target_table_name: Target table name.
        client_token: Client token.
        data_model_configuration: Data model configuration.
        record_version: Record version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DataSourceConfiguration"] = data_source_configuration
    kwargs["ReportConfiguration"] = report_configuration
    kwargs["TargetDatabaseName"] = target_database_name
    kwargs["TargetTableName"] = target_table_name
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if data_model_configuration is not None:
        kwargs["DataModelConfiguration"] = data_model_configuration
    if record_version is not None:
        kwargs["RecordVersion"] = record_version
    try:
        resp = await client.call("CreateBatchLoadTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create batch load task") from exc
    return CreateBatchLoadTaskResult(
        task_id=resp.get("TaskId"),
    )


async def describe_batch_load_task(
    task_id: str,
    region_name: str | None = None,
) -> DescribeBatchLoadTaskResult:
    """Describe batch load task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TaskId"] = task_id
    try:
        resp = await client.call("DescribeBatchLoadTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe batch load task") from exc
    return DescribeBatchLoadTaskResult(
        batch_load_task_description=resp.get("BatchLoadTaskDescription"),
    )


async def describe_endpoints(
    region_name: str | None = None,
) -> DescribeEndpointsResult:
    """Describe endpoints.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeEndpoints", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoints") from exc
    return DescribeEndpointsResult(
        endpoints=resp.get("Endpoints"),
    )


async def list_batch_load_tasks(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    task_status: str | None = None,
    region_name: str | None = None,
) -> ListBatchLoadTasksResult:
    """List batch load tasks.

    Args:
        next_token: Next token.
        max_results: Max results.
        task_status: Task status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if task_status is not None:
        kwargs["TaskStatus"] = task_status
    try:
        resp = await client.call("ListBatchLoadTasks", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list batch load tasks") from exc
    return ListBatchLoadTasksResult(
        next_token=resp.get("NextToken"),
        batch_load_tasks=resp.get("BatchLoadTasks"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def resume_batch_load_task(
    task_id: str,
    region_name: str | None = None,
) -> None:
    """Resume batch load task.

    Args:
        task_id: Task id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TaskId"] = task_id
    try:
        await client.call("ResumeBatchLoadTask", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to resume batch load task") from exc
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
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


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
    client = async_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
