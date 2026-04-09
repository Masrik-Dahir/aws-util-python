"""Tests for aws_util.redshift -- 100% line coverage."""
from __future__ import annotations

import time

import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError

import aws_util.redshift as mod
from aws_util.redshift import (
    ClusterResult,
    LoggingStatus,
    ParameterGroupResult,
    SnapshotResult,
    SubnetGroupResult,
    _parse_cluster,
    _parse_snapshot,
    create_cluster,
    create_cluster_parameter_group,
    create_cluster_snapshot,
    create_cluster_subnet_group,
    delete_cluster,
    delete_cluster_snapshot,
    describe_cluster_snapshots,
    describe_clusters,
    describe_logging_status,
    disable_logging,
    enable_logging,
    modify_cluster,
    reboot_cluster,
    restore_from_cluster_snapshot,
    wait_for_cluster,
    accept_reserved_node_exchange,
    add_partner,
    associate_data_share_consumer,
    authorize_cluster_security_group_ingress,
    authorize_data_share,
    authorize_endpoint_access,
    authorize_snapshot_access,
    batch_delete_cluster_snapshots,
    batch_modify_cluster_snapshots,
    cancel_resize,
    copy_cluster_snapshot,
    create_authentication_profile,
    create_cluster_security_group,
    create_custom_domain_association,
    create_endpoint_access,
    create_event_subscription,
    create_hsm_client_certificate,
    create_hsm_configuration,
    create_integration,
    create_redshift_idc_application,
    create_scheduled_action,
    create_snapshot_copy_grant,
    create_snapshot_schedule,
    create_tags,
    create_usage_limit,
    deauthorize_data_share,
    delete_authentication_profile,
    delete_cluster_parameter_group,
    delete_cluster_security_group,
    delete_cluster_subnet_group,
    delete_custom_domain_association,
    delete_endpoint_access,
    delete_event_subscription,
    delete_hsm_client_certificate,
    delete_hsm_configuration,
    delete_integration,
    delete_partner,
    delete_redshift_idc_application,
    delete_resource_policy,
    delete_scheduled_action,
    delete_snapshot_copy_grant,
    delete_snapshot_schedule,
    delete_tags,
    delete_usage_limit,
    deregister_namespace,
    describe_account_attributes,
    describe_authentication_profiles,
    describe_cluster_db_revisions,
    describe_cluster_parameter_groups,
    describe_cluster_parameters,
    describe_cluster_security_groups,
    describe_cluster_subnet_groups,
    describe_cluster_tracks,
    describe_cluster_versions,
    describe_custom_domain_associations,
    describe_data_shares,
    describe_data_shares_for_consumer,
    describe_data_shares_for_producer,
    describe_default_cluster_parameters,
    describe_endpoint_access,
    describe_endpoint_authorization,
    describe_event_categories,
    describe_event_subscriptions,
    describe_events,
    describe_hsm_client_certificates,
    describe_hsm_configurations,
    describe_inbound_integrations,
    describe_integrations,
    describe_node_configuration_options,
    describe_orderable_cluster_options,
    describe_partners,
    describe_redshift_idc_applications,
    describe_reserved_node_exchange_status,
    describe_reserved_node_offerings,
    describe_reserved_nodes,
    describe_resize,
    describe_scheduled_actions,
    describe_snapshot_copy_grants,
    describe_snapshot_schedules,
    describe_storage,
    describe_table_restore_status,
    describe_tags,
    describe_usage_limits,
    disable_snapshot_copy,
    disassociate_data_share_consumer,
    enable_snapshot_copy,
    failover_primary_compute,
    get_cluster_credentials,
    get_cluster_credentials_with_iam,
    get_identity_center_auth_token,
    get_reserved_node_exchange_configuration_options,
    get_reserved_node_exchange_offerings,
    get_resource_policy,
    list_recommendations,
    modify_aqua_configuration,
    modify_authentication_profile,
    modify_cluster_db_revision,
    modify_cluster_iam_roles,
    modify_cluster_maintenance,
    modify_cluster_parameter_group,
    modify_cluster_snapshot,
    modify_cluster_snapshot_schedule,
    modify_cluster_subnet_group,
    modify_custom_domain_association,
    modify_endpoint_access,
    modify_event_subscription,
    modify_integration,
    modify_redshift_idc_application,
    modify_scheduled_action,
    modify_snapshot_copy_retention_period,
    modify_snapshot_schedule,
    modify_usage_limit,
    pause_cluster,
    purchase_reserved_node_offering,
    put_resource_policy,
    register_namespace,
    reject_data_share,
    reset_cluster_parameter_group,
    resize_cluster,
    restore_table_from_cluster_snapshot,
    resume_cluster,
    revoke_cluster_security_group_ingress,
    revoke_endpoint_access,
    revoke_snapshot_access,
    rotate_encryption_key,
    update_partner_status,
)

REGION = "us-east-1"

# ---------------------------------------------------------------------------
# Sample API response dicts
# ---------------------------------------------------------------------------

_CLUSTER_RAW: dict = {
    "ClusterIdentifier": "my-cluster",
    "NodeType": "dc2.large",
    "ClusterStatus": "available",
    "DBName": "dev",
    "MasterUsername": "admin",
    "Endpoint": {"Address": "my-cluster.abc.redshift.amazonaws.com", "Port": 5439},
    "NumberOfNodes": 1,
    "PubliclyAccessible": False,
    "Encrypted": False,
    "VpcId": "vpc-123",
    "AvailabilityZone": "us-east-1a",
    "Tags": [{"Key": "env", "Value": "test"}],
}

_SNAPSHOT_RAW: dict = {
    "SnapshotIdentifier": "snap-1",
    "ClusterIdentifier": "my-cluster",
    "Status": "available",
    "SnapshotType": "manual",
    "NodeType": "dc2.large",
    "NumberOfNodes": 1,
    "DBName": "dev",
    "Encrypted": False,
}


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestClusterResultModel:
    def test_basic_fields(self) -> None:
        c = ClusterResult(
            cluster_identifier="c1",
            node_type="dc2.large",
            cluster_status="available",
        )
        assert c.cluster_identifier == "c1"
        assert c.number_of_nodes == 1
        assert c.tags == {}
        assert c.publicly_accessible is False
        assert c.encrypted is False

    def test_frozen(self) -> None:
        c = ClusterResult(
            cluster_identifier="c1",
            node_type="dc2.large",
            cluster_status="available",
        )
        with pytest.raises(Exception):
            c.cluster_status = "deleting"  # type: ignore[misc]

    def test_with_optional_fields(self) -> None:
        c = ClusterResult(
            cluster_identifier="c1",
            node_type="dc2.large",
            cluster_status="available",
            endpoint_address="host",
            endpoint_port=5439,
            db_name="dev",
            master_username="admin",
            vpc_id="vpc-1",
            availability_zone="us-east-1a",
            tags={"env": "prod"},
        )
        assert c.endpoint_address == "host"
        assert c.tags["env"] == "prod"


class TestSnapshotResultModel:
    def test_basic_fields(self) -> None:
        s = SnapshotResult(
            snapshot_identifier="s1",
            cluster_identifier="c1",
            status="available",
            snapshot_type="manual",
        )
        assert s.snapshot_identifier == "s1"
        assert s.encrypted is False
        assert s.node_type is None

    def test_frozen(self) -> None:
        s = SnapshotResult(
            snapshot_identifier="s1",
            cluster_identifier="c1",
            status="available",
            snapshot_type="manual",
        )
        with pytest.raises(Exception):
            s.status = "deleted"  # type: ignore[misc]


class TestParameterGroupResultModel:
    def test_fields(self) -> None:
        pg = ParameterGroupResult(
            parameter_group_name="pg1",
            parameter_group_family="redshift-1.0",
            description="test",
        )
        assert pg.parameter_group_name == "pg1"

    def test_frozen(self) -> None:
        pg = ParameterGroupResult(
            parameter_group_name="pg1",
            parameter_group_family="redshift-1.0",
            description="test",
        )
        with pytest.raises(Exception):
            pg.description = "new"  # type: ignore[misc]


class TestSubnetGroupResultModel:
    def test_fields(self) -> None:
        sg = SubnetGroupResult(
            cluster_subnet_group_name="sg1",
            description="test",
        )
        assert sg.cluster_subnet_group_name == "sg1"
        assert sg.subnet_ids == []
        assert sg.vpc_id is None
        assert sg.status is None

    def test_frozen(self) -> None:
        sg = SubnetGroupResult(
            cluster_subnet_group_name="sg1",
            description="test",
        )
        with pytest.raises(Exception):
            sg.description = "new"  # type: ignore[misc]


class TestLoggingStatusModel:
    def test_fields(self) -> None:
        ls = LoggingStatus(logging_enabled=True, bucket_name="b")
        assert ls.logging_enabled is True
        assert ls.bucket_name == "b"
        assert ls.s3_key_prefix is None

    def test_frozen(self) -> None:
        ls = LoggingStatus(logging_enabled=False)
        with pytest.raises(Exception):
            ls.logging_enabled = True  # type: ignore[misc]


# ---------------------------------------------------------------------------
# _parse_cluster / _parse_snapshot
# ---------------------------------------------------------------------------


class TestParseCluster:
    def test_full(self) -> None:
        c = _parse_cluster(_CLUSTER_RAW)
        assert c.cluster_identifier == "my-cluster"
        assert c.endpoint_address == "my-cluster.abc.redshift.amazonaws.com"
        assert c.endpoint_port == 5439
        assert c.tags == {"env": "test"}
        assert c.vpc_id == "vpc-123"

    def test_minimal(self) -> None:
        raw = {
            "ClusterIdentifier": "c",
            "NodeType": "dc2.large",
            "ClusterStatus": "creating",
        }
        c = _parse_cluster(raw)
        assert c.endpoint_address is None
        assert c.tags == {}


class TestParseSnapshot:
    def test_full(self) -> None:
        s = _parse_snapshot(_SNAPSHOT_RAW)
        assert s.snapshot_identifier == "snap-1"
        assert s.node_type == "dc2.large"

    def test_minimal(self) -> None:
        raw = {
            "SnapshotIdentifier": "s",
            "ClusterIdentifier": "c",
            "Status": "creating",
            "SnapshotType": "manual",
        }
        s = _parse_snapshot(raw)
        assert s.node_type is None
        assert s.encrypted is False


# ---------------------------------------------------------------------------
# create_cluster
# ---------------------------------------------------------------------------


