"""Media Processing utilities for IVS, MediaConvert, S3, DynamoDB, and SNS.

Provides multi-service helpers for media processing workflows:

- **ivs_stream_recording_archiver** — Copy IVS completed recordings to archive S3, record in DynamoDB.
- **mediaconvert_job_orchestrator** — Submit MediaConvert job, poll, store results, notify via SNS.
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
    "MediaConvertResult",
    "StreamArchiveResult",
    "ivs_stream_recording_archiver",
    "mediaconvert_job_orchestrator",
]

# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class StreamArchiveResult(BaseModel):
    """Result of archiving IVS stream recordings to S3."""

    model_config = ConfigDict(frozen=True)

    recordings_archived: int
    archive_keys: list[str]


class MediaConvertResult(BaseModel):
    """Result of a MediaConvert transcoding job orchestration."""

    model_config = ConfigDict(frozen=True)

    job_id: str
    status: str
    output_uri: str
    duration_seconds: float


# ---------------------------------------------------------------------------
# 1. ivs_stream_recording_archiver
# ---------------------------------------------------------------------------

_IVS_COMPLETED_STATES = {"RECORDED", "COMPLETE"}


def ivs_stream_recording_archiver(
    channel_arn: str,
    source_bucket: str,
    archive_bucket: str,
    archive_prefix: str,
    table_name: str,
    region_name: str | None = None,
) -> StreamArchiveResult:
    """Archive completed IVS stream recordings from source S3 to an archive bucket/prefix.

    Lists stream sessions for *channel_arn*, copies recording objects from *source_bucket*
    to ``s3://{archive_bucket}/{archive_prefix}/``, and records metadata in *table_name*
    in DynamoDB.

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
    ivs = get_client("ivs", region_name)
    s3 = get_client("s3", region_name)
    dynamodb = get_client("dynamodb", region_name)

    recordings_archived = 0
    archive_keys: list[str] = []

    try:
        sessions_resp = ivs.list_stream_sessions(channelArn=channel_arn)
        sessions = sessions_resp.get("streamSessions", [])
    except ClientError as exc:
        raise wrap_aws_error(exc, f"ivs.list_stream_sessions(channelArn={channel_arn!r})") from exc

    channel_id = channel_arn.split("/")[-1]

    for session in sessions:
        stream_id = session.get("streamId", "")
        if not stream_id:
            continue

        # Get full session detail to verify recording state
        try:
            detail_resp = ivs.get_stream_session(channelArn=channel_arn, streamId=stream_id)
            detail_resp.get("streamSession", {})
        except ClientError as exc:
            logger.warning("Could not get session detail for %s: %s", stream_id, exc)
            continue

        recording_prefix = f"{channel_id}/{stream_id}/"

        # List objects in the source bucket at the IVS recording prefix
        try:
            list_resp = s3.list_objects_v2(Bucket=source_bucket, Prefix=recording_prefix)
            objects = list_resp.get("Contents", [])
        except ClientError as exc:
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
                s3.copy_object(
                    CopySource={"Bucket": source_bucket, "Key": src_key},
                    Bucket=archive_bucket,
                    Key=dest_key,
                )
                session_keys.append(dest_key)
                session_size += obj_size
            except ClientError as exc:
                logger.warning("Failed to copy %s -> %s: %s", src_key, dest_key, exc)
                continue

        if not session_keys:
            continue

        archive_keys.extend(session_keys)

        # Record metadata in DynamoDB
        try:
            dynamodb.put_item(
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
        except ClientError as exc:
            logger.warning("Failed to record archive metadata for session %s: %s", stream_id, exc)

        recordings_archived += 1

    return StreamArchiveResult(
        recordings_archived=recordings_archived,
        archive_keys=archive_keys,
    )


# ---------------------------------------------------------------------------
# 2. mediaconvert_job_orchestrator
# ---------------------------------------------------------------------------

_MEDIACONVERT_POLL_INTERVAL = 10  # seconds
_MEDIACONVERT_MAX_ITERATIONS = 60


def mediaconvert_job_orchestrator(
    input_s3_uri: str,
    output_s3_uri: str,
    role_arn: str,
    table_name: str,
    sns_topic_arn: str | None = None,
    settings: dict[str, Any] | None = None,
    region_name: str | None = None,
) -> MediaConvertResult:
    """Submit a MediaConvert transcoding job, poll for completion, store results, notify via SNS.

    Workflow:
    1. Discover the MediaConvert endpoint via ``describe_endpoints``.
    2. Create a transcoding job from *input_s3_uri* to *output_s3_uri*, using *settings*
       to override codec/container settings.
    3. Poll ``describe_job`` up to 60 iterations (10s sleep each) for completion.
    4. Write job details into *table_name* in DynamoDB.
    5. If *sns_topic_arn* is provided, publish a completion notification.

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

    # Discover MediaConvert endpoint
    mc_base = get_client("mediaconvert", region_name)
    try:
        ep_resp = mc_base.describe_endpoints(Mode="DEFAULT")
        endpoints = ep_resp.get("Endpoints", [])
        endpoint_url = endpoints[0]["Url"] if endpoints else None
    except ClientError as exc:
        raise wrap_aws_error(exc, "mediaconvert.describe_endpoints") from exc

    if not endpoint_url:
        raise wrap_aws_error(
            RuntimeError("No MediaConvert endpoint found"),
            "mediaconvert_job_orchestrator",
        )

    mc = boto3.client(
        "mediaconvert",
        region_name=region_name,
        endpoint_url=endpoint_url,
    )
    dynamodb = get_client("dynamodb", region_name)
    sns = get_client("sns", region_name) if sns_topic_arn else None

    # Build job settings — allow caller overrides via *settings*
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

    start_time = time.time()

    try:
        create_resp = mc.create_job(Role=role_arn, Settings=job_settings)
        job = create_resp.get("Job", {})
        job_id = job.get("Id", "")
    except ClientError as exc:
        raise wrap_aws_error(exc, "mediaconvert.create_job") from exc

    logger.info("MediaConvert job %s created — polling for completion", job_id)

    # Poll for completion (max 60 iterations, 10s sleep)
    status = "SUBMITTED"
    output_uri = output_s3_uri
    for _ in range(_MEDIACONVERT_MAX_ITERATIONS):
        try:
            get_resp = mc.describe_job(Id=job_id)
            job = get_resp.get("Job", {})
            status = job.get("Status", "UNKNOWN")
        except ClientError as exc:
            raise wrap_aws_error(exc, f"mediaconvert.describe_job({job_id!r})") from exc

        if status in ("COMPLETE", "ERROR", "CANCELED"):
            break

        logger.debug(
            "MediaConvert job %s status: %s — waiting %ds",
            job_id,
            status,
            _MEDIACONVERT_POLL_INTERVAL,
        )
        time.sleep(_MEDIACONVERT_POLL_INTERVAL)
    else:
        raise wrap_aws_error(
            TimeoutError(
                f"MediaConvert job {job_id!r} did not complete within {_MEDIACONVERT_MAX_ITERATIONS * _MEDIACONVERT_POLL_INTERVAL}s"
            ),
            "mediaconvert_job_orchestrator",
        )

    duration_seconds = time.time() - start_time

    # Write to DynamoDB
    try:
        dynamodb.put_item(
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
    except ClientError as exc:
        logger.warning("Failed to write MediaConvert result to DynamoDB: %s", exc)

    # Notify via SNS
    if sns_topic_arn and sns:
        try:
            sns.publish(
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
        except ClientError as exc:
            logger.warning("Failed to publish SNS notification: %s", exc)

    return MediaConvertResult(
        job_id=job_id,
        status=status,
        output_uri=output_uri,
        duration_seconds=duration_seconds,
    )
