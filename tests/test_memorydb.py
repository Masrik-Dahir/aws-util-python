"""Tests for aws_util.memorydb -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

from aws_util.memorydb import (
    AclResult,
    ClusterResult,
    SnapshotResult,
    SubnetGroupResult,
    UserResult,
    _parse_acl,
    _parse_cluster,
    _parse_snapshot,
    _parse_subnet_group,
    _parse_user,
    copy_snapshot,
    create_acl,
    create_cluster,
    create_snapshot,
    create_subnet_group,
    create_user,
    delete_acl,
    delete_cluster,
    delete_snapshot,
    delete_user,
    describe_acls,
    describe_clusters,
    describe_snapshots,
    describe_subnet_groups,
    describe_users,
    update_acl,
    update_cluster,
    update_user,
    wait_for_cluster,
    batch_update_cluster,
    create_multi_region_cluster,
    create_parameter_group,
    delete_multi_region_cluster,
    delete_parameter_group,
    delete_subnet_group,
    describe_engine_versions,
    describe_events,
    describe_multi_region_clusters,
    describe_multi_region_parameter_groups,
    describe_multi_region_parameters,
    describe_parameter_groups,
    describe_parameters,
    describe_reserved_nodes,
    describe_reserved_nodes_offerings,
    describe_service_updates,
    failover_shard,
    list_allowed_multi_region_cluster_updates,
    list_allowed_node_type_updates,
    list_tags,
    purchase_reserved_nodes_offering,
    reset_parameter_group,
    tag_resource,
    untag_resource,
    update_multi_region_cluster,
    update_parameter_group,
    update_subnet_group,
)
from aws_util.exceptions import AwsServiceError, AwsTimeoutError


def _ce(code="ValidationException"):
    return ClientError(
        {"Error": {"Code": code, "Message": "boom"}}, "Op"
    )


# ---------------------------------------------------------------------------
# Parser unit tests
# ---------------------------------------------------------------------------


def test_parse_cluster():
    c = _parse_cluster({
        "Name": "c1",
        "Status": "available",
        "NodeType": "db.r6g.large",
        "Engine": "redis",
        "EngineVersion": "7.0",
        "NumberOfShards": 2,
        "ACLName": "acl1",
        "SubnetGroupName": "sg1",
        "Extra": 1,
    })
    assert isinstance(c, ClusterResult)
    assert c.name == "c1"
    assert c.status == "available"
    assert c.extra == {"Extra": 1}


def test_parse_cluster_minimal():
    c = _parse_cluster({"Name": "c1"})
    assert c.status == "unknown"
    assert c.node_type == "unknown"


def test_parse_snapshot_with_cluster_config():
    s = _parse_snapshot({
        "Name": "snap1",
        "Status": "available",
        "ClusterConfiguration": {"Name": "c1"},
        "Source": "manual",
        "Extra": True,
    })
    assert isinstance(s, SnapshotResult)
    assert s.cluster_name == "c1"
    assert s.extra == {"Extra": True}


def test_parse_snapshot_no_cluster_config():
    s = _parse_snapshot({"Name": "snap1"})
    assert s.cluster_name is None


def test_parse_user():
    u = _parse_user({
        "Name": "user1",
        "Status": "active",
        "AccessString": "on ~* +@all",
        "ACLNames": ["acl1"],
        "Extra": 1,
    })
    assert isinstance(u, UserResult)
    assert u.acl_names == ["acl1"]
    assert u.extra == {"Extra": 1}


def test_parse_acl():
    a = _parse_acl({
        "Name": "acl1",
        "Status": "active",
        "UserNames": ["u1", "u2"],
        "Extra": 99,
    })
    assert isinstance(a, AclResult)
    assert a.user_names == ["u1", "u2"]
    assert a.extra == {"Extra": 99}


def test_parse_subnet_group():
    sg = _parse_subnet_group({
        "Name": "sg1",
        "Description": "desc",
        "VpcId": "vpc-1",
        "Subnets": [
            {"Identifier": "sub-1"},
            {"Identifier": "sub-2"},
        ],
        "Extra": "x",
    })
    assert isinstance(sg, SubnetGroupResult)
    assert sg.subnet_ids == ["sub-1", "sub-2"]
    assert sg.extra == {"Extra": "x"}


def test_parse_subnet_group_non_dict_subnet():
    sg = _parse_subnet_group({
        "Name": "sg1",
        "Subnets": ["not-a-dict"],
    })
    assert sg.subnet_ids == []


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


@patch("aws_util.memorydb.get_client")
def test_create_cluster(mock_gc):
    client = MagicMock()
    client.create_cluster.return_value = {
        "Cluster": {"Name": "c1", "Status": "creating", "NodeType": "db.r6g.large"},
    }
    mock_gc.return_value = client
    r = create_cluster("c1")
    assert isinstance(r, ClusterResult)
    assert r.name == "c1"


@patch("aws_util.memorydb.get_client")
def test_create_cluster_all_opts(mock_gc):
    client = MagicMock()
    client.create_cluster.return_value = {
        "Cluster": {"Name": "c1", "Status": "creating", "NodeType": "db.r6g.large"},
    }
    mock_gc.return_value = client
    create_cluster(
        "c1",
        num_shards=2,
        num_replicas_per_shard=1,
        subnet_group_name="sg1",
        security_group_ids=["sg-1"],
        tags={"k": "v"},
    )
    kw = client.create_cluster.call_args[1]
    assert kw["NumShards"] == 2
    assert kw["NumReplicasPerShard"] == 1
    assert kw["SubnetGroupName"] == "sg1"
    assert kw["SecurityGroupIds"] == ["sg-1"]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


@patch("aws_util.memorydb.get_client")
def test_create_cluster_error(mock_gc):
    client = MagicMock()
    client.create_cluster.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_cluster("c1")


@patch("aws_util.memorydb.get_client")
def test_describe_clusters(mock_gc):
    client = MagicMock()
    client.describe_clusters.return_value = {
        "Clusters": [{"Name": "c1", "Status": "available", "NodeType": "db.r6g.large"}],
    }
    mock_gc.return_value = client
    assert len(describe_clusters()) == 1


@patch("aws_util.memorydb.get_client")
def test_describe_clusters_with_name(mock_gc):
    client = MagicMock()
    client.describe_clusters.return_value = {
        "Clusters": [{"Name": "c1", "Status": "available", "NodeType": "db.r6g.large"}],
    }
    mock_gc.return_value = client
    describe_clusters(cluster_name="c1")
    assert client.describe_clusters.call_args[1]["ClusterName"] == "c1"


@patch("aws_util.memorydb.get_client")
def test_describe_clusters_pagination(mock_gc):
    client = MagicMock()
    client.describe_clusters.side_effect = [
        {"Clusters": [{"Name": "c1", "Status": "available", "NodeType": "db.r6g.large"}], "NextToken": "t"},
        {"Clusters": [{"Name": "c2", "Status": "available", "NodeType": "db.r6g.large"}]},
    ]
    mock_gc.return_value = client
    assert len(describe_clusters()) == 2


@patch("aws_util.memorydb.get_client")
def test_describe_clusters_error(mock_gc):
    client = MagicMock()
    client.describe_clusters.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_clusters()


@patch("aws_util.memorydb.get_client")
def test_update_cluster(mock_gc):
    client = MagicMock()
    client.update_cluster.return_value = {
        "Cluster": {"Name": "c1", "Status": "modifying", "NodeType": "db.r6g.large"},
    }
    mock_gc.return_value = client
    r = update_cluster("c1")
    assert isinstance(r, ClusterResult)


@patch("aws_util.memorydb.get_client")
def test_update_cluster_all_opts(mock_gc):
    client = MagicMock()
    client.update_cluster.return_value = {
        "Cluster": {"Name": "c1", "Status": "modifying", "NodeType": "db.r6g.xlarge"},
    }
    mock_gc.return_value = client
    update_cluster("c1", node_type="db.r6g.xlarge", acl_name="acl2", security_group_ids=["sg-2"])
    kw = client.update_cluster.call_args[1]
    assert kw["NodeType"] == "db.r6g.xlarge"
    assert kw["ACLName"] == "acl2"
    assert kw["SecurityGroupIds"] == ["sg-2"]


@patch("aws_util.memorydb.get_client")
def test_update_cluster_error(mock_gc):
    client = MagicMock()
    client.update_cluster.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_cluster("c1")


@patch("aws_util.memorydb.get_client")
def test_delete_cluster(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_cluster("c1")
    client.delete_cluster.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_delete_cluster_with_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_cluster("c1", final_snapshot_name="final")
    kw = client.delete_cluster.call_args[1]
    assert kw["FinalSnapshotName"] == "final"


@patch("aws_util.memorydb.get_client")
def test_delete_cluster_error(mock_gc):
    client = MagicMock()
    client.delete_cluster.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_cluster("c1")


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


@patch("aws_util.memorydb.get_client")
def test_create_snapshot(mock_gc):
    client = MagicMock()
    client.create_snapshot.return_value = {
        "Snapshot": {"Name": "snap1", "Status": "creating"},
    }
    mock_gc.return_value = client
    r = create_snapshot("snap1", cluster_name="c1")
    assert isinstance(r, SnapshotResult)


@patch("aws_util.memorydb.get_client")
def test_create_snapshot_with_tags(mock_gc):
    client = MagicMock()
    client.create_snapshot.return_value = {
        "Snapshot": {"Name": "snap1", "Status": "creating"},
    }
    mock_gc.return_value = client
    create_snapshot("snap1", cluster_name="c1", tags={"k": "v"})
    kw = client.create_snapshot.call_args[1]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


@patch("aws_util.memorydb.get_client")
def test_create_snapshot_error(mock_gc):
    client = MagicMock()
    client.create_snapshot.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_snapshot("snap1", cluster_name="c1")


@patch("aws_util.memorydb.get_client")
def test_describe_snapshots(mock_gc):
    client = MagicMock()
    client.describe_snapshots.return_value = {
        "Snapshots": [{"Name": "snap1", "Status": "available"}],
    }
    mock_gc.return_value = client
    assert len(describe_snapshots()) == 1


@patch("aws_util.memorydb.get_client")
def test_describe_snapshots_with_filters(mock_gc):
    client = MagicMock()
    client.describe_snapshots.return_value = {"Snapshots": []}
    mock_gc.return_value = client
    describe_snapshots(snapshot_name="snap1", cluster_name="c1")
    kw = client.describe_snapshots.call_args[1]
    assert kw["SnapshotName"] == "snap1"
    assert kw["ClusterName"] == "c1"


@patch("aws_util.memorydb.get_client")
def test_describe_snapshots_pagination(mock_gc):
    client = MagicMock()
    client.describe_snapshots.side_effect = [
        {"Snapshots": [{"Name": "s1", "Status": "available"}], "NextToken": "t"},
        {"Snapshots": [{"Name": "s2", "Status": "available"}]},
    ]
    mock_gc.return_value = client
    assert len(describe_snapshots()) == 2


@patch("aws_util.memorydb.get_client")
def test_describe_snapshots_error(mock_gc):
    client = MagicMock()
    client.describe_snapshots.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_snapshots()


@patch("aws_util.memorydb.get_client")
def test_copy_snapshot(mock_gc):
    client = MagicMock()
    client.copy_snapshot.return_value = {
        "Snapshot": {"Name": "snap-copy", "Status": "creating"},
    }
    mock_gc.return_value = client
    r = copy_snapshot("snap1", "snap-copy")
    assert isinstance(r, SnapshotResult)


@patch("aws_util.memorydb.get_client")
def test_copy_snapshot_with_tags(mock_gc):
    client = MagicMock()
    client.copy_snapshot.return_value = {
        "Snapshot": {"Name": "snap-copy", "Status": "creating"},
    }
    mock_gc.return_value = client
    copy_snapshot("snap1", "snap-copy", tags={"k": "v"})
    kw = client.copy_snapshot.call_args[1]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


@patch("aws_util.memorydb.get_client")
def test_copy_snapshot_error(mock_gc):
    client = MagicMock()
    client.copy_snapshot.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        copy_snapshot("snap1", "snap-copy")


@patch("aws_util.memorydb.get_client")
def test_delete_snapshot(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_snapshot("snap1")
    client.delete_snapshot.assert_called_once_with(SnapshotName="snap1")


@patch("aws_util.memorydb.get_client")
def test_delete_snapshot_error(mock_gc):
    client = MagicMock()
    client.delete_snapshot.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_snapshot("snap1")


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


@patch("aws_util.memorydb.get_client")
def test_create_user(mock_gc):
    client = MagicMock()
    client.create_user.return_value = {
        "User": {"Name": "u1", "Status": "active"},
    }
    mock_gc.return_value = client
    r = create_user("u1")
    assert isinstance(r, UserResult)


@patch("aws_util.memorydb.get_client")
def test_create_user_all_opts(mock_gc):
    client = MagicMock()
    client.create_user.return_value = {
        "User": {"Name": "u1", "Status": "active"},
    }
    mock_gc.return_value = client
    create_user(
        "u1",
        authentication_mode={"Type": "password"},
        tags={"k": "v"},
    )
    kw = client.create_user.call_args[1]
    assert kw["AuthenticationMode"] == {"Type": "password"}
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


@patch("aws_util.memorydb.get_client")
def test_create_user_error(mock_gc):
    client = MagicMock()
    client.create_user.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_user("u1")


@patch("aws_util.memorydb.get_client")
def test_describe_users(mock_gc):
    client = MagicMock()
    client.describe_users.return_value = {
        "Users": [{"Name": "u1", "Status": "active"}],
    }
    mock_gc.return_value = client
    assert len(describe_users()) == 1


@patch("aws_util.memorydb.get_client")
def test_describe_users_with_name(mock_gc):
    client = MagicMock()
    client.describe_users.return_value = {
        "Users": [{"Name": "u1", "Status": "active"}],
    }
    mock_gc.return_value = client
    describe_users(user_name="u1")
    kw = client.describe_users.call_args[1]
    assert kw["UserName"] == "u1"


@patch("aws_util.memorydb.get_client")
def test_describe_users_pagination(mock_gc):
    client = MagicMock()
    client.describe_users.side_effect = [
        {"Users": [{"Name": "u1", "Status": "active"}], "NextToken": "t"},
        {"Users": [{"Name": "u2", "Status": "active"}]},
    ]
    mock_gc.return_value = client
    assert len(describe_users()) == 2


@patch("aws_util.memorydb.get_client")
def test_describe_users_error(mock_gc):
    client = MagicMock()
    client.describe_users.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_users()


@patch("aws_util.memorydb.get_client")
def test_update_user(mock_gc):
    client = MagicMock()
    client.update_user.return_value = {
        "User": {"Name": "u1", "Status": "modifying"},
    }
    mock_gc.return_value = client
    r = update_user("u1")
    assert isinstance(r, UserResult)


@patch("aws_util.memorydb.get_client")
def test_update_user_all_opts(mock_gc):
    client = MagicMock()
    client.update_user.return_value = {
        "User": {"Name": "u1", "Status": "modifying"},
    }
    mock_gc.return_value = client
    update_user(
        "u1",
        access_string="off",
        authentication_mode={"Type": "no-password-required"},
    )
    kw = client.update_user.call_args[1]
    assert kw["AccessString"] == "off"
    assert kw["AuthenticationMode"] == {"Type": "no-password-required"}


@patch("aws_util.memorydb.get_client")
def test_update_user_error(mock_gc):
    client = MagicMock()
    client.update_user.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_user("u1")


@patch("aws_util.memorydb.get_client")
def test_delete_user(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_user("u1")
    client.delete_user.assert_called_once_with(UserName="u1")


@patch("aws_util.memorydb.get_client")
def test_delete_user_error(mock_gc):
    client = MagicMock()
    client.delete_user.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_user("u1")


# ---------------------------------------------------------------------------
# ACL operations
# ---------------------------------------------------------------------------


@patch("aws_util.memorydb.get_client")
def test_create_acl(mock_gc):
    client = MagicMock()
    client.create_acl.return_value = {
        "ACL": {"Name": "acl1", "Status": "creating"},
    }
    mock_gc.return_value = client
    r = create_acl("acl1")
    assert isinstance(r, AclResult)


@patch("aws_util.memorydb.get_client")
def test_create_acl_all_opts(mock_gc):
    client = MagicMock()
    client.create_acl.return_value = {
        "ACL": {"Name": "acl1", "Status": "creating"},
    }
    mock_gc.return_value = client
    create_acl("acl1", user_names=["u1"], tags={"k": "v"})
    kw = client.create_acl.call_args[1]
    assert kw["UserNames"] == ["u1"]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


@patch("aws_util.memorydb.get_client")
def test_create_acl_error(mock_gc):
    client = MagicMock()
    client.create_acl.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_acl("acl1")


@patch("aws_util.memorydb.get_client")
def test_describe_acls(mock_gc):
    client = MagicMock()
    client.describe_acls.return_value = {
        "ACLs": [{"Name": "acl1", "Status": "active"}],
    }
    mock_gc.return_value = client
    assert len(describe_acls()) == 1


@patch("aws_util.memorydb.get_client")
def test_describe_acls_with_name(mock_gc):
    client = MagicMock()
    client.describe_acls.return_value = {"ACLs": []}
    mock_gc.return_value = client
    describe_acls(acl_name="acl1")
    kw = client.describe_acls.call_args[1]
    assert kw["ACLName"] == "acl1"


@patch("aws_util.memorydb.get_client")
def test_describe_acls_pagination(mock_gc):
    client = MagicMock()
    client.describe_acls.side_effect = [
        {"ACLs": [{"Name": "a1", "Status": "active"}], "NextToken": "t"},
        {"ACLs": [{"Name": "a2", "Status": "active"}]},
    ]
    mock_gc.return_value = client
    assert len(describe_acls()) == 2


@patch("aws_util.memorydb.get_client")
def test_describe_acls_error(mock_gc):
    client = MagicMock()
    client.describe_acls.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_acls()


@patch("aws_util.memorydb.get_client")
def test_update_acl(mock_gc):
    client = MagicMock()
    client.update_acl.return_value = {
        "ACL": {"Name": "acl1", "Status": "modifying"},
    }
    mock_gc.return_value = client
    r = update_acl("acl1")
    assert isinstance(r, AclResult)


@patch("aws_util.memorydb.get_client")
def test_update_acl_all_opts(mock_gc):
    client = MagicMock()
    client.update_acl.return_value = {
        "ACL": {"Name": "acl1", "Status": "modifying"},
    }
    mock_gc.return_value = client
    update_acl(
        "acl1",
        user_names_to_add=["u1"],
        user_names_to_remove=["u2"],
    )
    kw = client.update_acl.call_args[1]
    assert kw["UserNamesToAdd"] == ["u1"]
    assert kw["UserNamesToRemove"] == ["u2"]


@patch("aws_util.memorydb.get_client")
def test_update_acl_error(mock_gc):
    client = MagicMock()
    client.update_acl.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        update_acl("acl1")


@patch("aws_util.memorydb.get_client")
def test_delete_acl(mock_gc):
    client = MagicMock()
    mock_gc.return_value = client
    delete_acl("acl1")
    client.delete_acl.assert_called_once_with(ACLName="acl1")


@patch("aws_util.memorydb.get_client")
def test_delete_acl_error(mock_gc):
    client = MagicMock()
    client.delete_acl.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        delete_acl("acl1")


# ---------------------------------------------------------------------------
# Subnet group operations
# ---------------------------------------------------------------------------


@patch("aws_util.memorydb.get_client")
def test_create_subnet_group(mock_gc):
    client = MagicMock()
    client.create_subnet_group.return_value = {
        "SubnetGroup": {"Name": "sg1", "Subnets": []},
    }
    mock_gc.return_value = client
    r = create_subnet_group("sg1", subnet_ids=["sub-1"])
    assert isinstance(r, SubnetGroupResult)


@patch("aws_util.memorydb.get_client")
def test_create_subnet_group_all_opts(mock_gc):
    client = MagicMock()
    client.create_subnet_group.return_value = {
        "SubnetGroup": {"Name": "sg1", "Subnets": []},
    }
    mock_gc.return_value = client
    create_subnet_group(
        "sg1",
        subnet_ids=["sub-1"],
        description="desc",
        tags={"k": "v"},
    )
    kw = client.create_subnet_group.call_args[1]
    assert kw["Description"] == "desc"
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


@patch("aws_util.memorydb.get_client")
def test_create_subnet_group_error(mock_gc):
    client = MagicMock()
    client.create_subnet_group.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        create_subnet_group("sg1", subnet_ids=["sub-1"])


@patch("aws_util.memorydb.get_client")
def test_describe_subnet_groups(mock_gc):
    client = MagicMock()
    client.describe_subnet_groups.return_value = {
        "SubnetGroups": [{"Name": "sg1", "Subnets": []}],
    }
    mock_gc.return_value = client
    assert len(describe_subnet_groups()) == 1


@patch("aws_util.memorydb.get_client")
def test_describe_subnet_groups_with_name(mock_gc):
    client = MagicMock()
    client.describe_subnet_groups.return_value = {"SubnetGroups": []}
    mock_gc.return_value = client
    describe_subnet_groups(subnet_group_name="sg1")
    kw = client.describe_subnet_groups.call_args[1]
    assert kw["SubnetGroupName"] == "sg1"


@patch("aws_util.memorydb.get_client")
def test_describe_subnet_groups_pagination(mock_gc):
    client = MagicMock()
    client.describe_subnet_groups.side_effect = [
        {"SubnetGroups": [{"Name": "sg1", "Subnets": []}], "NextToken": "t"},
        {"SubnetGroups": [{"Name": "sg2", "Subnets": []}]},
    ]
    mock_gc.return_value = client
    assert len(describe_subnet_groups()) == 2


@patch("aws_util.memorydb.get_client")
def test_describe_subnet_groups_error(mock_gc):
    client = MagicMock()
    client.describe_subnet_groups.side_effect = _ce()
    mock_gc.return_value = client
    with pytest.raises(RuntimeError):
        describe_subnet_groups()


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


@patch("aws_util.memorydb.time")
@patch("aws_util.memorydb.describe_clusters")
def test_wait_for_cluster_immediate(mock_dc, mock_time):
    mock_time.monotonic.return_value = 0.0
    mock_dc.return_value = [
        ClusterResult(name="c1", status="available", node_type="db.r6g.large"),
    ]
    r = wait_for_cluster("c1")
    assert r.status == "available"


@patch("aws_util.memorydb.time")
@patch("aws_util.memorydb.describe_clusters")
def test_wait_for_cluster_not_found(mock_dc, mock_time):
    mock_time.monotonic.return_value = 0.0
    mock_dc.return_value = []
    with pytest.raises(AwsServiceError, match="not found"):
        wait_for_cluster("c1")


@patch("aws_util.memorydb.time")
@patch("aws_util.memorydb.describe_clusters")
def test_wait_for_cluster_timeout(mock_dc, mock_time):
    mock_time.monotonic.side_effect = [0.0, 700.0]
    mock_dc.return_value = [
        ClusterResult(name="c1", status="creating", node_type="db.r6g.large"),
    ]
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        wait_for_cluster("c1", timeout=600.0)


@patch("aws_util.memorydb.time")
@patch("aws_util.memorydb.describe_clusters")
def test_wait_for_cluster_polls_then_succeeds(mock_dc, mock_time):
    mock_time.monotonic.side_effect = [0.0, 1.0, 2.0]
    mock_dc.side_effect = [
        [ClusterResult(name="c1", status="creating", node_type="db.r6g.large")],
        [ClusterResult(name="c1", status="available", node_type="db.r6g.large")],
    ]
    r = wait_for_cluster("c1", timeout=600.0)
    assert r.status == "available"
    mock_time.sleep.assert_called()


REGION = "us-east-1"


@patch("aws_util.memorydb.get_client")
def test_batch_update_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_cluster.return_value = {}
    batch_update_cluster([], region_name=REGION)
    mock_client.batch_update_cluster.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_batch_update_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.batch_update_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_update_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to batch update cluster"):
        batch_update_cluster([], region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_create_multi_region_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_multi_region_cluster.return_value = {}
    create_multi_region_cluster("test-multi_region_cluster_name_suffix", "test-node_type", region_name=REGION)
    mock_client.create_multi_region_cluster.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_create_multi_region_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_multi_region_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_multi_region_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to create multi region cluster"):
        create_multi_region_cluster("test-multi_region_cluster_name_suffix", "test-node_type", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_create_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_parameter_group.return_value = {}
    create_parameter_group("test-parameter_group_name", "test-family", region_name=REGION)
    mock_client.create_parameter_group.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_create_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.create_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to create parameter group"):
        create_parameter_group("test-parameter_group_name", "test-family", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_delete_multi_region_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_multi_region_cluster.return_value = {}
    delete_multi_region_cluster("test-multi_region_cluster_name", region_name=REGION)
    mock_client.delete_multi_region_cluster.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_delete_multi_region_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_multi_region_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_multi_region_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to delete multi region cluster"):
        delete_multi_region_cluster("test-multi_region_cluster_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_delete_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_parameter_group.return_value = {}
    delete_parameter_group("test-parameter_group_name", region_name=REGION)
    mock_client.delete_parameter_group.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_delete_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete parameter group"):
        delete_parameter_group("test-parameter_group_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_delete_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_subnet_group.return_value = {}
    delete_subnet_group("test-subnet_group_name", region_name=REGION)
    mock_client.delete_subnet_group.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_delete_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.delete_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to delete subnet group"):
        delete_subnet_group("test-subnet_group_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_engine_versions(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_versions.return_value = {}
    describe_engine_versions(region_name=REGION)
    mock_client.describe_engine_versions.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_engine_versions_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_engine_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_engine_versions",
    )
    with pytest.raises(RuntimeError, match="Failed to describe engine versions"):
        describe_engine_versions(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_events(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.return_value = {}
    describe_events(region_name=REGION)
    mock_client.describe_events.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_events_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_events.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_events",
    )
    with pytest.raises(RuntimeError, match="Failed to describe events"):
        describe_events(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_multi_region_clusters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_multi_region_clusters.return_value = {}
    describe_multi_region_clusters(region_name=REGION)
    mock_client.describe_multi_region_clusters.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_multi_region_clusters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_multi_region_clusters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_multi_region_clusters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe multi region clusters"):
        describe_multi_region_clusters(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_multi_region_parameter_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_multi_region_parameter_groups.return_value = {}
    describe_multi_region_parameter_groups(region_name=REGION)
    mock_client.describe_multi_region_parameter_groups.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_multi_region_parameter_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_multi_region_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_multi_region_parameter_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe multi region parameter groups"):
        describe_multi_region_parameter_groups(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_multi_region_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_multi_region_parameters.return_value = {}
    describe_multi_region_parameters("test-multi_region_parameter_group_name", region_name=REGION)
    mock_client.describe_multi_region_parameters.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_multi_region_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_multi_region_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_multi_region_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe multi region parameters"):
        describe_multi_region_parameters("test-multi_region_parameter_group_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_parameter_groups(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_parameter_groups.return_value = {}
    describe_parameter_groups(region_name=REGION)
    mock_client.describe_parameter_groups.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_parameter_groups_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_parameter_groups.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_parameter_groups",
    )
    with pytest.raises(RuntimeError, match="Failed to describe parameter groups"):
        describe_parameter_groups(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_parameters(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_parameters.return_value = {}
    describe_parameters("test-parameter_group_name", region_name=REGION)
    mock_client.describe_parameters.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_parameters_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_parameters.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_parameters",
    )
    with pytest.raises(RuntimeError, match="Failed to describe parameters"):
        describe_parameters("test-parameter_group_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_reserved_nodes(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_reserved_nodes.return_value = {}
    describe_reserved_nodes(region_name=REGION)
    mock_client.describe_reserved_nodes.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_reserved_nodes_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_reserved_nodes.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_nodes",
    )
    with pytest.raises(RuntimeError, match="Failed to describe reserved nodes"):
        describe_reserved_nodes(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_reserved_nodes_offerings(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_reserved_nodes_offerings.return_value = {}
    describe_reserved_nodes_offerings(region_name=REGION)
    mock_client.describe_reserved_nodes_offerings.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_reserved_nodes_offerings_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_reserved_nodes_offerings.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_reserved_nodes_offerings",
    )
    with pytest.raises(RuntimeError, match="Failed to describe reserved nodes offerings"):
        describe_reserved_nodes_offerings(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_describe_service_updates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_service_updates.return_value = {}
    describe_service_updates(region_name=REGION)
    mock_client.describe_service_updates.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_describe_service_updates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.describe_service_updates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_service_updates",
    )
    with pytest.raises(RuntimeError, match="Failed to describe service updates"):
        describe_service_updates(region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_failover_shard(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.failover_shard.return_value = {}
    failover_shard("test-cluster_name", "test-shard_name", region_name=REGION)
    mock_client.failover_shard.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_failover_shard_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.failover_shard.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "failover_shard",
    )
    with pytest.raises(RuntimeError, match="Failed to failover shard"):
        failover_shard("test-cluster_name", "test-shard_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_list_allowed_multi_region_cluster_updates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allowed_multi_region_cluster_updates.return_value = {}
    list_allowed_multi_region_cluster_updates("test-multi_region_cluster_name", region_name=REGION)
    mock_client.list_allowed_multi_region_cluster_updates.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_list_allowed_multi_region_cluster_updates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allowed_multi_region_cluster_updates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_allowed_multi_region_cluster_updates",
    )
    with pytest.raises(RuntimeError, match="Failed to list allowed multi region cluster updates"):
        list_allowed_multi_region_cluster_updates("test-multi_region_cluster_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_list_allowed_node_type_updates(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allowed_node_type_updates.return_value = {}
    list_allowed_node_type_updates("test-cluster_name", region_name=REGION)
    mock_client.list_allowed_node_type_updates.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_list_allowed_node_type_updates_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_allowed_node_type_updates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_allowed_node_type_updates",
    )
    with pytest.raises(RuntimeError, match="Failed to list allowed node type updates"):
        list_allowed_node_type_updates("test-cluster_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_list_tags(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags.return_value = {}
    list_tags("test-resource_arn", region_name=REGION)
    mock_client.list_tags.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_list_tags_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.list_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags",
    )
    with pytest.raises(RuntimeError, match="Failed to list tags"):
        list_tags("test-resource_arn", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_purchase_reserved_nodes_offering(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.purchase_reserved_nodes_offering.return_value = {}
    purchase_reserved_nodes_offering("test-reserved_nodes_offering_id", region_name=REGION)
    mock_client.purchase_reserved_nodes_offering.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_purchase_reserved_nodes_offering_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.purchase_reserved_nodes_offering.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "purchase_reserved_nodes_offering",
    )
    with pytest.raises(RuntimeError, match="Failed to purchase reserved nodes offering"):
        purchase_reserved_nodes_offering("test-reserved_nodes_offering_id", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_reset_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_parameter_group.return_value = {}
    reset_parameter_group("test-parameter_group_name", region_name=REGION)
    mock_client.reset_parameter_group.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_reset_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.reset_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reset_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to reset parameter group"):
        reset_parameter_group("test-parameter_group_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_tag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.return_value = {}
    tag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.tag_resource.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_tag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_untag_resource(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.return_value = {}
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_untag_resource_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_update_multi_region_cluster(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_multi_region_cluster.return_value = {}
    update_multi_region_cluster("test-multi_region_cluster_name", region_name=REGION)
    mock_client.update_multi_region_cluster.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_update_multi_region_cluster_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_multi_region_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_multi_region_cluster",
    )
    with pytest.raises(RuntimeError, match="Failed to update multi region cluster"):
        update_multi_region_cluster("test-multi_region_cluster_name", region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_update_parameter_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_parameter_group.return_value = {}
    update_parameter_group("test-parameter_group_name", [], region_name=REGION)
    mock_client.update_parameter_group.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_update_parameter_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_parameter_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_parameter_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update parameter group"):
        update_parameter_group("test-parameter_group_name", [], region_name=REGION)


@patch("aws_util.memorydb.get_client")
def test_update_subnet_group(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_subnet_group.return_value = {}
    update_subnet_group("test-subnet_group_name", region_name=REGION)
    mock_client.update_subnet_group.assert_called_once()


@patch("aws_util.memorydb.get_client")
def test_update_subnet_group_error(mock_get):
    mock_client = MagicMock()
    mock_get.return_value = mock_client
    mock_client.update_subnet_group.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_subnet_group",
    )
    with pytest.raises(RuntimeError, match="Failed to update subnet group"):
        update_subnet_group("test-subnet_group_name", region_name=REGION)


def test_describe_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_clusters
    mock_client = MagicMock()
    mock_client.describe_clusters.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_clusters(cluster_name="test-cluster_name", region_name="us-east-1")
    mock_client.describe_clusters.assert_called_once()

def test_delete_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import delete_cluster
    mock_client = MagicMock()
    mock_client.delete_cluster.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    delete_cluster("test-cluster_name", final_snapshot_name="test-final_snapshot_name", region_name="us-east-1")
    mock_client.delete_cluster.assert_called_once()

def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_snapshots
    mock_client = MagicMock()
    mock_client.describe_snapshots.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_snapshots(snapshot_name="test-snapshot_name", cluster_name="test-cluster_name", region_name="us-east-1")
    mock_client.describe_snapshots.assert_called_once()

def test_describe_users_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_users
    mock_client = MagicMock()
    mock_client.describe_users.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_users(user_name="test-user_name", region_name="us-east-1")
    mock_client.describe_users.assert_called_once()

def test_describe_acls_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_acls
    mock_client = MagicMock()
    mock_client.describe_acls.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_acls(acl_name="test-acl_name", region_name="us-east-1")
    mock_client.describe_acls.assert_called_once()

def test_describe_subnet_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_subnet_groups
    mock_client = MagicMock()
    mock_client.describe_subnet_groups.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_subnet_groups(subnet_group_name="test-subnet_group_name", region_name="us-east-1")
    mock_client.describe_subnet_groups.assert_called_once()

def test_batch_update_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import batch_update_cluster
    mock_client = MagicMock()
    mock_client.batch_update_cluster.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    batch_update_cluster("test-cluster_names", service_update="test-service_update", region_name="us-east-1")
    mock_client.batch_update_cluster.assert_called_once()

def test_create_multi_region_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import create_multi_region_cluster
    mock_client = MagicMock()
    mock_client.create_multi_region_cluster.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    create_multi_region_cluster(True, "test-node_type", description="test-description", engine="test-engine", engine_version="test-engine_version", multi_region_parameter_group_name=True, num_shards="test-num_shards", tls_enabled="test-tls_enabled", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_multi_region_cluster.assert_called_once()

def test_create_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import create_parameter_group
    mock_client = MagicMock()
    mock_client.create_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    create_parameter_group("test-parameter_group_name", "test-family", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_parameter_group.assert_called_once()

def test_describe_engine_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_engine_versions
    mock_client = MagicMock()
    mock_client.describe_engine_versions.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_engine_versions(engine="test-engine", engine_version="test-engine_version", parameter_group_family="test-parameter_group_family", max_results=1, next_token="test-next_token", default_only="test-default_only", region_name="us-east-1")
    mock_client.describe_engine_versions.assert_called_once()

def test_describe_events_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_events
    mock_client = MagicMock()
    mock_client.describe_events.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_events(source_name="test-source_name", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_events.assert_called_once()

def test_describe_multi_region_clusters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_multi_region_clusters
    mock_client = MagicMock()
    mock_client.describe_multi_region_clusters.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_multi_region_clusters(multi_region_cluster_name=True, max_results=1, next_token="test-next_token", show_cluster_details="test-show_cluster_details", region_name="us-east-1")
    mock_client.describe_multi_region_clusters.assert_called_once()

def test_describe_multi_region_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_multi_region_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_multi_region_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_multi_region_parameter_groups(multi_region_parameter_group_name=True, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_multi_region_parameter_groups.assert_called_once()

def test_describe_multi_region_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_multi_region_parameters
    mock_client = MagicMock()
    mock_client.describe_multi_region_parameters.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_multi_region_parameters(True, source="test-source", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_multi_region_parameters.assert_called_once()

def test_describe_parameter_groups_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_parameter_groups
    mock_client = MagicMock()
    mock_client.describe_parameter_groups.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_parameter_groups(parameter_group_name="test-parameter_group_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_parameter_groups.assert_called_once()

def test_describe_parameters_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_parameters
    mock_client = MagicMock()
    mock_client.describe_parameters.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_parameters("test-parameter_group_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_parameters.assert_called_once()

def test_describe_reserved_nodes_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_reserved_nodes
    mock_client = MagicMock()
    mock_client.describe_reserved_nodes.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_reserved_nodes(reservation_id="test-reservation_id", reserved_nodes_offering_id="test-reserved_nodes_offering_id", node_type="test-node_type", duration=1, offering_type="test-offering_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_reserved_nodes.assert_called_once()

def test_describe_reserved_nodes_offerings_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_reserved_nodes_offerings
    mock_client = MagicMock()
    mock_client.describe_reserved_nodes_offerings.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_reserved_nodes_offerings(reserved_nodes_offering_id="test-reserved_nodes_offering_id", node_type="test-node_type", duration=1, offering_type="test-offering_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_reserved_nodes_offerings.assert_called_once()

def test_describe_service_updates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import describe_service_updates
    mock_client = MagicMock()
    mock_client.describe_service_updates.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    describe_service_updates(service_update_name="test-service_update_name", cluster_names="test-cluster_names", status="test-status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.describe_service_updates.assert_called_once()

def test_purchase_reserved_nodes_offering_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import purchase_reserved_nodes_offering
    mock_client = MagicMock()
    mock_client.purchase_reserved_nodes_offering.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    purchase_reserved_nodes_offering("test-reserved_nodes_offering_id", reservation_id="test-reservation_id", node_count=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.purchase_reserved_nodes_offering.assert_called_once()

def test_reset_parameter_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import reset_parameter_group
    mock_client = MagicMock()
    mock_client.reset_parameter_group.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    reset_parameter_group("test-parameter_group_name", all_parameters="test-all_parameters", parameter_names="test-parameter_names", region_name="us-east-1")
    mock_client.reset_parameter_group.assert_called_once()

def test_update_multi_region_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import update_multi_region_cluster
    mock_client = MagicMock()
    mock_client.update_multi_region_cluster.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    update_multi_region_cluster(True, node_type="test-node_type", description="test-description", engine_version="test-engine_version", shard_configuration={}, multi_region_parameter_group_name=True, update_strategy="test-update_strategy", region_name="us-east-1")
    mock_client.update_multi_region_cluster.assert_called_once()

def test_update_subnet_group_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.memorydb import update_subnet_group
    mock_client = MagicMock()
    mock_client.update_subnet_group.return_value = {}
    monkeypatch.setattr("aws_util.memorydb.get_client", lambda *a, **kw: mock_client)
    update_subnet_group("test-subnet_group_name", description="test-description", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.update_subnet_group.assert_called_once()
