"""Tests for aws_util.efs module."""
from __future__ import annotations

import json
import time
from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError

import aws_util.efs as efs_mod
from aws_util.efs import (
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

REGION = "us-east-1"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def efs_client():
    return boto3.client("efs", region_name=REGION)


@pytest.fixture
def vpc_resources():
    """Create a VPC + subnet for mount-target tests."""
    ec2 = boto3.client("ec2", region_name=REGION)
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]
    subnet = ec2.create_subnet(VpcId=vpc_id, CidrBlock="10.0.1.0/24")
    subnet_id = subnet["Subnet"]["SubnetId"]
    sg = ec2.create_security_group(
        GroupName="efs-sg", Description="EFS SG", VpcId=vpc_id
    )
    sg_id = sg["GroupId"]
    sg2 = ec2.create_security_group(
        GroupName="efs-sg-2", Description="EFS SG 2", VpcId=vpc_id
    )
    sg2_id = sg2["GroupId"]
    return {
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "sg_id": sg_id,
        "sg2_id": sg2_id,
    }


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestFileSystemResultModel:
    def test_basic_fields(self):
        fs = FileSystemResult(
            file_system_id="fs-12345",
            life_cycle_state="available",
        )
        assert fs.file_system_id == "fs-12345"
        assert fs.life_cycle_state == "available"
        assert fs.performance_mode == "generalPurpose"
        assert fs.encrypted is False
        assert fs.tags == {}
        assert fs.extra == {}

    def test_all_fields(self):
        fs = FileSystemResult(
            file_system_id="fs-12345",
            file_system_arn="arn:aws:elasticfilesystem:us-east-1:123:file-system/fs-12345",
            creation_time="2024-01-01T00:00:00Z",
            life_cycle_state="available",
            performance_mode="maxIO",
            throughput_mode="provisioned",
            encrypted=True,
            size_in_bytes={"Value": 1024},
            tags={"env": "prod"},
            extra={"OwnerId": "123456789012"},
        )
        assert fs.encrypted is True
        assert fs.throughput_mode == "provisioned"
        assert fs.tags["env"] == "prod"

    def test_frozen(self):
        fs = FileSystemResult(
            file_system_id="fs-12345",
            life_cycle_state="available",
        )
        with pytest.raises(Exception):
            fs.file_system_id = "changed"  # type: ignore[misc]


class TestMountTargetResultModel:
    def test_basic_fields(self):
        mt = MountTargetResult(
            mount_target_id="fsmt-12345",
            file_system_id="fs-12345",
            subnet_id="subnet-12345",
            life_cycle_state="available",
        )
        assert mt.mount_target_id == "fsmt-12345"
        assert mt.ip_address is None
        assert mt.extra == {}

    def test_frozen(self):
        mt = MountTargetResult(
            mount_target_id="fsmt-12345",
            file_system_id="fs-12345",
            subnet_id="subnet-12345",
            life_cycle_state="available",
        )
        with pytest.raises(Exception):
            mt.mount_target_id = "changed"  # type: ignore[misc]


class TestAccessPointResultModel:
    def test_basic_fields(self):
        ap = AccessPointResult(
            access_point_id="fsap-12345",
            file_system_id="fs-12345",
        )
        assert ap.access_point_id == "fsap-12345"
        assert ap.name is None
        assert ap.posix_user is None
        assert ap.extra == {}

    def test_frozen(self):
        ap = AccessPointResult(
            access_point_id="fsap-12345",
            file_system_id="fs-12345",
        )
        with pytest.raises(Exception):
            ap.access_point_id = "changed"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# create_file_system
# ---------------------------------------------------------------------------


class TestCreateFileSystem:
    def test_create_basic(self):
        result = create_file_system(region_name=REGION)
        assert result.file_system_id.startswith("fs-")
        assert result.life_cycle_state == "available"
        assert result.performance_mode == "generalPurpose"

    def test_create_with_token(self):
        result = create_file_system(
            creation_token="my-token", region_name=REGION
        )
        assert result.file_system_id.startswith("fs-")

    def test_create_encrypted(self):
        result = create_file_system(encrypted=True, region_name=REGION)
        assert result.encrypted is True

    def test_create_with_tags(self):
        result = create_file_system(
            tags={"env": "test"}, region_name=REGION
        )
        assert result.tags.get("env") == "test"

    def test_create_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_file_system.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "boom"}},
            "CreateFileSystem",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_file_system failed"):
            create_file_system(region_name=REGION)


