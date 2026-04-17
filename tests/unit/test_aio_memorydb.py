"""Tests for aws_util.aio.memorydb -- 100% line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.memorydb import (
    AclResult,
    ClusterResult,
    SnapshotResult,
    SubnetGroupResult,
    UserResult,
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


def _mf(mc):
    return lambda *a, **kw: mc


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def test_create_cluster(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Cluster": {"Name": "c1", "Status": "creating", "NodeType": "db.r6g.large"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await create_cluster("c1")
    assert isinstance(r, ClusterResult)


async def test_create_cluster_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Cluster": {"Name": "c1", "Status": "creating", "NodeType": "db.r6g.large"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await create_cluster(
        "c1",
        num_shards=2,
        num_replicas_per_shard=1,
        subnet_group_name="sg1",
        security_group_ids=["sg-1"],
        tags={"k": "v"},
    )
    kw = mc.call.call_args[1]
    assert kw["NumShards"] == 2
    assert kw["NumReplicasPerShard"] == 1
    assert kw["SubnetGroupName"] == "sg1"
    assert kw["SecurityGroupIds"] == ["sg-1"]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


async def test_create_cluster_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await create_cluster("c1")


async def test_describe_clusters(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Clusters": [{"Name": "c1", "Status": "available", "NodeType": "db.r6g.large"}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_clusters()) == 1


async def test_describe_clusters_with_name(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Clusters": [{"Name": "c1", "Status": "available", "NodeType": "db.r6g.large"}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await describe_clusters(cluster_name="c1")
    assert mc.call.call_args[1]["ClusterName"] == "c1"


async def test_describe_clusters_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Clusters": [{"Name": "c1", "Status": "available", "NodeType": "db.r6g.large"}], "NextToken": "t"},
        {"Clusters": [{"Name": "c2", "Status": "available", "NodeType": "db.r6g.large"}]},
    ]
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_clusters()) == 2


async def test_describe_clusters_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await describe_clusters()


async def test_update_cluster(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Cluster": {"Name": "c1", "Status": "modifying", "NodeType": "db.r6g.large"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await update_cluster("c1")
    assert isinstance(r, ClusterResult)


async def test_update_cluster_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Cluster": {"Name": "c1", "Status": "modifying", "NodeType": "db.r6g.xlarge"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await update_cluster("c1", node_type="db.r6g.xlarge", acl_name="acl2", security_group_ids=["sg-2"])
    kw = mc.call.call_args[1]
    assert kw["NodeType"] == "db.r6g.xlarge"
    assert kw["ACLName"] == "acl2"
    assert kw["SecurityGroupIds"] == ["sg-2"]


async def test_update_cluster_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await update_cluster("c1")


async def test_delete_cluster(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await delete_cluster("c1")


async def test_delete_cluster_with_snapshot(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await delete_cluster("c1", final_snapshot_name="final")
    kw = mc.call.call_args[1]
    assert kw["FinalSnapshotName"] == "final"


async def test_delete_cluster_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await delete_cluster("c1")


# ---------------------------------------------------------------------------
# Snapshot operations
# ---------------------------------------------------------------------------


async def test_create_snapshot(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Snapshot": {"Name": "snap1", "Status": "creating"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await create_snapshot("snap1", cluster_name="c1")
    assert isinstance(r, SnapshotResult)


async def test_create_snapshot_with_tags(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Snapshot": {"Name": "snap1", "Status": "creating"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await create_snapshot("snap1", cluster_name="c1", tags={"k": "v"})
    kw = mc.call.call_args[1]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


async def test_create_snapshot_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await create_snapshot("snap1", cluster_name="c1")


async def test_describe_snapshots(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Snapshots": [{"Name": "snap1", "Status": "available"}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_snapshots()) == 1


async def test_describe_snapshots_with_filters(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"Snapshots": []}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await describe_snapshots(snapshot_name="snap1", cluster_name="c1")
    kw = mc.call.call_args[1]
    assert kw["SnapshotName"] == "snap1"
    assert kw["ClusterName"] == "c1"


async def test_describe_snapshots_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Snapshots": [{"Name": "s1", "Status": "available"}], "NextToken": "t"},
        {"Snapshots": [{"Name": "s2", "Status": "available"}]},
    ]
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_snapshots()) == 2


async def test_describe_snapshots_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await describe_snapshots()


async def test_copy_snapshot(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Snapshot": {"Name": "snap-copy", "Status": "creating"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await copy_snapshot("snap1", "snap-copy")
    assert isinstance(r, SnapshotResult)


async def test_copy_snapshot_with_tags(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Snapshot": {"Name": "snap-copy", "Status": "creating"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await copy_snapshot("snap1", "snap-copy", tags={"k": "v"})
    kw = mc.call.call_args[1]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


async def test_copy_snapshot_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await copy_snapshot("snap1", "snap-copy")


async def test_delete_snapshot(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await delete_snapshot("snap1")


async def test_delete_snapshot_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await delete_snapshot("snap1")


# ---------------------------------------------------------------------------
# User operations
# ---------------------------------------------------------------------------


async def test_create_user(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "User": {"Name": "u1", "Status": "active"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await create_user("u1")
    assert isinstance(r, UserResult)


async def test_create_user_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "User": {"Name": "u1", "Status": "active"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await create_user(
        "u1",
        authentication_mode={"Type": "password"},
        tags={"k": "v"},
    )
    kw = mc.call.call_args[1]
    assert kw["AuthenticationMode"] == {"Type": "password"}
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


async def test_create_user_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await create_user("u1")


async def test_describe_users(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Users": [{"Name": "u1", "Status": "active"}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_users()) == 1


async def test_describe_users_with_name(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "Users": [{"Name": "u1", "Status": "active"}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await describe_users(user_name="u1")
    kw = mc.call.call_args[1]
    assert kw["UserName"] == "u1"


async def test_describe_users_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"Users": [{"Name": "u1", "Status": "active"}], "NextToken": "t"},
        {"Users": [{"Name": "u2", "Status": "active"}]},
    ]
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_users()) == 2


async def test_describe_users_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await describe_users()


async def test_update_user(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "User": {"Name": "u1", "Status": "modifying"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await update_user("u1")
    assert isinstance(r, UserResult)


async def test_update_user_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "User": {"Name": "u1", "Status": "modifying"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await update_user(
        "u1",
        access_string="off",
        authentication_mode={"Type": "no-password-required"},
    )
    kw = mc.call.call_args[1]
    assert kw["AccessString"] == "off"
    assert kw["AuthenticationMode"] == {"Type": "no-password-required"}


async def test_update_user_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await update_user("u1")


async def test_delete_user(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await delete_user("u1")


async def test_delete_user_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await delete_user("u1")


# ---------------------------------------------------------------------------
# ACL operations
# ---------------------------------------------------------------------------


async def test_create_acl(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "ACL": {"Name": "acl1", "Status": "creating"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await create_acl("acl1")
    assert isinstance(r, AclResult)


async def test_create_acl_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "ACL": {"Name": "acl1", "Status": "creating"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await create_acl("acl1", user_names=["u1"], tags={"k": "v"})
    kw = mc.call.call_args[1]
    assert kw["UserNames"] == ["u1"]
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


async def test_create_acl_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await create_acl("acl1")


async def test_describe_acls(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "ACLs": [{"Name": "acl1", "Status": "active"}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_acls()) == 1


async def test_describe_acls_with_name(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"ACLs": []}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await describe_acls(acl_name="acl1")
    kw = mc.call.call_args[1]
    assert kw["ACLName"] == "acl1"


async def test_describe_acls_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"ACLs": [{"Name": "a1", "Status": "active"}], "NextToken": "t"},
        {"ACLs": [{"Name": "a2", "Status": "active"}]},
    ]
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_acls()) == 2


async def test_describe_acls_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await describe_acls()


async def test_update_acl(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "ACL": {"Name": "acl1", "Status": "modifying"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await update_acl("acl1")
    assert isinstance(r, AclResult)


async def test_update_acl_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "ACL": {"Name": "acl1", "Status": "modifying"},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await update_acl(
        "acl1",
        user_names_to_add=["u1"],
        user_names_to_remove=["u2"],
    )
    kw = mc.call.call_args[1]
    assert kw["UserNamesToAdd"] == ["u1"]
    assert kw["UserNamesToRemove"] == ["u2"]


async def test_update_acl_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await update_acl("acl1")


async def test_delete_acl(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await delete_acl("acl1")


async def test_delete_acl_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await delete_acl("acl1")


# ---------------------------------------------------------------------------
# Subnet group operations
# ---------------------------------------------------------------------------


async def test_create_subnet_group(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "SubnetGroup": {"Name": "sg1", "Subnets": []},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    r = await create_subnet_group("sg1", subnet_ids=["sub-1"])
    assert isinstance(r, SubnetGroupResult)


async def test_create_subnet_group_all_opts(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "SubnetGroup": {"Name": "sg1", "Subnets": []},
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await create_subnet_group(
        "sg1",
        subnet_ids=["sub-1"],
        description="desc",
        tags={"k": "v"},
    )
    kw = mc.call.call_args[1]
    assert kw["Description"] == "desc"
    assert kw["Tags"] == [{"Key": "k", "Value": "v"}]


async def test_create_subnet_group_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await create_subnet_group("sg1", subnet_ids=["sub-1"])


async def test_describe_subnet_groups(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {
        "SubnetGroups": [{"Name": "sg1", "Subnets": []}],
    }
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_subnet_groups()) == 1


async def test_describe_subnet_groups_with_name(monkeypatch):
    mc = AsyncMock()
    mc.call.return_value = {"SubnetGroups": []}
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    await describe_subnet_groups(subnet_group_name="sg1")
    kw = mc.call.call_args[1]
    assert kw["SubnetGroupName"] == "sg1"


async def test_describe_subnet_groups_pagination(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = [
        {"SubnetGroups": [{"Name": "sg1", "Subnets": []}], "NextToken": "t"},
        {"SubnetGroups": [{"Name": "sg2", "Subnets": []}]},
    ]
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    assert len(await describe_subnet_groups()) == 2


async def test_describe_subnet_groups_error(monkeypatch):
    mc = AsyncMock()
    mc.call.side_effect = ValueError("boom")
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", _mf(mc))
    with pytest.raises(RuntimeError):
        await describe_subnet_groups()


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_cluster_immediate(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.memorydb.describe_clusters",
        AsyncMock(return_value=[
            ClusterResult(name="c1", status="available", node_type="db.r6g.large"),
        ]),
    )
    monkeypatch.setattr("aws_util.aio.memorydb.time.monotonic", lambda: 0.0)
    r = await wait_for_cluster("c1")
    assert r.status == "available"


async def test_wait_for_cluster_not_found(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.memorydb.describe_clusters",
        AsyncMock(return_value=[]),
    )
    monkeypatch.setattr("aws_util.aio.memorydb.time.monotonic", lambda: 0.0)
    with pytest.raises(AwsServiceError, match="not found"):
        await wait_for_cluster("c1")


async def test_wait_for_cluster_timeout(monkeypatch):
    monkeypatch.setattr(
        "aws_util.aio.memorydb.describe_clusters",
        AsyncMock(return_value=[
            ClusterResult(name="c1", status="creating", node_type="db.r6g.large"),
        ]),
    )
    _counter = {"n": 0}

    def _monotonic():
        _counter["n"] += 1
        if _counter["n"] <= 1:
            return 0.0
        return 700.0

    monkeypatch.setattr("aws_util.aio.memorydb.time.monotonic", _monotonic)
    with pytest.raises(AwsTimeoutError, match="did not reach"):
        await wait_for_cluster("c1", timeout=600.0)


async def test_wait_for_cluster_polls_then_succeeds(monkeypatch):
    _call_count = {"n": 0}

    async def _mock_describe(**kwargs):
        _call_count["n"] += 1
        if _call_count["n"] == 1:
            return [ClusterResult(name="c1", status="creating", node_type="db.r6g.large")]
        return [ClusterResult(name="c1", status="available", node_type="db.r6g.large")]

    monkeypatch.setattr("aws_util.aio.memorydb.describe_clusters", _mock_describe)
    monkeypatch.setattr("aws_util.aio.memorydb.time.monotonic", lambda: 0.0)
    monkeypatch.setattr("aws_util.aio.memorydb.asyncio.sleep", AsyncMock())
    r = await wait_for_cluster("c1", timeout=600.0)
    assert r.status == "available"


async def test_batch_update_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_update_cluster([], )
    mock_client.call.assert_called_once()


async def test_batch_update_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_update_cluster([], )


async def test_create_multi_region_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_multi_region_cluster("test-multi_region_cluster_name_suffix", "test-node_type", )
    mock_client.call.assert_called_once()


async def test_create_multi_region_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_multi_region_cluster("test-multi_region_cluster_name_suffix", "test-node_type", )


async def test_create_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_parameter_group("test-parameter_group_name", "test-family", )
    mock_client.call.assert_called_once()


async def test_create_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_parameter_group("test-parameter_group_name", "test-family", )


async def test_delete_multi_region_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_multi_region_cluster("test-multi_region_cluster_name", )
    mock_client.call.assert_called_once()


async def test_delete_multi_region_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_multi_region_cluster("test-multi_region_cluster_name", )


async def test_delete_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_parameter_group("test-parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_parameter_group("test-parameter_group_name", )


async def test_delete_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_subnet_group("test-subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_delete_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_subnet_group("test-subnet_group_name", )


async def test_describe_engine_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_engine_versions()
    mock_client.call.assert_called_once()


async def test_describe_engine_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_engine_versions()


async def test_describe_events(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_events()
    mock_client.call.assert_called_once()


async def test_describe_events_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_events()


async def test_describe_multi_region_clusters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_multi_region_clusters()
    mock_client.call.assert_called_once()


async def test_describe_multi_region_clusters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_multi_region_clusters()


async def test_describe_multi_region_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_multi_region_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_multi_region_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_multi_region_parameter_groups()


async def test_describe_multi_region_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_multi_region_parameters("test-multi_region_parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_multi_region_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_multi_region_parameters("test-multi_region_parameter_group_name", )


async def test_describe_parameter_groups(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_parameter_groups()
    mock_client.call.assert_called_once()


async def test_describe_parameter_groups_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_parameter_groups()


async def test_describe_parameters(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_parameters("test-parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_describe_parameters_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_parameters("test-parameter_group_name", )


async def test_describe_reserved_nodes(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_nodes()
    mock_client.call.assert_called_once()


async def test_describe_reserved_nodes_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_nodes()


async def test_describe_reserved_nodes_offerings(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_reserved_nodes_offerings()
    mock_client.call.assert_called_once()


async def test_describe_reserved_nodes_offerings_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_reserved_nodes_offerings()


async def test_describe_service_updates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_service_updates()
    mock_client.call.assert_called_once()


async def test_describe_service_updates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_service_updates()


async def test_failover_shard(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await failover_shard("test-cluster_name", "test-shard_name", )
    mock_client.call.assert_called_once()


async def test_failover_shard_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await failover_shard("test-cluster_name", "test-shard_name", )


async def test_list_allowed_multi_region_cluster_updates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_allowed_multi_region_cluster_updates("test-multi_region_cluster_name", )
    mock_client.call.assert_called_once()


async def test_list_allowed_multi_region_cluster_updates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_allowed_multi_region_cluster_updates("test-multi_region_cluster_name", )


async def test_list_allowed_node_type_updates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_allowed_node_type_updates("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_list_allowed_node_type_updates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_allowed_node_type_updates("test-cluster_name", )


async def test_list_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags("test-resource_arn", )


async def test_purchase_reserved_nodes_offering(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await purchase_reserved_nodes_offering("test-reserved_nodes_offering_id", )
    mock_client.call.assert_called_once()


async def test_purchase_reserved_nodes_offering_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await purchase_reserved_nodes_offering("test-reserved_nodes_offering_id", )


async def test_reset_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await reset_parameter_group("test-parameter_group_name", )
    mock_client.call.assert_called_once()


async def test_reset_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reset_parameter_group("test-parameter_group_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", [], )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_multi_region_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_multi_region_cluster("test-multi_region_cluster_name", )
    mock_client.call.assert_called_once()


async def test_update_multi_region_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_multi_region_cluster("test-multi_region_cluster_name", )


async def test_update_parameter_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_parameter_group("test-parameter_group_name", [], )
    mock_client.call.assert_called_once()


async def test_update_parameter_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_parameter_group("test-parameter_group_name", [], )


async def test_update_subnet_group(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_subnet_group("test-subnet_group_name", )
    mock_client.call.assert_called_once()


async def test_update_subnet_group_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.memorydb.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_subnet_group("test-subnet_group_name", )


@pytest.mark.asyncio
async def test_describe_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_clusters(cluster_name="test-cluster_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import delete_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await delete_cluster("test-cluster_name", final_snapshot_name="test-final_snapshot_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_snapshots_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_snapshots
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_snapshots(snapshot_name="test-snapshot_name", cluster_name="test-cluster_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_users_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_users
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_users(user_name="test-user_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_acls_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_acls
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_acls(acl_name="test-acl_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_subnet_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_subnet_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_subnet_groups(subnet_group_name="test-subnet_group_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_batch_update_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import batch_update_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await batch_update_cluster("test-cluster_names", service_update="test-service_update", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_multi_region_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import create_multi_region_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await create_multi_region_cluster(True, "test-node_type", description="test-description", engine="test-engine", engine_version="test-engine_version", multi_region_parameter_group_name=True, num_shards="test-num_shards", tls_enabled="test-tls_enabled", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import create_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await create_parameter_group("test-parameter_group_name", "test-family", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_engine_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_engine_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_engine_versions(engine="test-engine", engine_version="test-engine_version", parameter_group_family="test-parameter_group_family", max_results=1, next_token="test-next_token", default_only="test-default_only", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_events_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_events
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_events(source_name="test-source_name", source_type="test-source_type", start_time="test-start_time", end_time="test-end_time", duration=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_multi_region_clusters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_multi_region_clusters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_multi_region_clusters(multi_region_cluster_name=True, max_results=1, next_token="test-next_token", show_cluster_details="test-show_cluster_details", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_multi_region_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_multi_region_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_multi_region_parameter_groups(multi_region_parameter_group_name=True, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_multi_region_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_multi_region_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_multi_region_parameters(True, source="test-source", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_parameter_groups_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_parameter_groups
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_parameter_groups(parameter_group_name="test-parameter_group_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_parameters_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_parameters
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_parameters("test-parameter_group_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_nodes_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_reserved_nodes
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_nodes(reservation_id="test-reservation_id", reserved_nodes_offering_id="test-reserved_nodes_offering_id", node_type="test-node_type", duration=1, offering_type="test-offering_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_reserved_nodes_offerings_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_reserved_nodes_offerings
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_reserved_nodes_offerings(reserved_nodes_offering_id="test-reserved_nodes_offering_id", node_type="test-node_type", duration=1, offering_type="test-offering_type", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_service_updates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import describe_service_updates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await describe_service_updates(service_update_name="test-service_update_name", cluster_names="test-cluster_names", status="test-status", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_purchase_reserved_nodes_offering_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import purchase_reserved_nodes_offering
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await purchase_reserved_nodes_offering("test-reserved_nodes_offering_id", reservation_id="test-reservation_id", node_count=1, tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_reset_parameter_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import reset_parameter_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await reset_parameter_group("test-parameter_group_name", all_parameters="test-all_parameters", parameter_names="test-parameter_names", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_multi_region_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import update_multi_region_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await update_multi_region_cluster(True, node_type="test-node_type", description="test-description", engine_version="test-engine_version", shard_configuration={}, multi_region_parameter_group_name=True, update_strategy="test-update_strategy", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_subnet_group_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.memorydb import update_subnet_group
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.memorydb.async_client", lambda *a, **kw: mock_client)
    await update_subnet_group("test-subnet_group_name", description="test-description", subnet_ids="test-subnet_ids", region_name="us-east-1")
    mock_client.call.assert_called_once()
