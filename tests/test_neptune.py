"""Tests for aws_util.neptune -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.exceptions import AwsServiceError, AwsTimeoutError
from aws_util.neptune import (
    NeptuneCluster,
    NeptuneClusterSnapshot,
    NeptuneInstance,
    _parse_cluster,
    _parse_cluster_snapshot,
    _parse_instance,
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

_ERR = ClientError({"Error": {"Code": "X", "Message": "fail"}}, "op")

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


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def test_neptune_cluster_minimal():
    m = NeptuneCluster(
        db_cluster_identifier="c1", status="available",
        engine="neptune", engine_version="1.0",
    )
    assert m.endpoint is None
    assert m.extra == {}


def test_neptune_cluster_full():
    m = NeptuneCluster(
        db_cluster_identifier="c1", status="available",
        engine="neptune", engine_version="1.0",
        endpoint="ep", reader_endpoint="rep", port=8182,
        multi_az=True, storage_encrypted=True, extra={"k": "v"},
    )
    assert m.multi_az is True


def test_neptune_instance_minimal():
    m = NeptuneInstance(
        db_instance_identifier="i1", db_instance_class="db.r5.large",
        engine="neptune", engine_version="1.0", status="available",
    )
    assert m.endpoint_address is None


def test_neptune_instance_full():
    m = NeptuneInstance(
        db_instance_identifier="i1", db_instance_class="db.r5.large",
        engine="neptune", engine_version="1.0", status="available",
        endpoint_address="addr", endpoint_port=8182,
        availability_zone="us-east-1a",
        db_cluster_identifier="c1", extra={"k": "v"},
    )
    assert m.availability_zone == "us-east-1a"


def test_neptune_cluster_snapshot_minimal():
    m = NeptuneClusterSnapshot(
        db_cluster_snapshot_identifier="s1",
        db_cluster_identifier="c1", status="available",
        engine="neptune", engine_version="1.0",
    )
    assert m.snapshot_type is None


def test_neptune_cluster_snapshot_full():
    m = NeptuneClusterSnapshot(
        db_cluster_snapshot_identifier="s1",
        db_cluster_identifier="c1", status="available",
        engine="neptune", engine_version="1.0",
        snapshot_type="manual", allocated_storage=10,
        extra={"k": "v"},
    )
    assert m.allocated_storage == 10


# ---------------------------------------------------------------------------
# _parse helpers
# ---------------------------------------------------------------------------


def test_parse_cluster():
    r = _parse_cluster(_CLUSTER_DATA)
    assert r.db_cluster_identifier == "my-cluster"
    assert r.multi_az is True


def test_parse_instance():
    r = _parse_instance(_INSTANCE_DATA)
    assert r.db_instance_identifier == "my-instance"
    assert r.endpoint_address == "inst.amazonaws.com"
    assert r.endpoint_port == 8182


def test_parse_instance_no_endpoint():
    data = {
        "DBInstanceIdentifier": "i1",
        "DBInstanceClass": "db.r5.large",
        "Engine": "neptune",
        "DBInstanceStatus": "available",
        "Endpoint": "not-a-dict",
    }
    r = _parse_instance(data)
    assert r.endpoint_address is None
    assert r.endpoint_port is None


def test_parse_cluster_snapshot():
    r = _parse_cluster_snapshot(_SNAPSHOT_DATA)
    assert r.db_cluster_snapshot_identifier == "my-snap"
    assert r.allocated_storage == 10


# ---------------------------------------------------------------------------
# create_db_cluster
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster.return_value = {"DBCluster": _CLUSTER_DATA}
    r = create_db_cluster("my-cluster")
    assert r.db_cluster_identifier == "my-cluster"


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_with_version(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster.return_value = {"DBCluster": _CLUSTER_DATA}
    r = create_db_cluster("my-cluster", engine_version="1.2.0.0")
    assert r.db_cluster_identifier == "my-cluster"


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_db_cluster failed"):
        create_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# describe_db_clusters
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_describe_db_clusters_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"DBClusters": [_CLUSTER_DATA]}]
    r = describe_db_clusters()
    assert len(r) == 1


@patch("aws_util.neptune.get_client")
def test_describe_db_clusters_with_id(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"DBClusters": [_CLUSTER_DATA]}]
    r = describe_db_clusters("my-cluster")
    assert len(r) == 1


@patch("aws_util.neptune.get_client")
def test_describe_db_clusters_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_db_clusters failed"):
        describe_db_clusters()


# ---------------------------------------------------------------------------
# modify_db_cluster
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_cluster.return_value = {"DBCluster": _CLUSTER_DATA}
    r = modify_db_cluster("my-cluster", BackupRetentionPeriod=7)
    assert r.db_cluster_identifier == "my-cluster"


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_cluster.side_effect = _ERR
    with pytest.raises(RuntimeError, match="modify_db_cluster failed"):
        modify_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# delete_db_cluster
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_db_cluster("my-cluster")
    client.delete_db_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_cluster.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_db_cluster failed"):
        delete_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# create_db_instance
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_create_db_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_instance.return_value = {"DBInstance": _INSTANCE_DATA}
    r = create_db_instance("my-instance", "db.r5.large")
    assert r.db_instance_identifier == "my-instance"


@patch("aws_util.neptune.get_client")
def test_create_db_instance_with_cluster(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_instance.return_value = {"DBInstance": _INSTANCE_DATA}
    r = create_db_instance(
        "my-instance", "db.r5.large",
        db_cluster_identifier="my-cluster",
    )
    assert r.db_instance_identifier == "my-instance"


@patch("aws_util.neptune.get_client")
def test_create_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_db_instance failed"):
        create_db_instance("my-instance", "db.r5.large")


# ---------------------------------------------------------------------------
# describe_db_instances
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_describe_db_instances_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"DBInstances": [_INSTANCE_DATA]}]
    r = describe_db_instances()
    assert len(r) == 1


@patch("aws_util.neptune.get_client")
def test_describe_db_instances_with_id(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [{"DBInstances": [_INSTANCE_DATA]}]
    r = describe_db_instances("my-instance")
    assert len(r) == 1


@patch("aws_util.neptune.get_client")
def test_describe_db_instances_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_db_instances failed"):
        describe_db_instances()


# ---------------------------------------------------------------------------
# modify_db_instance
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_modify_db_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_instance.return_value = {"DBInstance": _INSTANCE_DATA}
    r = modify_db_instance("my-instance")
    assert r.db_instance_identifier == "my-instance"


@patch("aws_util.neptune.get_client")
def test_modify_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.modify_db_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="modify_db_instance failed"):
        modify_db_instance("my-instance")


# ---------------------------------------------------------------------------
# delete_db_instance
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_delete_db_instance_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_db_instance("my-instance")


@patch("aws_util.neptune.get_client")
def test_delete_db_instance_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.delete_db_instance.side_effect = _ERR
    with pytest.raises(RuntimeError, match="delete_db_instance failed"):
        delete_db_instance("my-instance")


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_snapshot_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster_snapshot.return_value = {
        "DBClusterSnapshot": _SNAPSHOT_DATA,
    }
    r = create_db_cluster_snapshot("my-snap", "my-cluster")
    assert r.db_cluster_snapshot_identifier == "my-snap"


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_snapshot_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.create_db_cluster_snapshot.side_effect = _ERR
    with pytest.raises(RuntimeError, match="create_db_cluster_snapshot"):
        create_db_cluster_snapshot("my-snap", "my-cluster")


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_snapshots_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [
        {"DBClusterSnapshots": [_SNAPSHOT_DATA]},
    ]
    r = describe_db_cluster_snapshots()
    assert len(r) == 1


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_snapshots_with_id(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.return_value = [
        {"DBClusterSnapshots": [_SNAPSHOT_DATA]},
    ]
    r = describe_db_cluster_snapshots("my-cluster")
    assert len(r) == 1


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_snapshots_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    p = MagicMock()
    client.get_paginator.return_value = p
    p.paginate.side_effect = _ERR
    with pytest.raises(RuntimeError, match="describe_db_cluster_snapshots"):
        describe_db_cluster_snapshots()


# ---------------------------------------------------------------------------
# failover_db_cluster
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.get_client")
def test_failover_db_cluster_ok(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.failover_db_cluster.return_value = {"DBCluster": _CLUSTER_DATA}
    r = failover_db_cluster("my-cluster")
    assert r.db_cluster_identifier == "my-cluster"


@patch("aws_util.neptune.get_client")
def test_failover_db_cluster_with_target(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.failover_db_cluster.return_value = {"DBCluster": _CLUSTER_DATA}
    r = failover_db_cluster(
        "my-cluster", target_db_instance_identifier="my-instance",
    )
    assert r.db_cluster_identifier == "my-cluster"


@patch("aws_util.neptune.get_client")
def test_failover_db_cluster_error(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    client.failover_db_cluster.side_effect = _ERR
    with pytest.raises(RuntimeError, match="failover_db_cluster failed"):
        failover_db_cluster("my-cluster")


# ---------------------------------------------------------------------------
# wait_for_db_cluster
# ---------------------------------------------------------------------------


@patch("aws_util.neptune.describe_db_clusters")
def test_wait_for_db_cluster_ok(mock_desc):
    mock_desc.return_value = [
        NeptuneCluster(
            db_cluster_identifier="c1", status="available",
            engine="neptune", engine_version="1.0",
        ),
    ]
    r = wait_for_db_cluster("c1")
    assert r.status == "available"


@patch("aws_util.neptune._time")
@patch("aws_util.neptune.describe_db_clusters")
def test_wait_for_db_cluster_timeout(mock_desc, mock_time):
    mock_time.monotonic.return_value = 9999.0
    mock_time.sleep = MagicMock()
    mock_desc.return_value = [
        NeptuneCluster(
            db_cluster_identifier="c1", status="creating",
            engine="neptune", engine_version="1.0",
        ),
    ]
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        wait_for_db_cluster("c1", timeout=1.0)


@patch("aws_util.neptune._time")
@patch("aws_util.neptune.describe_db_clusters")
def test_wait_for_db_cluster_not_found(mock_desc, mock_time):
    mock_time.monotonic.return_value = 0.0
    mock_desc.return_value = []
    with pytest.raises(AwsServiceError, match="not found"):
        wait_for_db_cluster("c1")


REGION = "us-east-1"


@patch("aws_util.neptune.get_client")
def test_add_role_to_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_role_to_db_cluster.return_value = {}
    add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)
    mock_client.add_role_to_db_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_add_role_to_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_role_to_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_role_to_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to add role to db cluster"):
        add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_add_source_identifier_to_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_source_identifier_to_subscription.return_value = {}
    add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)
    mock_client.add_source_identifier_to_subscription.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_add_source_identifier_to_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_source_identifier_to_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_source_identifier_to_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to add source identifier to subscription"):
        add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_add_tags_to_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_resource.return_value = {}
    add_tags_to_resource("test-resource_name", [], region_name=REGION)
    mock_client.add_tags_to_resource.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_add_tags_to_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.add_tags_to_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to add tags to resource"):
        add_tags_to_resource("test-resource_name", [], region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_apply_pending_maintenance_action(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_pending_maintenance_action.return_value = {}
    apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", region_name=REGION)
    mock_client.apply_pending_maintenance_action.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_apply_pending_maintenance_action_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.apply_pending_maintenance_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_pending_maintenance_action",
    )
    with pytest.raises(RuntimeError, match="Failed to apply pending maintenance action"):
        apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_copy_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_cluster_parameter_group.return_value = {}
    copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", region_name=REGION)
    mock_client.copy_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_copy_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to copy db cluster parameter group"):
        copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_copy_db_cluster_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_cluster_snapshot.return_value = {}
    copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.copy_db_cluster_snapshot.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_copy_db_cluster_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_cluster_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to copy db cluster snapshot"):
        copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_copy_db_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_parameter_group.return_value = {}
    copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", region_name=REGION)
    mock_client.copy_db_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_copy_db_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.copy_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to copy db parameter group"):
        copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_cluster_endpoint.return_value = {}
    create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", region_name=REGION)
    mock_client.create_db_cluster_endpoint.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_cluster_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to create db cluster endpoint"):
        create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_cluster_parameter_group.return_value = {}
    create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)
    mock_client.create_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_create_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create db cluster parameter group"):
        create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_create_db_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_parameter_group.return_value = {}
    create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)
    mock_client.create_db_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_create_db_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create db parameter group"):
        create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_create_db_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_subnet_group.return_value = {}
    create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], region_name=REGION)
    mock_client.create_db_subnet_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_create_db_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create db subnet group"):
        create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_create_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_event_subscription.return_value = {}
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)
    mock_client.create_event_subscription.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_create_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to create event subscription"):
        create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_create_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_global_cluster.return_value = {}
    create_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.create_global_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_create_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to create global cluster"):
        create_global_cluster("test-global_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_endpoint.return_value = {}
    delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)
    mock_client.delete_db_cluster_endpoint.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db cluster endpoint"):
        delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_parameter_group.return_value = {}
    delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.delete_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db cluster parameter group"):
        delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_snapshot.return_value = {}
    delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.delete_db_cluster_snapshot.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_db_cluster_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db cluster snapshot"):
        delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_db_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_parameter_group.return_value = {}
    delete_db_parameter_group("test-db_parameter_group_name", region_name=REGION)
    mock_client.delete_db_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_db_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db parameter group"):
        delete_db_parameter_group("test-db_parameter_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_db_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_subnet_group.return_value = {}
    delete_db_subnet_group("test-db_subnet_group_name", region_name=REGION)
    mock_client.delete_db_subnet_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_db_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete db subnet group"):
        delete_db_subnet_group("test-db_subnet_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_event_subscription.return_value = {}
    delete_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.delete_event_subscription.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to delete event subscription"):
        delete_event_subscription("test-subscription_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_delete_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_global_cluster.return_value = {}
    delete_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.delete_global_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_delete_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to delete global cluster"):
        delete_global_cluster("test-global_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_endpoints(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_endpoints.return_value = {}
    describe_db_cluster_endpoints(region_name=REGION)
    mock_client.describe_db_cluster_endpoints.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_endpoints_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_endpoints",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster endpoints"):
        describe_db_cluster_endpoints(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_parameter_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameter_groups.return_value = {}
    describe_db_cluster_parameter_groups(region_name=REGION)
    mock_client.describe_db_cluster_parameter_groups.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_parameter_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_parameter_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster parameter groups"):
        describe_db_cluster_parameter_groups(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameters.return_value = {}
    describe_db_cluster_parameters("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.describe_db_cluster_parameters.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster parameters"):
        describe_db_cluster_parameters("test-db_cluster_parameter_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_snapshot_attributes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_snapshot_attributes.return_value = {}
    describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.describe_db_cluster_snapshot_attributes.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_cluster_snapshot_attributes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_cluster_snapshot_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_snapshot_attributes",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db cluster snapshot attributes"):
        describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_engine_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_engine_versions.return_value = {}
    describe_db_engine_versions(region_name=REGION)
    mock_client.describe_db_engine_versions.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_engine_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_engine_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db engine versions"):
        describe_db_engine_versions(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_parameter_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_parameter_groups.return_value = {}
    describe_db_parameter_groups(region_name=REGION)
    mock_client.describe_db_parameter_groups.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_parameter_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_parameter_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db parameter groups"):
        describe_db_parameter_groups(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_parameters.return_value = {}
    describe_db_parameters("test-db_parameter_group_name", region_name=REGION)
    mock_client.describe_db_parameters.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db parameters"):
        describe_db_parameters("test-db_parameter_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_db_subnet_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_subnet_groups.return_value = {}
    describe_db_subnet_groups(region_name=REGION)
    mock_client.describe_db_subnet_groups.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_db_subnet_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_db_subnet_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_subnet_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe db subnet groups"):
        describe_db_subnet_groups(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_engine_default_cluster_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_default_cluster_parameters.return_value = {}
    describe_engine_default_cluster_parameters("test-db_parameter_group_family", region_name=REGION)
    mock_client.describe_engine_default_cluster_parameters.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_engine_default_cluster_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_default_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_default_cluster_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe engine default cluster parameters"):
        describe_engine_default_cluster_parameters("test-db_parameter_group_family", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_engine_default_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_default_parameters.return_value = {}
    describe_engine_default_parameters("test-db_parameter_group_family", region_name=REGION)
    mock_client.describe_engine_default_parameters.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_engine_default_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_default_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_default_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe engine default parameters"):
        describe_engine_default_parameters("test-db_parameter_group_family", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_event_categories(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_categories.return_value = {}
    describe_event_categories(region_name=REGION)
    mock_client.describe_event_categories.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_event_categories_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_categories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_categories",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event categories"):
        describe_event_categories(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_event_subscriptions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_subscriptions.return_value = {}
    describe_event_subscriptions(region_name=REGION)
    mock_client.describe_event_subscriptions.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_event_subscriptions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_event_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_subscriptions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe event subscriptions"):
        describe_event_subscriptions(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.return_value = {}
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_global_clusters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_global_clusters.return_value = {}
    describe_global_clusters(region_name=REGION)
    mock_client.describe_global_clusters.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_global_clusters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_global_clusters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_global_clusters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe global clusters"):
        describe_global_clusters(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_orderable_db_instance_options(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_orderable_db_instance_options.return_value = {}
    describe_orderable_db_instance_options("test-engine", region_name=REGION)
    mock_client.describe_orderable_db_instance_options.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_orderable_db_instance_options_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_orderable_db_instance_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_orderable_db_instance_options",
    )
    with pytest.raises(RuntimeError, match="Failed to describe orderable db instance options"):
        describe_orderable_db_instance_options("test-engine", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_pending_maintenance_actions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pending_maintenance_actions.return_value = {}
    describe_pending_maintenance_actions(region_name=REGION)
    mock_client.describe_pending_maintenance_actions.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_pending_maintenance_actions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_pending_maintenance_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pending_maintenance_actions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe pending maintenance actions"):
        describe_pending_maintenance_actions(region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_describe_valid_db_instance_modifications(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_valid_db_instance_modifications.return_value = {}
    describe_valid_db_instance_modifications("test-db_instance_identifier", region_name=REGION)
    mock_client.describe_valid_db_instance_modifications.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_describe_valid_db_instance_modifications_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_valid_db_instance_modifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_valid_db_instance_modifications",
    )
    with pytest.raises(RuntimeError, match="Failed to describe valid db instance modifications"):
        describe_valid_db_instance_modifications("test-db_instance_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_failover_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.failover_global_cluster.return_value = {}
    failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)
    mock_client.failover_global_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_failover_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.failover_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to failover global cluster"):
        failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_list_tags_for_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.return_value = {}
    list_tags_for_resource("test-resource_name", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_list_tags_for_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_endpoint(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_endpoint.return_value = {}
    modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)
    mock_client.modify_db_cluster_endpoint.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_endpoint_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_endpoint",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db cluster endpoint"):
        modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_parameter_group.return_value = {}
    modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], region_name=REGION)
    mock_client.modify_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db cluster parameter group"):
        modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_snapshot_attribute(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_snapshot_attribute.return_value = {}
    modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", region_name=REGION)
    mock_client.modify_db_cluster_snapshot_attribute.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_db_cluster_snapshot_attribute_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_cluster_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_snapshot_attribute",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db cluster snapshot attribute"):
        modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_db_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_parameter_group.return_value = {}
    modify_db_parameter_group("test-db_parameter_group_name", [], region_name=REGION)
    mock_client.modify_db_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_db_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db parameter group"):
        modify_db_parameter_group("test-db_parameter_group_name", [], region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_db_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_subnet_group.return_value = {}
    modify_db_subnet_group("test-db_subnet_group_name", [], region_name=REGION)
    mock_client.modify_db_subnet_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_db_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to modify db subnet group"):
        modify_db_subnet_group("test-db_subnet_group_name", [], region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_event_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_event_subscription.return_value = {}
    modify_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.modify_event_subscription.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_event_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_event_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to modify event subscription"):
        modify_event_subscription("test-subscription_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_modify_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_global_cluster.return_value = {}
    modify_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.modify_global_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_modify_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.modify_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to modify global cluster"):
        modify_global_cluster("test-global_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_promote_read_replica_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.promote_read_replica_db_cluster.return_value = {}
    promote_read_replica_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.promote_read_replica_db_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_promote_read_replica_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.promote_read_replica_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "promote_read_replica_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to promote read replica db cluster"):
        promote_read_replica_db_cluster("test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_reboot_db_instance(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reboot_db_instance.return_value = {}
    reboot_db_instance("test-db_instance_identifier", region_name=REGION)
    mock_client.reboot_db_instance.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_reboot_db_instance_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reboot_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_db_instance",
    )
    with pytest.raises(RuntimeError, match="Failed to reboot db instance"):
        reboot_db_instance("test-db_instance_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_remove_from_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_from_global_cluster.return_value = {}
    remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", region_name=REGION)
    mock_client.remove_from_global_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_remove_from_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_from_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_from_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to remove from global cluster"):
        remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_remove_role_from_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_role_from_db_cluster.return_value = {}
    remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)
    mock_client.remove_role_from_db_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_remove_role_from_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_role_from_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_role_from_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to remove role from db cluster"):
        remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_remove_source_identifier_from_subscription(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_source_identifier_from_subscription.return_value = {}
    remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)
    mock_client.remove_source_identifier_from_subscription.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_remove_source_identifier_from_subscription_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_source_identifier_from_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_source_identifier_from_subscription",
    )
    with pytest.raises(RuntimeError, match="Failed to remove source identifier from subscription"):
        remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_remove_tags_from_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_resource.return_value = {}
    remove_tags_from_resource("test-resource_name", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_remove_tags_from_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_name", [], region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_reset_db_cluster_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_db_cluster_parameter_group.return_value = {}
    reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.reset_db_cluster_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_reset_db_cluster_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_db_cluster_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to reset db cluster parameter group"):
        reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_reset_db_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_db_parameter_group.return_value = {}
    reset_db_parameter_group("test-db_parameter_group_name", region_name=REGION)
    mock_client.reset_db_parameter_group.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_reset_db_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_db_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to reset db parameter group"):
        reset_db_parameter_group("test-db_parameter_group_name", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_restore_db_cluster_from_snapshot(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restore_db_cluster_from_snapshot.return_value = {}
    restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", region_name=REGION)
    mock_client.restore_db_cluster_from_snapshot.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_restore_db_cluster_from_snapshot_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restore_db_cluster_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_cluster_from_snapshot",
    )
    with pytest.raises(RuntimeError, match="Failed to restore db cluster from snapshot"):
        restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_restore_db_cluster_to_point_in_time(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restore_db_cluster_to_point_in_time.return_value = {}
    restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", region_name=REGION)
    mock_client.restore_db_cluster_to_point_in_time.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_restore_db_cluster_to_point_in_time_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.restore_db_cluster_to_point_in_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_cluster_to_point_in_time",
    )
    with pytest.raises(RuntimeError, match="Failed to restore db cluster to point in time"):
        restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_start_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_db_cluster.return_value = {}
    start_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.start_db_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_start_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.start_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to start db cluster"):
        start_db_cluster("test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_stop_db_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_db_cluster.return_value = {}
    stop_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.stop_db_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_stop_db_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.stop_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_db_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to stop db cluster"):
        stop_db_cluster("test-db_cluster_identifier", region_name=REGION)


@patch("aws_util.neptune.get_client")
def test_switchover_global_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.switchover_global_cluster.return_value = {}
    switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)
    mock_client.switchover_global_cluster.assert_called_once()


@patch("aws_util.neptune.get_client")
def test_switchover_global_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.switchover_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "switchover_global_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to switchover global cluster"):
        switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)


def test_create_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_db_cluster
    mock_client = MagicMock()
    mock_client.create_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_db_cluster("test-db_cluster_identifier", engine_version="test-engine_version", region_name="us-east-1")
    mock_client.create_db_cluster.assert_called_once()

def test_describe_db_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_clusters
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_clusters(db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.get_paginator.assert_called_once()

def test_create_db_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_db_instance
    mock_client = MagicMock()
    mock_client.create_db_instance.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_db_instance("test-db_instance_identifier", "test-db_instance_class", db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.create_db_instance.assert_called_once()

def test_describe_db_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_instances
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_instances(db_instance_identifier="test-db_instance_identifier", region_name="us-east-1")
    mock_client.get_paginator.assert_called_once()

def test_describe_db_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_cluster_snapshots
    mock_client = MagicMock()
    mock_client.get_paginator.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_snapshots(db_cluster_identifier="test-db_cluster_identifier", region_name="us-east-1")
    mock_client.get_paginator.assert_called_once()

def test_failover_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import failover_db_cluster
    mock_client = MagicMock()
    mock_client.failover_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    failover_db_cluster("test-db_cluster_identifier", target_db_instance_identifier="test-target_db_instance_identifier", region_name="us-east-1")
    mock_client.failover_db_cluster.assert_called_once()

def test_add_role_to_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import add_role_to_db_cluster
    mock_client = MagicMock()
    mock_client.add_role_to_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.add_role_to_db_cluster.assert_called_once()

def test_copy_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import copy_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.copy_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_db_cluster_parameter_group.assert_called_once()

def test_copy_db_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import copy_db_cluster_snapshot
    mock_client = MagicMock()
    mock_client.copy_db_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", copy_tags=[{"Key": "k", "Value": "v"}], tags=[{"Key": "k", "Value": "v"}], source_region="test-source_region", region_name="us-east-1")
    mock_client.copy_db_cluster_snapshot.assert_called_once()

def test_copy_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import copy_db_parameter_group
    mock_client = MagicMock()
    mock_client.copy_db_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_db_parameter_group.assert_called_once()

def test_create_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_db_cluster_endpoint
    mock_client = MagicMock()
    mock_client.create_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_cluster_endpoint.assert_called_once()

def test_create_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.create_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_cluster_parameter_group.assert_called_once()

def test_create_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_db_parameter_group
    mock_client = MagicMock()
    mock_client.create_db_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_parameter_group.assert_called_once()

def test_create_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_db_subnet_group
    mock_client = MagicMock()
    mock_client.create_db_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", "test-subnet_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_subnet_group.assert_called_once()

def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_event_subscription
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_subscription.assert_called_once()

def test_create_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import create_global_cluster
    mock_client = MagicMock()
    mock_client.create_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    create_global_cluster("test-global_cluster_identifier", source_db_cluster_identifier="test-source_db_cluster_identifier", engine="test-engine", engine_version="test-engine_version", deletion_protection="test-deletion_protection", storage_encrypted="test-storage_encrypted", region_name="us-east-1")
    mock_client.create_global_cluster.assert_called_once()

def test_describe_db_cluster_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_cluster_endpoints
    mock_client = MagicMock()
    mock_client.describe_db_cluster_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_endpoints(db_cluster_identifier="test-db_cluster_identifier", db_cluster_endpoint_identifier="test-db_cluster_endpoint_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_endpoints.assert_called_once()

def test_describe_db_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_cluster_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameter_groups(db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_parameter_groups.assert_called_once()

def test_describe_db_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameters("test-db_cluster_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_parameters.assert_called_once()

def test_describe_db_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_engine_versions
    mock_client = MagicMock()
    mock_client.describe_db_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_engine_versions(engine="test-engine", engine_version="test-engine_version", db_parameter_group_family="test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", default_only="test-default_only", list_supported_character_sets=1, list_supported_timezones=1, region_name="us-east-1")
    mock_client.describe_db_engine_versions.assert_called_once()

def test_describe_db_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_db_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_parameter_groups(db_parameter_group_name="test-db_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_parameter_groups.assert_called_once()

def test_describe_db_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_parameters
    mock_client = MagicMock()
    mock_client.describe_db_parameters.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_parameters("test-db_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_parameters.assert_called_once()

def test_describe_db_subnet_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_db_subnet_groups
    mock_client = MagicMock()
    mock_client.describe_db_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_db_subnet_groups(db_subnet_group_name="test-db_subnet_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_subnet_groups.assert_called_once()

def test_describe_engine_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_engine_default_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_engine_default_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_cluster_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_default_cluster_parameters.assert_called_once()

def test_describe_engine_default_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_engine_default_parameters
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_default_parameters.assert_called_once()

def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_event_categories
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.describe_event_categories.assert_called_once()

def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_event_subscriptions
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_event_subscriptions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_global_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_global_clusters
    mock_client = MagicMock()
    mock_client.describe_global_clusters.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_global_clusters(global_cluster_identifier="test-global_cluster_identifier", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_global_clusters.assert_called_once()

def test_describe_orderable_db_instance_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_orderable_db_instance_options
    mock_client = MagicMock()
    mock_client.describe_orderable_db_instance_options.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_orderable_db_instance_options("test-engine", engine_version="test-engine_version", db_instance_class="test-db_instance_class", license_model="test-license_model", vpc="test-vpc", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_orderable_db_instance_options.assert_called_once()

def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import describe_pending_maintenance_actions
    mock_client = MagicMock()
    mock_client.describe_pending_maintenance_actions.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    describe_pending_maintenance_actions(resource_identifier="test-resource_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_pending_maintenance_actions.assert_called_once()

def test_failover_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import failover_global_cluster
    mock_client = MagicMock()
    mock_client.failover_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", allow_data_loss=True, switchover="test-switchover", region_name="us-east-1")
    mock_client.failover_global_cluster.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_name", filters=[{}], region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_modify_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import modify_db_cluster_endpoint
    mock_client = MagicMock()
    mock_client.modify_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", endpoint_type="test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", region_name="us-east-1")
    mock_client.modify_db_cluster_endpoint.assert_called_once()

def test_modify_db_cluster_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import modify_db_cluster_snapshot_attribute
    mock_client = MagicMock()
    mock_client.modify_db_cluster_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.modify_db_cluster_snapshot_attribute.assert_called_once()

def test_modify_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import modify_db_subnet_group
    mock_client = MagicMock()
    mock_client.modify_db_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    modify_db_subnet_group("test-db_subnet_group_name", "test-subnet_ids", db_subnet_group_description="test-db_subnet_group_description", region_name="us-east-1")
    mock_client.modify_db_subnet_group.assert_called_once()

def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import modify_event_subscription
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.modify_event_subscription.assert_called_once()

def test_modify_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import modify_global_cluster
    mock_client = MagicMock()
    mock_client.modify_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    modify_global_cluster("test-global_cluster_identifier", new_global_cluster_identifier="test-new_global_cluster_identifier", deletion_protection="test-deletion_protection", engine_version="test-engine_version", allow_major_version_upgrade=True, region_name="us-east-1")
    mock_client.modify_global_cluster.assert_called_once()

def test_reboot_db_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import reboot_db_instance
    mock_client = MagicMock()
    mock_client.reboot_db_instance.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    reboot_db_instance("test-db_instance_identifier", force_failover=True, region_name="us-east-1")
    mock_client.reboot_db_instance.assert_called_once()

def test_remove_role_from_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import remove_role_from_db_cluster
    mock_client = MagicMock()
    mock_client.remove_role_from_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.remove_role_from_db_cluster.assert_called_once()

def test_reset_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import reset_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.reset_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.reset_db_cluster_parameter_group.assert_called_once()

def test_reset_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import reset_db_parameter_group
    mock_client = MagicMock()
    mock_client.reset_db_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    reset_db_parameter_group("test-db_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.reset_db_parameter_group.assert_called_once()

def test_restore_db_cluster_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import restore_db_cluster_from_snapshot
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", availability_zones="test-availability_zones", engine_version="test-engine_version", port=1, db_subnet_group_name="test-db_subnet_group_name", database_name="test-database_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], serverless_v2_scaling_configuration={}, storage_type="test-storage_type", region_name="us-east-1")
    mock_client.restore_db_cluster_from_snapshot.assert_called_once()

def test_restore_db_cluster_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.neptune import restore_db_cluster_to_point_in_time
    mock_client = MagicMock()
    mock_client.restore_db_cluster_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.neptune.get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_to_point_in_time("test-db_cluster_identifier", "test-source_db_cluster_identifier", restore_type="test-restore_type", restore_to_time="test-restore_to_time", use_latest_restorable_time=True, port=1, db_subnet_group_name="test-db_subnet_group_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", serverless_v2_scaling_configuration={}, storage_type="test-storage_type", region_name="us-east-1")
    mock_client.restore_db_cluster_to_point_in_time.assert_called_once()
