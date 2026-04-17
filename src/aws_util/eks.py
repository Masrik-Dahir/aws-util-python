"""aws_util.eks — Amazon Elastic Kubernetes Service utilities.

Provides convenience wrappers around EKS cluster, nodegroup, Fargate profile,
and add-on management operations with Pydantic-modelled results.
"""

from __future__ import annotations

import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
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
# Models
# ---------------------------------------------------------------------------


class ClusterResult(BaseModel):
    """Metadata for an EKS cluster."""

    model_config = ConfigDict(frozen=True)

    name: str
    arn: str
    status: str
    endpoint: str | None = None
    role_arn: str
    version: str | None = None
    platform_version: str | None = None
    kubernetes_network_config: dict[str, Any] = {}
    certificate_authority: str | None = None
    created_at: str | None = None
    tags: dict[str, str] = {}
    extra: dict[str, Any] = {}


class NodegroupResult(BaseModel):
    """Metadata for an EKS managed node group."""

    model_config = ConfigDict(frozen=True)

    nodegroup_name: str
    cluster_name: str
    status: str
    capacity_type: str | None = None
    scaling_config: dict[str, Any] = {}
    instance_types: list[str] = []
    ami_type: str | None = None
    node_role: str | None = None
    subnets: list[str] = []
    extra: dict[str, Any] = {}


class AddonResult(BaseModel):
    """Metadata for an EKS add-on."""

    model_config = ConfigDict(frozen=True)

    addon_name: str
    cluster_name: str
    status: str
    addon_version: str | None = None
    service_account_role_arn: str | None = None
    extra: dict[str, Any] = {}


class FargateProfileResult(BaseModel):
    """Metadata for an EKS Fargate profile."""

    model_config = ConfigDict(frozen=True)

    fargate_profile_name: str
    cluster_name: str
    status: str
    pod_execution_role_arn: str | None = None
    subnets: list[str] = []
    selectors: list[dict[str, Any]] = []
    extra: dict[str, Any] = {}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_cluster(data: dict[str, Any]) -> ClusterResult:
    """Parse a raw EKS cluster dict into a :class:`ClusterResult`."""
    cert_data = data.get("certificateAuthority", {})
    created = data.get("createdAt")
    return ClusterResult(
        name=data["name"],
        arn=data["arn"],
        status=data["status"],
        endpoint=data.get("endpoint"),
        role_arn=data.get("roleArn", ""),
        version=data.get("version"),
        platform_version=data.get("platformVersion"),
        kubernetes_network_config=data.get("kubernetesNetworkConfig", {}),
        certificate_authority=cert_data.get("data") if cert_data else None,
        created_at=str(created) if created is not None else None,
        tags=data.get("tags", {}),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "name",
                "arn",
                "status",
                "endpoint",
                "roleArn",
                "version",
                "platformVersion",
                "kubernetesNetworkConfig",
                "certificateAuthority",
                "createdAt",
                "tags",
            }
        },
    )


def _parse_nodegroup(data: dict[str, Any]) -> NodegroupResult:
    """Parse a raw EKS nodegroup dict into a :class:`NodegroupResult`."""
    return NodegroupResult(
        nodegroup_name=data["nodegroupName"],
        cluster_name=data["clusterName"],
        status=data["status"],
        capacity_type=data.get("capacityType"),
        scaling_config=data.get("scalingConfig", {}),
        instance_types=data.get("instanceTypes", []),
        ami_type=data.get("amiType"),
        node_role=data.get("nodeRole"),
        subnets=data.get("subnets", []),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "nodegroupName",
                "clusterName",
                "status",
                "capacityType",
                "scalingConfig",
                "instanceTypes",
                "amiType",
                "nodeRole",
                "subnets",
            }
        },
    )


def _parse_addon(data: dict[str, Any]) -> AddonResult:
    """Parse a raw EKS addon dict into an :class:`AddonResult`."""
    return AddonResult(
        addon_name=data["addonName"],
        cluster_name=data["clusterName"],
        status=data["status"],
        addon_version=data.get("addonVersion"),
        service_account_role_arn=data.get("serviceAccountRoleArn"),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "addonName",
                "clusterName",
                "status",
                "addonVersion",
                "serviceAccountRoleArn",
            }
        },
    )


