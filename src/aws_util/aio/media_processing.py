"""Native async Media Processing — real non-blocking I/O via :mod:`aws_util.aio._engine`.

Async counterpart to :mod:`aws_util.media_processing`.  All models are re-exported
from the sync module.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

from aws_util.aio._engine import async_client
from aws_util.exceptions import wrap_aws_error
from aws_util.media_processing import (
    MediaConvertResult,
    StreamArchiveResult,
)

logger = logging.getLogger(__name__)

__all__ = [
    "MediaConvertResult",
    "StreamArchiveResult",
    "ivs_stream_recording_archiver",
    "mediaconvert_job_orchestrator",
]

_MEDIACONVERT_POLL_INTERVAL = 10.0  # seconds
_MEDIACONVERT_MAX_ITERATIONS = 60


# ---------------------------------------------------------------------------
# 1. ivs_stream_recording_archiver
# ---------------------------------------------------------------------------


async def ivs_stream_recording_archiver(
    channel_arn: str,
    source_bucket: str,
    archive_bucket: str,
    archive_prefix: str,
    table_name: str,
    region_name: str | None = None,
) -> StreamArchiveResult:
    """Archive completed IVS stream recordings to S3 and record in DynamoDB (async).

    Args:
        channel_arn: ARN of the IVS channel whose sessions to archive.
        source_bucket: S3 bucket where IVS wrote the original recordings.
        archive_bucket: Destination S3 bucket for archived recordings.
        archive_prefix: Key prefix under which to store archived objects.
        table_name: DynamoDB table name to record archive metadata.
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`StreamArchiveResult` with counts and list of archive S3 keys.

    Raises:
        AwsUtilError: If IVS session listing fails.
    """
    ivs = async_client("ivs", region_name)
    s3 = async_client("s3", region_name)
    dynamodb = async_client("dynamodb", region_name)

    recordings_archived = 0
    archive_keys: list[str] = []

    try:
        sessions_resp = await ivs.call("ListStreamSessions", channelArn=channel_arn)
        sessions = sessions_resp.get("streamSessions", [])
    except RuntimeError as exc:
        raise wrap_aws_error(exc, f"ivs.list_stream_sessions(channelArn={channel_arn!r})") from exc

    channel_id = channel_arn.split("/")[-1]

    for session in sessions:
        stream_id = session.get("streamId", "")
        if not stream_id:
            continue

        try:
            detail_resp = await ivs.call(
                "GetStreamSession", channelArn=channel_arn, streamId=stream_id
            )
            detail_resp.get("streamSession", {})
        except RuntimeError as exc:
            logger.warning("Could not get session detail for %s: %s", stream_id, exc)
            continue

        recording_prefix = f"{channel_id}/{stream_id}/"

        try:
            list_resp = await s3.call(
                "ListObjectsV2", Bucket=source_bucket, Prefix=recording_prefix
            )
            objects = list_resp.get("Contents", [])
        except RuntimeError as exc:
            logger.warning("Could not list recording objects for session %s: %s", stream_id, exc)
            continue

        if not objects:
            logger.debug("No recording objects found for session %s", stream_id)
            continue

        session_keys: list[str] = []
        session_size = 0

        for obj in objects:
            src_key = obj["Key"]
            obj_size = obj.get("Size", 0)
            relative = src_key[len(recording_prefix) :]
            dest_key = f"{archive_prefix.rstrip('/')}/{stream_id}/{relative}"

            try:
                await s3.call(
                    "CopyObject",
                    CopySource=f"{source_bucket}/{src_key}",
                    Bucket=archive_bucket,
                    Key=dest_key,
                )
                session_keys.append(dest_key)
                session_size += obj_size
            except RuntimeError as exc:
                logger.warning("Failed to copy %s -> %s: %s", src_key, dest_key, exc)
                continue

        if not session_keys:
            continue

        archive_keys.extend(session_keys)

        try:
            await dynamodb.call(
                "PutItem",
                TableName=table_name,
                Item={
                    "StreamId": {"S": stream_id},
                    "ChannelArn": {"S": channel_arn},
                    "SourceBucket": {"S": source_bucket},
                    "ArchiveBucket": {"S": archive_bucket},
                    "ArchivePrefix": {"S": f"{archive_prefix.rstrip('/')}/{stream_id}/"},
                    "ObjectCount": {"N": str(len(session_keys))},
                    "SizeBytes": {"N": str(session_size)},
                    "ArchivedAt": {"N": str(int(time.time()))},
                },
            )
        except RuntimeError as exc:
            logger.warning("Failed to record archive metadata for session %s: %s", stream_id, exc)

        recordings_archived += 1

    return StreamArchiveResult(
        recordings_archived=recordings_archived,
        archive_keys=archive_keys,
    )


# ---------------------------------------------------------------------------
# 2. mediaconvert_job_orchestrator
# ---------------------------------------------------------------------------


async def mediaconvert_job_orchestrator(
    input_s3_uri: str,
    output_s3_uri: str,
    role_arn: str,
    table_name: str,
    sns_topic_arn: str | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> MediaConvertResult:
    """Submit a MediaConvert job, poll for completion, store results, notify via SNS (async).

    Args:
        input_s3_uri: S3 URI of the source media file (``s3://bucket/key``).
        output_s3_uri: S3 URI prefix for transcoded outputs.
        role_arn: IAM role ARN that MediaConvert assumes to read/write S3.
        table_name: DynamoDB table name to store job result metadata.
        sns_topic_arn: Optional SNS topic ARN for completion notification.
        settings: Optional dict of codec/container settings to override defaults.
        region_name: AWS region. ``None`` uses the default region.

    Returns:
        :class:`MediaConvertResult` with job ID, status, output URI, and duration in seconds.

    Raises:
        AwsUtilError: If endpoint discovery or job creation fails, or job times out.
    """
    import boto3

    mediaconvert_base = async_client("mediaconvert", region_name)
    dynamodb = async_client("dynamodb", region_name)
    sns = async_client("sns", region_name) if sns_topic_arn else None

    # Discover MediaConvert endpoint
    try:
        ep_resp = await mediaconvert_base.call("DescribeEndpoints", Mode="DEFAULT")
        endpoints = ep_resp.get("Endpoints", [])
        endpoint_url = endpoints[0]["Url"] if endpoints else None
    except RuntimeError as exc:
        raise wrap_aws_error(exc, "mediaconvert.describe_endpoints") from exc

    if not endpoint_url:
        raise wrap_aws_error(
            RuntimeError("No MediaConvert endpoint found"),
            "mediaconvert_job_orchestrator",
        )

    # MediaConvert endpoint-specific client requires a custom URL — use sync client in thread
    mc_sync = boto3.client(
        "mediaconvert",
        region_name=region_name,
        endpoint_url=endpoint_url,
    )

    # Build job settings
    codec_settings: dict[str, Any] = {
        "Codec": "H_264",
        "H264Settings": {
            "RateControlMode": "QVBR",
            "MaxBitrate": 5_000_000,
        },
    }
    audio_settings: dict[str, Any] = {
        "Codec": "AAC",
        "AacSettings": {
            "Bitrate": 96_000,
            "CodingMode": "CODING_MODE_2_0",
            "SampleRate": 48_000,
        },
    }
    container = "MP4"

    if settings:
        if "VideoCodecSettings" in settings:
            codec_settings = settings["VideoCodecSettings"]
        if "AudioCodecSettings" in settings:
            audio_settings = settings["AudioCodecSettings"]
        if "Container" in settings:
            container = settings["Container"]

    job_settings: dict[str, Any] = {
        "Inputs": [
            {
                "FileInput": input_s3_uri,
                "AudioSelectors": {"Audio Selector 1": {"DefaultSelection": "DEFAULT"}},
                "VideoSelector": {},
                "TimecodeSource": "ZEROBASED",
            }
        ],
        "OutputGroups": [
            {
                "Name": "File Group",
                "OutputGroupSettings": {
                    "Type": "FILE_GROUP_SETTINGS",
                    "FileGroupSettings": {"Destination": output_s3_uri},
                },
                "Outputs": [
                    {
                        "ContainerSettings": {"Container": container},
                        "VideoDescription": {"CodecSettings": codec_settings},
                        "AudioDescriptions": [{"CodecSettings": audio_settings}],
                    }
                ],
            }
        ],
        "TimecodeConfig": {"Source": "ZEROBASED"},
    }

    start_time = time.monotonic()

    try:
        create_resp = await asyncio.to_thread(
            mc_sync.create_job, Role=role_arn, Settings=job_settings
        )
        job = create_resp.get("Job", {})
        job_id = job.get("Id", "")
    except Exception as exc:
        raise wrap_aws_error(exc, "mediaconvert.create_job") from exc  # type: ignore[arg-type]

    logger.info("MediaConvert job %s created — polling for completion", job_id)

    status = "SUBMITTED"
    output_uri = output_s3_uri

    for _ in range(_MEDIACONVERT_MAX_ITERATIONS):
        try:
            get_resp = await asyncio.to_thread(mc_sync.describe_job, Id=job_id)
            job = get_resp.get("Job", {})
            status = job.get("Status", "UNKNOWN")
        except Exception as exc:
            raise wrap_aws_error(exc, f"mediaconvert.describe_job({job_id!r})") from exc  # type: ignore[arg-type]

        if status in ("COMPLETE", "ERROR", "CANCELED"):
            break

        logger.debug(
            "MediaConvert job %s status: %s — waiting %.0fs",
            job_id,
            status,
            _MEDIACONVERT_POLL_INTERVAL,
        )
        await asyncio.sleep(_MEDIACONVERT_POLL_INTERVAL)
    else:
        raise wrap_aws_error(
            TimeoutError(
                f"MediaConvert job {job_id!r} did not complete within {_MEDIACONVERT_MAX_ITERATIONS * _MEDIACONVERT_POLL_INTERVAL}s"
            ),
            "mediaconvert_job_orchestrator",
        )

    duration_seconds = time.monotonic() - start_time

    # Write to DynamoDB
    try:
        await dynamodb.call(
            "PutItem",
            TableName=table_name,
            Item={
                "JobId": {"S": job_id},
                "Status": {"S": status},
                "InputUri": {"S": input_s3_uri},
                "OutputUri": {"S": output_uri},
                "RoleArn": {"S": role_arn},
                "DurationSeconds": {"N": str(round(duration_seconds, 3))},
                "CompletedAt": {"N": str(int(time.time()))},
            },
        )
    except RuntimeError as exc:
        logger.warning("Failed to write MediaConvert result to DynamoDB: %s", exc)

    # Notify via SNS
    if sns_topic_arn and sns:
        try:
            await sns.call(
                "Publish",
                TopicArn=sns_topic_arn,
                Subject=f"MediaConvert Job {status}: {job_id}",
                Message=json.dumps(
                    {
                        "job_id": job_id,
                        "status": status,
                        "input_uri": input_s3_uri,
                        "output_uri": output_uri,
                        "duration_seconds": duration_seconds,
                    }
                ),
            )
        except RuntimeError as exc:
            logger.warning("Failed to publish SNS notification: %s", exc)

    return MediaConvertResult(
        job_id=job_id,
        status=status,
        output_uri=output_uri,
        duration_seconds=duration_seconds,
    )
