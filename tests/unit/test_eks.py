"""Tests for aws_util.eks module."""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import boto3
import pytest
from botocore.exceptions import ClientError

import aws_util.eks as eks_mod
from aws_util.eks import (
    AddonResult,
    ClusterResult,
    FargateProfileResult,
    NodegroupResult,
    create_addon,
    create_cluster,
    create_fargate_profile,
    create_nodegroup,
    delete_addon,
    delete_cluster,
    delete_fargate_profile,
    delete_nodegroup,
    describe_addon,
    describe_cluster,
    describe_fargate_profile,
    describe_nodegroup,
    list_addons,
    list_clusters,
    list_fargate_profiles,
    list_nodegroups,
    update_addon,
    update_cluster_config,
    update_cluster_version,
    update_nodegroup_config,
    wait_for_cluster,
    wait_for_nodegroup,
    _parse_cluster,
    _parse_nodegroup,
    _parse_addon,
    _parse_fargate_profile,
    associate_access_policy,
    associate_encryption_config,
    associate_identity_provider_config,
    create_access_entry,
    create_eks_anywhere_subscription,
    create_pod_identity_association,
    delete_access_entry,
    delete_eks_anywhere_subscription,
    delete_pod_identity_association,
    deregister_cluster,
    describe_access_entry,
    describe_addon_configuration,
    describe_addon_versions,
    describe_cluster_versions,
    describe_eks_anywhere_subscription,
    describe_identity_provider_config,
    describe_insight,
    describe_insights_refresh,
    describe_pod_identity_association,
    describe_update,
    disassociate_access_policy,
    disassociate_identity_provider_config,
    list_access_entries,
    list_access_policies,
    list_associated_access_policies,
    list_eks_anywhere_subscriptions,
    list_identity_provider_configs,
    list_insights,
    list_pod_identity_associations,
    list_tags_for_resource,
    list_updates,
    register_cluster,
    start_insights_refresh,
    tag_resource,
    untag_resource,
    update_access_entry,
    update_eks_anywhere_subscription,
    update_nodegroup_version,
    update_pod_identity_association,
)

REGION = "us-east-1"
CLUSTER_NAME = "test-cluster"
ROLE_ARN = "arn:aws:iam::123456789012:role/eks-role"
SUBNET_IDS = ["subnet-12345"]
NODEGROUP_NAME = "test-nodegroup"
ADDON_NAME = "vpc-cni"
FARGATE_PROFILE_NAME = "test-fargate"


# ---------------------------------------------------------------------------
# Helpers — raw dicts matching AWS API shape
# ---------------------------------------------------------------------------


def _cluster_dict(**overrides: object) -> dict:
    d: dict = {
        "name": CLUSTER_NAME,
        "arn": f"arn:aws:eks:{REGION}:123456789012:cluster/{CLUSTER_NAME}",
        "status": "ACTIVE",
        "endpoint": "https://ABCDEF.gr7.us-east-1.eks.amazonaws.com",
        "roleArn": ROLE_ARN,
        "version": "1.28",
        "platformVersion": "eks.1",
        "kubernetesNetworkConfig": {"serviceIpv4Cidr": "10.100.0.0/16"},
        "certificateAuthority": {"data": "LS0tLS1C..."},
        "createdAt": "2024-01-01T00:00:00Z",
        "tags": {"env": "test"},
    }
    d.update(overrides)
    return d


def _nodegroup_dict(**overrides: object) -> dict:
    d: dict = {
        "nodegroupName": NODEGROUP_NAME,
        "clusterName": CLUSTER_NAME,
        "status": "ACTIVE",
        "capacityType": "ON_DEMAND",
        "scalingConfig": {"minSize": 1, "maxSize": 3, "desiredSize": 2},
        "instanceTypes": ["t3.medium"],
        "amiType": "AL2_x86_64",
        "nodeRole": ROLE_ARN,
        "subnets": SUBNET_IDS,
    }
    d.update(overrides)
    return d


def _addon_dict(**overrides: object) -> dict:
    d: dict = {
        "addonName": ADDON_NAME,
        "clusterName": CLUSTER_NAME,
        "status": "ACTIVE",
        "addonVersion": "v1.12.0",
        "serviceAccountRoleArn": ROLE_ARN,
    }
    d.update(overrides)
    return d