def _parse_fargate_profile(data: dict[str, Any]) -> FargateProfileResult:
    """Parse a raw EKS Fargate profile dict into a :class:`FargateProfileResult`."""
    return FargateProfileResult(
        fargate_profile_name=data["fargateProfileName"],
        cluster_name=data["clusterName"],
        status=data["status"],
        pod_execution_role_arn=data.get("podExecutionRoleArn"),
        subnets=data.get("subnets", []),
        selectors=data.get("selectors", []),
        extra={
            k: v
            for k, v in data.items()
            if k
            not in {
                "fargateProfileName",
                "clusterName",
                "status",
                "podExecutionRoleArn",
                "subnets",
                "selectors",
            }
        },
    )


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


def create_cluster(
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
    client = get_client("eks", region_name)
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
        resp = client.create_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_cluster failed for {name!r}") from exc
    return _parse_cluster(resp["cluster"])


def describe_cluster(
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
    client = get_client("eks", region_name)
    try:
        resp = client.describe_cluster(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_cluster failed for {name!r}") from exc
    return _parse_cluster(resp["cluster"])


def list_clusters(*, region_name: str | None = None) -> list[str]:
    """List all EKS cluster names in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of cluster names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = get_client("eks", region_name)
    names: list[str] = []
    try:
        paginator = client.get_paginator("list_clusters")
        for page in paginator.paginate():
            names.extend(page.get("clusters", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_clusters failed") from exc
    return names


def delete_cluster(
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
    client = get_client("eks", region_name)
    try:
        resp = client.delete_cluster(name=name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_cluster failed for {name!r}") from exc
    return _parse_cluster(resp["cluster"])


def update_cluster_version(
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
    client = get_client("eks", region_name)
    try:
        resp = client.update_cluster_version(name=name, version=version)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_cluster_version failed for {name!r}") from exc
    return resp.get("update", {})


def update_cluster_config(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {"name": name}
    if resources_vpc_config is not None:
        kwargs["resourcesVpcConfig"] = resources_vpc_config
    if logging is not None:
        kwargs["logging"] = logging

    try:
        resp = client.update_cluster_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_cluster_config failed for {name!r}") from exc
    return resp.get("update", {})


# ---------------------------------------------------------------------------
# Nodegroup operations
# ---------------------------------------------------------------------------


def create_nodegroup(
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
    client = get_client("eks", region_name)
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
        resp = client.create_nodegroup(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_nodegroup failed for {nodegroup_name!r}") from exc
    return _parse_nodegroup(resp["nodegroup"])


def describe_nodegroup(
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
    client = get_client("eks", region_name)
    try:
        resp = client.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_nodegroup failed for {nodegroup_name!r}") from exc
    return _parse_nodegroup(resp["nodegroup"])


def list_nodegroups(
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
    client = get_client("eks", region_name)
    names: list[str] = []
    try:
        paginator = client.get_paginator("list_nodegroups")
        for page in paginator.paginate(clusterName=cluster_name):
            names.extend(page.get("nodegroups", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_nodegroups failed") from exc
    return names


def delete_nodegroup(
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
    client = get_client("eks", region_name)
    try:
        resp = client.delete_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_nodegroup failed for {nodegroup_name!r}") from exc
    return _parse_nodegroup(resp["nodegroup"])


def update_nodegroup_config(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "nodegroupName": nodegroup_name,
    }
    if scaling_config is not None:
        kwargs["scalingConfig"] = scaling_config

    try:
        resp = client.update_nodegroup_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_nodegroup_config failed for {nodegroup_name!r}") from exc
    return resp.get("update", {})


# ---------------------------------------------------------------------------
# Fargate profile operations
# ---------------------------------------------------------------------------


def create_fargate_profile(
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
    client = get_client("eks", region_name)
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
        resp = client.create_fargate_profile(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(
            exc, f"create_fargate_profile failed for {fargate_profile_name!r}"
        ) from exc
    return _parse_fargate_profile(resp["fargateProfile"])


def describe_fargate_profile(
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
    client = get_client("eks", region_name)
    try:
        resp = client.describe_fargate_profile(
            clusterName=cluster_name,
            fargateProfileName=fargate_profile_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"describe_fargate_profile failed for {fargate_profile_name!r}",
        ) from exc
    return _parse_fargate_profile(resp["fargateProfile"])


def list_fargate_profiles(
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
    client = get_client("eks", region_name)
    names: list[str] = []
    try:
        paginator = client.get_paginator("list_fargate_profiles")
        for page in paginator.paginate(clusterName=cluster_name):
            names.extend(page.get("fargateProfileNames", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_fargate_profiles failed") from exc
    return names


def delete_fargate_profile(
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
    client = get_client("eks", region_name)
    try:
        resp = client.delete_fargate_profile(
            clusterName=cluster_name,
            fargateProfileName=fargate_profile_name,
        )
    except ClientError as exc:
        raise wrap_aws_error(
            exc,
            f"delete_fargate_profile failed for {fargate_profile_name!r}",
        ) from exc
    return _parse_fargate_profile(resp["fargateProfile"])


# ---------------------------------------------------------------------------
# Addon operations
# ---------------------------------------------------------------------------


def create_addon(
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
    client = get_client("eks", region_name)
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
        resp = client.create_addon(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"create_addon failed for {addon_name!r}") from exc
    return _parse_addon(resp["addon"])


def describe_addon(
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
    client = get_client("eks", region_name)
    try:
        resp = client.describe_addon(clusterName=cluster_name, addonName=addon_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"describe_addon failed for {addon_name!r}") from exc
    return _parse_addon(resp["addon"])


def list_addons(
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
    client = get_client("eks", region_name)
    names: list[str] = []
    try:
        paginator = client.get_paginator("list_addons")
        for page in paginator.paginate(clusterName=cluster_name):
            names.extend(page.get("addons", []))
    except ClientError as exc:
        raise wrap_aws_error(exc, "list_addons failed") from exc
    return names


def delete_addon(
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
    client = get_client("eks", region_name)
    try:
        resp = client.delete_addon(clusterName=cluster_name, addonName=addon_name)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"delete_addon failed for {addon_name!r}") from exc
    return _parse_addon(resp["addon"])


def update_addon(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {
        "clusterName": cluster_name,
        "addonName": addon_name,
    }
    if addon_version is not None:
        kwargs["addonVersion"] = addon_version
    if service_account_role_arn is not None:
        kwargs["serviceAccountRoleArn"] = service_account_role_arn

    try:
        resp = client.update_addon(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, f"update_addon failed for {addon_name!r}") from exc
    return resp.get("update", {})


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


def wait_for_cluster(
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
        cluster = describe_cluster(name, region_name=region_name)
        if cluster.status == target_status:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cluster {name!r} did not reach status {target_status!r} "
                f"within {timeout}s (current: {cluster.status!r})"
            )
        time.sleep(poll_interval)


def wait_for_nodegroup(
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
        ng = describe_nodegroup(cluster_name, nodegroup_name, region_name=region_name)
        if ng.status == target_status:
            return ng
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Nodegroup {nodegroup_name!r} did not reach status "
                f"{target_status!r} within {timeout}s "
                f"(current: {ng.status!r})"
            )
        time.sleep(poll_interval)


class AssociateAccessPolicyResult(BaseModel):
    """Result of associate_access_policy."""

    model_config = ConfigDict(frozen=True)

    cluster_name: str | None = None
    principal_arn: str | None = None
    associated_access_policy: dict[str, Any] | None = None


class AssociateEncryptionConfigResult(BaseModel):
    """Result of associate_encryption_config."""

    model_config = ConfigDict(frozen=True)

    update: dict[str, Any] | None = None


class AssociateIdentityProviderConfigResult(BaseModel):
    """Result of associate_identity_provider_config."""

    model_config = ConfigDict(frozen=True)

    update: dict[str, Any] | None = None
    tags: dict[str, Any] | None = None


class CreateAccessEntryResult(BaseModel):
    """Result of create_access_entry."""

    model_config = ConfigDict(frozen=True)

    access_entry: dict[str, Any] | None = None


class CreateEksAnywhereSubscriptionResult(BaseModel):
    """Result of create_eks_anywhere_subscription."""

    model_config = ConfigDict(frozen=True)

    subscription: dict[str, Any] | None = None


class CreatePodIdentityAssociationResult(BaseModel):
    """Result of create_pod_identity_association."""

    model_config = ConfigDict(frozen=True)

    association: dict[str, Any] | None = None


class DeleteEksAnywhereSubscriptionResult(BaseModel):
    """Result of delete_eks_anywhere_subscription."""

    model_config = ConfigDict(frozen=True)

    subscription: dict[str, Any] | None = None


class DeletePodIdentityAssociationResult(BaseModel):
    """Result of delete_pod_identity_association."""

    model_config = ConfigDict(frozen=True)

    association: dict[str, Any] | None = None


class DeregisterClusterResult(BaseModel):
    """Result of deregister_cluster."""

    model_config = ConfigDict(frozen=True)

    cluster: dict[str, Any] | None = None


class DescribeAccessEntryResult(BaseModel):
    """Result of describe_access_entry."""

    model_config = ConfigDict(frozen=True)

    access_entry: dict[str, Any] | None = None


class DescribeAddonConfigurationResult(BaseModel):
    """Result of describe_addon_configuration."""

    model_config = ConfigDict(frozen=True)

    addon_name: str | None = None
    addon_version: str | None = None
    configuration_schema: str | None = None
    pod_identity_configuration: list[dict[str, Any]] | None = None


class DescribeAddonVersionsResult(BaseModel):
    """Result of describe_addon_versions."""

    model_config = ConfigDict(frozen=True)

    addons: list[dict[str, Any]] | None = None
    next_token: str | None = None


class DescribeClusterVersionsResult(BaseModel):
    """Result of describe_cluster_versions."""

    model_config = ConfigDict(frozen=True)

    next_token: str | None = None
    cluster_versions: list[dict[str, Any]] | None = None


class DescribeEksAnywhereSubscriptionResult(BaseModel):
    """Result of describe_eks_anywhere_subscription."""

    model_config = ConfigDict(frozen=True)

    subscription: dict[str, Any] | None = None


class DescribeIdentityProviderConfigResult(BaseModel):
    """Result of describe_identity_provider_config."""

    model_config = ConfigDict(frozen=True)

    identity_provider_config: dict[str, Any] | None = None


class DescribeInsightResult(BaseModel):
    """Result of describe_insight."""

    model_config = ConfigDict(frozen=True)

    insight: dict[str, Any] | None = None


class DescribeInsightsRefreshResult(BaseModel):
    """Result of describe_insights_refresh."""

    model_config = ConfigDict(frozen=True)

    message: str | None = None
    status: str | None = None
    started_at: str | None = None
    ended_at: str | None = None


class DescribePodIdentityAssociationResult(BaseModel):
    """Result of describe_pod_identity_association."""

    model_config = ConfigDict(frozen=True)

    association: dict[str, Any] | None = None


class DescribeUpdateResult(BaseModel):
    """Result of describe_update."""

    model_config = ConfigDict(frozen=True)

    update: dict[str, Any] | None = None


class DisassociateIdentityProviderConfigResult(BaseModel):
    """Result of disassociate_identity_provider_config."""

    model_config = ConfigDict(frozen=True)

    update: dict[str, Any] | None = None


class ListAccessEntriesResult(BaseModel):
    """Result of list_access_entries."""

    model_config = ConfigDict(frozen=True)

    access_entries: list[str] | None = None
    next_token: str | None = None


class ListAccessPoliciesResult(BaseModel):
    """Result of list_access_policies."""

    model_config = ConfigDict(frozen=True)

    access_policies: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListAssociatedAccessPoliciesResult(BaseModel):
    """Result of list_associated_access_policies."""

    model_config = ConfigDict(frozen=True)

    cluster_name: str | None = None
    principal_arn: str | None = None
    next_token: str | None = None
    associated_access_policies: list[dict[str, Any]] | None = None


class ListEksAnywhereSubscriptionsResult(BaseModel):
    """Result of list_eks_anywhere_subscriptions."""

    model_config = ConfigDict(frozen=True)

    subscriptions: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListIdentityProviderConfigsResult(BaseModel):
    """Result of list_identity_provider_configs."""

    model_config = ConfigDict(frozen=True)

    identity_provider_configs: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListInsightsResult(BaseModel):
    """Result of list_insights."""

    model_config = ConfigDict(frozen=True)

    insights: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListPodIdentityAssociationsResult(BaseModel):
    """Result of list_pod_identity_associations."""

    model_config = ConfigDict(frozen=True)

    associations: list[dict[str, Any]] | None = None
    next_token: str | None = None


class ListTagsForResourceResult(BaseModel):
    """Result of list_tags_for_resource."""

    model_config = ConfigDict(frozen=True)

    tags: dict[str, Any] | None = None


class ListUpdatesResult(BaseModel):
    """Result of list_updates."""

    model_config = ConfigDict(frozen=True)

    update_ids: list[str] | None = None
    next_token: str | None = None


class RegisterClusterResult(BaseModel):
    """Result of register_cluster."""

    model_config = ConfigDict(frozen=True)

    cluster: dict[str, Any] | None = None


class StartInsightsRefreshResult(BaseModel):
    """Result of start_insights_refresh."""

    model_config = ConfigDict(frozen=True)

    message: str | None = None
    status: str | None = None


class UpdateAccessEntryResult(BaseModel):
    """Result of update_access_entry."""

    model_config = ConfigDict(frozen=True)

    access_entry: dict[str, Any] | None = None


class UpdateEksAnywhereSubscriptionResult(BaseModel):
    """Result of update_eks_anywhere_subscription."""

    model_config = ConfigDict(frozen=True)

    subscription: dict[str, Any] | None = None


class UpdateNodegroupVersionResult(BaseModel):
    """Result of update_nodegroup_version."""

    model_config = ConfigDict(frozen=True)

    update: dict[str, Any] | None = None


class UpdatePodIdentityAssociationResult(BaseModel):
    """Result of update_pod_identity_association."""

    model_config = ConfigDict(frozen=True)

    association: dict[str, Any] | None = None


def associate_access_policy(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    kwargs["policyArn"] = policy_arn
    kwargs["accessScope"] = access_scope
    try:
        resp = client.associate_access_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate access policy") from exc
    return AssociateAccessPolicyResult(
        cluster_name=resp.get("clusterName"),
        principal_arn=resp.get("principalArn"),
        associated_access_policy=resp.get("associatedAccessPolicy"),
    )


def associate_encryption_config(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["encryptionConfig"] = encryption_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.associate_encryption_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate encryption config") from exc
    return AssociateEncryptionConfigResult(
        update=resp.get("update"),
    )


def associate_identity_provider_config(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["oidc"] = oidc
    if tags is not None:
        kwargs["tags"] = tags
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.associate_identity_provider_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to associate identity provider config") from exc
    return AssociateIdentityProviderConfigResult(
        update=resp.get("update"),
        tags=resp.get("tags"),
    )


def create_access_entry(
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
    client = get_client("eks", region_name)
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
        resp = client.create_access_entry(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create access entry") from exc
    return CreateAccessEntryResult(
        access_entry=resp.get("accessEntry"),
    )


def create_eks_anywhere_subscription(
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
    client = get_client("eks", region_name)
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
        resp = client.create_eks_anywhere_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create eks anywhere subscription") from exc
    return CreateEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


def create_pod_identity_association(
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
    client = get_client("eks", region_name)
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
        resp = client.create_pod_identity_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to create pod identity association") from exc
    return CreatePodIdentityAssociationResult(
        association=resp.get("association"),
    )


def delete_access_entry(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    try:
        client.delete_access_entry(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete access entry") from exc
    return None


def delete_eks_anywhere_subscription(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.delete_eks_anywhere_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete eks anywhere subscription") from exc
    return DeleteEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


def delete_pod_identity_association(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["associationId"] = association_id
    try:
        resp = client.delete_pod_identity_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to delete pod identity association") from exc
    return DeletePodIdentityAssociationResult(
        association=resp.get("association"),
    )


def deregister_cluster(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    try:
        resp = client.deregister_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to deregister cluster") from exc
    return DeregisterClusterResult(
        cluster=resp.get("cluster"),
    )


def describe_access_entry(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    try:
        resp = client.describe_access_entry(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe access entry") from exc
    return DescribeAccessEntryResult(
        access_entry=resp.get("accessEntry"),
    )


def describe_addon_configuration(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["addonName"] = addon_name
    kwargs["addonVersion"] = addon_version
    try:
        resp = client.describe_addon_configuration(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe addon configuration") from exc
    return DescribeAddonConfigurationResult(
        addon_name=resp.get("addonName"),
        addon_version=resp.get("addonVersion"),
        configuration_schema=resp.get("configurationSchema"),
        pod_identity_configuration=resp.get("podIdentityConfiguration"),
    )


def describe_addon_versions(
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
    client = get_client("eks", region_name)
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
        resp = client.describe_addon_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe addon versions") from exc
    return DescribeAddonVersionsResult(
        addons=resp.get("addons"),
        next_token=resp.get("nextToken"),
    )


def describe_cluster_versions(
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
    client = get_client("eks", region_name)
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
        resp = client.describe_cluster_versions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster versions") from exc
    return DescribeClusterVersionsResult(
        next_token=resp.get("nextToken"),
        cluster_versions=resp.get("clusterVersions"),
    )


def describe_eks_anywhere_subscription(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    try:
        resp = client.describe_eks_anywhere_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe eks anywhere subscription") from exc
    return DescribeEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


def describe_identity_provider_config(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["identityProviderConfig"] = identity_provider_config
    try:
        resp = client.describe_identity_provider_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe identity provider config") from exc
    return DescribeIdentityProviderConfigResult(
        identity_provider_config=resp.get("identityProviderConfig"),
    )


def describe_insight(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["id"] = id
    try:
        resp = client.describe_insight(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe insight") from exc
    return DescribeInsightResult(
        insight=resp.get("insight"),
    )


def describe_insights_refresh(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    try:
        resp = client.describe_insights_refresh(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe insights refresh") from exc
    return DescribeInsightsRefreshResult(
        message=resp.get("message"),
        status=resp.get("status"),
        started_at=resp.get("startedAt"),
        ended_at=resp.get("endedAt"),
    )


def describe_pod_identity_association(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["associationId"] = association_id
    try:
        resp = client.describe_pod_identity_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe pod identity association") from exc
    return DescribePodIdentityAssociationResult(
        association=resp.get("association"),
    )


def describe_update(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["updateId"] = update_id
    if nodegroup_name is not None:
        kwargs["nodegroupName"] = nodegroup_name
    if addon_name is not None:
        kwargs["addonName"] = addon_name
    try:
        resp = client.describe_update(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to describe update") from exc
    return DescribeUpdateResult(
        update=resp.get("update"),
    )


def disassociate_access_policy(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    kwargs["policyArn"] = policy_arn
    try:
        client.disassociate_access_policy(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate access policy") from exc
    return None


def disassociate_identity_provider_config(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["identityProviderConfig"] = identity_provider_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.disassociate_identity_provider_config(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to disassociate identity provider config") from exc
    return DisassociateIdentityProviderConfigResult(
        update=resp.get("update"),
    )


def list_access_entries(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if associated_policy_arn is not None:
        kwargs["associatedPolicyArn"] = associated_policy_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_access_entries(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list access entries") from exc
    return ListAccessEntriesResult(
        access_entries=resp.get("accessEntries"),
        next_token=resp.get("nextToken"),
    )


def list_access_policies(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_access_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list access policies") from exc
    return ListAccessPoliciesResult(
        access_policies=resp.get("accessPolicies"),
        next_token=resp.get("nextToken"),
    )


def list_associated_access_policies(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    kwargs["principalArn"] = principal_arn
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_associated_access_policies(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list associated access policies") from exc
    return ListAssociatedAccessPoliciesResult(
        cluster_name=resp.get("clusterName"),
        principal_arn=resp.get("principalArn"),
        next_token=resp.get("nextToken"),
        associated_access_policies=resp.get("associatedAccessPolicies"),
    )


def list_eks_anywhere_subscriptions(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    if include_status is not None:
        kwargs["includeStatus"] = include_status
    try:
        resp = client.list_eks_anywhere_subscriptions(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list eks anywhere subscriptions") from exc
    return ListEksAnywhereSubscriptionsResult(
        subscriptions=resp.get("subscriptions"),
        next_token=resp.get("nextToken"),
    )


def list_identity_provider_configs(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_identity_provider_configs(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list identity provider configs") from exc
    return ListIdentityProviderConfigsResult(
        identity_provider_configs=resp.get("identityProviderConfigs"),
        next_token=resp.get("nextToken"),
    )


def list_insights(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    if filter is not None:
        kwargs["filter"] = filter
    if max_results is not None:
        kwargs["maxResults"] = max_results
    if next_token is not None:
        kwargs["nextToken"] = next_token
    try:
        resp = client.list_insights(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list insights") from exc
    return ListInsightsResult(
        insights=resp.get("insights"),
        next_token=resp.get("nextToken"),
    )


def list_pod_identity_associations(
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
    client = get_client("eks", region_name)
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
        resp = client.list_pod_identity_associations(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list pod identity associations") from exc
    return ListPodIdentityAssociationsResult(
        associations=resp.get("associations"),
        next_token=resp.get("nextToken"),
    )


def list_tags_for_resource(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    try:
        resp = client.list_tags_for_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("tags"),
    )


def list_updates(
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
    client = get_client("eks", region_name)
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
        resp = client.list_updates(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to list updates") from exc
    return ListUpdatesResult(
        update_ids=resp.get("updateIds"),
        next_token=resp.get("nextToken"),
    )


def register_cluster(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["name"] = name
    kwargs["connectorConfig"] = connector_config
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    if tags is not None:
        kwargs["tags"] = tags
    try:
        resp = client.register_cluster(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to register cluster") from exc
    return RegisterClusterResult(
        cluster=resp.get("cluster"),
    )


def start_insights_refresh(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["clusterName"] = cluster_name
    try:
        resp = client.start_insights_refresh(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to start insights refresh") from exc
    return StartInsightsRefreshResult(
        message=resp.get("message"),
        status=resp.get("status"),
    )


def tag_resource(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tags"] = tags
    try:
        client.tag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


def untag_resource(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["resourceArn"] = resource_arn
    kwargs["tagKeys"] = tag_keys
    try:
        client.untag_resource(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


def update_access_entry(
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
    client = get_client("eks", region_name)
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
        resp = client.update_access_entry(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update access entry") from exc
    return UpdateAccessEntryResult(
        access_entry=resp.get("accessEntry"),
    )


def update_eks_anywhere_subscription(
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
    client = get_client("eks", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["id"] = id
    kwargs["autoRenew"] = auto_renew
    if client_request_token is not None:
        kwargs["clientRequestToken"] = client_request_token
    try:
        resp = client.update_eks_anywhere_subscription(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update eks anywhere subscription") from exc
    return UpdateEksAnywhereSubscriptionResult(
        subscription=resp.get("subscription"),
    )


def update_nodegroup_version(
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
    client = get_client("eks", region_name)
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
        resp = client.update_nodegroup_version(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update nodegroup version") from exc
    return UpdateNodegroupVersionResult(
        update=resp.get("update"),
    )


def update_pod_identity_association(
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
    client = get_client("eks", region_name)
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
        resp = client.update_pod_identity_association(**kwargs)
    except ClientError as exc:
        raise wrap_aws_error(exc, "Failed to update pod identity association") from exc
    return UpdatePodIdentityAssociationResult(
        association=resp.get("association"),
    )
