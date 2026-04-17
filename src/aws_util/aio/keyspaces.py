"""Native async Amazon Keyspaces utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.keyspaces import (
    CreateTypeResult,
    DeleteTypeResult,
    GetTableAutoScalingSettingsResult,
    GetTypeResult,
    KeyspaceResult,
    ListTypesResult,
    TableResult,
    UpdateKeyspaceResult,
    _parse_keyspace,
    _parse_table,
)

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
# Keyspace operations
# ---------------------------------------------------------------------------


async def create_keyspace(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call("CreateKeyspace", keyspaceName=keyspace_name, **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "create_keyspace failed") from exc
    return KeyspaceResult(
        keyspace_name=keyspace_name,
        resource_arn=resp["resourceArn"],
    )


async def get_keyspace(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call("GetKeyspace", keyspaceName=keyspace_name)
    except Exception as exc:
        raise wrap_aws_error(exc, "get_keyspace failed") from exc
    return _parse_keyspace(resp)


async def list_keyspaces(
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
    client = async_client("keyspaces", region_name)
    keyspaces: list[KeyspaceResult] = []
    try:
        call_kwargs: dict[str, Any] = {**kwargs}
        while True:
            resp = await client.call("ListKeyspaces", **call_kwargs)
            for ks in resp.get("keyspaces", []):
                keyspaces.append(_parse_keyspace(ks))
            token = resp.get("nextToken")
            if not token:
                break
            call_kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_keyspaces failed") from exc
    return keyspaces


async def delete_keyspace(
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
    client = async_client("keyspaces", region_name)
    try:
        await client.call("DeleteKeyspace", keyspaceName=keyspace_name)
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_keyspace failed") from exc


# ---------------------------------------------------------------------------
# Table operations
# ---------------------------------------------------------------------------


async def create_table(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call(
            "CreateTable",
            keyspaceName=keyspace_name,
            tableName=table_name,
            schemaDefinition=schema_definition,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "create_table failed") from exc
    return TableResult(
        keyspace_name=keyspace_name,
        table_name=table_name,
        resource_arn=resp["resourceArn"],
    )


async def get_table(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call(
            "GetTable",
            keyspaceName=keyspace_name,
            tableName=table_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "get_table failed") from exc
    return _parse_table(resp)


async def list_tables(
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
    client = async_client("keyspaces", region_name)
    tables: list[TableResult] = []
    try:
        call_kwargs: dict[str, Any] = {"keyspaceName": keyspace_name, **kwargs}
        while True:
            resp = await client.call("ListTables", **call_kwargs)
            for t in resp.get("tables", []):
                tables.append(_parse_table(t))
            token = resp.get("nextToken")
            if not token:
                break
            call_kwargs["nextToken"] = token
    except Exception as exc:
        raise wrap_aws_error(exc, "list_tables failed") from exc
    return tables


async def delete_table(
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
    client = async_client("keyspaces", region_name)
    try:
        await client.call(
            "DeleteTable",
            keyspaceName=keyspace_name,
            tableName=table_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "delete_table failed") from exc


async def update_table(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call(
            "UpdateTable",
            keyspaceName=keyspace_name,
            tableName=table_name,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "update_table failed") from exc
    return resp["resourceArn"]


async def restore_table(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call(
            "RestoreTable",
            sourceKeyspaceName=source_keyspace_name,
            sourceTableName=source_table_name,
            targetKeyspaceName=target_keyspace_name,
            targetTableName=target_table_name,
            **kwargs,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "restore_table failed") from exc
    return resp["restoredTableARN"]


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


async def tag_resource(
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
    client = async_client("keyspaces", region_name)
    try:
        await client.call("TagResource", resourceArn=resource_arn, tags=tags)
    except Exception as exc:
        raise wrap_aws_error(exc, "tag_resource failed") from exc


async def list_tags_for_resource(
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
    client = async_client("keyspaces", region_name)
    try:
        resp = await client.call("ListTagsForResource", resourceArn=resource_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_tags_for_resource failed") from exc
    return resp.get("tags", [])


async def create_type(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["typeName"] = type_name
    kwargs["fieldDefinitions"] = field_definitions
    try:
        resp = await client.call("CreateType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create type") from exc
    return CreateTypeResult(
        keyspace_arn=resp.get("keyspaceArn"),
        type_name=resp.get("typeName"),
    )


async def delete_type(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["typeName"] = type_name
    try:
        resp = await client.call("DeleteType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete type") from exc
    return DeleteTypeResult(
        keyspace_arn=resp.get("keyspaceArn"),
        type_name=resp.get("typeName"),
    )


async def get_table_auto_scaling_settings(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["tableName"] = table_name
    try:
        resp = await client.call("GetTableAutoScalingSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get table auto scaling settings") from exc
    return GetTableAutoScalingSettingsResult(
        keyspace_name=resp.get("keyspaceName"),
        table_name=resp.get("tableName"),
        resource_arn=resp.get("resourceArn"),
        auto_scaling_specification=resp.get("autoScalingSpecification"),
        replica_specifications=resp.get("replicaSpecifications"),
    )


async def get_type(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["typeName"] = type_name
    try:
        resp = await client.call("GetType", **kwargs)
    except Exception as exc:
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


async def list_types(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListTypes", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list types") from exc
    return ListTypesResult(
        next_token=resp.get("nextToken"),
        types=resp.get("types"),
    )


async def untag_resource(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_keyspace(
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
    client = async_client("keyspaces", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["keyspaceName"] = keyspace_name
    kwargs["replicationSpecification"] = replication_specification
    if client_side_timestamps is not None:
        kwargs["clientSideTimestamps"] = client_side_timestamps
    try:
        resp = await client.call("UpdateKeyspace", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update keyspace") from exc
    return UpdateKeyspaceResult(
        resource_arn=resp.get("resourceArn"),
    )
