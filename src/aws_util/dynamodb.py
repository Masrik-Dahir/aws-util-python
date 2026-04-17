from __future__ import annotations

from typing import Any

import boto3
from boto3.dynamodb.conditions import Attr, ConditionBase, Key
from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "Attr",
    "BatchExecuteStatementResult",
    "BatchGetItemResult",
    "BatchWriteItemResult",
    "CreateBackupResult",
    "CreateGlobalTableResult",
    "CreateTableResult",
    "DeleteBackupResult",
    "DeleteResourcePolicyResult",
    "DeleteTableResult",
    "DescribeBackupResult",
    "DescribeContinuousBackupsResult",
    "DescribeContributorInsightsResult",
    "DescribeEndpointsResult",
    "DescribeExportResult",
    "DescribeGlobalTableResult",
    "DescribeGlobalTableSettingsResult",
    "DescribeImportResult",
    "DescribeKinesisStreamingDestinationResult",
    "DescribeLimitsResult",
    "DescribeTableReplicaAutoScalingResult",
    "DescribeTableResult",
    "DescribeTimeToLiveResult",
    "DisableKinesisStreamingDestinationResult",
    "DynamoKey",
    "EnableKinesisStreamingDestinationResult",
    "ExecuteStatementResult",
    "ExecuteTransactionResult",
    "ExportTableToPointInTimeResult",
    "GetResourcePolicyResult",
    "ImportTableResult",
    "Key",
    "ListBackupsResult",
    "ListContributorInsightsResult",
    "ListExportsResult",
    "ListGlobalTablesResult",
    "ListImportsResult",
    "ListTablesResult",
    "ListTagsOfResourceResult",
    "PutResourcePolicyResult",
    "RestoreTableFromBackupResult",
    "RestoreTableToPointInTimeResult",
    "TransactGetItemsResult",
    "TransactWriteItemsResult",
    "UpdateContinuousBackupsResult",
    "UpdateContributorInsightsResult",
    "UpdateGlobalTableResult",
    "UpdateGlobalTableSettingsResult",
    "UpdateKinesisStreamingDestinationResult",
    "UpdateTableReplicaAutoScalingResult",
    "UpdateTableResult",
    "UpdateTimeToLiveResult",
    "atomic_increment",
    "batch_execute_statement",
    "batch_get",
    "batch_get_item",
    "batch_write",
    "batch_write_item",
    "create_backup",
    "create_global_table",
    "create_table",
    "delete_backup",
    "delete_item",
    "delete_resource_policy",
    "delete_table",
    "describe_backup",
    "describe_continuous_backups",
    "describe_contributor_insights",
    "describe_endpoints",
    "describe_export",
    "describe_global_table",
    "describe_global_table_settings",
    "describe_import",
    "describe_kinesis_streaming_destination",
    "describe_limits",
    "describe_table",
    "describe_table_replica_auto_scaling",
    "describe_time_to_live",
    "disable_kinesis_streaming_destination",
    "enable_kinesis_streaming_destination",
    "execute_statement",
    "execute_transaction",
    "export_table_to_point_in_time",
    "get_item",
    "get_resource_policy",
    "import_table",
    "list_backups",
    "list_contributor_insights",
    "list_exports",
    "list_global_tables",
    "list_imports",
    "list_tables",
    "list_tags_of_resource",
    "put_if_not_exists",
    "put_item",
    "put_resource_policy",
    "query",
    "restore_table_from_backup",
    "restore_table_to_point_in_time",
    "scan",
    "tag_resource",
    "transact_get",
    "transact_get_items",
    "transact_write",
    "transact_write_items",
    "untag_resource",
    "update_continuous_backups",
    "update_contributor_insights",
    "update_global_table",
    "update_global_table_settings",
    "update_item",
    "update_item_raw",
    "update_kinesis_streaming_destination",
    "update_table",
    "update_table_replica_auto_scaling",
    "update_time_to_live",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class DynamoKey(BaseModel):
    """A DynamoDB primary key (partition key + optional sort key)."""

    model_config = ConfigDict(frozen=True)

    partition_key: str
    partition_value: Any
    sort_key: str | None = None
    sort_value: Any | None = None

    def as_dict(self) -> dict[str, Any]:
        """Return the key as a plain dict suitable for boto3 calls."""
        key: dict[str, Any] = {self.partition_key: self.partition_value}
        if self.sort_key is not None:
            key[self.sort_key] = self.sort_value
        return key


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _table_resource(table_name: str, region_name: str | None = None):
    """Return a boto3 DynamoDB Table resource (not a low-level client)."""
    kwargs: dict[str, str] = {}
    if region_name is not None:
        kwargs["region_name"] = region_name
    dynamodb = boto3.resource("dynamodb", **kwargs)  # type: ignore[call-overload]
    return dynamodb.Table(table_name)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def get_item(
    table_name: str,
    key: DynamoKey | dict[str, Any],
    consistent_read: bool = False,
    region_name: str | None = None,
) -> dict[str, Any] | None:
    """Fetch a single item by its primary key.

    Args:
        table_name: DynamoDB table name.
        key: Primary key as a :class:`DynamoKey` or plain dict.
        consistent_read: Use strongly consistent reads.  Defaults to
            eventually consistent.
        region_name: AWS region override.

    Returns:
        The item as a dict, or ``None`` if the key does not exist.

    Raises:
        RuntimeError: If the API call fails.
    """
    table = _table_resource(table_name, region_name)
    raw_key = key.as_dict() if isinstance(key, DynamoKey) else key
    try:
        resp = table.get_item(Key=raw_key, ConsistentRead=consistent_read)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"get_item failed on {table_name!r}") from exc
    return resp.get("Item")


def put_item(
    table_name: str,
    item: dict[str, Any],
    condition: ConditionBase | None = None,
    region_name: str | None = None,
) -> None:
    """Write (create or overwrite) an item in a DynamoDB table.

    Args:
        table_name: DynamoDB table name.
        item: Full item to write, including its primary key attributes.
        condition: Optional ``ConditionExpression`` that must be satisfied
            (e.g. ``Attr("version").eq(1)``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the write fails or the condition is not met.
    """
    table = _table_resource(table_name, region_name)
    kwargs: dict[str, Any] = {"Item": item}
    if condition is not None:
        kwargs["ConditionExpression"] = condition
    try:
        table.put_item(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"put_item failed on {table_name!r}") from exc


