"""Tests for aws_util.aio.rds -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.rds import (
    RDSInstance,
    RDSSnapshot,
    _parse_instances_from_resp,
    create_db_snapshot,
    delete_db_snapshot,
    describe_db_instances,
    describe_db_snapshots,
    get_db_instance,
    restore_db_from_snapshot,
    start_db_instance,
    stop_db_instance,
    wait_for_db_instance,
    wait_for_snapshot,
    add_role_to_db_cluster,
    add_role_to_db_instance,
    add_source_identifier_to_subscription,
    add_tags_to_resource,
    apply_pending_maintenance_action,
    authorize_db_security_group_ingress,
    backtrack_db_cluster,
    cancel_export_task,
    copy_db_cluster_parameter_group,
    copy_db_cluster_snapshot,
    copy_db_parameter_group,
    copy_db_snapshot,
    copy_option_group,
    create_blue_green_deployment,
    create_custom_db_engine_version,
    create_db_cluster,
    create_db_cluster_endpoint,
    create_db_cluster_parameter_group,
    create_db_cluster_snapshot,
    create_db_instance,
    create_db_instance_read_replica,
    create_db_parameter_group,
    create_db_proxy,
    create_db_proxy_endpoint,
    create_db_security_group,
    create_db_shard_group,
    create_db_subnet_group,
    create_event_subscription,
    create_global_cluster,
    create_integration,
    create_option_group,
    create_tenant_database,
    delete_blue_green_deployment,
    delete_custom_db_engine_version,
    delete_db_cluster,
    delete_db_cluster_automated_backup,
    delete_db_cluster_endpoint,
    delete_db_cluster_parameter_group,
    delete_db_cluster_snapshot,
    delete_db_instance,
    delete_db_instance_automated_backup,
    delete_db_parameter_group,
    delete_db_proxy,
    delete_db_proxy_endpoint,
    delete_db_security_group,
    delete_db_shard_group,
    delete_db_subnet_group,
    delete_event_subscription,
    delete_global_cluster,
    delete_integration,
    delete_option_group,
    delete_tenant_database,
    deregister_db_proxy_targets,
    describe_account_attributes,
    describe_blue_green_deployments,
    describe_certificates,
    describe_db_cluster_automated_backups,
    describe_db_cluster_backtracks,
    describe_db_cluster_endpoints,
    describe_db_cluster_parameter_groups,
    describe_db_cluster_parameters,
    describe_db_cluster_snapshot_attributes,
    describe_db_cluster_snapshots,
    describe_db_clusters,
    describe_db_engine_versions,
    describe_db_instance_automated_backups,
    describe_db_log_files,
    describe_db_major_engine_versions,
    describe_db_parameter_groups,
    describe_db_parameters,
    describe_db_proxies,
    describe_db_proxy_endpoints,
    describe_db_proxy_target_groups,
    describe_db_proxy_targets,
    describe_db_recommendations,
    describe_db_security_groups,
    describe_db_shard_groups,
    describe_db_snapshot_attributes,
    describe_db_snapshot_tenant_databases,
    describe_db_subnet_groups,
    describe_engine_default_cluster_parameters,
    describe_engine_default_parameters,
    describe_event_categories,
    describe_event_subscriptions,
    describe_events,
    describe_export_tasks,
    describe_global_clusters,
    describe_integrations,
    describe_option_group_options,
    describe_option_groups,
    describe_orderable_db_instance_options,
    describe_pending_maintenance_actions,
    describe_reserved_db_instances,
    describe_reserved_db_instances_offerings,
    describe_source_regions,
    describe_tenant_databases,
    describe_valid_db_instance_modifications,
    disable_http_endpoint,
    download_db_log_file_portion,
    enable_http_endpoint,
    failover_db_cluster,
    failover_global_cluster,
    list_tags_for_resource,
    modify_activity_stream,
    modify_certificates,
    modify_current_db_cluster_capacity,
    modify_custom_db_engine_version,
    modify_db_cluster,
    modify_db_cluster_endpoint,
    modify_db_cluster_parameter_group,
    modify_db_cluster_snapshot_attribute,
    modify_db_instance,
    modify_db_parameter_group,
    modify_db_proxy,
    modify_db_proxy_endpoint,
    modify_db_proxy_target_group,
    modify_db_recommendation,
    modify_db_shard_group,
    modify_db_snapshot,
    modify_db_snapshot_attribute,
    modify_db_subnet_group,
    modify_event_subscription,
    modify_global_cluster,
    modify_integration,
    modify_option_group,
    modify_tenant_database,
    promote_read_replica,
    promote_read_replica_db_cluster,
    purchase_reserved_db_instances_offering,
    reboot_db_cluster,
    reboot_db_instance,
    reboot_db_shard_group,
    register_db_proxy_targets,
    remove_from_global_cluster,
    remove_role_from_db_cluster,
    remove_role_from_db_instance,
    remove_source_identifier_from_subscription,
    remove_tags_from_resource,
    reset_db_cluster_parameter_group,
    reset_db_parameter_group,
    restore_db_cluster_from_s3,
    restore_db_cluster_from_snapshot,
    restore_db_cluster_to_point_in_time,
    restore_db_instance_from_db_snapshot,
    restore_db_instance_from_s3,
    restore_db_instance_to_point_in_time,
    revoke_db_security_group_ingress,
    start_activity_stream,
    start_db_cluster,
    start_db_instance_automated_backups_replication,
    start_export_task,
    stop_activity_stream,
    stop_db_cluster,
    stop_db_instance_automated_backups_replication,
    switchover_blue_green_deployment,
    switchover_global_cluster,
    switchover_read_replica,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


_DB_RESP = {
    "DBInstances": [
        {
            "DBInstanceIdentifier": "mydb",
            "DBInstanceClass": "db.t3.micro",
            "Engine": "postgres",
            "EngineVersion": "15.4",
            "DBInstanceStatus": "available",
            "Endpoint": {"Address": "mydb.abc.rds.amazonaws.com", "Port": 5432},
            "MultiAZ": True,
            "AllocatedStorage": 100,
            "TagList": [{"Key": "env", "Value": "prod"}],
        }
    ]
}

_SNAP_RESP = {
    "DBSnapshot": {
        "DBSnapshotIdentifier": "snap-1",
        "DBInstanceIdentifier": "mydb",
        "Status": "available",
        "SnapshotType": "manual",
        "Engine": "postgres",
        "AllocatedStorage": 100,
        "SnapshotCreateTime": "2024-01-01T00:00:00Z",
    }
}


# ---------------------------------------------------------------------------
# _parse_instances_from_resp
# ---------------------------------------------------------------------------


def test_parse_instances_from_resp():
    result = _parse_instances_from_resp(_DB_RESP)
    assert len(result) == 1
    inst = result[0]
    assert inst.db_instance_id == "mydb"
    assert inst.endpoint_address == "mydb.abc.rds.amazonaws.com"
    assert inst.endpoint_port == 5432
    assert inst.multi_az is True
    assert inst.storage_gb == 100
    assert inst.tags == {"env": "prod"}


def test_parse_instances_empty():
    assert _parse_instances_from_resp({}) == []


def test_parse_instances_no_endpoint():
    resp = {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "db1",
                "DBInstanceClass": "db.t3.micro",
                "Engine": "mysql",
                "EngineVersion": "8.0",
                "DBInstanceStatus": "creating",
            }
        ]
    }
    result = _parse_instances_from_resp(resp)
    assert result[0].endpoint_address is None
    assert result[0].endpoint_port is None


# ---------------------------------------------------------------------------
# describe_db_instances
# ---------------------------------------------------------------------------


async def test_describe_db_instances_no_ids(monkeypatch):
    mc = _mc(_DB_RESP)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_instances()
    assert len(result) == 1
    assert result[0].db_instance_id == "mydb"


async def test_describe_db_instances_with_ids(monkeypatch):
    mc = _mc(_DB_RESP)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_instances(db_instance_ids=["mydb"])
    assert len(result) == 1


async def test_describe_db_instances_with_filters(monkeypatch):
    mc = _mc(_DB_RESP)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_instances(
        filters=[{"Name": "engine", "Values": ["postgres"]}]
    )
    assert len(result) == 1


async def test_describe_db_instances_pagination_no_ids(monkeypatch):
    page1 = dict(_DB_RESP)
    page1["Marker"] = "tok"
    page2 = {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "db2",
                "DBInstanceClass": "db.t3.small",
                "Engine": "mysql",
                "EngineVersion": "8.0",
                "DBInstanceStatus": "available",
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_instances()
    assert len(result) == 2


async def test_describe_db_instances_pagination_with_ids(monkeypatch):
    page1 = dict(_DB_RESP)
    page1["Marker"] = "tok"
    page2 = {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "mydb",
                "DBInstanceClass": "db.t3.micro",
                "Engine": "postgres",
                "EngineVersion": "15.4",
                "DBInstanceStatus": "available",
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_instances(db_instance_ids=["mydb"])
    assert len(result) == 2


async def test_describe_db_instances_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_instances()


async def test_describe_db_instances_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_db_instances failed"):
        await describe_db_instances()


# ---------------------------------------------------------------------------
# get_db_instance
# ---------------------------------------------------------------------------


async def test_get_db_instance_found(monkeypatch):
    mc = _mc(_DB_RESP)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await get_db_instance("mydb")
    assert result is not None
    assert result.db_instance_id == "mydb"


async def test_get_db_instance_not_found(monkeypatch):
    mc = _mc({"DBInstances": []})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await get_db_instance("missing")
    assert result is None


# ---------------------------------------------------------------------------
# start_db_instance
# ---------------------------------------------------------------------------


async def test_start_db_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    await start_db_instance("mydb")
    mc.call.assert_awaited_once()


async def test_start_db_instance_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await start_db_instance("mydb")


async def test_start_db_instance_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to start"):
        await start_db_instance("mydb")


# ---------------------------------------------------------------------------
# stop_db_instance
# ---------------------------------------------------------------------------


async def test_stop_db_instance_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    await stop_db_instance("mydb")
    mc.call.assert_awaited_once()


async def test_stop_db_instance_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await stop_db_instance("mydb")


async def test_stop_db_instance_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to stop"):
        await stop_db_instance("mydb")


# ---------------------------------------------------------------------------
# create_db_snapshot
# ---------------------------------------------------------------------------


async def test_create_db_snapshot_ok(monkeypatch):
    mc = _mc(_SNAP_RESP)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await create_db_snapshot("mydb", "snap-1")
    assert isinstance(result, RDSSnapshot)
    assert result.snapshot_id == "snap-1"
    assert result.engine == "postgres"


async def test_create_db_snapshot_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_snapshot("mydb", "snap-1")


async def test_create_db_snapshot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to create snapshot"):
        await create_db_snapshot("mydb", "snap-1")


# ---------------------------------------------------------------------------
# delete_db_snapshot
# ---------------------------------------------------------------------------


async def test_delete_db_snapshot_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    await delete_db_snapshot("snap-1")
    mc.call.assert_awaited_once()


async def test_delete_db_snapshot_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_snapshot("snap-1")


async def test_delete_db_snapshot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
        await delete_db_snapshot("snap-1")


# ---------------------------------------------------------------------------
# describe_db_snapshots
# ---------------------------------------------------------------------------


async def test_describe_db_snapshots_ok(monkeypatch):
    mc = _mc(
        {
            "DBSnapshots": [
                {
                    "DBSnapshotIdentifier": "snap-1",
                    "DBInstanceIdentifier": "mydb",
                    "Status": "available",
                    "SnapshotType": "manual",
                    "Engine": "postgres",
                    "AllocatedStorage": 100,
                    "SnapshotCreateTime": "2024-01-01",
                }
            ]
        }
    )
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_snapshots(db_instance_id="mydb")
    assert len(result) == 1
    assert result[0].snapshot_id == "snap-1"


async def test_describe_db_snapshots_no_filter(monkeypatch):
    mc = _mc({"DBSnapshots": []})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_snapshots()
    assert result == []


async def test_describe_db_snapshots_pagination(monkeypatch):
    page1 = {
        "DBSnapshots": [
            {
                "DBSnapshotIdentifier": "s1",
                "DBInstanceIdentifier": "db",
                "Status": "available",
                "SnapshotType": "manual",
                "Engine": "mysql",
            }
        ],
        "Marker": "tok",
    }
    page2 = {
        "DBSnapshots": [
            {
                "DBSnapshotIdentifier": "s2",
                "DBInstanceIdentifier": "db",
                "Status": "available",
                "SnapshotType": "manual",
                "Engine": "mysql",
            }
        ]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await describe_db_snapshots()
    assert len(result) == 2


async def test_describe_db_snapshots_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_snapshots()


async def test_describe_db_snapshots_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_db_snapshots failed"):
        await describe_db_snapshots()


# ---------------------------------------------------------------------------
# wait_for_db_instance
# ---------------------------------------------------------------------------


async def test_wait_for_db_instance_immediate(monkeypatch):
    mc = _mc(_DB_RESP)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())
    result = await wait_for_db_instance("mydb")
    assert result.status == "available"


async def test_wait_for_db_instance_not_found(monkeypatch):
    mc = _mc({"DBInstances": []})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_db_instance("mydb")


async def test_wait_for_db_instance_timeout(monkeypatch):
    resp = {
        "DBInstances": [
            {
                "DBInstanceIdentifier": "mydb",
                "DBInstanceClass": "db.t3.micro",
                "Engine": "postgres",
                "EngineVersion": "15.4",
                "DBInstanceStatus": "creating",
            }
        ]
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())

    # Force monotonic to exceed deadline; use default fallback for any
    # extra calls after the iterator is exhausted (e.g. teardown).
    _real = time.monotonic
    values = [0.0, 0.0, 1300.0]
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
        await wait_for_db_instance("mydb", timeout=1200.0)


# ---------------------------------------------------------------------------
# wait_for_snapshot
# ---------------------------------------------------------------------------


async def test_wait_for_snapshot_immediate(monkeypatch):
    snap_resp = {
        "DBSnapshots": [
            {
                "DBSnapshotIdentifier": "snap-1",
                "DBInstanceIdentifier": "mydb",
                "Status": "available",
                "SnapshotType": "manual",
                "Engine": "postgres",
                "AllocatedStorage": 100,
            }
        ]
    }
    mc = _mc(snap_resp)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())
    result = await wait_for_snapshot("snap-1")
    assert result.status == "available"


async def test_wait_for_snapshot_not_found(monkeypatch):
    mc = _mc({"DBSnapshots": []})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_snapshot("snap-1")


async def test_wait_for_snapshot_timeout(monkeypatch):
    snap_resp = {
        "DBSnapshots": [
            {
                "DBSnapshotIdentifier": "snap-1",
                "DBInstanceIdentifier": "mydb",
                "Status": "creating",
                "SnapshotType": "manual",
                "Engine": "postgres",
            }
        ]
    }
    mc = _mc(snap_resp)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())

    _real = time.monotonic
    values = [0.0, 0.0, 2000.0]
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
        await wait_for_snapshot("snap-1", timeout=1800.0)


async def test_wait_for_snapshot_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="boom"):
        await wait_for_snapshot("snap-1")


async def test_wait_for_snapshot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    monkeypatch.setattr("aws_util.aio.rds.asyncio.sleep", AsyncMock())
    with pytest.raises(RuntimeError, match="describe snapshot"):
        await wait_for_snapshot("snap-1")


# ---------------------------------------------------------------------------
# restore_db_from_snapshot
# ---------------------------------------------------------------------------


async def test_restore_db_from_snapshot_ok(monkeypatch):
    resp = {
        "DBInstance": {
            "DBInstanceIdentifier": "restored",
            "DBInstanceClass": "db.t3.medium",
            "Engine": "postgres",
            "EngineVersion": "15.4",
            "DBInstanceStatus": "creating",
            "MultiAZ": False,
            "AllocatedStorage": 100,
        }
    }
    mc = _mc(resp)
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    result = await restore_db_from_snapshot(
        "snap-1", "restored", "db.t3.medium"
    )
    assert isinstance(result, RDSInstance)
    assert result.db_instance_id == "restored"
    assert result.status == "creating"


async def test_restore_db_from_snapshot_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_from_snapshot("snap-1", "db", "db.t3.medium")


async def test_restore_db_from_snapshot_generic_error(monkeypatch):
    mc = _mc()
    mc.call = AsyncMock(side_effect=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="restore_db_from_snapshot failed"):
        await restore_db_from_snapshot("snap-1", "db", "db.t3.medium")


async def test_add_role_to_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_add_role_to_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", )


async def test_add_role_to_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_role_to_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", )
    mock_client.call.assert_called_once()


async def test_add_role_to_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_role_to_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", )


async def test_add_source_identifier_to_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", )
    mock_client.call.assert_called_once()


async def test_add_source_identifier_to_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", )


async def test_add_tags_to_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await add_tags_to_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_add_tags_to_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await add_tags_to_resource("test-resource_name", [], )


async def test_apply_pending_maintenance_action(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", )
    mock_client.call.assert_called_once()


async def test_apply_pending_maintenance_action_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", )


async def test_authorize_db_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await authorize_db_security_group_ingress("test-db_security_group_name", )
    mock_client.call.assert_called_once()


async def test_authorize_db_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await authorize_db_security_group_ingress("test-db_security_group_name", )


async def test_backtrack_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await backtrack_db_cluster("test-db_cluster_identifier", "test-backtrack_to", )
    mock_client.call.assert_called_once()


async def test_backtrack_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await backtrack_db_cluster("test-db_cluster_identifier", "test-backtrack_to", )


async def test_cancel_export_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await cancel_export_task("test-export_task_identifier", )
    mock_client.call.assert_called_once()


async def test_cancel_export_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await cancel_export_task("test-export_task_identifier", )


async def test_copy_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", )
    mock_client.call.assert_called_once()


async def test_copy_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", )


async def test_copy_db_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_copy_db_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", )


async def test_copy_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", )
    mock_client.call.assert_called_once()


async def test_copy_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", )


async def test_copy_db_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_db_snapshot("test-source_db_snapshot_identifier", "test-target_db_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_copy_db_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_db_snapshot("test-source_db_snapshot_identifier", "test-target_db_snapshot_identifier", )


async def test_copy_option_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await copy_option_group("test-source_option_group_identifier", "test-target_option_group_identifier", "test-target_option_group_description", )
    mock_client.call.assert_called_once()


async def test_copy_option_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await copy_option_group("test-source_option_group_identifier", "test-target_option_group_identifier", "test-target_option_group_description", )


async def test_create_blue_green_deployment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_blue_green_deployment("test-blue_green_deployment_name", "test-source", )
    mock_client.call.assert_called_once()


async def test_create_blue_green_deployment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_blue_green_deployment("test-blue_green_deployment_name", "test-source", )


async def test_create_custom_db_engine_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_custom_db_engine_version("test-engine", "test-engine_version", )
    mock_client.call.assert_called_once()


async def test_create_custom_db_engine_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_custom_db_engine_version("test-engine", "test-engine_version", )


async def test_create_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster("test-db_cluster_identifier", "test-engine", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster("test-db_cluster_identifier", "test-engine", )


async def test_create_db_cluster_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", )


async def test_create_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", )


async def test_create_db_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_cluster_snapshot("test-db_cluster_snapshot_identifier", "test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_create_db_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_cluster_snapshot("test-db_cluster_snapshot_identifier", "test-db_cluster_identifier", )


async def test_create_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_instance("test-db_instance_identifier", "test-db_instance_class", "test-engine", )
    mock_client.call.assert_called_once()


async def test_create_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_instance("test-db_instance_identifier", "test-db_instance_class", "test-engine", )


async def test_create_db_instance_read_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_instance_read_replica("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_create_db_instance_read_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_instance_read_replica("test-db_instance_identifier", )


async def test_create_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", )
    mock_client.call.assert_called_once()


async def test_create_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", )


async def test_create_db_proxy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_proxy("test-db_proxy_name", "test-engine_family", "test-role_arn", [], )
    mock_client.call.assert_called_once()


async def test_create_db_proxy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_proxy("test-db_proxy_name", "test-engine_family", "test-role_arn", [], )


async def test_create_db_proxy_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_proxy_endpoint("test-db_proxy_name", "test-db_proxy_endpoint_name", [], )
    mock_client.call.assert_called_once()


async def test_create_db_proxy_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_proxy_endpoint("test-db_proxy_name", "test-db_proxy_endpoint_name", [], )


async def test_create_db_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_security_group("test-db_security_group_name", "test-db_security_group_description", )
    mock_client.call.assert_called_once()


async def test_create_db_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_security_group("test-db_security_group_name", "test-db_security_group_description", )


async def test_create_db_shard_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_shard_group("test-db_shard_group_identifier", "test-db_cluster_identifier", "test-max_acu", )
    mock_client.call.assert_called_once()


async def test_create_db_shard_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_shard_group("test-db_shard_group_identifier", "test-db_cluster_identifier", "test-max_acu", )


async def test_create_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], )
    mock_client.call.assert_called_once()


async def test_create_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], )


async def test_create_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )
    mock_client.call.assert_called_once()


async def test_create_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_event_subscription("test-subscription_name", "test-sns_topic_arn", )


async def test_create_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_create_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_global_cluster("test-global_cluster_identifier", )


async def test_create_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_integration("test-source_arn", "test-target_arn", "test-integration_name", )
    mock_client.call.assert_called_once()


async def test_create_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_integration("test-source_arn", "test-target_arn", "test-integration_name", )


async def test_create_option_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_option_group("test-option_group_name", "test-engine_name", "test-major_engine_version", "test-option_group_description", )
    mock_client.call.assert_called_once()


async def test_create_option_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_option_group("test-option_group_name", "test-engine_name", "test-major_engine_version", "test-option_group_description", )


async def test_create_tenant_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tenant_database("test-db_instance_identifier", "test-tenant_db_name", "test-master_username", )
    mock_client.call.assert_called_once()


async def test_create_tenant_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tenant_database("test-db_instance_identifier", "test-tenant_db_name", "test-master_username", )


async def test_delete_blue_green_deployment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_blue_green_deployment("test-blue_green_deployment_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_blue_green_deployment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_blue_green_deployment("test-blue_green_deployment_identifier", )


async def test_delete_custom_db_engine_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_custom_db_engine_version("test-engine", "test-engine_version", )
    mock_client.call.assert_called_once()


async def test_delete_custom_db_engine_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_custom_db_engine_version("test-engine", "test-engine_version", )


async def test_delete_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster("test-db_cluster_identifier", )


async def test_delete_db_cluster_automated_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_automated_backup("test-db_cluster_resource_id", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_automated_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_automated_backup("test-db_cluster_resource_id", )


async def test_delete_db_cluster_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )


async def test_delete_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )


async def test_delete_db_cluster_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_cluster_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", )


async def test_delete_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_instance("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_instance("test-db_instance_identifier", )


async def test_delete_db_instance_automated_backup(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_instance_automated_backup()
    mock_client.call.assert_called_once()


async def test_delete_db_instance_automated_backup_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_instance_automated_backup()


async def test_delete_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_parameter_group("test-db_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_parameter_group("test-db_parameter_group_name", )


async def test_delete_db_proxy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_proxy("test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_proxy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_proxy("test-db_proxy_name", )


async def test_delete_db_proxy_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_proxy_endpoint("test-db_proxy_endpoint_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_proxy_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_proxy_endpoint("test-db_proxy_endpoint_name", )


async def test_delete_db_security_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_security_group("test-db_security_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_security_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_security_group("test-db_security_group_name", )


async def test_delete_db_shard_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_shard_group("test-db_shard_group_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_db_shard_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_shard_group("test-db_shard_group_identifier", )


async def test_delete_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_db_subnet_group("test-db_subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_db_subnet_group("test-db_subnet_group_name", )


async def test_delete_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_delete_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_event_subscription("test-subscription_name", )


async def test_delete_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_global_cluster("test-global_cluster_identifier", )


async def test_delete_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_integration("test-integration_identifier", )
    mock_client.call.assert_called_once()


async def test_delete_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_integration("test-integration_identifier", )


async def test_delete_option_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_option_group("test-option_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_option_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_option_group("test-option_group_name", )


async def test_delete_tenant_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tenant_database("test-db_instance_identifier", "test-tenant_db_name", )
    mock_client.call.assert_called_once()


async def test_delete_tenant_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tenant_database("test-db_instance_identifier", "test-tenant_db_name", )


async def test_deregister_db_proxy_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_db_proxy_targets("test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_deregister_db_proxy_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_db_proxy_targets("test-db_proxy_name", )


async def test_describe_account_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_attributes()
    mock_client.call.assert_called_once()


async def test_describe_account_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_attributes()


async def test_describe_blue_green_deployments(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_blue_green_deployments()
    mock_client.call.assert_called_once()


async def test_describe_blue_green_deployments_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_blue_green_deployments()


async def test_describe_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_certificates()
    mock_client.call.assert_called_once()


async def test_describe_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_certificates()


async def test_describe_db_cluster_automated_backups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_automated_backups()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_automated_backups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_automated_backups()


async def test_describe_db_cluster_backtracks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_backtracks("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_backtracks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_backtracks("test-db_cluster_identifier", )


async def test_describe_db_cluster_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_endpoints()


async def test_describe_db_cluster_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_parameter_groups()


async def test_describe_db_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", )


async def test_describe_db_cluster_snapshot_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_snapshot_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", )


async def test_describe_db_cluster_snapshots(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_cluster_snapshots()
    mock_client.call.assert_called_once()


async def test_describe_db_cluster_snapshots_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_cluster_snapshots()


async def test_describe_db_clusters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_clusters()
    mock_client.call.assert_called_once()


async def test_describe_db_clusters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_clusters()


async def test_describe_db_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_db_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_engine_versions()


async def test_describe_db_instance_automated_backups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_instance_automated_backups()
    mock_client.call.assert_called_once()


async def test_describe_db_instance_automated_backups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_instance_automated_backups()


async def test_describe_db_log_files(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_log_files("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_db_log_files_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_log_files("test-db_instance_identifier", )


async def test_describe_db_major_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_major_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_db_major_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_major_engine_versions()


async def test_describe_db_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_parameter_groups()


async def test_describe_db_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_parameters("test-db_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_parameters("test-db_parameter_group_name", )


async def test_describe_db_proxies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_proxies()
    mock_client.call.assert_called_once()


async def test_describe_db_proxies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_proxies()


async def test_describe_db_proxy_endpoints(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_proxy_endpoints()
    mock_client.call.assert_called_once()


async def test_describe_db_proxy_endpoints_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_proxy_endpoints()


async def test_describe_db_proxy_target_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_proxy_target_groups("test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_proxy_target_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_proxy_target_groups("test-db_proxy_name", )


async def test_describe_db_proxy_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_proxy_targets("test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_describe_db_proxy_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_proxy_targets("test-db_proxy_name", )


async def test_describe_db_recommendations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_recommendations()
    mock_client.call.assert_called_once()


async def test_describe_db_recommendations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_recommendations()


async def test_describe_db_security_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_security_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_security_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_security_groups()


async def test_describe_db_shard_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_shard_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_shard_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_shard_groups()


async def test_describe_db_snapshot_attributes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_snapshot_attributes("test-db_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_db_snapshot_attributes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_snapshot_attributes("test-db_snapshot_identifier", )


async def test_describe_db_snapshot_tenant_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_snapshot_tenant_databases()
    mock_client.call.assert_called_once()


async def test_describe_db_snapshot_tenant_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_snapshot_tenant_databases()


async def test_describe_db_subnet_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_db_subnet_groups()
    mock_client.call.assert_called_once()


async def test_describe_db_subnet_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_db_subnet_groups()


async def test_describe_engine_default_cluster_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_default_cluster_parameters("test-db_parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_engine_default_cluster_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_default_cluster_parameters("test-db_parameter_group_family", )


async def test_describe_engine_default_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_default_parameters("test-db_parameter_group_family", )
    mock_client.call.assert_called_once()


async def test_describe_engine_default_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_default_parameters("test-db_parameter_group_family", )


async def test_describe_event_categories(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_categories()
    mock_client.call.assert_called_once()


async def test_describe_event_categories_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_categories()


async def test_describe_event_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_event_subscriptions()
    mock_client.call.assert_called_once()


async def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_event_subscriptions()


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_export_tasks(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_export_tasks()
    mock_client.call.assert_called_once()


async def test_describe_export_tasks_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_export_tasks()


async def test_describe_global_clusters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_global_clusters()
    mock_client.call.assert_called_once()


async def test_describe_global_clusters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_global_clusters()


async def test_describe_integrations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_integrations()
    mock_client.call.assert_called_once()


async def test_describe_integrations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_integrations()


async def test_describe_option_group_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_option_group_options("test-engine_name", )
    mock_client.call.assert_called_once()


async def test_describe_option_group_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_option_group_options("test-engine_name", )


async def test_describe_option_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_option_groups()
    mock_client.call.assert_called_once()


async def test_describe_option_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_option_groups()


async def test_describe_orderable_db_instance_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_orderable_db_instance_options("test-engine", )
    mock_client.call.assert_called_once()


async def test_describe_orderable_db_instance_options_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_orderable_db_instance_options("test-engine", )


async def test_describe_pending_maintenance_actions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pending_maintenance_actions()
    mock_client.call.assert_called_once()


async def test_describe_pending_maintenance_actions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pending_maintenance_actions()


async def test_describe_reserved_db_instances(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_db_instances()
    mock_client.call.assert_called_once()


async def test_describe_reserved_db_instances_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_db_instances()


async def test_describe_reserved_db_instances_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_db_instances_offerings()
    mock_client.call.assert_called_once()


async def test_describe_reserved_db_instances_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_db_instances_offerings()


async def test_describe_source_regions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_source_regions()
    mock_client.call.assert_called_once()


async def test_describe_source_regions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_source_regions()


async def test_describe_tenant_databases(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tenant_databases()
    mock_client.call.assert_called_once()


async def test_describe_tenant_databases_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tenant_databases()


async def test_describe_valid_db_instance_modifications(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_valid_db_instance_modifications("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_describe_valid_db_instance_modifications_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_valid_db_instance_modifications("test-db_instance_identifier", )


async def test_disable_http_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await disable_http_endpoint("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_disable_http_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disable_http_endpoint("test-resource_arn", )


async def test_download_db_log_file_portion(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await download_db_log_file_portion("test-db_instance_identifier", "test-log_file_name", )
    mock_client.call.assert_called_once()


async def test_download_db_log_file_portion_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await download_db_log_file_portion("test-db_instance_identifier", "test-log_file_name", )


async def test_enable_http_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await enable_http_endpoint("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_enable_http_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await enable_http_endpoint("test-resource_arn", )


async def test_failover_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_failover_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_db_cluster("test-db_cluster_identifier", )


async def test_failover_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_failover_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_name", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_name", )


async def test_modify_activity_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_activity_stream()
    mock_client.call.assert_called_once()


async def test_modify_activity_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_activity_stream()


async def test_modify_certificates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_certificates()
    mock_client.call.assert_called_once()


async def test_modify_certificates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_certificates()


async def test_modify_current_db_cluster_capacity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_current_db_cluster_capacity("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_current_db_cluster_capacity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_current_db_cluster_capacity("test-db_cluster_identifier", )


async def test_modify_custom_db_engine_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_custom_db_engine_version("test-engine", "test-engine_version", )
    mock_client.call.assert_called_once()


async def test_modify_custom_db_engine_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_custom_db_engine_version("test-engine", "test-engine_version", )


async def test_modify_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster("test-db_cluster_identifier", )


async def test_modify_db_cluster_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", )


async def test_modify_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], )


async def test_modify_db_cluster_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_cluster_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", )


async def test_modify_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_instance("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_instance("test-db_instance_identifier", )


async def test_modify_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_parameter_group("test-db_parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_parameter_group("test-db_parameter_group_name", [], )


async def test_modify_db_proxy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_proxy("test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_proxy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_proxy("test-db_proxy_name", )


async def test_modify_db_proxy_endpoint(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_proxy_endpoint("test-db_proxy_endpoint_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_proxy_endpoint_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_proxy_endpoint("test-db_proxy_endpoint_name", )


async def test_modify_db_proxy_target_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_proxy_target_group("test-target_group_name", "test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_proxy_target_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_proxy_target_group("test-target_group_name", "test-db_proxy_name", )


async def test_modify_db_recommendation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_recommendation("test-recommendation_id", )
    mock_client.call.assert_called_once()


async def test_modify_db_recommendation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_recommendation("test-recommendation_id", )


async def test_modify_db_shard_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_shard_group("test-db_shard_group_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_db_shard_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_shard_group("test-db_shard_group_identifier", )


async def test_modify_db_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_snapshot("test-db_snapshot_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_db_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_snapshot("test-db_snapshot_identifier", )


async def test_modify_db_snapshot_attribute(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_snapshot_attribute("test-db_snapshot_identifier", "test-attribute_name", )
    mock_client.call.assert_called_once()


async def test_modify_db_snapshot_attribute_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_snapshot_attribute("test-db_snapshot_identifier", "test-attribute_name", )


async def test_modify_db_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_db_subnet_group("test-db_subnet_group_name", [], )
    mock_client.call.assert_called_once()


async def test_modify_db_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_db_subnet_group("test-db_subnet_group_name", [], )


async def test_modify_event_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_event_subscription("test-subscription_name", )
    mock_client.call.assert_called_once()


async def test_modify_event_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_event_subscription("test-subscription_name", )


async def test_modify_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_global_cluster("test-global_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_global_cluster("test-global_cluster_identifier", )


async def test_modify_integration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_integration("test-integration_identifier", )
    mock_client.call.assert_called_once()


async def test_modify_integration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_integration("test-integration_identifier", )


async def test_modify_option_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_option_group("test-option_group_name", )
    mock_client.call.assert_called_once()


async def test_modify_option_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_option_group("test-option_group_name", )


async def test_modify_tenant_database(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await modify_tenant_database("test-db_instance_identifier", "test-tenant_db_name", )
    mock_client.call.assert_called_once()


async def test_modify_tenant_database_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await modify_tenant_database("test-db_instance_identifier", "test-tenant_db_name", )


async def test_promote_read_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await promote_read_replica("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_promote_read_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await promote_read_replica("test-db_instance_identifier", )


async def test_promote_read_replica_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await promote_read_replica_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_promote_read_replica_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await promote_read_replica_db_cluster("test-db_cluster_identifier", )


async def test_purchase_reserved_db_instances_offering(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_reserved_db_instances_offering("test-reserved_db_instances_offering_id", )
    mock_client.call.assert_called_once()


async def test_purchase_reserved_db_instances_offering_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_reserved_db_instances_offering("test-reserved_db_instances_offering_id", )


async def test_reboot_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_reboot_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_db_cluster("test-db_cluster_identifier", )


async def test_reboot_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_db_instance("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_reboot_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_db_instance("test-db_instance_identifier", )


async def test_reboot_db_shard_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_db_shard_group("test-db_shard_group_identifier", )
    mock_client.call.assert_called_once()


async def test_reboot_db_shard_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_db_shard_group("test-db_shard_group_identifier", )


async def test_register_db_proxy_targets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_db_proxy_targets("test-db_proxy_name", )
    mock_client.call.assert_called_once()


async def test_register_db_proxy_targets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_db_proxy_targets("test-db_proxy_name", )


async def test_remove_from_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_remove_from_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", )


async def test_remove_role_from_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_remove_role_from_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", )


async def test_remove_role_from_db_instance(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_role_from_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", )
    mock_client.call.assert_called_once()


async def test_remove_role_from_db_instance_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_role_from_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", )


async def test_remove_source_identifier_from_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", )
    mock_client.call.assert_called_once()


async def test_remove_source_identifier_from_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", )


async def test_remove_tags_from_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await remove_tags_from_resource("test-resource_name", [], )
    mock_client.call.assert_called_once()


async def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await remove_tags_from_resource("test-resource_name", [], )


async def test_reset_db_cluster_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_db_cluster_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", )


async def test_reset_db_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_db_parameter_group("test-db_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_db_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_db_parameter_group("test-db_parameter_group_name", )


async def test_restore_db_cluster_from_s3(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_cluster_from_s3("test-db_cluster_identifier", "test-engine", "test-master_username", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", )
    mock_client.call.assert_called_once()


async def test_restore_db_cluster_from_s3_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_cluster_from_s3("test-db_cluster_identifier", "test-engine", "test-master_username", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", )


async def test_restore_db_cluster_from_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", )
    mock_client.call.assert_called_once()


async def test_restore_db_cluster_from_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", )


async def test_restore_db_cluster_to_point_in_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_restore_db_cluster_to_point_in_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", )


async def test_restore_db_instance_from_db_snapshot(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_instance_from_db_snapshot("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_restore_db_instance_from_db_snapshot_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_instance_from_db_snapshot("test-db_instance_identifier", )


async def test_restore_db_instance_from_s3(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_instance_from_s3("test-db_instance_identifier", "test-db_instance_class", "test-engine", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", )
    mock_client.call.assert_called_once()


async def test_restore_db_instance_from_s3_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_instance_from_s3("test-db_instance_identifier", "test-db_instance_class", "test-engine", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", )


async def test_restore_db_instance_to_point_in_time(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await restore_db_instance_to_point_in_time("test-target_db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_restore_db_instance_to_point_in_time_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await restore_db_instance_to_point_in_time("test-target_db_instance_identifier", )


async def test_revoke_db_security_group_ingress(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await revoke_db_security_group_ingress("test-db_security_group_name", )
    mock_client.call.assert_called_once()


async def test_revoke_db_security_group_ingress_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await revoke_db_security_group_ingress("test-db_security_group_name", )


async def test_start_activity_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_activity_stream("test-resource_arn", "test-mode", "test-kms_key_id", )
    mock_client.call.assert_called_once()


async def test_start_activity_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_activity_stream("test-resource_arn", "test-mode", "test-kms_key_id", )


async def test_start_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_start_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_db_cluster("test-db_cluster_identifier", )


async def test_start_db_instance_automated_backups_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_db_instance_automated_backups_replication("test-source_db_instance_arn", )
    mock_client.call.assert_called_once()


async def test_start_db_instance_automated_backups_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_db_instance_automated_backups_replication("test-source_db_instance_arn", )


async def test_start_export_task(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_export_task("test-export_task_identifier", "test-source_arn", "test-s3_bucket_name", "test-iam_role_arn", "test-kms_key_id", )
    mock_client.call.assert_called_once()


async def test_start_export_task_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_export_task("test-export_task_identifier", "test-source_arn", "test-s3_bucket_name", "test-iam_role_arn", "test-kms_key_id", )


async def test_stop_activity_stream(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_activity_stream("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_stop_activity_stream_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_activity_stream("test-resource_arn", )


async def test_stop_db_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_db_cluster("test-db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_stop_db_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_db_cluster("test-db_cluster_identifier", )


async def test_stop_db_instance_automated_backups_replication(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await stop_db_instance_automated_backups_replication("test-source_db_instance_arn", )
    mock_client.call.assert_called_once()


async def test_stop_db_instance_automated_backups_replication_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await stop_db_instance_automated_backups_replication("test-source_db_instance_arn", )


async def test_switchover_blue_green_deployment(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await switchover_blue_green_deployment("test-blue_green_deployment_identifier", )
    mock_client.call.assert_called_once()


async def test_switchover_blue_green_deployment_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await switchover_blue_green_deployment("test-blue_green_deployment_identifier", )


async def test_switchover_global_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )
    mock_client.call.assert_called_once()


async def test_switchover_global_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", )


async def test_switchover_read_replica(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    await switchover_read_replica("test-db_instance_identifier", )
    mock_client.call.assert_called_once()


async def test_switchover_read_replica_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.rds.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await switchover_read_replica("test-db_instance_identifier", )


@pytest.mark.asyncio
async def test_add_role_to_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import add_role_to_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_authorize_db_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import authorize_db_security_group_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await authorize_db_security_group_ingress("test-db_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_id="test-ec2_security_group_id", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_backtrack_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import backtrack_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await backtrack_db_cluster("test-db_cluster_identifier", "test-backtrack_to", force=True, use_earliest_time_on_point_in_time_unavailable=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import copy_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import copy_db_cluster_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", copy_tags=[{"Key": "k", "Value": "v"}], tags=[{"Key": "k", "Value": "v"}], source_region="test-source_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import copy_db_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_db_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import copy_db_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await copy_db_snapshot("test-source_db_snapshot_identifier", "test-target_db_snapshot_identifier", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], copy_tags=[{"Key": "k", "Value": "v"}], pre_signed_url="test-pre_signed_url", option_group_name="test-option_group_name", target_custom_availability_zone="test-target_custom_availability_zone", snapshot_target="test-snapshot_target", copy_option_group="test-copy_option_group", snapshot_availability_zone="test-snapshot_availability_zone", source_region="test-source_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_copy_option_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import copy_option_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await copy_option_group("test-source_option_group_identifier", "test-target_option_group_identifier", "test-target_option_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_blue_green_deployment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_blue_green_deployment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_blue_green_deployment("test-blue_green_deployment_name", "test-source", target_engine_version="test-target_engine_version", target_db_parameter_group_name="test-target_db_parameter_group_name", target_db_cluster_parameter_group_name="test-target_db_cluster_parameter_group_name", tags=[{"Key": "k", "Value": "v"}], target_db_instance_class="test-target_db_instance_class", upgrade_target_storage_config={}, target_iops="test-target_iops", target_storage_type="test-target_storage_type", target_allocated_storage="test-target_allocated_storage", target_storage_throughput="test-target_storage_throughput", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_custom_db_engine_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_custom_db_engine_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_custom_db_engine_version("test-engine", "test-engine_version", database_installation_files_s3_bucket_name="test-database_installation_files_s3_bucket_name", database_installation_files_s3_prefix="test-database_installation_files_s3_prefix", image_id="test-image_id", kms_key_id="test-kms_key_id", source_custom_db_engine_version_identifier="test-source_custom_db_engine_version_identifier", use_aws_provided_latest_image=True, description="test-description", manifest="test-manifest", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster("test-db_cluster_identifier", "test-engine", availability_zones="test-availability_zones", backup_retention_period="test-backup_retention_period", character_set_name="test-character_set_name", database_name="test-database_name", db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", vpc_security_group_ids="test-vpc_security_group_ids", db_subnet_group_name="test-db_subnet_group_name", engine_version="test-engine_version", port=1, master_username="test-master_username", master_user_password="test-master_user_password", option_group_name="test-option_group_name", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", replication_source_identifier="test-replication_source_identifier", tags=[{"Key": "k", "Value": "v"}], storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, engine_mode="test-engine_mode", scaling_configuration={}, rds_custom_cluster_configuration={}, db_cluster_instance_class="test-db_cluster_instance_class", allocated_storage="test-allocated_storage", storage_type="test-storage_type", iops="test-iops", publicly_accessible="test-publicly_accessible", auto_minor_version_upgrade=True, deletion_protection="test-deletion_protection", global_cluster_identifier="test-global_cluster_identifier", enable_http_endpoint=True, copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", enable_global_write_forwarding=True, network_type="test-network_type", serverless_v2_scaling_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_limitless_database=True, cluster_scalability_type="test-cluster_scalability_type", db_system_id="test-db_system_id", manage_master_user_password="test-manage_master_user_password", enable_local_write_forwarding=True, master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, master_user_authentication_type="test-master_user_authentication_type", source_region="test-source_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_cluster_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_cluster_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_cluster_snapshot("test-db_cluster_snapshot_identifier", "test-db_cluster_identifier", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_instance("test-db_instance_identifier", "test-db_instance_class", "test-engine", db_name="test-db_name", allocated_storage="test-allocated_storage", master_username="test-master_username", master_user_password="test-master_user_password", db_security_groups="test-db_security_groups", vpc_security_group_ids="test-vpc_security_group_ids", availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", preferred_maintenance_window="test-preferred_maintenance_window", db_parameter_group_name="test-db_parameter_group_name", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", port=1, multi_az=True, engine_version="test-engine_version", auto_minor_version_upgrade=True, license_model="test-license_model", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", character_set_name="test-character_set_name", nchar_character_set_name="test-nchar_character_set_name", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], db_cluster_identifier="test-db_cluster_identifier", storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", domain="test-domain", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", domain_iam_role_name="test-domain_iam_role_name", promotion_tier="test-promotion_tier", timezone="test-timezone", enable_iam_database_authentication=True, database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", deletion_protection="test-deletion_protection", max_allocated_storage=1, enable_customer_owned_ip=True, network_type="test-network_type", backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", db_system_id="test-db_system_id", ca_certificate_identifier="test-ca_certificate_identifier", manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", multi_tenant=True, dedicated_log_volume="test-dedicated_log_volume", engine_lifecycle_support=1, master_user_authentication_type="test-master_user_authentication_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_instance_read_replica_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_instance_read_replica
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_instance_read_replica("test-db_instance_identifier", source_db_instance_identifier="test-source_db_instance_identifier", db_instance_class="test-db_instance_class", availability_zone="test-availability_zone", port=1, multi_az=True, auto_minor_version_upgrade=True, iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", db_parameter_group_name="test-db_parameter_group_name", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], db_subnet_group_name="test-db_subnet_group_name", vpc_security_group_ids="test-vpc_security_group_ids", storage_type="test-storage_type", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", enable_iam_database_authentication=True, database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, deletion_protection="test-deletion_protection", domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", replica_mode="test-replica_mode", enable_customer_owned_ip=True, network_type="test-network_type", max_allocated_storage=1, backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", allocated_storage="test-allocated_storage", source_db_cluster_identifier="test-source_db_cluster_identifier", dedicated_log_volume="test-dedicated_log_volume", upgrade_storage_config={}, ca_certificate_identifier="test-ca_certificate_identifier", source_region="test-source_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_proxy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_proxy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_proxy("test-db_proxy_name", "test-engine_family", "test-role_arn", "test-vpc_subnet_ids", default_auth_scheme="test-default_auth_scheme", auth="test-auth", vpc_security_group_ids="test-vpc_security_group_ids", require_tls=True, idle_client_timeout=1, debug_logging="test-debug_logging", tags=[{"Key": "k", "Value": "v"}], endpoint_network_type="test-endpoint_network_type", target_connection_network_type="test-target_connection_network_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_proxy_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_proxy_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_proxy_endpoint("test-db_proxy_name", "test-db_proxy_endpoint_name", "test-vpc_subnet_ids", vpc_security_group_ids="test-vpc_security_group_ids", target_role="test-target_role", tags=[{"Key": "k", "Value": "v"}], endpoint_network_type="test-endpoint_network_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_security_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_security_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_security_group("test-db_security_group_name", "test-db_security_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_shard_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_shard_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_shard_group("test-db_shard_group_identifier", "test-db_cluster_identifier", 1, compute_redundancy="test-compute_redundancy", min_acu="test-min_acu", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_db_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", "test-subnet_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_global_cluster("test-global_cluster_identifier", source_db_cluster_identifier="test-source_db_cluster_identifier", engine="test-engine", engine_version="test-engine_version", engine_lifecycle_support=1, deletion_protection="test-deletion_protection", database_name="test-database_name", storage_encrypted="test-storage_encrypted", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_integration("test-source_arn", "test-target_arn", "test-integration_name", kms_key_id="test-kms_key_id", additional_encryption_context={}, tags=[{"Key": "k", "Value": "v"}], data_filter=[{}], description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_option_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_option_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_option_group("test-option_group_name", "test-engine_name", "test-major_engine_version", "test-option_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_tenant_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import create_tenant_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await create_tenant_database("test-db_instance_identifier", "test-tenant_db_name", "test-master_username", master_user_password="test-master_user_password", character_set_name="test-character_set_name", nchar_character_set_name="test-nchar_character_set_name", manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_blue_green_deployment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import delete_blue_green_deployment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await delete_blue_green_deployment("test-blue_green_deployment_identifier", delete_target=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import delete_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await delete_db_cluster("test-db_cluster_identifier", skip_final_snapshot=True, final_db_snapshot_identifier="test-final_db_snapshot_identifier", delete_automated_backups=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_db_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import delete_db_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await delete_db_instance("test-db_instance_identifier", skip_final_snapshot=True, final_db_snapshot_identifier="test-final_db_snapshot_identifier", delete_automated_backups=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_db_instance_automated_backup_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import delete_db_instance_automated_backup
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await delete_db_instance_automated_backup(dbi_resource_id="test-dbi_resource_id", db_instance_automated_backups_arn="test-db_instance_automated_backups_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_tenant_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import delete_tenant_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await delete_tenant_database("test-db_instance_identifier", "test-tenant_db_name", skip_final_snapshot=True, final_db_snapshot_identifier="test-final_db_snapshot_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_deregister_db_proxy_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import deregister_db_proxy_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await deregister_db_proxy_targets("test-db_proxy_name", target_group_name="test-target_group_name", db_instance_identifiers="test-db_instance_identifiers", db_cluster_identifiers="test-db_cluster_identifiers", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_blue_green_deployments_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_blue_green_deployments
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_blue_green_deployments(blue_green_deployment_identifier="test-blue_green_deployment_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_certificates(certificate_identifier="test-certificate_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_automated_backups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_cluster_automated_backups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_automated_backups(db_cluster_resource_id="test-db_cluster_resource_id", db_cluster_identifier="test-db_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_backtracks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_cluster_backtracks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_backtracks("test-db_cluster_identifier", backtrack_identifier="test-backtrack_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_cluster_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_endpoints(db_cluster_identifier="test-db_cluster_identifier", db_cluster_endpoint_identifier="test-db_cluster_endpoint_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_cluster_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_parameter_groups(db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_parameters("test-db_cluster_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_cluster_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_cluster_snapshots(db_cluster_identifier="test-db_cluster_identifier", db_cluster_snapshot_identifier="test-db_cluster_snapshot_identifier", snapshot_type="test-snapshot_type", filters=[{}], max_records=1, marker="test-marker", include_shared=True, include_public=True, db_cluster_resource_id="test-db_cluster_resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_clusters(db_cluster_identifier="test-db_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", include_shared=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_engine_versions(engine="test-engine", engine_version="test-engine_version", db_parameter_group_family="test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", default_only="test-default_only", list_supported_character_sets=1, list_supported_timezones=1, include_all=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_instance_automated_backups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_instance_automated_backups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_instance_automated_backups(dbi_resource_id="test-dbi_resource_id", db_instance_identifier="test-db_instance_identifier", filters=[{}], max_records=1, marker="test-marker", db_instance_automated_backups_arn="test-db_instance_automated_backups_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_log_files_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_log_files
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_log_files("test-db_instance_identifier", filename_contains="test-filename_contains", file_last_written="test-file_last_written", file_size=1, filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_major_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_major_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_major_engine_versions(engine="test-engine", major_engine_version="test-major_engine_version", marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_parameter_groups(db_parameter_group_name="test-db_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_parameters("test-db_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_proxies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_proxies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_proxies(db_proxy_name="test-db_proxy_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_proxy_endpoints_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_proxy_endpoints
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_proxy_endpoints(db_proxy_name="test-db_proxy_name", db_proxy_endpoint_name="test-db_proxy_endpoint_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_proxy_target_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_proxy_target_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_proxy_target_groups("test-db_proxy_name", target_group_name="test-target_group_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_proxy_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_proxy_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_proxy_targets("test-db_proxy_name", target_group_name="test-target_group_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_recommendations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_recommendations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_recommendations(last_updated_after="test-last_updated_after", last_updated_before="test-last_updated_before", locale="test-locale", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_security_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_security_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_security_groups(db_security_group_name="test-db_security_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_shard_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_shard_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_shard_groups(db_shard_group_identifier="test-db_shard_group_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_snapshot_tenant_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_snapshot_tenant_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_snapshot_tenant_databases(db_instance_identifier="test-db_instance_identifier", db_snapshot_identifier="test-db_snapshot_identifier", snapshot_type="test-snapshot_type", filters=[{}], max_records=1, marker="test-marker", dbi_resource_id="test-dbi_resource_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_db_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_db_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_db_subnet_groups(db_subnet_group_name="test-db_subnet_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_engine_default_cluster_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_engine_default_cluster_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_default_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_engine_default_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_engine_default_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_event_categories
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_event_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_export_tasks_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_export_tasks
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_export_tasks(export_task_identifier=1, source_arn="test-source_arn", filters=[{}], marker="test-marker", max_records=1, source_type="test-source_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_global_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_global_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_global_clusters(global_cluster_identifier="test-global_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_integrations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_integrations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_integrations(integration_identifier="test-integration_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_option_group_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_option_group_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_option_group_options("test-engine_name", major_engine_version="test-major_engine_version", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_option_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_option_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_option_groups(option_group_name="test-option_group_name", filters=[{}], marker="test-marker", max_records=1, engine_name="test-engine_name", major_engine_version="test-major_engine_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_orderable_db_instance_options_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_orderable_db_instance_options
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_orderable_db_instance_options("test-engine", engine_version="test-engine_version", db_instance_class="test-db_instance_class", license_model="test-license_model", availability_zone_group="test-availability_zone_group", vpc="test-vpc", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_pending_maintenance_actions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_pending_maintenance_actions(resource_identifier="test-resource_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_db_instances_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_reserved_db_instances
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_db_instances(reserved_db_instance_id="test-reserved_db_instance_id", reserved_db_instances_offering_id="test-reserved_db_instances_offering_id", db_instance_class="test-db_instance_class", duration=1, product_description="test-product_description", offering_type="test-offering_type", multi_az=True, lease_id="test-lease_id", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_db_instances_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_reserved_db_instances_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_db_instances_offerings(reserved_db_instances_offering_id="test-reserved_db_instances_offering_id", db_instance_class="test-db_instance_class", duration=1, product_description="test-product_description", offering_type="test-offering_type", multi_az=True, filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_source_regions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_source_regions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_source_regions(target_region_name="test-target_region_name", max_records=1, marker="test-marker", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tenant_databases_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import describe_tenant_databases
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await describe_tenant_databases(db_instance_identifier="test-db_instance_identifier", tenant_db_name="test-tenant_db_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_download_db_log_file_portion_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import download_db_log_file_portion
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await download_db_log_file_portion("test-db_instance_identifier", "test-log_file_name", marker="test-marker", number_of_lines="test-number_of_lines", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_failover_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import failover_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await failover_db_cluster("test-db_cluster_identifier", target_db_instance_identifier="test-target_db_instance_identifier", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_failover_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import failover_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", allow_data_loss=True, switchover="test-switchover", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import list_tags_for_resource
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await list_tags_for_resource("test-resource_name", filters=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_activity_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_activity_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_activity_stream(resource_arn="test-resource_arn", audit_policy_state="test-audit_policy_state", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_certificates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_certificates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_certificates(certificate_identifier="test-certificate_identifier", remove_customer_override="test-remove_customer_override", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_current_db_cluster_capacity_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_current_db_cluster_capacity
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_current_db_cluster_capacity("test-db_cluster_identifier", capacity="test-capacity", seconds_before_timeout=1, timeout_action=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_custom_db_engine_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_custom_db_engine_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_custom_db_engine_version("test-engine", "test-engine_version", description="test-description", status="test-status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_cluster("test-db_cluster_identifier", new_db_cluster_identifier="test-new_db_cluster_identifier", apply_immediately=True, backup_retention_period="test-backup_retention_period", db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", vpc_security_group_ids="test-vpc_security_group_ids", port=1, master_user_password="test-master_user_password", option_group_name="test-option_group_name", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", cloudwatch_logs_export_configuration=1, engine_version="test-engine_version", allow_major_version_upgrade=True, db_instance_parameter_group_name="test-db_instance_parameter_group_name", domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", scaling_configuration={}, deletion_protection="test-deletion_protection", enable_http_endpoint=True, copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], enable_global_write_forwarding=True, db_cluster_instance_class="test-db_cluster_instance_class", allocated_storage="test-allocated_storage", storage_type="test-storage_type", iops="test-iops", auto_minor_version_upgrade=True, network_type="test-network_type", serverless_v2_scaling_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", manage_master_user_password="test-manage_master_user_password", rotate_master_user_password="test-rotate_master_user_password", enable_local_write_forwarding=True, master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", engine_mode="test-engine_mode", allow_engine_mode_change=True, aws_backup_recovery_point_arn="test-aws_backup_recovery_point_arn", enable_limitless_database=True, ca_certificate_identifier="test-ca_certificate_identifier", master_user_authentication_type="test-master_user_authentication_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_cluster_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", endpoint_type="test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_cluster_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_cluster_snapshot_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_instance("test-db_instance_identifier", allocated_storage="test-allocated_storage", db_instance_class="test-db_instance_class", db_subnet_group_name="test-db_subnet_group_name", db_security_groups="test-db_security_groups", vpc_security_group_ids="test-vpc_security_group_ids", apply_immediately=True, master_user_password="test-master_user_password", db_parameter_group_name="test-db_parameter_group_name", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", multi_az=True, engine_version="test-engine_version", allow_major_version_upgrade=True, auto_minor_version_upgrade=True, license_model="test-license_model", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", new_db_instance_identifier="test-new_db_instance_identifier", storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", ca_certificate_identifier="test-ca_certificate_identifier", domain="test-domain", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", disable_domain=True, copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", db_port_number=1, publicly_accessible="test-publicly_accessible", monitoring_role_arn="test-monitoring_role_arn", domain_iam_role_name="test-domain_iam_role_name", promotion_tier="test-promotion_tier", enable_iam_database_authentication=True, database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", cloudwatch_logs_export_configuration=1, processor_features="test-processor_features", use_default_processor_features=True, deletion_protection="test-deletion_protection", max_allocated_storage=1, certificate_rotation_restart="test-certificate_rotation_restart", replica_mode="test-replica_mode", automation_mode=True, resume_full_automation_mode_minutes="test-resume_full_automation_mode_minutes", enable_customer_owned_ip=True, network_type="test-network_type", aws_backup_recovery_point_arn="test-aws_backup_recovery_point_arn", manage_master_user_password="test-manage_master_user_password", rotate_master_user_password="test-rotate_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", multi_tenant=True, dedicated_log_volume="test-dedicated_log_volume", engine="test-engine", master_user_authentication_type="test-master_user_authentication_type", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_proxy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_proxy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_proxy("test-db_proxy_name", new_db_proxy_name="test-new_db_proxy_name", default_auth_scheme="test-default_auth_scheme", auth="test-auth", require_tls=True, idle_client_timeout=1, debug_logging="test-debug_logging", role_arn="test-role_arn", security_groups="test-security_groups", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_proxy_endpoint_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_proxy_endpoint
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_proxy_endpoint("test-db_proxy_endpoint_name", new_db_proxy_endpoint_name="test-new_db_proxy_endpoint_name", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_proxy_target_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_proxy_target_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_proxy_target_group("test-target_group_name", "test-db_proxy_name", connection_pool_config={}, new_name="test-new_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_recommendation_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_recommendation
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_recommendation("test-recommendation_id", locale="test-locale", status="test-status", recommended_action_updates="test-recommended_action_updates", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_shard_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_shard_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_shard_group("test-db_shard_group_identifier", max_acu=1, min_acu="test-min_acu", compute_redundancy="test-compute_redundancy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_snapshot("test-db_snapshot_identifier", engine_version="test-engine_version", option_group_name="test-option_group_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_snapshot_attribute
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_snapshot_attribute("test-db_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_db_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_db_subnet_group("test-db_subnet_group_name", "test-subnet_ids", db_subnet_group_description="test-db_subnet_group_description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_event_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_global_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_global_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_global_cluster("test-global_cluster_identifier", new_global_cluster_identifier="test-new_global_cluster_identifier", deletion_protection="test-deletion_protection", engine_version="test-engine_version", allow_major_version_upgrade=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_integration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_integration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_integration("test-integration_identifier", integration_name="test-integration_name", data_filter=[{}], description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_option_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_option_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_option_group("test-option_group_name", options_to_include={}, options_to_remove={}, apply_immediately=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_modify_tenant_database_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import modify_tenant_database
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await modify_tenant_database("test-db_instance_identifier", "test-tenant_db_name", master_user_password="test-master_user_password", new_tenant_db_name="test-new_tenant_db_name", manage_master_user_password="test-manage_master_user_password", rotate_master_user_password="test-rotate_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_promote_read_replica_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import promote_read_replica
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await promote_read_replica("test-db_instance_identifier", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_reserved_db_instances_offering_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import purchase_reserved_db_instances_offering
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await purchase_reserved_db_instances_offering("test-reserved_db_instances_offering_id", reserved_db_instance_id="test-reserved_db_instance_id", db_instance_count=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reboot_db_instance_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import reboot_db_instance
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await reboot_db_instance("test-db_instance_identifier", force_failover=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_db_proxy_targets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import register_db_proxy_targets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await register_db_proxy_targets("test-db_proxy_name", target_group_name="test-target_group_name", db_instance_identifiers="test-db_instance_identifiers", db_cluster_identifiers="test-db_cluster_identifiers", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_remove_role_from_db_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import remove_role_from_db_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import reset_db_cluster_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import reset_db_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await reset_db_parameter_group("test-db_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_cluster_from_s3_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import restore_db_cluster_from_s3
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await restore_db_cluster_from_s3("test-db_cluster_identifier", "test-engine", "test-master_username", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", availability_zones="test-availability_zones", backup_retention_period="test-backup_retention_period", character_set_name="test-character_set_name", database_name="test-database_name", db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", vpc_security_group_ids="test-vpc_security_group_ids", db_subnet_group_name="test-db_subnet_group_name", engine_version="test-engine_version", port=1, master_user_password="test-master_user_password", option_group_name="test-option_group_name", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", tags=[{"Key": "k", "Value": "v"}], storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, s3_prefix="test-s3_prefix", backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", storage_type="test-storage_type", network_type="test-network_type", serverless_v2_scaling_configuration={}, manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_cluster_from_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import restore_db_cluster_from_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", availability_zones="test-availability_zones", engine_version="test-engine_version", port=1, db_subnet_group_name="test-db_subnet_group_name", database_name="test-database_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, engine_mode="test-engine_mode", scaling_configuration={}, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", db_cluster_instance_class="test-db_cluster_instance_class", storage_type="test-storage_type", iops="test-iops", publicly_accessible="test-publicly_accessible", network_type="test-network_type", serverless_v2_scaling_configuration={}, rds_custom_cluster_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_cluster_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import restore_db_cluster_to_point_in_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await restore_db_cluster_to_point_in_time("test-db_cluster_identifier", restore_type="test-restore_type", source_db_cluster_identifier="test-source_db_cluster_identifier", restore_to_time="test-restore_to_time", use_latest_restorable_time=True, port=1, db_subnet_group_name="test-db_subnet_group_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", db_cluster_instance_class="test-db_cluster_instance_class", storage_type="test-storage_type", publicly_accessible="test-publicly_accessible", iops="test-iops", network_type="test-network_type", source_db_cluster_resource_id="test-source_db_cluster_resource_id", serverless_v2_scaling_configuration={}, scaling_configuration={}, engine_mode="test-engine_mode", rds_custom_cluster_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_instance_from_db_snapshot_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import restore_db_instance_from_db_snapshot
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await restore_db_instance_from_db_snapshot("test-db_instance_identifier", db_snapshot_identifier="test-db_snapshot_identifier", db_instance_class="test-db_instance_class", port=1, availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", multi_az=True, publicly_accessible="test-publicly_accessible", auto_minor_version_upgrade=True, license_model="test-license_model", db_name="test-db_name", engine="test-engine", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", tags=[{"Key": "k", "Value": "v"}], storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", vpc_security_group_ids="test-vpc_security_group_ids", domain="test-domain", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain_iam_role_name="test-domain_iam_role_name", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, db_parameter_group_name="test-db_parameter_group_name", deletion_protection="test-deletion_protection", enable_customer_owned_ip=True, network_type="test-network_type", backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", allocated_storage="test-allocated_storage", db_cluster_snapshot_identifier="test-db_cluster_snapshot_identifier", dedicated_log_volume="test-dedicated_log_volume", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_instance_from_s3_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import restore_db_instance_from_s3
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await restore_db_instance_from_s3("test-db_instance_identifier", "test-db_instance_class", "test-engine", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", db_name="test-db_name", allocated_storage="test-allocated_storage", master_username="test-master_username", master_user_password="test-master_user_password", db_security_groups="test-db_security_groups", vpc_security_group_ids="test-vpc_security_group_ids", availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", preferred_maintenance_window="test-preferred_maintenance_window", db_parameter_group_name="test-db_parameter_group_name", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", port=1, multi_az=True, engine_version="test-engine_version", auto_minor_version_upgrade=True, license_model="test-license_model", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], storage_type="test-storage_type", storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", enable_iam_database_authentication=True, s3_prefix="test-s3_prefix", database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, deletion_protection="test-deletion_protection", max_allocated_storage=1, network_type="test-network_type", manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", dedicated_log_volume="test-dedicated_log_volume", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_restore_db_instance_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import restore_db_instance_to_point_in_time
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await restore_db_instance_to_point_in_time("test-target_db_instance_identifier", source_db_instance_identifier="test-source_db_instance_identifier", restore_time="test-restore_time", use_latest_restorable_time=True, db_instance_class="test-db_instance_class", port=1, availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", multi_az=True, publicly_accessible="test-publicly_accessible", auto_minor_version_upgrade=True, license_model="test-license_model", db_name="test-db_name", engine="test-engine", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], tags=[{"Key": "k", "Value": "v"}], storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", vpc_security_group_ids="test-vpc_security_group_ids", domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, db_parameter_group_name="test-db_parameter_group_name", deletion_protection="test-deletion_protection", source_dbi_resource_id="test-source_dbi_resource_id", max_allocated_storage=1, enable_customer_owned_ip=True, network_type="test-network_type", source_db_instance_automated_backups_arn="test-source_db_instance_automated_backups_arn", backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", allocated_storage="test-allocated_storage", dedicated_log_volume="test-dedicated_log_volume", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_revoke_db_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import revoke_db_security_group_ingress
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await revoke_db_security_group_ingress("test-db_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_id="test-ec2_security_group_id", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_activity_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import start_activity_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await start_activity_stream("test-resource_arn", "test-mode", "test-kms_key_id", apply_immediately=True, engine_native_audit_fields_included="test-engine_native_audit_fields_included", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_db_instance_automated_backups_replication_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import start_db_instance_automated_backups_replication
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await start_db_instance_automated_backups_replication("test-source_db_instance_arn", backup_retention_period="test-backup_retention_period", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", source_region="test-source_region", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_start_export_task_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import start_export_task
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await start_export_task(1, "test-source_arn", "test-s3_bucket_name", "test-iam_role_arn", "test-kms_key_id", s3_prefix="test-s3_prefix", export_only=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_stop_activity_stream_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import stop_activity_stream
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await stop_activity_stream("test-resource_arn", apply_immediately=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_switchover_blue_green_deployment_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.rds import switchover_blue_green_deployment
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.rds.async_client", lambda *a, **kw: mock_client)
    await switchover_blue_green_deployment("test-blue_green_deployment_identifier", switchover_timeout=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