# ---------------------------------------------------------------------------
# describe_file_systems
# ---------------------------------------------------------------------------


class TestDescribeFileSystems:
    def test_describe_all(self):
        create_file_system(region_name=REGION)
        create_file_system(region_name=REGION)
        results = describe_file_systems(region_name=REGION)
        assert len(results) >= 2

    def test_describe_by_id(self):
        fs = create_file_system(region_name=REGION)
        results = describe_file_systems(
            file_system_id=fs.file_system_id, region_name=REGION
        )
        assert len(results) == 1
        assert results[0].file_system_id == fs.file_system_id

    def test_describe_by_token(self):
        create_file_system(creation_token="tok-1", region_name=REGION)
        results = describe_file_systems(
            creation_token="tok-1", region_name=REGION
        )
        assert len(results) == 1

    def test_describe_empty(self):
        results = describe_file_systems(region_name=REGION)
        assert results == []

    def test_describe_pagination(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_file_systems.side_effect = [
            {
                "FileSystems": [
                    {
                        "FileSystemId": "fs-aaa",
                        "LifeCycleState": "available",
                        "Tags": [],
                    }
                ],
                "NextMarker": "tok",
            },
            {
                "FileSystems": [
                    {
                        "FileSystemId": "fs-bbb",
                        "LifeCycleState": "available",
                        "Tags": [],
                    }
                ],
            },
        ]
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        results = describe_file_systems(region_name=REGION)
        assert len(results) == 2
        assert results[0].file_system_id == "fs-aaa"
        assert results[1].file_system_id == "fs-bbb"

    def test_describe_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_file_systems.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "boom"}},
            "DescribeFileSystems",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_file_systems failed"):
            describe_file_systems(region_name=REGION)


# ---------------------------------------------------------------------------
# update_file_system
# ---------------------------------------------------------------------------


