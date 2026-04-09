"""aws_util.timestream_write -- Amazon Timestream Write utilities.

Provides helpers for managing Timestream databases, tables, and writing
time-series records via the ``timestream-write`` boto3 service.  Each
function wraps a single API call with structured Pydantic result models
and consistent error handling.
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

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
# Models
# ---------------------------------------------------------------------------


class RetentionProperties(BaseModel):
    """Retention configuration for a Timestream table."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    memory_store_retention_period_in_hours: int = 24
    magnetic_store_retention_period_in_days: int = 73000


class MagneticStoreWriteProperties(BaseModel):
    """Magnetic-store write settings for a Timestream table."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    enable_magnetic_store_writes: bool = False


class DatabaseDescription(BaseModel):
    """Metadata describing a Timestream database."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    database_name: str
    arn: str | None = None
    table_count: int = 0
    kms_key_id: str | None = None
    creation_time: str | None = None
    last_updated_time: str | None = None


class TableDescription(BaseModel):
    """Metadata describing a Timestream table."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    database_name: str
    table_name: str
    arn: str | None = None
    table_status: str | None = None
    retention_properties: RetentionProperties | None = None
    magnetic_store_write_properties: MagneticStoreWriteProperties | None = None
    creation_time: str | None = None
    last_updated_time: str | None = None


class Record(BaseModel):
    """A single Timestream record for ingestion."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    dimensions: list[dict[str, str]] = []
    measure_name: str | None = None
    measure_value: str | None = None
    measure_value_type: str | None = None
    time: str | None = None
    time_unit: str | None = None
    measure_values: list[dict[str, str]] | None = None
    version: int | None = None


class WriteRecordsResult(BaseModel):
    """Result of a WriteRecords call."""

    model_config = ConfigDict(populate_by_name=True, frozen=True)

    records_ingested_total: int = 0
    records_ingested_memory_store: int = 0
    records_ingested_magnetic_store: int = 0


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_database(resp: dict[str, Any]) -> DatabaseDescription:
    """Parse a Database description dict into a model."""
    return DatabaseDescription(
        database_name=resp.get("DatabaseName", ""),
        arn=resp.get("Arn"),
        table_count=resp.get("TableCount", 0),
        kms_key_id=resp.get("KmsKeyId"),
        creation_time=(str(resp["CreationTime"]) if "CreationTime" in resp else None),
        last_updated_time=(str(resp["LastUpdatedTime"]) if "LastUpdatedTime" in resp else None),
    )


def _parse_table(resp: dict[str, Any]) -> TableDescription:
    """Parse a Table description dict into a model."""
    ret_props = resp.get("RetentionProperties")
    mag_props = resp.get("MagneticStoreWriteProperties")
    return TableDescription(
        database_name=resp.get("DatabaseName", ""),
        table_name=resp.get("TableName", ""),
        arn=resp.get("Arn"),
        table_status=resp.get("TableStatus"),
        retention_properties=(
            RetentionProperties(
                memory_store_retention_period_in_hours=ret_props.get(
                    "MemoryStoreRetentionPeriodInHours", 24
                ),
                magnetic_store_retention_period_in_days=ret_props.get(
                    "MagneticStoreRetentionPeriodInDays", 73000
                ),
            )
            if ret_props
            else None
        ),
        magnetic_store_write_properties=(
            MagneticStoreWriteProperties(
                enable_magnetic_store_writes=mag_props.get("EnableMagneticStoreWrites", False),
            )
            if mag_props
            else None
        ),
        creation_time=(str(resp["CreationTime"]) if "CreationTime" in resp else None),
        last_updated_time=(str(resp["LastUpdatedTime"]) if "LastUpdatedTime" in resp else None),
    )


def _build_record(rec: Record | dict[str, Any]) -> dict[str, Any]:
    """Convert a Record model (or plain dict) to an AWS-style dict."""
    if isinstance(rec, dict):
        return rec
    out: dict[str, Any] = {}
    if rec.dimensions:
        out["Dimensions"] = [
            {
                "Name": d.get("Name", d.get("name", "")),
                "Value": d.get("Value", d.get("value", "")),
                "DimensionValueType": d.get(
                    "DimensionValueType",
                    d.get("dimension_value_type", "VARCHAR"),
                ),
            }
            for d in rec.dimensions
        ]
    if rec.measure_name is not None:
        out["MeasureName"] = rec.measure_name
    if rec.measure_value is not None:
        out["MeasureValue"] = rec.measure_value
    if rec.measure_value_type is not None:
        out["MeasureValueType"] = rec.measure_value_type
    if rec.time is not None:
        out["Time"] = rec.time
    if rec.time_unit is not None:
        out["TimeUnit"] = rec.time_unit
    if rec.measure_values is not None:
        out["MeasureValues"] = rec.measure_values
    if rec.version is not None:
        out["Version"] = rec.version
    return out


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------