def _fargate_dict(**overrides: object) -> dict:
    d: dict = {
        "fargateProfileName": FARGATE_PROFILE_NAME,
        "clusterName": CLUSTER_NAME,
        "status": "ACTIVE",
        "podExecutionRoleArn": ROLE_ARN,
        "subnets": SUBNET_IDS,
        "selectors": [{"namespace": "default"}],
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_cluster_result_model(self):
        c = ClusterResult(
            name="c", arn="arn:...", status="ACTIVE", role_arn=ROLE_ARN
        )
        assert c.name == "c"
        assert c.endpoint is None
        assert c.tags == {}

    def test_nodegroup_result_model(self):
        ng = NodegroupResult(
            nodegroup_name="ng", cluster_name="c", status="ACTIVE"
        )
        assert ng.capacity_type is None
        assert ng.instance_types == []

    def test_addon_result_model(self):
        a = AddonResult(
            addon_name="vpc-cni", cluster_name="c", status="ACTIVE"
        )
        assert a.addon_version is None
        assert a.service_account_role_arn is None

    def test_fargate_profile_result_model(self):
        fp = FargateProfileResult(
            fargate_profile_name="fp", cluster_name="c", status="ACTIVE"
        )
        assert fp.subnets == []
        assert fp.selectors == []

    def test_models_are_frozen(self):
        c = ClusterResult(
            name="c", arn="arn:...", status="ACTIVE", role_arn=ROLE_ARN
        )
        with pytest.raises(Exception):
            c.name = "new"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_cluster_full(self):
        result = _parse_cluster(_cluster_dict())
        assert result.name == CLUSTER_NAME
        assert result.certificate_authority == "LS0tLS1C..."
        assert result.version == "1.28"
        assert result.tags == {"env": "test"}

    def test_parse_cluster_minimal(self):
        result = _parse_cluster({
            "name": "min",
            "arn": "arn:...",
            "status": "CREATING",
            "roleArn": ROLE_ARN,
        })
        assert result.endpoint is None
        assert result.certificate_authority is None
        assert result.created_at is None

    def test_parse_cluster_empty_cert_authority(self):
        data = _cluster_dict()
        data["certificateAuthority"] = {}
        result = _parse_cluster(data)
        assert result.certificate_authority is None

    def test_parse_cluster_no_cert_authority(self):
        data = _cluster_dict()
        del data["certificateAuthority"]
        result = _parse_cluster(data)
        assert result.certificate_authority is None

    def test_parse_cluster_extra_fields(self):
        data = _cluster_dict()
        data["someExtraField"] = "hello"
        result = _parse_cluster(data)
        assert result.extra["someExtraField"] == "hello"

    def test_parse_nodegroup_full(self):
        result = _parse_nodegroup(_nodegroup_dict())
        assert result.nodegroup_name == NODEGROUP_NAME
        assert result.capacity_type == "ON_DEMAND"
        assert result.instance_types == ["t3.medium"]

    def test_parse_nodegroup_extra_fields(self):
        data = _nodegroup_dict()
        data["diskSize"] = 50
        result = _parse_nodegroup(data)
        assert result.extra["diskSize"] == 50

    def test_parse_addon_full(self):
        result = _parse_addon(_addon_dict())
        assert result.addon_name == ADDON_NAME
        assert result.addon_version == "v1.12.0"

    def test_parse_addon_extra_fields(self):
        data = _addon_dict()
        data["health"] = {"issues": []}
        result = _parse_addon(data)
        assert result.extra["health"] == {"issues": []}

    def test_parse_fargate_profile_full(self):
        result = _parse_fargate_profile(_fargate_dict())
        assert result.fargate_profile_name == FARGATE_PROFILE_NAME
        assert result.selectors == [{"namespace": "default"}]

    def test_parse_fargate_profile_extra_fields(self):
        data = _fargate_dict()
        data["fargateProfileArn"] = "arn:..."
        result = _parse_fargate_profile(data)
        assert result.extra["fargateProfileArn"] == "arn:..."


# ---------------------------------------------------------------------------
# Cluster operations (moto-backed where possible)
# ---------------------------------------------------------------------------


class TestCreateCluster:
    def test_create_cluster_basic(self):
        result = create_cluster(
            CLUSTER_NAME,
            role_arn=ROLE_ARN,
            subnet_ids=SUBNET_IDS,
            region_name=REGION,
        )
        assert isinstance(result, ClusterResult)
        assert result.name == CLUSTER_NAME

    def test_create_cluster_with_all_options(self):
        result = create_cluster(
            "full-cluster",
            role_arn=ROLE_ARN,
            subnet_ids=SUBNET_IDS,
            security_group_ids=["sg-12345"],
            version="1.28",
            tags={"env": "test"},
            region_name=REGION,
        )
        assert result.name == "full-cluster"

    def test_create_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cluster.side_effect = ClientError(
            {"Error": {"Code": "ResourceInUseException", "Message": "exists"}},
            "CreateCluster",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_cluster failed"):
            create_cluster(
                CLUSTER_NAME,
                role_arn=ROLE_ARN,
                subnet_ids=SUBNET_IDS,
                region_name=REGION,
            )


class TestDescribeCluster:
    def test_describe_cluster(self):
        create_cluster(
            CLUSTER_NAME,
            role_arn=ROLE_ARN,
            subnet_ids=SUBNET_IDS,
            region_name=REGION,
        )
        result = describe_cluster(CLUSTER_NAME, region_name=REGION)
        assert isinstance(result, ClusterResult)
        assert result.name == CLUSTER_NAME

    def test_describe_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DescribeCluster",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_cluster failed"):
            describe_cluster("missing", region_name=REGION)


class TestListClusters:
    def test_list_clusters_empty(self):
        result = list_clusters(region_name=REGION)
        assert result == []

    def test_list_clusters_with_clusters(self):
        create_cluster(
            "c1", role_arn=ROLE_ARN, subnet_ids=SUBNET_IDS, region_name=REGION
        )
        create_cluster(
            "c2", role_arn=ROLE_ARN, subnet_ids=SUBNET_IDS, region_name=REGION
        )
        result = list_clusters(region_name=REGION)
        assert "c1" in result
        assert "c2" in result

    def test_list_clusters_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}},
            "ListClusters",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_clusters failed"):
            list_clusters(region_name=REGION)


class TestDeleteCluster:
    def test_delete_cluster(self):
        create_cluster(
            CLUSTER_NAME,
            role_arn=ROLE_ARN,
            subnet_ids=SUBNET_IDS,
            region_name=REGION,
        )
        result = delete_cluster(CLUSTER_NAME, region_name=REGION)
        assert isinstance(result, ClusterResult)
        assert result.name == CLUSTER_NAME

    def test_delete_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_cluster.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DeleteCluster",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_cluster failed"):
            delete_cluster("missing", region_name=REGION)