class TestUpdateFileSystem:
    def test_update_throughput_mode(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_file_system.return_value = {
            "FileSystemId": "fs-12345678",
            "LifeCycleState": "available",
            "PerformanceMode": "generalPurpose",
            "ThroughputMode": "bursting",
            "Encrypted": False,
            "Tags": [],
        }
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        updated = update_file_system(
            "fs-12345678",
            throughput_mode="bursting",
            region_name=REGION,
        )
        assert updated.file_system_id == "fs-12345678"

    def test_update_with_provisioned(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_file_system.return_value = {
            "FileSystemId": "fs-12345678",
            "LifeCycleState": "available",
            "ThroughputMode": "provisioned",
            "Tags": [],
        }
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        updated = update_file_system(
            "fs-12345678",
            throughput_mode="provisioned",
            provisioned_throughput_in_mibps=256.0,
            region_name=REGION,
        )
        assert updated.file_system_id == "fs-12345678"

    def test_update_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_file_system.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "UpdateFileSystem",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="update_file_system failed"):
            update_file_system("fs-bad", region_name=REGION)


# ---------------------------------------------------------------------------
# delete_file_system
# ---------------------------------------------------------------------------


class TestDeleteFileSystem:
    def test_delete_ok(self):
        fs = create_file_system(region_name=REGION)
        delete_file_system(fs.file_system_id, region_name=REGION)
        results = describe_file_systems(region_name=REGION)
        ids = [r.file_system_id for r in results]
        assert fs.file_system_id not in ids

    def test_delete_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_file_system.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "DeleteFileSystem",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_file_system failed"):
            delete_file_system("fs-bad", region_name=REGION)


# ---------------------------------------------------------------------------
# Mount-target operations
# ---------------------------------------------------------------------------


class TestMountTargets:
    def test_create_mount_target(self, vpc_resources):
        fs = create_file_system(region_name=REGION)
        mt = create_mount_target(
            fs.file_system_id,
            subnet_id=vpc_resources["subnet_id"],
            security_groups=[vpc_resources["sg_id"]],
            region_name=REGION,
        )
        assert mt.file_system_id == fs.file_system_id
        assert mt.subnet_id == vpc_resources["subnet_id"]

    def test_describe_mount_targets_by_fs(self, vpc_resources):
        fs = create_file_system(region_name=REGION)
        create_mount_target(
            fs.file_system_id,
            subnet_id=vpc_resources["subnet_id"],
            region_name=REGION,
        )
        results = describe_mount_targets(
            file_system_id=fs.file_system_id, region_name=REGION
        )
        assert len(results) == 1

    def test_describe_mount_targets_by_id(self, vpc_resources):
        fs = create_file_system(region_name=REGION)
        mt = create_mount_target(
            fs.file_system_id,
            subnet_id=vpc_resources["subnet_id"],
            region_name=REGION,
        )
        results = describe_mount_targets(
            mount_target_id=mt.mount_target_id, region_name=REGION
        )
        assert len(results) == 1
        assert results[0].mount_target_id == mt.mount_target_id

    def test_delete_mount_target(self, vpc_resources):
        fs = create_file_system(region_name=REGION)
        mt = create_mount_target(
            fs.file_system_id,
            subnet_id=vpc_resources["subnet_id"],
            region_name=REGION,
        )
        delete_mount_target(mt.mount_target_id, region_name=REGION)
        results = describe_mount_targets(
            file_system_id=fs.file_system_id, region_name=REGION
        )
        assert len(results) == 0

    def test_security_groups(self, vpc_resources):
        fs = create_file_system(region_name=REGION)
        mt = create_mount_target(
            fs.file_system_id,
            subnet_id=vpc_resources["subnet_id"],
            security_groups=[vpc_resources["sg_id"]],
            region_name=REGION,
        )
        sgs = describe_mount_target_security_groups(
            mt.mount_target_id, region_name=REGION
        )
        assert vpc_resources["sg_id"] in sgs

        modify_mount_target_security_groups(
            mt.mount_target_id,
            security_groups=[vpc_resources["sg2_id"]],
            region_name=REGION,
        )
        sgs2 = describe_mount_target_security_groups(
            mt.mount_target_id, region_name=REGION
        )
        assert vpc_resources["sg2_id"] in sgs2

    def test_create_mount_target_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_mount_target.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "CreateMountTarget",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_mount_target failed"):
            create_mount_target(
                "fs-bad", subnet_id="subnet-bad", region_name=REGION
            )

    def test_describe_mount_targets_pagination(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_mount_targets.side_effect = [
            {
                "MountTargets": [
                    {
                        "MountTargetId": "fsmt-aaa",
                        "FileSystemId": "fs-123",
                        "SubnetId": "subnet-123",
                        "LifeCycleState": "available",
                    }
                ],
                "NextMarker": "tok",
            },
            {
                "MountTargets": [
                    {
                        "MountTargetId": "fsmt-bbb",
                        "FileSystemId": "fs-123",
                        "SubnetId": "subnet-456",
                        "LifeCycleState": "available",
                    }
                ],
            },
        ]
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        results = describe_mount_targets(region_name=REGION)
        assert len(results) == 2

    def test_describe_mount_targets_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_mount_targets.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "boom"}},
            "DescribeMountTargets",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_mount_targets failed"):
            describe_mount_targets(region_name=REGION)

    def test_delete_mount_target_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_mount_target.side_effect = ClientError(
            {"Error": {"Code": "MountTargetNotFound", "Message": "nope"}},
            "DeleteMountTarget",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_mount_target failed"):
            delete_mount_target("fsmt-bad", region_name=REGION)

    def test_describe_sg_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_mount_target_security_groups.side_effect = ClientError(
            {"Error": {"Code": "MountTargetNotFound", "Message": "nope"}},
            "DescribeMountTargetSecurityGroups",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError,
            match="describe_mount_target_security_groups failed",
        ):
            describe_mount_target_security_groups("fsmt-bad", region_name=REGION)

    def test_modify_sg_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.modify_mount_target_security_groups.side_effect = ClientError(
            {"Error": {"Code": "MountTargetNotFound", "Message": "nope"}},
            "ModifyMountTargetSecurityGroups",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError,
            match="modify_mount_target_security_groups failed",
        ):
            modify_mount_target_security_groups(
                "fsmt-bad",
                security_groups=["sg-123"],
                region_name=REGION,
            )

    def test_create_mount_target_with_ip(self, vpc_resources):
        fs = create_file_system(region_name=REGION)
        mt = create_mount_target(
            fs.file_system_id,
            subnet_id=vpc_resources["subnet_id"],
            ip_address="10.0.1.100",
            region_name=REGION,
        )
        assert mt.ip_address == "10.0.1.100"


# ---------------------------------------------------------------------------
# Access-point operations
# ---------------------------------------------------------------------------


class TestAccessPoints:
    def test_create_access_point(self):
        fs = create_file_system(region_name=REGION)
        ap = create_access_point(fs.file_system_id, region_name=REGION)
        assert ap.file_system_id == fs.file_system_id

    def test_create_access_point_with_options(self):
        fs = create_file_system(region_name=REGION)
        ap = create_access_point(
            fs.file_system_id,
            posix_user={"Uid": 1000, "Gid": 1000},
            root_directory={
                "Path": "/data",
                "CreationInfo": {
                    "OwnerUid": 1000,
                    "OwnerGid": 1000,
                    "Permissions": "755",
                },
            },
            tags={"Name": "my-ap"},
            region_name=REGION,
        )
        assert ap.file_system_id == fs.file_system_id

    def test_describe_access_points(self):
        fs = create_file_system(region_name=REGION)
        create_access_point(fs.file_system_id, region_name=REGION)
        results = describe_access_points(
            file_system_id=fs.file_system_id, region_name=REGION
        )
        assert len(results) >= 1

    def test_describe_access_points_by_id(self):
        fs = create_file_system(region_name=REGION)
        ap = create_access_point(fs.file_system_id, region_name=REGION)
        results = describe_access_points(
            access_point_id=ap.access_point_id, region_name=REGION
        )
        assert len(results) == 1

    def test_delete_access_point(self):
        fs = create_file_system(region_name=REGION)
        ap = create_access_point(fs.file_system_id, region_name=REGION)
        delete_access_point(ap.access_point_id, region_name=REGION)
        results = describe_access_points(
            file_system_id=fs.file_system_id, region_name=REGION
        )
        ids = [r.access_point_id for r in results]
        assert ap.access_point_id not in ids

    def test_create_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_access_point.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "CreateAccessPoint",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_access_point failed"):
            create_access_point("fs-bad", region_name=REGION)

    def test_describe_access_points_pagination(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_access_points.side_effect = [
            {
                "AccessPoints": [
                    {
                        "AccessPointId": "fsap-aaa",
                        "FileSystemId": "fs-123",
                    }
                ],
                "NextToken": "tok",
            },
            {
                "AccessPoints": [
                    {
                        "AccessPointId": "fsap-bbb",
                        "FileSystemId": "fs-123",
                    }
                ],
            },
        ]
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        results = describe_access_points(region_name=REGION)
        assert len(results) == 2

    def test_describe_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_access_points.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "boom"}},
            "DescribeAccessPoints",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_access_points failed"):
            describe_access_points(region_name=REGION)

    def test_delete_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_access_point.side_effect = ClientError(
            {"Error": {"Code": "AccessPointNotFound", "Message": "nope"}},
            "DeleteAccessPoint",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_access_point failed"):
            delete_access_point("fsap-bad", region_name=REGION)


# ---------------------------------------------------------------------------
# Lifecycle configuration
# ---------------------------------------------------------------------------


class TestLifecycleConfiguration:
    def test_put_and_describe(self):
        fs = create_file_system(region_name=REGION)
        policies = [{"TransitionToIA": "AFTER_30_DAYS"}]
        result = put_lifecycle_configuration(
            fs.file_system_id,
            lifecycle_policies=policies,
            region_name=REGION,
        )
        assert isinstance(result, list)

        described = describe_lifecycle_configuration(
            fs.file_system_id, region_name=REGION
        )
        assert isinstance(described, list)

    def test_put_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.put_lifecycle_configuration.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "PutLifecycleConfiguration",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="put_lifecycle_configuration failed"
        ):
            put_lifecycle_configuration(
                "fs-bad",
                lifecycle_policies=[],
                region_name=REGION,
            )

    def test_describe_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_lifecycle_configuration.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "DescribeLifecycleConfiguration",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="describe_lifecycle_configuration failed"
        ):
            describe_lifecycle_configuration("fs-bad", region_name=REGION)


