"""Native async MSK utilities using :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsTimeoutError, wrap_aws_error
from aws_util.msk import (
    BatchAssociateScramSecretResult,
    BatchDisassociateScramSecretResult,
    ClusterResult,
    ConfigurationResult,
    CreateClusterV2Result,
    CreateReplicatorResult,
    CreateVpcConnectionResult,
    DeleteConfigurationResult,
    DeleteReplicatorResult,
    DeleteVpcConnectionResult,
    DescribeClusterOperationResult,
    DescribeClusterOperationV2Result,
    DescribeClusterV2Result,
    DescribeConfigurationResult,
    DescribeConfigurationRevisionResult,
    DescribeReplicatorResult,
    DescribeVpcConnectionResult,
    GetClusterPolicyResult,
    GetCompatibleKafkaVersionsResult,
    ListClientVpcConnectionsResult,
    ListClusterOperationsResult,
    ListClusterOperationsV2Result,
    ListClustersV2Result,
    ListConfigurationRevisionsResult,
    ListKafkaVersionsResult,
    ListReplicatorsResult,
    ListScramSecretsResult,
    ListTagsForResourceResult,
    ListVpcConnectionsResult,
    NodeResult,
    PutClusterPolicyResult,
    RebootBrokerResult,
    UpdateBrokerTypeResult,
    UpdateClusterKafkaVersionResult,
    UpdateConfigurationResult,
    UpdateConnectivityResult,
    UpdateMonitoringResult,
    UpdateRebalancingResult,
    UpdateReplicationInfoResult,
    UpdateSecurityResult,
    UpdateStorageResult,
    _parse_cluster,
    _parse_configuration,
    _parse_node,
)

__all__ = [
    "BatchAssociateScramSecretResult",
    "BatchDisassociateScramSecretResult",
    "ClusterResult",
    "ConfigurationResult",
    "CreateClusterV2Result",
    "CreateReplicatorResult",
    "CreateVpcConnectionResult",
    "DeleteConfigurationResult",
    "DeleteReplicatorResult",
    "DeleteVpcConnectionResult",
    "DescribeClusterOperationResult",
    "DescribeClusterOperationV2Result",
    "DescribeClusterV2Result",
    "DescribeConfigurationResult",
    "DescribeConfigurationRevisionResult",
    "DescribeReplicatorResult",
    "DescribeVpcConnectionResult",
    "GetClusterPolicyResult",
    "GetCompatibleKafkaVersionsResult",
    "ListClientVpcConnectionsResult",
    "ListClusterOperationsResult",
    "ListClusterOperationsV2Result",
    "ListClustersV2Result",
    "ListConfigurationRevisionsResult",
    "ListKafkaVersionsResult",
    "ListReplicatorsResult",
    "ListScramSecretsResult",
    "ListTagsForResourceResult",
    "ListVpcConnectionsResult",
    "NodeResult",
    "PutClusterPolicyResult",
    "RebootBrokerResult",
    "UpdateBrokerTypeResult",
    "UpdateClusterKafkaVersionResult",
    "UpdateConfigurationResult",
    "UpdateConnectivityResult",
    "UpdateMonitoringResult",
    "UpdateRebalancingResult",
    "UpdateReplicationInfoResult",
    "UpdateSecurityResult",
    "UpdateStorageResult",
    "batch_associate_scram_secret",
    "batch_disassociate_scram_secret",
    "create_cluster",
    "create_cluster_v2",
    "create_configuration",
    "create_replicator",
    "create_vpc_connection",
    "delete_cluster",
    "delete_cluster_policy",
    "delete_configuration",
    "delete_replicator",
    "delete_vpc_connection",
    "describe_cluster",
    "describe_cluster_operation",
    "describe_cluster_operation_v2",
    "describe_cluster_v2",
    "describe_configuration",
    "describe_configuration_revision",
    "describe_replicator",
    "describe_vpc_connection",
    "get_bootstrap_brokers",
    "get_cluster_policy",
    "get_compatible_kafka_versions",
    "list_client_vpc_connections",
    "list_cluster_operations",
    "list_cluster_operations_v2",
    "list_clusters",
    "list_clusters_v2",
    "list_configuration_revisions",
    "list_configurations",
    "list_kafka_versions",
    "list_nodes",
    "list_replicators",
    "list_scram_secrets",
    "list_tags_for_resource",
    "list_vpc_connections",
    "put_cluster_policy",
    "reboot_broker",
    "reject_client_vpc_connection",
    "tag_resource",
    "untag_resource",
    "update_broker_count",
    "update_broker_storage",
    "update_broker_type",
    "update_cluster_configuration",
    "update_cluster_kafka_version",
    "update_configuration",
    "update_connectivity",
    "update_monitoring",
    "update_rebalancing",
    "update_replication_info",
    "update_security",
    "update_storage",
    "wait_for_cluster",
]


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


async def create_cluster(
    cluster_name: str,
    *,
    kafka_version: str,
    number_of_broker_nodes: int,
    broker_node_group_info: dict[str, Any],
    encryption_info: dict[str, Any] | None = None,
    tags: dict[str, str] | None = None,
    region_name: str | None = None,
) -> ClusterResult:
    """Create an MSK cluster.

    Args:
        cluster_name: Name for the new cluster.
        kafka_version: Apache Kafka version (e.g. ``"2.8.1"``).
        number_of_broker_nodes: Number of broker nodes in the cluster.
        broker_node_group_info: Broker node configuration dict.
        encryption_info: Optional encryption configuration.
        tags: Optional resource tags.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult` for the new cluster.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {
        "ClusterName": cluster_name,
        "KafkaVersion": kafka_version,
        "NumberOfBrokerNodes": number_of_broker_nodes,
        "BrokerNodeGroupInfo": broker_node_group_info,
    }
    if encryption_info is not None:
        kwargs["EncryptionInfo"] = encryption_info
    if tags is not None:
        kwargs["Tags"] = tags

    try:
        resp = await client.call("CreateCluster", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_cluster failed for {cluster_name!r}") from exc
    return ClusterResult(
        cluster_name=cluster_name,
        cluster_arn=resp.get("ClusterArn", ""),
        state=resp.get("State", "CREATING"),
    )


async def describe_cluster(
    cluster_arn: str,
    *,
    region_name: str | None = None,
) -> ClusterResult:
    """Describe an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        region_name: AWS region override.

    Returns:
        A :class:`ClusterResult`.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        resp = await client.call("DescribeCluster", ClusterArn=cluster_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"describe_cluster failed for {cluster_arn!r}") from exc
    return _parse_cluster(resp.get("ClusterInfo", {}))


async def list_clusters(
    *,
    region_name: str | None = None,
) -> list[ClusterResult]:
    """List all MSK clusters in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ClusterResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        items = await client.paginate("ListClusters", "ClusterInfoList")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_clusters failed") from exc
    return [_parse_cluster(item) for item in items]


async def delete_cluster(
    cluster_arn: str,
    *,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Delete an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        region_name: AWS region override.

    Returns:
        The raw delete response dict containing cluster_arn and state.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        resp = await client.call("DeleteCluster", ClusterArn=cluster_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"delete_cluster failed for {cluster_arn!r}") from exc
    return {
        "cluster_arn": resp.get("ClusterArn", ""),
        "state": resp.get("State", ""),
    }


# ---------------------------------------------------------------------------
# Broker operations
# ---------------------------------------------------------------------------


async def update_broker_count(
    cluster_arn: str,
    *,
    target_number_of_broker_nodes: int,
    current_version: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update the number of broker nodes in an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        target_number_of_broker_nodes: Desired broker count.
        current_version: Current cluster version string.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        resp = await client.call(
            "UpdateBrokerCount",
            ClusterArn=cluster_arn,
            CurrentVersion=current_version,
            TargetNumberOfBrokerNodes=target_number_of_broker_nodes,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_broker_count failed for {cluster_arn!r}") from exc
    return {
        "cluster_arn": resp.get("ClusterArn", ""),
        "cluster_operation_arn": resp.get("ClusterOperationArn", ""),
    }


async def update_broker_storage(
    cluster_arn: str,
    *,
    target_broker_ebs_volume_info: list[dict[str, Any]],
    current_version: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update the EBS storage for broker nodes in an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        target_broker_ebs_volume_info: List of EBS volume info dicts.
        current_version: Current cluster version string.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        resp = await client.call(
            "UpdateBrokerStorage",
            ClusterArn=cluster_arn,
            CurrentVersion=current_version,
            TargetBrokerEBSVolumeInfo=target_broker_ebs_volume_info,
        )
    except Exception as exc:
        raise wrap_aws_error(exc, f"update_broker_storage failed for {cluster_arn!r}") from exc
    return {
        "cluster_arn": resp.get("ClusterArn", ""),
        "cluster_operation_arn": resp.get("ClusterOperationArn", ""),
    }


async def update_cluster_configuration(
    cluster_arn: str,
    *,
    configuration_info: dict[str, Any],
    current_version: str,
    region_name: str | None = None,
) -> dict[str, Any]:
    """Update the configuration of an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        configuration_info: Configuration info dict with Arn and Revision.
        current_version: Current cluster version string.
        region_name: AWS region override.

    Returns:
        The raw update response dict.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        resp = await client.call(
            "UpdateClusterConfiguration",
            ClusterArn=cluster_arn,
            CurrentVersion=current_version,
            ConfigurationInfo=configuration_info,
        )
    except Exception as exc:
        raise wrap_aws_error(
            exc,
            f"update_cluster_configuration failed for {cluster_arn!r}",
        ) from exc
    return {
        "cluster_arn": resp.get("ClusterArn", ""),
        "cluster_operation_arn": resp.get("ClusterOperationArn", ""),
    }


# ---------------------------------------------------------------------------
# Node operations
# ---------------------------------------------------------------------------


async def list_nodes(
    cluster_arn: str,
    *,
    region_name: str | None = None,
) -> list[NodeResult]:
    """List broker nodes for an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        region_name: AWS region override.

    Returns:
        A list of :class:`NodeResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        items = await client.paginate("ListNodes", "NodeInfoList", ClusterArn=cluster_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, "list_nodes failed") from exc
    return [_parse_node(item) for item in items]


