"""Tests for aws_util.aio.efs -- 100 % line coverage."""
from __future__ import annotations

import time
from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.efs import (
    AccessPointResult,
    FileSystemResult,
    MountTargetResult,
    create_access_point,
    create_file_system,
    create_mount_target,
    delete_access_point,
    delete_file_system,
    delete_file_system_policy,
    delete_mount_target,
    describe_access_points,
    describe_file_system_policy,
    describe_file_systems,
    describe_lifecycle_configuration,
    describe_mount_target_security_groups,
    describe_mount_targets,
    list_tags_for_resource,
    modify_mount_target_security_groups,
    put_file_system_policy,
    put_lifecycle_configuration,
    tag_resource,
    update_file_system,
    wait_for_file_system,
    create_replication_configuration,
    create_tags,
    delete_replication_configuration,
    delete_tags,
    describe_account_preferences,
    describe_backup_policy,
    describe_replication_configurations,
    describe_tags,
    put_account_preferences,
    put_backup_policy,
    untag_resource,
    update_file_system_protection,
)
from aws_util.exceptions import AwsTimeoutError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mc(rv=None, se=None):
    """Create an AsyncMock client with a .call method."""
    c = AsyncMock()
    if se:
        c.call.side_effect = se
    else:
        c.call.return_value = rv or {}
    return c


_FS_RESP = {
    "FileSystemId": "fs-12345678",
    "FileSystemArn": "arn:aws:elasticfilesystem:us-east-1:123:file-system/fs-12345678",
    "CreationTime": "2024-01-01T00:00:00Z",
    "LifeCycleState": "available",
    "PerformanceMode": "generalPurpose",
    "ThroughputMode": "bursting",
    "Encrypted": False,
    "SizeInBytes": {"Value": 0},
    "Tags": [{"Key": "env", "Value": "test"}],
    "OwnerId": "123456789012",
}

_FS_LIST_RESP = {"FileSystems": [_FS_RESP]}

_MT_RESP = {
    "MountTargetId": "fsmt-12345678",
    "FileSystemId": "fs-12345678",
    "SubnetId": "subnet-12345",
    "LifeCycleState": "available",
    "IpAddress": "10.0.1.5",
    "AvailabilityZoneName": "us-east-1a",
}

_MT_LIST_RESP = {"MountTargets": [_MT_RESP]}

_AP_RESP = {
    "AccessPointId": "fsap-12345678",
    "AccessPointArn": "arn:aws:elasticfilesystem:us-east-1:123:access-point/fsap-12345678",
    "FileSystemId": "fs-12345678",
    "LifeCycleState": "available",
    "PosixUser": {"Uid": 1000, "Gid": 1000},
    "RootDirectory": {"Path": "/data"},
    "Tags": [{"Key": "Name", "Value": "my-ap"}],
}

_AP_LIST_RESP = {"AccessPoints": [_AP_RESP]}


# ---------------------------------------------------------------------------
# Re-exported models
# ---------------------------------------------------------------------------


def test_models_re_exported():
    assert FileSystemResult is not None
    assert MountTargetResult is not None
    assert AccessPointResult is not None


# ---------------------------------------------------------------------------
# create_file_system
# ---------------------------------------------------------------------------