class TestUpdateClusterVersion:
    def test_update_cluster_version(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_version.return_value = {
            "update": {"id": "u1", "status": "InProgress"}
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_cluster_version(
            CLUSTER_NAME, version="1.29", region_name=REGION
        )
        assert result["id"] == "u1"

    def test_update_cluster_version_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_version.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterException", "Message": "bad"}},
            "UpdateClusterVersion",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="update_cluster_version failed"):
            update_cluster_version(
                CLUSTER_NAME, version="1.29", region_name=REGION
            )


class TestUpdateClusterConfig:
    def test_update_cluster_config_with_vpc(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_config.return_value = {
            "update": {"id": "u2", "status": "InProgress"}
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_cluster_config(
            CLUSTER_NAME,
            resources_vpc_config={"endpointPublicAccess": True},
            region_name=REGION,
        )
        assert result["id"] == "u2"

    def test_update_cluster_config_with_logging(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_config.return_value = {
            "update": {"id": "u3", "status": "InProgress"}
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_cluster_config(
            CLUSTER_NAME,
            logging={"clusterLogging": [{"types": ["api"], "enabled": True}]},
            region_name=REGION,
        )
        assert result["id"] == "u3"

    def test_update_cluster_config_minimal(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_config.return_value = {"update": {}}
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_cluster_config(CLUSTER_NAME, region_name=REGION)
        assert result == {}

    def test_update_cluster_config_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_config.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterException", "Message": "bad"}},
            "UpdateClusterConfig",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="update_cluster_config failed"):
            update_cluster_config(CLUSTER_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# Nodegroup operations (mock-based)
# ---------------------------------------------------------------------------


class TestCreateNodegroup:
    def test_create_nodegroup_basic(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_nodegroup.return_value = {
            "nodegroup": _nodegroup_dict()
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_nodegroup(
            CLUSTER_NAME,
            NODEGROUP_NAME,
            node_role=ROLE_ARN,
            subnets=SUBNET_IDS,
            region_name=REGION,
        )
        assert isinstance(result, NodegroupResult)
        assert result.nodegroup_name == NODEGROUP_NAME

    def test_create_nodegroup_all_options(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_nodegroup.return_value = {
            "nodegroup": _nodegroup_dict()
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_nodegroup(
            CLUSTER_NAME,
            NODEGROUP_NAME,
            node_role=ROLE_ARN,
            subnets=SUBNET_IDS,
            scaling_config={"minSize": 1, "maxSize": 5, "desiredSize": 3},
            instance_types=["t3.large"],
            ami_type="AL2_x86_64",
            capacity_type="ON_DEMAND",
            tags={"env": "test"},
            region_name=REGION,
        )
        assert result.nodegroup_name == NODEGROUP_NAME

    def test_create_nodegroup_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_nodegroup.side_effect = ClientError(
            {"Error": {"Code": "ResourceInUseException", "Message": "exists"}},
            "CreateNodegroup",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_nodegroup failed"):
            create_nodegroup(
                CLUSTER_NAME,
                NODEGROUP_NAME,
                node_role=ROLE_ARN,
                subnets=SUBNET_IDS,
                region_name=REGION,
            )


class TestDescribeNodegroup:
    def test_describe_nodegroup(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_nodegroup.return_value = {
            "nodegroup": _nodegroup_dict()
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_nodegroup(
            CLUSTER_NAME, NODEGROUP_NAME, region_name=REGION
        )
        assert result.nodegroup_name == NODEGROUP_NAME

    def test_describe_nodegroup_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_nodegroup.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DescribeNodegroup",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_nodegroup failed"):
            describe_nodegroup(
                CLUSTER_NAME, "missing", region_name=REGION
            )


class TestListNodegroups:
    def test_list_nodegroups(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"nodegroups": ["ng-1", "ng-2"]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_nodegroups(CLUSTER_NAME, region_name=REGION)
        assert result == ["ng-1", "ng-2"]

    def test_list_nodegroups_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}},
            "ListNodegroups",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_nodegroups failed"):
            list_nodegroups(CLUSTER_NAME, region_name=REGION)


class TestDeleteNodegroup:
    def test_delete_nodegroup(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_nodegroup.return_value = {
            "nodegroup": _nodegroup_dict(status="DELETING")
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = delete_nodegroup(
            CLUSTER_NAME, NODEGROUP_NAME, region_name=REGION
        )
        assert result.status == "DELETING"

    def test_delete_nodegroup_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_nodegroup.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DeleteNodegroup",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_nodegroup failed"):
            delete_nodegroup(
                CLUSTER_NAME, "missing", region_name=REGION
            )


class TestUpdateNodegroupConfig:
    def test_update_nodegroup_config_with_scaling(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_nodegroup_config.return_value = {
            "update": {"id": "u1", "status": "InProgress"}
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_nodegroup_config(
            CLUSTER_NAME,
            NODEGROUP_NAME,
            scaling_config={"minSize": 2, "maxSize": 6, "desiredSize": 4},
            region_name=REGION,
        )
        assert result["id"] == "u1"

    def test_update_nodegroup_config_minimal(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_nodegroup_config.return_value = {"update": {}}
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_nodegroup_config(
            CLUSTER_NAME, NODEGROUP_NAME, region_name=REGION
        )
        assert result == {}

    def test_update_nodegroup_config_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_nodegroup_config.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterException", "Message": "bad"}},
            "UpdateNodegroupConfig",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="update_nodegroup_config failed"
        ):
            update_nodegroup_config(
                CLUSTER_NAME, NODEGROUP_NAME, region_name=REGION
            )


# ---------------------------------------------------------------------------
# Fargate profile operations (mock-based)
# ---------------------------------------------------------------------------


class TestCreateFargateProfile:
    def test_create_fargate_profile_basic(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_fargate_profile.return_value = {
            "fargateProfile": _fargate_dict()
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_fargate_profile(
            CLUSTER_NAME,
            FARGATE_PROFILE_NAME,
            pod_execution_role_arn=ROLE_ARN,
            selectors=[{"namespace": "default"}],
            region_name=REGION,
        )
        assert isinstance(result, FargateProfileResult)
        assert result.fargate_profile_name == FARGATE_PROFILE_NAME

    def test_create_fargate_profile_all_options(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_fargate_profile.return_value = {
            "fargateProfile": _fargate_dict()
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_fargate_profile(
            CLUSTER_NAME,
            FARGATE_PROFILE_NAME,
            pod_execution_role_arn=ROLE_ARN,
            subnets=SUBNET_IDS,
            selectors=[{"namespace": "kube-system"}],
            tags={"env": "prod"},
            region_name=REGION,
        )
        assert result.fargate_profile_name == FARGATE_PROFILE_NAME

    def test_create_fargate_profile_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_fargate_profile.side_effect = ClientError(
            {"Error": {"Code": "ResourceInUseException", "Message": "exists"}},
            "CreateFargateProfile",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="create_fargate_profile failed"
        ):
            create_fargate_profile(
                CLUSTER_NAME,
                FARGATE_PROFILE_NAME,
                pod_execution_role_arn=ROLE_ARN,
                selectors=[{"namespace": "default"}],
                region_name=REGION,
            )


class TestDescribeFargateProfile:
    def test_describe_fargate_profile(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_fargate_profile.return_value = {
            "fargateProfile": _fargate_dict()
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_fargate_profile(
            CLUSTER_NAME, FARGATE_PROFILE_NAME, region_name=REGION
        )
        assert result.fargate_profile_name == FARGATE_PROFILE_NAME

    def test_describe_fargate_profile_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_fargate_profile.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DescribeFargateProfile",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="describe_fargate_profile failed"
        ):
            describe_fargate_profile(
                CLUSTER_NAME, "missing", region_name=REGION
            )


class TestListFargateProfiles:
    def test_list_fargate_profiles(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"fargateProfileNames": ["fp-1", "fp-2"]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_fargate_profiles(CLUSTER_NAME, region_name=REGION)
        assert result == ["fp-1", "fp-2"]

    def test_list_fargate_profiles_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}},
            "ListFargateProfiles",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_fargate_profiles failed"):
            list_fargate_profiles(CLUSTER_NAME, region_name=REGION)


class TestDeleteFargateProfile:
    def test_delete_fargate_profile(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_fargate_profile.return_value = {
            "fargateProfile": _fargate_dict(status="DELETING")
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = delete_fargate_profile(
            CLUSTER_NAME, FARGATE_PROFILE_NAME, region_name=REGION
        )
        assert result.status == "DELETING"

    def test_delete_fargate_profile_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_fargate_profile.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DeleteFargateProfile",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(
            RuntimeError, match="delete_fargate_profile failed"
        ):
            delete_fargate_profile(
                CLUSTER_NAME, "missing", region_name=REGION
            )


# ---------------------------------------------------------------------------
# Addon operations (mock-based)
# ---------------------------------------------------------------------------


class TestCreateAddon:
    def test_create_addon_basic(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_addon.return_value = {"addon": _addon_dict()}
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_addon(
            CLUSTER_NAME, ADDON_NAME, region_name=REGION
        )
        assert isinstance(result, AddonResult)
        assert result.addon_name == ADDON_NAME

    def test_create_addon_all_options(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_addon.return_value = {"addon": _addon_dict()}
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = create_addon(
            CLUSTER_NAME,
            ADDON_NAME,
            addon_version="v1.12.0",
            service_account_role_arn=ROLE_ARN,
            tags={"env": "test"},
            region_name=REGION,
        )
        assert result.addon_name == ADDON_NAME

    def test_create_addon_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_addon.side_effect = ClientError(
            {"Error": {"Code": "ResourceInUseException", "Message": "exists"}},
            "CreateAddon",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="create_addon failed"):
            create_addon(CLUSTER_NAME, ADDON_NAME, region_name=REGION)


class TestDescribeAddon:
    def test_describe_addon(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_addon.return_value = {"addon": _addon_dict()}
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = describe_addon(
            CLUSTER_NAME, ADDON_NAME, region_name=REGION
        )
        assert result.addon_name == ADDON_NAME

    def test_describe_addon_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_addon.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DescribeAddon",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="describe_addon failed"):
            describe_addon(CLUSTER_NAME, "missing", region_name=REGION)


class TestListAddons:
    def test_list_addons(self, monkeypatch):
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"addons": ["vpc-cni", "coredns"]}
        ]
        mock_client = MagicMock()
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = list_addons(CLUSTER_NAME, region_name=REGION)
        assert result == ["vpc-cni", "coredns"]

    def test_list_addons_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}},
            "ListAddons",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="list_addons failed"):
            list_addons(CLUSTER_NAME, region_name=REGION)


class TestDeleteAddon:
    def test_delete_addon(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_addon.return_value = {
            "addon": _addon_dict(status="DELETING")
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = delete_addon(CLUSTER_NAME, ADDON_NAME, region_name=REGION)
        assert result.status == "DELETING"

    def test_delete_addon_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_addon.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "nope"}},
            "DeleteAddon",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="delete_addon failed"):
            delete_addon(CLUSTER_NAME, "missing", region_name=REGION)


class TestUpdateAddon:
    def test_update_addon_with_version(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_addon.return_value = {
            "update": {"id": "u1", "status": "InProgress"}
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_addon(
            CLUSTER_NAME,
            ADDON_NAME,
            addon_version="v1.13.0",
            region_name=REGION,
        )
        assert result["id"] == "u1"

    def test_update_addon_with_service_account_role(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_addon.return_value = {
            "update": {"id": "u2", "status": "InProgress"}
        }
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_addon(
            CLUSTER_NAME,
            ADDON_NAME,
            service_account_role_arn=ROLE_ARN,
            region_name=REGION,
        )
        assert result["id"] == "u2"

    def test_update_addon_minimal(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_addon.return_value = {"update": {}}
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        result = update_addon(CLUSTER_NAME, ADDON_NAME, region_name=REGION)
        assert result == {}

    def test_update_addon_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_addon.side_effect = ClientError(
            {"Error": {"Code": "InvalidParameterException", "Message": "bad"}},
            "UpdateAddon",
        )
        monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
        with pytest.raises(RuntimeError, match="update_addon failed"):
            update_addon(CLUSTER_NAME, ADDON_NAME, region_name=REGION)


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


class TestWaitForCluster:
    def test_wait_for_cluster_already_active(self, monkeypatch):
        monkeypatch.setattr(
            eks_mod,
            "describe_cluster",
            lambda name, **kw: ClusterResult(
                name=name,
                arn="arn:...",
                status="ACTIVE",
                role_arn=ROLE_ARN,
            ),
        )
        result = wait_for_cluster(
            CLUSTER_NAME, timeout=5.0, poll_interval=0.01, region_name=REGION
        )
        assert result.status == "ACTIVE"

    def test_wait_for_cluster_transitions(self, monkeypatch):
        import time as _t

        monkeypatch.setattr(_t, "sleep", lambda s: None)
        call_count = {"n": 0}

        def fake_describe(name, **kw):
            call_count["n"] += 1
            status = "CREATING" if call_count["n"] < 2 else "ACTIVE"
            return ClusterResult(
                name=name, arn="arn:...", status=status, role_arn=ROLE_ARN
            )

        monkeypatch.setattr(eks_mod, "describe_cluster", fake_describe)
        result = wait_for_cluster(
            CLUSTER_NAME,
            timeout=10.0,
            poll_interval=0.001,
            region_name=REGION,
        )
        assert result.status == "ACTIVE"

    def test_wait_for_cluster_timeout(self, monkeypatch):
        monkeypatch.setattr(
            eks_mod,
            "describe_cluster",
            lambda name, **kw: ClusterResult(
                name=name,
                arn="arn:...",
                status="CREATING",
                role_arn=ROLE_ARN,
            ),
        )
        with pytest.raises(TimeoutError, match="did not reach status"):
            wait_for_cluster(
                CLUSTER_NAME,
                timeout=0.0,
                poll_interval=0.0,
                region_name=REGION,
            )


class TestWaitForNodegroup:
    def test_wait_for_nodegroup_already_active(self, monkeypatch):
        monkeypatch.setattr(
            eks_mod,
            "describe_nodegroup",
            lambda cn, nn, **kw: NodegroupResult(
                nodegroup_name=nn, cluster_name=cn, status="ACTIVE"
            ),
        )
        result = wait_for_nodegroup(
            CLUSTER_NAME,
            NODEGROUP_NAME,
            timeout=5.0,
            poll_interval=0.01,
            region_name=REGION,
        )
        assert result.status == "ACTIVE"

    def test_wait_for_nodegroup_transitions(self, monkeypatch):
        import time as _t

        monkeypatch.setattr(_t, "sleep", lambda s: None)
        call_count = {"n": 0}

        def fake_describe(cn, nn, **kw):
            call_count["n"] += 1
            status = "CREATING" if call_count["n"] < 2 else "ACTIVE"
            return NodegroupResult(
                nodegroup_name=nn, cluster_name=cn, status=status
            )

        monkeypatch.setattr(eks_mod, "describe_nodegroup", fake_describe)
        result = wait_for_nodegroup(
            CLUSTER_NAME,
            NODEGROUP_NAME,
            timeout=10.0,
            poll_interval=0.001,
            region_name=REGION,
        )
        assert result.status == "ACTIVE"

    def test_wait_for_nodegroup_timeout(self, monkeypatch):
        monkeypatch.setattr(
            eks_mod,
            "describe_nodegroup",
            lambda cn, nn, **kw: NodegroupResult(
                nodegroup_name=nn, cluster_name=cn, status="CREATING"
            ),
        )
        with pytest.raises(TimeoutError, match="did not reach status"):
            wait_for_nodegroup(
                CLUSTER_NAME,
                NODEGROUP_NAME,
                timeout=0.0,
                poll_interval=0.0,
                region_name=REGION,
            )


def test_associate_access_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_access_policy.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    associate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", {}, region_name=REGION)
    mock_client.associate_access_policy.assert_called_once()


def test_associate_access_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_access_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_access_policy",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate access policy"):
        associate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", {}, region_name=REGION)


def test_associate_encryption_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_encryption_config.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    associate_encryption_config("test-cluster_name", [], region_name=REGION)
    mock_client.associate_encryption_config.assert_called_once()


def test_associate_encryption_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_encryption_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_encryption_config",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate encryption config"):
        associate_encryption_config("test-cluster_name", [], region_name=REGION)


def test_associate_identity_provider_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_identity_provider_config.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    associate_identity_provider_config("test-cluster_name", {}, region_name=REGION)
    mock_client.associate_identity_provider_config.assert_called_once()


def test_associate_identity_provider_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.associate_identity_provider_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "associate_identity_provider_config",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to associate identity provider config"):
        associate_identity_provider_config("test-cluster_name", {}, region_name=REGION)


def test_create_access_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_entry.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    create_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)
    mock_client.create_access_entry.assert_called_once()


def test_create_access_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_access_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_access_entry",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create access entry"):
        create_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)


def test_create_eks_anywhere_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_eks_anywhere_subscription.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    create_eks_anywhere_subscription("test-name", {}, region_name=REGION)
    mock_client.create_eks_anywhere_subscription.assert_called_once()


def test_create_eks_anywhere_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_eks_anywhere_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_eks_anywhere_subscription",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create eks anywhere subscription"):
        create_eks_anywhere_subscription("test-name", {}, region_name=REGION)


def test_create_pod_identity_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_pod_identity_association.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    create_pod_identity_association("test-cluster_name", "test-namespace", "test-service_account", "test-role_arn", region_name=REGION)
    mock_client.create_pod_identity_association.assert_called_once()


def test_create_pod_identity_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_pod_identity_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_pod_identity_association",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create pod identity association"):
        create_pod_identity_association("test-cluster_name", "test-namespace", "test-service_account", "test-role_arn", region_name=REGION)


def test_delete_access_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_access_entry.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    delete_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)
    mock_client.delete_access_entry.assert_called_once()


def test_delete_access_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_access_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_access_entry",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete access entry"):
        delete_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)


def test_delete_eks_anywhere_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_eks_anywhere_subscription.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    delete_eks_anywhere_subscription("test-id", region_name=REGION)
    mock_client.delete_eks_anywhere_subscription.assert_called_once()


def test_delete_eks_anywhere_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_eks_anywhere_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_eks_anywhere_subscription",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete eks anywhere subscription"):
        delete_eks_anywhere_subscription("test-id", region_name=REGION)


def test_delete_pod_identity_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_pod_identity_association.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    delete_pod_identity_association("test-cluster_name", "test-association_id", region_name=REGION)
    mock_client.delete_pod_identity_association.assert_called_once()


def test_delete_pod_identity_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_pod_identity_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_pod_identity_association",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete pod identity association"):
        delete_pod_identity_association("test-cluster_name", "test-association_id", region_name=REGION)


def test_deregister_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_cluster.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    deregister_cluster("test-name", region_name=REGION)
    mock_client.deregister_cluster.assert_called_once()


def test_deregister_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.deregister_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "deregister_cluster",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to deregister cluster"):
        deregister_cluster("test-name", region_name=REGION)


def test_describe_access_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_access_entry.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)
    mock_client.describe_access_entry.assert_called_once()


def test_describe_access_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_access_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_access_entry",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe access entry"):
        describe_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)


def test_describe_addon_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addon_configuration.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_addon_configuration("test-addon_name", "test-addon_version", region_name=REGION)
    mock_client.describe_addon_configuration.assert_called_once()


def test_describe_addon_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addon_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_addon_configuration",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe addon configuration"):
        describe_addon_configuration("test-addon_name", "test-addon_version", region_name=REGION)


def test_describe_addon_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addon_versions.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_addon_versions(region_name=REGION)
    mock_client.describe_addon_versions.assert_called_once()


def test_describe_addon_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_addon_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_addon_versions",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe addon versions"):
        describe_addon_versions(region_name=REGION)


def test_describe_cluster_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_versions.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_cluster_versions(region_name=REGION)
    mock_client.describe_cluster_versions.assert_called_once()


def test_describe_cluster_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_versions",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster versions"):
        describe_cluster_versions(region_name=REGION)


def test_describe_eks_anywhere_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_eks_anywhere_subscription.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_eks_anywhere_subscription("test-id", region_name=REGION)
    mock_client.describe_eks_anywhere_subscription.assert_called_once()


def test_describe_eks_anywhere_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_eks_anywhere_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_eks_anywhere_subscription",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe eks anywhere subscription"):
        describe_eks_anywhere_subscription("test-id", region_name=REGION)


def test_describe_identity_provider_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_identity_provider_config.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_identity_provider_config("test-cluster_name", {}, region_name=REGION)
    mock_client.describe_identity_provider_config.assert_called_once()


def test_describe_identity_provider_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_identity_provider_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_identity_provider_config",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe identity provider config"):
        describe_identity_provider_config("test-cluster_name", {}, region_name=REGION)


