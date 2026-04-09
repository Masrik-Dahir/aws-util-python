"""Tests for aws_util.aio.neptune -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.neptune import (
    NeptuneCluster,
    NeptuneClusterSnapshot,
    NeptuneInstance,
    create_db_cluster,
    create_db_cluster_snapshot,
    create_db_instance,
    delete_db_cluster,
    delete_db_instance,
    describe_db_cluster_snapshots,
    describe_db_clusters,
    describe_db_instances,
    failover_db_cluster,
    modify_db_cluster,
    modify_db_instance,
    wait_for_db_cluster,
    add_role_to_db_cluster,
    add_source_identifier_to_subscription,
    add_tags_to_resource,
    apply_pending_maintenance_action,
    copy_db_cluster_parameter_group,
    copy_db_cluster_snapshot,
    copy_db_parameter_group,
    create_db_cluster_endpoint,
    create_db_cluster_parameter_group,
    create_db_parameter_group,
    create_db_subnet_group,
    create_event_subscription,
    create_global_cluster,
    delete_db_cluster_endpoint,
    delete_db_cluster_parameter_group,
    delete_db_cluster_snapshot,
    delete_db_parameter_group,
    delete_db_subnet_group,
    delete_event_subscription,
    delete_global_cluster,
    describe_db_cluster_endpoints,
    describe_db_cluster_parameter_groups,
    describe_db_cluster_parameters,
    describe_db_cluster_snapshot_attributes,
    describe_db_engine_versions,
    describe_db_parameter_groups,
    describe_db_parameters,
    describe_db_subnet_groups,
    describe_engine_default_cluster_parameters,
    describe_engine_default_parameters,
    describe_event_categories,
    describe_event_subscriptions,
    describe_events,
    describe_global_clusters,
    describe_orderable_db_instance_options,
    describe_pending_maintenance_actions,
    describe_valid_db_instance_modifications,
    failover_global_cluster,
    list_tags_for_resource,
    modify_db_cluster_endpoint,
    modify_db_cluster_parameter_group,
    modify_db_cluster_snapshot_attribute,
    modify_db_parameter_group,
    modify_db_subnet_group,
    modify_event_subscription,
    modify_global_cluster,
    promote_read_replica_db_cluster,
    reboot_db_instance,
    remove_from_global_cluster,
    remove_role_from_db_cluster,
    remove_source_identifier_from_subscription,
    remove_tags_from_resource,
    reset_db_cluster_parameter_group,
    reset_db_parameter_group,
    restore_db_cluster_from_snapshot,
    restore_db_cluster_to_point_in_time,
    start_db_cluster,
    stop_db_cluster,
    switchover_global_cluster,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError

_PATCH = "aws_util.aio.neptune.async_client"

_CLUSTER_DATA = {
    "DBClusterIdentifier": "my-cluster",
    "Status": "available",
    "Engine": "neptune",
    "EngineVersion": "1.2.0.0",
    "Endpoint": "ep.amazonaws.com",
    "ReaderEndpoint": "reader.amazonaws.com",
    "Port": 8182,
    "MultiAZ": True,
    "StorageEncrypted": True,
}

_INSTANCE_DATA = {
    "DBInstanceIdentifier": "my-instance",
    "DBInstanceClass": "db.r5.large",
    "Engine": "neptune",
    "EngineVersion": "1.2.0.0",
    "DBInstanceStatus": "available",
    "Endpoint": {"Address": "inst.amazonaws.com", "Port": 8182},
    "AvailabilityZone": "us-east-1a",
    "DBClusterIdentifier": "my-cluster",
}

_SNAPSHOT_DATA = {
    "DBClusterSnapshotIdentifier": "my-snap",
    "DBClusterIdentifier": "my-cluster",
    "Status": "available",
    "Engine": "neptune",
    "EngineVersion": "1.2.0.0",
    "SnapshotType": "manual",
    "AllocatedStorage": 10,
}


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# create_db_cluster
# ---------------------------------------------------------------------------


async def test_create_db_cluster_ok(monkeypatch):
    mc = _mc({"DBCluster": _CLUSTER_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_db_cluster("my-cluster")
    assert r.db_cluster_identifier == "my-cluster"


async def test_create_db_cluster_with_version(monkeypatch):
    mc = _mc({"DBCluster": _CLUSTER_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_db_cluster("my-cluster", engine_version="1.2.0.0")
    assert r.db_cluster_identifier == "my-cluster"


async def test_create_db_cluster_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_db_cluster failed"):
        await create_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# describe_db_clusters
# ---------------------------------------------------------------------------


async def test_describe_db_clusters_ok(monkeypatch):
    mc = _mc({"DBClusters": [_CLUSTER_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_clusters()
    assert len(r) == 1


async def test_describe_db_clusters_with_id(monkeypatch):
    mc = _mc({"DBClusters": [_CLUSTER_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_clusters("my-cluster")
    assert len(r) == 1


async def test_describe_db_clusters_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"DBClusters": [_CLUSTER_DATA], "Marker": "tok"},
        {"DBClusters": [{**_CLUSTER_DATA, "DBClusterIdentifier": "c2"}]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_clusters()
    assert len(r) == 2


async def test_describe_db_clusters_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_db_clusters failed"):
        await describe_db_clusters()


# ---------------------------------------------------------------------------
# modify_db_cluster
# ---------------------------------------------------------------------------


async def test_modify_db_cluster_ok(monkeypatch):
    mc = _mc({"DBCluster": _CLUSTER_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await modify_db_cluster("my-cluster")
    assert r.db_cluster_identifier == "my-cluster"


async def test_modify_db_cluster_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="modify_db_cluster failed"):
        await modify_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# delete_db_cluster
# ---------------------------------------------------------------------------


async def test_delete_db_cluster_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_db_cluster("my-cluster")
    mc.call.assert_awaited_once()


async def test_delete_db_cluster_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_db_cluster failed"):
        await delete_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# create_db_instance
# ---------------------------------------------------------------------------


async def test_create_db_instance_ok(monkeypatch):
    mc = _mc({"DBInstance": _INSTANCE_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_db_instance("my-instance", "db.r5.large")
    assert r.db_instance_identifier == "my-instance"


async def test_create_db_instance_with_cluster(monkeypatch):
    mc = _mc({"DBInstance": _INSTANCE_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_db_instance(
        "my-instance", "db.r5.large",
        db_cluster_identifier="my-cluster",
    )
    assert r.db_instance_identifier == "my-instance"


async def test_create_db_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_db_instance failed"):
        await create_db_instance("my-instance", "db.r5.large")


# ---------------------------------------------------------------------------
# describe_db_instances
# ---------------------------------------------------------------------------


async def test_describe_db_instances_ok(monkeypatch):
    mc = _mc({"DBInstances": [_INSTANCE_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_instances()
    assert len(r) == 1


async def test_describe_db_instances_with_id(monkeypatch):
    mc = _mc({"DBInstances": [_INSTANCE_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_instances("my-instance")
    assert len(r) == 1


async def test_describe_db_instances_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"DBInstances": [_INSTANCE_DATA], "Marker": "tok"},
        {"DBInstances": [{**_INSTANCE_DATA, "DBInstanceIdentifier": "i2"}]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_instances()
    assert len(r) == 2


async def test_describe_db_instances_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_db_instances failed"):
        await describe_db_instances()


# ---------------------------------------------------------------------------
# modify_db_instance
# ---------------------------------------------------------------------------


async def test_modify_db_instance_ok(monkeypatch):
    mc = _mc({"DBInstance": _INSTANCE_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await modify_db_instance("my-instance")
    assert r.db_instance_identifier == "my-instance"


async def test_modify_db_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="modify_db_instance failed"):
        await modify_db_instance("my-instance")


# ---------------------------------------------------------------------------
# delete_db_instance
# ---------------------------------------------------------------------------


async def test_delete_db_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    await delete_db_instance("my-instance")


async def test_delete_db_instance_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_db_instance failed"):
        await delete_db_instance("my-instance")


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def test_create_db_cluster_snapshot_ok(monkeypatch):
    mc = _mc({"DBClusterSnapshot": _SNAPSHOT_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await create_db_cluster_snapshot("my-snap", "my-cluster")
    assert r.db_cluster_snapshot_identifier == "my-snap"


async def test_create_db_cluster_snapshot_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_db_cluster_snapshot"):
        await create_db_cluster_snapshot("my-snap", "my-cluster")


async def test_describe_db_cluster_snapshots_ok(monkeypatch):
    mc = _mc({"DBClusterSnapshots": [_SNAPSHOT_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_cluster_snapshots()
    assert len(r) == 1


async def test_describe_db_cluster_snapshots_with_id(monkeypatch):
    mc = _mc({"DBClusterSnapshots": [_SNAPSHOT_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_cluster_snapshots("my-cluster")
    assert len(r) == 1


async def test_describe_db_cluster_snapshots_pagination(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=[
        {"DBClusterSnapshots": [_SNAPSHOT_DATA], "Marker": "tok"},
        {"DBClusterSnapshots": [{
            **_SNAPSHOT_DATA,
            "DBClusterSnapshotIdentifier": "s2",
        }]},
    ])
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await describe_db_cluster_snapshots()
    assert len(r) == 2


async def test_describe_db_cluster_snapshots_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_db_cluster_snapshots"):
        await describe_db_cluster_snapshots()


# ---------------------------------------------------------------------------
# failover_db_cluster
# ---------------------------------------------------------------------------


async def test_failover_db_cluster_ok(monkeypatch):
    mc = _mc({"DBCluster": _CLUSTER_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await failover_db_cluster("my-cluster")
    assert r.db_cluster_identifier == "my-cluster"


async def test_failover_db_cluster_with_target(monkeypatch):
    mc = _mc({"DBCluster": _CLUSTER_DATA})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await failover_db_cluster(
        "my-cluster", target_db_instance_identifier="my-instance",
    )
    assert r.db_cluster_identifier == "my-cluster"


async def test_failover_db_cluster_error(monkeypatch):
    mc = _mc(se=ValueError("bad"))
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="failover_db_cluster failed"):
        await failover_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# wait_for_db_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_db_cluster_ok(monkeypatch):
    mc = _mc({"DBClusters": [_CLUSTER_DATA]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    r = await wait_for_db_cluster("my-cluster")
    assert r.status == "available"


async def test_wait_for_db_cluster_not_found(monkeypatch):
    mc = _mc({"DBClusters": []})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    with pytest.raises(AwsServiceError, match="not found"):
        await wait_for_db_cluster("my-cluster")


async def test_wait_for_db_cluster_timeout(monkeypatch):
    data = {**_CLUSTER_DATA, "Status": "creating"}
    mc = _mc({"DBClusters": [data]})
    monkeypatch.setattr(_PATCH, lambda *a, **kw: mc)
    monkeypatch.setattr(
        "aws_util.aio.neptune.time.monotonic", lambda: 9999.0,
    )
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        await wait_for_db_cluster("my-cluster", timeout=1.0)


async def test_add_role_to_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_add_role_to_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", )


async def test_add_source_identifier_to_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", )
    mock_client.call.assert_called_once()


async def test_add_source_identifier_to_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", )


async def test_add_tags_to_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("test-resource_name", [], )


async def test_apply_pending_maintenance_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", )
    mock_client.call.assert_called_once()


async def test_apply_pending_maintenance_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", )


async def test_copy_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", )
    mock_client.call.assert_called_once()


async def test_copy_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", )


async def test_copy_db_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_copy_db_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", )


async def test_copy_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", )
    mock_client.call.assert_called_once()


async def test_copy_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", )


async def test_create_db_cluster_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", )


async def test_create_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", )


async def test_create_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", )


async def test_create_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], )
    mock_client.call.assert_called_once()


async def test_create_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], )


async def test_create_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )
    mock_client.call.assert_called_once()


async def test_create_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )


async def test_create_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_create_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_global_cluster("test-global_cluster_identifier", )


async def test_delete_db_cluster_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )


async def test_delete_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )


async def test_delete_db_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", )


async def test_delete_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_parameter_group("test-db_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_parameter_group("test-db_parameter_group_name", )


async def test_delete_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_subnet_group("test-db_subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_subnet_group("test-db_subnet_group_name", )


async def test_delete_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_delete_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_subscription("test-subscription_name", )


async def test_delete_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_global_cluster("test-global_cluster_identifier", )


async def test_describe_db_cluster_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_endpoints()


async def test_describe_db_cluster_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_parameter_groups()


async def test_describe_db_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", )


async def test_describe_db_cluster_snapshot_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_snapshot_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", )


async def test_describe_db_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_db_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_engine_versions()


async def test_describe_db_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_parameter_groups()


async def test_describe_db_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_parameters("test-db_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_parameters("test-db_parameter_group_name", )


async def test_describe_db_subnet_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_subnet_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_subnet_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_subnet_groups()


async def test_describe_engine_default_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_default_cluster_parameters("test-db_parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_engine_default_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_default_cluster_parameters("test-db_parameter_group_family", )


async def test_describe_engine_default_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_default_parameters("test-db_parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_engine_default_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_default_parameters("test-db_parameter_group_family", )


async def test_describe_event_categories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_categories()
    mock_client.call.assert_called_once()


async def test_describe_event_categories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_categories()


async def test_describe_event_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_subscriptions()
    mock_client.call.assert_called_once()


async def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_subscriptions()


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_global_clusters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_global_clusters()
    mock_client.call.assert_called_once()


async def test_describe_global_clusters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_global_clusters()


async def test_describe_orderable_db_instance_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_orderable_db_instance_options("test-engine", )
    mock_client.call.assert_called_once()


async def test_describe_orderable_db_instance_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_orderable_db_instance_options("test-engine", )


async def test_describe_pending_maintenance_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pending_maintenance_actions()
    mock_client.call.assert_called_once()


async def test_describe_pending_maintenance_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pending_maintenance_actions()


async def test_describe_valid_db_instance_modifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_valid_db_instance_modifications("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_valid_db_instance_modifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_valid_db_instance_modifications("test-db_instance_identifier", )


async def test_failover_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_failover_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_name", )


async def test_modify_db_cluster_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )


async def test_modify_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], )


async def test_modify_db_cluster_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", )


async def test_modify_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_parameter_group("test-db_parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_parameter_group("test-db_parameter_group_name", [], )


async def test_modify_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_subnet_group("test-db_subnet_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_subnet_group("test-db_subnet_group_name", [], )


async def test_modify_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_modify_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_event_subscription("test-subscription_name", )


async def test_modify_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_global_cluster("test-global_cluster_identifier", )


async def test_promote_read_replica_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await promote_read_replica_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_promote_read_replica_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await promote_read_replica_db_cluster("test-db_cluster_identifier", )


async def test_reboot_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_db_instance("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_reboot_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_db_instance("test-db_instance_identifier", )


async def test_remove_from_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_remove_from_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", )


async def test_remove_role_from_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_remove_role_from_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", )


async def test_remove_source_identifier_from_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", )
    mock_client.call.assert_called_once()


async def test_remove_source_identifier_from_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_name", [], )


async def test_reset_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )


async def test_reset_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_db_parameter_group("test-db_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_db_parameter_group("test-db_parameter_group_name", )


async def test_restore_db_cluster_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", )
    mock_client.call.assert_called_once()


async def test_restore_db_cluster_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", )


async def test_restore_db_cluster_to_point_in_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_restore_db_cluster_to_point_in_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", )


async def test_start_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_start_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_db_cluster("test-db_cluster_identifier", )


async def test_stop_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_stop_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_db_cluster("test-db_cluster_identifier", )


async def test_switchover_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    await switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_switchover_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.neptune.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )


@pytest.mark.asyncio
async def test_create_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster("test-db_cluster_identifier", engine_version="test-engine_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_clusters(db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_db_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_db_instance("test-db_instance_identifier", "test-db_instance_class", db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_instances(db_instance_identifier="test-db_instance_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_cluster_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_snapshots(db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_failover_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import failover_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await failover_db_cluster("test-db_cluster_identifier", target_db_instance_identifier="test-target_db_instance_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_add_role_to_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import add_role_to_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import copy_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import copy_db_cluster_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", copy_tags=[{"Key": "k", "Value": "v"}], tags=[{"Key": "k", "Value": "v"}], source_region="test-source_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import copy_db_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_db_cluster_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_db_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_db_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", "test-subnet_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import create_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await create_global_cluster("test-global_cluster_identifier", source_db_cluster_identifier="test-source_db_cluster_identifier", engine="test-engine", engine_version="test-engine_version", deletion_protection="test-deletion_protection", storage_encrypted="test-storage_encrypted", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_cluster_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_endpoints(db_cluster_identifier="test-db_cluster_identifier", db_cluster_endpoint_identifier="test-db_cluster_endpoint_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_cluster_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_parameter_groups(db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_engine_versions(engine="test-engine", engine_version="test-engine_version", db_parameter_group_family="test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", default_only="test-default_only", list_supported_character_sets=1, list_supported_timezones=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_parameter_groups(db_parameter_group_name="test-db_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_parameters("test-db_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_db_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_db_subnet_groups(db_subnet_group_name="test-db_subnet_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_engine_default_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_engine_default_cluster_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_default_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_engine_default_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_engine_default_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_event_categories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_event_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_global_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_global_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_global_clusters(global_cluster_identifier="test-global_cluster_identifier", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_orderable_db_instance_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_orderable_db_instance_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_orderable_db_instance_options("test-engine", engine_version="test-engine_version", db_instance_class="test-db_instance_class", license_model="test-license_model", vpc="test-vpc", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import describe_pending_maintenance_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await describe_pending_maintenance_actions(resource_identifier="test-resource_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_failover_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import failover_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", allow_data_loss=True, switchover="test-switchover", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_name", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import modify_db_cluster_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", endpoint_type="test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_cluster_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import modify_db_cluster_snapshot_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import modify_db_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await modify_db_subnet_group("test-db_subnet_group_name", "test-subnet_ids", db_subnet_group_description="test-db_subnet_group_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import modify_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import modify_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await modify_global_cluster("test-global_cluster_identifier", new_global_cluster_identifier="test-new_global_cluster_identifier", deletion_protection="test-deletion_protection", engine_version="test-engine_version", allow_major_version_upgrade=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reboot_db_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import reboot_db_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await reboot_db_instance("test-db_instance_identifier", force_failover=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_role_from_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import remove_role_from_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import reset_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import reset_db_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await reset_db_parameter_group("test-db_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_cluster_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import restore_db_cluster_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", availability_zones="test-availability_zones", engine_version="test-engine_version", port=1, db_subnet_group_name="test-db_subnet_group_name", database_name="test-database_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], serverless_v2_scaling_configuration={}, storage_type="test-storage_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_cluster_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.neptune import restore_db_cluster_to_point_in_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.neptune.async_client", lambda *a, **kw: mock_client)
    await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", restore_type="test-restore_type", restore_to_time="test-restore_to_time", use_latest_restorable_time=True, port=1, db_subnet_group_name="test-db_subnet_group_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", serverless_v2_scaling_configuration={}, storage_type="test-storage_type", region_name="us-east-1")
    mock_client.call.assert_called_once()
