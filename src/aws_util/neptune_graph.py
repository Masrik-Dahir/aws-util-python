"""aws_util.neptune_graph -- Amazon Neptune Analytics (neptune-graph) utilities.

Create, get, list, update, delete, snapshot, and reset Neptune Analytics
graphs.

Boto3 docs: https://docs.aws.amazon.com/boto3/latest/reference/services/neptune-graph.html
"""

from __future__ import annotations

from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict, Field

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

__all__ = [
    "CancelExportTaskResult",
    "CancelImportTaskResult",
    "CreateGraphUsingImportTaskResult",
    "CreatePrivateGraphEndpointResult",
    "DeletePrivateGraphEndpointResult",
    "ExecuteQueryResult",
    "GetExportTaskResult",
    "GetGraphSummaryResult",
    "GetImportTaskResult",
    "GetPrivateGraphEndpointResult",
    "GetQueryResult",
    "GraphResult",
    "GraphSnapshotResult",
    "ListExportTasksResult",
    "ListImportTasksResult",
    "ListPrivateGraphEndpointsResult",
    "ListQueriesResult",
    "ListTagsForResourceResult",
    "RestoreGraphFromSnapshotResult",
    "StartExportTaskResult",
    "StartGraphResult",
    "StartImportTaskResult",
    "StopGraphResult",
    "cancel_export_task",
    "cancel_import_task",
    "cancel_query",
    "create_graph",
    "create_graph_snapshot",
    "create_graph_using_import_task",
    "create_private_graph_endpoint",
    "delete_graph",
    "delete_graph_snapshot",
    "delete_private_graph_endpoint",
    "execute_query",
    "get_export_task",
    "get_graph",
    "get_graph_snapshot",
    "get_graph_summary",
    "get_import_task",
    "get_private_graph_endpoint",
    "get_query",
    "list_export_tasks",
    "list_graph_snapshots",
    "list_graphs",
    "list_import_tasks",
    "list_private_graph_endpoints",
    "list_queries",
    "list_tags_for_resource",
    "reset_graph",
    "restore_graph_from_snapshot",
    "start_export_task",
    "start_graph",
    "start_import_task",
    "stop_graph",
    "tag_resource",
    "untag_resource",
    "update_graph",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class GraphResult(BaseModel):
    """Metadata for a Neptune Analytics graph."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    arn: str | None = None
    status: str | None = None
    provisioned_memory: int | None = None
    endpoint: str | None = None
    public_connectivity: bool | None = None
    replica_count: int | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


class GraphSnapshotResult(BaseModel):
    """Metadata for a Neptune Analytics graph snapshot."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    arn: str | None = None
    status: str | None = None
    source_graph_id: str | None = None
    extra: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_GRAPH_KNOWN_KEYS = {
    "id",
    "name",
    "arn",
    "status",
    "provisionedMemory",
    "endpoint",
    "publicConnectivity",
    "replicaCount",
}

_SNAP_KNOWN_KEYS = {"id", "name", "arn", "status", "sourceGraphId"}


def _parse_graph(data: dict[str, Any]) -> GraphResult:
    """Parse a Neptune graph response dict into a model."""
    extra = {k: v for k, v in data.items() if k not in _GRAPH_KNOWN_KEYS}
    return GraphResult(
        id=data["id"],
        name=data["name"],
        arn=data.get("arn"),
        status=data.get("status"),
        provisioned_memory=data.get("provisionedMemory"),
        endpoint=data.get("endpoint"),
        public_connectivity=data.get("publicConnectivity"),
        replica_count=data.get("replicaCount"),
        extra=extra,
    )


def _parse_graph_snapshot(data: dict[str, Any]) -> GraphSnapshotResult:
    """Parse a Neptune graph snapshot response dict into a model."""
    extra = {k: v for k, v in data.items() if k not in _SNAP_KNOWN_KEYS}
    return GraphSnapshotResult(
        id=data["id"],
        name=data["name"],
        arn=data.get("arn"),
        status=data.get("status"),
        source_graph_id=data.get("sourceGraphId"),
        extra=extra,
    )


# ---------------------------------------------------------------------------
# Graph operations
# ---------------------------------------------------------------------------


def create_graph(
    name: str,
    provisioned_memory: int,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> GraphResult:
    """Create a Neptune Analytics graph.

    Args:
        name: Graph name.
        provisioned_memory: Provisioned memory in MiB.
        region_name: AWS region override.
        **kwargs: Additional CreateGraph parameters.

    Returns:
        The created :class:`GraphResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        resp = client.create_graph(
            graphName=name,
            provisionedMemory=provisioned_memory,
            **kwargs,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_graph failed") from exc
    return _parse_graph(resp)


def get_graph(
    graph_identifier: str,
    *,
    region_name: str | None = None,
) -> GraphResult:
    """Get details of a Neptune Analytics graph.

    Args:
        graph_identifier: Graph ID or ARN.
        region_name: AWS region override.

    Returns:
        The :class:`GraphResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        resp = client.get_graph(graphIdentifier=graph_identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_graph failed") from exc
    return _parse_graph(resp)


def list_graphs(
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[GraphResult]:
    """List all Neptune Analytics graphs.

    Args:
        region_name: AWS region override.
        **kwargs: Additional ListGraphs parameters.

    Returns:
        A list of :class:`GraphResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    graphs: list[GraphResult] = []
    try:
        paginator = client.get_paginator("list_graphs")
        for page in paginator.paginate(**kwargs):
            for g in page.get("graphs", []):
                graphs.append(_parse_graph(g))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_graphs failed") from exc
    return graphs


def delete_graph(
    graph_identifier: str,
    *,
    skip_snapshot: bool = True,
    region_name: str | None = None,
) -> None:
    """Delete a Neptune Analytics graph.

    Args:
        graph_identifier: Graph ID or ARN.
        skip_snapshot: Skip creating a final snapshot (default ``True``).
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        client.delete_graph(
            graphIdentifier=graph_identifier,
            skipSnapshot=skip_snapshot,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_graph failed") from exc


def update_graph(
    graph_identifier: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> GraphResult:
    """Update a Neptune Analytics graph.

    Args:
        graph_identifier: Graph ID or ARN.
        region_name: AWS region override.
        **kwargs: Additional UpdateGraph parameters.

    Returns:
        The updated :class:`GraphResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        resp = client.update_graph(graphIdentifier=graph_identifier, **kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "update_graph failed") from exc
    return _parse_graph(resp)


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


def create_graph_snapshot(
    graph_identifier: str,
    name: str,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> GraphSnapshotResult:
    """Create a snapshot of a Neptune Analytics graph.

    Args:
        graph_identifier: Graph ID or ARN.
        name: Snapshot name.
        region_name: AWS region override.
        **kwargs: Additional CreateGraphSnapshot parameters.

    Returns:
        The created :class:`GraphSnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        resp = client.create_graph_snapshot(
            graphIdentifier=graph_identifier,
            snapshotName=name,
            **kwargs,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "create_graph_snapshot failed") from exc
    return _parse_graph_snapshot(resp)


def get_graph_snapshot(
    snapshot_identifier: str,
    *,
    region_name: str | None = None,
) -> GraphSnapshotResult:
    """Get details of a Neptune Analytics graph snapshot.

    Args:
        snapshot_identifier: Snapshot ID or ARN.
        region_name: AWS region override.

    Returns:
        The :class:`GraphSnapshotResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        resp = client.get_graph_snapshot(snapshotIdentifier=snapshot_identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, "get_graph_snapshot failed") from exc
    return _parse_graph_snapshot(resp)


def list_graph_snapshots(
    graph_identifier: str | None = None,
    *,
    region_name: str | None = None,
    **kwargs: Any,
) -> list[GraphSnapshotResult]:
    """List Neptune Analytics graph snapshots.

    Args:
        graph_identifier: Filter by graph.
        region_name: AWS region override.
        **kwargs: Additional ListGraphSnapshots parameters.

    Returns:
        A list of :class:`GraphSnapshotResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    params: dict[str, Any] = {**kwargs}
    if graph_identifier is not None:
        params["graphIdentifier"] = graph_identifier
    snapshots: list[GraphSnapshotResult] = []
    try:
        paginator = client.get_paginator("list_graph_snapshots")
        for page in paginator.paginate(**params):
            for s in page.get("graphSnapshots", []):
                snapshots.append(_parse_graph_snapshot(s))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_graph_snapshots failed") from exc
    return snapshots


def delete_graph_snapshot(
    snapshot_identifier: str,
    *,
    region_name: str | None = None,
) -> None:
    """Delete a Neptune Analytics graph snapshot.

    Args:
        snapshot_identifier: Snapshot ID or ARN.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        client.delete_graph_snapshot(snapshotIdentifier=snapshot_identifier)
    except ClientError as exc:
        raise wrap_aws_error(exc, "delete_graph_snapshot failed") from exc


def reset_graph(
    graph_identifier: str,
    *,
    perform_clean_up: bool = True,
    region_name: str | None = None,
) -> GraphResult:
    """Reset a Neptune Analytics graph.

    Args:
        graph_identifier: Graph ID or ARN.
        perform_clean_up: Perform cleanup after reset.
        region_name: AWS region override.

    Returns:
        The reset :class:`GraphResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    try:
        resp = client.reset_graph(
            graphIdentifier=graph_identifier,
            performCleanUp=perform_clean_up,
        )
    except ClientError as exc:
        raise wrap_aws_error(exc, "reset_graph failed") from exc
    return _parse_graph(resp)


class CancelExportTaskResult(BaseModel):
    """Result of cancel_export_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    role_arn: str | None = None
    task_id: str | None = None
    status: str | None = None
    format: str | None = None
    destination: str | None = None
    kms_key_identifier: str | None = None
    parquet_type: str | None = None
    status_reason: str | None = None


class CancelImportTaskResult(BaseModel):
    """Result of cancel_import_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    task_id: str | None = None
    source: str | None = None
    format: str | None = None
    parquet_type: str | None = None
    role_arn: str | None = None
    status: str | None = None


class CreateGraphUsingImportTaskResult(BaseModel):
    """Result of create_graph_using_import_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    task_id: str | None = None
    source: str | None = None
    format: str | None = None
    parquet_type: str | None = None
    role_arn: str | None = None
    status: str | None = None
    import_options: dict[str, Any] | None = None


class CreatePrivateGraphEndpointResult(BaseModel):
    """Result of create_private_graph_endpoint."""

    model_config = ConfigDict(frozen=True)

    vpc_id: str | None = None
    subnet_ids: list[str] | None = None
    status: str | None = None
    vpc_endpoint_id: str | None = None


class DeletePrivateGraphEndpointResult(BaseModel):
    """Result of delete_private_graph_endpoint."""

    model_config = ConfigDict(frozen=True)

    vpc_id: str | None = None
    subnet_ids: list[str] | None = None
    status: str | None = None
    vpc_endpoint_id: str | None = None


class ExecuteQueryResult(BaseModel):
    """Result of execute_query."""

    model_config = ConfigDict(frozen=True)

    payload: bytes | None = None


class GetExportTaskResult(BaseModel):
    """Result of get_export_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    role_arn: str | None = None
    task_id: str | None = None
    status: str | None = None
    format: str | None = None
    destination: str | None = None
    kms_key_identifier: str | None = None
    parquet_type: str | None = None
    status_reason: str | None = None
    export_task_details: dict[str, Any] | None = None
    export_filter: dict[str, Any] | None = None


class GetGraphSummaryResult(BaseModel):
    """Result of get_graph_summary."""

    model_config = ConfigDict(frozen=True)

    version: str | None = None
    last_statistics_computation_time: str | None = None
    graph_summary: dict[str, Any] | None = None


class GetImportTaskResult(BaseModel):
    """Result of get_import_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    task_id: str | None = None
    source: str | None = None
    format: str | None = None
    parquet_type: str | None = None
    role_arn: str | None = None
    status: str | None = None
    import_options: dict[str, Any] | None = None
    import_task_details: dict[str, Any] | None = None
    attempt_number: int | None = None
    status_reason: str | None = None


class GetPrivateGraphEndpointResult(BaseModel):
    """Result of get_private_graph_endpoint."""

    model_config = ConfigDict(frozen=True)

    vpc_id: str | None = None
    subnet_ids: list[str] | None = None
    status: str | None = None
    vpc_endpoint_id: str | None = None


class GetQueryResult(BaseModel):
    """Result of get_query."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    query_string: str | None = None
    waited: int | None = None
    elapsed: int | None = None
    state: str | None = None


class ListExportTasksResult(BaseModel):
    """Result of list_export_tasks."""

    model_config = ConfigDict(frozen=True)

    tasks: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListImportTasksResult(BaseModel):
    """Result of list_import_tasks."""

    model_config = ConfigDict(frozen=True)

    tasks: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPrivateGraphEndpointsResult(BaseModel):
    """Result of list_private_graph_endpoints."""

    model_config = ConfigDict(frozen=True)

    private_graph_endpoints: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListQueriesResult(BaseModel):
    """Result of list_queries."""

    model_config = ConfigDict(frozen=True)

    queries: list[dict[str, Any]] | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class RestoreGraphFromSnapshotResult(BaseModel):
    """Result of restore_graph_from_snapshot."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    status: str | None = None
    status_reason: str | None = None
    create_time: str | None = None
    provisioned_memory: int | None = None
    endpoint: str | None = None
    public_connectivity: bool | None = None
    vector_search_configuration: dict[str, Any] | None = None
    replica_count: int | None = None
    kms_key_identifier: str | None = None
    source_snapshot_id: str | None = None
    deletion_protection: bool | None = None
    build_number: str | None = None


class StartExportTaskResult(BaseModel):
    """Result of start_export_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    role_arn: str | None = None
    task_id: str | None = None
    status: str | None = None
    format: str | None = None
    destination: str | None = None
    kms_key_identifier: str | None = None
    parquet_type: str | None = None
    status_reason: str | None = None
    export_filter: dict[str, Any] | None = None


class StartGraphResult(BaseModel):
    """Result of start_graph."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    status: str | None = None
    status_reason: str | None = None
    create_time: str | None = None
    provisioned_memory: int | None = None
    endpoint: str | None = None
    public_connectivity: bool | None = None
    vector_search_configuration: dict[str, Any] | None = None
    replica_count: int | None = None
    kms_key_identifier: str | None = None
    source_snapshot_id: str | None = None
    deletion_protection: bool | None = None
    build_number: str | None = None


class StartImportTaskResult(BaseModel):
    """Result of start_import_task."""

    model_config = ConfigDict(frozen=True)

    graph_id: str | None = None
    task_id: str | None = None
    source: str | None = None
    format: str | None = None
    parquet_type: str | None = None
    role_arn: str | None = None
    status: str | None = None
    import_options: dict[str, Any] | None = None


class StopGraphResult(BaseModel):
    """Result of stop_graph."""

    model_config = ConfigDict(frozen=True)

    id: str | None = None
    name: str | None = None
    arn: str | None = None
    status: str | None = None
    status_reason: str | None = None
    create_time: str | None = None
    provisioned_memory: int | None = None
    endpoint: str | None = None
    public_connectivity: bool | None = None
    vector_search_configuration: dict[str, Any] | None = None
    replica_count: int | None = None
    kms_key_identifier: str | None = None
    source_snapshot_id: str | None = None
    deletion_protection: bool | None = None
    build_number: str | None = None


def cancel_export_task(
    task_identifier: str,
    region_name: str | None = None,
) -> CancelExportTaskResult:
    """Cancel export task.

    Args:
        task_identifier: Task identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskIdentifier"] = task_identifier
    try:
        resp = client.cancel_export_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel export task") from exc
    return CancelExportTaskResult(
        graph_id=resp.get("graphId"),
        role_arn=resp.get("roleArn"),
        task_id=resp.get("taskId"),
        status=resp.get("status"),
        format=resp.get("format"),
        destination=resp.get("destination"),
        kms_key_identifier=resp.get("kmsKeyIdentifier"),
        parquet_type=resp.get("parquetType"),
        status_reason=resp.get("statusReason"),
    )


def cancel_import_task(
    task_identifier: str,
    region_name: str | None = None,
) -> CancelImportTaskResult:
    """Cancel import task.

    Args:
        task_identifier: Task identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskIdentifier"] = task_identifier
    try:
        resp = client.cancel_import_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel import task") from exc
    return CancelImportTaskResult(
        graph_id=resp.get("graphId"),
        task_id=resp.get("taskId"),
        source=resp.get("source"),
        format=resp.get("format"),
        parquet_type=resp.get("parquetType"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
    )


def cancel_query(
    graph_identifier: str,
    query_id: str,
    region_name: str | None = None,
) -> None:
    """Cancel query.

    Args:
        graph_identifier: Graph identifier.
        query_id: Query id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["queryId"] = query_id
    try:
        client.cancel_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to cancel query") from exc
    return None


def create_graph_using_import_task(
    graph_name: str,
    source: str,
    role_arn: str,
    *,
    tags: dict[str, Any] | None = None,
    public_connectivity: bool | None = None,
    kms_key_identifier: str | None = None,
    vector_search_configuration: dict[str, Any] | None = None,
    replica_count: int | None = None,
    deletion_protection: bool | None = None,
    import_options: dict[str, Any] | None = None,
    max_provisioned_memory: int | None = None,
    min_provisioned_memory: int | None = None,
    fail_on_error: bool | None = None,
    format: str | None = None,
    parquet_type: str | None = None,
    blank_node_handling: str | None = None,
    region_name: str | None = None,
) -> CreateGraphUsingImportTaskResult:
    """Create graph using import task.

    Args:
        graph_name: Graph name.
        source: Source.
        role_arn: Role arn.
        tags: Tags.
        public_connectivity: Public connectivity.
        kms_key_identifier: Kms key identifier.
        vector_search_configuration: Vector search configuration.
        replica_count: Replica count.
        deletion_protection: Deletion protection.
        import_options: Import options.
        max_provisioned_memory: Max provisioned memory.
        min_provisioned_memory: Min provisioned memory.
        fail_on_error: Fail on error.
        format: Format.
        parquet_type: Parquet type.
        blank_node_handling: Blank node handling.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphName"] = graph_name
    kwargs["source"] = source
    kwargs["roleArn"] = role_arn
    if tags is not None:
        kwargs["tags"] = tags
    if public_connectivity is not None:
        kwargs["publicConnectivity"] = public_connectivity
    if kms_key_identifier is not None:
        kwargs["kmsKeyIdentifier"] = kms_key_identifier
    if vector_search_configuration is not None:
        kwargs["vectorSearchConfiguration"] = vector_search_configuration
    if replica_count is not None:
        kwargs["replicaCount"] = replica_count
    if deletion_protection is not None:
        kwargs["deletionProtection"] = deletion_protection
    if import_options is not None:
        kwargs["importOptions"] = import_options
    if max_provisioned_memory is not None:
        kwargs["maxProvisionedMemory"] = max_provisioned_memory
    if min_provisioned_memory is not None:
        kwargs["minProvisionedMemory"] = min_provisioned_memory
    if fail_on_error is not None:
        kwargs["failOnError"] = fail_on_error
    if format is not None:
        kwargs["format"] = format
    if parquet_type is not None:
        kwargs["parquetType"] = parquet_type
    if blank_node_handling is not None:
        kwargs["blankNodeHandling"] = blank_node_handling
    try:
        resp = client.create_graph_using_import_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create graph using import task") from exc
    return CreateGraphUsingImportTaskResult(
        graph_id=resp.get("graphId"),
        task_id=resp.get("taskId"),
        source=resp.get("source"),
        format=resp.get("format"),
        parquet_type=resp.get("parquetType"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
        import_options=resp.get("importOptions"),
    )


def create_private_graph_endpoint(
    graph_identifier: str,
    *,
    vpc_id: str | None = None,
    subnet_ids: list[str] | None = None,
    vpc_security_group_ids: list[str] | None = None,
    region_name: str | None = None,
) -> CreatePrivateGraphEndpointResult:
    """Create private graph endpoint.

    Args:
        graph_identifier: Graph identifier.
        vpc_id: Vpc id.
        subnet_ids: Subnet ids.
        vpc_security_group_ids: Vpc security group ids.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    if vpc_id is not None:
        kwargs["vpcId"] = vpc_id
    if subnet_ids is not None:
        kwargs["subnetIds"] = subnet_ids
    if vpc_security_group_ids is not None:
        kwargs["vpcSecurityGroupIds"] = vpc_security_group_ids
    try:
        resp = client.create_private_graph_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create private graph endpoint") from exc
    return CreatePrivateGraphEndpointResult(
        vpc_id=resp.get("vpcId"),
        subnet_ids=resp.get("subnetIds"),
        status=resp.get("status"),
        vpc_endpoint_id=resp.get("vpcEndpointId"),
    )


def delete_private_graph_endpoint(
    graph_identifier: str,
    vpc_id: str,
    region_name: str | None = None,
) -> DeletePrivateGraphEndpointResult:
    """Delete private graph endpoint.

    Args:
        graph_identifier: Graph identifier.
        vpc_id: Vpc id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["vpcId"] = vpc_id
    try:
        resp = client.delete_private_graph_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete private graph endpoint") from exc
    return DeletePrivateGraphEndpointResult(
        vpc_id=resp.get("vpcId"),
        subnet_ids=resp.get("subnetIds"),
        status=resp.get("status"),
        vpc_endpoint_id=resp.get("vpcEndpointId"),
    )


def execute_query(
    graph_identifier: str,
    query_string: str,
    language: str,
    *,
    parameters: dict[str, Any] | None = None,
    plan_cache: str | None = None,
    explain_mode: str | None = None,
    query_timeout_milliseconds: int | None = None,
    region_name: str | None = None,
) -> ExecuteQueryResult:
    """Execute query.

    Args:
        graph_identifier: Graph identifier.
        query_string: Query string.
        language: Language.
        parameters: Parameters.
        plan_cache: Plan cache.
        explain_mode: Explain mode.
        query_timeout_milliseconds: Query timeout milliseconds.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["queryString"] = query_string
    kwargs["language"] = language
    if parameters is not None:
        kwargs["parameters"] = parameters
    if plan_cache is not None:
        kwargs["planCache"] = plan_cache
    if explain_mode is not None:
        kwargs["explainMode"] = explain_mode
    if query_timeout_milliseconds is not None:
        kwargs["queryTimeoutMilliseconds"] = query_timeout_milliseconds
    try:
        resp = client.execute_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to execute query") from exc
    return ExecuteQueryResult(
        payload=resp.get("payload"),
    )


def get_export_task(
    task_identifier: str,
    region_name: str | None = None,
) -> GetExportTaskResult:
    """Get export task.

    Args:
        task_identifier: Task identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskIdentifier"] = task_identifier
    try:
        resp = client.get_export_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get export task") from exc
    return GetExportTaskResult(
        graph_id=resp.get("graphId"),
        role_arn=resp.get("roleArn"),
        task_id=resp.get("taskId"),
        status=resp.get("status"),
        format=resp.get("format"),
        destination=resp.get("destination"),
        kms_key_identifier=resp.get("kmsKeyIdentifier"),
        parquet_type=resp.get("parquetType"),
        status_reason=resp.get("statusReason"),
        export_task_details=resp.get("exportTaskDetails"),
        export_filter=resp.get("exportFilter"),
    )


def get_graph_summary(
    graph_identifier: str,
    *,
    mode: str | None = None,
    region_name: str | None = None,
) -> GetGraphSummaryResult:
    """Get graph summary.

    Args:
        graph_identifier: Graph identifier.
        mode: Mode.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    if mode is not None:
        kwargs["mode"] = mode
    try:
        resp = client.get_graph_summary(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get graph summary") from exc
    return GetGraphSummaryResult(
        version=resp.get("version"),
        last_statistics_computation_time=resp.get("lastStatisticsComputationTime"),
        graph_summary=resp.get("graphSummary"),
    )


def get_import_task(
    task_identifier: str,
    region_name: str | None = None,
) -> GetImportTaskResult:
    """Get import task.

    Args:
        task_identifier: Task identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["taskIdentifier"] = task_identifier
    try:
        resp = client.get_import_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get import task") from exc
    return GetImportTaskResult(
        graph_id=resp.get("graphId"),
        task_id=resp.get("taskId"),
        source=resp.get("source"),
        format=resp.get("format"),
        parquet_type=resp.get("parquetType"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
        import_options=resp.get("importOptions"),
        import_task_details=resp.get("importTaskDetails"),
        attempt_number=resp.get("attemptNumber"),
        status_reason=resp.get("statusReason"),
    )


def get_private_graph_endpoint(
    graph_identifier: str,
    vpc_id: str,
    region_name: str | None = None,
) -> GetPrivateGraphEndpointResult:
    """Get private graph endpoint.

    Args:
        graph_identifier: Graph identifier.
        vpc_id: Vpc id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["vpcId"] = vpc_id
    try:
        resp = client.get_private_graph_endpoint(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get private graph endpoint") from exc
    return GetPrivateGraphEndpointResult(
        vpc_id=resp.get("vpcId"),
        subnet_ids=resp.get("subnetIds"),
        status=resp.get("status"),
        vpc_endpoint_id=resp.get("vpcEndpointId"),
    )


def get_query(
    graph_identifier: str,
    query_id: str,
    region_name: str | None = None,
) -> GetQueryResult:
    """Get query.

    Args:
        graph_identifier: Graph identifier.
        query_id: Query id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["queryId"] = query_id
    try:
        resp = client.get_query(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to get query") from exc
    return GetQueryResult(
        id=resp.get("id"),
        query_string=resp.get("queryString"),
        waited=resp.get("waited"),
        elapsed=resp.get("elapsed"),
        state=resp.get("state"),
    )


def list_export_tasks(
    *,
    graph_identifier: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListExportTasksResult:
    """List export tasks.

    Args:
        graph_identifier: Graph identifier.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    if graph_identifier is not None:
        kwargs["graphIdentifier"] = graph_identifier
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_export_tasks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list export tasks") from exc
    return ListExportTasksResult(
        tasks=resp.get("tasks"),
        next_token=resp.get("nextToken"),
    )


def list_import_tasks(
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListImportTasksResult:
    """List import tasks.

    Args:
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_import_tasks(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list import tasks") from exc
    return ListImportTasksResult(
        tasks=resp.get("tasks"),
        next_token=resp.get("nextToken"),
    )


def list_private_graph_endpoints(
    graph_identifier: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListPrivateGraphEndpointsResult:
    """List private graph endpoints.

    Args:
        graph_identifier: Graph identifier.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = client.list_private_graph_endpoints(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list private graph endpoints") from exc
    return ListPrivateGraphEndpointsResult(
        private_graph_endpoints=resp.get("privateGraphEndpoints"),
        next_token=resp.get("nextToken"),
    )


def list_queries(
    graph_identifier: str,
    max_results: int,
    *,
    state: str | None = None,
    region_name: str | None = None,
) -> ListQueriesResult:
    """List queries.

    Args:
        graph_identifier: Graph identifier.
        max_results: Max results.
        state: State.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["maxResults"] = max_results
    if state is not None:
        kwargs["state"] = state
    try:
        resp = client.list_queries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list queries") from exc
    return ListQueriesResult(
        queries=resp.get("queries"),
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
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def restore_graph_from_snapshot(
    snapshot_identifier: str,
    graph_name: str,
    *,
    provisioned_memory: int | None = None,
    deletion_protection: bool | None = None,
    tags: dict[str, Any] | None = None,
    replica_count: int | None = None,
    public_connectivity: bool | None = None,
    region_name: str | None = None,
) -> RestoreGraphFromSnapshotResult:
    """Restore graph from snapshot.

    Args:
        snapshot_identifier: Snapshot identifier.
        graph_name: Graph name.
        provisioned_memory: Provisioned memory.
        deletion_protection: Deletion protection.
        tags: Tags.
        replica_count: Replica count.
        public_connectivity: Public connectivity.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["snapshotIdentifier"] = snapshot_identifier
    kwargs["graphName"] = graph_name
    if provisioned_memory is not None:
        kwargs["provisionedMemory"] = provisioned_memory
    if deletion_protection is not None:
        kwargs["deletionProtection"] = deletion_protection
    if tags is not None:
        kwargs["tags"] = tags
    if replica_count is not None:
        kwargs["replicaCount"] = replica_count
    if public_connectivity is not None:
        kwargs["publicConnectivity"] = public_connectivity
    try:
        resp = client.restore_graph_from_snapshot(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to restore graph from snapshot") from exc
    return RestoreGraphFromSnapshotResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        create_time=resp.get("createTime"),
        provisioned_memory=resp.get("provisionedMemory"),
        endpoint=resp.get("endpoint"),
        public_connectivity=resp.get("publicConnectivity"),
        vector_search_configuration=resp.get("vectorSearchConfiguration"),
        replica_count=resp.get("replicaCount"),
        kms_key_identifier=resp.get("kmsKeyIdentifier"),
        source_snapshot_id=resp.get("sourceSnapshotId"),
        deletion_protection=resp.get("deletionProtection"),
        build_number=resp.get("buildNumber"),
    )


def start_export_task(
    graph_identifier: str,
    role_arn: str,
    format: str,
    destination: str,
    kms_key_identifier: str,
    *,
    parquet_type: str | None = None,
    export_filter: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> StartExportTaskResult:
    """Start export task.

    Args:
        graph_identifier: Graph identifier.
        role_arn: Role arn.
        format: Format.
        destination: Destination.
        kms_key_identifier: Kms key identifier.
        parquet_type: Parquet type.
        export_filter: Export filter.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["roleArn"] = role_arn
    kwargs["format"] = format
    kwargs["destination"] = destination
    kwargs["kmsKeyIdentifier"] = kms_key_identifier
    if parquet_type is not None:
        kwargs["parquetType"] = parquet_type
    if export_filter is not None:
        kwargs["exportFilter"] = export_filter
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.start_export_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start export task") from exc
    return StartExportTaskResult(
        graph_id=resp.get("graphId"),
        role_arn=resp.get("roleArn"),
        task_id=resp.get("taskId"),
        status=resp.get("status"),
        format=resp.get("format"),
        destination=resp.get("destination"),
        kms_key_identifier=resp.get("kmsKeyIdentifier"),
        parquet_type=resp.get("parquetType"),
        status_reason=resp.get("statusReason"),
        export_filter=resp.get("exportFilter"),
    )


def start_graph(
    graph_identifier: str,
    region_name: str | None = None,
) -> StartGraphResult:
    """Start graph.

    Args:
        graph_identifier: Graph identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    try:
        resp = client.start_graph(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start graph") from exc
    return StartGraphResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        create_time=resp.get("createTime"),
        provisioned_memory=resp.get("provisionedMemory"),
        endpoint=resp.get("endpoint"),
        public_connectivity=resp.get("publicConnectivity"),
        vector_search_configuration=resp.get("vectorSearchConfiguration"),
        replica_count=resp.get("replicaCount"),
        kms_key_identifier=resp.get("kmsKeyIdentifier"),
        source_snapshot_id=resp.get("sourceSnapshotId"),
        deletion_protection=resp.get("deletionProtection"),
        build_number=resp.get("buildNumber"),
    )


def start_import_task(
    source: str,
    graph_identifier: str,
    role_arn: str,
    *,
    import_options: dict[str, Any] | None = None,
    fail_on_error: bool | None = None,
    format: str | None = None,
    parquet_type: str | None = None,
    blank_node_handling: str | None = None,
    region_name: str | None = None,
) -> StartImportTaskResult:
    """Start import task.

    Args:
        source: Source.
        graph_identifier: Graph identifier.
        role_arn: Role arn.
        import_options: Import options.
        fail_on_error: Fail on error.
        format: Format.
        parquet_type: Parquet type.
        blank_node_handling: Blank node handling.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["source"] = source
    kwargs["graphIdentifier"] = graph_identifier
    kwargs["roleArn"] = role_arn
    if import_options is not None:
        kwargs["importOptions"] = import_options
    if fail_on_error is not None:
        kwargs["failOnError"] = fail_on_error
    if format is not None:
        kwargs["format"] = format
    if parquet_type is not None:
        kwargs["parquetType"] = parquet_type
    if blank_node_handling is not None:
        kwargs["blankNodeHandling"] = blank_node_handling
    try:
        resp = client.start_import_task(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start import task") from exc
    return StartImportTaskResult(
        graph_id=resp.get("graphId"),
        task_id=resp.get("taskId"),
        source=resp.get("source"),
        format=resp.get("format"),
        parquet_type=resp.get("parquetType"),
        role_arn=resp.get("roleArn"),
        status=resp.get("status"),
        import_options=resp.get("importOptions"),
    )


def stop_graph(
    graph_identifier: str,
    region_name: str | None = None,
) -> StopGraphResult:
    """Stop graph.

    Args:
        graph_identifier: Graph identifier.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["graphIdentifier"] = graph_identifier
    try:
        resp = client.stop_graph(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to stop graph") from exc
    return StopGraphResult(
        id=resp.get("id"),
        name=resp.get("name"),
        arn=resp.get("arn"),
        status=resp.get("status"),
        status_reason=resp.get("statusReason"),
        create_time=resp.get("createTime"),
        provisioned_memory=resp.get("provisionedMemory"),
        endpoint=resp.get("endpoint"),
        public_connectivity=resp.get("publicConnectivity"),
        vector_search_configuration=resp.get("vectorSearchConfiguration"),
        replica_count=resp.get("replicaCount"),
        kms_key_identifier=resp.get("kmsKeyIdentifier"),
        source_snapshot_id=resp.get("sourceSnapshotId"),
        deletion_protection=resp.get("deletionProtection"),
        build_number=resp.get("buildNumber"),
    )


def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
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
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
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
    client = get_client("neptune-graph", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None
