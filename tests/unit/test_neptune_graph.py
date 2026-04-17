"""Tests for aws_util.neptune_graph module."""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.neptune_graph as mod
from aws_util.neptune_graph import (
    GraphResult,
    GraphSnapshotResult,
    _parse_graph,
    _parse_graph_snapshot,
    create_graph,
    create_graph_snapshot,
    delete_graph,
    delete_graph_snapshot,
    get_graph,
    get_graph_snapshot,
    list_graph_snapshots,
    list_graphs,
    reset_graph,
    update_graph,
    cancel_export_task,
    cancel_import_task,
    cancel_query,
    create_graph_using_import_task,
    create_private_graph_endpoint,
    delete_private_graph_endpoint,
    execute_query,
    get_export_task,
    get_graph_summary,
    get_import_task,
    get_private_graph_endpoint,
    get_query,
    list_export_tasks,
    list_import_tasks,
    list_private_graph_endpoints,
    list_queries,
    list_tags_for_resource,
    restore_graph_from_snapshot,
    start_export_task,
    start_graph,
    start_import_task,
    stop_graph,
    tag_resource,
    untag_resource,
)

REGION = "us-east-1"

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

_GRAPH = {
    "id": "g-123",
    "name": "my-graph",
    "arn": "arn:aws:neptune-graph:us-east-1:123:graph/g-123",
    "status": "AVAILABLE",
    "provisionedMemory": 128,
    "endpoint": "g-123.us-east-1.neptune-graph.amazonaws.com",
    "publicConnectivity": False,
    "replicaCount": 1,
    "extraKey": "extraVal",
}

_SNAP = {
    "id": "gs-123",
    "name": "my-snap",
    "arn": "arn:aws:neptune-graph:us-east-1:123:snapshot/gs-123",
    "status": "AVAILABLE",
    "sourceGraphId": "g-123",
    "extraSnap": "val",
}


def _ce(code: str = "ServiceException", msg: str = "fail") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


def test_graph_result_model():
    r = GraphResult(id="g1", name="n1")
    assert r.id == "g1"
    assert r.name == "n1"
    assert r.arn is None
    assert r.extra == {}


def test_graph_snapshot_result_model():
    r = GraphSnapshotResult(id="gs1", name="sn1", source_graph_id="g1")
    assert r.id == "gs1"
    assert r.source_graph_id == "g1"


# ---------------------------------------------------------------------------
# _parse helpers
# ---------------------------------------------------------------------------


def test_parse_graph():
    r = _parse_graph(_GRAPH)
    assert r.id == "g-123"
    assert r.provisioned_memory == 128
    assert r.public_connectivity is False
    assert r.replica_count == 1
    assert "extraKey" in r.extra


def test_parse_graph_snapshot():
    r = _parse_graph_snapshot(_SNAP)
    assert r.id == "gs-123"
    assert r.source_graph_id == "g-123"
    assert "extraSnap" in r.extra


# ---------------------------------------------------------------------------
# create_graph
# ---------------------------------------------------------------------------


def test_create_graph_success(monkeypatch):
    client = MagicMock()
    client.create_graph.return_value = _GRAPH
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_graph("my-graph", 128, region_name=REGION)
    assert r.id == "g-123"


def test_create_graph_kwargs(monkeypatch):
    client = MagicMock()
    client.create_graph.return_value = _GRAPH
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_graph("g", 64, region_name=REGION, extra="val")
    assert r.id == "g-123"
    client.create_graph.assert_called_once_with(
        graphName="g", provisionedMemory=64, extra="val"
    )


def test_create_graph_error(monkeypatch):
    client = MagicMock()
    client.create_graph.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_graph failed"):
        create_graph("g", 64, region_name=REGION)


# ---------------------------------------------------------------------------
# get_graph
# ---------------------------------------------------------------------------