# ---------------------------------------------------------------------------
# Bootstrap brokers
# ---------------------------------------------------------------------------


async def get_bootstrap_brokers(
    cluster_arn: str,
    *,
    region_name: str | None = None,
) -> dict[str, str | None]:
    """Get the bootstrap broker connection strings for an MSK cluster.

    Args:
        cluster_arn: ARN of the MSK cluster.
        region_name: AWS region override.

    Returns:
        A dict with bootstrap broker connection strings by protocol.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        resp = await client.call("GetBootstrapBrokers", ClusterArn=cluster_arn)
    except Exception as exc:
        raise wrap_aws_error(exc, f"get_bootstrap_brokers failed for {cluster_arn!r}") from exc
    return {
        "bootstrap_broker_string": resp.get("BootstrapBrokerString"),
        "bootstrap_broker_string_tls": resp.get("BootstrapBrokerStringTls"),
        "bootstrap_broker_string_sasl_scram": resp.get("BootstrapBrokerStringSaslScram"),
        "bootstrap_broker_string_sasl_iam": resp.get("BootstrapBrokerStringSaslIam"),
        "bootstrap_broker_string_public_tls": resp.get("BootstrapBrokerStringPublicTls"),
        "bootstrap_broker_string_public_sasl_scram": resp.get(
            "BootstrapBrokerStringPublicSaslScram"
        ),
        "bootstrap_broker_string_public_sasl_iam": resp.get("BootstrapBrokerStringPublicSaslIam"),
    }


# ---------------------------------------------------------------------------
# Configuration operations
# ---------------------------------------------------------------------------


async def create_configuration(
    name: str,
    *,
    server_properties: str,
    kafka_versions: list[str],
    description: str | None = None,
    region_name: str | None = None,
) -> ConfigurationResult:
    """Create an MSK configuration.

    Args:
        name: Name for the new configuration.
        server_properties: Contents of the server.properties file.
        kafka_versions: List of compatible Apache Kafka versions.
        description: Optional description.
        region_name: AWS region override.

    Returns:
        A :class:`ConfigurationResult` for the new configuration.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {
        "Name": name,
        "ServerProperties": server_properties.encode("utf-8"),
        "KafkaVersions": kafka_versions,
    }
    if description is not None:
        kwargs["Description"] = description

    try:
        resp = await client.call("CreateConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, f"create_configuration failed for {name!r}") from exc
    created = resp.get("CreationTime")
    return ConfigurationResult(
        arn=resp.get("Arn", ""),
        name=resp.get("Name", name),
        creation_time=str(created) if created is not None else None,
        latest_revision=resp.get("LatestRevision", {}),
        state=resp.get("State"),
    )


async def list_configurations(
    *,
    region_name: str | None = None,
) -> list[ConfigurationResult]:
    """List all MSK configurations in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of :class:`ConfigurationResult` objects.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    try:
        items = await client.paginate("ListConfigurations", "Configurations")
    except Exception as exc:
        raise wrap_aws_error(exc, "list_configurations failed") from exc
    return [_parse_configuration(item) for item in items]


# ---------------------------------------------------------------------------
# Waiters
# ---------------------------------------------------------------------------


async def wait_for_cluster(
    cluster_arn: str,
    *,
    target_state: str = "ACTIVE",
    timeout: float = 600,
    poll_interval: float = 30,
    region_name: str | None = None,
) -> ClusterResult:
    """Poll until an MSK cluster reaches a desired state.

    Args:
        cluster_arn: ARN of the MSK cluster.
        target_state: State to wait for (default ``"ACTIVE"``).
        timeout: Maximum seconds to wait (default ``600``).
        poll_interval: Seconds between checks (default ``30``).
        region_name: AWS region override.

    Returns:
        The :class:`ClusterResult` in the target state.

    Raises:
        AwsTimeoutError: If the cluster does not reach the target state.
    """
    deadline = time.monotonic() + timeout
    while True:
        cluster = await describe_cluster(cluster_arn, region_name=region_name)
        if cluster.state == target_state:
            return cluster
        if time.monotonic() >= deadline:
            raise AwsTimeoutError(
                f"Cluster {cluster_arn!r} did not reach state "
                f"{target_state!r} within {timeout}s "
                f"(current: {cluster.state!r})"
            )
        await asyncio.sleep(poll_interval)


async def batch_associate_scram_secret(
    cluster_arn: str,
    secret_arn_list: list[str],
    region_name: str | None = None,
) -> BatchAssociateScramSecretResult:
    """Batch associate scram secret.

    Args:
        cluster_arn: Cluster arn.
        secret_arn_list: Secret arn list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["SecretArnList"] = secret_arn_list
    try:
        resp = await client.call("BatchAssociateScramSecret", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch associate scram secret") from exc
    return BatchAssociateScramSecretResult(
        cluster_arn=resp.get("ClusterArn"),
        unprocessed_scram_secrets=resp.get("UnprocessedScramSecrets"),
    )


async def batch_disassociate_scram_secret(
    cluster_arn: str,
    secret_arn_list: list[str],
    region_name: str | None = None,
) -> BatchDisassociateScramSecretResult:
    """Batch disassociate scram secret.

    Args:
        cluster_arn: Cluster arn.
        secret_arn_list: Secret arn list.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["SecretArnList"] = secret_arn_list
    try:
        resp = await client.call("BatchDisassociateScramSecret", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to batch disassociate scram secret") from exc
    return BatchDisassociateScramSecretResult(
        cluster_arn=resp.get("ClusterArn"),
        unprocessed_scram_secrets=resp.get("UnprocessedScramSecrets"),
    )


async def create_cluster_v2(
    cluster_name: str,
    *,
    tags: dict[str, Any] | None = None,
    provisioned: dict[str, Any] | None = None,
    serverless: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateClusterV2Result:
    """Create cluster v2.

    Args:
        cluster_name: Cluster name.
        tags: Tags.
        provisioned: Provisioned.
        serverless: Serverless.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterName"] = cluster_name
    if tags is not None:
        kwargs["Tags"] = tags
    if provisioned is not None:
        kwargs["Provisioned"] = provisioned
    if serverless is not None:
        kwargs["Serverless"] = serverless
    try:
        resp = await client.call("CreateClusterV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create cluster v2") from exc
    return CreateClusterV2Result(
        cluster_arn=resp.get("ClusterArn"),
        cluster_name=resp.get("ClusterName"),
        state=resp.get("State"),
        cluster_type=resp.get("ClusterType"),
    )


async def create_replicator(
    kafka_clusters: list[dict[str, Any]],
    replication_info_list: list[dict[str, Any]],
    replicator_name: str,
    service_execution_role_arn: str,
    *,
    description: str | None = None,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateReplicatorResult:
    """Create replicator.

    Args:
        kafka_clusters: Kafka clusters.
        replication_info_list: Replication info list.
        replicator_name: Replicator name.
        service_execution_role_arn: Service execution role arn.
        description: Description.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["KafkaClusters"] = kafka_clusters
    kwargs["ReplicationInfoList"] = replication_info_list
    kwargs["ReplicatorName"] = replicator_name
    kwargs["ServiceExecutionRoleArn"] = service_execution_role_arn
    if description is not None:
        kwargs["Description"] = description
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateReplicator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create replicator") from exc
    return CreateReplicatorResult(
        replicator_arn=resp.get("ReplicatorArn"),
        replicator_name=resp.get("ReplicatorName"),
        replicator_state=resp.get("ReplicatorState"),
    )


async def create_vpc_connection(
    target_cluster_arn: str,
    authentication: str,
    vpc_id: str,
    client_subnets: list[str],
    security_groups: list[str],
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateVpcConnectionResult:
    """Create vpc connection.

    Args:
        target_cluster_arn: Target cluster arn.
        authentication: Authentication.
        vpc_id: Vpc id.
        client_subnets: Client subnets.
        security_groups: Security groups.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetClusterArn"] = target_cluster_arn
    kwargs["Authentication"] = authentication
    kwargs["VpcId"] = vpc_id
    kwargs["ClientSubnets"] = client_subnets
    kwargs["SecurityGroups"] = security_groups
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("CreateVpcConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create vpc connection") from exc
    return CreateVpcConnectionResult(
        vpc_connection_arn=resp.get("VpcConnectionArn"),
        state=resp.get("State"),
        authentication=resp.get("Authentication"),
        vpc_id=resp.get("VpcId"),
        client_subnets=resp.get("ClientSubnets"),
        security_groups=resp.get("SecurityGroups"),
        creation_time=resp.get("CreationTime"),
        tags=resp.get("Tags"),
    )


async def delete_cluster_policy(
    cluster_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete cluster policy.

    Args:
        cluster_arn: Cluster arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    try:
        await client.call("DeleteClusterPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete cluster policy") from exc
    return None


async def delete_configuration(
    arn: str,
    region_name: str | None = None,
) -> DeleteConfigurationResult:
    """Delete configuration.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = await client.call("DeleteConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete configuration") from exc
    return DeleteConfigurationResult(
        arn=resp.get("Arn"),
        state=resp.get("State"),
    )


async def delete_replicator(
    replicator_arn: str,
    *,
    current_version: str | None = None,
    region_name: str | None = None,
) -> DeleteReplicatorResult:
    """Delete replicator.

    Args:
        replicator_arn: Replicator arn.
        current_version: Current version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicatorArn"] = replicator_arn
    if current_version is not None:
        kwargs["CurrentVersion"] = current_version
    try:
        resp = await client.call("DeleteReplicator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete replicator") from exc
    return DeleteReplicatorResult(
        replicator_arn=resp.get("ReplicatorArn"),
        replicator_state=resp.get("ReplicatorState"),
    )


async def delete_vpc_connection(
    arn: str,
    region_name: str | None = None,
) -> DeleteVpcConnectionResult:
    """Delete vpc connection.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = await client.call("DeleteVpcConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete vpc connection") from exc
    return DeleteVpcConnectionResult(
        vpc_connection_arn=resp.get("VpcConnectionArn"),
        state=resp.get("State"),
    )


async def describe_cluster_operation(
    cluster_operation_arn: str,
    region_name: str | None = None,
) -> DescribeClusterOperationResult:
    """Describe cluster operation.

    Args:
        cluster_operation_arn: Cluster operation arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterOperationArn"] = cluster_operation_arn
    try:
        resp = await client.call("DescribeClusterOperation", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster operation") from exc
    return DescribeClusterOperationResult(
        cluster_operation_info=resp.get("ClusterOperationInfo"),
    )


async def describe_cluster_operation_v2(
    cluster_operation_arn: str,
    region_name: str | None = None,
) -> DescribeClusterOperationV2Result:
    """Describe cluster operation v2.

    Args:
        cluster_operation_arn: Cluster operation arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterOperationArn"] = cluster_operation_arn
    try:
        resp = await client.call("DescribeClusterOperationV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster operation v2") from exc
    return DescribeClusterOperationV2Result(
        cluster_operation_info=resp.get("ClusterOperationInfo"),
    )


async def describe_cluster_v2(
    cluster_arn: str,
    region_name: str | None = None,
) -> DescribeClusterV2Result:
    """Describe cluster v2.

    Args:
        cluster_arn: Cluster arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    try:
        resp = await client.call("DescribeClusterV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe cluster v2") from exc
    return DescribeClusterV2Result(
        cluster_info=resp.get("ClusterInfo"),
    )


async def describe_configuration(
    arn: str,
    region_name: str | None = None,
) -> DescribeConfigurationResult:
    """Describe configuration.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = await client.call("DescribeConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe configuration") from exc
    return DescribeConfigurationResult(
        arn=resp.get("Arn"),
        creation_time=resp.get("CreationTime"),
        description=resp.get("Description"),
        kafka_versions=resp.get("KafkaVersions"),
        latest_revision=resp.get("LatestRevision"),
        name=resp.get("Name"),
        state=resp.get("State"),
    )


async def describe_configuration_revision(
    arn: str,
    revision: int,
    region_name: str | None = None,
) -> DescribeConfigurationRevisionResult:
    """Describe configuration revision.

    Args:
        arn: Arn.
        revision: Revision.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["Revision"] = revision
    try:
        resp = await client.call("DescribeConfigurationRevision", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe configuration revision") from exc
    return DescribeConfigurationRevisionResult(
        arn=resp.get("Arn"),
        creation_time=resp.get("CreationTime"),
        description=resp.get("Description"),
        revision=resp.get("Revision"),
        server_properties=resp.get("ServerProperties"),
    )


async def describe_replicator(
    replicator_arn: str,
    region_name: str | None = None,
) -> DescribeReplicatorResult:
    """Describe replicator.

    Args:
        replicator_arn: Replicator arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ReplicatorArn"] = replicator_arn
    try:
        resp = await client.call("DescribeReplicator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe replicator") from exc
    return DescribeReplicatorResult(
        creation_time=resp.get("CreationTime"),
        current_version=resp.get("CurrentVersion"),
        is_replicator_reference=resp.get("IsReplicatorReference"),
        kafka_clusters=resp.get("KafkaClusters"),
        replication_info_list=resp.get("ReplicationInfoList"),
        replicator_arn=resp.get("ReplicatorArn"),
        replicator_description=resp.get("ReplicatorDescription"),
        replicator_name=resp.get("ReplicatorName"),
        replicator_resource_arn=resp.get("ReplicatorResourceArn"),
        replicator_state=resp.get("ReplicatorState"),
        service_execution_role_arn=resp.get("ServiceExecutionRoleArn"),
        state_info=resp.get("StateInfo"),
        tags=resp.get("Tags"),
    )


async def describe_vpc_connection(
    arn: str,
    region_name: str | None = None,
) -> DescribeVpcConnectionResult:
    """Describe vpc connection.

    Args:
        arn: Arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    try:
        resp = await client.call("DescribeVpcConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe vpc connection") from exc
    return DescribeVpcConnectionResult(
        vpc_connection_arn=resp.get("VpcConnectionArn"),
        target_cluster_arn=resp.get("TargetClusterArn"),
        state=resp.get("State"),
        authentication=resp.get("Authentication"),
        vpc_id=resp.get("VpcId"),
        subnets=resp.get("Subnets"),
        security_groups=resp.get("SecurityGroups"),
        creation_time=resp.get("CreationTime"),
        tags=resp.get("Tags"),
    )


async def get_cluster_policy(
    cluster_arn: str,
    region_name: str | None = None,
) -> GetClusterPolicyResult:
    """Get cluster policy.

    Args:
        cluster_arn: Cluster arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    try:
        resp = await client.call("GetClusterPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get cluster policy") from exc
    return GetClusterPolicyResult(
        current_version=resp.get("CurrentVersion"),
        policy=resp.get("Policy"),
    )


async def get_compatible_kafka_versions(
    *,
    cluster_arn: str | None = None,
    region_name: str | None = None,
) -> GetCompatibleKafkaVersionsResult:
    """Get compatible kafka versions.

    Args:
        cluster_arn: Cluster arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_arn is not None:
        kwargs["ClusterArn"] = cluster_arn
    try:
        resp = await client.call("GetCompatibleKafkaVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get compatible kafka versions") from exc
    return GetCompatibleKafkaVersionsResult(
        compatible_kafka_versions=resp.get("CompatibleKafkaVersions"),
    )


async def list_client_vpc_connections(
    cluster_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListClientVpcConnectionsResult:
    """List client vpc connections.

    Args:
        cluster_arn: Cluster arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListClientVpcConnections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list client vpc connections") from exc
    return ListClientVpcConnectionsResult(
        client_vpc_connections=resp.get("ClientVpcConnections"),
        next_token=resp.get("NextToken"),
    )


async def list_cluster_operations(
    cluster_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListClusterOperationsResult:
    """List cluster operations.

    Args:
        cluster_arn: Cluster arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListClusterOperations", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cluster operations") from exc
    return ListClusterOperationsResult(
        cluster_operation_info_list=resp.get("ClusterOperationInfoList"),
        next_token=resp.get("NextToken"),
    )


async def list_cluster_operations_v2(
    cluster_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListClusterOperationsV2Result:
    """List cluster operations v2.

    Args:
        cluster_arn: Cluster arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListClusterOperationsV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list cluster operations v2") from exc
    return ListClusterOperationsV2Result(
        cluster_operation_info_list=resp.get("ClusterOperationInfoList"),
        next_token=resp.get("NextToken"),
    )


async def list_clusters_v2(
    *,
    cluster_name_filter: str | None = None,
    cluster_type_filter: str | None = None,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListClustersV2Result:
    """List clusters v2.

    Args:
        cluster_name_filter: Cluster name filter.
        cluster_type_filter: Cluster type filter.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    if cluster_name_filter is not None:
        kwargs["ClusterNameFilter"] = cluster_name_filter
    if cluster_type_filter is not None:
        kwargs["ClusterTypeFilter"] = cluster_type_filter
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListClustersV2", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list clusters v2") from exc
    return ListClustersV2Result(
        cluster_info_list=resp.get("ClusterInfoList"),
        next_token=resp.get("NextToken"),
    )


async def list_configuration_revisions(
    arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListConfigurationRevisionsResult:
    """List configuration revisions.

    Args:
        arn: Arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListConfigurationRevisions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list configuration revisions") from exc
    return ListConfigurationRevisionsResult(
        next_token=resp.get("NextToken"),
        revisions=resp.get("Revisions"),
    )


async def list_kafka_versions(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListKafkaVersionsResult:
    """List kafka versions.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListKafkaVersions", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list kafka versions") from exc
    return ListKafkaVersionsResult(
        kafka_versions=resp.get("KafkaVersions"),
        next_token=resp.get("NextToken"),
    )


async def list_replicators(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    replicator_name_filter: str | None = None,
    region_name: str | None = None,
) -> ListReplicatorsResult:
    """List replicators.

    Args:
        max_results: Max results.
        next_token: Next token.
        replicator_name_filter: Replicator name filter.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if replicator_name_filter is not None:
        kwargs["ReplicatorNameFilter"] = replicator_name_filter
    try:
        resp = await client.call("ListReplicators", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list replicators") from exc
    return ListReplicatorsResult(
        next_token=resp.get("NextToken"),
        replicators=resp.get("Replicators"),
    )


async def list_scram_secrets(
    cluster_arn: str,
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListScramSecretsResult:
    """List scram secrets.

    Args:
        cluster_arn: Cluster arn.
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListScramSecrets", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list scram secrets") from exc
    return ListScramSecretsResult(
        next_token=resp.get("NextToken"),
        secret_arn_list=resp.get("SecretArnList"),
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
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_vpc_connections(
    *,
    max_results: int | None = None,
    next_token: str | None = None,
    region_name: str | None = None,
) -> ListVpcConnectionsResult:
    """List vpc connections.

    Args:
        max_results: Max results.
        next_token: Next token.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if next_token is not None:
        kwargs["NextToken"] = next_token
    try:
        resp = await client.call("ListVpcConnections", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list vpc connections") from exc
    return ListVpcConnectionsResult(
        vpc_connections=resp.get("VpcConnections"),
        next_token=resp.get("NextToken"),
    )


async def put_cluster_policy(
    cluster_arn: str,
    policy: str,
    *,
    current_version: str | None = None,
    region_name: str | None = None,
) -> PutClusterPolicyResult:
    """Put cluster policy.

    Args:
        cluster_arn: Cluster arn.
        policy: Policy.
        current_version: Current version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["Policy"] = policy
    if current_version is not None:
        kwargs["CurrentVersion"] = current_version
    try:
        resp = await client.call("PutClusterPolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put cluster policy") from exc
    return PutClusterPolicyResult(
        current_version=resp.get("CurrentVersion"),
    )


async def reboot_broker(
    broker_ids: list[str],
    cluster_arn: str,
    region_name: str | None = None,
) -> RebootBrokerResult:
    """Reboot broker.

    Args:
        broker_ids: Broker ids.
        cluster_arn: Cluster arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["BrokerIds"] = broker_ids
    kwargs["ClusterArn"] = cluster_arn
    try:
        resp = await client.call("RebootBroker", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reboot broker") from exc
    return RebootBrokerResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def reject_client_vpc_connection(
    cluster_arn: str,
    vpc_connection_arn: str,
    region_name: str | None = None,
) -> None:
    """Reject client vpc connection.

    Args:
        cluster_arn: Cluster arn.
        vpc_connection_arn: Vpc connection arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["VpcConnectionArn"] = vpc_connection_arn
    try:
        await client.call("RejectClientVpcConnection", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to reject client vpc connection") from exc
    return None


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
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["Tags"] = tags
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
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceArn"] = resource_arn
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_broker_type(
    cluster_arn: str,
    current_version: str,
    target_instance_type: str,
    region_name: str | None = None,
) -> UpdateBrokerTypeResult:
    """Update broker type.

    Args:
        cluster_arn: Cluster arn.
        current_version: Current version.
        target_instance_type: Target instance type.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["CurrentVersion"] = current_version
    kwargs["TargetInstanceType"] = target_instance_type
    try:
        resp = await client.call("UpdateBrokerType", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update broker type") from exc
    return UpdateBrokerTypeResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def update_cluster_kafka_version(
    cluster_arn: str,
    current_version: str,
    target_kafka_version: str,
    *,
    configuration_info: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateClusterKafkaVersionResult:
    """Update cluster kafka version.

    Args:
        cluster_arn: Cluster arn.
        current_version: Current version.
        target_kafka_version: Target kafka version.
        configuration_info: Configuration info.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["CurrentVersion"] = current_version
    kwargs["TargetKafkaVersion"] = target_kafka_version
    if configuration_info is not None:
        kwargs["ConfigurationInfo"] = configuration_info
    try:
        resp = await client.call("UpdateClusterKafkaVersion", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update cluster kafka version") from exc
    return UpdateClusterKafkaVersionResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def update_configuration(
    arn: str,
    server_properties: bytes,
    *,
    description: str | None = None,
    region_name: str | None = None,
) -> UpdateConfigurationResult:
    """Update configuration.

    Args:
        arn: Arn.
        server_properties: Server properties.
        description: Description.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Arn"] = arn
    kwargs["ServerProperties"] = server_properties
    if description is not None:
        kwargs["Description"] = description
    try:
        resp = await client.call("UpdateConfiguration", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update configuration") from exc
    return UpdateConfigurationResult(
        arn=resp.get("Arn"),
        latest_revision=resp.get("LatestRevision"),
    )


async def update_connectivity(
    cluster_arn: str,
    connectivity_info: dict[str, Any],
    current_version: str,
    region_name: str | None = None,
) -> UpdateConnectivityResult:
    """Update connectivity.

    Args:
        cluster_arn: Cluster arn.
        connectivity_info: Connectivity info.
        current_version: Current version.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["ConnectivityInfo"] = connectivity_info
    kwargs["CurrentVersion"] = current_version
    try:
        resp = await client.call("UpdateConnectivity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update connectivity") from exc
    return UpdateConnectivityResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def update_monitoring(
    cluster_arn: str,
    current_version: str,
    *,
    enhanced_monitoring: str | None = None,
    open_monitoring: dict[str, Any] | None = None,
    logging_info: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateMonitoringResult:
    """Update monitoring.

    Args:
        cluster_arn: Cluster arn.
        current_version: Current version.
        enhanced_monitoring: Enhanced monitoring.
        open_monitoring: Open monitoring.
        logging_info: Logging info.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["CurrentVersion"] = current_version
    if enhanced_monitoring is not None:
        kwargs["EnhancedMonitoring"] = enhanced_monitoring
    if open_monitoring is not None:
        kwargs["OpenMonitoring"] = open_monitoring
    if logging_info is not None:
        kwargs["LoggingInfo"] = logging_info
    try:
        resp = await client.call("UpdateMonitoring", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update monitoring") from exc
    return UpdateMonitoringResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def update_rebalancing(
    cluster_arn: str,
    current_version: str,
    rebalancing: dict[str, Any],
    region_name: str | None = None,
) -> UpdateRebalancingResult:
    """Update rebalancing.

    Args:
        cluster_arn: Cluster arn.
        current_version: Current version.
        rebalancing: Rebalancing.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["CurrentVersion"] = current_version
    kwargs["Rebalancing"] = rebalancing
    try:
        resp = await client.call("UpdateRebalancing", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update rebalancing") from exc
    return UpdateRebalancingResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def update_replication_info(
    current_version: str,
    replicator_arn: str,
    source_kafka_cluster_arn: str,
    target_kafka_cluster_arn: str,
    *,
    consumer_group_replication: dict[str, Any] | None = None,
    topic_replication: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateReplicationInfoResult:
    """Update replication info.

    Args:
        current_version: Current version.
        replicator_arn: Replicator arn.
        source_kafka_cluster_arn: Source kafka cluster arn.
        target_kafka_cluster_arn: Target kafka cluster arn.
        consumer_group_replication: Consumer group replication.
        topic_replication: Topic replication.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["CurrentVersion"] = current_version
    kwargs["ReplicatorArn"] = replicator_arn
    kwargs["SourceKafkaClusterArn"] = source_kafka_cluster_arn
    kwargs["TargetKafkaClusterArn"] = target_kafka_cluster_arn
    if consumer_group_replication is not None:
        kwargs["ConsumerGroupReplication"] = consumer_group_replication
    if topic_replication is not None:
        kwargs["TopicReplication"] = topic_replication
    try:
        resp = await client.call("UpdateReplicationInfo", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update replication info") from exc
    return UpdateReplicationInfoResult(
        replicator_arn=resp.get("ReplicatorArn"),
        replicator_state=resp.get("ReplicatorState"),
    )


async def update_security(
    cluster_arn: str,
    current_version: str,
    *,
    client_authentication: dict[str, Any] | None = None,
    encryption_info: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> UpdateSecurityResult:
    """Update security.

    Args:
        cluster_arn: Cluster arn.
        current_version: Current version.
        client_authentication: Client authentication.
        encryption_info: Encryption info.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["CurrentVersion"] = current_version
    if client_authentication is not None:
        kwargs["ClientAuthentication"] = client_authentication
    if encryption_info is not None:
        kwargs["EncryptionInfo"] = encryption_info
    try:
        resp = await client.call("UpdateSecurity", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update security") from exc
    return UpdateSecurityResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )


async def update_storage(
    cluster_arn: str,
    current_version: str,
    *,
    provisioned_throughput: dict[str, Any] | None = None,
    storage_mode: str | None = None,
    volume_size_gb: int | None = None,
    region_name: str | None = None,
) -> UpdateStorageResult:
    """Update storage.

    Args:
        cluster_arn: Cluster arn.
        current_version: Current version.
        provisioned_throughput: Provisioned throughput.
        storage_mode: Storage mode.
        volume_size_gb: Volume size gb.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kafka", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ClusterArn"] = cluster_arn
    kwargs["CurrentVersion"] = current_version
    if provisioned_throughput is not None:
        kwargs["ProvisionedThroughput"] = provisioned_throughput
    if storage_mode is not None:
        kwargs["StorageMode"] = storage_mode
    if volume_size_gb is not None:
        kwargs["VolumeSizeGB"] = volume_size_gb
    try:
        resp = await client.call("UpdateStorage", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update storage") from exc
    return UpdateStorageResult(
        cluster_arn=resp.get("ClusterArn"),
        cluster_operation_arn=resp.get("ClusterOperationArn"),
    )