class TestCreateCluster:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster(
            "my-cluster", "dc2.large", "admin", "pass123",
        )
        assert result.cluster_identifier == "my-cluster"
        mock.create_cluster.assert_called_once()

    def test_with_tags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster(
            "my-cluster", "dc2.large", "admin", "pass123",
            tags={"env": "test"},
        )
        assert result.cluster_identifier == "my-cluster"
        call_kwargs = mock.create_cluster.call_args[1]
        assert "Tags" in call_kwargs

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster.side_effect = ClientError(
            {"Error": {"Code": "ClusterAlreadyExists", "Message": "exists"}},
            "CreateCluster",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to create Redshift cluster"):
            create_cluster("c", "dc2.large", "admin", "pass123")


# ---------------------------------------------------------------------------
# describe_clusters
# ---------------------------------------------------------------------------


class TestDescribeClusters:
    def test_all(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Clusters": [_CLUSTER_RAW]}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_clusters()
        assert len(result) == 1
        assert result[0].cluster_identifier == "my-cluster"

    def test_specific(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Clusters": [_CLUSTER_RAW]}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_clusters("my-cluster")
        assert len(result) == 1

    def test_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Clusters": []}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_clusters()
        assert result == []

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeClusters",
        )
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="describe_clusters failed"):
            describe_clusters()


# ---------------------------------------------------------------------------
# delete_cluster
# ---------------------------------------------------------------------------


class TestDeleteCluster:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.delete_cluster.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = delete_cluster("my-cluster")
        assert result.cluster_identifier == "my-cluster"

    def test_with_final_snapshot(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.delete_cluster.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = delete_cluster(
            "my-cluster",
            skip_final_snapshot=False,
            final_snapshot_identifier="final-snap",
        )
        assert result.cluster_identifier == "my-cluster"
        call_kwargs = mock.delete_cluster.call_args[1]
        assert call_kwargs["FinalClusterSnapshotIdentifier"] == "final-snap"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.delete_cluster.side_effect = ClientError(
            {"Error": {"Code": "ClusterNotFound", "Message": "not found"}},
            "DeleteCluster",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to delete Redshift cluster"):
            delete_cluster("missing")


# ---------------------------------------------------------------------------
# modify_cluster
# ---------------------------------------------------------------------------


class TestModifyCluster:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.modify_cluster.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = modify_cluster("my-cluster", NodeType="dc2.8xlarge")
        assert result.cluster_identifier == "my-cluster"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.modify_cluster.side_effect = ClientError(
            {"Error": {"Code": "InvalidClusterState", "Message": "bad state"}},
            "ModifyCluster",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to modify Redshift cluster"):
            modify_cluster("c")


# ---------------------------------------------------------------------------
# reboot_cluster
# ---------------------------------------------------------------------------


class TestRebootCluster:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.reboot_cluster.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = reboot_cluster("my-cluster")
        assert result.cluster_identifier == "my-cluster"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.reboot_cluster.side_effect = ClientError(
            {"Error": {"Code": "ClusterNotFound", "Message": "not found"}},
            "RebootCluster",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to reboot Redshift cluster"):
            reboot_cluster("missing")


# ---------------------------------------------------------------------------
# create_cluster_snapshot
# ---------------------------------------------------------------------------


class TestCreateClusterSnapshot:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_snapshot.return_value = {"Snapshot": _SNAPSHOT_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster_snapshot("snap-1", "my-cluster")
        assert result.snapshot_identifier == "snap-1"

    def test_with_tags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_snapshot.return_value = {"Snapshot": _SNAPSHOT_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster_snapshot(
            "snap-1", "my-cluster", tags={"k": "v"},
        )
        assert result.snapshot_identifier == "snap-1"
        call_kwargs = mock.create_cluster_snapshot.call_args[1]
        assert "Tags" in call_kwargs

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_snapshot.side_effect = ClientError(
            {"Error": {"Code": "ClusterNotFound", "Message": "not found"}},
            "CreateClusterSnapshot",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to create snapshot"):
            create_cluster_snapshot("s", "c")


# ---------------------------------------------------------------------------
# describe_cluster_snapshots
# ---------------------------------------------------------------------------


class TestDescribeClusterSnapshots:
    def test_all(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Snapshots": [_SNAPSHOT_RAW]}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_cluster_snapshots()
        assert len(result) == 1

    def test_filtered(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Snapshots": [_SNAPSHOT_RAW]}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_cluster_snapshots(
            cluster_identifier="my-cluster",
            snapshot_identifier="snap-1",
        )
        assert len(result) == 1

    def test_empty(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Snapshots": []}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_cluster_snapshots()
        assert result == []

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeClusterSnapshots",
        )
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="describe_cluster_snapshots failed"):
            describe_cluster_snapshots()


# ---------------------------------------------------------------------------
# delete_cluster_snapshot
# ---------------------------------------------------------------------------


class TestDeleteClusterSnapshot:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.delete_cluster_snapshot.return_value = {}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        delete_cluster_snapshot("snap-1")
        mock.delete_cluster_snapshot.assert_called_once()

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.delete_cluster_snapshot.side_effect = ClientError(
            {"Error": {"Code": "SnapshotNotFound", "Message": "not found"}},
            "DeleteClusterSnapshot",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
            delete_cluster_snapshot("missing")


# ---------------------------------------------------------------------------
# restore_from_cluster_snapshot
# ---------------------------------------------------------------------------


class TestRestoreFromClusterSnapshot:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.restore_from_cluster_snapshot.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = restore_from_cluster_snapshot("new-cluster", "snap-1")
        assert result.cluster_identifier == "my-cluster"

    def test_with_overrides(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.restore_from_cluster_snapshot.return_value = {"Cluster": _CLUSTER_RAW}
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = restore_from_cluster_snapshot(
            "new-cluster", "snap-1",
            node_type="dc2.8xlarge", number_of_nodes=4,
        )
        assert result.cluster_identifier == "my-cluster"
        call_kwargs = mock.restore_from_cluster_snapshot.call_args[1]
        assert call_kwargs["NodeType"] == "dc2.8xlarge"
        assert call_kwargs["NumberOfNodes"] == 4

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.restore_from_cluster_snapshot.side_effect = ClientError(
            {"Error": {"Code": "SnapshotNotFound", "Message": "not found"}},
            "RestoreFromClusterSnapshot",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="restore_from_cluster_snapshot failed"):
            restore_from_cluster_snapshot("c", "s")


# ---------------------------------------------------------------------------
# create_cluster_parameter_group
# ---------------------------------------------------------------------------


class TestCreateClusterParameterGroup:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_parameter_group.return_value = {
            "ClusterParameterGroup": {
                "ParameterGroupName": "pg1",
                "ParameterGroupFamily": "redshift-1.0",
                "Description": "test",
            }
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster_parameter_group(
            "pg1", "redshift-1.0", "test",
        )
        assert result.parameter_group_name == "pg1"

    def test_with_tags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_parameter_group.return_value = {
            "ClusterParameterGroup": {
                "ParameterGroupName": "pg1",
                "ParameterGroupFamily": "redshift-1.0",
                "Description": "test",
            }
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster_parameter_group(
            "pg1", "redshift-1.0", "test", tags={"k": "v"},
        )
        assert result.parameter_group_name == "pg1"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_parameter_group.side_effect = ClientError(
            {"Error": {"Code": "AlreadyExists", "Message": "exists"}},
            "CreateClusterParameterGroup",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to create parameter group"):
            create_cluster_parameter_group("pg1", "redshift-1.0", "test")


# ---------------------------------------------------------------------------
# create_cluster_subnet_group
# ---------------------------------------------------------------------------


class TestCreateClusterSubnetGroup:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_subnet_group.return_value = {
            "ClusterSubnetGroup": {
                "ClusterSubnetGroupName": "sg1",
                "Description": "test",
                "VpcId": "vpc-1",
                "Subnets": [{"SubnetIdentifier": "subnet-1"}],
                "SubnetGroupStatus": "Complete",
            }
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster_subnet_group("sg1", "test", ["subnet-1"])
        assert result.cluster_subnet_group_name == "sg1"
        assert result.subnet_ids == ["subnet-1"]
        assert result.vpc_id == "vpc-1"
        assert result.status == "Complete"

    def test_with_tags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_subnet_group.return_value = {
            "ClusterSubnetGroup": {
                "ClusterSubnetGroupName": "sg1",
                "Description": "test",
                "Subnets": [],
            }
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = create_cluster_subnet_group(
            "sg1", "test", ["subnet-1"], tags={"k": "v"},
        )
        assert result.cluster_subnet_group_name == "sg1"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.create_cluster_subnet_group.side_effect = ClientError(
            {"Error": {"Code": "AlreadyExists", "Message": "exists"}},
            "CreateClusterSubnetGroup",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to create subnet group"):
            create_cluster_subnet_group("sg1", "test", ["subnet-1"])


# ---------------------------------------------------------------------------
# describe_logging_status
# ---------------------------------------------------------------------------


class TestDescribeLoggingStatus:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.describe_logging_status.return_value = {
            "LoggingEnabled": True,
            "BucketName": "my-bucket",
            "S3KeyPrefix": "logs/",
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_logging_status("my-cluster")
        assert result.logging_enabled is True
        assert result.bucket_name == "my-bucket"
        assert result.s3_key_prefix == "logs/"

    def test_disabled(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.describe_logging_status.return_value = {
            "LoggingEnabled": False,
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = describe_logging_status("my-cluster")
        assert result.logging_enabled is False
        assert result.bucket_name is None

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.describe_logging_status.side_effect = ClientError(
            {"Error": {"Code": "ClusterNotFound", "Message": "not found"}},
            "DescribeLoggingStatus",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to describe logging"):
            describe_logging_status("missing")


# ---------------------------------------------------------------------------
# enable_logging
# ---------------------------------------------------------------------------


class TestEnableLogging:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.enable_logging.return_value = {
            "LoggingEnabled": True,
            "BucketName": "my-bucket",
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = enable_logging("my-cluster", "my-bucket")
        assert result.logging_enabled is True

    def test_with_prefix(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.enable_logging.return_value = {
            "LoggingEnabled": True,
            "BucketName": "my-bucket",
            "S3KeyPrefix": "logs/",
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = enable_logging("my-cluster", "my-bucket", s3_key_prefix="logs/")
        assert result.s3_key_prefix == "logs/"
        call_kwargs = mock.enable_logging.call_args[1]
        assert call_kwargs["S3KeyPrefix"] == "logs/"

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.enable_logging.side_effect = ClientError(
            {"Error": {"Code": "BucketNotFound", "Message": "not found"}},
            "EnableLogging",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to enable logging"):
            enable_logging("c", "bucket")


# ---------------------------------------------------------------------------
# disable_logging
# ---------------------------------------------------------------------------


class TestDisableLogging:
    def test_success(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.disable_logging.return_value = {
            "LoggingEnabled": False,
        }
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = disable_logging("my-cluster")
        assert result.logging_enabled is False

    def test_client_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock = MagicMock()
        mock.disable_logging.side_effect = ClientError(
            {"Error": {"Code": "ClusterNotFound", "Message": "not found"}},
            "DisableLogging",
        )
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="Failed to disable logging"):
            disable_logging("missing")


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


class TestWaitForCluster:
    def test_immediate_match(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Clusters": [_CLUSTER_RAW]}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        result = wait_for_cluster("my-cluster", timeout=5.0)
        assert result.cluster_status == "available"

    def test_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Clusters": []}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)

        with pytest.raises(RuntimeError, match="not found"):
            wait_for_cluster("ghost", timeout=1.0)

    def test_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        creating = dict(_CLUSTER_RAW)
        creating["ClusterStatus"] = "creating"
        mock_pag = MagicMock()
        mock_pag.paginate.return_value = [{"Clusters": [creating]}]
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        monkeypatch.setattr(time, "sleep", lambda s: None)

        with pytest.raises(TimeoutError, match="did not reach status"):
            wait_for_cluster(
                "my-cluster",
                target_status="available",
                timeout=0.0,
                poll_interval=0.0,
            )

    def test_poll_then_available(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Covers the time.sleep branch in the polling loop."""
        call_count = {"n": 0}

        creating = dict(_CLUSTER_RAW)
        creating["ClusterStatus"] = "creating"
        available = dict(_CLUSTER_RAW)
        available["ClusterStatus"] = "available"

        def fake_paginate(**kw: Any) -> list[dict]:
            call_count["n"] += 1
            if call_count["n"] < 2:
                return [{"Clusters": [creating]}]
            return [{"Clusters": [available]}]

        mock_pag = MagicMock()
        mock_pag.paginate.side_effect = fake_paginate
        mock = MagicMock()
        mock.get_paginator.return_value = mock_pag
        monkeypatch.setattr(mod, "get_client", lambda *a, **kw: mock)
        monkeypatch.setattr(time, "sleep", lambda s: None)

        result = wait_for_cluster(
            "my-cluster",
            target_status="available",
            timeout=60.0,
            poll_interval=0.001,
        )
        assert result.cluster_status == "available"


def test_accept_reserved_node_exchange(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_reserved_node_exchange.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    accept_reserved_node_exchange("test-reserved_node_id", "test-target_reserved_node_offering_id", region_name=REGION)
    mock_client.accept_reserved_node_exchange.assert_called_once()


def test_accept_reserved_node_exchange_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.accept_reserved_node_exchange.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "accept_reserved_node_exchange",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to accept reserved node exchange"):
        accept_reserved_node_exchange("test-reserved_node_id", "test-target_reserved_node_offering_id", region_name=REGION)


def test_add_partner(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_partner.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    add_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", region_name=REGION)
    mock_client.add_partner.assert_called_once()


def test_add_partner_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.add_partner.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "add_partner",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to add partner"):
        add_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", region_name=REGION)


def test_associate_data_share_consumer(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_data_share_consumer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    associate_data_share_consumer("test-data_share_arn", region_name=REGION)
    mock_client.associate_data_share_consumer.assert_called_once()


def test_associate_data_share_consumer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_data_share_consumer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_data_share_consumer",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate data share consumer"):
        associate_data_share_consumer("test-data_share_arn", region_name=REGION)


def test_authorize_cluster_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_cluster_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_cluster_security_group_ingress("test-cluster_security_group_name", region_name=REGION)
    mock_client.authorize_cluster_security_group_ingress.assert_called_once()


def test_authorize_cluster_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_cluster_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_cluster_security_group_ingress",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize cluster security group ingress"):
        authorize_cluster_security_group_ingress("test-cluster_security_group_name", region_name=REGION)


def test_authorize_data_share(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_data_share.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_data_share("test-data_share_arn", "test-consumer_identifier", region_name=REGION)
    mock_client.authorize_data_share.assert_called_once()


def test_authorize_data_share_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_data_share.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_data_share",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize data share"):
        authorize_data_share("test-data_share_arn", "test-consumer_identifier", region_name=REGION)


def test_authorize_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_endpoint_access("test-account", region_name=REGION)
    mock_client.authorize_endpoint_access.assert_called_once()


def test_authorize_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize endpoint access"):
        authorize_endpoint_access("test-account", region_name=REGION)


def test_authorize_snapshot_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_snapshot_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_snapshot_access("test-account_with_restore_access", region_name=REGION)
    mock_client.authorize_snapshot_access.assert_called_once()


def test_authorize_snapshot_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_snapshot_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_snapshot_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize snapshot access"):
        authorize_snapshot_access("test-account_with_restore_access", region_name=REGION)


def test_batch_delete_cluster_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_cluster_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    batch_delete_cluster_snapshots([], region_name=REGION)
    mock_client.batch_delete_cluster_snapshots.assert_called_once()


def test_batch_delete_cluster_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_delete_cluster_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_delete_cluster_snapshots",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch delete cluster snapshots"):
        batch_delete_cluster_snapshots([], region_name=REGION)


def test_batch_modify_cluster_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_modify_cluster_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    batch_modify_cluster_snapshots([], region_name=REGION)
    mock_client.batch_modify_cluster_snapshots.assert_called_once()


def test_batch_modify_cluster_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_modify_cluster_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_modify_cluster_snapshots",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch modify cluster snapshots"):
        batch_modify_cluster_snapshots([], region_name=REGION)


def test_cancel_resize(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_resize.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    cancel_resize("test-cluster_identifier", region_name=REGION)
    mock_client.cancel_resize.assert_called_once()


def test_cancel_resize_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.cancel_resize.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "cancel_resize",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to cancel resize"):
        cancel_resize("test-cluster_identifier", region_name=REGION)


def test_copy_cluster_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    copy_cluster_snapshot("test-source_snapshot_identifier", "test-target_snapshot_identifier", region_name=REGION)
    mock_client.copy_cluster_snapshot.assert_called_once()


def test_copy_cluster_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_cluster_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy cluster snapshot"):
        copy_cluster_snapshot("test-source_snapshot_identifier", "test-target_snapshot_identifier", region_name=REGION)


def test_create_authentication_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_authentication_profile.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", region_name=REGION)
    mock_client.create_authentication_profile.assert_called_once()


def test_create_authentication_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_authentication_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_authentication_profile",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create authentication profile"):
        create_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", region_name=REGION)


def test_create_cluster_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cluster_security_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_cluster_security_group("test-cluster_security_group_name", "test-description", region_name=REGION)
    mock_client.create_cluster_security_group.assert_called_once()


def test_create_cluster_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cluster_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cluster_security_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cluster security group"):
        create_cluster_security_group("test-cluster_security_group_name", "test-description", region_name=REGION)


def test_create_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", region_name=REGION)
    mock_client.create_custom_domain_association.assert_called_once()


def test_create_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create custom domain association"):
        create_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", region_name=REGION)


def test_create_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_endpoint_access("test-endpoint_name", "test-subnet_group_name", region_name=REGION)
    mock_client.create_endpoint_access.assert_called_once()


def test_create_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create endpoint access"):
        create_endpoint_access("test-endpoint_name", "test-subnet_group_name", region_name=REGION)


def test_create_event_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)
    mock_client.create_event_subscription.assert_called_once()


def test_create_event_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_event_subscription",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create event subscription"):
        create_event_subscription("test-subscription_name", "test-sns_topic_arn", region_name=REGION)


def test_create_hsm_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hsm_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_hsm_client_certificate("test-hsm_client_certificate_identifier", region_name=REGION)
    mock_client.create_hsm_client_certificate.assert_called_once()


def test_create_hsm_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hsm_client_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_hsm_client_certificate",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create hsm client certificate"):
        create_hsm_client_certificate("test-hsm_client_certificate_identifier", region_name=REGION)


def test_create_hsm_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hsm_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_hsm_configuration("test-hsm_configuration_identifier", "test-description", "test-hsm_ip_address", "test-hsm_partition_name", "test-hsm_partition_password", "test-hsm_server_public_certificate", region_name=REGION)
    mock_client.create_hsm_configuration.assert_called_once()


def test_create_hsm_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_hsm_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_hsm_configuration",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create hsm configuration"):
        create_hsm_configuration("test-hsm_configuration_identifier", "test-description", "test-hsm_ip_address", "test-hsm_partition_name", "test-hsm_partition_password", "test-hsm_server_public_certificate", region_name=REGION)


def test_create_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_integration("test-source_arn", "test-target_arn", "test-integration_name", region_name=REGION)
    mock_client.create_integration.assert_called_once()


def test_create_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_integration",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create integration"):
        create_integration("test-source_arn", "test-target_arn", "test-integration_name", region_name=REGION)


def test_create_redshift_idc_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_redshift_idc_application.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_redshift_idc_application("test-idc_instance_arn", "test-redshift_idc_application_name", "test-idc_display_name", "test-iam_role_arn", region_name=REGION)
    mock_client.create_redshift_idc_application.assert_called_once()


def test_create_redshift_idc_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_redshift_idc_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_redshift_idc_application",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create redshift idc application"):
        create_redshift_idc_application("test-idc_instance_arn", "test-redshift_idc_application_name", "test-idc_display_name", "test-iam_role_arn", region_name=REGION)


def test_create_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_scheduled_action("test-scheduled_action_name", {}, "test-schedule", "test-iam_role", region_name=REGION)
    mock_client.create_scheduled_action.assert_called_once()


def test_create_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create scheduled action"):
        create_scheduled_action("test-scheduled_action_name", {}, "test-schedule", "test-iam_role", region_name=REGION)


def test_create_snapshot_copy_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_copy_grant.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_snapshot_copy_grant("test-snapshot_copy_grant_name", region_name=REGION)
    mock_client.create_snapshot_copy_grant.assert_called_once()


def test_create_snapshot_copy_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_copy_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot_copy_grant",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot copy grant"):
        create_snapshot_copy_grant("test-snapshot_copy_grant_name", region_name=REGION)


def test_create_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_snapshot_schedule(region_name=REGION)
    mock_client.create_snapshot_schedule.assert_called_once()


def test_create_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create snapshot schedule"):
        create_snapshot_schedule(region_name=REGION)


def test_create_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tags.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_tags("test-resource_name", [], region_name=REGION)
    mock_client.create_tags.assert_called_once()


def test_create_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tags",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tags"):
        create_tags("test-resource_name", [], region_name=REGION)


def test_create_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_usage_limit("test-cluster_identifier", "test-feature_type", "test-limit_type", 1, region_name=REGION)
    mock_client.create_usage_limit.assert_called_once()


def test_create_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create usage limit"):
        create_usage_limit("test-cluster_identifier", "test-feature_type", "test-limit_type", 1, region_name=REGION)


def test_deauthorize_data_share(monkeypatch):
    mock_client = MagicMock()
    mock_client.deauthorize_data_share.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    deauthorize_data_share("test-data_share_arn", "test-consumer_identifier", region_name=REGION)
    mock_client.deauthorize_data_share.assert_called_once()


def test_deauthorize_data_share_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deauthorize_data_share.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deauthorize_data_share",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deauthorize data share"):
        deauthorize_data_share("test-data_share_arn", "test-consumer_identifier", region_name=REGION)


def test_delete_authentication_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_authentication_profile.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_authentication_profile("test-authentication_profile_name", region_name=REGION)
    mock_client.delete_authentication_profile.assert_called_once()


def test_delete_authentication_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_authentication_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_authentication_profile",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete authentication profile"):
        delete_authentication_profile("test-authentication_profile_name", region_name=REGION)


def test_delete_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_cluster_parameter_group("test-parameter_group_name", region_name=REGION)
    mock_client.delete_cluster_parameter_group.assert_called_once()


def test_delete_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cluster_parameter_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cluster parameter group"):
        delete_cluster_parameter_group("test-parameter_group_name", region_name=REGION)


def test_delete_cluster_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_security_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_cluster_security_group("test-cluster_security_group_name", region_name=REGION)
    mock_client.delete_cluster_security_group.assert_called_once()


def test_delete_cluster_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cluster_security_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cluster security group"):
        delete_cluster_security_group("test-cluster_security_group_name", region_name=REGION)


def test_delete_cluster_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_cluster_subnet_group("test-cluster_subnet_group_name", region_name=REGION)
    mock_client.delete_cluster_subnet_group.assert_called_once()


def test_delete_cluster_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cluster_subnet_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cluster subnet group"):
        delete_cluster_subnet_group("test-cluster_subnet_group_name", region_name=REGION)


def test_delete_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_custom_domain_association("test-cluster_identifier", "test-custom_domain_name", region_name=REGION)
    mock_client.delete_custom_domain_association.assert_called_once()


def test_delete_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete custom domain association"):
        delete_custom_domain_association("test-cluster_identifier", "test-custom_domain_name", region_name=REGION)


def test_delete_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_endpoint_access("test-endpoint_name", region_name=REGION)
    mock_client.delete_endpoint_access.assert_called_once()


def test_delete_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete endpoint access"):
        delete_endpoint_access("test-endpoint_name", region_name=REGION)


def test_delete_event_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.delete_event_subscription.assert_called_once()


def test_delete_event_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_event_subscription",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete event subscription"):
        delete_event_subscription("test-subscription_name", region_name=REGION)


def test_delete_hsm_client_certificate(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hsm_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_hsm_client_certificate("test-hsm_client_certificate_identifier", region_name=REGION)
    mock_client.delete_hsm_client_certificate.assert_called_once()


def test_delete_hsm_client_certificate_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hsm_client_certificate.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_hsm_client_certificate",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete hsm client certificate"):
        delete_hsm_client_certificate("test-hsm_client_certificate_identifier", region_name=REGION)


def test_delete_hsm_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hsm_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_hsm_configuration("test-hsm_configuration_identifier", region_name=REGION)
    mock_client.delete_hsm_configuration.assert_called_once()


def test_delete_hsm_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_hsm_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_hsm_configuration",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete hsm configuration"):
        delete_hsm_configuration("test-hsm_configuration_identifier", region_name=REGION)


def test_delete_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_integration("test-integration_arn", region_name=REGION)
    mock_client.delete_integration.assert_called_once()


def test_delete_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_integration",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete integration"):
        delete_integration("test-integration_arn", region_name=REGION)


def test_delete_partner(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partner.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", region_name=REGION)
    mock_client.delete_partner.assert_called_once()


def test_delete_partner_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_partner.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_partner",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete partner"):
        delete_partner("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", region_name=REGION)


def test_delete_redshift_idc_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_redshift_idc_application.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_redshift_idc_application("test-redshift_idc_application_arn", region_name=REGION)
    mock_client.delete_redshift_idc_application.assert_called_once()


def test_delete_redshift_idc_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_redshift_idc_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_redshift_idc_application",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete redshift idc application"):
        delete_redshift_idc_application("test-redshift_idc_application_arn", region_name=REGION)


def test_delete_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.delete_resource_policy.assert_called_once()


def test_delete_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_resource_policy",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete resource policy"):
        delete_resource_policy("test-resource_arn", region_name=REGION)


def test_delete_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_scheduled_action("test-scheduled_action_name", region_name=REGION)
    mock_client.delete_scheduled_action.assert_called_once()


def test_delete_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete scheduled action"):
        delete_scheduled_action("test-scheduled_action_name", region_name=REGION)


def test_delete_snapshot_copy_grant(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_copy_grant.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_snapshot_copy_grant("test-snapshot_copy_grant_name", region_name=REGION)
    mock_client.delete_snapshot_copy_grant.assert_called_once()


def test_delete_snapshot_copy_grant_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_copy_grant.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot_copy_grant",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot copy grant"):
        delete_snapshot_copy_grant("test-snapshot_copy_grant_name", region_name=REGION)


def test_delete_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_snapshot_schedule("test-schedule_identifier", region_name=REGION)
    mock_client.delete_snapshot_schedule.assert_called_once()


def test_delete_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete snapshot schedule"):
        delete_snapshot_schedule("test-schedule_identifier", region_name=REGION)


def test_delete_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_tags("test-resource_name", [], region_name=REGION)
    mock_client.delete_tags.assert_called_once()


def test_delete_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tags",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tags"):
        delete_tags("test-resource_name", [], region_name=REGION)


def test_delete_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    delete_usage_limit("test-usage_limit_id", region_name=REGION)
    mock_client.delete_usage_limit.assert_called_once()


def test_delete_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete usage limit"):
        delete_usage_limit("test-usage_limit_id", region_name=REGION)


def test_deregister_namespace(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_namespace.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    deregister_namespace({}, [], region_name=REGION)
    mock_client.deregister_namespace.assert_called_once()


def test_deregister_namespace_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_namespace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_namespace",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister namespace"):
        deregister_namespace({}, [], region_name=REGION)


def test_describe_account_attributes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_attributes.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_account_attributes(region_name=REGION)
    mock_client.describe_account_attributes.assert_called_once()


def test_describe_account_attributes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_attributes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_attributes",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account attributes"):
        describe_account_attributes(region_name=REGION)


def test_describe_authentication_profiles(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_authentication_profiles.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_authentication_profiles(region_name=REGION)
    mock_client.describe_authentication_profiles.assert_called_once()


def test_describe_authentication_profiles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_authentication_profiles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_authentication_profiles",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe authentication profiles"):
        describe_authentication_profiles(region_name=REGION)


def test_describe_cluster_db_revisions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_db_revisions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_db_revisions(region_name=REGION)
    mock_client.describe_cluster_db_revisions.assert_called_once()


def test_describe_cluster_db_revisions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_db_revisions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_db_revisions",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster db revisions"):
        describe_cluster_db_revisions(region_name=REGION)


def test_describe_cluster_parameter_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_parameter_groups(region_name=REGION)
    mock_client.describe_cluster_parameter_groups.assert_called_once()


def test_describe_cluster_parameter_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_parameter_groups",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster parameter groups"):
        describe_cluster_parameter_groups(region_name=REGION)


def test_describe_cluster_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_parameters("test-parameter_group_name", region_name=REGION)
    mock_client.describe_cluster_parameters.assert_called_once()


def test_describe_cluster_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_parameters",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster parameters"):
        describe_cluster_parameters("test-parameter_group_name", region_name=REGION)


def test_describe_cluster_security_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_security_groups(region_name=REGION)
    mock_client.describe_cluster_security_groups.assert_called_once()


def test_describe_cluster_security_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_security_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_security_groups",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster security groups"):
        describe_cluster_security_groups(region_name=REGION)


def test_describe_cluster_subnet_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_subnet_groups(region_name=REGION)
    mock_client.describe_cluster_subnet_groups.assert_called_once()


def test_describe_cluster_subnet_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_subnet_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_subnet_groups",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster subnet groups"):
        describe_cluster_subnet_groups(region_name=REGION)


def test_describe_cluster_tracks(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_tracks.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_tracks(region_name=REGION)
    mock_client.describe_cluster_tracks.assert_called_once()


def test_describe_cluster_tracks_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_tracks.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_tracks",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster tracks"):
        describe_cluster_tracks(region_name=REGION)


def test_describe_cluster_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_versions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_versions(region_name=REGION)
    mock_client.describe_cluster_versions.assert_called_once()


def test_describe_cluster_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_versions",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster versions"):
        describe_cluster_versions(region_name=REGION)


def test_describe_custom_domain_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_custom_domain_associations(region_name=REGION)
    mock_client.describe_custom_domain_associations.assert_called_once()


def test_describe_custom_domain_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_custom_domain_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_custom_domain_associations",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe custom domain associations"):
        describe_custom_domain_associations(region_name=REGION)


def test_describe_data_shares(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_shares.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_data_shares(region_name=REGION)
    mock_client.describe_data_shares.assert_called_once()


def test_describe_data_shares_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_shares.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_shares",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data shares"):
        describe_data_shares(region_name=REGION)


def test_describe_data_shares_for_consumer(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_shares_for_consumer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_data_shares_for_consumer(region_name=REGION)
    mock_client.describe_data_shares_for_consumer.assert_called_once()


def test_describe_data_shares_for_consumer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_shares_for_consumer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_shares_for_consumer",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data shares for consumer"):
        describe_data_shares_for_consumer(region_name=REGION)


def test_describe_data_shares_for_producer(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_shares_for_producer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_data_shares_for_producer(region_name=REGION)
    mock_client.describe_data_shares_for_producer.assert_called_once()


def test_describe_data_shares_for_producer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_data_shares_for_producer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_data_shares_for_producer",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe data shares for producer"):
        describe_data_shares_for_producer(region_name=REGION)


def test_describe_default_cluster_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_default_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_default_cluster_parameters("test-parameter_group_family", region_name=REGION)
    mock_client.describe_default_cluster_parameters.assert_called_once()


def test_describe_default_cluster_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_default_cluster_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_default_cluster_parameters",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe default cluster parameters"):
        describe_default_cluster_parameters("test-parameter_group_family", region_name=REGION)


def test_describe_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_endpoint_access(region_name=REGION)
    mock_client.describe_endpoint_access.assert_called_once()


def test_describe_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe endpoint access"):
        describe_endpoint_access(region_name=REGION)


def test_describe_endpoint_authorization(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint_authorization.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_endpoint_authorization(region_name=REGION)
    mock_client.describe_endpoint_authorization.assert_called_once()


def test_describe_endpoint_authorization_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_endpoint_authorization.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_endpoint_authorization",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe endpoint authorization"):
        describe_endpoint_authorization(region_name=REGION)


def test_describe_event_categories(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_event_categories(region_name=REGION)
    mock_client.describe_event_categories.assert_called_once()


def test_describe_event_categories_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_categories.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_categories",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event categories"):
        describe_event_categories(region_name=REGION)


def test_describe_event_subscriptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(region_name=REGION)
    mock_client.describe_event_subscriptions.assert_called_once()


def test_describe_event_subscriptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_event_subscriptions",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe event subscriptions"):
        describe_event_subscriptions(region_name=REGION)


def test_describe_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


def test_describe_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


def test_describe_hsm_client_certificates(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hsm_client_certificates.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_hsm_client_certificates(region_name=REGION)
    mock_client.describe_hsm_client_certificates.assert_called_once()


def test_describe_hsm_client_certificates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hsm_client_certificates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_hsm_client_certificates",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe hsm client certificates"):
        describe_hsm_client_certificates(region_name=REGION)


def test_describe_hsm_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hsm_configurations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_hsm_configurations(region_name=REGION)
    mock_client.describe_hsm_configurations.assert_called_once()


def test_describe_hsm_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_hsm_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_hsm_configurations",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe hsm configurations"):
        describe_hsm_configurations(region_name=REGION)


def test_describe_inbound_integrations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_inbound_integrations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_inbound_integrations(region_name=REGION)
    mock_client.describe_inbound_integrations.assert_called_once()


def test_describe_inbound_integrations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_inbound_integrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_inbound_integrations",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe inbound integrations"):
        describe_inbound_integrations(region_name=REGION)


def test_describe_integrations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_integrations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_integrations(region_name=REGION)
    mock_client.describe_integrations.assert_called_once()


def test_describe_integrations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_integrations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_integrations",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe integrations"):
        describe_integrations(region_name=REGION)


def test_describe_node_configuration_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_node_configuration_options.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_node_configuration_options("test-action_type", region_name=REGION)
    mock_client.describe_node_configuration_options.assert_called_once()


def test_describe_node_configuration_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_node_configuration_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_node_configuration_options",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe node configuration options"):
        describe_node_configuration_options("test-action_type", region_name=REGION)


def test_describe_orderable_cluster_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_orderable_cluster_options.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_orderable_cluster_options(region_name=REGION)
    mock_client.describe_orderable_cluster_options.assert_called_once()


def test_describe_orderable_cluster_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_orderable_cluster_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_orderable_cluster_options",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe orderable cluster options"):
        describe_orderable_cluster_options(region_name=REGION)


def test_describe_partners(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_partners.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_partners("test-account_id", "test-cluster_identifier", region_name=REGION)
    mock_client.describe_partners.assert_called_once()


def test_describe_partners_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_partners.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_partners",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe partners"):
        describe_partners("test-account_id", "test-cluster_identifier", region_name=REGION)


def test_describe_redshift_idc_applications(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_redshift_idc_applications.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_redshift_idc_applications(region_name=REGION)
    mock_client.describe_redshift_idc_applications.assert_called_once()


def test_describe_redshift_idc_applications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_redshift_idc_applications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_redshift_idc_applications",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe redshift idc applications"):
        describe_redshift_idc_applications(region_name=REGION)


def test_describe_reserved_node_exchange_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_node_exchange_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_reserved_node_exchange_status(region_name=REGION)
    mock_client.describe_reserved_node_exchange_status.assert_called_once()


def test_describe_reserved_node_exchange_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_node_exchange_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_node_exchange_status",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved node exchange status"):
        describe_reserved_node_exchange_status(region_name=REGION)


def test_describe_reserved_node_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_node_offerings.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_reserved_node_offerings(region_name=REGION)
    mock_client.describe_reserved_node_offerings.assert_called_once()


def test_describe_reserved_node_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_node_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_node_offerings",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved node offerings"):
        describe_reserved_node_offerings(region_name=REGION)


def test_describe_reserved_nodes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_nodes.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_reserved_nodes(region_name=REGION)
    mock_client.describe_reserved_nodes.assert_called_once()


def test_describe_reserved_nodes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_nodes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_nodes",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved nodes"):
        describe_reserved_nodes(region_name=REGION)


def test_describe_resize(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resize.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_resize("test-cluster_identifier", region_name=REGION)
    mock_client.describe_resize.assert_called_once()


def test_describe_resize_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_resize.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_resize",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe resize"):
        describe_resize("test-cluster_identifier", region_name=REGION)


def test_describe_scheduled_actions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_actions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_actions(region_name=REGION)
    mock_client.describe_scheduled_actions.assert_called_once()


def test_describe_scheduled_actions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_scheduled_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_scheduled_actions",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe scheduled actions"):
        describe_scheduled_actions(region_name=REGION)


def test_describe_snapshot_copy_grants(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_copy_grants.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_copy_grants(region_name=REGION)
    mock_client.describe_snapshot_copy_grants.assert_called_once()


def test_describe_snapshot_copy_grants_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_copy_grants.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshot_copy_grants",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshot copy grants"):
        describe_snapshot_copy_grants(region_name=REGION)


def test_describe_snapshot_schedules(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_schedules.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_schedules(region_name=REGION)
    mock_client.describe_snapshot_schedules.assert_called_once()


def test_describe_snapshot_schedules_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_snapshot_schedules.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_snapshot_schedules",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe snapshot schedules"):
        describe_snapshot_schedules(region_name=REGION)


def test_describe_storage(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_storage.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_storage(region_name=REGION)
    mock_client.describe_storage.assert_called_once()


def test_describe_storage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_storage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_storage",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe storage"):
        describe_storage(region_name=REGION)


def test_describe_table_restore_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table_restore_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_table_restore_status(region_name=REGION)
    mock_client.describe_table_restore_status.assert_called_once()


def test_describe_table_restore_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_table_restore_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_table_restore_status",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe table restore status"):
        describe_table_restore_status(region_name=REGION)


def test_describe_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_tags(region_name=REGION)
    mock_client.describe_tags.assert_called_once()


def test_describe_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tags",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tags"):
        describe_tags(region_name=REGION)


def test_describe_usage_limits(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_usage_limits.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_usage_limits(region_name=REGION)
    mock_client.describe_usage_limits.assert_called_once()


def test_describe_usage_limits_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_usage_limits.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_usage_limits",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe usage limits"):
        describe_usage_limits(region_name=REGION)


def test_disable_snapshot_copy(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_snapshot_copy.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    disable_snapshot_copy("test-cluster_identifier", region_name=REGION)
    mock_client.disable_snapshot_copy.assert_called_once()


def test_disable_snapshot_copy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disable_snapshot_copy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disable_snapshot_copy",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disable snapshot copy"):
        disable_snapshot_copy("test-cluster_identifier", region_name=REGION)


def test_disassociate_data_share_consumer(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_data_share_consumer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    disassociate_data_share_consumer("test-data_share_arn", region_name=REGION)
    mock_client.disassociate_data_share_consumer.assert_called_once()


def test_disassociate_data_share_consumer_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_data_share_consumer.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_data_share_consumer",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate data share consumer"):
        disassociate_data_share_consumer("test-data_share_arn", region_name=REGION)


def test_enable_snapshot_copy(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_snapshot_copy.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    enable_snapshot_copy("test-cluster_identifier", "test-destination_region", region_name=REGION)
    mock_client.enable_snapshot_copy.assert_called_once()


def test_enable_snapshot_copy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.enable_snapshot_copy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "enable_snapshot_copy",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to enable snapshot copy"):
        enable_snapshot_copy("test-cluster_identifier", "test-destination_region", region_name=REGION)


def test_failover_primary_compute(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_primary_compute.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    failover_primary_compute("test-cluster_identifier", region_name=REGION)
    mock_client.failover_primary_compute.assert_called_once()


def test_failover_primary_compute_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_primary_compute.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_primary_compute",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to failover primary compute"):
        failover_primary_compute("test-cluster_identifier", region_name=REGION)


def test_get_cluster_credentials(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_credentials.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_cluster_credentials("test-db_user", region_name=REGION)
    mock_client.get_cluster_credentials.assert_called_once()


def test_get_cluster_credentials_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_credentials.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cluster_credentials",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cluster credentials"):
        get_cluster_credentials("test-db_user", region_name=REGION)


def test_get_cluster_credentials_with_iam(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_credentials_with_iam.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_cluster_credentials_with_iam(region_name=REGION)
    mock_client.get_cluster_credentials_with_iam.assert_called_once()


def test_get_cluster_credentials_with_iam_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_credentials_with_iam.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cluster_credentials_with_iam",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cluster credentials with iam"):
        get_cluster_credentials_with_iam(region_name=REGION)


def test_get_identity_center_auth_token(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_center_auth_token.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_identity_center_auth_token([], region_name=REGION)
    mock_client.get_identity_center_auth_token.assert_called_once()


def test_get_identity_center_auth_token_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_identity_center_auth_token.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_identity_center_auth_token",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get identity center auth token"):
        get_identity_center_auth_token([], region_name=REGION)


def test_get_reserved_node_exchange_configuration_options(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reserved_node_exchange_configuration_options.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_reserved_node_exchange_configuration_options("test-action_type", region_name=REGION)
    mock_client.get_reserved_node_exchange_configuration_options.assert_called_once()


def test_get_reserved_node_exchange_configuration_options_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reserved_node_exchange_configuration_options.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reserved_node_exchange_configuration_options",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reserved node exchange configuration options"):
        get_reserved_node_exchange_configuration_options("test-action_type", region_name=REGION)


def test_get_reserved_node_exchange_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reserved_node_exchange_offerings.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_reserved_node_exchange_offerings("test-reserved_node_id", region_name=REGION)
    mock_client.get_reserved_node_exchange_offerings.assert_called_once()


def test_get_reserved_node_exchange_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_reserved_node_exchange_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_reserved_node_exchange_offerings",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get reserved node exchange offerings"):
        get_reserved_node_exchange_offerings("test-reserved_node_id", region_name=REGION)


def test_get_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_resource_policy("test-resource_arn", region_name=REGION)
    mock_client.get_resource_policy.assert_called_once()


def test_get_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_resource_policy",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get resource policy"):
        get_resource_policy("test-resource_arn", region_name=REGION)


def test_list_recommendations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    list_recommendations(region_name=REGION)
    mock_client.list_recommendations.assert_called_once()


def test_list_recommendations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_recommendations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_recommendations",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list recommendations"):
        list_recommendations(region_name=REGION)


def test_modify_aqua_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_aqua_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_aqua_configuration("test-cluster_identifier", region_name=REGION)
    mock_client.modify_aqua_configuration.assert_called_once()


def test_modify_aqua_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_aqua_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_aqua_configuration",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify aqua configuration"):
        modify_aqua_configuration("test-cluster_identifier", region_name=REGION)


def test_modify_authentication_profile(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_authentication_profile.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", region_name=REGION)
    mock_client.modify_authentication_profile.assert_called_once()


def test_modify_authentication_profile_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_authentication_profile.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_authentication_profile",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify authentication profile"):
        modify_authentication_profile("test-authentication_profile_name", "test-authentication_profile_content", region_name=REGION)


def test_modify_cluster_db_revision(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_db_revision.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_db_revision("test-cluster_identifier", "test-revision_target", region_name=REGION)
    mock_client.modify_cluster_db_revision.assert_called_once()


def test_modify_cluster_db_revision_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_db_revision.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_db_revision",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster db revision"):
        modify_cluster_db_revision("test-cluster_identifier", "test-revision_target", region_name=REGION)


def test_modify_cluster_iam_roles(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_iam_roles.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_iam_roles("test-cluster_identifier", region_name=REGION)
    mock_client.modify_cluster_iam_roles.assert_called_once()


def test_modify_cluster_iam_roles_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_iam_roles.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_iam_roles",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster iam roles"):
        modify_cluster_iam_roles("test-cluster_identifier", region_name=REGION)


def test_modify_cluster_maintenance(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_maintenance.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_maintenance("test-cluster_identifier", region_name=REGION)
    mock_client.modify_cluster_maintenance.assert_called_once()


def test_modify_cluster_maintenance_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_maintenance.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_maintenance",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster maintenance"):
        modify_cluster_maintenance("test-cluster_identifier", region_name=REGION)


def test_modify_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_parameter_group("test-parameter_group_name", [], region_name=REGION)
    mock_client.modify_cluster_parameter_group.assert_called_once()


def test_modify_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_parameter_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster parameter group"):
        modify_cluster_parameter_group("test-parameter_group_name", [], region_name=REGION)


def test_modify_cluster_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_snapshot("test-snapshot_identifier", region_name=REGION)
    mock_client.modify_cluster_snapshot.assert_called_once()


def test_modify_cluster_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster snapshot"):
        modify_cluster_snapshot("test-snapshot_identifier", region_name=REGION)


def test_modify_cluster_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_snapshot_schedule("test-cluster_identifier", region_name=REGION)
    mock_client.modify_cluster_snapshot_schedule.assert_called_once()


def test_modify_cluster_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster snapshot schedule"):
        modify_cluster_snapshot_schedule("test-cluster_identifier", region_name=REGION)


def test_modify_cluster_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_subnet_group("test-cluster_subnet_group_name", [], region_name=REGION)
    mock_client.modify_cluster_subnet_group.assert_called_once()


def test_modify_cluster_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cluster_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cluster_subnet_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cluster subnet group"):
        modify_cluster_subnet_group("test-cluster_subnet_group_name", [], region_name=REGION)


def test_modify_custom_domain_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_custom_domain_association.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", region_name=REGION)
    mock_client.modify_custom_domain_association.assert_called_once()


def test_modify_custom_domain_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_custom_domain_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_custom_domain_association",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify custom domain association"):
        modify_custom_domain_association("test-custom_domain_name", "test-custom_domain_certificate_arn", "test-cluster_identifier", region_name=REGION)


def test_modify_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_endpoint_access("test-endpoint_name", region_name=REGION)
    mock_client.modify_endpoint_access.assert_called_once()


def test_modify_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify endpoint access"):
        modify_endpoint_access("test-endpoint_name", region_name=REGION)


def test_modify_event_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", region_name=REGION)
    mock_client.modify_event_subscription.assert_called_once()


def test_modify_event_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_event_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_event_subscription",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify event subscription"):
        modify_event_subscription("test-subscription_name", region_name=REGION)


def test_modify_integration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_integration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_integration("test-integration_arn", region_name=REGION)
    mock_client.modify_integration.assert_called_once()


def test_modify_integration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_integration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_integration",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify integration"):
        modify_integration("test-integration_arn", region_name=REGION)


def test_modify_redshift_idc_application(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_redshift_idc_application.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_redshift_idc_application("test-redshift_idc_application_arn", region_name=REGION)
    mock_client.modify_redshift_idc_application.assert_called_once()


def test_modify_redshift_idc_application_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_redshift_idc_application.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_redshift_idc_application",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify redshift idc application"):
        modify_redshift_idc_application("test-redshift_idc_application_arn", region_name=REGION)


def test_modify_scheduled_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_scheduled_action("test-scheduled_action_name", region_name=REGION)
    mock_client.modify_scheduled_action.assert_called_once()


def test_modify_scheduled_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_scheduled_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_scheduled_action",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify scheduled action"):
        modify_scheduled_action("test-scheduled_action_name", region_name=REGION)


def test_modify_snapshot_copy_retention_period(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_copy_retention_period.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_copy_retention_period("test-cluster_identifier", 1, region_name=REGION)
    mock_client.modify_snapshot_copy_retention_period.assert_called_once()


def test_modify_snapshot_copy_retention_period_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_copy_retention_period.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_snapshot_copy_retention_period",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify snapshot copy retention period"):
        modify_snapshot_copy_retention_period("test-cluster_identifier", 1, region_name=REGION)


def test_modify_snapshot_schedule(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_schedule("test-schedule_identifier", [], region_name=REGION)
    mock_client.modify_snapshot_schedule.assert_called_once()


def test_modify_snapshot_schedule_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_snapshot_schedule.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_snapshot_schedule",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify snapshot schedule"):
        modify_snapshot_schedule("test-schedule_identifier", [], region_name=REGION)


def test_modify_usage_limit(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_usage_limit("test-usage_limit_id", region_name=REGION)
    mock_client.modify_usage_limit.assert_called_once()


def test_modify_usage_limit_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_usage_limit.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_usage_limit",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify usage limit"):
        modify_usage_limit("test-usage_limit_id", region_name=REGION)


def test_pause_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.pause_cluster.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    pause_cluster("test-cluster_identifier", region_name=REGION)
    mock_client.pause_cluster.assert_called_once()


def test_pause_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.pause_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "pause_cluster",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to pause cluster"):
        pause_cluster("test-cluster_identifier", region_name=REGION)


def test_purchase_reserved_node_offering(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_node_offering.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_node_offering("test-reserved_node_offering_id", region_name=REGION)
    mock_client.purchase_reserved_node_offering.assert_called_once()


def test_purchase_reserved_node_offering_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_node_offering.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_reserved_node_offering",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase reserved node offering"):
        purchase_reserved_node_offering("test-reserved_node_offering_id", region_name=REGION)


def test_put_resource_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)
    mock_client.put_resource_policy.assert_called_once()


def test_put_resource_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_resource_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_resource_policy",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put resource policy"):
        put_resource_policy("test-resource_arn", "test-policy", region_name=REGION)


def test_register_namespace(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_namespace.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    register_namespace({}, [], region_name=REGION)
    mock_client.register_namespace.assert_called_once()


def test_register_namespace_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_namespace.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_namespace",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register namespace"):
        register_namespace({}, [], region_name=REGION)


def test_reject_data_share(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_data_share.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    reject_data_share("test-data_share_arn", region_name=REGION)
    mock_client.reject_data_share.assert_called_once()


def test_reject_data_share_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_data_share.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_data_share",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject data share"):
        reject_data_share("test-data_share_arn", region_name=REGION)


def test_reset_cluster_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    reset_cluster_parameter_group("test-parameter_group_name", region_name=REGION)
    mock_client.reset_cluster_parameter_group.assert_called_once()


def test_reset_cluster_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_cluster_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_cluster_parameter_group",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset cluster parameter group"):
        reset_cluster_parameter_group("test-parameter_group_name", region_name=REGION)


def test_resize_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.resize_cluster.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    resize_cluster("test-cluster_identifier", region_name=REGION)
    mock_client.resize_cluster.assert_called_once()


def test_resize_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resize_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resize_cluster",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resize cluster"):
        resize_cluster("test-cluster_identifier", region_name=REGION)


def test_restore_table_from_cluster_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    restore_table_from_cluster_snapshot("test-cluster_identifier", "test-snapshot_identifier", "test-source_database_name", "test-source_table_name", "test-new_table_name", region_name=REGION)
    mock_client.restore_table_from_cluster_snapshot.assert_called_once()


def test_restore_table_from_cluster_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.restore_table_from_cluster_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "restore_table_from_cluster_snapshot",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to restore table from cluster snapshot"):
        restore_table_from_cluster_snapshot("test-cluster_identifier", "test-snapshot_identifier", "test-source_database_name", "test-source_table_name", "test-new_table_name", region_name=REGION)


def test_resume_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_cluster.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    resume_cluster("test-cluster_identifier", region_name=REGION)
    mock_client.resume_cluster.assert_called_once()


def test_resume_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.resume_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "resume_cluster",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to resume cluster"):
        resume_cluster("test-cluster_identifier", region_name=REGION)


def test_revoke_cluster_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_cluster_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    revoke_cluster_security_group_ingress("test-cluster_security_group_name", region_name=REGION)
    mock_client.revoke_cluster_security_group_ingress.assert_called_once()


def test_revoke_cluster_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_cluster_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_cluster_security_group_ingress",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke cluster security group ingress"):
        revoke_cluster_security_group_ingress("test-cluster_security_group_name", region_name=REGION)


def test_revoke_endpoint_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    revoke_endpoint_access(region_name=REGION)
    mock_client.revoke_endpoint_access.assert_called_once()


def test_revoke_endpoint_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_endpoint_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_endpoint_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke endpoint access"):
        revoke_endpoint_access(region_name=REGION)


def test_revoke_snapshot_access(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_snapshot_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    revoke_snapshot_access("test-account_with_restore_access", region_name=REGION)
    mock_client.revoke_snapshot_access.assert_called_once()


def test_revoke_snapshot_access_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_snapshot_access.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_snapshot_access",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke snapshot access"):
        revoke_snapshot_access("test-account_with_restore_access", region_name=REGION)


def test_rotate_encryption_key(monkeypatch):
    mock_client = MagicMock()
    mock_client.rotate_encryption_key.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    rotate_encryption_key("test-cluster_identifier", region_name=REGION)
    mock_client.rotate_encryption_key.assert_called_once()


def test_rotate_encryption_key_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rotate_encryption_key.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rotate_encryption_key",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rotate encryption key"):
        rotate_encryption_key("test-cluster_identifier", region_name=REGION)


def test_update_partner_status(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_partner_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    update_partner_status("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", "test-status", region_name=REGION)
    mock_client.update_partner_status.assert_called_once()


def test_update_partner_status_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_partner_status.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_partner_status",
    )
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update partner status"):
        update_partner_status("test-account_id", "test-cluster_identifier", "test-database_name", "test-partner_name", "test-status", region_name=REGION)


def test_associate_data_share_consumer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import associate_data_share_consumer
    mock_client = MagicMock()
    mock_client.associate_data_share_consumer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    associate_data_share_consumer("test-data_share_arn", associate_entire_account=1, consumer_arn="test-consumer_arn", consumer_region="test-consumer_region", allow_writes=True, region_name="us-east-1")
    mock_client.associate_data_share_consumer.assert_called_once()

def test_authorize_cluster_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import authorize_cluster_security_group_ingress
    mock_client = MagicMock()
    mock_client.authorize_cluster_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_cluster_security_group_ingress("test-cluster_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.authorize_cluster_security_group_ingress.assert_called_once()

def test_authorize_data_share_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import authorize_data_share
    mock_client = MagicMock()
    mock_client.authorize_data_share.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_data_share("test-data_share_arn", "test-consumer_identifier", allow_writes=True, region_name="us-east-1")
    mock_client.authorize_data_share.assert_called_once()

def test_authorize_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import authorize_endpoint_access
    mock_client = MagicMock()
    mock_client.authorize_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_endpoint_access(1, cluster_identifier="test-cluster_identifier", vpc_ids="test-vpc_ids", region_name="us-east-1")
    mock_client.authorize_endpoint_access.assert_called_once()

def test_authorize_snapshot_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import authorize_snapshot_access
    mock_client = MagicMock()
    mock_client.authorize_snapshot_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    authorize_snapshot_access(1, snapshot_identifier="test-snapshot_identifier", snapshot_arn="test-snapshot_arn", snapshot_cluster_identifier="test-snapshot_cluster_identifier", region_name="us-east-1")
    mock_client.authorize_snapshot_access.assert_called_once()

def test_batch_modify_cluster_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import batch_modify_cluster_snapshots
    mock_client = MagicMock()
    mock_client.batch_modify_cluster_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    batch_modify_cluster_snapshots("test-snapshot_identifier_list", manual_snapshot_retention_period="test-manual_snapshot_retention_period", force=True, region_name="us-east-1")
    mock_client.batch_modify_cluster_snapshots.assert_called_once()

def test_copy_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import copy_cluster_snapshot
    mock_client = MagicMock()
    mock_client.copy_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    copy_cluster_snapshot("test-source_snapshot_identifier", "test-target_snapshot_identifier", source_snapshot_cluster_identifier="test-source_snapshot_cluster_identifier", manual_snapshot_retention_period="test-manual_snapshot_retention_period", region_name="us-east-1")
    mock_client.copy_cluster_snapshot.assert_called_once()

def test_create_cluster_security_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_cluster_security_group
    mock_client = MagicMock()
    mock_client.create_cluster_security_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_cluster_security_group("test-cluster_security_group_name", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_cluster_security_group.assert_called_once()

def test_create_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_endpoint_access
    mock_client = MagicMock()
    mock_client.create_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_endpoint_access("test-endpoint_name", "test-subnet_group_name", cluster_identifier="test-cluster_identifier", resource_owner="test-resource_owner", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.create_endpoint_access.assert_called_once()

def test_create_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_event_subscription
    mock_client = MagicMock()
    mock_client.create_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_event_subscription("test-subscription_name", "test-sns_topic_arn", source_type="test-source_type", source_ids="test-source_ids", event_categories="test-event_categories", severity="test-severity", enabled=True, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_event_subscription.assert_called_once()

def test_create_hsm_client_certificate_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_hsm_client_certificate
    mock_client = MagicMock()
    mock_client.create_hsm_client_certificate.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_hsm_client_certificate("test-hsm_client_certificate_identifier", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_hsm_client_certificate.assert_called_once()

def test_create_hsm_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_hsm_configuration
    mock_client = MagicMock()
    mock_client.create_hsm_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_hsm_configuration({}, "test-description", "test-hsm_ip_address", "test-hsm_partition_name", "test-hsm_partition_password", "test-hsm_server_public_certificate", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_hsm_configuration.assert_called_once()

def test_create_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_integration
    mock_client = MagicMock()
    mock_client.create_integration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_integration("test-source_arn", "test-target_arn", "test-integration_name", kms_key_id="test-kms_key_id", tag_list="test-tag_list", additional_encryption_context={}, description="test-description", region_name="us-east-1")
    mock_client.create_integration.assert_called_once()

def test_create_redshift_idc_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_redshift_idc_application
    mock_client = MagicMock()
    mock_client.create_redshift_idc_application.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_redshift_idc_application("test-idc_instance_arn", "test-redshift_idc_application_name", "test-idc_display_name", "test-iam_role_arn", identity_namespace="test-identity_namespace", authorized_token_issuer_list="test-authorized_token_issuer_list", service_integrations="test-service_integrations", tags=[{"Key": "k", "Value": "v"}], sso_tag_keys="test-sso_tag_keys", region_name="us-east-1")
    mock_client.create_redshift_idc_application.assert_called_once()

def test_create_scheduled_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_scheduled_action
    mock_client = MagicMock()
    mock_client.create_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_scheduled_action("test-scheduled_action_name", "test-target_action", "test-schedule", "test-iam_role", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", end_time="test-end_time", enable=True, region_name="us-east-1")
    mock_client.create_scheduled_action.assert_called_once()

def test_create_snapshot_copy_grant_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_snapshot_copy_grant
    mock_client = MagicMock()
    mock_client.create_snapshot_copy_grant.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_snapshot_copy_grant("test-snapshot_copy_grant_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_snapshot_copy_grant.assert_called_once()

def test_create_snapshot_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_snapshot_schedule
    mock_client = MagicMock()
    mock_client.create_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_snapshot_schedule(schedule_definitions={}, schedule_identifier="test-schedule_identifier", schedule_description="test-schedule_description", tags=[{"Key": "k", "Value": "v"}], next_invocations="test-next_invocations", region_name="us-east-1")
    mock_client.create_snapshot_schedule.assert_called_once()

def test_create_usage_limit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import create_usage_limit
    mock_client = MagicMock()
    mock_client.create_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    create_usage_limit("test-cluster_identifier", "test-feature_type", 1, "test-amount", period="test-period", breach_action="test-breach_action", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_usage_limit.assert_called_once()

def test_describe_account_attributes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_account_attributes
    mock_client = MagicMock()
    mock_client.describe_account_attributes.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_account_attributes(attribute_names="test-attribute_names", region_name="us-east-1")
    mock_client.describe_account_attributes.assert_called_once()

def test_describe_authentication_profiles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_authentication_profiles
    mock_client = MagicMock()
    mock_client.describe_authentication_profiles.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_authentication_profiles(authentication_profile_name="test-authentication_profile_name", region_name="us-east-1")
    mock_client.describe_authentication_profiles.assert_called_once()

def test_describe_cluster_db_revisions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_db_revisions
    mock_client = MagicMock()
    mock_client.describe_cluster_db_revisions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_db_revisions(cluster_identifier="test-cluster_identifier", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cluster_db_revisions.assert_called_once()

def test_describe_cluster_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_cluster_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_parameter_groups(parameter_group_name="test-parameter_group_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_cluster_parameter_groups.assert_called_once()

def test_describe_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_parameters("test-parameter_group_name", source="test-source", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cluster_parameters.assert_called_once()

def test_describe_cluster_security_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_security_groups
    mock_client = MagicMock()
    mock_client.describe_cluster_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_security_groups(cluster_security_group_name="test-cluster_security_group_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_cluster_security_groups.assert_called_once()

def test_describe_cluster_subnet_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_subnet_groups
    mock_client = MagicMock()
    mock_client.describe_cluster_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_subnet_groups(cluster_subnet_group_name="test-cluster_subnet_group_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_cluster_subnet_groups.assert_called_once()

def test_describe_cluster_tracks_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_tracks
    mock_client = MagicMock()
    mock_client.describe_cluster_tracks.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_tracks(maintenance_track_name="test-maintenance_track_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cluster_tracks.assert_called_once()

def test_describe_cluster_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_cluster_versions
    mock_client = MagicMock()
    mock_client.describe_cluster_versions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_cluster_versions(cluster_version="test-cluster_version", cluster_parameter_group_family="test-cluster_parameter_group_family", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cluster_versions.assert_called_once()

def test_describe_custom_domain_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_custom_domain_associations
    mock_client = MagicMock()
    mock_client.describe_custom_domain_associations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_custom_domain_associations(custom_domain_name="test-custom_domain_name", custom_domain_certificate_arn="test-custom_domain_certificate_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_custom_domain_associations.assert_called_once()

def test_describe_data_shares_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_data_shares
    mock_client = MagicMock()
    mock_client.describe_data_shares.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_data_shares(data_share_arn="test-data_share_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_data_shares.assert_called_once()

def test_describe_data_shares_for_consumer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_data_shares_for_consumer
    mock_client = MagicMock()
    mock_client.describe_data_shares_for_consumer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_data_shares_for_consumer(consumer_arn="test-consumer_arn", status="test-status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_data_shares_for_consumer.assert_called_once()

def test_describe_data_shares_for_producer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_data_shares_for_producer
    mock_client = MagicMock()
    mock_client.describe_data_shares_for_producer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_data_shares_for_producer(producer_arn="test-producer_arn", status="test-status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_data_shares_for_producer.assert_called_once()

def test_describe_default_cluster_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_default_cluster_parameters
    mock_client = MagicMock()
    mock_client.describe_default_cluster_parameters.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_default_cluster_parameters("test-parameter_group_family", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_default_cluster_parameters.assert_called_once()

def test_describe_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_endpoint_access
    mock_client = MagicMock()
    mock_client.describe_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_endpoint_access(cluster_identifier="test-cluster_identifier", resource_owner="test-resource_owner", endpoint_name="test-endpoint_name", vpc_id="test-vpc_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_endpoint_access.assert_called_once()

def test_describe_endpoint_authorization_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_endpoint_authorization
    mock_client = MagicMock()
    mock_client.describe_endpoint_authorization.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_endpoint_authorization(cluster_identifier="test-cluster_identifier", account=1, grantee="test-grantee", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_endpoint_authorization.assert_called_once()

def test_describe_event_categories_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_event_categories
    mock_client = MagicMock()
    mock_client.describe_event_categories.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_event_categories(source_type="test-source_type", region_name="us-east-1")
    mock_client.describe_event_categories.assert_called_once()

def test_describe_event_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_event_subscriptions
    mock_client = MagicMock()
    mock_client.describe_event_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_event_subscriptions(subscription_name="test-subscription_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_event_subscriptions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_hsm_client_certificates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_hsm_client_certificates
    mock_client = MagicMock()
    mock_client.describe_hsm_client_certificates.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_hsm_client_certificates(hsm_client_certificate_identifier="test-hsm_client_certificate_identifier", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_hsm_client_certificates.assert_called_once()

def test_describe_hsm_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_hsm_configurations
    mock_client = MagicMock()
    mock_client.describe_hsm_configurations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_hsm_configurations(hsm_configuration_identifier={}, max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_hsm_configurations.assert_called_once()

def test_describe_inbound_integrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_inbound_integrations
    mock_client = MagicMock()
    mock_client.describe_inbound_integrations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_inbound_integrations(integration_arn="test-integration_arn", target_arn="test-target_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_inbound_integrations.assert_called_once()

def test_describe_integrations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_integrations
    mock_client = MagicMock()
    mock_client.describe_integrations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_integrations(integration_arn="test-integration_arn", max_records=1, marker="test-marker", filters=[{}], region_name="us-east-1")
    mock_client.describe_integrations.assert_called_once()

def test_describe_node_configuration_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_node_configuration_options
    mock_client = MagicMock()
    mock_client.describe_node_configuration_options.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_node_configuration_options("test-action_type", cluster_identifier="test-cluster_identifier", snapshot_identifier="test-snapshot_identifier", snapshot_arn="test-snapshot_arn", owner_account=1, filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_node_configuration_options.assert_called_once()

def test_describe_orderable_cluster_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_orderable_cluster_options
    mock_client = MagicMock()
    mock_client.describe_orderable_cluster_options.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_orderable_cluster_options(cluster_version="test-cluster_version", node_type="test-node_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_orderable_cluster_options.assert_called_once()

def test_describe_partners_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_partners
    mock_client = MagicMock()
    mock_client.describe_partners.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_partners(1, "test-cluster_identifier", database_name="test-database_name", partner_name="test-partner_name", region_name="us-east-1")
    mock_client.describe_partners.assert_called_once()

def test_describe_redshift_idc_applications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_redshift_idc_applications
    mock_client = MagicMock()
    mock_client.describe_redshift_idc_applications.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_redshift_idc_applications(redshift_idc_application_arn="test-redshift_idc_application_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_redshift_idc_applications.assert_called_once()

def test_describe_reserved_node_exchange_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_reserved_node_exchange_status
    mock_client = MagicMock()
    mock_client.describe_reserved_node_exchange_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_reserved_node_exchange_status(reserved_node_id="test-reserved_node_id", reserved_node_exchange_request_id="test-reserved_node_exchange_request_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_node_exchange_status.assert_called_once()

def test_describe_reserved_node_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_reserved_node_offerings
    mock_client = MagicMock()
    mock_client.describe_reserved_node_offerings.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_reserved_node_offerings(reserved_node_offering_id="test-reserved_node_offering_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_node_offerings.assert_called_once()

def test_describe_reserved_nodes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_reserved_nodes
    mock_client = MagicMock()
    mock_client.describe_reserved_nodes.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_reserved_nodes(reserved_node_id="test-reserved_node_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_nodes.assert_called_once()

def test_describe_scheduled_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_scheduled_actions
    mock_client = MagicMock()
    mock_client.describe_scheduled_actions.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_scheduled_actions(scheduled_action_name="test-scheduled_action_name", target_action_type="test-target_action_type", start_time="test-start_time", end_time="test-end_time", active="test-active", filters=[{}], marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_scheduled_actions.assert_called_once()

def test_describe_snapshot_copy_grants_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_snapshot_copy_grants
    mock_client = MagicMock()
    mock_client.describe_snapshot_copy_grants.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_copy_grants(snapshot_copy_grant_name="test-snapshot_copy_grant_name", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_snapshot_copy_grants.assert_called_once()

def test_describe_snapshot_schedules_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_snapshot_schedules
    mock_client = MagicMock()
    mock_client.describe_snapshot_schedules.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_snapshot_schedules(cluster_identifier="test-cluster_identifier", schedule_identifier="test-schedule_identifier", tag_keys="test-tag_keys", tag_values="test-tag_values", marker="test-marker", max_records=1, region_name="us-east-1")
    mock_client.describe_snapshot_schedules.assert_called_once()

def test_describe_table_restore_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_table_restore_status
    mock_client = MagicMock()
    mock_client.describe_table_restore_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_table_restore_status(cluster_identifier="test-cluster_identifier", table_restore_request_id="test-table_restore_request_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_table_restore_status.assert_called_once()

def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_tags
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_tags(resource_name="test-resource_name", resource_type="test-resource_type", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_tags.assert_called_once()

def test_describe_usage_limits_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import describe_usage_limits
    mock_client = MagicMock()
    mock_client.describe_usage_limits.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    describe_usage_limits(usage_limit_id=1, cluster_identifier="test-cluster_identifier", feature_type="test-feature_type", max_records=1, marker="test-marker", tag_keys="test-tag_keys", tag_values="test-tag_values", region_name="us-east-1")
    mock_client.describe_usage_limits.assert_called_once()

def test_disassociate_data_share_consumer_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import disassociate_data_share_consumer
    mock_client = MagicMock()
    mock_client.disassociate_data_share_consumer.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    disassociate_data_share_consumer("test-data_share_arn", disassociate_entire_account=1, consumer_arn="test-consumer_arn", consumer_region="test-consumer_region", region_name="us-east-1")
    mock_client.disassociate_data_share_consumer.assert_called_once()

def test_enable_snapshot_copy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import enable_snapshot_copy
    mock_client = MagicMock()
    mock_client.enable_snapshot_copy.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    enable_snapshot_copy("test-cluster_identifier", "test-destination_region", retention_period="test-retention_period", snapshot_copy_grant_name="test-snapshot_copy_grant_name", manual_snapshot_retention_period="test-manual_snapshot_retention_period", region_name="us-east-1")
    mock_client.enable_snapshot_copy.assert_called_once()

def test_get_cluster_credentials_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import get_cluster_credentials
    mock_client = MagicMock()
    mock_client.get_cluster_credentials.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_cluster_credentials("test-db_user", db_name="test-db_name", cluster_identifier="test-cluster_identifier", duration_seconds=1, auto_create=True, db_groups="test-db_groups", custom_domain_name="test-custom_domain_name", region_name="us-east-1")
    mock_client.get_cluster_credentials.assert_called_once()

def test_get_cluster_credentials_with_iam_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import get_cluster_credentials_with_iam
    mock_client = MagicMock()
    mock_client.get_cluster_credentials_with_iam.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_cluster_credentials_with_iam(db_name="test-db_name", cluster_identifier="test-cluster_identifier", duration_seconds=1, custom_domain_name="test-custom_domain_name", region_name="us-east-1")
    mock_client.get_cluster_credentials_with_iam.assert_called_once()

def test_get_reserved_node_exchange_configuration_options_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import get_reserved_node_exchange_configuration_options
    mock_client = MagicMock()
    mock_client.get_reserved_node_exchange_configuration_options.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_reserved_node_exchange_configuration_options("test-action_type", cluster_identifier="test-cluster_identifier", snapshot_identifier="test-snapshot_identifier", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.get_reserved_node_exchange_configuration_options.assert_called_once()

def test_get_reserved_node_exchange_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import get_reserved_node_exchange_offerings
    mock_client = MagicMock()
    mock_client.get_reserved_node_exchange_offerings.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    get_reserved_node_exchange_offerings("test-reserved_node_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.get_reserved_node_exchange_offerings.assert_called_once()

def test_list_recommendations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import list_recommendations
    mock_client = MagicMock()
    mock_client.list_recommendations.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    list_recommendations(cluster_identifier="test-cluster_identifier", namespace_arn="test-namespace_arn", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.list_recommendations.assert_called_once()

def test_modify_aqua_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_aqua_configuration
    mock_client = MagicMock()
    mock_client.modify_aqua_configuration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_aqua_configuration("test-cluster_identifier", aqua_configuration_status={}, region_name="us-east-1")
    mock_client.modify_aqua_configuration.assert_called_once()

def test_modify_cluster_iam_roles_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_cluster_iam_roles
    mock_client = MagicMock()
    mock_client.modify_cluster_iam_roles.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_iam_roles("test-cluster_identifier", add_iam_roles="test-add_iam_roles", remove_iam_roles="test-remove_iam_roles", default_iam_role_arn="test-default_iam_role_arn", region_name="us-east-1")
    mock_client.modify_cluster_iam_roles.assert_called_once()

def test_modify_cluster_maintenance_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_cluster_maintenance
    mock_client = MagicMock()
    mock_client.modify_cluster_maintenance.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_maintenance("test-cluster_identifier", defer_maintenance="test-defer_maintenance", defer_maintenance_identifier="test-defer_maintenance_identifier", defer_maintenance_start_time="test-defer_maintenance_start_time", defer_maintenance_end_time="test-defer_maintenance_end_time", defer_maintenance_duration=1, region_name="us-east-1")
    mock_client.modify_cluster_maintenance.assert_called_once()

def test_modify_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_cluster_snapshot
    mock_client = MagicMock()
    mock_client.modify_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_snapshot("test-snapshot_identifier", manual_snapshot_retention_period="test-manual_snapshot_retention_period", force=True, region_name="us-east-1")
    mock_client.modify_cluster_snapshot.assert_called_once()

def test_modify_cluster_snapshot_schedule_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_cluster_snapshot_schedule
    mock_client = MagicMock()
    mock_client.modify_cluster_snapshot_schedule.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_snapshot_schedule("test-cluster_identifier", schedule_identifier="test-schedule_identifier", disassociate_schedule="test-disassociate_schedule", region_name="us-east-1")
    mock_client.modify_cluster_snapshot_schedule.assert_called_once()

def test_modify_cluster_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_cluster_subnet_group
    mock_client = MagicMock()
    mock_client.modify_cluster_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_cluster_subnet_group("test-cluster_subnet_group_name", "test-subnet_ids", description="test-description", region_name="us-east-1")
    mock_client.modify_cluster_subnet_group.assert_called_once()

def test_modify_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_endpoint_access
    mock_client = MagicMock()
    mock_client.modify_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_endpoint_access("test-endpoint_name", vpc_security_group_ids="test-vpc_security_group_ids", region_name="us-east-1")
    mock_client.modify_endpoint_access.assert_called_once()

def test_modify_event_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_event_subscription
    mock_client = MagicMock()
    mock_client.modify_event_subscription.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_event_subscription("test-subscription_name", sns_topic_arn="test-sns_topic_arn", source_type="test-source_type", source_ids="test-source_ids", event_categories="test-event_categories", severity="test-severity", enabled=True, region_name="us-east-1")
    mock_client.modify_event_subscription.assert_called_once()

def test_modify_integration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_integration
    mock_client = MagicMock()
    mock_client.modify_integration.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_integration("test-integration_arn", description="test-description", integration_name="test-integration_name", region_name="us-east-1")
    mock_client.modify_integration.assert_called_once()

def test_modify_redshift_idc_application_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_redshift_idc_application
    mock_client = MagicMock()
    mock_client.modify_redshift_idc_application.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_redshift_idc_application("test-redshift_idc_application_arn", identity_namespace="test-identity_namespace", iam_role_arn="test-iam_role_arn", idc_display_name="test-idc_display_name", authorized_token_issuer_list="test-authorized_token_issuer_list", service_integrations="test-service_integrations", region_name="us-east-1")
    mock_client.modify_redshift_idc_application.assert_called_once()

def test_modify_scheduled_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_scheduled_action
    mock_client = MagicMock()
    mock_client.modify_scheduled_action.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_scheduled_action("test-scheduled_action_name", target_action="test-target_action", schedule="test-schedule", iam_role="test-iam_role", scheduled_action_description="test-scheduled_action_description", start_time="test-start_time", end_time="test-end_time", enable=True, region_name="us-east-1")
    mock_client.modify_scheduled_action.assert_called_once()

def test_modify_snapshot_copy_retention_period_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_snapshot_copy_retention_period
    mock_client = MagicMock()
    mock_client.modify_snapshot_copy_retention_period.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_snapshot_copy_retention_period("test-cluster_identifier", "test-retention_period", manual="test-manual", region_name="us-east-1")
    mock_client.modify_snapshot_copy_retention_period.assert_called_once()

def test_modify_usage_limit_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import modify_usage_limit
    mock_client = MagicMock()
    mock_client.modify_usage_limit.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    modify_usage_limit(1, amount="test-amount", breach_action="test-breach_action", region_name="us-east-1")
    mock_client.modify_usage_limit.assert_called_once()

def test_purchase_reserved_node_offering_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import purchase_reserved_node_offering
    mock_client = MagicMock()
    mock_client.purchase_reserved_node_offering.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_node_offering("test-reserved_node_offering_id", node_count=1, region_name="us-east-1")
    mock_client.purchase_reserved_node_offering.assert_called_once()

def test_reset_cluster_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import reset_cluster_parameter_group
    mock_client = MagicMock()
    mock_client.reset_cluster_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    reset_cluster_parameter_group("test-parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameters="test-parameters", region_name="us-east-1")
    mock_client.reset_cluster_parameter_group.assert_called_once()

def test_resize_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import resize_cluster
    mock_client = MagicMock()
    mock_client.resize_cluster.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    resize_cluster("test-cluster_identifier", cluster_type="test-cluster_type", node_type="test-node_type", number_of_nodes="test-number_of_nodes", classic="test-classic", reserved_node_id="test-reserved_node_id", target_reserved_node_offering_id="test-target_reserved_node_offering_id", region_name="us-east-1")
    mock_client.resize_cluster.assert_called_once()

def test_restore_table_from_cluster_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import restore_table_from_cluster_snapshot
    mock_client = MagicMock()
    mock_client.restore_table_from_cluster_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    restore_table_from_cluster_snapshot("test-cluster_identifier", "test-snapshot_identifier", "test-source_database_name", "test-source_table_name", "test-new_table_name", source_schema_name="test-source_schema_name", target_database_name="test-target_database_name", target_schema_name="test-target_schema_name", enable_case_sensitive_identifier=True, region_name="us-east-1")
    mock_client.restore_table_from_cluster_snapshot.assert_called_once()

def test_revoke_cluster_security_group_ingress_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import revoke_cluster_security_group_ingress
    mock_client = MagicMock()
    mock_client.revoke_cluster_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    revoke_cluster_security_group_ingress("test-cluster_security_group_name", cidrip="test-cidrip", ec2_security_group_name="test-ec2_security_group_name", ec2_security_group_owner_id="test-ec2_security_group_owner_id", region_name="us-east-1")
    mock_client.revoke_cluster_security_group_ingress.assert_called_once()

def test_revoke_endpoint_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import revoke_endpoint_access
    mock_client = MagicMock()
    mock_client.revoke_endpoint_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    revoke_endpoint_access(cluster_identifier="test-cluster_identifier", account=1, vpc_ids="test-vpc_ids", force=True, region_name="us-east-1")
    mock_client.revoke_endpoint_access.assert_called_once()

def test_revoke_snapshot_access_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import revoke_snapshot_access
    mock_client = MagicMock()
    mock_client.revoke_snapshot_access.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    revoke_snapshot_access(1, snapshot_identifier="test-snapshot_identifier", snapshot_arn="test-snapshot_arn", snapshot_cluster_identifier="test-snapshot_cluster_identifier", region_name="us-east-1")
    mock_client.revoke_snapshot_access.assert_called_once()

def test_update_partner_status_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.redshift import update_partner_status
    mock_client = MagicMock()
    mock_client.update_partner_status.return_value = {}
    monkeypatch.setattr("aws_util.redshift.get_client", lambda *a, **kw: mock_client)
    update_partner_status(1, "test-cluster_identifier", "test-database_name", "test-partner_name", "test-status", status_message="test-status_message", region_name="us-east-1")
    mock_client.update_partner_status.assert_called_once()