def test_get_graph_success(monkeypatch):
    client = MagicMock()
    client.get_graph.return_value = _GRAPH
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_graph("g-123", region_name=REGION)
    assert r.name == "my-graph"


def test_get_graph_error(monkeypatch):
    client = MagicMock()
    client.get_graph.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_graph failed"):
        get_graph("g-123", region_name=REGION)


# ---------------------------------------------------------------------------
# list_graphs
# ---------------------------------------------------------------------------


def test_list_graphs_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"graphs": [_GRAPH]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_graphs(region_name=REGION)
    assert len(r) == 1
    assert r[0].id == "g-123"


def test_list_graphs_empty(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"graphs": []}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    assert list_graphs(region_name=REGION) == []


def test_list_graphs_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_graphs failed"):
        list_graphs(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_graph
# ---------------------------------------------------------------------------


def test_delete_graph_success(monkeypatch):
    client = MagicMock()
    client.delete_graph.return_value = {}
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_graph("g-123", region_name=REGION)
    client.delete_graph.assert_called_once_with(
        graphIdentifier="g-123", skipSnapshot=True
    )


def test_delete_graph_no_skip(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_graph("g-123", skip_snapshot=False, region_name=REGION)
    client.delete_graph.assert_called_once_with(
        graphIdentifier="g-123", skipSnapshot=False
    )


def test_delete_graph_error(monkeypatch):
    client = MagicMock()
    client.delete_graph.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_graph failed"):
        delete_graph("g-123", region_name=REGION)


# ---------------------------------------------------------------------------
# update_graph
# ---------------------------------------------------------------------------


def test_update_graph_success(monkeypatch):
    client = MagicMock()
    client.update_graph.return_value = _GRAPH
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = update_graph("g-123", region_name=REGION, provisionedMemory=256)
    assert r.id == "g-123"


def test_update_graph_error(monkeypatch):
    client = MagicMock()
    client.update_graph.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="update_graph failed"):
        update_graph("g-123", region_name=REGION)


# ---------------------------------------------------------------------------
# create_graph_snapshot
# ---------------------------------------------------------------------------


def test_create_graph_snapshot_success(monkeypatch):
    client = MagicMock()
    client.create_graph_snapshot.return_value = _SNAP
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = create_graph_snapshot("g-123", "my-snap", region_name=REGION)
    assert r.id == "gs-123"


def test_create_graph_snapshot_error(monkeypatch):
    client = MagicMock()
    client.create_graph_snapshot.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="create_graph_snapshot failed"):
        create_graph_snapshot("g-123", "snap", region_name=REGION)


# ---------------------------------------------------------------------------
# get_graph_snapshot
# ---------------------------------------------------------------------------


def test_get_graph_snapshot_success(monkeypatch):
    client = MagicMock()
    client.get_graph_snapshot.return_value = _SNAP
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = get_graph_snapshot("gs-123", region_name=REGION)
    assert r.name == "my-snap"


def test_get_graph_snapshot_error(monkeypatch):
    client = MagicMock()
    client.get_graph_snapshot.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="get_graph_snapshot failed"):
        get_graph_snapshot("gs-123", region_name=REGION)


# ---------------------------------------------------------------------------
# list_graph_snapshots
# ---------------------------------------------------------------------------


def test_list_graph_snapshots_success(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"graphSnapshots": [_SNAP]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_graph_snapshots(region_name=REGION)
    assert len(r) == 1


def test_list_graph_snapshots_with_graph_id(monkeypatch):
    client = MagicMock()
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"graphSnapshots": [_SNAP]}]
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = list_graph_snapshots("g-123", region_name=REGION)
    assert len(r) == 1


def test_list_graph_snapshots_error(monkeypatch):
    client = MagicMock()
    client.get_paginator.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="list_graph_snapshots failed"):
        list_graph_snapshots(region_name=REGION)


# ---------------------------------------------------------------------------
# delete_graph_snapshot
# ---------------------------------------------------------------------------


