"""Tests for aws_util.aio.documentdb module."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock

import pytest

from aws_util.aio.documentdb import (
    ClusterResult,
    ClusterSnapshotResult,
    InstanceResult,
    copy_db_cluster_snapshot,
    create_db_cluster,
    create_db_cluster_snapshot,
    create_db_instance,
    delete_db_cluster,
    delete_db_cluster_snapshot,
    delete_db_instance,
    describe_db_cluster_snapshots,
    describe_db_clusters,
    describe_db_instances,
    failover_db_cluster,
    modify_db_cluster,
    modify_db_instance,
    reboot_db_instance,
    restore_db_cluster_from_snapshot,
    wait_for_db_cluster,
    wait_for_db_instance,
    add_source_identifier_to_subscription,
    add_tags_to_resource,
    apply_pending_maintenance_action,
    copy_db_cluster_parameter_group,
    create_db_cluster_parameter_group,
    create_db_subnet_group,
    create_event_subscription,
    create_global_cluster,
    delete_db_cluster_parameter_group,
    delete_db_subnet_group,
    delete_event_subscription,
    delete_global_cluster,
    describe_certificates,
    describe_db_cluster_parameter_groups,
    describe_db_cluster_parameters,
    describe_db_cluster_snapshot_attributes,
    describe_db_engine_versions,
    describe_db_subnet_groups,
    describe_engine_default_cluster_parameters,
    describe_event_categories,
    describe_event_subscriptions,
    describe_events,
    describe_global_clusters,
    describe_orderable_db_instance_options,
    describe_pending_maintenance_actions,
    failover_global_cluster,
    list_tags_for_resource,
    modify_db_cluster_parameter_group,
    modify_db_cluster_snapshot_attribute,
    modify_db_subnet_group,
    modify_event_subscription,
    modify_global_cluster,
    remove_from_global_cluster,
    remove_source_identifier_from_subscription,
    remove_tags_from_resource,
    reset_db_cluster_parameter_group,
    restore_db_cluster_to_point_in_time,
    start_db_cluster,
    stop_db_cluster,
    switchover_global_cluster,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError


REGION = "us-east-1"
CLUSTER_ID = "my-docdb-cluster"
INSTANCE_ID = "my-docdb-instance"
SNAP_ID = "my-snap"


def _mock_factory(mc):
    return lambda *a, **kw: mc


def _cluster_dict(**ov):
    d = {
        "DBClusterIdentifier": CLUSTER_ID, "Status": "available",
        "Engine": "docdb", "EngineVersion": "5.0.0",
        "Endpoint": "ep.com", "Port": 27017,
    }
    d.update(ov)
    return d


def _instance_dict(**ov):
    d = {
        "DBInstanceIdentifier": INSTANCE_ID, "DBInstanceClass": "db.r5.large",
        "DBInstanceStatus": "available", "Engine": "docdb",
        "EngineVersion": "5.0.0",
        "Endpoint": {"Address": "inst.com", "Port": 27017},
    }
    d.update(ov)
    return d


def _snapshot_dict(**ov):
    d = {
        "DBClusterSnapshotIdentifier": SNAP_ID,
        "DBClusterIdentifier": CLUSTER_ID,
        "Status": "available", "Engine": "docdb", "EngineVersion": "5.0.0",
    }
    d.update(ov)
    return d


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def test_create_db_cluster(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBCluster": _cluster_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await create_db_cluster(CLUSTER_ID, region_name=REGION)
    assert r.db_cluster_identifier == CLUSTER_ID


async def test_create_db_cluster_all_opts(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBCluster": _cluster_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await create_db_cluster(
        CLUSTER_ID, engine_version="5.0.0",
        db_subnet_group_name="sg", vpc_security_group_ids=["sg-1"],
        tags={"env": "test"}, region_name=REGION,
    )
    assert r.db_cluster_identifier == CLUSTER_ID


async def test_create_db_cluster_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_db_cluster(CLUSTER_ID, region_name=REGION)


async def test_describe_db_clusters(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBClusters": [_cluster_dict()]}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await describe_db_clusters(db_cluster_identifier=CLUSTER_ID, region_name=REGION)
    assert len(r) == 1


async def test_describe_db_clusters_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"DBClusters": [_cluster_dict()], "Marker": "tok"},
        {"DBClusters": [_cluster_dict(DBClusterIdentifier="other")]},
    ]
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await describe_db_clusters(region_name=REGION)
    assert len(r) == 2


async def test_describe_db_clusters_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_db_clusters(region_name=REGION)


async def test_modify_db_cluster(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBCluster": _cluster_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await modify_db_cluster(
        CLUSTER_ID, engine_version="5.1.0",
        master_user_password="pw", region_name=REGION,
    )
    assert r.db_cluster_identifier == CLUSTER_ID


async def test_modify_db_cluster_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await modify_db_cluster(CLUSTER_ID, region_name=REGION)


async def test_delete_db_cluster(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    await delete_db_cluster(CLUSTER_ID, region_name=REGION)


async def test_delete_db_cluster_with_snap(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    await delete_db_cluster(
        CLUSTER_ID, skip_final_snapshot=False,
        final_db_snapshot_identifier="final", region_name=REGION,
    )


async def test_delete_db_cluster_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_db_cluster(CLUSTER_ID, region_name=REGION)


async def test_failover_db_cluster(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBCluster": _cluster_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await failover_db_cluster(
        CLUSTER_ID, target_db_instance_identifier=INSTANCE_ID, region_name=REGION,
    )
    assert r.db_cluster_identifier == CLUSTER_ID


async def test_failover_db_cluster_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await failover_db_cluster(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


async def test_create_db_instance(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBInstance": _instance_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await create_db_instance(
        INSTANCE_ID, db_cluster_identifier=CLUSTER_ID,
        availability_zone="us-east-1a", tags={"e": "t"}, region_name=REGION,
    )
    assert r.db_instance_identifier == INSTANCE_ID


async def test_create_db_instance_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_db_instance(
            INSTANCE_ID, db_cluster_identifier=CLUSTER_ID, region_name=REGION,
        )


async def test_describe_db_instances(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBInstances": [_instance_dict()]}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await describe_db_instances(
        db_instance_identifier=INSTANCE_ID, region_name=REGION,
    )
    assert len(r) == 1


async def test_describe_db_instances_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"DBInstances": [_instance_dict()], "Marker": "tok"},
        {"DBInstances": [_instance_dict(DBInstanceIdentifier="other")]},
    ]
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await describe_db_instances(region_name=REGION)
    assert len(r) == 2


async def test_describe_db_instances_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_db_instances(region_name=REGION)


async def test_modify_db_instance(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBInstance": _instance_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await modify_db_instance(
        INSTANCE_ID, db_instance_class="db.r6g.large", region_name=REGION,
    )
    assert r.db_instance_identifier == INSTANCE_ID


async def test_modify_db_instance_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await modify_db_instance(INSTANCE_ID, region_name=REGION)


async def test_delete_db_instance(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    await delete_db_instance(INSTANCE_ID, region_name=REGION)


async def test_delete_db_instance_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_db_instance(INSTANCE_ID, region_name=REGION)


async def test_reboot_db_instance(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBInstance": _instance_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await reboot_db_instance(INSTANCE_ID, force_failover=True, region_name=REGION)
    assert r.db_instance_identifier == INSTANCE_ID


async def test_reboot_db_instance_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await reboot_db_instance(INSTANCE_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def test_create_db_cluster_snapshot(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBClusterSnapshot": _snapshot_dict()}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await create_db_cluster_snapshot(
        SNAP_ID, db_cluster_identifier=CLUSTER_ID,
        tags={"e": "t"}, region_name=REGION,
    )
    assert r.db_cluster_snapshot_identifier == SNAP_ID


async def test_create_db_cluster_snapshot_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await create_db_cluster_snapshot(
            SNAP_ID, db_cluster_identifier=CLUSTER_ID, region_name=REGION,
        )


async def test_describe_db_cluster_snapshots(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBClusterSnapshots": [_snapshot_dict()]}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await describe_db_cluster_snapshots(
        db_cluster_snapshot_identifier=SNAP_ID,
        db_cluster_identifier=CLUSTER_ID, region_name=REGION,
    )
    assert len(r) == 1


async def test_describe_db_cluster_snapshots_paginated(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = [
        {"DBClusterSnapshots": [_snapshot_dict()], "Marker": "tok"},
        {"DBClusterSnapshots": [_snapshot_dict(DBClusterSnapshotIdentifier="snap2")]},
    ]
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await describe_db_cluster_snapshots(region_name=REGION)
    assert len(r) == 2


async def test_describe_db_cluster_snapshots_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await describe_db_cluster_snapshots(region_name=REGION)


async def test_copy_db_cluster_snapshot(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DBClusterSnapshot": _snapshot_dict(DBClusterSnapshotIdentifier="copy"),
    }
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await copy_db_cluster_snapshot(
        SNAP_ID, "copy", tags={"e": "t"}, region_name=REGION,
    )
    assert r.db_cluster_snapshot_identifier == "copy"


async def test_copy_db_cluster_snapshot_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await copy_db_cluster_snapshot(SNAP_ID, "copy", region_name=REGION)


async def test_delete_db_cluster_snapshot(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    await delete_db_cluster_snapshot(SNAP_ID, region_name=REGION)


async def test_delete_db_cluster_snapshot_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await delete_db_cluster_snapshot(SNAP_ID, region_name=REGION)


async def test_restore_db_cluster_from_snapshot(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DBCluster": _cluster_dict(DBClusterIdentifier="restored"),
    }
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await restore_db_cluster_from_snapshot(
        "restored", snapshot_identifier=SNAP_ID,
        vpc_security_group_ids=["sg-1"], db_subnet_group_name="default",
        tags={"e": "t"}, region_name=REGION,
    )
    assert r.db_cluster_identifier == "restored"


async def test_restore_db_cluster_from_snapshot_error(monkeypatch):
    client = AsyncMock()
    client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(RuntimeError):
        await restore_db_cluster_from_snapshot(
            "x", snapshot_identifier=SNAP_ID, region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def test_wait_for_db_cluster_ready(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DBClusters": [_cluster_dict(Status="available")],
    }
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await wait_for_db_cluster(CLUSTER_ID, timeout=10, region_name=REGION)
    assert r.status == "available"


async def test_wait_for_db_cluster_not_found(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBClusters": []}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(AwsServiceError):
        await wait_for_db_cluster(CLUSTER_ID, timeout=10, region_name=REGION)


async def test_wait_for_db_cluster_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DBClusters": [_cluster_dict(Status="creating")],
    }
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        await wait_for_db_cluster(
            CLUSTER_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_wait_for_db_cluster_poll_then_ready(monkeypatch):
    """Cover the sleep branch: first poll creating, second available."""
    client = AsyncMock()
    client.call.side_effect = [
        {"DBClusters": [_cluster_dict(Status="creating")]},
        {"DBClusters": [_cluster_dict(Status="available")]},
    ]
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    r = await wait_for_db_cluster(
        CLUSTER_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert r.status == "available"


async def test_wait_for_db_instance_ready(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DBInstances": [_instance_dict(DBInstanceStatus="available")],
    }
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    r = await wait_for_db_instance(INSTANCE_ID, timeout=10, region_name=REGION)
    assert r.status == "available"


async def test_wait_for_db_instance_not_found(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {"DBInstances": []}
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    with pytest.raises(AwsServiceError):
        await wait_for_db_instance(INSTANCE_ID, timeout=10, region_name=REGION)


async def test_wait_for_db_instance_timeout(monkeypatch):
    client = AsyncMock()
    client.call.return_value = {
        "DBInstances": [_instance_dict(DBInstanceStatus="creating")],
    }
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    call_count2 = 0

    def _mono2():
        nonlocal call_count2
        call_count2 += 1
        return 0.0 if call_count2 <= 1 else 100.0

    monkeypatch.setattr(time, "monotonic", _mono2)
    with pytest.raises(AwsTimeoutError):
        await wait_for_db_instance(
            INSTANCE_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


async def test_wait_for_db_instance_poll_then_ready(monkeypatch):
    """Cover the sleep branch: first poll creating, second available."""
    client = AsyncMock()
    client.call.side_effect = [
        {"DBInstances": [_instance_dict(DBInstanceStatus="creating")]},
        {"DBInstances": [_instance_dict(DBInstanceStatus="available")]},
    ]
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", _mock_factory(client))
    monkeypatch.setattr("asyncio.sleep", AsyncMock())
    r = await wait_for_db_instance(
        INSTANCE_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert r.status == "available"


async def test_add_source_identifier_to_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", )
    mock_client.call.assert_called_once()


async def test_add_source_identifier_to_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", )


async def test_add_tags_to_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("test-resource_name", [], )


async def test_apply_pending_maintenance_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", )
    mock_client.call.assert_called_once()


async def test_apply_pending_maintenance_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", )


async def test_copy_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", )
    mock_client.call.assert_called_once()


async def test_copy_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", )


async def test_create_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", )


async def test_create_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], )
    mock_client.call.assert_called_once()


async def test_create_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], )


async def test_create_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )
    mock_client.call.assert_called_once()


async def test_create_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )


async def test_create_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_create_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_global_cluster("test-global_cluster_identifier", )


async def test_delete_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )


async def test_delete_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_subnet_group("test-db_subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_subnet_group("test-db_subnet_group_name", )


async def test_delete_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_delete_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_subscription("test-subscription_name", )


async def test_delete_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_global_cluster("test-global_cluster_identifier", )


async def test_describe_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_certificates()
    mock_client.call.assert_called_once()


async def test_describe_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_certificates()


async def test_describe_db_cluster_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_parameter_groups()


async def test_describe_db_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", )


async def test_describe_db_cluster_snapshot_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_snapshot_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", )


async def test_describe_db_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_db_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_engine_versions()


async def test_describe_db_subnet_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_subnet_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_subnet_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_subnet_groups()


async def test_describe_engine_default_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_default_cluster_parameters("test-db_parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_engine_default_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_default_cluster_parameters("test-db_parameter_group_family", )


async def test_describe_event_categories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_categories()
    mock_client.call.assert_called_once()


async def test_describe_event_categories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_categories()


async def test_describe_event_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_subscriptions()
    mock_client.call.assert_called_once()


async def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_subscriptions()


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_global_clusters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_global_clusters()
    mock_client.call.assert_called_once()


async def test_describe_global_clusters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_global_clusters()


async def test_describe_orderable_db_instance_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_orderable_db_instance_options("test-engine", )
    mock_client.call.assert_called_once()


async def test_describe_orderable_db_instance_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_orderable_db_instance_options("test-engine", )


async def test_describe_pending_maintenance_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pending_maintenance_actions()
    mock_client.call.assert_called_once()


async def test_describe_pending_maintenance_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pending_maintenance_actions()


async def test_failover_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_failover_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_name", )


async def test_modify_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], )


async def test_modify_db_cluster_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", )


async def test_modify_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_subnet_group("test-db_subnet_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_subnet_group("test-db_subnet_group_name", [], )


async def test_modify_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_modify_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_event_subscription("test-subscription_name", )


async def test_modify_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_global_cluster("test-global_cluster_identifier", )


async def test_remove_from_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_remove_from_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", )


async def test_remove_source_identifier_from_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", )
    mock_client.call.assert_called_once()


async def test_remove_source_identifier_from_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_name", [], )


async def test_reset_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )


async def test_restore_db_cluster_to_point_in_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_restore_db_cluster_to_point_in_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", )


async def test_start_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_start_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_db_cluster("test-db_cluster_identifier", )


async def test_stop_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_stop_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_db_cluster("test-db_cluster_identifier", )


async def test_switchover_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    await switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_switchover_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.documentdb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )


@pytest.mark.asyncio
async def test_describe_db_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_clusters(db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import delete_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await delete_db_cluster("test-db_cluster_identifier", final_db_snapshot_identifier="test-final_db_snapshot_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_instances(db_instance_identifier="test-db_instance_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_cluster_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_snapshots(db_cluster_snapshot_identifier="test-db_cluster_snapshot_identifier", db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import copy_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import create_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import create_db_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", "test-subnet_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import create_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import create_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await create_global_cluster("test-global_cluster_identifier", source_db_cluster_identifier="test-source_db_cluster_identifier", engine="test-engine", engine_version="test-engine_version", deletion_protection="test-deletion_protection", database_name="test-database_name", storage_encrypted="test-storage_encrypted", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_certificates(certificate_identifier="test-certificate_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_cluster_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_parameter_groups(db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_engine_versions(engine="test-engine", engine_version="test-engine_version", db_parameter_group_family="test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", default_only="test-default_only", list_supported_character_sets=1, list_supported_timezones=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_db_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_db_subnet_groups(db_subnet_group_name="test-db_subnet_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_engine_default_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_engine_default_cluster_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_event_categories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_event_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_global_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_global_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_global_clusters(global_cluster_identifier="test-global_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_orderable_db_instance_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_orderable_db_instance_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_orderable_db_instance_options("test-engine", engine_version="test-engine_version", db_instance_class="test-db_instance_class", license_model="test-license_model", vpc="test-vpc", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import describe_pending_maintenance_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await describe_pending_maintenance_actions(resource_identifier="test-resource_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_failover_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import failover_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", allow_data_loss=True, switchover="test-switchover", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_name", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_cluster_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import modify_db_cluster_snapshot_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import modify_db_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await modify_db_subnet_group("test-db_subnet_group_name", "test-subnet_ids", db_subnet_group_description="test-db_subnet_group_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import modify_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import modify_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await modify_global_cluster("test-global_cluster_identifier", new_global_cluster_identifier="test-new_global_cluster_identifier", deletion_protection="test-deletion_protection", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import reset_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_cluster_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.documentdb import restore_db_cluster_to_point_in_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.documentdb.async_client", lambda *a, **kw: mock_client)
    await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", restore_type="test-restore_type", restore_to_time="test-restore_to_time", use_latest_restorable_time=True, port=1, db_subnet_group_name="test-db_subnet_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_cloudwatch_logs_exports=True, deletion_protection="test-deletion_protection", serverless_v2_scaling_configuration={}, storage_type="test-storage_type", network_type="test-network_type", region_name="us-east-1")
    mock_client.call.assert_called_once()
