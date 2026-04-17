"""Tests for aws_util.cache_ops module."""
from __future__ import annotations

import json
import time
from typing import Any
from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

import aws_util.cache_ops as mod
from aws_util.cache_ops import (
    CacheInvalidationResult,
    CacheWarmerResult,
    MemoryDBSnapshotResult,
    elasticache_cache_invalidator,
    elasticache_warmer,
    memorydb_snapshot_to_s3,
)

REGION = "us-east-1"


def _client_error(code: str, msg: str = "err") -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": msg}}, "op")


def _mock() -> MagicMock:
    return MagicMock()


# ==================================================================
# Model tests
# ==================================================================


class TestModels:
    def test_cache_warmer_result(self) -> None:
        r = CacheWarmerResult(items_loaded=10, cluster_endpoint="redis.host:6379", errors=1)
        assert r.items_loaded == 10
        assert r.cluster_endpoint == "redis.host:6379"

    def test_cache_invalidation_result(self) -> None:
        r = CacheInvalidationResult(
            keys_to_invalidate=["k1", "k2"],
            cluster_endpoint="redis.host:6379",
            records_processed=5,
        )
        assert len(r.keys_to_invalidate) == 2
        assert r.records_processed == 5

    def test_memorydb_snapshot_result(self) -> None:
        r = MemoryDBSnapshotResult(
            snapshot_name="snap1", snapshot_arn="arn:snap",
            status="available", s3_key="path/metadata.json",
        )
        assert r.status == "available"

    def test_frozen(self) -> None:
        r = CacheWarmerResult(items_loaded=0, cluster_endpoint="", errors=0)
        with pytest.raises(Exception):
            r.items_loaded = 1  # type: ignore[misc]


# ==================================================================
# _extract_ddb_value
# ==================================================================


class TestExtractDdbValue:
    def test_string_type(self) -> None:
        assert mod._extract_ddb_value({"S": "hello"}) == "hello"

    def test_number_type(self) -> None:
        assert mod._extract_ddb_value({"N": "42"}) == "42"

    def test_bool_type(self) -> None:
        assert mod._extract_ddb_value({"BOOL": True}) == "True"

    def test_null_type(self) -> None:
        assert mod._extract_ddb_value({"NULL": True}) == "True"

    def test_complex_type_json(self) -> None:
        val = mod._extract_ddb_value({"L": [{"S": "a"}]})
        parsed = json.loads(val)
        assert "L" in parsed


# ==================================================================
# _describe_elasticache_endpoint
# ==================================================================


class TestDescribeElasticacheEndpoint:
    def test_redis_replication_group(self) -> None:
        client = _mock()
        client.describe_replication_groups.return_value = {
            "ReplicationGroups": [
                {
                    "NodeGroups": [
                        {"PrimaryEndpoint": {"Address": "redis.cluster.com", "Port": 6379}}
                    ]
                }
            ]
        }
        addr, port = mod._describe_elasticache_endpoint(client, "my-cluster")
        assert addr == "redis.cluster.com"
        assert port == 6379

    def test_memcached_cluster(self) -> None:
        client = _mock()
        client.describe_replication_groups.side_effect = _client_error("ReplicationGroupNotFoundFault")
        client.describe_cache_clusters.return_value = {
            "CacheClusters": [
                {
                    "ConfigurationEndpoint": {"Address": "mc.host.com", "Port": 11211}
                }
            ]
        }
        addr, port = mod._describe_elasticache_endpoint(client, "my-mc-cluster")
        assert addr == "mc.host.com"
        assert port == 11211

    def test_memcached_cluster_with_nodes(self) -> None:
        client = _mock()
        client.describe_replication_groups.side_effect = _client_error("NotFound")
        client.describe_cache_clusters.return_value = {
            "CacheClusters": [
                {
                    "CacheNodes": [
                        {"Endpoint": {"Address": "node1.host.com", "Port": 6379}}
                    ]
                }
            ]
        }
        addr, port = mod._describe_elasticache_endpoint(client, "cluster-id")
        assert addr == "node1.host.com"
        assert port == 6379

    def test_no_groups_no_clusters(self) -> None:
        client = _mock()
        client.describe_replication_groups.return_value = {"ReplicationGroups": []}
        client.describe_cache_clusters.return_value = {"CacheClusters": []}
        addr, port = mod._describe_elasticache_endpoint(client, "nonexistent")
        assert addr == ""
        assert port == 0

    def test_both_calls_error(self) -> None:
        client = _mock()
        client.describe_replication_groups.side_effect = _client_error("Error")
        client.describe_cache_clusters.side_effect = _client_error("Error")
        addr, port = mod._describe_elasticache_endpoint(client, "bad-cluster")
        assert addr == ""
        assert port == 0


