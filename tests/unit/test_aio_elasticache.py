"""Tests for aws_util.aio.elasticache — 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.elasticache import (
    CacheClusterResult,
    CacheSubnetGroupResult,
    ReplicationGroupResult,
    SnapshotResult,
    add_tags_to_resource,
    create_cache_cluster,
    create_cache_subnet_group,
    create_replication_group,
    create_snapshot,
    delete_cache_cluster,
    delete_replication_group,
    delete_snapshot,
    describe_cache_clusters,
    describe_cache_subnet_groups,
    describe_replication_groups,
    describe_snapshots,
    ensure_cache_cluster,
    ensure_replication_group,
    list_tags_for_resource,
    modify_cache_cluster,
    modify_replication_group,
    reboot_cache_cluster,
    wait_for_cache_cluster,
    wait_for_replication_group,
    authorize_cache_security_group_ingress,
    batch_apply_update_action,
    batch_stop_update_action,
    complete_migration,
    copy_serverless_cache_snapshot,
    copy_snapshot,
    create_cache_parameter_group,
    create_cache_security_group,
    create_global_replication_group,
    create_serverless_cache,
    create_serverless_cache_snapshot,
    create_user,
    create_user_group,
    decrease_node_groups_in_global_replication_group,
    decrease_replica_count,
    delete_cache_parameter_group,
    delete_cache_security_group,
    delete_cache_subnet_group,
    delete_global_replication_group,
    delete_serverless_cache,
    delete_serverless_cache_snapshot,
    delete_user,
    delete_user_group,
    describe_cache_engine_versions,
    describe_cache_parameter_groups,
    describe_cache_parameters,
    describe_cache_security_groups,
    describe_engine_default_parameters,
    describe_events,
    describe_global_replication_groups,
    describe_reserved_cache_nodes,
    describe_reserved_cache_nodes_offerings,
    describe_serverless_cache_snapshots,
    describe_serverless_caches,
    describe_service_updates,
    describe_update_actions,
    describe_user_groups,
    describe_users,
    disassociate_global_replication_group,
    export_serverless_cache_snapshot,
    failover_global_replication_group,
    increase_node_groups_in_global_replication_group,
    increase_replica_count,
    list_allowed_node_type_modifications,
    modify_cache_parameter_group,
    modify_cache_subnet_group,
    modify_global_replication_group,
    modify_replication_group_shard_configuration,
    modify_serverless_cache,
    modify_user,
    modify_user_group,
    purchase_reserved_cache_nodes_offering,
    rebalance_slots_in_global_replication_group,
    remove_tags_from_resource,
    reset_cache_parameter_group,
    revoke_cache_security_group_ingress,
    run_failover,
    run_migration,
    start_migration,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    """Build a mock async client."""
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


# ---------------------------------------------------------------------------
# Sample API response dicts
# ---------------------------------------------------------------------------

_CLUSTER_DATA: dict = {
    "CacheClusterId": "my-cluster",
    "CacheClusterStatus": "available",
    "CacheNodeType": "cache.t3.micro",
    "Engine": "redis",
    "EngineVersion": "7.0",
    "NumCacheNodes": 1,
    "PreferredAvailabilityZone": "us-east-1a",
    "CacheSubnetGroupName": "my-subnet",
}

_RG_DATA: dict = {
    "ReplicationGroupId": "my-rg",
    "Description": "test group",
    "Status": "available",
    "MemberClusters": ["my-cluster"],
    "NodeGroups": [{"NodeGroupId": "0001"}],
    "AutomaticFailover": "enabled",
}

_SUBNET_DATA: dict = {
    "CacheSubnetGroupName": "my-subnet",
    "CacheSubnetGroupDescription": "my description",
    "VpcId": "vpc-123",
    "Subnets": [
        {"SubnetIdentifier": "subnet-a"},
        {"SubnetIdentifier": "subnet-b"},
    ],
}

_SNAP_DATA: dict = {
    "SnapshotName": "my-snap",
    "CacheClusterId": "my-cluster",
    "ReplicationGroupId": "my-rg",
    "SnapshotStatus": "available",
}


# ---------------------------------------------------------------------------
# create_cache_cluster
# ---------------------------------------------------------------------------


async def test_create_cache_cluster_ok(monkeypatch):
    mc = _mc({"CacheCluster": _CLUSTER_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_cache_cluster("my-cluster")
    assert r.cache_cluster_id == "my-cluster"
    mc.call.assert_awaited_once()


async def test_create_cache_cluster_with_opts(monkeypatch):
    mc = _mc({"CacheCluster": _CLUSTER_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_cache_cluster(
        "my-cluster",
        cache_subnet_group_name="sg",
        security_group_ids=["sg-1"],
        tags={"env": "test"},
    )
    assert r.cache_cluster_id == "my-cluster"


async def test_create_cache_cluster_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cache_cluster("bad")


async def test_create_cache_cluster_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to create cache cluster"):
        await create_cache_cluster("bad")


# ---------------------------------------------------------------------------
# describe_cache_clusters
# ---------------------------------------------------------------------------


async def test_describe_cache_clusters_ok(monkeypatch):
    mc = _mc({"CacheClusters": [_CLUSTER_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_cache_clusters()
    assert len(result) == 1
    assert result[0].cache_cluster_id == "my-cluster"


async def test_describe_cache_clusters_with_id(monkeypatch):
    mc = _mc({"CacheClusters": [_CLUSTER_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_cache_clusters(cache_cluster_id="my-cluster")
    assert len(result) == 1


async def test_describe_cache_clusters_pagination(monkeypatch):
    page1 = {"CacheClusters": [_CLUSTER_DATA], "Marker": "tok"}
    page2 = {
        "CacheClusters": [
            {
                "CacheClusterId": "c2",
                "CacheClusterStatus": "available",
                "CacheNodeType": "cache.t3.micro",
                "Engine": "redis",
                "EngineVersion": "7.0",
                "NumCacheNodes": 1,
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_cache_clusters()
    assert len(result) == 2


async def test_describe_cache_clusters_empty(monkeypatch):
    mc = _mc({"CacheClusters": []})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    assert await describe_cache_clusters() == []


async def test_describe_cache_clusters_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_clusters()


async def test_describe_cache_clusters_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="describe_cache_clusters failed"):
        await describe_cache_clusters()


# ---------------------------------------------------------------------------
# modify_cache_cluster
# ---------------------------------------------------------------------------


async def test_modify_cache_cluster_ok(monkeypatch):
    mc = _mc({"CacheCluster": _CLUSTER_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await modify_cache_cluster("my-cluster", num_cache_nodes=3)
    assert r.cache_cluster_id == "my-cluster"


async def test_modify_cache_cluster_with_node_type(monkeypatch):
    mc = _mc({"CacheCluster": _CLUSTER_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await modify_cache_cluster(
        "my-cluster", cache_node_type="cache.r6g.large"
    )
    assert r.cache_cluster_id == "my-cluster"


async def test_modify_cache_cluster_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cache_cluster("bad")


async def test_modify_cache_cluster_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to modify cache cluster"):
        await modify_cache_cluster("bad")


# ---------------------------------------------------------------------------
# delete_cache_cluster
# ---------------------------------------------------------------------------


async def test_delete_cache_cluster_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    await delete_cache_cluster("my-cluster")
    mc.call.assert_awaited_once()


async def test_delete_cache_cluster_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cache_cluster("bad")


async def test_delete_cache_cluster_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to delete cache cluster"):
        await delete_cache_cluster("bad")


# ---------------------------------------------------------------------------
# reboot_cache_cluster
# ---------------------------------------------------------------------------


async def test_reboot_cache_cluster_ok(monkeypatch):
    mc = _mc({"CacheCluster": _CLUSTER_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await reboot_cache_cluster("my-cluster", node_ids_to_reboot=["0001"])
    assert r.cache_cluster_id == "my-cluster"


async def test_reboot_cache_cluster_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_cache_cluster("bad", node_ids_to_reboot=["0001"])


async def test_reboot_cache_cluster_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to reboot cache cluster"):
        await reboot_cache_cluster("bad", node_ids_to_reboot=["0001"])


# ---------------------------------------------------------------------------
# create_replication_group
# ---------------------------------------------------------------------------


async def test_create_replication_group_ok(monkeypatch):
    mc = _mc({"ReplicationGroup": _RG_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_replication_group("my-rg", description="test group")
    assert r.replication_group_id == "my-rg"


async def test_create_replication_group_with_opts(monkeypatch):
    mc = _mc({"ReplicationGroup": _RG_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_replication_group(
        "my-rg",
        description="test",
        primary_cluster_id="c1",
        num_cache_clusters=3,
        cache_node_type="cache.r6g.large",
        automatic_failover_enabled=True,
    )
    assert r.replication_group_id == "my-rg"


async def test_create_replication_group_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_replication_group("bad", description="test")


async def test_create_replication_group_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(
        RuntimeError, match="Failed to create replication group"
    ):
        await create_replication_group("bad", description="test")


# ---------------------------------------------------------------------------
# describe_replication_groups
# ---------------------------------------------------------------------------


async def test_describe_replication_groups_ok(monkeypatch):
    mc = _mc({"ReplicationGroups": [_RG_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_replication_groups()
    assert len(result) == 1


async def test_describe_replication_groups_with_id(monkeypatch):
    mc = _mc({"ReplicationGroups": [_RG_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_replication_groups(
        replication_group_id="my-rg"
    )
    assert len(result) == 1


async def test_describe_replication_groups_pagination(monkeypatch):
    page1 = {"ReplicationGroups": [_RG_DATA], "Marker": "tok"}
    page2 = {
        "ReplicationGroups": [
            {
                "ReplicationGroupId": "rg2",
                "Description": "desc2",
                "Status": "available",
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_replication_groups()
    assert len(result) == 2


async def test_describe_replication_groups_empty(monkeypatch):
    mc = _mc({"ReplicationGroups": []})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    assert await describe_replication_groups() == []


async def test_describe_replication_groups_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_groups()


async def test_describe_replication_groups_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(
        RuntimeError, match="describe_replication_groups failed"
    ):
        await describe_replication_groups()


# ---------------------------------------------------------------------------
# modify_replication_group
# ---------------------------------------------------------------------------


async def test_modify_replication_group_ok(monkeypatch):
    mc = _mc({"ReplicationGroup": _RG_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await modify_replication_group("my-rg", description="updated")
    assert r.replication_group_id == "my-rg"


async def test_modify_replication_group_with_failover(monkeypatch):
    mc = _mc({"ReplicationGroup": _RG_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await modify_replication_group(
        "my-rg", automatic_failover_enabled=True
    )
    assert r.replication_group_id == "my-rg"


async def test_modify_replication_group_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_replication_group("bad")


async def test_modify_replication_group_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(
        RuntimeError, match="Failed to modify replication group"
    ):
        await modify_replication_group("bad")


# ---------------------------------------------------------------------------
# delete_replication_group
# ---------------------------------------------------------------------------


async def test_delete_replication_group_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    await delete_replication_group("my-rg")
    mc.call.assert_awaited_once()


async def test_delete_replication_group_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_replication_group("bad")


async def test_delete_replication_group_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(
        RuntimeError, match="Failed to delete replication group"
    ):
        await delete_replication_group("bad")


# ---------------------------------------------------------------------------
# create_cache_subnet_group
# ---------------------------------------------------------------------------


async def test_create_cache_subnet_group_ok(monkeypatch):
    mc = _mc({"CacheSubnetGroup": _SUBNET_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_cache_subnet_group(
        "my-subnet", description="desc", subnet_ids=["subnet-a"]
    )
    assert r.name == "my-subnet"


async def test_create_cache_subnet_group_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cache_subnet_group(
            "bad", description="desc", subnet_ids=["s"]
        )


async def test_create_cache_subnet_group_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(
        RuntimeError, match="Failed to create cache subnet group"
    ):
        await create_cache_subnet_group(
            "bad", description="desc", subnet_ids=["s"]
        )


# ---------------------------------------------------------------------------
# describe_cache_subnet_groups
# ---------------------------------------------------------------------------


async def test_describe_cache_subnet_groups_ok(monkeypatch):
    mc = _mc({"CacheSubnetGroups": [_SUBNET_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_cache_subnet_groups()
    assert len(result) == 1


async def test_describe_cache_subnet_groups_with_name(monkeypatch):
    mc = _mc({"CacheSubnetGroups": [_SUBNET_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_cache_subnet_groups(name="my-subnet")
    assert len(result) == 1


async def test_describe_cache_subnet_groups_pagination(monkeypatch):
    page1 = {"CacheSubnetGroups": [_SUBNET_DATA], "Marker": "tok"}
    page2 = {
        "CacheSubnetGroups": [
            {
                "CacheSubnetGroupName": "sg2",
                "CacheSubnetGroupDescription": "d2",
                "VpcId": "vpc-2",
                "Subnets": [],
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_cache_subnet_groups()
    assert len(result) == 2


async def test_describe_cache_subnet_groups_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_subnet_groups()


async def test_describe_cache_subnet_groups_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(
        RuntimeError, match="describe_cache_subnet_groups failed"
    ):
        await describe_cache_subnet_groups()


# ---------------------------------------------------------------------------
# create_snapshot
# ---------------------------------------------------------------------------


async def test_create_snapshot_ok_with_cluster(monkeypatch):
    mc = _mc({"Snapshot": _SNAP_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_snapshot("my-snap", cache_cluster_id="my-cluster")
    assert r.snapshot_name == "my-snap"


async def test_create_snapshot_ok_with_rg(monkeypatch):
    mc = _mc({"Snapshot": _SNAP_DATA})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    r = await create_snapshot("my-snap", replication_group_id="my-rg")
    assert r.snapshot_name == "my-snap"


async def test_create_snapshot_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_snapshot("bad")


async def test_create_snapshot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to create snapshot"):
        await create_snapshot("bad")


# ---------------------------------------------------------------------------
# describe_snapshots
# ---------------------------------------------------------------------------


async def test_describe_snapshots_ok(monkeypatch):
    mc = _mc({"Snapshots": [_SNAP_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_snapshots()
    assert len(result) == 1


async def test_describe_snapshots_with_name(monkeypatch):
    mc = _mc({"Snapshots": [_SNAP_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_snapshots(snapshot_name="my-snap")
    assert len(result) == 1


async def test_describe_snapshots_with_cluster_id(monkeypatch):
    mc = _mc({"Snapshots": [_SNAP_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_snapshots(cache_cluster_id="my-cluster")
    assert len(result) == 1


async def test_describe_snapshots_pagination(monkeypatch):
    page1 = {"Snapshots": [_SNAP_DATA], "Marker": "tok"}
    page2 = {
        "Snapshots": [
            {
                "SnapshotName": "snap2",
                "SnapshotStatus": "available",
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    result = await describe_snapshots()
    assert len(result) == 2


async def test_describe_snapshots_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_snapshots()


async def test_describe_snapshots_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="describe_snapshots failed"):
        await describe_snapshots()


# ---------------------------------------------------------------------------
# delete_snapshot
# ---------------------------------------------------------------------------


async def test_delete_snapshot_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    await delete_snapshot("my-snap")
    mc.call.assert_awaited_once()


async def test_delete_snapshot_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_snapshot("bad")


async def test_delete_snapshot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
        await delete_snapshot("bad")


# ---------------------------------------------------------------------------
# list_tags_for_resource
# ---------------------------------------------------------------------------


async def test_list_tags_for_resource_ok(monkeypatch):
    mc = _mc({"TagList": [{"Key": "env", "Value": "prod"}]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    tags = await list_tags_for_resource("arn:aws:elasticache:us-east-1:123:cluster:c1")
    assert tags == {"env": "prod"}


async def test_list_tags_for_resource_empty(monkeypatch):
    mc = _mc({"TagList": []})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    tags = await list_tags_for_resource("arn:x")
    assert tags == {}


async def test_list_tags_for_resource_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("arn:x")


async def test_list_tags_for_resource_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to list tags"):
        await list_tags_for_resource("arn:x")


# ---------------------------------------------------------------------------
# add_tags_to_resource
# ---------------------------------------------------------------------------


async def test_add_tags_to_resource_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    await add_tags_to_resource("arn:x", tags={"env": "prod"})
    mc.call.assert_awaited_once()


async def test_add_tags_to_resource_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("arn:x", tags={"a": "b"})


async def test_add_tags_to_resource_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    with pytest.raises(RuntimeError, match="Failed to add tags"):
        await add_tags_to_resource("arn:x", tags={"a": "b"})


# ---------------------------------------------------------------------------
# wait_for_cache_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_cache_cluster_immediate(monkeypatch):
    mc = _mc({"CacheClusters": [_CLUSTER_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )
    r = await wait_for_cache_cluster("my-cluster")
    assert r.cache_cluster_status == "available"


async def test_wait_for_cache_cluster_not_found(monkeypatch):
    mc = _mc({"CacheClusters": []})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_cache_cluster("ghost")


async def test_wait_for_cache_cluster_timeout(monkeypatch):
    creating_data = dict(_CLUSTER_DATA)
    creating_data["CacheClusterStatus"] = "creating"
    mc = _mc({"CacheClusters": [creating_data]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )

    _real = time.monotonic
    values = [0.0, 0.0, 700.0]
    _idx = 0

    def _fake():
        nonlocal _idx
        if _idx < len(values):
            v = values[_idx]
            _idx += 1
            return v
        return _real()

    monkeypatch.setattr(time, "monotonic", _fake)

    with pytest.raises(TimeoutError, match="did not reach status"):
        await wait_for_cache_cluster("my-cluster", timeout=600.0)


async def test_wait_for_cache_cluster_sleep_branch(monkeypatch):
    """Covers the asyncio.sleep branch in the polling loop."""
    call_count = {"n": 0}

    async def fake_describe(**kw):
        call_count["n"] += 1
        status = "creating" if call_count["n"] < 2 else "available"
        data = dict(_CLUSTER_DATA)
        data["CacheClusterStatus"] = status
        return [
            CacheClusterResult(
                cache_cluster_id=data["CacheClusterId"],
                cache_cluster_status=data["CacheClusterStatus"],
                cache_node_type=data["CacheNodeType"],
                engine=data["Engine"],
                engine_version=data["EngineVersion"],
                num_cache_nodes=data["NumCacheNodes"],
            )
        ]

    monkeypatch.setattr(
        "aws_util.aio.elasticache.describe_cache_clusters", fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )
    r = await wait_for_cache_cluster("my-cluster", timeout=10.0, poll_interval=0.001)
    assert r.cache_cluster_status == "available"


# ---------------------------------------------------------------------------
# wait_for_replication_group
# ---------------------------------------------------------------------------


async def test_wait_for_replication_group_immediate(monkeypatch):
    mc = _mc({"ReplicationGroups": [_RG_DATA]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )
    r = await wait_for_replication_group("my-rg")
    assert r.status == "available"


async def test_wait_for_replication_group_not_found(monkeypatch):
    mc = _mc({"ReplicationGroups": []})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_replication_group("ghost")


async def test_wait_for_replication_group_timeout(monkeypatch):
    creating_data = dict(_RG_DATA)
    creating_data["Status"] = "creating"
    mc = _mc({"ReplicationGroups": [creating_data]})
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client", lambda *a, **kw: mc
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )

    _real = time.monotonic
    values = [0.0, 0.0, 700.0]
    _idx = 0

    def _fake():
        nonlocal _idx
        if _idx < len(values):
            v = values[_idx]
            _idx += 1
            return v
        return _real()

    monkeypatch.setattr(time, "monotonic", _fake)

    with pytest.raises(TimeoutError, match="did not reach status"):
        await wait_for_replication_group("my-rg", timeout=600.0)


async def test_wait_for_replication_group_sleep_branch(monkeypatch):
    """Covers the asyncio.sleep branch in the polling loop."""
    call_count = {"n": 0}

    async def fake_describe(**kw):
        call_count["n"] += 1
        status = "creating" if call_count["n"] < 2 else "available"
        return [
            ReplicationGroupResult(
                replication_group_id="my-rg",
                description="test",
                status=status,
            )
        ]

    monkeypatch.setattr(
        "aws_util.aio.elasticache.describe_replication_groups",
        fake_describe,
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.asyncio.sleep", AsyncMock()
    )
    r = await wait_for_replication_group(
        "my-rg", timeout=10.0, poll_interval=0.001
    )
    assert r.status == "available"


# ---------------------------------------------------------------------------
# ensure_cache_cluster
# ---------------------------------------------------------------------------


async def test_ensure_cache_cluster_existing(monkeypatch):
    cluster = CacheClusterResult(
        cache_cluster_id="c1",
        cache_cluster_status="available",
        cache_node_type="cache.t3.micro",
        engine="redis",
        engine_version="7.0",
        num_cache_nodes=1,
    )

    async def fake_describe(**kw):
        return [cluster]

    monkeypatch.setattr(
        "aws_util.aio.elasticache.describe_cache_clusters", fake_describe
    )
    r, created = await ensure_cache_cluster("c1")
    assert r.cache_cluster_id == "c1"
    assert created is False


async def test_ensure_cache_cluster_creates_new(monkeypatch):
    cluster = CacheClusterResult(
        cache_cluster_id="c1",
        cache_cluster_status="creating",
        cache_node_type="cache.t3.micro",
        engine="redis",
        engine_version="7.0",
        num_cache_nodes=1,
    )

    async def fake_describe(**kw):
        return []

    async def fake_create(*a, **kw):
        return cluster

    monkeypatch.setattr(
        "aws_util.aio.elasticache.describe_cache_clusters", fake_describe
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.create_cache_cluster", fake_create
    )
    r, created = await ensure_cache_cluster("c1")
    assert created is True


# ---------------------------------------------------------------------------
# ensure_replication_group
# ---------------------------------------------------------------------------


async def test_ensure_replication_group_existing(monkeypatch):
    rg = ReplicationGroupResult(
        replication_group_id="rg1",
        description="test",
        status="available",
    )

    async def fake_describe(**kw):
        return [rg]

    monkeypatch.setattr(
        "aws_util.aio.elasticache.describe_replication_groups",
        fake_describe,
    )
    r, created = await ensure_replication_group("rg1", description="test")
    assert r.replication_group_id == "rg1"
    assert created is False


async def test_ensure_replication_group_creates_new(monkeypatch):
    rg = ReplicationGroupResult(
        replication_group_id="rg1",
        description="test",
        status="creating",
    )

    async def fake_describe(**kw):
        return []

    async def fake_create(*a, **kw):
        return rg

    monkeypatch.setattr(
        "aws_util.aio.elasticache.describe_replication_groups",
        fake_describe,
    )
    monkeypatch.setattr(
        "aws_util.aio.elasticache.create_replication_group", fake_create
    )
    r, created = await ensure_replication_group("rg1", description="test")
    assert created is True


async def test_authorize_cache_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", )
    mock_client.call.assert_called_once()


async def test_authorize_cache_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", )


async def test_batch_apply_update_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_apply_update_action("test-service_update_name", )
    mock_client.call.assert_called_once()


async def test_batch_apply_update_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_apply_update_action("test-service_update_name", )


async def test_batch_stop_update_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_stop_update_action("test-service_update_name", )
    mock_client.call.assert_called_once()


async def test_batch_stop_update_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_stop_update_action("test-service_update_name", )


async def test_complete_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await complete_migration("test-replication_group_id", )
    mock_client.call.assert_called_once()


async def test_complete_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await complete_migration("test-replication_group_id", )


async def test_copy_serverless_cache_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_serverless_cache_snapshot("test-source_serverless_cache_snapshot_name", "test-target_serverless_cache_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_copy_serverless_cache_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_serverless_cache_snapshot("test-source_serverless_cache_snapshot_name", "test-target_serverless_cache_snapshot_name", )


async def test_copy_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_snapshot("test-source_snapshot_name", "test-target_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_copy_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_snapshot("test-source_snapshot_name", "test-target_snapshot_name", )


async def test_create_cache_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cache_parameter_group("test-cache_parameter_group_name", "test-cache_parameter_group_family", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_cache_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cache_parameter_group("test-cache_parameter_group_name", "test-cache_parameter_group_family", "test-description", )


async def test_create_cache_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cache_security_group("test-cache_security_group_name", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_cache_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cache_security_group("test-cache_security_group_name", "test-description", )


async def test_create_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_global_replication_group("test-global_replication_group_id_suffix", "test-primary_replication_group_id", )
    mock_client.call.assert_called_once()


async def test_create_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_global_replication_group("test-global_replication_group_id_suffix", "test-primary_replication_group_id", )


async def test_create_serverless_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_serverless_cache("test-serverless_cache_name", "test-engine", )
    mock_client.call.assert_called_once()


async def test_create_serverless_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_serverless_cache("test-serverless_cache_name", "test-engine", )


async def test_create_serverless_cache_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-serverless_cache_name", )
    mock_client.call.assert_called_once()


async def test_create_serverless_cache_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-serverless_cache_name", )


async def test_create_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_user("test-user_id", "test-user_name", "test-engine", "test-access_string", )
    mock_client.call.assert_called_once()


async def test_create_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_user("test-user_id", "test-user_name", "test-engine", "test-access_string", )


async def test_create_user_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_user_group("test-user_group_id", "test-engine", )
    mock_client.call.assert_called_once()


async def test_create_user_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_user_group("test-user_group_id", "test-engine", )


async def test_decrease_node_groups_in_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await decrease_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, )
    mock_client.call.assert_called_once()


async def test_decrease_node_groups_in_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await decrease_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, )


async def test_decrease_replica_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await decrease_replica_count("test-replication_group_id", True, )
    mock_client.call.assert_called_once()


async def test_decrease_replica_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await decrease_replica_count("test-replication_group_id", True, )


async def test_delete_cache_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cache_parameter_group("test-cache_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_cache_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cache_parameter_group("test-cache_parameter_group_name", )


async def test_delete_cache_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cache_security_group("test-cache_security_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_cache_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cache_security_group("test-cache_security_group_name", )


async def test_delete_cache_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cache_subnet_group("test-cache_subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_cache_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cache_subnet_group("test-cache_subnet_group_name", )


async def test_delete_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_global_replication_group("test-global_replication_group_id", True, )
    mock_client.call.assert_called_once()


async def test_delete_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_global_replication_group("test-global_replication_group_id", True, )


async def test_delete_serverless_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_serverless_cache("test-serverless_cache_name", )
    mock_client.call.assert_called_once()


async def test_delete_serverless_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_serverless_cache("test-serverless_cache_name", )


async def test_delete_serverless_cache_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_serverless_cache_snapshot("test-serverless_cache_snapshot_name", )
    mock_client.call.assert_called_once()


async def test_delete_serverless_cache_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_serverless_cache_snapshot("test-serverless_cache_snapshot_name", )


async def test_delete_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user("test-user_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user("test-user_id", )


async def test_delete_user_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_user_group("test-user_group_id", )
    mock_client.call.assert_called_once()


async def test_delete_user_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_user_group("test-user_group_id", )


async def test_describe_cache_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cache_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_cache_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_engine_versions()


async def test_describe_cache_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cache_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_cache_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_parameter_groups()


async def test_describe_cache_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cache_parameters("test-cache_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_cache_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_parameters("test-cache_parameter_group_name", )


async def test_describe_cache_security_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cache_security_groups()
    mock_client.call.assert_called_once()


async def test_describe_cache_security_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cache_security_groups()


async def test_describe_engine_default_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_default_parameters("test-cache_parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_engine_default_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_default_parameters("test-cache_parameter_group_family", )


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_global_replication_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_global_replication_groups()
    mock_client.call.assert_called_once()


async def test_describe_global_replication_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_global_replication_groups()


async def test_describe_reserved_cache_nodes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_cache_nodes()
    mock_client.call.assert_called_once()


async def test_describe_reserved_cache_nodes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_cache_nodes()


async def test_describe_reserved_cache_nodes_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_cache_nodes_offerings()
    mock_client.call.assert_called_once()


async def test_describe_reserved_cache_nodes_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_cache_nodes_offerings()


async def test_describe_serverless_cache_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_serverless_cache_snapshots()
    mock_client.call.assert_called_once()


async def test_describe_serverless_cache_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_serverless_cache_snapshots()


async def test_describe_serverless_caches(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_serverless_caches()
    mock_client.call.assert_called_once()


async def test_describe_serverless_caches_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_serverless_caches()


async def test_describe_service_updates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_updates()
    mock_client.call.assert_called_once()


async def test_describe_service_updates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_updates()


async def test_describe_update_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_update_actions()
    mock_client.call.assert_called_once()


async def test_describe_update_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_update_actions()


async def test_describe_user_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_user_groups()
    mock_client.call.assert_called_once()


async def test_describe_user_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_user_groups()


async def test_describe_users(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_users()
    mock_client.call.assert_called_once()


async def test_describe_users_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_users()


async def test_disassociate_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_global_replication_group("test-global_replication_group_id", "test-replication_group_id", "test-replication_group_region", )
    mock_client.call.assert_called_once()


async def test_disassociate_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_global_replication_group("test-global_replication_group_id", "test-replication_group_id", "test-replication_group_region", )


async def test_export_serverless_cache_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await export_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-s3_bucket_name", )
    mock_client.call.assert_called_once()


async def test_export_serverless_cache_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await export_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-s3_bucket_name", )


async def test_failover_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_global_replication_group("test-global_replication_group_id", "test-primary_region", "test-primary_replication_group_id", )
    mock_client.call.assert_called_once()


async def test_failover_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_global_replication_group("test-global_replication_group_id", "test-primary_region", "test-primary_replication_group_id", )


async def test_increase_node_groups_in_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await increase_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, )
    mock_client.call.assert_called_once()


async def test_increase_node_groups_in_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await increase_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, )


async def test_increase_replica_count(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await increase_replica_count("test-replication_group_id", True, )
    mock_client.call.assert_called_once()


async def test_increase_replica_count_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await increase_replica_count("test-replication_group_id", True, )


async def test_list_allowed_node_type_modifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_allowed_node_type_modifications()
    mock_client.call.assert_called_once()


async def test_list_allowed_node_type_modifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_allowed_node_type_modifications()


async def test_modify_cache_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cache_parameter_group("test-cache_parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_cache_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cache_parameter_group("test-cache_parameter_group_name", [], )


async def test_modify_cache_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_cache_subnet_group("test-cache_subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_modify_cache_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_cache_subnet_group("test-cache_subnet_group_name", )


async def test_modify_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_global_replication_group("test-global_replication_group_id", True, )
    mock_client.call.assert_called_once()


async def test_modify_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_global_replication_group("test-global_replication_group_id", True, )


async def test_modify_replication_group_shard_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_replication_group_shard_configuration("test-replication_group_id", 1, True, )
    mock_client.call.assert_called_once()


async def test_modify_replication_group_shard_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_replication_group_shard_configuration("test-replication_group_id", 1, True, )


async def test_modify_serverless_cache(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_serverless_cache("test-serverless_cache_name", )
    mock_client.call.assert_called_once()


async def test_modify_serverless_cache_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_serverless_cache("test-serverless_cache_name", )


async def test_modify_user(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_user("test-user_id", )
    mock_client.call.assert_called_once()


async def test_modify_user_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_user("test-user_id", )


async def test_modify_user_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_user_group("test-user_group_id", )
    mock_client.call.assert_called_once()


async def test_modify_user_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_user_group("test-user_group_id", )


async def test_purchase_reserved_cache_nodes_offering(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_reserved_cache_nodes_offering("test-reserved_cache_nodes_offering_id", )
    mock_client.call.assert_called_once()


async def test_purchase_reserved_cache_nodes_offering_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_reserved_cache_nodes_offering("test-reserved_cache_nodes_offering_id", )


async def test_rebalance_slots_in_global_replication_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await rebalance_slots_in_global_replication_group("test-global_replication_group_id", True, )
    mock_client.call.assert_called_once()


async def test_rebalance_slots_in_global_replication_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await rebalance_slots_in_global_replication_group("test-global_replication_group_id", True, )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_name", [], )


async def test_reset_cache_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_cache_parameter_group("test-cache_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_cache_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_cache_parameter_group("test-cache_parameter_group_name", )


async def test_revoke_cache_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", )
    mock_client.call.assert_called_once()


async def test_revoke_cache_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", )


async def test_run_failover(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_failover("test-replication_group_id", "test-node_group_id", )
    mock_client.call.assert_called_once()


async def test_run_failover_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_failover("test-replication_group_id", "test-node_group_id", )


async def test_run_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await run_migration("test-replication_group_id", [], )
    mock_client.call.assert_called_once()


async def test_run_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await run_migration("test-replication_group_id", [], )


async def test_start_migration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_migration("test-replication_group_id", [], )
    mock_client.call.assert_called_once()


async def test_start_migration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.elasticache.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_migration("test-replication_group_id", [], )


@pytest.mark.asyncio
async def test_describe_cache_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_cache_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_cache_clusters(cache_cluster_id="test-cache_cluster_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_replication_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_replication_groups(replication_group_id="test-replication_group_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cache_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_cache_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_cache_subnet_groups(name="test-name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_snapshots(snapshot_name="test-snapshot_name", cache_cluster_id="test-cache_cluster_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_apply_update_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import batch_apply_update_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await batch_apply_update_action("test-service_update_name", replication_group_ids="test-replication_group_ids", cache_cluster_ids="test-cache_cluster_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_stop_update_action_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import batch_stop_update_action
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await batch_stop_update_action("test-service_update_name", replication_group_ids="test-replication_group_ids", cache_cluster_ids="test-cache_cluster_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_complete_migration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import complete_migration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await complete_migration("test-replication_group_id", force=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_serverless_cache_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import copy_serverless_cache_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await copy_serverless_cache_snapshot("test-source_serverless_cache_snapshot_name", "test-target_serverless_cache_snapshot_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import copy_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await copy_snapshot("test-source_snapshot_name", "test-target_snapshot_name", target_bucket="test-target_bucket", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_cache_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_cache_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_cache_parameter_group("test-cache_parameter_group_name", "test-cache_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_cache_security_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_cache_security_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_cache_security_group("test-cache_security_group_name", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_global_replication_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_global_replication_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_global_replication_group("test-global_replication_group_id_suffix", "test-primary_replication_group_id", global_replication_group_description="test-global_replication_group_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_serverless_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_serverless_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_serverless_cache("test-serverless_cache_name", "test-engine", description="test-description", major_engine_version="test-major_engine_version", cache_usage_limits=1, kms_key_id="test-kms_key_id", security_group_ids="test-security_group_ids", snapshot_arns_to_restore="test-snapshot_arns_to_restore", tags=[{"Key": "k", "Value": "v"}], user_group_id="test-user_group_id", subnet_ids="test-subnet_ids", snapshot_retention_limit=1, daily_snapshot_time="test-daily_snapshot_time", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_serverless_cache_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_serverless_cache_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-serverless_cache_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_user("test-user_id", "test-user_name", "test-engine", "test-access_string", passwords="test-passwords", no_password_required=True, tags=[{"Key": "k", "Value": "v"}], authentication_mode="test-authentication_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import create_user_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await create_user_group("test-user_group_id", "test-engine", user_ids="test-user_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_decrease_node_groups_in_global_replication_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import decrease_node_groups_in_global_replication_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await decrease_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, global_node_groups_to_remove="test-global_node_groups_to_remove", global_node_groups_to_retain="test-global_node_groups_to_retain", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_decrease_replica_count_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import decrease_replica_count
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await decrease_replica_count("test-replication_group_id", True, new_replica_count=1, replica_configuration={}, replicas_to_remove="test-replicas_to_remove", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_serverless_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import delete_serverless_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await delete_serverless_cache("test-serverless_cache_name", final_snapshot_name="test-final_snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cache_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_cache_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_cache_engine_versions(engine="test-engine", engine_version="test-engine_version", cache_parameter_group_family="test-cache_parameter_group_family", max_records=1, marker="test-marker", default_only="test-default_only", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cache_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_cache_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_cache_parameter_groups(cache_parameter_group_name="test-cache_parameter_group_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cache_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_cache_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_cache_parameters("test-cache_parameter_group_name", source="test-source", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cache_security_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_cache_security_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_cache_security_groups(cache_security_group_name="test-cache_security_group_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_default_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_engine_default_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_engine_default_parameters("test-cache_parameter_group_family", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_global_replication_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_global_replication_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_global_replication_groups(global_replication_group_id="test-global_replication_group_id", max_records=1, marker="test-marker", show_member_info="test-show_member_info", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_cache_nodes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_reserved_cache_nodes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_cache_nodes(reserved_cache_node_id="test-reserved_cache_node_id", reserved_cache_nodes_offering_id="test-reserved_cache_nodes_offering_id", cache_node_type="test-cache_node_type", duration=1, product_description="test-product_description", offering_type="test-offering_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_cache_nodes_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_reserved_cache_nodes_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_cache_nodes_offerings(reserved_cache_nodes_offering_id="test-reserved_cache_nodes_offering_id", cache_node_type="test-cache_node_type", duration=1, product_description="test-product_description", offering_type="test-offering_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_serverless_cache_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_serverless_cache_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_serverless_cache_snapshots(serverless_cache_name="test-serverless_cache_name", serverless_cache_snapshot_name="test-serverless_cache_snapshot_name", snapshot_type="test-snapshot_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_serverless_caches_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_serverless_caches
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_serverless_caches(serverless_cache_name="test-serverless_cache_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_service_updates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_service_updates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_service_updates(service_update_name="test-service_update_name", service_update_status="test-service_update_status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_update_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_update_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_update_actions(service_update_name="test-service_update_name", replication_group_ids="test-replication_group_ids", cache_cluster_ids="test-cache_cluster_ids", engine="test-engine", service_update_status="test-service_update_status", service_update_time_range="test-service_update_time_range", update_action_status="test-update_action_status", show_node_level_update_status="test-show_node_level_update_status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_user_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_user_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_user_groups(user_group_id="test-user_group_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_users_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import describe_users
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await describe_users(engine="test-engine", user_id="test-user_id", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_increase_node_groups_in_global_replication_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import increase_node_groups_in_global_replication_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await increase_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, regional_configurations={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_increase_replica_count_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import increase_replica_count
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await increase_replica_count("test-replication_group_id", True, new_replica_count=1, replica_configuration={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_allowed_node_type_modifications_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import list_allowed_node_type_modifications
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await list_allowed_node_type_modifications(cache_cluster_id="test-cache_cluster_id", replication_group_id="test-replication_group_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_cache_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import modify_cache_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await modify_cache_subnet_group("test-cache_subnet_group_name", cache_subnet_group_description="test-cache_subnet_group_description", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_global_replication_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import modify_global_replication_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await modify_global_replication_group("test-global_replication_group_id", True, cache_node_type="test-cache_node_type", engine="test-engine", engine_version="test-engine_version", cache_parameter_group_name="test-cache_parameter_group_name", global_replication_group_description="test-global_replication_group_description", automatic_failover_enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_replication_group_shard_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import modify_replication_group_shard_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await modify_replication_group_shard_configuration("test-replication_group_id", 1, True, resharding_configuration={}, node_groups_to_remove="test-node_groups_to_remove", node_groups_to_retain="test-node_groups_to_retain", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_serverless_cache_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import modify_serverless_cache
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await modify_serverless_cache("test-serverless_cache_name", description="test-description", cache_usage_limits=1, remove_user_group="test-remove_user_group", user_group_id="test-user_group_id", security_group_ids="test-security_group_ids", snapshot_retention_limit=1, daily_snapshot_time="test-daily_snapshot_time", engine="test-engine", major_engine_version="test-major_engine_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_user_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import modify_user
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await modify_user("test-user_id", access_string="test-access_string", append_access_string="test-append_access_string", passwords="test-passwords", no_password_required=True, authentication_mode="test-authentication_mode", engine="test-engine", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_user_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import modify_user_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await modify_user_group("test-user_group_id", user_ids_to_add="test-user_ids_to_add", user_ids_to_remove="test-user_ids_to_remove", engine="test-engine", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_reserved_cache_nodes_offering_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import purchase_reserved_cache_nodes_offering
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await purchase_reserved_cache_nodes_offering("test-reserved_cache_nodes_offering_id", reserved_cache_node_id="test-reserved_cache_node_id", cache_node_count=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_cache_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.elasticache import reset_cache_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.elasticache.async_client", lambda *a, **kw: mock_client)
    await reset_cache_parameter_group("test-cache_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameter_name_values="test-parameter_name_values", region_name="us-east-1")
    mock_client.call.assert_called_once()