def test_delete_graph_snapshot_success(monkeypatch):
    client = MagicMock()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    delete_graph_snapshot("gs-123", region_name=REGION)
    client.delete_graph_snapshot.assert_called_once()


def test_delete_graph_snapshot_error(monkeypatch):
    client = MagicMock()
    client.delete_graph_snapshot.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="delete_graph_snapshot failed"):
        delete_graph_snapshot("gs-123", region_name=REGION)


# ---------------------------------------------------------------------------
# reset_graph
# ---------------------------------------------------------------------------


def test_reset_graph_success(monkeypatch):
    client = MagicMock()
    client.reset_graph.return_value = _GRAPH
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    r = reset_graph("g-123", region_name=REGION)
    assert r.id == "g-123"


def test_reset_graph_no_cleanup(monkeypatch):
    client = MagicMock()
    client.reset_graph.return_value = _GRAPH
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    reset_graph("g-123", perform_clean_up=False, region_name=REGION)
    client.reset_graph.assert_called_once_with(
        graphIdentifier="g-123", performCleanUp=False
    )


def test_reset_graph_error(monkeypatch):
    client = MagicMock()
    client.reset_graph.side_effect = _ce()
    monkeypatch.setattr(mod, "get_client", lambda *a, **kw: client)
    with pytest.raises(RuntimeError, match="reset_graph failed"):
        reset_graph("g-123", region_name=REGION)


# ---------------------------------------------------------------------------
# __all__
# ---------------------------------------------------------------------------


def test_all_exports():
    for name in mod.__all__:
        assert hasattr(mod, name)


def test_cancel_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    cancel_export_task("test-task_identifier", region_name=REGION)
    mock_client.cancel_export_task.assert_called_once()


def test_cancel_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_export_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel export task"):
        cancel_export_task("test-task_identifier", region_name=REGION)


def test_cancel_import_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_import_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    cancel_import_task("test-task_identifier", region_name=REGION)
    mock_client.cancel_import_task.assert_called_once()


def test_cancel_import_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_import_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_import_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel import task"):
        cancel_import_task("test-task_identifier", region_name=REGION)


def test_cancel_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_query.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    cancel_query("test-graph_identifier", "test-query_id", region_name=REGION)
    mock_client.cancel_query.assert_called_once()


def test_cancel_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_query",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel query"):
        cancel_query("test-graph_identifier", "test-query_id", region_name=REGION)


def test_create_graph_using_import_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_graph_using_import_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", region_name=REGION)
    mock_client.create_graph_using_import_task.assert_called_once()


def test_create_graph_using_import_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_graph_using_import_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_graph_using_import_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create graph using import task"):
        create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", region_name=REGION)


def test_create_private_graph_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_private_graph_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    create_private_graph_endpoint("test-graph_identifier", region_name=REGION)
    mock_client.create_private_graph_endpoint.assert_called_once()


def test_create_private_graph_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_private_graph_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_private_graph_endpoint",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create private graph endpoint"):
        create_private_graph_endpoint("test-graph_identifier", region_name=REGION)


def test_delete_private_graph_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_private_graph_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    delete_private_graph_endpoint("test-graph_identifier", "test-vpc_id", region_name=REGION)
    mock_client.delete_private_graph_endpoint.assert_called_once()


def test_delete_private_graph_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_private_graph_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_private_graph_endpoint",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete private graph endpoint"):
        delete_private_graph_endpoint("test-graph_identifier", "test-vpc_id", region_name=REGION)


def test_execute_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_query.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    execute_query("test-graph_identifier", "test-query_string", "test-language", region_name=REGION)
    mock_client.execute_query.assert_called_once()


def test_execute_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.execute_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "execute_query",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to execute query"):
        execute_query("test-graph_identifier", "test-query_string", "test-language", region_name=REGION)


def test_get_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    get_export_task("test-task_identifier", region_name=REGION)
    mock_client.get_export_task.assert_called_once()


