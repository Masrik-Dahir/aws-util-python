

"""Tests for aws_util.aio.neptune_graph -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

import aws_util.aio.neptune_graph as mod
from aws_util.neptune_graph import GraphResult, GraphSnapshotResult
from aws_util.aio.neptune_graph import (

    list_graph_snapshots,
    create_graph_using_import_task,
    create_private_graph_endpoint,
    execute_query,
    get_graph_summary,
    list_export_tasks,
    list_import_tasks,
    list_private_graph_endpoints,
    list_queries,
    restore_graph_from_snapshot,
    start_export_task,
    start_import_task,
    cancel_export_task,
    cancel_import_task,
    cancel_query,
    delete_private_graph_endpoint,
    get_export_task,
    get_import_task,
    get_private_graph_endpoint,
    get_query,
    list_tags_for_resource,
    start_graph,
    stop_graph,
    tag_resource,
    untag_resource,
)



REGION = "us-east-1"
_GRAPH = {
    "id": "g-123",
    "name": "my-graph",
    "arn": "arn:aws:neptune-graph:us-east-1:123:graph/g-123",
    "status": "AVAILABLE",
    "provisionedMemory": 128,
    "endpoint": "g-123.endpoint",
    "publicConnectivity": False,
    "replicaCount": 1,
}

_SNAP = {
    "id": "gs-123",
    "name": "my-snap",
    "arn": "arn:aws:neptune-graph:us-east-1:123:snapshot/gs-123",
    "status": "AVAILABLE",
    "sourceGraphId": "g-123",
}


@pytest.fixture()
def mock_client(monkeypatch):
    client = AsyncMock()
    monkeypatch.setattr(
        "aws_util.aio.neptune_graph.async_client",
        lambda *a, **kw: client,
    )
    return client


# ---------------------------------------------------------------------------
# create_graph
# ---------------------------------------------------------------------------


async def test_create_graph_success(mock_client):
    mock_client.call.return_value = _GRAPH
    r = await mod.create_graph("g", 128)
    assert r.id == "g-123"


async def test_create_graph_kwargs(mock_client):
    mock_client.call.return_value = _GRAPH
    await mod.create_graph("g", 64, extra="val")
    call_kw = mock_client.call.call_args
    assert call_kw[1]["extra"] == "val"


async def test_create_graph_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_graph("g", 64)


async def test_create_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_graph failed"):
        await mod.create_graph("g", 64)


# ---------------------------------------------------------------------------
# get_graph
# ---------------------------------------------------------------------------


async def test_get_graph_success(mock_client):
    mock_client.call.return_value = _GRAPH
    r = await mod.get_graph("g-123")
    assert r.name == "my-graph"


async def test_get_graph_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_graph("g-123")


async def test_get_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_graph failed"):
        await mod.get_graph("g-123")


# ---------------------------------------------------------------------------
# list_graphs
# ---------------------------------------------------------------------------


async def test_list_graphs_single(mock_client):
    mock_client.call.return_value = {"graphs": [_GRAPH]}
    r = await mod.list_graphs()
    assert len(r) == 1


async def test_list_graphs_pagination(mock_client):
    mock_client.call.side_effect = [
        {"graphs": [_GRAPH], "nextToken": "t1"},
        {"graphs": [_GRAPH]},
    ]
    r = await mod.list_graphs()
    assert len(r) == 2


async def test_list_graphs_empty(mock_client):
    mock_client.call.return_value = {"graphs": []}
    assert await mod.list_graphs() == []


async def test_list_graphs_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_graphs()


async def test_list_graphs_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_graphs failed"):
        await mod.list_graphs()


# ---------------------------------------------------------------------------
# delete_graph
# ---------------------------------------------------------------------------


async def test_delete_graph_success(mock_client):
    mock_client.call.return_value = {}
    await mod.delete_graph("g-123")
    mock_client.call.assert_called_once()


async def test_delete_graph_no_skip(mock_client):
    mock_client.call.return_value = {}
    await mod.delete_graph("g-123", skip_snapshot=False)
    kw = mock_client.call.call_args[1]
    assert kw["skipSnapshot"] is False


async def test_delete_graph_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_graph("g-123")


async def test_delete_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_graph failed"):
        await mod.delete_graph("g-123")


# ---------------------------------------------------------------------------
# update_graph
# ---------------------------------------------------------------------------


async def test_update_graph_success(mock_client):
    mock_client.call.return_value = _GRAPH
    r = await mod.update_graph("g-123", provisionedMemory=256)
    assert r.id == "g-123"


async def test_update_graph_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.update_graph("g-123")


async def test_update_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="update_graph failed"):
        await mod.update_graph("g-123")


# ---------------------------------------------------------------------------
# create_graph_snapshot
# ---------------------------------------------------------------------------


async def test_create_graph_snapshot_success(mock_client):
    mock_client.call.return_value = _SNAP
    r = await mod.create_graph_snapshot("g-123", "snap")
    assert r.id == "gs-123"


async def test_create_graph_snapshot_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.create_graph_snapshot("g-123", "snap")


async def test_create_graph_snapshot_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="create_graph_snapshot failed"):
        await mod.create_graph_snapshot("g-123", "snap")


# ---------------------------------------------------------------------------
# get_graph_snapshot
# ---------------------------------------------------------------------------


async def test_get_graph_snapshot_success(mock_client):
    mock_client.call.return_value = _SNAP
    r = await mod.get_graph_snapshot("gs-123")
    assert r.name == "my-snap"


async def test_get_graph_snapshot_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.get_graph_snapshot("gs-123")


async def test_get_graph_snapshot_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="get_graph_snapshot failed"):
        await mod.get_graph_snapshot("gs-123")


# ---------------------------------------------------------------------------
# list_graph_snapshots
# ---------------------------------------------------------------------------


async def test_list_graph_snapshots_success(mock_client):
    mock_client.call.return_value = {"graphSnapshots": [_SNAP]}
    r = await mod.list_graph_snapshots()
    assert len(r) == 1


async def test_list_graph_snapshots_with_graph(mock_client):
    mock_client.call.return_value = {"graphSnapshots": [_SNAP]}
    r = await mod.list_graph_snapshots("g-123")
    assert len(r) == 1
    kw = mock_client.call.call_args[1]
    assert kw["graphIdentifier"] == "g-123"


async def test_list_graph_snapshots_pagination(mock_client):
    mock_client.call.side_effect = [
        {"graphSnapshots": [_SNAP], "nextToken": "t1"},
        {"graphSnapshots": [_SNAP]},
    ]
    r = await mod.list_graph_snapshots()
    assert len(r) == 2


async def test_list_graph_snapshots_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.list_graph_snapshots()


async def test_list_graph_snapshots_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="list_graph_snapshots failed"):
        await mod.list_graph_snapshots()


# ---------------------------------------------------------------------------
# delete_graph_snapshot
# ---------------------------------------------------------------------------


async def test_delete_graph_snapshot_success(mock_client):
    mock_client.call.return_value = {}
    await mod.delete_graph_snapshot("gs-123")
    mock_client.call.assert_called_once()


async def test_delete_graph_snapshot_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.delete_graph_snapshot("gs-123")


async def test_delete_graph_snapshot_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="delete_graph_snapshot failed"):
        await mod.delete_graph_snapshot("gs-123")


# ---------------------------------------------------------------------------
# reset_graph
# ---------------------------------------------------------------------------


async def test_reset_graph_success(mock_client):
    mock_client.call.return_value = _GRAPH
    r = await mod.reset_graph("g-123")
    assert r.id == "g-123"


async def test_reset_graph_no_cleanup(mock_client):
    mock_client.call.return_value = _GRAPH
    await mod.reset_graph("g-123", perform_clean_up=False)
    kw = mock_client.call.call_args[1]
    assert kw["performCleanUp"] is False


async def test_reset_graph_runtime_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await mod.reset_graph("g-123")


async def test_reset_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="reset_graph failed"):
        await mod.reset_graph("g-123")


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


async def test_cancel_export_task(mock_client):
    mock_client.call.return_value = {}
    await cancel_export_task("test-task_identifier", )
    mock_client.call.assert_called_once()


async def test_cancel_export_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_export_task("test-task_identifier", )


async def test_cancel_export_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to cancel export task"):
        await cancel_export_task("test-task_identifier", )


async def test_cancel_import_task(mock_client):
    mock_client.call.return_value = {}
    await cancel_import_task("test-task_identifier", )
    mock_client.call.assert_called_once()


async def test_cancel_import_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_import_task("test-task_identifier", )


async def test_cancel_import_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to cancel import task"):
        await cancel_import_task("test-task_identifier", )


async def test_cancel_query(mock_client):
    mock_client.call.return_value = {}
    await cancel_query("test-graph_identifier", "test-query_id", )
    mock_client.call.assert_called_once()


async def test_cancel_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_query("test-graph_identifier", "test-query_id", )


async def test_cancel_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to cancel query"):
        await cancel_query("test-graph_identifier", "test-query_id", )


async def test_create_graph_using_import_task(mock_client):
    mock_client.call.return_value = {}
    await create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_graph_using_import_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", )


async def test_create_graph_using_import_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create graph using import task"):
        await create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", )


async def test_create_private_graph_endpoint(mock_client):
    mock_client.call.return_value = {}
    await create_private_graph_endpoint("test-graph_identifier", )
    mock_client.call.assert_called_once()


async def test_create_private_graph_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await create_private_graph_endpoint("test-graph_identifier", )


async def test_create_private_graph_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to create private graph endpoint"):
        await create_private_graph_endpoint("test-graph_identifier", )


async def test_delete_private_graph_endpoint(mock_client):
    mock_client.call.return_value = {}
    await delete_private_graph_endpoint("test-graph_identifier", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_delete_private_graph_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await delete_private_graph_endpoint("test-graph_identifier", "test-vpc_id", )


async def test_delete_private_graph_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to delete private graph endpoint"):
        await delete_private_graph_endpoint("test-graph_identifier", "test-vpc_id", )


async def test_execute_query(mock_client):
    mock_client.call.return_value = {}
    await execute_query("test-graph_identifier", "test-query_string", "test-language", )
    mock_client.call.assert_called_once()


async def test_execute_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await execute_query("test-graph_identifier", "test-query_string", "test-language", )


async def test_execute_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to execute query"):
        await execute_query("test-graph_identifier", "test-query_string", "test-language", )


async def test_get_export_task(mock_client):
    mock_client.call.return_value = {}
    await get_export_task("test-task_identifier", )
    mock_client.call.assert_called_once()


async def test_get_export_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_export_task("test-task_identifier", )


async def test_get_export_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get export task"):
        await get_export_task("test-task_identifier", )


async def test_get_graph_summary(mock_client):
    mock_client.call.return_value = {}
    await get_graph_summary("test-graph_identifier", )
    mock_client.call.assert_called_once()


async def test_get_graph_summary_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_graph_summary("test-graph_identifier", )


async def test_get_graph_summary_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get graph summary"):
        await get_graph_summary("test-graph_identifier", )


async def test_get_import_task(mock_client):
    mock_client.call.return_value = {}
    await get_import_task("test-task_identifier", )
    mock_client.call.assert_called_once()


async def test_get_import_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_import_task("test-task_identifier", )


async def test_get_import_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get import task"):
        await get_import_task("test-task_identifier", )


async def test_get_private_graph_endpoint(mock_client):
    mock_client.call.return_value = {}
    await get_private_graph_endpoint("test-graph_identifier", "test-vpc_id", )
    mock_client.call.assert_called_once()


async def test_get_private_graph_endpoint_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_private_graph_endpoint("test-graph_identifier", "test-vpc_id", )


async def test_get_private_graph_endpoint_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get private graph endpoint"):
        await get_private_graph_endpoint("test-graph_identifier", "test-vpc_id", )


async def test_get_query(mock_client):
    mock_client.call.return_value = {}
    await get_query("test-graph_identifier", "test-query_id", )
    mock_client.call.assert_called_once()


async def test_get_query_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await get_query("test-graph_identifier", "test-query_id", )


async def test_get_query_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to get query"):
        await get_query("test-graph_identifier", "test-query_id", )


async def test_list_export_tasks(mock_client):
    mock_client.call.return_value = {}
    await list_export_tasks()
    mock_client.call.assert_called_once()


async def test_list_export_tasks_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_export_tasks()


async def test_list_export_tasks_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list export tasks"):
        await list_export_tasks()


async def test_list_import_tasks(mock_client):
    mock_client.call.return_value = {}
    await list_import_tasks()
    mock_client.call.assert_called_once()


async def test_list_import_tasks_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_import_tasks()


async def test_list_import_tasks_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list import tasks"):
        await list_import_tasks()


async def test_list_private_graph_endpoints(mock_client):
    mock_client.call.return_value = {}
    await list_private_graph_endpoints("test-graph_identifier", )
    mock_client.call.assert_called_once()


async def test_list_private_graph_endpoints_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_private_graph_endpoints("test-graph_identifier", )


async def test_list_private_graph_endpoints_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list private graph endpoints"):
        await list_private_graph_endpoints("test-graph_identifier", )


async def test_list_queries(mock_client):
    mock_client.call.return_value = {}
    await list_queries("test-graph_identifier", 1, )
    mock_client.call.assert_called_once()


async def test_list_queries_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_queries("test-graph_identifier", 1, )


async def test_list_queries_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list queries"):
        await list_queries("test-graph_identifier", 1, )


async def test_list_tags_for_resource(mock_client):
    mock_client.call.return_value = {}
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_tags_for_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        await list_tags_for_resource("test-resource_arn", )


async def test_restore_graph_from_snapshot(mock_client):
    mock_client.call.return_value = {}
    await restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", )
    mock_client.call.assert_called_once()


async def test_restore_graph_from_snapshot_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", )


async def test_restore_graph_from_snapshot_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to restore graph from snapshot"):
        await restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", )


async def test_start_export_task(mock_client):
    mock_client.call.return_value = {}
    await start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", )
    mock_client.call.assert_called_once()


async def test_start_export_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", )


async def test_start_export_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start export task"):
        await start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", )


async def test_start_graph(mock_client):
    mock_client.call.return_value = {}
    await start_graph("test-graph_identifier", )
    mock_client.call.assert_called_once()


async def test_start_graph_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_graph("test-graph_identifier", )


async def test_start_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start graph"):
        await start_graph("test-graph_identifier", )


async def test_start_import_task(mock_client):
    mock_client.call.return_value = {}
    await start_import_task("test-source", "test-graph_identifier", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_start_import_task_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await start_import_task("test-source", "test-graph_identifier", "test-role_arn", )


async def test_start_import_task_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to start import task"):
        await start_import_task("test-source", "test-graph_identifier", "test-role_arn", )


async def test_stop_graph(mock_client):
    mock_client.call.return_value = {}
    await stop_graph("test-graph_identifier", )
    mock_client.call.assert_called_once()


async def test_stop_graph_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await stop_graph("test-graph_identifier", )


async def test_stop_graph_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to stop graph"):
        await stop_graph("test-graph_identifier", )


async def test_tag_resource(mock_client):
    mock_client.call.return_value = {}
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_tag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(mock_client):
    mock_client.call.return_value = {}
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(mock_client):
    mock_client.call.side_effect = RuntimeError("boom")
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_untag_resource_generic_error(mock_client):
    mock_client.call.side_effect = ValueError("bad")
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        await untag_resource("test-resource_arn", [], )


@pytest.mark.asyncio
async def test_list_graph_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import list_graph_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await list_graph_snapshots(graph_identifier="test-graph_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_graph_using_import_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import create_graph_using_import_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", tags=[{"Key": "k", "Value": "v"}], public_connectivity="test-public_connectivity", kms_key_identifier="test-kms_key_identifier", vector_search_configuration={}, replica_count=1, deletion_protection="test-deletion_protection", import_options=1, max_provisioned_memory=1, min_provisioned_memory="test-min_provisioned_memory", fail_on_error="test-fail_on_error", format="test-format", parquet_type="test-parquet_type", blank_node_handling="test-blank_node_handling", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_private_graph_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import create_private_graph_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await create_private_graph_endpoint("test-graph_identifier", vpc_id="test-vpc_id", subnet_ids="test-subnet_ids", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_execute_query_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import execute_query
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await execute_query("test-graph_identifier", "test-query_string", "test-language", parameters="test-parameters", plan_cache="test-plan_cache", explain_mode="test-explain_mode", query_timeout_milliseconds=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_graph_summary_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import get_graph_summary
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await get_graph_summary("test-graph_identifier", mode="test-mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_export_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import list_export_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await list_export_tasks(graph_identifier="test-graph_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_import_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import list_import_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await list_import_tasks(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_private_graph_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import list_private_graph_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await list_private_graph_endpoints("test-graph_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_queries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import list_queries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await list_queries("test-graph_identifier", 1, state="test-state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_graph_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import restore_graph_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", provisioned_memory="test-provisioned_memory", deletion_protection="test-deletion_protection", tags=[{"Key": "k", "Value": "v"}], replica_count=1, public_connectivity="test-public_connectivity", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_export_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import start_export_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", parquet_type="test-parquet_type", export_filter=[{}], tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_import_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune_graph import start_import_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune_graph.async_client", lambda *a, **kw: mock_client)
    await start_import_task("test-source", "test-graph_identifier", "test-role_arn", import_options=1, fail_on_error="test-fail_on_error", format="test-format", parquet_type="test-parquet_type", blank_node_handling="test-blank_node_handling", region_name="us-east-1")
    mock_client.call.assert_called_once()
