"""Native async Firehose utilities using the async engine."""

from __future__ import annotations

import json
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import AwsServiceError, wrap_aws_error
from aws_util.firehose import (
    CreateDeliveryStreamResult,
    DeliveryStream,
    FirehosePutResult,
    ListTagsForDeliveryStreamResult,
)

__all__ = [
    "CreateDeliveryStreamResult",
    "DeliveryStream",
    "FirehosePutResult",
    "ListTagsForDeliveryStreamResult",
    "create_delivery_stream",
    "delete_delivery_stream",
    "describe_delivery_stream",
    "list_delivery_streams",
    "list_tags_for_delivery_stream",
    "put_record",
    "put_record_batch",
    "put_record_batch_with_retry",
    "start_delivery_stream_encryption",
    "stop_delivery_stream_encryption",
    "tag_delivery_stream",
    "untag_delivery_stream",
    "update_destination",
]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _encode(data: bytes | str | dict | list) -> bytes:
    """Encode a record payload to bytes with trailing newline."""
    if isinstance(data, bytes):
        return data
    if isinstance(data, (dict, list)):
        return (json.dumps(data) + "\n").encode("utf-8")
    text = data if data.endswith("\n") else data + "\n"
    return text.encode("utf-8")


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


async def put_record(
    delivery_stream_name: str,
    data: bytes | str | dict | list,
    region_name: str | None = None,
) -> str:
    """Send a single record to a Kinesis Firehose delivery stream.

    Dicts and lists are JSON-encoded automatically.  A newline is appended for
    text-based destinations (S3, Elasticsearch) so records are line-delimited.

    Args:
        delivery_stream_name: Name of the delivery stream.
        data: Record payload.
        region_name: AWS region override.

    Returns:
        The assigned record ID.

    Raises:
        RuntimeError: If the put fails.
    """
    client = async_client("firehose", region_name)
    raw = _encode(data)
    try:
        resp = await client.call(
            "PutRecord",
            DeliveryStreamName=delivery_stream_name,
            Record={"Data": raw},
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"put_record failed on delivery stream {delivery_stream_name!r}"
        ) from exc
    return resp["RecordId"]


async def put_record_batch(
    delivery_stream_name: str,
    records: list[bytes | str | dict | list],
    region_name: str | None = None,
) -> FirehosePutResult:
    """Send up to 500 records to a Firehose delivery stream in one request.

    Args:
        delivery_stream_name: Name of the delivery stream.
        records: List of payloads (up to 500, max 4 MB total).
        region_name: AWS region override.

    Returns:
        A :class:`FirehosePutResult` describing successes and failures.

    Raises:
        RuntimeError: If the API call fails.
        ValueError: If more than 500 records are supplied.
    """
    if len(records) > 500:
        raise ValueError("put_record_batch supports at most 500 records per call")

    client = async_client("firehose", region_name)
    entries = [{"Data": _encode(r)} for r in records]
    try:
        resp = await client.call(
            "PutRecordBatch",
            DeliveryStreamName=delivery_stream_name,
            Records=entries,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"put_record_batch failed on {delivery_stream_name!r}") from exc
    return FirehosePutResult(
        failed_put_count=resp.get("FailedPutCount", 0),
        request_responses=resp.get("RequestResponses", []),
    )


async def list_delivery_streams(
    delivery_stream_type: str | None = None,
    region_name: str | None = None,
) -> list[str]:
    """List Kinesis Firehose delivery stream names in the account.

    Args:
        delivery_stream_type: Optional filter -- ``"DirectPut"``,
            ``"KinesisStreamAsSource"``, or ``"MSKAsSource"``.
        region_name: AWS region override.

    Returns:
        A list of delivery stream names.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    names: list[str] = []
    kwargs: dict[str, Any] = {}
    if delivery_stream_type:
        kwargs["DeliveryStreamType"] = delivery_stream_type
    try:
        while True:
            resp = await client.call("ListDeliveryStreams", Limit=100, **kwargs)
            names.extend(resp.get("DeliveryStreamNames", []))
            if not resp.get("HasMoreDeliveryStreams"):
                break
            kwargs["ExclusiveStartDeliveryStreamName"] = names[-1]
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "list_delivery_streams failed") from exc
    return names


async def describe_delivery_stream(
    delivery_stream_name: str,
    region_name: str | None = None,
) -> DeliveryStream:
    """Describe a Kinesis Firehose delivery stream.

    Args:
        delivery_stream_name: Name of the delivery stream.
        region_name: AWS region override.

    Returns:
        A :class:`DeliveryStream` with current metadata.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    try:
        resp = await client.call(
            "DescribeDeliveryStream",
            DeliveryStreamName=delivery_stream_name,
        )
    except RuntimeError as exc:
        raise wrap_aws_error(
            exc, f"describe_delivery_stream failed for {delivery_stream_name!r}"
        ) from exc
    desc = resp["DeliveryStreamDescription"]
    return DeliveryStream(
        delivery_stream_name=desc["DeliveryStreamName"],
        delivery_stream_arn=desc["DeliveryStreamARN"],
        delivery_stream_status=desc["DeliveryStreamStatus"],
        delivery_stream_type=desc["DeliveryStreamType"],
        create_timestamp=(
            str(desc.get("CreateTimestamp")) if desc.get("CreateTimestamp") else None
        ),
    )