def test_describe_insight(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_insight.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_insight("test-cluster_name", "test-id", region_name=REGION)
    mock_client.describe_insight.assert_called_once()


def test_describe_insight_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_insight.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_insight",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe insight"):
        describe_insight("test-cluster_name", "test-id", region_name=REGION)


def test_describe_insights_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_insights_refresh.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_insights_refresh("test-cluster_name", region_name=REGION)
    mock_client.describe_insights_refresh.assert_called_once()


def test_describe_insights_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_insights_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_insights_refresh",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe insights refresh"):
        describe_insights_refresh("test-cluster_name", region_name=REGION)


def test_describe_pod_identity_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pod_identity_association.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_pod_identity_association("test-cluster_name", "test-association_id", region_name=REGION)
    mock_client.describe_pod_identity_association.assert_called_once()


def test_describe_pod_identity_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_pod_identity_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_pod_identity_association",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe pod identity association"):
        describe_pod_identity_association("test-cluster_name", "test-association_id", region_name=REGION)


def test_describe_update(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_update.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    describe_update("test-name", "test-update_id", region_name=REGION)
    mock_client.describe_update.assert_called_once()


def test_describe_update_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_update.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_update",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe update"):
        describe_update("test-name", "test-update_id", region_name=REGION)


def test_disassociate_access_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_access_policy.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    disassociate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", region_name=REGION)
    mock_client.disassociate_access_policy.assert_called_once()


