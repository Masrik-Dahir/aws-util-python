"""aws_util.keyspaces -- Amazon Keyspaces (for Apache Cassandra) utilities.

Create, get, list, delete keyspaces and tables, plus tagging helpers.

Boto3 docs: https://docs.aws.amazon.com/boto3/latest/reference/services/keyspaces.html
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CreateTypeResult",
    "DeleteTypeResult",
    "GetTableAutoScalingSettingsResult",
    "GetTypeResult",
    "KeyspaceResult",
    "ListTypesResult",
    "TableResult",
    "UpdateKeyspaceResult",
    "create_keyspace",
    "create_table",
    "create_type",
    "delete_keyspace",
    "delete_table",
    "delete_type",
    "get_keyspace",
    "get_table",
    "get_table_auto_scaling_settings",
    "get_type",
    "list_keyspaces",
    "list_tables",
    "list_tags_for_resource",
    "list_types",
    "restore_table",
    "tag_resource",
    "untag_resource",
    "update_keyspace",
    "update_table",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class KeyspaceResult(BaseModel):
    """Metadata for an Amazon Keyspaces keyspace."""

    model_config = ConfigDict(frozen=True)

    keyspace_name: str
    resource_arn: str
    replication_strategy: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class TableResult(BaseModel):
    """Metadata for an Amazon Keyspaces table."""

    model_config = ConfigDict(frozen=True)

    keyspace_name: str
    table_name: str
    resource_arn: str
    status: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_KS_KNOWN = {"keyspaceName", "resourceArn", "replicationStrategy"}
_TBL_KNOWN = {"keyspaceName", "tableName", "resourceArn", "status"}


def _parse_keyspace(data: dict[str, Any]) -> KeyspaceResult:
    """Parse a Keyspaces keyspace response into a model."""
    extra = {k: v for k, v in data.items() if k not in _KS_KNOWN}
    return KeyspaceResult(
        keyspace_name=data["keyspaceName"],
        resource_arn=data["resourceArn"],
        replication_strategy=data.get("replicationStrategy"),
        extra=extra,
    )


def _parse_table(data: dict[str, Any]) -> TableResult:
    """Parse a Keyspaces table response into a model."""
    extra = {k: v for k, v in data.items() if k not in _TBL_KNOWN}
    return TableResult(
        keyspace_name=data["keyspaceName"],
        table_name=data["tableName"],
        resource_arn=data["resourceArn"],
        status=data.get("status"),
        extra=extra,
    )


# ---------------------------------------------------------------------------
# Keyspace operations
# ---------------------------------------------------------------------------


def create_keyspace(
    keyspace_name: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> KeyspaceResult:
    """Create an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Name of the keyspace to create.
        region_name: AWS region override.
        **kwargs: Additional CreateKeyspace parameters.

    Returns:
        The created :class:`KeyspaceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.create_keyspace(keyspaceName=keyspace_name, **kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_keyspace failed") from exc
    return KeyspaceResult(
        keyspace_name=keyspace_name,
        resource_arn=resp["resourceArn"],
    )


def get_keyspace(
    keyspace_name: str,
    *,
    region_name: str | None = None,
) -> KeyspaceResult:
    """Get details of an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Name of the keyspace.
        region_name: AWS region override.

    Returns:
        The :class:`KeyspaceResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.get_keyspace(keyspaceName=keyspace_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_keyspace failed") from exc
    return _parse_keyspace(resp)


def list_keyspaces(
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[KeyspaceResult]:
    """List all Amazon Keyspaces keyspaces.

    Args:
        region_name: AWS region override.
        **kwargs: Additional ListKeyspaces parameters.

    Returns:
        A list of :class:`KeyspaceResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    keyspaces: list[KeyspaceResult] = []
    try:
        paginator = client.get_paginator("list_keyspaces")
        for page in paginator.paginate(**kwargs):
            for ks in page.get("keyspaces", []):
                keyspaces.append(_parse_keyspace(ks))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_keyspaces failed") from exc
    return keyspaces


def delete_keyspace(
    keyspace_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Name of the keyspace to delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        client.delete_keyspace(keyspaceName=keyspace_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_keyspace failed") from exc


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


def create_table(
    keyspace_name: str,
    table_name: str,
    schema_definition: dict[str, Any],
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> TableResult:
    """Create a table in an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Parent keyspace name.
        table_name: Name of the table.
        schema_definition: Column and key schema definition.
        region_name: AWS region override.
        **kwargs: Additional CreateTable parameters.

    Returns:
        The created :class:`TableResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.create_table(
            keyspaceName=keyspace_name,
            tableName=table_name,
            schemaDefinition=schema_definition,
            **kwargs,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_table failed") from exc
    return TableResult(
        keyspace_name=keyspace_name,
        table_name=table_name,
        resource_arn=resp["resourceArn"],
    )


def get_table(
    keyspace_name: str,
    table_name: str,
    *,
    region_name: str | None = None,
) -> TableResult:
    """Get details of an Amazon Keyspaces table.

    Args:
        keyspace_name: Parent keyspace name.
        table_name: Name of the table.
        region_name: AWS region override.

    Returns:
        The :class:`TableResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.get_table(keyspaceName=keyspace_name, tableName=table_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_table failed") from exc
    return _parse_table(resp)


def list_tables(
    keyspace_name: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[TableResult]:
    """List tables in an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Parent keyspace name.
        region_name: AWS region override.
        **kwargs: Additional ListTables parameters.

    Returns:
        A list of :class:`TableResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    tables: list[TableResult] = []
    try:
        paginator = client.get_paginator("list_tables")
        for page in paginator.paginate(keyspaceName=keyspace_name, **kwargs):
            for t in page.get("tables", []):
                tables.append(_parse_table(t))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_tables failed") from exc
    return tables


def delete_table(
    keyspace_name: str,
    table_name: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a table from an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Parent keyspace name.
        table_name: Name of the table.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        client.delete_table(keyspaceName=keyspace_name, tableName=table_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_table failed") from exc


def update_table(
    keyspace_name: str,
    table_name: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> str:
    """Update a table in an Amazon Keyspaces keyspace.

    Args:
        keyspace_name: Parent keyspace name.
        table_name: Name of the table.
        region_name: AWS region override.
        **kwargs: Additional UpdateTable parameters.

    Returns:
        The resource ARN of the updated table.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.update_table(
            keyspaceName=keyspace_name,
            tableName=table_name,
            **kwargs,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_table failed") from exc
    return resp["resourceArn"]


def restore_table(
    source_keyspace_name: str,
    source_table_name: str,
    target_keyspace_name: str,
    target_table_name: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> str:
    """Restore a table from a point-in-time backup.

    Args:
        source_keyspace_name: Source keyspace name.
        source_table_name: Source table name.
        target_keyspace_name: Target keyspace name.
        target_table_name: Target table name.
        region_name: AWS region override.
        **kwargs: Additional RestoreTable parameters.

    Returns:
        The resource ARN of the restored table.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.restore_table(
            sourceKeyspaceName=source_keyspace_name,
            sourceTableName=source_table_name,
            targetKeyspaceName=target_keyspace_name,
            targetTableName=target_table_name,
            **kwargs,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "restore_table failed") from exc
    return resp["restoredTableARN"]


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


def tag_resource(
    resource_arn: str,
    tags: list[dict[str, str]],
    *,
    region_name: str | None = None,
) -> None:
    """Tag an Amazon Keyspaces resource.

    Args:
        resource_arn: ARN of the resource.
        tags: List of ``{"key": ..., "value": ...}`` dicts.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        client.tag_resource(resourceArn=resource_arn, tags=tags)
    except ClientError as exc:
        raise wrap_aws_error(exc, "tag_resource failed") from exc


def list_tags_for_resource(
    resource_arn: str,
    *,
    region_name: str | None = None,
) -> list[dict[str, str]]:
    """List tags for an Amazon Keyspaces resource.

    Args:
        resource_arn: ARN of the resource.
        region_name: AWS region override.

    Returns:
        A list of tag dicts.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    try:
        resp = client.list_tags_for_resource(resourceArn=resource_arn)
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_tags_for_resource failed") from exc
    return resp.get("tags", [])


class CreateTypeResult(BaseModel):
    """Result of create_type."""

    model_config = ConfigDict(frozen=True)

    keyspace_arn: str | None = None
    type_name: str | None = None


class DeleteTypeResult(BaseModel):
    """Result of delete_type."""

    model_config = ConfigDict(frozen=True)

    keyspace_arn: str | None = None
    type_name: str | None = None


class GetTableAutoScalingSettingsResult(BaseModel):
    """Result of get_table_auto_scaling_settings."""

    model_config = ConfigDict(frozen=True)

    keyspace_name: str | None = None
    table_name: str | None = None
    resource_arn: str | None = None
    auto_scaling_specification: dict[str, Any] | None = None
    replica_specifications: list[dict[str, Any]] | None = None


class GetTypeResult(BaseModel):
    """Result of get_type."""

    model_config = ConfigDict(frozen=True)

    keyspace_name: str | None = None
    type_name: str | None = None
    field_definitions: list[dict[str, Any]] | None = None
    last_modified_timestamp: str | None = None
    status: str | None = None
    direct_referring_tables: list[str] | None = None
    direct_parent_types: list[str] | None = None
    max_nesting_depth: int | None = None
    keyspace_arn: str | None = None


class ListTypesResult(BaseModel):
    """Result of list_types."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    types: list[str] | None = None


class UpdateKeyspaceResult(BaseModel):
    """Result of update_keyspace."""

    model_config = ConfigDict(frozen=True)

    resource_arn: str | None = None


def create_type(
    keyspace_name: str,
    type_name: str,
    field_definitions: list[dict[str, Any]],
    region_name: str | None = None,
) -> CreateTypeResult:
    """Create type.

    Args:
        keyspace_name: Keyspace name.
        type_name: Type name.
        field_definitions: Field definitions.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["typeName"] = type_name
    kwargs["fieldDefinitions"] = field_definitions
    try:
        resp = client.create_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create type") from exc
    return CreateTypeResult(
        keyspace_arn=resp.get("keyspaceArn"),
        type_name=resp.get("typeName"),
    )


def delete_type(
    keyspace_name: str,
    type_name: str,
    region_name: str | None = None,
) -> DeleteTypeResult:
    """Delete type.

    Args:
        keyspace_name: Keyspace name.
        type_name: Type name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["typeName"] = type_name
    try:
        resp = client.delete_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete type") from exc
    return DeleteTypeResult(
        keyspace_arn=resp.get("keyspaceArn"),
        type_name=resp.get("typeName"),
    )


def get_table_auto_scaling_settings(
    keyspace_name: str,
    table_name: str,
    region_name: str | None = None,
) -> GetTableAutoScalingSettingsResult:
    """Get table auto scaling settings.

    Args:
        keyspace_name: Keyspace name.
        table_name: Table name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["tableName"] = table_name
    try:
        resp = client.get_table_auto_scaling_settings(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get table auto scaling settings") from exc
    return GetTableAutoScalingSettingsResult(
        keyspace_name=resp.get("keyspaceName"),
        table_name=resp.get("tableName"),
        resource_arn=resp.get("resourceArn"),
        auto_scaling_specification=resp.get("autoScalingSpecification"),
        replica_specifications=resp.get("replicaSpecifications"),
    )


def get_type(
    keyspace_name: str,
    type_name: str,
    region_name: str | None = None,
) -> GetTypeResult:
    """Get type.

    Args:
        keyspace_name: Keyspace name.
        type_name: Type name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["typeName"] = type_name
    try:
        resp = client.get_type(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get type") from exc
    return GetTypeResult(
        keyspace_name=resp.get("keyspaceName"),
        type_name=resp.get("typeName"),
        field_definitions=resp.get("fieldDefinitions"),
        last_modified_timestamp=resp.get("lastModifiedTimestamp"),
        status=resp.get("status"),
        direct_referring_tables=resp.get("directReferringTables"),
        direct_parent_types=resp.get("directParentTypes"),
        max_nesting_depth=resp.get("maxNestingDepth"),
        keyspace_arn=resp.get("keyspaceArn"),
    )


def list_types(
    keyspace_name: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListTypesResult:
    """List types.

    Args:
        keyspace_name: Keyspace name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_types(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list types") from exc
    return ListTypesResult(
        next_token=resp.get("nextToken"),
        types=resp.get("types"),
    )


def untag_resource(
    resource_arn: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_keyspace(
    keyspace_name: str,
    replication_specification: dict[str, Any],
    *,
    client_side_timestamps: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateKeyspaceResult:
    """Update keyspace.

    Args:
        keyspace_name: Keyspace name.
        replication_specification: Replication specification.
        client_side_timestamps: Client side timestamps.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["replicationSpecification"] = replication_specification
    if client_side_timestamps is not None:
        kwargs["clientSideTimestamps"] = client_side_timestamps
    try:
        resp = client.update_keyspace(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update keyspace") from exc
    return UpdateKeyspaceResult(
        resource_arn=resp.get("resourceArn"),
    )