# ---------------------------------------------------------------------------
# File-system policy
# ---------------------------------------------------------------------------


class TestFileSystemPolicy:
    def test_put_and_describe(self):
        fs = create_file_system(region_name=REGION)
        policy_doc = json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "elasticfilesystem:ClientMount",
                        "Resource": f"arn:aws:elasticfilesystem:us-east-1:123456789012:file-system/{fs.file_system_id}",
                    }
                ],
            }
        )
        result = put_file_system_policy(
            fs.file_system_id, policy=policy_doc, region_name=REGION
        )
        assert isinstance(result, dict)

    def test_describe_no_policy(self):
        fs = create_file_system(region_name=REGION)
        result = describe_file_system_policy(
            fs.file_system_id, region_name=REGION
        )
        # moto may or may not raise PolicyNotFound; either None or a dict is ok
        assert result is None or isinstance(result, dict)

    def test_describe_policy_success(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_file_system_policy.return_value = {
            "FileSystemId": "fs-123",
            "Policy": "{}",
        }
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_file_system_policy("fs-123", region_name=REGION)
        assert result is not None
        assert result["FileSystemId"] == "fs-123"

    def test_delete_policy(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_file_system_policy.return_value = {}
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        delete_file_system_policy("fs-12345678", region_name=REGION)
        mock_client.delete_file_system_policy.assert_called_once_with(
            FileSystemId="fs-12345678"
        )

    def test_put_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.put_file_system_policy.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "PutFileSystemPolicy",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="put_file_system_policy failed"
        ):
            put_file_system_policy(
                "fs-bad", policy="{}", region_name=REGION
            )

    def test_describe_error_non_policy_not_found(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_file_system_policy.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "boom"}},
            "DescribeFileSystemPolicy",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="describe_file_system_policy failed"
        ):
            describe_file_system_policy("fs-bad", region_name=REGION)

    def test_describe_policy_not_found_returns_none(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_file_system_policy.side_effect = ClientError(
            {"Error": {"Code": "PolicyNotFound", "Message": "no policy"}},
            "DescribeFileSystemPolicy",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_file_system_policy("fs-123", region_name=REGION)
        assert result is None

    def test_describe_fs_not_found_returns_none(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_file_system_policy.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "no fs"}},
            "DescribeFileSystemPolicy",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_file_system_policy("fs-bad", region_name=REGION)
        assert result is None

    def test_delete_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_file_system_policy.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "DeleteFileSystemPolicy",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="delete_file_system_policy failed"
        ):
            delete_file_system_policy("fs-bad", region_name=REGION)


