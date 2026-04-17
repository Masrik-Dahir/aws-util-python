"""Tests for aws_util.msk module."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError

import aws_util.msk as msk_mod
from aws_util.msk import (
    ClusterResult,
    ConfigurationResult,
    NodeResult,
    _parse_cluster,
    _parse_configuration,
    _parse_node,
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
# Helpers -- raw dicts matching AWS API shape
# ---------------------------------------------------------------------------


def _cluster_dict(**overrides: object) -> dict:
    d: dict = {
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


def _configuration_dict(**overrides: object) -> dict:
    d: dict = {
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


def _node_dict(**overrides: object) -> dict:
    d: dict = {
        "NodeType": "BROKER",
        "NodeARN": f"{CLUSTER_ARN}/broker/1",
        "InstanceType": "kafka.m5.large",
        "BrokerNodeInfo": {
            "BrokerId": "1",
            "AttachedENIId": "eni-12345",
        },
    }
    d.update(overrides)
    return d


# ---------------------------------------------------------------------------
# Model tests
# ---------------------------------------------------------------------------


class TestModels:
    def test_cluster_result_model(self):
        c = ClusterResult(
            cluster_name="c", cluster_arn="arn:...", state="ACTIVE"
        )
        assert c.cluster_name == "c"
        assert c.cluster_type is None
        assert c.tags == {}

    def test_configuration_result_model(self):
        cfg = ConfigurationResult(arn="arn:...", name="cfg")
        assert cfg.state is None
        assert cfg.kafka_versions == []

    def test_node_result_model(self):
        n = NodeResult()
        assert n.node_type is None
        assert n.broker_node_info == {}

    def test_models_are_frozen(self):
        c = ClusterResult(
            cluster_name="c", cluster_arn="arn:...", state="ACTIVE"
        )
        with pytest.raises(Exception):
            c.cluster_name = "new"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Parse helpers
# ---------------------------------------------------------------------------


class TestParseHelpers:
    def test_parse_cluster_full(self):
        result = _parse_cluster(_cluster_dict())
        assert result.cluster_name == CLUSTER_NAME
        assert result.state == "ACTIVE"
        assert result.number_of_broker_nodes == 3
        assert result.tags == {"env": "test"}

    def test_parse_cluster_minimal(self):
        result = _parse_cluster({
            "ClusterName": "min",
            "ClusterArn": "arn:...",
            "State": "CREATING",
        })
        assert result.cluster_type is None
        assert result.creation_time is None
        assert result.current_version is None

    def test_parse_cluster_extra_fields(self):
        data = _cluster_dict()
        data["SomeExtraField"] = "hello"
        result = _parse_cluster(data)
        assert result.extra["SomeExtraField"] == "hello"

    def test_parse_configuration_full(self):
        result = _parse_configuration(_configuration_dict())
        assert result.name == "test-config"
        assert result.description == "Test configuration"
        assert result.kafka_versions == ["2.8.1"]

    def test_parse_configuration_minimal(self):
        result = _parse_configuration({"Arn": "arn:...", "Name": "min"})
        assert result.description is None
        assert result.creation_time is None

    def test_parse_configuration_extra_fields(self):
        data = _configuration_dict()
        data["ExtraField"] = "val"
        result = _parse_configuration(data)
        assert result.extra["ExtraField"] == "val"

    def test_parse_node_full(self):
        result = _parse_node(_node_dict())
        assert result.node_type == "BROKER"
        assert result.instance_type == "kafka.m5.large"

    def test_parse_node_minimal(self):
        result = _parse_node({})
        assert result.node_type is None
        assert result.node_arn is None

    def test_parse_node_extra_fields(self):
        data = _node_dict()
        data["AddedFieldInFuture"] = True
        result = _parse_node(data)
        assert result.extra["AddedFieldInFuture"] is True


# ---------------------------------------------------------------------------
# Cluster operations
# ---------------------------------------------------------------------------


class TestCreateCluster:
    def test_create_cluster_basic(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cluster.return_value = {
            "ClusterArn": CLUSTER_ARN,
            "ClusterName": CLUSTER_NAME,
            "State": "CREATING",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = create_cluster(
            CLUSTER_NAME,
            kafka_version=KAFKA_VERSION,
            number_of_broker_nodes=3,
            broker_node_group_info=BROKER_NODE_GROUP_INFO,
            region_name=REGION,
        )
        assert isinstance(result, ClusterResult)
        assert result.cluster_name == CLUSTER_NAME
        assert result.state == "CREATING"

    def test_create_cluster_with_all_options(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cluster.return_value = {
            "ClusterArn": CLUSTER_ARN,
            "ClusterName": CLUSTER_NAME,
            "State": "CREATING",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = create_cluster(
            CLUSTER_NAME,
            kafka_version=KAFKA_VERSION,
            number_of_broker_nodes=3,
            broker_node_group_info=BROKER_NODE_GROUP_INFO,
            encryption_info={"EncryptionInTransit": {"ClientBroker": "TLS"}},
            tags={"env": "test"},
            region_name=REGION,
        )
        assert result.cluster_arn == CLUSTER_ARN
        call_kwargs = mock_client.create_cluster.call_args[1]
        assert "EncryptionInfo" in call_kwargs
        assert "Tags" in call_kwargs

    def test_create_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_cluster.side_effect = ClientError(
            {"Error": {"Code": "ConflictException", "Message": "exists"}},
            "CreateCluster",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="create_cluster failed"):
            create_cluster(
                CLUSTER_NAME,
                kafka_version=KAFKA_VERSION,
                number_of_broker_nodes=3,
                broker_node_group_info=BROKER_NODE_GROUP_INFO,
                region_name=REGION,
            )


class TestDescribeCluster:
    def test_describe_cluster(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "ClusterInfo": _cluster_dict()
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = describe_cluster(CLUSTER_ARN, region_name=REGION)
        assert isinstance(result, ClusterResult)
        assert result.cluster_name == CLUSTER_NAME

    def test_describe_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.side_effect = ClientError(
            {
                "Error": {
                    "Code": "NotFoundException",
                    "Message": "not found",
                }
            },
            "DescribeCluster",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="describe_cluster failed"):
            describe_cluster("missing-arn", region_name=REGION)


class TestListClusters:
    def test_list_clusters_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"ClusterInfoList": []}]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = list_clusters(region_name=REGION)
        assert result == []

    def test_list_clusters_with_clusters(self, monkeypatch):
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"ClusterInfoList": [_cluster_dict(), _cluster_dict(ClusterName="c2")]}
        ]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = list_clusters(region_name=REGION)
        assert len(result) == 2
        assert result[0].cluster_name == CLUSTER_NAME

    def test_list_clusters_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}},
            "ListClusters",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="list_clusters failed"):
            list_clusters(region_name=REGION)


class TestDeleteCluster:
    def test_delete_cluster(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_cluster.return_value = {
            "ClusterArn": CLUSTER_ARN,
            "State": "DELETING",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = delete_cluster(CLUSTER_ARN, region_name=REGION)
        assert result["cluster_arn"] == CLUSTER_ARN
        assert result["state"] == "DELETING"

    def test_delete_cluster_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.delete_cluster.side_effect = ClientError(
            {"Error": {"Code": "NotFoundException", "Message": "nope"}},
            "DeleteCluster",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="delete_cluster failed"):
            delete_cluster("missing-arn", region_name=REGION)


# ---------------------------------------------------------------------------
# Broker operations
# ---------------------------------------------------------------------------


class TestUpdateBrokerCount:
    def test_update_broker_count(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_broker_count.return_value = {
            "ClusterArn": CLUSTER_ARN,
            "ClusterOperationArn": "arn:aws:kafka:op/123",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = update_broker_count(
            CLUSTER_ARN,
            target_number_of_broker_nodes=6,
            current_version=CURRENT_VERSION,
            region_name=REGION,
        )
        assert result["cluster_arn"] == CLUSTER_ARN
        assert result["cluster_operation_arn"] == "arn:aws:kafka:op/123"

    def test_update_broker_count_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_broker_count.side_effect = ClientError(
            {"Error": {"Code": "BadRequestException", "Message": "bad"}},
            "UpdateBrokerCount",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="update_broker_count failed"):
            update_broker_count(
                CLUSTER_ARN,
                target_number_of_broker_nodes=6,
                current_version=CURRENT_VERSION,
                region_name=REGION,
            )


class TestUpdateBrokerStorage:
    def test_update_broker_storage(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_broker_storage.return_value = {
            "ClusterArn": CLUSTER_ARN,
            "ClusterOperationArn": "arn:aws:kafka:op/456",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = update_broker_storage(
            CLUSTER_ARN,
            target_broker_ebs_volume_info=[
                {"KafkaBrokerNodeId": "All", "VolumeSizeGB": 200}
            ],
            current_version=CURRENT_VERSION,
            region_name=REGION,
        )
        assert result["cluster_arn"] == CLUSTER_ARN
        assert result["cluster_operation_arn"] == "arn:aws:kafka:op/456"

    def test_update_broker_storage_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_broker_storage.side_effect = ClientError(
            {"Error": {"Code": "BadRequestException", "Message": "bad"}},
            "UpdateBrokerStorage",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="update_broker_storage failed"
        ):
            update_broker_storage(
                CLUSTER_ARN,
                target_broker_ebs_volume_info=[
                    {"KafkaBrokerNodeId": "All", "VolumeSizeGB": 200}
                ],
                current_version=CURRENT_VERSION,
                region_name=REGION,
            )


class TestUpdateClusterConfiguration:
    def test_update_cluster_configuration(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_configuration.return_value = {
            "ClusterArn": CLUSTER_ARN,
            "ClusterOperationArn": "arn:aws:kafka:op/789",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = update_cluster_configuration(
            CLUSTER_ARN,
            configuration_info={"Arn": CONFIG_ARN, "Revision": 1},
            current_version=CURRENT_VERSION,
            region_name=REGION,
        )
        assert result["cluster_arn"] == CLUSTER_ARN
        assert result["cluster_operation_arn"] == "arn:aws:kafka:op/789"

    def test_update_cluster_configuration_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.update_cluster_configuration.side_effect = ClientError(
            {"Error": {"Code": "BadRequestException", "Message": "bad"}},
            "UpdateClusterConfiguration",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="update_cluster_configuration failed"
        ):
            update_cluster_configuration(
                CLUSTER_ARN,
                configuration_info={"Arn": CONFIG_ARN, "Revision": 1},
                current_version=CURRENT_VERSION,
                region_name=REGION,
            )


# ---------------------------------------------------------------------------
# Node operations
# ---------------------------------------------------------------------------


class TestListNodes:
    def test_list_nodes(self, monkeypatch):
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"NodeInfoList": [_node_dict(), _node_dict(NodeARN="arn:2")]}
        ]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = list_nodes(CLUSTER_ARN, region_name=REGION)
        assert len(result) == 2
        assert result[0].node_type == "BROKER"

    def test_list_nodes_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"NodeInfoList": []}]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = list_nodes(CLUSTER_ARN, region_name=REGION)
        assert result == []

    def test_list_nodes_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "NotFoundException", "Message": "nope"}},
            "ListNodes",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(RuntimeError, match="list_nodes failed"):
            list_nodes(CLUSTER_ARN, region_name=REGION)


# ---------------------------------------------------------------------------
# Bootstrap brokers
# ---------------------------------------------------------------------------


class TestGetBootstrapBrokers:
    def test_get_bootstrap_brokers(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_bootstrap_brokers.return_value = {
            "BootstrapBrokerString": "b-1:9092,b-2:9092",
            "BootstrapBrokerStringTls": "b-1:9094,b-2:9094",
            "BootstrapBrokerStringSaslScram": "b-1:9096,b-2:9096",
            "BootstrapBrokerStringSaslIam": "b-1:9098,b-2:9098",
            "BootstrapBrokerStringPublicTls": None,
            "BootstrapBrokerStringPublicSaslScram": None,
            "BootstrapBrokerStringPublicSaslIam": None,
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = get_bootstrap_brokers(CLUSTER_ARN, region_name=REGION)
        assert result["bootstrap_broker_string"] == "b-1:9092,b-2:9092"
        assert result["bootstrap_broker_string_tls"] == "b-1:9094,b-2:9094"
        assert result["bootstrap_broker_string_public_tls"] is None

    def test_get_bootstrap_brokers_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_bootstrap_brokers.side_effect = ClientError(
            {"Error": {"Code": "NotFoundException", "Message": "nope"}},
            "GetBootstrapBrokers",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="get_bootstrap_brokers failed"
        ):
            get_bootstrap_brokers("missing-arn", region_name=REGION)


# ---------------------------------------------------------------------------
# Configuration operations
# ---------------------------------------------------------------------------


class TestCreateConfiguration:
    def test_create_configuration_basic(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_configuration.return_value = {
            "Arn": CONFIG_ARN,
            "Name": "test-config",
            "CreationTime": "2024-01-01T00:00:00Z",
            "LatestRevision": {"Revision": 1},
            "State": "ACTIVE",
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = create_configuration(
            "test-config",
            server_properties="auto.create.topics.enable=true",
            kafka_versions=["2.8.1"],
            region_name=REGION,
        )
        assert isinstance(result, ConfigurationResult)
        assert result.arn == CONFIG_ARN

    def test_create_configuration_with_description(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_configuration.return_value = {
            "Arn": CONFIG_ARN,
            "Name": "test-config",
            "LatestRevision": {"Revision": 1},
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = create_configuration(
            "test-config",
            server_properties="auto.create.topics.enable=true",
            kafka_versions=["2.8.1"],
            description="My config",
            region_name=REGION,
        )
        assert result.name == "test-config"
        call_kwargs = mock_client.create_configuration.call_args[1]
        assert call_kwargs["Description"] == "My config"

    def test_create_configuration_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.create_configuration.side_effect = ClientError(
            {"Error": {"Code": "ConflictException", "Message": "exists"}},
            "CreateConfiguration",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="create_configuration failed"
        ):
            create_configuration(
                "test-config",
                server_properties="auto.create.topics.enable=true",
                kafka_versions=["2.8.1"],
                region_name=REGION,
            )


class TestListConfigurations:
    def test_list_configurations(self, monkeypatch):
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [
            {"Configurations": [_configuration_dict()]}
        ]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = list_configurations(region_name=REGION)
        assert len(result) == 1
        assert result[0].name == "test-config"

    def test_list_configurations_empty(self, monkeypatch):
        mock_client = MagicMock()
        mock_paginator = MagicMock()
        mock_paginator.paginate.return_value = [{"Configurations": []}]
        mock_client.get_paginator.return_value = mock_paginator
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = list_configurations(region_name=REGION)
        assert result == []

    def test_list_configurations_client_error(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.get_paginator.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "denied"}},
            "ListConfigurations",
        )
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        with pytest.raises(
            RuntimeError, match="list_configurations failed"
        ):
            list_configurations(region_name=REGION)


# ---------------------------------------------------------------------------
# Waiter
# ---------------------------------------------------------------------------


class TestWaitForCluster:
    def test_wait_for_cluster_already_active(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "ClusterInfo": _cluster_dict(State="ACTIVE")
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = wait_for_cluster(
            CLUSTER_ARN, region_name=REGION, poll_interval=0
        )
        assert result.state == "ACTIVE"

    def test_wait_for_cluster_becomes_active(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.side_effect = [
            {"ClusterInfo": _cluster_dict(State="CREATING")},
            {"ClusterInfo": _cluster_dict(State="ACTIVE")},
        ]
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        monkeypatch.setattr("aws_util.msk.time.sleep", lambda _: None)
        result = wait_for_cluster(
            CLUSTER_ARN, timeout=300, poll_interval=1, region_name=REGION
        )
        assert result.state == "ACTIVE"

    def test_wait_for_cluster_timeout(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "ClusterInfo": _cluster_dict(State="CREATING")
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        monkeypatch.setattr("aws_util.msk.time.sleep", lambda _: None)
        with pytest.raises(TimeoutError, match="did not reach state"):
            wait_for_cluster(
                CLUSTER_ARN, timeout=0, poll_interval=0, region_name=REGION
            )

    def test_wait_for_cluster_custom_target(self, monkeypatch):
        mock_client = MagicMock()
        mock_client.describe_cluster.return_value = {
            "ClusterInfo": _cluster_dict(State="DELETING")
        }
        monkeypatch.setattr(
            msk_mod, "get_client", lambda *a, **kw: mock_client
        )
        result = wait_for_cluster(
            CLUSTER_ARN,
            target_state="DELETING",
            region_name=REGION,
            poll_interval=0,
        )
        assert result.state == "DELETING"


def test_batch_associate_scram_secret(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_associate_scram_secret.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    batch_associate_scram_secret("test-cluster_arn", [], region_name=REGION)
    mock_client.batch_associate_scram_secret.assert_called_once()


def test_batch_associate_scram_secret_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_associate_scram_secret.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_associate_scram_secret",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch associate scram secret"):
        batch_associate_scram_secret("test-cluster_arn", [], region_name=REGION)


def test_batch_disassociate_scram_secret(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_disassociate_scram_secret.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    batch_disassociate_scram_secret("test-cluster_arn", [], region_name=REGION)
    mock_client.batch_disassociate_scram_secret.assert_called_once()


def test_batch_disassociate_scram_secret_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.batch_disassociate_scram_secret.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "batch_disassociate_scram_secret",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to batch disassociate scram secret"):
        batch_disassociate_scram_secret("test-cluster_arn", [], region_name=REGION)


def test_create_cluster_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cluster_v2.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    create_cluster_v2("test-cluster_name", region_name=REGION)
    mock_client.create_cluster_v2.assert_called_once()


def test_create_cluster_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_cluster_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_cluster_v2",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create cluster v2"):
        create_cluster_v2("test-cluster_name", region_name=REGION)


def test_create_replicator(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_replicator.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    create_replicator([], [], "test-replicator_name", "test-service_execution_role_arn", region_name=REGION)
    mock_client.create_replicator.assert_called_once()


def test_create_replicator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_replicator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_replicator",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create replicator"):
        create_replicator([], [], "test-replicator_name", "test-service_execution_role_arn", region_name=REGION)


def test_create_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_connection.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    create_vpc_connection("test-target_cluster_arn", "test-authentication", "test-vpc_id", [], [], region_name=REGION)
    mock_client.create_vpc_connection.assert_called_once()


def test_create_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.create_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "create_vpc_connection",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to create vpc connection"):
        create_vpc_connection("test-target_cluster_arn", "test-authentication", "test-vpc_id", [], [], region_name=REGION)


def test_delete_cluster_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_policy.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    delete_cluster_policy("test-cluster_arn", region_name=REGION)
    mock_client.delete_cluster_policy.assert_called_once()


def test_delete_cluster_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_cluster_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_cluster_policy",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete cluster policy"):
        delete_cluster_policy("test-cluster_arn", region_name=REGION)


def test_delete_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    delete_configuration("test-arn", region_name=REGION)
    mock_client.delete_configuration.assert_called_once()


def test_delete_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_configuration",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete configuration"):
        delete_configuration("test-arn", region_name=REGION)


def test_delete_replicator(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_replicator.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    delete_replicator("test-replicator_arn", region_name=REGION)
    mock_client.delete_replicator.assert_called_once()


def test_delete_replicator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_replicator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_replicator",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete replicator"):
        delete_replicator("test-replicator_arn", region_name=REGION)


def test_delete_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_connection.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    delete_vpc_connection("test-arn", region_name=REGION)
    mock_client.delete_vpc_connection.assert_called_once()


def test_delete_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.delete_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "delete_vpc_connection",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to delete vpc connection"):
        delete_vpc_connection("test-arn", region_name=REGION)


def test_describe_cluster_operation(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_operation.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_cluster_operation("test-cluster_operation_arn", region_name=REGION)
    mock_client.describe_cluster_operation.assert_called_once()


def test_describe_cluster_operation_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_operation.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_operation",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster operation"):
        describe_cluster_operation("test-cluster_operation_arn", region_name=REGION)


def test_describe_cluster_operation_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_operation_v2.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_cluster_operation_v2("test-cluster_operation_arn", region_name=REGION)
    mock_client.describe_cluster_operation_v2.assert_called_once()


def test_describe_cluster_operation_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_operation_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_operation_v2",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster operation v2"):
        describe_cluster_operation_v2("test-cluster_operation_arn", region_name=REGION)


def test_describe_cluster_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_v2.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_cluster_v2("test-cluster_arn", region_name=REGION)
    mock_client.describe_cluster_v2.assert_called_once()


def test_describe_cluster_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_cluster_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_cluster_v2",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe cluster v2"):
        describe_cluster_v2("test-cluster_arn", region_name=REGION)


def test_describe_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_configuration("test-arn", region_name=REGION)
    mock_client.describe_configuration.assert_called_once()


def test_describe_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe configuration"):
        describe_configuration("test-arn", region_name=REGION)


def test_describe_configuration_revision(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_revision.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_configuration_revision("test-arn", 1, region_name=REGION)
    mock_client.describe_configuration_revision.assert_called_once()


def test_describe_configuration_revision_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_configuration_revision.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_configuration_revision",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe configuration revision"):
        describe_configuration_revision("test-arn", 1, region_name=REGION)


def test_describe_replicator(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replicator.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_replicator("test-replicator_arn", region_name=REGION)
    mock_client.describe_replicator.assert_called_once()


def test_describe_replicator_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_replicator.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_replicator",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe replicator"):
        describe_replicator("test-replicator_arn", region_name=REGION)


def test_describe_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_connection.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    describe_vpc_connection("test-arn", region_name=REGION)
    mock_client.describe_vpc_connection.assert_called_once()


def test_describe_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.describe_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "describe_vpc_connection",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to describe vpc connection"):
        describe_vpc_connection("test-arn", region_name=REGION)


def test_get_cluster_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_policy.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    get_cluster_policy("test-cluster_arn", region_name=REGION)
    mock_client.get_cluster_policy.assert_called_once()


def test_get_cluster_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_cluster_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_cluster_policy",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get cluster policy"):
        get_cluster_policy("test-cluster_arn", region_name=REGION)


def test_get_compatible_kafka_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compatible_kafka_versions.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    get_compatible_kafka_versions(region_name=REGION)
    mock_client.get_compatible_kafka_versions.assert_called_once()


def test_get_compatible_kafka_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.get_compatible_kafka_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "get_compatible_kafka_versions",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to get compatible kafka versions"):
        get_compatible_kafka_versions(region_name=REGION)


def test_list_client_vpc_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_client_vpc_connections.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_client_vpc_connections("test-cluster_arn", region_name=REGION)
    mock_client.list_client_vpc_connections.assert_called_once()


def test_list_client_vpc_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_client_vpc_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_client_vpc_connections",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list client vpc connections"):
        list_client_vpc_connections("test-cluster_arn", region_name=REGION)


def test_list_cluster_operations(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cluster_operations.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_cluster_operations("test-cluster_arn", region_name=REGION)
    mock_client.list_cluster_operations.assert_called_once()


def test_list_cluster_operations_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cluster_operations.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cluster_operations",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cluster operations"):
        list_cluster_operations("test-cluster_arn", region_name=REGION)


def test_list_cluster_operations_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cluster_operations_v2.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_cluster_operations_v2("test-cluster_arn", region_name=REGION)
    mock_client.list_cluster_operations_v2.assert_called_once()


def test_list_cluster_operations_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_cluster_operations_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_cluster_operations_v2",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list cluster operations v2"):
        list_cluster_operations_v2("test-cluster_arn", region_name=REGION)


def test_list_clusters_v2(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_clusters_v2.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_clusters_v2(region_name=REGION)
    mock_client.list_clusters_v2.assert_called_once()


def test_list_clusters_v2_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_clusters_v2.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_clusters_v2",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list clusters v2"):
        list_clusters_v2(region_name=REGION)


def test_list_configuration_revisions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_revisions.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_configuration_revisions("test-arn", region_name=REGION)
    mock_client.list_configuration_revisions.assert_called_once()


def test_list_configuration_revisions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_configuration_revisions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_configuration_revisions",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list configuration revisions"):
        list_configuration_revisions("test-arn", region_name=REGION)


def test_list_kafka_versions(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_kafka_versions.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_kafka_versions(region_name=REGION)
    mock_client.list_kafka_versions.assert_called_once()


def test_list_kafka_versions_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_kafka_versions.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_kafka_versions",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list kafka versions"):
        list_kafka_versions(region_name=REGION)


def test_list_replicators(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_replicators.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_replicators(region_name=REGION)
    mock_client.list_replicators.assert_called_once()


def test_list_replicators_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_replicators.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_replicators",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list replicators"):
        list_replicators(region_name=REGION)


def test_list_scram_secrets(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_scram_secrets.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_scram_secrets("test-cluster_arn", region_name=REGION)
    mock_client.list_scram_secrets.assert_called_once()


def test_list_scram_secrets_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_scram_secrets.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_scram_secrets",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list scram secrets"):
        list_scram_secrets("test-cluster_arn", region_name=REGION)


def test_list_tags_for_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_tags_for_resource("test-resource_arn", region_name=REGION)
    mock_client.list_tags_for_resource.assert_called_once()


def test_list_tags_for_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_tags_for_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_tags_for_resource",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list tags for resource"):
        list_tags_for_resource("test-resource_arn", region_name=REGION)


def test_list_vpc_connections(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_connections.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    list_vpc_connections(region_name=REGION)
    mock_client.list_vpc_connections.assert_called_once()


def test_list_vpc_connections_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.list_vpc_connections.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "list_vpc_connections",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to list vpc connections"):
        list_vpc_connections(region_name=REGION)


def test_put_cluster_policy(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_cluster_policy.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    put_cluster_policy("test-cluster_arn", "test-policy", region_name=REGION)
    mock_client.put_cluster_policy.assert_called_once()


def test_put_cluster_policy_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.put_cluster_policy.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "put_cluster_policy",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to put cluster policy"):
        put_cluster_policy("test-cluster_arn", "test-policy", region_name=REGION)


def test_reboot_broker(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_broker.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    reboot_broker([], "test-cluster_arn", region_name=REGION)
    mock_client.reboot_broker.assert_called_once()


def test_reboot_broker_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reboot_broker.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reboot_broker",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reboot broker"):
        reboot_broker([], "test-cluster_arn", region_name=REGION)


def test_reject_client_vpc_connection(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_client_vpc_connection.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    reject_client_vpc_connection("test-cluster_arn", "test-vpc_connection_arn", region_name=REGION)
    mock_client.reject_client_vpc_connection.assert_called_once()


def test_reject_client_vpc_connection_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.reject_client_vpc_connection.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "reject_client_vpc_connection",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to reject client vpc connection"):
        reject_client_vpc_connection("test-cluster_arn", "test-vpc_connection_arn", region_name=REGION)


def test_tag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    tag_resource("test-resource_arn", {}, region_name=REGION)
    mock_client.tag_resource.assert_called_once()


def test_tag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.tag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "tag_resource",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to tag resource"):
        tag_resource("test-resource_arn", {}, region_name=REGION)


def test_untag_resource(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    untag_resource("test-resource_arn", [], region_name=REGION)
    mock_client.untag_resource.assert_called_once()


def test_untag_resource_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.untag_resource.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "untag_resource",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to untag resource"):
        untag_resource("test-resource_arn", [], region_name=REGION)


def test_update_broker_type(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_broker_type.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_broker_type("test-cluster_arn", "test-current_version", "test-target_instance_type", region_name=REGION)
    mock_client.update_broker_type.assert_called_once()


def test_update_broker_type_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_broker_type.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_broker_type",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update broker type"):
        update_broker_type("test-cluster_arn", "test-current_version", "test-target_instance_type", region_name=REGION)


def test_update_cluster_kafka_version(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cluster_kafka_version.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_cluster_kafka_version("test-cluster_arn", "test-current_version", "test-target_kafka_version", region_name=REGION)
    mock_client.update_cluster_kafka_version.assert_called_once()


def test_update_cluster_kafka_version_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_cluster_kafka_version.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_cluster_kafka_version",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update cluster kafka version"):
        update_cluster_kafka_version("test-cluster_arn", "test-current_version", "test-target_kafka_version", region_name=REGION)


def test_update_configuration(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_configuration("test-arn", "test-server_properties", region_name=REGION)
    mock_client.update_configuration.assert_called_once()


def test_update_configuration_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_configuration.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_configuration",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update configuration"):
        update_configuration("test-arn", "test-server_properties", region_name=REGION)


def test_update_connectivity(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connectivity.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_connectivity("test-cluster_arn", {}, "test-current_version", region_name=REGION)
    mock_client.update_connectivity.assert_called_once()


def test_update_connectivity_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_connectivity.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_connectivity",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update connectivity"):
        update_connectivity("test-cluster_arn", {}, "test-current_version", region_name=REGION)


def test_update_monitoring(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_monitoring.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_monitoring("test-cluster_arn", "test-current_version", region_name=REGION)
    mock_client.update_monitoring.assert_called_once()


def test_update_monitoring_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_monitoring.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_monitoring",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update monitoring"):
        update_monitoring("test-cluster_arn", "test-current_version", region_name=REGION)


def test_update_rebalancing(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rebalancing.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_rebalancing("test-cluster_arn", "test-current_version", {}, region_name=REGION)
    mock_client.update_rebalancing.assert_called_once()


def test_update_rebalancing_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_rebalancing.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_rebalancing",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update rebalancing"):
        update_rebalancing("test-cluster_arn", "test-current_version", {}, region_name=REGION)


def test_update_replication_info(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_replication_info.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_replication_info("test-current_version", "test-replicator_arn", "test-source_kafka_cluster_arn", "test-target_kafka_cluster_arn", region_name=REGION)
    mock_client.update_replication_info.assert_called_once()


def test_update_replication_info_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_replication_info.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_replication_info",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update replication info"):
        update_replication_info("test-current_version", "test-replicator_arn", "test-source_kafka_cluster_arn", "test-target_kafka_cluster_arn", region_name=REGION)


def test_update_security(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_security("test-cluster_arn", "test-current_version", region_name=REGION)
    mock_client.update_security.assert_called_once()


def test_update_security_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_security.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_security",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update security"):
        update_security("test-cluster_arn", "test-current_version", region_name=REGION)


def test_update_storage(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_storage.return_value = {}
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    update_storage("test-cluster_arn", "test-current_version", region_name=REGION)
    mock_client.update_storage.assert_called_once()


def test_update_storage_error(monkeypatch):
    mock_client = MagicMock()
    mock_client.update_storage.side_effect = ClientError(
        {"Error": {"Code": "ServiceException", "Message": "fail"}},
        "update_storage",
    )
    monkeypatch.setattr(msk_mod, "get_client", lambda *a, **kw: mock_client)
    with pytest.raises(RuntimeError, match="Failed to update storage"):
        update_storage("test-cluster_arn", "test-current_version", region_name=REGION)


def test_create_cluster_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import create_cluster_v2
    mock_client = MagicMock()
    mock_client.create_cluster_v2.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    create_cluster_v2("test-cluster_name", tags=[{"Key": "k", "Value": "v"}], provisioned="test-provisioned", serverless="test-serverless", region_name="us-east-1")
    mock_client.create_cluster_v2.assert_called_once()

def test_create_replicator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import create_replicator
    mock_client = MagicMock()
    mock_client.create_replicator.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    create_replicator("test-kafka_clusters", "test-replication_info_list", "test-replicator_name", "test-service_execution_role_arn", description="test-description", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_replicator.assert_called_once()

def test_create_vpc_connection_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import create_vpc_connection
    mock_client = MagicMock()
    mock_client.create_vpc_connection.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    create_vpc_connection("test-target_cluster_arn", "test-authentication", "test-vpc_id", "test-client_subnets", "test-security_groups", tags=[{"Key": "k", "Value": "v"}], region_name="us-east-1")
    mock_client.create_vpc_connection.assert_called_once()

def test_delete_replicator_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import delete_replicator
    mock_client = MagicMock()
    mock_client.delete_replicator.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    delete_replicator("test-replicator_arn", current_version="test-current_version", region_name="us-east-1")
    mock_client.delete_replicator.assert_called_once()

def test_get_compatible_kafka_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import get_compatible_kafka_versions
    mock_client = MagicMock()
    mock_client.get_compatible_kafka_versions.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    get_compatible_kafka_versions(cluster_arn="test-cluster_arn", region_name="us-east-1")
    mock_client.get_compatible_kafka_versions.assert_called_once()

def test_list_client_vpc_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_client_vpc_connections
    mock_client = MagicMock()
    mock_client.list_client_vpc_connections.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_client_vpc_connections("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_client_vpc_connections.assert_called_once()

def test_list_cluster_operations_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_cluster_operations
    mock_client = MagicMock()
    mock_client.list_cluster_operations.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_cluster_operations("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_cluster_operations.assert_called_once()

def test_list_cluster_operations_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_cluster_operations_v2
    mock_client = MagicMock()
    mock_client.list_cluster_operations_v2.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_cluster_operations_v2("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_cluster_operations_v2.assert_called_once()

def test_list_clusters_v2_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_clusters_v2
    mock_client = MagicMock()
    mock_client.list_clusters_v2.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_clusters_v2(cluster_name_filter=[{}], cluster_type_filter=[{}], max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_clusters_v2.assert_called_once()

def test_list_configuration_revisions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_configuration_revisions
    mock_client = MagicMock()
    mock_client.list_configuration_revisions.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_configuration_revisions("test-arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_configuration_revisions.assert_called_once()

def test_list_kafka_versions_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_kafka_versions
    mock_client = MagicMock()
    mock_client.list_kafka_versions.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_kafka_versions(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_kafka_versions.assert_called_once()

def test_list_replicators_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_replicators
    mock_client = MagicMock()
    mock_client.list_replicators.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_replicators(max_results=1, next_token="test-next_token", replicator_name_filter=[{}], region_name="us-east-1")
    mock_client.list_replicators.assert_called_once()

def test_list_scram_secrets_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_scram_secrets
    mock_client = MagicMock()
    mock_client.list_scram_secrets.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_scram_secrets("test-cluster_arn", max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_scram_secrets.assert_called_once()

def test_list_vpc_connections_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import list_vpc_connections
    mock_client = MagicMock()
    mock_client.list_vpc_connections.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    list_vpc_connections(max_results=1, next_token="test-next_token", region_name="us-east-1")
    mock_client.list_vpc_connections.assert_called_once()

def test_put_cluster_policy_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import put_cluster_policy
    mock_client = MagicMock()
    mock_client.put_cluster_policy.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    put_cluster_policy("test-cluster_arn", "{}", current_version="test-current_version", region_name="us-east-1")
    mock_client.put_cluster_policy.assert_called_once()

def test_update_cluster_kafka_version_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import update_cluster_kafka_version
    mock_client = MagicMock()
    mock_client.update_cluster_kafka_version.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    update_cluster_kafka_version("test-cluster_arn", "test-current_version", "test-target_kafka_version", configuration_info={}, region_name="us-east-1")
    mock_client.update_cluster_kafka_version.assert_called_once()

def test_update_configuration_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import update_configuration
    mock_client = MagicMock()
    mock_client.update_configuration.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    update_configuration("test-arn", {}, description="test-description", region_name="us-east-1")
    mock_client.update_configuration.assert_called_once()

def test_update_monitoring_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import update_monitoring
    mock_client = MagicMock()
    mock_client.update_monitoring.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    update_monitoring("test-cluster_arn", "test-current_version", enhanced_monitoring="test-enhanced_monitoring", open_monitoring="test-open_monitoring", logging_info="test-logging_info", region_name="us-east-1")
    mock_client.update_monitoring.assert_called_once()

def test_update_replication_info_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import update_replication_info
    mock_client = MagicMock()
    mock_client.update_replication_info.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    update_replication_info("test-current_version", "test-replicator_arn", "test-source_kafka_cluster_arn", "test-target_kafka_cluster_arn", consumer_group_replication="test-consumer_group_replication", topic_replication="test-topic_replication", region_name="us-east-1")
    mock_client.update_replication_info.assert_called_once()

def test_update_security_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import update_security
    mock_client = MagicMock()
    mock_client.update_security.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    update_security("test-cluster_arn", "test-current_version", client_authentication="test-client_authentication", encryption_info="test-encryption_info", region_name="us-east-1")
    mock_client.update_security.assert_called_once()

def test_update_storage_with_options(monkeypatch):
    from unittest.mock import MagicMock
    from aws_util.msk import update_storage
    mock_client = MagicMock()
    mock_client.update_storage.return_value = {}
    monkeypatch.setattr("aws_util.msk.get_client", lambda *a, **kw: mock_client)
    update_storage("test-cluster_arn", "test-current_version", provisioned_throughput="test-provisioned_throughput", storage_mode="test-storage_mode", volume_size_gb=1, region_name="us-east-1")
    mock_client.update_storage.assert_called_once()