def test_get_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_export_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get export task"):
        get_export_task("test-task_identifier", region_name=REGION)


def test_get_graph_summary(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_graph_summary.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    get_graph_summary("test-graph_identifier", region_name=REGION)
    mock_client.get_graph_summary.assert_called_once()


def test_get_graph_summary_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_graph_summary.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_graph_summary",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get graph summary"):
        get_graph_summary("test-graph_identifier", region_name=REGION)


def test_get_import_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_import_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    get_import_task("test-task_identifier", region_name=REGION)
    mock_client.get_import_task.assert_called_once()


def test_get_import_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_import_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_import_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get import task"):
        get_import_task("test-task_identifier", region_name=REGION)


def test_get_private_graph_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_private_graph_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    get_private_graph_endpoint("test-graph_identifier", "test-vpc_id", region_name=REGION)
    mock_client.get_private_graph_endpoint.assert_called_once()


def test_get_private_graph_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_private_graph_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_private_graph_endpoint",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get private graph endpoint"):
        get_private_graph_endpoint("test-graph_identifier", "test-vpc_id", region_name=REGION)


def test_get_query(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    get_query("test-graph_identifier", "test-query_id", region_name=REGION)
    mock_client.get_query.assert_called_once()


def test_get_query_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_query.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_query",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get query"):
        get_query("test-graph_identifier", "test-query_id", region_name=REGION)


def test_list_export_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_export_tasks.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_export_tasks(region_name=REGION)
    mock_client.list_export_tasks.assert_called_once()


def test_list_export_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_export_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_export_tasks",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list export tasks"):
        list_export_tasks(region_name=REGION)


def test_list_import_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_import_tasks.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_import_tasks(region_name=REGION)
    mock_client.list_import_tasks.assert_called_once()


def test_list_import_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_import_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_import_tasks",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list import tasks"):
        list_import_tasks(region_name=REGION)


def test_list_private_graph_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_private_graph_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_private_graph_endpoints("test-graph_identifier", region_name=REGION)
    mock_client.list_private_graph_endpoints.assert_called_once()


def test_list_private_graph_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_private_graph_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_private_graph_endpoints",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list private graph endpoints"):
        list_private_graph_endpoints("test-graph_identifier", region_name=REGION)


def test_list_queries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_queries.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_queries("test-graph_identifier", 1, region_name=REGION)
    mock_client.list_queries.assert_called_once()


def test_list_queries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_queries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_queries",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list queries"):
        list_queries("test-graph_identifier", 1, region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_restore_graph_from_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_graph_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", region_name=REGION)
    mock_client.restore_graph_from_snapshot.assert_called_once()


def test_restore_graph_from_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_graph_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_graph_from_snapshot",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore graph from snapshot"):
        restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", region_name=REGION)


def test_start_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_export_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", region_name=REGION)
    mock_client.start_export_task.assert_called_once()


def test_start_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_export_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start export task"):
        start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", region_name=REGION)


def test_start_graph(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_graph.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    start_graph("test-graph_identifier", region_name=REGION)
    mock_client.start_graph.assert_called_once()


def test_start_graph_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_graph.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_graph",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start graph"):
        start_graph("test-graph_identifier", region_name=REGION)


def test_start_import_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_import_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    start_import_task("test-source", "test-graph_identifier", "test-role_arn", region_name=REGION)
    mock_client.start_import_task.assert_called_once()


def test_start_import_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_import_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_import_task",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start import task"):
        start_import_task("test-source", "test-graph_identifier", "test-role_arn", region_name=REGION)