# ---------------------------------------------------------------------------
# Complex utilities
# ---------------------------------------------------------------------------


async def put_record_batch_with_retry(
    delivery_stream_name: str,
    records: list[bytes | str | dict | list],
    max_retries: int = 3,
    region_name: str | None = None,
) -> int:
    """Send records to Firehose, automatically retrying any that fail.

    Calls :func:`put_record_batch` and re-submits only the records that were
    rejected, up to *max_retries* times.

    Args:
        delivery_stream_name: Name of the delivery stream.
        records: Record payloads (up to 500 per call, split automatically).
        max_retries: Maximum retry attempts for failed records (default ``3``).
        region_name: AWS region override.

    Returns:
        Total number of records successfully delivered.

    Raises:
        RuntimeError: If records still fail after all retries.
    """
    total_delivered = 0
    for chunk_start in range(0, len(records), 500):
        chunk = records[chunk_start : chunk_start + 500]
        pending = list(chunk)
        attempt = 0
        while pending and attempt <= max_retries:
            result = await put_record_batch(
                delivery_stream_name,
                pending,
                region_name=region_name,
            )
            if result.all_succeeded:
                total_delivered += len(pending)
                pending = []
                break
            # Re-queue only the failed records
            failed: list[bytes | str | dict | list] = []
            for i, response in enumerate(result.request_responses):
                if response.get("ErrorCode"):
                    failed.append(pending[i])
                else:
                    total_delivered += 1
            pending = failed
            attempt += 1

        if pending:
            raise AwsServiceError(
                f"put_record_batch_with_retry: {len(pending)} record(s) "
                f"still failing after {max_retries} retries on stream "
                f"{delivery_stream_name!r}"
            )
    return total_delivered


