"""Tests for aws_util.elasticache — 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.elasticache as ec_mod
from aws_util.elasticache import (
    CacheClusterResult,
    CacheSubnetGroupResult,
    ReplicationGroupResult,
    SnapshotResult,
    _parse_cluster,
    _parse_replication_group,
    _parse_snapshot,
    _parse_subnet_group,
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

REGION = "us-east-1"

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
    "SomeExtra": "value",
}

_RG_DATA: dict = {
    "ReplicationGroupId": "my-rg",
    "Description": "test group",
    "Status": "available",
    "MemberClusters": ["my-cluster"],
    "NodeGroups": [{"NodeGroupId": "0001"}],
    "AutomaticFailover": "enabled",
    "SomeExtra": "value",
}

_SUBNET_DATA: dict = {
    "CacheSubnetGroupName": "my-subnet",
    "CacheSubnetGroupDescription": "my description",
    "VpcId": "vpc-123",
    "Subnets": [
        {"SubnetIdentifier": "subnet-a"},
        {"SubnetIdentifier": "subnet-b"},
    ],
    "SomeExtra": "value",
}

_SNAP_DATA: dict = {
    "SnapshotName": "my-snap",
    "CacheClusterId": "my-cluster",
    "ReplicationGroupId": "my-rg",
    "SnapshotStatus": "available",
    "SomeExtra": "value",
}


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestCacheClusterResultModel:
    def test_basic_fields(self):
        r = CacheClusterResult(
            cache_cluster_id="c1",
            cache_cluster_status="available",
            cache_node_type="cache.t3.micro",
            engine="redis",
            engine_version="7.0",
            num_cache_nodes=1,
        )
        assert r.cache_cluster_id == "c1"
        assert r.preferred_availability_zone is None
        assert r.extra == {}

    def test_frozen(self):
        r = CacheClusterResult(
            cache_cluster_id="c1",
            cache_cluster_status="available",
            cache_node_type="cache.t3.micro",
            engine="redis",
            engine_version="7.0",
            num_cache_nodes=1,
        )
        with pytest.raises(Exception):
            r.cache_cluster_id = "c2"  # type: ignore[misc]


class TestReplicationGroupResultModel:
    def test_basic_fields(self):
        r = ReplicationGroupResult(
            replication_group_id="rg1",
            description="desc",
            status="available",
        )
        assert r.replication_group_id == "rg1"
        assert r.member_clusters == []
        assert r.node_groups == []
        assert r.automatic_failover == "disabled"
        assert r.extra == {}

    def test_frozen(self):
        r = ReplicationGroupResult(
            replication_group_id="rg1",
            description="desc",
            status="available",
        )
        with pytest.raises(Exception):
            r.status = "creating"  # type: ignore[misc]


class TestCacheSubnetGroupResultModel:
    def test_basic_fields(self):
        r = CacheSubnetGroupResult(
            name="sg1", description="desc", vpc_id="vpc-1"
        )
        assert r.name == "sg1"
        assert r.subnets == []

    def test_frozen(self):
        r = CacheSubnetGroupResult(
            name="sg1", description="desc", vpc_id="vpc-1"
        )
        with pytest.raises(Exception):
            r.name = "sg2"  # type: ignore[misc]


class TestSnapshotResultModel:
    def test_basic_fields(self):
        r = SnapshotResult(snapshot_name="s1", snapshot_status="available")
        assert r.snapshot_name == "s1"
        assert r.cache_cluster_id is None
        assert r.replication_group_id is None

    def test_frozen(self):
        r = SnapshotResult(snapshot_name="s1", snapshot_status="available")
        with pytest.raises(Exception):
            r.snapshot_name = "s2"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


class TestParsers:
    def test_parse_cluster(self):
        r = _parse_cluster(_CLUSTER_DATA)
        assert r.cache_cluster_id == "my-cluster"
        assert r.cache_cluster_status == "available"
        assert r.engine == "redis"
        assert r.extra["SomeExtra"] == "value"

    def test_parse_cluster_minimal(self):
        r = _parse_cluster({"CacheClusterId": "x"})
        assert r.cache_cluster_id == "x"
        assert r.cache_cluster_status == "unknown"
        assert r.engine == "unknown"

    def test_parse_replication_group(self):
        r = _parse_replication_group(_RG_DATA)
        assert r.replication_group_id == "my-rg"
        assert r.description == "test group"
        assert r.automatic_failover == "enabled"
        assert r.extra["SomeExtra"] == "value"

    def test_parse_replication_group_minimal(self):
        r = _parse_replication_group({"ReplicationGroupId": "x"})
        assert r.replication_group_id == "x"
        assert r.status == "unknown"

    def test_parse_subnet_group(self):
        r = _parse_subnet_group(_SUBNET_DATA)
        assert r.name == "my-subnet"
        assert r.vpc_id == "vpc-123"
        assert r.subnets == ["subnet-a", "subnet-b"]
        assert r.extra["SomeExtra"] == "value"

    def test_parse_subnet_group_minimal(self):
        r = _parse_subnet_group({"CacheSubnetGroupName": "x"})
        assert r.name == "x"
        assert r.subnets == []

    def test_parse_snapshot(self):
        r = _parse_snapshot(_SNAP_DATA)
        assert r.snapshot_name == "my-snap"
        assert r.cache_cluster_id == "my-cluster"
        assert r.extra["SomeExtra"] == "value"

    def test_parse_snapshot_minimal(self):
        r = _parse_snapshot({"SnapshotName": "x"})
        assert r.snapshot_name == "x"
        assert r.snapshot_status == "unknown"


# ---------------------------------------------------------------------------
# create_cache_cluster
# ---------------------------------------------------------------------------


class TestCreateCacheCluster:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cache_cluster.return_value = {
            "CacheCluster": _CLUSTER_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_cache_cluster("my-cluster")
        assert r.cache_cluster_id == "my-cluster"
        mock_client.create_cache_cluster.assert_called_once()

    def test_with_optional_params(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cache_cluster.return_value = {
            "CacheCluster": _CLUSTER_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_cache_cluster(
            "my-cluster",
            cache_subnet_group_name="sg",
            security_group_ids=["sg-1"],
            tags={"env": "test"},
        )
        assert r.cache_cluster_id == "my-cluster"
        call_kwargs = mock_client.create_cache_cluster.call_args[1]
        assert call_kwargs["CacheSubnetGroupName"] == "sg"
        assert call_kwargs["SecurityGroupIds"] == ["sg-1"]
        assert call_kwargs["Tags"] == [{"Key": "env", "Value": "test"}]

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cache_cluster.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterValue", "Message": "fail"}},
            "CreateCacheCluster",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to create cache cluster"):
            create_cache_cluster("bad-cluster")


# ---------------------------------------------------------------------------
# describe_cache_clusters
# ---------------------------------------------------------------------------


class TestDescribeCacheClusters:
    def test_returns_all(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"CacheClusters": [_CLUSTER_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_cache_clusters()
        assert len(result) == 1
        assert result[0].cache_cluster_id == "my-cluster"

    def test_with_cluster_id(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"CacheClusters": [_CLUSTER_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_cache_clusters(cache_cluster_id="my-cluster")
        assert len(result) == 1

    def test_empty(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"CacheClusters": []}]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_cache_clusters()
        assert result == []

    def test_client_error(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeCacheClusters",
        )
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="describe_cache_clusters failed"):
            describe_cache_clusters()


# ---------------------------------------------------------------------------
# modify_cache_cluster
# ---------------------------------------------------------------------------


class TestModifyCacheCluster:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_cache_cluster.return_value = {
            "CacheCluster": _CLUSTER_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = modify_cache_cluster("my-cluster", num_cache_nodes=3)
        assert r.cache_cluster_id == "my-cluster"

    def test_with_cache_node_type(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_cache_cluster.return_value = {
            "CacheCluster": _CLUSTER_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = modify_cache_cluster(
            "my-cluster", cache_node_type="cache.r6g.large"
        )
        assert r.cache_cluster_id == "my-cluster"
        call_kwargs = mock_client.modify_cache_cluster.call_args[1]
        assert call_kwargs["CacheNodeType"] == "cache.r6g.large"

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_cache_cluster.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterValue", "Message": "fail"}},
            "ModifyCacheCluster",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to modify cache cluster"):
            modify_cache_cluster("bad-cluster")


# ---------------------------------------------------------------------------
# delete_cache_cluster
# ---------------------------------------------------------------------------


class TestDeleteCacheCluster:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_cache_cluster.return_value = {}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        delete_cache_cluster("my-cluster")
        mock_client.delete_cache_cluster.assert_called_once_with(
            CacheClusterId="my-cluster"
        )

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_cache_cluster.side_effect = ClientError(
            {"Error": {"Code": "CacheClusterNotFound", "Message": "not found"}},
            "DeleteCacheCluster",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to delete cache cluster"):
            delete_cache_cluster("ghost")


# ---------------------------------------------------------------------------
# reboot_cache_cluster
# ---------------------------------------------------------------------------


class TestRebootCacheCluster:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.reboot_cache_cluster.return_value = {
            "CacheCluster": _CLUSTER_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = reboot_cache_cluster("my-cluster", node_ids_to_reboot=["0001"])
        assert r.cache_cluster_id == "my-cluster"
        mock_client.reboot_cache_cluster.assert_called_once_with(
            CacheClusterId="my-cluster",
            CacheNodeIdsToReboot=["0001"],
        )

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.reboot_cache_cluster.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterValue", "Message": "fail"}},
            "RebootCacheCluster",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to reboot cache cluster"):
            reboot_cache_cluster("bad", node_ids_to_reboot=["0001"])


# ---------------------------------------------------------------------------
# create_replication_group
# ---------------------------------------------------------------------------


class TestCreateReplicationGroup:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_replication_group.return_value = {
            "ReplicationGroup": _RG_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_replication_group("my-rg", description="test group")
        assert r.replication_group_id == "my-rg"

    def test_with_optional_params(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_replication_group.return_value = {
            "ReplicationGroup": _RG_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_replication_group(
            "my-rg",
            description="test",
            primary_cluster_id="c1",
            num_cache_clusters=3,
            cache_node_type="cache.r6g.large",
            automatic_failover_enabled=True,
        )
        assert r.replication_group_id == "my-rg"
        call_kwargs = mock_client.create_replication_group.call_args[1]
        assert call_kwargs["PrimaryClusterId"] == "c1"
        assert call_kwargs["NumCacheClusters"] == 3
        assert call_kwargs["CacheNodeType"] == "cache.r6g.large"
        assert call_kwargs["AutomaticFailoverEnabled"] is True

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_replication_group.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterValue", "Message": "fail"}},
            "CreateReplicationGroup",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(
            RuntimeError, match="Failed to create replication group"
        ):
            create_replication_group("bad", description="test")


# ---------------------------------------------------------------------------
# describe_replication_groups
# ---------------------------------------------------------------------------


class TestDescribeReplicationGroups:
    def test_returns_all(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"ReplicationGroups": [_RG_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_replication_groups()
        assert len(result) == 1

    def test_with_id(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"ReplicationGroups": [_RG_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_replication_groups(
            replication_group_id="my-rg"
        )
        assert len(result) == 1

    def test_empty(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"ReplicationGroups": []}]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        assert describe_replication_groups() == []

    def test_client_error(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeReplicationGroups",
        )
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(
            RuntimeError, match="describe_replication_groups failed"
        ):
            describe_replication_groups()


# ---------------------------------------------------------------------------
# modify_replication_group
# ---------------------------------------------------------------------------


class TestModifyReplicationGroup:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_replication_group.return_value = {
            "ReplicationGroup": _RG_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = modify_replication_group("my-rg", description="updated")
        assert r.replication_group_id == "my-rg"

    def test_with_failover(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_replication_group.return_value = {
            "ReplicationGroup": _RG_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = modify_replication_group(
            "my-rg", automatic_failover_enabled=True
        )
        assert r.replication_group_id == "my-rg"
        call_kwargs = mock_client.modify_replication_group.call_args[1]
        assert call_kwargs["AutomaticFailoverEnabled"] is True

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_replication_group.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterValue", "Message": "fail"}},
            "ModifyReplicationGroup",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(
            RuntimeError, match="Failed to modify replication group"
        ):
            modify_replication_group("bad")


# ---------------------------------------------------------------------------
# delete_replication_group
# ---------------------------------------------------------------------------


class TestDeleteReplicationGroup:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_replication_group.return_value = {}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        delete_replication_group("my-rg")
        mock_client.delete_replication_group.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_replication_group.side_effect = ClientError(
            {"Error": {"Code": "ReplicationGroupNotFoundFault", "Message": "nf"}},
            "DeleteReplicationGroup",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(
            RuntimeError, match="Failed to delete replication group"
        ):
            delete_replication_group("ghost")


# ---------------------------------------------------------------------------
# create_cache_subnet_group
# ---------------------------------------------------------------------------


class TestCreateCacheSubnetGroup:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cache_subnet_group.return_value = {
            "CacheSubnetGroup": _SUBNET_DATA
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_cache_subnet_group(
            "my-subnet", description="desc", subnet_ids=["subnet-a"]
        )
        assert r.name == "my-subnet"

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cache_subnet_group.side_effect = ClientError(
            {"Error": {"Code": "CacheSubnetGroupAlreadyExists", "Message": "x"}},
            "CreateCacheSubnetGroup",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(
            RuntimeError, match="Failed to create cache subnet group"
        ):
            create_cache_subnet_group(
                "dup", description="desc", subnet_ids=["s"]
            )


# ---------------------------------------------------------------------------
# describe_cache_subnet_groups
# ---------------------------------------------------------------------------


class TestDescribeCacheSubnetGroups:
    def test_returns_all(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"CacheSubnetGroups": [_SUBNET_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_cache_subnet_groups()
        assert len(result) == 1

    def test_with_name(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"CacheSubnetGroups": [_SUBNET_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_cache_subnet_groups(name="my-subnet")
        assert len(result) == 1

    def test_client_error(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeCacheSubnetGroups",
        )
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(
            RuntimeError, match="describe_cache_subnet_groups failed"
        ):
            describe_cache_subnet_groups()


# ---------------------------------------------------------------------------
# create_snapshot
# ---------------------------------------------------------------------------


class TestCreateSnapshot:
    def test_success_with_cluster(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_snapshot.return_value = {"Snapshot": _SNAP_DATA}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_snapshot("my-snap", cache_cluster_id="my-cluster")
        assert r.snapshot_name == "my-snap"

    def test_success_with_rg(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_snapshot.return_value = {"Snapshot": _SNAP_DATA}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        r = create_snapshot("my-snap", replication_group_id="my-rg")
        assert r.snapshot_name == "my-snap"

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_snapshot.side_effect = ClientError(
            {"Error": {"Code": "SnapshotAlreadyExistsFault", "Message": "dup"}},
            "CreateSnapshot",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to create snapshot"):
            create_snapshot("dup-snap")


# ---------------------------------------------------------------------------
# describe_snapshots
# ---------------------------------------------------------------------------


class TestDescribeSnapshots:
    def test_returns_all(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Snapshots": [_SNAP_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_snapshots()
        assert len(result) == 1

    def test_with_name(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Snapshots": [_SNAP_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_snapshots(snapshot_name="my-snap")
        assert len(result) == 1

    def test_with_cluster_id(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Snapshots": [_SNAP_DATA]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        result = describe_snapshots(cache_cluster_id="my-cluster")
        assert len(result) == 1

    def test_client_error(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.side_effect = ClientError(
            {"Error": {"Code": "InternalFailure", "Message": "fail"}},
            "DescribeSnapshots",
        )
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="describe_snapshots failed"):
            describe_snapshots()


# ---------------------------------------------------------------------------
# delete_snapshot
# ---------------------------------------------------------------------------


class TestDeleteSnapshot:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_snapshot.return_value = {}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        delete_snapshot("my-snap")
        mock_client.delete_snapshot.assert_called_once_with(
            SnapshotName="my-snap"
        )

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_snapshot.side_effect = ClientError(
            {"Error": {"Code": "SnapshotNotFoundFault", "Message": "nf"}},
            "DeleteSnapshot",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to delete snapshot"):
            delete_snapshot("ghost")


# ---------------------------------------------------------------------------
# list_tags_for_resource
# ---------------------------------------------------------------------------


class TestListTagsForResource:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_tags_for_resource.return_value = {
            "TagList": [{"Key": "env", "Value": "prod"}]
        }
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        tags = list_tags_for_resource("arn:aws:elasticache:us-east-1:123:cluster:my-cluster")
        assert tags == {"env": "prod"}

    def test_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_tags_for_resource.return_value = {"TagList": []}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        tags = list_tags_for_resource("arn:aws:elasticache:us-east-1:123:cluster:my-cluster")
        assert tags == {}

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_tags_for_resource.side_effect = ClientError(
            {"Error": {"Code": "CacheClusterNotFound", "Message": "nf"}},
            "ListTagsForResource",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to list tags"):
            list_tags_for_resource("arn:bad")


# ---------------------------------------------------------------------------
# add_tags_to_resource
# ---------------------------------------------------------------------------


class TestAddTagsToResource:
    def test_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.add_tags_to_resource.return_value = {}
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        add_tags_to_resource(
            "arn:aws:elasticache:us-east-1:123:cluster:my-cluster",
            tags={"env": "prod"},
        )
        mock_client.add_tags_to_resource.assert_called_once()

    def test_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.add_tags_to_resource.side_effect = ClientError(
            {"Error": {"Code": "CacheClusterNotFound", "Message": "nf"}},
            "AddTagsToResource",
        )
        monkeypatch.setattr(ec_mod, "get_client", lambda *a, **kw: mock_client)

        with pytest.raises(RuntimeError, match="Failed to add tags"):
            add_tags_to_resource("arn:bad", tags={"a": "b"})


# ---------------------------------------------------------------------------
# wait_for_cache_cluster
# ---------------------------------------------------------------------------


class TestWaitForCacheCluster:
    def test_returns_immediately(self, monkeypatch):
        monkeypatch.setattr(
            ec_mod,
            "describe_cache_clusters",
            lambda **kw: [
                CacheClusterResult(
                    cache_cluster_id="c1",
                    cache_cluster_status="available",
                    cache_node_type="cache.t3.micro",
                    engine="redis",
                    engine_version="7.0",
                    num_cache_nodes=1,
                )
            ],
        )
        r = wait_for_cache_cluster("c1", timeout=5.0)
        assert r.cache_cluster_status == "available"

    def test_not_found(self, monkeypatch):
        monkeypatch.setattr(
            ec_mod, "describe_cache_clusters", lambda **kw: []
        )
        with pytest.raises(RuntimeError, match="not found"):
            wait_for_cache_cluster("ghost", timeout=1.0)

    def test_timeout(self, monkeypatch):
        monkeypatch.setattr(
            ec_mod,
            "describe_cache_clusters",
            lambda **kw: [
                CacheClusterResult(
                    cache_cluster_id="c1",
                    cache_cluster_status="creating",
                    cache_node_type="cache.t3.micro",
                    engine="redis",
                    engine_version="7.0",
                    num_cache_nodes=1,
                )
            ],
        )
        monkeypatch.setattr(time, "sleep", lambda s: None)
        with pytest.raises(TimeoutError, match="did not reach status"):
            wait_for_cache_cluster(
                "c1", target_status="available", timeout=0.0, poll_interval=0.0
            )

    def test_sleep_branch(self, monkeypatch):
        """Covers time.sleep in the polling loop."""
        monkeypatch.setattr(time, "sleep", lambda s: None)
        call_count = {"n": 0}

        def fake_describe(**kw):
            call_count["n"] += 1
            status = "creating" if call_count["n"] < 2 else "available"
            return [
                CacheClusterResult(
                    cache_cluster_id="c1",
                    cache_cluster_status=status,
                    cache_node_type="cache.t3.micro",
                    engine="redis",
                    engine_version="7.0",
                    num_cache_nodes=1,
                )
            ]

        monkeypatch.setattr(ec_mod, "describe_cache_clusters", fake_describe)
        r = wait_for_cache_cluster(
            "c1", timeout=10.0, poll_interval=0.001
        )
        assert r.cache_cluster_status == "available"


# ---------------------------------------------------------------------------
# wait_for_replication_group
# ---------------------------------------------------------------------------


class TestWaitForReplicationGroup:
    def test_returns_immediately(self, monkeypatch):
        monkeypatch.setattr(
            ec_mod,
            "describe_replication_groups",
            lambda **kw: [
                ReplicationGroupResult(
                    replication_group_id="rg1",
                    description="test",
                    status="available",
                )
            ],
        )
        r = wait_for_replication_group("rg1", timeout=5.0)
        assert r.status == "available"

    def test_not_found(self, monkeypatch):
        monkeypatch.setattr(
            ec_mod, "describe_replication_groups", lambda **kw: []
        )
        with pytest.raises(RuntimeError, match="not found"):
            wait_for_replication_group("ghost", timeout=1.0)

    def test_timeout(self, monkeypatch):
        monkeypatch.setattr(
            ec_mod,
            "describe_replication_groups",
            lambda **kw: [
                ReplicationGroupResult(
                    replication_group_id="rg1",
                    description="test",
                    status="creating",
                )
            ],
        )
        monkeypatch.setattr(time, "sleep", lambda s: None)
        with pytest.raises(TimeoutError, match="did not reach status"):
            wait_for_replication_group(
                "rg1", target_status="available", timeout=0.0, poll_interval=0.0
            )

    def test_sleep_branch(self, monkeypatch):
        """Covers time.sleep in the polling loop."""
        monkeypatch.setattr(time, "sleep", lambda s: None)
        call_count = {"n": 0}

        def fake_describe(**kw):
            call_count["n"] += 1
            status = "creating" if call_count["n"] < 2 else "available"
            return [
                ReplicationGroupResult(
                    replication_group_id="rg1",
                    description="test",
                    status=status,
                )
            ]

        monkeypatch.setattr(
            ec_mod, "describe_replication_groups", fake_describe
        )
        r = wait_for_replication_group(
            "rg1", timeout=10.0, poll_interval=0.001
        )
        assert r.status == "available"


# ---------------------------------------------------------------------------
# ensure_cache_cluster
# ---------------------------------------------------------------------------


class TestEnsureCacheCluster:
    def test_existing(self, monkeypatch):
        cluster = CacheClusterResult(
            cache_cluster_id="c1",
            cache_cluster_status="available",
            cache_node_type="cache.t3.micro",
            engine="redis",
            engine_version="7.0",
            num_cache_nodes=1,
        )
        monkeypatch.setattr(
            ec_mod, "describe_cache_clusters", lambda **kw: [cluster]
        )
        r, created = ensure_cache_cluster("c1")
        assert r.cache_cluster_id == "c1"
        assert created is False

    def test_creates_new(self, monkeypatch):
        cluster = CacheClusterResult(
            cache_cluster_id="c1",
            cache_cluster_status="creating",
            cache_node_type="cache.t3.micro",
            engine="redis",
            engine_version="7.0",
            num_cache_nodes=1,
        )
        monkeypatch.setattr(
            ec_mod, "describe_cache_clusters", lambda **kw: []
        )
        monkeypatch.setattr(
            ec_mod, "create_cache_cluster", lambda *a, **kw: cluster
        )
        r, created = ensure_cache_cluster("c1")
        assert created is True


# ---------------------------------------------------------------------------
# ensure_replication_group
# ---------------------------------------------------------------------------


class TestEnsureReplicationGroup:
    def test_existing(self, monkeypatch):
        rg = ReplicationGroupResult(
            replication_group_id="rg1",
            description="test",
            status="available",
        )
        monkeypatch.setattr(
            ec_mod, "describe_replication_groups", lambda **kw: [rg]
        )
        r, created = ensure_replication_group("rg1", description="test")
        assert r.replication_group_id == "rg1"
        assert created is False

    def test_creates_new(self, monkeypatch):
        rg = ReplicationGroupResult(
            replication_group_id="rg1",
            description="test",
            status="creating",
        )
        monkeypatch.setattr(
            ec_mod, "describe_replication_groups", lambda **kw: []
        )
        monkeypatch.setattr(
            ec_mod, "create_replication_group", lambda *a, **kw: rg
        )
        r, created = ensure_replication_group("rg1", description="test")
        assert created is True


def test_authorize_cache_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_cache_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    authorize_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", region_name=REGION)
    mock_client.authorize_cache_security_group_ingress.assert_called_once()


def test_authorize_cache_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.authorize_cache_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "authorize_cache_security_group_ingress",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to authorize cache security group ingress"):
        authorize_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", region_name=REGION)


def test_batch_apply_update_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_apply_update_action.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    batch_apply_update_action("test-service_update_name", region_name=REGION)
    mock_client.batch_apply_update_action.assert_called_once()


def test_batch_apply_update_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_apply_update_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_apply_update_action",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch apply update action"):
        batch_apply_update_action("test-service_update_name", region_name=REGION)


def test_batch_stop_update_action(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_stop_update_action.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    batch_stop_update_action("test-service_update_name", region_name=REGION)
    mock_client.batch_stop_update_action.assert_called_once()


def test_batch_stop_update_action_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_stop_update_action.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_stop_update_action",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch stop update action"):
        batch_stop_update_action("test-service_update_name", region_name=REGION)


def test_complete_migration(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_migration.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    complete_migration("test-replication_group_id", region_name=REGION)
    mock_client.complete_migration.assert_called_once()


def test_complete_migration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.complete_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "complete_migration",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to complete migration"):
        complete_migration("test-replication_group_id", region_name=REGION)


def test_copy_serverless_cache_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_serverless_cache_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    copy_serverless_cache_snapshot("test-source_serverless_cache_snapshot_name", "test-target_serverless_cache_snapshot_name", region_name=REGION)
    mock_client.copy_serverless_cache_snapshot.assert_called_once()


def test_copy_serverless_cache_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_serverless_cache_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_serverless_cache_snapshot",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy serverless cache snapshot"):
        copy_serverless_cache_snapshot("test-source_serverless_cache_snapshot_name", "test-target_serverless_cache_snapshot_name", region_name=REGION)


def test_copy_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    copy_snapshot("test-source_snapshot_name", "test-target_snapshot_name", region_name=REGION)
    mock_client.copy_snapshot.assert_called_once()


def test_copy_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.copy_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "copy_snapshot",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to copy snapshot"):
        copy_snapshot("test-source_snapshot_name", "test-target_snapshot_name", region_name=REGION)


def test_create_cache_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cache_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_cache_parameter_group("test-cache_parameter_group_name", "test-cache_parameter_group_family", "test-description", region_name=REGION)
    mock_client.create_cache_parameter_group.assert_called_once()


def test_create_cache_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cache_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cache_parameter_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cache parameter group"):
        create_cache_parameter_group("test-cache_parameter_group_name", "test-cache_parameter_group_family", "test-description", region_name=REGION)


def test_create_cache_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cache_security_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_cache_security_group("test-cache_security_group_name", "test-description", region_name=REGION)
    mock_client.create_cache_security_group.assert_called_once()


def test_create_cache_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cache_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cache_security_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cache security group"):
        create_cache_security_group("test-cache_security_group_name", "test-description", region_name=REGION)


def test_create_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_global_replication_group("test-global_replication_group_id_suffix", "test-primary_replication_group_id", region_name=REGION)
    mock_client.create_global_replication_group.assert_called_once()


def test_create_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create global replication group"):
        create_global_replication_group("test-global_replication_group_id_suffix", "test-primary_replication_group_id", region_name=REGION)


def test_create_serverless_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_serverless_cache.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_serverless_cache("test-serverless_cache_name", "test-engine", region_name=REGION)
    mock_client.create_serverless_cache.assert_called_once()


def test_create_serverless_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_serverless_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_serverless_cache",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create serverless cache"):
        create_serverless_cache("test-serverless_cache_name", "test-engine", region_name=REGION)


def test_create_serverless_cache_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_serverless_cache_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-serverless_cache_name", region_name=REGION)
    mock_client.create_serverless_cache_snapshot.assert_called_once()


def test_create_serverless_cache_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_serverless_cache_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_serverless_cache_snapshot",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create serverless cache snapshot"):
        create_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-serverless_cache_name", region_name=REGION)


def test_create_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_user("test-user_id", "test-user_name", "test-engine", "test-access_string", region_name=REGION)
    mock_client.create_user.assert_called_once()


def test_create_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user"):
        create_user("test-user_id", "test-user_name", "test-engine", "test-access_string", region_name=REGION)


def test_create_user_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_user_group("test-user_group_id", "test-engine", region_name=REGION)
    mock_client.create_user_group.assert_called_once()


def test_create_user_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_user_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_user_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create user group"):
        create_user_group("test-user_group_id", "test-engine", region_name=REGION)


def test_decrease_node_groups_in_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.decrease_node_groups_in_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    decrease_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, region_name=REGION)
    mock_client.decrease_node_groups_in_global_replication_group.assert_called_once()


def test_decrease_node_groups_in_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.decrease_node_groups_in_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decrease_node_groups_in_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to decrease node groups in global replication group"):
        decrease_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, region_name=REGION)


def test_decrease_replica_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.decrease_replica_count.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    decrease_replica_count("test-replication_group_id", True, region_name=REGION)
    mock_client.decrease_replica_count.assert_called_once()


def test_decrease_replica_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.decrease_replica_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "decrease_replica_count",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to decrease replica count"):
        decrease_replica_count("test-replication_group_id", True, region_name=REGION)


def test_delete_cache_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_cache_parameter_group("test-cache_parameter_group_name", region_name=REGION)
    mock_client.delete_cache_parameter_group.assert_called_once()


def test_delete_cache_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cache_parameter_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cache parameter group"):
        delete_cache_parameter_group("test-cache_parameter_group_name", region_name=REGION)


def test_delete_cache_security_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_security_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_cache_security_group("test-cache_security_group_name", region_name=REGION)
    mock_client.delete_cache_security_group.assert_called_once()


def test_delete_cache_security_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_security_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cache_security_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cache security group"):
        delete_cache_security_group("test-cache_security_group_name", region_name=REGION)


def test_delete_cache_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_cache_subnet_group("test-cache_subnet_group_name", region_name=REGION)
    mock_client.delete_cache_subnet_group.assert_called_once()


def test_delete_cache_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cache_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cache_subnet_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cache subnet group"):
        delete_cache_subnet_group("test-cache_subnet_group_name", region_name=REGION)


def test_delete_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_global_replication_group("test-global_replication_group_id", True, region_name=REGION)
    mock_client.delete_global_replication_group.assert_called_once()


def test_delete_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete global replication group"):
        delete_global_replication_group("test-global_replication_group_id", True, region_name=REGION)


def test_delete_serverless_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_serverless_cache.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_serverless_cache("test-serverless_cache_name", region_name=REGION)
    mock_client.delete_serverless_cache.assert_called_once()


def test_delete_serverless_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_serverless_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_serverless_cache",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete serverless cache"):
        delete_serverless_cache("test-serverless_cache_name", region_name=REGION)


def test_delete_serverless_cache_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_serverless_cache_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_serverless_cache_snapshot("test-serverless_cache_snapshot_name", region_name=REGION)
    mock_client.delete_serverless_cache_snapshot.assert_called_once()


def test_delete_serverless_cache_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_serverless_cache_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_serverless_cache_snapshot",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete serverless cache snapshot"):
        delete_serverless_cache_snapshot("test-serverless_cache_snapshot_name", region_name=REGION)


def test_delete_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_user("test-user_id", region_name=REGION)
    mock_client.delete_user.assert_called_once()


def test_delete_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user"):
        delete_user("test-user_id", region_name=REGION)


def test_delete_user_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_user_group("test-user_group_id", region_name=REGION)
    mock_client.delete_user_group.assert_called_once()


def test_delete_user_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_user_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_user_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete user group"):
        delete_user_group("test-user_group_id", region_name=REGION)


def test_describe_cache_engine_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_engine_versions(region_name=REGION)
    mock_client.describe_cache_engine_versions.assert_called_once()


def test_describe_cache_engine_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cache_engine_versions",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cache engine versions"):
        describe_cache_engine_versions(region_name=REGION)


def test_describe_cache_parameter_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_parameter_groups(region_name=REGION)
    mock_client.describe_cache_parameter_groups.assert_called_once()


def test_describe_cache_parameter_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cache_parameter_groups",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cache parameter groups"):
        describe_cache_parameter_groups(region_name=REGION)


def test_describe_cache_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_parameters.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_parameters("test-cache_parameter_group_name", region_name=REGION)
    mock_client.describe_cache_parameters.assert_called_once()


def test_describe_cache_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cache_parameters",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cache parameters"):
        describe_cache_parameters("test-cache_parameter_group_name", region_name=REGION)


def test_describe_cache_security_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_security_groups(region_name=REGION)
    mock_client.describe_cache_security_groups.assert_called_once()


def test_describe_cache_security_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cache_security_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cache_security_groups",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cache security groups"):
        describe_cache_security_groups(region_name=REGION)


def test_describe_engine_default_parameters(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_parameters("test-cache_parameter_group_family", region_name=REGION)
    mock_client.describe_engine_default_parameters.assert_called_once()


def test_describe_engine_default_parameters_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_default_parameters",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe engine default parameters"):
        describe_engine_default_parameters("test-cache_parameter_group_family", region_name=REGION)


def test_describe_events(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


def test_describe_events_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


def test_describe_global_replication_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_replication_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_global_replication_groups(region_name=REGION)
    mock_client.describe_global_replication_groups.assert_called_once()


def test_describe_global_replication_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_global_replication_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_global_replication_groups",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe global replication groups"):
        describe_global_replication_groups(region_name=REGION)


def test_describe_reserved_cache_nodes(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_cache_nodes.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_reserved_cache_nodes(region_name=REGION)
    mock_client.describe_reserved_cache_nodes.assert_called_once()


def test_describe_reserved_cache_nodes_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_cache_nodes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_cache_nodes",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved cache nodes"):
        describe_reserved_cache_nodes(region_name=REGION)


def test_describe_reserved_cache_nodes_offerings(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_cache_nodes_offerings.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_reserved_cache_nodes_offerings(region_name=REGION)
    mock_client.describe_reserved_cache_nodes_offerings.assert_called_once()


def test_describe_reserved_cache_nodes_offerings_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_reserved_cache_nodes_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_cache_nodes_offerings",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe reserved cache nodes offerings"):
        describe_reserved_cache_nodes_offerings(region_name=REGION)


def test_describe_serverless_cache_snapshots(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_serverless_cache_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_serverless_cache_snapshots(region_name=REGION)
    mock_client.describe_serverless_cache_snapshots.assert_called_once()


def test_describe_serverless_cache_snapshots_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_serverless_cache_snapshots.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_serverless_cache_snapshots",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe serverless cache snapshots"):
        describe_serverless_cache_snapshots(region_name=REGION)


def test_describe_serverless_caches(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_serverless_caches.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_serverless_caches(region_name=REGION)
    mock_client.describe_serverless_caches.assert_called_once()


def test_describe_serverless_caches_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_serverless_caches.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_serverless_caches",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe serverless caches"):
        describe_serverless_caches(region_name=REGION)


def test_describe_service_updates(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_updates.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_service_updates(region_name=REGION)
    mock_client.describe_service_updates.assert_called_once()


def test_describe_service_updates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_service_updates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_updates",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe service updates"):
        describe_service_updates(region_name=REGION)


def test_describe_update_actions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_update_actions.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_update_actions(region_name=REGION)
    mock_client.describe_update_actions.assert_called_once()


def test_describe_update_actions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_update_actions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_update_actions",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe update actions"):
        describe_update_actions(region_name=REGION)


def test_describe_user_groups(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_user_groups(region_name=REGION)
    mock_client.describe_user_groups.assert_called_once()


def test_describe_user_groups_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_user_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_user_groups",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe user groups"):
        describe_user_groups(region_name=REGION)


def test_describe_users(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_users.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_users(region_name=REGION)
    mock_client.describe_users.assert_called_once()


def test_describe_users_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_users.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_users",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe users"):
        describe_users(region_name=REGION)


def test_disassociate_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    disassociate_global_replication_group("test-global_replication_group_id", "test-replication_group_id", "test-replication_group_region", region_name=REGION)
    mock_client.disassociate_global_replication_group.assert_called_once()


def test_disassociate_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate global replication group"):
        disassociate_global_replication_group("test-global_replication_group_id", "test-replication_group_id", "test-replication_group_region", region_name=REGION)


def test_export_serverless_cache_snapshot(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_serverless_cache_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    export_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-s3_bucket_name", region_name=REGION)
    mock_client.export_serverless_cache_snapshot.assert_called_once()


def test_export_serverless_cache_snapshot_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.export_serverless_cache_snapshot.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "export_serverless_cache_snapshot",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to export serverless cache snapshot"):
        export_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-s3_bucket_name", region_name=REGION)


def test_failover_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    failover_global_replication_group("test-global_replication_group_id", "test-primary_region", "test-primary_replication_group_id", region_name=REGION)
    mock_client.failover_global_replication_group.assert_called_once()


def test_failover_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.failover_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to failover global replication group"):
        failover_global_replication_group("test-global_replication_group_id", "test-primary_region", "test-primary_replication_group_id", region_name=REGION)


def test_increase_node_groups_in_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.increase_node_groups_in_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    increase_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, region_name=REGION)
    mock_client.increase_node_groups_in_global_replication_group.assert_called_once()


def test_increase_node_groups_in_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.increase_node_groups_in_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "increase_node_groups_in_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to increase node groups in global replication group"):
        increase_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, region_name=REGION)


def test_increase_replica_count(monkeypatch):
    mock_client = MagicMock()
    mock_client.increase_replica_count.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    increase_replica_count("test-replication_group_id", True, region_name=REGION)
    mock_client.increase_replica_count.assert_called_once()


def test_increase_replica_count_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.increase_replica_count.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "increase_replica_count",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to increase replica count"):
        increase_replica_count("test-replication_group_id", True, region_name=REGION)


def test_list_allowed_node_type_modifications(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_allowed_node_type_modifications.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    list_allowed_node_type_modifications(region_name=REGION)
    mock_client.list_allowed_node_type_modifications.assert_called_once()


def test_list_allowed_node_type_modifications_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_allowed_node_type_modifications.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_allowed_node_type_modifications",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list allowed node type modifications"):
        list_allowed_node_type_modifications(region_name=REGION)


def test_modify_cache_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cache_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_cache_parameter_group("test-cache_parameter_group_name", [], region_name=REGION)
    mock_client.modify_cache_parameter_group.assert_called_once()


def test_modify_cache_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cache_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cache_parameter_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cache parameter group"):
        modify_cache_parameter_group("test-cache_parameter_group_name", [], region_name=REGION)


def test_modify_cache_subnet_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cache_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_cache_subnet_group("test-cache_subnet_group_name", region_name=REGION)
    mock_client.modify_cache_subnet_group.assert_called_once()


def test_modify_cache_subnet_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_cache_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_cache_subnet_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify cache subnet group"):
        modify_cache_subnet_group("test-cache_subnet_group_name", region_name=REGION)


def test_modify_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_global_replication_group("test-global_replication_group_id", True, region_name=REGION)
    mock_client.modify_global_replication_group.assert_called_once()


def test_modify_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify global replication group"):
        modify_global_replication_group("test-global_replication_group_id", True, region_name=REGION)


def test_modify_replication_group_shard_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_replication_group_shard_configuration.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_replication_group_shard_configuration("test-replication_group_id", 1, True, region_name=REGION)
    mock_client.modify_replication_group_shard_configuration.assert_called_once()


def test_modify_replication_group_shard_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_replication_group_shard_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_replication_group_shard_configuration",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify replication group shard configuration"):
        modify_replication_group_shard_configuration("test-replication_group_id", 1, True, region_name=REGION)


def test_modify_serverless_cache(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_serverless_cache.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_serverless_cache("test-serverless_cache_name", region_name=REGION)
    mock_client.modify_serverless_cache.assert_called_once()


def test_modify_serverless_cache_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_serverless_cache.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_serverless_cache",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify serverless cache"):
        modify_serverless_cache("test-serverless_cache_name", region_name=REGION)


def test_modify_user(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_user.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_user("test-user_id", region_name=REGION)
    mock_client.modify_user.assert_called_once()


def test_modify_user_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_user.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_user",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify user"):
        modify_user("test-user_id", region_name=REGION)


def test_modify_user_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_user_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_user_group("test-user_group_id", region_name=REGION)
    mock_client.modify_user_group.assert_called_once()


def test_modify_user_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.modify_user_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "modify_user_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to modify user group"):
        modify_user_group("test-user_group_id", region_name=REGION)


def test_purchase_reserved_cache_nodes_offering(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_cache_nodes_offering.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_cache_nodes_offering("test-reserved_cache_nodes_offering_id", region_name=REGION)
    mock_client.purchase_reserved_cache_nodes_offering.assert_called_once()


def test_purchase_reserved_cache_nodes_offering_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.purchase_reserved_cache_nodes_offering.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_reserved_cache_nodes_offering",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to purchase reserved cache nodes offering"):
        purchase_reserved_cache_nodes_offering("test-reserved_cache_nodes_offering_id", region_name=REGION)


def test_rebalance_slots_in_global_replication_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.rebalance_slots_in_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    rebalance_slots_in_global_replication_group("test-global_replication_group_id", True, region_name=REGION)
    mock_client.rebalance_slots_in_global_replication_group.assert_called_once()


def test_rebalance_slots_in_global_replication_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.rebalance_slots_in_global_replication_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "rebalance_slots_in_global_replication_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to rebalance slots in global replication group"):
        rebalance_slots_in_global_replication_group("test-global_replication_group_id", True, region_name=REGION)


def test_remove_tags_from_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    remove_tags_from_resource("test-resource_name", [], region_name=REGION)
    mock_client.remove_tags_from_resource.assert_called_once()


def test_remove_tags_from_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.remove_tags_from_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "remove_tags_from_resource",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to remove tags from resource"):
        remove_tags_from_resource("test-resource_name", [], region_name=REGION)


def test_reset_cache_parameter_group(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_cache_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    reset_cache_parameter_group("test-cache_parameter_group_name", region_name=REGION)
    mock_client.reset_cache_parameter_group.assert_called_once()


def test_reset_cache_parameter_group_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reset_cache_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_cache_parameter_group",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reset cache parameter group"):
        reset_cache_parameter_group("test-cache_parameter_group_name", region_name=REGION)


def test_revoke_cache_security_group_ingress(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_cache_security_group_ingress.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    revoke_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", region_name=REGION)
    mock_client.revoke_cache_security_group_ingress.assert_called_once()


def test_revoke_cache_security_group_ingress_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.revoke_cache_security_group_ingress.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "revoke_cache_security_group_ingress",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to revoke cache security group ingress"):
        revoke_cache_security_group_ingress("test-cache_security_group_name", "test-ec2_security_group_name", "test-ec2_security_group_owner_id", region_name=REGION)


def test_run_failover(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_failover.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    run_failover("test-replication_group_id", "test-node_group_id", region_name=REGION)
    mock_client.test_failover.assert_called_once()


def test_run_failover_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_failover.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_failover",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run failover"):
        run_failover("test-replication_group_id", "test-node_group_id", region_name=REGION)


def test_run_migration(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_migration.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    run_migration("test-replication_group_id", [], region_name=REGION)
    mock_client.test_migration.assert_called_once()


def test_run_migration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.test_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "test_migration",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to run migration"):
        run_migration("test-replication_group_id", [], region_name=REGION)


def test_start_migration(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_migration.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    start_migration("test-replication_group_id", [], region_name=REGION)
    mock_client.start_migration.assert_called_once()


def test_start_migration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_migration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_migration",
    )
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start migration"):
        start_migration("test-replication_group_id", [], region_name=REGION)


def test_batch_apply_update_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import batch_apply_update_action
    mock_client = MagicMock()
    mock_client.batch_apply_update_action.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    batch_apply_update_action("test-service_update_name", replication_group_ids="test-replication_group_ids", cache_cluster_ids="test-cache_cluster_ids", region_name="us-east-1")
    mock_client.batch_apply_update_action.assert_called_once()

def test_batch_stop_update_action_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import batch_stop_update_action
    mock_client = MagicMock()
    mock_client.batch_stop_update_action.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    batch_stop_update_action("test-service_update_name", replication_group_ids="test-replication_group_ids", cache_cluster_ids="test-cache_cluster_ids", region_name="us-east-1")
    mock_client.batch_stop_update_action.assert_called_once()

def test_complete_migration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import complete_migration
    mock_client = MagicMock()
    mock_client.complete_migration.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    complete_migration("test-replication_group_id", force=True, region_name="us-east-1")
    mock_client.complete_migration.assert_called_once()

def test_copy_serverless_cache_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import copy_serverless_cache_snapshot
    mock_client = MagicMock()
    mock_client.copy_serverless_cache_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    copy_serverless_cache_snapshot("test-source_serverless_cache_snapshot_name", "test-target_serverless_cache_snapshot_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_serverless_cache_snapshot.assert_called_once()

def test_copy_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import copy_snapshot
    mock_client = MagicMock()
    mock_client.copy_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    copy_snapshot("test-source_snapshot_name", "test-target_snapshot_name", target_bucket="test-target_bucket", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.copy_snapshot.assert_called_once()

def test_create_cache_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_cache_parameter_group
    mock_client = MagicMock()
    mock_client.create_cache_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_cache_parameter_group("test-cache_parameter_group_name", "test-cache_parameter_group_family", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_cache_parameter_group.assert_called_once()

def test_create_cache_security_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_cache_security_group
    mock_client = MagicMock()
    mock_client.create_cache_security_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_cache_security_group("test-cache_security_group_name", "test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_cache_security_group.assert_called_once()

def test_create_global_replication_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_global_replication_group
    mock_client = MagicMock()
    mock_client.create_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_global_replication_group("test-global_replication_group_id_suffix", "test-primary_replication_group_id", global_replication_group_description="test-global_replication_group_description", region_name="us-east-1")
    mock_client.create_global_replication_group.assert_called_once()

def test_create_serverless_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_serverless_cache
    mock_client = MagicMock()
    mock_client.create_serverless_cache.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_serverless_cache("test-serverless_cache_name", "test-engine", description="test-description", major_engine_version="test-major_engine_version", cache_usage_limits=1, kms_key_id="test-kms_key_id", security_group_ids="test-security_group_ids", snapshot_arns_to_restore="test-snapshot_arns_to_restore", tags=[{"Key": "k", "Value": "v"}], user_group_id="test-user_group_id", subnet_ids="test-subnet_ids", snapshot_retention_limit=1, daily_snapshot_time="test-daily_snapshot_time", region_name="us-east-1")
    mock_client.create_serverless_cache.assert_called_once()

def test_create_serverless_cache_snapshot_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_serverless_cache_snapshot
    mock_client = MagicMock()
    mock_client.create_serverless_cache_snapshot.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_serverless_cache_snapshot("test-serverless_cache_snapshot_name", "test-serverless_cache_name", kms_key_id="test-kms_key_id", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_serverless_cache_snapshot.assert_called_once()

def test_create_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_user
    mock_client = MagicMock()
    mock_client.create_user.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_user("test-user_id", "test-user_name", "test-engine", "test-access_string", passwords="test-passwords", no_password_required=True, tags=[{"Key": "k", "Value": "v"}], authentication_mode="test-authentication_mode", region_name="us-east-1")
    mock_client.create_user.assert_called_once()

def test_create_user_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import create_user_group
    mock_client = MagicMock()
    mock_client.create_user_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    create_user_group("test-user_group_id", "test-engine", user_ids="test-user_ids", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_user_group.assert_called_once()

def test_decrease_node_groups_in_global_replication_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import decrease_node_groups_in_global_replication_group
    mock_client = MagicMock()
    mock_client.decrease_node_groups_in_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    decrease_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, global_node_groups_to_remove="test-global_node_groups_to_remove", global_node_groups_to_retain="test-global_node_groups_to_retain", region_name="us-east-1")
    mock_client.decrease_node_groups_in_global_replication_group.assert_called_once()

def test_decrease_replica_count_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import decrease_replica_count
    mock_client = MagicMock()
    mock_client.decrease_replica_count.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    decrease_replica_count("test-replication_group_id", True, new_replica_count=1, replica_configuration={}, replicas_to_remove="test-replicas_to_remove", region_name="us-east-1")
    mock_client.decrease_replica_count.assert_called_once()

def test_delete_serverless_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import delete_serverless_cache
    mock_client = MagicMock()
    mock_client.delete_serverless_cache.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    delete_serverless_cache("test-serverless_cache_name", final_snapshot_name="test-final_snapshot_name", region_name="us-east-1")
    mock_client.delete_serverless_cache.assert_called_once()

def test_describe_cache_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_cache_engine_versions
    mock_client = MagicMock()
    mock_client.describe_cache_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_engine_versions(engine="test-engine", engine_version="test-engine_version", cache_parameter_group_family="test-cache_parameter_group_family", max_records=1, marker="test-marker", default_only="test-default_only", region_name="us-east-1")
    mock_client.describe_cache_engine_versions.assert_called_once()

def test_describe_cache_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_cache_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_cache_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_parameter_groups(cache_parameter_group_name="test-cache_parameter_group_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cache_parameter_groups.assert_called_once()

def test_describe_cache_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_cache_parameters
    mock_client = MagicMock()
    mock_client.describe_cache_parameters.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_parameters("test-cache_parameter_group_name", source="test-source", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cache_parameters.assert_called_once()

def test_describe_cache_security_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_cache_security_groups
    mock_client = MagicMock()
    mock_client.describe_cache_security_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_cache_security_groups(cache_security_group_name="test-cache_security_group_name", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_cache_security_groups.assert_called_once()

def test_describe_engine_default_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_engine_default_parameters
    mock_client = MagicMock()
    mock_client.describe_engine_default_parameters.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_engine_default_parameters("test-cache_parameter_group_family", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_engine_default_parameters.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_events(source_identifier="test-source_identifier", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_global_replication_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_global_replication_groups
    mock_client = MagicMock()
    mock_client.describe_global_replication_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_global_replication_groups(global_replication_group_id="test-global_replication_group_id", max_records=1, marker="test-marker", show_member_info="test-show_member_info", region_name="us-east-1")
    mock_client.describe_global_replication_groups.assert_called_once()

def test_describe_reserved_cache_nodes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_reserved_cache_nodes
    mock_client = MagicMock()
    mock_client.describe_reserved_cache_nodes.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_reserved_cache_nodes(reserved_cache_node_id="test-reserved_cache_node_id", reserved_cache_nodes_offering_id="test-reserved_cache_nodes_offering_id", cache_node_type="test-cache_node_type", duration=1, product_description="test-product_description", offering_type="test-offering_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_cache_nodes.assert_called_once()

def test_describe_reserved_cache_nodes_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_reserved_cache_nodes_offerings
    mock_client = MagicMock()
    mock_client.describe_reserved_cache_nodes_offerings.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_reserved_cache_nodes_offerings(reserved_cache_nodes_offering_id="test-reserved_cache_nodes_offering_id", cache_node_type="test-cache_node_type", duration=1, product_description="test-product_description", offering_type="test-offering_type", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_reserved_cache_nodes_offerings.assert_called_once()

def test_describe_serverless_cache_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_serverless_cache_snapshots
    mock_client = MagicMock()
    mock_client.describe_serverless_cache_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_serverless_cache_snapshots(serverless_cache_name="test-serverless_cache_name", serverless_cache_snapshot_name="test-serverless_cache_snapshot_name", snapshot_type="test-snapshot_type", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_serverless_cache_snapshots.assert_called_once()

def test_describe_serverless_caches_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_serverless_caches
    mock_client = MagicMock()
    mock_client.describe_serverless_caches.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_serverless_caches(serverless_cache_name="test-serverless_cache_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_serverless_caches.assert_called_once()

def test_describe_service_updates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_service_updates
    mock_client = MagicMock()
    mock_client.describe_service_updates.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_service_updates(service_update_name="test-service_update_name", service_update_status="test-service_update_status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_service_updates.assert_called_once()

def test_describe_update_actions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_update_actions
    mock_client = MagicMock()
    mock_client.describe_update_actions.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_update_actions(service_update_name="test-service_update_name", replication_group_ids="test-replication_group_ids", cache_cluster_ids="test-cache_cluster_ids", engine="test-engine", service_update_status="test-service_update_status", service_update_time_range="test-service_update_time_range", update_action_status="test-update_action_status", show_node_level_update_status="test-show_node_level_update_status", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_update_actions.assert_called_once()

def test_describe_user_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_user_groups
    mock_client = MagicMock()
    mock_client.describe_user_groups.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_user_groups(user_group_id="test-user_group_id", max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_user_groups.assert_called_once()

def test_describe_users_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import describe_users
    mock_client = MagicMock()
    mock_client.describe_users.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    describe_users(engine="test-engine", user_id="test-user_id", filters=[{}], max_records=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_users.assert_called_once()

def test_increase_node_groups_in_global_replication_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import increase_node_groups_in_global_replication_group
    mock_client = MagicMock()
    mock_client.increase_node_groups_in_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    increase_node_groups_in_global_replication_group("test-global_replication_group_id", 1, True, regional_configurations={}, region_name="us-east-1")
    mock_client.increase_node_groups_in_global_replication_group.assert_called_once()

def test_increase_replica_count_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import increase_replica_count
    mock_client = MagicMock()
    mock_client.increase_replica_count.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    increase_replica_count("test-replication_group_id", True, new_replica_count=1, replica_configuration={}, region_name="us-east-1")
    mock_client.increase_replica_count.assert_called_once()

def test_list_allowed_node_type_modifications_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import list_allowed_node_type_modifications
    mock_client = MagicMock()
    mock_client.list_allowed_node_type_modifications.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    list_allowed_node_type_modifications(cache_cluster_id="test-cache_cluster_id", replication_group_id="test-replication_group_id", region_name="us-east-1")
    mock_client.list_allowed_node_type_modifications.assert_called_once()

def test_modify_cache_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import modify_cache_subnet_group
    mock_client = MagicMock()
    mock_client.modify_cache_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_cache_subnet_group("test-cache_subnet_group_name", cache_subnet_group_description="test-cache_subnet_group_description", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.modify_cache_subnet_group.assert_called_once()

def test_modify_global_replication_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import modify_global_replication_group
    mock_client = MagicMock()
    mock_client.modify_global_replication_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_global_replication_group("test-global_replication_group_id", True, cache_node_type="test-cache_node_type", engine="test-engine", engine_version="test-engine_version", cache_parameter_group_name="test-cache_parameter_group_name", global_replication_group_description="test-global_replication_group_description", automatic_failover_enabled=True, region_name="us-east-1")
    mock_client.modify_global_replication_group.assert_called_once()

def test_modify_replication_group_shard_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import modify_replication_group_shard_configuration
    mock_client = MagicMock()
    mock_client.modify_replication_group_shard_configuration.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_replication_group_shard_configuration("test-replication_group_id", 1, True, resharding_configuration={}, node_groups_to_remove="test-node_groups_to_remove", node_groups_to_retain="test-node_groups_to_retain", region_name="us-east-1")
    mock_client.modify_replication_group_shard_configuration.assert_called_once()

def test_modify_serverless_cache_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import modify_serverless_cache
    mock_client = MagicMock()
    mock_client.modify_serverless_cache.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_serverless_cache("test-serverless_cache_name", description="test-description", cache_usage_limits=1, remove_user_group="test-remove_user_group", user_group_id="test-user_group_id", security_group_ids="test-security_group_ids", snapshot_retention_limit=1, daily_snapshot_time="test-daily_snapshot_time", engine="test-engine", major_engine_version="test-major_engine_version", region_name="us-east-1")
    mock_client.modify_serverless_cache.assert_called_once()

def test_modify_user_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import modify_user
    mock_client = MagicMock()
    mock_client.modify_user.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_user("test-user_id", access_string="test-access_string", append_access_string="test-append_access_string", passwords="test-passwords", no_password_required=True, authentication_mode="test-authentication_mode", engine="test-engine", region_name="us-east-1")
    mock_client.modify_user.assert_called_once()

def test_modify_user_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import modify_user_group
    mock_client = MagicMock()
    mock_client.modify_user_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    modify_user_group("test-user_group_id", user_ids_to_add="test-user_ids_to_add", user_ids_to_remove="test-user_ids_to_remove", engine="test-engine", region_name="us-east-1")
    mock_client.modify_user_group.assert_called_once()

def test_purchase_reserved_cache_nodes_offering_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import purchase_reserved_cache_nodes_offering
    mock_client = MagicMock()
    mock_client.purchase_reserved_cache_nodes_offering.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_cache_nodes_offering("test-reserved_cache_nodes_offering_id", reserved_cache_node_id="test-reserved_cache_node_id", cache_node_count=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.purchase_reserved_cache_nodes_offering.assert_called_once()

def test_reset_cache_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.elasticache import reset_cache_parameter_group
    mock_client = MagicMock()
    mock_client.reset_cache_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.elasticache.get_client", lambda *a, **kw: mock_client)
    reset_cache_parameter_group("test-cache_parameter_group_name", reset_all_parameters="test-reset_all_parameters", parameter_name_values="test-parameter_name_values", region_name="us-east-1")
    mock_client.reset_cache_parameter_group.assert_called_once()
