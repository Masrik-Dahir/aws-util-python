"""Native async Kinesis utilities — real non-blocking I/O via :mod:`aws_util.aio._engine`."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.kinesis import (
    DescribeAccountSettingsResult,
    DescribeLimitsResult,
    DescribeStreamConsumerResult,
    DescribeStreamSummaryResult,
    DisableEnhancedMonitoringResult,
    EnableEnhancedMonitoringResult,
    GetResourcePolicyResult,
    GetShardIteratorResult,
    KinesisPutResult,
    KinesisRecord,
    KinesisStream,
    ListShardsResult,
    ListStreamConsumersResult,
    ListTagsForResourceResult,
    ListTagsForStreamResult,
    RegisterStreamConsumerResult,
    SubscribeToShardResult,
    UpdateAccountSettingsResult,
    UpdateShardCountResult,
    UpdateStreamWarmThroughputResult,
)

__all__ = [
    "DescribeAccountSettingsResult",
    "DescribeLimitsResult",
    "DescribeStreamConsumerResult",
    "DescribeStreamSummaryResult",
    "DisableEnhancedMonitoringResult",
    "EnableEnhancedMonitoringResult",
    "GetResourcePolicyResult",
    "GetShardIteratorResult",
    "KinesisPutResult",
    "KinesisRecord",
    "KinesisStream",
    "ListShardsResult",
    "ListStreamConsumersResult",
    "ListTagsForResourceResult",
    "ListTagsForStreamResult",
    "RegisterStreamConsumerResult",
    "SubscribeToShardResult",
    "UpdateAccountSettingsResult",
    "UpdateShardCountResult",
    "UpdateStreamWarmThroughputResult",
    "add_tags_to_stream",
    "consume_stream",
    "create_stream",
    "decrease_stream_retention_period",
    "delete_resource_policy",
    "delete_stream",
    "deregister_stream_consumer",
    "describe_account_settings",
    "describe_limits",
    "describe_stream",
    "describe_stream_consumer",
    "describe_stream_summary",
    "disable_enhanced_monitoring",
    "enable_enhanced_monitoring",
    "get_records",
    "get_resource_policy",
    "get_shard_iterator",
    "increase_stream_retention_period",
    "list_shards",
    "list_stream_consumers",
    "list_streams",
    "list_tags_for_resource",
    "list_tags_for_stream",
    "merge_shards",
    "put_record",
    "put_records",
    "put_resource_policy",
    "register_stream_consumer",
    "remove_tags_from_stream",
    "split_shard",
    "start_stream_encryption",
    "stop_stream_encryption",
    "subscribe_to_shard",
    "tag_resource",
    "untag_resource",
    "update_account_settings",
    "update_max_record_size",
    "update_shard_count",
    "update_stream_mode",
    "update_stream_warm_throughput",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _encode_data(data: bytes | str | dict | list) -> bytes:
    """Encode a record payload to bytes."""
    if isinstance(data, bytes):
        return data
    if isinstance(data, (dict, list)):
        return json.dumps(data).encode("utf-8")
    return data.encode("utf-8")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def put_record(
    stream_name: str,
    data: bytes | str | dict | list,
    partition_key: str,
    region_name: str | None = None,
) -> KinesisRecord:
    """Publish a single record to a Kinesis data stream.

    Args:
        stream_name: Name of the Kinesis stream.
        data: Record payload.  Dicts/lists are JSON-encoded; strings are
            UTF-8 encoded.
        partition_key: Determines the shard the record is routed to.
        region_name: AWS region override.

    Returns:
        A :class:`KinesisRecord` with the assigned shard and sequence number.

    Raises:
        RuntimeError: If the put fails.
    """
    raw = _encode_data(data)
    try:
        client = async_client("kinesis", region_name)
        resp = await client.call(
            "PutRecord",
            StreamName=stream_name,
            Data=raw,
            PartitionKey=partition_key,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"put_record failed on stream {stream_name!r}") from exc
    return KinesisRecord(
        shard_id=resp["ShardId"],
        sequence_number=resp["SequenceNumber"],
    )


async def put_records(
    stream_name: str,
    records: list[dict[str, Any]],
    region_name: str | None = None,
) -> KinesisPutResult:
    """Publish up to 500 records to a Kinesis data stream in one request.

    Each record in *records* must be a dict with keys:

    * ``"data"`` -- payload (bytes, str, dict, or list)
    * ``"partition_key"`` -- routing key

    Args:
        stream_name: Name of the Kinesis stream.
        records: List of record dicts (up to 500, max 5 MB total).
        region_name: AWS region override.

    Returns:
        A :class:`KinesisPutResult` describing successes and failures.

    Raises:
        RuntimeError: If the API call fails.
        ValueError: If more than 500 records are supplied.
    """
    if len(records) > 500:
        raise ValueError("put_records supports at most 500 records per call")

    entries = [
        {
            "Data": _encode_data(r["data"]),
            "PartitionKey": r["partition_key"],
        }
        for r in records
    ]
    try:
        client = async_client("kinesis", region_name)
        resp = await client.call("PutRecords", StreamName=stream_name, Records=entries)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"put_records failed on stream {stream_name!r}") from exc
    return KinesisPutResult(
        failed_record_count=resp.get("FailedRecordCount", 0),
        records=resp.get("Records", []),
    )


async def list_streams(
    region_name: str | None = None,
) -> list[str]:
    """List the names of all Kinesis data streams in the account.

    Args:
        region_name: AWS region override.

    Returns:
        A list of stream names.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        client = async_client("kinesis", region_name)
        items = await client.paginate(
            "ListStreams",
            result_key="StreamNames",
            token_input="NextToken",
            token_output="NextToken",
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_streams failed") from exc
    return [str(s) for s in items]


async def describe_stream(
    stream_name: str,
    region_name: str | None = None,
) -> KinesisStream:
    """Describe a Kinesis data stream.

    Args:
        stream_name: Name of the stream.
        region_name: AWS region override.

    Returns:
        A :class:`KinesisStream` with current metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        client = async_client("kinesis", region_name)
        resp = await client.call("DescribeStreamSummary", StreamName=stream_name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"describe_stream failed for {stream_name!r}") from exc
    desc = resp["StreamDescriptionSummary"]
    return KinesisStream(
        stream_name=desc["StreamName"],
        stream_arn=desc["StreamARN"],
        stream_status=desc["StreamStatus"],
        shard_count=desc.get("OpenShardCount", 0),
        retention_period_hours=desc.get("RetentionPeriodHours", 24),
        creation_timestamp=desc.get("StreamCreationTimestamp"),
    )


async def get_records(
    stream_name: str,
    shard_id: str,
    shard_iterator_type: str = "TRIM_HORIZON",
    limit: int = 100,
    region_name: str | None = None,
) -> list[dict[str, Any]]:
    """Read records from a specific Kinesis shard.

    Decodes base64-encoded data payloads automatically.  JSON payloads are
    parsed into dicts.

    Args:
        stream_name: Name of the Kinesis stream.
        shard_id: The shard to read from.
        shard_iterator_type: Starting position -- ``"TRIM_HORIZON"`` (oldest),
            ``"LATEST"`` (newest), ``"AT_SEQUENCE_NUMBER"``, or
            ``"AFTER_SEQUENCE_NUMBER"``.
        limit: Maximum number of records to return (default 100).
        region_name: AWS region override.

    Returns:
        A list of record dicts with decoded ``data``, ``sequence_number``,
        ``partition_key``, and ``approximate_arrival_timestamp``.

    Raises:
        RuntimeError: If the API call fails.
    """
    try:
        client = async_client("kinesis", region_name)
        iter_resp = await client.call(
            "GetShardIterator",
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType=shard_iterator_type,
        )
        resp = await client.call(
            "GetRecords",
            ShardIterator=iter_resp["ShardIterator"],
            Limit=limit,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"get_records failed for {stream_name!r}/{shard_id!r}") from exc

    result: list[dict[str, Any]] = []
    for rec in resp.get("Records", []):
        raw = rec["Data"]
        try:
            decoded = json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError):
            decoded = raw if isinstance(raw, bytes) else raw
        result.append(
            {
                "data": decoded,
                "sequence_number": rec["SequenceNumber"],
                "partition_key": rec["PartitionKey"],
                "approximate_arrival_timestamp": rec.get("ApproximateArrivalTimestamp"),
            }
        )
    return result


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def consume_stream(
    stream_name: str,
    handler: Any,
    shard_iterator_type: str = "LATEST",
    duration_seconds: float = 60.0,
    poll_interval: float = 1.0,
    region_name: str | None = None,
) -> int:
    """Consume records from all shards of a Kinesis stream concurrently.

    Opens one shard iterator per shard and polls concurrently for
    *duration_seconds* seconds, calling ``handler(record)`` for each record.
    Records are dicts with decoded ``data``, ``sequence_number``,
    ``partition_key``, and ``approximate_arrival_timestamp`` fields.

    The handler may be a coroutine function (async) or a regular callable.

    Args:
        stream_name: Name of the Kinesis stream.
        handler: Callable accepting a single record dict.
        shard_iterator_type: Starting position -- ``"LATEST"`` (default) or
            ``"TRIM_HORIZON"`` (oldest available).
        duration_seconds: How long to consume (default ``60`` s).  Set to
            ``float("inf")`` for indefinite consumption.
        poll_interval: Seconds between ``GetRecords`` calls per shard.
        region_name: AWS region override.

    Returns:
        Total number of records processed across all shards.

    Raises:
        RuntimeError: If the stream description or shard reads fail.
    """
    import time as _time

    client = async_client("kinesis", region_name)

    # Verify stream exists
    try:
        await client.call("DescribeStreamSummary", StreamName=stream_name)
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to describe stream {stream_name!r}") from exc

    # List shards
    try:
        shard_resp = await client.call("ListShards", StreamName=stream_name)
        shard_ids = [s["ShardId"] for s in shard_resp.get("Shards", [])]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"Failed to list shards for {stream_name!r}") from exc

    deadline = _time.monotonic() + duration_seconds

    async def _consume_shard(shard_id: str) -> int:
        count = 0
        try:
            iter_resp = await client.call(
                "GetShardIterator",
                StreamName=stream_name,
                ShardId=shard_id,
                ShardIteratorType=shard_iterator_type,
            )
            shard_iter = iter_resp["ShardIterator"]

            while shard_iter and _time.monotonic() < deadline:
                try:
                    rec_resp = await client.call(
                        "GetRecords",
                        ShardIterator=shard_iter,
                        Limit=100,
                    )
                except RuntimeError:
                    break

                for rec in rec_resp.get("Records", []):
                    raw = rec["Data"]
                    try:
                        decoded = json.loads(raw)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        decoded = raw
                    record = {
                        "data": decoded,
                        "sequence_number": rec["SequenceNumber"],
                        "partition_key": rec["PartitionKey"],
                        "approximate_arrival_timestamp": rec.get("ApproximateArrivalTimestamp"),
                    }
                    result = handler(record)
                    if asyncio.iscoroutine(result):
                        await result
                    count += 1

                shard_iter = rec_resp.get("NextShardIterator")
                await asyncio.sleep(poll_interval)
        except Exception:
            pass
        return count

    results = await asyncio.gather(*[_consume_shard(sid) for sid in shard_ids])
    return sum(results)


async def add_tags_to_stream(
    tags: dict[str, Any],
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Add tags to stream.

    Args:
        tags: Tags.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Tags"] = tags
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("AddTagsToStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to add tags to stream") from exc
    return None


async def create_stream(
    stream_name: str,
    *,
    shard_count: int | None = None,
    stream_mode_details: dict[str, Any] | None = None,
    tags: dict[str, Any] | None = None,
    warm_throughput_mi_bps: int | None = None,
    max_record_size_in_ki_b: int | None = None,
    region_name: str | None = None,
) -> None:
    """Create stream.

    Args:
        stream_name: Stream name.
        shard_count: Shard count.
        stream_mode_details: Stream mode details.
        tags: Tags.
        warm_throughput_mi_bps: Warm throughput mi bps.
        max_record_size_in_ki_b: Max record size in ki b.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamName"] = stream_name
    if shard_count is not None:
        kwargs["ShardCount"] = shard_count
    if stream_mode_details is not None:
        kwargs["StreamModeDetails"] = stream_mode_details
    if tags is not None:
        kwargs["Tags"] = tags
    if warm_throughput_mi_bps is not None:
        kwargs["WarmThroughputMiBps"] = warm_throughput_mi_bps
    if max_record_size_in_ki_b is not None:
        kwargs["MaxRecordSizeInKiB"] = max_record_size_in_ki_b
    try:
        await client.call("CreateStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create stream") from exc
    return None


async def decrease_stream_retention_period(
    retention_period_hours: int,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Decrease stream retention period.

    Args:
        retention_period_hours: Retention period hours.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RetentionPeriodHours"] = retention_period_hours
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("DecreaseStreamRetentionPeriod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to decrease stream retention period") from exc
    return None


async def delete_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Delete resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        await client.call("DeleteResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete resource policy") from exc
    return None


async def delete_stream(
    *,
    stream_name: str | None = None,
    enforce_consumer_deletion: bool | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Delete stream.

    Args:
        stream_name: Stream name.
        enforce_consumer_deletion: Enforce consumer deletion.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if enforce_consumer_deletion is not None:
        kwargs["EnforceConsumerDeletion"] = enforce_consumer_deletion
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("DeleteStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete stream") from exc
    return None


async def deregister_stream_consumer(
    *,
    stream_arn: str | None = None,
    consumer_name: str | None = None,
    consumer_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Deregister stream consumer.

    Args:
        stream_arn: Stream arn.
        consumer_name: Consumer name.
        consumer_arn: Consumer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    if consumer_name is not None:
        kwargs["ConsumerName"] = consumer_name
    if consumer_arn is not None:
        kwargs["ConsumerARN"] = consumer_arn
    try:
        await client.call("DeregisterStreamConsumer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to deregister stream consumer") from exc
    return None


async def describe_account_settings(
    region_name: str | None = None,
) -> DescribeAccountSettingsResult:
    """Describe account settings.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe account settings") from exc
    return DescribeAccountSettingsResult(
        minimum_throughput_billing_commitment=resp.get("MinimumThroughputBillingCommitment"),
    )


async def describe_limits(
    region_name: str | None = None,
) -> DescribeLimitsResult:
    """Describe limits.

    Args:

        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}

    try:
        resp = await client.call("DescribeLimits", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe limits") from exc
    return DescribeLimitsResult(
        shard_limit=resp.get("ShardLimit"),
        open_shard_count=resp.get("OpenShardCount"),
        on_demand_stream_count=resp.get("OnDemandStreamCount"),
        on_demand_stream_count_limit=resp.get("OnDemandStreamCountLimit"),
    )


async def describe_stream_consumer(
    *,
    stream_arn: str | None = None,
    consumer_name: str | None = None,
    consumer_arn: str | None = None,
    region_name: str | None = None,
) -> DescribeStreamConsumerResult:
    """Describe stream consumer.

    Args:
        stream_arn: Stream arn.
        consumer_name: Consumer name.
        consumer_arn: Consumer arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    if consumer_name is not None:
        kwargs["ConsumerName"] = consumer_name
    if consumer_arn is not None:
        kwargs["ConsumerARN"] = consumer_arn
    try:
        resp = await client.call("DescribeStreamConsumer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe stream consumer") from exc
    return DescribeStreamConsumerResult(
        consumer_description=resp.get("ConsumerDescription"),
    )


async def describe_stream_summary(
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> DescribeStreamSummaryResult:
    """Describe stream summary.

    Args:
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("DescribeStreamSummary", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to describe stream summary") from exc
    return DescribeStreamSummaryResult(
        stream_description_summary=resp.get("StreamDescriptionSummary"),
    )


async def disable_enhanced_monitoring(
    shard_level_metrics: list[str],
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> DisableEnhancedMonitoringResult:
    """Disable enhanced monitoring.

    Args:
        shard_level_metrics: Shard level metrics.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ShardLevelMetrics"] = shard_level_metrics
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("DisableEnhancedMonitoring", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to disable enhanced monitoring") from exc
    return DisableEnhancedMonitoringResult(
        stream_name=resp.get("StreamName"),
        current_shard_level_metrics=resp.get("CurrentShardLevelMetrics"),
        desired_shard_level_metrics=resp.get("DesiredShardLevelMetrics"),
        stream_arn=resp.get("StreamARN"),
    )


async def enable_enhanced_monitoring(
    shard_level_metrics: list[str],
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> EnableEnhancedMonitoringResult:
    """Enable enhanced monitoring.

    Args:
        shard_level_metrics: Shard level metrics.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ShardLevelMetrics"] = shard_level_metrics
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("EnableEnhancedMonitoring", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to enable enhanced monitoring") from exc
    return EnableEnhancedMonitoringResult(
        stream_name=resp.get("StreamName"),
        current_shard_level_metrics=resp.get("CurrentShardLevelMetrics"),
        desired_shard_level_metrics=resp.get("DesiredShardLevelMetrics"),
        stream_arn=resp.get("StreamARN"),
    )


async def get_resource_policy(
    resource_arn: str,
    region_name: str | None = None,
) -> GetResourcePolicyResult:
    """Get resource policy.

    Args:
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = await client.call("GetResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get resource policy") from exc
    return GetResourcePolicyResult(
        policy=resp.get("Policy"),
    )


async def get_shard_iterator(
    shard_id: str,
    shard_iterator_type: str,
    *,
    stream_name: str | None = None,
    starting_sequence_number: str | None = None,
    timestamp: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> GetShardIteratorResult:
    """Get shard iterator.

    Args:
        shard_id: Shard id.
        shard_iterator_type: Shard iterator type.
        stream_name: Stream name.
        starting_sequence_number: Starting sequence number.
        timestamp: Timestamp.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ShardId"] = shard_id
    kwargs["ShardIteratorType"] = shard_iterator_type
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if starting_sequence_number is not None:
        kwargs["StartingSequenceNumber"] = starting_sequence_number
    if timestamp is not None:
        kwargs["Timestamp"] = timestamp
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("GetShardIterator", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to get shard iterator") from exc
    return GetShardIteratorResult(
        shard_iterator=resp.get("ShardIterator"),
    )


async def increase_stream_retention_period(
    retention_period_hours: int,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Increase stream retention period.

    Args:
        retention_period_hours: Retention period hours.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["RetentionPeriodHours"] = retention_period_hours
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("IncreaseStreamRetentionPeriod", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to increase stream retention period") from exc
    return None


async def list_shards(
    *,
    stream_name: str | None = None,
    next_token: str | None = None,
    exclusive_start_shard_id: str | None = None,
    max_results: int | None = None,
    stream_creation_timestamp: str | None = None,
    shard_filter: dict[str, Any] | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> ListShardsResult:
    """List shards.

    Args:
        stream_name: Stream name.
        next_token: Next token.
        exclusive_start_shard_id: Exclusive start shard id.
        max_results: Max results.
        stream_creation_timestamp: Stream creation timestamp.
        shard_filter: Shard filter.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if exclusive_start_shard_id is not None:
        kwargs["ExclusiveStartShardId"] = exclusive_start_shard_id
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if stream_creation_timestamp is not None:
        kwargs["StreamCreationTimestamp"] = stream_creation_timestamp
    if shard_filter is not None:
        kwargs["ShardFilter"] = shard_filter
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("ListShards", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list shards") from exc
    return ListShardsResult(
        shards=resp.get("Shards"),
        next_token=resp.get("NextToken"),
    )


async def list_stream_consumers(
    stream_arn: str,
    *,
    next_token: str | None = None,
    max_results: int | None = None,
    stream_creation_timestamp: str | None = None,
    region_name: str | None = None,
) -> ListStreamConsumersResult:
    """List stream consumers.

    Args:
        stream_arn: Stream arn.
        next_token: Next token.
        max_results: Max results.
        stream_creation_timestamp: Stream creation timestamp.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamARN"] = stream_arn
    if next_token is not None:
        kwargs["NextToken"] = next_token
    if max_results is not None:
        kwargs["MaxResults"] = max_results
    if stream_creation_timestamp is not None:
        kwargs["StreamCreationTimestamp"] = stream_creation_timestamp
    try:
        resp = await client.call("ListStreamConsumers", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list stream consumers") from exc
    return ListStreamConsumersResult(
        consumers=resp.get("Consumers"),
        next_token=resp.get("NextToken"),
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
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    try:
        resp = await client.call("ListTagsForResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for resource") from exc
    return ListTagsForResourceResult(
        tags=resp.get("Tags"),
    )


async def list_tags_for_stream(
    *,
    stream_name: str | None = None,
    exclusive_start_tag_key: str | None = None,
    limit: int | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> ListTagsForStreamResult:
    """List tags for stream.

    Args:
        stream_name: Stream name.
        exclusive_start_tag_key: Exclusive start tag key.
        limit: Limit.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if exclusive_start_tag_key is not None:
        kwargs["ExclusiveStartTagKey"] = exclusive_start_tag_key
    if limit is not None:
        kwargs["Limit"] = limit
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("ListTagsForStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for stream") from exc
    return ListTagsForStreamResult(
        tags=resp.get("Tags"),
        has_more_tags=resp.get("HasMoreTags"),
    )


async def merge_shards(
    shard_to_merge: str,
    adjacent_shard_to_merge: str,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Merge shards.

    Args:
        shard_to_merge: Shard to merge.
        adjacent_shard_to_merge: Adjacent shard to merge.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ShardToMerge"] = shard_to_merge
    kwargs["AdjacentShardToMerge"] = adjacent_shard_to_merge
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("MergeShards", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to merge shards") from exc
    return None


async def put_resource_policy(
    resource_arn: str,
    policy: str,
    region_name: str | None = None,
) -> None:
    """Put resource policy.

    Args:
        resource_arn: Resource arn.
        policy: Policy.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ResourceARN"] = resource_arn
    kwargs["Policy"] = policy
    try:
        await client.call("PutResourcePolicy", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to put resource policy") from exc
    return None


async def register_stream_consumer(
    stream_arn: str,
    consumer_name: str,
    *,
    tags: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> RegisterStreamConsumerResult:
    """Register stream consumer.

    Args:
        stream_arn: Stream arn.
        consumer_name: Consumer name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamARN"] = stream_arn
    kwargs["ConsumerName"] = consumer_name
    if tags is not None:
        kwargs["Tags"] = tags
    try:
        resp = await client.call("RegisterStreamConsumer", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to register stream consumer") from exc
    return RegisterStreamConsumerResult(
        consumer=resp.get("Consumer"),
    )


async def remove_tags_from_stream(
    tag_keys: list[str],
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Remove tags from stream.

    Args:
        tag_keys: Tag keys.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TagKeys"] = tag_keys
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("RemoveTagsFromStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to remove tags from stream") from exc
    return None


async def split_shard(
    shard_to_split: str,
    new_starting_hash_key: str,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Split shard.

    Args:
        shard_to_split: Shard to split.
        new_starting_hash_key: New starting hash key.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ShardToSplit"] = shard_to_split
    kwargs["NewStartingHashKey"] = new_starting_hash_key
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("SplitShard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to split shard") from exc
    return None


async def start_stream_encryption(
    encryption_type: str,
    key_id: str,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Start stream encryption.

    Args:
        encryption_type: Encryption type.
        key_id: Key id.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EncryptionType"] = encryption_type
    kwargs["KeyId"] = key_id
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("StartStreamEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start stream encryption") from exc
    return None


async def stop_stream_encryption(
    encryption_type: str,
    key_id: str,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Stop stream encryption.

    Args:
        encryption_type: Encryption type.
        key_id: Key id.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["EncryptionType"] = encryption_type
    kwargs["KeyId"] = key_id
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("StopStreamEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop stream encryption") from exc
    return None


async def subscribe_to_shard(
    consumer_arn: str,
    shard_id: str,
    starting_position: dict[str, Any],
    region_name: str | None = None,
) -> SubscribeToShardResult:
    """Subscribe to shard.

    Args:
        consumer_arn: Consumer arn.
        shard_id: Shard id.
        starting_position: Starting position.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["ConsumerARN"] = consumer_arn
    kwargs["ShardId"] = shard_id
    kwargs["StartingPosition"] = starting_position
    try:
        resp = await client.call("SubscribeToShard", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to subscribe to shard") from exc
    return SubscribeToShardResult(
        event_stream=resp.get("EventStream"),
    )


async def tag_resource(
    tags: dict[str, Any],
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Tag resource.

    Args:
        tags: Tags.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["Tags"] = tags
    kwargs["ResourceARN"] = resource_arn
    try:
        await client.call("TagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag resource") from exc
    return None


async def untag_resource(
    tag_keys: list[str],
    resource_arn: str,
    region_name: str | None = None,
) -> None:
    """Untag resource.

    Args:
        tag_keys: Tag keys.
        resource_arn: Resource arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TagKeys"] = tag_keys
    kwargs["ResourceARN"] = resource_arn
    try:
        await client.call("UntagResource", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag resource") from exc
    return None


async def update_account_settings(
    minimum_throughput_billing_commitment: dict[str, Any],
    region_name: str | None = None,
) -> UpdateAccountSettingsResult:
    """Update account settings.

    Args:
        minimum_throughput_billing_commitment: Minimum throughput billing commitment.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MinimumThroughputBillingCommitment"] = minimum_throughput_billing_commitment
    try:
        resp = await client.call("UpdateAccountSettings", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update account settings") from exc
    return UpdateAccountSettingsResult(
        minimum_throughput_billing_commitment=resp.get("MinimumThroughputBillingCommitment"),
    )


async def update_max_record_size(
    max_record_size_in_ki_b: int,
    *,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> None:
    """Update max record size.

    Args:
        max_record_size_in_ki_b: Max record size in ki b.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["MaxRecordSizeInKiB"] = max_record_size_in_ki_b
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        await client.call("UpdateMaxRecordSize", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update max record size") from exc
    return None


async def update_shard_count(
    target_shard_count: int,
    scaling_type: str,
    *,
    stream_name: str | None = None,
    stream_arn: str | None = None,
    region_name: str | None = None,
) -> UpdateShardCountResult:
    """Update shard count.

    Args:
        target_shard_count: Target shard count.
        scaling_type: Scaling type.
        stream_name: Stream name.
        stream_arn: Stream arn.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["TargetShardCount"] = target_shard_count
    kwargs["ScalingType"] = scaling_type
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    try:
        resp = await client.call("UpdateShardCount", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update shard count") from exc
    return UpdateShardCountResult(
        stream_name=resp.get("StreamName"),
        current_shard_count=resp.get("CurrentShardCount"),
        target_shard_count=resp.get("TargetShardCount"),
        stream_arn=resp.get("StreamARN"),
    )


async def update_stream_mode(
    stream_arn: str,
    stream_mode_details: dict[str, Any],
    *,
    warm_throughput_mi_bps: int | None = None,
    region_name: str | None = None,
) -> None:
    """Update stream mode.

    Args:
        stream_arn: Stream arn.
        stream_mode_details: Stream mode details.
        warm_throughput_mi_bps: Warm throughput mi bps.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["StreamARN"] = stream_arn
    kwargs["StreamModeDetails"] = stream_mode_details
    if warm_throughput_mi_bps is not None:
        kwargs["WarmThroughputMiBps"] = warm_throughput_mi_bps
    try:
        await client.call("UpdateStreamMode", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update stream mode") from exc
    return None


async def update_stream_warm_throughput(
    warm_throughput_mi_bps: int,
    *,
    stream_arn: str | None = None,
    stream_name: str | None = None,
    region_name: str | None = None,
) -> UpdateStreamWarmThroughputResult:
    """Update stream warm throughput.

    Args:
        warm_throughput_mi_bps: Warm throughput mi bps.
        stream_arn: Stream arn.
        stream_name: Stream name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("kinesis", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["WarmThroughputMiBps"] = warm_throughput_mi_bps
    if stream_arn is not None:
        kwargs["StreamARN"] = stream_arn
    if stream_name is not None:
        kwargs["StreamName"] = stream_name
    try:
        resp = await client.call("UpdateStreamWarmThroughput", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update stream warm throughput") from exc
    return UpdateStreamWarmThroughputResult(
        stream_arn=resp.get("StreamARN"),
        stream_name=resp.get("StreamName"),
        warm_throughput=resp.get("WarmThroughput"),
    )