def test_disassociate_access_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_access_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_access_policy",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate access policy"):
        disassociate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", region_name=REGION)


def test_disassociate_identity_provider_config(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_identity_provider_config.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    disassociate_identity_provider_config("test-cluster_name", {}, region_name=REGION)
    mock_client.disassociate_identity_provider_config.assert_called_once()


def test_disassociate_identity_provider_config_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.disassociate_identity_provider_config.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "disassociate_identity_provider_config",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to disassociate identity provider config"):
        disassociate_identity_provider_config("test-cluster_name", {}, region_name=REGION)


def test_list_access_entries(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_entries.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_access_entries("test-cluster_name", region_name=REGION)
    mock_client.list_access_entries.assert_called_once()


def test_list_access_entries_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_entries.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_entries",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list access entries"):
        list_access_entries("test-cluster_name", region_name=REGION)


def test_list_access_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_policies.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_access_policies(region_name=REGION)
    mock_client.list_access_policies.assert_called_once()


def test_list_access_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_access_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_access_policies",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list access policies"):
        list_access_policies(region_name=REGION)


def test_list_associated_access_policies(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_associated_access_policies.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_associated_access_policies("test-cluster_name", "test-principal_arn", region_name=REGION)
    mock_client.list_associated_access_policies.assert_called_once()


def test_list_associated_access_policies_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_associated_access_policies.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_associated_access_policies",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list associated access policies"):
        list_associated_access_policies("test-cluster_name", "test-principal_arn", region_name=REGION)