def update_item(
    table_name: str,
    key: DynamoKey | dict[str, Any],
    updates: dict[str, Any],
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update specific attributes of an existing item.

    Builds a ``SET`` expression automatically from the *updates* dict.
    All attribute names are aliased (e.g. ``#attr_0``, ``#attr_1``, ...)
    which handles DynamoDB reserved words automatically.

    Args:
        table_name: DynamoDB table name.
        key: Primary key of the item to update.
        updates: Mapping of attribute name -> new value.
        region_name: AWS region override.

    Returns:
        The item's updated attributes as a dict.

    Raises:
        RuntimeError: If the update fails.
    """
    table = _table_resource(table_name, region_name)
    raw_key = key.as_dict() if isinstance(key, DynamoKey) else key

    expr_parts = [f"#attr_{i} = :val_{i}" for i in range(len(updates))]
    update_expr = "SET " + ", ".join(expr_parts)
    names = {f"#attr_{i}": k for i, k in enumerate(updates)}
    values = {f":val_{i}": v for i, v in enumerate(updates.values())}

    try:
        resp = table.update_item(
            Key=raw_key,
            UpdateExpression=update_expr,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
            ReturnValues="ALL_NEW",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_item failed on {table_name!r}") from exc
    return resp.get("Attributes", {})


def update_item_raw(
    table_name: str,
    key: DynamoKey | dict[str, Any],
    update_expression: str,
    expression_attribute_names: dict[str, str] | None = None,
    expression_attribute_values: dict[str, Any] | None = None,
    condition_expression: str | ConditionBase | None = None,
    return_values: str = "ALL_NEW",
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update an item using a raw DynamoDB update expression.

    Use this for complex expressions that :func:`update_item` cannot
    build automatically, such as ``if_not_exists``, ``list_append``,
    ``ADD``, or ``REMOVE`` clauses.

    Example::

        update_item_raw(
            "my-table",
            {"pk": "order#1"},
            update_expression=(
                "SET #p = if_not_exists(#p, :zero) + :inc, "
                "#lu = :ts"
            ),
            expression_attribute_names={
                "#p": "processed_count",
                "#lu": "last_updated",
            },
            expression_attribute_values={
                ":zero": 0,
                ":inc": 1,
                ":ts": "2024-01-01T00:00:00Z",
            },
        )

    Args:
        table_name: DynamoDB table name.
        key: Primary key of the item to update.
        update_expression: Raw DynamoDB ``UpdateExpression`` string.
        expression_attribute_names: Alias mapping for attribute names
            (handles reserved words).
        expression_attribute_values: Value placeholders used in the
            expression.
        condition_expression: Optional condition that must be satisfied.
        return_values: Which attributes to return after the update.
            Defaults to ``"ALL_NEW"``.
        region_name: AWS region override.

    Returns:
        The item's attributes as a dict (shape depends on
        *return_values*).

    Raises:
        RuntimeError: If the update fails.
    """
    table = _table_resource(table_name, region_name)
    raw_key = key.as_dict() if isinstance(key, DynamoKey) else key

    kwargs: dict[str, Any] = {
        "Key": raw_key,
        "UpdateExpression": update_expression,
        "ReturnValues": return_values,
    }
    if expression_attribute_names:
        kwargs["ExpressionAttributeNames"] = expression_attribute_names
    if expression_attribute_values:
        kwargs["ExpressionAttributeValues"] = expression_attribute_values
    if condition_expression is not None:
        kwargs["ConditionExpression"] = condition_expression

    try:
        resp = table.update_item(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_item_raw failed on {table_name!r}") from exc
    return resp.get("Attributes", {})


def delete_item(
    table_name: str,
    key: DynamoKey | dict[str, Any],
    condition: ConditionBase | None = None,
    region_name: str | None = None,
) -> None:
    """Delete an item by its primary key.

    Args:
        table_name: DynamoDB table name.
        key: Primary key of the item to delete.
        condition: Optional ``ConditionExpression`` guard.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the deletion fails or the condition is not met.
    """
    table = _table_resource(table_name, region_name)
    raw_key = key.as_dict() if isinstance(key, DynamoKey) else key
    kwargs: dict[str, Any] = {"Key": raw_key}
    if condition is not None:
        kwargs["ConditionExpression"] = condition
    try:
        table.delete_item(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_item failed on {table_name!r}") from exc


def query(
    table_name: str,
    key_condition: ConditionBase,
    filter_condition: ConditionBase | None = None,
    index_name: str | None = None,
    limit: int | None = None,
    scan_index_forward: bool = True,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Query a table or GSI using a key condition expression.

    Handles pagination automatically unless *limit* is set.

    Args:
        table_name: DynamoDB table name.
        key_condition: A boto3 ``Key`` condition, e.g.
            ``Key("pk").eq("user#123")``.
        filter_condition: Optional post-filter ``Attr`` expression applied
            after the query.
        index_name: Name of the GSI or LSI to query.  Omit for the base table.
        limit: Maximum number of items to return across all pages.  ``None``
            returns all matching items.
        scan_index_forward: ``True`` (default) for ascending sort order,
            ``False`` for descending.
        region_name: AWS region override.

    Returns:
        A list of item dicts.

    Raises:
        RuntimeError: If the query fails.
    """
    table = _table_resource(table_name, region_name)
    kwargs: dict[str, Any] = {
        "KeyConditionExpression": key_condition,
        "ScanIndexForward": scan_index_forward,
    }
    if filter_condition is not None:
        kwargs["FilterExpression"] = filter_condition
    if index_name is not None:
        kwargs["IndexName"] = index_name

    items: list[dict[str, Any]] = []
    try:
        while True:
            resp = table.query(**kwargs)
            items.extend(resp.get("Items", []))
            if limit is not None and len(items) >= limit:
                return items[:limit]
            last_key = resp.get("LastEvaluatedKey")
            if not last_key:
                break
            kwargs["ExclusiveStartKey"] = last_key
    except ClientError as exc:
        raise wrap_aws_error(exc, f"query failed on {table_name!r}") from exc
    return items


def scan(
    table_name: str,
    filter_condition: ConditionBase | None = None,
    index_name: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Scan an entire table or GSI, optionally filtered.

    Full-table scans are expensive on large tables; prefer
    :func:`query` where possible.

    Args:
        table_name: DynamoDB table name.
        filter_condition: Optional ``Attr`` expression to filter items.
        index_name: GSI or LSI name.  Omit for the base table.
        limit: Maximum items to return.  ``None`` returns all items.
        region_name: AWS region override.

    Returns:
        A list of item dicts.

    Raises:
        RuntimeError: If the scan fails.
    """
    table = _table_resource(table_name, region_name)
    kwargs: dict[str, Any] = {}
    if filter_condition is not None:
        kwargs["FilterExpression"] = filter_condition
    if index_name is not None:
        kwargs["IndexName"] = index_name

    items: list[dict[str, Any]] = []
    try:
        while True:
            resp = table.scan(**kwargs)
            items.extend(resp.get("Items", []))
            if limit is not None and len(items) >= limit:
                return items[:limit]
            last_key = resp.get("LastEvaluatedKey")
            if not last_key:
                break
            kwargs["ExclusiveStartKey"] = last_key
    except ClientError as exc:
        raise wrap_aws_error(exc, f"scan failed on {table_name!r}") from exc
    return items


def batch_get(
    table_name: str,
    keys: list[DynamoKey | dict[str, Any]],
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Retrieve up to 100 items by key in a single batch request.

    Automatically retries unprocessed keys (throttling back-pressure).

    Args:
        table_name: DynamoDB table name.
        keys: List of primary keys (up to 100).
        region_name: AWS region override.

    Returns:
        A list of found items (order is not guaranteed by DynamoDB).

    Raises:
        RuntimeError: If the batch read fails.
        ValueError: If more than 100 keys are supplied.
    """
    if len(keys) > 100:
        raise ValueError("batch_get supports at most 100 keys per call")

    kwargs: dict[str, str] = {}
    if region_name is not None:
        kwargs["region_name"] = region_name
    dynamodb = boto3.resource("dynamodb", **kwargs)  # type: ignore[call-overload]

    raw_keys = [k.as_dict() if isinstance(k, DynamoKey) else k for k in keys]
    request = {table_name: {"Keys": raw_keys}}
    items: list[dict[str, Any]] = []

    try:
        while request:
            resp = dynamodb.batch_get_item(RequestItems=request)
            items.extend(resp.get("Responses", {}).get(table_name, []))
            request = resp.get("UnprocessedKeys", {})
    except ClientError as exc:
        raise wrap_aws_error(exc, f"batch_get failed on {table_name!r}") from exc
    return items


def batch_write(
    table_name: str,
    items: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Write up to 25 items per batch, retrying unprocessed items.

    Args:
        table_name: DynamoDB table name.
        items: Items to write.  Batches of 25 are sent automatically.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the batch write fails.
    """
    table = _table_resource(table_name, region_name)

    try:
        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"batch_write failed on {table_name!r}") from exc


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


def transact_write(
    operations: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Execute multiple write operations atomically (ACID transaction).

    Each operation is a dict in boto3 ``TransactWriteItems`` format, e.g.::

        {"Put":    {"TableName": "...", "Item": {...}}},
        {"Update": {"TableName": "...", "Key": {...}, "UpdateExpression": "..."}},
        {"Delete": {"TableName": "...", "Key": {...}}},
        {"ConditionCheck": {"TableName": "...", "Key": {...}, "ConditionExpression": "..."}}

    Args:
        operations: List of up to 100 write operation dicts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the transaction fails or a condition is not met.
        ValueError: If more than 100 operations are supplied.
    """
    if len(operations) > 100:
        raise ValueError("transact_write supports at most 100 operations")

    client = get_client("dynamodb", region_name)
    try:
        client.transact_write_items(TransactItems=operations)
    except ClientError as exc:
        raise wrap_aws_error(exc, "transact_write failed") from exc


def transact_get(
    items: list[dict[str, Any]],
    region_name: str | None = None,
) -> list[dict[str, Any] | None]:
    """Fetch multiple items atomically across tables (ACID read).

    Each entry is a dict with ``"TableName"`` and ``"Key"`` keys, matching
    the boto3 ``TransactGetItems`` format.

    .. note::

        Uses the low-level client API.  Number types are returned as
        ``Decimal`` which may differ from resource-layer deserialisation.

    Args:
        items: List of up to 100 ``{"Get": {"TableName": "...", "Key": {...}}}``
            dicts.
        region_name: AWS region override.

    Returns:
        A list of item dicts (or ``None`` for items that were not found),
        in the same order as *items*.

    Raises:
        RuntimeError: If the transaction fails.
        ValueError: If more than 100 items are requested.
    """
    if len(items) > 100:
        raise ValueError("transact_get supports at most 100 items")

    client = get_client("dynamodb", region_name)

    # Wrap plain dicts if caller used {TableName, Key} shorthand
    wrapped = [item if "Get" in item else {"Get": item} for item in items]
    try:
        resp = client.transact_get_items(TransactItems=wrapped)
    except ClientError as exc:
        raise wrap_aws_error(exc, "transact_get failed") from exc

    from boto3.dynamodb.types import TypeDeserializer

    deserializer = TypeDeserializer()

    results: list[dict[str, Any] | None] = []
    for entry in resp.get("Responses", []):
        if "Item" in entry:
            results.append({k: deserializer.deserialize(v) for k, v in entry["Item"].items()})
        else:
            results.append(None)
    return results


def atomic_increment(
    table_name: str,
    key: DynamoKey | dict[str, Any],
    attribute: str,
    amount: int = 1,
    region_name: str | None = None,
) -> int:
    """Atomically increment (or decrement) a numeric attribute.

    Creates the attribute with value *amount* if it does not exist.

    Args:
        table_name: DynamoDB table name.
        key: Primary key of the item.
        attribute: Name of the numeric attribute to increment.
        amount: Value to add (negative to decrement).  Defaults to ``1``.
        region_name: AWS region override.

    Returns:
        The new value of the attribute after the increment.

    Raises:
        RuntimeError: If the update fails.
    """
    table = _table_resource(table_name, region_name)
    raw_key = key.as_dict() if isinstance(key, DynamoKey) else key
    try:
        resp = table.update_item(
            Key=raw_key,
            UpdateExpression="ADD #attr :delta",
            ExpressionAttributeNames={"#attr": attribute},
            ExpressionAttributeValues={":delta": amount},
            ReturnValues="UPDATED_NEW",
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, f"atomic_increment failed on {table_name!r}.{attribute}") from exc
    return int(resp["Attributes"][attribute])


def put_if_not_exists(
    table_name: str,
    item: dict[str, Any],
    partition_key: str,
    region_name: str | None = None,
) -> bool:
    """Write an item only if the partition key does not already exist.

    Uses a ``ConditionExpression`` so the operation is atomic.

    Args:
        table_name: DynamoDB table name.
        item: Full item to write.
        partition_key: Name of the partition key attribute used in the
            condition check.
        region_name: AWS region override.

    Returns:
        ``True`` if the item was written, ``False`` if it already existed.

    Raises:
        RuntimeError: If the write fails for a reason other than the condition
            not being met.
    """
    table = _table_resource(table_name, region_name)
    try:
        table.put_item(
            Item=item,
            ConditionExpression=Attr(partition_key).not_exists(),
        )
        return True
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return False
        raise wrap_aws_error(exc, f"put_if_not_exists failed on {table_name!r}") from exc


class BatchExecuteStatementResult(BaseModel):
    """Result of batch_execute_statement."""

    model_config = ConfigDict(frozen=True)

    responses: list[dict[str, Any]] | None = None
    consumed_capacity: list[dict[str, Any]] | None = None


class BatchGetItemResult(BaseModel):
    """Result of batch_get_item."""

    model_config = ConfigDict(frozen=True)

    responses: dict[str, Any] | None = None
    unprocessed_keys: dict[str, Any] | None = None
    consumed_capacity: list[dict[str, Any]] | None = None


class BatchWriteItemResult(BaseModel):
    """Result of batch_write_item."""

    model_config = ConfigDict(frozen=True)

    unprocessed_items: dict[str, Any] | None = None
    item_collection_metrics: dict[str, Any] | None = None
    consumed_capacity: list[dict[str, Any]] | None = None


class CreateBackupResult(BaseModel):
    """Result of create_backup."""

    model_config = ConfigDict(frozen=True)

    backup_details: dict[str, Any] | None = None


class CreateGlobalTableResult(BaseModel):
    """Result of create_global_table."""

    model_config = ConfigDict(frozen=True)

    global_table_description: dict[str, Any] | None = None


class CreateTableResult(BaseModel):
    """Result of create_table."""

    model_config = ConfigDict(frozen=True)

    table_description: dict[str, Any] | None = None


class DeleteBackupResult(BaseModel):
    """Result of delete_backup."""

    model_config = ConfigDict(frozen=True)

    backup_description: dict[str, Any] | None = None


class DeleteResourcePolicyResult(BaseModel):
    """Result of delete_resource_policy."""

    model_config = ConfigDict(frozen=True)

    revision_id: str | None = None


class DeleteTableResult(BaseModel):
    """Result of delete_table."""

    model_config = ConfigDict(frozen=True)

    table_description: dict[str, Any] | None = None


class DescribeBackupResult(BaseModel):
    """Result of describe_backup."""

    model_config = ConfigDict(frozen=True)

    backup_description: dict[str, Any] | None = None


class DescribeContinuousBackupsResult(BaseModel):
    """Result of describe_continuous_backups."""

    model_config = ConfigDict(frozen=True)

    continuous_backups_description: dict[str, Any] | None = None


class DescribeContributorInsightsResult(BaseModel):
    """Result of describe_contributor_insights."""

    model_config = ConfigDict(frozen=True)

    table_name: str | None = None
    index_name: str | None = None
    contributor_insights_rule_list: list[str] | None = None
    contributor_insights_status: str | None = None
    last_update_date_time: str | None = None
    failure_exception: dict[str, Any] | None = None
    contributor_insights_mode: str | None = None


class DescribeEndpointsResult(BaseModel):
    """Result of describe_endpoints."""

    model_config = ConfigDict(frozen=True)

    endpoints: list[dict[str, Any]] | None = None


class DescribeExportResult(BaseModel):
    """Result of describe_export."""

    model_config = ConfigDict(frozen=True)

    export_description: dict[str, Any] | None = None


class DescribeGlobalTableResult(BaseModel):
    """Result of describe_global_table."""

    model_config = ConfigDict(frozen=True)

    global_table_description: dict[str, Any] | None = None


class DescribeGlobalTableSettingsResult(BaseModel):
    """Result of describe_global_table_settings."""

    model_config = ConfigDict(frozen=True)

    global_table_name: str | None = None
    replica_settings: list[dict[str, Any]] | None = None


class DescribeImportResult(BaseModel):
    """Result of describe_import."""

    model_config = ConfigDict(frozen=True)

    import_table_description: dict[str, Any] | None = None


class DescribeKinesisStreamingDestinationResult(BaseModel):
    """Result of describe_kinesis_streaming_destination."""

    model_config = ConfigDict(frozen=True)

    table_name: str | None = None
    kinesis_data_stream_destinations: list[dict[str, Any]] | None = None


class DescribeLimitsResult(BaseModel):
    """Result of describe_limits."""

    model_config = ConfigDict(frozen=True)

    account_max_read_capacity_units: int | None = None
    account_max_write_capacity_units: int | None = None
    table_max_read_capacity_units: int | None = None
    table_max_write_capacity_units: int | None = None


class DescribeTableResult(BaseModel):
    """Result of describe_table."""

    model_config = ConfigDict(frozen=True)

    table: dict[str, Any] | None = None


class DescribeTableReplicaAutoScalingResult(BaseModel):
    """Result of describe_table_replica_auto_scaling."""

    model_config = ConfigDict(frozen=True)

    table_auto_scaling_description: dict[str, Any] | None = None


class DescribeTimeToLiveResult(BaseModel):
    """Result of describe_time_to_live."""

    model_config = ConfigDict(frozen=True)

    time_to_live_description: dict[str, Any] | None = None


class DisableKinesisStreamingDestinationResult(BaseModel):
    """Result of disable_kinesis_streaming_destination."""

    model_config = ConfigDict(frozen=True)

    table_name: str | None = None
    stream_arn: str | None = None
    destination_status: str | None = None
    enable_kinesis_streaming_configuration: dict[str, Any] | None = None


class EnableKinesisStreamingDestinationResult(BaseModel):
    """Result of enable_kinesis_streaming_destination."""

    model_config = ConfigDict(frozen=True)

    table_name: str | None = None
    stream_arn: str | None = None
    destination_status: str | None = None
    enable_kinesis_streaming_configuration: dict[str, Any] | None = None


class ExecuteStatementResult(BaseModel):
    """Result of execute_statement."""

    model_config = ConfigDict(frozen=True)

    items: list[dict[str, Any]] | None = None
    next_token: str | None = None
    consumed_capacity: dict[str, Any] | None = None
    last_evaluated_key: dict[str, Any] | None = None


class ExecuteTransactionResult(BaseModel):
    """Result of execute_transaction."""

    model_config = ConfigDict(frozen=True)

    responses: list[dict[str, Any]] | None = None
    consumed_capacity: list[dict[str, Any]] | None = None


class ExportTableToPointInTimeResult(BaseModel):
    """Result of export_table_to_point_in_time."""

    model_config = ConfigDict(frozen=True)

    export_description: dict[str, Any] | None = None


class GetResourcePolicyResult(BaseModel):
    """Result of get_resource_policy."""

    model_config = ConfigDict(frozen=True)

    policy: str | None = None
    revision_id: str | None = None


class ImportTableResult(BaseModel):
    """Result of import_table."""

    model_config = ConfigDict(frozen=True)

    import_table_description: dict[str, Any] | None = None


class ListBackupsResult(BaseModel):
    """Result of list_backups."""

    model_config = ConfigDict(frozen=True)

    backup_summaries: list[dict[str, Any]] | None = None
    last_evaluated_backup_arn: str | None = None


class ListContributorInsightsResult(BaseModel):
    """Result of list_contributor_insights."""

    model_config = ConfigDict(frozen=True)

    contributor_insights_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListExportsResult(BaseModel):
    """Result of list_exports."""

    model_config = ConfigDict(frozen=True)

    export_summaries: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListGlobalTablesResult(BaseModel):
    """Result of list_global_tables."""

    model_config = ConfigDict(frozen=True)

    global_tables: list[dict[str, Any]] | None = None
    last_evaluated_global_table_name: str | None = None


class ListImportsResult(BaseModel):
    """Result of list_imports."""

    model_config = ConfigDict(frozen=True)

    import_summary_list: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTablesResult(BaseModel):
    """Result of list_tables."""

    model_config = ConfigDict(frozen=True)

    table_names: list[str] | None = None
    last_evaluated_table_name: str | None = None


class ListTagsOfResourceResult(BaseModel):
    """Result of list_tags_of_resource."""

    model_config = ConfigDict(frozen=True)

    tags: list[dict[str, Any]] | None = None
    next_token: str | None = None


class PutResourcePolicyResult(BaseModel):
    """Result of put_resource_policy."""

    model_config = ConfigDict(frozen=True)

    revision_id: str | None = None


class RestoreTableFromBackupResult(BaseModel):
    """Result of restore_table_from_backup."""

    model_config = ConfigDict(frozen=True)

    table_description: dict[str, Any] | None = None


class RestoreTableToPointInTimeResult(BaseModel):
    """Result of restore_table_to_point_in_time."""

    model_config = ConfigDict(frozen=True)

    table_description: dict[str, Any] | None = None


class TransactGetItemsResult(BaseModel):
    """Result of transact_get_items."""

    model_config = ConfigDict(frozen=True)

    consumed_capacity: list[dict[str, Any]] | None = None
    responses: list[dict[str, Any]] | None = None


class TransactWriteItemsResult(BaseModel):
    """Result of transact_write_items."""

    model_config = ConfigDict(frozen=True)

    consumed_capacity: list[dict[str, Any]] | None = None
    item_collection_metrics: dict[str, Any] | None = None


class UpdateContinuousBackupsResult(BaseModel):
    """Result of update_continuous_backups."""

    model_config = ConfigDict(frozen=True)

    continuous_backups_description: dict[str, Any] | None = None


class UpdateContributorInsightsResult(BaseModel):
    """Result of update_contributor_insights."""

    model_config = ConfigDict(frozen=True)

    table_name: str | None = None
    index_name: str | None = None
    contributor_insights_status: str | None = None
    contributor_insights_mode: str | None = None


class UpdateGlobalTableResult(BaseModel):
    """Result of update_global_table."""

    model_config = ConfigDict(frozen=True)

    global_table_description: dict[str, Any] | None = None


class UpdateGlobalTableSettingsResult(BaseModel):
    """Result of update_global_table_settings."""

    model_config = ConfigDict(frozen=True)

    global_table_name: str | None = None
    replica_settings: list[dict[str, Any]] | None = None


class UpdateKinesisStreamingDestinationResult(BaseModel):
    """Result of update_kinesis_streaming_destination."""

    model_config = ConfigDict(frozen=True)

    table_name: str | None = None
    stream_arn: str | None = None
    destination_status: str | None = None
    update_kinesis_streaming_configuration: dict[str, Any] | None = None


class UpdateTableResult(BaseModel):
    """Result of update_table."""

    model_config = ConfigDict(frozen=True)

    table_description: dict[str, Any] | None = None


class UpdateTableReplicaAutoScalingResult(BaseModel):
    """Result of update_table_replica_auto_scaling."""

    model_config = ConfigDict(frozen=True)

    table_auto_scaling_description: dict[str, Any] | None = None


class UpdateTimeToLiveResult(BaseModel):
    """Result of update_time_to_live."""

    model_config = ConfigDict(frozen=True)

    time_to_live_specification: dict[str, Any] | None = None


def batch_execute_statement(
    statements: list[dict[str, Any]],
    *,
    return_consumed_capacity: str | None = None,
    region_name: str | None = None,
) -> BatchExecuteStatementResult:
    """Batch execute statement.

    Args:
        statements: Statements.
        return_consumed_capacity: Return consumed capacity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Statements"] = statements
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    try:
        resp = client.batch_execute_statement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch execute statement") from exc
    return BatchExecuteStatementResult(
        responses=resp.get("Responses"),
        consumed_capacity=resp.get("ConsumedCapacity"),
    )


def batch_get_item(
    request_items: dict[str, Any],
    *,
    return_consumed_capacity: str | None = None,
    region_name: str | None = None,
) -> BatchGetItemResult:
    """Batch get item.

    Args:
        request_items: Request items.
        return_consumed_capacity: Return consumed capacity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RequestItems"] = request_items
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    try:
        resp = client.batch_get_item(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch get item") from exc
    return BatchGetItemResult(
        responses=resp.get("Responses"),
        unprocessed_keys=resp.get("UnprocessedKeys"),
        consumed_capacity=resp.get("ConsumedCapacity"),
    )


def batch_write_item(
    request_items: dict[str, Any],
    *,
    return_consumed_capacity: str | None = None,
    return_item_collection_metrics: str | None = None,
    region_name: str | None = None,
) -> BatchWriteItemResult:
    """Batch write item.

    Args:
        request_items: Request items.
        return_consumed_capacity: Return consumed capacity.
        return_item_collection_metrics: Return item collection metrics.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RequestItems"] = request_items
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    if return_item_collection_metrics is not None:
        kwargs["ReturnItemCollectionMetrics"] = return_item_collection_metrics
    try:
        resp = client.batch_write_item(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to batch write item") from exc
    return BatchWriteItemResult(
        unprocessed_items=resp.get("UnprocessedItems"),
        item_collection_metrics=resp.get("ItemCollectionMetrics"),
        consumed_capacity=resp.get("ConsumedCapacity"),
    )


def create_backup(
    table_name: str,
    backup_name: str,
    region_name: str | None = None,
) -> CreateBackupResult:
    """Create backup.

    Args:
        table_name: Table name.
        backup_name: Backup name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["BackupName"] = backup_name
    try:
        resp = client.create_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create backup") from exc
    return CreateBackupResult(
        backup_details=resp.get("BackupDetails"),
    )


def create_global_table(
    global_table_name: str,
    replication_group: list[dict[str, Any]],
    region_name: str | None = None,
) -> CreateGlobalTableResult:
    """Create global table.

    Args:
        global_table_name: Global table name.
        replication_group: Replication group.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalTableName"] = global_table_name
    kwargs["ReplicationGroup"] = replication_group
    try:
        resp = client.create_global_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create global table") from exc
    return CreateGlobalTableResult(
        global_table_description=resp.get("GlobalTableDescription"),
    )


def create_table(
    attribute_definitions: list[dict[str, Any]],
    table_name: str,
    key_schema: list[dict[str, Any]],
    *,
    local_secondary_indexes: list[dict[str, Any]] | None = None,
    global_secondary_indexes: list[dict[str, Any]] | None = None,
    billing_mode: str | None = None,
    provisioned_throughput: dict[str, Any] | None = None,
    stream_specification: dict[str, Any] | None = None,
    sse_specification: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    table_class: str | None = None,
    deletion_protection_enabled: bool | None = None,
    warm_throughput: dict[str, Any] | None = None,
    resource_policy: str | None = None,
    on_demand_throughput: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateTableResult:
    """Create table.

    Args:
        attribute_definitions: Attribute definitions.
        table_name: Table name.
        key_schema: Key schema.
        local_secondary_indexes: Local secondary indexes.
        global_secondary_indexes: Global secondary indexes.
        billing_mode: Billing mode.
        provisioned_throughput: Provisioned throughput.
        stream_specification: Stream specification.
        sse_specification: Sse specification.
        tags: Tags.
        table_class: Table class.
        deletion_protection_enabled: Deletion protection enabled.
        warm_throughput: Warm throughput.
        resource_policy: Resource policy.
        on_demand_throughput: On demand throughput.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["AttributeDefinitions"] = attribute_definitions
    kwargs["TableName"] = table_name
    kwargs["KeySchema"] = key_schema
    if local_secondary_indexes is not None:
        kwargs["LocalSecondaryIndexes"] = local_secondary_indexes
    if global_secondary_indexes is not None:
        kwargs["GlobalSecondaryIndexes"] = global_secondary_indexes
    if billing_mode is not None:
        kwargs["BillingMode"] = billing_mode
    if provisioned_throughput is not None:
        kwargs["ProvisionedThroughput"] = provisioned_throughput
    if stream_specification is not None:
        kwargs["StreamSpecification"] = stream_specification
    if sse_specification is not None:
        kwargs["SSESpecification"] = sse_specification
    if tags is not None:
        kwargs["Tags"] = tags
    if table_class is not None:
        kwargs["TableClass"] = table_class
    if deletion_protection_enabled is not None:
        kwargs["DeletionProtectionEnabled"] = deletion_protection_enabled
    if warm_throughput is not None:
        kwargs["WarmThroughput"] = warm_throughput
    if resource_policy is not None:
        kwargs["ResourcePolicy"] = resource_policy
    if on_demand_throughput is not None:
        kwargs["OnDemandThroughput"] = on_demand_throughput
    try:
        resp = client.create_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create table") from exc
    return CreateTableResult(
        table_description=resp.get("TableDescription"),
    )


def delete_backup(
    backup_arn: str,
    region_name: str | None = None,
) -> DeleteBackupResult:
    """Delete backup.

    Args:
        backup_arn: Backup arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BackupArn"] = backup_arn
    try:
        resp = client.delete_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete backup") from exc
    return DeleteBackupResult(
        backup_description=resp.get("BackupDescription"),
    )


def delete_resource_policy(
    resource_arn: str,
    *,
    expected_revision_id: str | None = None,
    region_name: str | None = None,
) -> DeleteResourcePolicyResult:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        expected_revision_id: Expected revision id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if expected_revision_id is not None:
        kwargs["ExpectedRevisionId"] = expected_revision_id
    try:
        resp = client.delete_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return DeleteResourcePolicyResult(
        revision_id=resp.get("RevisionId"),
    )


def delete_table(
    table_name: str,
    region_name: str | None = None,
) -> DeleteTableResult:
    """Delete table.

    Args:
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    try:
        resp = client.delete_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete table") from exc
    return DeleteTableResult(
        table_description=resp.get("TableDescription"),
    )


def describe_backup(
    backup_arn: str,
    region_name: str | None = None,
) -> DescribeBackupResult:
    """Describe backup.

    Args:
        backup_arn: Backup arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BackupArn"] = backup_arn
    try:
        resp = client.describe_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe backup") from exc
    return DescribeBackupResult(
        backup_description=resp.get("BackupDescription"),
    )


def describe_continuous_backups(
    table_name: str,
    region_name: str | None = None,
) -> DescribeContinuousBackupsResult:
    """Describe continuous backups.

    Args:
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    try:
        resp = client.describe_continuous_backups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe continuous backups") from exc
    return DescribeContinuousBackupsResult(
        continuous_backups_description=resp.get("ContinuousBackupsDescription"),
    )


def describe_contributor_insights(
    table_name: str,
    *,
    index_name: str | None = None,
    region_name: str | None = None,
) -> DescribeContributorInsightsResult:
    """Describe contributor insights.

    Args:
        table_name: Table name.
        index_name: Index name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    if index_name is not None:
        kwargs["IndexName"] = index_name
    try:
        resp = client.describe_contributor_insights(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe contributor insights") from exc
    return DescribeContributorInsightsResult(
        table_name=resp.get("TableName"),
        index_name=resp.get("IndexName"),
        contributor_insights_rule_list=resp.get("ContributorInsightsRuleList"),
        contributor_insights_status=resp.get("ContributorInsightsStatus"),
        last_update_date_time=resp.get("LastUpdateDateTime"),
        failure_exception=resp.get("FailureException"),
        contributor_insights_mode=resp.get("ContributorInsightsMode"),
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
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe endpoints") from exc
    return DescribeEndpointsResult(
        endpoints=resp.get("Endpoints"),
    )


def describe_export(
    export_arn: str,
    region_name: str | None = None,
) -> DescribeExportResult:
    """Describe export.

    Args:
        export_arn: Export arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ExportArn"] = export_arn
    try:
        resp = client.describe_export(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe export") from exc
    return DescribeExportResult(
        export_description=resp.get("ExportDescription"),
    )


def describe_global_table(
    global_table_name: str,
    region_name: str | None = None,
) -> DescribeGlobalTableResult:
    """Describe global table.

    Args:
        global_table_name: Global table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalTableName"] = global_table_name
    try:
        resp = client.describe_global_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe global table") from exc
    return DescribeGlobalTableResult(
        global_table_description=resp.get("GlobalTableDescription"),
    )


def describe_global_table_settings(
    global_table_name: str,
    region_name: str | None = None,
) -> DescribeGlobalTableSettingsResult:
    """Describe global table settings.

    Args:
        global_table_name: Global table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalTableName"] = global_table_name
    try:
        resp = client.describe_global_table_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe global table settings") from exc
    return DescribeGlobalTableSettingsResult(
        global_table_name=resp.get("GlobalTableName"),
        replica_settings=resp.get("ReplicaSettings"),
    )


def describe_import(
    import_arn: str,
    region_name: str | None = None,
) -> DescribeImportResult:
    """Describe import.

    Args:
        import_arn: Import arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ImportArn"] = import_arn
    try:
        resp = client.describe_import(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe import") from exc
    return DescribeImportResult(
        import_table_description=resp.get("ImportTableDescription"),
    )


def describe_kinesis_streaming_destination(
    table_name: str,
    region_name: str | None = None,
) -> DescribeKinesisStreamingDestinationResult:
    """Describe kinesis streaming destination.

    Args:
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    try:
        resp = client.describe_kinesis_streaming_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe kinesis streaming destination") from exc
    return DescribeKinesisStreamingDestinationResult(
        table_name=resp.get("TableName"),
        kinesis_data_stream_destinations=resp.get("KinesisDataStreamDestinations"),
    )


def describe_limits(
    region_name: str | None = None,
) -> DescribeLimitsResult:
    """Describe limits.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = client.describe_limits(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe limits") from exc
    return DescribeLimitsResult(
        account_max_read_capacity_units=resp.get("AccountMaxReadCapacityUnits"),
        account_max_write_capacity_units=resp.get("AccountMaxWriteCapacityUnits"),
        table_max_read_capacity_units=resp.get("TableMaxReadCapacityUnits"),
        table_max_write_capacity_units=resp.get("TableMaxWriteCapacityUnits"),
    )


def describe_table(
    table_name: str,
    region_name: str | None = None,
) -> DescribeTableResult:
    """Describe table.

    Args:
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    try:
        resp = client.describe_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe table") from exc
    return DescribeTableResult(
        table=resp.get("Table"),
    )


def describe_table_replica_auto_scaling(
    table_name: str,
    region_name: str | None = None,
) -> DescribeTableReplicaAutoScalingResult:
    """Describe table replica auto scaling.

    Args:
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    try:
        resp = client.describe_table_replica_auto_scaling(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe table replica auto scaling") from exc
    return DescribeTableReplicaAutoScalingResult(
        table_auto_scaling_description=resp.get("TableAutoScalingDescription"),
    )


def describe_time_to_live(
    table_name: str,
    region_name: str | None = None,
) -> DescribeTimeToLiveResult:
    """Describe time to live.

    Args:
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    try:
        resp = client.describe_time_to_live(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe time to live") from exc
    return DescribeTimeToLiveResult(
        time_to_live_description=resp.get("TimeToLiveDescription"),
    )


def disable_kinesis_streaming_destination(
    table_name: str,
    stream_arn: str,
    *,
    enable_kinesis_streaming_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> DisableKinesisStreamingDestinationResult:
    """Disable kinesis streaming destination.

    Args:
        table_name: Table name.
        stream_arn: Stream arn.
        enable_kinesis_streaming_configuration: Enable kinesis streaming configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["StreamArn"] = stream_arn
    if enable_kinesis_streaming_configuration is not None:
        kwargs["EnableKinesisStreamingConfiguration"] = enable_kinesis_streaming_configuration
    try:
        resp = client.disable_kinesis_streaming_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disable kinesis streaming destination") from exc
    return DisableKinesisStreamingDestinationResult(
        table_name=resp.get("TableName"),
        stream_arn=resp.get("StreamArn"),
        destination_status=resp.get("DestinationStatus"),
        enable_kinesis_streaming_configuration=resp.get("EnableKinesisStreamingConfiguration"),
    )


def enable_kinesis_streaming_destination(
    table_name: str,
    stream_arn: str,
    *,
    enable_kinesis_streaming_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> EnableKinesisStreamingDestinationResult:
    """Enable kinesis streaming destination.

    Args:
        table_name: Table name.
        stream_arn: Stream arn.
        enable_kinesis_streaming_configuration: Enable kinesis streaming configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["StreamArn"] = stream_arn
    if enable_kinesis_streaming_configuration is not None:
        kwargs["EnableKinesisStreamingConfiguration"] = enable_kinesis_streaming_configuration
    try:
        resp = client.enable_kinesis_streaming_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to enable kinesis streaming destination") from exc
    return EnableKinesisStreamingDestinationResult(
        table_name=resp.get("TableName"),
        stream_arn=resp.get("StreamArn"),
        destination_status=resp.get("DestinationStatus"),
        enable_kinesis_streaming_configuration=resp.get("EnableKinesisStreamingConfiguration"),
    )


def execute_statement(
    statement: str,
    *,
    parameters: list[dict[str, Any]] | None = None,
    consistent_read: bool | None = None,
    next_token: str | None = None,
    return_consumed_capacity: str | None = None,
    limit: int | None = None,
    return_values_on_condition_check_failure: str | None = None,
    region_name: str | None = None,
) -> ExecuteStatementResult:
    """Execute statement.

    Args:
        statement: Statement.
        parameters: Parameters.
        consistent_read: Consistent read.
        next_token: Next token.
        return_consumed_capacity: Return consumed capacity.
        limit: Limit.
        return_values_on_condition_check_failure: Return values on condition check failure.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Statement"] = statement
    if parameters is not None:
        kwargs["Parameters"] = parameters
    if consistent_read is not None:
        kwargs["ConsistentRead"] = consistent_read
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    if limit is not None:
        kwargs["Limit"] = limit
    if return_values_on_condition_check_failure is not None:
        kwargs["ReturnValuesOnConditionCheckFailure"] = return_values_on_condition_check_failure
    try:
        resp = client.execute_statement(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute statement") from exc
    return ExecuteStatementResult(
        items=resp.get("Items"),
        next_token=resp.get("NextToken"),
        consumed_capacity=resp.get("ConsumedCapacity"),
        last_evaluated_key=resp.get("LastEvaluatedKey"),
    )


def execute_transaction(
    transact_statements: list[dict[str, Any]],
    *,
    client_request_token: str | None = None,
    return_consumed_capacity: str | None = None,
    region_name: str | None = None,
) -> ExecuteTransactionResult:
    """Execute transaction.

    Args:
        transact_statements: Transact statements.
        client_request_token: Client request token.
        return_consumed_capacity: Return consumed capacity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransactStatements"] = transact_statements
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    try:
        resp = client.execute_transaction(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute transaction") from exc
    return ExecuteTransactionResult(
        responses=resp.get("Responses"),
        consumed_capacity=resp.get("ConsumedCapacity"),
    )


def export_table_to_point_in_time(
    table_arn: str,
    s3_bucket: str,
    *,
    export_time: str | None = None,
    client_token: str | None = None,
    s3_bucket_owner: str | None = None,
    s3_prefix: str | None = None,
    s3_sse_algorithm: str | None = None,
    s3_sse_kms_key_id: str | None = None,
    export_format: str | None = None,
    export_type: str | None = None,
    incremental_export_specification: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> ExportTableToPointInTimeResult:
    """Export table to point in time.

    Args:
        table_arn: Table arn.
        s3_bucket: S3 bucket.
        export_time: Export time.
        client_token: Client token.
        s3_bucket_owner: S3 bucket owner.
        s3_prefix: S3 prefix.
        s3_sse_algorithm: S3 sse algorithm.
        s3_sse_kms_key_id: S3 sse kms key id.
        export_format: Export format.
        export_type: Export type.
        incremental_export_specification: Incremental export specification.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableArn"] = table_arn
    kwargs["S3Bucket"] = s3_bucket
    if export_time is not None:
        kwargs["ExportTime"] = export_time
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if s3_bucket_owner is not None:
        kwargs["S3BucketOwner"] = s3_bucket_owner
    if s3_prefix is not None:
        kwargs["S3Prefix"] = s3_prefix
    if s3_sse_algorithm is not None:
        kwargs["S3SseAlgorithm"] = s3_sse_algorithm
    if s3_sse_kms_key_id is not None:
        kwargs["S3SseKmsKeyId"] = s3_sse_kms_key_id
    if export_format is not None:
        kwargs["ExportFormat"] = export_format
    if export_type is not None:
        kwargs["ExportType"] = export_type
    if incremental_export_specification is not None:
        kwargs["IncrementalExportSpecification"] = incremental_export_specification
    try:
        resp = client.export_table_to_point_in_time(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to export table to point in time") from exc
    return ExportTableToPointInTimeResult(
        export_description=resp.get("ExportDescription"),
    )


def get_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = client.get_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        policy=resp.get("Policy"),
        revision_id=resp.get("RevisionId"),
    )


def import_table(
    s3_bucket_source: dict[str, Any],
    input_format: str,
    table_creation_parameters: dict[str, Any],
    *,
    client_token: str | None = None,
    input_format_options: dict[str, Any] | None = None,
    input_compression_type: str | None = None,
    region_name: str | None = None,
) -> ImportTableResult:
    """Import table.

    Args:
        s3_bucket_source: S3 bucket source.
        input_format: Input format.
        table_creation_parameters: Table creation parameters.
        client_token: Client token.
        input_format_options: Input format options.
        input_compression_type: Input compression type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["S3BucketSource"] = s3_bucket_source
    kwargs["InputFormat"] = input_format
    kwargs["TableCreationParameters"] = table_creation_parameters
    if client_token is not None:
        kwargs["ClientToken"] = client_token
    if input_format_options is not None:
        kwargs["InputFormatOptions"] = input_format_options
    if input_compression_type is not None:
        kwargs["InputCompressionType"] = input_compression_type
    try:
        resp = client.import_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to import table") from exc
    return ImportTableResult(
        import_table_description=resp.get("ImportTableDescription"),
    )


def list_backups(
    *,
    table_name: str | None = None,
    limit: int | None = None,
    time_range_lower_bound: str | None = None,
    time_range_upper_bound: str | None = None,
    exclusive_start_backup_arn: str | None = None,
    backup_type: str | None = None,
    region_name: str | None = None,
) -> ListBackupsResult:
    """List backups.

    Args:
        table_name: Table name.
        limit: Limit.
        time_range_lower_bound: Time range lower bound.
        time_range_upper_bound: Time range upper bound.
        exclusive_start_backup_arn: Exclusive start backup arn.
        backup_type: Backup type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    if table_name is not None:
        kwargs["TableName"] = table_name
    if limit is not None:
        kwargs["Limit"] = limit
    if time_range_lower_bound is not None:
        kwargs["TimeRangeLowerBound"] = time_range_lower_bound
    if time_range_upper_bound is not None:
        kwargs["TimeRangeUpperBound"] = time_range_upper_bound
    if exclusive_start_backup_arn is not None:
        kwargs["ExclusiveStartBackupArn"] = exclusive_start_backup_arn
    if backup_type is not None:
        kwargs["BackupType"] = backup_type
    try:
        resp = client.list_backups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list backups") from exc
    return ListBackupsResult(
        backup_summaries=resp.get("BackupSummaries"),
        last_evaluated_backup_arn=resp.get("LastEvaluatedBackupArn"),
    )


def list_contributor_insights(
    *,
    table_name: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListContributorInsightsResult:
    """List contributor insights.

    Args:
        table_name: Table name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    if table_name is not None:
        kwargs["TableName"] = table_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    try:
        resp = client.list_contributor_insights(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list contributor insights") from exc
    return ListContributorInsightsResult(
        contributor_insights_summaries=resp.get("ContributorInsightsSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_exports(
    *,
    table_arn: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListExportsResult:
    """List exports.

    Args:
        table_arn: Table arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    if table_arn is not None:
        kwargs["TableArn"] = table_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_exports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list exports") from exc
    return ListExportsResult(
        export_summaries=resp.get("ExportSummaries"),
        next_token=resp.get("NextToken"),
    )


def list_global_tables(
    *,
    exclusive_start_global_table_name: str | None = None,
    limit: int | None = None,
    target_region_name: str | None = None,
    region_name: str | None = None,
) -> ListGlobalTablesResult:
    """List global tables.

    Args:
        exclusive_start_global_table_name: Exclusive start global table name.
        limit: Limit.
        target_region_name: Target region name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    if exclusive_start_global_table_name is not None:
        kwargs["ExclusiveStartGlobalTableName"] = exclusive_start_global_table_name
    if limit is not None:
        kwargs["Limit"] = limit
    if target_region_name is not None:
        kwargs["RegionName"] = target_region_name
    try:
        resp = client.list_global_tables(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list global tables") from exc
    return ListGlobalTablesResult(
        global_tables=resp.get("GlobalTables"),
        last_evaluated_global_table_name=resp.get("LastEvaluatedGlobalTableName"),
    )


def list_imports(
    *,
    table_arn: str | None = None,
    page_size: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListImportsResult:
    """List imports.

    Args:
        table_arn: Table arn.
        page_size: Page size.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    if table_arn is not None:
        kwargs["TableArn"] = table_arn
    if page_size is not None:
        kwargs["PageSize"] = page_size
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_imports(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list imports") from exc
    return ListImportsResult(
        import_summary_list=resp.get("ImportSummaryList"),
        next_token=resp.get("NextToken"),
    )


def list_tables(
    *,
    exclusive_start_table_name: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListTablesResult:
    """List tables.

    Args:
        exclusive_start_table_name: Exclusive start table name.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    if exclusive_start_table_name is not None:
        kwargs["ExclusiveStartTableName"] = exclusive_start_table_name
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = client.list_tables(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tables") from exc
    return ListTablesResult(
        table_names=resp.get("TableNames"),
        last_evaluated_table_name=resp.get("LastEvaluatedTableName"),
    )


def list_tags_of_resource(
    resource_arn: str,
    *,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListTagsOfResourceResult:
    """List tags of resource.

    Args:
        resource_arn: Resource arn.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = client.list_tags_of_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags of resource") from exc
    return ListTagsOfResourceResult(
        tags=resp.get("Tags"),
        next_token=resp.get("NextToken"),
    )


def put_resource_policy(
    resource_arn: str,
    policy: str,
    *,
    expected_revision_id: str | None = None,
    confirm_remove_self_resource_access: bool | None = None,
    region_name: str | None = None,
) -> PutResourcePolicyResult:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        expected_revision_id: Expected revision id.
        confirm_remove_self_resource_access: Confirm remove self resource access.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Policy"] = policy
    if expected_revision_id is not None:
        kwargs["ExpectedRevisionId"] = expected_revision_id
    if confirm_remove_self_resource_access is not None:
        kwargs["ConfirmRemoveSelfResourceAccess"] = confirm_remove_self_resource_access
    try:
        resp = client.put_resource_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return PutResourcePolicyResult(
        revision_id=resp.get("RevisionId"),
    )


def restore_table_from_backup(
    target_table_name: str,
    backup_arn: str,
    *,
    billing_mode_override: str | None = None,
    global_secondary_index_override: list[dict[str, Any]] | None = None,
    local_secondary_index_override: list[dict[str, Any]] | None = None,
    provisioned_throughput_override: dict[str, Any] | None = None,
    on_demand_throughput_override: dict[str, Any] | None = None,
    sse_specification_override: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RestoreTableFromBackupResult:
    """Restore table from backup.

    Args:
        target_table_name: Target table name.
        backup_arn: Backup arn.
        billing_mode_override: Billing mode override.
        global_secondary_index_override: Global secondary index override.
        local_secondary_index_override: Local secondary index override.
        provisioned_throughput_override: Provisioned throughput override.
        on_demand_throughput_override: On demand throughput override.
        sse_specification_override: Sse specification override.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetTableName"] = target_table_name
    kwargs["BackupArn"] = backup_arn
    if billing_mode_override is not None:
        kwargs["BillingModeOverride"] = billing_mode_override
    if global_secondary_index_override is not None:
        kwargs["GlobalSecondaryIndexOverride"] = global_secondary_index_override
    if local_secondary_index_override is not None:
        kwargs["LocalSecondaryIndexOverride"] = local_secondary_index_override
    if provisioned_throughput_override is not None:
        kwargs["ProvisionedThroughputOverride"] = provisioned_throughput_override
    if on_demand_throughput_override is not None:
        kwargs["OnDemandThroughputOverride"] = on_demand_throughput_override
    if sse_specification_override is not None:
        kwargs["SSESpecificationOverride"] = sse_specification_override
    try:
        resp = client.restore_table_from_backup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore table from backup") from exc
    return RestoreTableFromBackupResult(
        table_description=resp.get("TableDescription"),
    )


def restore_table_to_point_in_time(
    target_table_name: str,
    *,
    source_table_arn: str | None = None,
    source_table_name: str | None = None,
    use_latest_restorable_time: bool | None = None,
    restore_date_time: str | None = None,
    billing_mode_override: str | None = None,
    global_secondary_index_override: list[dict[str, Any]] | None = None,
    local_secondary_index_override: list[dict[str, Any]] | None = None,
    provisioned_throughput_override: dict[str, Any] | None = None,
    on_demand_throughput_override: dict[str, Any] | None = None,
    sse_specification_override: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RestoreTableToPointInTimeResult:
    """Restore table to point in time.

    Args:
        target_table_name: Target table name.
        source_table_arn: Source table arn.
        source_table_name: Source table name.
        use_latest_restorable_time: Use latest restorable time.
        restore_date_time: Restore date time.
        billing_mode_override: Billing mode override.
        global_secondary_index_override: Global secondary index override.
        local_secondary_index_override: Local secondary index override.
        provisioned_throughput_override: Provisioned throughput override.
        on_demand_throughput_override: On demand throughput override.
        sse_specification_override: Sse specification override.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetTableName"] = target_table_name
    if source_table_arn is not None:
        kwargs["SourceTableArn"] = source_table_arn
    if source_table_name is not None:
        kwargs["SourceTableName"] = source_table_name
    if use_latest_restorable_time is not None:
        kwargs["UseLatestRestorableTime"] = use_latest_restorable_time
    if restore_date_time is not None:
        kwargs["RestoreDateTime"] = restore_date_time
    if billing_mode_override is not None:
        kwargs["BillingModeOverride"] = billing_mode_override
    if global_secondary_index_override is not None:
        kwargs["GlobalSecondaryIndexOverride"] = global_secondary_index_override
    if local_secondary_index_override is not None:
        kwargs["LocalSecondaryIndexOverride"] = local_secondary_index_override
    if provisioned_throughput_override is not None:
        kwargs["ProvisionedThroughputOverride"] = provisioned_throughput_override
    if on_demand_throughput_override is not None:
        kwargs["OnDemandThroughputOverride"] = on_demand_throughput_override
    if sse_specification_override is not None:
        kwargs["SSESpecificationOverride"] = sse_specification_override
    try:
        resp = client.restore_table_to_point_in_time(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore table to point in time") from exc
    return RestoreTableToPointInTimeResult(
        table_description=resp.get("TableDescription"),
    )


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
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def transact_get_items(
    transact_items: list[dict[str, Any]],
    *,
    return_consumed_capacity: str | None = None,
    region_name: str | None = None,
) -> TransactGetItemsResult:
    """Transact get items.

    Args:
        transact_items: Transact items.
        return_consumed_capacity: Return consumed capacity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransactItems"] = transact_items
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    try:
        resp = client.transact_get_items(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to transact get items") from exc
    return TransactGetItemsResult(
        consumed_capacity=resp.get("ConsumedCapacity"),
        responses=resp.get("Responses"),
    )


def transact_write_items(
    transact_items: list[dict[str, Any]],
    *,
    return_consumed_capacity: str | None = None,
    return_item_collection_metrics: str | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> TransactWriteItemsResult:
    """Transact write items.

    Args:
        transact_items: Transact items.
        return_consumed_capacity: Return consumed capacity.
        return_item_collection_metrics: Return item collection metrics.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TransactItems"] = transact_items
    if return_consumed_capacity is not None:
        kwargs["ReturnConsumedCapacity"] = return_consumed_capacity
    if return_item_collection_metrics is not None:
        kwargs["ReturnItemCollectionMetrics"] = return_item_collection_metrics
    if client_request_token is not None:
        kwargs["ClientRequestToken"] = client_request_token
    try:
        resp = client.transact_write_items(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to transact write items") from exc
    return TransactWriteItemsResult(
        consumed_capacity=resp.get("ConsumedCapacity"),
        item_collection_metrics=resp.get("ItemCollectionMetrics"),
    )


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
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_continuous_backups(
    table_name: str,
    point_in_time_recovery_specification: dict[str, Any],
    region_name: str | None = None,
) -> UpdateContinuousBackupsResult:
    """Update continuous backups.

    Args:
        table_name: Table name.
        point_in_time_recovery_specification: Point in time recovery specification.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["PointInTimeRecoverySpecification"] = point_in_time_recovery_specification
    try:
        resp = client.update_continuous_backups(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update continuous backups") from exc
    return UpdateContinuousBackupsResult(
        continuous_backups_description=resp.get("ContinuousBackupsDescription"),
    )


def update_contributor_insights(
    table_name: str,
    contributor_insights_action: str,
    *,
    index_name: str | None = None,
    contributor_insights_mode: str | None = None,
    region_name: str | None = None,
) -> UpdateContributorInsightsResult:
    """Update contributor insights.

    Args:
        table_name: Table name.
        contributor_insights_action: Contributor insights action.
        index_name: Index name.
        contributor_insights_mode: Contributor insights mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["ContributorInsightsAction"] = contributor_insights_action
    if index_name is not None:
        kwargs["IndexName"] = index_name
    if contributor_insights_mode is not None:
        kwargs["ContributorInsightsMode"] = contributor_insights_mode
    try:
        resp = client.update_contributor_insights(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update contributor insights") from exc
    return UpdateContributorInsightsResult(
        table_name=resp.get("TableName"),
        index_name=resp.get("IndexName"),
        contributor_insights_status=resp.get("ContributorInsightsStatus"),
        contributor_insights_mode=resp.get("ContributorInsightsMode"),
    )


def update_global_table(
    global_table_name: str,
    replica_updates: list[dict[str, Any]],
    region_name: str | None = None,
) -> UpdateGlobalTableResult:
    """Update global table.

    Args:
        global_table_name: Global table name.
        replica_updates: Replica updates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalTableName"] = global_table_name
    kwargs["ReplicaUpdates"] = replica_updates
    try:
        resp = client.update_global_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update global table") from exc
    return UpdateGlobalTableResult(
        global_table_description=resp.get("GlobalTableDescription"),
    )


def update_global_table_settings(
    global_table_name: str,
    *,
    global_table_billing_mode: str | None = None,
    global_table_provisioned_write_capacity_units: int | None = None,
    global_table_provisioned_write_capacity_auto_scaling_settings_update: dict[str, Any]
    | None = None,
    global_table_global_secondary_index_settings_update: list[dict[str, Any]] | None = None,
    replica_settings_update: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateGlobalTableSettingsResult:
    """Update global table settings.

    Args:
        global_table_name: Global table name.
        global_table_billing_mode: Global table billing mode.
        global_table_provisioned_write_capacity_units: Global table provisioned write capacity units.
        global_table_provisioned_write_capacity_auto_scaling_settings_update: Global table provisioned write capacity auto scaling settings update.
        global_table_global_secondary_index_settings_update: Global table global secondary index settings update.
        replica_settings_update: Replica settings update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["GlobalTableName"] = global_table_name
    if global_table_billing_mode is not None:
        kwargs["GlobalTableBillingMode"] = global_table_billing_mode
    if global_table_provisioned_write_capacity_units is not None:
        kwargs["GlobalTableProvisionedWriteCapacityUnits"] = (
            global_table_provisioned_write_capacity_units
        )
    if global_table_provisioned_write_capacity_auto_scaling_settings_update is not None:
        kwargs["GlobalTableProvisionedWriteCapacityAutoScalingSettingsUpdate"] = (
            global_table_provisioned_write_capacity_auto_scaling_settings_update
        )
    if global_table_global_secondary_index_settings_update is not None:
        kwargs["GlobalTableGlobalSecondaryIndexSettingsUpdate"] = (
            global_table_global_secondary_index_settings_update
        )
    if replica_settings_update is not None:
        kwargs["ReplicaSettingsUpdate"] = replica_settings_update
    try:
        resp = client.update_global_table_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update global table settings") from exc
    return UpdateGlobalTableSettingsResult(
        global_table_name=resp.get("GlobalTableName"),
        replica_settings=resp.get("ReplicaSettings"),
    )


def update_kinesis_streaming_destination(
    table_name: str,
    stream_arn: str,
    *,
    update_kinesis_streaming_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateKinesisStreamingDestinationResult:
    """Update kinesis streaming destination.

    Args:
        table_name: Table name.
        stream_arn: Stream arn.
        update_kinesis_streaming_configuration: Update kinesis streaming configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["StreamArn"] = stream_arn
    if update_kinesis_streaming_configuration is not None:
        kwargs["UpdateKinesisStreamingConfiguration"] = update_kinesis_streaming_configuration
    try:
        resp = client.update_kinesis_streaming_destination(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update kinesis streaming destination") from exc
    return UpdateKinesisStreamingDestinationResult(
        table_name=resp.get("TableName"),
        stream_arn=resp.get("StreamArn"),
        destination_status=resp.get("DestinationStatus"),
        update_kinesis_streaming_configuration=resp.get("UpdateKinesisStreamingConfiguration"),
    )


def update_table(
    table_name: str,
    *,
    attribute_definitions: list[dict[str, Any]] | None = None,
    billing_mode: str | None = None,
    provisioned_throughput: dict[str, Any] | None = None,
    global_secondary_index_updates: list[dict[str, Any]] | None = None,
    stream_specification: dict[str, Any] | None = None,
    sse_specification: dict[str, Any] | None = None,
    replica_updates: list[dict[str, Any]] | None = None,
    table_class: str | None = None,
    deletion_protection_enabled: bool | None = None,
    multi_region_consistency: str | None = None,
    global_table_witness_updates: list[dict[str, Any]] | None = None,
    on_demand_throughput: dict[str, Any] | None = None,
    warm_throughput: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateTableResult:
    """Update table.

    Args:
        table_name: Table name.
        attribute_definitions: Attribute definitions.
        billing_mode: Billing mode.
        provisioned_throughput: Provisioned throughput.
        global_secondary_index_updates: Global secondary index updates.
        stream_specification: Stream specification.
        sse_specification: Sse specification.
        replica_updates: Replica updates.
        table_class: Table class.
        deletion_protection_enabled: Deletion protection enabled.
        multi_region_consistency: Multi region consistency.
        global_table_witness_updates: Global table witness updates.
        on_demand_throughput: On demand throughput.
        warm_throughput: Warm throughput.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    if attribute_definitions is not None:
        kwargs["AttributeDefinitions"] = attribute_definitions
    if billing_mode is not None:
        kwargs["BillingMode"] = billing_mode
    if provisioned_throughput is not None:
        kwargs["ProvisionedThroughput"] = provisioned_throughput
    if global_secondary_index_updates is not None:
        kwargs["GlobalSecondaryIndexUpdates"] = global_secondary_index_updates
    if stream_specification is not None:
        kwargs["StreamSpecification"] = stream_specification
    if sse_specification is not None:
        kwargs["SSESpecification"] = sse_specification
    if replica_updates is not None:
        kwargs["ReplicaUpdates"] = replica_updates
    if table_class is not None:
        kwargs["TableClass"] = table_class
    if deletion_protection_enabled is not None:
        kwargs["DeletionProtectionEnabled"] = deletion_protection_enabled
    if multi_region_consistency is not None:
        kwargs["MultiRegionConsistency"] = multi_region_consistency
    if global_table_witness_updates is not None:
        kwargs["GlobalTableWitnessUpdates"] = global_table_witness_updates
    if on_demand_throughput is not None:
        kwargs["OnDemandThroughput"] = on_demand_throughput
    if warm_throughput is not None:
        kwargs["WarmThroughput"] = warm_throughput
    try:
        resp = client.update_table(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update table") from exc
    return UpdateTableResult(
        table_description=resp.get("TableDescription"),
    )


def update_table_replica_auto_scaling(
    table_name: str,
    *,
    global_secondary_index_updates: list[dict[str, Any]] | None = None,
    provisioned_write_capacity_auto_scaling_update: dict[str, Any] | None = None,
    replica_updates: list[dict[str, Any]] | None = None,
    region_name: str | None = None,
) -> UpdateTableReplicaAutoScalingResult:
    """Update table replica auto scaling.

    Args:
        table_name: Table name.
        global_secondary_index_updates: Global secondary index updates.
        provisioned_write_capacity_auto_scaling_update: Provisioned write capacity auto scaling update.
        replica_updates: Replica updates.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    if global_secondary_index_updates is not None:
        kwargs["GlobalSecondaryIndexUpdates"] = global_secondary_index_updates
    if provisioned_write_capacity_auto_scaling_update is not None:
        kwargs["ProvisionedWriteCapacityAutoScalingUpdate"] = (
            provisioned_write_capacity_auto_scaling_update
        )
    if replica_updates is not None:
        kwargs["ReplicaUpdates"] = replica_updates
    try:
        resp = client.update_table_replica_auto_scaling(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update table replica auto scaling") from exc
    return UpdateTableReplicaAutoScalingResult(
        table_auto_scaling_description=resp.get("TableAutoScalingDescription"),
    )


def update_time_to_live(
    table_name: str,
    time_to_live_specification: dict[str, Any],
    region_name: str | None = None,
) -> UpdateTimeToLiveResult:
    """Update time to live.

    Args:
        table_name: Table name.
        time_to_live_specification: Time to live specification.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("dynamodb", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TableName"] = table_name
    kwargs["TimeToLiveSpecification"] = time_to_live_specification
    try:
        resp = client.update_time_to_live(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update time to live") from exc
    return UpdateTimeToLiveResult(
        time_to_live_specification=resp.get("TimeToLiveSpecification"),
    )