# ---------------------------------------------------------------------------
# Tagging
# ---------------------------------------------------------------------------


class TestTagging:
    def test_tag_and_list(self):
        fs = create_file_system(region_name=REGION)
        tag_resource(
            fs.file_system_id,
            tags={"team": "platform"},
            region_name=REGION,
        )
        tags = list_tags_for_resource(
            fs.file_system_id, region_name=REGION
        )
        assert tags["team"] == "platform"

    def test_tag_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.tag_resource.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "TagResource",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="tag_resource failed"):
            tag_resource(
                "fs-bad", tags={"k": "v"}, region_name=REGION
            )

    def test_list_tags_pagination(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_tags_for_resource.side_effect = [
            {
                "Tags": [{"Key": "a", "Value": "1"}],
                "NextToken": "tok",
            },
            {
                "Tags": [{"Key": "b", "Value": "2"}],
            },
        ]
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        tags = list_tags_for_resource("fs-123", region_name=REGION)
        assert tags == {"a": "1", "b": "2"}

    def test_list_tags_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.list_tags_for_resource.side_effect = ClientError(
            {"Error": {"Code": "FileSystemNotFound", "Message": "nope"}},
            "ListTagsForResource",
        )
        monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="list_tags_for_resource failed"
        ):
            list_tags_for_resource("fs-bad", region_name=REGION)


# ---------------------------------------------------------------------------
# wait_for_file_system
# ---------------------------------------------------------------------------


