"""Tests for aws_util.aio.msk -- 100 % line coverage."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from aws_util.aio.msk import (
    ClusterResult,
    ConfigurationResult,
    NodeResult,
    create_cluster,
    create_configuration,
    delete_cluster,
    describe_cluster,
    get_bootstrap_brokers,
    list_clusters,
    list_configurations,
    list_nodes,
    update_broker_count,
    update_broker_storage,
    update_cluster_configuration,
    wait_for_cluster,
    batch_associate_scram_secret,
    batch_disassociate_scram_secret,
    create_cluster_v2,
    create_replicator,
    create_vpc_connection,
    delete_cluster_policy,
    delete_configuration,
    delete_replicator,
    delete_vpc_connection,
    describe_cluster_operation,
    describe_cluster_operation_v2,
    describe_cluster_v2,
    describe_configuration,
    describe_configuration_revision,
    describe_replicator,
    describe_vpc_connection,
    get_cluster_policy,
    get_compatible_kafka_versions,
    list_client_vpc_connections,
    list_cluster_operations,
    list_cluster_operations_v2,
    list_clusters_v2,
    list_configuration_revisions,
    list_kafka_versions,
    list_replicators,
    list_scram_secrets,
    list_tags_for_resource,
    list_vpc_connections,
    put_cluster_policy,
    reboot_broker,
    reject_client_vpc_connection,
    tag_resource,
    untag_resource,
    update_broker_type,
    update_cluster_kafka_version,
    update_configuration,
    update_connectivity,
    update_monitoring,
    update_rebalancing,
    update_replication_info,
    update_security,
    update_storage,
)


REGION = "us-east-1"
CLUSTER_NAME = "test-msk-cluster"
CLUSTER_ARN = (
    f"arn:aws:kafka:{REGION}:123456789012:cluster/{CLUSTER_NAME}/abc-123"
)
KAFKA_VERSION = "2.8.1"
BROKER_NODE_GROUP_INFO: dict = {
    "InstanceType": "kafka.m5.large",
    "ClientSubnets": ["subnet-12345"],
    "SecurityGroups": ["sg-12345"],
}
CONFIG_ARN = f"arn:aws:kafka:{REGION}:123456789012:configuration/test-config/1"
CURRENT_VERSION = "K1V2E3N4"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_factory(mock_client):
    return lambda *a, **kw: mock_client


def _cluster_resp(**overrides) -> dict:
    d = {
        "ClusterName": CLUSTER_NAME,
        "ClusterArn": CLUSTER_ARN,
        "State": "ACTIVE",
        "ClusterType": "PROVISIONED",
        "CreationTime": "2024-01-01T00:00:00Z",
        "CurrentVersion": CURRENT_VERSION,
        "NumberOfBrokerNodes": 3,
        "BrokerNodeGroupInfo": BROKER_NODE_GROUP_INFO,
        "EncryptionInfo": {"EncryptionInTransit": {"ClientBroker": "TLS"}},
        "Tags": {"env": "test"},
    }
    d.update(overrides)
    return d


def _config_resp(**overrides) -> dict:
    d = {
        "Arn": CONFIG_ARN,
        "Name": "test-config",
        "CreationTime": "2024-01-01T00:00:00Z",
        "Description": "Test configuration",
        "KafkaVersions": ["2.8.1"],
        "LatestRevision": {"Revision": 1},
        "State": "ACTIVE",
    }
    d.update(overrides)
    return d


def _node_resp(**overrides) -> dict:
    d = {
        "NodeType": "BROKER",
        "NodeARN": f"{CLUSTER_ARN}/broker/1",
        "InstanceType": "kafka.m5.large",
        "BrokerNodeInfo": {"BrokerId": "1"},
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# create_cluster
# ---------------------------------------------------------------------------


async def test_create_cluster_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterArn": CLUSTER_ARN,
        "ClusterName": CLUSTER_NAME,
        "State": "CREATING",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await create_cluster(
        CLUSTER_NAME,
        kafka_version=KAFKA_VERSION,
        number_of_broker_nodes=3,
        broker_node_group_info=BROKER_NODE_GROUP_INFO,
    )
    assert isinstance(result, ClusterResult)
    assert result.cluster_name == CLUSTER_NAME


async def test_create_cluster_all_options(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterArn": CLUSTER_ARN,
        "State": "CREATING",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await create_cluster(
        CLUSTER_NAME,
        kafka_version=KAFKA_VERSION,
        number_of_broker_nodes=3,
        broker_node_group_info=BROKER_NODE_GROUP_INFO,
        encryption_info={"EncryptionInTransit": {"ClientBroker": "TLS"}},
        tags={"env": "test"},
    )
    call_kwargs = mock_client.call.call_args[1]
    assert "EncryptionInfo" in call_kwargs
    assert "Tags" in call_kwargs


async def test_create_cluster_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await create_cluster(
            CLUSTER_NAME,
            kafka_version=KAFKA_VERSION,
            number_of_broker_nodes=3,
            broker_node_group_info=BROKER_NODE_GROUP_INFO,
        )


async def test_create_cluster_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_cluster failed"):
        await create_cluster(
            CLUSTER_NAME,
            kafka_version=KAFKA_VERSION,
            number_of_broker_nodes=3,
            broker_node_group_info=BROKER_NODE_GROUP_INFO,
        )


# ---------------------------------------------------------------------------
# describe_cluster
# ---------------------------------------------------------------------------


async def test_describe_cluster_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {"ClusterInfo": _cluster_resp()}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await describe_cluster(CLUSTER_ARN)
    assert result.cluster_name == CLUSTER_NAME


async def test_describe_cluster_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await describe_cluster("missing-arn")


async def test_describe_cluster_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="describe_cluster failed"):
        await describe_cluster("missing-arn")


# ---------------------------------------------------------------------------
# list_clusters
# ---------------------------------------------------------------------------


async def test_list_clusters_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = [_cluster_resp(), _cluster_resp(ClusterName="c2")]
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await list_clusters()
    assert len(result) == 2
    assert result[0].cluster_name == CLUSTER_NAME


async def test_list_clusters_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_clusters()


async def test_list_clusters_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_clusters failed"):
        await list_clusters()


# ---------------------------------------------------------------------------
# delete_cluster
# ---------------------------------------------------------------------------


async def test_delete_cluster_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterArn": CLUSTER_ARN,
        "State": "DELETING",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await delete_cluster(CLUSTER_ARN)
    assert result["state"] == "DELETING"


async def test_delete_cluster_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await delete_cluster("missing")


async def test_delete_cluster_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = TypeError("t")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="delete_cluster failed"):
        await delete_cluster("missing")


# ---------------------------------------------------------------------------
# update_broker_count
# ---------------------------------------------------------------------------


async def test_update_broker_count_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterArn": CLUSTER_ARN,
        "ClusterOperationArn": "arn:aws:kafka:op/123",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await update_broker_count(
        CLUSTER_ARN,
        target_number_of_broker_nodes=6,
        current_version=CURRENT_VERSION,
    )
    assert result["cluster_arn"] == CLUSTER_ARN
    assert result["cluster_operation_arn"] == "arn:aws:kafka:op/123"


async def test_update_broker_count_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_broker_count(
            CLUSTER_ARN,
            target_number_of_broker_nodes=6,
            current_version=CURRENT_VERSION,
        )


async def test_update_broker_count_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_broker_count failed"):
        await update_broker_count(
            CLUSTER_ARN,
            target_number_of_broker_nodes=6,
            current_version=CURRENT_VERSION,
        )


# ---------------------------------------------------------------------------
# update_broker_storage
# ---------------------------------------------------------------------------


async def test_update_broker_storage_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterArn": CLUSTER_ARN,
        "ClusterOperationArn": "arn:aws:kafka:op/456",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await update_broker_storage(
        CLUSTER_ARN,
        target_broker_ebs_volume_info=[
            {"KafkaBrokerNodeId": "All", "VolumeSizeGB": 200}
        ],
        current_version=CURRENT_VERSION,
    )
    assert result["cluster_arn"] == CLUSTER_ARN


async def test_update_broker_storage_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_broker_storage(
            CLUSTER_ARN,
            target_broker_ebs_volume_info=[{"KafkaBrokerNodeId": "All"}],
            current_version=CURRENT_VERSION,
        )


async def test_update_broker_storage_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="update_broker_storage failed"):
        await update_broker_storage(
            CLUSTER_ARN,
            target_broker_ebs_volume_info=[{"KafkaBrokerNodeId": "All"}],
            current_version=CURRENT_VERSION,
        )


# ---------------------------------------------------------------------------
# update_cluster_configuration
# ---------------------------------------------------------------------------


async def test_update_cluster_configuration_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterArn": CLUSTER_ARN,
        "ClusterOperationArn": "arn:aws:kafka:op/789",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await update_cluster_configuration(
        CLUSTER_ARN,
        configuration_info={"Arn": CONFIG_ARN, "Revision": 1},
        current_version=CURRENT_VERSION,
    )
    assert result["cluster_arn"] == CLUSTER_ARN


async def test_update_cluster_configuration_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await update_cluster_configuration(
            CLUSTER_ARN,
            configuration_info={"Arn": CONFIG_ARN, "Revision": 1},
            current_version=CURRENT_VERSION,
        )


async def test_update_cluster_configuration_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(
        RuntimeError, match="update_cluster_configuration failed"
    ):
        await update_cluster_configuration(
            CLUSTER_ARN,
            configuration_info={"Arn": CONFIG_ARN, "Revision": 1},
            current_version=CURRENT_VERSION,
        )


# ---------------------------------------------------------------------------
# list_nodes
# ---------------------------------------------------------------------------


async def test_list_nodes_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = [_node_resp(), _node_resp(NodeARN="arn:2")]
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await list_nodes(CLUSTER_ARN)
    assert len(result) == 2
    assert result[0].node_type == "BROKER"


async def test_list_nodes_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_nodes(CLUSTER_ARN)


async def test_list_nodes_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_nodes failed"):
        await list_nodes(CLUSTER_ARN)


# ---------------------------------------------------------------------------
# get_bootstrap_brokers
# ---------------------------------------------------------------------------


async def test_get_bootstrap_brokers_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "BootstrapBrokerString": "b-1:9092,b-2:9092",
        "BootstrapBrokerStringTls": "b-1:9094,b-2:9094",
        "BootstrapBrokerStringSaslScram": "b-1:9096",
        "BootstrapBrokerStringSaslIam": "b-1:9098",
        "BootstrapBrokerStringPublicTls": None,
        "BootstrapBrokerStringPublicSaslScram": None,
        "BootstrapBrokerStringPublicSaslIam": None,
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await get_bootstrap_brokers(CLUSTER_ARN)
    assert result["bootstrap_broker_string"] == "b-1:9092,b-2:9092"
    assert result["bootstrap_broker_string_public_tls"] is None


async def test_get_bootstrap_brokers_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await get_bootstrap_brokers("missing")


async def test_get_bootstrap_brokers_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("v")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="get_bootstrap_brokers failed"):
        await get_bootstrap_brokers("missing")


# ---------------------------------------------------------------------------
# create_configuration
# ---------------------------------------------------------------------------


async def test_create_configuration_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Arn": CONFIG_ARN,
        "Name": "test-config",
        "CreationTime": "2024-01-01T00:00:00Z",
        "LatestRevision": {"Revision": 1},
        "State": "ACTIVE",
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await create_configuration(
        "test-config",
        server_properties="auto.create.topics.enable=true",
        kafka_versions=["2.8.1"],
    )
    assert isinstance(result, ConfigurationResult)
    assert result.arn == CONFIG_ARN


async def test_create_configuration_with_description(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "Arn": CONFIG_ARN,
        "Name": "test-config",
        "LatestRevision": {"Revision": 1},
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await create_configuration(
        "test-config",
        server_properties="auto.create.topics.enable=true",
        kafka_versions=["2.8.1"],
        description="My config",
    )
    call_kwargs = mock_client.call.call_args[1]
    assert call_kwargs["Description"] == "My config"


async def test_create_configuration_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("api")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="api"):
        await create_configuration(
            "cfg",
            server_properties="x=y",
            kafka_versions=["2.8.1"],
        )


async def test_create_configuration_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="create_configuration failed"):
        await create_configuration(
            "cfg",
            server_properties="x=y",
            kafka_versions=["2.8.1"],
        )


# ---------------------------------------------------------------------------
# list_configurations
# ---------------------------------------------------------------------------


async def test_list_configurations_success(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.return_value = [_config_resp()]
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await list_configurations()
    assert len(result) == 1
    assert result[0].name == "test-config"


async def test_list_configurations_runtime_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = RuntimeError("err")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="err"):
        await list_configurations()


async def test_list_configurations_generic_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.paginate.side_effect = ValueError("bad")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    with pytest.raises(RuntimeError, match="list_configurations failed"):
        await list_configurations()


# ---------------------------------------------------------------------------
# wait_for_cluster
# ---------------------------------------------------------------------------


async def test_wait_for_cluster_already_active(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterInfo": _cluster_resp(State="ACTIVE")
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_cluster(CLUSTER_ARN, poll_interval=0)
    assert result.state == "ACTIVE"


async def test_wait_for_cluster_becomes_active(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = [
        {"ClusterInfo": _cluster_resp(State="CREATING")},
        {"ClusterInfo": _cluster_resp(State="ACTIVE")},
    ]
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    monkeypatch.setattr("aws_util.aio.msk.asyncio.sleep", AsyncMock())
    result = await wait_for_cluster(
        CLUSTER_ARN, timeout=300, poll_interval=1
    )
    assert result.state == "ACTIVE"


async def test_wait_for_cluster_timeout(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterInfo": _cluster_resp(State="CREATING")
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    monkeypatch.setattr("aws_util.aio.msk.asyncio.sleep", AsyncMock())
    with pytest.raises(TimeoutError, match="did not reach state"):
        await wait_for_cluster(
            CLUSTER_ARN, timeout=0, poll_interval=0
        )


async def test_wait_for_cluster_custom_target(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {
        "ClusterInfo": _cluster_resp(State="DELETING")
    }
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client", _mock_factory(mock_client)
    )
    result = await wait_for_cluster(
        CLUSTER_ARN, target_state="DELETING", poll_interval=0
    )
    assert result.state == "DELETING"


async def test_batch_associate_scram_secret(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_associate_scram_secret("test-cluster_arn", [], )
    mock_client.call.assert_called_once()


async def test_batch_associate_scram_secret_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_associate_scram_secret("test-cluster_arn", [], )


async def test_batch_disassociate_scram_secret(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await batch_disassociate_scram_secret("test-cluster_arn", [], )
    mock_client.call.assert_called_once()


async def test_batch_disassociate_scram_secret_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await batch_disassociate_scram_secret("test-cluster_arn", [], )


async def test_create_cluster_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_cluster_v2("test-cluster_name", )
    mock_client.call.assert_called_once()


async def test_create_cluster_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_cluster_v2("test-cluster_name", )


async def test_create_replicator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_replicator([], [], "test-replicator_name", "test-service_execution_role_arn", )
    mock_client.call.assert_called_once()


async def test_create_replicator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_replicator([], [], "test-replicator_name", "test-service_execution_role_arn", )


async def test_create_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await create_vpc_connection("test-target_cluster_arn", "test-authentication", "test-vpc_id", [], [], )
    mock_client.call.assert_called_once()


async def test_create_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await create_vpc_connection("test-target_cluster_arn", "test-authentication", "test-vpc_id", [], [], )


async def test_delete_cluster_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_cluster_policy("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_delete_cluster_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_cluster_policy("test-cluster_arn", )


async def test_delete_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_configuration("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_configuration("test-arn", )


async def test_delete_replicator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_replicator("test-replicator_arn", )
    mock_client.call.assert_called_once()


async def test_delete_replicator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_replicator("test-replicator_arn", )


async def test_delete_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await delete_vpc_connection("test-arn", )
    mock_client.call.assert_called_once()


async def test_delete_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await delete_vpc_connection("test-arn", )


async def test_describe_cluster_operation(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_operation("test-cluster_operation_arn", )
    mock_client.call.assert_called_once()


async def test_describe_cluster_operation_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_operation("test-cluster_operation_arn", )


async def test_describe_cluster_operation_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_operation_v2("test-cluster_operation_arn", )
    mock_client.call.assert_called_once()


async def test_describe_cluster_operation_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_operation_v2("test-cluster_operation_arn", )


async def test_describe_cluster_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_cluster_v2("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_describe_cluster_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_cluster_v2("test-cluster_arn", )


async def test_describe_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_configuration("test-arn", )
    mock_client.call.assert_called_once()


async def test_describe_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration("test-arn", )


async def test_describe_configuration_revision(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_configuration_revision("test-arn", 1, )
    mock_client.call.assert_called_once()


async def test_describe_configuration_revision_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_configuration_revision("test-arn", 1, )


async def test_describe_replicator(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_replicator("test-replicator_arn", )
    mock_client.call.assert_called_once()


async def test_describe_replicator_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_replicator("test-replicator_arn", )


async def test_describe_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await describe_vpc_connection("test-arn", )
    mock_client.call.assert_called_once()


async def test_describe_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await describe_vpc_connection("test-arn", )


async def test_get_cluster_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_cluster_policy("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_get_cluster_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_cluster_policy("test-cluster_arn", )


async def test_get_compatible_kafka_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await get_compatible_kafka_versions()
    mock_client.call.assert_called_once()


async def test_get_compatible_kafka_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await get_compatible_kafka_versions()


async def test_list_client_vpc_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_client_vpc_connections("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_list_client_vpc_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_client_vpc_connections("test-cluster_arn", )


async def test_list_cluster_operations(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cluster_operations("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_list_cluster_operations_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cluster_operations("test-cluster_arn", )


async def test_list_cluster_operations_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_cluster_operations_v2("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_list_cluster_operations_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_cluster_operations_v2("test-cluster_arn", )


async def test_list_clusters_v2(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_clusters_v2()
    mock_client.call.assert_called_once()


async def test_list_clusters_v2_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_clusters_v2()


async def test_list_configuration_revisions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_configuration_revisions("test-arn", )
    mock_client.call.assert_called_once()


async def test_list_configuration_revisions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_configuration_revisions("test-arn", )


async def test_list_kafka_versions(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_kafka_versions()
    mock_client.call.assert_called_once()


async def test_list_kafka_versions_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_kafka_versions()


async def test_list_replicators(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_replicators()
    mock_client.call.assert_called_once()


async def test_list_replicators_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_replicators()


async def test_list_scram_secrets(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_scram_secrets("test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_list_scram_secrets_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_scram_secrets("test-cluster_arn", )


async def test_list_tags_for_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_tags_for_resource("test-resource_arn", )
    mock_client.call.assert_called_once()


async def test_list_tags_for_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_tags_for_resource("test-resource_arn", )


async def test_list_vpc_connections(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await list_vpc_connections()
    mock_client.call.assert_called_once()


async def test_list_vpc_connections_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await list_vpc_connections()


async def test_put_cluster_policy(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await put_cluster_policy("test-cluster_arn", "test-policy", )
    mock_client.call.assert_called_once()


async def test_put_cluster_policy_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await put_cluster_policy("test-cluster_arn", "test-policy", )


async def test_reboot_broker(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await reboot_broker([], "test-cluster_arn", )
    mock_client.call.assert_called_once()


async def test_reboot_broker_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reboot_broker([], "test-cluster_arn", )


async def test_reject_client_vpc_connection(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await reject_client_vpc_connection("test-cluster_arn", "test-vpc_connection_arn", )
    mock_client.call.assert_called_once()


async def test_reject_client_vpc_connection_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await reject_client_vpc_connection("test-cluster_arn", "test-vpc_connection_arn", )


async def test_tag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await tag_resource("test-resource_arn", {}, )
    mock_client.call.assert_called_once()


async def test_tag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await tag_resource("test-resource_arn", {}, )


async def test_untag_resource(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await untag_resource("test-resource_arn", [], )
    mock_client.call.assert_called_once()


async def test_untag_resource_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await untag_resource("test-resource_arn", [], )


async def test_update_broker_type(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_broker_type("test-cluster_arn", "test-current_version", "test-target_instance_type", )
    mock_client.call.assert_called_once()


async def test_update_broker_type_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_broker_type("test-cluster_arn", "test-current_version", "test-target_instance_type", )


async def test_update_cluster_kafka_version(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_cluster_kafka_version("test-cluster_arn", "test-current_version", "test-target_kafka_version", )
    mock_client.call.assert_called_once()


async def test_update_cluster_kafka_version_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_cluster_kafka_version("test-cluster_arn", "test-current_version", "test-target_kafka_version", )


async def test_update_configuration(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_configuration("test-arn", "test-server_properties", )
    mock_client.call.assert_called_once()


async def test_update_configuration_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_configuration("test-arn", "test-server_properties", )


async def test_update_connectivity(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_connectivity("test-cluster_arn", {}, "test-current_version", )
    mock_client.call.assert_called_once()


async def test_update_connectivity_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_connectivity("test-cluster_arn", {}, "test-current_version", )


async def test_update_monitoring(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_monitoring("test-cluster_arn", "test-current_version", )
    mock_client.call.assert_called_once()


async def test_update_monitoring_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_monitoring("test-cluster_arn", "test-current_version", )


async def test_update_rebalancing(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_rebalancing("test-cluster_arn", "test-current_version", {}, )
    mock_client.call.assert_called_once()


async def test_update_rebalancing_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_rebalancing("test-cluster_arn", "test-current_version", {}, )


async def test_update_replication_info(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_replication_info("test-current_version", "test-replicator_arn", "test-source_kafka_cluster_arn", "test-target_kafka_cluster_arn", )
    mock_client.call.assert_called_once()


async def test_update_replication_info_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_replication_info("test-current_version", "test-replicator_arn", "test-source_kafka_cluster_arn", "test-target_kafka_cluster_arn", )


async def test_update_security(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_security("test-cluster_arn", "test-current_version", )
    mock_client.call.assert_called_once()


async def test_update_security_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_security("test-cluster_arn", "test-current_version", )


async def test_update_storage(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.return_value = {}
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    await update_storage("test-cluster_arn", "test-current_version", )
    mock_client.call.assert_called_once()


async def test_update_storage_error(monkeypatch):
    mock_client = AsyncMock()
    mock_client.call.side_effect = RuntimeError("boom")
    monkeypatch.setattr(
        "aws_util.aio.msk.async_client",
        lambda *a, **kw: mock_client,
    )
    with pytest.raises(RuntimeError, match="boom"):
        await update_storage("test-cluster_arn", "test-current_version", )


@pytest.mark.asyncio
async def test_create_cluster_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import create_cluster_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await create_cluster_v2("test-cluster_name", tags=[{"Key": "k", "Value": "v"}], provisioned="test-provisioned", serverless="test-serverless", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_replicator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import create_replicator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await create_replicator("test-kafka_clusters", "test-replication_info_list", "test-replicator_name", "test-service_execution_role_arn", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_create_vpc_connection_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import create_vpc_connection
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await create_vpc_connection("test-target_cluster_arn", "test-authentication", "test-vpc_id", "test-client_subnets", "test-security_groups", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_delete_replicator_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import delete_replicator
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await delete_replicator("test-replicator_arn", current_version="test-current_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_get_compatible_kafka_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import get_compatible_kafka_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await get_compatible_kafka_versions(cluster_arn="test-cluster_arn", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_client_vpc_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_client_vpc_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_client_vpc_connections("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cluster_operations_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_cluster_operations
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_cluster_operations("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_cluster_operations_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_cluster_operations_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_cluster_operations_v2("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_clusters_v2_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_clusters_v2
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_clusters_v2(cluster_name_filter=[{}], cluster_type_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_configuration_revisions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_configuration_revisions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_configuration_revisions("test-arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_kafka_versions_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_kafka_versions
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_kafka_versions(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_replicators_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_replicators
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_replicators(max_results=1, next_token="test-next_token", replicator_name_filter=[{}], region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_scram_secrets_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_scram_secrets
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_scram_secrets("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_list_vpc_connections_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import list_vpc_connections
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await list_vpc_connections(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_put_cluster_policy_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import put_cluster_policy
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await put_cluster_policy("test-cluster_arn", "{}", current_version="test-current_version", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_cluster_kafka_version_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import update_cluster_kafka_version
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await update_cluster_kafka_version("test-cluster_arn", "test-current_version", "test-target_kafka_version", configuration_info={}, region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_configuration_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import update_configuration
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await update_configuration("test-arn", {}, description="test-description", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_monitoring_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import update_monitoring
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await update_monitoring("test-cluster_arn", "test-current_version", enhanced_monitoring="test-enhanced_monitoring", open_monitoring="test-open_monitoring", logging_info="test-logging_info", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_replication_info_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import update_replication_info
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await update_replication_info("test-current_version", "test-replicator_arn", "test-source_kafka_cluster_arn", "test-target_kafka_cluster_arn", consumer_group_replication="test-consumer_group_replication", topic_replication="test-topic_replication", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_security_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import update_security
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await update_security("test-cluster_arn", "test-current_version", client_authentication="test-client_authentication", encryption_info="test-encryption_info", region_name="us-east-1")
    mock_client.call.assert_called_once()

@pytest.mark.asyncio
async def test_update_storage_with_options(monkeypatch):
    from unittest.mock import AsyncMock
    from aws_util.aio.msk import update_storage
    mock_client = AsyncMock()
    mock_client.call = AsyncMock(return_value={})
    monkeypatch.setattr("aws_util.aio.msk.async_client", lambda *a, **kw: mock_client)
    await update_storage("test-cluster_arn", "test-current_version", provisioned_throughput="test-provisioned_throughput", storage_mode="test-storage_mode", volume_size_gb=1, region_name="us-east-1")
    mock_client.call.assert_called_once()