def create_database(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {"DatabaseName": database_name}
    if kms_key_id is not None:
        kwargs["KmsKeyId"] = kms_key_id
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = client.create_database(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_database failed") from exc
    return _parse_database(resp.get("Database", {}))


def describe_database(
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
    client = get_client("timestream-write", region_name)
    try:
        resp = client.describe_database(DatabaseName=database_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_database failed for {database_name!r}") from exc
    return _parse_database(resp.get("Database", {}))


def list_databases(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_databases(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_databases failed") from exc
    databases = [_parse_database(d) for d in resp.get("Databases", [])]
    return databases, resp.get("NextToken")


def delete_database(
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
    client = get_client("timestream-write", region_name)
    try:
        client.delete_database(DatabaseName=database_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_database failed for {database_name!r}") from exc
    return True


def update_database(
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
    client = get_client("timestream-write", region_name)
    try:
        resp = client.update_database(
            DatabaseName=database_name,
            KmsKeyId=kms_key_id,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_database failed for {database_name!r}") from exc
    return _parse_database(resp.get("Database", {}))


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


def create_table(
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
        retention_properties: Dict with
            ``MemoryStoreRetentionPeriodInHours`` and/or
            ``MagneticStoreRetentionPeriodInDays``.
        magnetic_store_write_properties: Dict with
            ``EnableMagneticStoreWrites``.
        tags: Optional list of ``{"Key": ..., "Value": ...}`` tags.
        region_name: AWS region override.

    Returns:
        A :class:`TableDescription` of the new table.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("timestream-write", region_name)
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
        resp = client.create_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_table failed") from exc
    return _parse_table(resp.get("Table", {}))


def describe_table(
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
    client = get_client("timestream-write", region_name)
    try:
        resp = client.describe_table(
            DatabaseName=database_name,
            TableName=table_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_table failed for {table_name!r}") from exc
    return _parse_table(resp.get("Table", {}))


def list_tables(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    if database_name is not None:
        kwargs["DatabaseName"] = database_name
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tables(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_tables failed") from exc
    tables = [_parse_table(t) for t in resp.get("Tables", [])]
    return tables, resp.get("NextToken")


def delete_table(
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
    client = get_client("timestream-write", region_name)
    try:
        client.delete_table(
            DatabaseName=database_name,
            TableName=table_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_table failed for {table_name!r}") from exc
    return True


def update_table(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {
        "DatabaseName": database_name,
        "TableName": table_name,
    }
    if retention_properties is not None:
        kwargs["RetentionProperties"] = retention_properties
    if magnetic_store_write_properties is not None:
        kwargs["MagneticStoreWriteProperties"] = magnetic_store_write_properties
    try:
        resp = client.update_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_table failed for {table_name!r}") from exc
    return _parse_table(resp.get("Table", {}))


# ---------------------------------------------------------------------------
# Write records
# ---------------------------------------------------------------------------


def write_records(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {
        "DatabaseName": database_name,
        "TableName": table_name,
        "Records": [_build_record(r) for r in records],
    }
    if common_attributes is not None:
        kwargs["CommonAttributes"] = _build_record(common_attributes)
    try:
        resp = client.write_records(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "write_records failed") from exc
    ingested = resp.get("RecordsIngested", {})
    return WriteRecordsResult(
        records_ingested_total=ingested.get("Total", 0),
        records_ingested_memory_store=ingested.get("MemoryStore", 0),
        records_ingested_magnetic_store=ingested.get("MagneticStore", 0),
    )


class CreateBatchLoadTaskResult(BaseModel):
    """Result of create_batch_load_task."""

    model_config = ConfigDict(frozen=True)

    task_id: str | None = None


class DescribeBatchLoadTaskResult(BaseModel):
    """Result of describe_batch_load_task."""

    model_config = ConfigDict(frozen=True)

    batch_load_task_description: dict[str, Any] | None = None


class DescribeEndpointsResult(BaseModel):
    """Result of describe_endpoints."""

    model_config = ConfigDict(frozen=True)

    endpoints: list[dict[str, Any]] | None = None


class ListBatchLoadTasksResult(BaseModel):
    """Result of list_batch_load_tasks."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    batch_load_tasks: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None


def create_batch_load_task(
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
    client = get_client("timestream-write", region_name)
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
        resp = client.create_batch_load_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create batch load task") from exc
    return CreateBatchLoadTaskResult(
        task_id=resp.get("TaskId"),
    )


def describe_batch_load_task(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TaskId"] = task_id
    try:
        resp = client.describe_batch_load_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe batch load task") from exc
    return DescribeBatchLoadTaskResult(
        batch_load_task_description=resp.get("BatchLoadTaskDescription"),
    )


def describe_endpoints(
    region_name: str | None = None,
) -> DescribeEndpointsResult:
    """Describe endpoints.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoints") from exc
    return DescribeEndpointsResult(
        endpoints=resp.get("Endpoints"),
    )


def list_batch_load_tasks(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if task_status is not None:
        kwargs["TaskStatus"] = task_status
    try:
        resp = client.list_batch_load_tasks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list batch load tasks") from exc
    return ListBatchLoadTasksResult(
        next_token=resp.get("NextToken"),
        batch_load_tasks=resp.get("BatchLoadTasks"),
    )


def list_tags_for_resource(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


def resume_batch_load_task(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TaskId"] = task_id
    try:
        client.resume_batch_load_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to resume batch load task") from exc
    return None


def tag_resource(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
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
    client = get_client("timestream-write", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