class TestWaitForFileSystem:
    def test_wait_already_available(self):
        fs = create_file_system(region_name=REGION)
        result = wait_for_file_system(
            fs.file_system_id,
            target_state="available",
            timeout=10,
            poll_interval=0.1,
            region_name=REGION,
        )
        assert result.file_system_id == fs.file_system_id
        assert result.life_cycle_state == "available"

    def test_wait_timeout(self, monkeypatch):
        fs = create_file_system(region_name=REGION)

        # Make describe always return "creating"
        original = efs_mod.describe_file_systems

        def _mock_describe(**kwargs):
            results = original(**kwargs)
            patched = []
            for r in results:
                patched.append(
                    FileSystemResult(
                        file_system_id=r.file_system_id,
                        life_cycle_state="creating",
                        performance_mode=r.performance_mode,
                    )
                )
            return patched

        monkeypatch.setattr(efs_mod, "describe_file_systems", _mock_describe)
        with pytest.raises(AwsTimeoutError, match="did not reach state"):
            wait_for_file_system(
                fs.file_system_id,
                timeout=0.1,
                poll_interval=0.05,
                region_name=REGION,
            )

    def test_wait_not_found(self, monkeypatch):
        monkeypatch.setattr(
            efs_mod, "describe_file_systems", lambda **kw: []
        )
        with pytest.raises(RuntimeError, match="not found"):
            wait_for_file_system(
                "fs-nonexistent",
                timeout=1,
                poll_interval=0.1,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# _parse helpers edge cases
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_file_system_minimal(self):
        raw = {
            "FileSystemId": "fs-123",
            "LifeCycleState": "creating",
        }
        result = efs_mod._parse_file_system(raw)
        assert result.file_system_id == "fs-123"
        assert result.file_system_arn is None
        assert result.creation_time is None
        assert result.tags == {}

    def test_parse_mount_target_minimal(self):
        raw = {
            "MountTargetId": "fsmt-123",
            "FileSystemId": "fs-123",
            "SubnetId": "subnet-123",
            "LifeCycleState": "available",
        }
        result = efs_mod._parse_mount_target(raw)
        assert result.ip_address is None
        assert result.availability_zone_name is None

    def test_parse_access_point_with_name_tag(self):
        raw = {
            "AccessPointId": "fsap-123",
            "FileSystemId": "fs-123",
            "Tags": [{"Key": "Name", "Value": "my-ap"}],
        }
        result = efs_mod._parse_access_point(raw)
        assert result.name == "my-ap"

    def test_parse_access_point_no_name_tag(self):
        raw = {
            "AccessPointId": "fsap-123",
            "FileSystemId": "fs-123",
            "Tags": [{"Key": "env", "Value": "prod"}],
        }
        result = efs_mod._parse_access_point(raw)
        assert result.name is None

    def test_parse_access_point_no_tags(self):
        raw = {
            "AccessPointId": "fsap-123",
            "FileSystemId": "fs-123",
        }
        result = efs_mod._parse_access_point(raw)
        assert result.name is None

    def test_parse_file_system_extra_keys(self):
        raw = {
            "FileSystemId": "fs-123",
            "LifeCycleState": "available",
            "OwnerId": "123456789012",
            "NumberOfMountTargets": 2,
        }
        result = efs_mod._parse_file_system(raw)
        assert result.extra["OwnerId"] == "123456789012"
        assert result.extra["NumberOfMountTargets"] == 2

    def test_parse_mount_target_extra_keys(self):
        raw = {
            "MountTargetId": "fsmt-123",
            "FileSystemId": "fs-123",
            "SubnetId": "subnet-123",
            "LifeCycleState": "available",
            "OwnerId": "123456789012",
        }
        result = efs_mod._parse_mount_target(raw)
        assert result.extra["OwnerId"] == "123456789012"

    def test_parse_access_point_extra_keys(self):
        raw = {
            "AccessPointId": "fsap-123",
            "FileSystemId": "fs-123",
            "OwnerId": "123456789012",
        }
        result = efs_mod._parse_access_point(raw)
        assert result.extra["OwnerId"] == "123456789012"


def test_create_replication_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_replication_configuration.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    create_replication_configuration("test-source_file_system_id", [], region_name=REGION)
    mock_client.create_replication_configuration.assert_called_once()


def test_create_replication_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_replication_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_replication_configuration",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create replication configuration"):
        create_replication_configuration("test-source_file_system_id", [], region_name=REGION)


def test_create_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tags.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    create_tags("test-file_system_id", [], region_name=REGION)
    mock_client.create_tags.assert_called_once()


def test_create_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_tags",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create tags"):
        create_tags("test-file_system_id", [], region_name=REGION)


def test_delete_replication_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_replication_configuration.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_replication_configuration("test-source_file_system_id", region_name=REGION)
    mock_client.delete_replication_configuration.assert_called_once()


def test_delete_replication_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_replication_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_replication_configuration",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete replication configuration"):
        delete_replication_configuration("test-source_file_system_id", region_name=REGION)


def test_delete_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    delete_tags("test-file_system_id", [], region_name=REGION)
    mock_client.delete_tags.assert_called_once()


