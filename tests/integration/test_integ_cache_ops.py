"""Integration tests for aws_util.cache_ops against LocalStack."""
from __future__ import annotations

import pytest

from tests.integration.conftest import REGION, ls_client

pytestmark = pytest.mark.integration


# ---------------------------------------------------------------------------
# 1. elasticache_warmer
# ---------------------------------------------------------------------------


class TestElasticacheWarmer:
    @pytest.mark.skip(reason="ElastiCache not available in LocalStack community")
    def test_warmer_scans_dynamodb_and_resolves_endpoint(self, dynamodb_table):
        from aws_util.cache_ops import elasticache_warmer

        # Seed DynamoDB with a few items
        ddb = ls_client("dynamodb")
        for i in range(3):
            ddb.put_item(
                TableName=dynamodb_table,
                Item={
                    "pk": {"S": f"key-{i}"},
                    "sk": {"S": f"sort-{i}"},
                    "cache_key": {"S": f"ckey-{i}"},
                    "cache_value": {"S": f"cval-{i}"},
                },
            )

        result = elasticache_warmer(
            cluster_id="test-cluster",
            table_name=dynamodb_table,
            key_attribute="cache_key",
            value_attribute="cache_value",
            region_name=REGION,
        )
        assert result.items_loaded >= 0
        assert isinstance(result.cluster_endpoint, str)
        assert isinstance(result.errors, int)


# ---------------------------------------------------------------------------
# 2. elasticache_cache_invalidator
# ---------------------------------------------------------------------------


class TestElasticacheCacheInvalidator:
    @pytest.mark.skip(reason="ElastiCache not available in LocalStack community")
    def test_invalidator_extracts_keys_from_stream_records(self):
        from aws_util.cache_ops import elasticache_cache_invalidator

        stream_records = [
            {
                "eventName": "MODIFY",
                "dynamodb": {
                    "Keys": {
                        "pk": {"S": "user-123"},
                        "sk": {"S": "profile"},
                    }
                },
            },
            {
                "eventName": "REMOVE",
                "dynamodb": {
                    "Keys": {
                        "pk": {"S": "user-456"},
                        "sk": {"S": "settings"},
                    }
                },
            },
        ]

        result = elasticache_cache_invalidator(
            cluster_id="test-cluster",
            stream_records=stream_records,
            key_prefix="app:",
            region_name=REGION,
        )
        assert result.records_processed == 2
        assert len(result.keys_to_invalidate) >= 1
        assert isinstance(result.cluster_endpoint, str)


# ---------------------------------------------------------------------------
# 3. memorydb_snapshot_to_s3
# ---------------------------------------------------------------------------


class TestMemorydbSnapshotToS3:
    @pytest.mark.skip(reason="MemoryDB not available in LocalStack community")
    def test_creates_snapshot_and_writes_metadata_to_s3(self, s3_bucket):
        from aws_util.cache_ops import memorydb_snapshot_to_s3

        result = memorydb_snapshot_to_s3(
            cluster_name="test-cluster",
            snapshot_name="test-snapshot",
            bucket=s3_bucket,
            key_prefix="memorydb-snapshots/",
            region_name=REGION,
        )
        assert result.snapshot_name == "test-snapshot"
        assert isinstance(result.snapshot_arn, str)
        assert result.status in ("available", "creating")
        assert result.s3_key is None or isinstance(result.s3_key, str)