def test_stop_graph(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_graph.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    stop_graph("test-graph_identifier", region_name=REGION)
    mock_client.stop_graph.assert_called_once()


def test_stop_graph_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_graph.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_graph",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop graph"):
        stop_graph("test-graph_identifier", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_create_graph_using_import_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import create_graph_using_import_task
    mock_client = MagicMock()
    mock_client.create_graph_using_import_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    create_graph_using_import_task("test-graph_name", "test-source", "test-role_arn", tags=[{"Key": "k", "Value": "v"}], public_connectivity="test-public_connectivity", kms_key_identifier="test-kms_key_identifier", vector_search_configuration={}, replica_count=1, deletion_protection="test-deletion_protection", import_options=1, max_provisioned_memory=1, min_provisioned_memory="test-min_provisioned_memory", fail_on_error="test-fail_on_error", format="test-format", parquet_type="test-parquet_type", blank_node_handling="test-blank_node_handling", region_name="us-east-1")
    mock_client.create_graph_using_import_task.assert_called_once()

def test_create_private_graph_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import create_private_graph_endpoint
    mock_client = MagicMock()
    mock_client.create_private_graph_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    create_private_graph_endpoint("test-graph_identifier", vpc_id="test-vpc_id", subnet_ids="test-subnet_ids", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.create_private_graph_endpoint.assert_called_once()

def test_execute_query_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import execute_query
    mock_client = MagicMock()
    mock_client.execute_query.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    execute_query("test-graph_identifier", "test-query_string", "test-language", parameters="test-parameters", plan_cache="test-plan_cache", explain_mode="test-explain_mode", query_timeout_milliseconds=1, region_name="us-east-1")
    mock_client.execute_query.assert_called_once()

def test_get_graph_summary_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import get_graph_summary
    mock_client = MagicMock()
    mock_client.get_graph_summary.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    get_graph_summary("test-graph_identifier", mode="test-mode", region_name="us-east-1")
    mock_client.get_graph_summary.assert_called_once()

def test_list_export_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import list_export_tasks
    mock_client = MagicMock()
    mock_client.list_export_tasks.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_export_tasks(graph_identifier="test-graph_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_export_tasks.assert_called_once()

def test_list_import_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import list_import_tasks
    mock_client = MagicMock()
    mock_client.list_import_tasks.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_import_tasks(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_import_tasks.assert_called_once()

def test_list_private_graph_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import list_private_graph_endpoints
    mock_client = MagicMock()
    mock_client.list_private_graph_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_private_graph_endpoints("test-graph_identifier", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_private_graph_endpoints.assert_called_once()

def test_list_queries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import list_queries
    mock_client = MagicMock()
    mock_client.list_queries.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    list_queries("test-graph_identifier", 1, state="test-state", region_name="us-east-1")
    mock_client.list_queries.assert_called_once()

def test_restore_graph_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import restore_graph_from_snapshot
    mock_client = MagicMock()
    mock_client.restore_graph_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    restore_graph_from_snapshot("test-snapshot_identifier", "test-graph_name", provisioned_memory="test-provisioned_memory", deletion_protection="test-deletion_protection", tags=[{"Key": "k", "Value": "v"}], replica_count=1, public_connectivity="test-public_connectivity", region_name="us-east-1")
    mock_client.restore_graph_from_snapshot.assert_called_once()

def test_start_export_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import start_export_task
    mock_client = MagicMock()
    mock_client.start_export_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    start_export_task("test-graph_identifier", "test-role_arn", "test-format", "test-destination", "test-kms_key_identifier", parquet_type="test-parquet_type", export_filter=[{}], tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.start_export_task.assert_called_once()

def test_start_import_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune_graph import start_import_task
    mock_client = MagicMock()
    mock_client.start_import_task.return_value = {}
    monkeypatch.setattr("aws_util.neptune_graph.get_client", lambda *a, **kw: mock_client)
    start_import_task("test-source", "test-graph_identifier", "test-role_arn", import_options=1, fail_on_error="test-fail_on_error", format="test-format", parquet_type="test-parquet_type", blank_node_handling="test-blank_node_handling", region_name="us-east-1")
    mock_client.start_import_task.assert_called_once()
