"""Native async EKS utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.eks import (
    AddonResult,
    AssociateAccessPolicyResult,
    AssociateEncryptionConfigResult,
    AssociateIdentityProviderConfigResult,
    ClusterResult,
    CreateAccessEntryResult,
    CreateEksAnywhereSubscriptionResult,
    CreatePodIdentityAssociationResult,
    DeleteEksAnywhereSubscriptionResult,
    DeletePodIdentityAssociationResult,
    DeregisterClusterResult,
    DescribeAccessEntryResult,
    DescribeAddonConfigurationResult,
    DescribeAddonVersionsResult,
    DescribeClusterVersionsResult,
    DescribeEksAnywhereSubscriptionResult,
    DescribeIdentityProviderConfigResult,
    DescribeInsightResult,
    DescribeInsightsRefreshResult,
    DescribePodIdentityAssociationResult,
    DescribeUpdateResult,
    DisassociateIdentityProviderConfigResult,
    FargateProfileResult,
    ListAccessEntriesResult,
    ListAccessPoliciesResult,
    ListAssociatedAccessPoliciesResult,
    ListEksAnywhereSubscriptionsResult,
    ListIdentityProviderConfigsResult,
    ListInsightsResult,
    ListPodIdentityAssociationsResult,
    ListTagsForResourceResult,
    ListUpdatesResult,
    NodegroupResult,
    RegisterClusterResult,
    StartInsightsRefreshResult,
    UpdateAccessEntryResult,
    UpdateEksAnywhereSubscriptionResult,
    UpdateNodegroupVersionResult,
    UpdatePodIdentityAssociationResult,
    _parse_addon,
    _parse_cluster,
    _parse_fargate_profile,
    _parse_nodegroup,
)
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error

__all__ = [
    "AddonResult",
    "AssociateAccessPolicyResult",
    "AssociateEncryptionConfigResult",
    "AssociateIdentityProviderConfigResult",
    "ClusterResult",
    "CreateAccessEntryResult",
    "CreateEksAnywhereSubscriptionResult",
    "CreatePodIdentityAssociationResult",
    "DeleteEksAnywhereSubscriptionResult",
    "DeletePodIdentityAssociationResult",
    "DeregisterClusterResult",
    "DescribeAccessEntryResult",
    "DescribeAddonConfigurationResult",
    "DescribeAddonVersionsResult",
    "DescribeClusterVersionsResult",
    "DescribeEksAnywhereSubscriptionResult",
    "DescribeIdentityProviderConfigResult",
    "DescribeInsightResult",
    "DescribeInsightsRefreshResult",
    "DescribePodIdentityAssociationResult",
    "DescribeUpdateResult",
    "DisassociateIdentityProviderConfigResult",
    "FargateProfileResult",
    "ListAccessEntriesResult",
    "ListAccessPoliciesResult",
    "ListAssociatedAccessPoliciesResult",
    "ListEksAnywhereSubscriptionsResult",
    "ListIdentityProviderConfigsResult",
    "ListInsightsResult",
    "ListPodIdentityAssociationsResult",
    "ListTagsForResourceResult",
    "ListUpdatesResult",
    "NodegroupResult",
    "RegisterClusterResult",
    "StartInsightsRefreshResult",
    "UpdateAccessEntryResult",
    "UpdateEksAnywhereSubscriptionResult",
    "UpdateNodegroupVersionResult",
    "UpdatePodIdentityAssociationResult",
    "associate_access_policy",
    "associate_encryption_config",
    "associate_identity_provider_config",
    "create_access_entry",
    "create_addon",
    "create_cluster",
    "create_eks_anywhere_subscription",
    "create_fargate_profile",
    "create_nodegroup",
    "create_pod_identity_association",
    "delete_access_entry",
    "delete_addon",
    "delete_cluster",
    "delete_eks_anywhere_subscription",
    "delete_fargate_profile",
    "delete_nodegroup",
    "delete_pod_identity_association",
    "deregister_cluster",
    "describe_access_entry",
    "describe_addon",
    "describe_addon_configuration",
    "describe_addon_versions",
    "describe_cluster",
    "describe_cluster_versions",
    "describe_eks_anywhere_subscription",
    "describe_fargate_profile",
    "describe_identity_provider_config",
    "describe_insight",
    "describe_insights_refresh",
    "describe_nodegroup",
    "describe_pod_identity_association",
    "describe_update",
    "disassociate_access_policy",
    "disassociate_identity_provider_config",
    "list_access_entries",
    "list_access_policies",
    "list_addons",
    "list_associated_access_policies",
    "list_clusters",
    "list_eks_anywhere_subscriptions",
    "list_fargate_profiles",
    "list_identity_provider_configs",
    "list_insights",
    "list_nodegroups",
    "list_pod_identity_associations",
    "list_tags_for_resource",
    "list_updates",
    "register_cluster",
    "start_insights_refresh",
    "tag_resource",
    "untag_resource",
    "update_access_entry",
    "update_addon",
    "update_cluster_config",
    "update_cluster_version",
    "update_eks_anywhere_subscription",
    "update_nodegroup_config",
    "update_nodegroup_version",
    "update_pod_identity_association",
    "wait_for_cluster",
    "wait_for_nodegroup",
]


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def create_cluster(
    name: str,
    *,
    role_arn: str,
    subnet_ids: list[str],
    security_group_ids: list[str] | None = None,
    version: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Create an EKS cluster.

    Args:
        name: Cluster name.
        role_arn: IAM role ARN for the cluster.
        subnet_ids: VPC subnet IDs for the cluster.
        security_group_ids: Optional security group IDs.
        version: Kubernetes version (e.g. ``"1.28"``).
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult` for the new cluster.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "name": name,
        "roleArn": role_arn,
        "resourcesVpcConfig": {
            "subnetIds": subnet_ids,
        },
    }
    if security_group_ids:
        kwargs["resourcesVpcConfig"]["securityGroupIds"] = security_group_ids
    if version:
        kwargs["version"] = version
    if tags:
        kwargs["tags"] = tags

    try:
        resp = await client.call("CreateCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_cluster failed for {name!r}") from exc
    return _parse_cluster(resp["cluster"])


async def describe_cluster(
    name: str,
    *,
    region_name: str | None = None,
) -> ClusterResult:
    """Describe an EKS cluster.

    Args:
        name: Cluster name.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call("DescribeCluster", name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_cluster failed for {name!r}") from exc
    return _parse_cluster(resp["cluster"])


async def list_clusters(*, region_name: str | None = None) -> list[str]:
    """List all EKS cluster names in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of cluster names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        items = await client.paginate("ListClusters", "clusters")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_clusters failed") from exc
    return [str(item) for item in items]


async def delete_cluster(
    name: str,
    *,
    region_name: str | None = None,
) -> ClusterResult:
    """Delete an EKS cluster.

    Args:
        name: Cluster name.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult` for the deleted cluster.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call("DeleteCluster", name=name)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_cluster failed for {name!r}") from exc
    return _parse_cluster(resp["cluster"])


async def update_cluster_version(
    name: str,
    *,
    version: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update the Kubernetes version of an EKS cluster.

    Args:
        name: Cluster name.
        version: Target Kubernetes version.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call("UpdateClusterVersion", name=name, version=version)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_cluster_version failed for {name!r}") from exc
    return resp.get("update", {})


async def update_cluster_config(
    name: str,
    *,
    resources_vpc_config: dict[str, Any] | None = None,
    logging: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update the configuration of an EKS cluster.

    Args:
        name: Cluster name.
        resources_vpc_config: Optional VPC configuration update.
        logging: Optional logging configuration update.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {"name": name}
    if resources_vpc_config is not None:
        kwargs["resourcesVpcConfig"] = resources_vpc_config
    if logging is not None:
        kwargs["logging"] = logging

    try:
        resp = await client.call("UpdateClusterConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_cluster_config failed for {name!r}") from exc
    return resp.get("update", {})


# ---------------------------------------------------------------------------
# Nodegroup operations
# ---------------------------------------------------------------------------


async def create_nodegroup(
    cluster_name: str,
    nodegroup_name: str,
    *,
    node_role: str,
    subnets: list[str],
    scaling_config: dict[str, Any] | None = None,
    instance_types: list[str] | None = None,
    ami_type: str | None = None,
    capacity_type: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> NodegroupResult:
    """Create a managed node group for an EKS cluster.

    Args:
        cluster_name: Name of the EKS cluster.
        nodegroup_name: Name for the new node group.
        node_role: IAM role ARN for the node group instances.
        subnets: VPC subnet IDs.
        scaling_config: Optional scaling configuration dict.
        instance_types: Optional list of EC2 instance types.
        ami_type: Optional AMI type (e.g. ``"AL2_x86_64"``).
        capacity_type: Optional capacity type (``"ON_DEMAND"`` or ``"SPOT"``).
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`NodegroupResult` for the new node group.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "nodegroupName": nodegroup_name,
        "nodeRole": node_role,
        "subnets": subnets,
    }
    if scaling_config is not None:
        kwargs["scalingConfig"] = scaling_config
    if instance_types is not None:
        kwargs["instanceTypes"] = instance_types
    if ami_type is not None:
        kwargs["amiType"] = ami_type
    if capacity_type is not None:
        kwargs["capacityType"] = capacity_type
    if tags is not None:
        kwargs["tags"] = tags

    try:
        resp = await client.call("CreateNodegroup", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_nodegroup failed for {nodegroup_name!r}") from exc
    return _parse_nodegroup(resp["nodegroup"])


async def describe_nodegroup(
    cluster_name: str,
    nodegroup_name: str,
    *,
    region_name: str | None = None,
) -> NodegroupResult:
    """Describe an EKS managed node group.

    Args:
        cluster_name: Name of the EKS cluster.
        nodegroup_name: Name of the node group.
        region_name: AWS region override.

    Returns:
        A :class:`NodegroupResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call(
            "DescribeNodegroup",
            clusterName=cluster_name,
            nodegroupName=nodegroup_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_nodegroup failed for {nodegroup_name!r}") from exc
    return _parse_nodegroup(resp["nodegroup"])


async def list_nodegroups(
    cluster_name: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List node group names for an EKS cluster.

    Args:
        cluster_name: Name of the EKS cluster.
        region_name: AWS region override.

    Returns:
        A list of node group names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        items = await client.paginate("ListNodegroups", "nodegroups", clusterName=cluster_name)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_nodegroups failed") from exc
    return [str(item) for item in items]


async def delete_nodegroup(
    cluster_name: str,
    nodegroup_name: str,
    *,
    region_name: str | None = None,
) -> NodegroupResult:
    """Delete an EKS managed node group.

    Args:
        cluster_name: Name of the EKS cluster.
        nodegroup_name: Name of the node group.
        region_name: AWS region override.

    Returns:
        A :class:`NodegroupResult` for the deleted node group.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call(
            "DeleteNodegroup",
            clusterName=cluster_name,
            nodegroupName=nodegroup_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_nodegroup failed for {nodegroup_name!r}") from exc
    return _parse_nodegroup(resp["nodegroup"])


async def update_nodegroup_config(
    cluster_name: str,
    nodegroup_name: str,
    *,
    scaling_config: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update the configuration of an EKS managed node group.

    Args:
        cluster_name: Name of the EKS cluster.
        nodegroup_name: Name of the node group.
        scaling_config: Optional scaling configuration update.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "nodegroupName": nodegroup_name,
    }
    if scaling_config is not None:
        kwargs["scalingConfig"] = scaling_config

    try:
        resp = await client.call("UpdateNodegroupConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_nodegroup_config failed for {nodegroup_name!r}") from exc
    return resp.get("update", {})


# ---------------------------------------------------------------------------
# Fargate profile operations
# ---------------------------------------------------------------------------


async def create_fargate_profile(
    cluster_name: str,
    fargate_profile_name: str,
    *,
    pod_execution_role_arn: str,
    subnets: list[str] | None = None,
    selectors: list[dict[str, Any]],
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> FargateProfileResult:
    """Create a Fargate profile for an EKS cluster.

    Args:
        cluster_name: Name of the EKS cluster.
        fargate_profile_name: Name for the Fargate profile.
        pod_execution_role_arn: IAM role ARN for pod execution.
        subnets: Optional VPC subnet IDs.
        selectors: Pod selectors for the profile.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`FargateProfileResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "fargateProfileName": fargate_profile_name,
        "podExecutionRoleArn": pod_execution_role_arn,
        "selectors": selectors,
    }
    if subnets is not None:
        kwargs["subnets"] = subnets
    if tags is not None:
        kwargs["tags"] = tags

    try:
        resp = await client.call("CreateFargateProfile", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(
            exc, f"create_fargate_profile failed for {fargate_profile_name!r}"
        ) from exc
    return _parse_fargate_profile(resp["fargateProfile"])


async def describe_fargate_profile(
    cluster_name: str,
    fargate_profile_name: str,
    *,
    region_name: str | None = None,
) -> FargateProfileResult:
    """Describe an EKS Fargate profile.

    Args:
        cluster_name: Name of the EKS cluster.
        fargate_profile_name: Name of the Fargate profile.
        region_name: AWS region override.

    Returns:
        A :class:`FargateProfileResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call(
            "DescribeFargateProfile",
            clusterName=cluster_name,
            fargateProfileName=fargate_profile_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"describe_fargate_profile failed for {fargate_profile_name!r}",
        ) from exc
    return _parse_fargate_profile(resp["fargateProfile"])


async def list_fargate_profiles(
    cluster_name: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List Fargate profile names for an EKS cluster.

    Args:
        cluster_name: Name of the EKS cluster.
        region_name: AWS region override.

    Returns:
        A list of Fargate profile names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        items = await client.paginate(
            "ListFargateProfiles",
            "fargateProfileNames",
            clusterName=cluster_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, "list_fargate_profiles failed") from exc
    return [str(item) for item in items]


async def delete_fargate_profile(
    cluster_name: str,
    fargate_profile_name: str,
    *,
    region_name: str | None = None,
) -> FargateProfileResult:
    """Delete an EKS Fargate profile.

    Args:
        cluster_name: Name of the EKS cluster.
        fargate_profile_name: Name of the Fargate profile.
        region_name: AWS region override.

    Returns:
        A :class:`FargateProfileResult` for the deleted profile.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call(
            "DeleteFargateProfile",
            clusterName=cluster_name,
            fargateProfileName=fargate_profile_name,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"delete_fargate_profile failed for {fargate_profile_name!r}",
        ) from exc
    return _parse_fargate_profile(resp["fargateProfile"])


# ---------------------------------------------------------------------------
# Addon operations
# ---------------------------------------------------------------------------


async def create_addon(
    cluster_name: str,
    addon_name: str,
    *,
    addon_version: str | None = None,
    service_account_role_arn: str | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> AddonResult:
    """Create an EKS add-on.

    Args:
        cluster_name: Name of the EKS cluster.
        addon_name: Name of the add-on (e.g. ``"vpc-cni"``).
        addon_version: Optional specific add-on version.
        service_account_role_arn: Optional IAM role for the service account.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        An :class:`AddonResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "addonName": addon_name,
    }
    if addon_version is not None:
        kwargs["addonVersion"] = addon_version
    if service_account_role_arn is not None:
        kwargs["serviceAccountRoleArn"] = service_account_role_arn
    if tags is not None:
        kwargs["tags"] = tags

    try:
        resp = await client.call("CreateAddon", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_addon failed for {addon_name!r}") from exc
    return _parse_addon(resp["addon"])


async def describe_addon(
    cluster_name: str,
    addon_name: str,
    *,
    region_name: str | None = None,
) -> AddonResult:
    """Describe an EKS add-on.

    Args:
        cluster_name: Name of the EKS cluster.
        addon_name: Name of the add-on.
        region_name: AWS region override.

    Returns:
        An :class:`AddonResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call(
            "DescribeAddon",
            clusterName=cluster_name,
            addonName=addon_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_addon failed for {addon_name!r}") from exc
    return _parse_addon(resp["addon"])


async def list_addons(
    cluster_name: str,
    *,
    region_name: str | None = None,
) -> list[str]:
    """List add-on names for an EKS cluster.

    Args:
        cluster_name: Name of the EKS cluster.
        region_name: AWS region override.

    Returns:
        A list of add-on names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        items = await client.paginate("ListAddons", "addons", clusterName=cluster_name)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_addons failed") from exc
    return [str(item) for item in items]


async def delete_addon(
    cluster_name: str,
    addon_name: str,
    *,
    region_name: str | None = None,
) -> AddonResult:
    """Delete an EKS add-on.

    Args:
        cluster_name: Name of the EKS cluster.
        addon_name: Name of the add-on.
        region_name: AWS region override.

    Returns:
        An :class:`AddonResult` for the deleted add-on.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    try:
        resp = await client.call(
            "DeleteAddon",
            clusterName=cluster_name,
            addonName=addon_name,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_addon failed for {addon_name!r}") from exc
    return _parse_addon(resp["addon"])


async def update_addon(
    cluster_name: str,
    addon_name: str,
    *,
    addon_version: str | None = None,
    service_account_role_arn: str | None = None,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update an EKS add-on.

    Args:
        cluster_name: Name of the EKS cluster.
        addon_name: Name of the add-on.
        addon_version: Optional new add-on version.
        service_account_role_arn: Optional IAM role for the service account.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "addonName": addon_name,
    }
    if addon_version is not None:
        kwargs["addonVersion"] = addon_version
    if service_account_role_arn is not None:
        kwargs["serviceAccountRoleArn"] = service_account_role_arn

    try:
        resp = await client.call("UpdateAddon", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_addon failed for {addon_name!r}") from exc
    return resp.get("update", {})


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def wait_for_cluster(
    name: str,
    *,
    target_status: str = "ACTIVE",
    timeout: float = 600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> ClusterResult:
    """Poll until an EKS cluster reaches a desired status.

    Args:
        name: Cluster name.
        target_status: Status to wait for (default ``"ACTIVE"``).
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between checks (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` in the target status.

    Raises:
        AwsTimeoutError: If the cluster does not reach the target status.
    """
    deadline = time.monotonic() + timeout
    while True:
        cluster = await describe_cluster(name, region_name=region_name)
        if cluster.status == target_status:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cluster {name!r} did not reach status {target_status!r} "
                f"within {timeout}s (current: {cluster.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def wait_for_nodegroup(
    cluster_name: str,
    nodegroup_name: str,
    *,
    target_status: str = "ACTIVE",
    timeout: float = 600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> NodegroupResult:
    """Poll until an EKS node group reaches a desired status.

    Args:
        cluster_name: Name of the EKS cluster.
        nodegroup_name: Name of the node group.
        target_status: Status to wait for (default ``"ACTIVE"``).
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between checks (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`NodegroupResult` in the target status.

    Raises:
        AwsTimeoutError: If the node group does not reach the target status.
    """
    deadline = time.monotonic() + timeout
    while True:
        ng = await describe_nodegroup(cluster_name, nodegroup_name, region_name=region_name)
        if ng.status == target_status:
            return ng
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Nodegroup {nodegroup_name!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {ng.status!r})"
            )
        await asyncio.sleep(poll_interval)


async def associate_access_policy(
    cluster_name: str,
    principal_arn: str,
    policy_arn: str,
    access_scope: dict[str, Any],
    region_name: str | None = None,
) -> AssociateAccessPolicyResult:
    """Associate access policy.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        policy_arn: Policy arn.
        access_scope: Access scope.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    kwargs["policyArn"] = policy_arn
    kwargs["accessScope"] = access_scope
    try:
        resp = await client.call("AssociateAccessPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate access policy") from exc
    return AssociateAccessPolicyResult(
        cluster_name=resp.get("clusterName"),
        principal_arn=resp.get("principalArn"),
        associated_access_policy=resp.get("associatedAccessPolicy"),
    )


async def associate_encryption_config(
    cluster_name: str,
    encryption_config: list[dict[str, Any]],
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> AssociateEncryptionConfigResult:
    """Associate encryption config.

    Args:
        cluster_name: Cluster name.
        encryption_config: Encryption config.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["encryptionConfig"] = encryption_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("AssociateEncryptionConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate encryption config") from exc
    return AssociateEncryptionConfigResult(
        update=resp.get("update"),
    )


async def associate_identity_provider_config(
    cluster_name: str,
    oidc: dict[str, Any],
    *,
    tags: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> AssociateIdentityProviderConfigResult:
    """Associate identity provider config.

    Args:
        cluster_name: Cluster name.
        oidc: Oidc.
        tags: Tags.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["oidc"] = oidc
    if tags is not None:
        kwargs["tags"] = tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("AssociateIdentityProviderConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to associate identity provider config") from exc
    return AssociateIdentityProviderConfigResult(
        update=resp.get("update"),
        tags=resp.get("tags"),
    )


async def create_access_entry(
    cluster_name: str,
    principal_arn: str,
    *,
    kubernetes_groups: list[str] | None = None,
    tags: dict[str, Any] | None = None,
    client_request_token: str | None = None,
    username: str | None = None,
    type_value: str | None = None,
    region_name: str | None = None,
) -> CreateAccessEntryResult:
    """Create access entry.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        kubernetes_groups: Kubernetes groups.
        tags: Tags.
        client_request_token: Client request token.
        username: Username.
        type_value: Type value.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    if kubernetes_groups is not None:
        kwargs["kubernetesGroups"] = kubernetes_groups
    if tags is not None:
        kwargs["tags"] = tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if username is not None:
        kwargs["username"] = username
    if type_value is not None:
        kwargs["type"] = type_value
    try:
        resp = await client.call("CreateAccessEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create access entry") from exc
    return CreateAccessEntryResult(
        access_entry=resp.get("accessEntry"),
    )


async def create_eks_anywhere_subscription(
    name: str,
    term: dict[str, Any],
    *,
    license_quantity: int | None = None,
    license_type: str | None = None,
    auto_renew: bool | None = None,
    client_request_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateEksAnywhereSubscriptionResult:
    """Create eks anywhere subscription.

    Args:
        name: Name.
        term: Term.
        license_quantity: License quantity.
        license_type: License type.
        auto_renew: Auto renew.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["term"] = term
    if license_quantity is not None:
        kwargs["licenseQuantity"] = license_quantity
    if license_type is not None:
        kwargs["licenseType"] = license_type
    if auto_renew is not None:
        kwargs["autoRenew"] = auto_renew
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("CreateEksAnywhereSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create eks anywhere subscription") from exc
    return CreateEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


async def create_pod_identity_association(
    cluster_name: str,
    namespace: str,
    service_account: str,
    role_arn: str,
    *,
    client_request_token: str | None = None,
    tags: dict[str, Any] | None = None,
    disable_session_tags: bool | None = None,
    target_role_arn: str | None = None,
    region_name: str | None = None,
) -> CreatePodIdentityAssociationResult:
    """Create pod identity association.

    Args:
        cluster_name: Cluster name.
        namespace: Namespace.
        service_account: Service account.
        role_arn: Role arn.
        client_request_token: Client request token.
        tags: Tags.
        disable_session_tags: Disable session tags.
        target_role_arn: Target role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["namespace"] = namespace
    kwargs["serviceAccount"] = service_account
    kwargs["roleArn"] = role_arn
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    if disable_session_tags is not None:
        kwargs["disableSessionTags"] = disable_session_tags
    if target_role_arn is not None:
        kwargs["targetRoleArn"] = target_role_arn
    try:
        resp = await client.call("CreatePodIdentityAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create pod identity association") from exc
    return CreatePodIdentityAssociationResult(
        association=resp.get("association"),
    )


async def delete_access_entry(
    cluster_name: str,
    principal_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete access entry.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    try:
        await client.call("DeleteAccessEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete access entry") from exc
    return None


async def delete_eks_anywhere_subscription(
    id: str,
    region_name: str | None = None,
) -> DeleteEksAnywhereSubscriptionResult:
    """Delete eks anywhere subscription.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("DeleteEksAnywhereSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete eks anywhere subscription") from exc
    return DeleteEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


async def delete_pod_identity_association(
    cluster_name: str,
    association_id: str,
    region_name: str | None = None,
) -> DeletePodIdentityAssociationResult:
    """Delete pod identity association.

    Args:
        cluster_name: Cluster name.
        association_id: Association id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["associationId"] = association_id
    try:
        resp = await client.call("DeletePodIdentityAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete pod identity association") from exc
    return DeletePodIdentityAssociationResult(
        association=resp.get("association"),
    )


async def deregister_cluster(
    name: str,
    region_name: str | None = None,
) -> DeregisterClusterResult:
    """Deregister cluster.

    Args:
        name: Name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    try:
        resp = await client.call("DeregisterCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister cluster") from exc
    return DeregisterClusterResult(
        cluster=resp.get("cluster"),
    )


async def describe_access_entry(
    cluster_name: str,
    principal_arn: str,
    region_name: str | None = None,
) -> DescribeAccessEntryResult:
    """Describe access entry.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    try:
        resp = await client.call("DescribeAccessEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe access entry") from exc
    return DescribeAccessEntryResult(
        access_entry=resp.get("accessEntry"),
    )


async def describe_addon_configuration(
    addon_name: str,
    addon_version: str,
    region_name: str | None = None,
) -> DescribeAddonConfigurationResult:
    """Describe addon configuration.

    Args:
        addon_name: Addon name.
        addon_version: Addon version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["addonName"] = addon_name
    kwargs["addonVersion"] = addon_version
    try:
        resp = await client.call("DescribeAddonConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe addon configuration") from exc
    return DescribeAddonConfigurationResult(
        addon_name=resp.get("addonName"),
        addon_version=resp.get("addonVersion"),
        configuration_schema=resp.get("configurationSchema"),
        pod_identity_configuration=resp.get("podIdentityConfiguration"),
    )


async def describe_addon_versions(
    *,
    kubernetes_version: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    addon_name: str | None = None,
    types: list[str] | None = None,
    publishers: list[str] | None = None,
    owners: list[str] | None = None,
    region_name: str | None = None,
) -> DescribeAddonVersionsResult:
    """Describe addon versions.

    Args:
        kubernetes_version: Kubernetes version.
        max_results: Max results.
        next_token: Next token.
        addon_name: Addon name.
        types: Types.
        publishers: Publishers.
        owners: Owners.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    if kubernetes_version is not None:
        kwargs["kubernetesVersion"] = kubernetes_version
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if addon_name is not None:
        kwargs["addonName"] = addon_name
    if types is not None:
        kwargs["types"] = types
    if publishers is not None:
        kwargs["publishers"] = publishers
    if owners is not None:
        kwargs["owners"] = owners
    try:
        resp = await client.call("DescribeAddonVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe addon versions") from exc
    return DescribeAddonVersionsResult(
        addons=resp.get("addons"),
        next_token=resp.get("nextToken"),
    )


async def describe_cluster_versions(
    *,
    cluster_type: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    default_only: bool | None = None,
    include_all: bool | None = None,
    cluster_versions: list[str] | None = None,
    status: str | None = None,
    version_status: str | None = None,
    region_name: str | None = None,
) -> DescribeClusterVersionsResult:
    """Describe cluster versions.

    Args:
        cluster_type: Cluster type.
        max_results: Max results.
        next_token: Next token.
        default_only: Default only.
        include_all: Include all.
        cluster_versions: Cluster versions.
        status: Status.
        version_status: Version status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_type is not None:
        kwargs["clusterType"] = cluster_type
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if default_only is not None:
        kwargs["defaultOnly"] = default_only
    if include_all is not None:
        kwargs["includeAll"] = include_all
    if cluster_versions is not None:
        kwargs["clusterVersions"] = cluster_versions
    if status is not None:
        kwargs["status"] = status
    if version_status is not None:
        kwargs["versionStatus"] = version_status
    try:
        resp = await client.call("DescribeClusterVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster versions") from exc
    return DescribeClusterVersionsResult(
        next_token=resp.get("nextToken"),
        cluster_versions=resp.get("clusterVersions"),
    )


async def describe_eks_anywhere_subscription(
    id: str,
    region_name: str | None = None,
) -> DescribeEksAnywhereSubscriptionResult:
    """Describe eks anywhere subscription.

    Args:
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = await client.call("DescribeEksAnywhereSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe eks anywhere subscription") from exc
    return DescribeEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


async def describe_identity_provider_config(
    cluster_name: str,
    identity_provider_config: dict[str, Any],
    region_name: str | None = None,
) -> DescribeIdentityProviderConfigResult:
    """Describe identity provider config.

    Args:
        cluster_name: Cluster name.
        identity_provider_config: Identity provider config.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["identityProviderConfig"] = identity_provider_config
    try:
        resp = await client.call("DescribeIdentityProviderConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe identity provider config") from exc
    return DescribeIdentityProviderConfigResult(
        identity_provider_config=resp.get("identityProviderConfig"),
    )


async def describe_insight(
    cluster_name: str,
    id: str,
    region_name: str | None = None,
) -> DescribeInsightResult:
    """Describe insight.

    Args:
        cluster_name: Cluster name.
        id: Id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["id"] = id
    try:
        resp = await client.call("DescribeInsight", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe insight") from exc
    return DescribeInsightResult(
        insight=resp.get("insight"),
    )


async def describe_insights_refresh(
    cluster_name: str,
    region_name: str | None = None,
) -> DescribeInsightsRefreshResult:
    """Describe insights refresh.

    Args:
        cluster_name: Cluster name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    try:
        resp = await client.call("DescribeInsightsRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe insights refresh") from exc
    return DescribeInsightsRefreshResult(
        message=resp.get("message"),
        status=resp.get("status"),
        started_at=resp.get("startedAt"),
        ended_at=resp.get("endedAt"),
    )


async def describe_pod_identity_association(
    cluster_name: str,
    association_id: str,
    region_name: str | None = None,
) -> DescribePodIdentityAssociationResult:
    """Describe pod identity association.

    Args:
        cluster_name: Cluster name.
        association_id: Association id.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["associationId"] = association_id
    try:
        resp = await client.call("DescribePodIdentityAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe pod identity association") from exc
    return DescribePodIdentityAssociationResult(
        association=resp.get("association"),
    )


async def describe_update(
    name: str,
    update_id: str,
    *,
    nodegroup_name: str | None = None,
    addon_name: str | None = None,
    region_name: str | None = None,
) -> DescribeUpdateResult:
    """Describe update.

    Args:
        name: Name.
        update_id: Update id.
        nodegroup_name: Nodegroup name.
        addon_name: Addon name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["updateId"] = update_id
    if nodegroup_name is not None:
        kwargs["nodegroupName"] = nodegroup_name
    if addon_name is not None:
        kwargs["addonName"] = addon_name
    try:
        resp = await client.call("DescribeUpdate", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe update") from exc
    return DescribeUpdateResult(
        update=resp.get("update"),
    )


async def disassociate_access_policy(
    cluster_name: str,
    principal_arn: str,
    policy_arn: str,
    region_name: str | None = None,
) -> None:
    """Disassociate access policy.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        policy_arn: Policy arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    kwargs["policyArn"] = policy_arn
    try:
        await client.call("DisassociateAccessPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate access policy") from exc
    return None


async def disassociate_identity_provider_config(
    cluster_name: str,
    identity_provider_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> DisassociateIdentityProviderConfigResult:
    """Disassociate identity provider config.

    Args:
        cluster_name: Cluster name.
        identity_provider_config: Identity provider config.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["identityProviderConfig"] = identity_provider_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("DisassociateIdentityProviderConfig", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disassociate identity provider config") from exc
    return DisassociateIdentityProviderConfigResult(
        update=resp.get("update"),
    )


async def list_access_entries(
    cluster_name: str,
    *,
    associated_policy_arn: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAccessEntriesResult:
    """List access entries.

    Args:
        cluster_name: Cluster name.
        associated_policy_arn: Associated policy arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if associated_policy_arn is not None:
        kwargs["associatedPolicyArn"] = associated_policy_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAccessEntries", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list access entries") from exc
    return ListAccessEntriesResult(
        access_entries=resp.get("accessEntries"),
        next_token=resp.get("nextToken"),
    )


async def list_access_policies(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAccessPoliciesResult:
    """List access policies.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAccessPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list access policies") from exc
    return ListAccessPoliciesResult(
        access_policies=resp.get("accessPolicies"),
        next_token=resp.get("nextToken"),
    )


async def list_associated_access_policies(
    cluster_name: str,
    principal_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListAssociatedAccessPoliciesResult:
    """List associated access policies.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListAssociatedAccessPolicies", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list associated access policies") from exc
    return ListAssociatedAccessPoliciesResult(
        cluster_name=resp.get("clusterName"),
        principal_arn=resp.get("principalArn"),
        next_token=resp.get("nextToken"),
        associated_access_policies=resp.get("associatedAccessPolicies"),
    )


async def list_eks_anywhere_subscriptions(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    include_status: list[str] | None = None,
    region_name: str | None = None,
) -> ListEksAnywhereSubscriptionsResult:
    """List eks anywhere subscriptions.

    Args:
        max_results: Max results.
        next_token: Next token.
        include_status: Include status.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if include_status is not None:
        kwargs["includeStatus"] = include_status
    try:
        resp = await client.call("ListEksAnywhereSubscriptions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list eks anywhere subscriptions") from exc
    return ListEksAnywhereSubscriptionsResult(
        subscriptions=resp.get("subscriptions"),
        next_token=resp.get("nextToken"),
    )


async def list_identity_provider_configs(
    cluster_name: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListIdentityProviderConfigsResult:
    """List identity provider configs.

    Args:
        cluster_name: Cluster name.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListIdentityProviderConfigs", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list identity provider configs") from exc
    return ListIdentityProviderConfigsResult(
        identity_provider_configs=resp.get("identityProviderConfigs"),
        next_token=resp.get("nextToken"),
    )


async def list_insights(
    cluster_name: str,
    *,
    filter: dict[str, Any] | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListInsightsResult:
    """List insights.

    Args:
        cluster_name: Cluster name.
        filter: Filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListInsights", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list insights") from exc
    return ListInsightsResult(
        insights=resp.get("insights"),
        next_token=resp.get("nextToken"),
    )


async def list_pod_identity_associations(
    cluster_name: str,
    *,
    namespace: str | None = None,
    service_account: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListPodIdentityAssociationsResult:
    """List pod identity associations.

    Args:
        cluster_name: Cluster name.
        namespace: Namespace.
        service_account: Service account.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if namespace is not None:
        kwargs["namespace"] = namespace
    if service_account is not None:
        kwargs["serviceAccount"] = service_account
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = await client.call("ListPodIdentityAssociations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list pod identity associations") from exc
    return ListPodIdentityAssociationsResult(
        associations=resp.get("associations"),
        next_token=resp.get("nextToken"),
    )


async def list_tags_for_resource(
    resource_arn: str,
    region_name: str | None = None,
) -> ListTagsForResourceResult:
    """List tags for resource.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


async def list_updates(
    name: str,
    *,
    nodegroup_name: str | None = None,
    addon_name: str | None = None,
    next_token: str | None = None,
    max_results: int | None = None,
    region_name: str | None = None,
) -> ListUpdatesResult:
    """List updates.

    Args:
        name: Name.
        nodegroup_name: Nodegroup name.
        addon_name: Addon name.
        next_token: Next token.
        max_results: Max results.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    if nodegroup_name is not None:
        kwargs["nodegroupName"] = nodegroup_name
    if addon_name is not None:
        kwargs["addonName"] = addon_name
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if max_results is not None:
        kwargs["maxResults"] = max_results
    try:
        resp = await client.call("ListUpdates", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list updates") from exc
    return ListUpdatesResult(
        update_ids=resp.get("updateIds"),
        next_token=resp.get("nextToken"),
    )


async def register_cluster(
    name: str,
    connector_config: dict[str, Any],
    *,
    client_request_token: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RegisterClusterResult:
    """Register cluster.

    Args:
        name: Name.
        connector_config: Connector config.
        client_request_token: Client request token.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["connectorConfig"] = connector_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = await client.call("RegisterCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register cluster") from exc
    return RegisterClusterResult(
        cluster=resp.get("cluster"),
    )


async def start_insights_refresh(
    cluster_name: str,
    region_name: str | None = None,
) -> StartInsightsRefreshResult:
    """Start insights refresh.

    Args:
        cluster_name: Cluster name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    try:
        resp = await client.call("StartInsightsRefresh", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start insights refresh") from exc
    return StartInsightsRefreshResult(
        message=resp.get("message"),
        status=resp.get("status"),
    )


async def tag_resource(
    resource_arn: str,
    tags: dict[str, Any],
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        resource_arn: Resource arn.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    resource_arn: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        resource_arn: Resource arn.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_access_entry(
    cluster_name: str,
    principal_arn: str,
    *,
    kubernetes_groups: list[str] | None = None,
    client_request_token: str | None = None,
    username: str | None = None,
    region_name: str | None = None,
) -> UpdateAccessEntryResult:
    """Update access entry.

    Args:
        cluster_name: Cluster name.
        principal_arn: Principal arn.
        kubernetes_groups: Kubernetes groups.
        client_request_token: Client request token.
        username: Username.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    if kubernetes_groups is not None:
        kwargs["kubernetesGroups"] = kubernetes_groups
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if username is not None:
        kwargs["username"] = username
    try:
        resp = await client.call("UpdateAccessEntry", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update access entry") from exc
    return UpdateAccessEntryResult(
        access_entry=resp.get("accessEntry"),
    )


async def update_eks_anywhere_subscription(
    id: str,
    auto_renew: bool,
    *,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> UpdateEksAnywhereSubscriptionResult:
    """Update eks anywhere subscription.

    Args:
        id: Id.
        auto_renew: Auto renew.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    kwargs["autoRenew"] = auto_renew
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("UpdateEksAnywhereSubscription", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update eks anywhere subscription") from exc
    return UpdateEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


async def update_nodegroup_version(
    cluster_name: str,
    nodegroup_name: str,
    *,
    version: str | None = None,
    release_version: str | None = None,
    launch_template: dict[str, Any] | None = None,
    force: bool | None = None,
    client_request_token: str | None = None,
    region_name: str | None = None,
) -> UpdateNodegroupVersionResult:
    """Update nodegroup version.

    Args:
        cluster_name: Cluster name.
        nodegroup_name: Nodegroup name.
        version: Version.
        release_version: Release version.
        launch_template: Launch template.
        force: Force.
        client_request_token: Client request token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["nodegroupName"] = nodegroup_name
    if version is not None:
        kwargs["version"] = version
    if release_version is not None:
        kwargs["releaseVersion"] = release_version
    if launch_template is not None:
        kwargs["launchTemplate"] = launch_template
    if force is not None:
        kwargs["force"] = force
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = await client.call("UpdateNodegroupVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update nodegroup version") from exc
    return UpdateNodegroupVersionResult(
        update=resp.get("update"),
    )


async def update_pod_identity_association(
    cluster_name: str,
    association_id: str,
    *,
    role_arn: str | None = None,
    client_request_token: str | None = None,
    disable_session_tags: bool | None = None,
    target_role_arn: str | None = None,
    region_name: str | None = None,
) -> UpdatePodIdentityAssociationResult:
    """Update pod identity association.

    Args:
        cluster_name: Cluster name.
        association_id: Association id.
        role_arn: Role arn.
        client_request_token: Client request token.
        disable_session_tags: Disable session tags.
        target_role_arn: Target role arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["associationId"] = association_id
    if role_arn is not None:
        kwargs["roleArn"] = role_arn
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if disable_session_tags is not None:
        kwargs["disableSessionTags"] = disable_session_tags
    if target_role_arn is not None:
        kwargs["targetRoleArn"] = target_role_arn
    try:
        resp = await client.call("UpdatePodIdentityAssociation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update pod identity association") from exc
    return UpdatePodIdentityAssociationResult(
        association=resp.get("association"),
    )
