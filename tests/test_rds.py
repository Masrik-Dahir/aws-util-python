"""Tests for aws_util.rds."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.rds as rds_mod
from aws_util.rds import (
    RDSInstance,
    RDSSnapshot,
    describe_db_instances,
    get_db_instance,
    start_db_instance,
    stop_db_instance,
    create_db_snapshot,
    delete_db_snapshot,
    describe_db_snapshots,
    wait_for_db_instance,
    wait_for_snapshot,
    restore_db_from_snapshot,
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

REGION = "us-east-1"

DB_INSTANCE_ID = "test-db"
DB_INSTANCE_CLASS = "db.t3.micro"
DB_ENGINE = "mysql"
DB_ENGINE_VERSION = "8.0.28"
SNAPSHOT_ID = "test-snap"


def _create_db_instance(client, db_id: str = DB_INSTANCE_ID) -> None:
    client.create_db_instance(
        DBInstanceIdentifier=db_id,
        DBInstanceClass=DB_INSTANCE_CLASS,
        Engine=DB_ENGINE,
        EngineVersion=DB_ENGINE_VERSION,
        MasterUsername="admin",
        MasterUserPassword="password1",
        AllocatedStorage=20,
    )


# ---------------------------------------------------------------------------
# RDSInstance model
# ---------------------------------------------------------------------------

class TestRDSInstanceModel:
    def test_basic_fields(self):
        inst = RDSInstance(
            db_instance_id="db-1",
            db_instance_class="db.t3.micro",
            engine="mysql",
            engine_version="8.0",
            status="available",
        )
        assert inst.db_instance_id == "db-1"
        assert inst.multi_az is False
        assert inst.tags == {}

    def test_with_tags(self):
        inst = RDSInstance(
            db_instance_id="db-1",
            db_instance_class="db.t3.micro",
            engine="mysql",
            engine_version="8.0",
            status="available",
            tags={"env": "prod"},
        )
        assert inst.tags["env"] == "prod"

    def test_frozen(self):
        inst = RDSInstance(
            db_instance_id="db-1",
            db_instance_class="db.t3.micro",
            engine="mysql",
            engine_version="8.0",
            status="available",
        )
        with pytest.raises(Exception):
            inst.status = "stopped"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# RDSSnapshot model
# ---------------------------------------------------------------------------

class TestRDSSnapshotModel:
    def test_basic_fields(self):
        snap = RDSSnapshot(
            snapshot_id="snap-1",
            db_instance_id="db-1",
            status="available",
            snapshot_type="manual",
            engine="mysql",
        )
        assert snap.snapshot_id == "snap-1"
        assert snap.allocated_storage is None


# ---------------------------------------------------------------------------
# describe_db_instances
# ---------------------------------------------------------------------------

class TestDescribeDbInstances:
    def test_returns_all_instances(self, rds_client):
        _create_db_instance(rds_client)
        result = describe_db_instances()
        assert any(i.db_instance_id == DB_INSTANCE_ID for i in result)

    def test_returns_specific_instance(self, rds_client):
        _create_db_instance(rds_client)
        result = describe_db_instances([DB_INSTANCE_ID])
        assert len(result) == 1
        assert result[0].db_instance_id == DB_INSTANCE_ID
        assert result[0].engine == DB_ENGINE

    def test_empty_when_no_instances(self, rds_client):
        result = describe_db_instances()
        assert result == []

    def test_with_filters(self, rds_client):
        _create_db_instance(rds_client)
        result = describe_db_instances(filters=[{"Name": "engine", "Values": ["mysql"]}])
        assert any(i.engine == "mysql" for i in result)

    def test_client_error_raises_runtime_error(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeDBInstances",
        )
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="describe_db_instances failed"):
            describe_db_instances()


# ---------------------------------------------------------------------------
# get_db_instance
# ---------------------------------------------------------------------------

class TestGetDbInstance:
    def test_returns_instance(self, rds_client):
        _create_db_instance(rds_client)
        inst = get_db_instance(DB_INSTANCE_ID)
        assert inst is not None
        assert inst.db_instance_id == DB_INSTANCE_ID

    def test_returns_none_for_unknown(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"DBInstances": []}]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        result = get_db_instance("nonexistent")
        assert result is None


# ---------------------------------------------------------------------------
# start_db_instance
# ---------------------------------------------------------------------------

class TestStartDbInstance:
    def test_start_client_error_raises_runtime_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.start_db_instance.side_effect = ClientError(
            {"Error": {"Code": "InvalidDBInstanceState", "Message": "not stopped"}},
            "StartDBInstance",
        )
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to start RDS instance"):
            start_db_instance("my-db")

    def test_start_calls_boto3(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.start_db_instance.return_value = {}
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        start_db_instance("my-db")
        mock_client.start_db_instance.assert_called_once_with(DBInstanceIdentifier="my-db")


# ---------------------------------------------------------------------------
# stop_db_instance
# ---------------------------------------------------------------------------

class TestStopDbInstance:
    def test_stop_client_error_raises_runtime_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.stop_db_instance.side_effect = ClientError(
            {"Error": {"Code": "InvalidDBInstanceState", "Message": "not running"}},
            "StopDBInstance",
        )
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to stop RDS instance"):
            stop_db_instance("my-db")

    def test_stop_calls_boto3(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.stop_db_instance.return_value = {}
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        stop_db_instance("my-db")
        mock_client.stop_db_instance.assert_called_once_with(DBInstanceIdentifier="my-db")


# ---------------------------------------------------------------------------
# create_db_snapshot
# ---------------------------------------------------------------------------

class TestCreateDbSnapshot:
    def test_creates_snapshot(self, rds_client):
        _create_db_instance(rds_client)
        snap = create_db_snapshot(DB_INSTANCE_ID, SNAPSHOT_ID)
        assert snap.snapshot_id == SNAPSHOT_ID
        assert snap.db_instance_id == DB_INSTANCE_ID
        assert snap.engine == DB_ENGINE

    def test_client_error_raises_runtime_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_db_snapshot.side_effect = ClientError(
            {"Error": {"Code": "DBInstanceNotFound", "Message": "not found"}},
            "CreateDBSnapshot",
        )
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to create snapshot"):
            create_db_snapshot("nonexistent", "snap-x")


# ---------------------------------------------------------------------------
# delete_db_snapshot
# ---------------------------------------------------------------------------

class TestDeleteDbSnapshot:
    def test_deletes_snapshot(self, rds_client):
        _create_db_instance(rds_client)
        create_db_snapshot(DB_INSTANCE_ID, SNAPSHOT_ID)
        # Should not raise
        delete_db_snapshot(SNAPSHOT_ID)

    def test_client_error_raises_runtime_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_db_snapshot.side_effect = ClientError(
            {"Error": {"Code": "DBSnapshotNotFound", "Message": "not found"}},
            "DeleteDBSnapshot",
        )
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
            delete_db_snapshot("ghost-snap")


# ---------------------------------------------------------------------------
# describe_db_snapshots
# ---------------------------------------------------------------------------

class TestDescribeDbSnapshots:
    def test_returns_snapshots(self, rds_client):
        _create_db_instance(rds_client)
        create_db_snapshot(DB_INSTANCE_ID, SNAPSHOT_ID)
        snaps = describe_db_snapshots(DB_INSTANCE_ID)
        assert any(s.snapshot_id == SNAPSHOT_ID for s in snaps)

    def test_empty_when_no_snapshots(self, rds_client):
        snaps = describe_db_snapshots()
        assert snaps == []

    def test_client_error_raises_runtime_error(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeDBSnapshots",
        )
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="describe_db_snapshots failed"):
            describe_db_snapshots()


# ---------------------------------------------------------------------------
# wait_for_db_instance
# ---------------------------------------------------------------------------

class TestWaitForDbInstance:
    def test_returns_immediately_when_status_matches(self, monkeypatch):
        mock_instance = RDSInstance(
            db_instance_id="db-1",
            db_instance_class="db.t3.micro",
            engine="mysql",
            engine_version="8.0",
            status="available",
        )
        monkeypatch.setattr(rds_mod, "get_db_instance", lambda *a, **kw: mock_instance)

        result = wait_for_db_instance("db-1", target_status="available", timeout=5.0)
        assert result.status == "available"

    def test_raises_runtime_error_when_not_found(self, monkeypatch):
        monkeypatch.setattr(rds_mod, "get_db_instance", lambda *a, **kw: None)

        with pytest.raises(RuntimeError, match="not found"):
            wait_for_db_instance("ghost", timeout=1.0)

    def test_raises_timeout_error(self, monkeypatch):
        mock_instance = RDSInstance(
            db_instance_id="db-1",
            db_instance_class="db.t3.micro",
            engine="mysql",
            engine_version="8.0",
            status="creating",
        )
        monkeypatch.setattr(rds_mod, "get_db_instance", lambda *a, **kw: mock_instance)
        import time
        monkeypatch.setattr(time, "sleep", lambda s: None)

        with pytest.raises(TimeoutError):
            wait_for_db_instance("db-1", target_status="available", timeout=0.0, poll_interval=0.0)


# ---------------------------------------------------------------------------
# wait_for_snapshot
# ---------------------------------------------------------------------------

class TestWaitForSnapshot:
    def test_returns_when_status_matches(self, monkeypatch):
        snap_data = {
            "DBSnapshots": [
                {
                    "DBSnapshotIdentifier": SNAPSHOT_ID,
                    "DBInstanceIdentifier": DB_INSTANCE_ID,
                    "Status": "available",
                    "SnapshotType": "manual",
                    "Engine": "mysql",
                    "AllocatedStorage": 20,
                }
            ]
        }
        mock_client = MagicMock()
        mock_client.describe_db_snapshots.return_value = snap_data
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        result = wait_for_snapshot(SNAPSHOT_ID, target_status="available", timeout=5.0)
        assert result.snapshot_id == SNAPSHOT_ID

    def test_raises_runtime_error_for_empty_snapshots(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_db_snapshots.return_value = {"DBSnapshots": []}
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="not found"):
            wait_for_snapshot("ghost-snap", timeout=1.0)

    def test_raises_timeout_error(self, monkeypatch):
        snap_data = {
            "DBSnapshots": [
                {
                    "DBSnapshotIdentifier": SNAPSHOT_ID,
                    "DBInstanceIdentifier": DB_INSTANCE_ID,
                    "Status": "creating",
                    "SnapshotType": "manual",
                    "Engine": "mysql",
                }
            ]
        }
        mock_client = MagicMock()
        mock_client.describe_db_snapshots.return_value = snap_data
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(TimeoutError):
            wait_for_snapshot(SNAPSHOT_ID, target_status="available", timeout=0.0, poll_interval=0.0)

    def test_client_error_raises_runtime_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_db_snapshots.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeDBSnapshots",
        )
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="describe snapshot"):
            wait_for_snapshot(SNAPSHOT_ID, timeout=1.0)


# ---------------------------------------------------------------------------
# restore_db_from_snapshot
# ---------------------------------------------------------------------------

class TestRestoreDbFromSnapshot:
    def test_restore_returns_rds_instance(self, rds_client):
        _create_db_instance(rds_client)
        create_db_snapshot(DB_INSTANCE_ID, SNAPSHOT_ID)
        restored = restore_db_from_snapshot(
            SNAPSHOT_ID, "restored-db", DB_INSTANCE_CLASS
        )
        assert restored.db_instance_id == "restored-db"
        assert restored.engine == DB_ENGINE

    def test_client_error_raises_runtime_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.restore_db_instance_from_db_snapshot.side_effect = ClientError(
            {"Error": {"Code": "DBSnapshotNotFound", "Message": "not found"}},
            "RestoreDBInstanceFromDBSnapshot",
        )
        monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="restore_db_from_snapshot failed"):
            restore_db_from_snapshot("ghost-snap", "new-db", "db.t3.micro")


def test_wait_for_db_instance_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_db_instance (line 317)."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
    import aws_util.rds as rds_mod
    from aws_util.rds import RDSInstance, wait_for_db_instance

    call_count = {"n": 0}

    def fake_get(db_id, region_name=None):
        call_count["n"] += 1
        status = "creating" if call_count["n"] < 2 else "available"
        return RDSInstance(db_instance_id=db_id, db_instance_class="db.t3.micro",
                           engine="mysql", engine_version="8.0", status=status)

    monkeypatch.setattr(rds_mod, "get_db_instance", fake_get)
    result = wait_for_db_instance("db-1", target_status="available", timeout=10.0,
                                  poll_interval=0.001, region_name="us-east-1")
    assert result.status == "available"


def test_wait_for_snapshot_sleep_branch(monkeypatch):
    """Covers time.sleep in wait_for_snapshot (line 370)."""
    import time
    from unittest.mock import MagicMock
    monkeypatch.setattr(time, "sleep", lambda s: None)
    import aws_util.rds as rds_mod
    from aws_util.rds import wait_for_snapshot

    call_count = {"n": 0}
    mock_client = MagicMock()

    def fake_describe_db_snapshots(DBSnapshotIdentifier):
        call_count["n"] += 1
        status = "creating" if call_count["n"] < 2 else "available"
        return {
            "DBSnapshots": [{
                "DBSnapshotIdentifier": DBSnapshotIdentifier,
                "DBInstanceIdentifier": "db-1",
                "Status": status,
                "SnapshotType": "manual",
                "Engine": "mysql",
            }]
        }

    mock_client.describe_db_snapshots.side_effect = fake_describe_db_snapshots
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    result = wait_for_snapshot("snap-1", target_status="available", timeout=10.0,
                               poll_interval=0.001, region_name="us-east-1")
    assert result.status == "available"


def test_add_role_to_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_role_to_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)
    mock_client.add_role_to_db_cluster.assert_called_once()


def test_add_role_to_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_role_to_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_role_to_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add role to db cluster"):
        add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)


def test_add_role_to_db_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_role_to_db_instance.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    add_role_to_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", region_name=REGION)
    mock_client.add_role_to_db_instance.assert_called_once()


def test_add_role_to_db_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_role_to_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_role_to_db_instance",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add role to db instance"):
        add_role_to_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", region_name=REGION)


def test_add_source_identifier_to_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_source_identifier_to_subscription.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)
    mock_client.add_source_identifier_to_subscription.assert_called_once()


def test_add_source_identifier_to_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_source_identifier_to_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_source_identifier_to_subscription",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add source identifier to subscription"):
        add_source_identifier_to_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)


def test_add_tags_to_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_resource.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    add_tags_to_resource("test-resource_name", [], region_name=REGION)
    mock_client.add_tags_to_resource.assert_called_once()


def test_add_tags_to_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_tags_to_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_tags_to_resource",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add tags to resource"):
        add_tags_to_resource("test-resource_name", [], region_name=REGION)


def test_apply_pending_maintenance_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.apply_pending_maintenance_action.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", region_name=REGION)
    mock_client.apply_pending_maintenance_action.assert_called_once()


def test_apply_pending_maintenance_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.apply_pending_maintenance_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "apply_pending_maintenance_action",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to apply pending maintenance action"):
        apply_pending_maintenance_action("test-resource_identifier", "test-apply_action", "test-opt_in_type", region_name=REGION)


def test_authorize_db_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_db_security_group_ingress.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    authorize_db_security_group_ingress("test-db_security_group_name", region_name=REGION)
    mock_client.authorize_db_security_group_ingress.assert_called_once()


def test_authorize_db_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_db_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_db_security_group_ingress",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize db security group ingress"):
        authorize_db_security_group_ingress("test-db_security_group_name", region_name=REGION)


def test_backtrack_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.backtrack_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    backtrack_db_cluster("test-db_cluster_identifier", "test-backtrack_to", region_name=REGION)
    mock_client.backtrack_db_cluster.assert_called_once()


def test_backtrack_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.backtrack_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "backtrack_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to backtrack db cluster"):
        backtrack_db_cluster("test-db_cluster_identifier", "test-backtrack_to", region_name=REGION)


def test_cancel_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_task.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    cancel_export_task("test-export_task_identifier", region_name=REGION)
    mock_client.cancel_export_task.assert_called_once()


def test_cancel_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_export_task",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel export task"):
        cancel_export_task("test-export_task_identifier", region_name=REGION)


def test_copy_db_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", region_name=REGION)
    mock_client.copy_db_cluster_parameter_group.assert_called_once()


def test_copy_db_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_cluster_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy db cluster parameter group"):
        copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", region_name=REGION)


def test_copy_db_cluster_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_cluster_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.copy_db_cluster_snapshot.assert_called_once()


def test_copy_db_cluster_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_cluster_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy db cluster snapshot"):
        copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", region_name=REGION)


def test_copy_db_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", region_name=REGION)
    mock_client.copy_db_parameter_group.assert_called_once()


def test_copy_db_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy db parameter group"):
        copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", region_name=REGION)


def test_copy_db_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    copy_db_snapshot("test-source_db_snapshot_identifier", "test-target_db_snapshot_identifier", region_name=REGION)
    mock_client.copy_db_snapshot.assert_called_once()


def test_copy_db_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_db_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_db_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy db snapshot"):
        copy_db_snapshot("test-source_db_snapshot_identifier", "test-target_db_snapshot_identifier", region_name=REGION)


def test_copy_option_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_option_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    copy_option_group("test-source_option_group_identifier", "test-target_option_group_identifier", "test-target_option_group_description", region_name=REGION)
    mock_client.copy_option_group.assert_called_once()


def test_copy_option_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_option_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_option_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy option group"):
        copy_option_group("test-source_option_group_identifier", "test-target_option_group_identifier", "test-target_option_group_description", region_name=REGION)


def test_create_blue_green_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_blue_green_deployment.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_blue_green_deployment("test-blue_green_deployment_name", "test-source", region_name=REGION)
    mock_client.create_blue_green_deployment.assert_called_once()


def test_create_blue_green_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_blue_green_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_blue_green_deployment",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create blue green deployment"):
        create_blue_green_deployment("test-blue_green_deployment_name", "test-source", region_name=REGION)


def test_create_custom_db_engine_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_db_engine_version.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_custom_db_engine_version("test-engine", "test-engine_version", region_name=REGION)
    mock_client.create_custom_db_engine_version.assert_called_once()


def test_create_custom_db_engine_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_db_engine_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_db_engine_version",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom db engine version"):
        create_custom_db_engine_version("test-engine", "test-engine_version", region_name=REGION)


def test_create_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_cluster("test-db_cluster_identifier", "test-engine", region_name=REGION)
    mock_client.create_db_cluster.assert_called_once()


def test_create_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db cluster"):
        create_db_cluster("test-db_cluster_identifier", "test-engine", region_name=REGION)


def test_create_db_cluster_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", region_name=REGION)
    mock_client.create_db_cluster_endpoint.assert_called_once()


def test_create_db_cluster_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db cluster endpoint"):
        create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", region_name=REGION)


def test_create_db_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)
    mock_client.create_db_cluster_parameter_group.assert_called_once()


def test_create_db_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db cluster parameter group"):
        create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)


def test_create_db_cluster_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_cluster_snapshot("test-db_cluster_snapshot_identifier", "test-db_cluster_identifier", region_name=REGION)
    mock_client.create_db_cluster_snapshot.assert_called_once()


def test_create_db_cluster_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_cluster_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db cluster snapshot"):
        create_db_cluster_snapshot("test-db_cluster_snapshot_identifier", "test-db_cluster_identifier", region_name=REGION)


def test_create_db_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_instance.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_instance("test-db_instance_identifier", "test-db_instance_class", "test-engine", region_name=REGION)
    mock_client.create_db_instance.assert_called_once()


def test_create_db_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_instance",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db instance"):
        create_db_instance("test-db_instance_identifier", "test-db_instance_class", "test-engine", region_name=REGION)


def test_create_db_instance_read_replica(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_instance_read_replica.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_instance_read_replica("test-db_instance_identifier", region_name=REGION)
    mock_client.create_db_instance_read_replica.assert_called_once()


def test_create_db_instance_read_replica_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_instance_read_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_instance_read_replica",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db instance read replica"):
        create_db_instance_read_replica("test-db_instance_identifier", region_name=REGION)


def test_create_db_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)
    mock_client.create_db_parameter_group.assert_called_once()


def test_create_db_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db parameter group"):
        create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", region_name=REGION)


def test_create_db_proxy(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_proxy.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_proxy("test-db_proxy_name", "test-engine_family", "test-role_arn", [], region_name=REGION)
    mock_client.create_db_proxy.assert_called_once()


def test_create_db_proxy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_proxy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_proxy",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db proxy"):
        create_db_proxy("test-db_proxy_name", "test-engine_family", "test-role_arn", [], region_name=REGION)


def test_create_db_proxy_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_proxy_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_proxy_endpoint("test-db_proxy_name", "test-db_proxy_endpoint_name", [], region_name=REGION)
    mock_client.create_db_proxy_endpoint.assert_called_once()


def test_create_db_proxy_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_proxy_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_proxy_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db proxy endpoint"):
        create_db_proxy_endpoint("test-db_proxy_name", "test-db_proxy_endpoint_name", [], region_name=REGION)


def test_create_db_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_security_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_security_group("test-db_security_group_name", "test-db_security_group_description", region_name=REGION)
    mock_client.create_db_security_group.assert_called_once()


def test_create_db_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_security_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db security group"):
        create_db_security_group("test-db_security_group_name", "test-db_security_group_description", region_name=REGION)


def test_create_db_shard_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_shard_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_shard_group("test-db_shard_group_identifier", "test-db_cluster_identifier", "test-max_acu", region_name=REGION)
    mock_client.create_db_shard_group.assert_called_once()


def test_create_db_shard_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_shard_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_shard_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db shard group"):
        create_db_shard_group("test-db_shard_group_identifier", "test-db_cluster_identifier", "test-max_acu", region_name=REGION)


def test_create_db_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_subnet_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], region_name=REGION)
    mock_client.create_db_subnet_group.assert_called_once()


def test_create_db_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_db_subnet_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create db subnet group"):
        create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", [], region_name=REGION)


def test_create_event_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)
    mock_client.create_event_subscription.assert_called_once()


def test_create_event_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_subscription",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create event subscription"):
        create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)


def test_create_global_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_global_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.create_global_cluster.assert_called_once()


def test_create_global_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_global_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create global cluster"):
        create_global_cluster("test-global_cluster_identifier", region_name=REGION)


def test_create_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_integration("test-source_arn", "test-target_arn", "test-integration_name", region_name=REGION)
    mock_client.create_integration.assert_called_once()


def test_create_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_integration",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create integration"):
        create_integration("test-source_arn", "test-target_arn", "test-integration_name", region_name=REGION)


def test_create_option_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_option_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_option_group("test-option_group_name", "test-engine_name", "test-major_engine_version", "test-option_group_description", region_name=REGION)
    mock_client.create_option_group.assert_called_once()


def test_create_option_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_option_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_option_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create option group"):
        create_option_group("test-option_group_name", "test-engine_name", "test-major_engine_version", "test-option_group_description", region_name=REGION)


def test_create_tenant_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tenant_database.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    create_tenant_database("test-db_instance_identifier", "test-tenant_db_name", "test-master_username", region_name=REGION)
    mock_client.create_tenant_database.assert_called_once()


def test_create_tenant_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tenant_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tenant_database",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tenant database"):
        create_tenant_database("test-db_instance_identifier", "test-tenant_db_name", "test-master_username", region_name=REGION)


def test_delete_blue_green_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_blue_green_deployment.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_blue_green_deployment("test-blue_green_deployment_identifier", region_name=REGION)
    mock_client.delete_blue_green_deployment.assert_called_once()


def test_delete_blue_green_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_blue_green_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_blue_green_deployment",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete blue green deployment"):
        delete_blue_green_deployment("test-blue_green_deployment_identifier", region_name=REGION)


def test_delete_custom_db_engine_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_db_engine_version.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_custom_db_engine_version("test-engine", "test-engine_version", region_name=REGION)
    mock_client.delete_custom_db_engine_version.assert_called_once()


def test_delete_custom_db_engine_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_db_engine_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_db_engine_version",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom db engine version"):
        delete_custom_db_engine_version("test-engine", "test-engine_version", region_name=REGION)


def test_delete_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.delete_db_cluster.assert_called_once()


def test_delete_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db cluster"):
        delete_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_delete_db_cluster_automated_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_automated_backup.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_cluster_automated_backup("test-db_cluster_resource_id", region_name=REGION)
    mock_client.delete_db_cluster_automated_backup.assert_called_once()


def test_delete_db_cluster_automated_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_automated_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_automated_backup",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db cluster automated backup"):
        delete_db_cluster_automated_backup("test-db_cluster_resource_id", region_name=REGION)


def test_delete_db_cluster_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)
    mock_client.delete_db_cluster_endpoint.assert_called_once()


def test_delete_db_cluster_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db cluster endpoint"):
        delete_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)


def test_delete_db_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.delete_db_cluster_parameter_group.assert_called_once()


def test_delete_db_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db cluster parameter group"):
        delete_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)


def test_delete_db_cluster_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.delete_db_cluster_snapshot.assert_called_once()


def test_delete_db_cluster_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_cluster_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db cluster snapshot"):
        delete_db_cluster_snapshot("test-db_cluster_snapshot_identifier", region_name=REGION)


def test_delete_db_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_instance.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_instance("test-db_instance_identifier", region_name=REGION)
    mock_client.delete_db_instance.assert_called_once()


def test_delete_db_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_instance",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db instance"):
        delete_db_instance("test-db_instance_identifier", region_name=REGION)


def test_delete_db_instance_automated_backup(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_instance_automated_backup.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_instance_automated_backup(region_name=REGION)
    mock_client.delete_db_instance_automated_backup.assert_called_once()


def test_delete_db_instance_automated_backup_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_instance_automated_backup.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_instance_automated_backup",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db instance automated backup"):
        delete_db_instance_automated_backup(region_name=REGION)


def test_delete_db_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_parameter_group("test-db_parameter_group_name", region_name=REGION)
    mock_client.delete_db_parameter_group.assert_called_once()


def test_delete_db_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db parameter group"):
        delete_db_parameter_group("test-db_parameter_group_name", region_name=REGION)


def test_delete_db_proxy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_proxy.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_proxy("test-db_proxy_name", region_name=REGION)
    mock_client.delete_db_proxy.assert_called_once()


def test_delete_db_proxy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_proxy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_proxy",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db proxy"):
        delete_db_proxy("test-db_proxy_name", region_name=REGION)


def test_delete_db_proxy_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_proxy_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_proxy_endpoint("test-db_proxy_endpoint_name", region_name=REGION)
    mock_client.delete_db_proxy_endpoint.assert_called_once()


def test_delete_db_proxy_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_proxy_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_proxy_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db proxy endpoint"):
        delete_db_proxy_endpoint("test-db_proxy_endpoint_name", region_name=REGION)


def test_delete_db_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_security_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_security_group("test-db_security_group_name", region_name=REGION)
    mock_client.delete_db_security_group.assert_called_once()


def test_delete_db_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_security_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db security group"):
        delete_db_security_group("test-db_security_group_name", region_name=REGION)


def test_delete_db_shard_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_shard_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_shard_group("test-db_shard_group_identifier", region_name=REGION)
    mock_client.delete_db_shard_group.assert_called_once()


def test_delete_db_shard_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_shard_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_shard_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db shard group"):
        delete_db_shard_group("test-db_shard_group_identifier", region_name=REGION)


def test_delete_db_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_subnet_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_db_subnet_group("test-db_subnet_group_name", region_name=REGION)
    mock_client.delete_db_subnet_group.assert_called_once()


def test_delete_db_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_db_subnet_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete db subnet group"):
        delete_db_subnet_group("test-db_subnet_group_name", region_name=REGION)


def test_delete_event_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_subscription.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.delete_event_subscription.assert_called_once()


def test_delete_event_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_subscription",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete event subscription"):
        delete_event_subscription("test-subscription_name", region_name=REGION)


def test_delete_global_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_global_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.delete_global_cluster.assert_called_once()


def test_delete_global_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_global_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete global cluster"):
        delete_global_cluster("test-global_cluster_identifier", region_name=REGION)


def test_delete_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_integration("test-integration_identifier", region_name=REGION)
    mock_client.delete_integration.assert_called_once()


def test_delete_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete integration"):
        delete_integration("test-integration_identifier", region_name=REGION)


def test_delete_option_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_option_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_option_group("test-option_group_name", region_name=REGION)
    mock_client.delete_option_group.assert_called_once()


def test_delete_option_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_option_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_option_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete option group"):
        delete_option_group("test-option_group_name", region_name=REGION)


def test_delete_tenant_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tenant_database.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    delete_tenant_database("test-db_instance_identifier", "test-tenant_db_name", region_name=REGION)
    mock_client.delete_tenant_database.assert_called_once()


def test_delete_tenant_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tenant_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tenant_database",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tenant database"):
        delete_tenant_database("test-db_instance_identifier", "test-tenant_db_name", region_name=REGION)


def test_deregister_db_proxy_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_db_proxy_targets.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    deregister_db_proxy_targets("test-db_proxy_name", region_name=REGION)
    mock_client.deregister_db_proxy_targets.assert_called_once()


def test_deregister_db_proxy_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_db_proxy_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_db_proxy_targets",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister db proxy targets"):
        deregister_db_proxy_targets("test-db_proxy_name", region_name=REGION)


def test_describe_account_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_attributes.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_account_attributes(region_name=REGION)
    mock_client.describe_account_attributes.assert_called_once()


def test_describe_account_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_attributes",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account attributes"):
        describe_account_attributes(region_name=REGION)


def test_describe_blue_green_deployments(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_blue_green_deployments.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_blue_green_deployments(region_name=REGION)
    mock_client.describe_blue_green_deployments.assert_called_once()


def test_describe_blue_green_deployments_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_blue_green_deployments.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_blue_green_deployments",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe blue green deployments"):
        describe_blue_green_deployments(region_name=REGION)


def test_describe_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_certificates.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_certificates(region_name=REGION)
    mock_client.describe_certificates.assert_called_once()


def test_describe_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_certificates",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe certificates"):
        describe_certificates(region_name=REGION)


def test_describe_db_cluster_automated_backups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_automated_backups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_automated_backups(region_name=REGION)
    mock_client.describe_db_cluster_automated_backups.assert_called_once()


def test_describe_db_cluster_automated_backups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_automated_backups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_automated_backups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster automated backups"):
        describe_db_cluster_automated_backups(region_name=REGION)


def test_describe_db_cluster_backtracks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_backtracks.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_backtracks("test-db_cluster_identifier", region_name=REGION)
    mock_client.describe_db_cluster_backtracks.assert_called_once()


def test_describe_db_cluster_backtracks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_backtracks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_backtracks",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster backtracks"):
        describe_db_cluster_backtracks("test-db_cluster_identifier", region_name=REGION)


def test_describe_db_cluster_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_endpoints.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_endpoints(region_name=REGION)
    mock_client.describe_db_cluster_endpoints.assert_called_once()


def test_describe_db_cluster_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_endpoints",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster endpoints"):
        describe_db_cluster_endpoints(region_name=REGION)


def test_describe_db_cluster_parameter_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameter_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameter_groups(region_name=REGION)
    mock_client.describe_db_cluster_parameter_groups.assert_called_once()


def test_describe_db_cluster_parameter_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_parameter_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster parameter groups"):
        describe_db_cluster_parameter_groups(region_name=REGION)


def test_describe_db_cluster_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameters.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameters("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.describe_db_cluster_parameters.assert_called_once()


def test_describe_db_cluster_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_parameters",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster parameters"):
        describe_db_cluster_parameters("test-db_cluster_parameter_group_name", region_name=REGION)


def test_describe_db_cluster_snapshot_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_snapshot_attributes.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", region_name=REGION)
    mock_client.describe_db_cluster_snapshot_attributes.assert_called_once()


def test_describe_db_cluster_snapshot_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_snapshot_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_snapshot_attributes",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster snapshot attributes"):
        describe_db_cluster_snapshot_attributes("test-db_cluster_snapshot_identifier", region_name=REGION)


def test_describe_db_cluster_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_snapshots.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_snapshots(region_name=REGION)
    mock_client.describe_db_cluster_snapshots.assert_called_once()


def test_describe_db_cluster_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_cluster_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_cluster_snapshots",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db cluster snapshots"):
        describe_db_cluster_snapshots(region_name=REGION)


def test_describe_db_clusters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_clusters.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_clusters(region_name=REGION)
    mock_client.describe_db_clusters.assert_called_once()


def test_describe_db_clusters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_clusters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_clusters",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db clusters"):
        describe_db_clusters(region_name=REGION)


def test_describe_db_engine_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_engine_versions.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_engine_versions(region_name=REGION)
    mock_client.describe_db_engine_versions.assert_called_once()


def test_describe_db_engine_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_engine_versions",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db engine versions"):
        describe_db_engine_versions(region_name=REGION)


def test_describe_db_instance_automated_backups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_instance_automated_backups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_instance_automated_backups(region_name=REGION)
    mock_client.describe_db_instance_automated_backups.assert_called_once()


def test_describe_db_instance_automated_backups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_instance_automated_backups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_instance_automated_backups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db instance automated backups"):
        describe_db_instance_automated_backups(region_name=REGION)


def test_describe_db_log_files(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_log_files.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_log_files("test-db_instance_identifier", region_name=REGION)
    mock_client.describe_db_log_files.assert_called_once()


def test_describe_db_log_files_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_log_files.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_log_files",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db log files"):
        describe_db_log_files("test-db_instance_identifier", region_name=REGION)


def test_describe_db_major_engine_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_major_engine_versions.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_major_engine_versions(region_name=REGION)
    mock_client.describe_db_major_engine_versions.assert_called_once()


def test_describe_db_major_engine_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_major_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_major_engine_versions",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db major engine versions"):
        describe_db_major_engine_versions(region_name=REGION)


def test_describe_db_parameter_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_parameter_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_parameter_groups(region_name=REGION)
    mock_client.describe_db_parameter_groups.assert_called_once()


def test_describe_db_parameter_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_parameter_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db parameter groups"):
        describe_db_parameter_groups(region_name=REGION)


def test_describe_db_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_parameters.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_parameters("test-db_parameter_group_name", region_name=REGION)
    mock_client.describe_db_parameters.assert_called_once()


def test_describe_db_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_parameters",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db parameters"):
        describe_db_parameters("test-db_parameter_group_name", region_name=REGION)


def test_describe_db_proxies(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxies.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_proxies(region_name=REGION)
    mock_client.describe_db_proxies.assert_called_once()


def test_describe_db_proxies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_proxies",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db proxies"):
        describe_db_proxies(region_name=REGION)


def test_describe_db_proxy_endpoints(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxy_endpoints.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_proxy_endpoints(region_name=REGION)
    mock_client.describe_db_proxy_endpoints.assert_called_once()


def test_describe_db_proxy_endpoints_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxy_endpoints.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_proxy_endpoints",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db proxy endpoints"):
        describe_db_proxy_endpoints(region_name=REGION)


def test_describe_db_proxy_target_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxy_target_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_proxy_target_groups("test-db_proxy_name", region_name=REGION)
    mock_client.describe_db_proxy_target_groups.assert_called_once()


def test_describe_db_proxy_target_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxy_target_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_proxy_target_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db proxy target groups"):
        describe_db_proxy_target_groups("test-db_proxy_name", region_name=REGION)


def test_describe_db_proxy_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxy_targets.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_proxy_targets("test-db_proxy_name", region_name=REGION)
    mock_client.describe_db_proxy_targets.assert_called_once()


def test_describe_db_proxy_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_proxy_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_proxy_targets",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db proxy targets"):
        describe_db_proxy_targets("test-db_proxy_name", region_name=REGION)


def test_describe_db_recommendations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_recommendations.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_recommendations(region_name=REGION)
    mock_client.describe_db_recommendations.assert_called_once()


def test_describe_db_recommendations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_recommendations",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db recommendations"):
        describe_db_recommendations(region_name=REGION)


def test_describe_db_security_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_security_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_security_groups(region_name=REGION)
    mock_client.describe_db_security_groups.assert_called_once()


def test_describe_db_security_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_security_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_security_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db security groups"):
        describe_db_security_groups(region_name=REGION)


def test_describe_db_shard_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_shard_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_shard_groups(region_name=REGION)
    mock_client.describe_db_shard_groups.assert_called_once()


def test_describe_db_shard_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_shard_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_shard_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db shard groups"):
        describe_db_shard_groups(region_name=REGION)


def test_describe_db_snapshot_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_snapshot_attributes.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_snapshot_attributes("test-db_snapshot_identifier", region_name=REGION)
    mock_client.describe_db_snapshot_attributes.assert_called_once()


def test_describe_db_snapshot_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_snapshot_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_snapshot_attributes",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db snapshot attributes"):
        describe_db_snapshot_attributes("test-db_snapshot_identifier", region_name=REGION)


def test_describe_db_snapshot_tenant_databases(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_snapshot_tenant_databases.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_snapshot_tenant_databases(region_name=REGION)
    mock_client.describe_db_snapshot_tenant_databases.assert_called_once()


def test_describe_db_snapshot_tenant_databases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_snapshot_tenant_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_snapshot_tenant_databases",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db snapshot tenant databases"):
        describe_db_snapshot_tenant_databases(region_name=REGION)


def test_describe_db_subnet_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_subnet_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_db_subnet_groups(region_name=REGION)
    mock_client.describe_db_subnet_groups.assert_called_once()


def test_describe_db_subnet_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_db_subnet_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_db_subnet_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe db subnet groups"):
        describe_db_subnet_groups(region_name=REGION)


def test_describe_engine_default_cluster_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_engine_default_cluster_parameters.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_engine_default_cluster_parameters("test-db_parameter_group_family", region_name=REGION)
    mock_client.describe_engine_default_cluster_parameters.assert_called_once()


def test_describe_engine_default_cluster_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_engine_default_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_default_cluster_parameters",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe engine default cluster parameters"):
        describe_engine_default_cluster_parameters("test-db_parameter_group_family", region_name=REGION)


def test_describe_engine_default_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_engine_default_parameters("test-db_parameter_group_family", region_name=REGION)
    mock_client.describe_engine_default_parameters.assert_called_once()


def test_describe_engine_default_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_default_parameters",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe engine default parameters"):
        describe_engine_default_parameters("test-db_parameter_group_family", region_name=REGION)


def test_describe_event_categories(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_event_categories(region_name=REGION)
    mock_client.describe_event_categories.assert_called_once()


def test_describe_event_categories_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_categories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_categories",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event categories"):
        describe_event_categories(region_name=REGION)


def test_describe_event_subscriptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(region_name=REGION)
    mock_client.describe_event_subscriptions.assert_called_once()


def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_subscriptions",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event subscriptions"):
        describe_event_subscriptions(region_name=REGION)


def test_describe_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


def test_describe_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


def test_describe_export_tasks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export_tasks.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_export_tasks(region_name=REGION)
    mock_client.describe_export_tasks.assert_called_once()


def test_describe_export_tasks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_export_tasks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_export_tasks",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe export tasks"):
        describe_export_tasks(region_name=REGION)


def test_describe_global_clusters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_clusters.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_global_clusters(region_name=REGION)
    mock_client.describe_global_clusters.assert_called_once()


def test_describe_global_clusters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_clusters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_global_clusters",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe global clusters"):
        describe_global_clusters(region_name=REGION)


def test_describe_integrations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_integrations.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_integrations(region_name=REGION)
    mock_client.describe_integrations.assert_called_once()


def test_describe_integrations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_integrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_integrations",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe integrations"):
        describe_integrations(region_name=REGION)


def test_describe_option_group_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_option_group_options.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_option_group_options("test-engine_name", region_name=REGION)
    mock_client.describe_option_group_options.assert_called_once()


def test_describe_option_group_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_option_group_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_option_group_options",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe option group options"):
        describe_option_group_options("test-engine_name", region_name=REGION)


def test_describe_option_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_option_groups.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_option_groups(region_name=REGION)
    mock_client.describe_option_groups.assert_called_once()


def test_describe_option_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_option_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_option_groups",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe option groups"):
        describe_option_groups(region_name=REGION)


def test_describe_orderable_db_instance_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_orderable_db_instance_options.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_orderable_db_instance_options("test-engine", region_name=REGION)
    mock_client.describe_orderable_db_instance_options.assert_called_once()


def test_describe_orderable_db_instance_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_orderable_db_instance_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_orderable_db_instance_options",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe orderable db instance options"):
        describe_orderable_db_instance_options("test-engine", region_name=REGION)


def test_describe_pending_maintenance_actions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pending_maintenance_actions.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_pending_maintenance_actions(region_name=REGION)
    mock_client.describe_pending_maintenance_actions.assert_called_once()


def test_describe_pending_maintenance_actions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pending_maintenance_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pending_maintenance_actions",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe pending maintenance actions"):
        describe_pending_maintenance_actions(region_name=REGION)


def test_describe_reserved_db_instances(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_db_instances.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_reserved_db_instances(region_name=REGION)
    mock_client.describe_reserved_db_instances.assert_called_once()


def test_describe_reserved_db_instances_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_db_instances.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_db_instances",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved db instances"):
        describe_reserved_db_instances(region_name=REGION)


def test_describe_reserved_db_instances_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_db_instances_offerings.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_reserved_db_instances_offerings(region_name=REGION)
    mock_client.describe_reserved_db_instances_offerings.assert_called_once()


def test_describe_reserved_db_instances_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_db_instances_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_db_instances_offerings",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved db instances offerings"):
        describe_reserved_db_instances_offerings(region_name=REGION)


def test_describe_source_regions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_source_regions.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_source_regions(region_name=REGION)
    mock_client.describe_source_regions.assert_called_once()


def test_describe_source_regions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_source_regions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_source_regions",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe source regions"):
        describe_source_regions(region_name=REGION)


def test_describe_tenant_databases(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tenant_databases.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_tenant_databases(region_name=REGION)
    mock_client.describe_tenant_databases.assert_called_once()


def test_describe_tenant_databases_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tenant_databases.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tenant_databases",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tenant databases"):
        describe_tenant_databases(region_name=REGION)


def test_describe_valid_db_instance_modifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_valid_db_instance_modifications.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    describe_valid_db_instance_modifications("test-db_instance_identifier", region_name=REGION)
    mock_client.describe_valid_db_instance_modifications.assert_called_once()


def test_describe_valid_db_instance_modifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_valid_db_instance_modifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_valid_db_instance_modifications",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe valid db instance modifications"):
        describe_valid_db_instance_modifications("test-db_instance_identifier", region_name=REGION)


def test_disable_http_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_http_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    disable_http_endpoint("test-resource_arn", region_name=REGION)
    mock_client.disable_http_endpoint.assert_called_once()


def test_disable_http_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_http_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_http_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable http endpoint"):
        disable_http_endpoint("test-resource_arn", region_name=REGION)


def test_download_db_log_file_portion(monkeypatch):
    mock_client = MagicMock()
    mock_client.download_db_log_file_portion.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    download_db_log_file_portion("test-db_instance_identifier", "test-log_file_name", region_name=REGION)
    mock_client.download_db_log_file_portion.assert_called_once()


def test_download_db_log_file_portion_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.download_db_log_file_portion.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "download_db_log_file_portion",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to download db log file portion"):
        download_db_log_file_portion("test-db_instance_identifier", "test-log_file_name", region_name=REGION)


def test_enable_http_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_http_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    enable_http_endpoint("test-resource_arn", region_name=REGION)
    mock_client.enable_http_endpoint.assert_called_once()


def test_enable_http_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_http_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_http_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable http endpoint"):
        enable_http_endpoint("test-resource_arn", region_name=REGION)


def test_failover_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    failover_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.failover_db_cluster.assert_called_once()


def test_failover_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to failover db cluster"):
        failover_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_failover_global_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_global_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)
    mock_client.failover_global_cluster.assert_called_once()


def test_failover_global_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_global_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to failover global cluster"):
        failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_name", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_name", region_name=REGION)


def test_modify_activity_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_activity_stream.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_activity_stream(region_name=REGION)
    mock_client.modify_activity_stream.assert_called_once()


def test_modify_activity_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_activity_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_activity_stream",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify activity stream"):
        modify_activity_stream(region_name=REGION)


def test_modify_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_certificates.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_certificates(region_name=REGION)
    mock_client.modify_certificates.assert_called_once()


def test_modify_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_certificates",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify certificates"):
        modify_certificates(region_name=REGION)


def test_modify_current_db_cluster_capacity(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_current_db_cluster_capacity.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_current_db_cluster_capacity("test-db_cluster_identifier", region_name=REGION)
    mock_client.modify_current_db_cluster_capacity.assert_called_once()


def test_modify_current_db_cluster_capacity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_current_db_cluster_capacity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_current_db_cluster_capacity",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify current db cluster capacity"):
        modify_current_db_cluster_capacity("test-db_cluster_identifier", region_name=REGION)


def test_modify_custom_db_engine_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_custom_db_engine_version.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_custom_db_engine_version("test-engine", "test-engine_version", region_name=REGION)
    mock_client.modify_custom_db_engine_version.assert_called_once()


def test_modify_custom_db_engine_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_custom_db_engine_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_custom_db_engine_version",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify custom db engine version"):
        modify_custom_db_engine_version("test-engine", "test-engine_version", region_name=REGION)


def test_modify_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.modify_db_cluster.assert_called_once()


def test_modify_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db cluster"):
        modify_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_modify_db_cluster_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)
    mock_client.modify_db_cluster_endpoint.assert_called_once()


def test_modify_db_cluster_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db cluster endpoint"):
        modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", region_name=REGION)


def test_modify_db_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], region_name=REGION)
    mock_client.modify_db_cluster_parameter_group.assert_called_once()


def test_modify_db_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db cluster parameter group"):
        modify_db_cluster_parameter_group("test-db_cluster_parameter_group_name", [], region_name=REGION)


def test_modify_db_cluster_snapshot_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster_snapshot_attribute.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", region_name=REGION)
    mock_client.modify_db_cluster_snapshot_attribute.assert_called_once()


def test_modify_db_cluster_snapshot_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_cluster_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_cluster_snapshot_attribute",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db cluster snapshot attribute"):
        modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", region_name=REGION)


def test_modify_db_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_instance.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_instance("test-db_instance_identifier", region_name=REGION)
    mock_client.modify_db_instance.assert_called_once()


def test_modify_db_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_instance",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db instance"):
        modify_db_instance("test-db_instance_identifier", region_name=REGION)


def test_modify_db_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_parameter_group("test-db_parameter_group_name", [], region_name=REGION)
    mock_client.modify_db_parameter_group.assert_called_once()


def test_modify_db_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db parameter group"):
        modify_db_parameter_group("test-db_parameter_group_name", [], region_name=REGION)


def test_modify_db_proxy(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_proxy.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_proxy("test-db_proxy_name", region_name=REGION)
    mock_client.modify_db_proxy.assert_called_once()


def test_modify_db_proxy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_proxy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_proxy",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db proxy"):
        modify_db_proxy("test-db_proxy_name", region_name=REGION)


def test_modify_db_proxy_endpoint(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_proxy_endpoint.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_proxy_endpoint("test-db_proxy_endpoint_name", region_name=REGION)
    mock_client.modify_db_proxy_endpoint.assert_called_once()


def test_modify_db_proxy_endpoint_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_proxy_endpoint.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_proxy_endpoint",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db proxy endpoint"):
        modify_db_proxy_endpoint("test-db_proxy_endpoint_name", region_name=REGION)


def test_modify_db_proxy_target_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_proxy_target_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_proxy_target_group("test-target_group_name", "test-db_proxy_name", region_name=REGION)
    mock_client.modify_db_proxy_target_group.assert_called_once()


def test_modify_db_proxy_target_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_proxy_target_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_proxy_target_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db proxy target group"):
        modify_db_proxy_target_group("test-target_group_name", "test-db_proxy_name", region_name=REGION)


def test_modify_db_recommendation(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_recommendation.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_recommendation("test-recommendation_id", region_name=REGION)
    mock_client.modify_db_recommendation.assert_called_once()


def test_modify_db_recommendation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_recommendation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_recommendation",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db recommendation"):
        modify_db_recommendation("test-recommendation_id", region_name=REGION)


def test_modify_db_shard_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_shard_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_shard_group("test-db_shard_group_identifier", region_name=REGION)
    mock_client.modify_db_shard_group.assert_called_once()


def test_modify_db_shard_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_shard_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_shard_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db shard group"):
        modify_db_shard_group("test-db_shard_group_identifier", region_name=REGION)


def test_modify_db_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_snapshot("test-db_snapshot_identifier", region_name=REGION)
    mock_client.modify_db_snapshot.assert_called_once()


def test_modify_db_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db snapshot"):
        modify_db_snapshot("test-db_snapshot_identifier", region_name=REGION)


def test_modify_db_snapshot_attribute(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_snapshot_attribute.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_snapshot_attribute("test-db_snapshot_identifier", "test-attribute_name", region_name=REGION)
    mock_client.modify_db_snapshot_attribute.assert_called_once()


def test_modify_db_snapshot_attribute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_snapshot_attribute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_snapshot_attribute",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db snapshot attribute"):
        modify_db_snapshot_attribute("test-db_snapshot_identifier", "test-attribute_name", region_name=REGION)


def test_modify_db_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_subnet_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_db_subnet_group("test-db_subnet_group_name", [], region_name=REGION)
    mock_client.modify_db_subnet_group.assert_called_once()


def test_modify_db_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_db_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_db_subnet_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify db subnet group"):
        modify_db_subnet_group("test-db_subnet_group_name", [], region_name=REGION)


def test_modify_event_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.modify_event_subscription.assert_called_once()


def test_modify_event_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_event_subscription",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify event subscription"):
        modify_event_subscription("test-subscription_name", region_name=REGION)


def test_modify_global_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_global_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_global_cluster("test-global_cluster_identifier", region_name=REGION)
    mock_client.modify_global_cluster.assert_called_once()


def test_modify_global_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_global_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify global cluster"):
        modify_global_cluster("test-global_cluster_identifier", region_name=REGION)


def test_modify_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_integration.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_integration("test-integration_identifier", region_name=REGION)
    mock_client.modify_integration.assert_called_once()


def test_modify_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_integration",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify integration"):
        modify_integration("test-integration_identifier", region_name=REGION)


def test_modify_option_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_option_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_option_group("test-option_group_name", region_name=REGION)
    mock_client.modify_option_group.assert_called_once()


def test_modify_option_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_option_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_option_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify option group"):
        modify_option_group("test-option_group_name", region_name=REGION)


def test_modify_tenant_database(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_tenant_database.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    modify_tenant_database("test-db_instance_identifier", "test-tenant_db_name", region_name=REGION)
    mock_client.modify_tenant_database.assert_called_once()


def test_modify_tenant_database_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_tenant_database.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_tenant_database",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify tenant database"):
        modify_tenant_database("test-db_instance_identifier", "test-tenant_db_name", region_name=REGION)


def test_promote_read_replica(monkeypatch):
    mock_client = MagicMock()
    mock_client.promote_read_replica.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    promote_read_replica("test-db_instance_identifier", region_name=REGION)
    mock_client.promote_read_replica.assert_called_once()


def test_promote_read_replica_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.promote_read_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "promote_read_replica",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to promote read replica"):
        promote_read_replica("test-db_instance_identifier", region_name=REGION)


def test_promote_read_replica_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.promote_read_replica_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    promote_read_replica_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.promote_read_replica_db_cluster.assert_called_once()


def test_promote_read_replica_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.promote_read_replica_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "promote_read_replica_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to promote read replica db cluster"):
        promote_read_replica_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_purchase_reserved_db_instances_offering(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_db_instances_offering.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    purchase_reserved_db_instances_offering("test-reserved_db_instances_offering_id", region_name=REGION)
    mock_client.purchase_reserved_db_instances_offering.assert_called_once()


def test_purchase_reserved_db_instances_offering_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_db_instances_offering.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_reserved_db_instances_offering",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase reserved db instances offering"):
        purchase_reserved_db_instances_offering("test-reserved_db_instances_offering_id", region_name=REGION)


def test_reboot_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    reboot_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.reboot_db_cluster.assert_called_once()


def test_reboot_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reboot db cluster"):
        reboot_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_reboot_db_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_db_instance.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    reboot_db_instance("test-db_instance_identifier", region_name=REGION)
    mock_client.reboot_db_instance.assert_called_once()


def test_reboot_db_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_db_instance",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reboot db instance"):
        reboot_db_instance("test-db_instance_identifier", region_name=REGION)


def test_reboot_db_shard_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_db_shard_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    reboot_db_shard_group("test-db_shard_group_identifier", region_name=REGION)
    mock_client.reboot_db_shard_group.assert_called_once()


def test_reboot_db_shard_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_db_shard_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_db_shard_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reboot db shard group"):
        reboot_db_shard_group("test-db_shard_group_identifier", region_name=REGION)


def test_register_db_proxy_targets(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_db_proxy_targets.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    register_db_proxy_targets("test-db_proxy_name", region_name=REGION)
    mock_client.register_db_proxy_targets.assert_called_once()


def test_register_db_proxy_targets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_db_proxy_targets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_db_proxy_targets",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register db proxy targets"):
        register_db_proxy_targets("test-db_proxy_name", region_name=REGION)


def test_remove_from_global_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_from_global_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", region_name=REGION)
    mock_client.remove_from_global_cluster.assert_called_once()


def test_remove_from_global_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_from_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_from_global_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove from global cluster"):
        remove_from_global_cluster("test-global_cluster_identifier", "test-db_cluster_identifier", region_name=REGION)


def test_remove_role_from_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_role_from_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)
    mock_client.remove_role_from_db_cluster.assert_called_once()


def test_remove_role_from_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_role_from_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_role_from_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove role from db cluster"):
        remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", region_name=REGION)


def test_remove_role_from_db_instance(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_role_from_db_instance.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    remove_role_from_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", region_name=REGION)
    mock_client.remove_role_from_db_instance.assert_called_once()


def test_remove_role_from_db_instance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_role_from_db_instance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_role_from_db_instance",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove role from db instance"):
        remove_role_from_db_instance("test-db_instance_identifier", "test-role_arn", "test-feature_name", region_name=REGION)


def test_remove_source_identifier_from_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_source_identifier_from_subscription.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)
    mock_client.remove_source_identifier_from_subscription.assert_called_once()


def test_remove_source_identifier_from_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_source_identifier_from_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_source_identifier_from_subscription",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove source identifier from subscription"):
        remove_source_identifier_from_subscription("test-subscription_name", "test-source_identifier", region_name=REGION)


def test_remove_tags_from_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    remove_tags_from_resource("test-resource_name", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_name", [], region_name=REGION)


def test_reset_db_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)
    mock_client.reset_db_cluster_parameter_group.assert_called_once()


def test_reset_db_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_db_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_db_cluster_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset db cluster parameter group"):
        reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", region_name=REGION)


def test_reset_db_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_db_parameter_group.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    reset_db_parameter_group("test-db_parameter_group_name", region_name=REGION)
    mock_client.reset_db_parameter_group.assert_called_once()


def test_reset_db_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_db_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_db_parameter_group",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset db parameter group"):
        reset_db_parameter_group("test-db_parameter_group_name", region_name=REGION)


def test_restore_db_cluster_from_s3(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_s3.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_from_s3("test-db_cluster_identifier", "test-engine", "test-master_username", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", region_name=REGION)
    mock_client.restore_db_cluster_from_s3.assert_called_once()


def test_restore_db_cluster_from_s3_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_s3.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_cluster_from_s3",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore db cluster from s3"):
        restore_db_cluster_from_s3("test-db_cluster_identifier", "test-engine", "test-master_username", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", region_name=REGION)


def test_restore_db_cluster_from_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", region_name=REGION)
    mock_client.restore_db_cluster_from_snapshot.assert_called_once()


def test_restore_db_cluster_from_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_cluster_from_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore db cluster from snapshot"):
        restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", region_name=REGION)


def test_restore_db_cluster_to_point_in_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_cluster_to_point_in_time.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_to_point_in_time("test-db_cluster_identifier", region_name=REGION)
    mock_client.restore_db_cluster_to_point_in_time.assert_called_once()


def test_restore_db_cluster_to_point_in_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_cluster_to_point_in_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_cluster_to_point_in_time",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore db cluster to point in time"):
        restore_db_cluster_to_point_in_time("test-db_cluster_identifier", region_name=REGION)


def test_restore_db_instance_from_db_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_instance_from_db_snapshot.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    restore_db_instance_from_db_snapshot("test-db_instance_identifier", region_name=REGION)
    mock_client.restore_db_instance_from_db_snapshot.assert_called_once()


def test_restore_db_instance_from_db_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_instance_from_db_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_instance_from_db_snapshot",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore db instance from db snapshot"):
        restore_db_instance_from_db_snapshot("test-db_instance_identifier", region_name=REGION)


def test_restore_db_instance_from_s3(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_instance_from_s3.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    restore_db_instance_from_s3("test-db_instance_identifier", "test-db_instance_class", "test-engine", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", region_name=REGION)
    mock_client.restore_db_instance_from_s3.assert_called_once()


def test_restore_db_instance_from_s3_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_instance_from_s3.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_instance_from_s3",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore db instance from s3"):
        restore_db_instance_from_s3("test-db_instance_identifier", "test-db_instance_class", "test-engine", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", region_name=REGION)


def test_restore_db_instance_to_point_in_time(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_instance_to_point_in_time.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    restore_db_instance_to_point_in_time("test-target_db_instance_identifier", region_name=REGION)
    mock_client.restore_db_instance_to_point_in_time.assert_called_once()


def test_restore_db_instance_to_point_in_time_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_db_instance_to_point_in_time.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_db_instance_to_point_in_time",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore db instance to point in time"):
        restore_db_instance_to_point_in_time("test-target_db_instance_identifier", region_name=REGION)


def test_revoke_db_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_db_security_group_ingress.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    revoke_db_security_group_ingress("test-db_security_group_name", region_name=REGION)
    mock_client.revoke_db_security_group_ingress.assert_called_once()


def test_revoke_db_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_db_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_db_security_group_ingress",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke db security group ingress"):
        revoke_db_security_group_ingress("test-db_security_group_name", region_name=REGION)


def test_start_activity_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_activity_stream.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    start_activity_stream("test-resource_arn", "test-mode", "test-kms_key_id", region_name=REGION)
    mock_client.start_activity_stream.assert_called_once()


def test_start_activity_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_activity_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_activity_stream",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start activity stream"):
        start_activity_stream("test-resource_arn", "test-mode", "test-kms_key_id", region_name=REGION)


def test_start_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    start_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.start_db_cluster.assert_called_once()


def test_start_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start db cluster"):
        start_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_start_db_instance_automated_backups_replication(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_db_instance_automated_backups_replication.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    start_db_instance_automated_backups_replication("test-source_db_instance_arn", region_name=REGION)
    mock_client.start_db_instance_automated_backups_replication.assert_called_once()


def test_start_db_instance_automated_backups_replication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_db_instance_automated_backups_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_db_instance_automated_backups_replication",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start db instance automated backups replication"):
        start_db_instance_automated_backups_replication("test-source_db_instance_arn", region_name=REGION)


def test_start_export_task(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_export_task.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    start_export_task("test-export_task_identifier", "test-source_arn", "test-s3_bucket_name", "test-iam_role_arn", "test-kms_key_id", region_name=REGION)
    mock_client.start_export_task.assert_called_once()


def test_start_export_task_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_export_task.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_export_task",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start export task"):
        start_export_task("test-export_task_identifier", "test-source_arn", "test-s3_bucket_name", "test-iam_role_arn", "test-kms_key_id", region_name=REGION)


def test_stop_activity_stream(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_activity_stream.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    stop_activity_stream("test-resource_arn", region_name=REGION)
    mock_client.stop_activity_stream.assert_called_once()


def test_stop_activity_stream_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_activity_stream.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_activity_stream",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop activity stream"):
        stop_activity_stream("test-resource_arn", region_name=REGION)


def test_stop_db_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_db_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    stop_db_cluster("test-db_cluster_identifier", region_name=REGION)
    mock_client.stop_db_cluster.assert_called_once()


def test_stop_db_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_db_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_db_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop db cluster"):
        stop_db_cluster("test-db_cluster_identifier", region_name=REGION)


def test_stop_db_instance_automated_backups_replication(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_db_instance_automated_backups_replication.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    stop_db_instance_automated_backups_replication("test-source_db_instance_arn", region_name=REGION)
    mock_client.stop_db_instance_automated_backups_replication.assert_called_once()


def test_stop_db_instance_automated_backups_replication_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.stop_db_instance_automated_backups_replication.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "stop_db_instance_automated_backups_replication",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to stop db instance automated backups replication"):
        stop_db_instance_automated_backups_replication("test-source_db_instance_arn", region_name=REGION)


def test_switchover_blue_green_deployment(monkeypatch):
    mock_client = MagicMock()
    mock_client.switchover_blue_green_deployment.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    switchover_blue_green_deployment("test-blue_green_deployment_identifier", region_name=REGION)
    mock_client.switchover_blue_green_deployment.assert_called_once()


def test_switchover_blue_green_deployment_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.switchover_blue_green_deployment.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "switchover_blue_green_deployment",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to switchover blue green deployment"):
        switchover_blue_green_deployment("test-blue_green_deployment_identifier", region_name=REGION)


def test_switchover_global_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.switchover_global_cluster.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)
    mock_client.switchover_global_cluster.assert_called_once()


def test_switchover_global_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.switchover_global_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "switchover_global_cluster",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to switchover global cluster"):
        switchover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", region_name=REGION)


def test_switchover_read_replica(monkeypatch):
    mock_client = MagicMock()
    mock_client.switchover_read_replica.return_value = {}
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    switchover_read_replica("test-db_instance_identifier", region_name=REGION)
    mock_client.switchover_read_replica.assert_called_once()


def test_switchover_read_replica_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.switchover_read_replica.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "switchover_read_replica",
    )
    monkeypatch.setattr(rds_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to switchover read replica"):
        switchover_read_replica("test-db_instance_identifier", region_name=REGION)


def test_add_role_to_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import add_role_to_db_cluster
    mock_client = MagicMock()
    mock_client.add_role_to_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    add_role_to_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.add_role_to_db_cluster.assert_called_once()

def test_authorize_db_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import authorize_db_security_group_ingress
    mock_client = MagicMock()
    mock_client.authorize_db_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    authorize_db_security_group_ingress("test-db_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_id="test-ec2_security_group_id", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.authorize_db_security_group_ingress.assert_called_once()

def test_backtrack_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import backtrack_db_cluster
    mock_client = MagicMock()
    mock_client.backtrack_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    backtrack_db_cluster("test-db_cluster_identifier", "test-backtrack_to", force=True, use_earliest_time_on_point_in_time_unavailable=True, region_name="us-east-1")
    mock_client.backtrack_db_cluster.assert_called_once()

def test_copy_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import copy_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.copy_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_parameter_group("test-source_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_identifier", "test-target_db_cluster_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_db_cluster_parameter_group.assert_called_once()

def test_copy_db_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import copy_db_cluster_snapshot
    mock_client = MagicMock()
    mock_client.copy_db_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    copy_db_cluster_snapshot("test-source_db_cluster_snapshot_identifier", "test-target_db_cluster_snapshot_identifier", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", copy_tags=[{"Key": "k", "Value": "v"}], tags=[{"Key": "k", "Value": "v"}], source_region="test-source_region", region_name="us-east-1")
    mock_client.copy_db_cluster_snapshot.assert_called_once()

def test_copy_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import copy_db_parameter_group
    mock_client = MagicMock()
    mock_client.copy_db_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    copy_db_parameter_group("test-source_db_parameter_group_identifier", "test-target_db_parameter_group_identifier", "test-target_db_parameter_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_db_parameter_group.assert_called_once()

def test_copy_db_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import copy_db_snapshot
    mock_client = MagicMock()
    mock_client.copy_db_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    copy_db_snapshot("test-source_db_snapshot_identifier", "test-target_db_snapshot_identifier", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], copy_tags=[{"Key": "k", "Value": "v"}], pre_signed_url="test-pre_signed_url", option_group_name="test-option_group_name", target_custom_availability_zone="test-target_custom_availability_zone", snapshot_target="test-snapshot_target", copy_option_group="test-copy_option_group", snapshot_availability_zone="test-snapshot_availability_zone", source_region="test-source_region", region_name="us-east-1")
    mock_client.copy_db_snapshot.assert_called_once()

def test_copy_option_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import copy_option_group
    mock_client = MagicMock()
    mock_client.copy_option_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    copy_option_group("test-source_option_group_identifier", "test-target_option_group_identifier", "test-target_option_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_option_group.assert_called_once()

def test_create_blue_green_deployment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_blue_green_deployment
    mock_client = MagicMock()
    mock_client.create_blue_green_deployment.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_blue_green_deployment("test-blue_green_deployment_name", "test-source", target_engine_version="test-target_engine_version", target_db_parameter_group_name="test-target_db_parameter_group_name", target_db_cluster_parameter_group_name="test-target_db_cluster_parameter_group_name", tags=[{"Key": "k", "Value": "v"}], target_db_instance_class="test-target_db_instance_class", upgrade_target_storage_config={}, target_iops="test-target_iops", target_storage_type="test-target_storage_type", target_allocated_storage="test-target_allocated_storage", target_storage_throughput="test-target_storage_throughput", region_name="us-east-1")
    mock_client.create_blue_green_deployment.assert_called_once()

def test_create_custom_db_engine_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_custom_db_engine_version
    mock_client = MagicMock()
    mock_client.create_custom_db_engine_version.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_custom_db_engine_version("test-engine", "test-engine_version", database_installation_files_s3_bucket_name="test-database_installation_files_s3_bucket_name", database_installation_files_s3_prefix="test-database_installation_files_s3_prefix", image_id="test-image_id", kms_key_id="test-kms_key_id", source_custom_db_engine_version_identifier="test-source_custom_db_engine_version_identifier", use_aws_provided_latest_image=True, description="test-description", manifest="test-manifest", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_custom_db_engine_version.assert_called_once()

def test_create_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_cluster
    mock_client = MagicMock()
    mock_client.create_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_cluster("test-db_cluster_identifier", "test-engine", availability_zones="test-availability_zones", backup_retention_period="test-backup_retention_period", character_set_name="test-character_set_name", database_name="test-database_name", db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", vpc_security_group_ids="test-vpc_security_group_ids", db_subnet_group_name="test-db_subnet_group_name", engine_version="test-engine_version", port=1, master_username="test-master_username", master_user_password="test-master_user_password", option_group_name="test-option_group_name", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", replication_source_identifier="test-replication_source_identifier", tags=[{"Key": "k", "Value": "v"}], storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, engine_mode="test-engine_mode", scaling_configuration={}, rds_custom_cluster_configuration={}, db_cluster_instance_class="test-db_cluster_instance_class", allocated_storage="test-allocated_storage", storage_type="test-storage_type", iops="test-iops", publicly_accessible="test-publicly_accessible", auto_minor_version_upgrade=True, deletion_protection="test-deletion_protection", global_cluster_identifier="test-global_cluster_identifier", enable_http_endpoint=True, copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", enable_global_write_forwarding=True, network_type="test-network_type", serverless_v2_scaling_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_limitless_database=True, cluster_scalability_type="test-cluster_scalability_type", db_system_id="test-db_system_id", manage_master_user_password="test-manage_master_user_password", enable_local_write_forwarding=True, master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, master_user_authentication_type="test-master_user_authentication_type", source_region="test-source_region", region_name="us-east-1")
    mock_client.create_db_cluster.assert_called_once()

def test_create_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_cluster_endpoint
    mock_client = MagicMock()
    mock_client.create_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_cluster_endpoint("test-db_cluster_identifier", "test-db_cluster_endpoint_identifier", "test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_cluster_endpoint.assert_called_once()

def test_create_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.create_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_cluster_parameter_group("test-db_cluster_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_cluster_parameter_group.assert_called_once()

def test_create_db_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_cluster_snapshot
    mock_client = MagicMock()
    mock_client.create_db_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_cluster_snapshot("test-db_cluster_snapshot_identifier", "test-db_cluster_identifier", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_cluster_snapshot.assert_called_once()

def test_create_db_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_instance
    mock_client = MagicMock()
    mock_client.create_db_instance.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_instance("test-db_instance_identifier", "test-db_instance_class", "test-engine", db_name="test-db_name", allocated_storage="test-allocated_storage", master_username="test-master_username", master_user_password="test-master_user_password", db_security_groups="test-db_security_groups", vpc_security_group_ids="test-vpc_security_group_ids", availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", preferred_maintenance_window="test-preferred_maintenance_window", db_parameter_group_name="test-db_parameter_group_name", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", port=1, multi_az=True, engine_version="test-engine_version", auto_minor_version_upgrade=True, license_model="test-license_model", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", character_set_name="test-character_set_name", nchar_character_set_name="test-nchar_character_set_name", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], db_cluster_identifier="test-db_cluster_identifier", storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", domain="test-domain", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", domain_iam_role_name="test-domain_iam_role_name", promotion_tier="test-promotion_tier", timezone="test-timezone", enable_iam_database_authentication=True, database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", deletion_protection="test-deletion_protection", max_allocated_storage=1, enable_customer_owned_ip=True, network_type="test-network_type", backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", db_system_id="test-db_system_id", ca_certificate_identifier="test-ca_certificate_identifier", manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", multi_tenant=True, dedicated_log_volume="test-dedicated_log_volume", engine_lifecycle_support=1, master_user_authentication_type="test-master_user_authentication_type", region_name="us-east-1")
    mock_client.create_db_instance.assert_called_once()

def test_create_db_instance_read_replica_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_instance_read_replica
    mock_client = MagicMock()
    mock_client.create_db_instance_read_replica.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_instance_read_replica("test-db_instance_identifier", source_db_instance_identifier="test-source_db_instance_identifier", db_instance_class="test-db_instance_class", availability_zone="test-availability_zone", port=1, multi_az=True, auto_minor_version_upgrade=True, iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", db_parameter_group_name="test-db_parameter_group_name", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], db_subnet_group_name="test-db_subnet_group_name", vpc_security_group_ids="test-vpc_security_group_ids", storage_type="test-storage_type", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", enable_iam_database_authentication=True, database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, deletion_protection="test-deletion_protection", domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", replica_mode="test-replica_mode", enable_customer_owned_ip=True, network_type="test-network_type", max_allocated_storage=1, backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", allocated_storage="test-allocated_storage", source_db_cluster_identifier="test-source_db_cluster_identifier", dedicated_log_volume="test-dedicated_log_volume", upgrade_storage_config={}, ca_certificate_identifier="test-ca_certificate_identifier", source_region="test-source_region", region_name="us-east-1")
    mock_client.create_db_instance_read_replica.assert_called_once()

def test_create_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_parameter_group
    mock_client = MagicMock()
    mock_client.create_db_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_parameter_group("test-db_parameter_group_name", "test-db_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_parameter_group.assert_called_once()

def test_create_db_proxy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_proxy
    mock_client = MagicMock()
    mock_client.create_db_proxy.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_proxy("test-db_proxy_name", "test-engine_family", "test-role_arn", "test-vpc_subnet_ids", default_auth_scheme="test-default_auth_scheme", auth="test-auth", vpc_security_group_ids="test-vpc_security_group_ids", require_tls=True, idle_client_timeout=1, debug_logging="test-debug_logging", tags=[{"Key": "k", "Value": "v"}], endpoint_network_type="test-endpoint_network_type", target_connection_network_type="test-target_connection_network_type", region_name="us-east-1")
    mock_client.create_db_proxy.assert_called_once()

def test_create_db_proxy_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_proxy_endpoint
    mock_client = MagicMock()
    mock_client.create_db_proxy_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_proxy_endpoint("test-db_proxy_name", "test-db_proxy_endpoint_name", "test-vpc_subnet_ids", vpc_security_group_ids="test-vpc_security_group_ids", target_role="test-target_role", tags=[{"Key": "k", "Value": "v"}], endpoint_network_type="test-endpoint_network_type", region_name="us-east-1")
    mock_client.create_db_proxy_endpoint.assert_called_once()

def test_create_db_security_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_security_group
    mock_client = MagicMock()
    mock_client.create_db_security_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_security_group("test-db_security_group_name", "test-db_security_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_security_group.assert_called_once()

def test_create_db_shard_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_shard_group
    mock_client = MagicMock()
    mock_client.create_db_shard_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_shard_group("test-db_shard_group_identifier", "test-db_cluster_identifier", 1, compute_redundancy="test-compute_redundancy", min_acu="test-min_acu", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_shard_group.assert_called_once()

def test_create_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_db_subnet_group
    mock_client = MagicMock()
    mock_client.create_db_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_db_subnet_group("test-db_subnet_group_name", "test-db_subnet_group_description", "test-subnet_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_db_subnet_group.assert_called_once()

def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_event_subscription
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", source_ids="test-source_ids", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_subscription.assert_called_once()

def test_create_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_global_cluster
    mock_client = MagicMock()
    mock_client.create_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_global_cluster("test-global_cluster_identifier", source_db_cluster_identifier="test-source_db_cluster_identifier", engine="test-engine", engine_version="test-engine_version", engine_lifecycle_support=1, deletion_protection="test-deletion_protection", database_name="test-database_name", storage_encrypted="test-storage_encrypted", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_global_cluster.assert_called_once()

def test_create_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_integration
    mock_client = MagicMock()
    mock_client.create_integration.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_integration("test-source_arn", "test-target_arn", "test-integration_name", kms_key_id="test-kms_key_id", additional_encryption_context={}, tags=[{"Key": "k", "Value": "v"}], data_filter=[{}], description="test-description", region_name="us-east-1")
    mock_client.create_integration.assert_called_once()

def test_create_option_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_option_group
    mock_client = MagicMock()
    mock_client.create_option_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_option_group("test-option_group_name", "test-engine_name", "test-major_engine_version", "test-option_group_description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_option_group.assert_called_once()

def test_create_tenant_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import create_tenant_database
    mock_client = MagicMock()
    mock_client.create_tenant_database.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    create_tenant_database("test-db_instance_identifier", "test-tenant_db_name", "test-master_username", master_user_password="test-master_user_password", character_set_name="test-character_set_name", nchar_character_set_name="test-nchar_character_set_name", manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_tenant_database.assert_called_once()

def test_delete_blue_green_deployment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import delete_blue_green_deployment
    mock_client = MagicMock()
    mock_client.delete_blue_green_deployment.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    delete_blue_green_deployment("test-blue_green_deployment_identifier", delete_target=True, region_name="us-east-1")
    mock_client.delete_blue_green_deployment.assert_called_once()

def test_delete_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import delete_db_cluster
    mock_client = MagicMock()
    mock_client.delete_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    delete_db_cluster("test-db_cluster_identifier", skip_final_snapshot=True, final_db_snapshot_identifier="test-final_db_snapshot_identifier", delete_automated_backups=True, region_name="us-east-1")
    mock_client.delete_db_cluster.assert_called_once()

def test_delete_db_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import delete_db_instance
    mock_client = MagicMock()
    mock_client.delete_db_instance.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    delete_db_instance("test-db_instance_identifier", skip_final_snapshot=True, final_db_snapshot_identifier="test-final_db_snapshot_identifier", delete_automated_backups=True, region_name="us-east-1")
    mock_client.delete_db_instance.assert_called_once()

def test_delete_db_instance_automated_backup_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import delete_db_instance_automated_backup
    mock_client = MagicMock()
    mock_client.delete_db_instance_automated_backup.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    delete_db_instance_automated_backup(dbi_resource_id="test-dbi_resource_id", db_instance_automated_backups_arn="test-db_instance_automated_backups_arn", region_name="us-east-1")
    mock_client.delete_db_instance_automated_backup.assert_called_once()

def test_delete_tenant_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import delete_tenant_database
    mock_client = MagicMock()
    mock_client.delete_tenant_database.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    delete_tenant_database("test-db_instance_identifier", "test-tenant_db_name", skip_final_snapshot=True, final_db_snapshot_identifier="test-final_db_snapshot_identifier", region_name="us-east-1")
    mock_client.delete_tenant_database.assert_called_once()

def test_deregister_db_proxy_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import deregister_db_proxy_targets
    mock_client = MagicMock()
    mock_client.deregister_db_proxy_targets.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    deregister_db_proxy_targets("test-db_proxy_name", target_group_name="test-target_group_name", db_instance_identifiers="test-db_instance_identifiers", db_cluster_identifiers="test-db_cluster_identifiers", region_name="us-east-1")
    mock_client.deregister_db_proxy_targets.assert_called_once()

def test_describe_blue_green_deployments_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_blue_green_deployments
    mock_client = MagicMock()
    mock_client.describe_blue_green_deployments.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_blue_green_deployments(blue_green_deployment_identifier="test-blue_green_deployment_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_blue_green_deployments.assert_called_once()

def test_describe_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_certificates
    mock_client = MagicMock()
    mock_client.describe_certificates.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_certificates(certificate_identifier="test-certificate_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_certificates.assert_called_once()

def test_describe_db_cluster_automated_backups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_cluster_automated_backups
    mock_client = MagicMock()
    mock_client.describe_db_cluster_automated_backups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_automated_backups(db_cluster_resource_id="test-db_cluster_resource_id", db_cluster_identifier="test-db_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_automated_backups.assert_called_once()

def test_describe_db_cluster_backtracks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_cluster_backtracks
    mock_client = MagicMock()
    mock_client.describe_db_cluster_backtracks.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_backtracks("test-db_cluster_identifier", backtrack_identifier="test-backtrack_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_backtracks.assert_called_once()

def test_describe_db_cluster_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_cluster_endpoints
    mock_client = MagicMock()
    mock_client.describe_db_cluster_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_endpoints(db_cluster_identifier="test-db_cluster_identifier", db_cluster_endpoint_identifier="test-db_cluster_endpoint_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_endpoints.assert_called_once()

def test_describe_db_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_cluster_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameter_groups(db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_parameter_groups.assert_called_once()

def test_describe_db_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_db_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_parameters("test-db_cluster_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_cluster_parameters.assert_called_once()

def test_describe_db_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_cluster_snapshots
    mock_client = MagicMock()
    mock_client.describe_db_cluster_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_cluster_snapshots(db_cluster_identifier="test-db_cluster_identifier", db_cluster_snapshot_identifier="test-db_cluster_snapshot_identifier", snapshot_type="test-snapshot_type", filters=[{}], max_records=1, marker="test-marker", include_shared=True, include_public=True, db_cluster_resource_id="test-db_cluster_resource_id", region_name="us-east-1")
    mock_client.describe_db_cluster_snapshots.assert_called_once()

def test_describe_db_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_clusters
    mock_client = MagicMock()
    mock_client.describe_db_clusters.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_clusters(db_cluster_identifier="test-db_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", include_shared=True, region_name="us-east-1")
    mock_client.describe_db_clusters.assert_called_once()

def test_describe_db_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_engine_versions
    mock_client = MagicMock()
    mock_client.describe_db_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_engine_versions(engine="test-engine", engine_version="test-engine_version", db_parameter_group_family="test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", default_only="test-default_only", list_supported_character_sets=1, list_supported_timezones=1, include_all=True, region_name="us-east-1")
    mock_client.describe_db_engine_versions.assert_called_once()

def test_describe_db_instance_automated_backups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_instance_automated_backups
    mock_client = MagicMock()
    mock_client.describe_db_instance_automated_backups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_instance_automated_backups(dbi_resource_id="test-dbi_resource_id", db_instance_identifier="test-db_instance_identifier", filters=[{}], max_records=1, marker="test-marker", db_instance_automated_backups_arn="test-db_instance_automated_backups_arn", region_name="us-east-1")
    mock_client.describe_db_instance_automated_backups.assert_called_once()

def test_describe_db_log_files_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_log_files
    mock_client = MagicMock()
    mock_client.describe_db_log_files.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_log_files("test-db_instance_identifier", filename_contains="test-filename_contains", file_last_written="test-file_last_written", file_size=1, filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_log_files.assert_called_once()

def test_describe_db_major_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_major_engine_versions
    mock_client = MagicMock()
    mock_client.describe_db_major_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_major_engine_versions(engine="test-engine", major_engine_version="test-major_engine_version", marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_db_major_engine_versions.assert_called_once()

def test_describe_db_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_db_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_parameter_groups(db_parameter_group_name="test-db_parameter_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_parameter_groups.assert_called_once()

def test_describe_db_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_parameters
    mock_client = MagicMock()
    mock_client.describe_db_parameters.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_parameters("test-db_parameter_group_name", source="test-source", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_parameters.assert_called_once()

def test_describe_db_proxies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_proxies
    mock_client = MagicMock()
    mock_client.describe_db_proxies.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_proxies(db_proxy_name="test-db_proxy_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_db_proxies.assert_called_once()

def test_describe_db_proxy_endpoints_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_proxy_endpoints
    mock_client = MagicMock()
    mock_client.describe_db_proxy_endpoints.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_proxy_endpoints(db_proxy_name="test-db_proxy_name", db_proxy_endpoint_name="test-db_proxy_endpoint_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_db_proxy_endpoints.assert_called_once()

def test_describe_db_proxy_target_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_proxy_target_groups
    mock_client = MagicMock()
    mock_client.describe_db_proxy_target_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_proxy_target_groups("test-db_proxy_name", target_group_name="test-target_group_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_db_proxy_target_groups.assert_called_once()

def test_describe_db_proxy_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_proxy_targets
    mock_client = MagicMock()
    mock_client.describe_db_proxy_targets.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_proxy_targets("test-db_proxy_name", target_group_name="test-target_group_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_db_proxy_targets.assert_called_once()

def test_describe_db_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_recommendations
    mock_client = MagicMock()
    mock_client.describe_db_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_recommendations(last_updated_after="test-last_updated_after", last_updated_before="test-last_updated_before", locale="test-locale", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_recommendations.assert_called_once()

def test_describe_db_security_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_security_groups
    mock_client = MagicMock()
    mock_client.describe_db_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_security_groups(db_security_group_name="test-db_security_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_security_groups.assert_called_once()

def test_describe_db_shard_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_shard_groups
    mock_client = MagicMock()
    mock_client.describe_db_shard_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_shard_groups(db_shard_group_identifier="test-db_shard_group_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_db_shard_groups.assert_called_once()

def test_describe_db_snapshot_tenant_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_snapshot_tenant_databases
    mock_client = MagicMock()
    mock_client.describe_db_snapshot_tenant_databases.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_snapshot_tenant_databases(db_instance_identifier="test-db_instance_identifier", db_snapshot_identifier="test-db_snapshot_identifier", snapshot_type="test-snapshot_type", filters=[{}], max_records=1, marker="test-marker", dbi_resource_id="test-dbi_resource_id", region_name="us-east-1")
    mock_client.describe_db_snapshot_tenant_databases.assert_called_once()

def test_describe_db_subnet_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_db_subnet_groups
    mock_client = MagicMock()
    mock_client.describe_db_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_db_subnet_groups(db_subnet_group_name="test-db_subnet_group_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_db_subnet_groups.assert_called_once()

def test_describe_engine_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_engine_default_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_engine_default_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_cluster_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_default_cluster_parameters.assert_called_once()

def test_describe_engine_default_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_engine_default_parameters
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_parameters("test-db_parameter_group_family", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_default_parameters.assert_called_once()

def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_event_categories
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_event_categories(source_type="test-source_type", filters=[{}], region_name="us-east-1")
    mock_client.describe_event_categories.assert_called_once()

def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_event_subscriptions
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(subscription_name="test-subscription_name", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_event_subscriptions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, event_categories="test-event_categories", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_export_tasks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_export_tasks
    mock_client = MagicMock()
    mock_client.describe_export_tasks.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_export_tasks(export_task_identifier=1, source_arn="test-source_arn", filters=[{}], marker="test-marker", max_records=1, source_type="test-source_type", region_name="us-east-1")
    mock_client.describe_export_tasks.assert_called_once()

def test_describe_global_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_global_clusters
    mock_client = MagicMock()
    mock_client.describe_global_clusters.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_global_clusters(global_cluster_identifier="test-global_cluster_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_global_clusters.assert_called_once()

def test_describe_integrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_integrations
    mock_client = MagicMock()
    mock_client.describe_integrations.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_integrations(integration_identifier="test-integration_identifier", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_integrations.assert_called_once()

def test_describe_option_group_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_option_group_options
    mock_client = MagicMock()
    mock_client.describe_option_group_options.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_option_group_options("test-engine_name", major_engine_version="test-major_engine_version", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_option_group_options.assert_called_once()

def test_describe_option_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_option_groups
    mock_client = MagicMock()
    mock_client.describe_option_groups.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_option_groups(option_group_name="test-option_group_name", filters=[{}], marker="test-marker", max_records=1, engine_name="test-engine_name", major_engine_version="test-major_engine_version", region_name="us-east-1")
    mock_client.describe_option_groups.assert_called_once()

def test_describe_orderable_db_instance_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_orderable_db_instance_options
    mock_client = MagicMock()
    mock_client.describe_orderable_db_instance_options.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_orderable_db_instance_options("test-engine", engine_version="test-engine_version", db_instance_class="test-db_instance_class", license_model="test-license_model", availability_zone_group="test-availability_zone_group", vpc="test-vpc", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_orderable_db_instance_options.assert_called_once()

def test_describe_pending_maintenance_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_pending_maintenance_actions
    mock_client = MagicMock()
    mock_client.describe_pending_maintenance_actions.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_pending_maintenance_actions(resource_identifier="test-resource_identifier", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_pending_maintenance_actions.assert_called_once()

def test_describe_reserved_db_instances_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_reserved_db_instances
    mock_client = MagicMock()
    mock_client.describe_reserved_db_instances.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_reserved_db_instances(reserved_db_instance_id="test-reserved_db_instance_id", reserved_db_instances_offering_id="test-reserved_db_instances_offering_id", db_instance_class="test-db_instance_class", duration=1, product_description="test-product_description", offering_type="test-offering_type", multi_az=True, lease_id="test-lease_id", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_db_instances.assert_called_once()

def test_describe_reserved_db_instances_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_reserved_db_instances_offerings
    mock_client = MagicMock()
    mock_client.describe_reserved_db_instances_offerings.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_reserved_db_instances_offerings(reserved_db_instances_offering_id="test-reserved_db_instances_offering_id", db_instance_class="test-db_instance_class", duration=1, product_description="test-product_description", offering_type="test-offering_type", multi_az=True, filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_db_instances_offerings.assert_called_once()

def test_describe_source_regions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_source_regions
    mock_client = MagicMock()
    mock_client.describe_source_regions.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_source_regions(target_region_name="test-target_region_name", max_records=1, marker="test-marker", filters=[{}], region_name="us-east-1")
    mock_client.describe_source_regions.assert_called_once()

def test_describe_tenant_databases_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import describe_tenant_databases
    mock_client = MagicMock()
    mock_client.describe_tenant_databases.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    describe_tenant_databases(db_instance_identifier="test-db_instance_identifier", tenant_db_name="test-tenant_db_name", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_tenant_databases.assert_called_once()

def test_download_db_log_file_portion_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import download_db_log_file_portion
    mock_client = MagicMock()
    mock_client.download_db_log_file_portion.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    download_db_log_file_portion("test-db_instance_identifier", "test-log_file_name", marker="test-marker", number_of_lines="test-number_of_lines", region_name="us-east-1")
    mock_client.download_db_log_file_portion.assert_called_once()

def test_failover_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import failover_db_cluster
    mock_client = MagicMock()
    mock_client.failover_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    failover_db_cluster("test-db_cluster_identifier", target_db_instance_identifier="test-target_db_instance_identifier", region_name="us-east-1")
    mock_client.failover_db_cluster.assert_called_once()

def test_failover_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import failover_global_cluster
    mock_client = MagicMock()
    mock_client.failover_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    failover_global_cluster("test-global_cluster_identifier", "test-target_db_cluster_identifier", allow_data_loss=True, switchover="test-switchover", region_name="us-east-1")
    mock_client.failover_global_cluster.assert_called_once()

def test_list_tags_for_resource_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import list_tags_for_resource
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_name", filters=[{}], region_name="us-east-1")
    mock_client.list_tags_for_resource.assert_called_once()

def test_modify_activity_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_activity_stream
    mock_client = MagicMock()
    mock_client.modify_activity_stream.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_activity_stream(resource_arn="test-resource_arn", audit_policy_state="test-audit_policy_state", region_name="us-east-1")
    mock_client.modify_activity_stream.assert_called_once()

def test_modify_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_certificates
    mock_client = MagicMock()
    mock_client.modify_certificates.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_certificates(certificate_identifier="test-certificate_identifier", remove_customer_override="test-remove_customer_override", region_name="us-east-1")
    mock_client.modify_certificates.assert_called_once()

def test_modify_current_db_cluster_capacity_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_current_db_cluster_capacity
    mock_client = MagicMock()
    mock_client.modify_current_db_cluster_capacity.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_current_db_cluster_capacity("test-db_cluster_identifier", capacity="test-capacity", seconds_before_timeout=1, timeout_action=1, region_name="us-east-1")
    mock_client.modify_current_db_cluster_capacity.assert_called_once()

def test_modify_custom_db_engine_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_custom_db_engine_version
    mock_client = MagicMock()
    mock_client.modify_custom_db_engine_version.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_custom_db_engine_version("test-engine", "test-engine_version", description="test-description", status="test-status", region_name="us-east-1")
    mock_client.modify_custom_db_engine_version.assert_called_once()

def test_modify_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_cluster
    mock_client = MagicMock()
    mock_client.modify_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_cluster("test-db_cluster_identifier", new_db_cluster_identifier="test-new_db_cluster_identifier", apply_immediately=True, backup_retention_period="test-backup_retention_period", db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", vpc_security_group_ids="test-vpc_security_group_ids", port=1, master_user_password="test-master_user_password", option_group_name="test-option_group_name", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", cloudwatch_logs_export_configuration=1, engine_version="test-engine_version", allow_major_version_upgrade=True, db_instance_parameter_group_name="test-db_instance_parameter_group_name", domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", scaling_configuration={}, deletion_protection="test-deletion_protection", enable_http_endpoint=True, copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], enable_global_write_forwarding=True, db_cluster_instance_class="test-db_cluster_instance_class", allocated_storage="test-allocated_storage", storage_type="test-storage_type", iops="test-iops", auto_minor_version_upgrade=True, network_type="test-network_type", serverless_v2_scaling_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", manage_master_user_password="test-manage_master_user_password", rotate_master_user_password="test-rotate_master_user_password", enable_local_write_forwarding=True, master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", engine_mode="test-engine_mode", allow_engine_mode_change=True, aws_backup_recovery_point_arn="test-aws_backup_recovery_point_arn", enable_limitless_database=True, ca_certificate_identifier="test-ca_certificate_identifier", master_user_authentication_type="test-master_user_authentication_type", region_name="us-east-1")
    mock_client.modify_db_cluster.assert_called_once()

def test_modify_db_cluster_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_cluster_endpoint
    mock_client = MagicMock()
    mock_client.modify_db_cluster_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_endpoint("test-db_cluster_endpoint_identifier", endpoint_type="test-endpoint_type", static_members="test-static_members", excluded_members="test-excluded_members", region_name="us-east-1")
    mock_client.modify_db_cluster_endpoint.assert_called_once()

def test_modify_db_cluster_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_cluster_snapshot_attribute
    mock_client = MagicMock()
    mock_client.modify_db_cluster_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_cluster_snapshot_attribute("test-db_cluster_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.modify_db_cluster_snapshot_attribute.assert_called_once()

def test_modify_db_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_instance
    mock_client = MagicMock()
    mock_client.modify_db_instance.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_instance("test-db_instance_identifier", allocated_storage="test-allocated_storage", db_instance_class="test-db_instance_class", db_subnet_group_name="test-db_subnet_group_name", db_security_groups="test-db_security_groups", vpc_security_group_ids="test-vpc_security_group_ids", apply_immediately=True, master_user_password="test-master_user_password", db_parameter_group_name="test-db_parameter_group_name", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", multi_az=True, engine_version="test-engine_version", allow_major_version_upgrade=True, auto_minor_version_upgrade=True, license_model="test-license_model", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", new_db_instance_identifier="test-new_db_instance_identifier", storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", ca_certificate_identifier="test-ca_certificate_identifier", domain="test-domain", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", disable_domain=True, copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", db_port_number=1, publicly_accessible="test-publicly_accessible", monitoring_role_arn="test-monitoring_role_arn", domain_iam_role_name="test-domain_iam_role_name", promotion_tier="test-promotion_tier", enable_iam_database_authentication=True, database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", cloudwatch_logs_export_configuration=1, processor_features="test-processor_features", use_default_processor_features=True, deletion_protection="test-deletion_protection", max_allocated_storage=1, certificate_rotation_restart="test-certificate_rotation_restart", replica_mode="test-replica_mode", automation_mode=True, resume_full_automation_mode_minutes="test-resume_full_automation_mode_minutes", enable_customer_owned_ip=True, network_type="test-network_type", aws_backup_recovery_point_arn="test-aws_backup_recovery_point_arn", manage_master_user_password="test-manage_master_user_password", rotate_master_user_password="test-rotate_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", multi_tenant=True, dedicated_log_volume="test-dedicated_log_volume", engine="test-engine", master_user_authentication_type="test-master_user_authentication_type", region_name="us-east-1")
    mock_client.modify_db_instance.assert_called_once()

def test_modify_db_proxy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_proxy
    mock_client = MagicMock()
    mock_client.modify_db_proxy.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_proxy("test-db_proxy_name", new_db_proxy_name="test-new_db_proxy_name", default_auth_scheme="test-default_auth_scheme", auth="test-auth", require_tls=True, idle_client_timeout=1, debug_logging="test-debug_logging", role_arn="test-role_arn", security_groups="test-security_groups", region_name="us-east-1")
    mock_client.modify_db_proxy.assert_called_once()

def test_modify_db_proxy_endpoint_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_proxy_endpoint
    mock_client = MagicMock()
    mock_client.modify_db_proxy_endpoint.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_proxy_endpoint("test-db_proxy_endpoint_name", new_db_proxy_endpoint_name="test-new_db_proxy_endpoint_name", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.modify_db_proxy_endpoint.assert_called_once()

def test_modify_db_proxy_target_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_proxy_target_group
    mock_client = MagicMock()
    mock_client.modify_db_proxy_target_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_proxy_target_group("test-target_group_name", "test-db_proxy_name", connection_pool_config={}, new_name="test-new_name", region_name="us-east-1")
    mock_client.modify_db_proxy_target_group.assert_called_once()

def test_modify_db_recommendation_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_recommendation
    mock_client = MagicMock()
    mock_client.modify_db_recommendation.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_recommendation("test-recommendation_id", locale="test-locale", status="test-status", recommended_action_updates="test-recommended_action_updates", region_name="us-east-1")
    mock_client.modify_db_recommendation.assert_called_once()

def test_modify_db_shard_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_shard_group
    mock_client = MagicMock()
    mock_client.modify_db_shard_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_shard_group("test-db_shard_group_identifier", max_acu=1, min_acu="test-min_acu", compute_redundancy="test-compute_redundancy", region_name="us-east-1")
    mock_client.modify_db_shard_group.assert_called_once()

def test_modify_db_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_snapshot
    mock_client = MagicMock()
    mock_client.modify_db_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_snapshot("test-db_snapshot_identifier", engine_version="test-engine_version", option_group_name="test-option_group_name", region_name="us-east-1")
    mock_client.modify_db_snapshot.assert_called_once()

def test_modify_db_snapshot_attribute_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_snapshot_attribute
    mock_client = MagicMock()
    mock_client.modify_db_snapshot_attribute.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_snapshot_attribute("test-db_snapshot_identifier", "test-attribute_name", values_to_add="test-values_to_add", values_to_remove="test-values_to_remove", region_name="us-east-1")
    mock_client.modify_db_snapshot_attribute.assert_called_once()

def test_modify_db_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_db_subnet_group
    mock_client = MagicMock()
    mock_client.modify_db_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_db_subnet_group("test-db_subnet_group_name", "test-subnet_ids", db_subnet_group_description="test-db_subnet_group_description", region_name="us-east-1")
    mock_client.modify_db_subnet_group.assert_called_once()

def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_event_subscription
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", event_categories="test-event_categories", enabled=True, region_name="us-east-1")
    mock_client.modify_event_subscription.assert_called_once()

def test_modify_global_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_global_cluster
    mock_client = MagicMock()
    mock_client.modify_global_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_global_cluster("test-global_cluster_identifier", new_global_cluster_identifier="test-new_global_cluster_identifier", deletion_protection="test-deletion_protection", engine_version="test-engine_version", allow_major_version_upgrade=True, region_name="us-east-1")
    mock_client.modify_global_cluster.assert_called_once()

def test_modify_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_integration
    mock_client = MagicMock()
    mock_client.modify_integration.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_integration("test-integration_identifier", integration_name="test-integration_name", data_filter=[{}], description="test-description", region_name="us-east-1")
    mock_client.modify_integration.assert_called_once()

def test_modify_option_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_option_group
    mock_client = MagicMock()
    mock_client.modify_option_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_option_group("test-option_group_name", options_to_include={}, options_to_remove={}, apply_immediately=True, region_name="us-east-1")
    mock_client.modify_option_group.assert_called_once()

def test_modify_tenant_database_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import modify_tenant_database
    mock_client = MagicMock()
    mock_client.modify_tenant_database.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    modify_tenant_database("test-db_instance_identifier", "test-tenant_db_name", master_user_password="test-master_user_password", new_tenant_db_name="test-new_tenant_db_name", manage_master_user_password="test-manage_master_user_password", rotate_master_user_password="test-rotate_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", region_name="us-east-1")
    mock_client.modify_tenant_database.assert_called_once()

def test_promote_read_replica_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import promote_read_replica
    mock_client = MagicMock()
    mock_client.promote_read_replica.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    promote_read_replica("test-db_instance_identifier", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", region_name="us-east-1")
    mock_client.promote_read_replica.assert_called_once()

def test_purchase_reserved_db_instances_offering_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import purchase_reserved_db_instances_offering
    mock_client = MagicMock()
    mock_client.purchase_reserved_db_instances_offering.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_db_instances_offering("test-reserved_db_instances_offering_id", reserved_db_instance_id="test-reserved_db_instance_id", db_instance_count=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.purchase_reserved_db_instances_offering.assert_called_once()

def test_reboot_db_instance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import reboot_db_instance
    mock_client = MagicMock()
    mock_client.reboot_db_instance.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    reboot_db_instance("test-db_instance_identifier", force_failover=True, region_name="us-east-1")
    mock_client.reboot_db_instance.assert_called_once()

def test_register_db_proxy_targets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import register_db_proxy_targets
    mock_client = MagicMock()
    mock_client.register_db_proxy_targets.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    register_db_proxy_targets("test-db_proxy_name", target_group_name="test-target_group_name", db_instance_identifiers="test-db_instance_identifiers", db_cluster_identifiers="test-db_cluster_identifiers", region_name="us-east-1")
    mock_client.register_db_proxy_targets.assert_called_once()

def test_remove_role_from_db_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import remove_role_from_db_cluster
    mock_client = MagicMock()
    mock_client.remove_role_from_db_cluster.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    remove_role_from_db_cluster("test-db_cluster_identifier", "test-role_arn", feature_name="test-feature_name", region_name="us-east-1")
    mock_client.remove_role_from_db_cluster.assert_called_once()

def test_reset_db_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import reset_db_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.reset_db_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    reset_db_cluster_parameter_group("test-db_cluster_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.reset_db_cluster_parameter_group.assert_called_once()

def test_reset_db_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import reset_db_parameter_group
    mock_client = MagicMock()
    mock_client.reset_db_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    reset_db_parameter_group("test-db_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.reset_db_parameter_group.assert_called_once()

def test_restore_db_cluster_from_s3_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import restore_db_cluster_from_s3
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_s3.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_from_s3("test-db_cluster_identifier", "test-engine", "test-master_username", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", availability_zones="test-availability_zones", backup_retention_period="test-backup_retention_period", character_set_name="test-character_set_name", database_name="test-database_name", db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", vpc_security_group_ids="test-vpc_security_group_ids", db_subnet_group_name="test-db_subnet_group_name", engine_version="test-engine_version", port=1, master_user_password="test-master_user_password", option_group_name="test-option_group_name", preferred_backup_window="test-preferred_backup_window", preferred_maintenance_window="test-preferred_maintenance_window", tags=[{"Key": "k", "Value": "v"}], storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, s3_prefix="test-s3_prefix", backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", storage_type="test-storage_type", network_type="test-network_type", serverless_v2_scaling_configuration={}, manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.restore_db_cluster_from_s3.assert_called_once()

def test_restore_db_cluster_from_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import restore_db_cluster_from_snapshot
    mock_client = MagicMock()
    mock_client.restore_db_cluster_from_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_from_snapshot("test-db_cluster_identifier", "test-snapshot_identifier", "test-engine", availability_zones="test-availability_zones", engine_version="test-engine_version", port=1, db_subnet_group_name="test-db_subnet_group_name", database_name="test-database_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, engine_mode="test-engine_mode", scaling_configuration={}, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", db_cluster_instance_class="test-db_cluster_instance_class", storage_type="test-storage_type", iops="test-iops", publicly_accessible="test-publicly_accessible", network_type="test-network_type", serverless_v2_scaling_configuration={}, rds_custom_cluster_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.restore_db_cluster_from_snapshot.assert_called_once()

def test_restore_db_cluster_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import restore_db_cluster_to_point_in_time
    mock_client = MagicMock()
    mock_client.restore_db_cluster_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    restore_db_cluster_to_point_in_time("test-db_cluster_identifier", restore_type="test-restore_type", source_db_cluster_identifier="test-source_db_cluster_identifier", restore_to_time="test-restore_to_time", use_latest_restorable_time=True, port=1, db_subnet_group_name="test-db_subnet_group_name", option_group_name="test-option_group_name", vpc_security_group_ids="test-vpc_security_group_ids", tags=[{"Key": "k", "Value": "v"}], kms_key_id="test-kms_key_id", enable_iam_database_authentication=True, backtrack_window="test-backtrack_window", enable_cloudwatch_logs_exports=True, db_cluster_parameter_group_name="test-db_cluster_parameter_group_name", deletion_protection="test-deletion_protection", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", db_cluster_instance_class="test-db_cluster_instance_class", storage_type="test-storage_type", publicly_accessible="test-publicly_accessible", iops="test-iops", network_type="test-network_type", source_db_cluster_resource_id="test-source_db_cluster_resource_id", serverless_v2_scaling_configuration={}, scaling_configuration={}, engine_mode="test-engine_mode", rds_custom_cluster_configuration={}, monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.restore_db_cluster_to_point_in_time.assert_called_once()

def test_restore_db_instance_from_db_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import restore_db_instance_from_db_snapshot
    mock_client = MagicMock()
    mock_client.restore_db_instance_from_db_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    restore_db_instance_from_db_snapshot("test-db_instance_identifier", db_snapshot_identifier="test-db_snapshot_identifier", db_instance_class="test-db_instance_class", port=1, availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", multi_az=True, publicly_accessible="test-publicly_accessible", auto_minor_version_upgrade=True, license_model="test-license_model", db_name="test-db_name", engine="test-engine", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", tags=[{"Key": "k", "Value": "v"}], storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", vpc_security_group_ids="test-vpc_security_group_ids", domain="test-domain", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], domain_iam_role_name="test-domain_iam_role_name", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, db_parameter_group_name="test-db_parameter_group_name", deletion_protection="test-deletion_protection", enable_customer_owned_ip=True, network_type="test-network_type", backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", allocated_storage="test-allocated_storage", db_cluster_snapshot_identifier="test-db_cluster_snapshot_identifier", dedicated_log_volume="test-dedicated_log_volume", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", region_name="us-east-1")
    mock_client.restore_db_instance_from_db_snapshot.assert_called_once()

def test_restore_db_instance_from_s3_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import restore_db_instance_from_s3
    mock_client = MagicMock()
    mock_client.restore_db_instance_from_s3.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    restore_db_instance_from_s3("test-db_instance_identifier", "test-db_instance_class", "test-engine", "test-source_engine", "test-source_engine_version", "test-s3_bucket_name", "test-s3_ingestion_role_arn", db_name="test-db_name", allocated_storage="test-allocated_storage", master_username="test-master_username", master_user_password="test-master_user_password", db_security_groups="test-db_security_groups", vpc_security_group_ids="test-vpc_security_group_ids", availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", preferred_maintenance_window="test-preferred_maintenance_window", db_parameter_group_name="test-db_parameter_group_name", backup_retention_period="test-backup_retention_period", preferred_backup_window="test-preferred_backup_window", port=1, multi_az=True, engine_version="test-engine_version", auto_minor_version_upgrade=True, license_model="test-license_model", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", publicly_accessible="test-publicly_accessible", tags=[{"Key": "k", "Value": "v"}], storage_type="test-storage_type", storage_encrypted="test-storage_encrypted", kms_key_id="test-kms_key_id", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], monitoring_interval="test-monitoring_interval", monitoring_role_arn="test-monitoring_role_arn", enable_iam_database_authentication=True, s3_prefix="test-s3_prefix", database_insights_mode="test-database_insights_mode", enable_performance_insights=True, performance_insights_kms_key_id="test-performance_insights_kms_key_id", performance_insights_retention_period="test-performance_insights_retention_period", enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, deletion_protection="test-deletion_protection", max_allocated_storage=1, network_type="test-network_type", manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", dedicated_log_volume="test-dedicated_log_volume", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, region_name="us-east-1")
    mock_client.restore_db_instance_from_s3.assert_called_once()

def test_restore_db_instance_to_point_in_time_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import restore_db_instance_to_point_in_time
    mock_client = MagicMock()
    mock_client.restore_db_instance_to_point_in_time.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    restore_db_instance_to_point_in_time("test-target_db_instance_identifier", source_db_instance_identifier="test-source_db_instance_identifier", restore_time="test-restore_time", use_latest_restorable_time=True, db_instance_class="test-db_instance_class", port=1, availability_zone="test-availability_zone", db_subnet_group_name="test-db_subnet_group_name", multi_az=True, publicly_accessible="test-publicly_accessible", auto_minor_version_upgrade=True, license_model="test-license_model", db_name="test-db_name", engine="test-engine", iops="test-iops", storage_throughput="test-storage_throughput", option_group_name="test-option_group_name", copy_tags_to_snapshot=[{"Key": "k", "Value": "v"}], tags=[{"Key": "k", "Value": "v"}], storage_type="test-storage_type", tde_credential_arn="test-tde_credential_arn", tde_credential_password="test-tde_credential_password", vpc_security_group_ids="test-vpc_security_group_ids", domain="test-domain", domain_iam_role_name="test-domain_iam_role_name", domain_fqdn="test-domain_fqdn", domain_ou="test-domain_ou", domain_auth_secret_arn="test-domain_auth_secret_arn", domain_dns_ips="test-domain_dns_ips", enable_iam_database_authentication=True, enable_cloudwatch_logs_exports=True, processor_features="test-processor_features", use_default_processor_features=True, db_parameter_group_name="test-db_parameter_group_name", deletion_protection="test-deletion_protection", source_dbi_resource_id="test-source_dbi_resource_id", max_allocated_storage=1, enable_customer_owned_ip=True, network_type="test-network_type", source_db_instance_automated_backups_arn="test-source_db_instance_automated_backups_arn", backup_target="test-backup_target", custom_iam_instance_profile="test-custom_iam_instance_profile", allocated_storage="test-allocated_storage", dedicated_log_volume="test-dedicated_log_volume", ca_certificate_identifier="test-ca_certificate_identifier", engine_lifecycle_support=1, manage_master_user_password="test-manage_master_user_password", master_user_secret_kms_key_id="test-master_user_secret_kms_key_id", region_name="us-east-1")
    mock_client.restore_db_instance_to_point_in_time.assert_called_once()

def test_revoke_db_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import revoke_db_security_group_ingress
    mock_client = MagicMock()
    mock_client.revoke_db_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    revoke_db_security_group_ingress("test-db_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_id="test-ec2_security_group_id", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.revoke_db_security_group_ingress.assert_called_once()

def test_start_activity_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import start_activity_stream
    mock_client = MagicMock()
    mock_client.start_activity_stream.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    start_activity_stream("test-resource_arn", "test-mode", "test-kms_key_id", apply_immediately=True, engine_native_audit_fields_included="test-engine_native_audit_fields_included", region_name="us-east-1")
    mock_client.start_activity_stream.assert_called_once()

def test_start_db_instance_automated_backups_replication_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import start_db_instance_automated_backups_replication
    mock_client = MagicMock()
    mock_client.start_db_instance_automated_backups_replication.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    start_db_instance_automated_backups_replication("test-source_db_instance_arn", backup_retention_period="test-backup_retention_period", kms_key_id="test-kms_key_id", pre_signed_url="test-pre_signed_url", source_region="test-source_region", region_name="us-east-1")
    mock_client.start_db_instance_automated_backups_replication.assert_called_once()

def test_start_export_task_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import start_export_task
    mock_client = MagicMock()
    mock_client.start_export_task.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    start_export_task(1, "test-source_arn", "test-s3_bucket_name", "test-iam_role_arn", "test-kms_key_id", s3_prefix="test-s3_prefix", export_only=1, region_name="us-east-1")
    mock_client.start_export_task.assert_called_once()

def test_stop_activity_stream_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import stop_activity_stream
    mock_client = MagicMock()
    mock_client.stop_activity_stream.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    stop_activity_stream("test-resource_arn", apply_immediately=True, region_name="us-east-1")
    mock_client.stop_activity_stream.assert_called_once()

def test_switchover_blue_green_deployment_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.rds import switchover_blue_green_deployment
    mock_client = MagicMock()
    mock_client.switchover_blue_green_deployment.return_value = {}
    monkeypatch.setattr("aws_util.rds.get_client", lambda *a, **kw: mock_client)
    switchover_blue_green_deployment("test-blue_green_deployment_identifier", switchover_timeout=1, region_name="us-east-1")
    mock_client.switchover_blue_green_deployment.assert_called_once()