async def test_create_file_system_ok(monkeypatch):
    mc = _mc(_FS_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await create_file_system()
    assert result.file_system_id == "fs-12345678"
    assert result.tags == {"env": "test"}
    mc.call.assert_awaited_once()

async def test_create_file_system_runtime_error(monkeypatch):
    mc = _mc(se=RuntimeError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="boom"):
        await create_file_system()


async def test_create_file_system_generic_error(monkeypatch):
    mc = _mc(se=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_file_system failed"):
        await create_file_system()


# ---------------------------------------------------------------------------
# describe_file_systems
# ---------------------------------------------------------------------------


async def test_describe_file_systems_ok(monkeypatch):
    mc = _mc(_FS_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_systems()
    assert len(result) == 1
    assert result[0].file_system_id == "fs-12345678"


async def test_describe_file_systems_with_filters(monkeypatch):
    mc = _mc(_FS_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_systems(
        file_system_id="fs-12345678", creation_token="tok"
    )
    assert len(result) == 1


async def test_describe_file_systems_pagination(monkeypatch):
    page1 = dict(_FS_LIST_RESP)
    page1["NextMarker"] = "tok"
    page2 = {"FileSystems": [dict(_FS_RESP, FileSystemId="fs-99999999")]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_systems()
    assert len(result) == 2


async def test_describe_file_systems_empty(monkeypatch):
    mc = _mc({"FileSystems": []})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_systems()
    assert result == []


async def test_describe_file_systems_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_file_systems failed"):
        await describe_file_systems()


# ---------------------------------------------------------------------------
# update_file_system
# ---------------------------------------------------------------------------


async def test_update_file_system_ok(monkeypatch):
    mc = _mc(_FS_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await update_file_system(
        "fs-12345678", throughput_mode="bursting"
    )
    assert result.file_system_id == "fs-12345678"


async def test_update_file_system_with_provisioned(monkeypatch):
    mc = _mc(_FS_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await update_file_system(
        "fs-12345678",
        throughput_mode="provisioned",
        provisioned_throughput_in_mibps=256.0,
    )
    assert result.file_system_id == "fs-12345678"


async def test_update_file_system_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="update_file_system failed"):
        await update_file_system("fs-bad")


# ---------------------------------------------------------------------------
# delete_file_system
# ---------------------------------------------------------------------------


async def test_delete_file_system_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    await delete_file_system("fs-12345678")
    mc.call.assert_awaited_once()


async def test_delete_file_system_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_file_system failed"):
        await delete_file_system("fs-bad")


# ---------------------------------------------------------------------------
# create_mount_target
# ---------------------------------------------------------------------------


async def test_create_mount_target_ok(monkeypatch):
    mc = _mc(_MT_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await create_mount_target(
        "fs-12345678", subnet_id="subnet-12345"
    )
    assert result.mount_target_id == "fsmt-12345678"
    assert result.ip_address == "10.0.1.5"

async def test_create_mount_target_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_mount_target failed"):
        await create_mount_target("fs-bad", subnet_id="subnet-bad")


# ---------------------------------------------------------------------------
# describe_mount_targets
# ---------------------------------------------------------------------------


async def test_describe_mount_targets_ok(monkeypatch):
    mc = _mc(_MT_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_mount_targets(file_system_id="fs-12345678")
    assert len(result) == 1


async def test_describe_mount_targets_by_id(monkeypatch):
    mc = _mc(_MT_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_mount_targets(mount_target_id="fsmt-12345678")
    assert len(result) == 1


async def test_describe_mount_targets_pagination(monkeypatch):
    page1 = dict(_MT_LIST_RESP)
    page1["NextMarker"] = "tok"
    page2 = {"MountTargets": [dict(_MT_RESP, MountTargetId="fsmt-99999999")]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_mount_targets()
    assert len(result) == 2


async def test_describe_mount_targets_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_mount_targets failed"):
        await describe_mount_targets()


# ---------------------------------------------------------------------------
# delete_mount_target
# ---------------------------------------------------------------------------


async def test_delete_mount_target_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    await delete_mount_target("fsmt-12345678")
    mc.call.assert_awaited_once()


async def test_delete_mount_target_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_mount_target failed"):
        await delete_mount_target("fsmt-bad")


# ---------------------------------------------------------------------------
# describe_mount_target_security_groups
# ---------------------------------------------------------------------------


async def test_describe_sg_ok(monkeypatch):
    mc = _mc({"SecurityGroups": ["sg-123", "sg-456"]})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_mount_target_security_groups("fsmt-12345678")
    assert result == ["sg-123", "sg-456"]


async def test_describe_sg_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError,
        match="describe_mount_target_security_groups failed",
    ):
        await describe_mount_target_security_groups("fsmt-bad")


# ---------------------------------------------------------------------------
# modify_mount_target_security_groups
# ---------------------------------------------------------------------------


async def test_modify_sg_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    await modify_mount_target_security_groups(
        "fsmt-12345678", security_groups=["sg-789"]
    )
    mc.call.assert_awaited_once()


async def test_modify_sg_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError,
        match="modify_mount_target_security_groups failed",
    ):
        await modify_mount_target_security_groups(
            "fsmt-bad", security_groups=["sg-123"]
        )


# ---------------------------------------------------------------------------
# create_access_point
# ---------------------------------------------------------------------------


async def test_create_access_point_ok(monkeypatch):
    mc = _mc(_AP_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await create_access_point("fs-12345678")
    assert result.access_point_id == "fsap-12345678"
    assert result.name == "my-ap"

async def test_create_access_point_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="create_access_point failed"):
        await create_access_point("fs-bad")


# ---------------------------------------------------------------------------
# describe_access_points
# ---------------------------------------------------------------------------


async def test_describe_access_points_ok(monkeypatch):
    mc = _mc(_AP_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_access_points(file_system_id="fs-12345678")
    assert len(result) == 1


async def test_describe_access_points_by_id(monkeypatch):
    mc = _mc(_AP_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_access_points(access_point_id="fsap-12345678")
    assert len(result) == 1


async def test_describe_access_points_pagination(monkeypatch):
    page1 = dict(_AP_LIST_RESP)
    page1["NextToken"] = "tok"
    page2 = {
        "AccessPoints": [dict(_AP_RESP, AccessPointId="fsap-99999999")]
    }
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_access_points()
    assert len(result) == 2


async def test_describe_access_points_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="describe_access_points failed"):
        await describe_access_points()


# ---------------------------------------------------------------------------
# delete_access_point
# ---------------------------------------------------------------------------


async def test_delete_access_point_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    await delete_access_point("fsap-12345678")
    mc.call.assert_awaited_once()


async def test_delete_access_point_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="delete_access_point failed"):
        await delete_access_point("fsap-bad")


# ---------------------------------------------------------------------------
# put_lifecycle_configuration
# ---------------------------------------------------------------------------


async def test_put_lifecycle_ok(monkeypatch):
    mc = _mc(
        {"LifecyclePolicies": [{"TransitionToIA": "AFTER_30_DAYS"}]}
    )
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await put_lifecycle_configuration(
        "fs-12345678",
        lifecycle_policies=[{"TransitionToIA": "AFTER_30_DAYS"}],
    )
    assert len(result) == 1


async def test_put_lifecycle_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError, match="put_lifecycle_configuration failed"
    ):
        await put_lifecycle_configuration(
            "fs-bad", lifecycle_policies=[]
        )


# ---------------------------------------------------------------------------
# describe_lifecycle_configuration
# ---------------------------------------------------------------------------


async def test_describe_lifecycle_ok(monkeypatch):
    mc = _mc(
        {"LifecyclePolicies": [{"TransitionToIA": "AFTER_30_DAYS"}]}
    )
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_lifecycle_configuration("fs-12345678")
    assert len(result) == 1


async def test_describe_lifecycle_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError, match="describe_lifecycle_configuration failed"
    ):
        await describe_lifecycle_configuration("fs-bad")


# ---------------------------------------------------------------------------
# put_file_system_policy
# ---------------------------------------------------------------------------


async def test_put_policy_ok(monkeypatch):
    mc = _mc({"FileSystemId": "fs-12345678", "Policy": "{}"})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await put_file_system_policy(
        "fs-12345678", policy="{}"
    )
    assert result["FileSystemId"] == "fs-12345678"


async def test_put_policy_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError, match="put_file_system_policy failed"
    ):
        await put_file_system_policy("fs-bad", policy="{}")


# ---------------------------------------------------------------------------
# describe_file_system_policy
# ---------------------------------------------------------------------------


async def test_describe_policy_ok(monkeypatch):
    mc = _mc({"FileSystemId": "fs-12345678", "Policy": "{}"})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_system_policy("fs-12345678")
    assert result is not None
    assert result["FileSystemId"] == "fs-12345678"


async def test_describe_policy_not_found(monkeypatch):
    mc = _mc(se=RuntimeError("PolicyNotFound"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_system_policy("fs-12345678")
    assert result is None


async def test_describe_policy_fs_not_found(monkeypatch):
    mc = _mc(se=RuntimeError("FileSystemNotFound"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await describe_file_system_policy("fs-bad")
    assert result is None


async def test_describe_policy_other_error(monkeypatch):
    mc = _mc(se=ValueError("generic"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError, match="describe_file_system_policy failed"
    ):
        await describe_file_system_policy("fs-bad")


# ---------------------------------------------------------------------------
# delete_file_system_policy
# ---------------------------------------------------------------------------


async def test_delete_policy_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    await delete_file_system_policy("fs-12345678")
    mc.call.assert_awaited_once()


async def test_delete_policy_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(
        RuntimeError, match="delete_file_system_policy failed"
    ):
        await delete_file_system_policy("fs-bad")


# ---------------------------------------------------------------------------
# tag_resource
# ---------------------------------------------------------------------------


async def test_tag_resource_ok(monkeypatch):
    mc = _mc()
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    await tag_resource("fs-12345678", tags={"team": "platform"})
    mc.call.assert_awaited_once()


async def test_tag_resource_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="tag_resource failed"):
        await tag_resource("fs-bad", tags={"k": "v"})


# ---------------------------------------------------------------------------
# list_tags_for_resource
# ---------------------------------------------------------------------------


async def test_list_tags_ok(monkeypatch):
    mc = _mc({"Tags": [{"Key": "env", "Value": "prod"}]})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await list_tags_for_resource("fs-12345678")
    assert result == {"env": "prod"}


async def test_list_tags_pagination(monkeypatch):
    page1 = {
        "Tags": [{"Key": "a", "Value": "1"}],
        "NextToken": "tok",
    }
    page2 = {"Tags": [{"Key": "b", "Value": "2"}]}
    mc = _mc()
    mc.call = AsyncMock(side_effect=[page1, page2])
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await list_tags_for_resource("fs-12345678")
    assert result == {"a": "1", "b": "2"}


async def test_list_tags_error(monkeypatch):
    mc = _mc(se=ValueError("boom"))
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="list_tags_for_resource failed"):
        await list_tags_for_resource("fs-bad")


# ---------------------------------------------------------------------------
# wait_for_file_system
# ---------------------------------------------------------------------------


async def test_wait_already_available(monkeypatch):
    mc = _mc(_FS_LIST_RESP)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await wait_for_file_system(
        "fs-12345678", timeout=5, poll_interval=0.01
    )
    assert result.life_cycle_state == "available"


async def test_wait_becomes_available(monkeypatch):
    creating_resp = {
        "FileSystems": [dict(_FS_RESP, LifeCycleState="creating")]
    }
    available_resp = _FS_LIST_RESP
    mc = _mc()
    mc.call = AsyncMock(side_effect=[creating_resp, available_resp])
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    result = await wait_for_file_system(
        "fs-12345678", timeout=5, poll_interval=0.01
    )
    assert result.life_cycle_state == "available"


async def test_wait_timeout(monkeypatch):
    creating_resp = {
        "FileSystems": [dict(_FS_RESP, LifeCycleState="creating")]
    }
    mc = _mc(creating_resp)
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(AwsTimeoutError, match="did not reach state"):
        await wait_for_file_system(
            "fs-12345678", timeout=0.05, poll_interval=0.01
        )


async def test_wait_not_found(monkeypatch):
    mc = _mc({"FileSystems": []})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mc)
    with pytest.raises(RuntimeError, match="not found"):
        await wait_for_file_system(
            "fs-nonexistent", timeout=1, poll_interval=0.01
        )


async def test_create_replication_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_replication_configuration("test-source_file_system_id", [], )
    mock_client.call.assert_called_once()


async def test_create_replication_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_replication_configuration("test-source_file_system_id", [], )


async def test_create_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_tags("test-file_system_id", [], )
    mock_client.call.assert_called_once()


async def test_create_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_tags("test-file_system_id", [], )


async def test_delete_replication_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_replication_configuration("test-source_file_system_id", )
    mock_client.call.assert_called_once()


async def test_delete_replication_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_replication_configuration("test-source_file_system_id", )


async def test_delete_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_tags("test-file_system_id", [], )
    mock_client.call.assert_called_once()


async def test_delete_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_tags("test-file_system_id", [], )


async def test_describe_account_preferences(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_account_preferences()
    mock_client.call.assert_called_once()


async def test_describe_account_preferences_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_account_preferences()


async def test_describe_backup_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_backup_policy("test-file_system_id", )
    mock_client.call.assert_called_once()


async def test_describe_backup_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_backup_policy("test-file_system_id", )


async def test_describe_replication_configurations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replication_configurations()
    mock_client.call.assert_called_once()


async def test_describe_replication_configurations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replication_configurations()


async def test_describe_tags(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_tags("test-file_system_id", )
    mock_client.call.assert_called_once()


async def test_describe_tags_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_tags("test-file_system_id", )


async def test_put_account_preferences(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_account_preferences("test-resource_id_type", )
    mock_client.call.assert_called_once()


async def test_put_account_preferences_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_account_preferences("test-resource_id_type", )


async def test_put_backup_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_backup_policy("test-file_system_id", {}, )
    mock_client.call.assert_called_once()


async def test_put_backup_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_backup_policy("test-file_system_id", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_id", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_id", [], )


async def test_update_file_system_protection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_file_system_protection("test-file_system_id", )
    mock_client.call.assert_called_once()


async def test_update_file_system_protection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.efs.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_file_system_protection("test-file_system_id", )


@pytest.mark.asyncio
async def test_delete_replication_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import delete_replication_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mock_client)
    await delete_replication_configuration("test-source_file_system_id", deletion_mode="test-deletion_mode", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_account_preferences_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import describe_account_preferences
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mock_client)
    await describe_account_preferences(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_replication_configurations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import describe_replication_configurations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mock_client)
    await describe_replication_configurations(file_system_id="test-file_system_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import describe_tags
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mock_client)
    await describe_tags("test-file_system_id", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_file_system_protection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import update_file_system_protection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mock_client)
    await update_file_system_protection("test-file_system_id", replication_overwrite_protection="test-replication_overwrite_protection", region_name="us-east-1")
    mock_client.call.assert_called_once()


@pytest.mark.asyncio
async def test_create_access_point_with_tags(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import create_access_point
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={"AccessPointId": "ap-1", "FileSystemId": "fs-1"})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: mock_client)
    await create_access_point("fs-1", posix_user={"Uid": 1000, "Gid": 1000}, root_directory={}, tags={"env": "test"}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_file_system_with_tags(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import create_file_system
    m = AsyncMock(); m.call = AsyncMock(return_value={"FileSystemId": "fs-1", "LifeCycleState": "available", "NumberOfMountTargets": 0, "SizeInBytes": {"Value": 0}})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: m)
    await create_file_system(creation_token="tk", tags={"env": "test"}, region_name="us-east-1")

@pytest.mark.asyncio
async def test_create_mount_target_opts(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.efs import create_mount_target
    m = AsyncMock(); m.call = AsyncMock(return_value={"MountTargetId": "mt-1", "FileSystemId": "fs-1", "SubnetId": "sn-1", "LifeCycleState": "available"})
    monkeypatch.setattr("aws_util.aio.efs.async_client", lambda *a, **kw: m)
    await create_mount_target(file_system_id="fs-1", subnet_id="sn-1", security_groups=["sg-1"], ip_address="10.0.0.1", region_name="us-east-1")