# ==================================================================
# elasticache_warmer
# ==================================================================


class TestElasticacheWarmer:
    def _build_clients(
        self,
        ec: MagicMock | None = None,
        ddb: MagicMock | None = None,
    ) -> Any:
        _ec = ec or _mock()
        _ddb = ddb or _mock()

        def factory(service, region_name=None):
            if service == "elasticache":
                return _ec
            if service == "dynamodb":
                return _ddb
            return _mock()
        return factory, _ec, _ddb

    def _with_redis_endpoint(self, ec: MagicMock) -> None:
        ec.describe_replication_groups.return_value = {
            "ReplicationGroups": [
                {"NodeGroups": [{"PrimaryEndpoint": {"Address": "redis.host", "Port": 6379}}]}
            ]
        }

    def test_success(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        ddb = _mock()
        ddb.scan.return_value = {
            "Items": [
                {"cache_key": {"S": "k1"}, "cache_value": {"S": "v1"}},
                {"cache_key": {"S": "k2"}, "cache_value": {"S": "v2"}},
            ]
        }
        factory, _, _ = self._build_clients(ec=ec, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = elasticache_warmer(
            cluster_id="my-cluster",
            table_name="seed-table",
            key_attribute="cache_key",
            value_attribute="cache_value",
            region_name=REGION,
        )
        assert result.items_loaded == 2
        assert result.cluster_endpoint == "redis.host:6379"
        assert result.errors == 0

    def test_endpoint_not_found(self, monkeypatch) -> None:
        ec = _mock()
        ec.describe_replication_groups.return_value = {"ReplicationGroups": []}
        ec.describe_cache_clusters.return_value = {"CacheClusters": []}
        factory, _, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            elasticache_warmer(
                cluster_id="bad", table_name="t",
                key_attribute="k", value_attribute="v",
                region_name=REGION,
            )

    def test_missing_attributes_counted_as_errors(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        ddb = _mock()
        ddb.scan.return_value = {
            "Items": [
                {"cache_key": {"S": "k1"}},  # missing value_attribute
                {"other": {"S": "x"}},  # missing both
            ]
        }
        factory, _, _ = self._build_clients(ec=ec, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = elasticache_warmer(
            cluster_id="c", table_name="t",
            key_attribute="cache_key", value_attribute="cache_value",
            region_name=REGION,
        )
        assert result.items_loaded == 0
        assert result.errors == 2

    def test_scan_pagination(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        ddb = _mock()
        ddb.scan.side_effect = [
            {
                "Items": [{"k": {"S": "k1"}, "v": {"S": "v1"}}],
                "LastEvaluatedKey": {"k": {"S": "k1"}},
            },
            {
                "Items": [{"k": {"S": "k2"}, "v": {"S": "v2"}}],
            },
        ]
        factory, _, _ = self._build_clients(ec=ec, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        result = elasticache_warmer(
            cluster_id="c", table_name="t",
            key_attribute="k", value_attribute="v",
            region_name=REGION,
        )
        assert result.items_loaded == 2
        assert ddb.scan.call_count == 2

    def test_scan_error(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        ddb = _mock()
        ddb.scan.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(ec=ec, ddb=ddb)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            elasticache_warmer(
                cluster_id="c", table_name="t",
                key_attribute="k", value_attribute="v",
                region_name=REGION,
            )


# ==================================================================
# elasticache_cache_invalidator
# ==================================================================


class TestElasticacheCacheInvalidator:
    def _build_clients(self, ec: MagicMock | None = None) -> Any:
        _ec = ec or _mock()

        def factory(service, region_name=None):
            if service == "elasticache":
                return _ec
            return _mock()
        return factory, _ec

    def _with_redis_endpoint(self, ec: MagicMock) -> None:
        ec.describe_replication_groups.return_value = {
            "ReplicationGroups": [
                {"NodeGroups": [{"PrimaryEndpoint": {"Address": "redis.host", "Port": 6379}}]}
            ]
        }

    def test_success(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        factory, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        records = [
            {
                "eventName": "MODIFY",
                "dynamodb": {
                    "Keys": {"pk": {"S": "user-1"}, "sk": {"S": "profile"}},
                },
            },
            {
                "eventName": "REMOVE",
                "dynamodb": {
                    "Keys": {"pk": {"S": "user-2"}},
                },
            },
        ]

        result = elasticache_cache_invalidator(
            cluster_id="c", stream_records=records,
            region_name=REGION,
        )
        assert result.records_processed == 2
        assert len(result.keys_to_invalidate) == 2
        assert result.cluster_endpoint == "redis.host:6379"

    def test_with_key_prefix(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        factory, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        records = [
            {
                "eventName": "INSERT",
                "dynamodb": {"Keys": {"pk": {"S": "k1"}}},
            },
        ]

        result = elasticache_cache_invalidator(
            cluster_id="c", stream_records=records,
            key_prefix="cache:",
            region_name=REGION,
        )
        assert all(k.startswith("cache:") for k in result.keys_to_invalidate)

    def test_duplicate_keys_deduplicated(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        factory, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        records = [
            {"eventName": "MODIFY", "dynamodb": {"Keys": {"pk": {"S": "k1"}}}},
            {"eventName": "MODIFY", "dynamodb": {"Keys": {"pk": {"S": "k1"}}}},
        ]

        result = elasticache_cache_invalidator(
            cluster_id="c", stream_records=records,
            region_name=REGION,
        )
        assert len(result.keys_to_invalidate) == 1
        assert result.records_processed == 2

    def test_record_with_no_keys(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        factory, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        records = [
            {"eventName": "MODIFY", "dynamodb": {"Keys": {}}},
            {"eventName": "MODIFY", "dynamodb": {}},
        ]

        result = elasticache_cache_invalidator(
            cluster_id="c", stream_records=records,
            region_name=REGION,
        )
        assert len(result.keys_to_invalidate) == 0
        assert result.records_processed == 2

    def test_empty_records(self, monkeypatch) -> None:
        ec = _mock()
        self._with_redis_endpoint(ec)
        factory, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        result = elasticache_cache_invalidator(
            cluster_id="c", stream_records=[],
            region_name=REGION,
        )
        assert result.records_processed == 0
        assert result.keys_to_invalidate == []

    def test_endpoint_not_found(self, monkeypatch) -> None:
        ec = _mock()
        ec.describe_replication_groups.return_value = {"ReplicationGroups": []}
        ec.describe_cache_clusters.return_value = {"CacheClusters": []}
        factory, _ = self._build_clients(ec=ec)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            elasticache_cache_invalidator(
                cluster_id="bad", stream_records=[],
                region_name=REGION,
            )


# ==================================================================
# memorydb_snapshot_to_s3
# ==================================================================


class TestMemorydbSnapshotToS3:
    def _build_clients(
        self,
        memorydb: MagicMock | None = None,
        s3: MagicMock | None = None,
    ) -> Any:
        _memorydb = memorydb or _mock()
        _s3 = s3 or _mock()

        def factory(service, region_name=None):
            if service == "memorydb":
                return _memorydb
            if service == "s3":
                return _s3
            return _mock()
        return factory, _memorydb, _s3

    def test_success(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.return_value = {
            "Snapshots": [{"ARN": "arn:snap", "Status": "available"}]
        }
        s3 = _mock()
        factory, _, _ = self._build_clients(memorydb=mdb, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = memorydb_snapshot_to_s3(
            cluster_name="my-cluster",
            snapshot_name="snap-1",
            bucket="dr-bucket",
            region_name=REGION,
        )
        assert result.snapshot_name == "snap-1"
        assert result.snapshot_arn == "arn:snap"
        assert result.status == "available"
        assert result.s3_key is not None
        assert "snap-1" in result.s3_key
        s3.put_object.assert_called_once()

    def test_create_snapshot_error(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(memorydb=mdb)
        monkeypatch.setattr(mod, "get_client", factory)

        with pytest.raises(RuntimeError):
            memorydb_snapshot_to_s3(
                cluster_name="c", snapshot_name="s",
                bucket="b", region_name=REGION,
            )

    def test_describe_snapshots_error(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.side_effect = _client_error("InternalServerError")
        factory, _, _ = self._build_clients(memorydb=mdb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        with pytest.raises(RuntimeError):
            memorydb_snapshot_to_s3(
                cluster_name="c", snapshot_name="s",
                bucket="b", region_name=REGION,
            )

    def test_snapshot_terminal_failed(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.return_value = {
            "Snapshots": [{"ARN": "arn:snap", "Status": "failed"}]
        }
        factory, _, _ = self._build_clients(memorydb=mdb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        with pytest.raises(RuntimeError):
            memorydb_snapshot_to_s3(
                cluster_name="c", snapshot_name="s",
                bucket="b", region_name=REGION,
            )

    def test_snapshot_terminal_deleted(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.return_value = {
            "Snapshots": [{"ARN": "arn:snap", "Status": "deleted"}]
        }
        factory, _, _ = self._build_clients(memorydb=mdb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        with pytest.raises(RuntimeError):
            memorydb_snapshot_to_s3(
                cluster_name="c", snapshot_name="s",
                bucket="b", region_name=REGION,
            )

    def test_snapshot_timeout(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.return_value = {
            "Snapshots": [{"ARN": "arn:snap", "Status": "creating"}]
        }
        factory, _, _ = self._build_clients(memorydb=mdb)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)
        # Make time.time() expire immediately
        call_count = [0]
        base = time.time()

        def fake_time():
            call_count[0] += 1
            if call_count[0] <= 2:
                return base
            return base + 2000  # past deadline
        monkeypatch.setattr(mod.time, "time", fake_time)

        with pytest.raises(RuntimeError):
            memorydb_snapshot_to_s3(
                cluster_name="c", snapshot_name="s",
                bucket="b", region_name=REGION,
            )

    def test_s3_write_error_swallowed(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.return_value = {
            "Snapshots": [{"ARN": "arn:snap", "Status": "available"}]
        }
        s3 = _mock()
        s3.put_object.side_effect = _client_error("AccessDenied")
        factory, _, _ = self._build_clients(memorydb=mdb, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = memorydb_snapshot_to_s3(
            cluster_name="c", snapshot_name="s",
            bucket="b", region_name=REGION,
        )
        assert result.status == "available"
        assert result.s3_key is None

    def test_custom_key_prefix(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.return_value = {
            "Snapshots": [{"ARN": "arn:snap", "Status": "available"}]
        }
        s3 = _mock()
        factory, _, _ = self._build_clients(memorydb=mdb, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = memorydb_snapshot_to_s3(
            cluster_name="c", snapshot_name="s",
            bucket="b", key_prefix="custom/",
            region_name=REGION,
        )
        assert result.s3_key is not None
        assert result.s3_key.startswith("custom/")

    def test_polling_waits_then_available(self, monkeypatch) -> None:
        mdb = _mock()
        mdb.create_snapshot.return_value = {
            "Snapshot": {"ARN": "arn:snap", "Status": "creating"}
        }
        mdb.describe_snapshots.side_effect = [
            {"Snapshots": [{"ARN": "arn:snap", "Status": "creating"}]},
            {"Snapshots": [{"ARN": "arn:snap", "Status": "available"}]},
        ]
        s3 = _mock()
        factory, _, _ = self._build_clients(memorydb=mdb, s3=s3)
        monkeypatch.setattr(mod, "get_client", factory)
        monkeypatch.setattr(mod.time, "sleep", lambda x: None)

        result = memorydb_snapshot_to_s3(
            cluster_name="c", snapshot_name="s",
            bucket="b", region_name=REGION,
        )
        assert result.status == "available"
        assert mdb.describe_snapshots.call_count == 2