def test_delete_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_tags",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete tags"):
        delete_tags("test-file_system_id", [], region_name=REGION)


def test_describe_account_preferences(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_preferences.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_account_preferences(region_name=REGION)
    mock_client.describe_account_preferences.assert_called_once()


def test_describe_account_preferences_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_account_preferences.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_account_preferences",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe account preferences"):
        describe_account_preferences(region_name=REGION)


def test_describe_backup_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_backup_policy.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_backup_policy("test-file_system_id", region_name=REGION)
    mock_client.describe_backup_policy.assert_called_once()


def test_describe_backup_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_backup_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_backup_policy",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe backup policy"):
        describe_backup_policy("test-file_system_id", region_name=REGION)


def test_describe_replication_configurations(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replication_configurations.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_replication_configurations(region_name=REGION)
    mock_client.describe_replication_configurations.assert_called_once()


def test_describe_replication_configurations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replication_configurations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replication_configurations",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe replication configurations"):
        describe_replication_configurations(region_name=REGION)


def test_describe_tags(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    describe_tags("test-file_system_id", region_name=REGION)
    mock_client.describe_tags.assert_called_once()


def test_describe_tags_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_tags.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_tags",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe tags"):
        describe_tags("test-file_system_id", region_name=REGION)


def test_put_account_preferences(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_preferences.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    put_account_preferences("test-resource_id_type", region_name=REGION)
    mock_client.put_account_preferences.assert_called_once()


def test_put_account_preferences_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_account_preferences.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_account_preferences",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put account preferences"):
        put_account_preferences("test-resource_id_type", region_name=REGION)


def test_put_backup_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_backup_policy.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    put_backup_policy("test-file_system_id", {}, region_name=REGION)
    mock_client.put_backup_policy.assert_called_once()


def test_put_backup_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_backup_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_backup_policy",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put backup policy"):
        put_backup_policy("test-file_system_id", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_id", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_id", [], region_name=REGION)


def test_update_file_system_protection(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_file_system_protection.return_value = {}
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    update_file_system_protection("test-file_system_id", region_name=REGION)
    mock_client.update_file_system_protection.assert_called_once()


def test_update_file_system_protection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_file_system_protection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_file_system_protection",
    )
    monkeypatch.setattr(efs_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update file system protection"):
        update_file_system_protection("test-file_system_id", region_name=REGION)


def test_delete_replication_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.efs import delete_replication_configuration
    mock_client = MagicMock()
    mock_client.delete_replication_configuration.return_value = {}
    monkeypatch.setattr("aws_util.efs.get_client", lambda *a, **kw: mock_client)
    delete_replication_configuration("test-source_file_system_id", deletion_mode="test-deletion_mode", region_name="us-east-1")
    mock_client.delete_replication_configuration.assert_called_once()

def test_describe_account_preferences_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.efs import describe_account_preferences
    mock_client = MagicMock()
    mock_client.describe_account_preferences.return_value = {}
    monkeypatch.setattr("aws_util.efs.get_client", lambda *a, **kw: mock_client)
    describe_account_preferences(next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_account_preferences.assert_called_once()

def test_describe_replication_configurations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.efs import describe_replication_configurations
    mock_client = MagicMock()
    mock_client.describe_replication_configurations.return_value = {}
    monkeypatch.setattr("aws_util.efs.get_client", lambda *a, **kw: mock_client)
    describe_replication_configurations(file_system_id="test-file_system_id", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.describe_replication_configurations.assert_called_once()

def test_describe_tags_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.efs import describe_tags
    mock_client = MagicMock()
    mock_client.describe_tags.return_value = {}
    monkeypatch.setattr("aws_util.efs.get_client", lambda *a, **kw: mock_client)
    describe_tags("test-file_system_id", max_items=1, marker="test-marker", region_name="us-east-1")
    mock_client.describe_tags.assert_called_once()

def test_update_file_system_protection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.efs import update_file_system_protection
    mock_client = MagicMock()
    mock_client.update_file_system_protection.return_value = {}
    monkeypatch.setattr("aws_util.efs.get_client", lambda *a, **kw: mock_client)
    update_file_system_protection("test-file_system_id", replication_overwrite_protection="test-replication_overwrite_protection", region_name="us-east-1")
    mock_client.update_file_system_protection.assert_called_once()
