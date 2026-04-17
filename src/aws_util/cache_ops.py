"""Cache Operations utilities for ElastiCache, DynamoDB Streams, and MemoryDB.

Provides multi-service helpers for cache management workflows:

- **elasticache_warmer** — Scan DynamoDB for seed data, describe ElastiCache endpoint, return
  formatted data ready for cache loading.
- **elasticache_cache_invalidator** — Parse DynamoDB Stream event records, extract changed keys,
  return invalidation set with ElastiCache endpoint.
- **memorydb_snapshot_to_s3** — Create a MemoryDB snapshot, wait for availability, copy metadata
  to S3 for cross-region DR.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from botocore.exceptions import ClientError
from pydantic import BaseModel, ConfigDict

from aws_util._client import get_client
from aws_util.exceptions import wrap_aws_error

logger = logging.getLogger(__name__)

__all__ = [
    "CacheInvalidationResult",
    "CacheWarmerResult",
    "MemoryDBSnapshotResult",
    "elasticache_cache_invalidator",
    "elasticache_warmer",
    "memorydb_snapshot_to_s3",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class CacheWarmerResult(BaseModel):
    """Result of preparing ElastiCache seed data from DynamoDB."""

    model_config = ConfigDict(frozen=True)

    items_loaded: int
    cluster_endpoint: str
    errors: int


class CacheInvalidationResult(BaseModel):
    """Result of computing cache invalidation keys from DynamoDB Stream records."""

    model_config = ConfigDict(frozen=True)

    keys_to_invalidate: list[str]
    cluster_endpoint: str
    records_processed: int


class MemoryDBSnapshotResult(BaseModel):
    """Result of creating and exporting a MemoryDB snapshot."""

    model_config = ConfigDict(frozen=True)

    snapshot_name: str
    snapshot_arn: str
    status: str
    s3_key: str | None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_ddb_value(attr: dict[str, Any]) -> str:
    """Extract the scalar string value from a DynamoDB attribute map."""
    for type_key in ("S", "N", "BOOL", "NULL"):
        if type_key in attr:
            return str(attr[type_key])
    return json.dumps(attr)


def _describe_elasticache_endpoint(
    client: Any,
    cluster_id: str,
) -> tuple[str, int]:
    """Return ``(endpoint_address, port)`` for a Redis replication group or Memcached cluster."""
    # Try Redis replication group first
    try:
        rg_resp = client.describe_replication_groups(ReplicationGroupId=cluster_id)
        groups = rg_resp.get("ReplicationGroups", [])
        if groups:
            node_groups = groups[0].get("NodeGroups", [])
            if node_groups:
                ep = node_groups[0].get("PrimaryEndpoint", {})
                return ep.get("Address", ""), ep.get("Port", 6379)
    except ClientError:
        pass

    # Fall back to Memcached cluster
    try:
        mc_resp = client.describe_cache_clusters(
            CacheClusterId=cluster_id,
            ShowCacheNodeInfo=True,
        )
        clusters = mc_resp.get("CacheClusters", [])
        if clusters:
            config_ep = clusters[0].get("ConfigurationEndpoint")
            if config_ep:
                return config_ep.get("Address", ""), config_ep.get("Port", 11211)
            nodes = clusters[0].get("CacheNodes", [])
            if nodes:
                ep = nodes[0].get("Endpoint", {})
                return ep.get("Address", ""), ep.get("Port", 6379)
    except ClientError:
        pass

    return "", 0


# ---------------------------------------------------------------------------
# 1. elasticache_warmer
# ---------------------------------------------------------------------------


def elasticache_warmer(
    cluster_id: str,
    table_name: str,
    key_attribute: str,
    value_attribute: str,
    region_name: str | None = None,
) -> CacheWarmerResult:
    """Pre-populate an ElastiCache cluster by reading seed data from DynamoDB.

    Describes the ElastiCache cluster to obtain its endpoint, then scans *table_name*
    extracting *key_attribute* / *value_attribute* pairs. Because direct Redis protocol
    requires a VPC network path (not an AWS API), the function returns the endpoint and
    the count of items prepared so the caller can load them with their preferred client.

    Args:
        cluster_id: ElastiCache cluster or replication group identifier.
        table_name: DynamoDB table to scan for seed data.
        key_attribute: DynamoDB attribute name to use as the Redis key.
        value_attribute: DynamoDB attribute name to use as the Redis value.
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`CacheWarmerResult` with endpoint, item count, and error count.

    Raises:
        AwsUtilError: If the ElastiCache endpoint cannot be resolved.
    """
    elasticache = get_client("elasticache", region_name)
    dynamodb = get_client("dynamodb", region_name)

    endpoint, port = _describe_elasticache_endpoint(elasticache, cluster_id)
    if not endpoint:
        raise wrap_aws_error(
            RuntimeError(f"Could not resolve endpoint for ElastiCache cluster {cluster_id!r}"),
            "elasticache_warmer",
        )

    cluster_endpoint = f"{endpoint}:{port}"
    items_loaded = 0
    errors = 0

    scan_kwargs: dict[str, Any] = {"TableName": table_name}
    while True:
        try:
            scan_resp = dynamodb.scan(**scan_kwargs)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"dynamodb.scan({table_name!r})") from exc

        for item in scan_resp.get("Items", []):
            key_attr = item.get(key_attribute)
            value_attr = item.get(value_attribute)
            if key_attr and value_attr:
                try:
                    _extract_ddb_value(key_attr)
                    _extract_ddb_value(value_attr)
                    items_loaded += 1
                except Exception as exc:
                    logger.warning("Skipping item due to extraction error: %s", exc)
                    errors += 1
            else:
                errors += 1

        last_key = scan_resp.get("LastEvaluatedKey")
        if not last_key:
            break
        scan_kwargs["ExclusiveStartKey"] = last_key

    logger.info(
        "ElastiCache warmer: cluster %s at %s, %d items prepared, %d errors",
        cluster_id,
        cluster_endpoint,
        items_loaded,
        errors,
    )

    return CacheWarmerResult(
        items_loaded=items_loaded,
        cluster_endpoint=cluster_endpoint,
        errors=errors,
    )


# ---------------------------------------------------------------------------
# 2. elasticache_cache_invalidator
# ---------------------------------------------------------------------------


def elasticache_cache_invalidator(
    cluster_id: str,
    stream_records: list[dict[str, Any]],
    key_prefix: str = "",
    region_name: str | None = None,
) -> CacheInvalidationResult:
    """Extract invalidation keys from DynamoDB stream event records and look up cluster endpoint.

    Parses pre-fetched DynamoDB stream event records (in the Lambda event format with
    ``eventName`` and ``dynamodb`` fields), derives cache keys from the changed items'
    primary key attributes, and describes the ElastiCache cluster endpoint.

    Args:
        cluster_id: ElastiCache cluster or replication group identifier.
        stream_records: List of DynamoDB stream event record dicts (already parsed from
            a Kinesis/Lambda event). Each dict should contain ``eventName`` and ``dynamodb``
            keys following the DynamoDB Streams record format.
        key_prefix: String prefix to prepend to every cache key (default ``""``).
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`CacheInvalidationResult` with keys to invalidate, endpoint, and record count.

    Raises:
        AwsUtilError: If the ElastiCache endpoint cannot be resolved.
    """
    elasticache = get_client("elasticache", region_name)

    keys_to_invalidate: list[str] = []
    records_processed = 0

    for record in stream_records:
        records_processed += 1
        event_name = record.get("eventName", "")
        dynamodb_data = record.get("dynamodb", {})
        keys = dynamodb_data.get("Keys", {})

        if not keys:
            continue

        # Build a composite cache key from sorted primary key attributes
        key_parts = []
        for attr_name in sorted(keys.keys()):
            key_parts.append(f"{attr_name}={_extract_ddb_value(keys[attr_name])}")

        if key_parts:
            raw_key = ":".join(key_parts)
            cache_key = f"{key_prefix}{raw_key}" if key_prefix else raw_key
            if cache_key not in keys_to_invalidate:
                keys_to_invalidate.append(cache_key)
                logger.debug(
                    "Queued cache invalidation for key=%s (event=%s)", cache_key, event_name
                )

    # Describe ElastiCache endpoint
    endpoint, port = _describe_elasticache_endpoint(elasticache, cluster_id)
    if not endpoint:
        raise wrap_aws_error(
            RuntimeError(f"Could not resolve endpoint for ElastiCache cluster {cluster_id!r}"),
            "elasticache_cache_invalidator",
        )

    cluster_endpoint = f"{endpoint}:{port}"

    logger.info(
        "Cache invalidator: %d records processed, %d keys to invalidate at %s",
        records_processed,
        len(keys_to_invalidate),
        cluster_endpoint,
    )

    return CacheInvalidationResult(
        keys_to_invalidate=keys_to_invalidate,
        cluster_endpoint=cluster_endpoint,
        records_processed=records_processed,
    )


# ---------------------------------------------------------------------------
# 3. memorydb_snapshot_to_s3
# ---------------------------------------------------------------------------

_MEMORYDB_POLL_INTERVAL = 15  # seconds
_MEMORYDB_MAX_WAIT = 900  # 15 minutes


def memorydb_snapshot_to_s3(
    cluster_name: str,
    snapshot_name: str,
    bucket: str,
    key_prefix: str = "memorydb-snapshots/",
    region_name: str | None = None,
) -> MemoryDBSnapshotResult:
    """Create a MemoryDB snapshot, wait for completion, then copy snapshot metadata to S3.

    Workflow:
    1. Create a MemoryDB snapshot for *cluster_name*.
    2. Poll ``describe_snapshots`` until the snapshot status is ``"available"``.
    3. Write snapshot metadata JSON to S3 at ``{key_prefix}{snapshot_name}/metadata.json``
       for cross-region DR reference.

    Args:
        cluster_name: Name of the MemoryDB cluster to snapshot.
        snapshot_name: Name to assign to the new snapshot.
        bucket: S3 bucket for snapshot metadata export.
        key_prefix: S3 key prefix under *bucket* (default ``"memorydb-snapshots/"``).
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`MemoryDBSnapshotResult` with snapshot ARN, status, and S3 key written.

    Raises:
        AwsUtilError: If snapshot creation fails or reaches a terminal error state.
    """
    memorydb = get_client("memorydb", region_name)
    s3 = get_client("s3", region_name)

    # Create snapshot
    try:
        create_resp = memorydb.create_snapshot(
            ClusterName=cluster_name,
            SnapshotName=snapshot_name,
        )
        snapshot = create_resp.get("Snapshot", {})
        snapshot_arn = snapshot.get("ARN", "")
        status = snapshot.get("Status", "creating")
    except ClientError as exc:
        raise wrap_aws_error(exc, f"memorydb.create_snapshot({snapshot_name!r})") from exc

    logger.info(
        "MemoryDB snapshot %s created (ARN=%s) — polling for availability",
        snapshot_name,
        snapshot_arn,
    )

    # Poll until available
    deadline = time.time() + _MEMORYDB_MAX_WAIT
    while time.time() < deadline:
        try:
            desc_resp = memorydb.describe_snapshots(SnapshotName=snapshot_name)
            snapshots = desc_resp.get("Snapshots", [])
            if snapshots:
                status = snapshots[0].get("Status", status)
                snapshot_arn = snapshots[0].get("ARN", snapshot_arn)
        except ClientError as exc:
            raise wrap_aws_error(exc, f"memorydb.describe_snapshots({snapshot_name!r})") from exc

        if status == "available":
            break
        if status in ("failed", "deleted"):
            raise wrap_aws_error(
                RuntimeError(
                    f"MemoryDB snapshot {snapshot_name!r} reached terminal state: {status}"
                ),
                "memorydb_snapshot_to_s3",
            )

        logger.debug(
            "MemoryDB snapshot %s status: %s — waiting %ds",
            snapshot_name,
            status,
            _MEMORYDB_POLL_INTERVAL,
        )
        time.sleep(_MEMORYDB_POLL_INTERVAL)
    else:
        raise wrap_aws_error(
            TimeoutError(
                f"MemoryDB snapshot {snapshot_name!r} did not become available within {_MEMORYDB_MAX_WAIT}s"
            ),
            "memorydb_snapshot_to_s3",
        )

    # Copy snapshot metadata to S3
    s3_key: str | None = None
    metadata_key = f"{key_prefix.rstrip('/')}/{snapshot_name}/metadata.json"
    metadata = {
        "cluster_name": cluster_name,
        "snapshot_name": snapshot_name,
        "snapshot_arn": snapshot_arn,
        "status": status,
        "exported_at": int(time.time()),
    }
    try:
        s3.put_object(
            Bucket=bucket,
            Key=metadata_key,
            Body=json.dumps(metadata).encode("utf-8"),
            ContentType="application/json",
        )
        s3_key = metadata_key
        logger.info("MemoryDB snapshot metadata written to s3://%s/%s", bucket, metadata_key)
    except ClientError as exc:
        logger.warning("Failed to write snapshot metadata to S3: %s", exc)

    return MemoryDBSnapshotResult(
        snapshot_name=snapshot_name,
        snapshot_arn=snapshot_arn,
        status=status,
        s3_key=s3_key,
    )
