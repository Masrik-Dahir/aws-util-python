"""Tests for aws_util.aio.eks — 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.eks import (
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
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _cluster_resp(**overrides) -> dict:
    d = {
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


def _nodegroup_resp(**overrides) -> dict:
    d = {
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


def _addon_resp(**overrides) -> dict:
    d = {
        "addonName": ADDON_NAME,
        "clusterName": CLUSTER_NAME,
        "status": "ACTIVE",
        "addonVersion": "v1.12.0",
        "serviceAccountRoleArn": ROLE_ARN,
    }
    d.update(overrides)
    return d


def _fargate_resp(**overrides) -> dict:
    d = {
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
# create_cluster
# ---------------------------------------------------------------------------


async def test_create_cluster_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"cluster": _cluster_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_cluster(
        CLUSTER_NAME,
        role_arn=ROLE_ARN,
        subnet_ids=SUBNET_IDS,
    )
    assert isinstance(result, ClusterResult)
    assert result.name == CLUSTER_NAME


async def test_create_cluster_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"cluster": _cluster_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_cluster(
        CLUSTER_NAME,
        role_arn=ROLE_ARN,
        subnet_ids=SUBNET_IDS,
        security_group_ids=["sg-12345"],
        version="1.28",
        tags={"env": "test"},
    )
    assert result.name == CLUSTER_NAME
    call_kwargs = mock_client.call.call_args[1]
    assert "securityGroupIds" in call_kwargs["resourcesVpcConfig"]
    assert call_kwargs["version"] == "1.28"
    assert call_kwargs["tags"] == {"env": "test"}


async def test_create_cluster_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await create_cluster(
            CLUSTER_NAME, role_arn=ROLE_ARN, subnet_ids=SUBNET_IDS
        )


async def test_create_cluster_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_cluster failed"):
        await create_cluster(
            CLUSTER_NAME, role_arn=ROLE_ARN, subnet_ids=SUBNET_IDS
        )


# ---------------------------------------------------------------------------
# describe_cluster
# ---------------------------------------------------------------------------


async def test_describe_cluster_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"cluster": _cluster_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await describe_cluster(CLUSTER_NAME)
    assert result.name == CLUSTER_NAME


async def test_describe_cluster_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_cluster("missing")


async def test_describe_cluster_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_cluster failed"):
        await describe_cluster("missing")


# ---------------------------------------------------------------------------
# list_clusters
# ---------------------------------------------------------------------------


async def test_list_clusters_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["cluster-1", "cluster-2"]
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await list_clusters()
    assert result == ["cluster-1", "cluster-2"]


async def test_list_clusters_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_clusters()


async def test_list_clusters_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_clusters failed"):
        await list_clusters()


# ---------------------------------------------------------------------------
# delete_cluster
# ---------------------------------------------------------------------------


async def test_delete_cluster_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "cluster": _cluster_resp(status="DELETING")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await delete_cluster(CLUSTER_NAME)
    assert result.status == "DELETING"


async def test_delete_cluster_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_cluster("missing")


async def test_delete_cluster_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_cluster failed"):
        await delete_cluster("missing")


# ---------------------------------------------------------------------------
# update_cluster_version
# ---------------------------------------------------------------------------


async def test_update_cluster_version_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "update": {"id": "u1", "status": "InProgress"}
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_cluster_version(CLUSTER_NAME, version="1.29")
    assert result["id"] == "u1"


async def test_update_cluster_version_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_cluster_version(CLUSTER_NAME, version="1.29")


async def test_update_cluster_version_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_cluster_version failed"):
        await update_cluster_version(CLUSTER_NAME, version="1.29")


# ---------------------------------------------------------------------------
# update_cluster_config
# ---------------------------------------------------------------------------


async def test_update_cluster_config_with_vpc(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "update": {"id": "u2", "status": "InProgress"}
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_cluster_config(
        CLUSTER_NAME,
        resources_vpc_config={"endpointPublicAccess": True},
    )
    assert result["id"] == "u2"
    call_kwargs = mock_client.call.call_args[1]
    assert "resourcesVpcConfig" in call_kwargs


async def test_update_cluster_config_with_logging(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"update": {"id": "u3"}}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_cluster_config(
        CLUSTER_NAME,
        logging={"clusterLogging": []},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "logging" in call_kwargs


async def test_update_cluster_config_minimal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"update": {}}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_cluster_config(CLUSTER_NAME)
    assert result == {}
    call_kwargs = mock_client.call.call_args[1]
    assert "resourcesVpcConfig" not in call_kwargs
    assert "logging" not in call_kwargs


async def test_update_cluster_config_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_cluster_config(CLUSTER_NAME)


async def test_update_cluster_config_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_cluster_config failed"):
        await update_cluster_config(CLUSTER_NAME)


# ---------------------------------------------------------------------------
# create_nodegroup
# ---------------------------------------------------------------------------


async def test_create_nodegroup_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"nodegroup": _nodegroup_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_nodegroup(
        CLUSTER_NAME,
        NODEGROUP_NAME,
        node_role=ROLE_ARN,
        subnets=SUBNET_IDS,
    )
    assert isinstance(result, NodegroupResult)
    assert result.nodegroup_name == NODEGROUP_NAME


async def test_create_nodegroup_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"nodegroup": _nodegroup_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_nodegroup(
        CLUSTER_NAME,
        NODEGROUP_NAME,
        node_role=ROLE_ARN,
        subnets=SUBNET_IDS,
        scaling_config={"minSize": 1, "maxSize": 5, "desiredSize": 3},
        instance_types=["t3.large"],
        ami_type="AL2_x86_64",
        capacity_type="ON_DEMAND",
        tags={"env": "test"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["scalingConfig"]["maxSize"] == 5
    assert call_kwargs["instanceTypes"] == ["t3.large"]
    assert call_kwargs["amiType"] == "AL2_x86_64"
    assert call_kwargs["capacityType"] == "ON_DEMAND"
    assert call_kwargs["tags"] == {"env": "test"}


async def test_create_nodegroup_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await create_nodegroup(
            CLUSTER_NAME, NODEGROUP_NAME, node_role=ROLE_ARN, subnets=SUBNET_IDS
        )


async def test_create_nodegroup_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_nodegroup failed"):
        await create_nodegroup(
            CLUSTER_NAME, NODEGROUP_NAME, node_role=ROLE_ARN, subnets=SUBNET_IDS
        )


# ---------------------------------------------------------------------------
# describe_nodegroup
# ---------------------------------------------------------------------------


async def test_describe_nodegroup_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"nodegroup": _nodegroup_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await describe_nodegroup(CLUSTER_NAME, NODEGROUP_NAME)
    assert result.nodegroup_name == NODEGROUP_NAME


async def test_describe_nodegroup_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_nodegroup(CLUSTER_NAME, "missing")


async def test_describe_nodegroup_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_nodegroup failed"):
        await describe_nodegroup(CLUSTER_NAME, "missing")


# ---------------------------------------------------------------------------
# list_nodegroups
# ---------------------------------------------------------------------------


async def test_list_nodegroups_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["ng-1", "ng-2"]
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await list_nodegroups(CLUSTER_NAME)
    assert result == ["ng-1", "ng-2"]


async def test_list_nodegroups_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_nodegroups(CLUSTER_NAME)


async def test_list_nodegroups_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_nodegroups failed"):
        await list_nodegroups(CLUSTER_NAME)


# ---------------------------------------------------------------------------
# delete_nodegroup
# ---------------------------------------------------------------------------


async def test_delete_nodegroup_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "nodegroup": _nodegroup_resp(status="DELETING")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await delete_nodegroup(CLUSTER_NAME, NODEGROUP_NAME)
    assert result.status == "DELETING"


async def test_delete_nodegroup_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_nodegroup(CLUSTER_NAME, "missing")


async def test_delete_nodegroup_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_nodegroup failed"):
        await delete_nodegroup(CLUSTER_NAME, "missing")


# ---------------------------------------------------------------------------
# update_nodegroup_config
# ---------------------------------------------------------------------------


async def test_update_nodegroup_config_with_scaling(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "update": {"id": "u1", "status": "InProgress"}
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_nodegroup_config(
        CLUSTER_NAME,
        NODEGROUP_NAME,
        scaling_config={"minSize": 2, "maxSize": 6, "desiredSize": 4},
    )
    assert result["id"] == "u1"
    call_kwargs = mock_client.call.call_args[1]
    assert "scalingConfig" in call_kwargs


async def test_update_nodegroup_config_minimal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"update": {}}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_nodegroup_config(CLUSTER_NAME, NODEGROUP_NAME)
    assert result == {}
    call_kwargs = mock_client.call.call_args[1]
    assert "scalingConfig" not in call_kwargs


async def test_update_nodegroup_config_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_nodegroup_config(CLUSTER_NAME, NODEGROUP_NAME)


async def test_update_nodegroup_config_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_nodegroup_config failed"):
        await update_nodegroup_config(CLUSTER_NAME, NODEGROUP_NAME)


# ---------------------------------------------------------------------------
# create_fargate_profile
# ---------------------------------------------------------------------------


async def test_create_fargate_profile_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"fargateProfile": _fargate_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_fargate_profile(
        CLUSTER_NAME,
        FARGATE_PROFILE_NAME,
        pod_execution_role_arn=ROLE_ARN,
        selectors=[{"namespace": "default"}],
    )
    assert isinstance(result, FargateProfileResult)
    assert result.fargate_profile_name == FARGATE_PROFILE_NAME


async def test_create_fargate_profile_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"fargateProfile": _fargate_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_fargate_profile(
        CLUSTER_NAME,
        FARGATE_PROFILE_NAME,
        pod_execution_role_arn=ROLE_ARN,
        subnets=SUBNET_IDS,
        selectors=[{"namespace": "kube-system"}],
        tags={"env": "prod"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["subnets"] == SUBNET_IDS
    assert call_kwargs["tags"] == {"env": "prod"}


async def test_create_fargate_profile_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await create_fargate_profile(
            CLUSTER_NAME,
            FARGATE_PROFILE_NAME,
            pod_execution_role_arn=ROLE_ARN,
            selectors=[{"namespace": "default"}],
        )


async def test_create_fargate_profile_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_fargate_profile failed"):
        await create_fargate_profile(
            CLUSTER_NAME,
            FARGATE_PROFILE_NAME,
            pod_execution_role_arn=ROLE_ARN,
            selectors=[{"namespace": "default"}],
        )


# ---------------------------------------------------------------------------
# describe_fargate_profile
# ---------------------------------------------------------------------------


async def test_describe_fargate_profile_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"fargateProfile": _fargate_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await describe_fargate_profile(
        CLUSTER_NAME, FARGATE_PROFILE_NAME
    )
    assert result.fargate_profile_name == FARGATE_PROFILE_NAME


async def test_describe_fargate_profile_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_fargate_profile(CLUSTER_NAME, "missing")


async def test_describe_fargate_profile_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_fargate_profile failed"):
        await describe_fargate_profile(CLUSTER_NAME, "missing")


# ---------------------------------------------------------------------------
# list_fargate_profiles
# ---------------------------------------------------------------------------


async def test_list_fargate_profiles_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["fp-1", "fp-2"]
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await list_fargate_profiles(CLUSTER_NAME)
    assert result == ["fp-1", "fp-2"]


async def test_list_fargate_profiles_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_fargate_profiles(CLUSTER_NAME)


async def test_list_fargate_profiles_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_fargate_profiles failed"):
        await list_fargate_profiles(CLUSTER_NAME)


# ---------------------------------------------------------------------------
# delete_fargate_profile
# ---------------------------------------------------------------------------


async def test_delete_fargate_profile_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "fargateProfile": _fargate_resp(status="DELETING")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await delete_fargate_profile(CLUSTER_NAME, FARGATE_PROFILE_NAME)
    assert result.status == "DELETING"


async def test_delete_fargate_profile_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_fargate_profile(CLUSTER_NAME, "missing")


async def test_delete_fargate_profile_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_fargate_profile failed"):
        await delete_fargate_profile(CLUSTER_NAME, "missing")


# ---------------------------------------------------------------------------
# create_addon
# ---------------------------------------------------------------------------


async def test_create_addon_basic(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"addon": _addon_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_addon(CLUSTER_NAME, ADDON_NAME)
    assert isinstance(result, AddonResult)
    assert result.addon_name == ADDON_NAME


async def test_create_addon_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"addon": _addon_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await create_addon(
        CLUSTER_NAME,
        ADDON_NAME,
        addon_version="v1.12.0",
        service_account_role_arn=ROLE_ARN,
        tags={"env": "test"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["addonVersion"] == "v1.12.0"
    assert call_kwargs["serviceAccountRoleArn"] == ROLE_ARN
    assert call_kwargs["tags"] == {"env": "test"}


async def test_create_addon_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await create_addon(CLUSTER_NAME, ADDON_NAME)


async def test_create_addon_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_addon failed"):
        await create_addon(CLUSTER_NAME, ADDON_NAME)


# ---------------------------------------------------------------------------
# describe_addon
# ---------------------------------------------------------------------------


async def test_describe_addon_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"addon": _addon_resp()}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await describe_addon(CLUSTER_NAME, ADDON_NAME)
    assert result.addon_name == ADDON_NAME


async def test_describe_addon_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_addon(CLUSTER_NAME, "missing")


async def test_describe_addon_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_addon failed"):
        await describe_addon(CLUSTER_NAME, "missing")


# ---------------------------------------------------------------------------
# list_addons
# ---------------------------------------------------------------------------


async def test_list_addons_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = ["vpc-cni", "coredns"]
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await list_addons(CLUSTER_NAME)
    assert result == ["vpc-cni", "coredns"]


async def test_list_addons_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_addons(CLUSTER_NAME)


async def test_list_addons_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_addons failed"):
        await list_addons(CLUSTER_NAME)


# ---------------------------------------------------------------------------
# delete_addon
# ---------------------------------------------------------------------------


async def test_delete_addon_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "addon": _addon_resp(status="DELETING")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await delete_addon(CLUSTER_NAME, ADDON_NAME)
    assert result.status == "DELETING"


async def test_delete_addon_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_addon(CLUSTER_NAME, "missing")


async def test_delete_addon_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = KeyError("k")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_addon failed"):
        await delete_addon(CLUSTER_NAME, "missing")


# ---------------------------------------------------------------------------
# update_addon
# ---------------------------------------------------------------------------


async def test_update_addon_with_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "update": {"id": "u1", "status": "InProgress"}
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_addon(
        CLUSTER_NAME, ADDON_NAME, addon_version="v1.13.0"
    )
    assert result["id"] == "u1"
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["addonVersion"] == "v1.13.0"


async def test_update_addon_with_service_account_role(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"update": {"id": "u2"}}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_addon(
        CLUSTER_NAME, ADDON_NAME, service_account_role_arn=ROLE_ARN
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["serviceAccountRoleArn"] == ROLE_ARN


async def test_update_addon_minimal(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"update": {}}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await update_addon(CLUSTER_NAME, ADDON_NAME)
    assert result == {}
    call_kwargs = mock_client.call.call_args[1]
    assert "addonVersion" not in call_kwargs
    assert "serviceAccountRoleArn" not in call_kwargs


async def test_update_addon_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_addon(CLUSTER_NAME, ADDON_NAME)


async def test_update_addon_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = OSError("os")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_addon failed"):
        await update_addon(CLUSTER_NAME, ADDON_NAME)


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_cluster_immediate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"cluster": _cluster_resp(status="ACTIVE")}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_cluster(CLUSTER_NAME)
    assert result.status == "ACTIVE"


async def test_wait_for_cluster_after_poll(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"cluster": _cluster_resp(status="CREATING")},
        {"cluster": _cluster_resp(status="ACTIVE")},
    ]
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.eks.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_cluster(
            CLUSTER_NAME, timeout=300, poll_interval=0.01
        )
    assert result.status == "ACTIVE"


async def test_wait_for_cluster_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "cluster": _cluster_resp(status="CREATING")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.eks.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(TimeoutError, match="did not reach status"):
            await wait_for_cluster(
                CLUSTER_NAME, timeout=0.0, poll_interval=0.001
            )


# ---------------------------------------------------------------------------
# wait_for_nodegroup
# ---------------------------------------------------------------------------


async def test_wait_for_nodegroup_immediate(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "nodegroup": _nodegroup_resp(status="ACTIVE")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_nodegroup(CLUSTER_NAME, NODEGROUP_NAME)
    assert result.status == "ACTIVE"


async def test_wait_for_nodegroup_after_poll(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"nodegroup": _nodegroup_resp(status="CREATING")},
        {"nodegroup": _nodegroup_resp(status="ACTIVE")},
    ]
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.eks.asyncio.sleep", new_callable=AsyncMock):
        result = await wait_for_nodegroup(
            CLUSTER_NAME, NODEGROUP_NAME, timeout=300, poll_interval=0.01
        )
    assert result.status == "ACTIVE"


async def test_wait_for_nodegroup_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "nodegroup": _nodegroup_resp(status="CREATING")
    }
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client", _mock_factory(mock_client)
    )
    with patch("aws_util.aio.eks.asyncio.sleep", new_callable=AsyncMock):
        with pytest.raises(TimeoutError, match="did not reach status"):
            await wait_for_nodegroup(
                CLUSTER_NAME, NODEGROUP_NAME, timeout=0.0, poll_interval=0.001
            )


async def test_associate_access_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", {}, )
    mock_client.call.assert_called_once()


async def test_associate_access_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", {}, )


async def test_associate_encryption_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_encryption_config("test-cluster_name", [], )
    mock_client.call.assert_called_once()


async def test_associate_encryption_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_encryption_config("test-cluster_name", [], )


async def test_associate_identity_provider_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await associate_identity_provider_config("test-cluster_name", {}, )
    mock_client.call.assert_called_once()


async def test_associate_identity_provider_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await associate_identity_provider_config("test-cluster_name", {}, )


async def test_create_access_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_access_entry("test-cluster_name", "test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_create_access_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_access_entry("test-cluster_name", "test-principal_arn", )


async def test_create_eks_anywhere_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_eks_anywhere_subscription("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_create_eks_anywhere_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_eks_anywhere_subscription("test-name", {}, )


async def test_create_pod_identity_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_pod_identity_association("test-cluster_name", "test-namespace", "test-service_account", "test-role_arn", )
    mock_client.call.assert_called_once()


async def test_create_pod_identity_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_pod_identity_association("test-cluster_name", "test-namespace", "test-service_account", "test-role_arn", )


async def test_delete_access_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_access_entry("test-cluster_name", "test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_delete_access_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_access_entry("test-cluster_name", "test-principal_arn", )


async def test_delete_eks_anywhere_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_eks_anywhere_subscription("test-id", )
    mock_client.call.assert_called_once()


async def test_delete_eks_anywhere_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_eks_anywhere_subscription("test-id", )


async def test_delete_pod_identity_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_pod_identity_association("test-cluster_name", "test-association_id", )
    mock_client.call.assert_called_once()


async def test_delete_pod_identity_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_pod_identity_association("test-cluster_name", "test-association_id", )


async def test_deregister_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await deregister_cluster("test-name", )
    mock_client.call.assert_called_once()


async def test_deregister_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await deregister_cluster("test-name", )


async def test_describe_access_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_access_entry("test-cluster_name", "test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_describe_access_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_access_entry("test-cluster_name", "test-principal_arn", )


async def test_describe_addon_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_addon_configuration("test-addon_name", "test-addon_version", )
    mock_client.call.assert_called_once()


async def test_describe_addon_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_addon_configuration("test-addon_name", "test-addon_version", )


async def test_describe_addon_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_addon_versions()
    mock_client.call.assert_called_once()


async def test_describe_addon_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_addon_versions()


async def test_describe_cluster_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_versions()
    mock_client.call.assert_called_once()


async def test_describe_cluster_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_versions()


async def test_describe_eks_anywhere_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_eks_anywhere_subscription("test-id", )
    mock_client.call.assert_called_once()


async def test_describe_eks_anywhere_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_eks_anywhere_subscription("test-id", )


async def test_describe_identity_provider_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_identity_provider_config("test-cluster_name", {}, )
    mock_client.call.assert_called_once()


async def test_describe_identity_provider_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_identity_provider_config("test-cluster_name", {}, )


async def test_describe_insight(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_insight("test-cluster_name", "test-id", )
    mock_client.call.assert_called_once()


async def test_describe_insight_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_insight("test-cluster_name", "test-id", )


async def test_describe_insights_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_insights_refresh("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_describe_insights_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_insights_refresh("test-cluster_name", )


async def test_describe_pod_identity_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_pod_identity_association("test-cluster_name", "test-association_id", )
    mock_client.call.assert_called_once()


async def test_describe_pod_identity_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_pod_identity_association("test-cluster_name", "test-association_id", )


async def test_describe_update(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_update("test-name", "test-update_id", )
    mock_client.call.assert_called_once()


async def test_describe_update_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_update("test-name", "test-update_id", )


async def test_disassociate_access_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", )
    mock_client.call.assert_called_once()


async def test_disassociate_access_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_access_policy("test-cluster_name", "test-principal_arn", "test-policy_arn", )


async def test_disassociate_identity_provider_config(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await disassociate_identity_provider_config("test-cluster_name", {}, )
    mock_client.call.assert_called_once()


async def test_disassociate_identity_provider_config_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await disassociate_identity_provider_config("test-cluster_name", {}, )


async def test_list_access_entries(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_entries("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_list_access_entries_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_entries("test-cluster_name", )


async def test_list_access_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_access_policies()
    mock_client.call.assert_called_once()


async def test_list_access_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_access_policies()


async def test_list_associated_access_policies(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_associated_access_policies("test-cluster_name", "test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_list_associated_access_policies_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_associated_access_policies("test-cluster_name", "test-principal_arn", )


async def test_list_eks_anywhere_subscriptions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_eks_anywhere_subscriptions()
    mock_client.call.assert_called_once()


async def test_list_eks_anywhere_subscriptions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_eks_anywhere_subscriptions()


async def test_list_identity_provider_configs(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_identity_provider_configs("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_list_identity_provider_configs_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_identity_provider_configs("test-cluster_name", )


async def test_list_insights(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_insights("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_list_insights_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_insights("test-cluster_name", )


async def test_list_pod_identity_associations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_pod_identity_associations("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_list_pod_identity_associations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_pod_identity_associations("test-cluster_name", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_updates(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_updates("test-name", )
    mock_client.call.assert_called_once()


async def test_list_updates_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_updates("test-name", )


async def test_register_cluster(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await register_cluster("test-name", {}, )
    mock_client.call.assert_called_once()


async def test_register_cluster_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await register_cluster("test-name", {}, )


async def test_start_insights_refresh(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await start_insights_refresh("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_start_insights_refresh_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await start_insights_refresh("test-cluster_name", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_access_entry(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_access_entry("test-cluster_name", "test-principal_arn", )
    mock_client.call.assert_called_once()


async def test_update_access_entry_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_access_entry("test-cluster_name", "test-principal_arn", )


async def test_update_eks_anywhere_subscription(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_eks_anywhere_subscription("test-id", True, )
    mock_client.call.assert_called_once()


async def test_update_eks_anywhere_subscription_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_eks_anywhere_subscription("test-id", True, )


async def test_update_nodegroup_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_nodegroup_version("test-cluster_name", "test-nodegroup_name", )
    mock_client.call.assert_called_once()


async def test_update_nodegroup_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_nodegroup_version("test-cluster_name", "test-nodegroup_name", )


async def test_update_pod_identity_association(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_pod_identity_association("test-cluster_name", "test-association_id", )
    mock_client.call.assert_called_once()


async def test_update_pod_identity_association_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.eks.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_pod_identity_association("test-cluster_name", "test-association_id", )


@pytest.mark.asyncio
async def test_update_cluster_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_cluster_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_cluster_config("test-name", resources_vpc_config={}, logging="test-logging", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_nodegroup_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_nodegroup_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_nodegroup_config("test-cluster_name", "test-nodegroup_name", scaling_config={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_addon_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_addon
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_addon("test-cluster_name", "test-addon_name", addon_version="test-addon_version", service_account_role_arn=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_encryption_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import associate_encryption_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await associate_encryption_config("test-cluster_name", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_associate_identity_provider_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import associate_identity_provider_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await associate_identity_provider_config("test-cluster_name", "test-oidc", tags=[{"Key": "k", "Value": "v"}], client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_access_entry_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import create_access_entry
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await create_access_entry("test-cluster_name", "test-principal_arn", kubernetes_groups="test-kubernetes_groups", tags=[{"Key": "k", "Value": "v"}], client_request_token="test-client_request_token", username="test-username", type_value="test-type_value", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_eks_anywhere_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import create_eks_anywhere_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await create_eks_anywhere_subscription("test-name", "test-term", license_quantity="test-license_quantity", license_type="test-license_type", auto_renew=True, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_pod_identity_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import create_pod_identity_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await create_pod_identity_association("test-cluster_name", "test-namespace", 1, "test-role_arn", client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], disable_session_tags=True, target_role_arn="test-target_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_addon_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import describe_addon_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await describe_addon_versions(kubernetes_version="test-kubernetes_version", max_results=1, next_token="test-next_token", addon_name="test-addon_name", types="test-types", publishers=True, owners="test-owners", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_cluster_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import describe_cluster_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await describe_cluster_versions(cluster_type="test-cluster_type", max_results=1, next_token="test-next_token", default_only="test-default_only", include_all=True, cluster_versions="test-cluster_versions", status="test-status", version_status="test-version_status", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_describe_update_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import describe_update
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await describe_update("test-name", "test-update_id", nodegroup_name="test-nodegroup_name", addon_name="test-addon_name", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_disassociate_identity_provider_config_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import disassociate_identity_provider_config
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await disassociate_identity_provider_config("test-cluster_name", {}, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_entries_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_access_entries
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_access_entries("test-cluster_name", associated_policy_arn="test-associated_policy_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_access_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_access_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_access_policies(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_associated_access_policies_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_associated_access_policies
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_associated_access_policies("test-cluster_name", "test-principal_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_eks_anywhere_subscriptions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_eks_anywhere_subscriptions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_eks_anywhere_subscriptions(max_results=1, next_token="test-next_token", include_status=True, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_identity_provider_configs_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_identity_provider_configs
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_identity_provider_configs("test-cluster_name", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_insights_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_insights
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_insights("test-cluster_name", filter="test-filter", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_pod_identity_associations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_pod_identity_associations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_pod_identity_associations("test-cluster_name", namespace="test-namespace", service_account=1, max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_updates_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import list_updates
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await list_updates("test-name", nodegroup_name="test-nodegroup_name", addon_name="test-addon_name", next_token="test-next_token", max_results=1, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_register_cluster_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import register_cluster
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await register_cluster("test-name", {}, client_request_token="test-client_request_token", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_access_entry_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_access_entry
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_access_entry("test-cluster_name", "test-principal_arn", kubernetes_groups="test-kubernetes_groups", client_request_token="test-client_request_token", username="test-username", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_eks_anywhere_subscription_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_eks_anywhere_subscription
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_eks_anywhere_subscription("test-id", True, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_nodegroup_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_nodegroup_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_nodegroup_version("test-cluster_name", "test-nodegroup_name", version="test-version", release_version="test-release_version", launch_template="test-launch_template", force=True, client_request_token="test-client_request_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_pod_identity_association_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.eks import update_pod_identity_association
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.eks.async_client", lambda *a, **kw: mock_client)
    await update_pod_identity_association("test-cluster_name", "test-association_id", role_arn="test-role_arn", client_request_token="test-client_request_token", disable_session_tags=True, target_role_arn="test-target_role_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()