def test_list_eks_anywhere_subscriptions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_eks_anywhere_subscriptions.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_eks_anywhere_subscriptions(region_name=REGION)
    mock_client.list_eks_anywhere_subscriptions.assert_called_once()


def test_list_eks_anywhere_subscriptions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_eks_anywhere_subscriptions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_eks_anywhere_subscriptions",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list eks anywhere subscriptions"):
        list_eks_anywhere_subscriptions(region_name=REGION)


def test_list_identity_provider_configs(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_provider_configs.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_identity_provider_configs("test-cluster_name", region_name=REGION)
    mock_client.list_identity_provider_configs.assert_called_once()


def test_list_identity_provider_configs_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_identity_provider_configs.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_identity_provider_configs",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list identity provider configs"):
        list_identity_provider_configs("test-cluster_name", region_name=REGION)


def test_list_insights(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_insights.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_insights("test-cluster_name", region_name=REGION)
    mock_client.list_insights.assert_called_once()


def test_list_insights_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_insights.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_insights",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list insights"):
        list_insights("test-cluster_name", region_name=REGION)


def test_list_pod_identity_associations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_pod_identity_associations.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_pod_identity_associations("test-cluster_name", region_name=REGION)
    mock_client.list_pod_identity_associations.assert_called_once()


def test_list_pod_identity_associations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_pod_identity_associations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_pod_identity_associations",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list pod identity associations"):
        list_pod_identity_associations("test-cluster_name", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_updates(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_updates.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    list_updates("test-name", region_name=REGION)
    mock_client.list_updates.assert_called_once()


def test_list_updates_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_updates.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_updates",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list updates"):
        list_updates("test-name", region_name=REGION)


def test_register_cluster(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_cluster.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    register_cluster("test-name", {}, region_name=REGION)
    mock_client.register_cluster.assert_called_once()


def test_register_cluster_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.register_cluster.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "register_cluster",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to register cluster"):
        register_cluster("test-name", {}, region_name=REGION)


def test_start_insights_refresh(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_insights_refresh.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    start_insights_refresh("test-cluster_name", region_name=REGION)
    mock_client.start_insights_refresh.assert_called_once()


def test_start_insights_refresh_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.start_insights_refresh.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "start_insights_refresh",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to start insights refresh"):
        start_insights_refresh("test-cluster_name", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_access_entry(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_access_entry.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    update_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)
    mock_client.update_access_entry.assert_called_once()


def test_update_access_entry_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_access_entry.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_access_entry",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update access entry"):
        update_access_entry("test-cluster_name", "test-principal_arn", region_name=REGION)


def test_update_eks_anywhere_subscription(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_eks_anywhere_subscription.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    update_eks_anywhere_subscription("test-id", True, region_name=REGION)
    mock_client.update_eks_anywhere_subscription.assert_called_once()


def test_update_eks_anywhere_subscription_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_eks_anywhere_subscription.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_eks_anywhere_subscription",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update eks anywhere subscription"):
        update_eks_anywhere_subscription("test-id", True, region_name=REGION)


def test_update_nodegroup_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_nodegroup_version.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    update_nodegroup_version("test-cluster_name", "test-nodegroup_name", region_name=REGION)
    mock_client.update_nodegroup_version.assert_called_once()


def test_update_nodegroup_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_nodegroup_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_nodegroup_version",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update nodegroup version"):
        update_nodegroup_version("test-cluster_name", "test-nodegroup_name", region_name=REGION)


def test_update_pod_identity_association(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_pod_identity_association.return_value = {}
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    update_pod_identity_association("test-cluster_name", "test-association_id", region_name=REGION)
    mock_client.update_pod_identity_association.assert_called_once()


def test_update_pod_identity_association_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_pod_identity_association.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_pod_identity_association",
    )
    monkeypatch.setattr(eks_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update pod identity association"):
        update_pod_identity_association("test-cluster_name", "test-association_id", region_name=REGION)


def test_update_cluster_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_cluster_config
    mock_client = MagicMock()
    mock_client.update_cluster_config.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_cluster_config("test-name", resources_vpc_config={}, logging="test-logging", region_name="us-east-1")
    mock_client.update_cluster_config.assert_called_once()

def test_update_nodegroup_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_nodegroup_config
    mock_client = MagicMock()
    mock_client.update_nodegroup_config.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_nodegroup_config("test-cluster_name", "test-nodegroup_name", scaling_config={}, region_name="us-east-1")
    mock_client.update_nodegroup_config.assert_called_once()

def test_update_addon_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_addon
    mock_client = MagicMock()
    mock_client.update_addon.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_addon("test-cluster_name", "test-addon_name", addon_version="test-addon_version", service_account_role_arn=1, region_name="us-east-1")
    mock_client.update_addon.assert_called_once()

def test_associate_encryption_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import associate_encryption_config
    mock_client = MagicMock()
    mock_client.associate_encryption_config.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    associate_encryption_config("test-cluster_name", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.associate_encryption_config.assert_called_once()

def test_associate_identity_provider_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import associate_identity_provider_config
    mock_client = MagicMock()
    mock_client.associate_identity_provider_config.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    associate_identity_provider_config("test-cluster_name", "test-oidc", tags=[{"Key": "k", "Value": "v"}], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.associate_identity_provider_config.assert_called_once()

def test_create_access_entry_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import create_access_entry
    mock_client = MagicMock()
    mock_client.create_access_entry.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    create_access_entry("test-cluster_name", "test-principal_arn", kubernetes_groups="test-kubernetes_groups", tags=[{"Key": "k", "Value": "v"}], client_request_token="test-client_request_token", username="test-username", type_value="test-type_value", region_name="us-east-1")
    mock_client.create_access_entry.assert_called_once()

def test_create_eks_anywhere_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import create_eks_anywhere_subscription
    mock_client = MagicMock()
    mock_client.create_eks_anywhere_subscription.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    create_eks_anywhere_subscription("test-name", "test-term", license_quantity="test-license_quantity", license_type="test-license_type", auto_renew=True, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_eks_anywhere_subscription.assert_called_once()

def test_create_pod_identity_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import create_pod_identity_association
    mock_client = MagicMock()
    mock_client.create_pod_identity_association.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    create_pod_identity_association("test-cluster_name", "test-namespace", 1, "test-role_arn", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], disable_session_tags=True, target_role_arn="test-target_role_arn", region_name="us-east-1")
    mock_client.create_pod_identity_association.assert_called_once()

def test_describe_addon_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import describe_addon_versions
    mock_client = MagicMock()
    mock_client.describe_addon_versions.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    describe_addon_versions(kubernetes_version="test-kubernetes_version", max_results=1, next_token="test-next_token", addon_name="test-addon_name", types="test-types", publishers=True, owners="test-owners", region_name="us-east-1")
    mock_client.describe_addon_versions.assert_called_once()

def test_describe_cluster_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import describe_cluster_versions
    mock_client = MagicMock()
    mock_client.describe_cluster_versions.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    describe_cluster_versions(cluster_type="test-cluster_type", max_results=1, next_token="test-next_token", default_only="test-default_only", include_all=True, cluster_versions="test-cluster_versions", status="test-status", version_status="test-version_status", region_name="us-east-1")
    mock_client.describe_cluster_versions.assert_called_once()

def test_describe_update_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import describe_update
    mock_client = MagicMock()
    mock_client.describe_update.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    describe_update("test-name", "test-update_id", nodegroup_name="test-nodegroup_name", addon_name="test-addon_name", region_name="us-east-1")
    mock_client.describe_update.assert_called_once()

def test_disassociate_identity_provider_config_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import disassociate_identity_provider_config
    mock_client = MagicMock()
    mock_client.disassociate_identity_provider_config.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    disassociate_identity_provider_config("test-cluster_name", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.disassociate_identity_provider_config.assert_called_once()

def test_list_access_entries_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_access_entries
    mock_client = MagicMock()
    mock_client.list_access_entries.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_access_entries("test-cluster_name", associated_policy_arn="test-associated_policy_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_access_entries.assert_called_once()

def test_list_access_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_access_policies
    mock_client = MagicMock()
    mock_client.list_access_policies.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_access_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_access_policies.assert_called_once()

def test_list_associated_access_policies_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_associated_access_policies
    mock_client = MagicMock()
    mock_client.list_associated_access_policies.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_associated_access_policies("test-cluster_name", "test-principal_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_associated_access_policies.assert_called_once()

def test_list_eks_anywhere_subscriptions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_eks_anywhere_subscriptions
    mock_client = MagicMock()
    mock_client.list_eks_anywhere_subscriptions.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_eks_anywhere_subscriptions(max_results=1, next_token="test-next_token", include_status=True, region_name="us-east-1")
    mock_client.list_eks_anywhere_subscriptions.assert_called_once()

def test_list_identity_provider_configs_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_identity_provider_configs
    mock_client = MagicMock()
    mock_client.list_identity_provider_configs.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_identity_provider_configs("test-cluster_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_identity_provider_configs.assert_called_once()

def test_list_insights_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_insights
    mock_client = MagicMock()
    mock_client.list_insights.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_insights("test-cluster_name", filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_insights.assert_called_once()

def test_list_pod_identity_associations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_pod_identity_associations
    mock_client = MagicMock()
    mock_client.list_pod_identity_associations.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_pod_identity_associations("test-cluster_name", namespace="test-namespace", service_account=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_pod_identity_associations.assert_called_once()

def test_list_updates_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import list_updates
    mock_client = MagicMock()
    mock_client.list_updates.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    list_updates("test-name", nodegroup_name="test-nodegroup_name", addon_name="test-addon_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.list_updates.assert_called_once()

def test_register_cluster_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import register_cluster
    mock_client = MagicMock()
    mock_client.register_cluster.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    register_cluster("test-name", {}, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.register_cluster.assert_called_once()

def test_update_access_entry_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_access_entry
    mock_client = MagicMock()
    mock_client.update_access_entry.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_access_entry("test-cluster_name", "test-principal_arn", kubernetes_groups="test-kubernetes_groups", client_request_token="test-client_request_token", username="test-username", region_name="us-east-1")
    mock_client.update_access_entry.assert_called_once()

def test_update_eks_anywhere_subscription_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_eks_anywhere_subscription
    mock_client = MagicMock()
    mock_client.update_eks_anywhere_subscription.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_eks_anywhere_subscription("test-id", True, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_eks_anywhere_subscription.assert_called_once()

def test_update_nodegroup_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_nodegroup_version
    mock_client = MagicMock()
    mock_client.update_nodegroup_version.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_nodegroup_version("test-cluster_name", "test-nodegroup_name", version="test-version", release_version="test-release_version", launch_template="test-launch_template", force=True, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.update_nodegroup_version.assert_called_once()

def test_update_pod_identity_association_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.eks import update_pod_identity_association
    mock_client = MagicMock()
    mock_client.update_pod_identity_association.return_value = {}
    monkeypatch.setattr("aws_util.eks.get_client", lambda *a, **kw: mock_client)
    update_pod_identity_association("test-cluster_name", "test-association_id", role_arn="test-role_arn", client_request_token="test-client_request_token", disable_session_tags=True, target_role_arn="test-target_role_arn", region_name="us-east-1")
    mock_client.update_pod_identity_association.assert_called_once()