async def create_delivery_stream(
    delivery_stream_name: str,
    *,
    delivery_stream_type: str | None = None,
    direct_put_source_configuration: dict[str, Any] | None = None,
    kinesis_stream_source_configuration: dict[str, Any] | None = None,
    delivery_stream_encryption_configuration_input: dict[str, Any] | None = None,
    s3_destination_configuration: dict[str, Any] | None = None,
    extended_s3_destination_configuration: dict[str, Any] | None = None,
    redshift_destination_configuration: dict[str, Any] | None = None,
    elasticsearch_destination_configuration: dict[str, Any] | None = None,
    amazonopensearchservice_destination_configuration: dict[str, Any] | None = None,
    splunk_destination_configuration: dict[str, Any] | None = None,
    http_endpoint_destination_configuration: dict[str, Any] | None = None,
    tags: list[dict[str, Any]] | None = None,
    amazon_open_search_serverless_destination_configuration: dict[str, Any] | None = None,
    msk_source_configuration: dict[str, Any] | None = None,
    snowflake_destination_configuration: dict[str, Any] | None = None,
    iceberg_destination_configuration: dict[str, Any] | None = None,
    database_source_configuration: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> CreateDeliveryStreamResult:
    """Create delivery stream.

    Args:
        delivery_stream_name: Delivery stream name.
        delivery_stream_type: Delivery stream type.
        direct_put_source_configuration: Direct put source configuration.
        kinesis_stream_source_configuration: Kinesis stream source configuration.
        delivery_stream_encryption_configuration_input: Delivery stream encryption configuration input.
        s3_destination_configuration: S3 destination configuration.
        extended_s3_destination_configuration: Extended s3 destination configuration.
        redshift_destination_configuration: Redshift destination configuration.
        elasticsearch_destination_configuration: Elasticsearch destination configuration.
        amazonopensearchservice_destination_configuration: Amazonopensearchservice destination configuration.
        splunk_destination_configuration: Splunk destination configuration.
        http_endpoint_destination_configuration: Http endpoint destination configuration.
        tags: Tags.
        amazon_open_search_serverless_destination_configuration: Amazon open search serverless destination configuration.
        msk_source_configuration: Msk source configuration.
        snowflake_destination_configuration: Snowflake destination configuration.
        iceberg_destination_configuration: Iceberg destination configuration.
        database_source_configuration: Database source configuration.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    if delivery_stream_type is not None:
        kwargs["DeliveryStreamType"] = delivery_stream_type
    if direct_put_source_configuration is not None:
        kwargs["DirectPutSourceConfiguration"] = direct_put_source_configuration
    if kinesis_stream_source_configuration is not None:
        kwargs["KinesisStreamSourceConfiguration"] = kinesis_stream_source_configuration
    if delivery_stream_encryption_configuration_input is not None:
        kwargs["DeliveryStreamEncryptionConfigurationInput"] = (
            delivery_stream_encryption_configuration_input
        )
    if s3_destination_configuration is not None:
        kwargs["S3DestinationConfiguration"] = s3_destination_configuration
    if extended_s3_destination_configuration is not None:
        kwargs["ExtendedS3DestinationConfiguration"] = extended_s3_destination_configuration
    if redshift_destination_configuration is not None:
        kwargs["RedshiftDestinationConfiguration"] = redshift_destination_configuration
    if elasticsearch_destination_configuration is not None:
        kwargs["ElasticsearchDestinationConfiguration"] = elasticsearch_destination_configuration
    if amazonopensearchservice_destination_configuration is not None:
        kwargs["AmazonopensearchserviceDestinationConfiguration"] = (
            amazonopensearchservice_destination_configuration
        )
    if splunk_destination_configuration is not None:
        kwargs["SplunkDestinationConfiguration"] = splunk_destination_configuration
    if http_endpoint_destination_configuration is not None:
        kwargs["HttpEndpointDestinationConfiguration"] = http_endpoint_destination_configuration
    if tags is not None:
        kwargs["Tags"] = tags
    if amazon_open_search_serverless_destination_configuration is not None:
        kwargs["AmazonOpenSearchServerlessDestinationConfiguration"] = (
            amazon_open_search_serverless_destination_configuration
        )
    if msk_source_configuration is not None:
        kwargs["MSKSourceConfiguration"] = msk_source_configuration
    if snowflake_destination_configuration is not None:
        kwargs["SnowflakeDestinationConfiguration"] = snowflake_destination_configuration
    if iceberg_destination_configuration is not None:
        kwargs["IcebergDestinationConfiguration"] = iceberg_destination_configuration
    if database_source_configuration is not None:
        kwargs["DatabaseSourceConfiguration"] = database_source_configuration
    try:
        resp = await client.call("CreateDeliveryStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to create delivery stream") from exc
    return CreateDeliveryStreamResult(
        delivery_stream_arn=resp.get("DeliveryStreamARN"),
    )


async def delete_delivery_stream(
    delivery_stream_name: str,
    *,
    allow_force_delete: bool | None = None,
    region_name: str | None = None,
) -> None:
    """Delete delivery stream.

    Args:
        delivery_stream_name: Delivery stream name.
        allow_force_delete: Allow force delete.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    if allow_force_delete is not None:
        kwargs["AllowForceDelete"] = allow_force_delete
    try:
        await client.call("DeleteDeliveryStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to delete delivery stream") from exc
    return None


async def list_tags_for_delivery_stream(
    delivery_stream_name: str,
    *,
    exclusive_start_tag_key: str | None = None,
    limit: int | None = None,
    region_name: str | None = None,
) -> ListTagsForDeliveryStreamResult:
    """List tags for delivery stream.

    Args:
        delivery_stream_name: Delivery stream name.
        exclusive_start_tag_key: Exclusive start tag key.
        limit: Limit.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    if exclusive_start_tag_key is not None:
        kwargs["ExclusiveStartTagKey"] = exclusive_start_tag_key
    if limit is not None:
        kwargs["Limit"] = limit
    try:
        resp = await client.call("ListTagsForDeliveryStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to list tags for delivery stream") from exc
    return ListTagsForDeliveryStreamResult(
        tags=resp.get("Tags"),
        has_more_tags=resp.get("HasMoreTags"),
    )


async def start_delivery_stream_encryption(
    delivery_stream_name: str,
    *,
    delivery_stream_encryption_configuration_input: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Start delivery stream encryption.

    Args:
        delivery_stream_name: Delivery stream name.
        delivery_stream_encryption_configuration_input: Delivery stream encryption configuration input.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    if delivery_stream_encryption_configuration_input is not None:
        kwargs["DeliveryStreamEncryptionConfigurationInput"] = (
            delivery_stream_encryption_configuration_input
        )
    try:
        await client.call("StartDeliveryStreamEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to start delivery stream encryption") from exc
    return None


async def stop_delivery_stream_encryption(
    delivery_stream_name: str,
    region_name: str | None = None,
) -> None:
    """Stop delivery stream encryption.

    Args:
        delivery_stream_name: Delivery stream name.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    try:
        await client.call("StopDeliveryStreamEncryption", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to stop delivery stream encryption") from exc
    return None


async def tag_delivery_stream(
    delivery_stream_name: str,
    tags: list[dict[str, Any]],
    region_name: str | None = None,
) -> None:
    """Tag delivery stream.

    Args:
        delivery_stream_name: Delivery stream name.
        tags: Tags.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    kwargs["Tags"] = tags
    try:
        await client.call("TagDeliveryStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to tag delivery stream") from exc
    return None


async def untag_delivery_stream(
    delivery_stream_name: str,
    tag_keys: list[str],
    region_name: str | None = None,
) -> None:
    """Untag delivery stream.

    Args:
        delivery_stream_name: Delivery stream name.
        tag_keys: Tag keys.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    kwargs["TagKeys"] = tag_keys
    try:
        await client.call("UntagDeliveryStream", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to untag delivery stream") from exc
    return None


async def update_destination(
    delivery_stream_name: str,
    current_delivery_stream_version_id: str,
    destination_id: str,
    *,
    s3_destination_update: dict[str, Any] | None = None,
    extended_s3_destination_update: dict[str, Any] | None = None,
    redshift_destination_update: dict[str, Any] | None = None,
    elasticsearch_destination_update: dict[str, Any] | None = None,
    amazonopensearchservice_destination_update: dict[str, Any] | None = None,
    splunk_destination_update: dict[str, Any] | None = None,
    http_endpoint_destination_update: dict[str, Any] | None = None,
    amazon_open_search_serverless_destination_update: dict[str, Any] | None = None,
    snowflake_destination_update: dict[str, Any] | None = None,
    iceberg_destination_update: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> None:
    """Update destination.

    Args:
        delivery_stream_name: Delivery stream name.
        current_delivery_stream_version_id: Current delivery stream version id.
        destination_id: Destination id.
        s3_destination_update: S3 destination update.
        extended_s3_destination_update: Extended s3 destination update.
        redshift_destination_update: Redshift destination update.
        elasticsearch_destination_update: Elasticsearch destination update.
        amazonopensearchservice_destination_update: Amazonopensearchservice destination update.
        splunk_destination_update: Splunk destination update.
        http_endpoint_destination_update: Http endpoint destination update.
        amazon_open_search_serverless_destination_update: Amazon open search serverless destination update.
        snowflake_destination_update: Snowflake destination update.
        iceberg_destination_update: Iceberg destination update.
        region_name: AWS region override.

    Raises:
        RuntimeError: If the API call fails.
    """
    client = async_client("firehose", region_name)
    kwargs: dict[str, Any] = {}
    kwargs["DeliveryStreamName"] = delivery_stream_name
    kwargs["CurrentDeliveryStreamVersionId"] = current_delivery_stream_version_id
    kwargs["DestinationId"] = destination_id
    if s3_destination_update is not None:
        kwargs["S3DestinationUpdate"] = s3_destination_update
    if extended_s3_destination_update is not None:
        kwargs["ExtendedS3DestinationUpdate"] = extended_s3_destination_update
    if redshift_destination_update is not None:
        kwargs["RedshiftDestinationUpdate"] = redshift_destination_update
    if elasticsearch_destination_update is not None:
        kwargs["ElasticsearchDestinationUpdate"] = elasticsearch_destination_update
    if amazonopensearchservice_destination_update is not None:
        kwargs["AmazonopensearchserviceDestinationUpdate"] = (
            amazonopensearchservice_destination_update
        )
    if splunk_destination_update is not None:
        kwargs["SplunkDestinationUpdate"] = splunk_destination_update
    if http_endpoint_destination_update is not None:
        kwargs["HttpEndpointDestinationUpdate"] = http_endpoint_destination_update
    if amazon_open_search_serverless_destination_update is not None:
        kwargs["AmazonOpenSearchServerlessDestinationUpdate"] = (
            amazon_open_search_serverless_destination_update
        )
    if snowflake_destination_update is not None:
        kwargs["SnowflakeDestinationUpdate"] = snowflake_destination_update
    if iceberg_destination_update is not None:
        kwargs["IcebergDestinationUpdate"] = iceberg_destination_update
    try:
        await client.call("UpdateDestination", **kwargs)
    except Exception as exc:
        raise wrap_aws_error(exc, "Failed to update destination") from exc
    return None
