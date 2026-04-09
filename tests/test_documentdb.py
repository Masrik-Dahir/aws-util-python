"""Tests for aws_util.documentdb module."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.documentdb as docdb_mod
from aws_util.documentdb import (
    ClusterResult,
    ClusterSnapshotResult,
    InstanceResult,
    _parse_cluster,
    _parse_instance,
    _parse_snapshot,
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


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _cluster_dict(**overrides):
    d = {
        "DBClusterIdentifier": CLUSTER_ID,
        "Status": "available",
        "Engine": "docdb",
        "EngineVersion": "5.0.0",
        "Endpoint": "cluster.example.com",
        "ReaderEndpoint": "reader.example.com",
        "Port": 27017,
        "MasterUsername": "admin",
        "DBSubnetGroup": "default",
    }
    d.update(overrides)
    return d


def _instance_dict(**overrides):
    d = {
        "DBInstanceIdentifier": INSTANCE_ID,
        "DBInstanceClass": "db.r5.large",
        "DBInstanceStatus": "available",
        "Engine": "docdb",
        "EngineVersion": "5.0.0",
        "Endpoint": {"Address": "inst.example.com", "Port": 27017},
        "DBClusterIdentifier": CLUSTER_ID,
        "AvailabilityZone": "us-east-1a",
    }
    d.update(overrides)
    return d


def _snapshot_dict(**overrides):
    d = {
        "DBClusterSnapshotIdentifier": SNAP_ID,
        "DBClusterIdentifier": CLUSTER_ID,
        "Status": "available",
        "Engine": "docdb",
        "EngineVersion": "5.0.0",
        "SnapshotType": "manual",
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parse_cluster():
    c = _parse_cluster(_cluster_dict())
    assert c.db_cluster_identifier == CLUSTER_ID
    assert c.status == "available"


def test_parse_instance():
    i = _parse_instance(_instance_dict())
    assert i.db_instance_identifier == INSTANCE_ID
    assert i.endpoint_address == "inst.example.com"


def test_parse_instance_no_endpoint():
    i = _parse_instance(_instance_dict(Endpoint=None))
    assert i.endpoint_address is None


def test_parse_snapshot():
    s = _parse_snapshot(_snapshot_dict())
    assert s.db_cluster_snapshot_identifier == SNAP_ID


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster.return_value = {"DBCluster": _cluster_dict()}
    result = create_db_cluster(CLUSTER_ID, region_name=REGION)
    assert result.db_cluster_identifier == CLUSTER_ID


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster_all_opts(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster.return_value = {"DBCluster": _cluster_dict()}
    result = create_db_cluster(
        CLUSTER_ID,
        engine_version="5.0.0",
        db_subnet_group_name="sg",
        vpc_security_group_ids=["sg-1"],
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.db_cluster_identifier == CLUSTER_ID


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster.side_effect = _client_error("DBClusterAlreadyExistsFault")
    with pytest.raises(RuntimeError):
        create_db_cluster(CLUSTER_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_clusters(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBClusters": [_cluster_dict()]},
    ]
    result = describe_db_clusters(
        db_cluster_identifier=CLUSTER_ID, region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.documentdb.get_client")
def test_describe_db_clusters_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error("DBClusterNotFoundFault")
    with pytest.raises(RuntimeError):
        describe_db_clusters(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_db_cluster(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_cluster.return_value = {"DBCluster": _cluster_dict()}
    result = modify_db_cluster(
        CLUSTER_ID,
        engine_version="5.1.0",
        master_user_password="newpw",
        region_name=REGION,
    )
    assert result.db_cluster_identifier == CLUSTER_ID


@patch("aws_util.documentdb.get_client")
def test_modify_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_cluster.side_effect = _client_error("InvalidDBClusterStateFault")
    with pytest.raises(RuntimeError):
        modify_db_cluster(CLUSTER_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_cluster.return_value = {}
    delete_db_cluster(CLUSTER_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster_with_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_cluster.return_value = {}
    delete_db_cluster(
        CLUSTER_ID,
        skip_final_snapshot=False,
        final_db_snapshot_identifier="final-snap",
        region_name=REGION,
    )


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_cluster.side_effect = _client_error("DBClusterNotFoundFault")
    with pytest.raises(RuntimeError):
        delete_db_cluster(CLUSTER_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_failover_db_cluster(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.failover_db_cluster.return_value = {"DBCluster": _cluster_dict()}
    result = failover_db_cluster(
        CLUSTER_ID, target_db_instance_identifier=INSTANCE_ID, region_name=REGION,
    )
    assert result.db_cluster_identifier == CLUSTER_ID


@patch("aws_util.documentdb.get_client")
def test_failover_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.failover_db_cluster.side_effect = _client_error("DBClusterNotFoundFault")
    with pytest.raises(RuntimeError):
        failover_db_cluster(CLUSTER_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Instance operations
# ---------------------------------------------------------------------------


@patch("aws_util.documentdb.get_client")
def test_create_db_instance(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_instance.return_value = {"DBInstance": _instance_dict()}
    result = create_db_instance(
        INSTANCE_ID,
        db_cluster_identifier=CLUSTER_ID,
        availability_zone="us-east-1a",
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.db_instance_identifier == INSTANCE_ID


@patch("aws_util.documentdb.get_client")
def test_create_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_instance.side_effect = _client_error("DBInstanceAlreadyExistsFault")
    with pytest.raises(RuntimeError):
        create_db_instance(INSTANCE_ID, db_cluster_identifier=CLUSTER_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_instances(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBInstances": [_instance_dict()]},
    ]
    result = describe_db_instances(
        db_instance_identifier=INSTANCE_ID, region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.documentdb.get_client")
def test_describe_db_instances_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error("DBInstanceNotFoundFault")
    with pytest.raises(RuntimeError):
        describe_db_instances(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_db_instance(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_instance.return_value = {"DBInstance": _instance_dict()}
    result = modify_db_instance(
        INSTANCE_ID, db_instance_class="db.r6g.large", region_name=REGION,
    )
    assert result.db_instance_identifier == INSTANCE_ID


@patch("aws_util.documentdb.get_client")
def test_modify_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_instance.side_effect = _client_error("InvalidDBInstanceStateFault")
    with pytest.raises(RuntimeError):
        modify_db_instance(INSTANCE_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_instance(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_instance.return_value = {}
    delete_db_instance(INSTANCE_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_instance.side_effect = _client_error("DBInstanceNotFoundFault")
    with pytest.raises(RuntimeError):
        delete_db_instance(INSTANCE_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_reboot_db_instance(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.reboot_db_instance.return_value = {"DBInstance": _instance_dict()}
    result = reboot_db_instance(INSTANCE_ID, force_failover=True, region_name=REGION)
    assert result.db_instance_identifier == INSTANCE_ID


@patch("aws_util.documentdb.get_client")
def test_reboot_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.reboot_db_instance.side_effect = _client_error("InvalidDBInstanceStateFault")
    with pytest.raises(RuntimeError):
        reboot_db_instance(INSTANCE_ID, region_name=REGION)


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster_snapshot.return_value = {
        "DBClusterSnapshot": _snapshot_dict(),
    }
    result = create_db_cluster_snapshot(
        SNAP_ID, db_cluster_identifier=CLUSTER_ID,
        tags={"env": "test"}, region_name=REGION,
    )
    assert result.db_cluster_snapshot_identifier == SNAP_ID


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster_snapshot.side_effect = _client_error(
        "DBClusterSnapshotAlreadyExistsFault",
    )
    with pytest.raises(RuntimeError):
        create_db_cluster_snapshot(
            SNAP_ID, db_cluster_identifier=CLUSTER_ID, region_name=REGION,
        )


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_snapshots(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBClusterSnapshots": [_snapshot_dict()]},
    ]
    result = describe_db_cluster_snapshots(
        db_cluster_snapshot_identifier=SNAP_ID,
        db_cluster_identifier=CLUSTER_ID,
        region_name=REGION,
    )
    assert len(result) == 1


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_snapshots_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = _client_error("DBClusterSnapshotNotFoundFault")
    with pytest.raises(RuntimeError):
        describe_db_cluster_snapshots(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_copy_db_cluster_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.copy_db_cluster_snapshot.return_value = {
        "DBClusterSnapshot": _snapshot_dict(
            DBClusterSnapshotIdentifier="copy-snap",
        ),
    }
    result = copy_db_cluster_snapshot(
        SNAP_ID, "copy-snap", tags={"env": "test"}, region_name=REGION,
    )
    assert result.db_cluster_snapshot_identifier == "copy-snap"


@patch("aws_util.documentdb.get_client")
def test_copy_db_cluster_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.copy_db_cluster_snapshot.side_effect = _client_error(
        "DBClusterSnapshotNotFoundFault",
    )
    with pytest.raises(RuntimeError):
        copy_db_cluster_snapshot(SNAP_ID, "copy", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_cluster_snapshot.return_value = {}
    delete_db_cluster_snapshot(SNAP_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_cluster_snapshot.side_effect = _client_error(
        "DBClusterSnapshotNotFoundFault",
    )
    with pytest.raises(RuntimeError):
        delete_db_cluster_snapshot(SNAP_ID, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_restore_db_cluster_from_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.restore_db_cluster_from_snapshot.return_value = {
        "DBCluster": _cluster_dict(DBClusterIdentifier="restored"),
    }
    result = restore_db_cluster_from_snapshot(
        "restored",
        snapshot_identifier=SNAP_ID,
        vpc_security_group_ids=["sg-1"],
        db_subnet_group_name="default",
        tags={"env": "test"},
        region_name=REGION,
    )
    assert result.db_cluster_identifier == "restored"


@patch("aws_util.documentdb.get_client")
def test_restore_db_cluster_from_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.restore_db_cluster_from_snapshot.side_effect = _client_error(
        "DBClusterSnapshotNotFoundFault",
    )
    with pytest.raises(RuntimeError):
        restore_db_cluster_from_snapshot(
            "restored", snapshot_identifier=SNAP_ID, region_name=REGION,
        )


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_cluster_ready(mock_gc, monkeypatch):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBClusters": [_cluster_dict(Status="available")]},
    ]
    result = wait_for_db_cluster(CLUSTER_ID, timeout=10, region_name=REGION)
    assert result.status == "available"


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_cluster_not_found(mock_gc, monkeypatch):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [{"DBClusters": []}]
    with pytest.raises(AwsServiceError):
        wait_for_db_cluster(CLUSTER_ID, timeout=10, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_cluster_timeout(mock_gc, monkeypatch):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBClusters": [_cluster_dict(Status="creating")]},
    ]
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_count = 0

    def _mono():
        nonlocal call_count
        call_count += 1
        return 0.0 if call_count <= 1 else 100.0

    monkeypatch.setattr(time, "monotonic", _mono)
    with pytest.raises(AwsTimeoutError):
        wait_for_db_cluster(
            CLUSTER_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_cluster_poll_then_ready(mock_gc, monkeypatch):
    """Cover the sleep branch: first poll creating, second available."""
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = [
        [{"DBClusters": [_cluster_dict(Status="creating")]}],
        [{"DBClusters": [_cluster_dict(Status="available")]}],
    ]
    monkeypatch.setattr(time, "sleep", lambda s: None)
    result = wait_for_db_cluster(
        CLUSTER_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert result.status == "available"


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_instance_ready(mock_gc, monkeypatch):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBInstances": [_instance_dict(DBInstanceStatus="available")]},
    ]
    result = wait_for_db_instance(INSTANCE_ID, timeout=10, region_name=REGION)
    assert result.status == "available"


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_instance_not_found(mock_gc, monkeypatch):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [{"DBInstances": []}]
    with pytest.raises(AwsServiceError):
        wait_for_db_instance(INSTANCE_ID, timeout=10, region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_instance_timeout(mock_gc, monkeypatch):
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.return_value = [
        {"DBInstances": [_instance_dict(DBInstanceStatus="creating")]},
    ]
    monkeypatch.setattr(time, "sleep", lambda s: None)
    call_count2 = 0

    def _mono2():
        nonlocal call_count2
        call_count2 += 1
        return 0.0 if call_count2 <= 1 else 100.0

    monkeypatch.setattr(time, "monotonic", _mono2)
    with pytest.raises(AwsTimeoutError):
        wait_for_db_instance(
            INSTANCE_ID, timeout=1, poll_interval=0.1, region_name=REGION,
        )


@patch("aws_util.documentdb.get_client")
def test_wait_for_db_instance_poll_then_ready(mock_gc, monkeypatch):
    """Cover the sleep branch: first poll creating, second available."""
    client = MagicMock()
    mock_gc.return_value = client
    paginator = MagicMock()
    client.get_paginator.return_value = paginator
    paginator.paginate.side_effect = [
        [{"DBInstances": [_instance_dict(DBInstanceStatus="creating")]}],
        [{"DBInstances": [_instance_dict(DBInstanceStatus="available")]}],
    ]
    monkeypatch.setattr(time, "sleep", lambda s: None)
    result = wait_for_db_instance(
        INSTANCE_ID, timeout=600, poll_interval=1.0, region_name=REGION,
    )
    assert result.status == "available"


@patch("aws_util.documentdb.get_client")
def test_add_source_identifier_to_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_source_identifier_to_subscription.return_value = {}
    add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)
    mock_client.add_source_identifier_to_subscription.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_add_source_identifier_to_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_source_identifier_to_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_source_identifier_to_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to add source identifier to subscription"):
        add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_add_tags_to_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_resource.return_value = {}
    add_tags_to_resource("test-resource_name", [], region_name=REGION)
    mock_client.add_tags_to_resource.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_add_tags_to_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to add tags to resource"):
        add_tags_to_resource("test-resource_name", [], region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_apply_pending_maintenance_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_pending_maintenance_action.return_value = {}
    apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", region_name=REGION)
    mock_client.apply_pending_maintenance_action.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_apply_pending_maintenance_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_pending_maintenance_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_pending_maintenance_action",
    )
    with pytest.raises(RuntimeError, match="Failed to apply pending maintenance action"):
        apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_copy_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_cluster_parameter_group.return_value = {}
    copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", region_name=REGION)
    mock_client.copy_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_copy_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to copy db cluster parameter group"):
        copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_cluster_parameter_group.return_value = {}
    create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)
    mock_client.create_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_create_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create db cluster parameter group"):
        create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_create_db_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_subnet_group.return_value = {}
    create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], region_name=REGION)
    mock_client.create_db_subnet_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_create_db_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create db subnet group"):
        create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_create_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_event_subscription.return_value = {}
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)
    mock_client.create_event_subscription.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_create_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to create event subscription"):
        create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_create_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_global_cluster.return_value = {}
    create_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.create_global_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_create_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to create global cluster"):
        create_global_cluster("test-global_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_parameter_group.return_value = {}
    delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.delete_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_delete_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db cluster parameter group"):
        delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_db_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_subnet_group.return_value = {}
    delete_db_subnet_group("test-db_subnet_group_name", region_name=REGION)
    mock_client.delete_db_subnet_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_delete_db_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db subnet group"):
        delete_db_subnet_group("test-db_subnet_group_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_event_subscription.return_value = {}
    delete_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.delete_event_subscription.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_delete_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to delete event subscription"):
        delete_event_subscription("test-subscription_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_delete_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_global_cluster.return_value = {}
    delete_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.delete_global_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_delete_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to delete global cluster"):
        delete_global_cluster("test-global_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_certificates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificates.return_value = {}
    describe_certificates(region_name=REGION)
    mock_client.describe_certificates.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_certificates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_certificates",
    )
    with pytest.raises(RuntimeError, match="Failed to describe certificates"):
        describe_certificates(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_parameter_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameter_groups.return_value = {}
    describe_db_cluster_parameter_groups(region_name=REGION)
    mock_client.describe_db_cluster_parameter_groups.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_parameter_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_parameter_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster parameter groups"):
        describe_db_cluster_parameter_groups(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameters.return_value = {}
    describe_db_cluster_parameters("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.describe_db_cluster_parameters.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster parameters"):
        describe_db_cluster_parameters("test-db_cluster_parameter_group_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_snapshot_attributes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_snapshot_attributes.return_value = {}
    describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.describe_db_cluster_snapshot_attributes.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_db_cluster_snapshot_attributes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_snapshot_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_snapshot_attributes",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster snapshot attributes"):
        describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_engine_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_engine_versions.return_value = {}
    describe_db_engine_versions(region_name=REGION)
    mock_client.describe_db_engine_versions.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_db_engine_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_engine_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db engine versions"):
        describe_db_engine_versions(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_db_subnet_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_subnet_groups.return_value = {}
    describe_db_subnet_groups(region_name=REGION)
    mock_client.describe_db_subnet_groups.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_db_subnet_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_subnet_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_subnet_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db subnet groups"):
        describe_db_subnet_groups(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_engine_default_cluster_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_default_cluster_parameters.return_value = {}
    describe_engine_default_cluster_parameters("test-db_parameter_group_family", region_name=REGION)
    mock_client.describe_engine_default_cluster_parameters.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_engine_default_cluster_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_default_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_default_cluster_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe engine default cluster parameters"):
        describe_engine_default_cluster_parameters("test-db_parameter_group_family", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_event_categories(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_categories.return_value = {}
    describe_event_categories(region_name=REGION)
    mock_client.describe_event_categories.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_event_categories_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_categories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_categories",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event categories"):
        describe_event_categories(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_event_subscriptions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_subscriptions.return_value = {}
    describe_event_subscriptions(region_name=REGION)
    mock_client.describe_event_subscriptions.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_event_subscriptions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_subscriptions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event subscriptions"):
        describe_event_subscriptions(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.return_value = {}
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_global_clusters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_global_clusters.return_value = {}
    describe_global_clusters(region_name=REGION)
    mock_client.describe_global_clusters.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_global_clusters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_global_clusters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_global_clusters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe global clusters"):
        describe_global_clusters(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_orderable_db_instance_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_orderable_db_instance_options.return_value = {}
    describe_orderable_db_instance_options("test-engine", region_name=REGION)
    mock_client.describe_orderable_db_instance_options.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_orderable_db_instance_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_orderable_db_instance_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_orderable_db_instance_options",
    )
    with pytest.raises(RuntimeError, match="Failed to describe orderable db instance options"):
        describe_orderable_db_instance_options("test-engine", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_describe_pending_maintenance_actions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pending_maintenance_actions.return_value = {}
    describe_pending_maintenance_actions(region_name=REGION)
    mock_client.describe_pending_maintenance_actions.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_describe_pending_maintenance_actions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pending_maintenance_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pending_maintenance_actions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe pending maintenance actions"):
        describe_pending_maintenance_actions(region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_failover_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.failover_global_cluster.return_value = {}
    failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)
    mock_client.failover_global_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_failover_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.failover_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to failover global cluster"):
        failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_name", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_parameter_group.return_value = {}
    modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], region_name=REGION)
    mock_client.modify_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_modify_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db cluster parameter group"):
        modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_db_cluster_snapshot_attribute(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_snapshot_attribute.return_value = {}
    modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", region_name=REGION)
    mock_client.modify_db_cluster_snapshot_attribute.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_modify_db_cluster_snapshot_attribute_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_snapshot_attribute",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db cluster snapshot attribute"):
        modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_db_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_subnet_group.return_value = {}
    modify_db_subnet_group("test-db_subnet_group_name", [], region_name=REGION)
    mock_client.modify_db_subnet_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_modify_db_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db subnet group"):
        modify_db_subnet_group("test-db_subnet_group_name", [], region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_event_subscription.return_value = {}
    modify_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.modify_event_subscription.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_modify_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to modify event subscription"):
        modify_event_subscription("test-subscription_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_modify_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_global_cluster.return_value = {}
    modify_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.modify_global_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_modify_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to modify global cluster"):
        modify_global_cluster("test-global_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_remove_from_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_from_global_cluster.return_value = {}
    remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", region_name=REGION)
    mock_client.remove_from_global_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_remove_from_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_from_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_from_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to remove from global cluster"):
        remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_remove_source_identifier_from_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_source_identifier_from_subscription.return_value = {}
    remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)
    mock_client.remove_source_identifier_from_subscription.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_remove_source_identifier_from_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_source_identifier_from_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_source_identifier_from_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to remove source identifier from subscription"):
        remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_remove_tags_from_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_resource.return_value = {}
    remove_tags_from_resource("test-resource_name", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_remove_tags_from_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_name", [], region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_reset_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_db_cluster_parameter_group.return_value = {}
    reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.reset_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_reset_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to reset db cluster parameter group"):
        reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_restore_db_cluster_to_point_in_time(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restore_db_cluster_to_point_in_time.return_value = {}
    restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", region_name=REGION)
    mock_client.restore_db_cluster_to_point_in_time.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_restore_db_cluster_to_point_in_time_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restore_db_cluster_to_point_in_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_cluster_to_point_in_time",
    )
    with pytest.raises(RuntimeError, match="Failed to restore db cluster to point in time"):
        restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_start_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_db_cluster.return_value = {}
    start_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.start_db_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_start_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to start db cluster"):
        start_db_cluster("test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_stop_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_db_cluster.return_value = {}
    stop_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.stop_db_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_stop_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to stop db cluster"):
        stop_db_cluster("test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.documentdb.get_client")
def test_switchover_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.switchover_global_cluster.return_value = {}
    switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)
    mock_client.switchover_global_cluster.assert_called_once()


@patch("aws_util.documentdb.get_client")
def test_switchover_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.switchover_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "switchover_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to switchover global cluster"):
        switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)


def test_delete_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import delete_db_cluster
    mock_client = MagicMock()
    mock_client.delete_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    delete_db_cluster("test-db_cluster_identifier", final_db_snapshot_identifier="test-final_db_snapshot_identifier", region_name="us-east-1")
    mock_client.delete_db_cluster.assert_called_once()

def test_copy_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import copy_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.copy_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_db_cluster_parameter_group.assert_called_once()

def test_create_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import create_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.create_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_cluster_parameter_group.assert_called_once()

def test_create_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import create_db_subnet_group
    mock_client = MagicMock()
    mock_client.create_db_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", "test-subnet_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_subnet_group.assert_called_once()

def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import create_event_subscription
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_subscription.assert_called_once()

def test_create_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import create_global_cluster
    mock_client = MagicMock()
    mock_client.create_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    create_global_cluster("test-global_cluster_identifier", source_db_cluster_identifier="test-source_db_cluster_identifier", engine="test-engine", engine_version="test-engine_version", deletion_protection="test-deletion_protection", database_name="test-database_name", storage_encrypted="test-storage_encrypted", region_name="us-east-1")
    mock_client.create_global_cluster.assert_called_once()

def test_describe_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_certificates
    mock_client = MagicMock()
    mock_client.describe_certificates.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_certificates(certificate_identifier="test-certificate_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_certificates.assert_called_once()

def test_describe_db_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_db_cluster_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameter_groups(db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_parameter_groups.assert_called_once()

def test_describe_db_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_db_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameters("test-db_cluster_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_parameters.assert_called_once()

def test_describe_db_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_db_engine_versions
    mock_client = MagicMock()
    mock_client.describe_db_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_db_engine_versions(engine="test-engine", engine_version="test-engine_version", db_parameter_group_family="test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", default_only="test-default_only", list_supported_character_sets=1, list_supported_timezones=1, region_name="us-east-1")
    mock_client.describe_db_engine_versions.assert_called_once()

def test_describe_db_subnet_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_db_subnet_groups
    mock_client = MagicMock()
    mock_client.describe_db_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_db_subnet_groups(db_subnet_group_name="test-db_subnet_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_subnet_groups.assert_called_once()

def test_describe_engine_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_engine_default_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_engine_default_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_cluster_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_default_cluster_parameters.assert_called_once()

def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_event_categories
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.describe_event_categories.assert_called_once()

def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_event_subscriptions
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_event_subscriptions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_global_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_global_clusters
    mock_client = MagicMock()
    mock_client.describe_global_clusters.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_global_clusters(global_cluster_identifier="test-global_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_global_clusters.assert_called_once()

def test_describe_orderable_db_instance_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_orderable_db_instance_options
    mock_client = MagicMock()
    mock_client.describe_orderable_db_instance_options.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_orderable_db_instance_options("test-engine", engine_version="test-engine_version", db_instance_class="test-db_instance_class", license_model="test-license_model", vpc="test-vpc", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_orderable_db_instance_options.assert_called_once()

def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import describe_pending_maintenance_actions
    mock_client = MagicMock()
    mock_client.describe_pending_maintenance_actions.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    describe_pending_maintenance_actions(resource_identifier="test-resource_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_pending_maintenance_actions.assert_called_once()

def test_failover_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import failover_global_cluster
    mock_client = MagicMock()
    mock_client.failover_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", allow_data_loss=True, switchover="test-switchover", region_name="us-east-1")
    mock_client.failover_global_cluster.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_name", filters=[{}], region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_modify_db_cluster_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import modify_db_cluster_snapshot_attribute
    mock_client = MagicMock()
    mock_client.modify_db_cluster_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.modify_db_cluster_snapshot_attribute.assert_called_once()

def test_modify_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import modify_db_subnet_group
    mock_client = MagicMock()
    mock_client.modify_db_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    modify_db_subnet_group("test-db_subnet_group_name", "test-subnet_ids", db_subnet_group_description="test-db_subnet_group_description", region_name="us-east-1")
    mock_client.modify_db_subnet_group.assert_called_once()

def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import modify_event_subscription
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.modify_event_subscription.assert_called_once()

def test_modify_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import modify_global_cluster
    mock_client = MagicMock()
    mock_client.modify_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    modify_global_cluster("test-global_cluster_identifier", new_global_cluster_identifier="test-new_global_cluster_identifier", deletion_protection="test-deletion_protection", region_name="us-east-1")
    mock_client.modify_global_cluster.assert_called_once()

def test_reset_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import reset_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.reset_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.reset_db_cluster_parameter_group.assert_called_once()

def test_restore_db_cluster_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.documentdb import restore_db_cluster_to_point_in_time
    mock_client = MagicMock()
    mock_client.restore_db_cluster_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.documentdb.get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", restore_type="test-restore_type", restore_to_time="test-restore_to_time", use_latest_restorable_time=True, port=1, db_subnet_group_name="test-db_subnet_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_cloudwatch_logs_exports=True, deletion_protection="test-deletion_protection", serverless_v2_scaling_configuration={}, storage_type="test-storage_type", network_type="test-network_type", region_name="us-east-1")
    mock_client.restore_db_cluster_to_point_in_time.assert_called_once()
